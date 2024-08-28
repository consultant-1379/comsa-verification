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
import copy
import re
import time
import os
from org.apache.log4j import Logger
from java.lang import System


logger = None

class FTSdp556(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.AlarmLogFileName_ExpectedValue = 'FmAlarmLog'

        self.testCompAlarmLogText = ""
        self.testCompAlertLogText = ""
        self.copyTestCompToTarget = "NO"
        self.comsaLogCfgTestFile = ''
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.createComSaConfigFile = ''
        self.restartCluster = ''
        self.faultyComSaConfigFile = ''
        self.test_config= testConfig
        self.testcase_tag = tag

        self.reqComSaVersion = "R1A01"
        self.reqComVersion = "R6A01"
        self.reqCmwVersion = "R5A04"
        self.reqComSaRelease = "3"
        self.reqComRelease = "2"
        self.reqCmwRelease = "1"

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
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.FmAlarmLogPath = dict.get("FM_ALARM_LOG_PATH")
        self.FmAlertLogPath = dict.get("FM_ALERT_LOG_PATH")
        self.comsaLogCfgFilePath = dict.get("COMSA_FOR_COREMW")
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

        global logger
        #self.logger = Logger.getLogger('comsa_lib')
        logger = Logger.getLogger('comsa_lib')
        self.myLogger.info('Exit setUp')

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

    def runTest(self):
        self.logger.info('runTest')

        self.setTestStep('Check the required versions of ComSA, Com and CMW is installed')
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
        self.fail(ComsaOK[0],ComsaOK[1])
        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion )
        self.fail(ComOK[0],ComOK[1])
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
        self.fail(CmwOK[0],CmwOK[1])


        if ComsaOK[1] and ComOK[1] and CmwOK[1]:

            self.setTestStep('runTest')

            if self.installStressTool:
                self.setTestStep('======== Install the stress tool ========')
                self.comsa_lib.installStressToolOnTarget(self)
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

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM
                # 2 local disk tasks writing 4 MB, NFS disk stress 1 task writing 64K bytes
                #result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

                # No CPU, only local and NFS disk
                #result = self.comsa_lib.startStressToolOnTarget(self, 0, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

                # 50% CPU, 50% memory plus local and NFS disk stress
                result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

                # 50% CPU, 50% memory plus NFS disk stress
                #result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            self.restart_COM_cmd = 'comsa-mim-tool com_switchover'
            self.comRestartWaitTime = 10
            self.startUnixTime = 0

            self.target_com_compdir = '/opt/com/lib/comp/'
            self.testCompName = "testComp556.so"
            configDir_path = '%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles)
            self.testComp_path = '%s%s'  %(configDir_path, self.testCompName)

            self.comsaLogCfgFileName = 'com_sa_log.cfg'


            self.FmAlarmLog_DefaultCfgFileName ='FmAlarmLog.cfg'
            self.FmAlertLog_DefaultCfgFileName ='FmAlertLog.cfg'

            #Defining the parameter names for com_sa_log.cfg
            self.AlarmLogFileNameText = "AlarmLogFileName"
            self.AlertLogFileNameText = "AlertLogFileName"
            self.AlarmFilesRotatedText = "AlarmFilesRotated"
            self.AlertFilesRotatedText = "AlertFilesRotated"
            self.AlarmMaxLogFileSizeText = "AlarmMaxLogFileSize"
            self.AlertMaxLogFileSizeText = "AlertMaxLogFileSize"

            self.Alarm_LOG_SVC_VERSION_Text = "LOG_SVC_VERSION"
            self.Alarm_FORMAT_Text = "FORMAT"
            self.Alarm_MAX_FILE_SIZE_Text = "MAX_FILE_SIZE"
            self.Alarm_FIXED_LOG_REC_SIZE_Text = "FIXED_LOG_REC_SIZE"
            self.Alarm_LOG_FULL_ACTION_Text = "LOG_FULL_ACTION"
            self.Alarm_LOG_SVC_VERSION_Value = ""
            self.Alarm_FORMAT_Value = ""
            self.Alarm_MAX_FILE_SIZE_Value = ""
            self.Alarm_FIXED_LOG_REC_SIZE_Value = ""
            self.Alarm_LOG_FULL_ACTION_Value = ""

            self.Alert_LOG_SVC_VERSION_Text = "LOG_SVC_VERSION"
            self.Alert_FORMAT_Text = "FORMAT"
            self.Alert_MAX_FILE_SIZE_Text = "MAX_FILE_SIZE"
            self.Alert_FIXED_LOG_REC_SIZE_Text = "FIXED_LOG_REC_SIZE"
            self.Alert_LOG_FULL_ACTION_Text = "LOG_FULL_ACTION"
            self.Alert_LOG_SVC_VERSION_Value = ""
            self.Alert_FORMAT_Value = ""
            self.Alert_MAX_FILE_SIZE_Value = ""
            self.Alert_FIXED_LOG_REC_SIZE_Value = ""
            self.Alert_LOG_FULL_ACTION_Value = ""

            self.lastAlarmLogFileName = ""
            self.lastAlertLogFileName = ""
            self.lastAlarmCfgFileName = ""
            self.lastAlertCfgFileName = ""

    ####################################################################################################################
            self.noOfScs = len(self.testConfig['controllers'])
            self.findActiveAndStandbyController()
            self.fixLastLine()

    ####################################################################################################################
    ###########################     Test cases: from TC-FT556-001 to TC-FT556-008    ###################################
    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-001':
                self.checkSystemConfig()

    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-002':
                # this will call TC-FT556-001 inside
                self.loadTestComponent_and_checkLogWriting()

    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-003':
                self.modifyComSaLogCfgFile(self.comsaLogCfgTestFile)
                self.loadTestComponent_and_checkLogWriting()

    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-004':
                self.modifyComSaLogCfgFile(self.comsaLogCfgTestFile)
                self.loadTestComponent_and_checkLogWriting()

    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-005':
                self.modifyComSaLogCfgFile(self.comsaLogCfgTestFile)
                self.loadTestComponent_and_checkLogWriting()

    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-006':
                if self.noOfScs == 2:
                    self.removeTestCompFromActiveSC()
                    self.copyTestCompToStandbySC()
                    self.switchOver()
                    self.findActiveAndStandbyController()
                    #self.fixLastLine()
                    self.loadTestComponent_and_checkLogWriting()
                elif self.noOfScs == 1:
                    self.setAdditionalResultInfo('Switch-over is not valid for single node clusters.')

    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-007':
                self.setTestStep('Cluster reboot')
                result = self.comsa_lib.restartCluster(self.testConfig, self.linuxDistro, self.distroTypes)
                if self.noOfScs == 2:
                    self.copyTestCompToActiveSC()
                    self.copyTestCompToStandbySC()
                elif self.noOfScs == 1:
                    self.copyTestCompToActiveSC()
                self.findActiveAndStandbyController()
                #self.fixLastLine()
                self.loadTestComponent_and_checkLogWriting()

    ####################################################################################################################

            if self.testcase_tag == 'TC-FT556-008':
                # Restore back the original com_sa_log.cfg file by removing it and restarting COM
                self.removeComSaLogCfgFile()
                # remove test component from both of the SCs
                self.removeTestCompFromActiveSC()
                if self.noOfScs == 2:
                    self.removeTestCompFromStandbySC()
                '''
                restart COM to:
                    -get back the original com_sa_log.cfg file
                    -to unload test component
                '''
                self.restartCom()

    ####################################################################################################################

        else:
            self.logger.info('Skipped SDP556 tests because of COMSA/COM/CMW version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")

    def tearDown(self):
        self.setTestStep('tearDown')
        '''
        Here we don't do anything.
        We do the cleaning in cleanup-testcase.
        The reason is, we don't want to remove test component and restart COM after each TC, because:
        -we need to check the alarm and alert logs and cfg files after each restart of COM (we don't want to check again during teardown)
        -this solution results faster TC run
        '''

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

    def findActiveAndStandbyController(self):
        self.setTestStep('Find active and standby controllers')
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

        if self.noOfScs == 2:
            self.standbySubrack = standbyController[0]
            self.standbySlot =    standbyController[1]
            self.standbyController = (standbyController[0], standbyController[1])
            self.myLogger.info('standby controller param: (%s,%s)' %(str(self.standbySubrack), str(self.standbySlot)) )

        return


    def checkAlarmAndAlertCfgFiles(self):
        self.setTestStep('Checking alarm and alert config files - comparing to %s file' %self.comsaLogCfgFileName)

        # read and parse parameters from com_sa_log.cfg
        cmd = 'cat %s%s' %(self.comsaLogCfgFilePath,self.comsaLogCfgFileName)
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        lines = result[1].splitlines()
        # predefinition is needed, because python can crash in a negative case where there is no value given at all in the for loop
        AlarmLogFileNameValue    = ''
        AlertLogFileNameValue    = ''
        AlarmFilesRotatedValue   = ''
        AlertFilesRotatedValue   = ''
        AlarmMaxLogFileSizeValue = ''
        AlertMaxLogFileSizeValue = ''

        for line in lines:
            tempList = line.split('=')

            if tempList[0] == self.AlarmLogFileNameText:
                AlarmLogFileNameValue = tempList[1]
                self.myLogger.info('Found %s=%s         in %s' %(self.AlarmLogFileNameText,AlarmLogFileNameValue,self.comsaLogCfgFileName))
            if tempList[0] == self.AlertLogFileNameText:
                AlertLogFileNameValue = tempList[1]
                self.myLogger.info('Found %s=%s         in %s' %(self.AlertLogFileNameText,AlertLogFileNameValue,self.comsaLogCfgFileName))
            if tempList[0] == self.AlarmFilesRotatedText:
                AlarmFilesRotatedValue = tempList[1]
                self.myLogger.info('Found %s=%s         in %s' %(self.AlarmFilesRotatedText,AlarmFilesRotatedValue,self.comsaLogCfgFileName))
            if tempList[0] == self.AlertFilesRotatedText:
                AlertFilesRotatedValue = tempList[1]
                self.myLogger.info('Found %s=%s         in %s' %(self.AlertFilesRotatedText,AlertFilesRotatedValue,self.comsaLogCfgFileName))
            if tempList[0] == self.AlarmMaxLogFileSizeText:
                AlarmMaxLogFileSizeValue = tempList[1]
                self.myLogger.info('Found %s=%s         in %s' %(self.AlarmMaxLogFileSizeText,AlarmMaxLogFileSizeValue,self.comsaLogCfgFileName))
            if tempList[0] == self.AlertMaxLogFileSizeText:
                AlertMaxLogFileSizeValue = tempList[1]
                self.myLogger.info('Found %s=%s         in %s' %(self.AlertMaxLogFileSizeText,AlertMaxLogFileSizeValue,self.comsaLogCfgFileName))
        AlarmLogFileNameValue = AlarmLogFileNameValue + ".cfg"
        AlertLogFileNameValue = AlertLogFileNameValue + ".cfg"

        # check if FmAlarm/FmAlert cfg files have the right name by comparing to the names found in com_sa_log.cfg
        self.refreshLastCfgFileNames()
        if AlarmLogFileNameValue == self.lastAlarmCfgFileName:
            self.myLogger.debug('(%s) = (%s)' %(AlarmLogFileNameValue,self.lastAlarmCfgFileName))
        else:
            self.fail('ERROR', 'name of alarm log cfg file is not matching to parameter found in com_sa_log.cfg: (%s) != (%s)' %(AlarmLogFileNameValue,result[1]))

        if AlertLogFileNameValue == self.lastAlertCfgFileName:
            self.myLogger.debug('(%s) = (%s)' %(AlertLogFileNameValue,self.lastAlertCfgFileName))
        else:
            self.fail('ERROR', 'name of alert log cfg file is not matching to parameter found in com_sa_log.cfg: (%s) != (%s)' %(AlertLogFileNameValue,result[1]))


        # read and compare parameters from FmAlarm config with parameters from com_sa_log.cfg file
        cmd = 'cat %s%s' %(self.FmAlarmLogPath,self.lastAlarmCfgFileName)
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        self.checkFileExists(str(result[1]))
        lines = result[1].splitlines()
        for line in lines:
            tempList = line.split(':')
            tempStr = str(tempList[1]).lstrip()

            if tempList[0] == self.Alarm_LOG_SVC_VERSION_Text:
                self.Alarm_LOG_SVC_VERSION_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alarm_LOG_SVC_VERSION_Text,self.Alarm_LOG_SVC_VERSION_Value,self.FmAlarmLogPath,self.FmAlarmLog_DefaultCfgFileName))
            if tempList[0] == self.Alarm_FORMAT_Text:
                self.Alarm_FORMAT_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alarm_FORMAT_Text,self.Alarm_FORMAT_Value,self.FmAlarmLogPath,self.FmAlarmLog_DefaultCfgFileName))
            if tempList[0] == self.Alarm_MAX_FILE_SIZE_Text:
                self.Alarm_MAX_FILE_SIZE_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alarm_MAX_FILE_SIZE_Text,self.Alarm_MAX_FILE_SIZE_Value,self.FmAlarmLogPath,self.FmAlarmLog_DefaultCfgFileName))
            if tempList[0] == self.Alarm_FIXED_LOG_REC_SIZE_Text:
                self.Alarm_FIXED_LOG_REC_SIZE_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alarm_FIXED_LOG_REC_SIZE_Text,self.Alarm_FIXED_LOG_REC_SIZE_Value,self.FmAlarmLogPath,self.FmAlarmLog_DefaultCfgFileName))
            if tempList[0] == self.Alarm_LOG_FULL_ACTION_Text:
                self.Alarm_LOG_FULL_ACTION_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alarm_LOG_FULL_ACTION_Text,self.Alarm_LOG_FULL_ACTION_Value,self.FmAlarmLogPath,self.FmAlarmLog_DefaultCfgFileName))

        # left side: alarm log cfg          right side: com_sa_log.cfg
        if self.Alarm_MAX_FILE_SIZE_Value == AlarmMaxLogFileSizeValue:
            self.myLogger.debug('(%s) = (%s)' %(self.Alarm_MAX_FILE_SIZE_Value,AlarmMaxLogFileSizeValue))
        else:
            self.fail('ERROR', 'parameters in alarm log cfg file are not matching to parameters in com_sa_log.cfg: (%s) != (%s)' %(self.Alarm_MAX_FILE_SIZE_Value,AlarmMaxLogFileSizeValue))
        if self.Alarm_LOG_FULL_ACTION_Value == ("ROTATE " + AlarmFilesRotatedValue):
            self.myLogger.debug('(%s) = (%s)' %(self.Alarm_LOG_FULL_ACTION_Value,AlarmFilesRotatedValue))
        else:
            self.fail('ERROR', 'parameters in alarm log cfg file are not matching to parameters in com_sa_log.cfg: (%s) != (%s)' %(self.Alarm_LOG_FULL_ACTION_Value,AlarmFilesRotatedValue))

        # read and compare parameters from FmAlert config with parameters from com_sa_log.cfg file
        cmd = 'cat %s%s' %(self.FmAlertLogPath,self.lastAlertCfgFileName)
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        self.checkFileExists(str(result[1]))
        lines = result[1].splitlines()
        for line in lines:
            tempList = line.split(':')
            tempStr = str(tempList[1]).lstrip()

            if tempList[0] == self.Alert_LOG_SVC_VERSION_Text:
                self.Alert_LOG_SVC_VERSION_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alert_LOG_SVC_VERSION_Text,self.Alert_LOG_SVC_VERSION_Value,self.FmAlertLogPath,self.FmAlertLog_DefaultCfgFileName))
            if tempList[0] == self.Alert_FORMAT_Text:
                self.Alert_FORMAT_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alert_FORMAT_Text,self.Alert_FORMAT_Value,self.FmAlertLogPath,self.FmAlertLog_DefaultCfgFileName))
            if tempList[0] == self.Alert_MAX_FILE_SIZE_Text:
                self.Alert_MAX_FILE_SIZE_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alert_MAX_FILE_SIZE_Text,self.Alert_MAX_FILE_SIZE_Value,self.FmAlertLogPath,self.FmAlertLog_DefaultCfgFileName))
            if tempList[0] == self.Alert_FIXED_LOG_REC_SIZE_Text:
                self.Alert_FIXED_LOG_REC_SIZE_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alert_FIXED_LOG_REC_SIZE_Text,self.Alert_FIXED_LOG_REC_SIZE_Value,self.FmAlertLogPath,self.FmAlertLog_DefaultCfgFileName))
            if tempList[0] == self.Alert_LOG_FULL_ACTION_Text:
                self.Alert_LOG_FULL_ACTION_Value = tempStr
                self.myLogger.info('Found %s: %s         in %s%s' %(self.Alert_LOG_FULL_ACTION_Text,self.Alert_LOG_FULL_ACTION_Value,self.FmAlertLogPath,self.FmAlertLog_DefaultCfgFileName))

        if self.Alert_MAX_FILE_SIZE_Value == AlertMaxLogFileSizeValue:
            self.myLogger.debug('(%s) = (%s)' %(self.Alert_MAX_FILE_SIZE_Value,AlertMaxLogFileSizeValue))
        else:
            self.fail('ERROR', 'parameters in alert log cfg file are not matching to parameters in com_sa_log.cfg: (%s) != (%s)' %(self.Alert_MAX_FILE_SIZE_Value,AlertMaxLogFileSizeValue))
        if self.Alert_LOG_FULL_ACTION_Value == ("ROTATE " + AlertFilesRotatedValue):
            self.myLogger.debug('(%s) = (%s)' %(self.Alert_LOG_FULL_ACTION_Value,AlertFilesRotatedValue))
        else:
            self.fail('ERROR', 'parameters in alert log cfg file are not matching to parameters in com_sa_log.cfg: (%s) != (%s)' %(self.Alert_LOG_FULL_ACTION_Value,AlertFilesRotatedValue))

        self.myLogger.debug('leave checkAlarmAndAlertCfgFiles function')
        return

    def loadTestComponent_and_checkLogWriting(self):
        if self.copyTestCompToTarget == "YES":
            self.setTestStep('Load test component')
            self.copyTestCompToActiveSC()
        # save Unix time before restarting COM
        self.startUnixTime = self.getCurrentUnixTime()
        # restart COM here
        self.restartCom()
        # Run TC-FT556-001 again
        self.checkSystemConfig()
        self.checkLogWrite()
        return

    def checkLogWrite(self):
        self.setTestStep('Checking the alarm/alert logs if they have the text coming from the test component')


        # The build machine at DEK (Ubuntu Vbox) appears to be slower than the one used at EAB (SuSE)
        # Determine on which server we run using the same method as in 'sourceme.tcsh'
        self.myLogger.debug('Get the host type')
        cmd = 'test -f /etc/SuSE-release ; echo $?'
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        eabHost = int(result[1])
        if eabHost == 0:
            self.myLogger.info('This test is running at EAB SuSE server')
        else:
            self.myLogger.info('This test is NOT running at EAB SuSE server')

        # The delay is needed even in the vSphere targets, so we enable it for all test executions
        #if eabHost == 1:
        #self.myLogger.info('Extra delay needed at DEK server only ...')
        coremwLogWriteDelay = 40 # seconds to wait - may need to be fine tuned.
        self.logger.info('Wait for %s seconds for CoreMW to write to the log...' %coremwLogWriteDelay)
        self.miscLib.waitTime(coremwLogWriteDelay)

        searchPatterns = ['testComp556', 'Alarm test log']
        result = self.comsa_lib.getEventTimestampFromAlarmAlertLog(self.activeSubrack,self.activeSlot, searchPatterns, self.startUnixTime, \
                                                                   self.testConfig, facility = 'alarm')
        self.fail(result[0], result[1])

        searchPatterns = ['testComp556', 'Alert test log']
        result = self.comsa_lib.getEventTimestampFromAlarmAlertLog(self.activeSubrack,self.activeSlot, searchPatterns, self.startUnixTime, \
                self.testConfig, facility = 'alert')
        self.fail(result[0], result[1])

        return

    def checkIfNoTimeStamp(self,result,text):
        if len(result) < 10:
            self.fail('ERROR', '%s not found in log' %text)
        return

    def checkFileExists(self,text):
        if "No such file or directory" in text:
            self.fail('ERROR', text)
        else:
            self.myLogger.info('command result: (%s)' %text)
        return

    def getCurrentUnixTime(self):
        self.myLogger.debug('entering getCurrentUnixTime()')
        cmd = 'date +%s'
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        currentUnixTime = int(result[1])
        self.myLogger.info('Current Unix time is: (%i)' %currentUnixTime)
        self.myLogger.debug('leaving getCurrentUnixTime()')
        # return type is integer
        return currentUnixTime

    def getLastAlarmLogFileName(self):
        cmd = 'cd %s;ls -t *.log | head -1' %self.FmAlarmLogPath
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        self.myLogger.info('Last modified Alarm log file name is: (%s)'%result[1])
        return result[1]

    def getLastAlertLogFileName(self):
        cmd = 'cd %s;ls -t *.log | head -1' %self.FmAlertLogPath
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        self.myLogger.info('Last modified Alert log file name is: (%s)'%result[1])
        return result[1]

    def getLastAlarmCfgFileName(self):
        cmd = 'cd %s;ls -t *.cfg | head -1' %self.FmAlarmLogPath
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        self.myLogger.info('Last modified Alarm cfg file name is: (%s)'%result[1])
        return result[1]

    def getLastAlertCfgFileName(self):
        cmd = 'cd %s;ls -t *.cfg | head -1' %self.FmAlertLogPath
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        self.myLogger.info('Last modified Alert cfg file name is: (%s)'%result[1])
        return result[1]

    def checkSystemConfig(self):
        self.checkAlarmAndAlertCfgFiles()
        self.refreshLastLogFileNames()
        self.cliTest()
        return

    def refreshLastLogFileNames(self):
        self.lastAlarmLogFileName = self.getLastAlarmLogFileName()
        self.lastAlertLogFileName = self.getLastAlertLogFileName()
        return

    def refreshLastCfgFileNames(self):
        self.lastAlarmCfgFileName = self.getLastAlarmCfgFileName()
        self.lastAlertCfgFileName = self.getLastAlertCfgFileName()
        return

    def copyTestCompToActiveSC(self):
        self.setTestStep('Copy test component to active SC')
        self.sshLib.setConfig(self.activeSubrack,self.activeSlot,self.activeSlot)
        self.myLogger.debug('Copy testcomp to target under: %s' %self.target_com_compdir)
        result = self.sshLib.remoteCopy(self.testComp_path, self.target_com_compdir, timeout = 60)
        self.fail(result[0],result[1])
        #Change permission of copied files to guarantee COM can get the sufficient permission.
        cmd = 'chmod 777 %s%s'%(self.target_com_compdir, self.testCompName)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])
        return

    def copyTestCompToStandbySC(self):
        self.setTestStep('Copy test component to standby SC')
        if self.noOfScs == 1:
            self.fail('ERROR', 'Running on a one-node configuration. \
            We should not have ended up in the copyTestCompToStandbySC method.')
        self.sshLib.setConfig(self.standbySubrack,self.standbySlot,self.standbySlot)
        self.myLogger.debug('Copy testcomp to target under: %s' %self.target_com_compdir)
        result = self.sshLib.remoteCopy(self.testComp_path, self.target_com_compdir, timeout = 60)
        self.fail(result[0],result[1])
        #Change permission of copied files to guarantee COM can get the sufficient permission.
        cmd = 'chmod 777 %s%s'%(self.target_com_compdir, self.testCompName)
        result = self.sshLib.sendCommand(cmd, self.standbyController[0], self.standbyController[1])
        self.fail(result[0],result[1])
        # set back the config to the active
        self.sshLib.setConfig(self.activeSubrack,self.activeSlot,self.activeSlot)
        return

    def removeTestCompFromActiveSC(self):
        self.setTestStep('Deleting test component from active SC')
        cmd = '\\rm -f %s%s' %(self.target_com_compdir,self.testCompName)
        self.myLogger.debug('tearDown: Delete %s by: %s' %(self.testCompName, cmd))
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        return

    def removeTestCompFromStandbySC(self):
        self.setTestStep('Deleting test component from standby SC')
        if self.noOfScs == 1:
            self.fail('ERROR', 'Running on a one-node configuration. \
            We should not have ended up in the copyTestCompToStandbySC method.')
        cmd = '\\rm -f %s%s' %(self.target_com_compdir,self.testCompName)
        self.myLogger.debug('tearDown: Delete %s by: %s' %(self.testCompName, cmd))
        result = self.sshLib.sendCommand(cmd,self.standbySubrack,self.standbySlot)
        self.fail(result[0], result[1])
        return

    def removeComSaLogCfgFile(self):
        self.setTestStep('Removing com_sa_log.cfg')
        cmd = '\\rm -f %s%s' %(self.comsaLogCfgFilePath,self.comsaLogCfgFileName)
        self.myLogger.debug('tearDown: Removing %s by command: %s' %(self.comsaLogCfgFileName,cmd))
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        return

    def restartCom(self):
        self.setTestStep('Restarting COM')
        result = self.comsa_lib.comRestart(self, self.activeSubrack,self.activeSlot, self.memoryCheck)
        self.fail(result[0], result[1])

    def modifyComSaLogCfgFile(self,testFile):
        self.setTestStep('Modify %s' %self.comsaLogCfgFileName)
        self.sshLib.setConfig(self.activeSubrack,self.activeSlot,self.activeSlot)
        testFilePath = '%s%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles,testFile)
        self.myLogger.debug('Copy COM SA test log cfg file to target under: %s' %self.comsaLogCfgFilePath)
        result = self.sshLib.remoteCopy(testFilePath, self.comsaLogCfgFilePath, timeout = 60)
        self.fail(result[0],result[1])

        result = self.sshLib.sendCommand('\mv -f %s/%s %s/%s' %(self.comsaLogCfgFilePath, testFile, self.comsaLogCfgFilePath,self.comsaLogCfgFileName))
        #result = self.sshLib.remoteCopy(testFilePath, '%s%s' %(self.comsaLogCfgFilePath,self.comsaLogCfgFileName), timeout = 60)
        self.fail(result[0],result[1])

        return

    def fixLastLine(self):
        # temporary fix to get the split lines to find the last line, unfortunately in com_sa_log.cfg there is no '\n' in the last line
        cmd = 'echo "" >> %s%s' %(self.comsaLogCfgFilePath,self.comsaLogCfgFileName)
        result = self.sshLib.sendCommand(cmd,self.activeSubrack,self.activeSlot)
        self.fail(result[0], result[1])
        return

    def switchOver(self):
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

        result = self.comsa_lib.lockSu(controller[0], activeController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck, self.installStressTool)
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

        result = self.comsa_lib.unlockSu(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern, False, self.installStressTool)
        self.fail(result[0], result[1])
        self.myLogger.info('%s' %str(result[1]))


        self.setTestStep('Verify that the former active SC becomes standby.')

        result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        if result[1] != 'STANDBY':
            self.fail(result[0], 'The former active controller did not become standby after the sericeUnit was unlocked.')

        self.myLogger.info('The former active controller became standby')
        return


    def cliTest(self):
        self.setTestStep('CLI testing')

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)

        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        for list_index in range (0,len(lists[0])):
            result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
            self.fail(result[0], result[1])

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
