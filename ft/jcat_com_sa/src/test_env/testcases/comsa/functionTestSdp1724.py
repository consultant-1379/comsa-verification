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

    ==================================
    TEST CASE SPECIFICATION:

    Tag:

    Id:
    ""
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import re
import os

from java.lang import System

class FTSdp1724(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        self.testcase_tag = tag

        self.modelfile_mp1 = ""
        self.modelfile_mp2 = ""
        self.modelfile_mp3 = ""
        self.modelfile_mp4 = ""
        self.modelfile_mp5 = ""

        self.modelfile_imm_classes1  = ""
        self.modelfile_imm_classes2  = ""
        self.modelfile_imm_classes3  = ""
        self.modelfile_imm_classes4  = ""
        self.modelfile_imm_classes5  = ""

        self.modelfile_imm_objects1 = ""
        self.modelfile_imm_objects2 = ""
        self.modelfile_imm_objects3 = ""
        self.modelfile_imm_objects4 = ""
        self.modelfile_imm_objects5 = ""

        self.pattern_1 = "" # Pattern shall come from the xml file to remove the loaded object(s).
        self.pattern_2 = ""
        self.pattern_3 = ""
        self.pattern_4 = ""
        self.pattern_5 = ""

        self.unexpectedPattern1 = ""
        self.unexpectedPattern2 = ""
        self.unexpectedPattern3 = ""
        self.unexpectedPattern4 = ""
        self.unexpectedPattern5 = ""
        self.unexpectedPattern6 = ""
        self.unexpectedPattern7 = ""
        self.unexpectedPattern8 = ""
        self.unexpectedPattern9 = ""
        self.unexpectedPattern10 = ""
        self.unexpectedPattern11 = ""
        self.unexpectedPattern12 = ""
        self.unexpectedPattern13 = ""
        self.unexpectedPattern14 = ""
        self.unexpectedPattern15 = ""
        self.unexpectedPattern16 = ""
        self.unexpectedPattern17 = ""
        self.unexpectedPattern18 = ""
        self.unexpectedPattern19 = ""
        self.unexpectedPattern20 = ""
        self.unexpectedPattern21 = ""
        self.unexpectedPattern22 = ""
        self.unexpectedPattern23 = ""
        self.unexpectedPattern24 = ""
        self.unexpectedPattern25 = ""
        self.unexpectedPattern26 = ""
        self.unexpectedPattern27 = ""
        self.unexpectedPattern28 = ""
        self.unexpectedPattern29 = ""
        self.unexpectedPattern30 = ""
        self.unexpectedPattern31 = ""
        self.unexpectedPattern32 = ""
        self.unexpectedPattern33 = ""
        self.unexpectedPattern34 = ""
        self.unexpectedPattern35 = ""
        self.unexpectedPattern36 = ""
        self.unexpectedPattern37 = ""
        self.unexpectedPattern38 = ""
        self.unexpectedPattern39 = ""
        self.unexpectedPattern40 = ""
        self.unexpectedPattern41 = ""
        self.unexpectedPattern42 = ""
        self.unexpectedPattern43 = ""
        self.unexpectedPattern44 = ""
        self.unexpectedPattern45 = ""
        self.unexpectedPattern46 = ""
        self.unexpectedPattern47 = ""
        self.unexpectedPattern48 = ""
        self.unexpectedPattern49 = ""
        self.unexpectedPattern50 = ""

        self.testCons1Regexp1 = ""
        self.testCons1Regexp2 = ""
        self.testCons1Regexp3 = ""
        self.testCons1Regexp4 = ""
        self.testCons1Regexp5 = ""
        self.testCons2Regexp1 = ""
        self.testCons2Regexp2 = ""
        self.testCons2Regexp3 = ""
        self.testCons2Regexp4 = ""
        self.testCons2Regexp5 = ""
        self.testCons3Regexp1 = ""
        self.testCons3Regexp2 = ""
        self.testCons3Regexp3 = ""
        self.testCons3Regexp4 = ""
        self.testCons3Regexp5 = ""


        self.testOI_name = "imm-applier"

        self.searchPatterns_subscription_1 = "" # com: testConsumer*: maf_start(): failed to addSubscription (-1)
        self.searchPatterns_subscription_2 = ''
        self.unexpected_searchPatterns_subscription_1 =''
        self.unexpected_searchPatterns_subscription_2 =''

        self.searchPatterns1 = "" # This is the patterns used by the function getEventTimestampFromComLog
        self.searchPatterns2 = ""
        self.searchPatterns3 = ""
        self.searchPatterns4 = ""
        self.searchPatterns5 = ""
        self.searchPatterns6 = ""
        self.searchPatterns7 = ""
        self.searchPatterns8 = ""
        self.searchPatterns9 = ""
        self.searchPatterns10 = ""
        self.searchPatterns11= ""
        self.searchPatterns12 = ""
        self.searchPatterns13 = ""
        self.searchPatterns14 = ""
        self.searchPatterns15 = ""
        self.searchPatterns16 = ""
        self.searchPatterns17 = ""
        self.searchPatterns18 = ""
        self.searchPatterns19 = ""
        self.searchPatterns20 = ""
        self.searchPatterns21 = ""
        self.searchPatterns22 = ""
        self.searchPatterns23 = ""
        self.searchPatterns24 = ""
        self.searchPatterns25 = ""
        self.searchPatterns26 = ""
        self.searchPatterns27 = ""
        self.searchPatterns28 = ""
        self.searchPatterns29 = ""
        self.searchPatterns30 = ""
        self.searchPatterns31 = ""
        self.searchPatterns32 = ""
        self.searchPatterns33 = ""
        self.searchPatterns34 = ""
        self.searchPatterns35 = ""
        self.searchPatterns36 = ""
        self.searchPatterns37 = ""
        self.searchPatterns38 = ""
        self.searchPatterns39 = ""
        self.searchPatterns40 = ""
        self.searchPatterns41 = ""
        self.searchPatterns42 = ""
        self.searchPatterns43 = ""
        self.searchPatterns44 = ""
        self.searchPatterns45 = ""
        self.searchPatterns46 = ""
        self.searchPatterns47 = ""
        self.searchPatterns48 = ""
        self.searchPatterns49 = ""
        self.searchPatterns50 = ""

        self.searchPatterns1Matches = "1" # this variable makes it possible to define the number of expected matches on a search pattern. By default this is one.
        self.searchPatterns2Matches = "1"
        self.searchPatterns3Matches = "1"
        self.searchPatterns4Matches = "1"
        self.searchPatterns5Matches = "1"
        self.searchPatterns6Matches = "1"
        self.searchPatterns7Matches = "1"
        self.searchPatterns8Matches = "1"
        self.searchPatterns9Matches = "1"
        self.searchPatterns10Matches = "1"
        self.searchPatterns11Matches= "1"
        self.searchPatterns12Matches = "1"
        self.searchPatterns13Matches = "1"
        self.searchPatterns14Matches = "1"
        self.searchPatterns15Matches = "1"
        self.searchPatterns16Matches = "1"
        self.searchPatterns17Matches = "1"
        self.searchPatterns18Matches = "1"
        self.searchPatterns19Matches = "1"
        self.searchPatterns20Matches = "1"
        self.searchPatterns21Matches = "1"
        self.searchPatterns22Matches = "1"
        self.searchPatterns23Matches = "1"
        self.searchPatterns24Matches = "1"
        self.searchPatterns25Matches = "1"
        self.searchPatterns26Matches = "1"
        self.searchPatterns27Matches = "1"
        self.searchPatterns28Matches = "1"
        self.searchPatterns29Matches = "1"
        self.searchPatterns30Matches = "1"
        self.searchPatterns31Matches = "1"
        self.searchPatterns32Matches = "1"
        self.searchPatterns33Matches = "1"
        self.searchPatterns34Matches = "1"
        self.searchPatterns35Matches = "1"
        self.searchPatterns36Matches = "1"
        self.searchPatterns37Matches = "1"
        self.searchPatterns38Matches = "1"
        self.searchPatterns39Matches = "1"
        self.searchPatterns40Matches = "1"
        self.searchPatterns41Matches = "1"
        self.searchPatterns42Matches = "1"
        self.searchPatterns43Matches = "1"
        self.searchPatterns44Matches = "1"
        self.searchPatterns45Matches = "1"
        self.searchPatterns46Matches = "1"
        self.searchPatterns47Matches = "1"
        self.searchPatterns48Matches = "1"
        self.searchPatterns49Matches = "1"
        self.searchPatterns50Matches = "1"

        self.testOIarg1 = ""
        self.testOIarg2 = ""
        self.testOIarg3 = ""
        self.testOIarg4 = ""
        self.testOIarg5= ""
        self.testOIarg6 = ""
        self.testOIarg7 = ""
        self.testOIarg8 = ""
        self.testOIarg9 = ""
        self.testOIarg10 = ""
        self.testOIarg11 = ""
        self.testOIarg12 = ""
        self.testOIarg13 = ""
        self.testOIarg14 = ""
        self.testOIarg15 = ""
        self.testOIarg16 = ""
        self.testOIarg17 = ""
        self.testOIarg18 = ""
        self.testOIarg19 = ""
        self.testOIarg20 = ""

        self.testOIarg_tearDown1 = ""
        self.testOIarg_tearDown2 = ""
        self.testOIarg_tearDown3 = ""
        self.testOIarg_tearDown4 = ""
        self.testOIarg_tearDown5 = ""
        self.testOIarg_tearDown6 = ""
        self.testOIarg_tearDown7 = ""
        self.testOIarg_tearDown8 = ""
        self.testOIarg_tearDown9 = ""
        self.testOIarg_tearDown10 = ""

        self.test_consumer_1 = ""
        self.test_consumer_2 = ""
        self.test_consumer_3 = ""

        self.disable_class_notify_1 = ""
        self.disable_objectOrAttr_1 = ""
        self.disable_class_notify_2 = ""
        self.disable_objectOrAttr_2 = ""
        self.disable_class_notify_3 = ""
        self.disable_objectOrAttr_3 = ""
        self.disable_class_notify_4 = ""
        self.disable_objectOrAttr_4 = ""
        self.disable_class_notify_5 = ""
        self.disable_objectOrAttr_5 = ""
        self.disable_class_notify_6 = ""
        self.disable_objectOrAttr_6 = ""
        self.disable_class_notify_7 = ""
        self.disable_objectOrAttr_7 = ""
        self.disable_class_notify_8 = ""
        self.disable_objectOrAttr_8 = ""
        self.disable_class_notify_9 = ""
        self.disable_objectOrAttr_9 = ""
        self.disable_class_notify_10 = ""
        self.disable_objectOrAttr_10 = ""
        self.disable_class_notify_11 = ""
        self.disable_objectOrAttr_11 = ""
        self.disable_class_notify_12 = ""
        self.disable_objectOrAttr_12 = ""
        self.disable_class_notify_13 = ""
        self.disable_objectOrAttr_13 = ""
        self.disable_class_notify_14 = ""
        self.disable_objectOrAttr_14 = ""
        self.disable_class_notify_15 = ""
        self.disable_objectOrAttr_15 = ""
        self.disable_class_notify_16 = ""
        self.disable_objectOrAttr_16 = ""
        self.disable_class_notify_17 = ""
        self.disable_objectOrAttr_17 = ""
        self.disable_class_notify_18 = ""
        self.disable_objectOrAttr_18 = ""
        self.disable_class_notify_19 = ""
        self.disable_objectOrAttr_19 = ""
        self.disable_class_notify_20 = ""
        self.disable_objectOrAttr_20 = ""
        self.disable_class_notify_21 = ""
        self.disable_objectOrAttr_21 = ""
        self.disable_class_notify_22 = ""
        self.disable_objectOrAttr_22 = ""
        self.disable_class_notify_23 = ""
        self.disable_objectOrAttr_23 = ""
        self.disable_class_notify_24 = ""
        self.disable_objectOrAttr_24 = ""
        self.disable_class_notify_25 = ""
        self.disable_objectOrAttr_25 = ""
        self.disable_class_notify_26 = ""
        self.disable_objectOrAttr_26 = ""
        self.disable_class_notify_27 = ""
        self.disable_objectOrAttr_27 = ""
        self.disable_class_notify_28 = ""
        self.disable_objectOrAttr_28 = ""
        self.disable_class_notify_29 = ""
        self.disable_objectOrAttr_29 = ""
        self.disable_class_notify_30 = ""
        self.disable_objectOrAttr_30 = ""

        self.enable_class_notify_1 = ""
        self.enable_objectOrAttr_1 = ""
        self.enable_class_notify_2 = ""
        self.enable_objectOrAttr_2 = ""
        self.enable_class_notify_3 = ""
        self.enable_objectOrAttr_3 = ""
        self.enable_class_notify_4 = ""
        self.enable_objectOrAttr_4 = ""
        self.enable_class_notify_5 = ""
        self.enable_objectOrAttr_5 = ""
        self.enable_class_notify_6 = ""
        self.enable_objectOrAttr_6 = ""
        self.enable_class_notify_7 = ""
        self.enable_objectOrAttr_7 = ""
        self.enable_class_notify_8 = ""
        self.enable_objectOrAttr_8 = ""
        self.enable_class_notify_9 = ""
        self.enable_objectOrAttr_9 = ""
        self.enable_class_notify_10 = ""
        self.enable_objectOrAttr_10 = ""
        self.enable_class_notify_11 = ""
        self.enable_objectOrAttr_11 = ""
        self.enable_class_notify_12 = ""
        self.enable_objectOrAttr_12 = ""
        self.enable_class_notify_13 = ""
        self.enable_objectOrAttr_13 = ""
        self.enable_class_notify_14 = ""
        self.enable_objectOrAttr_14 = ""
        self.enable_class_notify_15 = ""
        self.enable_objectOrAttr_15 = ""
        self.enable_class_notify_16 = ""
        self.enable_objectOrAttr_16 = ""
        self.enable_class_notify_17 = ""
        self.enable_objectOrAttr_17 = ""
        self.enable_class_notify_18 = ""
        self.enable_objectOrAttr_18 = ""
        self.enable_class_notify_19 = ""
        self.enable_objectOrAttr_19 = ""
        self.enable_class_notify_20 = ""
        self.enable_objectOrAttr_20 = ""
        self.enable_class_notify_21 = ""
        self.enable_objectOrAttr_21 = ""
        self.enable_class_notify_22 = ""
        self.enable_objectOrAttr_22 = ""
        self.enable_class_notify_23 = ""
        self.enable_objectOrAttr_23 = ""
        self.enable_class_notify_24 = ""
        self.enable_objectOrAttr_24 = ""
        self.enable_class_notify_25 = ""
        self.enable_objectOrAttr_25 = ""
        self.enable_class_notify_26 = ""
        self.enable_objectOrAttr_26 = ""
        self.enable_class_notify_27 = ""
        self.enable_objectOrAttr_27 = ""
        self.enable_class_notify_28 = ""
        self.enable_objectOrAttr_28 = ""
        self.enable_class_notify_29 = ""
        self.enable_objectOrAttr_29 = ""
        self.enable_class_notify_30 = ""
        self.enable_objectOrAttr_30 = ""

        # Use the CLI to initiate OM transactions that trigger sending CM-notifications.
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
        self.imm_input_4 = {}
        self.imm_expected_output_4 = {}
        self.imm_nonexpected_output_4 = {}
        self.imm_input_5 = {}
        self.imm_expected_output_5 = {}
        self.imm_nonexpected_output_5 = {}
        self.imm_input_6 = {}
        self.imm_expected_output_6 = {}
        self.imm_nonexpected_output_6 = {}
        self.imm_input_7 = {}
        self.imm_expected_output_7 = {}
        self.imm_nonexpected_output_7 = {}
        self.imm_input_8 = {}
        self.imm_expected_output_8 = {}
        self.imm_nonexpected_output_8 = {}
        self.imm_input_9 = {}
        self.imm_expected_output_9 = {}
        self.imm_nonexpected_output_9 = {}
        self.imm_input_10 = {}
        self.imm_expected_output_10 = {}
        self.imm_nonexpected_output_10 = {}
        self.imm_input_11 = {}
        self.imm_expected_output_11 = {}
        self.imm_nonexpected_output_11 = {}
        self.imm_input_12 = {}
        self.imm_expected_output_12 = {}
        self.imm_nonexpected_output_12 = {}
        self.imm_input_13 = {}
        self.imm_expected_output_13 = {}
        self.imm_nonexpected_output_13 = {}
        self.imm_input_14 = {}
        self.imm_expected_output_14 = {}
        self.imm_nonexpected_output_14 = {}
        self.imm_input_15 = {}
        self.imm_expected_output_15 = {}
        self.imm_nonexpected_output_15 = {}
        self.imm_input_16 = {}
        self.imm_expected_output_16 = {}
        self.imm_nonexpected_output_16 = {}
        self.imm_input_17 = {}
        self.imm_expected_output_17 = {}
        self.imm_nonexpected_output_17 = {}
        self.imm_input_18 = {}
        self.imm_expected_output_18 = {}
        self.imm_nonexpected_output_18 = {}
        self.imm_input_19 = {}
        self.imm_expected_output_19 = {}
        self.imm_nonexpected_output_19 = {}
        self.imm_input_20 = {}
        self.imm_expected_output_20 = {}
        self.imm_nonexpected_output_20 = {}

        self.ntfsendMsg1 = ""
        self.doSwitchover = "False"

        self.reqComSaVersion = "R3A10"
        self.reqComSaMajorVersion = "3"
        self.reqComVersion = "R6A15"
        self.reqCmwVersion = "R6A12"
        self.reqComSaRelease = "3"
        self.reqComRelease = "2"
        self.reqCmwRelease = "1"

        """
        The intention with the variable below is to make possible running SDP1724 test cases
        as part of the stability test suite. That means that there should be no COM process restart
        during the test case execution. This is achieved by adding the parts skipped from this test
        case to the stability test case's preparation steps.
        """
        self.runAsPartOfStabilitySuite = 'False'


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_MODELFILE_PATH"))
        self.testOI_path_in_fileSystem = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_TESTOI_PATH"))
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.target_com_compdir = dict.get('COM_COMP_DIR')

        if self.testcase_tag == 'TC-MR24146-005' :
            self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MR24146_MODELFILE_PATH"))
        else:
            self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_MODELFILE_PATH"))

        self.reqComSaReleaseV4 = "3"
        self.reqComSaVersionV4 = "R8A05"
        self.ComSa_v4 = ('SUCCESS', False)
        self.ComSa_v4 = self.lib.checkComponentVersion('comsa', self.reqComSaReleaseV4, self.reqComSaVersionV4)
        if self.ComSa_v4[1]:
            self.path_to_testConsumer = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_TESTCONSUMER_V4_PATH"))
        else:
            self.path_to_testConsumer = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_TESTCONSUMER_PATH"))

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])
        """
        Stress Tool option
        """
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.runAsPartOfStabilitySuite = eval(self.runAsPartOfStabilitySuite)

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')

        self.setTestStep('Check the required versions of ComSA, Com and CMW is installed')
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
        self.fail(ComsaOK[0],ComsaOK[1])
        ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion)
        self.fail(ComsaMajorOK[0],ComsaMajorOK[1])
        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion )
        self.fail(ComOK[0],ComOK[1])
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
        self.fail(CmwOK[0],CmwOK[1])
        self.testSkipped = False

        if ComsaOK[1] and ComsaMajorOK[1] and ComOK[1] and CmwOK[1]:

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
                result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 0, 0)
                self.sshLib.setTimeout(stressTimeOut)

            self.setTestStep('### Prepare-steps for function test of SDP1724')

            self.noOfScs = len(self.testConfig['controllers'])
            # Paths and files on target
            self.tempdir_on_target = '/home/SDP1724_tempdir/'
            self.path_to_cfgFile = '/home/'

            self.resultedstartTime = 0

            self.findActiveAndStandbyController()

            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                        self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

            self.setTestStep('Create temporary directory on target')

            if self.runAsPartOfStabilitySuite == True:
                self.myLogger.info('Large parts of the setUp skipped. Is is presumed that these parts are done inside the stability test case preparations phase.')
                self.resultedstartTime = self.getCurrentUnixTime()
                self.myLogger.debug('Current Linux Time :%s'%self.resultedstartTime)
            else:
                cmd = 'mkdir %s' %self.tempdir_on_target
                self.myLogger.debug('Create temporary directory on target: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])

                self.copyModelFilesToTarget()
                self.registeringModelFiles()
                self.loadingClassesToImm()
                self.loadingObjectsToImm()
                self.copyTestCompToActiveSC()

                if self.doSwitchover == 'True' and self.noOfScs > 1:
                    self.copyTestCompToStandbySC()

                self.populateTestConsumerConfigFiles()
                #self.testOIrunTimeCachedAttributes()
                self.copyTestOiToTarget()
                self.ToggleNotifyingFlag()

                self.resultedstartTime = self.getCurrentUnixTime()
                self.myLogger.debug('Current Linux Time :%s'%self.resultedstartTime)

                """
                Restart COM
                """
                if self.doSwitchover == 'True'  and self.noOfScs > 1:
                    for controller in self.testConfig['controllers']:
                        result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                        self.fail(result[0], result[1])
                else:
                    self.restartCom()

            self.getComPid()
            self.cliTesting()
            self.immTesting()
            self.testOiTesting()
            self.ntfSendSessions()

            self.addSubscriptionForTestConsumersExpectedLogs()
            self.addSubscriptionForTestConsumersUnExpectedLogs()

            """ This lists below will contain all issues found during verification of expected and unexpected patterns
             The purpose is to NOT fail the test cases at the first problem found, but run through all the patterns and gather all problems"""
            self.expectedLogsIssues = []
            self.unexpectedLogsFound = []

            self.expectedLogs()
            self.unexpectedLogs()

            if len(self.expectedLogsIssues) != 0:
                self.setAdditionalResultInfo('The following issues were found during verification of expected log entries: %s' %str(self.expectedLogsIssues))
            if len(self.unexpectedLogsFound) != 0:
                self.setAdditionalResultInfo('Log entries matched the following unexpected search patterns : %s' %str(self.unexpectedLogsFound))

            if len(self.expectedLogsIssues) != 0 or len(self.unexpectedLogsFound) != 0:
                self.fail('ERROR', 'Expected logs not found or unexpected logs found.')

            if self.doSwitchover == 'True' and self.noOfScs > 1:

                self.switchOver()
                self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                            self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)
                self.resultedstartTime = self.getCurrentUnixTime()
                self.myLogger.debug('Current Linux Time after the Switchover:%s'%self.resultedstartTime)

                self.getComPid()
                self.cliTesting()
                self.immTesting()
                self.testOiTesting()
                self.ntfSendSessions()

                self.expectedLogs()
                self.unexpectedLogs()


        else:
            self.logger.info('Skipped SDP1724 tests because of COMSA/COM/CMW version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.testSkipped = True


        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')

        if self.testSkipped == False:
            if self.testcase_tag != 'TC-MR24146-005' :
                exitCliString = "exit";
                #check for COM 3.2
                tmpComRelease = "3"
                tmpComMajorVersion = "1"
                tmpComMajorOK = ('SUCCESS', True)
                tmpComMajorOK = self.lib.checkComponentMajorVersion('com', tmpComRelease, tmpComMajorVersion, [], True)

                if tmpComMajorOK[1] == False:
                    exitCliString = '"end" "exit"'

                cmd = '%s "configure" "ManagedElement=1" "no ObjImpComplexClassSv=1" "no ObjImpTestClass=1" "no ObjImpComplexClassMv=1" "no ObjImpComplexClassSv=3" "no ObjImpTestClass=3" "no ObjImpComplexClassMv=3" "no ObjImpComplexClassMv=4" "no CmNtfCfgTest=100" "no CmNtfCfgTest=500" "no TestMixClass=1" "no TestMixClass=2" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
                self.myLogger.debug('showing the entire configuration')
                self.comsa_lib.executeCliSession(cmd)

            self.testOiTestingTearDown()
            if self.runAsPartOfStabilitySuite == True:
                self.myLogger.info('Large parts of the tearDown skipped. Is is presumed that these parts are done inside the stability test case teadDown phase.')
            else:
                ###########################################################################################################################
                #######################          Removing the model files, imm classes and temporary-directory    #########################
                ###########################################################################################################################
                self.setTestStep("Delete the used objects")

                failures = []

                #Remove the loaded MOM files
                self.setTestStep("Remove the loaded MOM Files")

                if self.modelfile_mp1 != "":
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp1))
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_mp2 != "":
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp2))
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_mp3 != "":
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp3))
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_mp4 != "":
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp4))
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_mp5 != "":
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp5))
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                # Remove the test consumers from target
                self.setTestStep('tearDown: Removing the used test_consumers')
                if self.test_consumer_1 != '':
                    self.myLogger.debug('tearDown: Removing test_consumer_1 from the target under: %s' %self.target_com_compdir)
                    cmd = '\\rm -f %s%s'%(self.target_com_compdir,self.test_consumer_1)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])
                    testCons1CfgFileName = '%s.cfg' %self.test_consumer_1.split('.')[0]
                    cmd = '\\rm -f %s%s'%(self.path_to_cfgFile, testCons1CfgFileName)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.test_consumer_2 != '':
                    self.myLogger.debug('tearDown: Removing test_consumer_2 from the target under: %s' %self.target_com_compdir)
                    cmd = '\\rm -f %s%s'%(self.target_com_compdir,self.test_consumer_2)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])
                    testCons2CfgFileName = '%s.cfg' %self.test_consumer_2.split('.')[0]
                    cmd = '\\rm -f %s%s'%(self.path_to_cfgFile, testCons2CfgFileName)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.test_consumer_3 != '':
                    self.myLogger.debug('tearDown: Removing test_consumer_3 from the target under: %s' %self.target_com_compdir)
                    cmd = '\\rm -f %s%s'%(self.target_com_compdir,self.test_consumer_3)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])
                    testCons3CfgFileName = '%s.cfg' %self.test_consumer_3.split('.')[0]
                    cmd = '\\rm -f %s%s'%(self.path_to_cfgFile, testCons3CfgFileName)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                #Restart COM
                #self.restartCom()
                if self.doSwitchover == 'True'  and self.noOfScs > 1:
                    for controller in self.testConfig['controllers']:
                        result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                        self.fail(result[0], result[1])
                else:
                    self.restartCom()

                if self.pattern_1 != "":
                    result = self.comsa_lib.removeImmObjects(self.pattern_1, self.activeController[0], self.activeController[1]) # pattern is being defined above under inti which shall come from xml file.
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.pattern_2 != "":
                    result = self.comsa_lib.removeImmObjects(self.pattern_2, self.activeController[0], self.activeController[1]) # pattern is being defined above under inti which shall come from xml file.
                    if result [0] != 'SUCCESS':
                        failures.append(result[1])

                if self.pattern_3 != "":
                    result = self.comsa_lib.removeImmObjects(self.pattern_3, self.activeController[0], self.activeController[1]) # pattern is being defined above under inti which shall come from xml file.
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.pattern_4 != "":
                    result = self.comsa_lib.removeImmObjects(self.pattern_4, self.activeController[0], self.activeController[1]) # pattern is being defined above under inti which shall come from xml file.
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.pattern_5 != "":
                    result = self.comsa_lib.removeImmObjects(self.pattern_5, self.activeController[0], self.activeController[1]) # pattern is being defined above under inti which shall come from xml file.
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                #Remove the loaded classes
                self.setTestStep("Remove the loaded classes")

                if self.modelfile_imm_classes1 != "":
                    result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes1), self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_imm_classes2 != "":
                    result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes2), self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_imm_classes3 != "":
                    result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes3), self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_imm_classes4 != "":
                    result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes4), self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                if self.modelfile_imm_classes5 != "":
                    result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes5), self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        failures.append(result[1])

                # Remove temporary directory from target
                cmd = '\\rm -rf %s' %self.tempdir_on_target
                self.myLogger.debug('tearDown: Remove temporary directory from target by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                if result[0] != 'SUCCESS':
                    failures.append(result[1])

                # Workaround for TR HR10473
                pattern = '/usr/lib64/opensaf/osafntfimcnd active'
                if pattern != '':
                   result = self.comsa_lib.findAndRestartActiveProcessFromPattern(pattern, self.testConfig)
                if result[0] != 'SUCCESS':
                    failures.append(result[1])

                if len(failures) != 0:
                    self.fail("Error", "The following issues appeared during the phase of teardown: %s"%str(failures))

        else:
            self.myLogger.info('Teardown skipped')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)
        coreTestCase.CoreTestCase.tearDown(self)

        ###########################################################################################################################
        #######################                        Support Methods                  ###########################################
        ###########################################################################################################################

    def copyModelFilesToTarget(self):
        self.setTestStep('Copy model files to target')
        if self.modelfile_mp1 != "":
            self.copyFileToTarget(self.modelfile_path, self.modelfile_mp1, self.tempdir_on_target)

        if self.modelfile_mp2 != "":
            self.copyFileToTarget(self.modelfile_path, self.modelfile_mp2, self.tempdir_on_target)

        if self.modelfile_mp3 != "":
            self.copyFileToTarget(self.modelfile_path, self.modelfile_mp3, self.tempdir_on_target)

        if self.modelfile_mp4 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_mp4, self.tempdir_on_target)

        if self.modelfile_mp5 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_mp5, self.tempdir_on_target)

        if self.modelfile_imm_classes1 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_classes1, self.tempdir_on_target)

        if self.modelfile_imm_classes2 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_classes2, self.tempdir_on_target)

        if self.modelfile_imm_classes3 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_classes3, self.tempdir_on_target)

        if self.modelfile_imm_classes4 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_classes4, self.tempdir_on_target)

        if self.modelfile_imm_classes5 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_classes5, self.tempdir_on_target)

        if self.modelfile_imm_objects1 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects1, self.tempdir_on_target)

        if self.modelfile_imm_objects2 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects2, self.tempdir_on_target)

        if self.modelfile_imm_objects3 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects3, self.tempdir_on_target)

        if self.modelfile_imm_objects4 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects4, self.tempdir_on_target)

        if self.modelfile_imm_objects5 != "":
                self.copyFileToTarget(self.modelfile_path, self.modelfile_imm_objects5, self.tempdir_on_target)

    def registeringModelFiles(self):
        self.setTestStep('Registering the model files:mp')

        if self.modelfile_mp1 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp1))
            self.fail(result[0],result[1])

        if self.modelfile_mp2 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp2))
            self.fail(result[0],result[1])

        if self.modelfile_mp3 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp3))
            self.fail(result[0],result[1])

        if self.modelfile_mp4 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp4))
            self.fail(result[0],result[1])

        if self.modelfile_mp5 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp5))
            self.fail(result[0],result[1])

    def loadingClassesToImm(self):
        self.setTestStep('Loading classes to IMM')

        if self.modelfile_imm_classes1 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes1))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes2 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes2))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes3 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes3))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes4 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes4))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes5 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes5))
            self.fail(result[0],result[1])

    def loadingObjectsToImm(self):
        self.setTestStep("Loading Objects to IMM")

        if self.modelfile_imm_objects1 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects1))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects2 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects2))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects3 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects3))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects4 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects4))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects5 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects5))
            self.fail(result[0],result[1])

    def restartCom(self):
        self.setTestStep('Restarting COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        self.fail(result[0], result[1])

    def copyTestCompToActiveSC(self):
        self.setTestStep('Copying the test consumer to the target and Registering to COM')

        self.sshLib.setConfig(self.activeSubrack,self.activeSlot,self.activeSlot)
        if self.test_consumer_1 != '':
            self.myLogger.debug('Copying test_consumer to the target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.path_to_testConsumer, self.test_consumer_1, self.target_com_compdir)
            self.miscLib.waitTime(5)

        if self.test_consumer_2 != '':
            self.myLogger.debug('Copying test_consumer to the target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.path_to_testConsumer, self.test_consumer_2, self.target_com_compdir)
            self.miscLib.waitTime(5)

        if self.test_consumer_3 != '':
            self.myLogger.debug('Copying test_consumer to the target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.path_to_testConsumer, self.test_consumer_3, self.target_com_compdir)
            self.miscLib.waitTime(5)

        #self.restartCom()
        #self.pidOfActiveController= self.getComPid()
        #self.myLogger.debug('Process id after 1st restart of Active controller: %s'%self.pidOfActiveController)

    def copyTestCompToStandbySC(self):
        self.setTestStep('Copy test component to standby SC')
        if self.noOfScs == 1:
            self.fail('ERROR', 'Running on a one-node configuration. \
            We should not have ended up in the copyTestCompToStandbySC method.')
        self.sshLib.setConfig(self.standbySubrack,self.standbySlot,self.standbySlot)

        if self.test_consumer_1 != '':
            self.myLogger.debug('Copy test_consumer_1 to target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.path_to_testConsumer, self.test_consumer_1, self.target_com_compdir)
            self.miscLib.waitTime(5)

        if self.test_consumer_2 != '':
            self.myLogger.debug('Copy test_consumer_2 to target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.path_to_testConsumer, self.test_consumer_2, self.target_com_compdir)
            self.miscLib.waitTime(5)

        if self.test_consumer_3 != '':
            self.myLogger.debug('Copy test_consumer_3 to target under: %s' %self.target_com_compdir)
            self.copyFileToTarget(self.path_to_testConsumer, self.test_consumer_3, self.target_com_compdir)
            self.miscLib.waitTime(5)

        self.sshLib.setConfig(self.activeSubrack,self.activeSlot,self.activeSlot)
        return

    def getCmEventUnixTimeFromSyslogEntry(self, logEntry, charsNeeded = 19):
        """
        Returns int unix time in seconds precision.
        """
        if len(logEntry) < charsNeeded:
            self.fail('ERROR', 'The function expects a string that contains at least a unix time with a predifined precision which is %d characters long' %charsNeeded)
        unixTimeString = logEntry[-19:]
        if 'long' not in str(type(eval(unixTimeString))):
            self.fail('ERROR', 'The last %d character in the log entry were expected to be a number of type long. Received: %s' %(charsNeeded, unixTimeString))
        return ('SUCCESS', int(logEntry[-19:][:10]))

    def compareUnixStartTimeWithCmEventUnixTime(self, resultedstartTime, logEntry):
        """
        Returns ('SUCCESS', True) if Cm Event time is greater or equal to the startTime
        Returns ('ERROR', 'CM Event time in logEntry is smaller than the start time. %d' %eventTime) if Cm Event time is smaller than the startTime
        """
        result = self.getCmEventUnixTimeFromSyslogEntry(logEntry)
        eventTime = result[1]
        if eventTime < self.resultedstartTime:
            self.myLogger.error('CM Event time in logEntry %s is smaller than the start time. ' %searchPattern)
            self.expectedLogsIssues.append('CM Event time in logEntry %s is smaller than the start time. ' %searchPattern)
            #self.fail('ERROR', 'CM Event time in logEntry is smaller than the start time. %d' %eventTime)

    def evaluateSearchPattern(self, searchPattern, numberOfMatches, resultedstartTime, logDir):
        result = self.lib.getEventTimestampFromSyslogWithLogEntry(self.activeController[0], self.activeController[1], eval(searchPattern), self.resultedstartTime, self.testConfig,logDir)
        #self.fail(result[0],result[1])
        self.sshLib.tearDownHandles()
        if result[0] != 'SUCCESS':
            self.myLogger.error('No log entry found for search pattern: %s' %searchPattern)
            self.expectedLogsIssues.append('No log entry found for search pattern: %s' %searchPattern)
            return
        self.myLogger.debug('Found text in syslog at: %s' %result[1])
        if 'int' in str(type(eval(numberOfMatches))):
            expedtedNumberOfLogs = eval(numberOfMatches)
        else:
            self.myLogger.error('Function evaluateSearchPattern called with argument "numberOfMatches" that is not of type int. Will use default value 1')
            self.setAdditionalResultInfo('WARNING: Function evaluateSearchPattern called with argument "numberOfMatches" that is not of type int. Used default value 1')
            expedtedNumberOfLogs = 1
        if len(result[2]) != expedtedNumberOfLogs:
            self.myLogger.error('Expected %d matches for the search pattern. Received: %d. They are: %s.' %(expedtedNumberOfLogs, len(result[2]), result[2]))
            self.expectedLogsIssues.append('Expected %d matches for the search pattern. Received: %d. They are: %s.' %(expedtedNumberOfLogs, len(result[2]), result[2]))
            return
            #self.fail('ERROR', 'More than one match for the search pattern. Expected exactly one. Received: %d. They are: %s. Evaluating the last entry in the list!' %(len(result[2]), result[2]))
        for logEntry in result[2]:
            self.compareUnixStartTimeWithCmEventUnixTime(self.resultedstartTime, logEntry)


    def evaluateUnexpectedSearchPattern(self, searchPattern, resultedstartTime, logDir):
        result = self.lib.getEventTimestampFromSyslogWithLogEntry(self.activeController[0], self.activeController[1], eval(searchPattern), self.resultedstartTime, self.testConfig,logDir)
        self.sshLib.tearDownHandles()
        if (result[0] == "SUCCESS"):
            self.myLogger.error("Unexpected pattern found: %s" %searchPattern)
            #self.fail("ERROR", "Unexpected pattern found: %s" %searchPattern)
            self.unexpectedLogsFound.append(searchPattern)

    def populateTestConsumerConfigFiles(self):
        self.setTestStep('Creation of test-consumer-config files and copying it to the target.')
        testCons1CfgContent = ''
        testCons2CfgContent = ''
        testCons3CfgContent = ''
        if self.testCons1Regexp1 != '':
            testCons1CfgContent += self.testCons1Regexp1 + '\n'
        if self.testCons1Regexp2 != '':
            testCons1CfgContent += self.testCons1Regexp2 + '\n'
        if self.testCons1Regexp3 != '':
            testCons1CfgContent += self.testCons1Regexp3 + '\n'
        if self.testCons1Regexp4 != '':
            testCons1CfgContent += self.testCons1Regexp4 + '\n'
        if self.testCons1Regexp5 != '':
            testCons1CfgContent += self.testCons1Regexp5 + '\n'
        if self.testCons2Regexp1 != '':
            testCons2CfgContent += self.testCons2Regexp1 + '\n'
        if self.testCons2Regexp2 != '':
            testCons2CfgContent += self.testCons2Regexp2 + '\n'
        if self.testCons2Regexp3 != '':
            testCons2CfgContent += self.testCons2Regexp3 + '\n'
        if self.testCons2Regexp4 != '':
            testCons2CfgContent += self.testCons2Regexp4 + '\n'
        if self.testCons2Regexp5 != '':
            testCons2CfgContent += self.testCons2Regexp5 + '\n'
        if self.testCons3Regexp1 != '':
            testCons3CfgContent += self.testCons3Regexp1 + '\n'
        if self.testCons3Regexp2 != '':
            testCons3CfgContent += self.testCons3Regexp2 + '\n'
        if self.testCons3Regexp3 != '':
            testCons3CfgContent += self.testCons3Regexp3 + '\n'
        if self.testCons3Regexp4 != '':
            testCons3CfgContent += self.testCons3Regexp4 + '\n'
        if self.testCons3Regexp5 != '':
            testCons3CfgContent += self.testCons3Regexp5 + '\n'

        if testCons1CfgContent != '':
            testCons1CfgFileName = '%s.cfg' %self.test_consumer_1.split('.')[0]
            cmd = 'echo "%s" > %s%s' %(testCons1CfgContent, self.path_to_cfgFile, testCons1CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

        if testCons2CfgContent != '':
            testCons2CfgFileName = '%s.cfg' %self.test_consumer_2.split('.')[0]
            cmd = 'echo "%s" > %s%s' %(testCons2CfgContent, self.path_to_cfgFile, testCons2CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

        if testCons3CfgContent != '':
            testCons3CfgFileName = '%s.cfg' %self.test_consumer_3.split('.')[0]
            cmd = 'echo "%s" > %s%s' %(testCons3CfgContent, self.path_to_cfgFile, testCons3CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

    def checkComPidUnchanged(self):
        result = self.comsa_lib.getProcessId(self.activeController[0], self.activeController[1], 'com', '/etc/com.cfg')
        self.fail(result[0], result[1])
        if 'int' not in str(type(result[1])):
            self.fail('ERROR', 'Expected exactly one COM process to be active. Found: %d: %s' %(len(result[1]), str(result[1])))
        if result[1] != self.comPid:
            self.fail('ERROR', 'COM process restarted unexpectedly. Current PID: %d. Expected PID: %d' %(result[1], self.comPid))

    def getComPid(self):
        result = self.comsa_lib.getProcessId(self.activeController[0], self.activeController[1], 'com', '/etc/com.cfg')
        self.fail(result[0], result[1])
        if 'int' not in str(type(result[1])):
            self.fail('ERROR', 'Expected exactly one COM process to be active. Found: %d: %s' %(len(result[1]), str(result[1])))
        self.comPid = result[1]

    def getCurrentUnixTime(self):
        self.myLogger.debug('Resetting the timer')
        cmd = 'date +\%s'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        startTime = int(result[1])
        self.myLogger.debug("Result of first time:%s"%startTime)
        return startTime

    def cliTesting(self):
        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)
        if len(lists) != 0:
            self.setTestStep('CLI Testing')

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        #self.lib.messageBox('stop')

        for list_index in range (0,len(lists[0])):
            #self.lib.messageBox('stop')
            #self.lib.messageBox('stop')
            result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
            self.fail(result[0], result[1])
            self.checkComPidUnchanged()


    def immTesting(self):
        #Create the input, the expected output and the non-expected output lists for imm
        lists1 = self.comsa_lib.load_TC_imm_config(self)     #load imm_input
        if len(lists1) != 0:
            self.setTestStep('IMM Testing')

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

        #Send the imm commands and process the results element-by-element
        #One element of the list is one imm session.

        for list_index1 in range (0,len(lists1[0])):
           result = self.comsa_lib.runImmSession(lists1, list_index1)
           self.fail(result[0], result[1])
           self.checkComPidUnchanged()


    def testOiTesting(self):
        self.setTestStep('Testing runtime cases with test object implementer')
        self.runTestOICmd(self.testOIarg1)
        self.runTestOICmd(self.testOIarg2)
        self.runTestOICmd(self.testOIarg3)
        self.runTestOICmd(self.testOIarg4)
        self.runTestOICmd(self.testOIarg5)
        self.runTestOICmd(self.testOIarg6)
        self.runTestOICmd(self.testOIarg7)
        self.runTestOICmd(self.testOIarg8)
        self.runTestOICmd(self.testOIarg9)
        self.runTestOICmd(self.testOIarg10)
        self.runTestOICmd(self.testOIarg11)
        self.runTestOICmd(self.testOIarg12)
        self.runTestOICmd(self.testOIarg13)
        self.runTestOICmd(self.testOIarg14)
        self.runTestOICmd(self.testOIarg15)
        self.runTestOICmd(self.testOIarg16)
        self.runTestOICmd(self.testOIarg17)
        self.runTestOICmd(self.testOIarg18)
        self.runTestOICmd(self.testOIarg19)
        self.runTestOICmd(self.testOIarg20)

    def testOiTestingTearDown(self):
        self.setTestStep('Tear Down: runtime cases with test object implementer')
        self.runTestOICmd(self.testOIarg_tearDown1)
        self.runTestOICmd(self.testOIarg_tearDown2)
        self.runTestOICmd(self.testOIarg_tearDown3)
        self.runTestOICmd(self.testOIarg_tearDown4)
        self.runTestOICmd(self.testOIarg_tearDown5)
        self.runTestOICmd(self.testOIarg_tearDown6)
        self.runTestOICmd(self.testOIarg_tearDown7)
        self.runTestOICmd(self.testOIarg_tearDown8)
        self.runTestOICmd(self.testOIarg_tearDown9)
        self.runTestOICmd(self.testOIarg_tearDown10)

    def runTestOICmd(self, testOIarg):
        if testOIarg != "":
            cmd = 'date; %s%s %s' %(self.tempdir_on_target, self.testOI_name, testOIarg)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            self.checkComPidUnchanged()


    '''
    def cliTesting(self):
        self.setTestStep('CLI Testing')

        self.setTestStep('### Check which SC runs the CLI')
        #Creates the login params according to which controller runs the CLI

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0],result[1])
        self.activeController = result[1]

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])


        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)

        #self.lib.messageBox('stop')
        #self.lib.messageBox('stop')

        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        for list_index in range (0,len(lists[0])):
            #self.comsa_lib.getProcessId(self.activeController[0], self.activeController[1], 'com', '/etc/com.cfg')
            result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
            #self.comsa_lib.getProcessId(self.activeController[0], self.activeController[1], 'com', '/etc/com.cfg')
            self.fail(result[0], result[1])
    '''
    def ntfSendSessions(self):
        if self.ntfsendMsg1 != "":
            self.setTestStep('### NtfSend')
            result = self.sshLib.sendCommand(self.ntfsendMsg1)
            self.fail(result[0], result[1])

    def addSubscriptionForTestConsumersExpectedLogs(self):

        self.setTestStep('Check logs after CLI test: Look for the expected texts in the syslog for addSubscription !')

        if self.searchPatterns_subscription_1 != '':
            result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], eval(self.searchPatterns_subscription_1), self.resultedstartTime, self.testConfig,logDir = '/var/log/')
            self.myLogger.debug('Time in the function addSubscriptionForTestConsumersExpectedLogs: %s'%self.resultedstartTime)
            self.fail(result[0], result[1])

        if self.searchPatterns_subscription_2 != '':
            result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], eval(self.searchPatterns_subscription_2), self.resultedstartTime, self.testConfig,logDir = '/var/log/')
            if(result[0]== 'SUCCESS'):
                self.fail(result[0], result[1])

    def addSubscriptionForTestConsumersUnExpectedLogs(self):
        self.setTestStep('Check for Unexpected logs after CLI test: Look for the Non expected texts in the syslog for addSubscription !')

        if self.unexpected_searchPatterns_subscription_1 !='':
           result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], eval(self.unexpected_searchPatterns_subscription_1), self.resultedstartTime, self.testConfig,logDir = '/var/log/')
           if(result[0]== 'SUCCESS'):
               self.myLogger.debug('UnExpected logs exists: %s'%self.unexpected_searchPatterns_subscription_1)
               self.fail('Error','Unexpected logs exists: %s'%self.unexpected_searchPatterns_subscription_1)

        if self.unexpected_searchPatterns_subscription_2 !='':
           result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], eval(self.unexpected_searchPatterns_subscription_2), self.resultedstartTime, self.testConfig,logDir = '/var/log/')
           if(result[0]== 'SUCCESS'):
               self.myLogger.debug('UnExpected logs exists: %s'%self.unexpected_searchPatterns_subscription_2)
               self.fail('Error','Unexpected logs exists: %s'%self.unexpected_searchPatterns_subscription_2)


    def expectedLogs(self):
        self.setTestStep('### Check logs after CLI test: Look for the expected texts in the syslog')
        logDir = '/var/log/'

        if self.searchPatterns1 != "":
            self.evaluateSearchPattern(self.searchPatterns1, self.searchPatterns1Matches, self.resultedstartTime, logDir)
        if self.searchPatterns2 != "":
            self.evaluateSearchPattern(self.searchPatterns2, self.searchPatterns2Matches, self.resultedstartTime, logDir)
        if self.searchPatterns3 != "":
            self.evaluateSearchPattern(self.searchPatterns3, self.searchPatterns3Matches, self.resultedstartTime, logDir)
        if self.searchPatterns4 != "":
            self.evaluateSearchPattern(self.searchPatterns4, self.searchPatterns4Matches, self.resultedstartTime, logDir)
        if self.searchPatterns5 != "":
            self.evaluateSearchPattern(self.searchPatterns5, self.searchPatterns5Matches, self.resultedstartTime, logDir)
        if self.searchPatterns6 != "":
            self.evaluateSearchPattern(self.searchPatterns6, self.searchPatterns6Matches, self.resultedstartTime, logDir)
        if self.searchPatterns7 != "":
            self.evaluateSearchPattern(self.searchPatterns7, self.searchPatterns7Matches, self.resultedstartTime, logDir)
        if self.searchPatterns8 != "":
            self.evaluateSearchPattern(self.searchPatterns8, self.searchPatterns8Matches, self.resultedstartTime, logDir)
        if self.searchPatterns9 != "":
            self.evaluateSearchPattern(self.searchPatterns9, self.searchPatterns9Matches, self.resultedstartTime, logDir)
        if self.searchPatterns10 != "":
            self.evaluateSearchPattern(self.searchPatterns10, self.searchPatterns10Matches, self.resultedstartTime, logDir)
        if self.searchPatterns11 != "":
            self.evaluateSearchPattern(self.searchPatterns11, self.searchPatterns11Matches, self.resultedstartTime, logDir)
        if self.searchPatterns12 != "":
            self.evaluateSearchPattern(self.searchPatterns12, self.searchPatterns12Matches, self.resultedstartTime, logDir)
        if self.searchPatterns13 != "":
            self.evaluateSearchPattern(self.searchPatterns13, self.searchPatterns13Matches, self.resultedstartTime, logDir)
        if self.searchPatterns14 != "":
            self.evaluateSearchPattern(self.searchPatterns14, self.searchPatterns14Matches, self.resultedstartTime, logDir)
        if self.searchPatterns15 != "":
            self.evaluateSearchPattern(self.searchPatterns15, self.searchPatterns15Matches, self.resultedstartTime, logDir)
        if self.searchPatterns16 != "":
            self.evaluateSearchPattern(self.searchPatterns16, self.searchPatterns16Matches, self.resultedstartTime, logDir)
        if self.searchPatterns17 != "":
            self.evaluateSearchPattern(self.searchPatterns17, self.searchPatterns17Matches, self.resultedstartTime, logDir)
        if self.searchPatterns18 != "":
            self.evaluateSearchPattern(self.searchPatterns18, self.searchPatterns18Matches, self.resultedstartTime, logDir)
        if self.searchPatterns19 != "":
            self.evaluateSearchPattern(self.searchPatterns19, self.searchPatterns19Matches, self.resultedstartTime, logDir)
        if self.searchPatterns20 != "":
            self.evaluateSearchPattern(self.searchPatterns20, self.searchPatterns20Matches, self.resultedstartTime, logDir)
        if self.searchPatterns21 != "":
            self.evaluateSearchPattern(self.searchPatterns21, self.searchPatterns21Matches, self.resultedstartTime, logDir)
        if self.searchPatterns22 != "":
            self.evaluateSearchPattern(self.searchPatterns22, self.searchPatterns22Matches, self.resultedstartTime, logDir)
        if self.searchPatterns23 != "":
            self.evaluateSearchPattern(self.searchPatterns23, self.searchPatterns23Matches, self.resultedstartTime, logDir)
        if self.searchPatterns24 != "":
            self.evaluateSearchPattern(self.searchPatterns24, self.searchPatterns24Matches, self.resultedstartTime, logDir)
        if self.searchPatterns25 != "":
            self.evaluateSearchPattern(self.searchPatterns25, self.searchPatterns25Matches, self.resultedstartTime, logDir)
        if self.searchPatterns26 != "":
            self.evaluateSearchPattern(self.searchPatterns26, self.searchPatterns26Matches, self.resultedstartTime, logDir)
        if self.searchPatterns27 != "":
            self.evaluateSearchPattern(self.searchPatterns27, self.searchPatterns27Matches, self.resultedstartTime, logDir)
        if self.searchPatterns28 != "":
            self.evaluateSearchPattern(self.searchPatterns28, self.searchPatterns28Matches, self.resultedstartTime, logDir)
        if self.searchPatterns29 != "":
            self.evaluateSearchPattern(self.searchPatterns29, self.searchPatterns29Matches, self.resultedstartTime, logDir)
        if self.searchPatterns30 != "":
            self.evaluateSearchPattern(self.searchPatterns30, self.searchPatterns30Matches, self.resultedstartTime, logDir)
        if self.searchPatterns31 != "":
            self.evaluateSearchPattern(self.searchPatterns31, self.searchPatterns31Matches, self.resultedstartTime, logDir)
        if self.searchPatterns32 != "":
            self.evaluateSearchPattern(self.searchPatterns32, self.searchPatterns32Matches, self.resultedstartTime, logDir)
        if self.searchPatterns33 != "":
            self.evaluateSearchPattern(self.searchPatterns33, self.searchPatterns33Matches, self.resultedstartTime, logDir)
        if self.searchPatterns34 != "":
            self.evaluateSearchPattern(self.searchPatterns34, self.searchPatterns34Matches, self.resultedstartTime, logDir)
        if self.searchPatterns35 != "":
            self.evaluateSearchPattern(self.searchPatterns35, self.searchPatterns35Matches, self.resultedstartTime, logDir)
        if self.searchPatterns36 != "":
            self.evaluateSearchPattern(self.searchPatterns36, self.searchPatterns36Matches, self.resultedstartTime, logDir)
        if self.searchPatterns37 != "":
            self.evaluateSearchPattern(self.searchPatterns37, self.searchPatterns37Matches, self.resultedstartTime, logDir)
        if self.searchPatterns38 != "":
            self.evaluateSearchPattern(self.searchPatterns38, self.searchPatterns38Matches, self.resultedstartTime, logDir)
        if self.searchPatterns39 != "":
            self.evaluateSearchPattern(self.searchPatterns39, self.searchPatterns39Matches, self.resultedstartTime, logDir)
        if self.searchPatterns40 != "":
            self.evaluateSearchPattern(self.searchPatterns40, self.searchPatterns40Matches, self.resultedstartTime, logDir)
        if self.searchPatterns41 != "":
            self.evaluateSearchPattern(self.searchPatterns41, self.searchPatterns41Matches, self.resultedstartTime, logDir)
        if self.searchPatterns42 != "":
            self.evaluateSearchPattern(self.searchPatterns42, self.searchPatterns42Matches, self.resultedstartTime, logDir)
        if self.searchPatterns43 != "":
            self.evaluateSearchPattern(self.searchPatterns43, self.searchPatterns43Matches, self.resultedstartTime, logDir)
        if self.searchPatterns44 != "":
            self.evaluateSearchPattern(self.searchPatterns44, self.searchPatterns44Matches, self.resultedstartTime, logDir)
        if self.searchPatterns45 != "":
            self.evaluateSearchPattern(self.searchPatterns45, self.searchPatterns45Matches, self.resultedstartTime, logDir)
        if self.searchPatterns46 != "":
            self.evaluateSearchPattern(self.searchPatterns46, self.searchPatterns46Matches, self.resultedstartTime, logDir)
        if self.searchPatterns47 != "":
            self.evaluateSearchPattern(self.searchPatterns47, self.searchPatterns47Matches, self.resultedstartTime, logDir)
        if self.searchPatterns48 != "":
            self.evaluateSearchPattern(self.searchPatterns48, self.searchPatterns48Matches, self.resultedstartTime, logDir)
        if self.searchPatterns49 != "":
            self.evaluateSearchPattern(self.searchPatterns49, self.searchPatterns49Matches, self.resultedstartTime, logDir)
        if self.searchPatterns50 != "":
            self.evaluateSearchPattern(self.searchPatterns50, self.searchPatterns50Matches, self.resultedstartTime, logDir)

    def unexpectedLogs(self):
        self.setTestStep('Grep for the un-uxpected Pattern')
        logDir = '/var/log/'

        if self.unexpectedPattern1 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern1, self.resultedstartTime, logDir)
        if self.unexpectedPattern2 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern2, self.resultedstartTime, logDir)
        if self.unexpectedPattern3 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern3, self.resultedstartTime, logDir)
        if self.unexpectedPattern4 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern4, self.resultedstartTime, logDir)
        if self.unexpectedPattern5 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern5, self.resultedstartTime, logDir)
        if self.unexpectedPattern6 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern6, self.resultedstartTime, logDir)
        if self.unexpectedPattern7 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern7, self.resultedstartTime, logDir)
        if self.unexpectedPattern8 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern8, self.resultedstartTime, logDir)
        if self.unexpectedPattern9 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern9, self.resultedstartTime, logDir)
        if self.unexpectedPattern10 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern10, self.resultedstartTime, logDir)
        if self.unexpectedPattern11 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern11, self.resultedstartTime, logDir)
        if self.unexpectedPattern12 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern12, self.resultedstartTime, logDir)
        if self.unexpectedPattern13 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern13, self.resultedstartTime, logDir)
        if self.unexpectedPattern14 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern14, self.resultedstartTime, logDir)
        if self.unexpectedPattern15 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern15, self.resultedstartTime, logDir)
        if self.unexpectedPattern16 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern16, self.resultedstartTime, logDir)
        if self.unexpectedPattern17 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern17, self.resultedstartTime, logDir)
        if self.unexpectedPattern18 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern18, self.resultedstartTime, logDir)
        if self.unexpectedPattern19 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern19, self.resultedstartTime, logDir)
        if self.unexpectedPattern20 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern20, self.resultedstartTime, logDir)
        if self.unexpectedPattern21 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern21, self.resultedstartTime, logDir)
        if self.unexpectedPattern22 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern22, self.resultedstartTime, logDir)
        if self.unexpectedPattern23 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern23, self.resultedstartTime, logDir)
        if self.unexpectedPattern24 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern24, self.resultedstartTime, logDir)
        if self.unexpectedPattern25 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern25, self.resultedstartTime, logDir)
        if self.unexpectedPattern26 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern26, self.resultedstartTime, logDir)
        if self.unexpectedPattern27 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern27, self.resultedstartTime, logDir)
        if self.unexpectedPattern28 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern28, self.resultedstartTime, logDir)
        if self.unexpectedPattern29 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern29, self.resultedstartTime, logDir)
        if self.unexpectedPattern30 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern30, self.resultedstartTime, logDir)
        if self.unexpectedPattern31 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern31, self.resultedstartTime, logDir)
        if self.unexpectedPattern32 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern32, self.resultedstartTime, logDir)
        if self.unexpectedPattern33 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern33, self.resultedstartTime, logDir)
        if self.unexpectedPattern34 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern34, self.resultedstartTime, logDir)
        if self.unexpectedPattern35 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern35, self.resultedstartTime, logDir)
        if self.unexpectedPattern36 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern36, self.resultedstartTime, logDir)
        if self.unexpectedPattern37 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern37, self.resultedstartTime, logDir)
        if self.unexpectedPattern38 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern38, self.resultedstartTime, logDir)
        if self.unexpectedPattern39 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern39, resultedstartTime, logDir)
        if self.unexpectedPattern40 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern40, resultedstartTime, logDir)
        if self.unexpectedPattern41 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern41, resultedstartTime, logDir)
        if self.unexpectedPattern42 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern42, resultedstartTime, logDir)
        if self.unexpectedPattern43 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern43, resultedstartTime, logDir)
        if self.unexpectedPattern44 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern44, resultedstartTime, logDir)
        if self.unexpectedPattern45 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern45, resultedstartTime, logDir)
        if self.unexpectedPattern46 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern46, resultedstartTime, logDir)
        if self.unexpectedPattern47 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern47, resultedstartTime, logDir)
        if self.unexpectedPattern48 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern48, resultedstartTime, logDir)
        if self.unexpectedPattern49 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern49, resultedstartTime, logDir)
        if self.unexpectedPattern50 != "":
            self.evaluateUnexpectedSearchPattern(self.unexpectedPattern50, resultedstartTime, logDir)



    def copyTestOiToTarget(self):

        if self.testOIarg1 != "":
            self.setTestStep("Copy test object implementer binary to target")
            self.copyFileToTarget(self.testOI_path_in_fileSystem, self.testOI_name, self.tempdir_on_target)
            result = self.sshLib.sendCommand('chmod +x %s%s' %(self.tempdir_on_target, self.testOI_name))
            self.fail(result[0], result[1])


    def ToggleNotifyingFlag(self):

        self.setTestStep("Toggle Notify Flag")
        self.myLogger.debug('Toggle Notify Flag, Disable sending Notifications')
        if self.disable_class_notify_1 != "" and self.disable_objectOrAttr_1 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_1,self.disable_objectOrAttr_1)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_1 != "" and self.enable_objectOrAttr_1 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_1,self.enable_objectOrAttr_1)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_2 != "" and self.disable_objectOrAttr_2 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_2,self.disable_objectOrAttr_2)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_2 != "" and self.enable_objectOrAttr_2 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_2,self.enable_objectOrAttr_2)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_3 != "" and self.disable_objectOrAttr_3 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_3,self.disable_objectOrAttr_3)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_3 != "" and self.enable_objectOrAttr_3 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_3,self.enable_objectOrAttr_3)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_4 != "" and self.disable_objectOrAttr_4 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_4,self.disable_objectOrAttr_4)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_4 != "" and self.enable_objectOrAttr_4 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_4,self.enable_objectOrAttr_4)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_5 != "" and self.disable_objectOrAttr_5 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_5,self.disable_objectOrAttr_5)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_5 != "" and self.enable_objectOrAttr_5 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_5,self.enable_objectOrAttr_5)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_6 != "" and self.disable_objectOrAttr_6 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_6,self.disable_objectOrAttr_6)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_6 != "" and self.enable_objectOrAttr_6 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_6,self.enable_objectOrAttr_6)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_7 != "" and self.disable_objectOrAttr_7 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_7,self.disable_objectOrAttr_7)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_7 != "" and self.enable_objectOrAttr_7 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_7,self.enable_objectOrAttr_7)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_8 != "" and self.disable_objectOrAttr_8 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_8,self.disable_objectOrAttr_8)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_8 != "" and self.enable_objectOrAttr_8 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_8,self.enable_objectOrAttr_8)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_9!= "" and self.disable_objectOrAttr_9 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_9,self.disable_objectOrAttr_9)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_9 != "" and self.enable_objectOrAttr_9 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_9,self.enable_objectOrAttr_9)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_10 != "" and self.disable_objectOrAttr_10 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_10,self.disable_objectOrAttr_10)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_10 != "" and self.enable_objectOrAttr_10 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_10,self.enable_objectOrAttr_10)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_11 != "" and self.disable_objectOrAttr_11 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_11,self.disable_objectOrAttr_11)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_11 != "" and self.enable_objectOrAttr_11 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_11,self.enable_objectOrAttr_11)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_12 != "" and self.disable_objectOrAttr_12 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_12,self.disable_objectOrAttr_12)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_12 != "" and self.enable_objectOrAttr_12 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_12,self.enable_objectOrAttr_12)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_13 != "" and self.disable_objectOrAttr_13 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_13,self.disable_objectOrAttr_13)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_13 != "" and self.enable_objectOrAttr_13 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_13,self.enable_objectOrAttr_13)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_14 != "" and self.disable_objectOrAttr_14 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_14,self.disable_objectOrAttr_14)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_14 != "" and self.enable_objectOrAttr_14 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_14,self.enable_objectOrAttr_14)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_15 != "" and self.disable_objectOrAttr_15 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_15,self.disable_objectOrAttr_15)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_15 != "" and self.enable_objectOrAttr_15 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_15,self.enable_objectOrAttr_15)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_16 != "" and self.disable_objectOrAttr_16 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_16,self.disable_objectOrAttr_16)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_16 != "" and self.enable_objectOrAttr_16 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_16,self.enable_objectOrAttr_16)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_17 != "" and self.disable_objectOrAttr_17 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_17,self.disable_objectOrAttr_17)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_17 != "" and self.enable_objectOrAttr_17 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_17,self.enable_objectOrAttr_17)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_18 != "" and self.disable_objectOrAttr_18 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_18,self.disable_objectOrAttr_18)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_18 != "" and self.enable_objectOrAttr_18 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_18,self.enable_objectOrAttr_18)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_19 != "" and self.disable_objectOrAttr_19 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_19,self.disable_objectOrAttr_19)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_19 != "" and self.enable_objectOrAttr_19 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_19,self.enable_objectOrAttr_19)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_20 != "" and self.disable_objectOrAttr_20 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_20,self.disable_objectOrAttr_20)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_20 != "" and self.enable_objectOrAttr_20 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_20,self.enable_objectOrAttr_20)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.disable_class_notify_21 != "" and self.disable_objectOrAttr_21 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_21,self.disable_objectOrAttr_21)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_21 != "" and self.enable_objectOrAttr_21 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_21,self.enable_objectOrAttr_21)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_22 != "" and self.disable_objectOrAttr_22 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_22,self.disable_objectOrAttr_22)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_22 != "" and self.enable_objectOrAttr_22 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_22,self.enable_objectOrAttr_22)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_23 != "" and self.disable_objectOrAttr_23 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_23,self.disable_objectOrAttr_23)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_23 != "" and self.enable_objectOrAttr_23 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_23,self.enable_objectOrAttr_23)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_24 != "" and self.disable_objectOrAttr_24 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_24,self.disable_objectOrAttr_24)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_24 != "" and self.enable_objectOrAttr_24 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_24,self.enable_objectOrAttr_24)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_25 != "" and self.disable_objectOrAttr_25 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_25,self.disable_objectOrAttr_25)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_25 != "" and self.enable_objectOrAttr_25 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_25,self.enable_objectOrAttr_25)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_26 != "" and self.disable_objectOrAttr_26 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_26,self.disable_objectOrAttr_26)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_26 != "" and self.enable_objectOrAttr_26 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_26,self.enable_objectOrAttr_26)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_27 != "" and self.disable_objectOrAttr_27 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_27,self.disable_objectOrAttr_27)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_27 != "" and self.enable_objectOrAttr_27 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_27,self.enable_objectOrAttr_27)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_28 != "" and self.disable_objectOrAttr_28 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_28,self.disable_objectOrAttr_28)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_28 != "" and self.enable_objectOrAttr_28 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_28,self.enable_objectOrAttr_28)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_29 != "" and self.disable_objectOrAttr_29 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_29,self.disable_objectOrAttr_29)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_29 != "" and self.enable_objectOrAttr_29 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_19,self.enable_objectOrAttr_29)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_30 != "" and self.disable_objectOrAttr_30 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_30,self.disable_objectOrAttr_30)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_30 != "" and self.enable_objectOrAttr_30 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_30,self.enable_objectOrAttr_30)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

    def switchOver (self):
        self.setTestStep('Switch over')

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

        self.activeController = (controller[0], activeController)

        self.myLogger.info('The former active controller became standby')
        return

    def findActiveAndStandbyController(self):
        self.setTestStep('Find active and standby controllers')
        if self.installStressTool:
            self.miscLib.waitTime(150)

        activeController = 0
        standbyController = 0

        controllers = self.testConfig['controllers']
        self.myLogger.info('Checking HA state for Com SA on the controllers')
        for controller in controllers:
            result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            if result[1] == 'ACTIVE':
                activeController = controller
                self.myLogger.info('Found active controller: %s' %str(controller))
            elif result[1] == 'STANDBY':
                standbyController = controller
                self.myLogger.info('Found standby controller: %s' %str(controller))
        self.myLogger.info('findActiveController returns activeController: (%s) standbyController: (%s)' %(activeController,standbyController))

        self.activeSubrack =  activeController[0]
        self.activeSlot =     activeController[1]
        self.activeController = (activeController[0], activeController[1])
        self.myLogger.info('active  controller param: (%s,%s)' %(str(self.activeSubrack),  str(self.activeSlot))  )

        if self.noOfScs == 2 and standbyController != 0:
            self.standbySubrack = standbyController[0]
            self.standbySlot = standbyController[1]
            self.myLogger.info('standby controller param: (%s,%s)' %(str(self.standbySubrack), str(self.standbySlot)) )

    def copyFileToTarget(self, source, filename, destination):
            self.myLogger.debug('copyFileToTarget: source=%s filename=%s destination=%s' %(source, filename, destination))
            result = self.sshLib.remoteCopy('%s%s' % (source, filename), destination, timeout = 60)
            self.fail(result[0],result[1])
            self.miscLib.waitTime(3)

            cmd = "chmod 640 %s%s; chown root:com-core %s%s" %(destination, filename, destination, filename)
            result = self.sshLib.sendCommand(cmd);
            self.fail(result[0],result[1])



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
