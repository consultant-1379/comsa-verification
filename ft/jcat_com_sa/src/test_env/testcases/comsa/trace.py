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


    TC-MISC-025 - COMSA, PMTSA enable trace
    TC-MISC-026 - COMSA, PMTSA disable trace

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

    Restore:
    N/A

    Description:

    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MISC-025

    Id:
    "COMSA, PMTSA enable trace"
    ==================================
    Tag:
    TC-MISC-026

    Id:
    "COMSA, PMTSA disable trace"
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import os

class Trace(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        # parameters from the config files

        self.configFile  = {}

        self.ntfsendMsg = ""

        self.expectedComSA_debug = {}
        self.unexpectedComSA_debug = {}

        self.expectedPmtSA_debug = {}
        self.unexpectedPmtSA_debug = {}

        self.expectedComSA_enter_leave = {}
        self.unexpectedComSA_enter_leave = {}

        self.expectedPmtSA_enter_leave = {}
        self.unexpectedPmtSA_enter_leave = {}

        self.enableOnly = ''
        self.disableOnly = ''
        self.testOnly = ''

        self.startTimeSyslog = 0
        self.startTimeTracelog = 0

        self.syslogCheckFlag = True
        self.comsaFlag = True

        self.reqComSaRelease = "3"
        self.reqComSaVersion = "R3K01"

        self.syslogDir = '/var/log/'
        self.tracelogDir = '/var/opt/comsa/'
        self.configFile_tempdir = '/home/trace/'
        self.configFilePathOnTarget = '/storage/clear/comsa_for_coremw-apr9010555/'

        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.comsaForCoreMW = dict.get("COMSA_FOR_COREMW")

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

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

        self.logger.info('Exit setUp')

    def runTest(self):
        self.skip_test = False

        self.setTestStep('Check the required versions of ComSA is installed')
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
        self.fail(ComsaOK[0],ComsaOK[1])

        if ComsaOK[1]:
            self.logger.info('runTest')
            """
            # Create temporary directory on target
            self.setTestStep("### Create temporary directory on target")
            cmd = 'mkdir -p %s' %self.configFile_tempdir
            self.myLogger.debug('Create temporary directory on target: %s' %cmd)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # Copy com_sa_trace.conf on target to temporary directory on target
            self.setTestStep("### Copy com_sa_trace.conf on target to temporary directory on target")
            cmd = '\cp %s%s %s' %(self.configFilePathOnTarget,self.configFile, self.configFile_tempdir)
            self.myLogger.debug('Copy com_sa_trace.conf on target to temporary directory on target')
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            """
            # Work around in case cluster reboot (somewhere in the past), and cause /var/opt/comsa is lost.
            cmd = 'mkdir -p /var/opt/comsa'
            result = self.sshLib.sendCommand(cmd)

            # Modify com_sa_trace.conf on target
            self.setTestStep("### Modify com_sa_trace.conf on target")
            if self.enableOnly == 'True':
                cmd = 'sed -i s/COMSA_GLOBAL_TRACE=disable/COMSA_GLOBAL_TRACE=enable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                self.myLogger.debug('Modify COMSA_GLOBAL_TRACE to enable')
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                cmd = 'sed -i s/COMSA_TRACE_GROUP_01=disable/COMSA_TRACE_GROUP_01=enable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                self.myLogger.debug('Modify COMSA_TRACE_GROUP_01 to enable')
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
            if self.disableOnly == 'True':
                cmd = 'sed -i s/COMSA_GLOBAL_TRACE=enable/COMSA_GLOBAL_TRACE=disable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                self.myLogger.debug('Modify COMSA_GLOBAL_TRACE to disable')
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                cmd = 'sed -i s/COMSA_TRACE_GROUP_01=enable/COMSA_TRACE_GROUP_01=disable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                self.myLogger.debug('Modify COMSA_TRACE_GROUP_01 to disable')
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

            # Waiting for 21 seconds for the trace enable take effect
            self.miscLib.waitTime(21)

            # Getting Linux System Time
            self.setTestStep("### Getting Linux System Time")

            # Getting Linux Time for matching the string in syslog
            dateCommandSyslog = "date +%s"
            result = self.sshLib.sendCommand(dateCommandSyslog)
            self.fail(result[0],result[1])
            self.startTimeSyslog = int(result[1])
            self.myLogger.info("Linux System Time for matching string in syslog is: %s" %(self.startTimeSyslog))

            # Getting Linux Time for matching the string in tracelog
            dateCommandTracelog = "date +%s.%6N"
            result = self.sshLib.sendCommand(dateCommandTracelog)
            self.fail(result[0],result[1])
            self.startTimeTracelog = (result[1])
            self.myLogger.info("Linux System Time for matching string in tracelog is: %s" %(self.startTimeTracelog))

            # Com switch over
            self.setTestStep("### Com switchover")
            cmd = "pgrep -f 'etc/com.cfg'"
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            comPid1=result[1]

            cmd = 'comsa-mim-tool com_switchover'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            self.miscLib.waitTime(10)

            cmd = "pgrep -f 'etc/com.cfg'"
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            comPid2=result[1]

            if comPid1 == comPid2:
                self.fail('ERROR', 'COM has same PID before and after the comsa-mim-tool com_switchover')

            if self.ntfsendMsg != "":
                result = self.sshLib.sendCommand(self.ntfsendMsg)
                self.fail(result[0], result[1])
            # Search pattern
            self.setTestStep("### Check text in logs")
            if self.enableOnly == 'True' or self.testOnly == 'True':
                self.expectedLogs()
            if self.disableOnly == 'True':
                self.unexpectedLogs()

            coreTestCase.CoreTestCase.runTest(self)

        else:
            self.logger.info('Skipped trace tests because of COMSA version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True

    def tearDown(self):
        self.setTestStep('tearDown')

        """
        if self.skip_test == False:
            # Copy com_sa_trace.conf on temporary directory to old position on target
            self.setTestStep("### Copy com_sa_trace.conf on temporary directory to old position on target")
            cmd = '\cp %s%s %s' %(self.configFile_tempdir,self.configFile , self.configFilePathOnTarget)
            self.myLogger.debug('Copy com_sa_trace.conf on target to temporary directory on target')
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # Delete temporary directory
            self.setTestStep("### Delete temporary directory")
            cmd = '\\rm -rf %s' %self.configFile_tempdir
            self.myLogger.debug('Delete temporary directory')
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

        else:
            self.myLogger.info('Teardown skipped')
        """
        coreTestCase.CoreTestCase.tearDown(self)

        #########################
        #### SUPPORT METHODS ####
        #########################

    def expectedLogs(self):
        if self.expectedPmtSA_enter_leave != {}:
            self.comsaFlag = False
            self.syslogCheckFlag = False
            self.evaluateExpectedSearchPattern([self.expectedPmtSA_enter_leave], self.startTimeTracelog, self.comsaFlag, self.tracelogDir)
        if self.expectedComSA_enter_leave != {}:
            self.comsaFlag = True
            self.evaluateExpectedSearchPattern([self.expectedComSA_enter_leave], self.startTimeTracelog, self.comsaFlag, self.tracelogDir)
        # Wait 10 seconds for switchover
        self.miscLib.waitTime(10)
        if self.expectedComSA_debug != {}:
            self.syslogCheckFlag = True
            self.evaluateExpectedSearchPattern([self.expectedComSA_debug], self.startTimeSyslog, self.comsaFlag, self.syslogDir)
        if self.expectedPmtSA_debug != {}:
            self.evaluateExpectedSearchPattern([self.expectedPmtSA_debug], self.startTimeSyslog, self.comsaFlag, self.syslogDir)

    def unexpectedLogs(self):
        if self.unexpectedPmtSA_enter_leave != {}:
            self.comsaFlag = False
            self.syslogCheckFlag = False
            self.evaluateUnexpectedSearchPattern([self.unexpectedPmtSA_enter_leave], self.startTimeTracelog, self.comsaFlag, self.tracelogDir)
        if self.unexpectedComSA_enter_leave != {}:
            self.comsaFlag = True
            self.evaluateUnexpectedSearchPattern([self.unexpectedComSA_enter_leave], self.startTimeTracelog, self.comsaFlag, self.tracelogDir)
        if self.unexpectedComSA_debug != {}:
            self.syslogCheckFlag = True
            self.evaluateUnexpectedSearchPattern([self.unexpectedComSA_debug], self.startTimeSyslog, self.comsaFlag, self.syslogDir)
        if self.unexpectedPmtSA_debug != {}:
            self.evaluateUnexpectedSearchPattern([self.unexpectedPmtSA_debug], self.startTimeSyslog, self.comsaFlag, self.syslogDir)

    def evaluateExpectedSearchPattern(self, searchPattern, startTimeSyslog, comsaFlag, logDir):
        if self.syslogCheckFlag == True:
            result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, self.startTimeSyslog, self.testConfig, logDir)
        else:
            result = self.comsa_lib.getEventTimestampFromTracelog(self.activeController[0], self.activeController[1], searchPattern, self.startTimeTracelog, self.testConfig, comsaFlag, logDir)
        self.sshLib.tearDownHandles()
        self.fail(result[0],result[1])
        self.myLogger.debug('Found %s in log at: %s' %(searchPattern,result[1]))

    def evaluateUnexpectedSearchPattern(self, searchPattern, startTimeSyslog, comsaFlag, logDir):
        if self.syslogCheckFlag == True:
            result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, self.startTimeSyslog, self.testConfig, logDir)
        else:
            result = self.comsa_lib.getEventTimestampFromTracelog(self.activeController[0], self.activeController[1], searchPattern, self.startTimeTracelog, self.testConfig, comsaFlag, logDir)
        self.sshLib.tearDownHandles()
        if (result[0] == "SUCCESS"):
            self.myLogger.error("Unexpected pattern found: %s" %searchPattern)

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases

