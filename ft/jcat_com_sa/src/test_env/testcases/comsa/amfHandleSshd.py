#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
###############################################################################
#
# Ericsson AB 2015 All rights reserved.
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

    TC-AMFSSHD-001 Run CLI and Netconf over SSH when SSHD is configured by COM under AMF
    TC-AMFSSHD-002 COM is stoped -> SSHD (NBI) is stopped, UC3: COM is started up -> SSHD NBI is started
    TC-AMFSSHD-003 SSHD crashes and verify it will is restarted by AMF
    TC-AMFSSHD-004 Upgrade COM from older to SSHD capable and confirm that OAM SSHD can be configured
    TC-AMFSSHD-005 Upgrade COM SA from older to SSHD capable and confirm that OAM SSHD can be configured
    TC-AMFSSHD-006 Perform COM SA switchover and verify that the SSHD is handled as expected
    TC-AMFSSHD-007 Upgrade COM from older to SSHD capable with campaign backup enabled. Confirm that OAM SSHD can be configured

    Help:
    The script requires the following files (and formats):
    CORE MW: the runtime tar file
    COM: the runtime sdp and the installation sdp

    ""
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib
import omp.tf.ssh_lib as ssh_lib
import coremw.saf_lib as saf_lib
import omp.tf.hw_lib as hw_lib
from java.lang import System
from org.apache.log4j import Logger

class amfHandleSshd(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.testcase_tag = tag
        # parameters from the config files
        self.pathToConfigFiles = {}
        self.serviceInstanceName = 'ComSa'
        self.amfNodePattern = 'Cmw'
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.reqCmwRelease = ""
        self.reqCmwVersion = ""
        self.reqComRelease = ""
        self.reqComVersion = ""
        self.reqComSaRelease = ""
        self.reqComSaVersion = ""
        self.backupName = "sshd_backup"
        self.storedBackupFilesLocation = {}
        self.comBackupName = {}
        self.comsaBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}
        self.lotcBackupLocation = {}
        self.activeCtrlAddr = ""
        self.createBackupDuringCampaign = ""

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.buildLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("SRC"))
        self.cxpArchive = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.absDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        self.testDir =  '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST"))
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.configLocation = '/cluster/storage/system/config/'
        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
        self.comSshdConfigOam = 'sshd_config_oam'
        self.amfSshdTempDir = '/home/amfSshdTmp/'
        self.sshdMainConfig = '/etc/ssh/sshd_config'
        self.temp_dir = '/home/coremw/incoming/'
        self.temp_bfu = '/home/comsa_upgrade/'

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER_RHEL')
        else:
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER')

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)
        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])
        command = 'mkdir -p %s' %self.amfSshdTempDir
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])
        self.noOfScs = len(self.testConfig['controllers'])
        self.ipaddressSc1 = self.targetData['ipAddress']['ctrl']['ctrl1']
        if self.noOfScs == 2:
            self.ipaddressSc2 = self.targetData['ipAddress']['ctrl']['ctrl2']
        self.pwdFreeScript = 'pwdfree_ssh.py'

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-actionTest-%s' %user
        self.tokenPatternNetconf = 'buildToken-netconf-%s' %user
        self.tokenPatternSshSetup = 'buildToken-ssh-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5
        self.buildDir = dict.get('BUILD_TOKENS')
        self.oamSshdconfiguration = '/storage/system/config/com-apr9010443/etc/sshd/sshd_config_oam'

        self.resourceFilesLocation = dict.get("PATH_TO_MR29930")
        self.modelFileList = dict.get("COM_MODEL_FILE_LIST")
        self.clearLocation = '/cluster/storage/clear/'
        self.configLocation = '/cluster/storage/system/config/'
        self.softwareLocation = '/cluster/storage/system/software'
        self.comsaDirUnderPso = 'comsa_for_coremw-apr9010555'
        self.comsaBin = '/opt/comsa/bin/'
        self.comPidFile = '/opt/com/run/com.pid'
        self.homeTempDir = '/home/tempAmfSshd/'
        self.pathToCmwInstallation = '%s/' %self.homeTempDir
        self.pathToComInstallation = '%scom/' %self.homeTempDir
        self.pathToComsaInstallation = '%scomsa/' %self.homeTempDir
        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        # we will test with CMW 3.6 PRA, but currently, CMW 3.6 SH11 is being used
        self.CoreMWSdp36PRA = 'coremw_x86_64-3.6_SH11-runtime_CXP9020355_1_R9A19.tar'
        self.coremw36 = "%s/coremw/coremw3.6"%self.resourceFilesLocation
        self.com50 = "%s/com/com5.0"%self.resourceFilesLocation
        self.com51 = "%s/com/com5.1"%self.resourceFilesLocation
        self.ComSABuild = "%s/comsa"%self.resourceFilesLocation
        self.comsa35 = "%s/comsa/comsa3.5"%self.resourceFilesLocation
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')
        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
            self.cxpSdpNameOffical = dict.get('CXP_SDP_NAME_RHEL_OFFICIAL')
        else:
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))
            self.cxpSdpNameOffical = dict.get('CXP_SDP_NAME_OFFICIAL')
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.myLogger.info('runTest')
        ComsaOK = ('SUCCESS', True)
        ComOK = ('SUCCESS', True)
        CmwOK = ('SUCCESS', True)
        self.skip_test = False

        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
        self.fail(ComsaOK[0],ComsaOK[1])
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
        self.fail(CmwOK[0],CmwOK[1])
        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion )
        self.fail(ComOK[0],ComOK[1])

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
        self.activeCtrlAddr = self.targetData['ipAddress']['ctrl']['ctrl%d'%activeController]
        #self.pathToConfigFiles = '%s%s'%(self.MY_REPOSITORY, self.pathToConfigFiles)
        if ComsaOK[1] and CmwOK[1] and ComOK[1]:
            self.skip_test = False
        else:
            self.skip_test = True

        # In TC-AMFSSHD-006, if cluster is single, there is no switchover so skip it
        if self.noOfScs == 1 and self.testcase_tag == 'TC-AMFSSHD-006':
            self.skip_test = True

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
            result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)
            self.sshLib.setTimeout(stressTimeOut)

        if self.skip_test == False:
            self.startUnixTime = 0
            if (self.testcase_tag == 'TC-AMFSSHD-004' or
                self.testcase_tag == 'TC-AMFSSHD-005' or
                self.testcase_tag == 'TC-AMFSSHD-006' or
                self.testcase_tag == 'TC-AMFSSHD-007'):
                # Verify that SSHD is controlled by COM SA
                self.setTestStep('Verify that SSHD is under control of COM SA')
                cmd = '%s "show" "exit"' %self.cli_active_controller_login_params
                result = self.comsa_lib.executeCliSession(cmd)
                if 'ManagedElement=1' not in result[1]:
                    self.fail('ERROR', 'SSHD is not under control of COM SA')

                if (self.testcase_tag == 'TC-AMFSSHD-004' or
                    self.testcase_tag == 'TC-AMFSSHD-007'):
                    # 1.Create Backup and Copy backup files to stored location
                    self.setTestStep('======== Backup system ========')
                    self.backupCluster(self.backupName)

                    # 2.Copy backup files to stored location
                    self.setTestStep('======== Copy backup files to stored location =========')

                    #result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
                    self.fail(result[0], result[1])
                    self.copyBackupFiles(self.backupName)

                    # Copy com backup files to stored location
                    self.comBackupName = self.findComBackup(self.comBackupName)
                    self.copyComBackupFiles(self.comBackupName)

                    # 3.Uninstall system
                    self.setTestStep('======== Uninstall system ========')

                    result = self.sshLib.sendCommand('mkdir %s' %self.homeTempDir)
                    self.fail(result[0],result[1])

                    #copy uninstall script to cluster
                    result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName1), self.homeTempDir, timeout = 120)
                    self.fail(result[0], result[1])

                    result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName2), self.homeTempDir, timeout = 120)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.homeTempDir)
                    self.fail(result[0], result[1])

                    #run Uninstall
                    result = self.comsa_lib.unInstallSystem(self.homeTempDir, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater)
                    self.fail(result[0], result[1])

                    cmw_uninstall_command2 = '%s%s' %(self.homeTempDir, self.uninstallScriptName2)
                    result = self.sshLib.sendCommand (cmw_uninstall_command2)
                    self.fail(result[0], result[1])

                    self.lib.resetDumps()

                    # Install CoreMw 3.5 PRA
                    self.setTestStep('======== Install CoreMW 3.6 ========')
                    result = self.sshLib.remoteCopy('%s/%s' %(self.coremw36, self.CoreMWSdp36PRA), self.pathToCmwInstallation, timeout = 120)
                    self.fail(result[0],result[1])

                    result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp36PRA, backupRpms = self.backupRpmScript)
                    self.fail(result[0], result[1])

                    # Install COM
                    self.setTestStep('======== Install COM 5.0========')
                    result = self.installCOM(self.com50, self.pathToComInstallation)

                    # Install COM SA
                    self.setTestStep('======== Install current COM SA ========')
                    self.installCOMSA(self.ComSABuild, self.pathToComsaInstallation, 'True')

                    # Upgrade COM to COM 5.1 PRA
                    self.setTestStep('======== Upgrade to COM 5.1 PRA ========')
                    self.upgradeCOM(self.com51, self.pathToComInstallation)

                if self.testcase_tag == 'TC-AMFSSHD-005':
                    # 1.Create Backup and Copy backup files to stored location
                    self.setTestStep('======== Backup system ========')
                    self.backupCluster(self.backupName)

                    # 2.Copy backup files to stored location
                    self.setTestStep('======== Copy backup files to stored location =========')

                    result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
                    self.fail(result[0], result[1])

                    self.copyBackupFiles(self.backupName)

                    # 3.Restore COM backup
                    self.setTestStep('======== Restore COM backup ========')
                    self.myLogger.debug('Restore the COM backup ')
                    self.setTestStep('Restore the COM backup')
                    self.comBackupName = self.findComBackup(self.comBackupName)
                    result = self.comsa_lib.restoreSystem(self, self.comBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 2, removeBackup = False)
                    self.fail(result[0],result[1])

                    # 4.Install old COM SA (COM SA 3.5 PRA)
                    self.setTestStep('======== Installing old COM SA ========')
                    result = self.sshLib.sendCommand('mkdir %s' %self.homeTempDir)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                    self.fail(result[0], result[1])

                    self.installCOMSA(self.comsa35, self.pathToComsaInstallation, 'False')

                    # 5.Upgrade to COM SA build
                    self.setTestStep('======== Upgrading to current COM SA  ========')
                    # Create COM-SA temp directory
                    cmd = 'mkdir -p %s' %self.temp_dir
                    self.myLogger.debug('Create COM SA temp directory by: %s' %cmd)
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0],result[1])

                    self.upgradeCOMSA()

            # remove all configurations added by COM SA in /etc/ssh/sshd_config
            self.removeAllCOMSAsshdConfig()
            # activate SSHD configured by COM
            self.ActivateAmfControllSshd(26)  # set the CLI port to 26
            # restart COM SA
            self.restartCOMSAbyAmfAdmin()
            # activate SSHD configured by COM. We have to do this step because after restarting, config is reverted back again
            self.ActivateAmfControllSshd(26)  # set the CLI port to 26
            # Need to kill SSHD configured by COM process to load new configuration
            self.reloadSSHDOam()
            # set up authorized key
            self.setupAuthorizedKey()
            # Should wait for configuration come up completely
            #self.miscLib.waitTime(30)
            # SSH to port 26 and check CLI is running. Now active node should be node 1
            self.testCLIonPort(26)
            # SSH to port 830 and check Netconf is running
            self.testNetconfOnPort(830)

            if self.testcase_tag == 'TC-AMFSSHD-002' or self.testcase_tag == 'TC-AMFSSHD-006':
                self.setTestStep('Lock COM SA on both SCs')
                # lock all SC's
                self.lockSu(1)
                if self.noOfScs == 2:
                    self.lockSu(2)
                self.setTestStep('Check: There is NO COM process running')
                # check there is no COM process running
                command = 'pgrep com'
                result = self.sshLib.sendCommand(command, 2, 1)
                self.fail(result[0], result[1])
                if result[1] != '':
                    self.fail('ERROR', 'There is STILL a COM running')
                else:
                    if self.noOfScs == 2:
                        result = self.sshLib.sendCommand(command, 2, 2)
                        self.fail(result[0], result[1])
                        if result[1] != '':
                            self.fail('ERROR', 'There is STILL a COM running')
                self.setTestStep('Check: There is NO SSHD configured by COM running')
                # check that there is no SSHD configured COM process is running
                command = 'ps auxwww | grep "\d*.*/usr/sbin/sshd\s\-D -f %s"  | awk \'{print $2}\'' %self.oamSshdconfiguration
                result = self.sshLib.sendCommand(command, 2, 1)
                self.fail(result[0], result[1])
                if result[1] != '':
                    self.fail('ERROR', 'There is STILL a SSHD configured by COM running')
                else:
                    if self.noOfScs == 2:
                        result = self.sshLib.sendCommand(command, 2, 2)
                        self.fail(result[0], result[1])
                        if result[1] != '':
                            self.fail('ERROR', 'There is STILL a SSHD configured by COM running')
                self.setTestStep('Unlock COM SA on both SCs')
                if self.testcase_tag == 'TC-AMFSSHD-002':
                    # unlock all SC's
                    self.unlockSu(1)
                    if self.noOfScs == 2:
                        self.unlockSu(2)

                if self.testcase_tag == 'TC-AMFSSHD-006':
                    # unlock all SC's
                    if self.noOfScs == 2:
                        self.unlockSu(2)
                        self.unlockSu(1)

                # update ACTIVE system controller
                result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                self.activeController = result[1]
                self.activeCtrlAddr = self.targetData['ipAddress']['ctrl']['ctrl%d'%self.activeController[1]]

                # activate Amf handling SSHD
                self.ActivateAmfControllSshd(26)   # Set the CLI port to 26
                # reload the configuration
                self.reloadSSHDOam()
                # Set up Authorized Key
                self.setupAuthorizedKey()
                self.setTestStep('Check: There is a SSHD configured by COM running')
                # check that there is SSHD configured COM process is running
                command = 'ps auxwww | grep "\d*.*/usr/sbin/sshd\s\-D -f %s"  | awk \'{print $2}\'' %self.oamSshdconfiguration
                result = self.sshLib.sendCommand(command, 2, self.activeController[1])
                self.fail(result[0], result[1])
                if result[1] == '':
                    self.fail('ERROR', 'There is no SSHD configured by COM running')
                # SSH to port 26 and check CLI is running. Now active node should be node 1
                self.testCLIonPort(26)
                # SSH to port 830 and check Netconf is running
                self.testNetconfOnPort(830)

            if self.testcase_tag == 'TC-AMFSSHD-003':
                # Simulate SSHD crashs
                cmd = 'date +\%s'
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])
                currTime = int(result[1])

                self.setTestStep('Simulating crash of the OAM controlled SSHD')
                command = 'kill -9 $(ps aux | grep sshd_config_oam | grep -v grep |  awk \'{print $2}\')'
                result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                self.activeController = result[1]

                self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)
                self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])
                result = self.sshLib.sendCommand(command)
                self.fail(result[0], result[1])
                self.miscLib.waitTime(20)

                # Verify that the SSHD configured by COM is running
                command = 'ps aux | grep sshd_config_oam | grep -v grep |  awk \'{print $2}\''
                result = self.sshLib.sendCommand(command)
                self.fail(result[0], result[1])
                if result[1] == '':
                   self.fail("ERROR", "OAM SSHD is not running")

                # Confirm CLI works again
                self.myLogger.info('Confirm CLI works again')
                self.testCLIonPort(26)
                # SSH to port 830 and check Netconf is running
                self.testNetconfOnPort(830)

            self.comsa_lib.removeAuthorizedKey(self.testConfig)
        else:
            if ComOK[1] == False:
                self.myLogger.info('Skipped the test because the COM version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; COM version is not compatible')
            if ComsaOK[1] == False:
                self.myLogger.info('Skipped the test because the COM SA version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; COM SA version is not compatible')
            if CmwOK[1] == False:
                self.myLogger.info('Skipped the test because the CMW version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; CMW version is not compatible')

            if ((self.noOfScs == 1) and (self.testcase_tag == 'TC-AMFSSHD-006')):
                self.myLogger.info('Skipped the switchover test because running on a single-node cluster')
                self.setAdditionalResultInfo('Test skipped; Running on a single-node cluster')

        self.myLogger.info("exit runTest")

        coreTestCase.CoreTestCase.runTest(self)

    def reloadSSHDOam(self):
        self.setTestStep('Reloading SSHD Oam configuration')
        result = self.sshLib.sendCommand('ps auxwww | grep "\d*.*/usr/sbin/sshd\s\-D -f %s"  | awk \'{print $2}\'' %self.oamSshdconfiguration, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        pidSshd = result[1]
        result = self.sshLib.sendCommand('kill -1 %s' %pidSshd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])

    def testCLIonPort(self, Port):
        self.setTestStep('Test CLI on Port :%s' %Port)
        #This function required to run setupAuthorizedKey() first
        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params_for_sshd(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script, Port)
        cmd = '%s "show" "exit"' %self.cli_active_controller_login_params
        result = self.comsa_lib.executeCliSession(cmd)
        if 'ManagedElement=1' not in result[1]:
            self.fail('ERROR', 'SSHD is not under control of COM')

    def testNetconfOnPort(self, Port):
        self.setTestStep('Test Netconf on Port :%s' %Port)
        #This function required to run setupAuthorizedKey() first
        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params_for_sshd(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script, Port)
        cmd = '%s "<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"> <close-session/> </rpc> ]]>]]>"' %self.cli_active_controller_login_params
        result = self.comsa_lib.executeNetConfSession(cmd)
        if '<capability>urn:ietf:params:netconf:base' not in result[1]:
            self.fail('ERROR', 'NetConf is not under control of COM')

    def setupAuthorizedKey(self):
        self.setTestStep('Creating authorized key to active controller')

        self.pathToConfigFilesForAuthorized = '%s%s'%(self.MY_REPOSITORY, self.pathToConfigFiles)
        cmd = '%s%s %s  -k ~/.ssh/id_rsa' %(self.pathToConfigFilesForAuthorized, self.pwdFreeScript, self.activeCtrlAddr)

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

    def removeAllCOMSAsshdConfig(self):
        self.myLogger.info('Removing all changess in the main SSHD configuration made by COM SA')
        # remove all COM SA sshd config on both SCs
        command = 'update_sshd -d'
        result = self.sshLib.sendCommand(command,2,1)
        self.fail(result[0], result[1])
        if self.noOfScs == 2:
            result = self.sshLib.sendCommand(command,2,2)
            self.fail(result[0], result[1])

    def ActivateAmfControllSshd(self,cliPort):
        self.setTestStep('Activate AMF controlled SSHD')
        # backup the file sshd_config_oam
        command = 'cp %s/com-apr9010443/etc/sshd/%s %s%s' %(self.configLocation, self.comSshdConfigOam, self.amfSshdTempDir, self.comSshdConfigOam)
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        # Enable COM controlled SSHD
        command = 'sed  -i "s/<sshdManagement>.*<\/sshdManagement>/<sshdManagement>true<\/sshdManagement>/" %s/com-apr9010443/lib/comp/libcom_sshd_manager.cfg' %self.configLocation
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        command = 'sed  -i "s/<cliPort>[0-9]*<\/cliPort>/<cliPort>%s<\/cliPort>/" %s/com-apr9010443/lib/comp/libcom_sshd_manager.cfg' %(cliPort, self.configLocation)
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        command = 'sed  -i "s/ListenAddress *[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}:[0-9]\+/ListenAddress 0\.0\.0\.0/" %s/com-apr9010443/etc/sshd/%s' %(self.configLocation, self.comSshdConfigOam)
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        command = 'sed  -i "s/DenyUsers root/#DenyUsers root/" %s/com-apr9010443/etc/sshd/%s' %(self.configLocation, self.comSshdConfigOam)
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])


    def DeactivateAmfControllSshd(self,cliPort):
        self.setTestStep('Deactivate AMF controlled SSHD')

        # restore the file sshd_config_oam
        command = 'cp %s%s %s/com-apr9010443/etc/sshd/%s' %(self.amfSshdTempDir, self.comSshdConfigOam, self.configLocation, self.comSshdConfigOam)
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        # Disable COM controll SSHD
        command = 'sed  -i "s/<sshdManagement>.*<\/sshdManagement>/<sshdManagement>false<\/sshdManagement>/" %s/com-apr9010443/lib/comp/libcom_sshd_manager.cfg' %self.configLocation
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        command = 'sed  -i "s/<cliPort>[0-9]*<\/cliPort>/<cliPort>%s<\/cliPort>/" %s/com-apr9010443/lib/comp/libcom_sshd_manager.cfg' %(cliPort, self.configLocation)
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

    def lockSu(self, scNumber):
        self.myLogger.info('Locking su safSu=Cmw%s,safSg=2N,safApp=ERIC-ComSa' %scNumber)
        command = 'amf-adm lock safSu=Cmw%s,safSg=2N,safApp=ERIC-ComSa' %scNumber
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        command = 'amf-adm lock-in safSu=Cmw%s,safSg=2N,safApp=ERIC-ComSa' %scNumber
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

    def unlockSu(self, scNumber):
        self.myLogger.info('Unlocking su safSu=Cmw%s,safSg=2N,safApp=ERIC-ComSa' %scNumber)
        command = 'amf-adm unlock-in safSu=Cmw%s,safSg=2N,safApp=ERIC-ComSa' %scNumber
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

        command = 'amf-adm unlock safSu=Cmw%s,safSg=2N,safApp=ERIC-ComSa' %scNumber
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])

    def restartCOMSAbyAmfAdmin(self):
        if self.activeController[1] == 1:
            self.setTestStep('Restarting COM SA on SC-1 by amf-adm lock/unlock')
            # Lock SC-2 first. This will prevent switchover
            if self.noOfScs == 2:
                self.lockSu(2)
            self.lockSu(1)
            # Sleep 10 seconds
            self.miscLib.waitTime(10)
            # Unlock SC-1 first. So it will continue to be the active SC.
            self.unlockSu(1)
            if self.noOfScs == 2:
                self.unlockSu(2)
        if self.activeController[1] == 2:
            self.setTestStep('Restarting COM SA on SC-2 by amf-adm lock/unlock')
            # Lock SC-1 first. This will prevent switchover
            self.lockSu(1)
            if self.noOfScs == 2:
                self.lockSu(2)
            # Sleep 10 seconds
            self.miscLib.waitTime(10)
            # Unlock SC-2 first. So it will continue to be the active SC.
            if self.noOfScs == 2:
                self.unlockSu(2)
            self.unlockSu(1)

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
        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout = 120, numberOfRetries = 5)
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

        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout = 120, numberOfRetries = 5)
        self.fail(result[0], result[1])
        comInstSdpName = name_list.split('/')[len(name_list.split('/')) - 1]

        #Install to system
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comInstSdpName, 'com', False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')

    def installCOMSA(self, setupFilesDir, pathToComsaInstallation, buildComsa):
        self.logger.info('installCOMSA: Called')
        self.logger.info('installCOMSA: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCOMSA: pathToComsaInstallation = %s' %pathToComsaInstallation)

        if buildComsa == 'True':
            sdpNames = [self.cxpSdpName, self.installSdpName, self.installSdpNameSingle, self.removeSdpName, self.removeSdpNameSingle]
            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildTokenDir, self.tokenPattern)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0], result[1])
            makeOption = ''
            if self.linuxDistro == self.distroTypes[1]: # rhel
                makeOption = 'rhel_sdp'
            result = self.comsa_lib.buildCOMSA(self.buildSrc, self.buildRelease, len(self.testConfig['controllers']), sdpNames, makeOption)
            self.fail(result[0], result[1])

            result = self.comsa_lib.copyComSaSdpsToSwDir(self.buildRelease, self.resourceFilesLocation, len(self.testConfig['controllers']), sdpNames, self.linuxDistro)
            self.fail(result[0], result[1])

            # Release the token
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildTokenDir, self.tokenPattern)
            self.fail(result[0], result[1])

        # Install time
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        noOfScs = len(self.testConfig['controllers'])
        result = self.miscLib.execCommand("ls %s/%s | awk -F'/' '{print $NF}'" %(setupFilesDir,self.cxpSdpName))
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', result[1])
        self.cxpSdpName = result[1].rstrip()
        if noOfScs == 2:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' %(setupFilesDir, self.cxpSdpName), '%s/%s' %(setupFilesDir, self.installSdpName)], self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpName, 'comsa', False, backupRpms = self.backupRpmScript)
        elif noOfScs == 1:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' %(setupFilesDir, self.cxpSdpName), '%s/%s' %(setupFilesDir, self.installSdpNameSingle)],self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpNameSingle, 'comsa', False, backupRpms = self.backupRpmScript)

        self.fail(result[0], result[1])
        campaignStartTime = result[2] # This is not used!!!
        campaignName = result[3] # This is not used!!!

        self.logger.info('installCOMSA: Exit')

    def upgradeCOM(self, setupFilesDir, pathToComInstallation):
        self.logger.info('UpgradeCOM: Called')
        self.logger.info('upgradeCOM: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('upgradeCOM: pathToComInstallation = %s' %pathToComInstallation)
        result = self.sshLib.sendCommand('rm -rf %s' %pathToComInstallation) #def sendCommand(command, subrack=0, slot=0):
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
        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout = 120, numberOfRetries = 5)
        self.fail(result[0], result[1])

        comRtSdpname = name_list.split('/')[len(name_list.split('/')) - 1]

        # determine suitable package for 1 or 2 controller node
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            cmd = 'ls %s/ERIC-COM-BFU*.sdp' %(setupFilesDir)
        elif noOfScs == 1:
            cmd = 'ls %s/ERIC-COM-BFU*.sdp' %(setupFilesDir)
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

        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout = 120, numberOfRetries = 5)
        self.fail(result[0], result[1])
        comUpgdSdpName = name_list.split('/')[len(name_list.split('/')) - 1]

        #Install to system
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comUpgdSdpName, 'com',
                                            False, False, False, False, False, self.createBackupDuringCampaign, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')

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
                self.logger.info('findComBackup: Exit')
                self.fail('ERROR', 'findComBackup: COM backup not found!')
            self.logger.info('findComBackup: Exit')
            return backupName

    def copyComBackupFiles(self,tmpComBackupName):
        if tmpComBackupName != {}:
            command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, tmpComBackupName, self.storedBackupFilesLocation, tmpComBackupName)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

            command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, tmpComBackupName, self.storedBackupFilesLocation, tmpComBackupName)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

            command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.lotcBackupLocation, tmpComBackupName, self.storedBackupFilesLocation)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

    def copyBackupFiles(self, backupName):
        result = self.sshLib.sendCommand('mkdir %s' %self.storedBackupFilesLocation)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, backupName, self.storedBackupFilesLocation, backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, backupName, self.storedBackupFilesLocation, backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, backupName, self.storedBackupFilesLocation, backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.lotcBackupLocation, backupName, self.storedBackupFilesLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

    def replaceCopiedComBackupFiles(self,comBackupName):
        command = '\cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, comBackupName, self.comBackupLocation, comBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, comBackupName, self.cmwBackupLocation, comBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, comBackupName, self.lotcBackupLocation)
        result = self.sshLib.sendCommand (command)
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

    def replaceCopiedBackupFiles(self, tmpBackupName):

        #recopy the backup files
        command = '\cp %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, tmpBackupName, self.comsaBackupLocation, tmpBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = 'mkdir -p %s' %(self.comBackupLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])
        command = '\cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, tmpBackupName, self.comBackupLocation, tmpBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, tmpBackupName, self.cmwBackupLocation, tmpBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, tmpBackupName, self.lotcBackupLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

    def upgradeCOMSA(self):
        self.setTestStep('Build the current COM SA with comsabuild all')

        #using buildAndStoreCOMSA() fn
        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
        if BuildPath[0] != 'SUCCESS':
            self.logger.error(result[1])
            self.logger.debug('upgradeCOMSAFromStream: Exit')
            return (BuildPath[0], 'Build COM SA failed')

        self.setTestStep('Copy the COM SA installation files to the target')

        # copy the BFU archives to the target.
        self.myLogger.debug('Copying the BFU archive files to the target')
        result = self.comsa_lib.copyFilesToTarget(['%s/' %BuildPath[9], '%s/' %BuildPath[10]], self.temp_bfu, True)
        self.fail(result[0],result[1])

        self.setTestStep('Unpack the COM SA installation archives on the target')
        self.myLogger.debug('Unpacking the BFU archives on the target')
        # BuildPath[4]:  is tar file of COM SA bundle
        cmd = 'cd %s ; tar xf %s' %(self.temp_bfu, BuildPath[4])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        # BuildPath[5]: is tar file of COM SA template
        cmd = 'cd %s ; tar xf %s' %(self.temp_bfu, BuildPath[5])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.setTestStep('Import the COM SA BFU campaign and bundle SDPs to CoreMW repository')
        self.myLogger.debug('Importing the COM SA BFU campaign and bundle SDPs to CoreMW repository')
        # BuildPath[1] : is runtime sdp file of COM SA
        bfuBundleSdp = '%s%s' %(self.temp_bfu, self.cxpSdpNameOffical)

        # copy to /home/coremw/incoming because importSwBundle() uses this dir !
        cmd = '\cp -f %s %s' %(bfuBundleSdp, self.temp_dir)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # determine the BFU campaign SDP name with full path
        cmd = 'find %s  -type f | grep sdp | grep UBFU' %(self.temp_bfu)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        upgradeCampaignSdp = result[1]

        # copy to /home/coremw/incoming because importSwBundle() uses this dir !
        cmd = '\cp %s %s' %(upgradeCampaignSdp, self.temp_dir)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # obtain only the filename of the campaign SDP
        cmd = 'ls -lR %s | grep \'C+P\' | awk \'{print $9}\'' %(self.temp_bfu)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        upgradeCampaignSdp = result[1]

        # Run the upgrade campaign

        self.setTestStep('Run the COM SA upgrade campaign')
        self.myLogger.debug('Run the COM SA upgrade campaign')

        result = self.comsa_lib.installComp(self.temp_dir, self.cxpSdpNameOffical, upgradeCampaignSdp, 'comsa', createBackup = False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])

        campaignStartTime = result[2]
        campaignName = result[3]
        result = self.comsa_lib.calculateComponentInstallationTime(campaignStartTime, campaignName, self.testConfig)
        self.fail(result[0], result[1])
        comsaInstallationTime = result[1]

        result = self.lib.getComponentVersion(self.comsaCxpNumber)
        self.fail(result[0], result[1])
        self.setAdditionalResultInfo('To Release: %s, Version: %s' %(result[1], result[2]))

        self.setAdditionalResultInfo('COM SA upgrade time: %d' %comsaInstallationTime)
        self.comsa_lib.addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'COM SA upgrade time', comsaInstallationTime)
        self.myLogger.info('charMeasurements - COM SA upgrade time: %s' %str(comsaInstallationTime))

    def tearDown(self):
        self.setTestStep('tearDown')
        if self.skip_test == False:
            self.myLogger.info('Teardown')
            self.comsa_lib.removeAuthorizedKey(self.testConfig)
            self.DeactivateAmfControllSshd(22)  # set the port back to 22
            # Restart COM SA
            self.restartCOMSAbyAmfAdmin()

            if (self.testcase_tag == 'TC-AMFSSHD-004' or
                self.testcase_tag == 'TC-AMFSSHD-005' or
                self.testcase_tag == 'TC-AMFSSHD-007'):
                self.replaceCopiedBackupFiles(self.backupName)
                #replace the com backup files
                if self.comBackupName != {}:
                    self.replaceCopiedComBackupFiles(self.comBackupName)
                # self.setTestStep('======== Restore system ========')
                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                self.fail(result[0],result[1])

            # Remove temp dir
            command = '\\rm -r %s' %self.amfSshdTempDir
            result = self.sshLib.sendCommand(command,2,1)
            self.fail(result[0], result[1])

        else:
            self.myLogger.info('Teardown skipped')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
