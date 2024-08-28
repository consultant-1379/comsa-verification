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

        Delete testcases:

            TC-FT763-001 - SDP763 FT - Register object instance case: Delete an object that is registered to MAFOI with permission Yes
            TC-FT763-002 - SDP763 FT - Register object instance case: Delete an object that is registered to MAFOI with permission NO

            TC-FT763-003 - SDP763 FT - Register class case: Delete an object that is registered to MAFOI with permission Yes
            TC-FT763-004 - SDP763 FT - Register class case: Delete an object that is registered to MAFOI with permission NO

        Create testcases:

            TC-FT763-005 - SDP763 FT - Register class case: Create an object that is registered to MAFOI with permission Yes, and create a Runtime-NonCached attribute under that object
            TC-FT763-006 - SDP763 FT - Register class case: Create an object that is registered to MAFOI with permission Yes, and create a Cached attribute under that object
            TC-FT763-007 - SDP763 FT - Register class case: Create an object that is registered to MAFOI with permission NO, and create an attribute under that object

        Set testcases:

            TC-FT763-008 - SDP763 FT - Register object instance case: Modify a Runtime-NonCached attribute of an object that is registered to MAFOI with permission Yes
            TC-FT763-009 - SDP763 FT - Register object instance case: Modify a Runtime-NonCached attribute of an object that is registered to MAFOI with permission NO
            TC-FT763-010 - SDP763 FT - Register object instance case: Modify a Cached attribute of an object that is registered to MAFOI with permission Yes
            TC-FT763-011 - SDP763 FT - Register object instance case: Modify a Cached attribute of an object that is registered to MAFOI with permission NO

            TC-FT763-012 - SDP763 FT - Register class case: Modify a Runtime-NonCached attribute of an object that is registered to MAFOI with permission Yes
            TC-FT763-013 - SDP763 FT - Register class case: Modify a Cached attribute of an object that is registered to MAFOI with permission YES
            TC-FT763-014 - SDP763 FT - Register class case: Modify an attribute of an object that is registered to MAFOI with permission NO


        Get testcases:

            TC-FT763-015 - SDP763 FT - Register object instance case: Get an object instance by "show" command. The object is registered to MAFOI
            TC-FT763-016 - SDP763 FT - Register class case: Get an object instance by "show" command. The object is registered to MAFOI

        Actiontest testcases:

            Will be added later

    Priority:
    High

    Requirement:
    -

    Sensitivity:
    Low

    Description:
    Function test of SDP763

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

    *********************************************************************************************************

    Test Steps:

        * Check which SC runs the CLI

        * Copy the model files to target:

            -Create temporary directory on target
            -Copy mp model file to target tempdir
            -Copy imm_class model file to target tempdir
            -Copy imm_object model file to target tempdir

        * Registering the model files:

            -Adding mp.xml file path to target model file list (/home/com/etc/model/model_file_list.cfg)
            -Loading classes to IMM
            -Loading objects to IMM (creating instances)

        * Building mafOI:

            -Delete old defines.h
            -Create new "defines.h" with the right parameters (permission, cached/non-cached)
            -make clean
            -Check if file is removed after make clean
            -make
            -Check if building was successful

        * Register mafOI to COM:

            -Copy mafOI to target under "/opt/com/lib/comp/"
            -Restart COM

        * CLI testing

            -Run CLI sessions
            -Check the output

    *********************************************************************************************************

    TearDown Steps:

        1. Give delete-permission to all objects and classes:

            * Building mafOI:

                -Delete old defines.h
                -Create the teardown version (permission YES to all) of defines.h
                -make clean
                -Check if file is removed after make clean
                -make
                -Check if building was successful

            * Register mafOI to COM:

                -Copy mafOI to target under COM comp lib
                -Restart COM

        2. Delete all objects and classes (instances and definitions from IMM also):

                -In CLI delete the objects used by this TC (e.g. ObjImpTestClass=1)
                -immcfg --delete-class TestClass
                -immcfg --delete-class ObjImpTestClass
                -Remove mp.xml file path from "/home/com/etc/model/model_file_list.cfg"
                -Restart COM
                -Delete mafOI from target under "/opt/com/lib/comp/"
                -Restart COM
                -Remove target tempdir

    *********************************************************************************************************

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

"""
import test_env.fw.coreTestCase as coreTestCase
import time
import os

from java.lang import System

class FTSdp763(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        self.testcase_tag = tag
        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        self.number_of_alarms = 0
        self.number_of_lines = 0
        self.expected_alarm1 = ""
        self.longDn = ""
        #self.pathToConfigFiles = {}

        if self.longDn != 'True':
            self.reqCmwVersion = "R1A01"
        else:
            self.reqCmwVersion = "R10A01"

        self.reqComSaVersion = "R1A01"
        self.reqComVersion = "R1A01"
        self.reqComSaRelease = "3"
        self.reqComRelease = "2"
        self.reqCmwRelease = "1"

        self.modelfile_mp = ""
        self.modelfile_mp2 = ""
        self.modelfile_mp3 = ""
        self.modelfile_imm_classes  = ""
        self.modelfile_imm_classes2  = ""
        self.modelfile_imm_classes3  = ""
        self.modelfile_imm_objects = ''
        self.modelfile_imm_objects2 = ''
        self.modelfile_imm_objects3 = ''

        self.setup_NEGATIVE_CASE_SETTING = ""

        self.setup_RETURN_VALUES = ""
        self.setup_MAF_RETURN_VALUES = ""
        self.setup_REG1 = ""
        self.setup_REG1_PERMISSION = ""
        self.setup_REG2 = ""
        self.setup_REG2_PERMISSION = ""
        self.setup_REG3 = ""
        self.setup_REG3_PERMISSION = ""
        self.setup_REG4 = ""
        self.setup_REG4_PERMISSION = ""
        self.setup_REG5 = ""
        self.setup_REG5_PERMISSION = ""

        self.attribute1 = {}
        self.attribute1_type = {}
        self.attribute1_type_maf = {}
        self.attribute1_value = {}
        self.attribute2 = {}
        self.attribute2_type = {}
        self.attribute2_type_maf = {}
        self.attribute2_value = {}
        self.attribute3 = {}
        self.attribute3_type = {}
        self.attribute3_type_maf = {}
        self.attribute3_value = {}
        self.attribute4 = {}
        self.attribute4_type = {}
        self.attribute4_type_maf = {}
        self.attribute4_value = {}
        self.attribute5 = {}
        self.attribute5_type = {}
        self.attribute5_type_maf = {}
        self.attribute5_value = {}
        self.attribute6 = {}
        self.attribute6_type = {}
        self.attribute6_type_maf = {}
        self.attribute6_value = {}
        self.attribute7 = {}
        self.attribute7_type = {}
        self.attribute7_type_maf = {}
        self.attribute7_value = {}
        self.attribute8 = {}
        self.attribute8_type = {}
        self.attribute8_type_maf = {}
        self.attribute8_value = {}
        self.attribute9 = {}
        self.attribute9_type = {}
        self.attribute9_type_maf = {}
        self.attribute9_value = {}
        self.attribute10 = {}
        self.attribute10_type = {}
        self.attribute10_type_maf = {}
        self.attribute10_value = {}
        self.attribute11 = {}
        self.attribute11_type = {}
        self.attribute11_type_maf = {}
        self.attribute11_value = {}
        self.attribute12 = {}
        self.attribute12_type = {}
        self.attribute12_type_maf = {}
        self.attribute12_value = {}
        self.attribute13 = {}
        self.attribute13_type = {}
        self.attribute13_type_maf = {}
        self.attribute13_value = {}
        self.attribute14 = {}
        self.attribute14_type = {}
        self.attribute14_type_maf = {}
        self.attribute14_value = {}
        self.attribute15 = {}
        self.attribute15_type = {}
        self.attribute15_type_maf = {}
        self.attribute15_value = {}

        self.setup_action_obj = {}
        self.actionDn = {}

        self.teardown_REG1 = ""
        self.teardown_REG1_PERMISSION = ""
        self.teardown_REG2 = ""
        self.teardown_REG2_PERMISSION = ""
        self.teardown_REG3 = ""
        self.teardown_REG3_PERMISSION = ""
        self.teardown_REG4 = ""
        self.teardown_REG4_PERMISSION = ""
        self.teardown_REG5 = ""
        self.teardown_REG5_PERMISSION = ""

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

        self.expected_init_log_1 = {}
        self.expected_init_log_2 = {}
        self.expected_init_log_3 = {}
        self.expected_init_log_4 = {}
        self.expected_init_log_5 = {}
        self.expected_init_log_6 = {}
        self.expected_init_log_7 = {}
        self.expected_init_log_8 = {}
        self.expected_init_log_9 = {}
        self.expected_init_log_10 = {}
        self.expected_init_log_11 = {}
        self.expected_init_log_12 = {}
        self.expected_init_log_13 = {}
        self.expected_init_log_14 = {}
        self.expected_init_log_15 = {}
        self.expected_init_log_16 = {}
        self.expected_init_log_17 = {}
        self.expected_init_log_18 = {}
        self.expected_init_log_19 = {}
        self.expected_init_log_20 = {}

        self.expected_test_log_1 = {}
        self.expected_test_log_2 = {}
        self.expected_test_log_3 = {}
        self.expected_test_log_4 = {}
        self.expected_test_log_5 = {}
        self.expected_test_log_6 = {}
        self.expected_test_log_7 = {}
        self.expected_test_log_8 = {}
        self.expected_test_log_9 = {}
        self.expected_test_log_10 = {}
        self.expected_test_log_11 = {}
        self.expected_test_log_12 = {}
        self.expected_test_log_13 = {}
        self.expected_test_log_14 = {}
        self.expected_test_log_15 = {}
        self.expected_test_log_16 = {}
        self.expected_test_log_17 = {}
        self.expected_test_log_18 = {}
        self.expected_test_log_19 = {}
        self.expected_test_log_20 = {}
        self.expected_test_log_21 = {}
        self.expected_test_log_22 = {}
        self.expected_test_log_23 = {}
        self.expected_test_log_24 = {}
        self.expected_test_log_25 = {}
        self.expected_test_log_26 = {}
        self.expected_test_log_27 = {}
        self.expected_test_log_28 = {}
        self.expected_test_log_29 = {}
        self.expected_test_log_30 = {}
        self.expected_test_log_31 = {}
        self.expected_test_log_32 = {}
        self.expected_test_log_33 = {}
        self.expected_test_log_34 = {}
        self.expected_test_log_35 = {}
        self.expected_test_log_36 = {}
        self.expected_test_log_37 = {}
        self.expected_test_log_38 = {}
        self.expected_test_log_39 = {}
        self.expected_test_log_40 = {}
        self.expected_test_log_41 = {}
        self.expected_test_log_42 = {}
        self.expected_test_log_43 = {}
        self.expected_test_log_44 = {}
        self.expected_test_log_45 = {}
        self.expected_test_log_46 = {}
        self.expected_test_log_47 = {}
        self.expected_test_log_48 = {}
        self.expected_test_log_49 = {}
        self.expected_test_log_50 = {}


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        if self.testcase_tag == 'TC-FT872-002' or self.testcase_tag == 'TC-MR35347-011':
            self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MODEL_FILE_PATH"))
        elif self.testcase_tag == 'TC-MR24146-004':
            self.modelfile_path = dict.get("MR24146_MODELFILE_PATH")
        else:
            self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT763_MODELFILE_PATH"))

        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")

        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = dict.get('REPLACE_COM_SCRIPT_VALGRIND')
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.PERSISTENT_STORAGE_API = dict.get("PERSISTENT_STORAGE_API")

        self.reqComSaReleaseV4 = "3"
        self.reqComSaVersionV4 = "R8A01"
        self.ComSa_v4 = ('SUCCESS', False)
        self.ComSa_v4 = self.lib.checkComponentVersion('comsa', self.reqComSaReleaseV4, self.reqComSaVersionV4)
        if self.ComSa_v4[1]:
            self.mafOI_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('TEST_COMPONENT_763_V4_PATH'))
        else:
            self.mafOI_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('TEST_COMPONENT_763_PATH'))
        self.buildDir = dict.get('BUILD_TOKENS')

        self.mafOI_file = 'test-maf-oi.so'
        self.defines_headerfile = 'defines2.h'

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.logger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')

        self.setTestStep('Check the required versions of ComSA, Com and CMW is installed')
        self.doTearDown = False
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
        self.fail(ComsaOK[0],ComsaOK[1])
        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion )
        self.fail(ComOK[0],ComOK[1])
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
        self.fail(CmwOK[0],CmwOK[1])

        if ComsaOK[1] and ComOK[1] and CmwOK[1]:
            self.doTearDown = True

            ###############################################################################
            ################ Prepare steps for functiontest of SDP763 #####################
            ###############################################################################

            self.setTestStep('### Check which SC runs the CLI')
            #Creates the login params according to which controller runs the CLI

            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0],result[1])
            self.activeController = result[1]

            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

            self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

            self.setTestStep('### Prepare-steps for functiontest of SDP763')

            # Variables needed for the build token management
            dirName = System.getProperty("logdir")
            user = os.environ['USER']
            self.tokenPattern = 'buildToken-%s' %user
            self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
            self.numberOfGetTokenRetries = 5


            ###############################################################################################

            #Paths and files on target:
            PERSISTENT_STORAGE_API_CONFIG="%s/config" %self.PERSISTENT_STORAGE_API
            cmd = "cat %s" %PERSISTENT_STORAGE_API_CONFIG
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            if 'No such file or directory' in result[1]:
                self.target_model_path = '/home/com/etc/model/'
            else:
                self.target_model_path = '%s/com-apr9010443/etc/model/' %result[1]
            self.target_model_file = 'model_file_list.cfg'
            self.tempdir_on_target = '/home/SDP763_tempdir/'
            self.ntf_log_file = 'ntf_log'
            self.target_com_compdir = '/opt/com/lib/comp/'

            modelfile_imm_classes = self.modelfile_imm_classes
            modelfile_imm_classes2 = self.modelfile_imm_classes2
            modelfile_imm_classes3 = self.modelfile_imm_classes3

            self.comRestartWaitTime = 10

            ###############################################################################################
            ###############################################################################################

            self.setTestStep('### Copy the model files to target')
            #Create temporary directory on target
            cmd = 'mkdir %s' %self.tempdir_on_target
            self.myLogger.debug('Create temporary directory on target: %s' %cmd)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])

            self.myLogger.debug('Copy the model files to the target')
            self.copyFileToTarget(self.modelfile_path, self.modelfile_mp, self.tempdir_on_target)

            if self.modelfile_mp2 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_mp2, self.tempdir_on_target)

            if self.modelfile_mp3 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_mp3, self.tempdir_on_target)

            self.copyFileToTarget(self.modelfile_path, modelfile_imm_classes, self.tempdir_on_target)

            if modelfile_imm_classes2 != "":
                self.copyFileToTarget(self.modelfile_path, modelfile_imm_classes2, self.tempdir_on_target)

            if modelfile_imm_classes3 != "":
                self.copyFileToTarget(self.modelfile_path, modelfile_imm_classes3, self.tempdir_on_target)

            if self.modelfile_imm_objects != '':
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects, self.tempdir_on_target)
            if self.modelfile_imm_objects2 != '':
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects2, self.tempdir_on_target)
            if self.modelfile_imm_objects3 != '':
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects3, self.tempdir_on_target)

            ###############################################################################################

            if self.longDn == 'True':
                cmd = 'immlist -a longDnsAllowed opensafImm=opensafImm,safApp=safImmService'
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                if result[1] != 'longDnsAllowed=1':
                    self.setTestStep('###Set attribute longDnsAllowed=1###')
                    cmd = 'immcfg --admin-owner-clear opensafImm=opensafImm,safApp=safImmService'
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])

                    cmd = 'immcfg -m -a longDnsAllowed=1 opensafImm=opensafImm,safApp=safImmService'
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])


                    # Restart COM
                    self.myLogger.debug('Restart COM')
                    result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                    self.fail(result[0],result[1])

                    self.miscLib.waitTime(10)

            self.setTestStep('### Registering the model files')
            #Adding the path to target model file list
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s/%s' %(self.tempdir_on_target, self.modelfile_mp))
            self.fail(result[0],result[1])
            if self.modelfile_mp2 != "":
                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s/%s' %(self.tempdir_on_target, self.modelfile_mp2))
                self.fail(result[0],result[1])
            if self.modelfile_mp3 != "":
                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s/%s' %(self.tempdir_on_target, self.modelfile_mp3))
                self.fail(result[0],result[1])

            self.myLogger.debug('Loading classes to IMM')
            cmd = 'immcfg -f %s%s' %(self.tempdir_on_target, modelfile_imm_classes)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if result[1] != '':
                self.fail('ERROR', result[1])
            if modelfile_imm_classes2 != "":
                cmd = 'immcfg -f %s%s' %(self.tempdir_on_target, modelfile_imm_classes2)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            if modelfile_imm_classes3 != "":
                cmd = 'immcfg -f %s%s' %(self.tempdir_on_target, modelfile_imm_classes3)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

            if self.modelfile_imm_objects != '':
                self.myLogger.debug('Loading objects to IMM (creating instances)')
                cmd = 'immcfg -f %s%s' %(self.tempdir_on_target, self.modelfile_imm_objects)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            if self.modelfile_imm_objects2 != '':
                self.myLogger.debug('Loading objects2 to IMM (creating instances)')
                cmd = 'immcfg -f %s%s' %(self.tempdir_on_target, self.modelfile_imm_objects2)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            if self.modelfile_imm_objects3 != '':
                self.myLogger.debug('Loading objects2 to IMM (creating instances)')
                cmd = 'immcfg -f %s%s' %(self.tempdir_on_target, self.modelfile_imm_objects3)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

            if self.testcase_tag == 'TC-FT872-002' or self.testcase_tag == 'TC-MR24146-004'  or self.testcase_tag == 'TC-MR35347-011':
                id = ''
                if self.longDn == 'True':
                    id = 'This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_1'
                else:
                    id = '1'
                cmd = 'immcfg -c Sdp617ActiontestRoot sdp617ActiontestRootId=%s' %id
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
                cmd = 'immcfg -c ActionTest actionTestId=1,sdp617ActiontestRootId=%s' %id
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            else:
                if self.setup_action_obj == 'YES':
                    if self.actionDn == {}:
                        self.fail('ERROR', 'The DN of the action has to be defined in the xml file of the test case.')
                    self.myLogger.debug('Creating object for actiontest')
                    cmd = 'immcfg -c ActionTest %s' %self.actionDn
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])

            ###############################################################################################

            self.setTestStep('### Building mafOI')
            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0],result[1])

            #Delete old defines.h
            cmd = '\\rm -f %s%s' %(self.mafOI_path, self.defines_headerfile)
            self.myLogger.debug('Delete old %s by: %s' %(self.defines_headerfile, cmd))
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0],result[1])

            #Create new defines.h with the right parameters
            cmd = 'echo "%s" > %s%s' %(self.create_headerfile_text_for_setup(), self.mafOI_path, self.defines_headerfile)
            self.myLogger.debug('Create new defines.h with the right parameters: %s' %cmd)
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0],result[1])

            #Do make clean before building mafOI
            cmd = 'cd %s;make clean' %self.mafOI_path
            self.myLogger.debug('Do make clean before building mafOI by: %s' %cmd)
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0],result[1])
            cmd = 'ls %s | grep -c %s' %(self.mafOI_path, self.mafOI_file)
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0],result[1])
            if result[1].split()[0] != '0':
                self.fail('ERROR', 'File is not removed after make clean!')

            #Build mafOI
            cmd = 'cd %s;make' %self.mafOI_path
            self.myLogger.debug('Building mafOI by: %s' %cmd)
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0],result[1])

            cmd = 'ls %s | grep -c %s' %(self.mafOI_path, self.mafOI_file)
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0],result[1])
            if result[1].split()[0] != '1':
                self.fail('ERROR', 'Building was unsuccessful!')

            ###############################################################################################

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

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
                res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            self.setTestStep('### Register mafOI to COM')
            self.myLogger.debug('Copy mafOI to target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.mafOI_path, self.mafOI_file, self.target_com_compdir)
            self.miscLib.waitTime(3)

            self.myLogger.debug('Change the mafOI permissions: %s%s' %(self.target_com_compdir, self.mafOI_file))
            cmd = "chmod 640 %s%s; chown root:com-core %s%s" %(self.target_com_compdir, self.mafOI_file, self.target_com_compdir, self.mafOI_file)
            result = self.sshLib.sendCommand(cmd);
            self.fail(result[0],result[1])

            # Release the build token
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            self.fail(result[0],result[1])

            #Resetting the timer for log-checking (Start new log-checking from here)
            self.myLogger.debug('Resetting the timer for log-checking')
            cmd = 'date +\%s'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            startTime = int(result[1])
            #startTime = time.time()

            #Restart COM
            self.myLogger.debug('Restart COM')
            result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartWaitTime)
            self.fail(result[0],result[1])

            self.setTestStep('### Check logs after COM restart: Look for the expected texts in the syslog')
            logtext_list = self.create_expected_init_log_list()

            for logtext_index in range (0,len(logtext_list)):
                self.myLogger.debug('Check if syslog has: %s' %logtext_list[logtext_index])
                if logtext_list[logtext_index][0] == "[" and logtext_list[logtext_index][-1:] == "]":
                    searchPattern = eval(logtext_list[logtext_index])
                else:
                    searchPattern = [logtext_list[logtext_index]]
                result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, startTime, self.testConfig)
                self.fail(result[0],result[1])
                self.myLogger.debug('Found text in syslog at: %s' %result[1])

            #Resetting the timer for log-checking (Start new log-checking from here)
            self.myLogger.debug('Resetting the timer for log-checking')
            cmd = 'date +\%s'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            startTime = int(result[1])
            #startTime = time.time()

            ###############################################################################
            ############################### CLI testing ###################################
            ###############################################################################

            #self.lib.messageBox('do some manual testing')
            #self.lib.messageBox('do some manual testing')

            self.setTestStep('### CLI testing')
            #Create the input, the expected output and the non-expected output lists
            lists = self.comsa_lib.load_TC_cli_config(self)

            #Send the cli commands and process the results element-by-element
            #One element of the list is one cli session.
            for list_index in range (0,len(lists[0])):
                self.setTestStep('### Running CLI test step %d' %list_index)
                result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
                self.fail(result[0], result[1])

            ###############################################################################################
            #self.miscLib.waitTime(20)
            self.setTestStep('### Check logs after CLI test: Look for the expected texts in the syslog')

            if self.installStressTool:
                self.myLogger.debug('Stress is enabled so wait for one minute before checking syslog')
                self.miscLib.waitTime(60)

            logtext_list = self.create_expected_test_log_list()
            for logtext_index in range (0,len(logtext_list)):
                self.myLogger.debug('Check if syslog has: %s' %logtext_list[logtext_index])
                if logtext_list[logtext_index][0] == "[" and logtext_list[logtext_index][-1:] == "]":
                    searchPattern = eval(logtext_list[logtext_index])
                else:
                    searchPattern = [logtext_list[logtext_index]]
                result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, startTime, self.testConfig)
                self.fail(result[0],result[1])
                self.myLogger.debug('Found text in syslog at: %s' %result[1])
            #self.lib.messageBox('Stop ###############################################################################################################################################')
            if self.testcase_tag == 'TC-FT1120-001' or self.testcase_tag == 'TC-MR29443-001':
                expected_line_number = -1
                if int(self.number_of_alarms) == 1:
                    expected_line_number = int(self.number_of_lines)

                self.myLogger.debug('Read notifications')
                cmd = 'ntfread | tail -n %d > %s%s' % (expected_line_number, self.tempdir_on_target, self.ntf_log_file)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])

                self.myLogger.debug('check if %s%s file created' %(self.tempdir_on_target, self.ntf_log_file))
                cmd = 'ls %s%s' %(self.tempdir_on_target, self.ntf_log_file)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.myLogger.debug('expected: (%s%s) current: (%s)' %(self.tempdir_on_target, self.ntf_log_file, result[1]))
                if result[1] != '%s%s' %(self.tempdir_on_target, self.ntf_log_file):
                    self.fail('ERROR','Alarm did not come, no log file created by ntfread')


                cmd = 'cat %s%s' %(self.tempdir_on_target, self.ntf_log_file)
                self.myLogger.debug('Reading the log of ntfread by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.logger.info('%s' %result[1])
                self.fail(result[0],result[1])
                alarm_string = str(result[1])
                # print out the multi line alarm
                self.myLogger.debug('original alarm_string : (%s)' %alarm_string)
                # replacing all the '\n' characters to ' '
                alarm_string=alarm_string.replace('\n',' ')
                # print the alarm in 1 single line
                #if "nohup" in alarm_string:
                #    alarm_string = alarm_string[22:]
                self.myLogger.debug('alarm_string in 1 line: (%s)' %alarm_string)
                self.myLogger.debug('the expected alarm    : (%s)' %self.expected_alarm1)

                # Check the number of alarms
                self.myLogger.debug('counting the alarms in the NTF log file')
                cmd = 'wc -l %s%s | sed \'s/ .*//g\'' %(self.tempdir_on_target, self.ntf_log_file)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.miscLib.waitTime(20)
                self.fail(result[0],result[1])
                self.logger.info('Found %s lines in alarm file' %result[1])
                if expected_line_number == int(result[1]):
                    self.myLogger.debug('Number of expected alarms are matching to the number of received')
                    result = ('SUCCESS','Number of expected alarms are matching to the number of received')
                else:
                    result = ('ERROR','Number of expected alarms (%d) are NOT matching to the number of received (%d)' %(expected_line_number, int(result[1])))
                self.fail(result[0],result[1])

                if self.expected_alarm1 == alarm_string:
                    self.logger.info('Alarm matching')
                    result = ('SUCCESS','Alarm matching to the expected one')
                else:
                    self.logger.info('Alarm NOT matching to the expected one! len(expected)=%d len(actual)=%d' %(len(self.expected_alarm1),len(alarm_string)))
                    self.logger.info('Alarm NOT matching to the expected one! expected (%s) actual (%s)' %(self.expected_alarm1[:10],alarm_string[:10]))
                    self.logger.info('Alarm NOT matching to the expected one! expected (%s) actual (%s)' %(self.expected_alarm1[-10:],alarm_string[-10:]))
                    for iStr in xrange(len(self.expected_alarm1)):
                        if (self.expected_alarm1[iStr] != alarm_string[iStr]):
                            self.logger.info('Alarm NOT matching to the expected one! (%d) expected (%c) actual (%c)' %(iStr, self.expected_alarm1[iStr],alarm_string[iStr]));
                    result = ('ERROR','Alarm NOT matching to the expected one!')
                self.fail(result[0],result[1])

        else:
                self.logger.info('Skipped SDP763 tests because of COMSA/COM/CMW version not compatible!')
                self.setAdditionalResultInfo('Test skipped; version not compatible')

        coreTestCase.CoreTestCase.runTest(self)

    def tearDown(self):
        self.setTestStep('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        if self.doTearDown:
            ###############################################################################
            ################################### Cleanup ###################################
            ###############################################################################

            #Delete mafOI from COM comp dir
            cmd = '\\rm -f %s%s' %(self.target_com_compdir, self.mafOI_file)
            self.myLogger.debug('tearDown: Delete %s from %s by: %s' %(self.target_com_compdir, self.mafOI_file, cmd))
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0],result[1])

            #Delete old defines.h from Clearcase path
            cmd = '\\rm -f %s%s' %(self.mafOI_path, self.defines_headerfile)
            self.myLogger.debug('tearDown: Delete old %s by: %s' %(self.defines_headerfile, cmd))
            self.miscLib.execCommand(cmd)

            #Create the teardown version (permission YES to all) of defines.h
            cmd = 'echo "%s" > %s%s' %(self.create_headerfile_text_for_teardown(), self.mafOI_path, self.defines_headerfile)
            self.myLogger.debug('tearDown: Create the teardown version (permission YES to all) of defines.h: %s' %cmd)
            self.miscLib.execCommand(cmd)

            #Do make clean before building mafOI
            cmd = 'cd %s;make clean' %self.mafOI_path
            self.myLogger.debug('tearDown: Do make clean before building mafOI by: %s' %cmd)
            self.miscLib.execCommand(cmd)

            #Build mafOI
            cmd = 'cd %s;make' %self.mafOI_path
            self.myLogger.debug('tearDown: Building mafOI by: %s' %cmd)
            self.miscLib.execCommand(cmd)

            #Copy mafOI to target under COM comp dir
            self.myLogger.debug('tearDown: Copy mafOI to target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.mafOI_path, self.mafOI_file, self.target_com_compdir)

            # Do make clean at the end
            cmd = 'cd %s;make clean' %self.mafOI_path
            self.myLogger.debug('tearDown: Do make clean at the end')
            self.miscLib.execCommand(cmd)

            #Delete defines.h
            cmd = '\\rm -f %s%s' %(self.mafOI_path, self.defines_headerfile)
            self.myLogger.debug('Delete old %s by: %s' %(self.defines_headerfile, cmd))
            self.miscLib.execCommand(cmd)

            # Release the build token
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            self.fail(result[0],result[1])

            #Restart COM
            self.myLogger.debug('tearDown: Restart COM')
            self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartWaitTime)

            #Check if the active controller has changed after COM restart
            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0],result[1])
            self.activeController = result[1]

            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

            self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

            exitCliString = "exit";
            #check for COM 3.2
            tmpComRelease = "3"
            tmpComMajorVersion = "1"
            tmpComMajorOK = ('SUCCESS', True)
            tmpComMajorOK = self.lib.checkComponentMajorVersion('com', tmpComRelease, tmpComMajorVersion, [], True)

            if tmpComMajorOK[1] == False:
                exitCliString = '"end" "exit"'

            # Delete all objects by CLI
            cmd = '%s "configure" "ManagedElement=1" "no ObjImpTestClass=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "ObjImpTestClass=1" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)

            cmd = '%s "configure" "ManagedElement=1" "no ObjImpTestClassTwo=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "ObjImpTestClass=1" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)

            # Delete all objects by CLI
            cmd = '%s "configure" "ManagedElement=1" "no ObjImpEmptyClass=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "ObjImpEmptyClass=1" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)

            # Delete all objects by CLI
            cmd = '%s "configure" "ManagedElement=1" "no ObjImpComplexClass=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "ObjImpComplexClass=1" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)

            # Delete all objects by CLI
            cmd = '%s "configure" "ManagedElement=1,TOPROOT1=1,TestClass1=1,TestClass2=1,TOPROOT12=1,TestClass12=1,TestClass22=1" "no TOPROOT13=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "TOPROOT13=1" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)
                        # Delete all objects by CLI
            cmd = '%s "configure" "ManagedElement=1,TOPROOT1=1,TestClass1=1,TestClass2=1" "no TOPROOT12=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "TOPROOT12=1" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)
                        # Delete all objects by CLI
            cmd = '%s "configure" "ManagedElement=1" "no TOPROOT1=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "TOPROOT1=1" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)

            # Delete all objects of MR20275
            cmd = '%s "configure" "ManagedElement=1" "no TestStructAttr=one" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('tearDown: Delete object "no TestStructAttr=one" by CLI')
            result = self.comsa_lib.executeCliSession(cmd)
            self.miscLib.waitTime(3)

            #Delete objects
            cmd = 'immcfg -d ActionTest=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d ObjImpTestClass=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d ObjImpTestClassTwo=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d ObjImpEmptyClass=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d testClassTwoId=1,testClassOneId=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d testClassOneId=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d ObjImpComplexClass=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d mAiD=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d oBjimPTEsTclAsSiD=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg -d oBJimpCOMPLEXclassiD=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            # delete object ObjectMr20275Id=1 of MR 20275
            cmd = 'immcfg -d ObjectMr20275Id=1'
            self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            if self.testcase_tag == 'TC-FT872-002' or self.testcase_tag == 'TC-MR24146-004' or self.testcase_tag == 'TC-MR35347-011':
                id = ''
                if self.longDn == "True":
                    id = 'This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_1'
                else:
                    id = '1'
                cmd = 'immcfg -d actionTestId=1,sdp617ActiontestRootId=%s' %id
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
                cmd = 'immcfg -d sdp617ActiontestRootId=%s' %id
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

            #Delete classes
            cmd = 'immcfg --delete-class ActionTest'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestStruct'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class ObjImpTestClass'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class ObjImpTestClassTwo'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class ObjImpEmptyClass'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClassOne'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClassTwo'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class ObjImpComplexClass'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            cmd = 'immcfg --delete-class TOPROOT1'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClass1'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClass2'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            cmd = 'immcfg --delete-class TOPROOT12'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClass12'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClass22'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            cmd = 'immcfg --delete-class TOPROOT13'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClass13'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'immcfg --delete-class TestClass23'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            # delete class ObjectMr20275 of Mr20275
            cmd = 'immcfg --delete-class ObjectMr20275'
            self.myLogger.debug('tearDown: Delete test class: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            #Remove mp.xml file path from "/home/com/etc/model/model_file_list.cfg"
            if self.modelfile_mp3 != "":
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s/%s' %(self.tempdir_on_target, self.modelfile_mp3))
                self.fail(result[0],result[1])
            if self.modelfile_mp2 != "":
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s/%s' %(self.tempdir_on_target, self.modelfile_mp2))
                self.fail(result[0],result[1])
            result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s/%s' %(self.tempdir_on_target, self.modelfile_mp))
            self.fail(result[0],result[1])


            #Remove mp.xml file path from "/home/com/etc/model/model_file_list.cfg"
            #cmd = 'sed -in \'/%s/d\' %s%s' %(self.modelfile_mp, self.target_model_path, self.target_model_file)
            #self.myLogger.debug('tearDown: Remove "%s" file path from "%s%s" by: %s' %(self.modelfile_mp, self.target_model_path, self.target_model_file, cmd))
            #result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

            #Delete mafOI from COM comp dir
            cmd = '\\rm -f %s%s' %(self.target_com_compdir, self.mafOI_file)
            self.myLogger.debug('tearDown: Delete %s from %s by: %s' %(self.target_com_compdir, self.mafOI_file, cmd))
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.miscLib.waitTime(3)

            #Restart COM
            self.myLogger.debug('tearDown: Restart COM')
            self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartWaitTime)

            #Remove temporary directory from target
            cmd = '\\rm -rf %s' %self.tempdir_on_target
            self.myLogger.debug('tearDown: Remove temporary directory from target by: %s' %cmd)
            self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

        coreTestCase.CoreTestCase.tearDown(self) #NEED TO RUN THIS!
        #########################
        #### SUPPORT METHODS ####
        #########################

    def copyFileToTarget(self, source, filename, destination):
            self.myLogger.debug('copyFileToTarget: source=%s filename=%s destination=%s' %(source, filename, destination))
            result = self.sshLib.remoteCopy('%s%s' % (source, filename), destination, timeout = 60)
            self.fail(result[0],result[1])
            self.miscLib.waitTime(3)

            cmd = "chmod 640 %s%s; chown root:com-core %s%s" %(destination, filename, destination, filename)
            result = self.sshLib.sendCommand(cmd);
            self.fail(result[0],result[1])

    def create_headerfile_text_for_setup(self):

        text_for_headerfile = ''
        if self.longDn == "True":
            text_for_headerfile += '#define TEST_FOR_LONG_DN\n'
        text_for_headerfile += self.setup_NEGATIVE_CASE_SETTING + '\n'
        if self.ComSa_v4[1]:
            text_for_headerfile += self.setup_MAF_RETURN_VALUES + '\n'
        else:
            text_for_headerfile += self.setup_RETURN_VALUES + '\n'
        text_for_headerfile += self.setup_REG1 + '\n'
        text_for_headerfile += self.setup_REG1_PERMISSION + '\n'
        text_for_headerfile += self.setup_REG2 + '\n'
        text_for_headerfile += self.setup_REG2_PERMISSION + '\n'
        text_for_headerfile += self.setup_REG3 + '\n'
        text_for_headerfile += self.setup_REG3_PERMISSION + '\n'
        text_for_headerfile += self.setup_REG4 + '\n'
        text_for_headerfile += self.setup_REG4_PERMISSION + '\n'
        text_for_headerfile += self.setup_REG5 + '\n'
        text_for_headerfile += self.setup_REG5_PERMISSION + '\n'

        if self.attribute1 != {} and self.attribute1_type != {} and self.attribute1_value != {} and self.attribute1_type_maf != {}:
            text_for_headerfile += self.attribute1 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute1_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute1_type + '\n'
            text_for_headerfile += self.attribute1_value + '\n'
        if self.attribute2 != {} and self.attribute2_type != {} and self.attribute2_value != {} and self.attribute2_type_maf != {}:
            text_for_headerfile += self.attribute2 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute2_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute2_type + '\n'
            text_for_headerfile += self.attribute2_value + '\n'
        if self.attribute3 != {} and self.attribute3_type != {} and self.attribute3_value != {} and self.attribute3_type_maf != {}:
            text_for_headerfile += self.attribute3 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute3_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute3_type + '\n'
            text_for_headerfile += self.attribute3_value + '\n'
        if self.attribute4 != {} and self.attribute4_type != {} and self.attribute4_value != {} and self.attribute4_type_maf != {}:
            text_for_headerfile += self.attribute4 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute4_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute4_type + '\n'
            text_for_headerfile += self.attribute4_value + '\n'
        if self.attribute5 != {} and self.attribute5_type != {} and self.attribute5_value != {} and self.attribute5_type_maf != {}:
            text_for_headerfile += self.attribute5 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute5_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute5_type + '\n'
            text_for_headerfile += self.attribute5_value + '\n'
        if self.attribute6 != {} and self.attribute6_type != {} and self.attribute6_value != {} and self.attribute6_type_maf != {}:
            text_for_headerfile += self.attribute6 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute6_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute6_type + '\n'
            text_for_headerfile += self.attribute6_value + '\n'
        if self.attribute7 != {} and self.attribute7_type != {} and self.attribute7_value != {} and self.attribute7_type_maf != {}:
            text_for_headerfile += self.attribute7 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute7_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute7_type + '\n'
            text_for_headerfile += self.attribute7_value + '\n'
        if self.attribute8 != {} and self.attribute8_type != {} and self.attribute8_value != {} and self.attribute8_type_maf != {}:
            text_for_headerfile += self.attribute8 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute8_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute8_type + '\n'
            text_for_headerfile += self.attribute8_value + '\n'
        if self.attribute9 != {} and self.attribute9_type != {} and self.attribute9_value != {} and self.attribute9_type_maf != {}:
            text_for_headerfile += self.attribute9 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute9_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute9_type + '\n'
            text_for_headerfile += self.attribute9_value + '\n'
        if self.attribute10 != {} and self.attribute10_type != {} and self.attribute10_value != {} and self.attribute10_type_maf != {}:
            text_for_headerfile += self.attribute10 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute10_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute10_type + '\n'
            text_for_headerfile += self.attribute10_value + '\n'
        if self.attribute11 != {} and self.attribute11_type != {} and self.attribute11_value != {} and self.attribute11_type_maf != {}:
            text_for_headerfile += self.attribute11 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute11_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute11_type + '\n'
            text_for_headerfile += self.attribute11_value + '\n'
        if self.attribute12 != {} and self.attribute12_type != {} and self.attribute12_value != {} and self.attribute12_type_maf != {}:
            text_for_headerfile += self.attribute12 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute12_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute12_type + '\n'
            text_for_headerfile += self.attribute12_value + '\n'
        if self.attribute13 != {} and self.attribute13_type != {} and self.attribute13_value != {} and self.attribute13_type_maf != {}:
            text_for_headerfile += self.attribute13 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute13_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute13_type + '\n'
            text_for_headerfile += self.attribute13_value + '\n'
        if self.attribute14 != {} and self.attribute14_type != {} and self.attribute14_value != {} and self.attribute14_type_maf != {}:
            text_for_headerfile += self.attribute14 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute14_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute14_type + '\n'
            text_for_headerfile += self.attribute14_value + '\n'
        if self.attribute15 != {} and self.attribute15_type != {} and self.attribute15_value != {} and self.attribute15_type_maf != {}:
            text_for_headerfile += self.attribute15 + '\n'
            if self.ComSa_v4[1]:
                text_for_headerfile += self.attribute15_type_maf + '\n'
            else:
                text_for_headerfile += self.attribute15_type + '\n'
            text_for_headerfile += self.attribute15_value + '\n'

        self.myLogger.debug('create_headerfile_text_for_setup:\n%s' %text_for_headerfile)
        return text_for_headerfile

    def create_headerfile_text_for_teardown(self):

        text_for_headerfile = ''
        text_for_headerfile += self.teardown_REG1 + '\n'
        text_for_headerfile += self.teardown_REG1_PERMISSION + '\n'
        text_for_headerfile += self.teardown_REG2 + '\n'
        text_for_headerfile += self.teardown_REG2_PERMISSION + '\n'
        text_for_headerfile += self.teardown_REG3 + '\n'
        text_for_headerfile += self.teardown_REG3_PERMISSION + '\n'
        text_for_headerfile += self.teardown_REG4 + '\n'
        text_for_headerfile += self.teardown_REG4_PERMISSION + '\n'
        text_for_headerfile += self.teardown_REG5 + '\n'
        text_for_headerfile += self.teardown_REG5_PERMISSION + '\n'

        self.myLogger.debug('create_headerfile_text_for_teardown:\n%s' %text_for_headerfile)
        return text_for_headerfile


    def create_expected_init_log_list(self):
        '''
        This method loads the expected log texts from the data received from the xml,
         and creates a list of the expected log texts.
        1. Checking the data received from the xml
        2. Create list
        3. return list

        The method returns 1 lists:   return_log_list
        '''
        self.myLogger.debug('enter create_expected_init_log_list function')
        return_log_list = []
        #Only append to list if the expected log text is present
        if self.expected_init_log_1 != {}:
            return_log_list.append(self.expected_init_log_1)
        if self.expected_init_log_2 != {}:
            return_log_list.append(self.expected_init_log_2)
        if self.expected_init_log_3 != {}:
            return_log_list.append(self.expected_init_log_3)
        if self.expected_init_log_4 != {}:
            return_log_list.append(self.expected_init_log_4)
        if self.expected_init_log_5 != {}:
            return_log_list.append(self.expected_init_log_5)
        if self.expected_init_log_6 != {}:
            return_log_list.append(self.expected_init_log_6)
        if self.expected_init_log_7 != {}:
            return_log_list.append(self.expected_init_log_7)
        if self.expected_init_log_8 != {}:
            return_log_list.append(self.expected_init_log_8)
        if self.expected_init_log_9 != {}:
            return_log_list.append(self.expected_init_log_9)
        if self.expected_init_log_10 != {}:
            return_log_list.append(self.expected_init_log_10)
        if self.expected_init_log_11 != {}:
            return_log_list.append(self.expected_init_log_11)
        if self.expected_init_log_12 != {}:
            return_log_list.append(self.expected_init_log_12)
        if self.expected_init_log_13 != {}:
            return_log_list.append(self.expected_init_log_13)
        if self.expected_init_log_14 != {}:
            return_log_list.append(self.expected_init_log_14)
        if self.expected_init_log_15 != {}:
            return_log_list.append(self.expected_init_log_15)
        if self.expected_init_log_16 != {}:
            return_log_list.append(self.expected_init_log_16)
        if self.expected_init_log_17 != {}:
            return_log_list.append(self.expected_init_log_17)
        if self.expected_init_log_18 != {}:
            return_log_list.append(self.expected_init_log_18)
        if self.expected_init_log_19 != {}:
            return_log_list.append(self.expected_init_log_19)
        if self.expected_init_log_20 != {}:
            return_log_list.append(self.expected_init_log_20)

        self.myLogger.debug('leave create_expected_init_log_list function')
        return return_log_list

    def create_expected_test_log_list(self):
        '''
        This method loads the expected log texts from the data received from the xml,
         and creates a list of the expected log texts.
        1. Checking the data received from the xml
        2. Create list
        3. return list

        The method returns 1 lists:   return_log_list
        '''
        self.myLogger.debug('enter create_expected_test_log_list function')
        return_log_list = []
        #Only append to list if the expected log text is present
        if self.expected_test_log_1 != {}:
            return_log_list.append(self.expected_test_log_1)
        if self.expected_test_log_2 != {}:
            return_log_list.append(self.expected_test_log_2)
        if self.expected_test_log_3 != {}:
            return_log_list.append(self.expected_test_log_3)
        if self.expected_test_log_4 != {}:
            return_log_list.append(self.expected_test_log_4)
        if self.expected_test_log_5 != {}:
            return_log_list.append(self.expected_test_log_5)
        if self.expected_test_log_6 != {}:
            return_log_list.append(self.expected_test_log_6)
        if self.expected_test_log_7 != {}:
            return_log_list.append(self.expected_test_log_7)
        if self.expected_test_log_8 != {}:
            return_log_list.append(self.expected_test_log_8)
        if self.expected_test_log_9 != {}:
            return_log_list.append(self.expected_test_log_9)
        if self.expected_test_log_10 != {}:
            return_log_list.append(self.expected_test_log_10)
        if self.expected_test_log_11 != {}:
            return_log_list.append(self.expected_test_log_11)
        if self.expected_test_log_12 != {}:
            return_log_list.append(self.expected_test_log_12)
        if self.expected_test_log_13 != {}:
            return_log_list.append(self.expected_test_log_13)
        if self.expected_test_log_14 != {}:
            return_log_list.append(self.expected_test_log_14)
        if self.expected_test_log_15 != {}:
            return_log_list.append(self.expected_test_log_15)
        if self.expected_test_log_16 != {}:
            return_log_list.append(self.expected_test_log_16)
        if self.expected_test_log_17 != {}:
            return_log_list.append(self.expected_test_log_17)
        if self.expected_test_log_18 != {}:
            return_log_list.append(self.expected_test_log_18)
        if self.expected_test_log_19 != {}:
            return_log_list.append(self.expected_test_log_19)
        if self.expected_test_log_20 != {}:
            return_log_list.append(self.expected_test_log_20)
        if self.expected_test_log_21 != {}:
            return_log_list.append(self.expected_test_log_21)
        if self.expected_test_log_22 != {}:
            return_log_list.append(self.expected_test_log_22)
        if self.expected_test_log_23 != {}:
            return_log_list.append(self.expected_test_log_23)
        if self.expected_test_log_24 != {}:
            return_log_list.append(self.expected_test_log_24)
        if self.expected_test_log_25 != {}:
            return_log_list.append(self.expected_test_log_25)
        if self.expected_test_log_26 != {}:
            return_log_list.append(self.expected_test_log_26)
        if self.expected_test_log_27 != {}:
            return_log_list.append(self.expected_test_log_27)
        if self.expected_test_log_28 != {}:
            return_log_list.append(self.expected_test_log_28)
        if self.expected_test_log_29 != {}:
            return_log_list.append(self.expected_test_log_29)
        if self.expected_test_log_30 != {}:
            return_log_list.append(self.expected_test_log_30)
        if self.expected_test_log_31 != {}:
            return_log_list.append(self.expected_test_log_31)
        if self.expected_test_log_32 != {}:
            return_log_list.append(self.expected_test_log_32)
        if self.expected_test_log_33 != {}:
            return_log_list.append(self.expected_test_log_33)
        if self.expected_test_log_34 != {}:
            return_log_list.append(self.expected_test_log_34)
        if self.expected_test_log_35 != {}:
            return_log_list.append(self.expected_test_log_35)
        if self.expected_test_log_36 != {}:
            return_log_list.append(self.expected_test_log_36)
        if self.expected_test_log_37 != {}:
            return_log_list.append(self.expected_test_log_37)
        if self.expected_test_log_38 != {}:
            return_log_list.append(self.expected_test_log_38)
        if self.expected_test_log_39 != {}:
            return_log_list.append(self.expected_test_log_39)
        if self.expected_test_log_40 != {}:
            return_log_list.append(self.expected_test_log_40)
        if self.expected_test_log_41 != {}:
            return_log_list.append(self.expected_test_log_41)
        if self.expected_test_log_42 != {}:
            return_log_list.append(self.expected_test_log_42)
        if self.expected_test_log_43 != {}:
            return_log_list.append(self.expected_test_log_43)
        if self.expected_test_log_44 != {}:
            return_log_list.append(self.expected_test_log_44)
        if self.expected_test_log_45 != {}:
            return_log_list.append(self.expected_test_log_45)
        if self.expected_test_log_46 != {}:
            return_log_list.append(self.expected_test_log_46)
        if self.expected_test_log_47 != {}:
            return_log_list.append(self.expected_test_log_47)
        if self.expected_test_log_48 != {}:
            return_log_list.append(self.expected_test_log_48)
        if self.expected_test_log_49 != {}:
            return_log_list.append(self.expected_test_log_49)
        if self.expected_test_log_50 != {}:
            return_log_list.append(self.expected_test_log_50)

        self.myLogger.debug('leave create_expected_test_log_list function')
        return return_log_list


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
