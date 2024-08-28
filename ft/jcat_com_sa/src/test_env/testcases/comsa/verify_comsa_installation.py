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


    Priority:


    Requirement:


    Sensitivity:


    Restrictions:


    Test tools:


    Configuration:
    2SC+nPL

    Action:


    Result:


    Restore:


    Description:


"""
import test_env.fw.coreTestCase as coreTestCase
import os
import re

class ComSAVerifyInstall(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
#ADDED
        self.ssh_cli_tester_script = {}
        self.set_pw_script = {}
        self.set_pw_script_rhel = {}
        self.set_login_script = {}
        self.ssh_cli_input = {}
        self.ssh_cli_expected_output = {}
        self.ssh_cli_nonexpected_output = {}
#END ADDED
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
        self.immObjectsFile = {}
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.immObjPattern = '[]'

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
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

        self.setTestStep('Prepare for testing')

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0],result[1])
        activeSc = result[1]

        #Creates the login params according to which controller runs the CLI
        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    activeSc, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

#ADDED
        result = self.create_active_controller_login_params(1, activeSc)
        self.fail(result[0],result[1])
        self.ssh_cli_active_controller_login_params = result[1]
#END ADDED

        cmd = '%s "show all" "exit"' %self.cli_active_controller_login_params
        self.myLogger.debug('showing the entire configuration')
        result = self.miscLib.execCommand(cmd)

        exitCliString = "exit";
        #check for COM 3.2
        tmpComRelease = "3"
        tmpComMajorVersion = "1"
        tmpComMajorOK = ('SUCCESS', True)
        tmpComMajorOK = self.lib.checkComponentMajorVersion('com', tmpComRelease, tmpComMajorVersion, [], True)

        if tmpComMajorOK[1] == False:
            exitCliString = '"end" "exit"'

        if 'SnmpTargetV1=1' in result[1]:
            cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV1=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete SnmpTargetV1, just in case it was left there')
            result1 = self.miscLib.execCommand(cmd)
        if 'SnmpTargetV1=2' in result[1]:
            cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV1=2" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete SnmpTargetV1, just in case it was left there')
            result1 = self.miscLib.execCommand(cmd)
#ADDED
        if 'SnmpTargetV2C=1' in result[1]:
            cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV2C=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete SnmpTargetV2C, just in case it was left there')
            result1 = self.miscLib.execCommand(cmd)
#END ADDED
        if 'SnmpTargetV2C=2' in result[1]:
            cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV2C=2" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete SnmpTargetV2C, just in case it was left there')
            result1 = self.miscLib.execCommand(cmd)
        if 'userLabel' in result[1]:
            cmd = '%s "configure" "ManagedElement=1" "no userLabel" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete userLabel, just in case it was left there')
            result1 = self.miscLib.execCommand(cmd)
        if 'siteLocation' in result[1]:
            cmd = '%s "configure" "ManagedElement=1" "no siteLocation" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
            self.myLogger.debug('Delete siteLocation, just in case it was left there')
            result1 = self.miscLib.execCommand(cmd)


        self.logger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')

#ADDED
        self.setTestStep('SSH to CLI and "show" (Chapter 4.3)')
#Ugly fix for no running load_TC_cli_config in this test
        ssh_input = []
        ssh_input.append(self.ssh_cli_input)
        #ssh_input = self.ssh_cli_input
        ssh_expected = []
        ssh_expected.append(self.ssh_cli_expected_output)
        ssh_nonexpected=[]
        ssh_nonexpected.append(self.ssh_cli_nonexpected_output)

        #Send the input and compare output to expected and nonexpected
        self.run_input_vs_expected(self.ssh_cli_active_controller_login_params, ssh_input, ssh_expected, ssh_nonexpected)
#END ADDED



        self.setTestStep('Read configuration and use CLI via /opt/com/bin/cliss (Chapter 5.1')
        #Create the input, the expected output and the non-expected output lists
        lists = self.load_TC_cli_config()
        cli_input_list = lists[0]
        cli_expected_output_list = lists[1]
        cli_nonexpected_output_list = lists[2]
        connection_failed = 'Connection to COM failed. (Connection refused)' #NEEDED?

        #Send the input and compare output to expected and nonexpected
#ADDED
        self.run_input_vs_expected(self.cli_active_controller_login_params, cli_input_list, cli_expected_output_list, cli_nonexpected_output_list)
#END ADDED


# ADDED as function run_input_vs_expected
#        for list_index in range (0,len(cli_input_list)):
#
#            #Send CLI command
#            cmd = '%s %s' %(self.cli_active_controller_login_params, cli_input_list[list_index])
#            self.myLogger.debug('Sending CLI command')
#            result = self.miscLib.execCommand(cmd)
#            self.debug_logger_line_by_line(result[1].splitlines())
#            self.fail(result[0],result[1])
#            cli_output_lines = result[1].splitlines()
#
#            #Compare cli output to the expected output
#            cli_expected_output = eval(cli_expected_output_list[list_index])
#            cli_nonexpected_output = eval(cli_nonexpected_output_list[list_index])
#            self.myLogger.debug('Checking CLI output')
#            result = self.check_CLI_output(cli_output_lines, cli_expected_output, cli_nonexpected_output)
#            print"check_CLI_output result is: %s %s" %(result[0],result[1])
#            self.fail(result[0],result[1])
#            self.miscLib.waitTime(1)

#END ADDED

#ADDED
        #Setup a new test account
        self.setTestStep('Adding user to emergency group (Chapter 5.2)')
        # SLES11
        if self.linuxDistro == self.distroTypes[0]:
            cmd = 'useradd -P /cluster/etc -G com-emergency testuser'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
        # RHEL
        elif self.linuxDistro == self.distroTypes[1]:
            cmd = 'useradd -G com-emergency testuser'
            for controller in self.testConfig['controllers']:
                result = self.sshLib.sendCommand(cmd, controller[0], controller[1])
                self.fail(result[0],result[1])
        # SLES12
        elif self.linuxDistro == self.distroTypes[2]:
            cmd = 'useradd -G com-emergency testuser'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
        else:
            self.fail('ERROR', 'Unknown linux distribution - behavior needs to be understood first')
        self.miscLib.waitTime(5)

       #Add a password for the new user
        if self.linuxDistro == self.distroTypes[0]:
            cmd = '%s%s./%s %s testuser testtest' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.set_pw_script, self.targetData['ipAddress']['ctrl']['ctrl1'] )
            result = self.miscLib.execCommand(cmd)
            if 'Password changed.' not in result[1]:
                self.fail('ERROR', 'Could not add a password to the new user')
            self.debug_logger_line_by_line(result[1].splitlines())
            self.fail(result[0],result[1])

            #Update the login.allow
            cmd = "echo 'testuser all' >> /cluster/etc/login.allow"
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
        elif self.linuxDistro == self.distroTypes[1]:
            for controller in self.testConfig['controllers']:
                cmd = '%s%s./%s %s testuser testtest' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.set_pw_script_rhel, self.targetData['ipAddress']['ctrl']['ctrl%d' %controller[1]] )
                result = self.miscLib.execCommand(cmd)
                self.debug_logger_line_by_line(result[1].splitlines())
                self.fail(result[0],result[1])
        elif self.linuxDistro == self.distroTypes[2]:
            cmd = '%s%s./%s %s testuser testtest' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.set_pw_script, self.targetData['ipAddress']['ctrl']['ctrl1'] )
            result = self.miscLib.execCommand(cmd)
            if 'password updated successfully' not in result[1]:
                self.fail('ERROR', 'Could not add a password to the new user')
            self.debug_logger_line_by_line(result[1].splitlines())
            self.fail(result[0],result[1])

            #Update the login.allow
            cmd = "echo 'testuser all' >> /cluster/etc/login.allow"
            result = self.sshLib.sendCommand(cmd)
        self.miscLib.waitTime(2)

        self.miscLib.waitTime(5)

        #Login as the new user
        cmd = '%s%s./%s %s testuser testtest' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.set_login_script, self.targetData['ipAddress']['ctrl']['ctrl1'] )
        result = self.miscLib.execCommand(cmd)
        pattern = re.compile('SC-2-1.[~|/]')
        if not re.search(pattern, result[1]):
            self.fail('ERROR', 'Could not log in as newly created user')
        #self.debug_logger_line_by_line(result[1].splitlines()) NEEDED?
        self.fail(result[0],result[1])


    def tearDown(self):
        self.setTestStep('tearDown')
        coreTestCase.CoreTestCase.tearDown(self)

        #Delete the new user
        if self.linuxDistro == self.distroTypes[0]:
            cmd = 'userdel -P /cluster/etc testuser'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            cmd = "sed -i '/testuser all/d' /cluster/etc/login.allow"
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
        elif self.linuxDistro == self.distroTypes[1]:
            for controller in self.testConfig['controllers']:
                cmd = 'userdel testuser'
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
        elif self.linuxDistro == self.distroTypes[2]:
            cmd = 'userdel testuser'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            cmd = "sed -i '/testuser all/d' /cluster/etc/login.allow"
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])



        #########################
        #### SUPPORT METHODS ####
        #########################

    def load_TC_cli_config(self):
        '''
        This method loads the configs from the data received from the xml,
         and creates a list of the CLI inputs, expected outputs, non-expected outputs.
        1. Checking the data received from the xml
        2. Create list
        3. return list

        The method returns 3 lists:
         (cli_input_list, cli_expected_output_list, cli_nonexpected_output_list)

        '''
        self.myLogger.debug('enter load_TC_cli_config function')
        cli_input_list = []
        cli_expected_output_list = []
        cli_nonexpected_output_list = []
        #Only append to the corresponding list if the CLI input and the expected output is present
        if self.cli_input_1 != {} and self.cli_expected_output_1 != {} and self.cli_nonexpected_output_1 != {}:
            cli_input_list.append(self.cli_input_1)
            cli_expected_output_list.append(self.cli_expected_output_1)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_1)
        if self.cli_input_2 != {} and self.cli_expected_output_2 != {} and self.cli_nonexpected_output_2 != {}:
            cli_input_list.append(self.cli_input_2)
            cli_expected_output_list.append(self.cli_expected_output_2)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_2)
        if self.cli_input_3 != {} and self.cli_expected_output_3 != {} and self.cli_nonexpected_output_3 != {}:
            cli_input_list.append(self.cli_input_3)
            cli_expected_output_list.append(self.cli_expected_output_3)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_3)
        if self.cli_input_4 != {} and self.cli_expected_output_4 != {} and self.cli_nonexpected_output_4 != {}:
            cli_input_list.append(self.cli_input_4)
            cli_expected_output_list.append(self.cli_expected_output_4)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_4)
        if self.cli_input_5 != {} and self.cli_expected_output_5 != {} and self.cli_nonexpected_output_5 != {}:
            cli_input_list.append(self.cli_input_5)
            cli_expected_output_list.append(self.cli_expected_output_5)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_5)
        if self.cli_input_6 != {} and self.cli_expected_output_6 != {} and self.cli_nonexpected_output_6 != {}:
            cli_input_list.append(self.cli_input_6)
            cli_expected_output_list.append(self.cli_expected_output_6)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_6)
        if self.cli_input_7 != {} and self.cli_expected_output_7 != {} and self.cli_nonexpected_output_7 != {}:
            cli_input_list.append(self.cli_input_7)
            cli_expected_output_list.append(self.cli_expected_output_7)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_7)
        if self.cli_input_8 != {} and self.cli_expected_output_8 != {} and self.cli_nonexpected_output_8 != {}:
            cli_input_list.append(self.cli_input_8)
            cli_expected_output_list.append(self.cli_expected_output_8)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_8)
        if self.cli_input_9 != {} and self.cli_expected_output_9 != {} and self.cli_nonexpected_output_9 != {}:
            cli_input_list.append(self.cli_input_9)
            cli_expected_output_list.append(self.cli_expected_output_9)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_9)
        if self.cli_input_10 != {} and self.cli_expected_output_10 != {} and self.cli_nonexpected_output_10 != {}:
            cli_input_list.append(self.cli_input_10)
            cli_expected_output_list.append(self.cli_expected_output_10)
            cli_nonexpected_output_list.append(self.cli_nonexpected_output_10)

        self.myLogger.debug('leave load_TC_cli_config function')
        return (cli_input_list, cli_expected_output_list, cli_nonexpected_output_list)

    def create_active_controller_login_params(self, flag, activeSc):
        '''
        The method creates the login params according to which controller runs the CLI.
        1. Try to access CLI on SC1 (lets call it active SC)
        2. Try to access CLI on SC2 (lets call it active SC)
        3. Creates the login params for the active SC.

        The method returns:
         'SUCCESS', <cli login params> - if the CLI is running on 1 of the 2 SCs.
         'ERROR', 'Can not access CLI on SC1 and on SC2' - if the CLI is not running on any of the 2 SCs.

        '''
        user_name = self.targetData['user']
        password = self.targetData['pwd']
        SC_ip = self.targetData['ipAddress']['ctrl']['ctrl%d'%activeSc[1]]
        SC_prompt = self.testConfig['testNodesNames'][activeSc[1] - 1]
        cli_script_path = '%s/%s'%(self.MY_REPOSITORY, self.pathToConfigFiles)
        if flag == 0:
            cli_script_name = self.cli_tester_script
        elif flag == 1:
            cli_script_name = self.ssh_cli_tester_script
        CLI_login_params = "%s./%s %s %s %s %s" %(cli_script_path, cli_script_name, SC_ip, user_name, password, SC_prompt)

        return ('SUCCESS', CLI_login_params)

    def check_CLI_output(self, cli_output_lines, cli_expected_output, cli_nonexpected_output):
        '''
        This method compares the cli output to the expected.
        1. Looking for the index of the first cli line (">")
        2. Compare output line-by-line(from the first to the last cli line) to the expected lines
        3. Process and return result

        The method returns:
         'SUCCESS', 1 - if the cli output matches to the expected output
         'ERROR', 0 - if the cli output not matches to the expected output

        '''
        self.myLogger.debug('enter check_CLI_output function')
        all_matching = False
        nonexpected_item_present = True
        cli_output = []
        first_line = 0
        comp_result = ''

        #Looking for the index of the first cli line (">")
        self.myLogger.debug('Looking for the index of the first cli line')
        for lines in range(0,len(cli_output_lines)):
            if len(cli_output_lines[lines]) != 0 and cli_output_lines[lines][0] == '>':
                first_line = lines
                break

        #Compare output line-by-line(from the first to the last cli line) to the expected lines
        self.myLogger.debug('Compare output line-by-line')
        for item in cli_expected_output:
            for lines in range(first_line,len(cli_output_lines)):
                #if cli_output_lines[lines] == item:
                if item in cli_output_lines[lines]:
                    all_matching = True
                    break
                else:
                    all_matching = False
            #If one of the expected elements missing, then it will break with False
            if all_matching == False:
                self.myLogger.error('Missing output: %s' %item)
                break
        #Compare output line-by-line(from the first to the last cli line) to the non-expected lines
        self.myLogger.debug('Look for non-existing items line-by-line')
        for item in cli_nonexpected_output:
            for lines in range(first_line,len(cli_output_lines)):
                if item.lower() in cli_output_lines[lines].lower():
                    nonexpected_item_present = True
                    break
                else:
                    nonexpected_item_present = False
            #If one of the non-expected elements missing, then it will break with False
            if nonexpected_item_present == True:
                self.myLogger.error('Non-expected items found: %s' %item)
                break

        if all_matching == True and nonexpected_item_present == False:
            ret = 'SUCCESS'
            comp_result = 'CLI output is matching to the expected output and non-expected items are not present'
            self.logger.info('%s' %comp_result)
        else:
            ret = 'ERROR'
            comp_result = 'CLI output is NOT matching to the expected output or non-expected items are present'
            self.logger.error('%s' %comp_result)

        self.myLogger.debug('leave check_CLI_output function')
        return (ret, comp_result)

    def debug_logger_line_by_line(self,output_lines):
        '''This method creates debug-level logs line-by-line using self.myLogger.debug'''
        for lines in output_lines:
            self.myLogger.debug(lines)
        return

#ADDED
    def run_input_vs_expected(self, login_params, input, expected, nonexpected):
        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        for list_index in range (0,len(input)):

            #Send CLI command
            cmd = '%s %s' %(login_params, input[list_index])
            self.myLogger.debug('Sending CLI command')
            result = self.miscLib.execCommand(cmd)
            self.debug_logger_line_by_line(result[1].splitlines())
            self.fail(result[0],result[1])
            cli_output_lines = result[1].splitlines()

            #Compare cli output to the expected output
            cli_expected_output = eval(expected[list_index])
            cli_nonexpected_output = eval(nonexpected[list_index])
            self.myLogger.debug('Checking CLI output')
            result = self.check_CLI_output(cli_output_lines, cli_expected_output, cli_nonexpected_output)
            print"check_CLI_output result is: %s %s" %(result[0],result[1])
            self.fail(result[0],result[1])
            self.miscLib.waitTime(1)

        return

#END ADDED

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
