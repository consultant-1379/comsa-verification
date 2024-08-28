#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2007 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained
# herein confidential and shall protect the same in whole or in part
# from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################

'''File information:
   ===================================================


   Author:

   Description:

'''
#############IMPORT##################

import re
from org.apache.log4j import Logger
from java.lang import System
import tg_lib
import time
import decimal
import sys
import os
import string
import datetime
import smtplib
from email.mime.text import MIMEText

import test_env.bin.lib.parameterHandler as ph
import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException


import omp.tf.ssh_lib as ssh_lib
import omp.tf.hw_lib as hw_lib
import omp.tf.ethswitch_lib as ethswitch_lib
import omp.tf.misc_lib as misc_lib
import coremw.notification_lib as notification_lib
import coremw.testapp_lib as testapp_lib
import coremw.saf_lib as saf_lib

#############GLOBALS##################

mostResentDumps = []
# EJNOLSZ: The lines below should be uncommented if we want to use the library broker
#ethswitch_lib = None
#hw_lib = None
#ssh_lib = None
#misc_lib = None
#testapp_lib = None
logger = None
targetData = None
activeController = 1
testCaseConfig = {}
testSuiteConfig = {}
logDir = ''
globalTimeStamp = 0

#############setUp / tearDown#############

def setUp(logLevel, currentSut):
    global ethswitch_lib
    global hw_lib
    global ssh_lib
    global misc_lib
    global testapp_lib
    global logger
    global targetData
    global logDir
    global amfNodeNameSeparator

    logger = Logger.getLogger('lib')
    logger.setLevel(logLevel)
    logger.info("lib: Initiating!")
    logDir = System.getProperty("logdir")
    amfNodeNameSeparator = System.getProperty("amfNodeNameSeparator")
    result = misc_lib.execCommand ('date +"%Y%m%d%H%M%S"')
    time_stamp = string.strip(result[1].split()[0])
    System.setProperty("BuildComsaPath", '/tmp/xtemp_$USER-%s' %time_stamp)
    System.setProperty("IsBuildCOMSA", "False")
#    EJNOLSZ: The lines below should be uncommented if we want to use the library broker
#    ethswitch_lib = currentSut.getLibrary("EthSwitchLib")
#    hw_lib = currentSut.getLibrary("HwLib")
#    ssh_lib = currentSut.getLibrary("SshLib")
#    misc_lib = currentSut.getLibrary("MiscLib")
#    testapp_lib = currentSut.getLibrary("TestAppLib")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    return


def tearDown():
    #logger_lib.logMessage("lib: Bye bye !!", logLevel='debug')
    swDir = System.getProperty("swDirNumber")
    if (swDir == 'undef'):
        response = System.getProperty("BuildComsaPath")
        result = misc_lib.execCommand ('\\rm -rf %s' %response)
    logger.debug("lib: bye, bye!")
    return

#############################################################################################
# lib functions
#############################################################################################

def checkSystemNodes(testConfig):
    '''
    power on node().

    Arguments:
    (dict testConfig)

    Returns:
    list('SUCCESS',[]) or
    list('ERROR', [(<subrack>,<slot>)])
    NOTE:

    Dependencies:
    ssh_lib, target_data

    '''

    logger.info('enter checkSystemNodes')
    result = ['SUCCESS', []]
    for subrack, slot in testConfig['testNodes']:
        response = hw_lib.powerStatus(subrack, slot)
        while re.search('Authentication type NONE not supported',response[1]):
            response = hw_lib.powerStatus(subrack, slot)
        if response[0] == 'SUCCESS' and re.search('off',response[1]):
            logger.info("Checking HW subrack: %d, slot; %d result: %s" % (subrack, slot, response))
            result[1]. append((subrack,slot))
            result[0] = 'ERROR'
    logger.info('leave checkSystemNodes')
    return result



def checkSwitches(testConfig):

    logger.info('enter checkSwitches')
    result = ['SUCCESS', []]
    for idx, s in enumerate(testConfig['switches']):
        switch = 'switch_%d' % (idx+1)
        response = ethswitch_lib.getListIfNotUpAdminStatus(switch)
        logger.info("Checking %s result: %s" % (switch, response))
        if response[1] != [] and response[2] != []:
            logger.error("Checking %s result: %s" % (switch, response))
            result[1].append((switch))
            result[0] = 'ERROR'

    logger.info('leave checkSwitches')

    return result


def checkNetwork(testConfig):

    logger.info('enter checkNetwork')

    result = ['SUCCESS',[]]

    targetType = 'hw_target' #hårdlött, ska hämtas från target data
    #targetType = target_data.data['targetType']

    #WORKAROUND HEADING: ping problem from gw-pc
    #WORKAROUND DESCRIPTION:
    #sometimes, after an cluster restart, the first ping command
    #sent from the gw-pc hangs. This problem has been seen with LOTC4.1
    #The workaround is to send a dummy ping to the SC-1 and ignore the result
    #Further investigation needed
    #WORKAROUND DESCRIPTION END
    response = ssh_lib.sendCommand('ping -c 1 192.168.0.1',  9, 9)
    if len(testConfig['testNodes']) > 1:
        response = ssh_lib.sendCommand('ping -c 1 192.168.0.2',  9, 9)
    #WORKAROUND END


    for subrack, slot in testConfig['testNodes']:
        blade = 'blade_%s_%s' %  (subrack, slot)
        if targetType == 'simulator_target':
            ipAddress = targetData['ipAddress']['ipmi'][blade]
            response = misc_lib.execCommand ("ping -c 3 -i 3 %s" % (ipAddress))
        else:
            ipAddress = targetData['ipAddress']['blades'][blade]
            response = ssh_lib.sendCommand(" ping -c 3 -i 3 %s" % (ipAddress),  9, 9)
        if response[0] != 'SUCCESS':
            return response
        if re.search('3 packets transmitted, 3 received',response[1]):
            logger.info('ConnectionEstablished: Connection established')
        elif re.search('3 packets transmitted, 2 received',response[1]):
            logger.info('ConnectionEstablished: Connection established')
        elif re.search('3 packets transmitted, 1 received',response[1]):
            logger.info('ConnectionEstablished: Connection established')
        else:
            logger.warn('Unable to ping Subrack: %s; Slot: %s ping stat: %s' % (subrack, slot, response[1]))
            result[1].append((subrack, slot))
            result[0] = 'ERROR'

    logger.info('leave checkNetwork')

    return result


def checkDumps(tag):

    logger.info('enter checkDumps')

    global mostResentDumps
    result = ['SUCCESS',[]]

    # wait until controller is up
    cmd = 'ls'
    for i in range(20):
        ret = ssh_lib.sendCommand(cmd)
        if ret[0] == 'SUCCESS' and ret[1] != '':
            break
        else:
            misc_lib.waitTime(30)

    # check for core dumps
    cmd = 'ls -lrt  /cluster/dumps/*.core'
    ret = ssh_lib.sendCommand(cmd)
    if ret[0] != 'SUCCESS':
        return ret

    newDumps = []
    btInfos = []
    if re.search('No such file or directory',ret[1]):
        logger.info('No core dumps found')
    else:
        dumpList = ret[1].splitlines()
        if len(dumpList) > 0 and len(mostResentDumps) == 0:
            newDumps = dumpList
        elif len(dumpList) > 0 and len(mostResentDumps) > 0:
            if dumpList[len(dumpList) - 1] != mostResentDumps[len(mostResentDumps) - 1]:
                if mostResentDumps[len(mostResentDumps) - 1] in dumpList:
                    newDumps = dumpList[dumpList.index(mostResentDumps[len(mostResentDumps) - 1])+1:]
                else:
                    newDumps = dumpList

        #check if scripts exist
        cmd = "[ -f /home/test/frequency.sh ] && [ -f /home/test/backtrace.sh ] && [ -f /home/test/all_bt.sh ] && echo 'Files exist'"
        ret = ssh_lib.sendCommand(cmd)

        if ret[1] == 'Files exist':
            dumpPaths = []
            for dump in newDumps:
                dump = dump.split()
                dumpPaths.append(dump[len(dump)-1])

            file_dumps = '/home/tspsaf/public_html/test_env/dump_tools/dumps'
            file = open(file_dumps, 'a')

            controller1 = targetData['ipAddress']['ctrl']['ctrl1']

            for dump in dumpPaths:
                # generate cluster_key for ssh without password
                repo = os.environ['MY_REPOSITORY']
                cmd = "%s/test_env/misc/dump_handling/nopassword_cluster.py -n %s -k %s/test_env/misc/dump_handling/cluster_key" % (repo, controller1, repo)
                ret = misc_lib.execCommand(cmd)
                #SUM=`$BT $DUMP | sed 's/([^)]*)/(...)/' | sed 's/0x[0-9a-fA-F]*/0x????????/' | grep "#[0-9]*" | md5sum`
                cmd = "ssh -i %s/test_env/misc/dump_handling/cluster_key root@%s \" COLUMNS=240 /home/test/backtrace.sh %s \""  % (repo, controller1, dump)
                ret = misc_lib.execCommand(cmd)
                btInfos.append(ret[1])


                cmd = "ssh -i %s/test_env/misc/dump_handling/cluster_key root@%s \" COLUMNS=240 /home/test/backtrace.sh %s | sed 's/([^)]*)/(...)/' | sed 's/0x[0-9a-fA-F]*/0x????????/' | grep '#[0-9]*' | md5sum \"" % (repo, controller1, dump)
                ret = misc_lib.execCommand(cmd)

                if re.search('/com.',dump):
                    logger.info('This is a COM dump, will not be added to the file_backtraces, no email will be sent.')
                else:
                    # get md5sum
                    temp = ret[1].split()
                    md5sum = temp[0]
                    file = open(file_dumps, 'r')
                    text = file.read()
                    file.close()

                    # get stats

                    """
                    FIX ME: We are now using GIT, not clearcase. What is the GIT equivalent of view?

                    child_stdin, child_stdout, child_stderr = os.popen3(["cleartool", "lsstream", "-short"])
                    stdoutString = child_stdout.read()
                    ccview = stdoutString.strip()
                    """
                    ccview = "not_using_clearcase"

                    cmd = "ls -lrt  /cluster/dumps/*.core | grep '%s' | awk '{print $6 \" \" $7 \" \" $8}'" % dump
                    res = ssh_lib.sendCommand(cmd)
                    if res[0]!='SUCCESS' or res[1]=='':
                        currtime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        currtime = res[1]
                    user = os.environ.get("USER")
                    target = targetData['target']

                    if md5sum not in text:
                        # save backtrace if the coredump's md5sum is not in dumps!
                        cmd = "cd /home/test; ./backtrace.sh %s" % dump
                        ret = ssh_lib.sendCommand(cmd)
                        file_backtraces = '/home/tspsaf/public_html/test_env/dump_tools/backtraces'
                        file = open(file_backtraces, 'a')
                        file.write(len(md5sum)*'*')
                        file.write("\n%s\n" % md5sum)
                        file.write(len(md5sum)*'*')
                        file.write("\n%s\n\n\n" % ret[1])
                        file.close()

                        #send a mail to all in 'you'
                        me = 'checkDumps'
                        you = ['ingvar.khan@ericsson.com', 'per-erik.persson@ericsson.com', 'marianne.bergstrom@ericsson.com', 'xinyue.wang@ericsson.com']

                        stats = 'Dump: %s\nTag: %s\nUser: %s\nTarget: %s\nStream: %s\nTime: %s\nId: %s' % (dump, tag, user, target, ccview, currtime, md5sum)
                        msg = MIMEText('%s\n\n%s\n\nThe coredump history can be found here:\n%s\n\nThe backtraces can be found here:\n%s' % (ret[1], stats, file_dumps, file_backtraces))
                        msg['Subject'] = 'New coredump found'
                        msg['From'] = me
                        msg['To'] = ', '.join(you)

                        try:
                            s = smtplib.SMTP('localhost')
                            s.sendmail(me, you, msg.as_string())
                            s.quit()
                            logger.info('Successfully sent email')
                        except:
                            logger.info('Error: unable to send email')

                    # store the data in dumps
                    file = open(file_dumps, 'a')
                    file.write(dump + '   ' + tag + '   ' + user + '   ' + target + '   ' + ccview + '   ' + currtime + '   ' + md5sum + '\n')
                    file.close()

    # need to print all component version in case we have at least 1 dumps.
    if len(btInfos) > 0:
        logger.info("cmw-repository-list in case coredumps generated")
        cmd = 'cmw-repository-list'
        result = ssh_lib.sendCommand(cmd)
        temp = result[1].split('\n')
        for line in temp:
            logger.info(line)

    if len(newDumps) > 0:
        result = ['ERROR', newDumps, btInfos]

    logger.info('leave checkDumps')
    return result


def resetDumps():

    logger.info('enter resetDumps')

    global mostResentDumps

    cmd = """ls -lrt /cluster/dumps/*.core"""
    dumpList = ssh_lib.sendCommand(cmd)
    #if result == 'SUCCESS':
    if dumpList[0] != 'SUCCESS':
        return dumpList

    if dumpList[1].find('No such file or directory') != -1:
        result = 'SUCCESS', mostResentDumps
    else:
        mostResentDumps = dumpList[1].splitlines()
        result = 'SUCCESS', mostResentDumps

    logger.info('leave resetDumps')

    return result


def checkSystemInterface(interfaces):

    logger.info('enter checkSystemInterface')

    result = ['SUCCESS', {}]
    for interface in interfaces:
        if interface =='vip':
            response = misc_lib.execCommand(" ping -c 2 %s" % (targetData['ipAddress']['vip']['vip_3']))
        elif(interface=='NB'):
            misc_lib.execCommand(" ping -c 1 %s" % (targetData['ipAddress']['ctrl'][interface])) #Wake up call on nbi
            response = misc_lib.execCommand(" ping -c 2 %s" % (targetData['ipAddress']['ctrl'][interface]))
        else:
            response = misc_lib.execCommand(" ping -c 2 %s" % (targetData['ipAddress']['ctrl'][interface]))
        if response != 'SUCCESS':
            return response
        if re.search('2 packets transmitted, 2 received',response):
            reply = 'Connection to interface %s established' % interface
            logger.info(reply)
        else:
            reply = 'Connection to interface %s NOT established' % interface
            logger.error(reply)
            result[0] = 'ERROR'
        result[1][interface]= reply

    logger.info('leave checkSystemInterface')

    return result


def checkTestAppLoad(testConfig, testApplicationLoadDeviation):

    logger.info('enter checkTestAppLoad')

    result = ['SUCCESS', {}]
    #SC's
    for subrack, slot in testConfig['controllers']:
        response, load = readProcessorLoad(subrack, slot)
        if response == 'ERROR':
            result[1]['SC_%s_%s' % (subrack, slot)] = 'Failed to measure load'
            result[0] = 'ERROR'
        elif load == 0:
            result[1]['SC_%s_%s' % (subrack, slot)] = 0
        else:
            onesc = 0
            if testConfig['testAppEnabledBlades']['onesc'] == (subrack, slot):
                onesc =  testConfig['testInstanceConfiguration']['onesc']['load']
            sc = testConfig['testInstanceConfiguration']['sc']['load']
            all = testConfig['testInstanceConfiguration']['all']['load']
            estimatedLoad = float(onesc) + float(sc) + float(all)
            if estimatedLoad != 0:
                diff = abs(float(load) - estimatedLoad)
                result[1]['SC_%s_%s' % (subrack, slot)] = round((diff / estimatedLoad)*100, 1)
            else:
                result[1]['SC_%s_%s' % (subrack, slot)] = 0
            if result[1]['SC_%s_%s' % (subrack, slot)] > testApplicationLoadDeviation['sc'] :
                result[0] = 'ERROR'

    #PL's
    for subrack, slot in testConfig['payloads']:
        response, load = readProcessorLoad(subrack, slot)
        if response == 'ERROR':
            result[1]['PL_%s_%s' % (subrack, slot)] = 'Failed to measure load'
            result[0] = 'ERROR'
        elif load == 0:
            result[1]['PL_%s_%s' % (subrack, slot)] = 0
        else:
            onepl = 0
            if testConfig['testAppEnabledBlades']['onepl'] == (subrack, slot):
                onepl =  testConfig['testInstanceConfiguration']['onepl']['load']
            pl = testConfig['testInstanceConfiguration']['pl']['load']
            all = testConfig['testInstanceConfiguration']['all']['load']
            estimatedLoad = float(onepl) + float(pl) + float(all)
            if estimatedLoad != 0:
                diff = abs(float(load) - estimatedLoad)
                result[1]['PL_%s_%s' % (subrack, slot)] = round((diff / estimatedLoad)*100, 1)
            else:
                result[1]['PL_%s_%s' % (subrack, slot)] = 0
            if result[1]['PL_%s_%s' % (subrack, slot)] > testApplicationLoadDeviation['pl'] :
                result[0] = 'ERROR'

    logger.info('leave checkTestAppLoad')

    return result


def checkSwCompStates(testConfig, swType):

    #använd testconfig för att exkludera noder ex) node reduction
    global testCaseConfig
    global testSuiteConfig
    logger.debug('enter checkSwCompStates: %s' % swType)
    amfNodeNameSeparator = str(System.getProperty("amfNodeNameSeparator"))
    hostnameSeparator = str(System.getProperty("hostnameSeparator"))
    errorInfo = []
    safComps = []
    temp = []
    faultyNodes = []

    result = saf_lib.checkClusterStatus()
    okFlag = True
    if result[0] == 'ERROR':
        errorInfo =  result[1]
        faultyNodes = []
        for i, node in enumerate(testConfig['testNodes']):
            amfNodeName = saf_lib.getAmfNodeName(node[0], node[1])
            #amfNodeName = re.sub(hostnameSeparator,amfNodeNameSeparator,nodeName)
            if re.search(amfNodeName,str(errorInfo)):
                faultyNodes.append(testConfig['testNodes'][i])
                okFlag = False
        result = ('ERROR', errorInfo, faultyNodes)

    if not okFlag:
        for node in faultyNodes:
            logger.warn('faulty node: %s %s' % (node[0], node[1]))

    logger.debug('leave checkSwCompStates: %s' % swType)

    return result


def searchForSwBundleOnNode(searchString = '', node = 'SC-2-1'):

    logger.debug('enter searchForSwBundleOnNode')
    logger.info('Getting installed SW bundles for %s' % searchString)
    result = saf_lib.getInstalledSwBundlesOnNode(node)
    if result[0] == 'ERROR': return ('ERROR','failed to get info about installed sw bundles on node %s' % node)

    matches = []
    for bundle in result[1]:
        if re.search(searchString,bundle):
            matches.append(bundle)
    if len(matches) == 0:
        result = ('ERROR','NO MATCH on node %s' % node)
    else:
        result = ('SUCCESS', matches)

    logger.debug('leave searchForSwBundleOnNode')
    return result



def readProcessorLoad(subrack, slot, measurements = 6):

    logger.info('enter readProcessorLoad')

    ret = ['SUCCESS', '']

    logger.info("readProcessorLoad(%u,%u,%u)" % (subrack,slot,measurements))

    result = ssh_lib.sendCommand("vmstat 1 %d" % (int(measurements)), subrack, slot)
    if (result[0] != 'SUCCESS') or (result[1] == ''):
        return ('ERROR', result[1])
    #if (result[0] == 'SUCCESS'):
    retval = result[1].split('\n')[3:]
    response = []
    for r in retval:
        response.append(int(r.split()[14]))
    response = 100 - (sum(response)/len(response))
    logger.debug("readProcessorLoad: Load measured for blade_%u_%u result: %2u%%"\
                          % (subrack, slot, response))
    ret[1] = str(int(response))
    #else:
    #    logger.error("readProcessorLoad: Load measuring for blade_%u_%u FAILED!"\
    #                      % (subrack, slot))
    #    ret = result[0],result[1]

    logger.info('leave readProcessorLoad')

    return ret

def checkTestAppStatistic(testConfig, testApplicationAcceptedLostCalls ):

    logger.info('enter checkTestAppStatistic')

    result = ['SUCCESS', {}]
    instances = testConfig['testInstanceConfiguration'].keys()
    #remove some instances when running with 0 PLs
    if 0 == len(testConfig['payloads']):
        instances.remove('onepl')
        instances.remove('pl')
    if 1 == len(testConfig['controllers']):
        instances.remove('sc')
    for instance in instances:
        value = testapp_lib.getTotalStatistics(instance)
        if value[0] != 'SUCCESS':
            return value
        if float(value[1]['send']) > 0:
            lost = round(((float(value[1]['send']) - float(value[1]['recv']))/float(value[1]['send']))*100, 2)
            result[1][instance] = lost
            if lost > testApplicationAcceptedLostCalls:
                result[0] = 'ERROR'
        else:
            result[1][instance] = 0

    logger.info('leave checkTestAppStatistic')

    return result


def setProcessorLoad(testConfig, loadSc = '', loadPl = '', loadProfile = ''):

    logger.info('enter setProcessorLoad')
    logger.debug('debug debug')

    result = ['SUCCESS', []]
    instances = testConfig['testInstanceConfiguration'].keys()
    #remove some instances when running with 0 PLs
    if 0 == len(testConfig['payloads']):
        instances.remove('onepl')
        instances.remove('pl')
    for instance in instances:
        if loadProfile != '':
            profile = loadProfile
        else:
            profile = testConfig['testInstanceConfiguration'][instance]['profile']

        if instance == 'sc' and loadSc != '':
            load = loadSc
        elif instance == 'pl' and loadPl != '':
            load = loadPl
        else:
            load = testConfig['testInstanceConfiguration'][instance]['load']
        res = setProcessorLoadTestApplication(testConfig, instance, profile, load, tcpConn = 499, tcpTime = 200)
        if res[0]== 'ERROR':
            result[0] = res[0]

    logger.info('leave setProcessorLoad')

    return result


def setProcessorLoadTestApplication(testConfig, instance, profile, load, tcpConn = 499, tcpTime = 250):

    logger.info('enter setProcessorLoadTestApplication')
    logger.debug('debug debug')
    instance = instance.upper()
    intensity = 5

    blades = len(testConfig['testAppEnabledBlades'][instance.lower()])

    if blades == 0:
        result = ('ERROR', "No such instance configured: %s" % instance)
    else:
        targetType = targetData['targetType']
        executionCapacityFactor = targetData['execution_capacity_factor']

        # Quick fix for Sun system load
        if float(executionCapacityFactor) > 3.0:
            profile = 'ultra'
            executionCapacityFactor = (float(executionCapacityFactor) - 1.0) / 5.8
            #executionCapacityFactor = (float(executionCapacityFactor) - 1.0) / 2

        logger.debug("Calculating intensity for target type: %s, instance type: %s, exec capacity: %s, nr of blades: %s, load: %d" % (targetType, instance, executionCapacityFactor, blades, int(load)))
        intensityLevel = int(float(executionCapacityFactor) * float(load) * float(blades) * float(intensity))


        return setIntensetyTestApplication(testConfig, instance, profile, intensityLevel, tcpConn, tcpTime)

    logger.info('leave setProcessorLoadTestApplication')
    return result


##this function is added to trim TestApp to a appropriate intensity level.
def setIntensetyTestApplication(testConfig, instance, profile, intensityLevel, tcpConn=499, tcpTime=250):


    #print "***  type=%-10s cap=%-4.2f instance=%-5s profile=%-8s load=%-2d  intensity=%-3d intensityLevel=%-5d" %\
    #   (targetType, float(executionCapacityFactor), instance, profile, int(load), int(intensity), int(intensityLevel))

    # Calculate TCP connections to use

    nodes = 2  # Assume 2 nodes (acceptable for single node instances as well)

    if instance == 'ALL':
        nodes = len(testConfig['testNodes'])
    elif instance == 'PL':
        nodes = len(testConfig['payloads'])
    elif instance == 'SC':
        nodes = len(testConfig['controllers'])

    tcpConn = 300 + (nodes * 15)

    # If the intensityLevel is 0, set the tcpConnections, and timeout to zero as well
    # Quick fix to avoid even more configuration parameters, rethink and reimplement
    if intensityLevel == 0:
        tcpConn = 0
        tcpTime = 0

    if instance=='PL': # external generator
        try:
            # The external Tgen is always restarted for bug compatibility with
            # old versions of TGC.
            # A working TGC will report "No TGen registered" when the external
            # Tgen is not started.
            tg_lib.instantiateExternalTG()
            result =  testapp_lib.setConfiguration(instance, profile, intensityLevel, 'info', tcpConn, tcpTime)
            if result[0] != 'SUCCESS':
                logger.error('Failed to configure external load generator')
                return result
            #if re.search('No TGen registered', result[1]) and instance=='PL' :
            #    logger.warn('No external generator registered. Trying to instantiate the external TG')
            #    tg_lib.instantiateExternalTG()
            #    result =  testapp_lib.setConfiguration(instance, profile, intensityLevel, 'info', tcpConn, tcpTime)
        except tg_lib.NoExternalTgen:
            logger.warn('Ignoring setting processor load to TestApp %s instance. No external traffic generator defined' % (instance))
            result = testapp_lib.setConfiguration(instance, profile, intensityLevel, 'info', tcpConn, tcpTime)
            if result[0] != 'SUCCESS':
                return result
    else:
        result = testapp_lib.setConfiguration(instance, profile, intensityLevel, 'info', tcpConn, tcpTime)
        if result[0] != 'SUCCESS':
            return result


    if not re.search('result-string: OK',result[1]):
        logger.error("setProcessorLoad: Trouble configuring Test App intensity to: %u" % (intensityLevel))

    logger.info('leave setProcessorLoadTestApplication')

    return result


def resetTestAppStatistics(testConfig):

    logger.info('enter resetTestAppStatistics')

    result = ssh_lib.sendCommand('ls -1  /home/test/var/lib/testapp/ | grep config')
    if result[0] == 'SUCCESS' and result[1] != '': #is not possible to
        result = ['SUCCESS', []]
        instances = testConfig['testInstanceConfiguration'].keys()
        #remove some instances when running with 0 PLs
        if 0 == len(testConfig['payloads']):
            instances.remove('onepl')
            instances.remove('pl')
        for instance in instances:
            response  = testapp_lib.resetStatistics(instance)
            if response[1] != 'SUCCESS':
                return response
            result[1].append(response[1])

    logger.info('leave resetTestAppStatistics')

    return result


def repairSwitch(switch):

    logger.info('enter repairSwitch')

    result = 'SUCCESS'
    response = ethswitch_lib.checkAndFixAllPortToUp(switch)
    if response[0] != 'SUCCESS':
        return response

    logger.info("Checking %s result: %s" % (switch, response[1]))

    logger.info('leave repairSwitch')

    return result


def getHostname(testConfig, subrack = 2, slot=1 ):

    global targetData

    hostNameSeparator = targetData['hostnameSeparator']
    dict={}
    idx = testConfig['testNodes'].index((subrack,slot))
    types = testConfig['testNodesTypes'][idx]
    ## Get real hostname
    #Start
    #Start
    cmd = 'hostname | wc -m'
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS' and result[1] != "":
        lenghtOfNode = int(result[1]) - 3
        cmd = 'hostname | cut -c 4-%d' %(lenghtOfNode)
        result = ssh_lib.sendCommand(cmd)
        hostName = result[1]
        #End
    #dict['hostname'] = '%s%s%s%s%s' % (types,hostNameSeparator,subrack, hostNameSeparator, slot)
        dict['hostname'] = '%s%s%s%s%s' % (types,hostNameSeparator,hostName, hostNameSeparator, slot)
    #hostNameSeparatorPattern = targetData['hostnameSeparatorPatterns']
    #dict['hostname'] = '%s%s%s%s%s' % (types,hostNameSeparator,subrack, hostNameSeparator, slot)
    #dict['pattern'] = '%s%s%s%s%s' % (types,hostNameSeparatorPattern,subrack, hostNameSeparatorPattern, slot)
    #dict['separator'] = hostNameSeparator
    return dict


def switchActCtrlBlade(testConfig):

    global activeController

    logger.info('enter switchActCtrlBlade')

    if activeController == 1:
        setActCtrlBlade(testConfig, 2)
    else:
        setActCtrlBlade(testConfig, 1)

    logger.info('leave switchActCtrlBlade')

    return


def setActCtrlBlade(testConfig, ac = 1):

    global activeController

    logger.info('enter  setActCtrlBlade')

    activeController = ac
    subrack, slot = testConfig['controllers'][activeController -1]
    result = ssh_lib.setConfig(subrack, slot, activeController)

    logger.info('leave  setActCtrlBlade')

    return


def getActCtrlBlade(testConfig):

    global activeController

    logger.info('enter  getActCtrlBlade')

    index = activeController - 1
    blade = testConfig['controllers'][index]

    logger.info('leave  getActCtrlBlade')

    return blade


def updateActiveController(testConfig):
    global activeController

    #global testConfig

    logger.info('enter updateActiveController')

    #This System Controller is assigned : HA ACTIVE STATE
    controllers=testConfig['controllers']
    result = queryHaStateActiveController()

    if result[0] != 'SUCCESS':
        logger.error(result[1])
        subrack, slot = controllers[activeController - 1]
        result = 'ERROR', [subrack, slot]
        return result

    if result[1] == 'ACTIVE':# to be modified for coreMw
        subrack, slot = controllers[activeController - 1]
        result = result[0], [subrack, slot]
    else:
        if len(testConfig['controllers']) == 1:

            logger.error('There is only one controller and it is not active!')
            subrack, slot = controllers[activeController - 1]
            result = 'ERROR', [subrack, slot]
            return result

        switchActCtrlBlade(testConfig)
        result = queryHaStateActiveController()

        if result[0] == 'SUCCESS' and result[1] =='ACTIVE':# to be modified for coreMw
            subrack, slot = controllers[activeController-1]
            result = result[0], [subrack, slot]
        else:
            subrack, slot = controllers[activeController-1]
            result = 'ERROR',[subrack, slot]

    logger.info('leave updateActiveController')
    return result


####to be modified for coreMw##### - #ENJOLSZ has done a modification but I think that the whole method should be moved to the saf_lib!
def queryHaStateActiveController():

    global activeController

    logger.info('enter queryHaStateActiveController')

    ssh_lib.tearDownHandles()

    activeSlot = activeController

    #activeSubrack, activeSlot, activeCtrl = ssh_lib.getConfig()
    nodeName = 'SC%s%d' %(amfNodeNameSeparator, activeSlot)
    DN = 'safSISU=safSu=%s\,safSg=2N\,safApp=OpenSAF,safSi=SC-2N,safApp=OpenSAF' %nodeName
    result = ssh_lib.sendCommand("amf-state siass ha '%s'" %DN)
    if len(result[1].splitlines()) < 2:
        logger.info('leave queryHaStateActiveController')
        return ('ERROR', 'Wrong data received while checking active controller HA state. %s' %result[1])
    if len(result[1].splitlines()[len(result[1].splitlines()) - 1].split("=")) != 2:
        logger.info('leave queryHaStateActiveController')
        return ('ERROR', 'no active or standby state found for current SC. %s' %result[1])
    if len(result[1].splitlines()[len(result[1].splitlines()) - 1].split("=")[1].split("(")) != 2:
        logger.info('leave queryHaStateActiveController')
        return ('ERROR', 'no active or standby state found for current SC. %s' %result[1])
    haStateActiveCtrl = result[1].splitlines()[len(result[1].splitlines()) - 1].split("=")[1].split("(")[0]
    logger.info('%s HA state is: %s' %(nodeName, haStateActiveCtrl))
    logger.info('leave queryHaStateActiveController')
    return ('SUCCESS', haStateActiveCtrl)
####remove this function for coreMw END#####


def logSystemInformation(listOfCmds):

    logger.info('enter logSystemInformation')

    result = ssh_lib.getTimeout()
    defTimeout = result[1]
    ssh_lib.setTimeout(90)

    result = ['SUCCESS', []]
    for cmd in listOfCmds:
        response = ssh_lib.sendCommand(cmd)
        if response[0] != 'SUCCESS':
            return response
        logger.info('cmd:%s result:%s' % (cmd, response[1]))
        result[1].append(response[1])

    result = ssh_lib.sendCommand(cmd)
    ssh_lib.setTimeout(defTimeout)

    logger.info('leave logSystemInformation')

    return result


def getXmlParams(param):

    global testCaseConfig
    global testSuiteConfig

    data = ph.getData(testCaseConfig,param)
    if data != 'suiteConf':
        result =  data
    else:
        result = ph.getData(testSuiteConfig, param)

    return result

def setXmlParams(tcConfig, tsConfig):

    global testCaseConfig
    global testSuiteConfig

    testCaseConfig = tcConfig
    testSuiteConfig = tsConfig

    return 'SUCCESS'


def setSyslogEntry(testConfig, entry, myId):

    hostNameList = []
    if getEASPI() > '1.1':
        remoteLoginType = 'ssh'
    else:
        remoteLoginType = 'rsh'

    for subrack, slot in testConfig["testNodes"] :
        node = getHostname(testConfig, subrack, slot)['hostname']
        hostNameList.append(node)
        if entry == 'setup':
            msg = """%s %s 'logger -t "system test" ">>>>>>>>>>>>>> Startpoint in %s (setUp)  >>>>>>>>>>>>>>"'""" % (remoteLoginType, node, myId)
        else:
            msg = """%s %s 'logger -t "system test" "<<<<<<<<<<<<<< Endpoint in %s (tearDown)  <<<<<<<<<<<<<<"'""" % (remoteLoginType, node, myId)
#        msg = """grep "OpenSAF: Service Initialization Success" /var/log/PL-2-3/messages | awk '{print $1" "$2" "$3}' | tail -1"""
        response = ssh_lib.sendCommand(msg)
        #if response[0] == 'ERROR':
        #    result[0]='ERROR'
    result = response[0],response[1],hostNameList

    return result


def collectInfo(tcTag,testConfig):

    logger.debug('enter collectInfo')

    global logDir
    global targetData

    #try:
    timeout = 1800
    operationTimeout = 1800
    okFlag = False

    timeNow = time.time()
    endTime = timeNow + timeout

    while timeNow < endTime and okFlag == False:
        result = ssh_lib.getConfig()
        subrack, slot  = result[0:2]
        if 'vbox' == targetData['targetType'].split('_')[0] or 'qemu' == targetData['targetType'].split('_')[0]:
            result = misc_lib.execCommand("ping -c 2 %s" % (targetData['ipAddress']['ctrl']['ctrl%d'%slot]))
        else:
            result = hw_lib.pingBlade(subrack, slot)
        if result[0] == 'SUCCESS':
            result = ssh_lib.sendCommand('mkdir -p /home/coremw')
            if result[0] != 'SUCCESS':
                logger.warn('failed to create /home/coremw on blade %s %s' %(subrack, slot))
            result = saf_lib.collectInfo(tcTag, operationTimeout)
            if result[0] == 'SUCCESS':
                okFlag = True
            else:
                logger.warn('failed to create collect info on blade %s %s' %(subrack, slot))
        else:
            switchActCtrlBlade(testConfig)
            result = ssh_lib.getConfig()
            subrack, slot = result[0:2]
            result = hw_lib.pingBlade(subrack, slot)
            if result[0] == 'SUCCESS':
                result = ssh_lib.sendCommand('mkdir -p /home/coremw')
                if result[0] != 'SUCCESS':
                    logger.warn('failed to create /home/coremw on blade %s %s' %(subrack, slot))
                result = saf_lib.collectInfo(tcTag, operationTimeout)
                if result[0] == 'SUCCESS':
                    okFlag = True
                else:
                    logger.warn('failed to create collect info on blade %s %s' %(subrack, slot))
            else:
                switchActCtrlBlade(testConfig)
        if not okFlag:
            misc_lib.waitTime(15)
            timeNow = time.time()

    if okFlag:
        collectInfoFile = result[1]
        result = ssh_lib.remoteCopyFrom(collectInfoFile, logDir, 60)
        if result[0] != 'SUCCESS':
            logger.error('Could not copy collect info file from target system. %s' % result[1])
            ret = ('ERROR', 'Could not copy collect info file from target system. %s' % result[1])
        else:
            logger.debug('%s created and stored in %s, on your local machine' % (collectInfoFile, logDir))
            ret = ('SUCCESS', '%s created and stored in %s, on your local machine' % (collectInfoFile, logDir))
    else:
        logger.error('Could not create collectInfo file on either system controller blade. %s' %result[1])
        ret = ('ERROR', 'Could not create collectInfo file on either system controller blade. %s' %result[1])

    logger.debug('leave collectInfo')
    return ret


def getProcessMemoryUsage( subrack, slot, process ):
    logger.debug('enter getProcessMemoryUsage')
    ret = []
    retpid = []
    result = ssh_lib.sendCommand('pgrep -f %s' % (process), subrack, slot)
    res= result[1].splitlines()

    for r in res :
        resVal = unicode(r)
        if result[0] == 'ERROR':
            logger.error('Failed to get status for process %s , subrack: %d, slot: %d' % (process, subrack, slot))
            logger.debug('leave getProcessMemoryUsage')
            return(result[0],0,result[1])

        if (resVal.isnumeric()):
            pid = int(resVal)
        else:
            logger.error('Failed to get status for process %s , subrack: %d, slot: %d' % (process, subrack, slot))
            logger.debug('leave getProcessMemoryUsage')
            return('ERROR',0,'Non numeric value in return for process %s' % (process))

        result = ssh_lib.sendCommand( 'cat /proc/%u/status | grep Vm' % (pid), subrack, slot )
        #print 'Memory usage for %s ( %u ):\n%s' % ( process, pid, resVal )

        if result[0] == 'SUCCESS' and result[1].find("Vm"):
            continue

        if result[0] == 'ERROR':
            logger.error('Failed to get status for process %s id:%us , subrack: %d, slot: %d'\
                              % (process,pid, subrack, slot))
            logger.debug('leave getProcessMemoryUsage')
            return(result[0],0,result[1])

        ret.append(result[1])
        retpid.append(pid)

    logger.debug('leave getProcessMemoryUsage')
    return ("SUCCESS", retpid, ret)


def timeStamp():
    '''
    Start and stop the timer.

    Arguments: None

    Returns:
    float -- the delta time between two consecutive calls to this function, the
             resolution is with two decimals.

    NOTE:
    '''
    logger.debug('enter timeStamp')

    global globalTimeStamp

    timeStamptimeNow = time.time()
    if (globalTimeStamp == 0):
        globalTimeStamp = timeStamptimeNow
    diffTime = (timeStamptimeNow - globalTimeStamp)
    globalTimeStamp = timeStamptimeNow
    timePrint = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    logger.debug("timeStamp() [%.2f] %s" % (diffTime,timePrint))
    logger.debug('leave timeStamp')
    return decimal.Decimal("%.2f" % (diffTime))


def measureRamMemoryUsage (subrack, slot):
    logger.debug('enter measureRamMemoryUsage')
    result = ssh_lib.sendCommand('free -k', subrack, slot)
    if (result[0] == 'ERROR') or (result[1] == ''):
        logger.error('Failed to access subrack: %d, slot: %d' % (subrack, slot))
        logger.debug('leave measureRamMemoryUsage')
        return ("ERROR", "No Measurement possible.")

    arr = result[1].splitlines()[1].split()

    used = int(arr[2])
    buff = int(arr[5])
    cached = int(arr[6])

    usedmemory = str(used - buff - cached)
    logger.debug('leave measureRamMemoryUsage')
    return ("SUCCESS", usedmemory)

def measureRamMemoryUsageForAllBlades(testConfig):
    logger.debug('enter measureRamMemoryUsageForAllBlades')
    failedMeasurement = False
    readMem = {}
    for subrack, slot in testConfig["testNodes"]:
        result = measureRamMemoryUsage(subrack, slot)
        if result[0] != "SUCCESS":
            failedMeasurement = True
            logger.debug('One measureRamMemoryUsage has failed.')
        readMem[(subrack, slot)] = result[1]

    if failedMeasurement:
        logger.debug('leave measureRamMemoryUsageForAllBlades')
        return ('ERROR', readMem)

    logger.debug('leave measureRamMemoryUsageForAllBlades')
    return ('SUCCESS', readMem)

def getBladeUptime(subrack, slot):
    logger.debug('enter getBladeUptime')
    result = ssh_lib.sendCommand("cat /proc/uptime | cut -f1 -d' '", subrack, slot)
    if (result[0] == 'ERROR'):
        logger.error('Failed to send command to subrack: %d, slot: %d' % (subrack, slot))
        logger.debug('leave getBladeUptime')
        return result
    elif('float' not in str(type(eval(result[1])))):
        logger.error('Result not of type float. %s' %result[1])
        logger.debug('leave getBladeUptime')
        return ('ERROR', 'getBladeUptime result not of type float. %s' %result[1])
    else:
        return ('SUCCESS', result[1])
    logger.debug('leave getBladeUptime')

def getSysBladeUptimes(testConfig):
    logger.debug('enter getSysBladeUptimes')
    bladeUptimes = {}
    for subrack, slot in testConfig["testNodes"]:
        result = getBladeUptime(subrack, slot)
        if result[0] != "SUCCESS":
            return result[1]
            logger.debug('leave getSysBladeUptimes')
        bladeUptimes[(subrack, slot)] = float(result[1])
    logger.debug('leave getSysBladeUptimes')
    return ('SUCCESS', bladeUptimes)

def messageBox(message, defaultAnswer= None,  auto=False):
    #logger.info('enter messageBox')

    if  (auto == False):
        if defaultAnswer != None:
            message =  '# '+message+" "+"["+defaultAnswer+"]"+' #'
        else:
            message =  '# '+message+' #'
    elif(auto == True):
        message =  '# '+message+' #'
    frame = "#"*len(message)

    print frame
    print message
    print frame

    response = ''

    old_stdout = sys.stdout

    while (sys.stdin):
        if  (auto == True):
            break
        in_p = sys.stdin.read(1)
        response = response + in_p
        if (in_p == '\n'):
            break
        sys.stdout = in_p

    sys.stdout = old_stdout

    response = response.strip('\n')
    if response == '':
        response = defaultAnswer

    #logger.info('leave messageBox')

    return response


def readStartUpTimeFromNotifications(testConfig, subrack, slot):
    '''
    This method returns the latest time when a blade specified by (subrack, slot) has started up (joined the cluster)
    1. Read notifications which contain startup information about the specified blade.
    2. Get the time stamp from the newest notification

    Known problem:
    The method is not working for SC startup time in case the whole cluster was restarted. This is due to the fact that
    the ntfConsumer is an application and it starts logging after the system controller has already started up. No events
    from before the start of the ntfConsumer are logged (except for alarms?)
    '''

    logger.debug('enter readStartUpTime')
    hostnameSeparatorInNotifications = str(System.getProperty("clmNodeNameSeparator"))
    bladeType = testConfig['testNodesTypes'][testConfig['testNodes'].index((subrack,slot))]
    bladeName = '%s%s%d%s%d' %(bladeType, hostnameSeparatorInNotifications, subrack, hostnameSeparatorInNotifications, slot)

    #bladeRestartPattern = 'Opensaf Initialization is successful on a node safAmfNode=%s,safAmfCluster=myAmfCluster' %bladeName
    bladeRestartPattern = 'CLM node safNode=%s,safCluster=myClmCluster Joined' %bladeName

    result = notification_lib.readNotification(bladeRestartPattern)
    if result[0] != 'SUCCESS':
        ret = result
        logger.debug('leave readStartUpTime')
        return ret

    notfications = result[1]
    # We are interested only in the latest blade startup time
    result = notification_lib.getAttributeFromNotification(notfications[len(notfications) - 1], 'eventTime')
    if result[0] != 'SUCCESS':
        ret = result
        logger.debug('leave readStartUpTime')
        return ret

    startUpTime = result[1][0]
    startUpTime = float(startUpTime[:10] + "." + startUpTime[10:19])

    ret = ('SUCCESS', startUpTime)

    logger.debug('leave readStartUpTime')
    return ret


def readStartUpTimeFromSyslog(testConfig, subrack, slot, startTime):
    '''
    This method returns the     latest time when a blade specified by (subrack, slot) has started up (joined the cluster)
    1. Read notifications which contain startup information about the specified blade.
    2. Get the time stamp from the syslog
    '''

    logger.debug('enter readStartUpTimeFromSyslog')

    searchPatterns = ['Executing TestApp wrapper script', 'instantiate']
    result = getEventTimestampFromSyslog(subrack, slot, searchPatterns, startTime, testConfig)
    if result[0] != 'SUCCESS':
        logger.debug('leave readStartUpTimeFromSyslog')
        return result
    startUpTime = result[1][0]

    logger.debug('leave readStartUpTimeFromSyslog')
    return ('SUCCESS', startUpTime)


def calculateClusterRestartTime(timeCalcList):
    '''
    The method will return the cluster restart time based on the payload blade restart times list given as argument.
    Cluster restart time is considered the time when at least one blade with components with 1+1 redundancy and
    at least one blade with components with N-way redundancy have the middleware in functional state.
    The method has the hardcoded presumtion that components with 1+1 redundancy are installed on blades 2_3 and 2_4. Change the way
    the variable "onePlusOneCompMinTime" is calculated in case this presumtion is not true.
    The algorithm to calculate the cluster restart time is taken from the characteristics test directive for the TSP SAF 2.0 project.
    The method returns:
    ('SUCCESS', <float(clusterRestartTime)>)
    ('ERROR', <error message>)
    '''

    logger.debug('enter calculateClusterRestartTime()')
    if 'list' not in str(type(timeCalcList)):
        return ('ERROR', 'Input parameter in method calculateClusterRestartTime() has to be a list')
    if len(timeCalcList) > 1:
        onePlusOneCompMinTime = timeCalcList.pop(timeCalcList.index(min(timeCalcList[:2]))) #we remove from the list the blade with 1+1 components that came up first
        nWayCompMinTime = min(timeCalcList)
        clusterRestartTime = max(onePlusOneCompMinTime, nWayCompMinTime)
        #self.logger.info("Cluster restart time (One 1+1 redundant blade and any other one more blade): %f" %clusterRestartTime)
    else:
        clusterRestartTime = timeCalcList[0]
    logger.debug('leave calculateClusterRestartTime()')
    return ('SUCCESS', clusterRestartTime)

def getCmwRepositoryListVersion(bundle):
    result = ssh_lib.sendCommand("cmw-repository-list | grep %s | grep -v NotUsed | awk '{print $1}'" % bundle)
    temp = result[1].split('-')
    version = str(temp[-1])
    return version

def getCxpArchiveVersion(bundle, cxpArchive):
    result = misc_lib.execCommand("packageinfo %s/%s.sdp | awk '{print $3}'" % (cxpArchive, bundle))
    temp = result[1].split('-')
    version = temp[-1].strip()
    return version

def getCxpArchive(cxpNames, cxpArchive):
    repoListVersions = []
    cxpListVersions = []
    for bundle in cxpNames.split(','):
        repoListVersions.append(getCmwRepositoryListVersion(bundle))
        cxpListVersions.append(getCxpArchiveVersion(bundle, cxpArchive))
    for version in repoListVersions:
        if version in cxpListVersions:
            cxpArchive = cxpArchive + '/new'
            break
    logger.info('cxpArchive=%s' % cxpArchive)
    return cxpArchive

def createCampaignBundle(pathToCampXmlfile, campBundleName, pathToCxpArch):
    '''
    Create upgrade bundle

    Arguments:
    (str pathToCampXmlfile (absolute path, including file name, to the campaign.xml file),\
     str campBundleName (ex ERIC-testAppInstall.sdp))

    Returns:
    tuple('SUCCESS',str<path to campign bundel (including campBundleName)>) or
    tuple('ERROR', str<error info>)

    NOTE:

    Dependencies:

    '''
    logger.debug('enter createCampaignBundle')

    home = os.environ['HOME']
    pathToEtfTemplate = '%s/test_env/misc/ETF_template.xml' % os.environ['MY_REPOSITORY']
    tempDir = 'campaign_temp'
    pathTotempdir = os.path.join(pathToCxpArch,tempDir)

    #move some files
    cmd = '\\rm -rf %s' % pathTotempdir
    result = misc_lib.execCommand (cmd)
    cmd = 'mkdir %s' % pathTotempdir
    result = misc_lib.execCommand (cmd)
    cmd = '\cp %s %s' % (pathToCampXmlfile,pathTotempdir)
    result = misc_lib.execCommand (cmd)
    cmd = '\cp %s %s' % (pathToEtfTemplate,os.path.join(pathTotempdir,'ETF.xml'))
    result = misc_lib.execCommand (cmd)

    #edit ETF.xml file
    cmd = 'cat %s' % os.path.join(pathTotempdir,'campaign*.xml')
    result = misc_lib.execCommand (cmd)
    campaign = result[1].split('\n')
    smfCampName = ''
    for line in campaign:
        if re.search('safSmfCampaign="safSmfCampaign=',line):
            temp = line.split('=')
            temp = temp[2]
            smfCampName = temp.strip('">')
            break

    fileName = os.path.join(pathTotempdir,'ETF.xml')
    try:
        fd = open(fileName, 'r')
    except:
        errorStr = 'Open file %s FAILED' % fileName
        logger.error(errorStr)
        return ('ERROR', errorStr)

    tempFile = fd.read()
    fd.close()
    newFile = re.sub("###", smfCampName, tempFile)
    fd = open(fileName, 'w')
    fd.write(newFile)
    fd.close()

    #create campaign bundle
    cmd = 'cd  %s;tar -zcvf ../%s *' % (pathTotempdir, campBundleName)
    result = misc_lib.execCommand (cmd)
    pathToCampBundle = os.path.join(pathToCxpArch,campBundleName)

    #clean up
    cmd = '\\rm -rf %s' % pathTotempdir
    result = misc_lib.execCommand (cmd)

    logger.debug('leave createCampaignBundle')


    return ('SUCCESS',pathToCampBundle)

##############################################################################
# build test packages
##############################################################################
def createTestPackage(package, revPrefix = 'T', buildArg = False):
    '''
    Create test package based on released package (SW bundle or configuration package).

    Arguments:
    str(package) -- name of the package(see the dict paths for valid package name)

    Returns:
    tuple('SUCCESS', list['newPackageName','revision','path to file','package name and revision'])
or tuple('ERROR', 'some error info')

    NOTE:
    '''

    logger.debug('enter createTestPackage')

    paths={'ERIC-TA_TAPP'       :{'FETCH':'/vobs/coremw/release/cxp_archive/ERIC-TA_TAPP-CXP9013968_3.sdp','BUILD':''},
           'ERIC-TA_TGC'        :{'FETCH':'/vobs/coremw/release/cxp_archive/ERIC-TA_TGC-CXP9013968_5.sdp','BUILD' : ''},
           'ERIC-TA_TGEN'       :{'FETCH':'/vobs/coremw/release/cxp_archive/ERIC-TA_TGEN-CXP9013968_4.sdp','BUILD' : ''},
           'ERIC-LOTC_SC'       :{'FETCH':'/vobs/coremw/release/cxp_archive/lotc_tmp/ERIC-LINUX_CONTROL-CXP9013151_2.sdp','BUILD' : ''},
           'ERIC-LOTC_PL'       :{'FETCH':'/vobs/coremw/release/cxp_archive/lotc_tmp/ERIC-LINUX_PAYLOAD-CXP9013152_2.sdp','BUILD' : ''},
           'LOTC_RUNTIME'       :'/vobs/linux/release/lotc/ERIC-LINUX_RUNTIME-CXP9020125_2.tar.gz',
           'CXP_ARCH'           :'/vobs/coremw/release/cxp_archive/',
           'CXP_ARCH_TMP'       :'/vobs/coremw/release/cxp_archive/tmp',
           'CXP_ARCH_LOTC_TMP'  :'/vobs/coremw/release/cxp_archive/lotc_tmp'}

    if not paths.has_key(package) or package == 'CXP_ARCH' or package == 'CXP_ARCH_TMP':
        errorStr = 'Wrong argument, %s does not exist as package' % package
        logger.error(errorStr)
        return ('ERROR', errorStr)

    #Extract package names
    packageName = paths[package]['FETCH']
    packageName = packageName.split('/')
    packageName = packageName.pop()
    newPackageName = packageName[:len(packageName) -4] +'_' + revPrefix + packageName[len(packageName)-4:]
    packageInfo = []

    defTimeout = ssh_lib.getTimeout()
    ssh_lib.setTimeout(600)

    if package == 'ERIC-LOTC_SC' or package == 'ERIC-LOTC_PL':
        if makeDir(paths['CXP_ARCH_LOTC_TMP'])[0] == 'ERROR':
            errorStr='make directory %s FAILED' % paths['CXP_ARCH_LOTC_TMP']
            logger.error(errorStr)
            return ('ERROR',  errorStr)
        else:
            result = fetchPackage(package, packageName, paths['CXP_ARCH'],paths['CXP_ARCH_TMP'],paths['CXP_ARCH_LOTC_TMP'])

    elif (package == 'ERIC-TA_TAPP' or package == 'ERIC-TA_TGC' or package == 'ERIC-TA_TGEN' ) and not buildArg == False:
        misc_lib.execCommand('\mv -f %s %s/%s' % (paths[package]['FETCH'],paths['CXP_ARCH'],package))
        result = ('SUCCESS','BUILD')

    else:
    # default
        result = fetchPackage(package, packageName, paths['CXP_ARCH'],paths['CXP_ARCH_TMP'])

    # if fetching the package failed, return error
    if result[0] == 'ERROR':
        return ('ERROR', 'fetch package %s FAILED' % packageName)

    # if recommended to build, build and copy to temp folder
    elif result[1] == 'BUILD':
        if buildArg:
            result = buildPackage(package, paths['CXP_ARCH'], buildArg)
        else:
            result = buildPackage(package, paths['CXP_ARCH'])

        if result[0] == 'ERROR':
            return ('ERROR', 'failed to build package %s' % packageName)
        else:
            if misc_lib.execCommand('\mv -f %s/%s %s' % (paths['CXP_ARCH'], packageName, paths['CXP_ARCH_TMP']))[0] == 'ERROR':
                return ('ERROR','move package %s from %s to %s FAILED' % (packageName,paths['CXP_ARCH'],paths['CXP_ARCH_TMP']))

    # extract the package
    if extractPackage(packageName, paths['CXP_ARCH_TMP'])[0] == 'ERROR':
        return ('ERROR', 'extract package %s FAILED' % packageName)

    # remove the original packageFile
    if misc_lib.execCommand('\\rm -f %s/%s' % (paths['CXP_ARCH_TMP'], packageName))[0] == 'ERROR':
        return ('ERROR', 'remove existing %s FAILED' % packageName)

    # edit the ETF.xml file
    result = editPackageFiles(packageName, paths['CXP_ARCH_TMP'], revPrefix)
    if result[0] == 'ERROR':
        return ('ERROR', 'edit package %s FAILED' % packageName)
    else:
        packageInfo = result[1]

    # create new package with edited files
    if createNewPackage(newPackageName, paths['CXP_ARCH_TMP'])[0] == 'ERROR':
        return ('ERROR', 'create test package %s FAILED' % newPackageName)

    # remove the temp folders
    if removeDir( paths['CXP_ARCH_TMP'])[0] == 'ERROR':
        return ('ERROR','failed to remove temp directory')
    if removeDir(paths['CXP_ARCH_LOTC_TMP'])[0] == 'ERROR':
        return ('ERROR','failed to remove lotc temp directory')

    # why is it here ?
    if (package == 'ERIC-TA_TAPP' or package == 'ERIC-TA_TGC' or package == 'ERIC-TA_TGEN') and not buildArg == False:
        misc_lib.execCommand('\mv -f %s/%s %s' % (paths['CXP_ARCH'],package,paths[package]['FETCH']))

    ssh_lib.setTimeout(defTimeout)

    logger.debug('leave createTestPackage')

    return ('SUCCESS', [newPackageName, packageInfo[0], paths['CXP_ARCH'],  packageInfo[1]])


def makeDir(dirName):
    """
    make a directory, removed before it's created(if it's already exists).
    dirName is absolute path and name to the directory
    """

    #make temp dir
    cmd = '\\rm -rf %s' % dirName
    result = misc_lib.execCommand(cmd)
    logger.info('make dir %s' % dirName)
    cmd = 'mkdir %s' % dirName
    result = misc_lib.execCommand(cmd)
    if result[0] == 'ERROR':
        result = ('ERROR', 'create directory %s FAILED' % dirName)
        logger.error(result[1])
    else:
        result = ('SUCCESS','%s created' % dirName)

    return result

def removeDir(dirName):
    """
    remove a directory
    """

    if misc_lib.execCommand('\\rm -rf %s' % dirName)[0] == 'ERROR':
        result = ('ERROR','Could not remove %s' % dirName)
        logger.error(result[1])
    else:
        result = ('SUCCESS', '%s removed' % dirName)

    return result




def fetchPackage(package, packageName, cxpArch, cxpArchTemp, cxpArchLotcTemp = ''):

    relVob = '/vobs/coremw/release/sdp/'
    lotcRuntime = '/vobs/linux/release/lotc/ERIC-LINUX_RUNTIME-CXP9020125_2.tar.gz'

    #check if package exist in cxp_archive
    result = misc_lib.execCommand('ls %s | grep %s' % (cxpArch, packageName ))

    # if exists, copy to temp folder
    if re.search(packageName,result[1]):
        cmd = '\cp %s/%s %s' % (cxpArch, packageName, cxpArchTemp)
        if misc_lib.execCommand(cmd)[0] == 'ERROR':
            result = ('ERROR','Command %s FAILED' % cmd)
            logger.error(result[1])
        else:
            result = ('SUCCESS', 'Package %s found in %s and copied to %s' % (packageName, cxpArch, cxpArchTemp))
            logger.info(result)
    # if not exists, check if it exists under release vob
    else:
        # untar linux runtime and copy the package to cxpArchTemp
        if package == 'ERIC-LOTC_SC' or package == 'ERIC-LOTC_PL':
            runtimePackage = lotcRuntime.split('/')
            runtimePackage = runtimePackage.pop()
            misc_lib.execCommand('\cp %s %s' % (lotcRuntime, cxpArchLotcTemp))
            misc_lib.execCommand('cd %s; tar xvf %s' % (cxpArchLotcTemp, runtimePackage))
            cmd = '\cp %s/%s %s' % (cxpArchLotcTemp, packageName, cxpArchTemp)
            if misc_lib.execCommand(cmd)[0] == 'ERROR':
                result = ('ERROR', 'Command %s FAILED' % cmd)
                logger.error(result[1])
            else:
                result = ('SUCCESS', 'package %s fetched from %s and coped to %s' % (packageName,lotcRuntime, cxpArchTemp))
        else:
            if re.search(packageName,misc_lib.execCommand('ls %s | grep %s' % (relVob, packageName ))[1]):
                cmd = '\cp %s/%s %s' % (relVob, packageName, cxpArchTemp )
                result = misc_lib.execCommand(cmd)
                if result[0] == 'ERROR':
                    errorStr = 'Command %s FAILED' % cmd
                    logger.error(errorStr)
                    result = ('ERROR', errorStr)
                else:
                    result = ('SUCCESS', 'package %s fetched from %s and copied to %s' % (packageName,relVob, cxpArchTemp))
    # if not available anywhere, recommend to build
            else:
                result = ('SUCCESS', 'BUILD')
    return result


def buildPackage(package, cxpArch, buildArg = False):
    logger.info('Build the package')

    # Run the safbuild command with the BASH shell, then set it back
    # to whatever it was before. This is so that that the buildArg
    # parameter is exported to the environment into the Makefile.
    original_shell = os.getenv("SHELL")
    os.environ["SHELL"] = '/bin/bash'

    if buildArg:
        misc_lib.execCommand("export %s ; /vobs/coremw/dev/abs/build/cmwbuild %s" % (buildArg, package))
    else:
        misc_lib.execCommand("/vobs/coremw/dev/abs/build/cmwbuild %s" % package)

    result = misc_lib.execCommand('ls -l %s' %  cxpArch)
    if result[0] == 'ERROR' or not re.search(package, result[1]):
        result = ('ERROR','Build %s FAILED' % package)
        logger.error(result[1])
    else:
        result = ('SUCCESS', '%s was successfully built' % package)

    os.environ["SHELL"] = original_shell

    return result



def extractPackage(packageName, archive):

    #Extract the package
    logger.info('Extract the package: %s' % packageName)
    result = misc_lib.execCommand('cd %s;tar xf %s' % (archive, packageName))
    if result[0] == 'ERROR':
        result = ('ERROR','extract package %s FAILED' % packageName)
        logger.error(result[1])
    return result


def editPackageFiles(packageName, archive, revPrefix):

    #Open ETF.xml
    fileName = '%s/ETF.xml' % archive
    try:
        fd = open(fileName, 'r')
    except:
        errorStr = 'Open file %s FAILED' % fileName
        logger.error(errorStr)
        return ('ERROR', errorStr)

    etfFile = fd.read()
    fd.close()

    #Get and create revisions
    packageName = packageName.split('.')
    packageName = packageName[0]
    pattern = packageName + '-'
    index = etfFile.find(pattern) + len(pattern)
    revStr = etfFile[index : index + 10].split('\n')
    revStr = revStr[0].rstrip('">')
    revStr2 = revStr[ : len(revStr) -2] + '-' + revStr[len(revStr) -2 : len(revStr)]
    subStr = revPrefix + revStr[1:]
    subStr2 = revPrefix + revStr2[1:]
    #newEtfFile = re.sub(revStr, subStr, etfFile)
    packageNameAndRev = packageName + '-' + subStr
    oldPackageNameAndRev = packageName + '-' + revStr


    fileString = 'ETF.xml,offline-install,offline-remove,online-remove,online-install, IDENTITY'
    cmd = 'ls %s' % archive
    result = misc_lib.execCommand(cmd)
    fileList =  result[1].split('\n')
    for packFile in fileList:
        if re.search(packFile, fileString) and not packFile == '':
            fileName = os.path.join(archive, packFile)
            try:
                fd = open(fileName, 'r')
            except:
                errorStr = 'Open file %s FAILED' % fileName
                logge.error(errorStr)
                return ('ERROR', errorStr)

            tempFile = fd.read()
            fd.close()
            newFile = re.sub(revStr, subStr, tempFile)
            newFile = re.sub(revStr2, subStr2, newFile)
            fd = open(fileName, 'w')
            fd.write(newFile)
            fd.close()
        elif re.search('.rpm',packFile) and re.search(revStr, packFile):
            newPackFile = re.sub(revStr, subStr, packFile)
            cmd = '\mv -f %s/%s %s/%s' % (archive, packFile, archive, newPackFile)
            result = misc_lib.execCommand(cmd)
        elif re.search('.rpm', packFile) and re.search(revStr2, packFile):
            newPackFile = re.sub(revStr2, subStr2, packFile)
            cmd = '\mv -f %s/%s %s/%s' % (archive, packFile, archive, newPackFile)
            result = misc_lib.execCommand(cmd)

    return ('SUCCESS', [subStr, packageNameAndRev, oldPackageNameAndRev])


def createNewPackage(newPackageName, archive):

    #Create new test package
    cmd = 'cd  %s;\\rm -f ../%s' % (archive, newPackageName)
    result = misc_lib.execCommand(cmd)

    cmd = 'cd  %s;tar -zcvf ../%s *' % (archive, newPackageName)
    result = misc_lib.execCommand(cmd)
    if result[0] == 'ERROR':
        result = ('ERROR','Command %s FAILED' % cmd)
        logger.error(result[1])
    else:
        result = ('SUCCESS','package %s created' % newPackageName)

    return result


def getEventTimestampFromSyslog(subrack, slot, searchPatterns, startTime, testConfig, logDir = '/var/log/' ):
    '''
    This method will return the timestamp of all the events in which the elements of the search pattern were found.

    The method only returns the matches that occued after the startTime (defined in unix time)

    Main steps:
    1. list all occurance time stamps with
        grep 'search patterns' /var/log/SC-2-1/messages* | cut -d: -f2-4 | awk '{print $1" " $2" "$3}'
    2. compare times with start time (readable format)
    3. convert relevant times to unix time using timeConv
    4. sort list

    Arguments:
    int subrack
    int slot
    list [searchPatterns]
    int startTime (unix time)

    Returns
    ('ERROR', 'error message')
    ('SUCCESS', [list of ints representing unix times])
    '''

    logger.debug('enter getEventTimestampFromSyslog()')

    # 1. list all occurance time stamps with
    hostname = getHostname(testConfig, subrack, slot)['hostname']
    logger.info('get hostname testing %s subrack %d slot %d' % (hostname, subrack, slot))
    logDir += hostname

    readableTimes = []
    cmd = """grep -ia "%s" %s/messages*""" %(searchPatterns[0], logDir)
    if len(searchPatterns) > 1:
        for i in range(len(searchPatterns)-1):
            cmd += """ | grep -i "%s" """ %(searchPatterns[i+1])
    cmd += """ | cut -d: -f1-4 | awk '{print $1" " $2" "$3}'"""
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getEventTimestampFromSyslog()')
        return result
    if result[1] != '':
        tempList = result[1].splitlines()
        for element in tempList:
            if logDir in element and element.count(":") == 3:
                dateString = "%s:%s:%s" %(element.split(':')[1], element.split(':')[2],element.split(':')[3])
                readableTimes.append(dateString)
            elif logDir not in element and element.count(":") == 2:
                readableTimes.append(element)
            else:
                logger.debug('leave getEventTimestampFromSyslog()')
                return ('ERROR', 'Unexpected format of the timestamp when looking for the following search pattern: %s' %str(searchPatterns))

    if len(readableTimes) == 0:
        logger.debug('leave getEventTimestampFromSyslog()')
        return ('ERROR', 'No entry found in the syslog for the following search pattern: %s' %str(searchPatterns))

    # convert unix start time to readable format in order to later use the faster python compare method isDateMoreRecent()
    result = timeConvUnixToReadable(startTime)
    if result[0] != 'SUCCESS':
        return result
    reabableStartTime = result[1]

    #2. compare times with start time (readable format)
    #3. convert relevant times to unix time using timeConv
    timesAfterStartTime = []
    for readableTime in readableTimes:
        result = isDateMoreRecent(reabableStartTime, readableTime)
        if result[0] != 'SUCCESS':
            return result
        if result[1] == True:
            result = timeConv(readableTime)
            if result[0] != 'SUCCESS':
                return result
            timesAfterStartTime.append(result[1])

    if len(timesAfterStartTime) == 0:
        return ('ERROR', 'No entry found in the syslog after the start time for the following search pattern: %s' %str(searchPatterns))
    else:
        #4. sort list
        timesAfterStartTime.sort()
        result = ('SUCCESS', timesAfterStartTime)

    logger.debug('leave getEventTimestampFromSyslog()')
    return result

def getEventTimestampFromSyslogWithLogEntry(subrack, slot, searchPatterns, startTime, testConfig, logDir = '/var/log/' ):
    '''
    This method will return the timestamp of all the events in which the elements of the search pattern were found.

    The method only returns the matches that occued after the startTime (defined in unix time)

    Main steps:
    1. list all logs that match the search patterns with
        grep 'search patterns' /var/log/SC-2-1/messages*
    2. compare times with start time (readable format)
    3. convert relevant times to unix time using timeConv

    Arguments:
    int subrack
    int slot
    list [searchPatterns]
    int startTime (unix time)

    Returns
    ('ERROR', 'error message')
    ('SUCCESS', [list of ints representing unix times])
    '''

    logger.debug('enter getEventTimestampFromSyslogWithLogEntry()')
    logger.info('getEventTimestampFromSyslogWithLogEntry: startTime: %d' %startTime)

    # 1. list all occurance time stamps with
    hostname = getHostname(testConfig, subrack, slot)['hostname']
    logger.info('get hostname testing %s subrack %d slot %d' % (hostname, subrack, slot))
    logDir += hostname

    logEntries = []
    readableTimes = []

    cmd = """grep -iha "%s" %s/messages*""" %(searchPatterns[0], logDir)
    if len(searchPatterns) > 1:
        for i in range(len(searchPatterns)-1):
            cmd += """ | grep -i "%s" """ %(searchPatterns[i+1])
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getEventTimestampFromSyslogWithLogEntry()')
        return result
    if result[1] != '':
        tempList = result[1].splitlines()
        for element in tempList:
            logEntries.append(element)
            readableTimes.append(element[:15])

    if len(readableTimes) == 0:
        logger.debug('leave getEventTimestampFromSyslogWithLogEntry()')
        return ('ERROR', 'No entry found in the syslog for the following search pattern: %s' %str(searchPatterns))

    # convert unix start time to readable format in order to later use the faster python compare method isDateMoreRecent()
    result = timeConvUnixToReadable(startTime)
    if result[0] != 'SUCCESS':
        return result
    reabableStartTime = result[1]

    #2. compare times with start time (readable format)
    #3. convert relevant times to unix time using timeConv
    timesAfterStartTime = []
    logEntriesAfterStartTime = []
    for readableTime in readableTimes:
        result = isDateMoreRecent(reabableStartTime, readableTime)
        if result[0] != 'SUCCESS':
            return result
        if result[1] == True:
            result = timeConv(readableTime)
            if result[0] != 'SUCCESS':
                return result
            timesAfterStartTime.append(result[1])
            logEntriesAfterStartTime.append(logEntries[readableTimes.index(readableTime)])


    if len(timesAfterStartTime) == 0:
        logger.debug('leave getEventTimestampFromSyslogWithLogEntry()')
        return ('ERROR', 'No entry found in the syslog after the start time for the following search pattern: %s' %str(searchPatterns))
    else:
        result = ('SUCCESS', timesAfterStartTime, logEntriesAfterStartTime)

    logger.debug('leave getEventTimestampFromSyslogWithLogEntry()')
    return result

def calculateProcedureLengthDelimitedBySyslogEntries(subrack, slot, startTime, beginPattern, endPattern, testConfig, timeStampAfterCharacter = False, characterDelimiter = ':', convertLluToFloat = True, takeFirstBeginEntryAndLastEndEntry = False):
    """
    The method calculates the time period between two syslog events defined by beginPattern and endPattern.
    Only events that happened after startTime are considered.
    If there is more than one match, the method returns error.
    There is the possibility to use a time stamp that is part of the log entry.
        In this case the time stamp of the log entry is ignored and the time is taken from the log content.
        It is presumed that the time stamp contained in the log entry is in Unix time format.
        Example: 'Dec 30 02:20:14 SC-2-1 com: COM_SA mafLCMterminate called at: 1388393554.886591152'.
            If timeStampAfterCharacter is True and characterDelimiter is ":" the method will identify the time stamp 1388393554.886591152 which will be handled as a float.
        No other characters are allowed after the time stamp.

    Interface:
        subrack, slot - ints defining the node where to execute the command
        startTime - int representation of Unix time after which the syslog events are considered
        beginPattern - list of strings defining the pattern of the syslog entry that marks the beginning of the sequence
        endPattern - list of strings defining the pattern of the syslog entry that marks the end of the sequence
        testConfig - dict: must come from self.testConfig
        timeStampAfterCharacter - bool. If False: time of the log entry is considered and characterDelimiter is ignored
                                        If True: a time stamp is expected at the end of the log entry in Unix time format.
                                            The time stamp must be placed after the string defined by characterDelimiter
        characterDelimiter - string: used to split up the log entry. The last element of the split will be used to extract the time stamp. See example above.
        convertLluToFloat - bool: used if the returned number is in unix time with milliseconds precision as an unsinged long long
            Example: 1397716452199 will be converted to float("1397716452.199")
        takeFirstBeginEntryAndLastEndEntry - bool: If we know in advance that several log entries will match the search patterns we can choose
            to use the first entry that matches the begin pattern and the last entry that matches the end pattern by setting this argument to True

    Returns:
        ('SUCCESS', procedureLength) - procedureLength can be int or float
        ('ERROR', 'some relevant error message')

    """
    logger.debug("enter lib: calculateProcedureLengthDelimitedBySyslogEntries")
    logger.info('Input params: startTime: %d' %startTime)

    result = getEventTimestampFromSyslogWithLogEntry(subrack, slot, beginPattern, startTime, testConfig)
    logger.info('lib: calculateProcedureLengthDelimitedBySyslogEntries: getEventTimestampFromSyslogWithLogEntry result: %s' %str(result))
    if result[0] != 'SUCCESS':
        logger.debug("leave lib: calculateProcedureLengthDelimitedBySyslogEntries")
        return ('ERROR', 'No log entry found for the following search pattern:. %s' %str(beginPattern))
    elif len(result[1]) != 1:
        if (takeFirstBeginEntryAndLastEndEntry):
            result = ('SUCCESS', result[1][:1], result[2][:1])
        else:
            logger.debug("leave lib: calculateProcedureLengthDelimitedBySyslogEntries")
            return ('ERROR', 'Expected exactly one match for the search pattern %s. Received: %d' %(str(beginPattern), len(result[1])))

    if timeStampAfterCharacter == False:
        startOfProcedure = result[1][0]
    else:
        startOfProcedure = eval(result[2][0].split(characterDelimiter)[len(result[2][0].split(characterDelimiter)) - 1])
        if convertLluToFloat:
            startOfProcedure = convertLluToMilliSecFloat(startOfProcedure)
    logger.info('lib: calculateProcedureLengthDelimitedBySyslogEntries: startOfProcedure: %s' %startOfProcedure)

    result = getEventTimestampFromSyslogWithLogEntry(subrack, slot, endPattern, startTime, testConfig)
    logger.info('lib: calculateProcedureLengthDelimitedBySyslogEntries: getEventTimestampFromSyslogWithLogEntry result: %s' %str(result))
    if result[0] != 'SUCCESS':
        logger.debug("leave lib: calculateProcedureLengthDelimitedBySyslogEntries")
        return ('ERROR', 'No log entry found for the following search pattern:. %s' %str(endPattern))
    elif len(result[1]) != 1:
        if (takeFirstBeginEntryAndLastEndEntry):
            result = ('SUCCESS', result[1][-1:], result[2][-1:])
        else:
            logger.debug("leave lib: calculateProcedureLengthDelimitedBySyslogEntries")
            return ('ERROR', 'Expected exactly one match for the search pattern %s. Received: %d' %(str(endPattern), len(result[1])))

    if timeStampAfterCharacter == False:
        endOfProcedure = result[1][0]
    else:
        endOfProcedure = eval(result[2][0].split(characterDelimiter)[len(result[2][0].split(characterDelimiter)) - 1])
        if convertLluToFloat:
            endOfProcedure = convertLluToMilliSecFloat(endOfProcedure)
    logger.info('lib: calculateProcedureLengthDelimitedBySyslogEntries: endOfProcedure: %s' %endOfProcedure)

    procedureLength = endOfProcedure - startOfProcedure
    if procedureLength < 0:
        result = ('ERROR', procedureLength)
    else:
        result = ('SUCCESS', procedureLength)

    logger.info('lib: calculateProcedureLengthDelimitedBySyslogEntries will return: %s ' %str(result))

    logger.debug("leave lib: calculateProcedureLengthDelimitedBySyslogEntries")
    return result

def convertLluToMilliSecFloat(lluFormatNumber):
    """
    Returns a float from a number which represents a unix time with milliseconds precision (unsinged long long)
    """
    seconds = str(lluFormatNumber)[:10]
    milliseconds = str(lluFormatNumber)[10:]
    floatFormatNumber = '%s.%s' %(seconds, milliseconds)
    return float(floatFormatNumber)


def getTimeFromEvent(keyword):
    # returns a list (of longs) of eventTime times (in nanoseconds (10^-9 s)) from an event with a given keyword

    logger.debug('enter getTimeFromEvent()')
    result = notification_lib.readNotification()
    if (result[0] != 'SUCCESS'):
        logger.debug('leave getTimeFromEvent()')
        return result
    times = []

    for notif in result[1]:
        if re.search(keyword, notif):
            print notif
            notifattrlist = str(notif).split('\n')
            for item in notifattrlist:
                if re.search('eventTime', item):
                    time = item.split()[2]
                    times.append(int(time))
    logger.debug('leave getTimeFromEvent()')
    return times



def syncStateCheck(timeout = 1800):
    # this function should be moved to another lotc related class in the future
    '''
    Checks the current drbd sync state and waits until state is UpToDate/UpToDate

    Arguments:
    int timeout = Timeout in seconds

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', result[1])

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter syncStateCheck()')

    for i in range(timeout/30):
        cmd = 'grep "UpToDate/UpToDate" /proc/drbd'
        result = ssh_lib.sendCommand(cmd)
        if '' != result[1]:
            break
        misc_lib.waitTime(30)

    logger.debug('leave syncStateCheck()')
    return result



def timeConv(timeString):
    '''
    The method converts humanly readable time to unix time format
    '''
    logger.debug('enter timeConv()')
    result = misc_lib.execCommand('date -d "%s" +%%s' %timeString)
    if result[0] != 'SUCCESS':
        logger.debug('leave timeConv()')
        return result
    unixTime = int(result[1])
    logger.debug('leave timeConv()')
    return ('SUCCESS', unixTime)


def timeConvUnixToReadable(timeString):
    '''
    This method converts unix time to humanly readable in the format of syslog, that is "month day hour:minute:second"
    '''
    logger.debug('enter timeConvUnixToReadable()')
    #print timeString
    #print type(timeString)
    result = misc_lib.execCommand('date --date "GMT 1970-01-01 %s sec" "+%%b %%d %%T"' %str(timeString))
    if result[0] != 'SUCCESS':
        logger.debug('leave timeConvUnixToReadable()')
        return result
    logger.debug('leave timeConvUnixToReadable()')
    return result


def getStorageLocation():
    location = ' '
    cmd = 'cmwea storage-location-get;echo RetCode=$?'
    result = ssh_lib.sendCommand(cmd)
    if re.search('RetCode=0',result[1]):
        location = string.strip(result[1].split()[0])
        if len(location) != 0:
            return location


def getCoreMWStorageLocation():
    return getStorageLocation()+'/coremw'


def getSoftWareLocation():
    location = ' '
    SPI = getEASPI()
    if SPI == '1.2':
        cmd = 'cmwea software-location-get;echo RetCode=$?'
        result = ssh_lib.sendCommand(cmd)
        if re.search('RetCode=0',result[1]):
            location = string.strip(result[1].split()[0])
            if len(location) != 0:
                return location+'/coremw'
    else:
        return getCoreMWStorageLocation()


def getConfigLocation():
    location = ' '
    SPI = getEASPI()
    if SPI == '1.2':
        cmd = 'cmwea config-location-get;echo RetCode=$?'
        result = ssh_lib.sendCommand(cmd)
        if re.search('RetCode=0',result[1]):
            location = string.strip(result[1].split()[0])
            if len(location) != 0:
                return location+'/coremw'
    else:
        return getCoreMWStorageLocation()


def getNoBackupLocation():
    location = ' '
    SPI = getEASPI()
    if SPI == '1.2':
        cmd = 'cmwea no-backup-location-get;echo RetCode=$?'
        result = ssh_lib.sendCommand(cmd)
        if re.search('RetCode=0',result[1]):
            location = string.strip(result[1].split()[0])
            if len(location) != 0:
                return location+'/coremw'
    else:
        return getCoreMWStorageLocation()


def getClearLocation():
    location = ' '
    SPI = getEASPI()
    if SPI == '1.2':
        cmd = 'cmwea clear-location-get;echo RetCode=$?'
        result = ssh_lib.sendCommand(cmd)
        if re.search('RetCode=0',result[1]):
            location = string.strip(result[1].split()[0])
            if len(location) != 0:
                return location+'/coremw'
    else:
        return getCoreMWStorageLocation()


def getEASPI():
    SPI = ' '
    cmd = 'cmwea spi-revision-get;echo RetCode=$?'
    result = ssh_lib.sendCommand(cmd)
    if re.search('RetCode=0',result[1]):
        SPI = string.strip(result[1].split()[0])
        if len(SPI) != 0:
            return SPI


def waitForCluster(self, charMeasurement = False, maxWaitTime = 1200, startTime = 9999999999):
        '''
        The method repeatedly polls for the payload blades' startup time and exits when new startup info is received from all blades
        or timeout is reached.
        The method returns:
        ('SUCCESS', [<float(bladesRestartTimes)>]) - if the startup times of all the blades are more recent than the start time
        ('ERROR', 'The payload blades of the test cluster did not start up within the allowed %d seconds' %maxWaitTime) - if the condition above is not met
        '''
        # maybe put startTime here or create a rebootClusterWaitForCluster function
        #misc_lib.waitTime(240)


        # wait until controller 1 is up
        """
        self.setTestStep('###wait until controller 1 is up')
        #misc_lib.waitTime(180)
        cmd = 'ls'
        for i in range(20):
            result = self.sshLib.sendCommand(cmd,2,1)
            if result[0] == 'SUCCESS' and result[1] != '':
                break
            else:
                misc_lib.waitTime(30)
        """

        if charMeasurement:
            self.myLogger.debug('enter waitForCluster()')
            endTime = startTime + maxWaitTime
            restartFlag = False
            ret = ('ERROR', 'The blades of the test cluster did not start up within the allowed %d seconds' %maxWaitTime)
            while (time.time() < endTime and restartFlag == False):
                startUpTimes = []
                for subrack, slot in self.testConfig["testNodes"]:
                    if 'testApp' in self.testSuiteConfig['defaultSuiteCheck']['runtest']['appl']['appl']:
                        # maybe just read the last occurence of "Executing testApp wrapper script" and not all?
                        result =  self.lib.readStartUpTimeFromSyslog(self.testConfig, subrack, slot, startTime)
                    else:
                        result =  self.lib.readStartUpTimeFromNotifications(self.testConfig, subrack, slot)
                    if result[0] == 'SUCCESS':
                        startUpTime = result[1]
                        startUpTimes.append(startUpTime)
                if len(startUpTimes) == len(self.testConfig["testNodes"]) and min(startUpTimes) > startTime:
                    restartFlag = True
                    bladesRestartTimes = []
                    for subrack, slot in self.testConfig["testNodes"]:
                        bladesRestartTimes.append(startUpTimes[slot - 1] - startTime)
                    ret = ('SUCCESS', bladesRestartTimes)
                else:
                    misc_lib.waitTime(15)


        # Wait until all components are up
        self.setTestStep('Wait until all components are started')
        while self.timeToQuit > time.time():
            misc_lib.waitTime(60)
            result = self.safLib.checkClusterStatus()
            if re.search('Status OK',result[1]):
                break
            if re.search('cmw-status: command not found',result[1]):
                self.setTestInfo('cmw-status: command not found')
                result = self.sshLib.tearDownHandles()

        if self.timeToQuit < time.time():
            self.fail('ERROR', 'Campaign took longer than %s minutes' % self.campaignTimeout)


        self.myLogger.debug('leave waitForCluster()')
        return ret


def waitForClusterUp(maxWaitTime = 1200):

    nrOfWaitLoops = maxWaitTime / 30
    for i in range(nrOfWaitLoops):
        ssh_lib.tearDownHandles()
        result =  saf_lib.checkClusterStatus()
        if result[0] == 'SUCCESS':
            break
        else:
            misc_lib.waitTime(30)

    return result


def waitForNodeDown(amfNodeName, maxWaitTime = 600):

    logger.info('enter waitForNodeDown')

    nrOfWaitLoops = maxWaitTime / 10

    cmd = 'amf-state node oper safAmfNode=%s,safAmfCluster=myAmfCluster | grep DISABLED' % amfNodeName
    okFlag = False
    for i in range(nrOfWaitLoops):
        ssh_lib.tearDownHandles()
        result =  ssh_lib.sendCommand(cmd)
        if result[0] == 'SUCCESS' and result[1] != '':
            result = (result[0],'node:%s is down' % amfNodeName)
            okFlag = True
            break
        else:
            misc_lib.waitTime(10)

    if okFlag == False:
        result = ('ERROR','%s was not restarted whitin %s s' % (amfNodeName,maxWaitTime))

    logger.info('leave waitForNodeDown')
    return result


def waitForClusterDown(testConfig, maxWaitTime = 600):

    logger.info('enter waitForClusterDown')

    nrOfWaitLoops = maxWaitTime
    controller1 = targetData['ipAddress']['ctrl']['ctrl1']
    controller2 = targetData['ipAddress']['ctrl']['ctrl2']
    cmd = 'ping -c 1 -W 1 %s | grep 100%s' % (controller1,'%')
    if len(testConfig['testNodes']) > 1:
        cmd = cmd + ';ping -c 1 -W 1 %s | grep 100%s' % (controller2,'%')

    okFlag = False
    for i in range(nrOfWaitLoops):
        result = misc_lib.execCommand(cmd)
        if result[0] == 'SUCCESS' and len(re.findall('100% packet loss',result[1])) == 2:
            result = (result[0],'cluster is down')
            okFlag = True
            break
        else:
            misc_lib.waitTime(1)

    if okFlag == False:
        result = ('ERROR','cluster was not restarted whitin %s s' % maxWaitTime)

    logger.info('leave waitForClusterDown')
    return result


def installExtTgen(repo, archive):
    logger.debug('enter installExtTgen')


    ##########  This section should be removed when all GW-pc's are upgraded  START ##############
    #Check if the old format of testApp is installed on gw-pc,
    cmd = 'rpm -qa | grep -i TA_'
    result = ssh_lib.sendCommand(cmd,9,9)
    if result[0] == 'ERROR':
        logger.warn('failed to get rpm list for the external testApp components on gw-pc')

    if  result[1] == []:
        logger.info('no external testApp components, with the old format, are installed on gw-pc')
    else:
        logger.info('Remove of external testApp components, the old format, on gw-pc')
        rpmList = result[1].split()
        for rpm in  rpmList:
            rpm = rpm.strip()
            cmd = 'rpm -e %s' % rpm
            result = ssh_lib.sendCommand(cmd,9,9)
        ##########  This section should be removed when all GW-pc's are upgraded  END ##############


    cmd = 'rpm -qa | grep  Test_App-Tgen'
    result = ssh_lib.sendCommand(cmd,9,9)
    if result[0] == 'ERROR':
        logger.warn('failed to execute rpm list on gw-pc')
        return ('ERROR','failed to execute rpm list on gw-pc')

    installedVersion = result[1]
    reinstallFlag = False
    installed = True
    if installedVersion == '':
        reinstallFlag = True
        installed = False
    else:
        cmd = 'ls  %s | grep %s' % (archive, installedVersion)
        result = misc_lib.execCommand(cmd)
        if result[1] != '':
            logger.info('tgen is up-to-date on the gw-pc')
            return ('SUCCESS','tgen is up-to-date on the gw-pc')
        else:
            reinstallFlag = True

    #install or update external tgen on gw-pc
    if reinstallFlag:
        if installed:
            logger.info('###Remove of external testApp components, the new format, on gw-pc')
            cmd = 'rpm -qa | grep  Test_App-'
            result = ssh_lib.sendCommand(cmd,9,9)
            rpmList = result[1].split()
            rpmList.sort()# NOTE: the tgen must be installed before tgen
            for rpm in  rpmList:
                rpm = rpm.strip()
                cmd = 'rpm -e %s' % rpm
                result = ssh_lib.sendCommand(cmd,9,9)

        logger.info('install the external tgen on gw-pc')
        cmd = 'mkdir /home/test_temp'
        result = ssh_lib.sendCommand(cmd,9,9)
        rpmList = []
        cmd = 'ls  %s | grep Test_App-libs-SAFless' % archive
        result = misc_lib.execCommand(cmd)
        if result[1] != '':
            rpmList.append(result[1])
        cmd = 'ls  %s | grep Test_App-Tgen-SAFless' % archive
        result = misc_lib.execCommand(cmd)
        if result[1] != '':
            rpmList.append(result[1])

        host = targetData['ipAddress']['ctrl']['testpc']
        user = targetData['user']
        passwd = targetData['pwd']
        destpath = '/home/test_temp/'
        for rpm in rpmList:
            file = rpm.strip()
            file1 = '%s%s' % (archive,file)
            ssh_lib.sCopy(file1, host, destpath, user, passwd, timeout = 60)
            cmd = 'rpm -i %s%s' % (destpath,file)
            ssh_lib.sendCommand(cmd,9,9)

        logger.info('Reboot the gw-pc and wait 120s')
        cmd = 'reboot'
        ssh_lib.sendCommand(cmd,9,9)
        misc_lib.waitTime(120)
        for i in range(10):
            cmd = 'hostname'
            result = ssh_lib.sendCommand(cmd,9,9)
            if result[0] == 'SUCCESS' and result[1] != '':
                break
            else:
                misc_lib.waitTime(30)

        cmd = '\\rm -rf /home/test_temp'
        result = ssh_lib.sendCommand(cmd,9,9)

    logger.debug('leave installExtTgen')
    return ('SUCCESS','external tgen is updated on the gw-pc')


def uploadTestAppCompToCxpArchive(repo, archive):

    logger.debug('enter uploadTestAppCompToCxpArchive')

    archive2 = archive + '/new'

    #download the latest testApp version to cxp archive
    cmd = '\\rm -f %s/Test_App*' % archive
    misc_lib.execCommand(cmd)
    cmd = '\\rm -f %s/Test_App*' % archive2
    misc_lib.execCommand(cmd)

    testAppBundles = []
    testAppBundles.append('Test_App-Tgen-SAFless-*.x86_64.rpm')
    testAppBundles.append('Test_App-libs-SAFless-*.x86_64.rpm')
    testAppBundles.append('Test_App*schema_upgrade.sdp')

    #tgen, libs, schema upgrade
    for bundle in testAppBundles:
        cmd = '\cp %s/apps/testApp/release/%s %s' % (repo, bundle, archive)
        result = misc_lib.execCommand(cmd)
        if result[0] == 'SUCCESS':
            res = ('SUCCESS','All testApp components are uploaded to cxp_archive')
        else:
             res = ('ERROR','Failed to upload the testApp components to  cxp_archive')

    #testapp
    cmd = '\cp %s/apps/testApp/release/Test_App*64.sdp %s/Test_App.sdp' % (repo, archive)
    result = misc_lib.execCommand(cmd)
    if result[0] == 'SUCCESS':
        res = ('SUCCESS','All testApp components are uploaded to cxp_archive')
    else:
         res = ('ERROR','Failed to upload the testApp components to  cxp_archive')

    #testapp upgrade
    cmd = '\cp %s/apps/testApp/release/Test_App*64.upgrade.sdp %s/Test_App.sdp' % (repo, archive2)
    result = misc_lib.execCommand(cmd)
    if result[0] == 'SUCCESS':
        res = ('SUCCESS','All testApp components are uploaded to cxp_archive')
    else:
         res = ('ERROR','Failed to upload the testApp components to  cxp_archive')

    logger.debug('leave uploadTestAppCompToCxpArchive')
    return res

def getComponentVersion(compCxpNumber = 'CXP9017697'): # default for SLES

    cmd = "cmw-repository-list | grep Used | grep -v NotUsed | grep '%s'" %compCxpNumber

    """
    Example for COM SA:  ERIC-ComSa-CXP9017697_3-R4A09
        release number is 3
        version number is R4A09
        majorVersion is 4
    """

    release = ''
    Version = ''
    majorVersion = ''

    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        return result
    if 'command not found' in result[1]:
        return ('ERROR', 'Not possible to interpret result for checking version of component %s. Result was: %s' %(compCxpNumber, result[1]))
    if len(result[1].splitlines()) == 1:
        relevantLine = result[1].split()[0]
    else:
        relevantLines = []
        for line in result[1].splitlines():
            if 'WARNING: ' not in line:
                relevantLines.append(line)
        if len(relevantLines) != 1:
            return ('ERROR', 'Not possible to interpret result for checking version of component %s. Result was: %s' %(compCxpNumber, result[1]))
        relevantLine = relevantLines[0]

    product = relevantLine.split()[0]
    release = product.split('-')[2].split('_')[1]
    Version = product.split('-')[3]
    majorVersion = Version[1]

    if release == '' or Version == '' or majorVersion == '':
        return ('ERROR', 'Found release number or version or majorVersion to be empty. Release: %s. Version: %s. Major version: %s' %(release, Version, majorVersion))
    logger.info('getComponentVersion leave: release(%s) Version(%s) majorVersion(%s)' %(release, Version, majorVersion))
    return ('SUCCESS', release, Version, majorVersion)

def getInstallationLevel():
    """
    Installation level 1 means only CMW is installed
    Installation level 2 means CMW and COM are installed
    Installation level 3 means CMW, COM and COM SA are installed
    """
    logger.debug("enter lib.getInstallationLevel")
    installationLevel = 0
    cmd = "cmw-repository-list | grep Used | grep -v NotUsed"
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug("leave lib.getInstallationLevel")
        return result

    if 'CXP9017566' in result[1]: # COREMW_COMMON CXP number
        installationLevel = 1
    if 'CXP9017585' in result[1]: # COM CXP number
        installationLevel = 2
    if 'CXP9026454' in result[1]: # COM for RHEL CXP number
        installationLevel = 2
    if 'CXP9017697' in result[1]: # ComSa CXP number
        installationLevel = 3
    if 'CXP9028073' in result[1]: # ComSa CXP number RHEL
        installationLevel = 3
    logger.info("lib.getInstallationLevel returns installation level: %d" %installationLevel)
    logger.debug("leave lib.getInstallationLevel")
    return ('SUCCESS', installationLevel)

def tokeniseVersion(version):
    """
    Assuming that the version format is [letter, numbers, letter, numbers]
    """
    versionlist = []
    for i, c in enumerate(version):
        if i == 0:
            versionlist.append(c);
        elif c.isalpha():
            minorLetterPos = i;
    versionlist.append(version[1:minorLetterPos])
    versionlist.append(version[minorLetterPos])
    versionlist.append(version[minorLetterPos+1:])
    logger.debug('tokeniseVersion %s %s'% (version, versionlist))
    return versionlist

def checkComponentVersion(component, reqRelease, reqVersion, offlineVersion = []):
    """
    reqRelease and reqVersion are strings.
    reqRelease is the required release number
    reqVersion is the required version number, see example below

    Example for COM SA:  ERIC-ComSa-CXP9017697_3-R4A09
        release number is 3
        version number is R4A09
    """
    # TODO: need implement check version for RHEL
    result = getLinuxDistro()
    if result[0] == 'SUCCESS' and result[1] == 'RhelType':
        logger.debug('RHEL detected, skip checkComponentVersion')
        return ('SUCCESS', True)
    logger.debug('enter checkComponentVersion')

    lookFor = getComponentProductNumber(component)
    if (lookFor == 'ERROR'):
        return ('ERROR','checkComponentVersion only handles "comsa", "com" and "cmw" as arguments')

    if len(offlineVersion) == 0:
        result = getComponentVersion(lookFor)
        if result[0] != 'SUCCESS':
            return result
        release = result[1]
        Version = result[2]
    elif len(offlineVersion) == 3:
        logger.debug('offlineVersion case')
        release = offlineVersion[0]
        Version = offlineVersion[1]
    else:
        return ('ERROR','checkComponentVersion called with wrong offlineVersions (%s)' %str(offlineVersion))

    logger.debug('checkComponentVersion reqRelease %s reqVersion %s release %s Version %s'%(reqRelease, reqVersion, release, Version))
    reqVerList = tokeniseVersion(reqVersion)
    verList = tokeniseVersion(Version)

    #Compare release and version number with the expected  the five characters in the version number (the last set of numbers together)
    res = True
    if verList[0] == 'P':
        if ord(release) < ord(reqRelease):
            res = False
        elif ord(release) > ord(reqRelease):
            res = True
        elif int(verList[1]) < int(reqVerList[1]):
            res = False
    elif verList[0] == 'R':
        if ord(release) < ord(reqRelease):
            res = False
        elif ord(release) > ord(reqRelease):
            res = True
        elif int(verList[1]) < int(reqVerList[1]):
            res = False
        elif int(verList[1]) > int(reqVerList[1]):
            res = True
        elif ord(verList[2]) < ord(reqVerList[2]):
            res = False
        elif ord(verList[2]) > ord(reqVerList[2]):
            res = True
        elif int(verList[3]) < int(reqVerList[3]):
            res = False
    else:
        return ('ERROR','Version number does not begin with R or P!')

    if res == False:
        logger.error('Current version: (%s, %s). Expected at least: (%s, %s) ' %(release, Version, reqRelease, reqVersion))
    logger.debug('leave checkComponentVersion')
    return ('SUCCESS', res)

def checkExactComponentVersion(component, reqRelease, reqVersion, offlineVersion = []):
    """
    reqRelease and reqVersion are strings.
    reqRelease is the required release number
    reqVersion is the required version number, see example below

    Example for COM SA:  ERIC-ComSa-CXP9017697_3-R4A09
        release number is 3
        version number is R4A09
    """
    logger.debug('enter checkExactComponentVersion')

    lookFor = getComponentProductNumber(component)
    if (lookFor == 'ERROR'):
        return ('ERROR','checkExactComponentVersion only handles "comsa", "com" and "cmw" as arguments')

    if len(offlineVersion) == 0:
        result = getComponentVersion(lookFor)
        if result[0] != 'SUCCESS':
            return result
        release = result[1]
        Version = result[2]
    elif len(offlineVersion) == 3:
        logger.debug('offlineVersion case')
        release = offlineVersion[0]
        Version = offlineVersion[1]
    else:
        return ('ERROR','checkExactComponentVersion called with wrong offlineVersions (%s)' %str(offlineVersion))

    #Compare release and version number with the expected five characters in the version number (the last set of numbers together)
    if Version[0] == 'P' or Version[0] == 'R':
        if ord(release) ==  ord(reqRelease) and Version == reqVersion:
            res = True
        else:
            res = False
    else:
        return ('ERROR','Version number does not begin with R or P!')

    if res == False:
        logger.warn('Current version: (%s, %s). Expected exactly: (%s, %s) ' %(release, Version, reqRelease, reqVersion))
    logger.debug('leave checkExactComponentVersion')
    return ('SUCCESS', res)

def checkObsoleteComponentVersion(component, obsRelease, obsVersion):
    """
    obsRelease and obsVersion are strings.
    obsRelease is the obsolete release number
    obsVersion is the obsolete version number, see example below

    Example for COM SA:  ERIC-ComSa-CXP9017697_3-R4A09
        release number is 3
        version number is R4A09
    """
    # TODO: need implement check version for RHEL
    logger.debug('enter checkObsoleteComponentVersion')
    lookFor = getComponentProductNumber(component)
    if (lookFor == 'ERROR'):
        return ('ERROR','checkObsoleteComponentVersion only handles "comsa", "com" and "cmw" as arguments')

    result = getComponentVersion(lookFor)
    if result[0] != 'SUCCESS':
        return result
    release = result[1]
    Version = result[2]

    #Compare release and version number with the expected  the five characters in the version number (the last set of numbers together)
    res = False
    if ord(release) < ord(obsRelease):
        res = True
    elif Version[0] == 'R' or Version[0] == 'P':
        if Version[1] < obsVersion[1]:
            res = True
        elif Version[1] == obsVersion[1]:
            if ord(Version[2]) < ord(obsVersion[2]):
                res = True
            elif ord(Version[2]) == ord(obsVersion[2]):
                if  int(Version[3:]) < int(obsVersion[3:]):
                    res = True
    else:
        return ('ERROR','Version number does not begin with R or P!')

    if res == False:
        logger.error('checkObsoleteComponentVersion Current version: (%s, %s). Expected at least: (%s, %s) ' %(release, Version, obsRelease, obsVersion))
    logger.debug('leave checkObsoleteComponentVersion')
    return ('SUCCESS', res)

def checkComponentMajorVersion(component, reqRelease, reqMajorVersion, offlineVersion = [], noError = False):
    """
    reqRelease and reqVersion are strings.
    reqRelease is the required release number
    reqVersion is the required version number, see example below

    Example for COM SA:  ERIC-ComSa-CXP9017697_3-R4A09
        release number is 3
        reqMajorVersion number is 4 (from R4A09)
    """
    # TODO: need implement check version for RHEL
    result = getLinuxDistro()
    if result[0] == 'SUCCESS' and result[1] == 'RhelType':
        logger.debug('RHEL detected, skip checkComponentMajorVersion')
        return ('SUCCESS', True)

    logger.debug('enter checkComponentMajorVersion')
    lookFor = getComponentProductNumber(component)
    if (lookFor == 'ERROR'):
        return ('ERROR','checkComponentMajorVersion only handles "comsa", "com" and "cmw" as arguments')

    if len(offlineVersion) == 0:
        result = getComponentVersion(lookFor)
        if result[0] != 'SUCCESS':
            return result
        release = result[1]
        majorVersion = result[3]
    elif len(offlineVersion) == 3:
        logger.debug('offlineVersion case')
        release = offlineVersion[0]
        majorVersion = offlineVersion[2]
    else:
        return ('ERROR','checkComponentMajorVersion called with wrong offlineVersions (%s)' %str(offlineVersion))

    #Compare release and version number with the expected  the five characters in the version number (the last set of numbers together)
    res = True
    if ord(release) < ord(reqRelease):
        res = False
    elif ord(release) > ord(reqRelease):
        res = True
    elif int(majorVersion) < int(reqMajorVersion):
        res = False

    if res == False:
        if noError == True:
            logger.warn('Current version: (%s, %s). Expected at least: (%s, %s) ' %(release, majorVersion, reqRelease, reqMajorVersion))
        else:
            logger.error('Current version: (%s, %s). Expected at least: (%s, %s) ' %(release, majorVersion, reqRelease, reqMajorVersion))
    logger.debug('leave checkComponentMajorVersion')
    return ('SUCCESS', res)

def getComponentProductNumber(component):
    productNumber = 'ERROR'
    if component == 'comsa':
        productNumber = 'CXP9017697'
        result = getLinuxDistro()
        if result[0] == 'SUCCESS' and result[1] == 'RhelType':
            productNumber = 'CXP9028073'
    elif component == 'com':
        productNumber = 'CXP9017585'
        result = getLinuxDistro()
        if result[0] == 'SUCCESS' and result[1] == 'RhelType':
            productNumber = 'CXP9026454'
    elif component == 'cmw':
        productNumber = 'CXP9017566'
        # TODO: product number for CMW in RHEL
    return productNumber

def checkComponentMajorVersionFromSdp(component, pathToComponent, reqRelease, reqMajorVersion, noError = False):
    """
    reqRelease and reqVersion are strings.
    reqRelease is the required release number
    reqVersion is the required version number, see example below

    Example for COM SA:  ERIC-ComSa-CXP9017697_3-R4A09
        release number is 3
        reqMajorVersion number is 4 (from R4A09)
    """
    logger.debug('enter checkComponentMajorVersionFromSdp')
    if component == 'comsa':
        cmd = 'tar tf %s | grep rpm' %pathToComponent
        result = misc_lib.execCommand(cmd)
        product = result[1].split()[0].split('.')[0]

        release = product.split('-')[1].split('_')[1]
        Version = product.split('-')[2]
        majorVersion = Version[1]

        #Compare release and version number with the expected  the five characters in the version number (the last set of numbers together)
        res = True
        if ord(release) < ord(reqRelease):
            res = False
        elif ord(release) > ord(reqRelease):
            res = True
        elif int(majorVersion) < int(reqMajorVersion):
            res = False

        if res == False:
            if noError == True:
                logger.warn('Current version: (%s, %s). Expected at least: (%s, %s) ' %(release, majorVersion, reqRelease, reqMajorVersion))
            else:
                logger.error('Current version: (%s, %s). Expected at least: (%s, %s) ' %(release, majorVersion, reqRelease, reqMajorVersion))
        logger.debug('leave checkComponentMajorVersionFromSdp')
        return ('SUCCESS', res)
    #TODO: implement for com and coremw components if need

    return ('SUCCESS', [])

def isDateMoreRecent(dateString1, dateString2):
    '''
    The dateString has to be specified in the format of the syslog (that is "month day hour:minute:second").
    The purpose of this method is to support the getEventTimeStamp method so that we compare the times read from syslog
    with this method instead of running the timeConv method which executes a date command on the local linux machine

    Returns
    ('ERROR', 'Some relevant error message')
    ('SUCCESS', True) if the date defined by dateString2 is more recent or equal to the date defined by dateString1
    ('SUCCESS', False) if the date defined by dateString2 is older than the date defined by dateString1
    '''

    result = ('ERROR', 'Method not executed correctly')

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    month1 = months.index(dateString1.split()[0])
    month2 = months.index(dateString2.split()[0])
    if month1 < month2:
        result = ('SUCCESS', True)
    elif month1 > month2:
        result = ('SUCCESS', False)
    else:
        day1 = int(dateString1.split()[1])
        day2 = int(dateString2.split()[1])
        if day1 < day2:
            result = ('SUCCESS', True)
        elif day1 > day2:
            result = ('SUCCESS', False)
        else:
            hour1 = int(dateString1.split()[2].split(':')[0])
            hour2 = int(dateString2.split()[2].split(':')[0])
            if hour1 < hour2:
                result = ('SUCCESS', True)
            elif hour1 > hour2:
                result = ('SUCCESS', False)
            else:
                minute1 = int(dateString1.split()[2].split(':')[1])
                minute2 = int(dateString2.split()[2].split(':')[1])
                if minute1 < minute2:
                    result = ('SUCCESS', True)
                elif minute1 > minute2:
                    result = ('SUCCESS', False)
                else:
                    second1 = int(dateString1.split()[2].split(':')[2])
                    second2 = int(dateString2.split()[2].split(':')[2])
                    if second1 <= second2:
                        result = ('SUCCESS', True)
                    elif second1 > second2:
                        result = ('SUCCESS', False)

    return result

def powerReset(testConfig,targetData, subrack = 0,slot = 0):
    '''
    Power reset of node or cluster via IPMI interface. If the cluster has no IPMI
    support, then reboot -f is executed on the node.


    Arguments:
    dict(targetData) int(subrack), int(slot)

    Returns:
    ('SUCCESS','node x restarted') or
    ('ERROR', 'Failed to do power reset of node x')

    NOTE:
    slot and subrack have the default value 0, means all nodes.
    '''

    targetType = ''
    command = ''

    if re.search('sun',targetData['targetType']) or re.search('cots',targetData['targetType']):
        targetType = 'hw'
    else:
        targetType = 'virtualized'

    if subrack != 0 and slot != 0:
        if targetType == 'hw':
            blade = 'blade_%d_%d' %(subrack, slot)
            ssh_lib.tearDownBlade(blade)
            cmd = 'ipmitool -I lanplus -U root -P rootroot -H %s chassis power reset' %(targetData['ipAddress']['ipmi'][blade])
            result = ssh_lib.sendCommand(cmd, 9, 9)
        else:
            cmd = 'reboot -f'
            result = ssh_lib.sendCommand(cmd, slot, subrack)
    else:
        if targetType == 'hw':
            for i, v in enumerate(testConfig['testNodes']):
                if testConfig['testNodesTypes'][i] == 'PL':
                    blade = 'blade_%s_%s' % (v[0], v[1])
                    ipmiAddress = targetData['ipAddress']['ipmi'][blade]
                    command = command + "ipmitool -I lanplus -U root -P rootroot -H %s chassis power reset; " % (ipmiAddress)
                    ssh_lib.tearDownBlade(blade) #tear down the blade before power off via gw-pc

            result = ssh_lib.getConfig()

            scBlades = ('blade_2_1', 'blade_2_2')

            if (result[0], result[1]) == (2,1):
                command = command + "ipmitool -I lanplus -U root -P rootroot -H %s chassis power reset; " % \
                                 targetData['ipAddress']['ipmi'][scBlades[1]]
                command = command + "ipmitool -I lanplus -U root -P rootroot -H %s chassis power reset; " % \
                                 targetData['ipAddress']['ipmi'][scBlades[0]]
                result = ssh_lib.sendCommand(command, 9, 9)
            elif (result[0], result[1]) == (2,2):
                command = command + "ipmitool -I lanplus -U root -P rootroot -H %s chassis power reset; " % \
                             targetData['ipAddress']['ipmi'][scBlades[0]]
                command = command + "ipmitool -I lanplus -U root -P rootroot -H %s chassis power reset; " % \
                             targetData['ipAddress']['ipmi'][scBlades[1]]
                result = ssh_lib.sendCommand(command, 9, 9)
            else:
                logger.error('No or erronuous active controller found')
                result = ('ERROR','No or erronuous active controller found')

        else:
            logger.warn('reboot -f of all nodes in the cluster is not implemented')
            result = ('ERROR','reboot -f of all nodes in the cluster is not implemented')


    return result



def lockSU(suDN):

    cmd = 'amf-adm lock %s' % suDN
    result = ssh_lib.sendCommand(cmd)

    return result


def unlockSU(suDN):

    cmd = 'amf-adm unlock %s' % suDN
    result = ssh_lib.sendCommand(cmd)

    return result



def refreshSshLibHandlesAllSCs(testConfig):
    for controller in testConfig['controllers']:
        ssh_lib.setConfig(controller[0], controller[1], controller[1])
        ssh_lib.setUpBlade('blade_%d_%d'%(controller[0], controller[1]))
        ssh_lib.tearDownHandles()
        ssh_lib.setUpBlade('blade_%d_%d'%(controller[0], controller[1]))


def getLinuxDistro(types = ["Sles11Type", "RhelType", "Sles12Type"]):
    comment = """
    The method currently can recognize SLES (LDEwS) and RedHat (LDEfR)

    If you extend the method to support other distros, please update this comment.
    Returns:
    ('SUCCESS', 'SLES') or
    ('SUCCESS', 'RedHat') or
    ('ERROR', 'Unknown linux distribution found. Command result: %s' %result[1]) or
    ('ERROR', 'some other relevant error message')
    """

    logger.debug('enter getLinuxDistro')
    distroCmd = 'ls /etc/*release'
    result = ssh_lib.sendCommand(distroCmd)

    if result[0] != 'SUCCESS':
        logger.debug('leave getLinuxDistro')
        return result
    if 'SuSE-release' in result[1] and 'redhat-release' not in result[1]:
        cmd = "cat /etc/SuSE-release | grep VERSION | awk '{print $3}'"
        result = ssh_lib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            logger.debug('leave getLinuxDistro')
            return result
        if result[1] == '11':
            ret = ('SUCCESS', types[0])
        else:
            ret = ('SUCCESS', types[2])
        #ret = ('SUCCESS', 'SLES')
    elif 'redhat-release' in result[1] and 'SuSE-release' not in result[1]:
        ret = ('SUCCESS', types[1])
        #ret = ('SUCCESS', 'RedHat')
    else:
        ret = ('ERROR', 'Unknown linux distribution found. "%s" command result: "%s"' %(distroCmd, result[1]))

    logger.debug('getLinuxDistro returns: %s' %str(ret))
    logger.debug('leave getLinuxDistro')
    return ret

def updateLinuxDistroInDictionary(dict, distroTypes, force = False):
    logger.debug('enter updateLinuxDistroToDictionary')
    if not dict.has_key('linuxDistro'):
        dict['linuxDistro'] = {}
        dict['linuxDistro']['types'] = distroTypes
        result = getLinuxDistro(dict['linuxDistro']['types'])
        if result[0] != 'SUCCESS':
            ret = result
        else:
            dict['linuxDistro']['value'] = dict['linuxDistro']['types'][dict['linuxDistro']['types'].index(result[1])]
            ret = ('SUCCESS', dict)
    elif force == True:
        result = getLinuxDistro(dict['linuxDistro']['types'])
        if result[0] != 'SUCCESS':
            ret = result
        else:
            dict['linuxDistro']['value'] = dict['linuxDistro']['types'][dict['linuxDistro']['types'].index(result[1])]
            ret = ('SUCCESS', dict)
    else:
        # The dictionary already contains the Linux distribution, leave it unchanged
        ret = ('SUCCESS', dict)
    if ret[0] == 'SUCCESS' and dict['linuxDistro']['value'] != "":
        logger.info('found Linux distribution: %s' %dict['linuxDistro']['value'])
    logger.debug('leave updateLinuxDistroToDictionary')
    return ret


##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print 'main'
