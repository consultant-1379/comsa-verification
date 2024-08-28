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
    TC-AVL-002    Availability control - Switchover


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
    TC-AVL-002


    Id:
    Switchover


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

class Switchover(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        # parameters from the config files


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
        if noOfScs == 2:
            self.setTestStep('runTest find active comSa node')

            activeController = 0
            standbyController = 0

            controllers = self.testConfig['controllers']
            self.myLogger.info('Checking HA state for Com SA on the controllers')
            for controller in controllers:
                result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                if result[1] == 'ACTIVE':
                    activeController = controller[1]
                    self.myLogger.info('Found active controller: %s' %str(controller))
                elif result[1] == 'STANDBY':
                    standbyController = controller[1]
                    self.myLogger.info('Found standby controller: %s' %str(controller))

            if activeController == 0:
                self.fail('ERROR', 'No controller found with active instance of ComSa')
            if standbyController == 0:
                self.fail('ERROR', 'No controller found with standby instance of ComSa.')


            self.setTestStep('Get ComSa DN and lock ')

            result = self.comsa_lib.lockSu(controller[0], activeController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck)
            self.fail(result[0], result[1])
            lockTime = result[2]

            self.setTestStep('Verify that the former standby SC became active ')

            result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], standbyController, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            if result[1] != 'ACTIVE':
                self.fail(result[0], 'The former standby controller did not become active after the former active controller was locked.')

            self.myLogger.info('The former standby controller became active')
            oldActiveController = activeController
            activeController = standbyController
            standbyController = 0


            self.setTestStep('Unlock the locked SC')

            result = self.comsa_lib.unlockSu(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck)
            self.fail(result[0], result[1])
            self.myLogger.info('%s' %str(result[1]))


            self.setTestStep('Verify that the former active SC becomes standby.')

            result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            if result[1] != 'STANDBY':
                self.fail(result[0], 'The former active controller did not become standby after the sericeUnit was unlocked.')

            self.myLogger.info('The former active controller became standby')
            #standbyController = oldActiveController

            comsaStartedPattern = ['osafamfnd', 'Assigned', 'safSi=2N,safApp=ERIC-ComSa', 'ACTIVE to']
            result = self.lib.getEventTimestampFromSyslog(controller[0], activeController, comsaStartedPattern, int(lockTime), self.testConfig)
            self.fail(result[0], result[1])
            matches = result[1]
            if len(matches) != 1:
                self.fail('ERROR', 'Expected only one match. Received: %s' %str(matches))
            switchoverTime = matches[0] - int(lockTime)
            self.setAdditionalResultInfo('Switchover time was: %d seconds.' %switchoverTime)
            self.comsa_lib.addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'Switchover time(s) in seconds during test suite', switchoverTime)
            self.myLogger.info('charMeasurements - Switchover time(s) in seconds during test suite: %s' %str(switchoverTime))

            coreTestCase.CoreTestCase.runTest(self)
        else:
            self.setAdditionalResultInfo('Running a single node configuration. \
            This test case is not valid in this configuration.')
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')
        self.myLogger.info("enter tearDown")
        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info("exit tearDown")



        #########################
        #### SUPPORT METHODS ####
        #########################



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
