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

    TC-MR35347-000 : Enable long DN
    TC-MR35347-001 : Testing CLI config
    TC-MR35347-002 : Testing NETCONF
    TC-MR35347-003 : Testing Invalid NETCONF
    TC-MR35347-004 : Creating PM Job
    TC-MR35347-099 : Disable long DN
    TC-MR35347-005 : Testing CLI config with CMW3.4PRA
    TC-MR35347-006 : Testing NETCONF with CMW3.4PRA
    TC-MR35347-007 : Creating PM Job with CMW3.4PRA
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
    TC-MR35347-001

    Id:
    ""
"""
import test_env.fw.coreTestCase as coreTestCase

import os,sys,re
from java.lang import System

class functionTestMr35347(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        self.testcase_tag = tag

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.uninstallScriptLocation = dict.get('PATH_TO_MR24760')
        self.resourceFilesLocation = dict.get("PATH_TO_MR20275")

        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')

        self.pathToPmtSaFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("PATH_TO_PMTSA_FILES"))
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.comNoBackup = dict.get("COM_NO_BACKUP")

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]

        self.MR35347 = '/home/MR35347/'
        self.pathToCmwInstallation = '%s/coremw/' %self.MR35347
        self.pathToComInstallation = '%s/com/' %self.MR35347
        self.pathToComsaInstallation = '%s/comsa/' %self.MR35347
        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        self.CoreMW = "%s/coremw3.4cp11" %self.resourceFilesLocation
        self.CoreMWSdp = 'coremw_x86_64-3.4_CP11-runtime_CXP9020355_1_R8M.tar'


        # parameters from the config files
        self.backupName = {}
        self.comBackupName = {}
        self.comsaBackupLocation = {}
        self.storedBackupFilesLocation = {}
        self.loctBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}

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

        self.scriptFile = {}
        self.pwdFreeScript = {}
        self.helloFile = {}
        self.actionFile = {}
        self.closeFile = {}
        self.logFile = {}
        self.respFile = {}

        self.useExternalModels = {}
        self.momFile = {}
        self.immClassesFile = {}
        self.immObjectsFile = {}
        self.modelFileType = ''
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.immObjPattern = '[]'
        self.immObjPattern2 = '[]'

        self.reqCmwVersion = "R10A01"        #CMW3.6
        self.reqCmwRelease = "1"
        self.reqComSaVersion = "R6A01"
        self.reqComSaRelease = "3"

        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MR35347_MODELFILE_PATH"))
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.buildDir = dict.get('BUILD_TOKENS')
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        self.swDir = System.getProperty("swDirNumber")

        self.COM_latest = "%s%s/com" %(self.installRoot, self.swDir)
        self.COMSA_latest = "%s%s/comsa" %(self.installRoot, self.swDir)

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-actionTest-%s' %user
        self.tokenPatternNetconf = 'buildToken-netconf-%s' %user
        self.tokenPatternSshSetup = 'buildToken-ssh-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

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
        CmwOK = ('SUCCESS', True)
        ComsaOK = ('SUCCESS', True)
        self.skip_test = False
        self.isRunningComSa3_2Bwd = False
        self.setTestStep('Check the required versions of COMSA is installed')

        self.logger.info('Check if the required version of CMW is installed: %s %s' % (self.reqCmwRelease, self.reqCmwVersion))
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion)
        self.fail(CmwOK[0],CmwOK[1])

        self.logger.info('Check if the required version of COMSA is installed: %s %s' % (self.reqComSaRelease, self.reqComSaVersion))
        #ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
        #self.fail(ComsaOK[0],ComsaOK[1])

        if self.restoreSnapshot:
            offlineVersion = ['','','']
            ComSaOK = ['', False]

            result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'COMSA')
            if result[0] == "REGTEST":
                offlineVersion[0] = result[1]
                offlineVersion[1] = result[2]
                offlineVersion[2] = result[3]
                ComSaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion, offlineVersion)
            else:
                ComSaOK[1] = True
        elif self.runUninstallationScript:
            ComSaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
        else:
            self.fail('ERROR', 'Normally we should not have ended up here: either self.restoreSnapshot or self.runUninstallationScript should be True!')

        if not CmwOK[1]:
            self.logger.info('Skipping the MR35347 tests because the CMW version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; CMW version not compatible: %s %s' % (self.reqCmwRelease, self.reqCmwVersion))
            self.skip_test = True
        elif not ComsaOK[1]:
            self.logger.info('Skipping the MR35347 tests because the COMSA version is obsolete for this test!')
            self.setAdditionalResultInfo('Test skipped; COMSA version not compatible: %s %s' % (self.reqComSaRelease, self.reqComSaVersion))
            self.skip_test = True
        else:
            self.logger.info('Starting the MR35347 tests because the COMSA version is compatible!')
            self.logger.info('runTest')
            self.setTestStep('Read configuration via CLI')

           ############################################################################################
            if (self.testcase_tag == 'TC-MR35347-005' or self.testcase_tag == 'TC-MR35347-006' or self.testcase_tag == 'TC-MR35347-007'):
                if not self.restoreSnapshot:
                    # 1.Create Backup and Copy backup files to stored location
                    self.setTestStep('======== Backup system ========')
                    self.backupCluster(self.backupName)

                    # 2.Copy backup files to stored location
                    self.setTestStep('======== Copy backup files to stored location =========')

                    result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.storedBackupFilesLocation)
                    self.fail(result[0], result[1])

                    command = 'cp %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = 'cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = 'cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = 'cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.backupName, self.storedBackupFilesLocation)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    # Copy com backup files to stored location
                    self.comBackupName = self.findComBackup(self.comBackupName)
                    if self.comBackupName != {}:

                         command = 'cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
                         result = self.sshLib.sendCommand (command)
                         self.fail(result[0], result[1])

                         command = 'cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
                         result = self.sshLib.sendCommand (command)
                         self.fail(result[0], result[1])

                         command = 'cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.comBackupName, self.storedBackupFilesLocation)
                         result = self.sshLib.sendCommand (command)
                         self.fail(result[0], result[1])

                    # 3.Uninstall system

                    self.setTestStep('======== Uninstall system ========')

                    result = self.sshLib.sendCommand('mkdir %s' %self.MR35347)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                    self.fail(result[0], result[1])

                    # copy uninstall script to cluster

                    result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation, self.uninstallScriptName1), self.MR35347, timeout = 120)
                    self.fail(result[0], result[1])

                    result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation, self.uninstallScriptName2), self.MR35347, timeout = 120)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.MR35347)
                    self.fail(result[0], result[1])



                # run Uninstall

                result = self.comsa_lib.unInstallSystem(self.MR35347, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
                self.fail(result[0], result[1])

                if not self.restoreSnapshot:
                    cmw_uninstall_command2 = '%s%s' %(self.MR35347, self.uninstallScriptName2)
                    result = self.sshLib.sendCommand (cmw_uninstall_command2)
                    self.fail(result[0], result[1])

                # 4.Install
                if self.restoreSnapshot:
                    result = self.sshLib.sendCommand('mkdir %s' %self.MR35347)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                    self.fail(result[0], result[1])

                # Install CoreMW
                self.setTestStep('======== Install CoreMW ========')

                result = self.sshLib.remoteCopy('%s/%s' %(self.CoreMW, self.CoreMWSdp), self.pathToCmwInstallation, timeout = 120)
                self.fail(result[0],result[1])

                result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp, backupRpms = self.backupRpmScript)
                self.fail(result[0], result[1])

                # Install COM
                self.setTestStep('======== Install COM ========')

                self.installCOM(self.COM_latest, self.pathToComInstallation)
                self.fail(result[0], result[1])

                # Install COMSA
                self.setTestStep('======== Install COM SA ========')

                self.installCOMSA(self.COMSA_latest, self.pathToComsaInstallation)
                self.fail(result[0], result[1])

                # Set 1000 restarts before failover
                self.setTestStep('======== setComSaSuRestartMax to 1000 restarts before failover ========')
                result = self.comsa_lib.setComSaSuRestartMax(False, 1000)
                self.fail(result[0], result[1])

            elif (self.testcase_tag == 'TC-MR35347-000'):
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

            elif (self.testcase_tag == 'TC-MR35347-099'):
                self.setTestStep('###Set attribute longDnsAllowed=0###')
                cmd = 'immlist -a longDnsAllowed opensafImm=opensafImm,safApp=safImmService'
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                if result[1] != 'longDnsAllowed=1':
                    self.myLogger.warning('longDnAllowed attribute is 0')
                else:
                    cmd = 'immcfg --admin-owner-clear opensafImm=opensafImm,safApp=safImmService'
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])

                    cmd = 'immcfg -m -a longDnsAllowed=0 opensafImm=opensafImm,safApp=safImmService'
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])

                    # Restart COM
                    self.myLogger.debug('Restart COM')
                    result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                    self.fail(result[0],result[1])

                    self.miscLib.waitTime(10)

            else :
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

            ############################################################################################

            if self.useExternalModels == 'yes':

                self.setTestStep('Upload model files to the target')
                cmd = 'mkdir -p %s' %self.modelFilePathOnTarget
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                #Copy actionTest application to target
                self.myLogger.debug('Copy model files to target')
                if self.immClassesFile != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile), self.modelFilePathOnTarget, timeout = 60)
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

            if self.testcase_tag == 'TC-MR35347-002' or self.testcase_tag == 'TC-MR35347-003' or self.testcase_tag == 'TC-MR35347-006':
                self.activeController = (0,0)
                activeController = 0

                controllers = self.testConfig['controllers']
                self.myLogger.info('Checking HA state for Com SA on the controllers')
                for controller in controllers:
                    result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
                    self.fail(result[0], result[1])
                    if result[1] == 'ACTIVE':
                        activeController = controller[1]
                        self.myLogger.info('Found active controller: %s' %str(controller))

                if activeController == 0:
                    self.fail('ERROR', 'No controller found with active instance of ComSa')

                self.activeController = (controller[0], activeController)
                activeCtrlAddr = self.targetData['ipAddress']['ctrl']['ctrl%d'%activeController]

                self.setTestStep('runTest creating authorized key to active controller')
                cmd = '%s%s%s %s  -k ~/.ssh/id_rsa' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.pwdFreeScript, activeCtrlAddr)
                # Get a build token
                for i in range(self.numberOfGetTokenRetries):
                    result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPatternSshSetup)
                    if result[0] == 'SUCCESS':
                        break
                    self.fail(result[0],result[1])

                result = self.miscLib.execCommand(cmd)
                self.fail(result[0], result[1])
                if 'Passwordless setup is done and persistent' or 'Passwordless is already setup' in result[1]:
                    self.myLogger.debug('pwdfree script execution OK.')
                else:
                    self.fail('ERROR', 'Unexpected return from execution of pwdfree script: %s' %result[1])

                # Release the build token
                result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPatternSshSetup)
                self.fail(result[0],result[1])

                self.setTestStep('execute netconf command and parsing the interim result')
                execScript = '%s%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.scriptFile)
                hello = '%s%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.helloFile)
                close = '%s%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.closeFile)
                logFile = '%s%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.logFile)
                actionFiles = self.actionFile
                respFile = '%s%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles, self.respFile)

                result = self.executeNetconfSession(execScript, hello, actionFiles, close, activeCtrlAddr, logFile, respFile)
                self.fail(result[0], result[1])

            # Check once again for active controller before doing CLI.
            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            self.activeController = result[1]

            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                        self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

            self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

            self.setTestStep('###Send the CLI command and process the results###')
            #Create the input, the expected output and the non-expected output lists
            lists = self.comsa_lib.load_TC_cli_config(self)
            #Create the input, the expected output and the non-expected output lists
            lists1 = self.comsa_lib.load_TC_imm_config(self)

            #Send the cli commands and process the results element-by-element
            #One element of the list is one cli session.
            for list_index in range(0,len(lists[0])):
                result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
                self.fail(result[0], result[1])

            # Check object in IMM
            self.setTestStep('###Check objects in IMM###')

            # Send the IMM commands and process the results element-by-element
            #One element of the list is one imm session.
            for list_index1 in range(0,len(lists1[0])):
                result = self.comsa_lib.runImmSession(lists1, list_index1)
                self.fail(result[0], result[1])

    def backupCluster(self, backupName):
        self.logger.info('backupCluster: backupName = %s' %backupName)

        result = self.safLib.isBackup(backupName)
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])
        elif result != ('SUCCESS','NOT EXIST'):
            result = self.safLib.backupRemove(backupName)
            if result[0] != 'SUCCESS':
                self.fail(result[0], result[1])

        result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.testSuiteConfig['restoreBackup'] = backupName
        self.logger.info('backupCluster: exit')

    def installCOM(self, setupFilesDir, pathToComInstallation):
        self.logger.info('installCOM: Called')
        self.logger.info('installCOM: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCOM: pathToComInstallation = %s' %pathToComInstallation)
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        cmd = 'ls %s/COM-*.sdp' %(setupFilesDir)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM runtime sdp file not found at specified location: %s/ .' %setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM runtime sdp file found at specified location: %s/: %s.' %(setupFilesDir, str(result[1])))
        name_list = result[1].strip()
        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])

        comRtSdpname = name_list.split('/')[len(name_list.split('/')) - 1]

        # determine suitable package for 1 or 2 controller node
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            cmd = 'ls %s/ERIC-COM-I1*.sdp' %(setupFilesDir)
        elif noOfScs == 1:
            cmd = 'ls %s/ERIC-COM-I2*.sdp' %(setupFilesDir)
        else:
            self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' %str(noOfScs))

        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM campaign sdp file not found at specified location: %s/ .' %setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM campaign sdp file found at specified location: %s/: %s.' %(setupFilesDir, str(result[1])))
        name_list = result[1].strip()
        self.logger.info('name_list: (%s)'%name_list)

        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])
        comInstSdpName = name_list.split('/')[len(name_list.split('/')) - 1]

        #Install to system
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comInstSdpName, 'com', backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')


    def installCOMSA(self, setupFilesDir, pathToComsaInstallation):
        self.logger.info('installCOMSA: Called')
        self.logger.info('installCOMSA: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCOMSA: pathToComsaInstallation = %s' %pathToComsaInstallation)

       # Install time

        result = self.sshLib.sendCommand('rm -rf %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        noOfScs = len(self.testConfig['controllers'])
        result = self.miscLib.execCommand("ls %s/%s | awk -F'/' '{print $NF}'" %(setupFilesDir, self.cxpSdpName))
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', result[1])
        self.cxpSdpName = result[1].rstrip()
        if noOfScs == 2:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' %(setupFilesDir, self.cxpSdpName), '%s/%s' %(setupFilesDir, self.installSdpName)], self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpName, 'comsa', backupRpms = self.backupRpmScript)
        elif noOfScs == 1:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' %(setupFilesDir, self.cxpSdpName),\
                                              '%s/%s' %(setupFilesDir, self.installSdpNameSingle)],self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpNameSingle, 'comsa', backupRpms = self.backupRpmScript)

        self.fail(result[0], result[1])
        campaignStartTime = result[2] # This is not used!!!
        campaignName = result[3] # This is not used!!!

        self.logger.info('installCOMSA: Exit')

    def findComBackup(self, comBackupName):
        """
        If comBackupName is defined, the method simply returns the same name.
        If comBackupName is not defined, the method returns the latest backup which's name
        contains COM (case insensitive), but does not contain comsa, com_sa, com-sa (case insensitive)
        """
        self.logger.info('findComBackup: Called')
        if comBackupName != {}:
            self.logger.info('findComBackup: Exit')
            return comBackupName
        else:
            cmd = """cmw-partial-backup-list 2>&1 | sed 's/\[//g' | sed 's/\]//g' | grep -i com | egrep -iv '(comsa)|(com_sa)|(com-sa)' | tail -1 | awk '{print $NF}' """
            # We search for the latest COM backup
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            backupName = result[1]
            if backupName == '':
                if self.linuxDistro != self.distroTypes[1]:
                    self.logger.info('findComBackup: Exit')
                    self.fail('ERROR', 'findComBackup: COM backup not found!')
                elif self.linuxDistro == self.distroTypes[1]:
                    # For RHEL systems we try to reinstall COM instead of restoring a COM backup
                    backupName == 'com_autobackup'
                    #self.logger.info('findComBackup: Exit')
                    #self.fail('ERROR', 'findComBackup: COM backup not found!')
            self.logger.info('findComBackup: Exit')
            return backupName

    def tearDown(self):
        self.setTestStep('tearDown')

        if self.skip_test == False:

            if self.installStressTool:
                self.setTestStep('======== Stopping the stress tool on target ========')
                self.comsa_lib.stopStressToolOnTarget(self)

            if (self.testcase_tag == 'TC-MR35347-002' or self.testcase_tag == 'TC-MR35347-003' or self.testcase_tag == 'TC-MR35347-006'):
                tdFailures = []

                self.setTestStep('remove authorized keys from the cluster')
                self.comsa_lib.removeAuthorizedKey(self.testConfig)

            if self.useExternalModels == 'yes':
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
                if len(eval(self.immObjPattern2)) > 0:
                    immObjPatterns2 = eval(self.immObjPattern2)
                    for immObjPattern2 in immObjPatterns2:
                        self.myLogger.debug('Removing the object %s' %immObjPattern2)
                        cmd = 'immfind | grep -i %s | xargs immcfg -d' %immObjPattern2
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

                self.setTestStep('Remove model folder')
                cmd = '\\rm -rf  %s' %self.modelFilePathOnTarget
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])


            if (self.testcase_tag == 'TC-MR35347-005' or self.testcase_tag == 'TC-MR35347-006' or self.testcase_tag == 'TC-MR35347-007'):
                if not self.restoreSnapshot:
                    # .Restore system
                    self.setTestStep('======== Restore system ========')
                    #recopy the backup files
                    command = 'cp %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comsaBackupLocation, self.backupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = 'cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comBackupLocation, self.backupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = 'cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.cmwBackupLocation, self.backupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = 'cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupName, self.loctBackupLocation)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                    self.fail(result[0],result[1])

                    self.myLogger.info("exit runTest")

            self.setTestStep('Remove folder')
            cmd = '\\rm -rf  %s' %self.MR35347
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])



        else:
            coreTestCase.CoreTestCase.tearDown(self)
            self.setTestStep('leave tearDown')

        #########################
        #### SUPPORT METHODS ####
        #########################


    def readFile(self, logFile):
        try:
            fd = open(logFile, 'r')
        except:
            self.myLogger.error('Open file %s FAILED' % logFile)
            return ('ERROR', 'Could not read file: %s' %logFile)
        fileContent = fd.read()
        fd.close()
        return ('SUCCESS', fileContent)

    def sendNetconfMessage(self, execScript, hello, action, close, activeCtrlAddr, logFile):

     #result = self.miscLib.execCommand('%s %s %s  %s %s %s' %(execScript, hello, action, close, activeCtrlAddr, logFile))
     #result = self.miscLib.execCommand('cat %s %s %s | ssh root@%s -s -t -t netconf > %s' %(hello, action, close, activeCtrlAddr, logFile))
        if self.isRunningComSa3_2Bwd == True:
            result = self.miscLib.execCommand('cat %s %s %s | ssh root@%s -s -t -t netconf > %s' %(hello, action, close, activeCtrlAddr, logFile))
        else:
            result = self.miscLib.execCommand('cat %s %s %s | ssh root@%s -s -t netconf > %s' %(hello, action, close, activeCtrlAddr, logFile))
     #this will fail for some reason, but the output is saved in the log file and this is what matters

        result = self.readFile(logFile)
        if result[0] != 'SUCCESS':
            return result
        xmlMessage = result[1]
        return ('SUCCESS', xmlMessage)

    def executeNetconfSession(self, execScript, hello, actionFiles, close, activeCtrlAddr, logFile, expectedResp):

        self.myLogger.debug('enter executeNetconfSession')
        if 'list' in str(type(eval(actionFiles))):
            actionFiles = eval(actionFiles)
            action = ''
            if len(actionFiles) == 0:
                self.myLogger.debug('leave executeNetconfSession')
                return ('ERROR', 'No action file defined for the netconf operation! Edit the actionFile parameter in the xml config file of the test case.')
            for i in range(len(actionFiles)):
                action += ' %s%s%s' %(self.MY_REPOSITORY, self.pathToConfigFiles, actionFiles[i])
        elif 'str' in str(type(actionFiles)):
            action = '%s%s/%s' %(self.MY_REPOSITORY, self.pathToConfigFiles, actionFiles)
        else:
            self.myLogger.debug('leave executeNetconfSession')
            return ('ERROR', 'Unsupported variable type for actionFiles: %s' %str(type(actionFiles)))

        self.myLogger.debug('action: %s' %action)

    # Get a build token
        for i in range(self.numberOfGetTokenRetries):
            result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPatternNetconf)
            if result[0] == 'SUCCESS':
                break
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result

        result = self.sendNetconfMessage(execScript, hello, action, close, activeCtrlAddr, logFile)
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result
        xmlMessage = result[1]
        self.myLogger.info('The replied xml message is: \n%s' %xmlMessage)

    # Release the build token
        result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPatternNetconf)
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result

        result = self.readFile(expectedResp)
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result
        expectedResponses = result[1]

    #print 'expectedResponses: ',expectedResponses

        if xmlMessage.count('error') > expectedResponses.count('error') or xmlMessage.count('failed') > expectedResponses.count('failed'):
            self.myLogger.debug('leave executeNetconfSession')
            return ('ERROR', 'The xml response contained an unexpected error. \n%s' %xmlMessage)

        expectedResponses = eval(expectedResponses)
        if not 'list' in str(type(expectedResponses)):
            self.myLogger.debug('leave executeNetconfSession')
            return ('ERROR', 'The expected responses provided have to be in a list format in the %s text file.' %respFile)
        elementsNotFound = []
        for message in expectedResponses:
            if message in xmlMessage:
                self.myLogger.debug('%s found in xml response.' %message)
            else:
                elementsNotFound.append(message)
        if len(elementsNotFound) != 0:
            self.myLogger.debug('leave executeNetconfSession')
            return('ERROR', 'The following elements were not found in the xml response message: %s' %str(elementsNotFound))

        self.myLogger.debug('leave executeNetconfSession')
        return ('SUCCESS', xmlMessage)

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
