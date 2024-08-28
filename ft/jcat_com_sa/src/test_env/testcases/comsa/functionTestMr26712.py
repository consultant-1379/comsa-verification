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

    TC-MR26712-001 : Create objects of class that has two parents using CLI and check the objects in IMM
    TC-MR26712-002 - Read in CLI objects created by importing files
    TC-MR26712-003 - Create the objects from TC-MR26712-002 using CLI
    TC-MR26712-004 : Create objects with more complex parent-child relationships
    TC-MR26712-005 : Create objects of class that has two parents, one with splitImmDn 'true', the other 'false'
    TC-MR26712-006 : Negative TC using class with two parents, both with splitImmDn 'true' - only valid for COMSA3.3
    TC-MR26712-007 : Delete an object of class that has two parents and observe the other objectsare still in IMM
    TC-MR26712-008 : Create and delete objects using modified model with more complex parent-child relationships - only valid for COMSA3.3
    TC-MR26712-009 : Reproduce CLI sequence of HR94824 with Reference Attribute which is converted from IMM to 3GPP format
    TC-MR26712-010 : Negative TC using class with two parents, both with splitImmDn 'true' - only valid for COMSA3.4 (updated error message)

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

    Run testcases with the config given in xml.
    It is mandatory to fill out the following parameters in config xml:

    cli_input_<number from 1 to 32>
    cli_expected_output_<number from 1 to 32>
    cli_nonexpected_output_<number from 1 to 32>

    The above lines are defining a CLI session.
    The above lines need to be repeated as the number of CLI sessions.
    Each CLI session must have all the 3 lines(cli input, exp output and nonexp output).
    You can have a maximum of 10 CLI sessions.
    To see an example, please check the xml files which are already checked in to SVN.

    Result:
    CLI output is matching to the expected output and non-expected outputs are not present

    Restore:
    N/A

    Description:

    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-001

    Id:
    "Create objects of class that has two parents using CLI and check the objects in IMM"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-002

    Id:
    "Read in CLI objects created by importing files"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-003

    Id:
    "Create the objects from TC-MR26712-002 using CLI"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-004

    Id:
    "Create objects with more complex parent-child relationships"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-005

    Id:
    "Create objects of class that has two parents, only one has split=true."
   ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-006

    Id:
    "Negative test - create class with 2 parents with SplitImmDn true, check model failure" - only valid for COMSA3.3
   ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-007

    Id:
    "Delete an object of class that has two parents and observe the other objectsare still in IMM"
   ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-008

    Id:
    "Create and delete objects using modified model with more complex parent-child relationships" - only valid for COMSA3.3
   ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-009

    Id:
    "Reproduce CLI sequence of HR94824 with Reference Attribute which is converted from IMM to 3GPP format"
   ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR26712-010

    Id:
    "Negative test - create class with 2 parents with SplitImmDn true, check model failure" - only valid for COMSA3.4 (updated error message)
   ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import os
from java.lang import System

class functiontestMR26712(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig

        # parameters from the config files
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

        self.imm_input_1 = {}
        self.imm_expected_output_1 = {}
        self.imm_nonexpected_output_1 = {}
        self.imm_input_2 = {}
        self.imm_expected_output_2 = {}
        self.imm_nonexpected_output_2 = {}
        self.imm_input_3 = {}
        self.imm_expected_output_3 = {}
        self.imm_nonexpected_output_3 = {}

        self.useExternalModels = {}
        self.pathToModelFiles = {}
        self.momFile = {}
        self.momFile2 = {}
        self.momFile3 = {}
        self.immClassesFile = {}
        self.immClassesFile2 = {}
        self.immClassesFile3 = {}
        self.immClassesFile4 = {}
        self.immClassesFile5 = {}
        self.immClassesFile6 = {}
        self.immObjectsFile = {}
        self.immObjectsFile2 = {}
        self.modelFileType = ''
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.immObjPattern = '[]'

        self.reqComVersion = "R8A06"
        self.reqComRelease = "2"
        self.reqComSaVersion = "R1A01"
        self.reqComSaRelease = "3"
        # Two test cases MR26712 006 and 008 will not work after 3_R5A01
        # This version introduced No Root Class functionality and model checking rules so these invalid models cannot be imported
        # The version values have been initialised high, so all test cases are valid unless the test specifies an obsolete version in the xml file.
        self.obsoleteComSaVersion = "R9A99"
        self.obsoleteComSaRelease = "9"

        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MR26712_MODELFILE_PATH"))
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

        self.logger.info('Exit setUp')

    def runTest(self):
        ComOK = ('SUCCESS', True)
        ComsaOK = ('SUCCESS', True)
        ComsaInvalid = ('SUCCESS', True)
        self.skip_test = False

        self.setTestStep('Check the required versions of COM/COMSA is installed')

        self.logger.info('Check if the required version of COM is installed: %s %s' % (self.reqComRelease, self.reqComVersion))
        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion)
        self.fail(ComOK[0],ComOK[1])

        self.logger.info('Check if the required version of COMSA is installed: %s %s' % (self.reqComSaRelease, self.reqComSaVersion))
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
        self.fail(ComsaOK[0],ComsaOK[1])

        # Two test cases MR26712 006 and 008 will not work after 3_R5A01
        if self.linuxDistro == self.distroTypes[0]: #sles11
            self.logger.info('Check if an obsolete version of COMSA is installed: %s %s' % (self.obsoleteComSaRelease, self.obsoleteComSaVersion))
            ComsaObsolete = self.lib.checkObsoleteComponentVersion('comsa', self.obsoleteComSaRelease, self.obsoleteComSaVersion)
            self.fail(ComsaObsolete[0],ComsaObsolete[1])
        else: # rhel or sles12
            if self.tag == 'TC-MR26712-006' or self.tag == 'TC-MR26712-008':
                ComsaObsolete = ('SUCCESS', False)
            else:
                ComsaObsolete = ('SUCCESS', True)

        if not ComOK[1]:
            self.logger.info('Skipping the MR26712 tests because the COM version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; COM version not compatible')
            self.skip_test = True
        elif not ComsaOK[1]:
            self.logger.info('Skipping the MR26712 tests because the COMSA version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; COMSA version not compatible: %s %s' % (self.reqComSaVersion, self.reqComSaVersion))
            self.skip_test = True
        elif not ComsaObsolete[1]:
            self.logger.info('Skipping the MR26712 tests because the COMSA version is obsolete for this test!')
            self.setAdditionalResultInfo('Test skipped; COMSA version obsolete: %s %s' % (self.obsoleteComSaRelease, self.obsoleteComSaVersion))
            self.skip_test = True
        else:
            self.logger.info('Starting the MR26712 tests because the COM version is compatible!')
            self.logger.info('runTest')
            self.setTestStep('Read configuration via CLI')

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
                #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)
                # with the local disk stress (as above) TC-FT1272-002 and -006 did fail.

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
                res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            if self.useExternalModels == 'yes':

                self.setTestStep('Upload model files to the target')
                cmd = 'mkdir -p %s' %self.modelFilePathOnTarget
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                #Copy actionTest application to target
                self.myLogger.debug('Copy model files to target')
                if self.momFile != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                if self.immClassesFile != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                if self.immObjectsFile != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immObjectsFile), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])

                if self.momFile2 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile2), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                if self.immClassesFile2 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile2), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                if self.immObjectsFile2 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immObjectsFile2), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])

                if self.momFile3 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile3), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                if self.immClassesFile3 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile3), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])

                if self.immClassesFile4 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile4), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])

                if self.immClassesFile5 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile5), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])

                if self.immClassesFile6 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile6), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])

                # Add model file to COM
                if self.momFile != {}:
                    result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                    self.fail(result[0],result[1])
                if self.momFile2 != {}:
                    result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2))
                    self.fail(result[0],result[1])
                if self.momFile3 != {}:
                    result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile3))
                    self.fail(result[0],result[1])

                self.setTestStep('### Loading model files to IMM')

                #Loading model files
                self.myLogger.debug('Loading model files')
                if self.immClassesFile != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])
                if self.immClassesFile2 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile2)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])
                if self.immClassesFile3 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile3)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])
                if self.immClassesFile4 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile4)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])
                if self.immClassesFile5 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile5)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])
                if self.immClassesFile6 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile6)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])

                if self.immObjectsFile != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immObjectsFile)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])
                if self.immObjectsFile2 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immObjectsFile2)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])

                # Restart COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                self.fail(result[0],result[1])

                self.miscLib.waitTime(10)

            self.setTestStep('###Send the CLI command and process the results###')
            #Create the input, the expected output and the non-expected output lists
            lists = self.comsa_lib.load_TC_cli_config(self)
            #Create the input, the expected output and the non-expected output lists
            lists1 = self.comsa_lib.load_TC_imm_config(self)


            #Send the cli commands and process the results element-by-element
            #One element of the list is one cli session.
            for list_index in range(0,len(lists[0])):
                if list_index == 10 and self.tag == 'TC-MR26712-008':
                    result = self.comsa_lib.runImmSession(lists1, 0)
                    self.fail(result[0], result[1])
                result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
                self.fail(result[0], result[1])

            # Check object in IMM
            self.setTestStep('###Check objects in IMM###')

            # Send the IMM commands and process the results element-by-element
            #One element of the list is one imm session.
            for list_index1 in range(0,len(lists1[0])):
                if list_index1 == 0 and self.tag == 'TC-MR26712-008':
                    self.logger.info('continue check')
                else:
                    result = self.comsa_lib.runImmSession(lists1, list_index1)
                    self.fail(result[0], result[1])
            coreTestCase.CoreTestCase.runTest(self)



    def tearDown(self):
        self.setTestStep('tearDown')
        if self.skip_test == False:
            if self.installStressTool:
                self.setTestStep('======== Stopping the stress tool on target ========')
                self.comsa_lib.stopStressToolOnTarget(self)

            if self.useExternalModels == 'yes':

                if self.momFile != {}:
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                    self.fail(result[0],result[1])
                if self.momFile2 != {}:
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2))
                    self.fail(result[0],result[1])
                if self.momFile3 != {}:
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile3))
                    self.fail(result[0],result[1])

                # Restart COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                self.fail(result[0],result[1])

                self.miscLib.waitTime(10)

                self.setTestStep('### Removing model files from IMM')

                #Removing model files
                self.myLogger.debug('Removing the IMM models')
                help = """ In order to clean the IMM from the objects and classes in a dynamic way we need to define a list of patterns
                of the imm_objects which should be searched for with immlist and all the matches will be removed with immcfg -d.
                We have to be careful what we provide and should always test manually before automating, to make sure that we
                do not remove something that should remain!
                """
                if len(eval(self.immObjPattern)) > 0:
                    immObjPatterns = eval(self.immObjPattern)
                    for immObjPattern in immObjPatterns:
                        self.myLogger.debug('Removing the object %s' %immObjPattern)
                        cmd = 'immfind | grep -i %s | xargs immcfg -d' %immObjPattern
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0],result[1])
                        if result[1] != '':
                            self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))

                # Below we remove all the classes imported from the imm_classes model file
                if self.immClassesFile != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile2 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile2)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile3 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile3)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile4 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile4)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile5 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile5)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile6 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile6)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                self.setTestStep('Remove model folder')
                cmd = '\\rm -rf  %s' %self.modelFilePathOnTarget
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])


            coreTestCase.CoreTestCase.tearDown(self)

        #########################
        #### SUPPORT METHODS ####
        #########################

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
