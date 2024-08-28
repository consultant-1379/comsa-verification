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

    TC-CDT-001 - Complex Datatypes - Creating a struct
    TC-CDT-002 - Complex Datatypes - Update the attribute value
    TC-CDT-003 - Complex Datatypes - Creating another struct
    TC-CDT-004 - Complex Datatypes - Update an attribute and discarding the change
    TC-CDT-005 - Complex Datatypes - Deleting a struct
    TC-CDT-006 - Complex Datatypes - Recreating the same struct

    Priority:
    High

    Requirement:
    -

    Sensitivity:
    Low

    Description:
    Complex Datatypes testcases

    Restrictions:
    -

    Test tools:
    -

    Help:
    The test script is driven by the following parameters:

    Test script:
    N/A

    Configuration:
    2SC+nPL

    Action:
    Run testcases with the config given in xml

    Result:

        CLI output are matching to the expected

    Restore:
    N/A

    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CDT-001

    Id:
    "Complex Datatypes - Creating a struct"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CDT-002

    Id:
    "Complex Datatypes - Update the attribute value"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CDT-003

    Id:
    "Complex Datatypes - Creating another struct"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CDT-004

    Id:
    "Complex Datatypes - Update an attribute and discarding the change"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CDT-005

    Id:
    "Complex Datatypes - Deleting a struct"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CDT-006

    Id:
    "Complex Datatypes - Recreating the same struct"
    ==================================
"""
import test_env.fw.coreTestCase as coreTestCase
import time
import os

from java.lang import System

class CompDatatypes(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.compDatatypes_tempdir = '/home/compDatatypes/'
        self.modelfile_imm = 'imm.xml'
        self.modelfile_mp = 'mp.xml'
        self.runSetUp = False
        self.runTearDown = False
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

        self.reqComSaRelease = "3"
        self.reqComSaMajorVersion = "1"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("EXAMPLE_MODELFILE_PATH"))
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        if self.runSetUp == 'True':
            self.runSetUp = True
        if self.runTearDown == 'True':
            self.runTearDown = True

        self.importModelsOnce=False
        if self.testSuiteConfig.has_key('importModelsOnce'):
            self.importModelsOnce = eval(self.testSuiteConfig['importModelsOnce']['importModelsOnce'])

        self.logger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')

        ###############################################################################
        ################ Prepare steps for Complex Datatypes CLI testing ##################
        ###############################################################################

        ComsaMajorOK = ('SUCCESS', True)
        self.skip_test = False

        ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion)
        self.fail(ComsaMajorOK[0],ComsaMajorOK[1])

        if ComsaMajorOK[1] == True:

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

            self.setTestStep('### Find active controller')

            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0],result[1])
            self.activeController = result[1]

            self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                        self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

            if self.runSetUp == False and self.importModelsOnce == True:
                self.myLogger.info('Skip importing model files')
            else:
                #Create temporary directory on target
                cmd = 'mkdir -p %s' %self.compDatatypes_tempdir
                self.myLogger.debug('Create temporary directory on target: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                #Wait for "mkdir" command respond
                if self.installStressTool:
                    self.miscLib.waitTime(20)
                self.fail(result[0],result[1])

                self.setTestStep('### Copy the model files to target')
                self.myLogger.debug('Copy model files to target')
                self.sshLib.remoteCopy('%s%s' %(self.modelfile_path,self.modelfile_imm), self.compDatatypes_tempdir, timeout = 60)
                self.fail(result[0],result[1])
                self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_mp), self.compDatatypes_tempdir, timeout = 60)
                self.fail(result[0],result[1])

                self.setTestStep('### Loading model files to IMM')
                #Loading model files

                #self.lib.messageBox('do some manual testingg')

                self.myLogger.debug('Loading model files')
                cmd = 'immcfg -f %s%s' %(self.compDatatypes_tempdir, self.modelfile_imm)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.compDatatypes_tempdir, self.modelfile_mp))
                self.fail(result[0],result[1])

                # Restart COM
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                self.fail(result[0],result[1])

            ###############################################################################
            ############################### CLI testing ###################################
            ###############################################################################

            #self.lib.messageBox('do some manual testingg')
            #self.lib.messageBox('do some manual testingg')

            self.setTestStep('### CLI testing')
            startTime = time.time()
            #Create the input, the expected output and the non-expected output lists
            lists = self.comsa_lib.load_TC_cli_config(self)

            #Send the cli commands and process the results element-by-element
            #One element of the list is one cli session.
            for list_index in range (0,len(lists[0])):
                result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
                self.fail(result[0], result[1])
        else:
            self.logger.info('Skipped tests because of COMSA version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True

        coreTestCase.CoreTestCase.runTest(self)

    def tearDown(self):
        self.setTestStep('tearDown')
        ###############################################################################
        ################################### Cleanup ###################################
        ###############################################################################
        if self.skip_test == False:

            exitCliString = "exit";
            #check for COM 3.2
            tmpComRelease = "3"
            tmpComMajorVersion = "1"
            tmpComMajorOK = ('SUCCESS', True)
            tmpComMajorOK = self.lib.checkComponentMajorVersion('com', tmpComRelease, tmpComMajorVersion, [], True)

            if tmpComMajorOK[1] == False:
                exitCliString = '"end" "exit"'

            # Delete class "CmwTest=1"
            cmd = '%s "configure" "ManagedElement=1" "no CmwTest=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete class "CmwTest=1"')
            result = self.comsa_lib.executeCliSession(cmd)        # Delete class "CmwTest=2"
            # Delete class "CmwTest=2"
            cmd = '%s "configure" "ManagedElement=1" "no CmwTest=2" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete class "CmwTest=2"')
            result = self.comsa_lib.executeCliSession(cmd)        # Delete class "CmwTest=2"

            if self.runTearDown == False and self.importModelsOnce == True:
                self.myLogger.info('Skip removing model files')
            else:
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.compDatatypes_tempdir, self.modelfile_mp))
                self.fail(result[0],result[1])

                # Restart COM
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                self.fail(result[0],result[1])

                cmd = """grep \"<class\" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.compDatatypes_tempdir, self.modelfile_imm)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))

                #Remove temporary directory from target
                cmd = '\\rm -rf %s' %self.compDatatypes_tempdir
                self.myLogger.debug('Remove temporary directory from target by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            cmd = '%s "show ManagedElement=1, SystemFunctions=1, SysM=1" "exit"' %self.cli_active_controller_login_params
            self.myLogger.debug('Show "SysM=1"')
            result = self.miscLib.execCommand(cmd)

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)

        #########################
        #### SUPPORT METHODS ####
        #########################


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
