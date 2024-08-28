#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
###############################################################################
#
# Ericsson AB 2010 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and dissemination to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################
"""
GENERAL INFORMATION:

    Test cases:

    TC-FT815-001 - Functiontest of SDP815 - Check IMM-I-FileM is registered by COMSA

    Priority:
    High

    Requirement:
    -

    Sensitivity:
    Low

    Restrictions:
    -

    Test tools:
    -

    Configuration:
    2SC+nPL

    Action:

    Result:



    Restore:
    N/A

    Description:

    -Check if CMW has MDF, if NO then skip the following steps and PASS the testcase, otherwise continue:
    -Check if IMM-I-FileM is registered to a SC
    -Do a switch-over
    -Check if IMM-I-FileM is still registered to a SC

    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-FT815-001

    Id:
    ""
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import os, time, re, copy

from java.lang import System
class FTSdp815(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.testcase_tag = tag
        self.test_config = testConfig
        # parameters from the config files
        self.mdfStatusCommand = 'cmw-model-status'
        self.immFileM_controllerNames = ['SC-1', 'SC-2']
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        coreTestCase.CoreTestCase.setUp(self)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.logger.info('Exit setUp')

    def runTest(self):

        ###############################################################################
        ######################### Functiontest of SDP815 ##############################
        ###############################################################################

        self.setTestStep('runTest')
        self.myLogger.info('enter runTest')

        ###############################################################################
        ########################### Check if CMW has MDF ##############################
        ###############################################################################

        self.setTestStep('check if CMW has MDF')
        result = self.sshLib.sendCommand(self.mdfStatusCommand)

        if self.installStressTool:
            self.setTestStep('======== Install the stress tool ========')
            self.comsa_lib.installStressToolOnTarget(self)
            stressTimeOut = 60
            self.setTestStep('======== Start the stress tool ========')

            # Determine the number of processor cores in the node
            result = self.comsa_lib.getNumOfCPUsOnNode(self)
            self.fail(result[0],result[1])
            numOfCpuCores = result[1];
            self.myLogger.debug('Found %s CPU cores' %numOfCpuCores)

            # Determine the total physical RAM in the node
            result = self.comsa_lib.getBytesOfRamOnNode(self)
            self.fail(result[0],result[1])
            totalRamBytes = result[1];
            tenPercentOfTotalRam = int(totalRamBytes) // 10
            self.myLogger.debug('Found total %s bytes of RAM, 10 percent is %s' %(totalRamBytes, tenPercentOfTotalRam))

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, no disk stress
            #result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 0, 0)

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM
            # plus NFS disk stress 1 task 64K bytes blocks plus local disk stress 2 tasks 4M bytes blocks
            result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)
            self.sshLib.setTimeout(stressTimeOut)

        if 'command not found' not in result[1]:
            self.myLogger.info('CMW has MDF')
            ###############################################################################
            ############## Check if IMM-I-FileM is registered by the active SC ############
            ###############################################################################

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

            noOfScs = len(self.testConfig['controllers'])
            if noOfScs == 2 and standbyController == 0:
                self.fail('ERROR', 'No controller found with standby instance of ComSa.')

            if activeController == 1:
                name_of_active_SC = self.immFileM_controllerNames[0]
            elif activeController == 2:
                name_of_active_SC = self.immFileM_controllerNames[1]
            else:
                self.fail('ERROR', 'Unknown controller number: %s' %str(activeController))

            if noOfScs == 2:
                if standbyController == 1:
                    name_of_standby_SC = self.immFileM_controllerNames[0]
                elif standbyController == 2:
                    name_of_standby_SC = self.immFileM_controllerNames[1]
                else:
                    self.fail('ERROR', 'Unknown controller number: %s' %str(standbyController))

            self.setTestStep('Check if IMM-I-FileM is registered to a SC')

            ######## TO DO
            #cmd = '%s | grep "Model Type: IMM-I-FileM" -A 1 | tail -1' %self.mdfStatusCommand
            cmd = """%s | grep "IMM-I-FileM_R1" -A 2 | tail -1""" %self.mdfStatusCommand
            result = self.sshLib.sendCommand(cmd)

            if (name_of_active_SC in result[1]) or (name_of_standby_SC in result[1]):
                self.myLogger.info('IMM-I-FileM is registered')
            else:
                self.fail('ERROR', 'IMM-I-FileM is NOT registered to a System Controller. This could still be fine in case some older LOTC is used e.g. LOTC 4.0')

            ###############################################################################
            ############################# First switch-over ###############################
            ###############################################################################
            if noOfScs == 2:
                self.setTestStep('Get ComSa DN and lock ')

                result = self.comsa_lib.lockSu(controller[0], activeController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck)
                self.fail(result[0], result[1])

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

                ########################################################################################
                ### After the first switch-over: Check if IMM-I-FileM is registered by the active SC ###
                ########################################################################################

                self.setTestStep('After switch-over: find active comSa node after switch-over')

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
                elif standbyController == 0:
                    self.fail('ERROR', 'No controller found with standby instance of ComSa.')

                if activeController == 1:
                    name_of_active_SC = self.immFileM_controllerNames[0]
                elif activeController == 2:
                    name_of_active_SC = self.immFileM_controllerNames[1]
                else:
                    self.fail('ERROR', 'Unknown controller number: %s' %str(activeController))

                if standbyController == 1:
                    name_of_standby_SC = self.immFileM_controllerNames[0]
                elif standbyController == 2:
                    name_of_standby_SC = self.immFileM_controllerNames[1]
                else:
                    self.fail('ERROR', 'Unknown controller number: %s' %str(standbyController))

                self.setTestStep('After the first switch-over: Check if IMM-I-FileM is registered by the active SC')

                cmd = """%s | grep "IMM-I-FileM_R1" -A 2 | tail -1""" %self.mdfStatusCommand
                result = self.sshLib.sendCommand(cmd)

                #if (name_of_active_SC in result[1]) and (name_of_standby_SC not in result[1]):
                #    self.myLogger.info('IMM-I-FileM registered to the active SC')
                #else:
                #    self.fail('ERROR', 'IMM-I-FileM is NOT registered to the active SC. This could still be fine in case some older LOTC is used e.g. LOTC 4.0')
                if (name_of_active_SC in result[1]) or (name_of_standby_SC in result[1]):
                    self.myLogger.info('IMM-I-FileM is registered')
                else:
                    self.fail('ERROR', 'IMM-I-FileM is NOT registered to a System Controller. This could still be fine in case some older LOTC is used e.g. LOTC 4.0')

        else:
            self.myLogger.info('CMW has no MDF')

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")

    def tearDown(self):
        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)
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
