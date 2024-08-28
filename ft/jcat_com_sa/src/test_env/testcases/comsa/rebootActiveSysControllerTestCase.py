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

class RebootActiveController(coreTestCase.CoreTestCase):

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
        self.setTestStep('runTest find active comSa node')

        activeController = 0
        standbyController = 0

        controllers = self.testConfig['controllers']
        self.myLogger.debug('self.testConfig Testing ......%s' %self.testConfig['controllers'])
        self.myLogger.info('Checking HA state for Com SA on the controllers')
        for controller in controllers:
            #what is inside of controller !
            self.myLogger.debug('What is inside of controllers ???? Controllers: %s' %str(controllers))
            self.myLogger.debug('Controller: %s' %str(controller))

            result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            if result[1] == 'ACTIVE':
                activeController = controller
                self.myLogger.info('Found active controller: %s' %str(controller))
            elif result[1] == 'STANDBY':
                standbyController = controller
                self.myLogger.info('Found standby controller: %s' %str(controller))

        noOfScs = len(self.testConfig['controllers'])
        if activeController == 0:
            self.fail('ERROR', 'No controller found with active instance of ComSa')
        if noOfScs == 2 and standbyController == 0:
            self.fail('ERROR', 'No controller found with standby instance of ComSa.')
        elif noOfScs == 1:
            self.setAdditionalResultInfo('Running a single node configuration. \
            Only checking that COM-SA restarts successfully after cluster reboot')


       # Test step 2

        self.setTestStep('Reboot Active Service Controller')
        self.myLogger.info('Rebooting: %s' %str(activeController))

        #result = self.safLib.clusterRebootNode(controller[0], controller[1])
        if self.memoryCheck:
            result = self.comsa_lib.comRestart(self, activeController[0],activeController[1], self.memoryCheck)
            self.fail(result[0],result[1])

        result = self.safLib.clusterRebootNode(activeController[0],activeController[1])
        self.fail(result[0], result[1])

        # Test Step 3

        self.setTestStep('Wait for the Active Controller to come up')
        # Wait until controller 1 is up
        #self.setTestStep('Wait until controller 1 is up')
        #self.myLogger.debug('Wait until controller 1 is up')
        self.miscLib.waitTime(60)


        # Check CMW status, and wait for status ok
        self.setTestStep('Check CMW status, and wait for status ok')
        self.myLogger.debug('Check CMW status, and wait for status ok')
        okFlag = False
        for i in range(30):
            result = self.safLib.checkClusterStatus('off', 'su node comp')
            if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
            else:
                if re.search('cmw-status: command not found', result[1]):
                        self.sshLib.tearDownHandles()
                self.miscLib.waitTime(30)
        if okFlag == False:
            self.fail('ERROR','Cmw status-check timeout')

       # Test Step 4

        self.setTestStep('Find Active System Controller')

        newActiveController = 0
        newStandbyController = 0

        controllers = self.testConfig['controllers']
        self.myLogger.info('Checking HA state for Com SA on the controllers')
        for controller in controllers:
            result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            if result[1] == 'ACTIVE':
                newActiveController = controller
                self.myLogger.info('Found New active controller: %s' %str(newActiveController))
            elif result[1] == 'STANDBY':
                newStandbyController = controller

                self.myLogger.info('Found New standby controller: %s' %str(newStandbyController))

        if newActiveController == 0:
            self.fail('ERROR', 'No controller found with active instance of ComSa')
        if noOfScs == 2:
            if newStandbyController == 0:
                self.fail('ERROR', 'No controller found with standby instance of ComSa.')

            if newActiveController == activeController:
                self.fail('ERROR', 'New Active controller could not be the same like old active controller, it must switch its state from Active Controller to the Standby Controller !!!')
            if newStandbyController == standbyController:
                self.fail('ERROR','New Standby controller could not be the same like old Standby controller, it must switch its state from Standby Controller to the Active Controller !!!')


        coreTestCase.CoreTestCase.runTest(self)
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
