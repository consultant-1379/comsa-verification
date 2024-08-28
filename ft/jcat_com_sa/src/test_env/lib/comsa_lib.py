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

   Author: ejnolsz

   Description: A collection of methods specific to COM SA functionality.

'''

#############IMPORT##################

from org.apache.log4j import Logger
from java.lang import System
from random import randint
import os
import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException
import omp.tf.ssh_lib as ssh_lib
import omp.tf.hw_lib as hw_lib
import omp.tf.misc_lib as misc_lib
import test_env.lib.lib as lib
import test_env.lib.utils as utils
import coremw.saf_lib as saf_lib
import re
import time
import copy
# add a comment line
#############GLOBALS##################


logger = None
targetData = None
MY_REPOSITORY = os.environ['MY_REPOSITORY']

#############exceptions#############



#############setUp / tearDown#############

def setUp(logLevel,currentSut):

    global logger
    global targetData

    # Variables needed for the build token management
    global dirName
    global user
    global tokenPattern
    global suiteLogDir
    global numberOfGetTokenRetries
    global swDirGlobal

    dirName = System.getProperty("logdir")
    user = os.environ['USER']
    tokenPattern = 'buildToken-%s' %user
    suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
    numberOfGetTokenRetries = 5
    swDirGlobal = System.getProperty("swDirNumber")

    logger = Logger.getLogger('comsa_lib')
    logger.setLevel(logLevel)

    logger.info("comsa_lib: Initiating!")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    return


def tearDown():
    #logger_lib.logMessage("lib: Bye bye !!", logLevel='debug')
    logger.debug("comsa_lib: bye, bye!")
    return


#############lib functions#############

def comRestart(self, subrack, slot, valgrindEnabled, waitTime = 10, charMeasurement = False, failoverTest = False, noPidExpectedAfterRestart = False, calcStartStopTimes = False):
    """This method should be used to restart the COM process
    valgrindEnabled has to be either True or False (logical values, not strings)
    """
    # check if running code coverage
    coverageEnabled = False
    if self.testSuiteConfig.has_key('codeCoveredCheck'):
        coverageEnabled = eval(self.testSuiteConfig['codeCoveredCheck']['codeCoveredCheck'])


    logger.debug("enter comsa_lib: comRestart")

    # Check PID of COM process before the restart
    #result = getProcessId(subrack, slot, 'com')
    result = getProcessId(subrack, slot, 'com', '/etc/com.cfg')
    if result[0] != 'SUCCESS':
        logger.debug("leave comsa_lib: comRestart")
        return ('ERROR', 'Could not get a PID for the COM process. %s' %result[1])
    elif 'list' in str(type(result[1])):
        logger.debug("leave comsa_lib: comRestart")
        return ('ERROR', 'More than one PID found for the COM process. This is not handled now. %s' %result[1])

    pidBeforeRestart = result[1]
    comRestartCommand = ''
    comRestartCommand2= ''
    if charMeasurement:
        comRestartCommand += 'date +%s; '
    if valgrindEnabled:
        comRestartCommand += 'kill -1 %s' %pidBeforeRestart
    elif coverageEnabled:
        comRestartCommand += 'amf-adm -t 120 lock safSu=Cmw1,safSg=2N,safApp=ERIC-ComSa;amf-adm -t 120 lock-in safSu=Cmw1,safSg=2N,safApp=ERIC-ComSa;amf-adm -t 120 lock safSu=Cmw2,safSg=2N,safApp=ERIC-ComSa;amf-adm -t 120 lock-in safSu=Cmw2,safSg=2N,safApp=ERIC-ComSa;'
        comRestartCommand2 += 'amf-adm -t 120 unlock-in safSu=Cmw1,safSg=2N,safApp=ERIC-ComSa;amf-adm -t 120 unlock safSu=Cmw1,safSg=2N,safApp=ERIC-ComSa;amf-adm -t 120 unlock-in safSu=Cmw2,safSg=2N,safApp=ERIC-ComSa;amf-adm -t 120 unlock safSu=Cmw2,safSg=2N,safApp=ERIC-ComSa'
    elif failoverTest:
        comRestartCommand += 'kill -9 %s' %pidBeforeRestart
    else:
        comRestartCommand += 'comsa-mim-tool com_switchover'

    result = getCurrentUnixTimeOnTarget()
    if result[0] != 'SUCCESS':
        logger.debug("leave comsa_lib: comRestart")
        return('ERROR', 'COM restart command not successful: %s' %result[1])
    startTime = result[1]

    # Restart COM
    if coverageEnabled:
        logger.debug('Set time out for Coverage')
        ssh_lib.setTimeout(300, subrack, slot)
    else:
        ssh_lib.setTimeout(90, subrack, slot)

    result = ssh_lib.sendCommand(comRestartCommand, subrack, slot)
    if result[0] != 'SUCCESS':
        logger.debug("leave comsa_lib: comRestart")
        return('ERROR', 'COM restart command not successful: %s' %result[1])

    if coverageEnabled:
        misc_lib.waitTime(5)
        logger.debug('Set time out for Coverage')
        ssh_lib.setTimeout(300, subrack, slot)
        result = ssh_lib.sendCommand(comRestartCommand2, subrack, slot)
        if result[0] != 'SUCCESS':
            logger.debug("leave comsa_lib: comRestart")
            return('ERROR', 'COM restart command not successful: %s' %result[1])

    """
    if not valgrindEnabled:
        if 'COM - Stop' and 'COM - Starting with configuration' in result[1]:
            logger.debug('Expected printouts at COM restart received')
        else:
            logger.debug("leave comsa_lib: comRestart")
            return('ERROR', '"COM - Stop" or "COM - Starting with configuration" not received in the printout of the COM restart command: %s' %result[1])
    """

    if charMeasurement:
        restartTime = result[1].splitlines()[0]


    if valgrindEnabled:
        waitTime*=18

    if  self.installStressTool:
        waitTime*=20
        logger.debug("comsa_lib: comRestart: increasing the wait time to %s since stress is enabled" %waitTime)

    misc_lib.waitTime(waitTime)

    """
    This part is added in order to gather characteristics data about COM SA start/stop times.
    """

    if calcStartStopTimes:
        result = verifyComSaSupportReadingStartStopTimes()
        if result == ('SUCCESS', True):
            calculateSysDependentComSaStartStopTimes(self, subrack, slot, startTime, self.testConfig, failoverTest)
            calculatePureComSaStartStopTimes(self, subrack, slot, startTime, self.testConfig, failoverTest)


    """
    End of part added for characteristics measurements
    """

    # Check that the COM process has a new PID
    # Alternative way to get the PID:
    # result = getProcessId(subrack, slot, 'com')
    if noPidExpectedAfterRestart == False:
        result = getProcessId(subrack, slot, 'com', '/etc/com.cfg')
        if result[0] != 'SUCCESS':
            logger.debug("leave comsa_lib: comRestart")
            return ('ERROR', 'Could not get a PID for the COM process. %s' %result[1])
        pidAfterRestart = result[1]
        if pidBeforeRestart == pidAfterRestart:
            logger.debug("leave comsa_lib: comRestart")
            return ('ERROR', 'The COM process did not get a new PID. pidBeforeRestart: %d, pidAfterRestart: %d' %(pidBeforeRestart, pidAfterRestart))
        elif 'list' in str(type(pidAfterRestart)):
            logger.debug("leave comsa_lib: comRestart")
            return ('ERROR', 'More than one PID found for the COM process. This was not expected. %s' %result[1])
        else:
            logger.debug("leave comsa_lib: comRestart")
            if charMeasurement:
                return ('SUCCESS', pidAfterRestart, 'COM process was restarted')
            else:
                return ('SUCCESS', pidAfterRestart, 'COM process was restarted')
    else:
        logger.debug("leave comsa_lib: comRestart")
        return ('SUCCESS', restartTime, 'COM process restarted.')

def verifyComSaSupportReadingStartStopTimes():
    """
    New log entries were introduced in the COM SA source code starting with 3.4 Sh10
    to clearly mark the beginning and finalizing of the COM SA start and stop procedures.
    """

    logger.debug("enter comsa_lib: verifyComSaSupportReadingStartStopTimes")

    # This is not the optimal place to define such variables. Feel free to improve!
    neededComSaRelease = '3'
    neededComSaMajorVer = '5'
    neededComSaVersion = "R5A09"

    ComsaOK = lib.checkComponentVersion('comsa', neededComSaRelease, neededComSaVersion)
    if ComsaOK[0] != 'SUCCESS':
        logger.debug("leave comsa_lib: verifyComSaSupportReadingStartStopTimes")
        return ComsaOK
    ComsaMajorOK = lib.checkComponentMajorVersion('comsa', neededComSaRelease, neededComSaMajorVer)
    if ComsaMajorOK[0] != 'SUCCESS':
        logger.debug("leave comsa_lib: verifyComSaSupportReadingStartStopTimes")
        return ComsaMajorOK

    if ComsaOK[1] and ComsaMajorOK[1]:
        logger.debug("leave comsa_lib: verifyComSaSupportReadingStartStopTimes")
        return ('SUCCESS', True)
    else:
        logger.debug("leave comsa_lib: verifyComSaSupportReadingStartStopTimes")
        return ('SUCCESS', False)


def calculateSysDependentComSaStartStopTimes(self, subrack, slot, startTime, testConfig, failoverTest):
    logger.debug("enter comsa_lib: calculateSysDependentComSaStartStopTimes")

    events = {'System dependent COM SA stopping time(s) (seconds)': [['COM_SA', 'component stop procedure begins'], ['COM SA terminate procedure completed']], \
              'System dependent COM SA startup time(s) (seconds)': [['COM SA init procedure begins'], ['COM_SA', 'component start procedure completed']], \
              'System dependent PMT SA stopping time(s) (seconds)': [['PMT SA component stop procedure begins'], ['PMT SA terminate procedure completed']], \
              'System dependent PMT SA startup time(s) (seconds)': [['PMT SA init procedure begins'], ['PMT SA component start procedure completed']], \
              'System dependent combined COM SA and PMT SA stopping time(s) (seconds)': [['SA component stop procedure begins'], ['SA terminate procedure completed']], \
              'System dependent combined COM SA and PMT SA startup time(s) (seconds)': [['SA init procedure begins'], ['SA component start procedure completed']]}

    for key in events.keys():
        calculateStartStopEvent(self, key, events[key][0], events[key][1], subrack, slot, startTime, testConfig, failoverTest, takeFirstBeginEntryAndLastEndEntry = True)
    logger.debug("leave comsa_lib: calculateSysDependentComSaStartStopTimes")


def calculatePureComSaStartStopTimes(self, subrack, slot, startTime, testConfig, failoverTest):
    logger.debug("enter comsa_lib: calculateSysDependentComSaStartStopTimes")
    stopEvents = {'COM SA OAM SA component stop': [['OAM SA component stop procedure begins'], ['OAM SA component stop procedure completed']], \
                  'COM SA MW SA component stop': [['maf_comSAMwComponentStop()', 'MW SA component stop procedure begins'], ['maf_comSAMwComponentStop()', 'MW SA component stop procedure completed']], \
                  'COM SA BASE MW SA component stop': [['maf_coremw_stop()', 'MW SA component stop procedure begins'], ['maf_coremw_stop()', 'MW SA component stop procedure completed']], \
                  #'COM SA BASE MW SA component stop': [['maf_coremw_stop()', 'MW SA component stop procedure begins'], ['maf_coremw_stop()', 'MW SA component stop procedure completed']], \
                  'PMT SA component stop': [['PMT SA component stop procedure begins'], ['PMT SA component stop procedure completed']], \
                  'COM SA terminate': [['COM SA terminate procedure begins'], ['COM SA terminate procedure completed']], \
                  'PMT SA terminate': [['PMT SA terminate procedure begins'], ['PMT SA terminate procedure completed']]}

    startEvents = {'COM SA init': [['COM SA init procedure begins'], ['COM SA init procedure completed']], \
                   'PMT SA init': [['PMT SA init procedure begins'], ['PMT SA init procedure ends']], \
                   'COM SA OAM SA component start': [['OAM SA component start procedure begins'], ['OAM SA component start procedure completed']], \
                   'COM SA MW SA component start': [['MW SA component start procedure begins'], ['MW SA component start procedure completed']], \
                   'PMT SA component start': [['PMT SA component start procedure begins'], ['PMT SA component start procedure completed']]}

    comSaStopTime = 0.0
    for key in stopEvents.keys():
        result = lib.calculateProcedureLengthDelimitedBySyslogEntries(subrack, slot, startTime, stopEvents[key][0], stopEvents[key][1], testConfig, timeStampAfterCharacter = True)
        if result[0] != 'SUCCESS':
            logger.warn('WARNING: Problem getting %s time: %s' %(key, result[1]))
            #self.setAdditionalResultInfo('WARNING: Unable to get %s. %s' %(event, result[1]))
        else:
            #self.setAdditionalResultInfo('%s: %s' %(event, str(result[1])))
            comSaStopTime += result[1]

    comSaStartTime = 0.0
    for key in startEvents.keys():
        result = lib.calculateProcedureLengthDelimitedBySyslogEntries(subrack, slot, startTime, startEvents[key][0], startEvents[key][1], testConfig, timeStampAfterCharacter = True)
        if result[0] != 'SUCCESS':
            logger.warn('WARNING: Problem getting %s time: %s' %(key, result[1]))
            #self.setAdditionalResultInfo('WARNING: Unable to get %s. %s' %(event, result[1]))
        else:
            #self.setAdditionalResultInfo('%s: %s' %(event, str(result[1])))
            comSaStartTime += result[1]

    addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'Pure COM SA stopping time(s) (seconds)', float("%.3f" %comSaStopTime))
    addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'Pure COM SA starting time(s) (seconds)', float("%.3f" %comSaStartTime))
    logger.info('charMeasurements: Pure COM SA stopping time(s) (seconds) %.3f' %comSaStopTime)
    logger.info('charMeasurements" Pure COM SA starting time(s) (seconds) %.3f' %comSaStartTime)


    logger.debug("leave comsa_lib: calculateSysDependentComSaStartStopTimes")



def calculateStartStopEvent(self, event, beginPattern, endPattern, subrack, slot, startTime, testConfig, failoverTest, takeFirstBeginEntryAndLastEndEntry = False):
    logger.debug("enter comsa_lib: calculateStartStopEvent")
    if not failoverTest:
        result = lib.calculateProcedureLengthDelimitedBySyslogEntries(subrack, slot, startTime, beginPattern, endPattern, testConfig, timeStampAfterCharacter = True, takeFirstBeginEntryAndLastEndEntry = takeFirstBeginEntryAndLastEndEntry)
        if result[0] != 'SUCCESS':
            logger.warn('WARNING: Problem getting COM SA startup time. %s' %result[1])
            #self.setAdditionalResultInfo('WARNING: Unable to get %s. %s' %(event, result[1]))
        else:
            #self.setAdditionalResultInfo('%s: %s' %(event, str(result[1])))
            addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', event, float("%.3f" %result[1]))
            logger.info('charMeasurements - %s: %.3f' %(event, result[1]))
    logger.debug("leave comsa_lib: calculateStartStopEvent")


def addDataToTestSuiteConfig(testSuiteConfig, key, event, value):
    logger.debug("enter comsa_lib: addDataToTestSuiteConfig")
    if testSuiteConfig.has_key(key):
        if testSuiteConfig[key].has_key(event):
            testSuiteConfig[key][event].append(value)
        else:
            testSuiteConfig[key][event] = [value]
    else:
        testSuiteConfig[key] = {}
        testSuiteConfig[key][event] = [value]
    logger.debug("leave comsa_lib: addDataToTestSuiteConfig")


def getProcessId(subrack, slot, processName, path=''):
    """The method returns the PID of the process.
    If path is specified, 'pgrep -f' will be used, otherwise 'pgrep -x'
    KNOWN BUG: If you specify path, you still need to specify process name, even if it is not used.
    """
    logger.debug("enter comsa_lib: getProcessId")
    if path == '':
        cmd = 'pgrep -x %s' %processName
    else:
        cmd = 'pgrep -f "%s"' %path

    logger.debug("Sending command %s" %cmd)
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[0] != 'SUCCESS':
        logger.debug("leave comsa_lib: getProcessId")
        return('ERROR', 'Executing %s command not successful: %s' %(cmd, result[1]))
    lines = result[1].splitlines()
    if len(lines) > 1:
        pid = []
        for i in range(len(lines)):
            if 'int' in str(type(eval(lines[i]))):
                pid.append(eval(lines[i]))
            else:
                logger.debug("leave comsa_lib: getProcessId")
                return ('ERROR', 'Data returned by %s command not of type int' %cmd)
    elif len(lines) == 1:
        if 'int' in str(type(eval(lines[0]))):
            pid = eval(lines[0])
        else:
            return ('ERROR', 'Data returned by %s command not of type int' %cmd)
    else:
        return ('ERROR', ' %s command returned an empty response.' %cmd)

    logger.debug("leave comsa_lib: getProcessId")
    logger.debug("comsa_lib: found PID(s): %s" %str(pid))
    return ('SUCCESS', pid)


def getComSaServiceInstanceHaState(subrack, slot , serviceInstances, amfNodePattern):
    '''
    Get the SI HA state of a specific payload

    Arguments:
    (int subrack, int slot, {string}, amfNodePattern)
    Obs seviceInstance shall be a list or a string

    Returns:
    tuple('SUCCESS',resultList) or
    tuple('ERROR', 'error message')

    '''
    # subrack and slot have to be integers
    # serviceInstances has to be a list of strings
    logger.debug('enter getServiceInstanceHaState')

    varType=type(serviceInstances)
    varType=str(varType)
    pattern = "list"
    serviceInstanceList = []

    if (re.search(pattern, varType)):  # is it a list or a scalar?
        serviceInstanceList = serviceInstances
    else:
        serviceInstanceList.append(serviceInstances)

    amfNode = '%s%s'%(amfNodePattern, slot)

    resultList = []
    response = 'SUCCESS'

    for serviceInstance in serviceInstanceList:
        # Ignore the ERIC-ComSa-sshd component
        result = ssh_lib.sendCommand('amf-find csiass | grep %s | grep safSu=%s | grep -v safCsi=ERIC-ComSa-sshd' %(serviceInstance, amfNode))
        lines = result[1].splitlines()
        if len(lines) != 1 :
            logger.debug('leave getServiceInstanceHaState')
            return ('ERROR', 'Ambiguous query, less or more than one match finding the DN for %s on amf node %s . \n%s' %(serviceInstance, amfNode, result[1]))
        DN = str(lines[0])
        cmd = "amf-state csiass ha '%s'" %DN
        result = ssh_lib.sendCommand(cmd)
        if len(result[1].splitlines()) < 0:
            logger.error(result)
            logger.error(">>> failed to get %s ha state." %serviceInstance)
            logger.debug('leave getServiceInstanceHaState')
            return ('ERROR', 'failed to get %s ha state on amf node %s' %(serviceInstance, amfNode))
        else:
            lines = result[1].splitlines()[1]
        elements = lines.split('=')
        if len(elements) == 2 and 'saAmfCSICompHAState' in elements[0]:
            haState = elements[1].split('(')[0]
            resultList.append(str(haState))
        else:
            logger.error(">>> failed to get %s ha state." %serviceInstance)
            logger.debug('leave getServiceInstanceHaState')
            return ('ERROR', 'failed to get %s ha stateon amf node %s' %(serviceInstance, amfNode))

    if len(resultList) ==1:
        resultList = resultList[0]
    logger.debug('getServiceInstanceHaState returns: %s' %str((response, resultList)))
    logger.debug('leave getServiceInstanceHaState')
    return (response,resultList)


def getSuReadinessState(subrack, slot , serviceUnit, amfNodePattern):
    '''
    getSuReadinessState

    Arguments:
    (int subrack, int slot, list serviceUnit, string amfNodePattern)
    Observation serviceUnit shall be a list of strings or a string

    Returns:
    tuple('SUCCESS',suReadiState, DN) or
    tuple('ERROR', 'error message')
    '''

    logger.debug('enter getSuReadinessState')

    varType=type(serviceUnit)
    varType=str(varType)
    pattern = "list"
    serviceUnitList = []
    if (re.search(pattern, varType)):  # is it a list or a scalar?
        serviceUnitList = serviceUnit
    else:
        serviceUnitList.append(serviceUnit)

    amfNode = '%s%s'%(amfNodePattern, slot)

    for serviceUnit in serviceUnitList:
        cmd = 'amf-find su | grep %s | grep %s' %(amfNode, serviceUnit)
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        lines = result[1].splitlines()
        if len(lines) != 1 :
            logger.debug('leave getSuReadinessState')
            return ('ERROR', 'Ambiguous query, less or more than one match for %s on amf node %s. \n%s' %(serviceUnit, amfNode, result[1]))
        DN = str(lines[0])

        cmd = 'amf-state su readi %s' %DN
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        lines = result[1].splitlines()[1]
        elements = lines.split('=')
        if len(elements) == 2:
            suReadiState = str(elements[1].split('(')[0])
            logger.debug('getSuReadinessState returns: %s' %str(('SUCCESS', suReadiState, DN)))
            logger.debug('leave getSuReadinessState')
            return('SUCCESS', suReadiState, DN)
        else:
            logger.error(">>> failed to get %s Su radiness state." %serviceUnit)
            logger.debug('leave getSuReadinessState')
            return ('ERROR', 'failed to get %s Su readiness state' %serviceUnit)

def lockSu(subrack, slot, serviceUnit, amfNodePattern, memoryCheck = False, installStressTool = False):
    '''
    1. check if the su is in active state and find the DN
    2. lock the su
    3. check that the su is out of service
    4. returns  ('SUCCESS', 'Lock serviceUnit OK on controller (%s, %s).' %(subrack, slot)) or
                ('ERROR', 'error message')
    '''

    logger.debug('enter lockSu')
    result = getSuReadinessState(subrack, slot , serviceUnit, amfNodePattern)
    if result[0] != 'SUCCESS':
        logger.debug('leave lockSu')
        return result
    elif result[1] != 'IN-SERVICE':
        logger.debug('leave lockSu')
        return ('ERROR', 'The serviceUnit is not in service and will not be locked.')

    DN = result[2]
    cmd = 'date +%%s; amf-adm lock %s' %DN
    if memoryCheck:
        logger.debug('Set time out for Valgrind')
        ssh_lib.setTimeout(120, subrack, slot)
    if installStressTool:
        logger.debug('Set time out for Overload using stress')
        ssh_lib.setTimeout(200, subrack, slot)

    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[0] != 'SUCCESS':
        logger.debug('leave lockSu')
        return result
    elif len(result[1].splitlines()) != 1:
        logger.debug('leave lockSu')
        return ('ERROR', 'Expected a response that only contains the date in unix format. Received: %s' %result[1])
    startTime = result[1]

    misc_lib.waitTime(5)

    result = getSuReadinessState(subrack, slot , serviceUnit, amfNodePattern)
    if result[0] != 'SUCCESS':
        logger.debug('leave lockSu')
        return result
    elif result[1] != 'OUT-OF-SERVICE':
        logger.debug('leave lockSu')
        return ('ERROR', 'The serviceUnit is not out of service. The lock operation did not succeed.')

    logger.debug('lockSu returns: %s' %str(('SUCCESS', 'Lock serviceUnit OK on controller (%s, %s).' %(subrack, slot))))
    logger.debug('leave lockSu')
    return ('SUCCESS', 'Lock serviceUnit OK on controller (%s, %s).' %(subrack, slot), startTime)


def unlockSu(subrack, slot, serviceUnit, amfNodePattern, memoryCheck = False, installStressTool = False):
    '''
    1. check if the su is in out of service state and find the DN
    2. unlock the su
    3. check that the su is active state
    4. returns ('SUCCESS', 'Unlock serviceUnit OK on controller (%s, %s).' %(subrack, slot)) or
               ('ERROR', 'error message')
    '''

    logger.debug('enter unlockSu')
    result = getSuReadinessState(subrack, slot , serviceUnit, amfNodePattern)
    if result[0] != 'SUCCESS':
        logger.debug('leave unlockSu')
        return result
    elif result[1] != 'OUT-OF-SERVICE':
        logger.debug('leave unlockSu')
        return ('ERROR', 'The serviceUnit is not in out of service state and will not be unlocked.')

    DN = result[2]
    cmd = 'amf-adm unlock %s' %DN
    if memoryCheck:
        logger.debug('Set time out for Valgrind')
        ssh_lib.setTimeout(120, subrack, slot)
    if installStressTool:
        logger.debug('Set time out for Overload using stress')
        ssh_lib.setTimeout(200, subrack, slot)

    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[0] != 'SUCCESS':
        logger.debug('leave unlockSu')
        return result
    elif result[1] != '':
        logger.debug('leave unlockSu')
        return ('ERROR', 'Expected an empty response to the unlock su command. Received: %s' %result[1])

    misc_lib.waitTime(5)

    result = getSuReadinessState(subrack, slot , serviceUnit, amfNodePattern)
    if result[0] != 'SUCCESS':
        logger.debug('leave unlockSu')
        return result
    elif result[1] != 'IN-SERVICE':
        logger.debug('leave unlockSu')
        return ('ERROR', 'The serviceUnit is not in service. The unlock operation did not succeed.')

    logger.debug('unlockSu returns: %s' %str(('SUCCESS', 'Unlock serviceUnit OK on controller (%s, %s).' %(subrack, slot))))
    logger.debug('leave unlockSu')
    return ('SUCCESS', 'Unlock serviceUnit OK on controller (%s, %s).' %(subrack, slot))

def switchover(testConfig):
    '''
    This is not yet fully usable.
    '''


    activeController = 0
    standbyController = 0

    pass

    comment = '''
    controllers = testConfig['controllers']
    logger.info('Checking HA state for Com SA on the controllers')
    for controller in controllers:
        result = getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        if result[1] == 'ACTIVE':
            activeController = controller[1]
            logger.info('Found active controller: %s' %str(controller))
        elif result[1] == 'STANDBY':
            standbyController = controller[1]
            logger.info('Found standby controller: %s' %str(controller))

    if activeController == 0:
        self.fail('ERROR', 'No controller found with active instance of ComSa')
    elif standbyController == 0:
        self.fail('ERROR', 'No controller found with standby instance of ComSa.')


    self.setTestStep('Get ComSa DN and lock ')

    result = self.lockSu(controller[0], activeController, self.serviceInstanceName, self.amfNodePattern)
    self.fail(result[0], result[1])


    self.setTestStep('Verify that the former standby SC became active ')

    result = self.getComSaServiceInstanceHaState(controller[0], standbyController, self.serviceInstanceName, self.amfNodePattern)
    self.fail(result[0], result[1])
    if result[1] != 'ACTIVE':
        self.fail(result[0], 'The former standby controller did not become active after the former active controller was locked.')

    logger.info('The former standby controller became active')
    oldActiveController = activeController
    activeController = standbyController
    standbyController = 0


    self.setTestStep('Unlock the locked SC')

    result = self.unlockSu(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern)
    self.fail(result[0], result[1])
    logger.info('%s' %str(result[1]))


    self.setTestStep('Verify that the former active SC becomes standby.')

    result = self.getComSaServiceInstanceHaState(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern)
    self.fail(result[0], result[1])
    if result[1] != 'STANDBY':
        self.fail(result[0], 'The former active controller did not become standby after the sericeUnit was unlocked.')

    logger.info('The former active controller became standby')
    #standbyController = oldActiveController
    '''

def checkPso():
    '''This method checks if the PSO is in place in the test cluster.
    Interface:
    ('SUCCESS', True) if test cluster has PSO
    ('SUCCESS', False) if test cluster does not have PSO
    ('ERROR', 'some error message')
    '''
    logger.debug('enter checkPso')
    cmd = "ls /usr/share/"
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave checkPso')
        return result
    if ' pso ' in result[1]:
        logger.debug('leave checkPso')
        return ('SUCCESS', True)
    else:
        logger.debug('leave checkPso')
        return ('SUCCESS', False)

def findActiveController(testConfig, serviceInstanceName, amfNodePattern):
    '''
    Finds the active COM SA controller
    '''

    logger.debug('enter findActiveController')
    controllers = testConfig['controllers']

    activeController = 0
    standbyController = 0

    logger.info('Checking HA state for Com SA on the controllers')
    for controller in controllers:
        result = getComSaServiceInstanceHaState(controller[0], controller[1], serviceInstanceName, amfNodePattern)
        if result[0] != 'SUCCESS':
            logger.debug('leave findActiveController')
            return result
        if result[1] == 'ACTIVE':
            activeController = controller
            logger.info('Found active controller: %s' %str(controller))
        elif result[1] == 'STANDBY':
            standbyController = controller
            logger.info('Found standby controller: %s' %str(controller))

    if activeController == 0:
        logger.debug('leave findActiveController')
        return ('ERROR', 'No controller found with active instance of ComSa')
    elif standbyController == 0 and len(controllers) == 2:
        logger.debug('leave findActiveController')
        return ('ERROR', 'No controller found with standby instance of ComSa.')

    logger.debug('leave findActiveController')
    return ('SUCCESS', activeController)

def findPassiveController(testConfig, serviceInstanceName, amfNodePattern):
    '''
    Finds the passive COM SA controller
    '''

    logger.debug('enter findPassiveController')
    controllers = testConfig['controllers']

    activeController = 0
    standbyController = 0

    logger.info('Checking HA state for Com SA on the controllers')
    for controller in controllers:
        result = getComSaServiceInstanceHaState(controller[0], controller[1], serviceInstanceName, amfNodePattern)
        if result[0] != 'SUCCESS':
            logger.debug('leave findActiveController')
            return result
        if result[1] == 'ACTIVE':
            activeController = controller
            logger.info('Found active controller: %s' %str(controller))
        elif result[1] == 'STANDBY':
            standbyController = controller
            logger.info('Found standby controller: %s' %str(controller))

    if activeController == 0:
        logger.debug('leave findPassiveController')
        return ('ERROR', 'No controller found with active instance of ComSa')
    elif standbyController == 0 and len(controllers) == 2:
        logger.debug('leave findActiveController')
        return ('ERROR', 'No controller found with standby instance of ComSa.')

    logger.debug('leave findPassiveController')
    return ('SUCCESS', standbyController)


def getComSaSuRestartMax():
    '''
    Returns:
    ('ERROR', 'Some relevant error message')
    ('SUCCESS', saAmfSGSuRestartMaxInUse, saAmfSGSuRestartMax, saAmfSgtDefSuRestartMax)
    saAmfSGSuRestartMaxInUse    this is the value of the parameter that is actually used by the system. If saAmfSGSuRestartMax is empty or None, \
                                than the saAmfSgtDefSuRestartMax is in use. If it has a value (any int) that it that value that is active.
    saAmfSGSuRestartMax         can have a real value of type int or can be None, if not assigned.
    saAmfSgtDefSuRestartMax     will always have to have a value
    '''
    logger.debug('enter getComSaSuRestartMax')
    cmd = "immfind | grep ComSa | sed 's/\\\\/\\\\\\\\/g' | xargs immlist | grep SuRestartMax"
    saAmfSGSuRestartMaxInUse = None
    saAmfSgtDefSuRestartMax = None
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getComSaSuRestartMax')
        return result
    lines = result[1].splitlines()
    if len(lines) != 2:
        logger.debug('leave getComSaSuRestartMax')
        return ('ERROR', 'We expected only 2 matches for the search pattern, one for the default value and one for the given value. Received: %s' %result[1])
    for line in lines:
        if 'saAmfSGSuRestartMax' in line:
            splitLine = line.split()
            if len(splitLine) == 4:
                saAmfSGSuRestartMax = splitLine[2]
                if 'int' in str(type(eval(saAmfSGSuRestartMax))):
                    saAmfSGSuRestartMax = int(saAmfSGSuRestartMax)
                else:
                    logger.debug('leave getComSaSuRestartMax')
                    return ('ERROR', 'The field evaluated was expected to be an integer. Instead we evaluated: %s' %splitLine[2])
            elif len(splitLine) == 3 and '<Empty>' in splitLine:
                saAmfSGSuRestartMax = None
            else:
                logger.debug('leave getComSaSuRestartMax')
                return ('ERROR', 'The format of the match for the search pattern is not usable. Expected exactly 3 or 4 fields. Received: %s' %line)
        elif 'saAmfSgtDefSuRestartMax' in line:
            splitLine = line.split()
            if len(splitLine) == 4:
                saAmfSgtDefSuRestartMax = splitLine[2]
                if 'int' in str(type(eval(saAmfSgtDefSuRestartMax))):
                    saAmfSgtDefSuRestartMax = int(saAmfSgtDefSuRestartMax)
                else:
                    logger.debug('leave getComSaSuRestartMax')
                    return ('ERROR', 'The field evaluated was expected to be an integer. Instead we evaluated: %s' %splitLine[2])
            else:
                logger.debug('leave getComSaSuRestartMax')
                return ('ERROR', 'The format of the match for the search pattern is not usable. Expected exactly 4 fields. Received: %s' %line)

    if saAmfSgtDefSuRestartMax == None:
        logger.debug('leave getComSaSuRestartMax')
        return ('ERROR', 'Information about saAmfSgtDefSuRestartMax was not received as response to the immfind command. Received: %s' %result[1])

    if saAmfSGSuRestartMax == None:
        saAmfSGSuRestartMaxInUse = saAmfSgtDefSuRestartMax
    else:
        saAmfSGSuRestartMaxInUse = saAmfSGSuRestartMax

    logger.debug('leave getComSaSuRestartMax')
    return ('SUCCESS', saAmfSGSuRestartMaxInUse, saAmfSGSuRestartMax, saAmfSgtDefSuRestartMax)

def setComSaSuRestartMax(toDefault, value = None):
    '''
    If toDefault == True: the method will find the default value first and then set it. Value will not be considered and is optional.
    if toDefault == False: the method will set the value passed as argument
    value is the new desired value for the saAmfSGSuRestartMax parameter and it has to be an int

    Returns
    ('SUCCESS', 'operation successful)
    ('SUCCESS', 'No operation needed. Default value already set and active in the system')
    ('ERROR', 'Some relevant error message' )
    '''

    logger.debug('enter setComSaSuRestartMax')

    if toDefault == True:
        result = getComSaSuRestartMax()
        if result[0] != 'SUCCESS':
            logger.debug('leave setComSaSuRestartMax')
            return result
        currentValue = result[1]
        if result [2] == None and result[1] == result[3]:
            logger.debug('leave setComSaSuRestartMax')
            return ('SUCCESS', 'No operation needed. Default value already set and active in the system' )
        cmd = 'immcfg -a saAmfSGSuRestartMax-=%d safSg=2N,safApp=ERIC-ComSa' %currentValue
    elif toDefault == False:
        if value == None:
            logger.debug('leave setComSaSuRestartMax')
            return ('ERROR', 'The input parameter value has to be defined.' )
        elif 'int' not in str(type(value)):
            logger.debug('leave setComSaSuRestartMax')
            return ('ERROR', 'The input parameter value has to be an int. Got %s' %str(value))
        cmd = 'immcfg -a saAmfSGSuRestartMax=%d safSg=2N,safApp=ERIC-ComSa' %value
    else:
        logger.debug('leave setComSaSuRestartMax')
        return ('ERROR', 'The input parameter toDefault has to be either True or False. Got: %s' %str(toDefault))
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getComSaSuRestartMax')
        return result
    if result[1] != '':
        logger.debug('leave getComSaSuRestartMax')
        return ('ERROR', 'Expected an empty response to the set command. Received: %s' %result[1])

    logger.debug('leave getComSaSuRestartMax')
    return ('SUCCESS', 'operation successful')


    logger.debug('leave setComSaSuRestartMax')

def addMomFileToCom(subrack, slot, file, opthandler='MW_OAM', commit=True):
    #change persmisson for all models when run with COM Sugar
    cmd = 'chmod 777 %s' %(file)
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    cmd='/opt/com/bin/com_mim_tool --addModelFile=%s' %(file)
    if opthandler != '':
        cmd += ' --modelHandler=%s' %opthandler
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[0] != 'SUCCESS' or 'Operation completed' not in result[1]:
        return ('ERROR', result[1])

    if commit:
        cmd='/opt/com/bin/com_mim_tool --commit'
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        if result[0] != 'SUCCESS' or 'Operation completed' not in result[1]:
            return ('ERROR', result[1])
        if 'Modelfile entry already' and 'Skipping adding of modelfile' in result[1]:
            return ('ERROR', 'The specified model file is already imported to the system: "%s"' %result[1])

    return ('SUCCESS', 'OK')

def removeMomFileFromCom(subrack, slot, file, opthandler='MW_OAM', commit=True):
    cmd='/opt/com/bin/com_mim_tool --removeModelFile=%s' %(file)
    if opthandler != '':
        cmd += ' --modelHandler=%s' %opthandler
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[0] != 'SUCCESS' or 'Operation completed' not in result[1]:
        return ('ERROR', result[1])

    if commit:
        cmd='/opt/com/bin/com_mim_tool --commit'
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        if result[0] != 'SUCCESS' or 'Operation completed' not in result[1]:
            return ('ERROR', result[1])

    return ('SUCCESS', 'OK')

def importImmClassOrObject(subrack, slot, file):
    cmd = 'immcfg -f %s'%(file)
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[0] != 'SUCCESS':
        return('ERROR', result[1])
    if result[1] != '':
        return('ERROR', result[1])

    return('SUCCESS', 'OK')

def installValgrind(testConfig, pathToRpms):
    logger.debug('enter installValgrind')
    # Copy files to target
    cmd = 'ls %s | grep rpm' %pathToRpms
    result = misc_lib.execCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave installValgrind')
        return result
    rpms=result[1].splitlines()

    for rpm in rpms:
        result = ssh_lib.remoteCopy('%s/%s' %(pathToRpms, rpm), '/cluster/rpms/', timeout = 60)
        if result[0] != 'SUCCESS':
            logger.debug('leave installValgrind')
            return result
        # Install the copied rpm
        for controller in testConfig['controllers']:
            cmd = 'cluster rpm -a %s -n %d' %(rpm, testConfig['controllers'].index(controller) + 1)
            result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
            if result[0] != 'SUCCESS':
                logger.debug('leave installValgrind')
                return result

    # Activate rpms
    for controller in testConfig['controllers']:
        cmd = 'cluster rpm -A -n %d' %(testConfig['controllers'].index(controller) + 1)
        result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
        if result[0] != 'SUCCESS':
            logger.debug('leave installValgrind')
            return result

    logger.debug('leave installValgrind')
    return ('SUCCESS', 'OK')

def activateValgrind(self, testConfig, pathToRpms, replaceComScript, pathOnTarget, installRpm = True, comScript='/opt/com/bin/com.sh', pathToValgrindLogs = '/cluster/valgrind_log'):
    logger.debug('enter activateValgrind')
    result = checkIfValgrindActive(pathToValgrindLogs, testConfig)
    logger.info('checkIfValgrindActive returner: %s' %str(result))
    if result == ('SUCCESS', 2):
        logger.debug('Valgrind already installed')
        logger.debug('leave activateValgrind')
        return ('SUCCESS', 'Valgrind already installed')
    elif result == ('SUCCESS', 1):
        logger.info('Valgrind rpms are already installed')
        installRpm = False

    if installRpm:
        dict = self.comsa_lib.getGlobalConfig(self)
        pathToSles11Rpms = dict.get('PATH_TO_VALGRIND_SLES11_RPMS')
        pathToSles12Rpms = dict.get('PATH_TO_VALGRIND_SLES12_RPMS')
        tmpPathToRpms = ''
        if self.linuxDistro == 'Sles12Type':
            tmpPathToRpms = "%s/%s" %(pathToRpms, pathToSles12Rpms)
        else:
            tmpPathToRpms = "%s/%s" %(pathToRpms, pathToSles11Rpms)
        result = installValgrind(testConfig, tmpPathToRpms)
        if result[0] != 'SUCCESS':
            logger.debug('leave activateValgrind')
            return result

    cmd = 'mkdir -p "%s"' %pathOnTarget
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave activateValgrind')
        return result

    result = ssh_lib.remoteCopy(replaceComScript, pathOnTarget, timeout = 60)
    if result[0] != 'SUCCESS':
        logger.debug('leave activateValgrind')
        return result

    replaceScriptFileName = replaceComScript.split('/')[len(replaceComScript.split('/')) - 1]
    cmd = 'chmod +x %s/%s' %(pathOnTarget, replaceScriptFileName)
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave activateValgrind')
        return result
    elif 'No such file or directory' in result[1]:
        logger.debug('leave activateValgrind')
        return ('ERROR', result[1])

    # Replace original com.sh with valgrind com.sh
    for controller in testConfig['controllers']:
        cmd = 'mkdir -p "%s"' %pathToValgrindLogs
        result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
        if result[0] != 'SUCCESS':
            logger.debug('leave activateValgrind')
            return result
        cmd = '%s/%s "%s" %s' %(pathOnTarget, replaceScriptFileName, pathToValgrindLogs, comScript)
        result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
        if result[0] != 'SUCCESS':
            logger.debug('leave activateValgrind')
            return result
        result = comRestart(self, controller[0], controller[1], True)
        if result[0] != 'SUCCESS':
            logger.debug('leave activateValgrind')
            return result

    return ('SUCCESS', 'OK')

def checkIfValgrindActive(pathToValgrindLogs, testConfig, comScript='/opt/com/bin/com.sh'):
    '''
    This function checkes if valgrind is enabled on the target
    1. Check if com.sh contains valgrind data
    2. Check if valgrind rpms are active

    Returns:
    ('ERROR', 'Some relevant error message') in case of unexpected behaviour
    ('SUCCESS', 0) if Valgrind is not installed on the target
    ('SUCCESS', 1) if Valgrind rpms are installed and active on the target
    ('SUCCESS', 2) if Valgrind rpms are installed and active on the target and com.sh is updated with valgrind is installed and active on the target
    '''
    res = ('ERROR', '')
    retValue = 0

    for controller in testConfig['controllers']:
        cmd = 'cluster rpm -l -n %d | grep valgrind' %controller[1]
        result = ssh_lib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            return result
        elif result[1] == '':
            return ('SUCCESS', 0)

    retValue = 1 # if we reached this point it means that the valgrind rpms are installed

    cmd = 'grep "%s" %s' %(pathToValgrindLogs, comScript)
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        return ('SUCCESS', retValue)
    elif 'No such file or directory' in result[1]:
        return ('SUCCESS', retValue)
    elif result[1] == '':
        return ('SUCCESS', retValue)

    retValue = 2 # if we reached this point it means that the valgrind rpms are installed and the com.sh is updated with valgrind content

    return ('SUCCESS', retValue)


def getEventTimestampFromAlarmAlertLog(subrack, slot, searchPatterns, startTime, testConfig, facility = 'alarm', logDir = '/storage/no-backup/coremw/var/log/saflog/FaultManagementLog/' ):
    '''
    This method will return the timestamp of all the events in which the elements of the search pattern were found.

    The method only returns the matches that occued after the startTime (defined in unix time)

    Main steps:
    1. list all occurance time stamps with
        grep 'search patterns' /var/log/SC-2-1/messages* | cut -d\; -f2 | sed 's/T/ /' | sed 's/Z//''
    2. compare times with start time (readable format)
    3. convert relevant times to unix time using timeConv
    4. sort list

    Arguments:
    int subrack
    int slot
    list [searchPatterns]
    str startTime (unix time)
    self.testConfig
    str facility has to be either alarm or alert

    Returns
    ('ERROR', 'error message')
    ('SUCCESS', [list of ints representing unix times])
    '''

    logger.debug('enter getEventTimestampFromAlarmAlertLog()')
    numOfRetries = 4;

    # 1. list all occurance time stamps with
    facilityOptions = ['alarm', 'alert']
    if facility in facilityOptions:
        logDir += facility
    else:
        return ('ERROR', 'Facility parameter has to be either alarm or alert. Received: %s' %facility)

    readableTimes = []
    cmd = """grep -ih "%s" %s/*.log""" %(searchPatterns[0], logDir)
    if len(searchPatterns) > 1:
        for i in range(len(searchPatterns)-1):
            cmd += """ | grep -i "%s" """ %(searchPatterns[i+1])
    cmd += """ | cut -d\; -f2 | sed 's/T/ /' | sed 's/Z//' | cut -d+ -f1"""
    for x in range(0, numOfRetries):
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        if result[0] != 'SUCCESS' or 'grep: ' in result[1]:
            logger.debug('leave getEventTimestampFromAlarmAlertLog()')
            return ('ERROR', result[1])
        if result[1] != '':
            #Find out matched pattern ,break for loop
            readableTimes = result[1].splitlines()
        else:
            logger.debug('leave getEventTimestampFromAlarmAlertLog()')
            if x == 3 or len(searchPatterns) == 1:
                return ('ERROR', 'No entry found in the %s log for the following search pattern: %s' %(facility, str(searchPatterns)))

        # convert unix start time to readable format in order to later use the faster python compare method isDateMoreRecent()
        result = timeConvUnixToReadableAlarmFormat(startTime)
        if result[0] != 'SUCCESS':
            return result
        readableStartTime = result[1]

        #2. compare times with start time (readable format)
        #3. convert relevant times to unix time using timeConv
        timesAfterStartTime = []
        for readableTime in readableTimes:
            result = isDateMoreRecentAlarmFormat(readableStartTime, readableTime)
            if result[0] != 'SUCCESS':
                return result
            if result[1] == True:
                result = lib.timeConv(readableTime)
                if result[0] != 'SUCCESS':
                    return result
                timesAfterStartTime.append(result[1])

        if len(timesAfterStartTime) == 0:
            if x == 3 or len(searchPatterns) == 1:
                return ('ERROR', 'No entry found in the %s log for the following search pattern: %s' %(facility, str(searchPatterns)))
        else:
            #4. sort list
            timesAfterStartTime.sort()
            result = ('SUCCESS', timesAfterStartTime)
            break
        misc_lib.waitTime(10)

    logger.debug('leave getEventTimestampFromAlarmAlertLog()')
    return result

def timeConvUnixToReadableAlarmFormat(timeString):
    '''
    This method converts unix time to humanly readable in the format of syslog, that is "month day hour:minute:second"
    '''
    logger.debug('enter timeConvUnixToReadableAlarmFormat()')
    #print timeString
    #print type(timeString)
    result = misc_lib.execCommand('date --date "GMT 1970-01-01 %s sec" "+%%Y-%%m-%%d %%T"' %str(timeString))
    if result[0] != 'SUCCESS':
        logger.debug('leave timeConvUnixToReadableAlarmFormat()')
        return result
    logger.debug('leave timeConvUnixToReadableAlarmFormat()')
    return result


def isDateMoreRecentAlarmFormat(dateString1, dateString2):
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

    year1 = int(dateString1.split('-')[0])
    year2 = int(dateString2.split('-')[0])
    if year1 < year2:
        result = ('SUCCESS', True)
    elif year1 > year2:
        result = ('SUCCESS', False)
    else:
        month1 = int(dateString1.split('-')[1])
        month2 = int(dateString2.split('-')[1])
        if month1 < month2:
            result = ('SUCCESS', True)
        elif month1 > month2:
            result = ('SUCCESS', False)
        else:
            day1 = int(dateString1.split('-')[2].split()[0])
            day2 = int(dateString2.split('-')[2].split()[0])
            if day1 < day2:
                result = ('SUCCESS', True)
            elif day1 > day2:
                result = ('SUCCESS', False)
            else:
                hour1 = int(dateString1.split('-')[2].split()[1].split(':')[0])
                hour2 = int(dateString2.split('-')[2].split()[1].split(':')[0])
                if hour1 < hour2:
                    result = ('SUCCESS', True)
                elif hour1 > hour2:
                    result = ('SUCCESS', False)
                else:
                    minute1 = int(dateString1.split('-')[2].split()[1].split(':')[1])
                    minute2 = int(dateString2.split('-')[2].split()[1].split(':')[1])
                    if minute1 < minute2:
                        result = ('SUCCESS', True)
                    elif minute1 > minute2:
                        result = ('SUCCESS', False)
                    else:
                        second1 = int(dateString1.split('-')[2].split()[1].split(':')[2])
                        second2 = int(dateString2.split('-')[2].split()[1].split(':')[2])
                        if second1 <= second2:
                            result = ('SUCCESS', True)
                        elif second1 > second2:
                            result = ('SUCCESS', False)

    return result

def getEventTimestampFromTracelog(subrack, slot, searchPatterns, startTime, testConfig, comsaFlag, logDir = '/var/opt/comsa/'):
    '''
    This method will return the timestamp of all the events in which the elements of the search pattern were found.

    The method only returns the matches that occued after the startTime (defined in unix time)

    Main steps:
    1. list all occurance time stamps with
        grep 'search patterns' /var/opt/comsa/comsa.trc* | cut -d: -f1-4 | awk '{print $1" "$2}' if comsaFlag = True
        grep 'search patterns' /var/opt/comsa/pmtsa.trc* | cut -d: -f1-4 | awk '{print $1" "$2}' if comsaFlag = False
    2. compare times with start time (readable format)
    3. convert relevant times to unix time using timeConvTraceFormat
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

    logger.debug('enter getEventTimestampFromTracelog()')

    # 1. list all occurance time stamps with

    readableTimes = []
    if comsaFlag == True:
        cmd = """grep -i "%s" %scomsa.trc*""" %(searchPatterns[0], logDir)
    else:
        cmd = """grep -i "%s" %spmtsa.trc*""" %(searchPatterns[0], logDir)
    if len(searchPatterns) > 1:
        for i in range(len(searchPatterns)-1):
            cmd += """ | grep -i "%s" """ %(searchPatterns[i+1])
    cmd += """ | cut -d: -f1-4 | awk '{print $1" "$2}'"""
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getEventTimestampFromTracelog()')
        return result
    '''
        Check that the directory really exist
    '''
    if 'No such file or directory' in result[1]:
        logger.debug('leave getEventTimestampFromTracelog()')
        #result[0] = 'ERROR'
        return ('ERROR', result[1])
    if result[1] != '':
        tempList = result[1].splitlines()
        for element in tempList:
            if logDir in element:
                # fix index out of range error
                tmpElement = element.split(':')
                sizeTmpElement = len(tmpElement)
                if sizeTmpElement >= 4:
                    dateString = "%s:%s:%s.%s" %(tmpElement[1],tmpElement[2],tmpElement[3].split('.')[0],tmpElement[3].split('.')[1])
                    readableTimes.append(dateString)
            else:
                readableTimes.append(element)

    if len(readableTimes) == 0:
        logger.debug('leave getEventTimestampFromTracelog()')
        return ('ERROR', 'No entry found in the trace log for the following search pattern: %s' %str(searchPatterns))

    # convert unix start time to readable format in order to later use the faster python compare method isDateMoreRecentTraceFormat()
    result = timeConvUnixToReadableTraceFormat(startTime)
    if result[0] != 'SUCCESS':
        return result
    reabableStartTime = result[1]

    #2. compare times with start time (readable format)
    #3. convert relevant times to unix time using timeConvTraceFormat
    timesAfterStartTime = []
    for readableTime in readableTimes:
        result = isDateMoreRecentTraceFormat(reabableStartTime, readableTime)
        if result[0] != 'SUCCESS':
            return result
        if result[1] == True:
            result = timeConvTraceFormat(readableTime)
            if result[0] != 'SUCCESS':
                return result
            timesAfterStartTime.append(result[1])

    if len(timesAfterStartTime) == 0:
        return ('ERROR', 'No entry found in the trace log after the start time for the following search pattern: %s' %str(searchPatterns))
    else:
        #4. sort list
        timesAfterStartTime.sort()
        result = ('SUCCESS', timesAfterStartTime)

    logger.debug('leave getEventTimestampFromTracelog()')
    return result

def timeConvTraceFormat(timeString):
    '''
    The method converts humanly readable time to unix time format
    '''

    result = misc_lib.execCommand('date -d "%s" +%%s.%%6N' %timeString)

    if result[0] != 'SUCCESS':
        logger.debug('leave timeConvTraceFormat()')
        return result
    unixTime = result[1]
    return ('SUCCESS', unixTime)

def timeConvUnixToReadableTraceFormat(timeString):
    '''
    This method converts unix time to humanly readable in the format of tracelog, that is "year-month-day hour:minute:second.microsecond"
    '''
    #print timeString
    #print type(timeString)
    result = misc_lib.execCommand('date --date "GMT 1970-01-01 %s sec" "+%%F %%T.%%6N"' %str(timeString))
    if result[0] != 'SUCCESS':
        logger.debug('leave timeConvUnixToReadableTraceFormat()')
        return result
    return result

def isDateMoreRecentTraceFormat(dateString1, dateString2):
    '''
    The dateString has to be specified in the format of the tracelog (that is "year-month-day hour:minute:second.microsecond").
    The purpose of this method is to support the getEventTimestampFromTracelog method so that we compare the times read from tracelog
    with this method instead of running the timeConvTraceFormat method which executes a date command on the local linux machine

    Returns
    ('ERROR', 'Some relevant error message')
    ('SUCCESS', True) if the date defined by dateString2 is more recent or equal to the date defined by dateString1
    ('SUCCESS', False) if the date defined by dateString2 is older than the date defined by dateString1
    '''
    result = ('ERROR', 'Method not executed correctly')

    year1 = int(dateString1.split()[0].split('-')[0])
    year2 = int(dateString2.split()[0].split('-')[0])

    if year1 < year2:
        result = ('SUCCESS', True)
    elif year1 > year2:
        result = ('SUCCESS', False)
    else:
        month1 = int(dateString1.split()[0].split('-')[1])
        month2 = int(dateString2.split()[0].split('-')[1])
        if month1 < month2:
            result = ('SUCCESS', True)
        elif month1 > month2:
            result = ('SUCCESS', False)
        else:
            day1 = int(dateString1.split()[0].split('-')[2])
            day2 = int(dateString2.split()[0].split('-')[2])
            if day1 < day2:
                result = ('SUCCESS', True)
            elif day1 > day2:
                result = ('SUCCESS', False)
            else:
                hour1 = int(dateString1.split()[1].split(':')[0])
                hour2 = int(dateString2.split()[1].split(':')[0])
                if hour1 < hour2:
                    result = ('SUCCESS', True)
                elif hour1 > hour2:
                    result = ('SUCCESS', False)
                else:
                    minute1 = int(dateString1.split()[1].split(':')[1])
                    minute2 = int(dateString2.split()[1].split(':')[1])
                    if minute1 < minute2:
                        result = ('SUCCESS', True)
                    elif minute1 > minute2:
                        result = ('SUCCESS', False)
                    else:
                        second1 = int(dateString1.split()[1].split(':')[2].split('.')[0])
                        second2 = int(dateString2.split()[1].split(':')[2].split('.')[0])
                        if second1 < second2:
                            result = ('SUCCESS', True)
                        elif second1 > second2:
                            result = ('SUCCESS', False)
                        else:
                            microsecond1 = int(dateString1.split()[1].split(':')[2].split('.')[1])
                            microsecond2 = int(dateString2.split()[1].split(':')[2].split('.')[1])
                            if microsecond1 < microsecond2:
                                result = ('SUCCESS', True)
                            elif microsecond1 > microsecond2:
                                result = ('SUCCESS', False)
    return result

# CLI specific methods

def create_active_controller_login_params(activeSc, testConfig, targetData, cli_script_path, cli_script_name):

    user_name = targetData['user']
    password = targetData['pwd']
    SC_ip = targetData['ipAddress']['ctrl']['ctrl%d'%activeSc[1]]
    SC_prompt = testConfig['testNodesNames'][activeSc[1] - 1]
    cli_script_path = '%s/%s'%(MY_REPOSITORY, cli_script_path)
    CLI_login_params = "%s./%s %s %s %s %s" %(cli_script_path, cli_script_name, SC_ip, user_name, password, SC_prompt)

    return CLI_login_params

def get_active_controller_ip(activeSc, targetData):

    SC_ip = targetData['ipAddress']['ctrl']['ctrl%d'%activeSc[1]]
    return SC_ip

def create_active_controller_login_params_for_sshd(activeSc, testConfig, targetData, cli_script_path, cli_script_name, port):

    user_name = targetData['user']
    password = targetData['pwd']
    SC_ip = targetData['ipAddress']['ctrl']['ctrl%d'%activeSc[1]]
    SC_prompt = testConfig['testNodesNames'][activeSc[1] - 1]
    cli_script_path = '%s/%s'%(MY_REPOSITORY, cli_script_path)
    CLI_login_params = "%s./%s %s:%s %s %s %s" %(cli_script_path, cli_script_name, SC_ip, port, user_name, password, SC_prompt)

    return CLI_login_params

def executeCliSession(cmd, numberOfRetries=10):

    logger.debug('Sending CLI command')
    for iteration in range(numberOfRetries):
        result = misc_lib.execCommand(cmd)
        if 'IF YOU ARE NOT AN AUTHORIZED USER, PLEASE EXIT IMMEDIATELY' in result[1]:
            break
        else:
            logger.info('WARNING: There was a broken CLI session!')
            result = ('ERROR', 'The CLI session was not successful: %s' %result[1])
        misc_lib.waitTime(3)
    if result[0] != 'SUCCESS':
        return result
    elif 'IF YOU ARE NOT AN AUTHORIZED USER, PLEASE EXIT IMMEDIATELY' not in result[1]:
        return ('ERROR', 'There was no successful CLI session after %d tries' %numberOfRetries)

    return result

def executeNetConfSession(cmd, numberOfRetries=10):

    logger.debug('Sending NetConf command')
    for iteration in range(numberOfRetries):
        result = misc_lib.execCommand(cmd)
        if '<capability>urn:ietf:params:netconf:base' in result[1]:
            break
        else:
            logger.info('WARNING: There was a broken NetConf session!')
            result = ('ERROR', 'The NetConf session was not successful: %s' %result[1])
    if result[0] != 'SUCCESS':
        return result
    elif '<capability>urn:ietf:params:netconf:base' not in result[1]:
        return ('ERROR', 'There was no successful NetConf session after %d tries' %numberOfRetries)

    return result

def load_TC_cli_config(self):
    '''
    This method loads the configs from the data received from the xml,
     and creates a list of the CLI inputs, expected outputs, non-expected outputs.
    1. Checking the data received from the xml
    2. Create list
    3. return list

    The method returns 3 lists:
     (cli_input_list, cli_expected_output_list, cli_nonexpected_output_list)

    '''
    self.myLogger.debug('enter load_TC_cli_config function')
    cli_input_list = []
    cli_expected_output_list = []
    cli_nonexpected_output_list = []
    #Only append to the corresponding list if the CLI input and the expected output is present
    if self.cli_input_1 != {} and self.cli_expected_output_1 != {} and self.cli_nonexpected_output_1 != {}:
        cli_input_list.append(self.cli_input_1)
        cli_expected_output_list.append(self.cli_expected_output_1)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_1)
    if self.cli_input_2 != {} and self.cli_expected_output_2 != {} and self.cli_nonexpected_output_2 != {}:
        cli_input_list.append(self.cli_input_2)
        cli_expected_output_list.append(self.cli_expected_output_2)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_2)
    if self.cli_input_3 != {} and self.cli_expected_output_3 != {} and self.cli_nonexpected_output_3 != {}:
        cli_input_list.append(self.cli_input_3)
        cli_expected_output_list.append(self.cli_expected_output_3)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_3)
    if self.cli_input_4 != {} and self.cli_expected_output_4 != {} and self.cli_nonexpected_output_4 != {}:
        cli_input_list.append(self.cli_input_4)
        cli_expected_output_list.append(self.cli_expected_output_4)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_4)
    if self.cli_input_5 != {} and self.cli_expected_output_5 != {} and self.cli_nonexpected_output_5 != {}:
        cli_input_list.append(self.cli_input_5)
        cli_expected_output_list.append(self.cli_expected_output_5)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_5)
    if self.cli_input_6 != {} and self.cli_expected_output_6 != {} and self.cli_nonexpected_output_6 != {}:
        cli_input_list.append(self.cli_input_6)
        cli_expected_output_list.append(self.cli_expected_output_6)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_6)
    if self.cli_input_7 != {} and self.cli_expected_output_7 != {} and self.cli_nonexpected_output_7 != {}:
        cli_input_list.append(self.cli_input_7)
        cli_expected_output_list.append(self.cli_expected_output_7)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_7)
    if self.cli_input_8 != {} and self.cli_expected_output_8 != {} and self.cli_nonexpected_output_8 != {}:
        cli_input_list.append(self.cli_input_8)
        cli_expected_output_list.append(self.cli_expected_output_8)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_8)
    if self.cli_input_9 != {} and self.cli_expected_output_9 != {} and self.cli_nonexpected_output_9 != {}:
        cli_input_list.append(self.cli_input_9)
        cli_expected_output_list.append(self.cli_expected_output_9)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_9)
    if self.cli_input_10 != {} and self.cli_expected_output_10 != {} and self.cli_nonexpected_output_10 != {}:
        cli_input_list.append(self.cli_input_10)
        cli_expected_output_list.append(self.cli_expected_output_10)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_10)
    if self.cli_input_11 != {} and self.cli_expected_output_11 != {} and self.cli_nonexpected_output_11 != {}:
        cli_input_list.append(self.cli_input_11)
        cli_expected_output_list.append(self.cli_expected_output_11)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_11)
    if self.cli_input_12 != {} and self.cli_expected_output_12 != {} and self.cli_nonexpected_output_12 != {}:
        cli_input_list.append(self.cli_input_12)
        cli_expected_output_list.append(self.cli_expected_output_12)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_12)
    if self.cli_input_13 != {} and self.cli_expected_output_13 != {} and self.cli_nonexpected_output_13 != {}:
        cli_input_list.append(self.cli_input_13)
        cli_expected_output_list.append(self.cli_expected_output_13)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_13)
    if self.cli_input_14 != {} and self.cli_expected_output_14 != {} and self.cli_nonexpected_output_14 != {}:
        cli_input_list.append(self.cli_input_14)
        cli_expected_output_list.append(self.cli_expected_output_14)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_14)
    if self.cli_input_15 != {} and self.cli_expected_output_15 != {} and self.cli_nonexpected_output_15 != {}:
        cli_input_list.append(self.cli_input_15)
        cli_expected_output_list.append(self.cli_expected_output_15)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_15)
    if self.cli_input_16 != {} and self.cli_expected_output_16 != {} and self.cli_nonexpected_output_16 != {}:
        cli_input_list.append(self.cli_input_16)
        cli_expected_output_list.append(self.cli_expected_output_16)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_16)
    if self.cli_input_17 != {} and self.cli_expected_output_17 != {} and self.cli_nonexpected_output_17 != {}:
        cli_input_list.append(self.cli_input_17)
        cli_expected_output_list.append(self.cli_expected_output_17)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_17)
    if self.cli_input_18 != {} and self.cli_expected_output_18 != {} and self.cli_nonexpected_output_18 != {}:
        cli_input_list.append(self.cli_input_18)
        cli_expected_output_list.append(self.cli_expected_output_18)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_18)
    if self.cli_input_19 != {} and self.cli_expected_output_19 != {} and self.cli_nonexpected_output_19 != {}:
        cli_input_list.append(self.cli_input_19)
        cli_expected_output_list.append(self.cli_expected_output_19)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_19)
    if self.cli_input_20 != {} and self.cli_expected_output_20 != {} and self.cli_nonexpected_output_20 != {}:
        cli_input_list.append(self.cli_input_20)
        cli_expected_output_list.append(self.cli_expected_output_20)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_20)
    if self.cli_input_21 != {} and self.cli_expected_output_21 != {} and self.cli_nonexpected_output_21 != {}:
        cli_input_list.append(self.cli_input_21)
        cli_expected_output_list.append(self.cli_expected_output_21)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_21)
    if self.cli_input_22 != {} and self.cli_expected_output_22 != {} and self.cli_nonexpected_output_22 != {}:
        cli_input_list.append(self.cli_input_22)
        cli_expected_output_list.append(self.cli_expected_output_22)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_22)
    if self.cli_input_23 != {} and self.cli_expected_output_23 != {} and self.cli_nonexpected_output_23 != {}:
        cli_input_list.append(self.cli_input_23)
        cli_expected_output_list.append(self.cli_expected_output_23)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_23)
    if self.cli_input_24 != {} and self.cli_expected_output_24 != {} and self.cli_nonexpected_output_24 != {}:
        cli_input_list.append(self.cli_input_24)
        cli_expected_output_list.append(self.cli_expected_output_24)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_24)
    if self.cli_input_25 != {} and self.cli_expected_output_25 != {} and self.cli_nonexpected_output_25 != {}:
        cli_input_list.append(self.cli_input_25)
        cli_expected_output_list.append(self.cli_expected_output_25)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_25)
    if self.cli_input_26 != {} and self.cli_expected_output_26 != {} and self.cli_nonexpected_output_26 != {}:
        cli_input_list.append(self.cli_input_26)
        cli_expected_output_list.append(self.cli_expected_output_26)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_26)
    if self.cli_input_27 != {} and self.cli_expected_output_27 != {} and self.cli_nonexpected_output_27 != {}:
        cli_input_list.append(self.cli_input_27)
        cli_expected_output_list.append(self.cli_expected_output_27)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_27)
    if self.cli_input_28 != {} and self.cli_expected_output_28 != {} and self.cli_nonexpected_output_28 != {}:
        cli_input_list.append(self.cli_input_28)
        cli_expected_output_list.append(self.cli_expected_output_28)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_28)
    if self.cli_input_29 != {} and self.cli_expected_output_29 != {} and self.cli_nonexpected_output_29 != {}:
        cli_input_list.append(self.cli_input_29)
        cli_expected_output_list.append(self.cli_expected_output_29)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_29)
    if self.cli_input_30 != {} and self.cli_expected_output_30 != {} and self.cli_nonexpected_output_30 != {}:
        cli_input_list.append(self.cli_input_30)
        cli_expected_output_list.append(self.cli_expected_output_30)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_30)
    if self.cli_input_31 != {} and self.cli_expected_output_31 != {} and self.cli_nonexpected_output_31 != {}:
        cli_input_list.append(self.cli_input_31)
        cli_expected_output_list.append(self.cli_expected_output_31)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_31)
    if self.cli_input_32 != {} and self.cli_expected_output_32 != {} and self.cli_nonexpected_output_32 != {}:
        cli_input_list.append(self.cli_input_32)
        cli_expected_output_list.append(self.cli_expected_output_32)
        cli_nonexpected_output_list.append(self.cli_nonexpected_output_32)

    #check for COM 3.2
    self.ComRelease = "3"
    self.ComMajorVersion = "1"
    ComMajorOK = ('SUCCESS', True)
    ComMajorOK = self.lib.checkComponentMajorVersion('com', self.ComRelease, self.ComMajorVersion, [], True)

    if ComMajorOK[1] == False:
        for list_index in range(0,len(cli_input_list)):
            # Well, if the input CLI string is for configuration and there is no "end"
            if cli_input_list[list_index].find('"configure"') != -1 and cli_input_list[list_index].find('"end"') == -1:
                cli_input_list[list_index] = cli_input_list[list_index].replace('"exit"', '"end" "exit"')
            # In case input string is not a configuration command, or the string is dedicated to COM 3.2 and older, do nothing

    self.myLogger.debug('leave load_TC_cli_config function')
    return (cli_input_list, cli_expected_output_list, cli_nonexpected_output_list)

def load_TC_cli_alt_config(self):
    '''
    This method loads alternative set of configs from the data received from the xml,
     and creates a list of the CLI inputs, expected outputs, non-expected outputs.
    1. Checking the data received from the xml
    2. Create list
    3. return list

    The method returns 3 lists:
     (cli_input_alt_list, cli_expected_output_alt_list, cli_nonexpected_output_alt_list)

    '''
    self.myLogger.debug('enter load_TC_cli_alt_config function')
    cli_alt_input_list = []
    cli_alt_expected_output_list = []
    cli_alt_nonexpected_output_list = []
    #Only append to the corresponding list if the CLI input and the expected output is present
    if self.cli_alt_input_1 != {} and self.cli_alt_expected_output_1 != {} and self.cli_alt_nonexpected_output_1 != {}:
        cli_alt_input_list.append(self.cli_alt_input_1)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_1)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_1)
    if self.cli_alt_input_2 != {} and self.cli_alt_expected_output_2 != {} and self.cli_alt_nonexpected_output_2 != {}:
        cli_alt_input_list.append(self.cli_alt_input_2)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_2)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_2)
    if self.cli_alt_input_3 != {} and self.cli_alt_expected_output_3 != {} and self.cli_alt_nonexpected_output_3 != {}:
        cli_alt_input_list.append(self.cli_alt_input_3)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_3)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_3)
    if self.cli_alt_input_4 != {} and self.cli_alt_expected_output_4 != {} and self.cli_alt_nonexpected_output_4 != {}:
        cli_alt_input_list.append(self.cli_alt_input_4)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_4)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_4)
    if self.cli_alt_input_5 != {} and self.cli_alt_expected_output_5 != {} and self.cli_alt_nonexpected_output_5 != {}:
        cli_alt_input_list.append(self.cli_alt_input_5)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_5)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_5)
    if self.cli_alt_input_6 != {} and self.cli_alt_expected_output_6 != {} and self.cli_alt_nonexpected_output_6 != {}:
        cli_alt_input_list.append(self.cli_alt_input_6)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_6)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_6)
    if self.cli_alt_input_7 != {} and self.cli_alt_expected_output_7 != {} and self.cli_alt_nonexpected_output_7 != {}:
        cli_alt_input_list.append(self.cli_alt_input_7)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_7)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_7)
    if self.cli_alt_input_8 != {} and self.cli_alt_expected_output_8 != {} and self.cli_alt_nonexpected_output_8 != {}:
        cli_alt_input_list.append(self.cli_alt_input_8)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_8)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_8)
    if self.cli_alt_input_9 != {} and self.cli_alt_expected_output_9 != {} and self.cli_alt_nonexpected_output_9 != {}:
        cli_alt_input_list.append(self.cli_alt_input_9)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_9)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_9)
    if self.cli_alt_input_10 != {} and self.cli_alt_expected_output_10 != {} and self.cli_alt_nonexpected_output_10 != {}:
        cli_alt_input_list.append(self.cli_alt_input_10)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_10)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_10)
    if self.cli_alt_input_11 != {} and self.cli_alt_expected_output_11 != {} and self.cli_alt_nonexpected_output_11 != {}:
        cli_alt_input_list.append(self.cli_alt_input_11)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_11)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_11)
    if self.cli_alt_input_12 != {} and self.cli_alt_expected_output_12 != {} and self.cli_alt_nonexpected_output_12 != {}:
        cli_alt_input_list.append(self.cli_alt_input_12)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_12)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_12)
    if self.cli_alt_input_13 != {} and self.cli_alt_expected_output_13 != {} and self.cli_alt_nonexpected_output_13 != {}:
        cli_alt_input_list.append(self.cli_alt_input_13)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_13)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_13)
    if self.cli_alt_input_14 != {} and self.cli_alt_expected_output_14 != {} and self.cli_alt_nonexpected_output_14 != {}:
        cli_alt_input_list.append(self.cli_alt_input_14)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_14)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_14)
    if self.cli_alt_input_15 != {} and self.cli_alt_expected_output_15 != {} and self.cli_alt_nonexpected_output_15 != {}:
        cli_alt_input_list.append(self.cli_alt_input_15)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_15)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_15)
    if self.cli_alt_input_16 != {} and self.cli_alt_expected_output_16 != {} and self.cli_alt_nonexpected_output_16 != {}:
        cli_alt_input_list.append(self.cli_alt_input_16)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_16)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_16)
    if self.cli_alt_input_17 != {} and self.cli_alt_expected_output_17 != {} and self.cli_alt_nonexpected_output_17 != {}:
        cli_alt_input_list.append(self.cli_alt_input_17)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_17)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_17)
    if self.cli_alt_input_18 != {} and self.cli_alt_expected_output_18 != {} and self.cli_alt_nonexpected_output_18 != {}:
        cli_alt_input_list.append(self.cli_alt_input_18)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_18)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_18)
    if self.cli_alt_input_19 != {} and self.cli_alt_expected_output_19 != {} and self.cli_alt_nonexpected_output_19 != {}:
        cli_alt_input_list.append(self.cli_alt_input_19)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_19)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_19)
    if self.cli_alt_input_20 != {} and self.cli_alt_expected_output_20 != {} and self.cli_alt_nonexpected_output_20 != {}:
        cli_alt_input_list.append(self.cli_alt_input_20)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_20)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_20)
    if self.cli_alt_input_21 != {} and self.cli_alt_expected_output_21 != {} and self.cli_alt_nonexpected_output_21 != {}:
        cli_alt_input_list.append(self.cli_alt_input_21)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_21)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_21)
    if self.cli_alt_input_22 != {} and self.cli_alt_expected_output_22 != {} and self.cli_alt_nonexpected_output_22 != {}:
        cli_alt_input_list.append(self.cli_alt_input_22)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_22)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_22)
    if self.cli_alt_input_23 != {} and self.cli_alt_expected_output_23 != {} and self.cli_alt_nonexpected_output_23 != {}:
        cli_alt_input_list.append(self.cli_alt_input_23)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_23)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_23)
    if self.cli_alt_input_24 != {} and self.cli_alt_expected_output_24 != {} and self.cli_alt_nonexpected_output_24 != {}:
        cli_alt_input_list.append(self.cli_alt_input_24)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_24)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_24)
    if self.cli_alt_input_25 != {} and self.cli_alt_expected_output_25 != {} and self.cli_alt_nonexpected_output_25 != {}:
        cli_alt_input_list.append(self.cli_alt_input_25)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_25)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_25)
    if self.cli_alt_input_26 != {} and self.cli_alt_expected_output_26 != {} and self.cli_alt_nonexpected_output_26 != {}:
        cli_alt_input_list.append(self.cli_alt_input_26)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_26)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_26)
    if self.cli_alt_input_27 != {} and self.cli_alt_expected_output_27 != {} and self.cli_alt_nonexpected_output_27 != {}:
        cli_alt_input_list.append(self.cli_alt_input_27)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_27)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_27)
    if self.cli_alt_input_28 != {} and self.cli_alt_expected_output_28 != {} and self.cli_alt_nonexpected_output_28 != {}:
        cli_alt_input_list.append(self.cli_alt_input_28)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_28)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_28)
    if self.cli_alt_input_29 != {} and self.cli_alt_expected_output_29 != {} and self.cli_alt_nonexpected_output_29 != {}:
        cli_alt_input_list.append(self.cli_alt_input_29)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_29)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_29)
    if self.cli_alt_input_30 != {} and self.cli_alt_expected_output_30 != {} and self.cli_alt_nonexpected_output_30 != {}:
        cli_alt_input_list.append(self.cli_alt_input_30)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_30)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_30)
    if self.cli_alt_input_31 != {} and self.cli_alt_expected_output_31 != {} and self.cli_alt_nonexpected_output_31 != {}:
        cli_alt_input_list.append(self.cli_alt_input_31)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_31)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_31)
    if self.cli_alt_input_32 != {} and self.cli_alt_expected_output_32 != {} and self.cli_alt_nonexpected_output_32 != {}:
        cli_alt_input_list.append(self.cli_alt_input_32)
        cli_alt_expected_output_list.append(self.cli_alt_expected_output_32)
        cli_alt_nonexpected_output_list.append(self.cli_alt_nonexpected_output_32)

    #check for COM 3.2
    self.ComRelease = "3"
    self.ComMajorVersion = "1"
    ComMajorOK = ('SUCCESS', True)
    ComMajorOK = self.lib.checkComponentMajorVersion('com', self.ComRelease, self.ComMajorVersion, [], True)

    if ComMajorOK[1] == False:
        for list_index in range(0,len(cli_alt_input_list)):
            # Well, if the input CLI string is for configuration and there is no "end"
            if cli_alt_input_list[list_index].find('"configure"') != -1 and cli_alt_input_list[list_index].find('"end"') == -1:
                cli_alt_input_list[list_index] = cli_alt_input_list[list_index].replace('"exit"', '"end" "exit"')
            # In case input string is not a configuration command, or the string is dedicated to COM 3.2 and older, do nothing

    self.myLogger.debug('leave load_TC_cli_alt_config function')
    return (cli_alt_input_list, cli_alt_expected_output_list, cli_alt_nonexpected_output_list)

def check_CLI_output(cli_output_lines, cli_expected_output, cli_nonexpected_output):
    '''
    This method compares the cli output to the expected.
    1. Looking for the index of the first cli line (">")
    2. Compare output line-by-line(from the first to the last cli line) to the expected lines
    3. Process and return result

    The method returns:
     'SUCCESS', 1 - if the cli output matches to the expected output
     'ERROR', 0 - if the cli output not matches to the expected output

    '''
    logger.debug('enter check_CLI_output function')
    all_matching = False
    nonexpected_item_present = True
    cli_output = []
    first_line = 0
    comp_result = ''

    #Looking for the index of the first cli line (">")
    logger.debug('Looking for the index of the first cli line')
    for lines in range(0,len(cli_output_lines)):
        if len(cli_output_lines[lines]) != 0 and cli_output_lines[lines][0] == '>':
            first_line = lines
            break
    for lines in range(first_line,len(cli_output_lines)):
        if (len(cli_output_lines[lines]) > 100): #Just output the long lines
            logger.debug('Original output: len[%d] %s' %(len(cli_output_lines[lines]), cli_output_lines[lines]))
            # replace some endline character.
            cli_output_lines[lines]  = re.compile(" \b| \x1B\[D").sub("",cli_output_lines[lines])
            logger.debug('Replaced output: len[%d] %s' %(len(cli_output_lines[lines]), cli_output_lines[lines]))

    #Compare output line-by-line(from the first to the last cli line) to the expected lines
    logger.debug('Compare output line-by-line')
    for item in cli_expected_output:
        for lines in range(first_line,len(cli_output_lines)):
            # Use regex to check expected output since COM5.0sh8 changed the cliss output
            regex = re.compile(item)
            if regex.search(cli_output_lines[lines]) is not None:
                all_matching = True
                break
            else:
                all_matching = False
        #If one of the expected elements missing, then it will break with False
        if all_matching == False:
            logger.error('Missing output: %s' %item)
            break
    #Compare output line-by-line(from the first to the last cli line) to the non-expected lines
    logger.debug('Look for non-existing items line-by-line')
    for item in cli_nonexpected_output:
        for lines in range(first_line,len(cli_output_lines)):
            if item.lower() in cli_output_lines[lines].lower():
                nonexpected_item_present = True
                break
            else:
                nonexpected_item_present = False
        #If one of the non-expected elements missing, then it will break with False
        if nonexpected_item_present == True:
            logger.error('Non-expected items found: %s' %item)
            break

    if all_matching == True and nonexpected_item_present == False:
        ret = 'SUCCESS'
        comp_result = 'CLI output is matching to the expected output and non-expected items are not present'
        logger.info('%s' %comp_result)
    else:
        ret = 'ERROR'
        comp_result = 'CLI output is NOT matching to the expected output or non-expected items are present'
        logger.error('%s' %comp_result)

    logger.debug('leave check_CLI_output function')
    return (ret, comp_result)

def runCliSession(lists, index, cli_active_controller_login_params):

    cli_input_list = lists[0]
    cli_expected_output_list = lists[1]
    cli_nonexpected_output_list = lists[2]

    cmd = '%s %s' %(cli_active_controller_login_params, cli_input_list[index])
    result = executeCliSession(cmd)
    if result[0] != 'SUCCESS':
        return result
    debug_logger_line_by_line(result[1].splitlines())
    cli_output_lines = result[1].splitlines()

    #Compare cli output to the expected output
    cli_expected_output = eval(cli_expected_output_list[index])
    cli_nonexpected_output = eval(cli_nonexpected_output_list[index])
    logger.debug('Checking CLI output')
    result = check_CLI_output(cli_output_lines, cli_expected_output, cli_nonexpected_output)
    print "check_CLI_output result is: %s %s" %(result[0],result[1])
    if result[0] != 'SUCCESS':
        return result
    misc_lib.waitTime(1)

    return ('SUCCESS', 'OK')


def load_TC_imm_config(self):
    '''
    This method loads the configs from the data received from the xml,
     and creates a list of the IMM inputs, expected outputs, non-expected outputs.
    1. Checking the data received from the xml
    2. Create list
    3. return list

    The method returns 3 lists:
     (imm_input_list, imm_expected_output_list, imm_nonexpected_output_list)

    '''
    self.myLogger.debug('enter load_TC_IMM_config function')
    imm_input_list = []
    imm_expected_output_list = []
    imm_nonexpected_output_list = []
    #Only append to the corresponding list if the IMM input and the expected output is present
    if self.imm_input_1 != {} and self.imm_expected_output_1 != {} and self.imm_nonexpected_output_1 != {}:
        imm_input_list.append(self.imm_input_1)
        imm_expected_output_list.append(self.imm_expected_output_1)
        imm_nonexpected_output_list.append(self.imm_nonexpected_output_1)
    if self.imm_input_2 != {} and self.imm_expected_output_2 != {} and self.imm_nonexpected_output_2 != {}:
        imm_input_list.append(self.imm_input_2)
        imm_expected_output_list.append(self.imm_expected_output_2)
        imm_nonexpected_output_list.append(self.imm_nonexpected_output_2)
    if self.imm_input_3 != {} and self.imm_expected_output_3 != {} and self.imm_nonexpected_output_3 != {}:
        imm_input_list.append(self.imm_input_3)
        imm_expected_output_list.append(self.imm_expected_output_3)
        imm_nonexpected_output_list.append(self.imm_nonexpected_output_3)


    self.myLogger.debug('leave load_TC_IMM_config function')
    return (imm_input_list, imm_expected_output_list, imm_nonexpected_output_list)

def check_IMM_output(imm_output_lines, imm_expected_output, imm_nonexpected_output):
    '''
    This method compares the imm output to the expected.
    1. Compare output line-by-line(from the first to the last imm line) to the expected lines
    2. Process and return result

    The method returns:
     'SUCCESS', 1 - if the imm output matches to the expected output
     'ERROR', 0 - if the imm output not matches to the expected output

    '''
    logger.debug('enter check_IMM_output function')
    all_matching = False
    nonexpected_item_present = True
    comp_result = ''

    #Compare output line-by-line(from the first to the last imm line) to the expected lines
    logger.debug('Compare output line-by-line')
    for item in imm_expected_output:
        for lines in range(0,len(imm_output_lines)):
            #if imm_output_lines[lines] == item:
            if item in imm_output_lines[lines]:
                all_matching = True
                break
            else:
                all_matching = False
        #If one of the expected elements missing, then it will break with False
        if all_matching == False:
            logger.error('Missing output: %s' %item)
            break
    #Compare output line-by-line(from the first to the last imm line) to the non-expected lines
    logger.debug('Look for non-existing items line-by-line')
    for item in imm_nonexpected_output:
        for lines in range(0,len(imm_output_lines)):
            if item in imm_output_lines[lines]:
                nonexpected_item_present = True
                break
            else:
                nonexpected_item_present = False
        #If one of the non-expected elements missing, then it will break with False
        if nonexpected_item_present == True:
            logger.error('Non-expected items found: %s' %item)
            break

    if all_matching == True and nonexpected_item_present == False:
        ret = 'SUCCESS'
        comp_result = 'IMM output is matching to the expected output and non-expected items are not present'
        logger.info('%s' %comp_result)
    else:
        ret = 'ERROR'
        comp_result = 'IMM output is NOT matching to the expected output or non-expected items are present'
        logger.error('%s' %comp_result)

    logger.debug('leave check_IMM_output function')
    return (ret, comp_result)

def runImmSession(lists, index):

    imm_input_list = lists[0]
    imm_expected_output_list = lists[1]
    imm_nonexpected_output_list = lists[2]

    cmd = '%s' %(imm_input_list[index])
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        return result
    debug_logger_line_by_line(result[1].splitlines())
    imm_output_lines = result[1].splitlines()

    #Compare imm output to the expected output
    imm_expected_output = eval(imm_expected_output_list[index])
    imm_nonexpected_output = eval(imm_nonexpected_output_list[index])
    logger.debug('Checking IMM output')
    result = check_IMM_output(imm_output_lines, imm_expected_output, imm_nonexpected_output)
    if result[0] != 'SUCCESS':
        return result
    misc_lib.waitTime(1)

    return ('SUCCESS', 'OK')


def debug_logger_line_by_line(output_lines):
    '''This method creates debug-level logs line-by-line using logger.debug'''
    for lines in output_lines:
        logger.debug(lines)
    return


def removeImmObjects(pattern, subrack = 0, slot = 0):
    """ In order to clean the IMM from the objects and classes in a dynamic way we need to define a list of patterns
    of the imm_objects which should be searched for with immlist and all the matches will be removed with immcfg -d.
    We have to be careful what we provide and should always test manually before automating, to make sure that we
    do not remove something that should remain!
    """
    ret = ('ERROR', '')
    cmd = 'immfind | grep -i %s | xargs immcfg -d' %pattern
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[0] != 'SUCCESS':
        ret = result
    if result[1] != '':
        logger.info('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))
        ret = ('ERROR', 'The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))
    else:
        ret = ('SUCCESS', 'Operation succeeded')

    return ret

def removeImmClassesFromImportedModelFile(pathToImmClassesFile, subrack = 0, slot = 0):
    '''
    pathToImmClassesFile has to contain the absolute path to the imm_classes file including the file name
    '''
    cmd = """grep "<class" %s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(pathToImmClassesFile)
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    if result[1] != '':
        return ('ERROR','The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
    else:
        return ('SUCCESS', 'OK')


def getEventTimestampFromComLog(subrack, slot, searchPatterns, startTime, logPattern , logDir):
    '''
    This method will return the timestamp of all the events in which the elements of the search pattern were found.

    The method only returns the matches that occued after the startTime (defined in unix time)

    Main steps:
    1. select relevant syslog file based on the time stamp of the first entry in the syslog
    2. search occurencies of the event defined by the search patterns
    3. remove matches from before the startTime
    4. returns a list of unix times of the events found

    Arguments:
    int subrack
    int slot
    list [searchPatterns]
    int startTime (unix time)

    Returns
    ('ERROR', 'error message')
    ('SUCCESS', [list of ints representing unix times])
    '''

    logger.debug('enter getEventTimestampFromComLog()')

# 1. select relevant syslog files based on the time stamp of the first entry in the syslog

    cmd = 'ls -t %s | grep %s' %(logDir, logPattern)
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getEventTimestampFromComLog()')
        return result
    messagesFiles = result[1].splitlines()
    messagesFile = ''
    for messageFile in messagesFiles:
        result = ssh_lib.sendCommand("""head -1 %s/%s | awk '{print $2" "$3}'"""%(logDir, messageFile))
        if result[0] != 'SUCCESS':
            logger.debug('leave getEventTimestampFromComLog()')
            return result
        result = lib.timeConv(result[1])
        if result[0] != 'SUCCESS':
            logger.debug('leave getEventTimestampFromComLog()')
            return result
        unixTime = result[1]
        if unixTime < startTime:
            messagesFile = messageFile
            break

    if messagesFile == '':
        messagesFile = messagesFiles[len(messagesFiles)-1]
        logger.warn('No syslog file found with log begin before defined startTime. Start parsing from oldest to newest log file!')
        #return ('ERROR', 'No syslog file found with log begin before defined startTime')

    messagesFilesConsidered =  messagesFiles[:messagesFiles.index(messagesFile)+1]
    messagesFilesConsidered.reverse()

# 2. search occurencies of the component getting active state
    if "type 'list'" not in str(type(searchPatterns)):
        logger.error('The search patterns were not defined in a list. It must be specified in a list of strings.')
        logger.debug('leave getEventTimestampFromComLog()')
        return ('ERROR', 'The search patterns were not defined in a list. It must be specified in a list of strings.')
    if len(searchPatterns) == 0:
        logger.error('The search pattern list is empty. Nothing to search for!')
        logger.debug('leave getEventTimestampFromComLog()')
        return ('ERROR', 'The search pattern list is empty. Nothing to search for!')


    readableTimes = []
    for messagesFile in messagesFilesConsidered:
        cmd = """grep -i "%s" %s/%s""" %(searchPatterns[0], logDir, messagesFile)
        if len(searchPatterns) > 1:
            for i in range(len(searchPatterns)-1):
                cmd += """| grep -i "%s" """ %(searchPatterns[i+1])
        cmd += """| awk '{print $2" "$3}'"""
        result = ssh_lib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            logger.debug('leave getEventTimestampFromComLog()')
            return result
        if result[1] != '':
            tempList = result[1].splitlines()
            for element in tempList:
                readableTimes.append(element)


    if len(readableTimes) == 0:
        logger.debug('leave getEventTimestampFromComLog()')
        return ('ERROR', 'No entry found in the syslog for the following search pattern: %s' %str(searchPatterns))

    unixTimes = []
    for readableTime in readableTimes:
        result = lib.timeConv(readableTime)
        if result[0] != 'SUCCESS':
            logger.debug('leave getEventTimestampFromComLog()')
            return result
        unixTimes.append(result[1])

# 3. remove matches from before the startTime
    timesAfterStartTime = []
    for unixTime in unixTimes:
        if unixTime >= startTime:
            timesAfterStartTime.append(unixTime)

    if len(timesAfterStartTime) == 0:
        return ('ERROR', 'No entry found in the syslog after the start time for the following search pattern: %s' %str(searchPatterns))
    else:
        result = ('SUCCESS', timesAfterStartTime)


    logger.debug('leave getEventTimestampFromComLog()')
    return result


def processRestart(subrack, slot, processName = '', path = '', pid = ''):
    if pid == '':
        result = getProcessId(subrack, slot, processName, path)
        if result[0] != 'SUCCESS':
            return result
        else:
            pid = result[1]
            if 'int' in str(type(pid)):
                pid = [pid]
                if len(pid) != 1:
                    logger.warn("More than 1 PID found. All will be restarted!")

    for processId in pid:
        cmd = 'kill %d' %processId
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        if result[0] != 'SUCCESS':
            return result

    result = getProcessId(subrack, slot, processName, path)
    if result[0] != 'SUCCESS':
        return result
    newPid = result[1]
    if 'int' in str(type(newPid)):
        newPid = [newPid]
    for newProcessId in newPid:
        if newProcessId in pid:
            return ('ERROR', 'Same PID %s found after process restart' %newProcessId)

    return('SUCCESS', newPid)

def findAndRestartActiveProcessFromPattern(pattern, testConfig):
    ntfCtrl = (0,0)
    for controller in testConfig['controllers']:
        result = getProcessId(controller[0], controller[1], '', path = pattern)
        if result[0] == 'SUCCESS':
            ntfCtrl = controller
            break
    if ntfCtrl == (0,0):
        return ('ERROR', 'No controller found with active instance ')
    pid = result[1]
    if 'int' not in str(type(pid)):
        return ('ERROR', 'Expected a result of type int from call to function getProcessId().')
    result = processRestart(ntfCtrl[0], ntfCtrl[1], pid = [pid], path = pattern)
    return result

def reInstallComponents(self, buildComSa, buildSrc, buildRelease, sdpNames, swDir, uninstallScriptLocation, \
                        uninstallScriptName, testConfig, testSuiteConfig, buildTokenDir, sshKeyUpdater, \
                        components_to_install = ["CMW","COM","COMSA"], destinationOnTarget = '/home/release/autoinstall/', \
                        createBackup = True, resetCluster = 'undef', makeOption = '', useComsaBuild = False):
    """
    The function cleans the test target (uninstalls components), restarts the cluster and then installs Core MW and optionally COM and COM-SA (defined by installation level)
    Interface:
    buildComSa: string: 'True' or 'False': COM-SA will wither be built from the function or a ready COM-SA build is used from swDir
    buildSrc: string: the location where COM-SA is built
    buildRelease: string: the location where the binaries are put after the build of COM-SA
    sdpNames: list of strings: [cxpSdpName, installSdpName, installSdpNameSingle]
    swDir: string: location where the binaries for the installation are placed. Under swDir the following direcotries are needed: coremw, com, comsa.
            The installation binaries for each component have to be in the respective sub-directory
    uninstallScriptLocation: string: absolute path of the uninstall script
    uninstallScriptName: string: name of the uninstall script
    testConfig: dictionary: self.testConfig
    components_to_install: list of string:
        example inputs:
        ['CMW']
        ['COM']
        ['COMSA']
        ['CMW','COM','COMSA']
    makeOption: make or make coverage
    Returns:
        ('SUCCESS', '') in case of successful installation
        ('ERROR', 'some relevant error message')

    """

    logger.debug('enter reInstallComponents (%s)' %str(components_to_install))

    coreMwTarFileName = ''
    comRtSdp = ''
    comInstSdp = ''
    comsaRtSdp = ''
    comsaInstSdp = ''
    comsaRemoveSdp = ''
    comsaTempTar = ''
    comsaRunTimeTar = ''

    coreMwTarFileNameFullPath = ''
    comRtSdpFullPath = ''
    comInstSdpFullPath = ''
    comsaRtSdpFullPath = ''
    comsaInstSdpFullPath = ''
    comsaTempTarFullPath = ''
    comsaRunTimeTarFullPath = ''
    if buildComSa == 'True' and "COMSA" in components_to_install:
        # Get a build token
        for i in range(numberOfGetTokenRetries):
            result = getBuildToken(suiteLogDir, buildTokenDir, tokenPattern)
            if result[0] == 'SUCCESS':
                break
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result
        if useComsaBuild == False:
            result = buildCOMSA(buildSrc, buildRelease, len(testConfig['controllers']), sdpNames, makeOption)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave reInstallComponents')
                return result
            result = copyComSaSdpsToSwDir(buildRelease, swDir, len(testConfig['controllers']), sdpNames, self.linuxDistro)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave reInstallComponents')
                return result
        else:
            result = buildCOMSAScript(buildSrc, buildRelease, len(testConfig['controllers']), sdpNames, self.linuxDistro)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave reInstallComponents')
                return result
            result = copyComSaSdpsToSwDir(buildRelease, swDir, len(testConfig['controllers']), sdpNames, self.linuxDistro)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave reInstallComponents')
                return result
            result = copyComSaCxpArchiveToSwDir(buildRelease, swDir, self.linuxDistro)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave reInstallComponents')
                return result

        # Release the build token
        result = releaseToken(suiteLogDir, buildTokenDir, tokenPattern)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result

    result = checkIfSwInPlace(swDir, components_to_install, self.distroTypes, self.linuxDistro)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave reInstallComponents')
        return result

    coreMwTarFileName = result[1]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'cmw', ['runtimeTar', coreMwTarFileName])

    comRtSdp = result[2]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'com', ['runtime', comRtSdp])

    comInstSdp = result[3]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'com', ['install', comInstSdp])

    comsaRtSdp = result[4]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'comsa', ['runtime', comsaRtSdp])

    comsaInstSdp = result[5]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'comsa', ['install', comsaInstSdp])

    comsaRemoveSdp = result[6]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'comsa', ['remove', comsaRemoveSdp])

    comsaTempTar = result[7]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'comsa', ['runtimeTar', comsaTempTar])

    comsaRunTimeTar = result[8]
    addDataToTestSuiteConfig(testSuiteConfig, 'instFileNames', 'comsa', ['templateTar', comsaRunTimeTar])

    coreMwTarFileNameFullPath = result[9]
    comRtSdpFullPath = result[10]
    comInstSdpFullPath = result[11]
    comsaRtSdpFullPath = result[12]
    comsaInstSdpFullPath = result[13]
    comsaRemoveSdpFullPath = result[14]
    comsaTempTarFullPath = result[15]
    comsaRunTimeTarFullPath = result[16]

    lib.refreshSshLibHandlesAllSCs(testConfig)

    if resetCluster != 'undef':
        logger.info('Restore snapshot %s' %resetCluster)
        result = unInstallSystem(destinationOnTarget, uninstallScriptName, testConfig, testSuiteConfig, self.linuxDistro, self.distroTypes, sshKeyUpdater, resetCluster = resetCluster)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result

    # remove the destinationOnTarget only the first time, since copyFilesToTarget removes it.
    removeDir = True

    # copy the files to target
    # Note: do the copy of all components first. If there is a problem with copying, it should be caught as early as possible (not after installation of some of the components).
    if "CMW" in components_to_install:
        result = copyFilesToTarget(['%s/%s' %(uninstallScriptLocation, uninstallScriptName), coreMwTarFileNameFullPath], destinationOnTarget, removeDir)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result
        removeDir = False
    if "COM" in components_to_install:
        result = copyFilesToTarget([comRtSdpFullPath, comInstSdpFullPath], destinationOnTarget, removeDir)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result
        removeDir = False
    if "COMSA" in components_to_install:
        result = copyFilesToTarget([comsaRtSdpFullPath, comsaInstSdpFullPath, comsaRemoveSdpFullPath], destinationOnTarget, removeDir)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result

    # uninstall components and install CMW
    if "CMW" in components_to_install:
        if resetCluster == 'undef':
            logger.debug('uninstall components')
            result = unInstallSystem(destinationOnTarget, uninstallScriptName, testConfig, testSuiteConfig, self.linuxDistro, self.distroTypes, sshKeyUpdater, resetCluster = resetCluster)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave reInstallComponents')
                return result
        logger.debug('install CMW')
        result = installCoreMw(destinationOnTarget, coreMwTarFileName, createBackup, backupRpms = self.backupRpmScript)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result

    # install COM
    if "COM" in components_to_install:
        logger.debug('install COM')
        if comRtSdp == '' or comInstSdp == '':
            logger.debug('leave reInstallComponents')
            return ('ERROR', 'reInstallComponents: comRtSdp or comInstSdp have not been assigned a value')
        result = installComp(destinationOnTarget, comRtSdp, comInstSdp, 'com', createBackup, backupRpms = self.backupRpmScript)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result

    # install COMSA
    if "COMSA" in components_to_install:
        if comsaRtSdp == '' or comsaInstSdp == '':
            logger.debug('leave reInstallComponents')
            return ('ERROR', 'reInstallComponents: comsaRtSdp or comsaInstSdp have not been assigned a value')
        logger.debug('install COMSA')
        result = installComp(destinationOnTarget, comsaRtSdp, comsaInstSdp, 'comsa', createBackup, backupRpms = self.backupRpmScript)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result
        campaignStartTime = result[2]
        campaignName = result[3]

        result = calculateComponentInstallationTime(campaignStartTime, campaignName, testConfig)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave reInstallComponents')
            return result
        comsaInstallationTime = result[1]
        logger.info('COM SA installation time was: %d' %comsaInstallationTime)
        ret = ('SUCCESS', comsaInstallationTime)

    logger.debug('leave reInstallComponents')
    if "COMSA" in components_to_install:
        return ret
    else:
        return result

def calculateComponentInstallationTime(startTime, campaignName, testConfig):
    endTime = []
    searchPattern = ['Upgrade campaign completed safSmfCampaign=%s'%campaignName]
    for controller in testConfig['controllers']:
        result = lib.getEventTimestampFromSyslog(controller[0], controller[1], searchPattern, startTime, testConfig)
        if result[0] == 'SUCCESS' and len(result[1]) > 1:
            return('ERROR', 'More than one match for installation complete message after given startTime. This was unexpected. Received timestamps: %s' %result[1])
        elif result[0] == 'SUCCESS' and len(result[1]) == 1:
            endTime.append(result[1][0])
    if len(endTime) != 1:
        return ('ERROR', 'Expected exacly one timestamp for end of installation log entry. Received: %s' %endTime)
    installationTime = endTime[0] - startTime
    return ('SUCCESS', installationTime)

def checkIfSwInPlace(localPathToSw, components_to_install, distroTypes, linuxDistro):
    """
    The method checks if the files needed for the installation of the components are in place.
    It is expected that there is
        - only one Core MW tar file in the localPathToSw/coremw directoruy
        - Exactly one CXP and one campaign file in the com and comsa directories under localPathToSw/compName/
    Returns:
        ('SUCCESS', coreMwTarFileName, comRtSdp, comInstSdp, comsaRtSdp, comsaInstSdp, \
            coreMwTarFileNameFullPath, comRtSdpFullPath, comInstSdpFullPath, comsaRtSdpFullPath, comsaInstSdpFullPath)
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter checkIfSwInPlace')
    coreMwTarFileName = ''
    comRtSdp = ''
    comInstSdp = ''
    comsaRtSdp = ''
    comsaInstSdp = ''
    comsaRemoveSdp = ''
    comsaTempTar=''
    comsaRunTimeTar=''

    coreMwTarFileNameFullPath = ''
    comRtSdpFullPath = ''
    comInstSdpFullPath = ''
    comsaRtSdpFullPath = ''
    comsaInstSdpFullPath = ''
    comsaRemoveSdpFullPath = ''
    comsaTempTarFullPath=''
    comsaRunTimeTarFullPath=''

    if "CMW" in components_to_install:
        logger.debug('"CMW" is in components_to_install')
        result = findFilesMatchingPattern('%scoremw/*.tar*' %localPathToSw)
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one Core MW tar file found at specified location: %scoremw/: %s.' %(localPathToSw, str(result[1])))
        coreMwTarFileNameFullPath = result[1][0].strip()
        coreMwTarFileName = coreMwTarFileNameFullPath.split('/')[len(coreMwTarFileNameFullPath.split('/')) - 1]

    if "COM" in components_to_install:
        logger.debug('"COM" is in components_to_install')
        result = findFilesMatchingPattern('%scom/COM-*.sdp' %localPathToSw)
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one COM runtime sdp file found at specified location: %scom/: %s.' %(localPathToSw, str(result[1])))
        comRtSdpFullPath = result[1][0].strip()
        comRtSdp = comRtSdpFullPath.split('/')[len(comRtSdpFullPath.split('/')) - 1]

        result = findFilesMatchingPattern('%scom/ERIC-COM-I*.sdp' %localPathToSw)
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one COM campaign sdp file found at specified location: %scom/: %s.' %(localPathToSw, str(result[1])))
        comInstSdpFullPath = result[1][0].strip()
        comInstSdp = comInstSdpFullPath.split('/')[len(comInstSdpFullPath.split('/')) - 1]

    if "COMSA" in components_to_install:
        logger.debug('"COMSA" is in components_to_install')
        result = findFilesMatchingPattern('%scomsa/*CXP*sdp' %localPathToSw)
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one COM SA runtime sdp file found at specified location: %scomsa/: %s.' %(localPathToSw, str(result[1])))
        comsaRtSdpFullPath = result[1][0].strip()
        comsaRtSdp = comsaRtSdpFullPath.split('/')[len(comsaRtSdpFullPath.split('/')) - 1]

        result = findFilesMatchingPattern('%scomsa/*install*sdp' %localPathToSw)
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one COM SA installation sdp file found at specified location: %scomsa/: %s.' %(localPathToSw, str(result[1])))
        comsaInstSdpFullPath = result[1][0].strip()
        comsaInstSdp = comsaInstSdpFullPath.split('/')[len(comsaInstSdpFullPath.split('/')) - 1]

        cmd = 'ls %scomsa/*remove*sdp' %(localPathToSw)
        result = findFilesMatchingPattern('%scomsa/*remove*sdp' %localPathToSw)
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one COM SA remove sdp file found at specified location: %scomsa/: %s.' %(localPathToSw, str(result[1])))
        comsaRemoveSdpFullPath = result[1][0].strip()
        comsaRemoveSdp = comsaRemoveSdpFullPath.split('/')[len(comsaRemoveSdpFullPath.split('/')) - 1]
        #Find tar file for COM_SA_D_TEMPLATE
        if linuxDistro == distroTypes[1]: # rhel
            comsaTmplCxp = "CXP9028075"
            comsaRunTimeCxp = "CXP9028074"
        else:
            comsaTmplCxp = "CXP9017695"
            comsaRunTimeCxp = "CXP9018914"
        result = findFilesMatchingPattern('%scomsa/*%s*.tar*' %(localPathToSw, comsaTmplCxp))
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one *%s*.tar* file found at specified location: %scomsa/: %s.' %(comsaTmplCxp, localPathToSw, str(result[1])))
        comsaTempTarFullPath = result[1][0].strip()
        comsaTempTar = comsaTempTarFullPath.split('/')[len(comsaTempTarFullPath.split('/')) - 1]

        #Find tar file for COM_SA_RUNTIME
        result = findFilesMatchingPattern('%scomsa/*%s*.tar' %(localPathToSw, comsaRunTimeCxp))
        if result[0] != 'SUCCESS':
            logger.debug('leave checkIfSwInPlace')
            return result
        if len(result[1]) > 1:
            logger.debug('leave checkIfSwInPlace')
            return ('ERROR', 'checkIfSwInPlace: More than one *%s*.tar file found at specified location: %scomsa/: %s.' %(comsaRunTimeCxp, localPathToSw, str(result[1])))
        comsaRunTimeTarFullPath = result[1][0].strip()
        comsaRunTimeTar = comsaRunTimeTarFullPath.split('/')[len(comsaRunTimeTarFullPath.split('/')) - 1]


    result = ('SUCCESS', coreMwTarFileName, comRtSdp, comInstSdp, comsaRtSdp, comsaInstSdp, comsaRemoveSdp, comsaTempTar, comsaRunTimeTar, \
            coreMwTarFileNameFullPath, comRtSdpFullPath, comInstSdpFullPath, comsaRtSdpFullPath, comsaInstSdpFullPath, comsaRemoveSdpFullPath, \
            comsaTempTarFullPath, comsaRunTimeTarFullPath)
    logger.debug('SW list:')
    logger.debug('   coreMwTarFileName: \"%s\"' %coreMwTarFileName)
    logger.debug('   comRtSdp: \"%s\"' %comRtSdp)
    logger.debug('   comInstSdp: \"%s\"' %comInstSdp)
    logger.debug('   comsaRtSdp: \"%s\"' %comsaRtSdp)
    logger.debug('   comsaInstSdp: \"%s\"' %comsaInstSdp)
    logger.debug('   comsaRemoveSdp: \"%s\"' %comsaRemoveSdp)
    logger.debug('   comsaTempTar: \"%s\"' %comsaTempTar)
    logger.debug('   comsaRunTimeTar: \"%s\"' %comsaRunTimeTar)
    logger.debug('   coreMwTarFileNameFullPath: \"%s\"' %coreMwTarFileNameFullPath)
    logger.debug('   comRtSdpFullPath: \"%s\"' %comRtSdpFullPath)
    logger.debug('   comInstSdpFullPath: \"%s\"' %comInstSdpFullPath)
    logger.debug('   comsaRtSdpFullPath: \"%s\"' %comsaRtSdpFullPath)
    logger.debug('   comsaInstSdpFullPath: \"%s\"' %comsaInstSdpFullPath)
    logger.debug('   comsaRemoveSdpFullPath: \"%s\"' %comsaRemoveSdpFullPath)
    logger.debug('   comsaTempTarFullPath: \"%s\"' %comsaTempTarFullPath)
    logger.debug('   comsaRunTimeTarFullPath: \"%s\"' %comsaRunTimeTarFullPath)
    logger.debug('leave checkIfSwInPlace')
    return result

def findFilesMatchingPattern(pattern, onTarget = False):
    """
    onTarget = False: files are searched locally
    onTarget = True: files are searched on the target
    """
    logger.debug('enter findFilesMatchingPattern')
    cmd = 'ls %s' %pattern
    if onTarget == True:
        result = ssh_lib.sendCommand(cmd)
    elif onTarget == False:
        result = misc_lib.execCommand(cmd)

    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave findFilesMatchingPattern')
        return result
    if 'No such file or directory' in result[1]:
        logger.debug('leave findFilesMatchingPattern')
        return ('ERROR', 'findFilesMatchingPattern: file not found matching pattern: %s.' %pattern)

    logger.debug('leave findFilesMatchingPattern')
    return ('SUCCESS', result[1].splitlines())

def copyFilesToTarget(fileList, destinationOnTarget, removeDestinationOnTarget =  True):
    """
    WARNING: Using this method will result in cleaning the content of destinationOnTarget!!!
    The method copies the files in the fileList to the test target to destinationOnTarget
    fileList is a list of strings
    destinationOnTarget is a string

    Returns:
        ('SUCCESS', 'copyFilesToTarget: Files successfully copied to the target.')
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter copyFilesToTarget')
    if removeDestinationOnTarget:
        cmd = '\\rm -rf %s' %destinationOnTarget
        result = ssh_lib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave copyFilesToTarget')
            return result
    cmd = 'mkdir -p %s' %destinationOnTarget
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave copyFilesToTarget')
        return result

    logger.debug('copy file(s) in fileList')
    logger.info('file list: %s' %fileList)
    for file in fileList:
        if file != None and file != "":
            logger.debug('file is \"%s\"' %file)
            result = ssh_lib.remoteCopy(file, destinationOnTarget, timeout = 120, numberOfRetries = 5)
            if result[0] != 'SUCCESS':
                logger.debug('copying file(s) from fileList FAILED')
                logger.error(result[1])
                logger.debug('leave copyFilesToTarget')
                return result
        elif file == "":
            logger.error("file is empty")
            return ['ERROR','file is empty']

    logger.debug('leave copyFilesToTarget')
    return ('SUCCESS', 'copyFilesToTarget: Files successfully copied to the target.')


def unInstallSystem(tmpDirOnTarget, uninstallScriptName, testConfig, testSuiteConfig, linuxDistro, distroTypes, sshKeyUpdater, resetCluster = 'undef'):
    """
    The method is running the uninstallation script, restarts the test target and then runs the unsinstallation script one more time
    tmpDirOnTarget: string: absolute path where the uninstallation script is located on the test target
    uninstallScriptName: string: name of the uninstall script
    testConfig: dictionary: self.testConfig
    Returns:
        ('SUCCESS', 'unInstallSystem: Uninstallation of system completed.')
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter unInstallSystem')
    if resetCluster == 'undef':
        cmd = 'chmod u+x %s%s' %(tmpDirOnTarget, uninstallScriptName)
        result = ssh_lib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result

        uninstallationSshTimeout = 300

        result = ssh_lib.setTimeout(uninstallationSshTimeout)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result

        cmd = '%s%s' %(tmpDirOnTarget, uninstallScriptName)
        result = ssh_lib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result
        if 'Error: All nodes not up, Exiting' in result[1]:
            logger.debug('leave unInstallSystem')
            return ('ERROR', 'unInstallSystem: Execution of uninstallation script failed. %s' %result[1])

        # Doing uninstall causes all existing backups to be removed.
        # therefore the backup stored under testSuiteConfig['restoreBackup'] will be lost
        if testSuiteConfig.has_key('restoreBackup'):
            testSuiteConfig.__delitem__('restoreBackup')

        ssh_lib.tearDownHandles()

        result = calculateLatestSystemStartup(testConfig, linuxDistro, distroTypes)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result
        currentStartUpTimes = result[1]

        result = ssh_lib.sendCommand('cluster reboot -a')
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result

        misc_lib.waitTime(150)

        result = waitForMoreRecentStartUpTime(currentStartUpTimes, testConfig, linuxDistro, distroTypes)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result

        result = waitForTipcUp(testConfig)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result

        result = ssh_lib.setTimeout(uninstallationSshTimeout)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result

        result = ssh_lib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result
        if 'Error: All nodes not up, Exiting' in result[1]:
            logger.debug('leave unInstallSystem')
            return ('ERROR', 'unInstallSystem: Execution of uninstallation script failed. %s' %result[1])
    else:
        result = hw_lib.virtualTargetSnapRestore(resetCluster)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result
        # In the test cases if we use snapshots to clean the system
        # we do not backup the cluster and do not restore it after the tests
        # therefore the backup stored under testSuiteConfig['restoreBackup'] will be lost
        if testSuiteConfig.has_key('restoreBackup'):
            testSuiteConfig.__delitem__('restoreBackup')
        result = hw_lib.waitForPingAllCtrlInClusterOK(testConfig)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result
        # It takes time between the blade is pingable and the SSH daemon starts. This may need further adjustment.
        misc_lib.waitTime(30)
        utils.updateLocalSshKeys(testConfig, sshKeyUpdater)
        lib.refreshSshLibHandlesAllSCs(testConfig)
        result = waitForTipcUp(testConfig)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave unInstallSystem')
            return result
        lib.updateLinuxDistroInDictionary(testSuiteConfig, distroTypes, force = True)

    lib.refreshSshLibHandlesAllSCs(testConfig)

    logger.debug('leave unInstallSystem')
    return ('SUCCESS', 'unInstallSystem: Uninstallation of system completed.')

def calculateLatestSystemStartup(testConfig, linuxDistro, distroTypes):
    controllerDict = {}

    lib.refreshSshLibHandlesAllSCs(testConfig)

    for controller in testConfig['controllers']:
        ssh_lib.setConfig(controller[0],controller[1],controller[1])
        result = ssh_lib.sendCommand("date +%s; uptime", controller[0], controller[1])
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave calculateLatestSystemStartup')
            return result
        if len(result[1].splitlines()) != 2:
            logger.debug('leave calculateLatestSystemStartup')
            return ('ERROR', 'Expected a response that has exacly two lines. Received: %s' %result[1])
        unixTimeOnTarget = result[1].splitlines()[0]
        if unixTimeOnTarget.isdigit() == True:
            unixTimeOnTarget = int(unixTimeOnTarget)
        else:
            logger.debug('leave calculateLatestSystemStartup')
            return ('ERROR', 'Expected a number representing the unix time on target. Received: %s' %result[1].splitlines()[0])
        uptimeLine = result[1].splitlines()[1]
        if 'day' in uptimeLine:
            days = uptimeLine.split()[2]
            if days.isdigit() == True:
                days = int(days)
            else:
                logger.debug('leave calculateLatestSystemStartup')
                return ('ERROR', 'Expected a number representing the days of uptime of the blade. Received: %s' %result[1].splitlines()[1])
            if len(uptimeLine.split()) > 3 and ':' in uptimeLine.split()[4]:
                uptimeLine = uptimeLine.split()[4]
                hours = uptimeLine.split(':')[0]
                if hours.isdigit():
                    hours = int(hours)
                else:
                    logger.debug('leave calculateLatestSystemStartup')
                    return ('ERROR', 'Expected a number representing the hours of uptime of the blade. Received: %s' %result[1].splitlines()[1])
                minutes = uptimeLine.split(':')[1][:-1]
                if minutes.isdigit() == True:
                    minutes = int(minutes)
                else:
                    logger.debug('leave calculateLatestSystemStartup')
                    return ('ERROR', 'Expected a number representing the minutes of uptime of the blade. Received: %s' %result[1].splitlines()[1])
            else:
                logger.debug('leave calculateLatestSystemStartup')
                return ('ERROR', 'Expected a field representing the hours:minutes of uptime of the blade. Received: %s' %result[1].splitlines()[1])
            uptimeSeconds = days*24*60*60 + hours*60*60 + minutes*60
        else:
            if linuxDistro == distroTypes[1] and uptimeLine.split()[3].strip() == "min,":
                minutes = uptimeLine.split()[2]
                if minutes.isdigit() == True:
                    minutes = int(minutes)
                uptimeSeconds = minutes*60
            else:
                uptimeLine = uptimeLine.split()[2]
                if ':' in uptimeLine:
                    hours = uptimeLine.split(':')[0]
                    if hours.isdigit():
                        hours = int(hours)
                    else:
                        logger.debug('leave calculateLatestSystemStartup')
                        return ('ERROR', 'Expected a number representing the hours of uptime of the blade. Received: %s' %result[1].splitlines()[1])
                    minutes = uptimeLine.split(':')[1][:-1]
                    if minutes.isdigit() == True:
                        minutes = int(minutes)
                    else:
                        logger.debug('leave calculateLatestSystemStartup')
                        return ('ERROR', 'Expected a number representing the minutes of uptime of the blade. Received: %s' %result[1].splitlines()[1])
                else:
                    logger.debug('leave calculateLatestSystemStartup')
                    return ('ERROR', 'Expected uptime information of the blade in the format hours:minutes. Received: %s' %uptimeLine)
                uptimeSeconds = hours*3600 + minutes*60

        controllerDict[controller] = unixTimeOnTarget - uptimeSeconds
    logger.debug('leave calculateLatestSystemStartup')
    return ('SUCCESS', controllerDict)

def waitForMoreRecentStartUpTime(controllerDict, testConfig, linuxDistro, distroTypes, timeout = 900, minimalDiff = 60, waitBetweenIterations = 5):
    logger.debug('enter waitForMoreRecentStartUpTime')
    #initialUptimes = controllerDict
    successDict = {}
    for controller in controllerDict.keys():
        successDict[controller] = False

    timeNow = int(time.time())
    endTime = timeNow + timeout

    while timeNow < endTime:
        result = calculateLatestSystemStartup(testConfig, linuxDistro, distroTypes)
        if result[0] == 'SUCCESS':
            newUptimes = result[1]
            for controller in controllerDict.keys():
                if newUptimes[controller] - controllerDict[controller] > minimalDiff:
                    successDict[controller] = True
        if False not in successDict.values():
            break
        misc_lib.waitTime(waitBetweenIterations)
        timeNow = int(time.time())

    if False not in successDict.values():
        logger.debug('leave waitForMoreRecentStartUpTime')
        return ('SUCCESS', 'New cluster startUpTime more recent than previously')
    else:
        logger.debug('leave waitForMoreRecentStartUpTime')
        return ('ERROR', 'No more recent startUpTime calculated for the controller blades.')


def waitForClusterUnavailable(testConfig, timeout = 900, waitBetweenIterations = 5):
    """
    The method makes sure that the cluster reboots.
    It will ping the controller blades until they are unavailable.
    """

    logger.debug('enter waitForClusterUnavailable')
    controllerList = copy.deepcopy(testConfig['controllers'])

    startTime = int(time.time())
    endTime = startTime + timeout
    currentTime = startTime
    clusterUnreacheable = False

    while currentTime < endTime and clusterUnreacheable == False:
        lib.refreshSshLibHandlesAllSCs(testConfig)
        for controller in controllerList:
            result = ssh_lib.sendCommand('echo "%s"; date' %str(controller), controller[0], controller[1])
            if result[0] != 'SUCCESS':
                controllerList.pop(controllerList.index(controller))
            if len(controllerList) == 0:
                clusterUnreacheable = True
                break
            misc_lib.waitTime(waitBetweenIterations)
        currentTime = int(time.time())

    if clusterUnreacheable == False:
        logger.debug('enter waitForClusterUnavailable')
        return ('ERROR', 'Cluster did not become unavailable in the allowed time frame of %d seconds.' %timeout)
    else:
        logger.debug('enter waitForClusterUnavailable')
        return ('SUCCESS', 'Cluster become unavailable.')


def waitForTipcUp(testConfig, timeout = 600, waitBetweenIterations = 10):
    """
    The method waits until the tipc links are up on the cluster
    testConfig: dictionary: self.testConfig
    timeout: int: maximum time in seconds to wait for the tipc links.
    waitBetweenIterations: int: time in seconds between checking the tipc links
    Returns:
        ('SUCCESS', 'waitForTipcUp: All tipc links up')
        ('ERROR', 'waitForTipcUp: All tipc links not up: %s' %result[1])
    """

    logger.debug('enter waitForTipcUp')
    if len(testConfig['controllers']) == 1:
        cmd = 'ls'
    else:
        cmd = 'tipc-config -n'

    okFlag = False
    for i in range(int(timeout/waitBetweenIterations)):
        result = ssh_lib.sendCommand(cmd)
        logger.debug('###tipc link status: %s' % result[1])
        # This condition is not good for 1-node clusters
        if len(testConfig['controllers']) == 1 and result[0] == 'SUCCESS':
            okFlag = True
            break
        if len(testConfig['controllers']) != 1 and result[0] == 'SUCCESS' and result[1].count('up') == len(testConfig['testNodesTypes']) - 1 :
            okFlag = True
            break
        misc_lib.waitTime(waitBetweenIterations)

    if okFlag == True:
        logger.debug('leave waitForTipcUp')
        return ('SUCCESS', 'waitForTipcUp: All tipc links up')
    else:
        logger.debug('leave waitForTipcUp')
        return ('ERROR', 'waitForTipcUp: All tipc links not up: %s' %result[1])

def waitForClusterStatusOk(waitTime = 900, timeBetweenIterations = 15):
    """
    The method waits for the cluster status to be OK.
    Interface:
        int waitTime: maximum time allowed for the method to check the status of the cluster
        int timeBetweenIterations: wait time between the iterations

    Returns:
        ('SUCCESS', 'Cluster status: OK')
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter waitForClusterStatusOk')
    okFlag = False
    timeNow = int(time.time())
    endTime = timeNow + waitTime
    while int(time.time()) < endTime:
        result = saf_lib.checkClusterStatus()
        if result == ('SUCCESS', 'Status OK'):
            logger.info(result[1])
            okFlag = True
            break
        else:
            ssh_lib.tearDownHandles()
            misc_lib.waitTime(timeBetweenIterations)

    if okFlag == False:
        ret = ('ERROR','Cmw status-check timeout')
    else:
        ret = ('SUCCESS', 'Cluster status: OK')

    logger.debug('leave waitForClusterStatusOk')
    return ret

def backupCreateWrapper(backupName, timeout = 2400, hostData = True, backupRpms = '/home/backup_rpms.sh'):

    result = lib.getLinuxDistro()
    if result[0] == 'SUCCESS':
        if result[1] != "RhelType":
            cmd = "find %s" %backupRpms
            result = ssh_lib.sendCommand(cmd)
            if result[0] != 'SUCCESS':
                return result
            else:
                if 'No such file or directory' in result[1]:
                    logger.warn('WARNING: There is no backup rpm script, backup/restore may have unexpected result!')
                else:
                    cmd = "%s -c %s" %(backupRpms, backupName)
                    result = ssh_lib.sendCommand(cmd)
                    if result[0] != 'SUCCESS':
                        return result
    else:
        return result

    result = saf_lib.backupCreate(backupName, timeout, False)
    if result[0] != 'SUCCESS':
        return result
    return ('SUCCESS','backupCreateWrapper success')

def backupRestoreWrapper(backupName, timeout = 2400, hostData = True, backupRpms = '/home/backup_rpms.sh'):

    result = saf_lib.backupRestore(backupName, timeout, False)
    if result[0] != 'SUCCESS':
        return result

    result = lib.getLinuxDistro()
    if result[0] == 'SUCCESS':
        if result[1] != "RhelType":
            cmd = "find %s" %backupRpms
            result = ssh_lib.sendCommand(cmd)
            if result[0] != 'SUCCESS':
                return result
            else:
                cmd = "%s -r %s" %(backupRpms, backupName)
                result = ssh_lib.sendCommand(cmd)
                if result[0] != 'SUCCESS':
                    return result
    else:
        return result

    return ('SUCCESS','backupRestoreWrapper success')


def installCoreMw(pathToCmwInstallation, coreMwTarFileName, createBackup = True, backupRpms = '/home/backup_rpms.sh'):
    """
    The method installs Core MW on the test target.
    pathToCmwInstallation: string: path on the target where the Core MW tar file is located
    coreMwTarFileName: string: name of the Core MW tar file

    Returns:
        ('SUCCESS', 'installCoreMw: CoreMW installation completed successfully')
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter installCoreMw')
    coreMwDir = 'coremw'
    cmd = 'mkdir -p %s%s;  \mv -f %s%s %s%s' %(pathToCmwInstallation, coreMwDir, pathToCmwInstallation, coreMwTarFileName, pathToCmwInstallation, coreMwDir)
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installCoreMw')
        return result

    pathToCmwInstallation = '%s%s' %(pathToCmwInstallation, coreMwDir)
    result = ssh_lib.sendCommand('cd %s; tar xvf %s' %(pathToCmwInstallation, coreMwTarFileName))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installCoreMw')
        return result
    if 'No such file or directory' in result[1]:
        logger.debug('leave installCoreMw')
        return ('ERROR', 'installCoreMw: File not found: %s/%s.' %(pathToCmwInstallation, coreMwTarFileName))

    cmd = 'chmod u+x %s/install' %pathToCmwInstallation
    result = ssh_lib.sendCommand (cmd)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installCoreMw')
        return result
    if 'No such file or directory' in result[1]:
        logger.debug('leave installCoreMw')
        return ('ERROR', 'installCoreMw: File not found: %s/install.' %pathToCmwInstallation)

    logger.debug('Getting Default Time out')
    result = ssh_lib.getTimeout()
    defTimeout = result[1]
    logger.debug('Setting Time Out to 3600 sec or one hour')
    ssh_lib.setTimeout(3600)

    cmd = 'cd %s; ./install' %pathToCmwInstallation
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installCoreMw')
        return result
    expectedPrintout = "Install script completed successfully"
    if 'No such file or directory' in result[1]:
        logger.debug('leave installCoreMw')
        return ('ERROR', 'installCoreMw: File not found: %s/install.' %pathToCmwInstallation)
    elif expectedPrintout not in result[1]:
        logger.debug('leave installCoreMw')
        return ('ERROR', 'installCoreMw: Expected printout "%s" not received. Installation log: %s' %(expectedPrintout, result[1]))
    logger.debug('Setting back the default time out : %s' %(defTimeout))

    ssh_lib.setTimeout(defTimeout)
    ssh_lib.tearDownHandles()

    misc_lib.waitTime(15)

    result = saf_lib.checkClusterStatus()
    if result != ('SUCCESS', 'Status OK'):
        logger.debug('leave installCoreMw')
        return ('ERROR','installCoreMw: cmw-status command did not return OK after installation of Core MW')

    if createBackup:
        backupName = 'cmw_autobackup'
        result = saf_lib.isBackup(backupName)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave installCoreMw')
            return result
        elif result != ('SUCCESS','NOT EXIST'):
            result = saf_lib.backupRemove(backupName)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave installCoreMw')
                return result
        result = backupCreateWrapper(backupName, backupRpms = backupRpms)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave installCoreMw')
            return result

    logger.debug('leave installCoreMw')
    return ('SUCCESS', 'installCoreMw: CoreMW installation completed successfully')

def installComp(pathToAppInstallation, appRtSdp, appInstSdp, compName = 'comsa', createBackup = True,
                removeCampaign = False, charMeas = False, rollingUpgrade = False, acceptFailedBackup = False,
                createBackupDuringCampaign = False, backupRpms = '/home/backup_rpms.sh', supportBfuSameVer = False):
    """
    The method installs a component on the test target.
    pathToAppInstallation: string: path on the target where the component SDP files are located
    appRtSdp: string: name of the component runtime SDP file name
    appInstSdp: string: name of the component installation campaign file name
    compName: string: name of the component
    removeCampaign: Bool: if True an uninstallation is performed and appRtSdp is not used, but it still has to have a value (to keep backwards comp for the interface)

    Returns:
        ('SUCCESS', 'installComp: Component %s installed successfully.' %compName)
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter installComp')
    if removeCampaign == False and supportBfuSameVer == False:
        result = importSdpPackage('%s/%s' %(pathToAppInstallation, appRtSdp))
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave installComp')
            return result

    result = importSdpPackage('%s/%s' %(pathToAppInstallation, appInstSdp))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installComp')
        return result
    campaignName = result[1]

    result = getCurrentUnixTimeOnTarget()
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installComp')
        return result
    startTime = result[1]

#     createBackupDuringCampaign = not charMeas
#     createBackupDuringCampaign = False
    result = saf_lib.upgradeStart(campaignName, createBackupDuringCampaign)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installComp')
        return result

    result = waitForCampaignReady(campaignName, rollingUpgrade = rollingUpgrade)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installComp')
        return result

    result = saf_lib.upgradeCommit(campaignName)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installComp')
        return result

    result = saf_lib.removeSwBundle(campaignName)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave installComp')
        return result

    result = saf_lib.checkClusterStatus()
    if result != ('SUCCESS', 'Status OK'):
        logger.debug('leave installComp')
        return ('ERROR','installComp: cmw-status command did not return OK after installation of COM')

    if createBackup:
        backupName = '%s_autobackup' %compName
        result = lib.getLinuxDistro()
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave installComp')
            return result
        linuxDistro = result[1]
        if linuxDistro == 'RhelType': # due to unstable functionality on RHEL, always remove the backup before create, don't care result
            result = saf_lib.backupRemove(backupName)
        else:
            result = saf_lib.isBackup(backupName)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave installComp')
                return result
            elif result != ('SUCCESS','NOT EXIST'):
                result = saf_lib.backupRemove(backupName)
                if result[0] != 'SUCCESS':
                    logger.error(result[1])
                    logger.debug('leave installComp')
                    return result

        result = backupCreateWrapper(backupName, backupRpms = backupRpms)
        if result[0] != 'SUCCESS':
            if acceptFailedBackup == False:
                logger.error(result[1])
                logger.debug('leave installComp')
                return result
            else:
                logger.warn('Failed to create backup %s. Method returned: %s' %(backupName, str(result)))

    logger.debug('leave installComp')
    return ('SUCCESS', 'installComp: Component %s installed successfully.' %compName, startTime, campaignName)

def importSdpPackage(fileName):
    """
    The method is almost a copy of the saf_lib.importSdpPackage() method, with the difference that
        the Sdp package path can be specified and does not have to be under /home/coremw/incoming/

    fileName has to be absolute path on target System of the SDP package to be imported

    Returns:
        ('SUCCESS', 'output of cmw-sdp-import command')
        ('ERROR', 'some relevant error message')

    """
    logger.debug('enter importSdpPackage')
    cmd = 'cmw-sdp-import %s' %fileName
    result = ssh_lib.getTimeout()
    if result[0] == 'SUCCESS':
        initTimeout = result[1]
    else:
        logger.error(result[1])
        logger.debug('leave importSdpPackage')
        return result
    ssh_lib.setTimeout(600)
    result = ssh_lib.sendCommand(cmd)
    ssh_lib.setTimeout(initTimeout)
    if result[0] == 'SUCCESS' and 'command not found' not in result[1]:
        bundleStr = 'imported \(type=Bundle\)'
        campStr = 'imported \(type=Campaign\)'
        if re.search(bundleStr,result[1]) or re.search(campStr,result[1]):
            swBundlePackageId = result[1].split(' ')[0]
            result = ('SUCCESS', swBundlePackageId)
        elif re.search('Already imported', result[1]):
            logger.warn(result[1])
            swBundlePackageId = result[1].split('[')[1]
            swBundlePackageId = swBundlePackageId.split(']')[0]
            result = ('SUCCESS', swBundlePackageId)
        else:
            errorInfo = str(result[1])
            result =  ('ERROR',errorInfo)
            logger.error(errorInfo)
    else:
        errorInfo = 'Import sw bundle file %s FAILED: %s' %(fileName, result[1])
        result =  ('ERROR',errorInfo)
        logger.error(errorInfo)

    logger.debug('leave importSdpPackage')
    return result


def waitForCampaignReady(campaignName, timeout = 900, waitBetweenIterations = 15, campExpectedToFail = False, rollingUpgrade = False):
    """
    The method monitors the status of a campaign and returns as soon as the campaing finishes or an error is detected or the timeout has been passed.
    campaignName: string: the name of the campaign to be monitored
    timeout: int: the maximum amount of time in seconds the method will execute
    waitBetweenIterations: int: the amount of time in seconds between checking the camapaign status
    campExpectedToFail: bool: In certain test cases it is expected that the camapaing will fail.
        When campExpectedToFail is True and the campaign fails, the method will return SUCCESS

    Returns:
        ('SUCCESS', 'OK') if the expected campaign outcome has been reached
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter waitForCampaignReady')
    startTimeCamp = int(time.time())
    endTime = startTimeCamp + timeout

    campaignStatus = ''
    while time.time() < endTime:
        ssh_lib.tearDownHandles()
        if rollingUpgrade == True:
            numberOfRetries = 3
            for i in range(numberOfRetries):
                 result = saf_lib.upgradeStatusCheck(campaignName)
                 if result[0] == 'SUCCESS':
                     break
                 elif i != numberOfRetries:
                     misc_lib.waitTime(15)
        else:
            result = saf_lib.upgradeStatusCheck(campaignName)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave waitForCampaignReady')
            return result
        cmdResult = result[1].splitlines()
        if len(cmdResult) != 1:
            logger.debug('leave waitForCampaignReady')
            return ('ERROR', 'waitForCampaignReady: Expected a response to the campaign status check that is exactly one line. Received: %s' %result[1])
        cmdResult = cmdResult[0].split('=')
        if len(cmdResult) != 2:
            logger.debug('leave waitForCampaignReady')
            return ('ERROR', 'waitForCampaignReady: Expected a response to the campaign status that has only one "=" sign in it. Received: %s' %cmdResult)
        elif cmdResult[0] != campaignName:
            logger.debug('leave waitForCampaignReady')
            return ('ERROR', 'waitForCampaignReady: Expected the campaign name to be on the left side of the "=" sign. Received: %s' %cmdResult[0])
        campaignStatus = cmdResult[1]
        if campaignStatus == 'COMPLETED':
            break
        elif '=FAILED' in result[1]:
            logger.info('The campaign failed. Exact status is: %s' %result[1])
            break
        elif 'error=' in result[1]:
            logger.info('The campaign contains an error. Exact status is: %s' %result[1])
            break
        else:
            misc_lib.waitTime(waitBetweenIterations)

    if campExpectedToFail == False:
        if campaignStatus == 'COMPLETED':
            ret = ('SUCCESS', 'OK')
        else:
            ret = ('ERROR', 'waitForCampaignReady: Campaign %s did not complete in allocated time or failed. Exact status is: %s' %(campaignName, result[1]))
    elif campExpectedToFail == True:
        if 'FAILED' in result[1]:
            ret = ('SUCCESS', 'OK')
        else:
            ret = ('ERROR', 'waitForCampaignReady: Campaign %s expected to fail but did not fail. Exact status is: %s' %(campaignName, result[1]))

    logger.debug('leave waitForCampaignReady')
    return ret

def buildAndStoreCOMSA(self):
    """
    The method builds COM-SA and includes bundle and template archive
    COM SA builds in the first times, and will be stored base on option swDirNumber.
    if option swDirNumber is defined, COM SA will store in /home/jenkinuser/release/install/<your_folder>/comsa/
    else it will be store in /tmp/xtemp_$USER-<time_sample>/comsa/
    After this function, there are 2 variable:
      +IsBuildCOMSA: Default is False, if COM SA already build, it will be True.
      +BuildComsaPath: The directory of COM SA will be store.
    Returns:
        ('SUCCESS', comsaRtSdp, comsaInstSdp, comsaRemoveSdp, comsaTempTar, comsaRunTimeTar, comsaRtSdpFullPath, comsaInstSdpFullPath, comsaRemoveSdpFullPath, comsaTempTarFullPath, comsaRunTimeTarFullPath)
        ('ERROR', 'some relevant error message')
    """

    comsaRtSdp = ''
    comsaInstSdp = ''
    comsaRemoveSdp = ''
    comsaTempTar = ''
    comsaRunTimeTar = ''

    comsaRtSdpFullPath = ''
    comsaInstSdpFullPath = ''
    comsaRemoveSdpFullPath = ''
    comsaTempTarFullPath = ''
    comsaRunTimeTarFullPath = ''

    logger.debug('enter buildAndStoreCOMSA')
    IsBuildCOMSA = System.getProperty("IsBuildCOMSA")
    buildComsa = System.getProperty("buildComSa")
    swDir = System.getProperty("swDirNumber")
    if IsBuildCOMSA == "True" or ( swDir != 'undef' and buildComsa == "False"):
        if IsBuildCOMSA == "True":
            logger.info('buildAndStoreCOMSA: COM SA aleady build in first times')
            srcDir = System.getProperty("BuildComsaPath")
        elif (buildComsa == "False" and swDir != 'undef'):
            logger.info('buildAndStoreCOMSA: Skip building COM SA, package is available.')
            dict = self.comsa_lib.getGlobalConfig(self)
            installRoot = dict.get('JENKINUSER_R_INSTALL')
            srcDir = '%s%s' %(installRoot, swDir)
            result = findFilesMatchingPattern('%s/comsa/*.sdp %s/comsa/*tar*' %(srcDir, srcDir))
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave buildAndStoreCOMSA')
                return result
            logger.debug('buildAndStoreCOMSA: Set value for IsBuildCOMSA is True and BuildComsaPath')
            System.setProperty("IsBuildCOMSA", "True")
            System.setProperty("BuildComsaPath", '%s' %srcDir)
        result = checkIfSwInPlace('%s/' %srcDir, ['COMSA'], self.distroTypes, self.linuxDistro)
        if result[0] != 'SUCCESS':
            System.setProperty("IsBuildCOMSA", "False")
            logger.error(result[1])
            logger.debug('leave buildAndStoreCOMSA')
            return ('ERROR','buildAndStoreCOMSA: checkIfSwInPlace failed')
    else:
        #Build COMSA
        logger.info('buildAndStoreCOMSA: Build COM SA')
        dict = self.comsa_lib.getGlobalConfig(self)
        absDir = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get("ABS"))
        cxpArchive = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get("CXP_ARCHIVE"))
        installRoot = dict.get('JENKINUSER_R_INSTALL')
        if self.linuxDistro == self.distroTypes[1]: # rhel
            deplTemplArchive = "COM_SA_D_TEMPLATE-CXP9028075_1.tar.gz"
            bundleArchive = "COM_SA_RUNTIME-CXP9028074_1.tar"
            cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            buildRelease = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get('RELEASE_RHEL'))
        else:
            deplTemplArchive = "COM_SA_D_TEMPLATE-CXP9017695_*.tar.gz"
            bundleArchive = "COM_SA_RUNTIME-CXP9018914_*.tar"
            cxpSdpName = dict.get('CXP_SDP_NAME')
            buildRelease = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get('RELEASE'))
        installSdpName = dict.get('INSTALL_SDP_NAME')
        installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        removeSdpName = dict.get('REMOVE_SDP_NAME')
        removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        buildTokenDir= dict.get('BUILD_TOKENS')
        sdpNames = [cxpSdpName, installSdpName, installSdpNameSingle, removeSdpName, removeSdpNameSingle]
        if ( swDir == 'undef'):
            srcDir = System.getProperty("BuildComsaPath")
            logger.debug('buildAndStoreCOMSA: Create new folder to store COM SA package')
            result = misc_lib.execCommand('mkdir -p %s/comsa' %srcDir)
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave buildAndStoreCOMSA')
                return result
        else:
            srcDir = '%s%s' %(installRoot, swDir)
            result = findFilesMatchingPattern('%s/comsa' %srcDir)
            if result[0] != 'SUCCESS':
                result = misc_lib.execCommand('mkdir -p %s/comsa' %srcDir)
                if result[0] != 'SUCCESS':
                    logger.error(result[1])
                    logger.debug('leave buildAndStoreCOMSA')
                    return result
            # Build COM SA
        for i in range(numberOfGetTokenRetries):
            result = getBuildToken(suiteLogDir, buildTokenDir, tokenPattern)
            if result[0] == 'SUCCESS':
                break
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave buildAndStoreCOMSA')
            return result

        result = misc_lib.execCommand('%scomsabuild clean; %scomsabuild all' %(absDir, absDir))
        if result[0] != 'SUCCESS':
            logger.debug('leave buildAndStoreCOMSA')
            return ('ERROR', 'Build has compiler ERROR %s' %result[0] )

        # Release the build token
        result = releaseToken(suiteLogDir, buildTokenDir, tokenPattern)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave buildAndStoreCOMSA')
            return result
        # Find tar file after build
        result = misc_lib.execCommand('\\rm -rf %s/comsa/*CXP*' %srcDir)
        if result[0] != 'SUCCESS':
            logger.debug('leave buildAndStoreCOMSA')
            return result
        result = findFilesMatchingPattern('%s/%s' %(cxpArchive,bundleArchive))
        if result[0] != 'SUCCESS':
            logger.debug('leave buildAndStoreCOMSA')
            return result
        if len(result[1]) > 1:
            logger.debug('leave buildAndStoreCOMSA')
            return ('ERROR', 'buildAndStoreCOMSA: More than one Bundle Archive tar file found at specified location: %s: %s.' %(cxpArchive, str(result[1])))
        else:
            result = misc_lib.execCommand('\cp -f %s/%s %s/comsa' %(cxpArchive, bundleArchive, srcDir))
            if result[0] != 'SUCCESS':
                logger.debug('leave buildAndStoreCOMSA')
                return result
        result = findFilesMatchingPattern('%s/%s' %(cxpArchive,deplTemplArchive))
        if result[0] != 'SUCCESS':
            logger.debug('leave buildAndStoreCOMSA')
            return result
        if len(result[1]) > 1:
            logger.debug('leave buildAndStoreCOMSA')
            return ('ERROR', 'buildAndStoreCOMSA: More than one Deploy Template Archive tar file found at specified location: %s: %s.' %(cxpArchive, str(result[1])))
        else:
            result = misc_lib.execCommand('\cp -f %s/%s %s/comsa' %(cxpArchive, deplTemplArchive, srcDir))
            if result[0] != 'SUCCESS':
                logger.debug('leave buildAndStoreCOMSA')
                return result
        # Copy sdp to srcDir
        result = copyComSaSdpsToSwDir(buildRelease, '%s/' %srcDir, len(self.testConfig['controllers']), sdpNames, self.linuxDistro)
        if result[0] != 'SUCCESS':
            logger.debug('leave buildAndStoreCOMSA')
            return result
        result = checkIfSwInPlace('%s/' %srcDir, ['COMSA'], self.distroTypes, self.linuxDistro)
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave buildAndStoreCOMSA')
            return ('ERROR','buildAndStoreCOMSA: checkIfSwInPlace failed')
        logger.debug('buildAndStoreCOMSA: Set value for IsBuildCOMSA is True and BuildComsaPath')
        System.setProperty("IsBuildCOMSA", "True")
        System.setProperty("BuildComsaPath", '%s' %srcDir)
    comsaRtSdp = result[4]
    comsaInstSdp = result[5]
    comsaRemoveSdp = result[6]
    comsaTempTar = result[7]
    comsaRunTimeTar = result[8]

    comsaRtSdpFullPath = result[12]
    comsaInstSdpFullPath = result[13]
    comsaRemoveSdpFullPath = result[14]
    comsaTempTarFullPath = result[15]
    comsaRunTimeTarFullPath = result[16]
    files = ['SUCCESS', comsaRtSdp, comsaInstSdp, comsaRemoveSdp, comsaTempTar, comsaRunTimeTar, comsaRtSdpFullPath, comsaInstSdpFullPath, comsaRemoveSdpFullPath, comsaTempTarFullPath, comsaRunTimeTarFullPath]
    logger.debug('leave buildAndStoreCOMSA')
    return files

def buildCOMSA(buildSrc, buildRelease, noOfSCs, sdpNames, makeOption = ''):
    """
    The method builds COM-SA
    buildSrc: string: path to where COM-SA can be built.
    buildRelease: string: path to where the COM-SA binaries are put
    noOfSCs: number of system controllers in the test cluster
    sdpNames: list of strings: contains the expected files names to be produced by the build operation

    Returns:
        ('SUCCESS', 'buildCOMSA: COM SA built successfully')
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter buildCOMSA')

    # Build COM SA
    misc_lib.execCommand("bash -c 'pushd %s ; make clean ; make %s ; popd '" %(buildSrc, makeOption))

    # Check the result of the build
    # Check CXP sdp neither 3.x nor 4.0
    result = misc_lib.execCommand("ls %s/%s" %(buildRelease,sdpNames[0]))
    if 'No such file or directory' in result[1]:
        return ('ERROR', 'buildCOMSA: The CXP SDP file %s was not found in the release directory %s' %(sdpNames[0], buildRelease))
    result = misc_lib.execCommand('ls -l %s' %buildRelease)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave buildCOMSA')
        return result
    #Check install sdp
    if noOfSCs == 2:
        if sdpNames[1] not in result[1]: #The install sdp
            logger.debug('leave buildCOMSA')
            return ('ERROR', 'buildCOMSA: The installation SDP file %s was not found in the release directory %s' %(sdpNames[1], buildRelease))
    elif noOfSCs == 1:
        if sdpNames[2] not in result[1]: #The install_single sdp
            logger.debug('leave buildCOMSA')
            return ('ERROR', 'buildCOMSA: The installation SDP file %s was not found in the release directory %s' %(sdpNames[2], buildRelease))
    else:
        logger.debug('leave buildCOMSA')
        return ('ERROR', 'buildCOMSA: Number of system controllers should be either 1 or 2. Value is %d which is not handled currently' %sdpNames)

    logger.debug('COM SA built successfully')
    logger.debug('leave buildCOMSA')
    return ('SUCCESS', 'buildCOMSA: COM SA built successfully')

def buildCOMSAScript(buildSrc, buildRelease, noOfSCs, sdpNames, linuxDistro):
    """
    The method builds COM-SA using comsabuild script
    buildSrc: string: path to where COM-SA can be built.
    buildRelease: string: path to where the COM-SA binaries are put
    noOfSCs: number of system controllers in the test cluster
    sdpNames: list of strings: contains the expected files names to be produced by the build operation

    Returns:
        ('SUCCESS', 'buildCOMSAScript: COM SA built successfully')
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter buildCOMSAScript')

    # Build COM SA
    misc_lib.execCommand("bash -c 'pushd %s ; ./comsabuild clean ; ./comsabuild all ; popd '" %buildSrc)

    # Check the result of the build
    if linuxDistro == 'RhelType':
        cxpArchivePath = '%s../cxp_archive' %buildRelease
        deplTemplArchive = "COM_SA_D_TEMPLATE-CXP9028075_1.tar.gz"
        bundleArchive = "COM_SA_RUNTIME-CXP9028074_1.tar"
    else:
        cxpArchivePath = '%scxp_archive' %buildRelease
        deplTemplArchive = "COM_SA_D_TEMPLATE-CXP9017695_*.tar.gz"
        bundleArchive = "COM_SA_RUNTIME-CXP9018914_*.tar"
    result = misc_lib.execCommand('ls -l %s/%s' %(buildRelease, sdpNames[0]))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave buildCOMSAScript')
        return result
    if 'No such file or directory' in result[1]: #The CXP sdp
        logger.debug('leave buildCOMSAScript')
        return ('ERROR', 'buildCOMSAScript: The CXP SDP file was not found in the release directory %s' %(buildRelease))
    result = misc_lib.execCommand('ls -l %s' %buildRelease)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave buildCOMSAScript')
        return result
    if noOfSCs == 2:
        if sdpNames[1] not in result[1]: #The install sdp
            logger.debug('leave buildCOMSAScript')
            return ('ERROR', 'buildCOMSAScript: The installation SDP file %s was not found in the release directory %s' %(sdpNames[1], buildRelease))
    elif noOfSCs == 1:
        if sdpNames[2] not in result[1]: #The install_single sdp
            logger.debug('leave buildCOMSAScript')
            return ('ERROR', 'buildCOMSAScript: The installation SDP file %s was not found in the release directory %s' %(sdpNames[2], buildRelease))
    else:
        logger.debug('leave buildCOMSAScript')
        return ('ERROR', 'buildCOMSAScript: Number of system controllers should be either 1 or 2. Value is %d which is not handled currently' %sdpNames)

    result = misc_lib.execCommand('ls -l %s/%s' % (cxpArchivePath, deplTemplArchive))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave buildCOMSAScript')
        return result
    if 'No such file or directory' in result[1]:
        logger.debug('leave buildCOMSAScript')
        return ('ERROR', 'buildCOMSAScript: The template file was not found in the release directory %s' %(cxpArchivePath))

    result = misc_lib.execCommand('ls -l %s/%s' % (cxpArchivePath, bundleArchive))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave buildCOMSAScript')
        return result
    if 'No such file or directory' in result[1]:
        logger.debug('leave buildCOMSAScript')
        return ('ERROR', 'buildCOMSAScript: The runtime file was not found in the release directory %s' %(cxpArchivePath))

    logger.debug('COM SA built successfully')
    logger.debug('leave buildCOMSAScript')
    return ('SUCCESS', 'buildCOMSAScript: COM SA built successfully')

def checkCOMSACompileWarnings(buildSrc, buildTokenDir, makeOption = ''):
    """
    The method builds COM-SA
    buildSrc: string: path to where COM-SA can be built.
    buildRelease: string: path to where the COM-SA binaries are put
    noOfSCs: number of system controllers in the test cluster
    sdpNames: list of strings: contains the expected files names to be produced by the build operation

    Returns:
        ('SUCCESS', 'buildCOMSA: COM SA built successfully')
        ('ERROR', 'some relevant error message')
    """

    logger.debug('enter checkCOMSACompileWarnings')

    # Get a build token
    for i in range(numberOfGetTokenRetries):
        result = getBuildToken(suiteLogDir, buildTokenDir, tokenPattern)
        if result[0] == 'SUCCESS':
            break
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave checkCOMSACompileWarnings')
        return result

    # Build COM SA
    result = misc_lib.execCommand("bash -c 'pushd %s ; make clean ; make %s; popd '" %(buildSrc,makeOption))

    logger.debug('checking for compiler warnings')
    #Check for compiler warnings.

    lines = result[1].splitlines()
    if len(lines) > 1:
        for i in range(len(lines)):
             if 'warning' in lines[i]:
                 releaseToken(suiteLogDir, buildTokenDir, tokenPattern)
                 logger.debug('leave checkCOMSACompileWarnings')
                 return ('ERROR', 'make has compiler warning %s' %lines[i] )

    # Release the build token
    result = releaseToken(suiteLogDir, buildTokenDir, tokenPattern)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave checkCOMSACompileWarnings')
        return result

    logger.debug('leave checkCOMSACompileWarnings')
    return ('SUCCESS', 'checkCOMSACompileWarnings: COM SA compiles with no warnings')

def copyComSaSdpsToSwDir(buildRelease, swDir, noOfSCs, sdpNames, linuxDistro = ''):
    """
    The method is used to copy the files produced after the build of COM-SA from the release directory to the swDir/comsa directory
        which is used by the installation methods
    buildRelease: string: path to the files created during the build of COM-SA
    swDir: string: path to the directory used to store the component binaries for the installation
    noOfSCs: number of system controllers in the test cluster
    sdpNames: list of strings: contains the files names produced by the build operation

    Returns:
        ('SUCCESS', 'copyComSaSdpsToSwDir: Files copied successfully')
        ('ERROR', 'some relevant error message')
    """
    logger.debug('enter copyComSaSdpsToSwDir')
    result = misc_lib.execCommand('\\rm -f %s/comsa/*.sdp' %swDir)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave copyComSaSdpsToSwDir')
        return result
    result = misc_lib.execCommand('\cp %s/%s %s/comsa/' %(buildRelease, sdpNames[0], swDir))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave copyComSaSdpsToSwDir')
        return result
    if noOfSCs == 2:
        result = misc_lib.execCommand('\cp %s/%s %s/comsa/' %(buildRelease, sdpNames[1], swDir))
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave copyComSaSdpsToSwDir')
            return result
        if len(sdpNames) > 2:
            result = misc_lib.execCommand('\cp %s/%s %s/comsa/' %(buildRelease, sdpNames[3], swDir))
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave copyComSaSdpsToSwDir')
                return result
    elif noOfSCs == 1:
        result = misc_lib.execCommand('\cp %s/%s %s/comsa/' %(buildRelease, sdpNames[2], swDir))
        if result[0] != 'SUCCESS':
            logger.error(result[1])
            logger.debug('leave copyComSaSdpsToSwDir')
            return result
        if len(sdpNames) > 3:
            result = misc_lib.execCommand('\cp %s/%s %s/comsa/' %(buildRelease, sdpNames[4], swDir))
            if result[0] != 'SUCCESS':
                logger.error(result[1])
                logger.debug('leave copyComSaSdpsToSwDir')
                return result
    else:
        logger.debug('leave copyComSaSdpsToSwDir')
        return ('ERROR', 'copyComSaSdpsToSwDir: Number of system controllers should be either 1 or 2. Value is %d which is not handled currently' %sdpNames)

    logger.debug('Files copied successfully')
    logger.debug('leave copyComSaSdpsToSwDir')
    return ('SUCCESS', 'copyComSaSdpsToSwDir: Files copied successfully')

def copyComSaCxpArchiveToSwDir(buildRelease, swDir, linuxDistro = ''):
    """
    The method is used to copy the files produced after the build of COM-SA from the release directory to the swDir/comsa directory
        which is used by the installation methods
    buildRelease: string: path to the files created during the build of COM-SA
    swDir: string: path to the directory used to store the component binaries for the installation

    Returns:
        ('SUCCESS', 'copyComSaCxpArchiveToSwDir: Files copied successfully')
        ('ERROR', 'some relevant error message')
    """
    if linuxDistro == 'RhelType':
        deplTemplArchive = "COM_SA_D_TEMPLATE-CXP9028075_1.tar.gz"
        bundleArchive = "COM_SA_RUNTIME-CXP9028074_1.tar"
        cxpArchivePath = '%s../cxp_archive' %buildRelease
    else:
        deplTemplArchive = "COM_SA_D_TEMPLATE-CXP9017695_*.tar.gz"
        bundleArchive = "COM_SA_RUNTIME-CXP9018914_*.tar"
        cxpArchivePath = '%scxp_archive' %buildRelease
    logger.debug('enter copyComSaCxpArchiveToSwDir')
    result = misc_lib.execCommand('\\rm -f %s/comsa/*.tar*' %swDir)
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave copyComSaCxpArchiveToSwDir')
        return result
    result = misc_lib.execCommand('\cp %s/%s %s/comsa/' %(cxpArchivePath, deplTemplArchive, swDir))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave copyComSaCxpArchiveToSwDir')
        return result
    result = misc_lib.execCommand('\cp %s/%s %s/comsa/' %(cxpArchivePath, bundleArchive, swDir))
    if result[0] != 'SUCCESS':
        logger.error(result[1])
        logger.debug('leave copyComSaCxpArchiveToSwDir')
        return result

    logger.debug('Files copied successfully')
    logger.debug('leave copyComSaCxpArchiveToSwDir')
    return ('SUCCESS', 'copyComSaCxpArchiveToSwDir: Files copied successfully')

def getBuildToken(testSuiteName, buildDir, tokenPattern, tokenTimeout = 300, waitTime = 360):
    """
    This method grants exclusivity over the build system for the test suite that it is called from.
    The method should be called from a loop, because there is a possibility that two tokens are created
    almost at the same time. This is detected by the method (returns error), but the retry mechanism is not part of it.
    """
    logger.debug('enter getBuildToken')

    result = getTokenList(buildDir, tokenPattern)
    if result[0] != 'SUCCESS':
        logger.debug('leave getBuildToken')
        return result
    if len(result[1]) != 0:
        result = waitForEmptyTokenList(buildDir, result[1], result[2], tokenTimeout, waitTime, tokenPattern)
        if result[0] != 'SUCCESS':
            logger.debug('leave getBuildToken')
            return result

    # Create build token
    cmd = 'touch "%s/%s%s"' %(buildDir, tokenPattern, testSuiteName)
    result = misc_lib.execCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getBuildToken')
        return result

    """ Wait a few seconds and see that there is only one token
    to exclude the case of parallel creation of tokens in different suites almost at the same time. """
    waitTime = randint(1,5)
    misc_lib.waitTime(waitTime)
    result = getTokenList(buildDir, tokenPattern)
    if result[0] != 'SUCCESS':
        logger.debug('leave getBuildToken')
        return result
    if len(result[1]) != 1:
        # We remove the token created above to allow a retry mechanism
        releaseToken(testSuiteName, buildDir, tokenPattern)
        logger.error('Another token has been created almost at the same time as the token in the current suite. Try again!')
        logger.debug('leave getBuildToken')
        return ('ERROR', 'Another token has been created almost at the same time as the token in the current suite. Try again!')
    else:
        logger.debug('leave getBuildToken')
        return ('SUCCESS', 'Token created')


def waitForEmptyTokenList(buildDir, tokenAgeList, tokenFileNames, tokenTimeout, waitTime, tokenPattern):

    logger.debug('enter waitForEmptyTokenList')

    tokenListEmpty = False

    result = getCurrentLocalUnixTime()
    if result[0] != 'SUCCESS':
        logger.debug('leave getBuildToken')
        return result
    currentUnixTime = result[1]

    timeNow = int(time.time())
    endTime = timeNow + waitTime

    while int(time.time()) < endTime:
        tokenDict = {}
        for file in tokenFileNames:
            tokenDict[file] = tokenAgeList[tokenFileNames.index(file)]
        for file in tokenDict.keys():
            if (currentUnixTime - tokenDict[file]) > tokenTimeout:
                result = deleteUnusedToken(buildDir, file)
                if result[0] != 'SUCCESS':
                    logger.debug('leave waitForEmptyTokenList')
                    return result
                tokenDict.__delitem__(file)
        if len(tokenDict) == 0:
            tokenListEmpty = True
            break
        misc_lib.waitTime(5)
        result = getTokenList(buildDir, tokenPattern)
        if result[0] != 'SUCCESS':
            logger.debug('leave waitForEmptyTokenList')
            return result
        if len(result[1]) == 0:
            tokenListEmpty = True
            break
        tokenAgeList = result[1]
        tokenFileNames = result[2]
        timeNow = int(time.time())

    if tokenListEmpty == True:
        ret = ('SUCCESS', 'No build token in the build directory')
    else:
        ret = ('ERROR', 'There are build token(s) in the build directory after the expiration of the timeout.')

    logger.debug('leave waitForEmptyTokenList')
    return ret

def releaseToken(testSuiteName, buildDir, tokenPattern):
    """
    This method releases the build token got before building
    """
    logger.debug('enter releaseToken')
    cmd = '\\rm "%s/%s%s"' %(buildDir, tokenPattern, testSuiteName)
    result = misc_lib.execCommand(cmd)
    logger.debug('leave releaseToken')
    return result

def deleteUnusedToken(buildDir, fileName):
    """
    This method deletes a build token (specified by exact file name)
    """
    logger.debug('enter deleteUnusedToken')
    cmd = '\\rm "%s/%s"' %(buildDir, fileName)
    result = misc_lib.execCommand(cmd)
    logger.debug('leave deleteUnusedToken')
    return result


def getTokenList(buildDir, tokenPattern):
    logger.debug('enter getTokenList')
    ageList = []
    fileList = []
    cmd = """ls -l --time-style=+%%s %s | grep %s | awk '{print $6" "$7}'""" %(buildDir, tokenPattern)
    result = misc_lib.execCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getTokenList')
        return result
    if result[1] != '':
        for line in result[1].splitlines():
            if 'int' not in str(type(eval(line.split(" ")[0]))):
                logger.debug('leave getTokenList')
                return ('ERROR', 'Expected a response of type int. Received: %s' %str(type(eval(result[1]))))
            ageList.append(int(line.split(" ")[0]))
            fileList.append(line.split(" ")[1])
    logger.debug('leave getTokenList')
    return ('SUCCESS', ageList, fileList)


def getCurrentLocalUnixTime():
    logger.debug('enter getCurrentLocalUnixTime')
    cmd = 'date +%s'
    result = misc_lib.execCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getCurrentLocalUnixTime')
        return result
    if 'int' not in str(type(eval(result[1]))):
        logger.debug('leave getCurrentLocalUnixTime')
        return ('ERROR', 'Expected a response of type int. Received: %s' %str(type(eval(result[1]))))
    logger.debug('leave getCurrentLocalUnixTime')
    return ('SUCCESS', int(result[1]))

def getCurrentUnixTimeOnTarget():
    logger.debug('enter getCurrentUnixTimeOnTarget')
    cmd = 'date +%s'
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave getCurrentUnixTimeOnTarget')
        return result
    if 'int' not in str(type(eval(result[1]))):
        logger.debug('leave getCurrentUnixTimeOnTarget')
        return ('ERROR', 'Expected a response of type int. Received: %s' %str(type(eval(result[1]))))
    logger.debug('leave getCurrentUnixTimeOnTarget')
    return ('SUCCESS', int(result[1]))

def restartCluster(testConfig, linuxDistro, distroTypes, waitTimeAfterReboot = 150):
    """
    The method performs the following steps:
        - restarts the cluster
        - makes sure that all system controller blades restart
        - waits for the cluster to become operational

    Returns:
        ('SUCCESS', 'Cluster restarted, up and running again.') OR
        ('ERROR', 'Some relevant error message.')
    """
    result = calculateLatestSystemStartup(testConfig, linuxDistro, distroTypes)
    if result[0] != 'SUCCESS':
        logger.debug('leave restartCluster')
        return result
    currentStartUpTimes = result[1]

    result = saf_lib.clusterReboot()
    if result[0] != 'SUCCESS':
        logger.debug('leave restartCluster')
        return result

    misc_lib.waitTime(waitTimeAfterReboot)

    result = waitForMoreRecentStartUpTime(currentStartUpTimes, testConfig, linuxDistro, distroTypes)
    if result[0] != 'SUCCESS':
        logger.debug('leave restartCluster')
        return result

    result = waitForClusterStatusOk()
    if result[0] != 'SUCCESS':
        logger.debug('leave restartCluster')
        return result

    logger.debug('leave restartCluster')
    return ('SUCCESS', 'Cluster restarted, up and running again.')

def restoreSystem(self, backupName, testConfig, testSuiteConfig, distroTypes, desiredInstallationLevel = 3, \
                  pathToInstallationFiles = '/home/release/autoinstall/', localPathToSw = '/home/jenkinuser/release/install/', supportedComponents = ['cmw', 'com', 'comsa'], removeBackup = True, noBackupArea = '/storage/no-backup/'):
    """
    This method performs the complete procedure of
        - checking if backup to restore exists
        - performs the restore of the backup
        - restarts the cluster
        - waits for the cluster to come up in operational state
        - optionally removes the backup

    Returns:
        ('SUCCESS', 'System restored') OR
        ('ERROR', 'Some relevant error message.')
    """
    logger.debug('enter restoreSystem')
    logger.info('Trying to restore %s' %backupName)

    global swDirGlobal

    result = saf_lib.isBackup(backupName)
    if self.linuxDistro != distroTypes[1] and result != ('SUCCESS','EXIST'):
        logger.debug('leave restoreSystem')
        return ('ERROR', 'Not possible to restore backup %s. isBackup method returned: %s' %(backupName, str(result)))
    # If Rhel distribution and the backup does not exist we need to re-install the component(s) instead of restoring the partial backup
    elif self.linuxDistro == distroTypes[1] and result != ('SUCCESS','EXIST'):
        logger.info('Partial backup %s not found on RHEL system. Trying to re-install the standard version of the components.' %backupName)
        if desiredInstallationLevel > 3:
            return ('ERROR', 'The work-around for re-installing COM and/or COM SA instead of restoring to a backup\
             that is no longer available does not support installation of components on top of COM SA.')
        result = lib.getInstallationLevel()
        if result[0] != 'SUCCESS':
            logger.debug('leave restoreSystem')
            return result
        currentInstallationLevel = result[1]

        help = """
        Installation level 1 means only CMW is installed
        Installation level 2 means CMW and COM are installed
        Installation level 3 means CMW, COM and COM SA are installed

        Possible scenarios:
        Current    Desired       Action
        level 3    level 3       restore level 2, install level 3
        level 3    level 2       restore level 1, install level 2
        level 3    level 1       do a cluster snapshot restore, then install Core MW

        level 2    level 3       install level 3
        level 2    level 2       restore level 1, install level 2
        level 2    level 1       do a cluster snapshot restore, then install Core MW

        level 1    level 3       install level 2, install level 3
        level 1    level 2       install level 2
        level 1    level 1       do a cluster snapshot restore, then install Core MW
        """

        if desiredInstallationLevel == 1:
            # No working backup of coremw remaining and on RHEL system, so do a complete re-installation after a clean snapshot restore
            dict = self.comsa_lib.getGlobalConfig(self)

            #Prepare arguments for reInstallComponents
            buildComsa = System.getProperty("buildComSa")
            buildSrc = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get('ABS'))
            buildRelease = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get("RELEASE_RHEL"))

            cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            installSdpName = dict.get('INSTALL_SDP_NAME')
            installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
            removeSdpName = dict.get('REMOVE_SDP_NAME')
            removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
            sdpNames = [cxpSdpName, installSdpName, installSdpNameSingle, removeSdpName, removeSdpNameSingle]
            localPathToSw = '%s%s/' %(localPathToSw, System.getProperty("swDirNumber"))
            uninstallScriptPath =  '%s%s' %(os.environ['COMSA_VERIFICATION'], dict.get("TEST"))
            uninstallScriptName = dict.get('UNINSTALL_SCRIPT_NAME_RHEL')
            buildTokenDir = dict.get('BUILD_TOKENS')
            sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(os.environ['MY_REPOSITORY'], dict.get("PATH_TO_CONFIG_FILES"))
            tmpDirOnTarget = dict.get('AUTOINSTALL_DIR_TARGET')
            ClusterReset = System.getProperty("resetCluster")

            result = reInstallComponents(self, buildComsa, buildSrc, buildRelease, sdpNames, localPathToSw, uninstallScriptPath, uninstallScriptName, testConfig, \
                                                            testSuiteConfig, buildTokenDir, sshKeyUpdater, components_to_install = ["CMW"], \
                                                            destinationOnTarget = tmpDirOnTarget, resetCluster = ClusterReset, useComsaBuild = True)
            noOfScs = len(testConfig['controllers'])
            if result[0] != 'SUCCESS':
                self.myLogger.error(result[1])
                # send email
                emailReport(self, True).send("INSTALLATION FAILED", noOfScs)
                """
                We stop test execution here if the re-installation has failed.
                It makes no sense to continue testing on a system that is not properly installed.
                """
                os._exit(1)
            else:
                #self.setAdditionalResultInfo('COM SA installation time was: %d seconds.' %result[1])
                #addDataToTestSuiteConfig(testSuiteConfig, 'charMeasurements', 'COM SA installation time', result[1])
                testSuiteConfig['sdpFilesOnTarget'] = True

        elif currentInstallationLevel >= desiredInstallationLevel:
            result = restoreSystem(self, '%s_autobackup' %supportedComponents[desiredInstallationLevel - 2], testConfig, testSuiteConfig, distroTypes, \
                                   desiredInstallationLevel = desiredInstallationLevel - 1 , \
                                   pathToInstallationFiles = pathToInstallationFiles, removeBackup = False, noBackupArea = noBackupArea)
            if result[0] != 'SUCCESS':
                logger.debug('leave restoreSystem')
                return result

            result = prepareInstallationFiles(desiredInstallationLevel, supportedComponents, pathToInstallationFiles, testSuiteConfig, localPathToSw, distroTypes, self.linuxDistro)
            if result[0] != 'SUCCESS':
                logger.debug('leave restoreSystem')
                return result
            appRtSdp = result[1]
            appInstSdp = result[2]

            result = installComp(pathToInstallationFiles, appRtSdp, appInstSdp, compName=supportedComponents[desiredInstallationLevel-1], createBackup=True, acceptFailedBackup=True, backupRpms = self.backupRpmScript)
            if result[0] != 'SUCCESS':
                logger.debug('leave restoreSystem')
                return result
        # Example: we are on a system with COM and wanted to restore a COM SA backup, we simply install COM SA
        else:
            for i in range(desiredInstallationLevel - currentInstallationLevel):
                result = prepareInstallationFiles(currentInstallationLevel + i + 1, supportedComponents, pathToInstallationFiles, testSuiteConfig, localPathToSw, distroTypes, self.linuxDistro)
                if result[0] != 'SUCCESS':
                    logger.debug('leave restoreSystem')
                    return result
                appRtSdp = result[1]
                appInstSdp = result[2]

                result = installComp(pathToInstallationFiles, appRtSdp, appInstSdp, compName=supportedComponents[desiredInstallationLevel-1], createBackup=True, acceptFailedBackup=True, backupRpms = self.backupRpmScript)
                if result[0] != 'SUCCESS':
                    logger.debug('leave restoreSystem')
                    return result
        if desiredInstallationLevel == 3:
            # We need to set saAmfSGSuRestartMax to a high level in order to not have a failover of the COM process after 3 COM restarts
            # It is a pragmatic way to hardcode the value to 1000 instead of
            # further extending the interface of the restoreSytem method and get it passed as an argument
            # This hardcoding could be revisited in case it generates undesired behavior
            result = setComSaSuRestartMax(False, value = 1000)
            if result[0] != 'SUCCESS':
                logger.debug('leave restoreSystem')
                return result
        if removeBackup == False:
            result = backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
            if result[0] != 'SUCCESS':
                logger.error('Could not create backup on RHEL system after installing component. %s. \
                This is not a critical failure, the test should not be failed due to this.' %result[1])
                #return result
            else:
                # We need to overwrite the safe backup created at the beginning of the test suite with the one that we have just created
                # because the old backup is no longer accessible.
                if testSuiteConfig.has_key('restoreBackup') and backupName != testSuiteConfig['restoreBackup'] and desiredInstallationLevel == 3:
                    testSuiteConfig['restoreBackup'] = backupName
        logger.debug('leave restoreSystem')
        return ('SUCCESS', 'System restored')

    # Backup exists
    else:
        result = backupRestoreWrapper(backupName, backupRpms = self.backupRpmScript)
        if result[0] != 'SUCCESS':
            logger.debug('leave restoreSystem')
            return result
        if 'Failed to restore' in result[1]:
            if self.linuxDistro == distroTypes[1]:
                # If restore of the backup failed on a RHEL system we need to remove the
                # faulty backup so that the next test case does not try to restore the same faulty backup
                if testSuiteConfig.has_key('restoreBackup') and backupName == testSuiteConfig['restoreBackup']:
                    testSuiteConfig.__delitem__('restoreBackup')
                result = saf_lib.backupRemove(backupName)
                if result[0] != 'SUCCESS':
                    logger.debug('leave restoreSystem')
                    return result
                # Then we try to restore the system again: in this recursive call the other branch of restoreSystem will be executed
                # where backupName does not exist and the system will try to re-install the component instead.
                result = restoreSystem(self, backupName, testConfig, testSuiteConfig, distroTypes, desiredInstallationLevel, pathToInstallationFiles, \
                   localPathToSw, supportedComponents, removeBackup, noBackupArea)
                logger.debug('leave restoreSystem')
                # We exit here independently of the result because we do not want to continue the procedure
                # with restartCluster, remove/create backup etc which were already executed in the call
                # to restoreSystem() above
                return result
            else:
                logger.debug('leave restoreSystem')
                return ('ERROR', 'Failed to restore Host OS from backup %s' %backupName)

        result = restartCluster(testConfig, self.linuxDistro, distroTypes)
        if result[0] != 'SUCCESS':
            logger.debug('leave restoreSystem')
            return result

        # If we run on a RedHat system the backup that we restore will be lost.
        # Therefore we create a new backup with the same name.
        if self.linuxDistro == distroTypes[1]:
            # Check for the consistency of the backup system. This is needed because backup restores can lead to inconsistend data
            result = utils.checkBackupAreaConsistency(noBackupArea = noBackupArea)
            if result[0] != 'SUCCESS':
                logger.debug('leave restoreSystem')
                return result

            # Then create the backup
            if removeBackup == False:
                result = backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
                if result[0] != 'SUCCESS':
                    if self.linuxDistro == distroTypes[1]:
                        logger.error('Could not create backup on RHEL system after installing component. %s. \
                        This is not a critical failure, the test should not be failed due to this.' %result[1])
                    else:
                        logger.debug('leave restoreSystem')
                        return result
        else:
            if removeBackup == True:
                result = saf_lib.backupRemove(backupName)
                if result[0] != 'SUCCESS':
                    logger.debug('leave restoreSystem')
                    return result

    logger.debug('leave restoreSystem')
    return ('SUCCESS', 'System restored')

def prepareInstallationFiles(desiredInstallationLevel, supportedComponents, pathToInstallationFiles, testSuiteConfig, localPathToSw, distroTypes, linuxDistro):

    global swDirGlobal

    runtimeFile = ''
    installationFile = ''

    component = supportedComponents[desiredInstallationLevel - 1]

    if testSuiteConfig.has_key('sdpFilesOnTarget') and testSuiteConfig['sdpFilesOnTarget'] == True\
        and testSuiteConfig.has_key('instFileNames') and System.getProperty("resetCluster") == "undef":
        for element in testSuiteConfig['instFileNames'][component]:
            if 'runtime' in element:
                runtimeFile = testSuiteConfig['instFileNames'][component][testSuiteConfig['instFileNames'][component].index(element)][1]
            elif 'install' in element:
                installationFile = testSuiteConfig['instFileNames'][component][testSuiteConfig['instFileNames'][component].index(element)][1]
        if runtimeFile == '':
            logger.debug('leave prepareInstallationFiles')
            return ('ERROR', 'Runtime file not defined for %s in test suite config' %component)
        if installationFile == '':
            logger.debug('leave prepareInstallationFiles')
            return ('ERROR', 'Installation file not defined for %s in test suite config' %component)
    else:
        if swDirGlobal == 'undef':
            logger.debug('leave prepareInstallationFiles')
            return ('ERROR', 'Files needed for the re-installation not found')
        else:
            result = checkIfSwInPlace('%s/%s/' %(localPathToSw, swDirGlobal), [component.upper()], distroTypes, linuxDistro)
            if result[0] != 'SUCCESS':
                logger.debug('leave prepareInstallationFiles')
                return result
            if desiredInstallationLevel == 2:
                compRtSdpRel = result[2]
                compInstSdpRel = result[3]
                compRtSdpAbs = result[10]
                compInstSdpAbs = result[11]
            elif desiredInstallationLevel == 3:
                compRtSdpRel = result[4]
                compInstSdpRel = result[5]
                compRtSdpAbs = result[12]
                compInstSdpAbs = result[13]
            files = [compRtSdpRel, compInstSdpRel, compRtSdpAbs, compInstSdpAbs]
            if '' in files:
                logger.debug('leave prepareInstallationFiles')
                return ('ERROR', 'At least one file not found: %s' %str(files))

            result = copyFilesToTarget([compRtSdpAbs, compInstSdpAbs], pathToInstallationFiles, removeDestinationOnTarget=False)
            if result[0] != 'SUCCESS':
                logger.debug('leave prepareInstallationFiles')
                return result

            runtimeFile = compRtSdpRel
            installationFile = compInstSdpRel

    logger.debug('leave prepareInstallationFiles')
    return('SUCCESS', runtimeFile, installationFile)


def getComSaOfflineVersion(testSuiteConfig):
    '''
    Read the offlineVersion of COM SA from testsuite config.
    Note: setting the values can be done in a TC and calling this function can be done in another TC in the same suite.

    Return values if COM SA offline version found in testsuite config:
        returnValue[0] = "REGTEST"
        returnValue[1] = COMSA_release
        returnValue[2] = COMSA_version
        returnValue[3] = COMSA_majorVersion
    Return values if COM SA offline version not found in testsuite config:
        returnValue[0] = "EMPTY"
    '''
    logger.debug('enter getComSaOfflineVersion')
    COMSA_release_key = 'COMSA_release'
    COMSA_version_key = 'COMSA_version'
    COMSA_majorVersion_key = 'COMSA_majorVersion'
    COMSA_release = ''
    COMSA_version = ''
    COMSA_majorVersion = ''
    returnValue = ['','','','']

    if testSuiteConfig.has_key(COMSA_release_key) and testSuiteConfig.has_key(COMSA_version_key) and testSuiteConfig.has_key(COMSA_majorVersion_key):
        logger.info("COMSA_release and COMSA_version exist is testsuite config")
        COMSA_release = testSuiteConfig.get(COMSA_release_key)
        COMSA_version = testSuiteConfig.get(COMSA_version_key)
        COMSA_majorVersion = testSuiteConfig.get(COMSA_majorVersion_key)
        logger.info("COMSA_release: (%s)" %COMSA_release)
        logger.info("COMSA_version: (%s)" %COMSA_version)
        logger.info("COMSA_majorVersion: (%s)" %COMSA_majorVersion)

    if COMSA_release == '' or COMSA_version == '' or COMSA_majorVersion == '':
        returnValue[0] = "EMPTY"
    else:
        returnValue[0] = "REGTEST"
        returnValue[1] = COMSA_release
        returnValue[2] = COMSA_version
        returnValue[3] = COMSA_majorVersion
    logger.debug('leave getComSaOfflineVersion')
    return returnValue


def getOfflineVersion(testSuiteConfig, component):
    '''
    Read the offlineVersion of component from testsuite config.
    Note: setting the values can be done in a TC and calling this function can be done in another TC in the same suite.

    Return values if component offline version found in testsuite config:
        returnValue[0] = "REGTEST"
        returnValue[1] = component_release
        returnValue[2] = component_version
        returnValue[3] = component_majorVersion
    Return values if component offline version not found in testsuite config:
        returnValue[0] = "EMPTY"
    '''
    logger.debug('enter getOfflineVersion')

    compName = component.upper()
    release_key = 'release'
    version_key = 'version'
    majorVersion_key = 'majorVersion'


    release = ''
    version = ''
    majorVersion = ''

    if testSuiteConfig.has_key('releases') and testSuiteConfig['releases'].has_key(compName):
        if testSuiteConfig['releases'][compName].has_key(release_key):
            release = testSuiteConfig['releases'][compName][release_key]
            logger.info("%s release: (%s)" %(component, release))
        if testSuiteConfig['releases'][compName].has_key(version_key):
            version = testSuiteConfig['releases'][compName][version_key]
            logger.info("%s version: (%s)" %(component, version))
        if testSuiteConfig['releases'][compName].has_key(majorVersion_key):
            majorVersion = testSuiteConfig['releases'][compName][majorVersion_key]
            logger.info("%s majorVersion: (%s)" %(component, majorVersion))

    returnValue = ['','','','']
    if release == '' or version == '' or majorVersion == '':
        returnValue[0] = "EMPTY"
    else:
        returnValue[0] = "REGTEST"
        returnValue[1] = release
        returnValue[2] = version
        returnValue[3] = majorVersion
    logger.debug('leave getComSaOfflineVersion')
    return returnValue

def findNewLeaks(pathToKnownLeaks, pathToLeaksOnTarget, local = False):
    cmd = 'ls %s' %pathToKnownLeaks
    result = misc_lib.execCommand(cmd)
    if result[0] != 'SUCCESS':
        return result
    knownLeaks = result[1].split()

    if local == False:
        result = ssh_lib.sendCommand('ls %s' %pathToLeaksOnTarget)
    else:
        cmd = 'ls %s' %pathToLeaksOnTarget
        result = misc_lib.execCommand(cmd)
    if result[0] != 'SUCCESS':
        return result
    foundLeaks = result[1].split()

    md5SumFiles = re.compile(r'[0-9a-f]{32}')
    newLeaks = []

    for leak in foundLeaks:
        if md5SumFiles.match(leak):
            if leak not in knownLeaks:
                newLeaks.append(leak)

    if len(newLeaks) != 0:
        for leak in newLeaks:
            if local == False:
                result = ssh_lib.remoteCopyFrom('%s/%s' %(pathToLeaksOnTarget, leak), pathToKnownLeaks)
            else:
                cmd = 'cp %s/%s %s' %(pathToLeaksOnTarget, leak, pathToKnownLeaks)
                result = misc_lib.execCommand(cmd)
            if result[0] != 'SUCCESS':
                return result
        return ('ERROR', 'The files with the following name(s) under %s contain new memory leaks: %s' %(pathToKnownLeaks, str(newLeaks)))
    else:
        return ('SUCCESS', 'No new memory leaks found')

def removeAuthorizedKey(testConfig):
    logger.info('remove authorized keys from the cluster')
    noOfSCs = len(testConfig['controllers'])
    if noOfSCs == 1:
        result = ssh_lib.sendCommand('\\rm -f /boot/patch/root/.ssh/authorized_keys ', 2, 1)
        if result[0] != 'SUCCESS':
            return result
        result = ssh_lib.sendCommand('\\rm -f /root/.ssh/authorized_keys ', 2, 1)
        if result[0] != 'SUCCESS':
            return result
    else:
        logger.info('remove authorized keys from both SCs')
        result = ssh_lib.sendCommand('\\rm -f /boot/patch/root/.ssh/authorized_keys ', 2, 1)
        if result[0] != 'SUCCESS':
            return result
        result = ssh_lib.sendCommand('\\rm -f /root/.ssh/authorized_keys ', 2, 1)
        if result[0] != 'SUCCESS':
            return result
        result = ssh_lib.sendCommand('\\rm -f /boot/patch/root/.ssh/authorized_keys ', 2, 2)
        if result[0] != 'SUCCESS':
            return result
        result = ssh_lib.sendCommand('\\rm -f /root/.ssh/authorized_keys ', 2, 2)
        if result[0] != 'SUCCESS':
            return result
        return ('SUCCESS','Authorized keys removed')

def stopOpensafService(testConfig):
    logger.info('Stopping Opensafd on all nodes')
    noOfPLs = len(testConfig['payloads'])
    noOfSCs = len(testConfig['controllers'])
    result =  ssh_lib.getTimeout()
    defTimeout =  result[1]
    ssh_lib.setTimeout(60)
    if noOfPLs != 0:
        for pl in range(1 + noOfSCs, noOfPLs + noOfSCs + 1):
            result = ssh_lib.sendCommand('cmwea hostname-get 1,1,%s' %pl)
            if result[0] != 'SUCCESS':
                ssh_lib.setTimeout(defTimeout)
                return result
            result = ssh_lib.sendCommand('ssh %s \'service opensafd stop; exit\'' %result[1])
            if result[0] != 'SUCCESS':
                ssh_lib.setTimeout(defTimeout)
                return result
    if noOfSCs == 1:
        result = ssh_lib.sendCommand('service opensafd stop')
        if result[0] != 'SUCCESS':
            ssh_lib.setTimeout(defTimeout)
            return result
    else:
        result = ssh_lib.sendCommand('service opensafd stop', 2, 1)
        if result[0] != 'SUCCESS':
            ssh_lib.setTimeout(defTimeout)
            return result
        result = ssh_lib.sendCommand('service opensafd stop', 2, 2)
        if result[0] != 'SUCCESS':
            ssh_lib.setTimeout(defTimeout)
            return result
    misc_lib.waitTime(20)
    ssh_lib.setTimeout(defTimeout)
    return ('SUCCESS', 'Service opensafd stopped')

def startOpensafService(testConfig):
    logger.info('Starting Opensafd on all nodes')
    noOfPLs = len(testConfig['payloads'])
    noOfSCs = len(testConfig['controllers'])
    result =  ssh_lib.getTimeout()
    defTimeout =  result[1]
    ssh_lib.setTimeout(60)
    if noOfSCs == 1:
        result = ssh_lib.sendCommand('service opensafd start')
        if result[0] != 'SUCCESS':
            ssh_lib.setTimeout(defTimeout)
            return result
    else:
        result = ssh_lib.sendCommand('service opensafd start', 2, 1)
        if result[0] != 'SUCCESS':
            ssh_lib.setTimeout(defTimeout)
            return result
        result = ssh_lib.sendCommand('service opensafd start', 2, 2)
        if result[0] != 'SUCCESS':
            ssh_lib.setTimeout(defTimeout)
            return result
    misc_lib.waitTime(20)
    if noOfPLs != 0:
         for pl in range(1 + noOfSCs, noOfPLs + noOfSCs + 1):
            result = ssh_lib.sendCommand('cmwea hostname-get 1,1,%s' %pl)
            if result[0] != 'SUCCESS':
                ssh_lib.setTimeout(defTimeout)
                return result
            result = ssh_lib.sendCommand('ssh %s \'service opensafd start; exit\'' %result[1])
            if result[0] != 'SUCCESS':
                ssh_lib.setTimeout(defTimeout)
                return result
    result = waitForClusterStatusOk()
    if result != 'SUCCESS':
        ssh_lib.setTimeout(defTimeout)
        return result
    ssh_lib.setTimeout(defTimeout)
    return ('SUCCESS', 'Service opensafd started')

#########################################################################################
#
# class globalConfig()
#
# Description:
#               This class provides the global variables for COMSA testcases
#
#########################################################################################
class globalConfig():

    # by default debugging is turned off
    def __init__(self,globalSelf,debugEnabled = False):
        self.globalSelf = globalSelf
        self.configFileName = "globalPaths.cfg"
        self.configFilePath = "/test_env/testcases/comsa/configFiles/"
        self.debugEnabled = debugEnabled
        self.listForDebug = []

    def debug(self,text):
        if self.debugEnabled:
            self.globalSelf.myLogger.debug(text)

    # Functionality: calls subfunctions to parse the config file and create a dictionary from it
    # returns: the dictionary
    def get_GlobalConfig(self):
        self.debug('enter get_GlobalConfig')

        # open the config file, read line-by-line and put the lines to a list
        lineList = self.readConfigFile()
        dict = self.createDictionary(lineList)

        self.globalSelf.myLogger.info('Parsed config(')
        for key in self.listForDebug:
            self.globalSelf.myLogger.info('                %s = %s' %(key,dict.get(key)))
        self.globalSelf.myLogger.info('             )')

        self.debug('leave get_GlobalConfig')
        return dict

    # Functionality: read and parse the config file
    # Description: open the config file, read line-by-line, do white-space filtering and put the lines to a list
    # returns: the list
    def readConfigFile(self):
        self.debug('enter readConfigFile')

        configFilePath = MY_REPOSITORY + self.configFilePath + self.configFileName
        self.debug('opening config file: %s' %configFilePath)
        configFile = open(configFilePath, 'r')

        # Remove whitespaces and new-line chars
        # and put the pure string lines to a list
        # Skip blank lines and commented lines. Lines containing "#" char won't be processed at all
        lineList = []
        for line in configFile:
            theLine = line.replace(' ','').replace('\t','').replace('\n','')
            # Empty lines and lines containing "#" char won't be processed at all
            if ('#' not in theLine) and (len(theLine) != 0):
                lineList.append(theLine)

        for line in lineList:
            self.debug('line: (%s)' %line)

        self.debug('leave readConfigFile')
        return lineList

    # Creates the dictionary from the line-list
    # returns: the dictionary
    def createDictionary(self, lineList):
        self.debug('enter createDictionary')

        dict = {}
        for element in lineList:
            keyValuePair = element.split('=')
            if len(keyValuePair) == 2:
                dict = self.parseValue(keyValuePair,dict)
            else:
                self.globalSelf.myLogger.info('ERROR: invalid line in config: (%s)' %element)

        self.debug('leave createDictionary')
        return dict

    # parses the line and put the key-value pairs to the dictionary
    # Parallely creates a list of the keys(needed for ordered debug printout).
    def parseValue(self, keyValuePair, dict):
        self.debug('enter parseValue')
        self.debug('key: %s value: %s' %(keyValuePair[0],keyValuePair[1]))

        key = keyValuePair[0]
        value = keyValuePair[1]
        outputStr = ""

        valueElements = value.split('+')
        for element in valueElements:
            self.debug('element: %s' %element)
            dictRes = dict.get('%s' %element)
            if dictRes == None:
                outputStr += element
            else:
                outputStr += dictRes

        dict.setdefault(key,outputStr)
        # for the ordered debugging only
        self.listForDebug.append(key)

        self.debug('leave parseValue')
        return dict


def installStressToolOnTarget(self):
    """
    This method do:
    0. Check if the rpms are loaded already on target
    1. Check if it is one or two node cluster
    2. copy the stress tool rpms to target
    3. install the rpms
    """

    dict = self.comsa_lib.getGlobalConfig(self)
    self.stressToolRpmsHere = dict.get("PATH_TO_STRESSTOOOL")
    self.tmpMrDirOnTarget = '/home/release/'+ 'tools/' + 'stress/'
    self.rpmNames = ['libcgroup.rpm', 'stress-1.0.4-2.1.x86_64.rpm', 'stress-manager.rpm']
    self.PathTostressRpms = ['%s/%s' %(self.stressToolRpmsHere, 'libcgroup.rpm'), \
                             '%s/%s' %(self.stressToolRpmsHere, 'stress-1.0.4-2.1.x86_64.rpm'), \
                             '%s/%s' %(self.stressToolRpmsHere, 'stress-manager.rpm')]
    cmd = 'which stress'
    result = self.sshLib.sendCommand(cmd)
    self.fail(result[0], result[1])
    if result[1] == '/usr/bin/stress':
        self.setTestStep('The stress tool is already installed')
        return ('SUCCESS', 'stress tool already installed')
    else:
        self.setTestStep('Copy stress tool rpms to target')

        result = self.comsa_lib.copyFilesToTarget( self.PathTostressRpms, self.tmpMrDirOnTarget )
        self.fail(result[0], result[1])

        self.setTestStep('Install stress tool rpms on target')
        # copy the rpms to the cluster directory on target
        for rpm in self.rpmNames:
            cmd = 'cp %s/%s /cluster/rpms' %(self.tmpMrDirOnTarget, rpm)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

        # add them to the configurations
        for rpm in self.rpmNames:
            for controller in self.testConfig['controllers']:
                cmd = 'cluster rpm --add %s --node %d' %(rpm, self.testConfig['controllers'].index(controller) + 1)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

        # activate must be executed locally on each controller node

        # Log into the active controller and get the node identity
        self.setTestStep('activate rpms')

        for controller in self.testConfig['controllers']:
            cmd = 'cluster rpm --activate --node %d' %(self.testConfig['controllers'].index(controller) + 1)
            result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
            if result[0] != 'SUCCESS':
                logger.debug('leave installStressToolOnTarget, it failed on controller: %s' %str(controller))
                return result

        self.setTestStep('Done with stress tool installation')


#########################################################################################
#
# Function: startStressToolOnTarget
#
# Description:
#
#              This function starts the stress tool on a cluster to generate background
#              activity.
#
#              Before starting the stress tool the function tries to kill any already running stress processes
#
#              The default values provided are the ones that is possible to run on a
#              Vsphere virtual box
#
#########################################################################################
def startStressToolOnTarget(self, cpuLoad=1, sync=0, numberOfvm=1 , memoryBytes=1000000000, timeToExecuteSec=60*60*60,
                             localDiskLoad=0, localDiskBytes=0, nfsDiskLoad=0, nfsDiskBytes=0):
    """
    This method start the stress tool on both controllers with the parameters value set
    """

    # Kiil any already running stress processes
    stopStressToolOnTarget(self)

    timeOut = 60

    # The CPU and memory are always grouped together. If the CPU is 0 then the memory is not stressed either
    if cpuLoad == 0:
        self.setTestStep('No stress tool for local disk load requested')
    else:
        if sync == 0:
            cmd = 'nohup stress --cpu %s --vm %s --vm-bytes %s --timeout %s --vm-keep >> nohup.out 2>&1 &' \
                %(cpuLoad, numberOfvm, memoryBytes, timeToExecuteSec)
        else:
            cmd = 'nohup stress --cpu %s --io %s --vm %s --vm-bytes %s --timeout %s --vm-keep >> nohup.out 2>&1 &' \
                %(cpuLoad, sync, numberOfvm, memoryBytes, timeToExecuteSec)

        for controller in self.testConfig['controllers']:
            self.sshLib.setTimeout(timeOut)
            result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
            if result[0] != 'SUCCESS':
                logger.debug('leave startStressToolOnTarget, it failed on controller: %s' %str(controller))
                return result

        self.setTestStep('Done with starting the stress tool for CPU and memory')

    # Start stress on disks if any was requested
    localDiskLocation = "cd /var/log;"
    nfsDiskLocation   = "cd /cluster;"

    if localDiskLoad == 0:
        self.setTestStep('No stress tool for local disk load requested')
    else:
        cmd = '%s nohup stress --hdd %s --hdd-bytes %s --timeout %s >> nohup.out 2>&1 &' \
        %(localDiskLocation, localDiskLoad, localDiskBytes, timeToExecuteSec)

        for controller in self.testConfig['controllers']:
            self.sshLib.setTimeout(timeOut)
            result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
            if result[0] != 'SUCCESS':
                logger.debug('leave startStressToolOnTarget, it failed starting local disk stress on controller: %s' %str(controller))
                return result

        self.setTestStep('Done with starting the stress tool for local disk load')

    if nfsDiskLoad == 0:
        self.setTestStep('No stress tool for NFS disk load requested')
    else:
        cmd = '%s nohup stress --hdd %s --hdd-bytes %s --timeout %s >> nohup.out 2>&1 &' \
        %(nfsDiskLocation, nfsDiskLoad, nfsDiskBytes, timeToExecuteSec)

        for controller in self.testConfig['controllers']:
            self.sshLib.setTimeout(timeOut)
            result = ssh_lib.sendCommand(cmd, controller[0], controller[1])
            if result[0] != 'SUCCESS':
                logger.debug('leave startStressToolOnTarget, it failed starting NFS disk stress on controller: %s' %str(controller))
                return result

        self.setTestStep('Done with starting the stress tool for NFS disk load')

#########################################################################################
def stopStressToolOnTarget(self):

    """
    This method stops any stress tool processes on both controllers
    """

    # Kiil any already running stress processes
    cmd = '/etc/init.d/stress_manager stop'

    for controller in self.testConfig['controllers']:
        result_chk = self.sshLib.sendCommand(cmd, controller[0], controller[1])
        self.fail(result_chk[0], result_chk[1])


def getNumOfCPUsOnNode(self):
    """
    This method returns the number of CPU cores on a node
    """
    # Determine the number of processor cores in the node
    cmd = 'grep -c ^processor /proc/cpuinfo'
    result = self.sshLib.sendCommand(cmd)
    self.fail(result[0],result[1])
    if result[0] != 'SUCCESS':
        logger.debug('getNumOfCPUsOnNode failed.')
    return result


def getBytesOfRamOnNode(self):
    """
    This method returns the RAM size in bytes on a node
    """
    # Determine the total physical RAM in the node
    cmd = 'free -b | grep -i  mem | awk \'{print $2}\''
    result = self.sshLib.sendCommand(cmd)
    self.fail(result[0],result[1])
    if result[0] != 'SUCCESS':
        logger.debug('getBytesOfRamOnNode failed.')
    return result


def getVboxKvmClusterConfig(self):
    config = System.getProperty("###__TARGET_SYSTEM__###")
    if 'vbox' == config.split('_')[0] or 'qemu' == config.split('_')[0]:
        return True
    else:
        return False


#########################################################################################
#
# Function: getGlobalConfig
#
# Description:
#
#              This function is the interface between the testcases
#              and the function which provides the global variables for COMSA testcases.
#
#########################################################################################
def getGlobalConfig(self):
    self.myLogger.debug('enter comsa_lib.getGlobalConfig')
    # debugging is turned off by default (by "False")
    res = globalConfig(self,False).get_GlobalConfig()
    self.myLogger.debug('leave comsa_lib.getGlobalConfig')
    return res

#########################################################################################
#
# class emailReport()
#
# Description:
#               This class handles the email reporting for regtest
#
#########################################################################################
class emailReport():

    # by default debugging is turned off
    def __init__(self, globalSelf, debugEnabled = False):
        self.globalSelf = globalSelf
        #self.dict = getGlobalConfig(globalSelf)
        self.debugEnabled = debugEnabled

    def debug(self,text):
        if self.debugEnabled:
            self.globalSelf.myLogger.debug(text)

    # Functionality: create email content based on the status and send this email to the subscribers who are in the list
    def send(self, status, noOfScs):
        self.debug('enter send')

        # read the list of subscribers from config file
        subList = self.getSubscribersList()
        # create text for the email depending on the "status"
        emailContent = self.createEmailContent(status, subList, noOfScs)
        # send the emails
        self.sendEmails(subList, emailContent)

        self.debug('leave send')
        return

    # Functionality: read the IDs from the config file
    # Description: open the config file, read line-by-line, do white-space filtering and put the lines to a list
    # returns: the list
    def getSubscribersList(self):
        self.debug('enter getSubscribersList')

        filePath = MY_REPOSITORY + self.globalSelf.emailListFilePath + self.globalSelf.emailListFileName
        self.debug('opening config file: %s' %filePath)
        theFile = open(filePath, 'r')

        # Remove whitespaces and new-line chars
        # and put the pure string lines to a list
        # Skip blank lines and commented lines. Lines containing "#" char won't be processed at all
        subList = []
        for line in theFile:
            theLine = line.replace(' ','').replace('\t','').replace('\n','')
            # Empty lines and lines containing "#" char won't be processed at all
            # Double entries not allowed.
            if ('#' not in theLine) and (len(theLine) != 0) and (theLine not in subList):
                subList.append(theLine)

        for line in subList:
            self.debug('subscriber: (%s)' %line)

        self.debug('leave getSubscribersList')
        return subList

    # returns: 2 element list
    #            element 0 is the subject of the email
    #            element 1 is the text of the email
    def createEmailContent(self, status, subList, noOfScs):
        self.debug('enter createEmailContent')
        extra_info = ""

        # get current user's ID
        currentUser = os.environ['USER']
        hostName    = os.environ['HOST']
        self.debug('currentUser: (%s)' %currentUser)
        self.debug('hostName: (%s)' %hostName)
        dek_server = "cbaserv"

        # read the absolute path of the current JCAT log directory
        logdir = System.getProperty("logdir")
        self.debug('logdir: (%s)' %logdir)
        logFileLink = "file://" + logdir + "/index.html" + "\n\n"
        self.debug('dek compare: (%s) (%s)' %(hostName[:len(dek_server)], dek_server))
        if hostName[:len(dek_server)] == dek_server:
            # DEK Server
            logFileLink += "file://" + hostName + ".dek-tpc.internal" + logdir + "/index.html"
        else:
            # EAB Server
            # Remove /proj/coremw_scratch and add the link to public website
            logFileLink += "https://cc-userarea.rnd.ki.sw.ericsson.se" + logdir[len("/proj/coremw_scratch"):] + "/"
            # To setup the link:
            # mkdir /proj/tspsaf/www/public_html/<x-id>
            # cd /proj/tspsaf/www/public_html/<x-id>
            # ln -s /proj/coremw_scratch/<x-id>/logs logs

        self.debug('logFileLink: (%s)' %logFileLink)
        suiteName = System.getProperty("suiteName").split('.')[0]
        clusterName = targetData['target']
        clusterIpAddrCtrl1 = targetData['ipAddress']['ctrl']['ctrl1']
        sw_config = 'unknown'
        result = saf_lib.getInstalledSwOnRepository()
        if result[0] == 'SUCCESS':
            sw_config = result[1]
        result = ssh_lib.sendCommand("cluster info | egrep -v '(Installation Type:)|(Source info:)'")
        os_config = 'unknown'
        if result[0] == 'SUCCESS':
            os_config = result[1]

        text = "\nThis is an automatic mail generated by an automated test run.\n"
        text += "You received this mail, because your are in the following email list:\n"
        text += MY_REPOSITORY + self.globalSelf.emailListFilePath + self.globalSelf.emailListFileName + "\n\n"
        text += "Host name is: %s\n" %hostName
        if 2 == noOfScs:
            text += "Target name: %s - Dual Node\n" %clusterName
        elif 1 == noOfScs:
            text += 'Target name: %s - One Node\n' %clusterName
        else:
            text += "Target name: %s - Unknown Node\n" %clusterName

        text += "Target system controller 1 IP adress is: %s\n\n" %clusterIpAddrCtrl1
        text += "Source commitID: %s\n" %os.environ['COMSA_REPO_PATH_COMMIT_ID']
        text += "Verification commitID: %s\n\n" %os.environ['COMSA_VERIFICATION_COMMIT_ID']

        if sw_config != 'unknown':
            text += "SW configuration on the target is: \n%s\n" %sw_config
        if os_config != 'unknown':
            text += "OS configuration on the target is: \n%s\n" %os_config

        # create email text
        if status == "INSTALLATION FAILED":
            text += "\nInstallation of Core MW, COM or COM SA failed.\n\n"
            text += "The test execution will be terminated with immediate effect.\n"
            text += "For details check the link to the test logs below.\n"
            text += logFileLink + "\n\n"

        elif status == "STARTED":
            text += "\n\nLink of the test logs:\n"
            text += logFileLink + "\n\n"
            text += "You will receive another mail as soon as the regtest finishes."

        elif status == "COMPILER WARNINGS":
            text += "\nCompilation of COM SA has warnings.\n\n"
            text += "The test execution will be terminated with immediate effect.\n"
            text += "For details check the link to the test logs below.\n"
            text += logFileLink + "\n\n"

        elif status == "FINISHED":
            #passedTCs = self.globalSelf.miscLib.execCommand("grep -c \"PA\" %s/tpt.txt")
            #failedTCs = self.globalSelf.miscLib.execCommand("grep -c \"NP\" %s/tpt.txt")
            #totalTCs = self.globalSelf.miscLib.execCommand("wc -l %s/tpt.txt")

            runTCs = 'unknown'
            passedTCs = 'unknown'
            failedTCs = 'unknown'
            errorTCs = 'unknown'

            result = self.getTestCasePassRates('TCs run', logdir)
            if result[0] == 'SUCCESS':
                runTCs = result[1]
            result = self.getTestCasePassRates('TCs passed', logdir)
            if result[0] == 'SUCCESS':
                passedTCs = result[1]
            result = self.getTestCasePassRates('TCs failed', logdir)
            if result[0] == 'SUCCESS':
                failedTCs = result[1]
            result = self.getTestCasePassRates('TCs error', logdir)
            if result[0] == 'SUCCESS':
                errorTCs = result[1]

            failedTcTags = []
            notPassedCode = 'NP'
            result = misc_lib.execCommand('grep %s "%s/tpt.txt"' %(notPassedCode, logdir))
            for line in result[1].splitlines():
                if 'TC-' in line:
                    failedTcTags.append(line.split(",")[1])


            text += "\n\nTest suite finished.\n"
            text += "\n\nLink of the test logs:\n"
            text += logFileLink + "\n\n\n"
            text += "Total number of test cases run: %s (the tearDown test case is not part of the report)" %runTCs
            text += "Test cases passed: %s" %passedTCs
            text += "Test cases failed: %s" %failedTCs
            text += "Test cases error: %s" %errorTCs
            #text += "PASSED: %s\n\n" %passedTCs[1]
            #text += "PASSED: (not working yet)\n\n"
            #text += "FAILED: %s\n\n" %failedTCs[1]
            #text += "FAILED: (not working yet)\n\n"
            text += "--------------\n\n"
            #text += "TOTAL: %s" %totalTCs[1]
            #text += "TOTAL: (not working yet)"
            if len(failedTcTags) > 0:
                text += "Failed test cases: %s" %str(failedTcTags)

            # Add links to code coverage results (if any)

            searchPattern0 = "cov_comsa_"
            searchPattern1 = "Coverage report:"
            searchPattern2 = "html_ut"
            result = misc_lib.execCommand('grep %s "%s/report.htm" | grep "%s" | grep %s | awk \'{print$28}\' | sed \'s/<.*//\'' %(searchPattern0, logdir, searchPattern1, searchPattern2))
            if result[0] == 'SUCCESS':
                if result[1] != "":
                    utCoverageLink = result[1]
                    text += "\n\nUT Code Coverage results link: \n%s\n\n" %utCoverageLink

            searchPattern1 = "FT Coverage report:"
            result = misc_lib.execCommand('grep %s "%s/report.htm" | grep "%s" | awk \'{print$37}\' | sed \'s/<.*//\'' %(searchPattern0, logdir, searchPattern1))
            if result[0] == 'SUCCESS':
                if result[1] != "":
                    utCoverageLink = result[1]
                    text += "\n\nFT Code Coverage results link: \n%s\n\n" %utCoverageLink

            result = misc_lib.execCommand('grep %s "%s/report.htm" | grep "%s" | awk \'{print$40}\' | sed \'s/<.*//\'' %(searchPattern0, logdir, searchPattern1))
            if result[0] == 'SUCCESS':
                if result[1] != "":
                    covResultsLink = result[1]
                    text += "Combined UT+FT Code Coverage results link: \n%s\n\n" %covResultsLink

        else:
            text = "ERROR: \"status\" not set for the email report. Check the testautomation code!"

        self.debug('text: (%s)' %text)

        # create email subject


        if status == "FINISHED":
            extra_info = 'Total TCs: %s Passed: %s' %(runTCs, passedTCs)
            subject = "%s (by %s) %s %s" %(suiteName, currentUser, status, extra_info)
        else:
            subject = "%s (by %s) status: %s %s" %(suiteName, currentUser, status, extra_info)
        self.debug('subject: (%s)' %subject)

        self.debug('leave createEmailContent')
        return [subject, text]

    # send the emails
    def sendEmails(self, subList, emailContent):
        self.debug('enter sendEmails')

        email_subject = emailContent[0]
        email_text = emailContent[1]

        self.debug('email_subject (%s)' %email_subject)
        self.debug('email_text (%s)' %email_text)

        for email_address in subList:
            self.globalSelf.myLogger.info('Sending email to %s' %email_address)
            cmd = 'echo "%s" | mail -s "%s" "%s"' %(email_text, email_subject, email_address)
            self.debug('cmd: (%s)' %cmd)
            os.popen(cmd)

        self.debug('leave sendEmails')
        return

    def getTestCasePassRates(self, field, logdir):
        self.debug('get number of %s' %field)
        cmd = """grep '%s' "%s/report.htm" | awk -F '<td>' '{print $3}' | cut -d\< -f1""" %(field, logdir)
        result = misc_lib.execCommand(cmd)
        if result[0] != 'SUCCESS':
            self.debug('Unable to get value for %s. Problem: %s' %(field, result[1]))
        else:
            self.debug('%s: %s' %(field, result[1]))
        return result

