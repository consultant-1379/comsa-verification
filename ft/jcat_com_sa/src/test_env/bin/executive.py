#!/usr/bin/env jython
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2009 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained
# herein confidential and shall protect the same in whole or in partF
# from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################
import os, sys, re, platform

from junit.textui import TestRunner

from java.io import FileInputStream
from java.util import Properties
from java.lang import System
import omp.tf.misc_lib as misc_lib
import omp.tf.ssh_lib as ssh_lib
#import omp.tf.dataprovider.sshlibdata as sshdata

import string
import signal
import sys
import subprocess
#import select

System.setProperty("catroot", os.getenv("JCAT_FW"))
System.setProperty("extroot", os.getenv("JCAT_EXTENSIONS"))
System.setProperty("ompextroot", os.getenv("JCAT_OMP_EXTENSIONS"))
System.setProperty("ompcmwroot", os.getenv("JCAT_OMP_CORE_MW"))

System.setProperty("log4j.configuration", "file://%s/scripts/log4j.properties" % os.getenv("JCAT_FW"))

from org.apache.log4j import Logger
from org.apache.log4j.spi import RootLogger
from org.apache.log4j import LogManager
from org.apache.log4j import Level

import lib.argumentHandler as ah
import lib.commonUtils as cu
import lib.parameterHandler as ph
import lib.config as config
import omp.target.target_data as target_data

#sys.path.append('/vobs/tspsaf/tools/targetconf/lib')   ##behövs denna då PYTHONPATH är satt?
#import target_data as target_data_trenoll
import target_data_vCluster as target_data_trenoll
import target_data_qemu as target_data_qemu
import booking_lib

##thes are used to create a nonbloking stdin
import java.io.BufferedReader
import java.io.InputStreamReader
import java.lang.System
import time

import test_env.fw.coreTestSuite as coreTestSuite

#dataGuran = sshdata.sshlibdata()

def setTargetHwData(targetHw, optionsPayloads, separator='-'):

    if 'qemu' == targetHw.split('_')[0]:
        data = target_data_qemu.setTargetHwData(targetHw)
    else:
        data = target_data_trenoll.setTargetHwData(targetHw)
    
    #### Adding the data that is missing in trenoll file above
    data['hostnameSeparator'] = separator
    data['runTibsim'] = 'False'
    data['ipmiPwd'] = 'rootroot'
    #### Changing the value of Keys to match JCAT
    data['ctrlBladePattern'] = '(SC[_-]2[_-]\d*.*#\s)'
    data['payloadBladePattern'] = '(PL[_-]2[_-]\d*.*#\s)'
    data['testPcPattern'] = '(gwhost\d+)'
    data['vipTgPattern'] = '(safTg\d+.+#)'
    data['switchDevicePattern'] = '(console>)'


    # if we want to have varying number of PLs:
    #data['physical_size'] = int(optionsPayloads) + 2 # +2 for system controllers
    #temp_blades = []
    #temp_ipmi = []
    #startWith=1
    #if 'cots_target_20B' == targetHw:
    #    startWith=5
    #for bladeNumber in range (int(optionsPayloads) + 2):
    #    temp_blades.append(('blade_2_%s' % str (bladeNumber + 1), '192.168.0.%s' % str(bladeNumber+1)))
    #    temp_ipmi.append(('blade_2_%s' % str (bladeNumber + 1), '192.168.0.%s' % str(bladeNumber + startWith+100)))
    #data['ipAddress']['blades'] = dict(temp_blades)
    #data['ipAddress']['ipmi'] = dict(temp_ipmi)


    target_data.setTargetXmlData(data)
    #dataGuran.initialize()
    return data


def showResult(logDir):
    """
    Show test result in web browser.
    """
    if eval(System.getProperty("displayFirefox")):
        indexFile = "file://" + logDir + "/index.html"
        os.popen3("/usr/bin/firefox " + indexFile)
    
def evaluateTestResults(logDir):
    notPassedCode = 'NP'
    result = misc_lib.execCommand('grep %s "%s/tpt.txt"' %(notPassedCode, logDir))
    if 'TC-' in result[1]:
        returnCode = 2
    else:
        returnCode = 0
    return returnCode 
    
def main(arguments):

    #read the options
    if arguments == []:
        arguments.append('--help')
    print arguments
    
    parser = ah.setup_option_parser()
    options, args = parser.parse_args(args=arguments)

    if options.debug:
        import pydevd;pydevd.settrace()
#       print('Start up in debug mode')
        
    #Define Java properties

    #System.setProperty("sutConfigurationFile", options.config)

    System.setProperty("logdir", options.logdirectory)
    System.setProperty("testname", options.suitename)
    System.setProperty("suiteName", options.suite)

    System.setProperty("hostnameSeparator", options.hostnameSeparator)
    System.setProperty("loadpl", options.loadpl)
    System.setProperty("loadsc", options.loadsc)
    System.setProperty("loadprofile", options.loadprofile)
    System.setProperty("amfNodeNameSeparator", options.amfNodeNameSeparator)
    System.setProperty("clmNodeNameSeparator", options.clmNodeNameSeparator)
    System.setProperty("currentRelease", options.currentRelease)
    
    if options.productSettings == 'coremw':
        testCaseRepository = '/%s/test_env/testcases/coremw/' % options.repository
        testCaseConfRepository = '/%s/test_env/testcases/coremw/parameters/' % options.repository
        testsuiteDirectory = '/%s/test_env/testsuites/coremw/' % options.repository
    else:
        testCaseRepository = '/%s/test_env/testcases/comsa/' % options.repository
        testCaseConfRepository = '/%s/test_env/testcases/comsa/parameters/' % options.repository  
        testsuiteDirectory = '/%s/test_env/testsuites/comsa/' % options.repository   
    System.setProperty("testCaseRepository", testCaseRepository)
    System.setProperty("testCaseConfRepository", testCaseConfRepository)
    System.setProperty("testsuiteDirectory", testsuiteDirectory)

    System.setProperty("singleTestCase", options.singleTestCase)
    System.setProperty("singleTestCaseIterations", options.singleTestCaseIterations)
    System.setProperty("###__TARGET_SYSTEM__###", options.config)
    System.setProperty("nrOfPlNodes", str(options.payloads))
    System.setProperty("nrOfScNodes", str(options.controllers))
    System.setProperty("groupID", options.config) #host name in testStatistics
    System.setProperty("setUpCheck", options.setUpCheck)
    System.setProperty("runTestCheck", options.runTestCheck)
    System.setProperty("tearDownCheck", options.tearDownCheck)
    System.setProperty("hostname", platform.uname()[1])
    System.setProperty("swDirNumber", options.swDirNumber)
    System.setProperty("installSw", options.installSw)
    System.setProperty("buildComSa", options.buildComSa)
    System.setProperty("runStressTool", options.runStressTool)
    System.setProperty("checkCompilerWarn", options.checkCompilerWarn)
    System.setProperty("displayFirefox", options.displayFirefox)
    System.setProperty("resetCluster", options.resetCluster)
    
    #specific parameters for characteristic measurements
    System.setProperty("storeMeas", options.storeMeas)
    System.setProperty("compareMeas", options.compareMeas)


    #just to get access to this option in the  reinstall script
    System.setProperty("reinstallLevel", options.reinstall)
    #Start
    System.setProperty("nodenameLevel", options.nodename)
    #End
    System.setProperty("tracelogLevel", options.tracelogs)
    
    System.setProperty("destinationProfile", options.destinationProfile)
    
    randomSuite = bool(options.randomSuite)
    if randomSuite:
        System.setProperty("randomSuite", options.randomSuite)

    clcTestSuite = bool(options.clcTestSuite)
    if clcTestSuite:
        System.setProperty("clcTestSuite", options.clcTestSuite)

    dbStorage = bool(options.dbStore)
    if dbStorage:
        System.setProperty("logwriters", "se.ericsson.jcat.fw.logging.writers.DbLogWriter2")
        System.setProperty("dbprop","/home/tspsaf/dbProp/logdb.properties")
        #System.setProperty("dbprop","/home/erapeik/dbProp/logdb.properties")#change when we have a web site

    logger = Logger.getLogger('Executive')
    logger.setLevel(Level.toLevel(options.loglevel))
    
     ###PLACE HOLDER FOR SDP1226###
    if options.storeMeas != '':
        misc_lib.setUp()
     #check temp_dir exist or not, if not then make temp dir
        cmd = "test -d /tmp/char;echo $?"
        result = misc_lib.execCommand(cmd)
        if result[1] == '1\n':
            cmd = "mkdir -m 777 /tmp/char/"
            result = misc_lib.execCommand(cmd)
            if result[0] == 'ERROR':
                result = ('ERROR', 'create directory %s FAILED' % dirName)
                logger.error(result[1])
     # check measFileName exist or not, if not then make measFileName
        cmd = "test -f /tmp/char/measData.dat;echo $?"
        result = misc_lib.execCommand(cmd)
        if result[1] == '1\n':
            measFileName = "/tmp/char/measData.dat"
            headingText = "TC-tag;TC-name;value(unit);CMW-tag;LOTC-version;VIP-version;HW;NrOfNodes;Date\n"
            try:
                fdata = open(measFileName, 'w')
                try:
                    fwriter = fdata.write(headingText)
                finally:
                    fdata.close()
            except:
                logger.error("Storing Measurement data to a file failed.")
                sys.exit(0) 
    ###PLACE HOLDER FOR SDP1226 END###  
    

    #create a unique test name

    MY_WORKSPACE=os.getenv('$MY_WORKPACE/../..')
    p1 = subprocess.Popen(["git", "branch"], cwd=MY_WORKSPACE, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '*'], stdin=p1.stdout, stdout=subprocess.PIPE)
    stdoutString = p2.communicate()[0].strip()


    #child_stdin, child_stdout, child_stderr = os.popen3(["git", "branch"], cwd=MY_WORKSPACE])#!!! need to be changed, get git branch instead???
    #stdoutString = child_stdout.read()
    #stderrString = child_stderr.read()
    #child_stdin.close()
    #child_stdout.close()
    #child_stderr.close()
    #if stderrString != "":
    #    logger.error("Linux command result: %s" % stderrString.strip())
    #    sys.exit(0)
    if len(stdoutString) == 0:
        logger.error("ERROR: Not possible to get current stream/branch.")
        sys.exit(1)
    currView = stdoutString.lstrip('* ')

    if options.singleTestCase != '':
        System.setProperty("name",  'CMW-' + '%s-%s' % (currView, options.definedTestName)) #test suite name in testStatistics
    else:
        System.setProperty("name", 'CMW-' + '%s-%s' % (currView,options.definedTestName)) #test suite name in testStatistics


    #create a unique test name

    # set targetHardware name in target_data and create target_data.data
    print options.config
    if (re.search('.xml', options.config)):
        logger.error("Target error. Please remove the extension '.xml' in --config and try again. ex: cots_target_22 ")
        sys.exit(1)
    elif re.search('No target booked', options.config):
        logger.error("No target booked from this machine. Please use --config")
        sys.exit(1)
    elif re.search('cots_target', options.config) or re.search('sun_target', options.config) or re.search('essim_target', options.config) or re.search('vbox_target', options.config) or re.search('qemu_target', options.config):
        setTargetHwData(options.config, options.payloads, options.hostnameSeparator)
    else:
        logger.error("Not a valid target. Please check the value of parameter: --config")
        sys.exit(1)
    
    # new python implementation:
    
    TIMEOUT = 60
    s = 'Y'    
    
    def interrupted(signum, frame):
        print 'Quit - timed out!'
        sys.exit(1)
    
    def input():
        try:
            print 'You have %s seconds to make your choice...' % TIMEOUT
            foo = raw_input()
            return foo
        except:
            return
    
    print
    print "Checking that you're running on a Node that you've booked..."
    
    if (booking_lib.bookedByCurrentUser(options.config)):
        print
        print "You are - have a nice day! :)"
    elif 'vbox' == options.config.split('_')[0]:
        print
        print "Oops running a vbox, lets hope it works"
    elif 'qemu' == options.config.split('_')[0]:
        print
        print "Oops running a qemu, lets hope it works"
    else:
        #misc_lib.setUp()
        print "You are trying to run a test on a Node that you haven't booked!"
        print "Node Name: %s" % options.config
        #cmd = "grep %s /home/tspsaf/public_html/test_env/node_booking/node_bookings | awk '{print $2}'" % options.config
        #result = misc_lib.execCommand(cmd)
        #print "Booked by: %s" % result[1]
        #print "Last run: %s" % booking_lib.getLastTestRun(options.config)
        print "Would you like to continue? Y/[N]"
        
        signal.signal(signal.SIGALRM, interrupted)
        signal.alarm(TIMEOUT)        
        s = input()        
        signal.alarm(0)
        s = s.upper()
        
        if (s == "Y" or s == "YES"):
            warningString = 'OK, I hope you know what you are doing!!!'
            warningLine = len(warningString)*'*'
            print warningLine
            print warningString
            print warningLine
        elif(s == "N" or s == "NO" or s == ""):
            print "Quit - requested by user"
            sys.exit(1)
        else:
            print "Invalid input: \"%s\"" % s
            sys.exit(1)
                
    print
    
    """
    # old java implementation:
    
    #verefies if we are booked to to target
    print "verifying that you are running on a node booked by you...."

    ## when a node is booked on no one, then it throws exception
    query = True
    try:
        if (booking_lib.bookedByCurrentUser(options.config)):
            print "you are, have a nice day :)"
            query = False
    except:
        pass

    #Query users that are not booked to the node to continue
    if (query):

        #create a java nonblocking stdin reader... NO there aren't any one available in python :/
        input = java.io.InputStreamReader(java.lang.System.in)
        br = java.io.BufferedReader(input)

        TIME = 60*5
        done = False
        while not done:
            print "You are trying to run a test on a Node you are not booked on"
            print "Node Name: %s" % options.config
            print "booked by: %s" % "(not implemented... complain to Lenart :) )"
            print "Last run: %s" % booking_lib.getLastTestRun(options.config)
            print "would you like to continue Yes/[No] "

            count = 0
            while not br.ready():
                time.sleep(1)
                count = count + 1

                #if we time out we quit this as if the user answer Yes
                if(TIME < count):
                    print 'timed out we continue any way....'
                    done = True
                    break

            #red keyboard and interpret answer
            if (br.ready()):
                key_input = br.readLine();
                key_input = key_input.upper()

                if (key_input == "Y" or key_input == "YES"):
                    print 'ok, I hope you know what you are doing!!!'
                    done = True
                elif(key_input == "N" or key_input == "NO" or key_input == ""):
                    print "quit, request by user"
                    sys.exit(1)
                else:
                    print "invalid input: \"%s\"" % key_input

                print
                print
                print
        ##end While True
    ##end if (query):

    """

    if options.loglevel == "": # set the default logLevel
        options.loglevel = "INFO"
    System.setProperty("jcat.logging", options.loglevel)
    rootLogger = RootLogger(Level.toLevel(options.loglevel))
    rootLogger.setLevel(Level.toLevel(options.loglevel))


    if options.singleTestCase != '':
        if (len(options.singleTestCase) < 4 or
            options.singleTestCase[0:3] != "TC-"):
            logger.error('ERROR: The test case must be specified with "TC-" ' +
                         'followed by a number.')
            sys.exit(1)
        suiteDir = System.getProperty("testsuiteDirectory")
        suite = '%s%s' % (suiteDir, "singleTestCaseSuite.xml")
        tmpSuite = '%s%s' % (suiteDir, "tmpSingleTestCaseSuite.xml")
        result = os.system('\\rm -f %s' % tmpSuite)
        if options.controllers == 1:
            result = os.system('sed -e "s/,\'ctrl2\'//" %s > %s' % (suite, tmpSuite))
        else:
            result = os.system('\cp -f %s %s' % (suite, tmpSuite))
        suite = tmpSuite
        os.system('chmod +w %s' %suite)
        tcNumber = options.singleTestCase.split("-")
        tcNumber = tcNumber[1] + '_' + tcNumber[2]
        child_stdin, child_stdout, child_stderr = os.popen3(
            "cd " + testCaseConfRepository + " && ls *" + tcNumber +
            "*.xml")
        stdoutString = child_stdout.read()
        stderrString = child_stderr.read()
        child_stdin.close()
        child_stdout.close()
        child_stderr.close()
        if stderrString != "":
            logger.error("Linux command result: %s" % stderrString.strip())
            sys.exit(0)
        if len(stdoutString) == 0:
            logger.error("ERROR: The test case could not be found.")
            sys.exit(1)
        tcConfigFile = stdoutString.strip()
        appendTcSpecificTextInTestSuiteFile = """    <testcase1>
        <tag>%s</tag>
        <config>%s</config>
        <useDefaultSuiteCheck>True</useDefaultSuiteCheck>
        <key></key>
        <iter>%s</iter>
        <assertOnError>true</assertOnError>
    </testcase1>
</testsuite>""" % (options.singleTestCase, tcConfigFile, options.singleTestCaseIterations)
        try:
            fdata = open(suite, 'a')
            try:
                fwriter = fdata.write(appendTcSpecificTextInTestSuiteFile)
            finally:
                fdata.close()
        except:
            logger.error("Appending test case specific data to generic test suite failed.")
            sys.exit(0)
    else:
        suiteDir = System.getProperty("testsuiteDirectory")
        suite = '%s%s' % (suiteDir, options.suite)
   
    #Start
    # Check that the length of hostnames does not exceed maximum characters
    if  options.nodename != '':
        nodeName = options.nodename
        nrOfSc = options.controllers
        nrOfPl = options.payloads 
        for cnt in range(nrOfSc):              
               SCname = "SC-%s-%u" % (nodeName,cnt+1)
               if len(SCname) > 55 :
                  logger.error('ERROR: The length of nodename %s should be less than 56' % SCname)
                  sys.exit(1)
        for cnt in range(nrOfPl):
               cnt = cnt + 2
               PLname = "PL-%s-%u" % (nodeName, cnt+1)
               if len(SCname) > 55 :
                  logger.error('ERROR: The length of nodename %s should be less than 56' % PLname)
                  sys.exit(1)
   # End
    
    SUT_config = "%s%s%s" % (options.repository, options.config_dir, options.config)
    test_config = "%s%s%s" % (options.repository, options.testConfig_dir, options.testConfig)

    logger.debug(">>>>>> Configuration data <<<<<<<<")
    logger.debug("TestSuite config used: %s" % suite)
    # logger.debug("SUT config used: %s" % SUT_config ) # This is not used any more. The trget_data from OMPSAF3.0 is used instead.
    logger.debug("Test Config used: %s" % test_config)
    logger.debug(">>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<")

    try:
        #get test suite configuration
        ph.fixSuite(suite)
        testSuiteConfig = ph.getXmlConfig(suite)
    except Exception, err:
        logger.error('\n ERROR: exception in testSuiteConfig : %s \n' % str(err))
        sys.exit(1)

    # This is a hack to be able to use the existing test suites for single node configuration
    if System.getProperty("nrOfScNodes") == '1' and testSuiteConfig['defaultSuiteCheck']['setup']['interfaces']['interfaces'] == "['ctrl1','ctrl2']":
        testSuiteConfig['defaultSuiteCheck']['setup']['interfaces']['interfaces'] = "['ctrl1']"
    if System.getProperty("nrOfScNodes") == '1' and testSuiteConfig['defaultSuiteCheck']['runtest']['interfaces']['interfaces'] == "['ctrl1','ctrl2']":
        testSuiteConfig['defaultSuiteCheck']['runtest']['interfaces']['interfaces'] = "['ctrl1']"
    if System.getProperty("nrOfScNodes") == '1' and testSuiteConfig['defaultSuiteCheck']['teardown']['interfaces']['interfaces'] == "['ctrl1','ctrl2']":
        testSuiteConfig['defaultSuiteCheck']['teardown']['interfaces']['interfaces'] = "['ctrl1']"
    #End of hack
    
    #populate test cases
    testConfig = config.getConfig(options.controllers , options.payloads, test_config)
    testCasesInstances = cu.populateTestCases(testSuiteConfig, testConfig, options.randomSuite, options.clcTestSuite)

    #Set/get the suite for unit test
    testSuite = coreTestSuite.CoreTestSuite(Level.toLevel(options.loglevel))
    test = testSuite.suite(testCasesInstances)

    #run the suite
    booking_lib.logUsage(options.config)
    runner = TestRunner()
    runner.run(test)

    logDir = System.getProperty("logdir")
    
    if str(options.openReport) == 'True':
        showResult(logDir)

    returnCode = evaluateTestResults(logDir)

    sys.exit(returnCode)

if __name__ == "__main__":
    main(sys.argv[1:])
