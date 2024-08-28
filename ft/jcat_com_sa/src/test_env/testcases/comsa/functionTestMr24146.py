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

    TC-MR24146-001 : Create objects of class that has attribute of type EcimFloat

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
    TC-MR24146-001

    Id:
    "Create objects of class that has attribute of type EcimFloat"
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import os

from java.lang import System

class functiontestMR24146(coreTestCase.CoreTestCase):

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

        self.useExternalModels = {}
        self.pathToModelFiles = {}
        self.momFile = {}
        self.immClassesFile = {}
        self.immClassesFile2 = {}
        self.immClassesFile3 = {}
        self.modelFileType = ''
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.immObjPattern = '[]'
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
        self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MR24146_MODELFILE_PATH"))
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = dict.get('REPLACE_COM_SCRIPT_VALGRIND')
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

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
            res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
            #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

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

            if self.immClassesFile2 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile2), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

            if self.immClassesFile3 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile3), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

            # Add model file to COM
            if self.momFile != {}:
                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
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

            # Restart COM
            self.myLogger.debug('Restart COM')
            result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
            self.fail(result[0],result[1])

            self.miscLib.waitTime(10)

        self.setTestStep('###Send the CLI command and process the results###')
        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)

        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        for list_index in range(0,len(lists[0])):
            result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
            self.fail(result[0], result[1])

        coreTestCase.CoreTestCase.runTest(self)


    def tearDown(self):
        self.setTestStep('tearDown')

        if self.useExternalModels == 'yes':

            if self.momFile != {}:
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
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
