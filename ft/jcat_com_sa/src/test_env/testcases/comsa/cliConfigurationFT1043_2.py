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

    TC-FT1043-002 - CLI change configuration - changing an attribute value
    TC-FT1043-003 - CLI change configuration - creating a new object
    TC-FT1043-004 - CLI change configuration - deleting an object and committing the change

    Priority:
    High

    Requirement:
    Run TC-FT1043-001 before running any of the above test cases

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

    cli_input_<number from 1 to 10>
    cli_expected_output_<number from 1 to 10>
    cli_nonexpected_output_<number from 1 to 10>

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
    TC-FT1043-002

    Id:
    "CLI change configuration - changing an attribute value"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-FT1043-003

    Id:
    "CLI change configuration - creating a new object"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-FT1043-004

    Id:
    "CLI change configuration - deleting an object and committing the change"
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import time
import os

class CLIconfigurationFT1043_2(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        # parameters from the config files
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

        self.testOIFile = 'testOI'
        self.killTestOI = 'False'
        self.pathOnTargetSystem = '/home/coremw/incoming/'
        self.testOIRunParams = ''
        self.methodName = ''
        self.serchPatternSyslog1 = ''
        self.serchPatternSyslog2 = ''
        self.serchPatternSyslog3 = ''
        self.serchPatternSyslog4 = ''
        self.serchPatternSyslog5 = ''
        self.serchPatternSyslog6 = ''
        self.twoStepCliExecution = 'False'
        self.cliBreakAt = ''


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

        self.logger.info('Exit setUp')

    def runTest(self):
        self.setTestStep('runTest')
        self.logger.info('runTest')

        #self.lib.messageBox('do a backup here too')
        #self.lib.messageBox('do a backup here too')

        if self.testSuiteConfig.has_key('failedSetUpTestCase') and self.testSuiteConfig['failedSetUpTestCase'] == 'True':
            self.fail('ERROR', 'The setup test case failed, so this test case will not work anyway. Skipping!')

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0],result[1])
        amf_active_SC = result[1]
        subrack, slot = amf_active_SC

        cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    amf_active_SC, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)


        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)
        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        #self.sshLib.setClearNode2prompt(True)

        self.sshLib.tearDownHandles()

        if self.twoStepCliExecution == 'True':
            for list_index in range (0, eval(self.cliBreakAt)):
                result = self.comsa_lib.runCliSession(lists, list_index, cli_active_controller_login_params)
                self.fail(result[0], result[1])

        cmd = 'pgrep %s' %(self.testOIFile)
        result = self.sshLib.sendCommand(cmd, subrack, slot)
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])
        elif result[1] != '':
            cmd = 'pkill %s' %(self.testOIFile)
            result = self.sshLib.sendCommand(cmd, subrack, slot)
            self.fail(result[0], result[1])


        cmd = 'nohup %s%s %s >>nohup.out 2>&1 &' %(self.pathOnTargetSystem, self.testOIFile, self.testOIRunParams) #make a copy of the original model file. This will be restored by the end of the test
        result = self.sshLib.sendCommand(cmd, subrack, slot)
        self.fail(result[0], result[1])

        #get the PID
        cmd = 'pgrep %s' %(self.testOIFile) #make a copy of the original model file. This will be restored by the end of the test
        result = self.sshLib.sendCommand(cmd, subrack, slot)
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])
        elif len(result[1].splitlines()) != 1:
            self.fail('ERROR', 'None or more than one PID found %s. Expecting a single PID as response. Exinting! Pids found: %s' %(self.testOIFile, result[1]))
        else:
            self.pid = result[1]


        cmd = 'kill -usr2 %s' %self.pid
        result = self.sshLib.sendCommand(cmd, subrack, slot)
        self.fail(result[0], result[1])
#        if not 'testOI: Trace is ON' in result[1]:
#            self.fail('ERROR', 'The expected "testOI: Trace is ON" message not received. Exiting!')

        if self.killTestOI == 'True':
            # This is the actual difference compared to the FT1043 functionality.
            # We kill the testOI, but the transactions will still not be possible to commit due to imm not allowing them

            cmd = 'kill %s' %self.pid
            result = self.sshLib.sendCommand(cmd, subrack, slot)
            if result[0] != 'SUCCESS':
                self.fail(result[0], result[1])


        #self.lib.messageBox('start manual testing')
        self.setTestStep('Read configuration via CLI')

        cmd = 'date +\%s'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        startTime = int(result[1])
        self.myLogger.info('The start time is: %s' %str(startTime))

        if self.twoStepCliExecution == 'True':
            startElem = eval(self.cliBreakAt)
        else:
            startElem = 0

        for list_index in range (startElem, len(lists[0])):
            result = self.comsa_lib.runCliSession(lists, list_index, cli_active_controller_login_params)
            self.fail(result[0], result[1])



        #print 'The first search pattern is: ', self.serchPatternSyslog1
        if self.serchPatternSyslog1 != '':
            result = self.lib.getEventTimestampFromSyslog(subrack, slot, eval(self.serchPatternSyslog1), startTime, self.testConfig)
            self.fail(result[0],result[1])
            self.myLogger.info('Match found in syslog at UNIX time: %s' %result[1])

        if self.serchPatternSyslog2 != '':
            result = self.lib.getEventTimestampFromSyslog(subrack, slot, eval(self.serchPatternSyslog2), startTime, self.testConfig)
            self.fail(result[0],result[1])
            self.myLogger.info('Match found in syslog at UNIX time: %s' %result[1])

        if self.serchPatternSyslog3 != '':
            result = self.lib.getEventTimestampFromSyslog(subrack, slot, eval(self.serchPatternSyslog3), startTime, self.testConfig)
            self.fail(result[0],result[1])
            self.myLogger.info('Match found in syslog at UNIX time: %s' %result[1])

        if self.serchPatternSyslog4 != '':
            result = self.lib.getEventTimestampFromSyslog(subrack, slot, eval(self.serchPatternSyslog4), startTime, self.testConfig)
            self.fail(result[0],result[1])
            self.myLogger.info('Match found in syslog at UNIX time: %s' %result[1])

        if self.serchPatternSyslog5 != '':
            result = self.lib.getEventTimestampFromSyslog(subrack, slot, eval(self.serchPatternSyslog5), startTime, self.testConfig)
            self.fail(result[0],result[1])
            self.myLogger.info('Match found in syslog at UNIX time: %s' %result[1])

        if self.serchPatternSyslog6 != '':
            result = self.lib.getEventTimestampFromSyslog(subrack, slot, eval(self.serchPatternSyslog6), startTime, self.testConfig)
            self.fail(result[0],result[1])
            self.myLogger.info('Match found in syslog at UNIX time: %s' %result[1])

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.myLogger.info('tearDown')

        cmd = 'kill %s' %self.pid
        result = self.sshLib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])

        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info('exit tearDown')


        #########################
        #### SUPPORT METHODS ####
        #########################


    def getEventTimestampFromComLog(self, subrack, slot, searchPatterns, startTime, logPattern , logDir):
        '''
        This method will return the timestamp of all the events in which the elements of the search pattern were found.

        The method only returns the matches that occued after the startTime (defined in unix time)

        Main steps:
        1. select relevant syslog file based on the time stamp of the first entry in the syslog
        2. search occurencies of the event defined by the search patterns
        3. remove matches from before the startTime
        4. returns a list of unix times of the events found

        Arguments:
        int subrack
        int slot
        list [searchPatterns]
        int startTime (unix time)

        Returns
        ('ERROR', 'error message')
        ('SUCCESS', [list of ints representing unix times])
        '''

        self.myLogger.debug('enter getEventTimestampFromComLog()')

    # 1. select relevant syslog files based on the time stamp of the first entry in the syslog

        cmd = 'ls -t %s | grep %s' %(logDir, logPattern)
        result = self.sshLib.sendCommand(cmd)
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave getEventTimestampFromComLog()')
            return result
        messagesFiles = result[1].splitlines()
        messagesFile = ''
        for messageFile in messagesFiles:
            result = self.sshLib.sendCommand("""head -1 %s/%s | awk '{print $2" "$3}'"""%(logDir, messageFile))
            if result[0] != 'SUCCESS':
                self.myLogger.debug('leave getEventTimestampFromComLog()')
                return result
            result = self.lib.timeConv(result[1])
            if result[0] != 'SUCCESS':
                self.myLogger.debug('leave getEventTimestampFromComLog()')
                return result
            unixTime = result[1]
            if unixTime < startTime:
                messagesFile = messageFile
                break

        if messagesFile == '':
            messagesFile = messagesFiles[len(messagesFiles)-1]
            self.myLogger.warn('No syslog file found with log begin before defined startTime. Start parsing from oldest to newest log file!')
            #return ('ERROR', 'No syslog file found with log begin before defined startTime')

        messagesFilesConsidered =  messagesFiles[:messagesFiles.index(messagesFile)+1]
        messagesFilesConsidered.reverse()

    # 2. search occurencies of the component getting active state
        if "type 'list'" not in str(type(searchPatterns)):
            self.myLogger.error('The search patterns were not defined in a list. It must be specified in a list of strings.')
            self.myLogger.debug('leave getEventTimestampFromComLog()')
            return ('ERROR', 'The search patterns were not defined in a list. It must be specified in a list of strings.')
        if len(searchPatterns) == 0:
            self.myLogger.error('The search pattern list is empty. Nothing to search for!')
            self.myLogger.debug('leave getEventTimestampFromComLog()')
            return ('ERROR', 'The search pattern list is empty. Nothing to search for!')


        readableTimes = []
        for messagesFile in messagesFilesConsidered:
            cmd = """grep -i "%s" %s/%s""" %(searchPatterns[0], logDir, messagesFile)
            if len(searchPatterns) > 1:
                for i in range(len(searchPatterns)-1):
                    cmd += """| grep -i "%s" """ %(searchPatterns[i+1])
            cmd += """| awk '{print $2" "$3}'"""
            result = self.sshLib.sendCommand(cmd)
            if result[0] != 'SUCCESS':
                self.myLogger.debug('leave getEventTimestampFromComLog()')
                return result
            if result[1] != '':
                tempList = result[1].splitlines()
                for element in tempList:
                    readableTimes.append(element)


        if len(readableTimes) == 0:
            self.myLogger.debug('leave getEventTimestampFromComLog()')
            return ('ERROR', 'No entry found in the LOG for the following search pattern: %s' %str(searchPatterns))

        unixTimes = []
        for readableTime in readableTimes:
            result = self.lib.timeConv(readableTime)
            if result[0] != 'SUCCESS':
                self.myLogger.debug('leave getEventTimestampFromComLog()')
                return result
            unixTimes.append(result[1])

    # 3. remove matches from before the startTime
        timesAfterStartTime = []
        for unixTime in unixTimes:
            if unixTime >= startTime:
                timesAfterStartTime.append(unixTime)

        if len(timesAfterStartTime) == 0:
            return ('ERROR', 'No entry found in the LOG after the start time for the following search pattern: %s' %str(searchPatterns))
        else:
            result = ('SUCCESS', timesAfterStartTime)


        self.myLogger.debug('leave getEventTimestampFromComLog()')
        return result




def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
