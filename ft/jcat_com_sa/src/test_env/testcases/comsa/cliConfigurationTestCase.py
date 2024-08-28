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

    TC-CLI-001 - CLI read configuration - read top level
    TC-CLI-002 - CLI read configuration - read next level
    TC-CLI-003 - CLI read configuration - read the entire configuration
    TC-CLI-004 - CLI read configuration - try to read a non-existing object
    TC-CLI-005 - CLI change configuration - changing an attribute value
    TC-CLI-006 - CLI change configuration - changing multiple attribute values
    TC-CLI-007 - CLI change configuration - creating a new object but aborting the operation
    TC-CLI-008 - CLI change configuration - creating multiple objects but aborting the operation
    TC-CLI-009 - CLI change configuration - creating a new object
    TC-CLI-010 - CLI change configuration - creating multiple objects at the same time
    TC-CLI-011 - CLI change configuration - deleting an object and aborting the change
    TC-CLI-012 - CLI change configuration - deleting multiple objects and aborting the change
    TC-CLI-013 - CLI change configuration - deleting an object and committing the change
    TC-CLI-014 - CLI change configuration - deleting multiple objects and committing the change
    TC-CLI-015 - CLI change configuration - deleting and recreating an object
    TC-CLI-016 - CLI change configuration - delete an attribute, change the same attribute and then commit
    TC-CLI-017 - CLI change configuration - change an attribute value multiple times and commit
    TC-MISC-023 - Error messages are misleading when missing value in MO

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
    TC-CLI-001

    Id:
    "CLI read configuration - read top level"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-002

    Id:
    "CLI read configuration - read next level"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-003

    Id:
    "CLI read configuration - read the entire configuration"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-004

    Id:
    "CLI read configuration - try to read a non-existing object"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-005

    Id:
    "CLI change configuration - changing an attribute value"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-006

    Id:
    "CLI change configuration - changing multiple attribute values"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-007

    Id:
    "CLI change configuration - creating a new object but aborting the operation"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-008

    Id:
    "CLI change configuration - creating multiple objects but aborting the operation"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-009

    Id:
    "CLI change configuration - creating a new object"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-010

    Id:
    "CLI change configuration - creating multiple objects at the same time"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-011

    Id:
    "CLI change configuration - deleting an object and aborting the change"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-012

    Id:
    "CLI change configuration - deleting multiple objects and aborting the change"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-013

    Id:
    "CLI change configuration - deleting an object and committing the change"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-014

    Id:
    "CLI change configuration - deleting multiple objects and committing the change"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-015

    Id:
    "CLI change configuration - deleting and recreating an object"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-016

    Id:
    "CLI change configuration - delete an attribute, change the same attribute and then commit"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-CLI-017

    Id:
    "CLI change configuration - change an attribute value multiple times and commit"
    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MISC-023

    Id:
    "Error messages are misleading when missing value in MO"
    ==================================

    Tag:
    TC-MISC-037

    Id:
    "getMoAttribute() for an unset attribute"
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import os
from java.lang import System


class CLIconfiguration(coreTestCase.CoreTestCase):

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
        self.immObjectsFile = {}
        self.momFile2 = {}
        self.immClassesFile2 = {}
        self.immObjectsFile2 = {}
        self.modelFileType = ''
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.immObjPattern = '[]'
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        self.reqCmwRelease = "1"
        self.reqCmwVersion = "R5A11"
        #TC-MISC-034 and TC-MISC-035 need to be skipped from comsa3.5sh08 3_R6A09
        self.obsoleteComSaVersion = "R9A01"
        self.obsoleteComSaRelease = "9"

        self.configFile  = {}
        self.configFilePathOnTarget = '/storage/clear/comsa_for_coremw-apr9010555/'
        self.enableComSaTrace = ''
        self.startTimeSyslog = 0
        self.syslogDir = '/var/log/'
        self.tempDirConfigFile = '/home/HT85987/'
        self.configFileSystemPath = '/storage/system/config/comsa_for_coremw-apr9010555/etc/'

        self.immasynctimeoutConfig = ''
        self.greaterDefaultValue = ''

        self.expectedComSA_syslog_1 = {}
        self.expectedComSA_syslog_2 = {}
        self.expectedComSA_syslog_3 = {}

        self.unexpectedComSA_syslog_1 = {}

        self.expectedImmasynctimeout_syslog = {}

        self.reqComSaVersion = "R1A01"

        self.reqComSaRelease = "3"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        if self.modelFileType == 'CDT':
            self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("EXAMPLE_MODELFILE_PATH"))
        else:
            self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT763_MODELFILE_PATH"))
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        """
        Stress Tool parameters
        """
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

        if not self.memoryCheck:
            cmd = '%s "show all" "exit"' %self.cli_active_controller_login_params
            self.myLogger.debug('showing the entire configuration')
            result = self.comsa_lib.executeCliSession(cmd)

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
                result1 = self.comsa_lib.executeCliSession(cmd)
            if 'SnmpTargetV1=2' in result[1]:
                cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV1=2" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
                self.myLogger.debug('Delete SnmpTargetV1, just in case it was left there')
                result1 = self.comsa_lib.executeCliSession(cmd)
            if 'SnmpTargetV2C=1' in result[1]:
                cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV2C=1" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
                self.myLogger.debug('Delete SnmpTargetV2C, just in case it was left there')
                result1 = self.comsa_lib.executeCliSession(cmd)
            if 'SnmpTargetV2C=2' in result[1]:
                cmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, SysM=1, Snmp=1" "no SnmpTargetV2C=2" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
                self.myLogger.debug('Delete SnmpTargetV2C, just in case it was left there')
                result1 = self.comsa_lib.executeCliSession(cmd)
            if 'userLabel' in result[1]:
                cmd = '%s "configure" "ManagedElement=1" "no userLabel" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
                self.myLogger.debug('Delete userLabel, just in case it was left there')
                result1 = self.comsa_lib.executeCliSession(cmd)
            if 'siteLocation' in result[1]:
                cmd = '%s "configure" "ManagedElement=1" "no siteLocation" "commit" %s' %(self.cli_active_controller_login_params, exitCliString)
                self.myLogger.debug('Delete siteLocation, just in case it was left there')
                result1 = self.comsa_lib.executeCliSession(cmd)

        self.logger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        if self.immasynctimeoutConfig == 'True':
            self.logger.info('Copy origin comsa.cfg file to temporary directory')
            # Create the temporary directory to store the origin comsa.cfg file
            cmd = 'mkdir -p %s' %self.tempDirConfigFile
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # Copy the comsa.cfg file to temporary directory
            cmd = '\cp %s%s %s' %(self.configFileSystemPath,self.configFile, self.tempDirConfigFile)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # Change the imma sync timeout to greater than default value
            if self.greaterDefaultValue == 'True':
                cmd = "sed -i 's/imma_syncr_timeout=.*/imma_syncr_timeout=12000/' %s%s" %(self.configFileSystemPath,self.configFile)
            else:
                cmd = "sed -i 's/imma_syncr_timeout=.*/imma_syncr_timeout=6/' %s%s" %(self.configFileSystemPath,self.configFile)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # Getting Linux System Time
            self.setTestStep("### Getting Linux System Time")

            # Getting Linux Time for matching the string in syslog
            dateCommandSyslog = "date +%s"
            result = self.sshLib.sendCommand(dateCommandSyslog)
            self.fail(result[0],result[1])
            self.startTimeSyslog = int(result[1])
            self.myLogger.info("Linux System Time for matching string in syslog is: %s" %(self.startTimeSyslog))

            # Restart com
            cmd = 'comsa-mim-tool com_switchover'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            self.miscLib.waitTime(20)

            self.setTestStep("### Check the value of imma sync timeout in the syslog")
            self.expectedLogs()
        else:
            self.setTestStep('Read configuration via CLI')
            CmwMajorOK = ('SUCCESS', True)
            self.skip_test = False

            CmwMajorOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion, [])
            self.fail(CmwMajorOK[0],CmwMajorOK[1])

            if self.linuxDistro == self.distroTypes[0]: #sles11
                #TC-MISC-034 and TC-MISC-035 need to be skipped from comsa3.5sh08 3_R6A09
                self.logger.info('Check if an obsolete version of COMSA is installed: %s %s' % (self.obsoleteComSaRelease, self.obsoleteComSaVersion))
                ComsaObsolete = self.lib.checkObsoleteComponentVersion('comsa', self.obsoleteComSaRelease, self.obsoleteComSaVersion)
                self.fail(ComsaObsolete[0],ComsaObsolete[1])
            else: # rhel or sles12
                if self.tag == 'TC-MISC-034' or self.tag == 'TC-MISC-035':
                    ComsaObsolete = ('SUCCESS', False)
                else:
                    ComsaObsolete = ('SUCCESS', True)

            ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion, [])
            self.fail(ComsaOK[0],ComsaOK[1])

            if CmwMajorOK[1] == True and ComsaObsolete[1] == True and ComsaOK[1] == True:

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

                    # set the stress tool to occupy all CPU cores and 90% of the physical RAM, nwith NFS disk stress 1 task 64K bytes blocks
                    result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

                    # this is 100% of the RAM with no disk stress
                    # result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 10, tenPercentOfTotalRam, 60*60*60, 0, 0, 0, 0)

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


                    if self.momFile != {}:
                        result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                        self.fail(result[0],result[1])
                    if self.momFile2 != {}:
                        result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2))
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

                if self.enableComSaTrace == 'True':
                    # Getting Linux System Time
                    self.setTestStep("### Getting Linux System Time")

                    # Getting Linux Time for matching the string in syslog
                    dateCommandSyslog = "date +%s"
                    result = self.sshLib.sendCommand(dateCommandSyslog)
                    self.fail(result[0],result[1])
                    self.startTimeSyslog = int(result[1])
                    self.myLogger.info("Linux System Time for matching string in syslog is: %s" %(self.startTimeSyslog))

                    # Modify com_sa_trace.conf on target
                    self.setTestStep("### Modify com_sa_trace.conf on target")

                    cmd = 'sed -i s/COMSA_GLOBAL_TRACE=disable/COMSA_GLOBAL_TRACE=enable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                    self.myLogger.debug('Modify COMSA_GLOBAL_TRACE to enable')
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0],result[1])

                    cmd = 'sed -i s/COMSA_TRACE_GROUP_01=disable/COMSA_TRACE_GROUP_01=enable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                    self.myLogger.debug('Modify COMSA_TRACE_GROUP_01 to enable')
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0],result[1])

                    self.miscLib.waitTime(20)

                #Create the input, the expected output and the non-expected output lists
                lists = self.comsa_lib.load_TC_cli_config(self)
                self.setTestStep('CLI Testing')
                #Send the cli commands and process the results element-by-element
                #One element of the list is one cli session.
                for list_index in range(0,len(lists[0])):
                    result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
                    self.fail(result[0], result[1])

                if self.enableComSaTrace == 'True':
                    # Search pattern
                    self.setTestStep("### Check text in logs")

                    self.expectedLogs()
                    self.unexpectedLogs()

                    cmd = 'sed -i s/COMSA_GLOBAL_TRACE=enable/COMSA_GLOBAL_TRACE=disable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                    self.myLogger.debug('Modify COMSA_GLOBAL_TRACE to disable')
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0],result[1])

                    cmd = 'sed -i s/COMSA_TRACE_GROUP_01=enable/COMSA_TRACE_GROUP_01=disable/g %s%s' %(self.configFilePathOnTarget, self.configFile )
                    self.myLogger.debug('Modify COMSA_TRACE_GROUP_01 to disable')
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0],result[1])

            else:
                if CmwMajorOK[1] == False:
                    self.logger.info('Skipped tests because of CMW version not compatible!')
                    self.setAdditionalResultInfo('Test skipped, CMW version not compatible')
                if ComsaObsolete[1] == False:
                    self.logger.info('Skipped tests because of COMSA version not compatible!')
                    self.setAdditionalResultInfo('Test skipped, COMSA version not compatible')
                if ComsaOK[1] == False:
                    self.logger.info('Skipped tests because of COMSA version not compatible!')
                    self.setAdditionalResultInfo('Test skipped, COMSA version not compatible')
                self.skip_test = True
        coreTestCase.CoreTestCase.runTest(self)

    def expectedLogs(self):
        if self.expectedComSA_syslog_1 != {}:
            self.evaluateExpectedSearchPattern([self.expectedComSA_syslog_1], self.startTimeSyslog, self.syslogDir)
        if self.expectedComSA_syslog_2 != {}:
            self.evaluateExpectedSearchPattern([self.expectedComSA_syslog_2], self.startTimeSyslog, self.syslogDir)
        if self.expectedComSA_syslog_3 != {}:
            self.evaluateExpectedSearchPattern([self.expectedComSA_syslog_3], self.startTimeSyslog, self.syslogDir)
        if self.expectedImmasynctimeout_syslog != {}:
            self.evaluateExpectedSearchPattern([self.expectedImmasynctimeout_syslog], self.startTimeSyslog, self.syslogDir)

    def unexpectedLogs(self):
        if self.unexpectedComSA_syslog_1 != {}:
            self.evaluateUnexpectedSearchPattern([self.unexpectedComSA_syslog_1], self.startTimeSyslog, self.syslogDir)

    def evaluateExpectedSearchPattern(self, searchPattern, startTimeSyslog, logDir):
        result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, startTimeSyslog, self.testConfig, logDir)

        self.sshLib.tearDownHandles()
        self.fail(result[0],result[1])
        self.myLogger.debug('Found %s in log at: %s' %(searchPattern,result[1]))

    def evaluateUnexpectedSearchPattern(self, searchPattern, startTimeSyslog, logDir):
        result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, startTimeSyslog, self.testConfig, logDir)

        self.sshLib.tearDownHandles()
        if (result[0] == "SUCCESS"):
            self.myLogger.error("Unexpected pattern found: %s" %searchPattern)

    def tearDown(self):
        self.setTestStep('tearDown')
        if self.immasynctimeoutConfig == 'True':
            # Copy the origin comsa.cfg file back to system path
            cmd = '\cp %s%s %s' %(self.tempDirConfigFile,self.configFile, self.configFileSystemPath)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # Restart com
            cmd = 'comsa-mim-tool com_switchover'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            self.miscLib.waitTime(20)

            # Remove the temporary directory
            cmd = '\rm -rf %s' %(self.tempDirConfigFile)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
        else:
            if self.skip_test == False:
                if self.useExternalModels == 'yes':
                    if self.momFile != {}:
                        result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                        self.fail(result[0],result[1])
                    if self.momFile2 != {}:
                        result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2))
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
