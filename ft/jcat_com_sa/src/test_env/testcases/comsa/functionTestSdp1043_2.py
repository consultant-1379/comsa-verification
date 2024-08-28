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
    TC-FT1043-011    Preparing the cluster for test


    Sensitivity:
    Low

    Description:

    Restrictions:
    -

    Test tools:

    Help:
    The test cases testing SDP1043  can only be run together. The test cases are not independent of each other. Always run the test cases in the order
    that is in the ftSdp1043.xml test suite.

    This test script (functionTestSdp1043) prepares the cluster for the actual tests and should always be run first.



    TEST CASE SPECIFICATION:

    Tag:
    TC-FT1043-001


    Id:
    FunctionTestSdp1043


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
import os
import re

from java.lang import System

class FTSdp1043_2(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )

        # parameters from the config files

        self.testOIFile = 'testOI'
        self.immClassesFile = 'imm_classes.xml'
        self.mpFile = 'mp.xml'
        self.pathOnTargetSystem = '/home/coremw/incoming/'
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.backupName = 'FT1043_initialBackup'
        self.startImplementor = 'no'
        self.cli_input_1 = {}
        self.cli_expected_output_1 = {}
        self.cli_nonexpected_output_1 = {}
        self.cli_input_2 = {}
        self.cli_expected_output_2 = {}
        self.cli_nonexpected_output_2 = {}
        self.cli_input_3 = {}
        self.cli_expected_output_3 = {}
        self.cli_nonexpected_output_3 = {}
        self.cli_input_4 = {}
        self.cli_expected_output_4 = {}
        self.cli_nonexpected_output_4 = {}
        self.cli_input_5 = {}
        self.cli_expected_output_5 = {}
        self.cli_nonexpected_output_5 = {}
        self.cli_input_6 = {}
        self.cli_expected_output_6 = {}
        self.cli_nonexpected_output_6 = {}
        self.cli_input_7 = {}
        self.cli_expected_output_7 = {}
        self.cli_nonexpected_output_7 = {}
        self.cli_input_8 = {}
        self.cli_expected_output_8 = {}
        self.cli_nonexpected_output_8 = {}
        self.cli_input_9 = {}
        self.cli_expected_output_9 = {}
        self.cli_nonexpected_output_9 = {}
        self.cli_input_10 = {}
        self.cli_expected_output_10 = {}
        self.cli_nonexpected_output_10 = {}
        self.cli_input_11 = {}
        self.cli_expected_output_11 = {}
        self.cli_nonexpected_output_11 = {}
        self.cli_input_12 = {}
        self.cli_expected_output_12 = {}
        self.cli_nonexpected_output_12 = {}
        self.cli_input_13 = {}
        self.cli_expected_output_13 = {}
        self.cli_nonexpected_output_13 = {}
        self.cli_input_14 = {}
        self.cli_expected_output_14 = {}
        self.cli_nonexpected_output_14 = {}
        self.cli_input_15 = {}
        self.cli_expected_output_15 = {}
        self.cli_nonexpected_output_15 = {}
        self.cli_input_16 = {}
        self.cli_expected_output_16 = {}
        self.cli_nonexpected_output_16 = {}
        self.cli_input_17 = {}
        self.cli_expected_output_17 = {}
        self.cli_nonexpected_output_17 = {}
        self.cli_input_18 = {}
        self.cli_expected_output_18 = {}
        self.cli_nonexpected_output_18 = {}
        self.cli_input_19 = {}
        self.cli_expected_output_19 = {}
        self.cli_nonexpected_output_19 = {}
        self.cli_input_20 = {}
        self.cli_expected_output_20 = {}
        self.cli_nonexpected_output_20 = {}
        self.cli_input_21 = {}
        self.cli_expected_output_21 = {}
        self.cli_nonexpected_output_21 = {}
        self.cli_input_22 = {}
        self.cli_expected_output_22 = {}
        self.cli_nonexpected_output_22 = {}
        self.cli_input_23 = {}
        self.cli_expected_output_23 = {}
        self.cli_nonexpected_output_23 = {}
        self.cli_input_24 = {}
        self.cli_expected_output_24 = {}
        self.cli_nonexpected_output_24 = {}
        self.cli_input_25 = {}
        self.cli_expected_output_25 = {}
        self.cli_nonexpected_output_25 = {}
        self.cli_input_26 = {}
        self.cli_expected_output_26 = {}
        self.cli_nonexpected_output_26 = {}
        self.cli_input_27 = {}
        self.cli_expected_output_27 = {}
        self.cli_nonexpected_output_27 = {}
        self.cli_input_28 = {}
        self.cli_expected_output_28 = {}
        self.cli_nonexpected_output_28 = {}
        self.cli_input_29 = {}
        self.cli_expected_output_29 = {}
        self.cli_nonexpected_output_29 = {}
        self.cli_input_30 = {}
        self.cli_expected_output_30 = {}
        self.cli_nonexpected_output_30 = {}
        self.cli_input_31 = {}
        self.cli_expected_output_31 = {}
        self.cli_nonexpected_output_31 = {}
        self.cli_input_32 = {}
        self.cli_expected_output_32 = {}
        self.cli_nonexpected_output_32 = {}


    def id(self):
        return self.name

    def setUp(self):
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.pathToTestOI = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("PATH_TO_TESTOI"))
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.buildDir = dict.get('BUILD_TOKENS')

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))
        coreTestCase.CoreTestCase.setUp(self)

        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0],result[1])

        self.activeController = result[1]

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        exitCliString = "exit";
        #check for COM 3.2
        tmpComRelease = "3"
        tmpComMajorVersion = "1"
        tmpComMajorOK = ('SUCCESS', True)
        tmpComMajorOK = self.lib.checkComponentMajorVersion('com', tmpComRelease, tmpComMajorVersion, [], True)

        if tmpComMajorOK[1] == False:
            exitCliString = '"end" "exit"'

        cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV1=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
        self.myLogger.debug('Delete class "CmwTest=1"')
        result = self.miscLib.execCommand(cmd)
        # Delete class "CmwTest=2"
        cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV2C=2" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
        self.myLogger.debug('Delete class "CmwTest=2"')
        result = self.miscLib.execCommand(cmd)




    def runTest(self):

        self.setTestStep('runTest')
        self.myLogger.info('enter runTest')

        # Create a backup
        result = self.backupSystem()

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-testOI-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        # Get a build token
        for i in range(self.numberOfGetTokenRetries):
            result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            if result[0] == 'SUCCESS':
                break
        self.fail(result[0],result[1])

        result = self.miscLib.execCommand("bash -c 'pushd %s ; make clean ; make errstrtest; popd '" %self.pathToTestOI)
        #self.fail(result[0], result[1]) # this fails for some reason!!!

        result = self.miscLib.execCommand('ls -l %s' %self.pathToTestOI)
        if result[0] != 'SUCCESS':
            self.testSuiteConfig['failedSetUpTestCase'] = 'True'
            self.fail(result[0], result[1])
        elif not '%s' %(self.testOIFile) in result[1]:
            self.testSuiteConfig['failedSetUpTestCase'] = 'True'
            self.fail('ERROR', 'The testOI file was not found in the expected directory. Exiting!\n%s' %result[1])


        result = self.sshLib.sendCommand('mkdir -p %s' %self.pathOnTargetSystem)
        if result[0] != 'SUCCESS':
            self.testSuiteConfig['failedSetUpTestCase'] = 'True'
            self.fail(result[0], result[1])

        result = self.sshLib.remoteCopy('%s%s' %(self.pathToTestOI, self.testOIFile), self.pathOnTargetSystem)
        if result[0] != 'SUCCESS':
            self.testSuiteConfig['failedSetUpTestCase'] = 'True'
            self.fail(result[0], result[1])

        # Release the build token
        result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
        self.fail(result[0],result[1])

        if self.installStressTool:
            self.setTestStep('======== Install the stress tool ========')
            self.comsa_lib.installStressToolOnTarget(self)
            self.setTestStep('======== Start the stress tool ========')

            # Determine the number of processor cores in the node
            res = self.comsa_lib.getNumOfCPUsOnNode(self)
            self.fail(res[0],res[1])
            numOfCpuCores = res[1];
            self.myLogger.debug('Found %s CPU cores' %numOfCpuCores)

            # Determine the total physical RAM in the node
            res = self.comsa_lib.getBytesOfRamOnNode(self)
            self.fail(res[0],res[1])
            totalRamBytes = res[1];
            tenPercentOfTotalRam = int(totalRamBytes) // 10
            self.myLogger.debug('Found total %s bytes of RAM, 10 percent is %s' %(totalRamBytes, tenPercentOfTotalRam))

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, no disk stress
            #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 0, 0)

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
            res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            stressTimeOut = 60
            self.sshLib.setTimeout(stressTimeOut)

        # Restart COM
        self.myLogger.debug('Restart COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        if result[0] != 'SUCCESS':
            self.testSuiteConfig['failedSetUpTestCase'] = 'True'
            self.fail(result[0], result[1])

        cmd = 'chmod +x %s%s' %(self.pathOnTargetSystem, self.testOIFile)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        if result[0] != 'SUCCESS':
            self.testSuiteConfig['failedSetUpTestCase'] = 'True'
            self.fail(result[0], result[1])

        #self.lib.messageBox('do some manual testing')

        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)

        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        for list_index in range (0,len(lists[0])):
            result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
            self.fail(result[0], result[1])


        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.myLogger.info('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info('exit tearDown')


####################################
######## SUPPORT METHODS ###########
####################################
    def backupSystem(self):
        # Skip creating the backup if there is a safe backup created at the beginning of the test suite
        self.myLogger.debug('enter backupSystem')
        backupFound = False
        if self.testSuiteConfig.has_key('restoreBackup'):
            result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
            if result == ('SUCCESS', 'EXIST'):
                self.backupName = self.testSuiteConfig['restoreBackup']
                backupFound = True
            elif result == ('SUCCESS','NOT EXIST'):
                self.testSuiteConfig.__delitem__('restoreBackup')
        if backupFound == False:
            result = self.safLib.isBackup(self.backupName)
            if result[0] != 'SUCCESS':
                self.testSuiteConfig['failedSetUpTestCase'] = 'True'
                self.fail(result[0], result[1])
            elif result != ('SUCCESS','NOT EXIST'):
                result = self.safLib.backupRemove(self.backupName)
                if result[0] != 'SUCCESS':
                    self.testSuiteConfig['failedSetUpTestCase'] = 'True'
                    self.fail(result[0], result[1])
            result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
            if result[0] != 'SUCCESS':
                if self.linuxDistro == self.distroTypes[1]:
                    self.myLogger.warn('Could not create backup on RHEL system. This is not a critical fault')
                else:
                    self.testSuiteConfig['failedSetUpTestCase'] = 'True'
                    self.fail(result[0], result[1])

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
