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
   	TC-MR24146-003 - Testing MR24146: Any Return Type from CM Action

    Priority:
    High

    Requirement:
    -

    Sensitivity:
    Low

    Description:
    CM action testcases

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

        For CLI testing:
            CLI output and trace in "/var/log/messages" are matching to the expected

        For testing with external test script:
            All test must be passed after running the external test script

    Restore:
    N/A

   ==================================
	 Tag:
    TC-MR24146-003

    Id:
    "Testing MR24146: Any Return Type from CM Action"
    ==================================
"""
import test_env.fw.coreTestCase as coreTestCase
import time
import os
from java.lang import System

class CMactionFp(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.testcase_tag = tag
        # parameters from the config files
        self.expected_trace_value_1 = {}
        self.expected_trace_value_2 = {}
        self.expected_trace_value_3 = {}
        self.expected_trace_value_4 = {}
        self.expected_trace_value_5 = {}
        self.expected_trace_value_6 = {}
        self.expected_trace_value_7 = {}
        self.expected_trace_value_8 = {}
        self.expected_trace_value_9 = {}
        self.expected_trace_value_10 = {}
        self.expected_trace_value_11 = {}
        self.expected_trace_value_12 = {}
        self.expected_trace_value_13 = {}
        self.expected_trace_value_14 = {}
        self.expected_trace_value_15 = {}
        self.expected_trace_value_16 = {}
        self.expected_trace_value_17 = {}
        self.expected_trace_value_18 = {}
        self.expected_trace_value_19 = {}
        self.expected_trace_value_20 = {}

        self.external_script_path = {}
        self.external_script_name = {}
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

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

        self.number_of_steps = {}

        self.cli_sessions_step1 = {}
        self.trace_entries_read_step1 = {}
        self.cli_sessions_step2 = {}
        self.trace_entries_read_step2 = {}
        self.cli_sessions_step3 = {}
        self.trace_entries_read_step3 = {}
        self.cli_sessions_step4 = {}
        self.trace_entries_read_step4 = {}
        self.cli_sessions_step5 = {}
        self.trace_entries_read_step5 = {}
        self.cli_sessions_step6 = {}
        self.trace_entries_read_step6 = {}
        self.cli_sessions_step7 = {}
        self.trace_entries_read_step7 = {}
        self.cli_sessions_step8 = {}
        self.trace_entries_read_step8 = {}
        self.cli_sessions_step9 = {}
        self.trace_entries_read_step9 = {}
        self.cli_sessions_step10 = {}
        self.trace_entries_read_step10 = {}
        self.cli_sessions_step11 = {}
        self.trace_entries_read_step11 = {}
        self.cli_sessions_step12 = {}
        self.trace_entries_read_step12 = {}
        self.cli_sessions_step13 = {}
        self.trace_entries_read_step13 = {}
        self.cli_sessions_step14 = {}
        self.trace_entries_read_step14 = {}
        self.cli_sessions_step15 = {}
        self.trace_entries_read_step15 = {}
        self.cli_sessions_step16 = {}
        self.trace_entries_read_step16 = {}
        self.immObjPattern = '[]'


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

         # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)

        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.actionTest_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("ACTION_TEST_PATH"))
        self.external_script_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("ACTION_TEST_NETCONF"))
        self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get ("MR24146_MODELFILE_PATH"))
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.buildDir = dict.get('BUILD_TOKENS')

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        # Create a backup
        self.createInitBackup()

        self.logger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0],result[1])
        self.activeController = result[1]

        cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        ###############################################################################
        ################ Prepare steps for CM actiontest testing ######################
        ###############################################################################

        self.setTestStep('### Prepare steps for CM actiontest CLI testing')
        self.actionTest_tempdir = '/home/actiontest/'
        self.actionTest_file = 'actionTestAppl'
       	self.modelfile_imm = 'ActiontestMom_imm_classes.xml'
        self.modelfile_mp  = 'ActiontestMom_mp.xml'


        self.setTestStep('### Check which SC runs the CLI')
        #Creates the login params according to which controller runs the CLI

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

        #Create temporary directory on target
        cmd = 'mkdir %s' %self.actionTest_tempdir
        self.myLogger.debug('Create temporary directory on target: %s' %cmd)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])

        #self.lib.messageBox('change the testApp file!')
        #self.lib.messageBox('change the testApp file!')

        self.setTestStep('### Building the test-application')

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-actionTest-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        # Get a build token
        for i in range(self.numberOfGetTokenRetries):
            result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            if result[0] == 'SUCCESS':
                break
        self.fail(result[0],result[1])

        #Do make clean before building the test-application
        cmd = 'cd %s;make clean' %self.actionTest_path
        self.myLogger.debug('Do make clean before building the test-application by: %s' %cmd)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0],result[1])
        cmd = 'ls %s | grep -c %s' %(self.actionTest_path, self.actionTest_file)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0],result[1])
        if result[1].split()[0] != '0':
            self.fail('ERROR', 'File is not removed after make clean!')

        #Build the test-application
        cmd = 'cd %s;make' %self.actionTest_path
        self.myLogger.debug('Building the test-application by: %s' %cmd)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0],result[1])
        cmd = 'ls %s | grep -c %s' %(self.actionTest_path, self.actionTest_file)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0],result[1])
        if result[1].split()[0] != '1':
            self.fail('ERROR', 'Building was unsuccessful!')

        #self.lib.messageBox('change the testApp file!')
        #self.lib.messageBox('change the testApp file!')

        self.setTestStep('### Copy the test-application and the model files to target')
        #Copy actionTest application to target
        self.myLogger.debug('Copy actionTest application to target')
        result = self.sshLib.remoteCopy('%s%s' %(self.actionTest_path, self.actionTest_file), self.actionTest_tempdir, timeout = 60)
        self.fail(result[0],result[1])

        # Release the build token
        result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
        self.fail(result[0],result[1])

        #Copy model files to target
        self.myLogger.debug('Copy model files to target')
        result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path,self.modelfile_imm), self.actionTest_tempdir, timeout = 60)
        self.fail(result[0],result[1])

        result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_mp), self.actionTest_tempdir, timeout = 60)
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

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus NFS disk stress, no local disk stress
            #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

            stressTimeOut = 60
            self.sshLib.setTimeout(stressTimeOut)

        self.setTestStep('### Registering the model files')
        #Adding the path to target model file list
        result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.actionTest_tempdir, self.modelfile_mp))
        self.fail(result[0],result[1])

        # Restart COM
        self.myLogger.debug('Restart COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        self.fail(result[0],result[1])

        self.setTestStep('### Loading model files to IMM')

        #Loading model files
        self.myLogger.debug('Loading model files to IMM')
        cmd = 'immcfg -f %s%s' %(self.actionTest_tempdir, self.modelfile_imm)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])
        if result[1] != '':
            self.fail('ERROR', result[1])
        cmd = 'immcfg -c Sdp617ActiontestRoot sdp617ActiontestRootId=1'
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])
        if result[1] != '':
            self.fail('ERROR', result[1])
        cmd = 'immcfg -c ActionTest actionTestId=1,sdp617ActiontestRootId=1'
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])
        if result[1] != '':
            self.fail('ERROR', result[1])

        self.setTestStep('### Running the test-application')
        #Giving permission for execution
        cmd = 'chmod u+x %s%s' %(self.actionTest_tempdir, self.actionTest_file)
        self.myLogger.debug('Giving permission for execution by: %s' %cmd)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])

        #Start actionTest application
        save_default_timeout = self.sshLib.getTimeout(self.activeController[0], self.activeController[1])
        self.sshLib.setTimeout(8, self.activeController[0], self.activeController[1])
        cmd = 'nohup %s%s >>nohup.out 2>&1 &' %(self.actionTest_tempdir, self.actionTest_file)
        self.myLogger.debug('Start actionTest application by: %s' %cmd)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])

        self.sshLib.setTimeout(save_default_timeout, self.activeController[0], self.activeController[1])
        actiontest_pid = result[1].split()[1]

        self.setTestStep('### Enable the trace')
        cmd = 'kill -usr2 %s' %actiontest_pid
        self.myLogger.debug('Enable trace by: %s' %cmd)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])
        #if result[1] == '':
        #    self.myLogger.debug('Trace successfully enabled: "%s"' %cmd)
        #else:
        #    self.fail('ERROR',"Trace did not turn on!")
        if 'No such process' in result[1]:
            self.fail('ERROR', 'Trace not turned on, the process does not exist!')

        #self.lib.messageBox('change the testApp file!')
        #self.lib.messageBox('change the testApp file!')

        ###############################################################################
        ############################### CLI testing ###################################
        ###############################################################################

        self.setTestStep('### CLI testing')

        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)

        traces = self.load_expected_trace_lists()

        self.myLogger.debug('Number of steps is %s' %self.number_of_steps)
        if 'int' in str(type(eval(self.number_of_steps))):
            steps = eval(self.number_of_steps)
        else:
            self.fail('ERROR', 'self.number_of_steps has to be a string representation of an int. It is instead: %s' %str(self.number_of_steps))

        cli_sessions_per_step = self.load_cli_steps_list()
        traces_checked_per_step = self.load_traces_steps_list()

        cli_session_step = 0
        trace_entry_step = 0

        for step in range(steps):
            self.setTestStep('### Running step %d' %step)

            if 'int' in str(type(eval(cli_sessions_per_step[step]))):
                cli_sessions_this_step = eval(cli_sessions_per_step[step])
            else:
                self.fail('ERROR', 'cli_sessions_per_step has to be a list of string representations of ints. It contains at least one non-int element: %s' %str(cli_sessions_per_step))

            if 'int' in str(type(eval(traces_checked_per_step[step]))):
                traces_checked_this_step = eval(traces_checked_per_step[step])
            else:
                self.fail('ERROR', 'traces_checked_per_step has to be a list of string representations of ints. It contains at least one non-int element: %s' %str(cli_sessions_per_step))

            cmd = 'date +\%s'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            startTime = int(result[1])

            #Send the cli commands and process the results element-by-element
            #One element of the list is one cli session.
            for list_index in range (cli_session_step, cli_session_step + cli_sessions_this_step):
                result = self.comsa_lib.runCliSession(lists, list_index, cli_active_controller_login_params)
                self.fail(result[0], result[1])

            cli_session_step = cli_session_step + cli_sessions_this_step

            self.myLogger.info('trace_entry_step is: %s' %str(trace_entry_step))
            self.myLogger.info('traces_checked_this_step is: %s' %str(traces_checked_this_step))

            for trace_entry in traces[trace_entry_step: trace_entry_step + traces_checked_this_step]:
                self.myLogger.info('Searching for %s in the logs:' %trace_entry)
                searchPattern = [trace_entry]
                result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, startTime, self.testConfig)
                self.fail(result[0],result[1])

            trace_entry_step = trace_entry_step + traces_checked_this_step

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')
        ###############################################################################
        ################################### Cleanup ###################################
        ###############################################################################

        tdFailures = []

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        if self.memoryCheck:
            for controller in self.testConfig['controllers']:
                result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                self.fail(result[0],result[1])

        result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup=False)
        if result[0] != 'SUCCESS':
            self.myLogger.error('Failed to restore system. %s' %result[1])
            tdFailures.append('Failed to restore system. %s' %result[1])

        if self.memoryCheck:
            self.setTestStep('Activating Valgrind')
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            if result[0] != 'SUCCESS':
                self.myLogger.error('Failed to activate Valgrind. %s' %result[1])
                tdFailures.append('Failed to activate Valgrind. %s' %result[1])


        cmd = '\\rm -rf %s' %self.actionTest_tempdir
        self.myLogger.debug('Remove temporary directory from target by: %s' %cmd)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        if result[0] != 'SUCCESS' or result[1] != '':
            self.myLogger.error('Failed to remove actionTest temp dir')
            tdFailures.append((cmd, result))

        if len(tdFailures) != 0:
            self.fail('ERROR', 'The following failures occurred during tearDown: %s' %str(tdFailures))

        coreTestCase.CoreTestCase.tearDown(self)

        #########################
        #### SUPPORT METHODS ####
        #########################


    def load_expected_trace_lists(self):
        '''
        This method loads the expected traces from the data received from the xml,
         and creates a list of the search patterns.
        1. Checking the data received from the xml
        2. Create list
        3. return list

        The method returns 3 lists:
         (cli_input_list, cli_expected_output_list, cli_nonexpected_output_list)

        '''
        self.myLogger.debug('enter load_expected_trace_lists function')
        trace_list = []
        if self.expected_trace_value_1 != {}:
            trace_list.append(self.expected_trace_value_1)
        if self.expected_trace_value_2 != {}:
            trace_list.append(self.expected_trace_value_2)
        if self.expected_trace_value_3 != {}:
            trace_list.append(self.expected_trace_value_3)
        if self.expected_trace_value_4 != {}:
            trace_list.append(self.expected_trace_value_4)
        if self.expected_trace_value_5 != {}:
            trace_list.append(self.expected_trace_value_5)
        if self.expected_trace_value_6 != {}:
            trace_list.append(self.expected_trace_value_6)
        if self.expected_trace_value_7 != {}:
            trace_list.append(self.expected_trace_value_7)
        if self.expected_trace_value_8 != {}:
            trace_list.append(self.expected_trace_value_8)
        if self.expected_trace_value_9 != {}:
            trace_list.append(self.expected_trace_value_9)
        if self.expected_trace_value_10 != {}:
            trace_list.append(self.expected_trace_value_10)
        if self.expected_trace_value_11 != {}:
            trace_list.append(self.expected_trace_value_11)
        if self.expected_trace_value_12 != {}:
            trace_list.append(self.expected_trace_value_12)
        if self.expected_trace_value_13 != {}:
            trace_list.append(self.expected_trace_value_13)
        if self.expected_trace_value_14 != {}:
            trace_list.append(self.expected_trace_value_14)
        if self.expected_trace_value_15 != {}:
            trace_list.append(self.expected_trace_value_15)
        if self.expected_trace_value_16 != {}:
            trace_list.append(self.expected_trace_value_16)
        if self.expected_trace_value_17 != {}:
            trace_list.append(self.expected_trace_value_17)
        if self.expected_trace_value_18 != {}:
            trace_list.append(self.expected_trace_value_18)
        if self.expected_trace_value_19 != {}:
            trace_list.append(self.expected_trace_value_19)
        if self.expected_trace_value_20 != {}:
            trace_list.append(self.expected_trace_value_20)



        self.myLogger.debug('leave load_expected_trace_lists function')
        return (trace_list)


    def load_cli_steps_list(self):
        '''
        This method loads the number of CLI sessions from the data received from the xml for each test step
         and creates a list of the search patterns.
        1. Checking the data received from the xml
        2. Create list
        3. return list

        The method returns 3 lists:
         (cli_steps)

        '''
        self.myLogger.debug('enter load_cli_steps_list function')
        cli_steps = []

        if self.cli_sessions_step1 != {}:
            cli_steps.append(self.cli_sessions_step1)
        if self.cli_sessions_step2 != {}:
            cli_steps.append(self.cli_sessions_step2)
        if self.cli_sessions_step3 != {}:
            cli_steps.append(self.cli_sessions_step3)
        if self.cli_sessions_step4 != {}:
            cli_steps.append(self.cli_sessions_step4)
        if self.cli_sessions_step5 != {}:
            cli_steps.append(self.cli_sessions_step5)
        if self.cli_sessions_step6 != {}:
            cli_steps.append(self.cli_sessions_step6)
        if self.cli_sessions_step7 != {}:
            cli_steps.append(self.cli_sessions_step7)
        if self.cli_sessions_step8 != {}:
            cli_steps.append(self.cli_sessions_step8)
        if self.cli_sessions_step9 != {}:
            cli_steps.append(self.cli_sessions_step9)
        if self.cli_sessions_step10 != {}:
            cli_steps.append(self.cli_sessions_step10)
        if self.cli_sessions_step11 != {}:
            cli_steps.append(self.cli_sessions_step11)
        if self.cli_sessions_step12 != {}:
            cli_steps.append(self.cli_sessions_step12)
        if self.cli_sessions_step13 != {}:
            cli_steps.append(self.cli_sessions_step13)
        if self.cli_sessions_step14 != {}:
            cli_steps.append(self.cli_sessions_step14)
        if self.cli_sessions_step15 != {}:
            cli_steps.append(self.cli_sessions_step15)
        if self.cli_sessions_step16 != {}:
            cli_steps.append(self.cli_sessions_step16)

        self.myLogger.debug('leave load_cli_steps_list function')
        return (cli_steps)


    def load_traces_steps_list(self):
        '''
        This method loads the number of CLI sessions from the data received from the xml for each test step
         and creates a list of the search patterns.
        1. Checking the data received from the xml
        2. Create list
        3. return list

        The method returns 3 lists:
         (traces_steps)

        '''
        self.myLogger.debug('enter traces_steps function')
        traces_steps = []

        if self.trace_entries_read_step1 != {}:
            traces_steps.append(self.trace_entries_read_step1)
        if self.trace_entries_read_step2 != {}:
            traces_steps.append(self.trace_entries_read_step2)
        if self.trace_entries_read_step3 != {}:
            traces_steps.append(self.trace_entries_read_step3)
        if self.trace_entries_read_step4 != {}:
            traces_steps.append(self.trace_entries_read_step4)
        if self.trace_entries_read_step5 != {}:
            traces_steps.append(self.trace_entries_read_step5)
        if self.trace_entries_read_step6 != {}:
            traces_steps.append(self.trace_entries_read_step6)
        if self.trace_entries_read_step7 != {}:
            traces_steps.append(self.trace_entries_read_step7)
        if self.trace_entries_read_step8 != {}:
            traces_steps.append(self.trace_entries_read_step8)
        if self.trace_entries_read_step9 != {}:
            traces_steps.append(self.trace_entries_read_step9)
        if self.trace_entries_read_step10 != {}:
            traces_steps.append(self.trace_entries_read_step10)
        if self.trace_entries_read_step11 != {}:
            traces_steps.append(self.trace_entries_read_step11)
        if self.trace_entries_read_step12 != {}:
            traces_steps.append(self.trace_entries_read_step12)
        if self.trace_entries_read_step13 != {}:
            traces_steps.append(self.trace_entries_read_step13)
        if self.trace_entries_read_step14 != {}:
            traces_steps.append(self.trace_entries_read_step14)
        if self.trace_entries_read_step15 != {}:
            traces_steps.append(self.trace_entries_read_step15)
        if self.trace_entries_read_step16 != {}:
            traces_steps.append(self.trace_entries_read_step16)

        self.myLogger.debug('leave traces_steps function')
        return (traces_steps)

    def createInitBackup(self):
        # Skip creating the backup if there is a safe backup created at the beginning of the test suite
        self.backupName = None
        if self.testSuiteConfig.has_key('restoreBackup'):
            result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
            if result == ('SUCCESS', 'EXIST'):
                self.backupName = self.testSuiteConfig['restoreBackup']
        if self.backupName == None or self.testSuiteConfig.has_key('restoreBackup') == False:
            self.backupName = 'cmActionTempBackup'
            result = self.safLib.isBackup(self.backupName)
            self.fail(result[0], result[1])
            if result != ('SUCCESS','NOT EXIST'):
                result = self.safLib.backupRemove(self.backupName)
                self.fail(result[0], result[1])
            result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
            if result[0] != 'SUCCESS' and self.linuxDistro == self.distroTypes[1]:
                self.myLogger.warn('Could not create backup on RHEL system. This is not a critical fault')
            else:
                self.fail(result[0], result[1])

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases

