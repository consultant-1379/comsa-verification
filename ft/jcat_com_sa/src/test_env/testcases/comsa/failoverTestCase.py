#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
###############################################################################
#
# Copyright Ericsson AB 2010 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################


''' GENERAL INFORMATION:

    Tags:
    TC-AVL-003    Availability control - Failover


    Sensitivity:
    Low

    Description:

    Restrictions:
    -

    Test tools:

    Help:
    The test script is driven by the following parameters:





    TEST CASE SPECIFICATION:

    Tag:
    TC-AVL-003


    Id:
    Failover


    Priority:
    High


    Requirement:


    Test script:
    N/A


    Configuration:
    2SC+nPL


    Action:


    Result:


    Restore:
    N/A

==================================

'''

import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os

from java.lang import System

class Failover(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )

        # parameters from the config files

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.myLogger.info('enter setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        self.modifyFlag = False
        self.failoverCalled = False
        self.memoryCheck = False

        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.myLogger.info('exit setUp')

    def runTest(self):

        self.setTestStep('runTest')
        self.myLogger.info('enter runTest')

        noOfScs = len(self.testConfig['controllers'])
        if noOfScs != 2:
            self.setAdditionalResultInfo('The failover test case is only valid in a configuration with 2 system controllers.')
        else:
            self.setTestStep('Get getComSaSuRestartMax values and restore default if necessary')


            result = self.comsa_lib.getComSaSuRestartMax()
            self.fail(result[0], result[1])
            self.originalSuRestartMax = result[1]
            self.defaultSuRestartMax = result[3]

            if self.originalSuRestartMax != self.defaultSuRestartMax:
                result = self.comsa_lib.setComSaSuRestartMax(True) #suRestartMax is reset to Default
                self.fail(result[0], result[1])
                self.modifyFlag = True

            self.setTestStep('REstart the cluster to reset all failover related counters')

            # this is to save the valgrdind logs before cluster reboot
            if self.memoryCheck:
                for controller in self.testConfig['controllers']:
                    result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                    self.fail(result[0],result[1])

            for i in range(3):
                self.setTestStep('-------- Loop %d --------' %(i+1))
                result = self.comsa_lib.restartCluster(self.testConfig, self.linuxDistro, self.distroTypes)
                self.fail(result[0], result[1])

                self.setTestStep('runTest find active comSa node')

                result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])

                activeController = result[1]
                standbyController = self.testConfig['controllers'][(self.testConfig['controllers'].index(activeController)+1)%2]

                numberOfRestartsNeeded = self.defaultSuRestartMax*2 + 1

                self.failover(activeController, numberOfRestartsNeeded)
            #self.failover(standbyController, numberOfRestartsNeeded)


            comment = ''' This part needs confirmation. Open question: after how many restarts on the standby shall there be a cluster reboot?

            self.setTestStep('Restart the COM process the number of times needed to get a cluster reboot as a recovery mechanism')


            for i in range(numberOfRestartsNeeded):
                print '####### EJNOLSZ: in restarting the former standby: i is: ', i
                result = self.comsa_lib.comRestart(self, activeController[0], activeController[1], self.memoryCheck)
                if (i+1) != numberOfRestartsNeeded:
                    self.fail(result[0], result[1])
                    result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)

                    self.fail(result[0], result[1])
                    currentActiveController = result[1]
                    print '####### EJNOLSZ: in restarting the former standby: current active controller is: ', currentActiveController
                    comment = """
                    if ((i+1) != numberOfRestartsNeeded) and (currentActiveController != standbyController):
                        self.fail('ERROR', 'The failover happened earlier than expected!')
                    if ((i+1) == numberOfRestartsNeeded) and (currentActiveController == standbyController):
                        self.fail('ERROR', 'The expected failover did not happen!')
                    """
                else:
                    self.miscLib.waitTime(20)
                    result = self.safLib.checkClusterStatus()
                    if result[0] == 'SUCCESS':
                        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
                        if result[0] == 'SUCCESS' and result[1] == standbyController:
                            self.fail('ERROR', 'There was no further recovery mechanism from the former standby controller which had become active after the failover. The cluster should have rebooted')

                        self.fail('ERROR', 'It seems that the cluster did not reboot')

                    else:
                        self.miscLib.waitTime(160)

                        testEndTime = int(time.time()) + 720
                        restartFlag = False
                        while (time.time() < testEndTime and restartFlag == False):
                            result = self.sshLib.sendCommand('cmw-status node comp su')
                            if result[0] == 'SUCCESS' and 'Status OK' in result[1]:
                                restartFlag = True
                            else:
                                self.sshLib.tearDownHandles()
                                self.miscLib.waitTime(15)

            '''

            if self.memoryCheck:
                for controller in self.testConfig['controllers']:
                    result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                    self.fail(result[0],result[1])

            result = self.comsa_lib.restartCluster(self.testConfig, self.linuxDistro, self.distroTypes)
            self.fail(result[0], result[1])

            coreTestCase.CoreTestCase.runTest(self)

        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')
        self.myLogger.info("enter tearDown")

        if self.modifyFlag == True:
            result = self.comsa_lib.setComSaSuRestartMax(False, self.originalSuRestartMax)
            self.fail(result[0], result[1])

        if self.failoverCalled == True:
            result = self.comsa_lib.restartCluster(self.testConfig, self.linuxDistro, self.distroTypes)
            self.fail(result[0], result[1])


        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info("exit tearDown")

    def failover(self, activeController, numberOfRestartsNeeded):
        self.setTestStep('Restart the COM process on controller %s the number of times needed to get a failover' %str(activeController))

        self.failoverCalled = True

        for i in range(numberOfRestartsNeeded):
            if (i+1) == numberOfRestartsNeeded:
                result = self.comsa_lib.comRestart(self, activeController[0], activeController[1], self.memoryCheck, charMeasurement = True, failoverTest = True, noPidExpectedAfterRestart = True)
                self.myLogger.info('comRestart returned %s' %str(result))
            else:
                result = self.comsa_lib.comRestart(self, activeController[0], activeController[1], self.memoryCheck, failoverTest = True)
                self.myLogger.info('comRestart returned %s' %str(result))
            self.fail(result[0], result[1])
            if (i+1) == numberOfRestartsNeeded:
                restartTime = int(result[1])

            #result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            #self.fail(result[0], result[1])
            #currentActiveController = activeController
            if (i+1) == numberOfRestartsNeeded:
                currentActiveController = self.testConfig['controllers'][(self.testConfig['controllers'].index(activeController)+1)%2]

            """
            if ((i+1) != numberOfRestartsNeeded) and (currentActiveController != activeController):
                self.fail('ERROR', 'The failover happened earlier than expected!')
            if ((i+1) == numberOfRestartsNeeded) and (currentActiveController == activeController):
                self.fail('ERROR', 'The expected failover did not happen!')
            """
            if (i+1) == numberOfRestartsNeeded:
                comsaStartedPattern = ['osafamfnd', 'Assigned', 'safSi=2N,safApp=ERIC-ComSa', 'ACTIVE to']
                result = self.lib.getEventTimestampFromSyslog(currentActiveController[0], currentActiveController[1], comsaStartedPattern, restartTime, self.testConfig)
                self.fail(result[0], result[1])
                matches = result[1]
                if len(matches) != 1:
                    self.fail('ERROR', 'Expected only one match. Received: %s' %str(matches))
                failoverTime = matches[0] - restartTime
                self.setAdditionalResultInfo('Failover time was: %d seconds.' %failoverTime)
                self.comsa_lib.addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'failover', failoverTime)
                self.myLogger.info('charMeasurements - failover %s:'  %str(failoverTime))

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
