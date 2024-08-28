#!/vobs/tsp_saf/tools/Python/linux/bin/python
# coding=iso-8859-1
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

    TC-SUGAR-001 Install COM SA 3.7 in SUGaR environment and observe that COM and COM SA execute as a non-root user
    TC-SUGAR-002 Upgrade COM SA to COM SA 3.7 in SUGaR environment and observe that COM and COM SA start to execute as a non-root user.
    TC-SUGAR-003 Execute backups while COM and COM SA execute as a non-root user
    TC-SUGAR-004 Installing COM SA in non SUGaR environment. Observe the correct permissions and that COM and COM SA execute as root
    TC-SUGAR-005 Install COM SA in a non-SUGaR environment. Then upgrade CoreMW and after that upgrade COM to SUGaR and observe reduced privileges of COM and COM SA
    TC-SUGAR-006 Install COM SA in a non-SUGaR environment. Then upgrade COM and after that upgrade CoreMW to SUGaR and observe reduced privileges of COM and COM SA
    TC-SUGAR-007 Upgrade COM SA to COM SA 3.7 in non-SUGaR environment and observe that COM and COM SA execute as root user.

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

class Sugar(coreTestCase.CoreTestCase):

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
        self.backupName = "sugar_backup"
        self.comBackupName = {}
        self.storedBackupFilesLocation = {}
        self.comsaBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}
        self.lotcBackupLocation = {}
        self.testBackupName = "testBackup"


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

        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' % (self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.pathToModelFiles = '%s%s' % (self.COMSA_VERIF_PATH, dict.get("FT763_MODELFILE_PATH"))
        self.installStressTool = eval(System.getProperty("runStressTool"))
        self.temp_dir = '/home/coremw/incoming/'
        self.temp_bfu = '/home/bfu/'
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        self.cxpArchive = '%s%s' % (self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.absDir = '%s%s' % (self.COMSA_REPO_PATH, dict.get("ABS"))
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.deplTemplArchive = dict.get('COM_SA_DEPL_TEMPL_ARCHIVE_RHEL')
            self.bundleArchive = dict.get('COM_SA_BUNDLE_ARCHIVE_RHEL')
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.buildRelease = '%s%s' % (self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.deplTemplArchive = dict.get('COM_SA_DEPL_TEMPL_ARCHIVE')
            self.bundleArchive = dict.get('COM_SA_BUNDLE_ARCHIVE')
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.buildRelease = '%s%s' % (self.COMSA_REPO_PATH, dict.get('RELEASE'))
        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' % user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5
        self.buildDir = dict.get('BUILD_TOKENS')

        self.resourceFilesLocation = dict.get("PATH_TO_MR36131")
        self.modelFileList = dict.get("COM_MODEL_FILE_LIST")
        self.clearLocation = '/cluster/storage/clear/'
        self.configLocation = '/cluster/storage/system/config/'
        self.softwareLocation = '/cluster/storage/system/software'
        self.nobackupLocation = '/cluster/storage/no-backup/'
        self.storageLocation = '/cluster/home/'
        self.comsaDirUnderPso = 'comsa_for_coremw-apr9010555'
        self.comsaBin = '/usr/bin/'
        self.comPidFile = '/opt/com/run/com.pid'
        self.homeTempDir = '/home/tempSugarMR/'
        self.pathToCmwInstallation = '%s/coremw/' % self.homeTempDir
        self.pathToComInstallation = '%s/com/' % self.homeTempDir
        self.pathToComsaInstallation = '%s/comsa/' % self.homeTempDir
        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        self.CoreMWSdp34 = 'coremw_x86_64-3.4_CP11-runtime_CXP9020355_1_R8M.tar'
        self.CoreMWSdp35PRA = 'coremw_x86_64-3.5_PRA.tar'
        self.CoreMWSdp35CP = 'coremw_x86_64-3.5_CP5-runtime_CXP9020355_1_R9F.tar'
        self.CoreMWSdp35CP_DEPL = 'coremw_x86_64-3.5_CP5-deployment_CXP9017564_1_R9F.tar'
        self.campaignCMWUgradeName = 'ERIC-CMWUpgrade'
        self.coremw34 = "%s/coremw/coremw3.4cp11/" % self.resourceFilesLocation
        self.coremw35 = "%s/coremw/coremw3.5cp5/" % self.resourceFilesLocation
        self.com50 = "%s/com/com5.0/" % self.resourceFilesLocation
        self.com51 = "%s/com/com5.1/" % self.resourceFilesLocation
        self.sugar_com = "%s/com/sugar_combb/" % self.resourceFilesLocation
        self.ComSABuild = "%s/comsa/" % self.resourceFilesLocation
        self.comsa35 = "%s/comsa/comsa3.5/" % self.resourceFilesLocation
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')
        self.buildSrc = '%s%s' % (self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' % (self.MY_REPOSITORY, self.pathToConfigFiles)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs=self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.myLogger.info('runTest')
        ComsaOK = ('SUCCESS', True)
        ComOK = ('SUCCESS', True)
        CmwOK = ('SUCCESS', True)
        self.skip_test = False
        self.skip_sles12 = False

        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
        self.fail(ComsaOK[0], ComsaOK[1])
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion)
        self.fail(CmwOK[0], CmwOK[1])
        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion)
        self.fail(ComOK[0], ComOK[1])

        if ComsaOK[1] and CmwOK[1] and ComOK[1]:
            self.skip_test = False
        else:
            self.skip_test = True

        # Skipped those testcases which required old coremw and com installation
        if self.testcase_tag == 'TC-SUGAR-002' or self.testcase_tag == 'TC-SUGAR-004' or self.testcase_tag == 'TC-SUGAR-005' or self.testcase_tag == 'TC-SUGAR-006' or self.testcase_tag == 'TC-SUGAR-007':
            self.skip_sles12 = True

        if self.skip_sles12 and self.linuxDistro == self.distroTypes[2]:
            self.skip_test = True

        if self.installStressTool:
            self.setTestStep('======== Install the stress tool ========')
            self.comsa_lib.installStressToolOnTarget(self)
            stressTimeOut = 60
            self.setTestStep('======== Start the stress tool ========')

            # Determine the number of processor cores in the node
            result = self.comsa_lib.getNumOfCPUsOnNode(self)
            self.fail(result[0], result[1])
            numOfCpuCores = result[1];
            self.myLogger.debug('Found %s CPU cores' % numOfCpuCores)

            # Determine the total physical RAM in the node
            result = self.comsa_lib.getBytesOfRamOnNode(self)
            self.fail(result[0], result[1])
            totalRamBytes = result[1];
            tenPercentOfTotalRam = int(totalRamBytes) // 10
            self.myLogger.debug('Found total %s bytes of RAM, 10 percent is %s' % (totalRamBytes, tenPercentOfTotalRam))

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, no disk stress
            # result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 0, 0)

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM
            # plus NFS disk stress 1 task 64K bytes blocks plus local disk stress 2 tasks 4M bytes blocks
            result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60 * 60 * 60, 0, 0, 1, 65536)
            self.sshLib.setTimeout(stressTimeOut)

        if self.skip_test == False:
            self.startUnixTime = 0
            if self.testcase_tag == 'TC-SUGAR-001':
                self.checkSugarSupported()

            elif self.testcase_tag == 'TC-SUGAR-003':
                # Create a backup
                self.setTestStep('Creating backup system name %s' % self.backupName)
                result = saf_lib.isBackup(self.backupName)
                self.fail(result[0], result[1])
                if result != ('SUCCESS', 'NOT EXIST'):
                    result = saf_lib.backupRemove(self.backupName)
                    self.fail(result[0], result[1])

                result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
                self.fail(result[0], result[1])
                # List all backups
                result = saf_lib.isBackup(self.backupName)
                self.fail(result[0], result[1])
                if result != ('SUCCESS', 'EXIST'):
                    self.fail('ERROR', 'Can\'t find backup name %s' % self.backupName)
                # Restore a backup
                self.setTestStep('Restoring system backup name %s' % self.backupName)
                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup=False)
                self.fail(result[0], result[1])
                # Remove a backup
                result = saf_lib.isBackup(self.backupName)
                self.fail(result[0], result[1])
                if result != ('SUCCESS', 'NOT EXIST'):
                    result = saf_lib.backupRemove(self.backupName)
                    self.fail(result[0], result[1])
                # Observe that all the above operations are successful.
                self.checkSugarSupported()
            elif self.testcase_tag == 'TC-SUGAR-002':

                self.setTestStep('Restore the COM backup')
                self.comBackupName = self.findComBackup(self.comBackupName)
                result = self.comsa_lib.restoreSystem(self, self.comBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 2, removeBackup = False)
                self.fail(result[0],result[1])

                # Install COMSA
                self.setTestStep('======== Install old COM SA ========')

                self.installCOMSA(self.comsa35, self.pathToComsaInstallation, 'False')

                self.checkSugarNoneSupported()

                # Upgrade COMSA
                self.upgradeCOMSA()

                # Check Sugar supported in COMSA 3.7
                self.checkSugarSupported()

            elif self.testcase_tag == 'TC-SUGAR-004' or self.testcase_tag == 'TC-SUGAR-005' or self.testcase_tag == 'TC-SUGAR-006' or self.testcase_tag == 'TC-SUGAR-007':

                # 1.Create Backup and Copy backup files to stored location
                self.setTestStep('======== Backup system ========')
                self.backupCluster(self.backupName)

                # 2.Copy backup files to stored location
                self.setTestStep('======== Copy backup files to stored location =========')

                result = self.sshLib.sendCommand('\\rm -rf %s' % self.storedBackupFilesLocation)
                self.fail(result[0], result[1])
                self.copyBackupFiles(self.backupName)


                # 3.Uninstall system

                self.setTestStep('======== Uninstall system ========')

                result = self.sshLib.sendCommand('mkdir %s' % self.homeTempDir)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' % self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' % self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' % self.pathToComsaInstallation)
                self.fail(result[0], result[1])

                # copy uninstall script to cluster
                result = self.sshLib.remoteCopy('%s/%s' % (self.uninstallScriptLocation2, self.uninstallScriptName1), self.homeTempDir, timeout=120)
                self.fail(result[0], result[1])

                result = self.sshLib.remoteCopy('%s/%s' % (self.uninstallScriptLocation2, self.uninstallScriptName2), self.homeTempDir, timeout=120)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('chmod +x %s/*.sh' % self.homeTempDir)
                self.fail(result[0], result[1])

                # run Uninstall
                result = self.comsa_lib.unInstallSystem(self.homeTempDir, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater)
                self.fail(result[0], result[1])

                cmw_uninstall_command2 = '%s%s' % (self.homeTempDir, self.uninstallScriptName2)
                result = self.sshLib.sendCommand (cmw_uninstall_command2)
                self.fail(result[0], result[1])

                self.lib.resetDumps()

                # 4.Install
                result = self.sshLib.sendCommand('mkdir %s' % self.homeTempDir)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' % self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' % self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' % self.pathToComsaInstallation)
                self.fail(result[0], result[1])

                # Install CoreMW 3.4
                self.setTestStep('======== Install CoreMW 3.4 ========')

                result = self.sshLib.remoteCopy('%s/%s' % (self.coremw34, self.CoreMWSdp34), self.pathToCmwInstallation, timeout=120)
                self.fail(result[0], result[1])

                result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp34, backupRpms = self.backupRpmScript)
                self.fail(result[0], result[1])

                # Install COM
                self.setTestStep('======== Install COM 5.0========')

                result = self.installCOM(self.com50, self.pathToComInstallation)

                if self.testcase_tag == 'TC-SUGAR-007':
                    # Install COMSA 3.5
                    self.setTestStep('======== Install COM SA 3.5 ========')

                    self.installCOMSA(self.comsa35, self.pathToComsaInstallation, 'False')

                    self.checkSugarNoneSupported()
                else:
                    # Install current COMSA
                    self.setTestStep('======== Install current COM SA ========')

                    self.installCOMSA(self.ComSABuild, self.pathToComsaInstallation, 'True')

                    self.checkSugarNoneSupported()

                if self.testcase_tag == 'TC-SUGAR-005':

                    # Upgrade CMW
                    self.setTestStep('======== Upgrade to CMW35CP5 ========')
                    self.logToSys()
                    self.upgradeCMW()
                    self.checkSugarNoneSupported()

                    # Upgrade COM
                    self.setTestStep('======== Upgrade to COM51PRA ========')  # Currently using COM BB
                    self.logToSys()
                    self.upgradeCOM(self.sugar_com, self.pathToComInstallation)
                    self.checkSugarSupported()

                elif self.testcase_tag == 'TC-SUGAR-006':

                    # Upgrade COM
                    self.setTestStep('======== Upgrade to COM51PRA ========')  # Currently using COM BB
                    self.logToSys()
                    self.upgradeCOM(self.sugar_com, self.pathToComInstallation)
                    self.checkSugarNoneSupported()

                    # Upgrade CMW
                    self.setTestStep('======== Upgrade to CMW35CP5 ========')
                    self.logToSys()
                    self.upgradeCMW()
                    self.checkSugarSupported()

                elif self.testcase_tag == 'TC-SUGAR-007':

                    # Upgrade COMSA
                    self.setTestStep('======== Upgrade to current COMSA ========')
                    self.logToSys()
                    self.upgradeCOMSA()
                    self.checkSugarNoneSupported()

        else:
            if self.skip_sles12 == True:
                self.myLogger.info('Skipped the test because SLES12 is detected!')
                self.setAdditionalResultInfo('Test skipped; Running under SLES12')
            if ComOK[1] == False:
                self.myLogger.info('Skipped the test because the COM version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; COM version is not compatible')
            if ComsaOK[1] == False:
                self.myLogger.info('Skipped the test because the COM SA version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; COM SA version is not compatible')
            if CmwOK[1] == False:
                self.myLogger.info('Skipped the test because the CMW version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; CMW version is not compatible')

        self.myLogger.info("exit runTest")

        coreTestCase.CoreTestCase.runTest(self)

    def findComBackup(self, comBackupName):
        """
        If comBackupName is defined, the method simply returns the same name.
        If comBackupName is not defined, the method returns the latest backup which's name
        contains COM (case insensitive), but does not contain comsa, com_sa, com-sa (case insensitive)
        """
        self.myLogger.info('findComBackup: Called')
        if comBackupName != {}:
            self.myLogger.info('findComBackup: Exit')
            return comBackupName
        else:
            cmd = """cmw-partial-backup-list 2>&1 | sed 's/\[//g' | sed 's/\]//g' | grep -i com | egrep -iv '(comsa)|(com_sa)|(com-sa)' | tail -1 | awk '{print $NF}' """
            # We search for the latest COM backup
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            backupName = result[1]
            if backupName == '':
                self.myLogger.info('findComBackup: Exit')
                self.fail('ERROR', 'findComBackup: COM backup not found!')
            self.myLogger.info('findComBackup: Exit')
            return backupName


    def installCOM(self, setupFilesDir, pathToComInstallation):
        self.logger.info('installCOM: Called')
        self.logger.info('installCOM: setupFilesDir = %s' % setupFilesDir)
        self.logger.info('installCOM: pathToComInstallation = %s' % pathToComInstallation)
        result = self.sshLib.sendCommand('\\rm -rf %s' % pathToComInstallation)  # def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' % pathToComInstallation)  # def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])


        cmd = 'ls %s/COM-*.sdp' % (setupFilesDir)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM runtime sdp file not found at specified location: %s/ .' % setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM runtime sdp file found at specified location: %s/: %s.' % (setupFilesDir, str(result[1])))
        name_list = result[1].strip()
        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout=120, numberOfRetries=5)
        self.fail(result[0], result[1])

        comRtSdpname = name_list.split('/')[len(name_list.split('/')) - 1]

        # determine suitable package for 1 or 2 controller node
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            cmd = 'ls %s/ERIC-COM-I1*.sdp' % (setupFilesDir)
        elif noOfScs == 1:
            cmd = 'ls %s/ERIC-COM-I2*.sdp' % (setupFilesDir)
        else:
            self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' % str(noOfScs))

        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM campaign sdp file not found at specified location: %s/ .' % setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM campaign sdp file found at specified location: %s/: %s.' % (setupFilesDir, str(result[1])))
        name_list = result[1].strip()
        self.logger.info('name_list: (%s)' % name_list)

        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout=120, numberOfRetries=5)
        self.fail(result[0], result[1])
        comInstSdpName = name_list.split('/')[len(name_list.split('/')) - 1]

        # Install to system
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comInstSdpName, 'com', False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')

    def installCOMSA(self, setupFilesDir, pathToComsaInstallation, buildComsa):
        self.logger.info('installCOMSA: Called')
        self.logger.info('installCOMSA: setupFilesDir = %s' % setupFilesDir)
        self.logger.info('installCOMSA: pathToComsaInstallation = %s' % pathToComsaInstallation)

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

        result = self.sshLib.sendCommand('\\rm -rf %s' % pathToComsaInstallation)  # def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' % pathToComsaInstallation)  # def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' % (setupFilesDir, self.cxpSdpName), '%s/%s' % (setupFilesDir, self.installSdpName)], self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpName, 'comsa', False, backupRpms = self.backupRpmScript)
        elif noOfScs == 1:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' % (setupFilesDir, self.cxpSdpName), '%s/%s' % (setupFilesDir, self.installSdpNameSingle)], self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpNameSingle, 'comsa', False, backupRpms = self.backupRpmScript)

        self.fail(result[0], result[1])
        campaignStartTime = result[2]  # This is not used!!!
        campaignName = result[3]  # This is not used!!!

        self.logger.info('installCOMSA: Exit')

    def upgradeCMW(self):
        self.logger.info('upgradeCMW: Called')
        self.logger.info('upgradeCMW: setupFilesDir = %s' % self.coremw35)
        self.logger.info('upgradeCMW: pathToCmwInstallation = %s' % self.pathToCmwInstallation)
        self.logger.info('upgradeCMW: Copying of File(s) for CMW installation to the target.')

        # Cleaning the directory
        result = self.sshLib.sendCommand('rm -rf %s' % self.pathToCmwInstallation)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' % self.pathToCmwInstallation)
        self.fail(result[0], result[1])

        # Copy deployment tar file
        result = self.sshLib.remoteCopy('%s%s' %(self.coremw35, self.CoreMWSdp35CP_DEPL), self.pathToCmwInstallation, timeout=120, numberOfRetries=5)
        self.fail(result[0], result[1])
        #Copy runtime tar file
        result = self.sshLib.remoteCopy('%s%s' %(self.coremw35, self.CoreMWSdp35CP), self.pathToCmwInstallation, timeout=120, numberOfRetries=5)
        self.fail(result[0], result[1])

        #extract all tar files
        result = self.sshLib.sendCommand('tar xvf %s/*depl*.tar* ' % (self.pathToCmwInstallation))
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('tar xvf %s/*CXP9020355*.tar* ' % (self.pathToCmwInstallation))
        self.fail(result[0], result[1])

        # Upgrade of CMW
        cmw_common = 'COREMW_COMMON-CXP9017566_1.sdp'
        cmw_sc = 'COREMW_OPENSAF-CXP9017656_1.sdp'
        cmw_opensaf = 'COREMW_SC-CXP9017565_1.sdp'
        cmw_campaign='ERIC-COREMW-C+P-TEMPLATE-CXP9017564_1.sdp'

        self.logger.info('upgradeCMW: Upgrade of CMW ')
        # Import SDP package
        self.logger.info ('upgradeCMW: Importing SDP')
        result = self.comsa_lib.importSdpPackage(cmw_common)
        self.fail(result[0], result[1])

        result = self.comsa_lib.importSdpPackage(cmw_sc)
        self.fail(result[0], result[1])

        result = self.comsa_lib.importSdpPackage(cmw_opensaf)
        self.fail(result[0], result[1])

        result = self.comsa_lib.importSdpPackage(cmw_campaign)
        self.fail(result[0], result[1])

        # Start campaign
        self.logger.info ('upgradeCMW: campaign start')
        self.safLib.upgradeStart(self.campaignCMWUgradeName, '')
        self.fail(result[0], result[1])

        result = self.comsa_lib.waitForCampaignReady(self.campaignCMWUgradeName, timeout=2500, rollingUpgrade=True)
        self.fail(result[0], result[1])

        # Commiting the campaign
        self.logger.info ('upgradeCMW: Commiting')
        result = self.safLib.upgradeCommit(self.campaignCMWUgradeName)
        self.fail(result[0], result[1])

        result = self.safLib.removeSwBundle(self.campaignCMWUgradeName)
        self.fail(result[0], result[1])

        # Checking the cmw-status
        self.logger.info('upgradeCMW: Checking cmw-status ......')
        result = self.comsa_lib.waitForClusterStatusOk()
        self.logger.info('upgradeCMW: Exit')

    def upgradeCOM(self, setupFilesDir, pathToComInstallation):
        self.logger.info('UpgradeCOM: Called')
        self.logger.info('upgradeCOM: setupFilesDir = %s' % setupFilesDir)
        self.logger.info('upgradeCOM: pathToComInstallation = %s' % pathToComInstallation)
        result = self.sshLib.sendCommand('rm -rf %s' % pathToComInstallation)  # def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' % pathToComInstallation)  # def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])


        cmd = 'ls %s/COM-*.sdp' % (setupFilesDir)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM runtime sdp file not found at specified location: %s/ .' % setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM runtime sdp file found at specified location: %s/: %s.' % (setupFilesDir, str(result[1])))
        name_list = result[1].strip()
        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout=120, numberOfRetries=5)
        self.fail(result[0], result[1])

        comRtSdpname = name_list.split('/')[len(name_list.split('/')) - 1]

        # determine suitable package for 1 or 2 controller node
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            cmd = 'ls %s/ERIC-COM-BFU*.sdp' % (setupFilesDir)
        elif noOfScs == 1:
            cmd = 'ls %s/ERIC-COM-BFU*.sdp' % (setupFilesDir)
        else:
            self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' % str(noOfScs))

        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM campaign sdp file not found at specified location: %s/ .' % setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM campaign sdp file found at specified location: %s/: %s.' % (setupFilesDir, str(result[1])))
        name_list = result[1].strip()
        self.logger.info('name_list: (%s)' % name_list)

        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout=120, numberOfRetries=5)
        self.fail(result[0], result[1])
        comUpgdSdpName = name_list.split('/')[len(name_list.split('/')) - 1]

        # Install to system
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comUpgdSdpName, 'com', False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')


    def copyBackupFiles(self, backupName):


        result = self.sshLib.sendCommand('mkdir %s' % self.storedBackupFilesLocation)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scomsa_%s.tar.gz' % (self.comsaBackupLocation, backupName, self.storedBackupFilesLocation, backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' % (self.comBackupLocation, backupName, self.storedBackupFilesLocation, backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' % (self.cmwBackupLocation, backupName, self.storedBackupFilesLocation, backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' % (self.lotcBackupLocation, backupName, self.storedBackupFilesLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

    def backupCluster(self, backupName):
        self.logger.info('backupCluster: backupName = %s' % backupName)

        result = self.safLib.isBackup(backupName)
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])
        elif result != ('SUCCESS', 'NOT EXIST'):
            result = self.safLib.backupRemove(backupName)
            if result[0] != 'SUCCESS':
                self.fail(result[0], result[1])

        result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.testSuiteConfig['restoreBackup'] = backupName
        self.logger.info('backupCluster: exit')

    def logToSys(self):
        self.logger.info('logToSys: Called')
        #get date time
        command = 'date +%s'
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])
        self.clusterTime = result[1]

        #log to both SC
        command = 'logger "logToSys: called at %s"' %self.clusterTime
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            result = self.sshLib.sendCommand (command,2,1)
            self.fail(result[0], result[1])
            result = self.sshLib.sendCommand (command,2,2)
            self.fail(result[0], result[1])
        elif noOfScs == 1:
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])
        self.logger.info('logToSys: exiting')

    def checkSugarSupported(self):
        # Check permission list of file
        self.setTestStep('Check Sugar is supported ')
        self.checkFolderPermission('/opt/com', 'root', 'com-core', '755')
        self.checkFolderPermission('/opt/com/bin', 'root', 'com-core', '755')
        self.checkFolderPermission('/opt/com/lib', 'root', 'com-core', '750')
        self.checkFolderPermission('/opt/com/lib/comp', 'root', 'com-core', '750')
        self.checkFolderPermission('/opt/com/etc', 'root', 'com-core', '750')
        self.checkFolderPermission('/var/opt/comsa', 'com-core', 'com-core', '770')
        # self.checkFolderPermission(self.comsaBin, 'root', 'com-core', '750')

        self.checkFolderPermission('%s/comsa' % self.storageLocation, 'com-core', 'com-core', '750')
        self.checkFolderPermission('%s/comsa_for_coremw-apr9010555' % self.configLocation, 'root', 'com-core', '770')
        self.checkFolderPermission('%s/comsa_for_coremw-apr9010555' % self.softwareLocation, 'com-core', 'com-core', '750')
        self.checkFolderPermission('%s/comsa_for_coremw-apr9010555' % self.clearLocation, 'root', 'com-core', '770')
        self.checkFolderPermission('%s/comsa_for_coremw-apr9010555' % self.nobackupLocation, 'com-core', 'com-core', '750')
        self.checkFolderPermission('%s/com-apr9010443' % self.configLocation, 'root', 'com-core', '770')
        self.checkFolderPermission('%s/com-apr9010443' % self.clearLocation, 'root', 'com-core', '770')
        self.checkFolderPermission('%s/coremw/var/log/saflog/FaultManagementLog' % self.nobackupLocation, 'cmw-core', 'system-nbi-data', '770')
        self.checkFolderPermission('%s/coremw/var/log/saflog/FaultManagementLog/alarm' % self.nobackupLocation, 'cmw-core', 'system-nbi-data', '770')
        self.checkFolderPermission('%s/coremw/var/log/saflog/FaultManagementLog/alert' % self.nobackupLocation, 'cmw-core', 'system-nbi-data', '770')

        self.checkFilePermission('%scomsa-mim-tool' % self.comsaBin, 'root', 'com-core', '755')
        self.checkFilePermission('%scomsa_pso' % self.comsaBin, 'root', 'com-core', '755')
        self.checkFilePermission('%sbackup_comsa' % self.comsaBin, 'root', 'com-core', '755')
        self.checkFilePermission('%supdate_sshd' % self.comsaBin, 'root', 'com-core', '755')
        self.checkFilePermission('%scomsa.sh' % self.comsaBin, 'root', 'com-core', '755')
        self.checkFilePermission('%scomsa_storage' % self.comsaBin, 'root', 'com-core', '755')
        self.checkFilePermission('%sis-com-sshd-flag-enabled.sh' % self.comsaBin, 'root', 'com-core', '755')

        #self.checkFilePermission('/opt/com/lib/comp/coremw-com-sa.cfg', 'root', 'com-core', '640')
        self.checkFilePermission('/opt/com/lib/comp/coremw-com-sa.so', 'root', 'com-core', '640')
        self.checkFilePermission('/opt/com/lib/comp/coremw-pmt-sa.so', 'root', 'com-core', '640')
        self.checkFilePermission('/opt/com/lib/comsa_tp.so', 'com-core', 'com-core', '640')

        self.checkFilePermission('%s/com-apr9010443/lib/comp/coremw-com-sa.cfg' %self.configLocation, 'root', 'com-core', '640')
        self.checkFilePermission('%s/comsa_for_coremw-apr9010555/comsa_mdf_consumer' %self.configLocation, 'root', 'com-core', '755')
        #self.checkFilePermission('/opt/com/etc/com_sa_trace.conf', 'root', 'com-core', '640')
        self.checkFilePermission('%s/comsa_for_coremw-apr9010555/com_sa_trace.conf' % self.clearLocation, '', 'com-core', '660')
        self.checkFilePermission('%s/comsa_for_coremw-apr9010555/com_sa.trace' % self.clearLocation, '', 'com-core', '660')
        self.checkFilePermission('%s/com-apr9010443/etc/com.cfg' % self.configLocation, 'root', 'com-core', '660')
        self.checkFilePermission('%s/com-apr9010443/etc/com.cfg.bak' % self.configLocation, 'root', 'com-core', '660')
        self.checkFilePermission('%s/com-apr9010443/etc/model/model_file_list.cfg' % self.configLocation, 'root', 'com-core', '660')
        self.checkFilePermission('%s/com-apr9010443/etc/model/model_file_list.cfg.bak' % self.configLocation, 'root', 'com-core', '660')

        # check COM model files

        #self.checkFilePermission('%s/comsa_for_coremw-apr9010555/repository/CmwPm_mp.xml' % self.configLocation, 'root', 'com-core', '660')
        #self.checkFilePermission('%s/comsa_for_coremw-apr9010555/repository/CmwSwIM_mp.xml' % self.configLocation, 'root', 'com-core', '660')
        #self.checkFilePermission('%s/comsa_for_coremw-apr9010555/repository/CmwSwM_mp.xml' % self.configLocation, 'root', 'com-core', '660')

        # Check comsa_run_as_non_root
        self.setTestStep('Check if file .comsa_run_as_non_root exists')
        cmd = 'ls  %s/comsa_for_coremw-apr9010555/.comsa_run_as_non_root' % self.configLocation
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File %s/comsa_for_coremw-apr9010555/.comsa_run_as_non_root don\'t exist' % self.configLocation)

        # check if COM run under com-core user.
        self.setTestStep('Check if COM is running under com-core user')
        cmd = 'cat %s' % self.comPidFile
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        comPid = result[1]

        cmd = 'ps aux |grep \'/storage/system/config/com-apr9010443/etc/com.cfg\' |grep  %s| awk \'{print $1}\'' % comPid
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != 'com-core'):
            self.fail('ERROR', 'Com should be run under com-core user!')

        # check UMASK for com-core user
        self.setTestStep('Check umask for com-core user')
        cmd = 'su -c \'umask\' -l com-core -s /bin/bash 2>/dev/null'
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != '0027'):
            self.fail('ERROR', 'Umask of com-core should be 0027 instant of %s' % result[1])

    def checkSugarNoneSupported(self):
        self.setTestStep('Check permission of files and folders in a none supported SUGAR')

        # Check comsa_run_as_non_root
        #self.setTestStep('Check if file .comsa_run_as_non_root exists')
        #cmd = 'ls  %s/comsa_for_coremw-apr9010555/.comsa_run_as_non_root' % self.configLocation
        #result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        #self.fail(result[0], result[1])
        #if 'No such file or directory' not in result[1]:
         #   self.fail('ERROR', 'File %s/comsa_for_coremw-apr9010555/.comsa_run_as_non_root exist' % self.configLocation)

        # check if COM run under root user.
        self.setTestStep('Check if COM is running under root user')
        cmd = 'cat %s' % self.comPidFile
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        comPid = result[1]
        cmd = 'ps aux |grep \'/storage/system/config/com-apr9010443/etc/com.cfg\' |grep  %s| awk \'{print $1}\'' % comPid
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != 'root'):
            self.fail('ERROR', 'Com should be run under root user!')

    def checkFolderPermission(self, foldername, owner, group, permission):
        self.myLogger.debug('Check permission of folders %s' % (foldername))
        cmd = " stat -c '%%a' %s" % (foldername)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != permission):
            self.fail('ERROR', 'Wrong permission found! Folder: %s, Expected: %s, Found: %s' % (foldername, permission, result[1]))
        cmd = "ll -d %s | awk '{print $3}'" % (foldername)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != owner):
            self.fail('ERROR', 'Wrong owner found! Folder: %s, Expected: %s, Found: %s' % (foldername, owner, result[1]))
        cmd = "ll -d %s | awk '{print $4}'" % (foldername)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != group):
            self.fail('ERROR', 'Wrong group found! Folder: %s, Expected: %s, Found: %s' % (foldername, group, result[1]))
        else:
             self.myLogger.info('Check permission for folder successful')

    def checkFilePermission(self, filename, owner, group, permission):
        self.myLogger.debug("Check permission of files %s" % filename)
        # Check permission
        cmd = "stat -c '%%a' %s" % (filename)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != permission):
            self.fail('ERROR', 'Wrong permission found! File: %s, Expected: %s, Found: %s' % (filename, permission, result[1]))
        cmd = "ll %s | awk '{print $3}'" % (filename)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != owner) and (owner != ''):
            self.fail('ERROR', 'Wrong owner found! File: %s, Expected: %s, Found: %s' % (filename, owner, result[1]))
        cmd = "ll %s | awk '{print $4}'" % (filename)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if (result[1] != group):
            self.fail('ERROR', 'Wrong group found! File: %s, Expected: %s, Found: %s' % (filename, group, result[1]))
        else:
             self.myLogger.info('Check permission for file successful')

    def replaceCopiedBackupFiles(self, tmpBackupName):

        # recopy the backup files
        command = '\cp %scomsa_%s.tar.gz %s/%s.tar.gz ' % (self.storedBackupFilesLocation, tmpBackupName, self.comsaBackupLocation, tmpBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = 'mkdir -p %s' % (self.comBackupLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %scom_%s.tar.gz %s/%s.tar.gz ' % (self.storedBackupFilesLocation, tmpBackupName, self.comBackupLocation, tmpBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' % (self.storedBackupFilesLocation, tmpBackupName, self.cmwBackupLocation, tmpBackupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' % (self.storedBackupFilesLocation, tmpBackupName, self.lotcBackupLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

    def upgradeCOMSA(self):
        dict = self.comsa_lib.getGlobalConfig(self)
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.bfu_bundle_name = dict.get('CXP_SDP_NAME_RHEL_OFFICIAL')
        else:
            self.bfu_bundle_name = dict.get('CXP_SDP_NAME_OFFICIAL')
        self.setTestStep('Build the current COMSA with comsabuild all')

        # Verify if the package is already built and avaialable under swDirNumber directory
        bundleFound = False
        deplPackageFound = False
        self.swDir = System.getProperty("swDirNumber")
        if self.swDir != 'undef':
            self.localPathToSw = '%s%s/comsa/' % (self.installRoot, self.swDir)
            result = self.miscLib.execCommand('ls -l %s' % self.localPathToSw)
            self.fail(result[0], result[1])
            if '%s' % (self.bundleArchive) in result[1]:
                bundleFound = True
            if '%s' % (self.deplTemplArchive) in result[1]:
                deplPackageFound = True

        if bundleFound == True and deplPackageFound == True:
            self.myLogger.info('Skip building COM SA, package is available.')
            srcDir = '%s%s/comsa/' % (self.installRoot, self.swDir)
        else:
            srcDir = self.cxpArchive
            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0], result[1])

            self.myLogger.debug('Building the current COMSA with comsabuild all')
            result = self.miscLib.execCommand('%s/comsabuild clean; %s/comsabuild all' % (self.absDir, self.absDir))
            #self.fail(result[0], result[1]) # this fails for some reason!!!

            result = self.miscLib.execCommand('ls -l %s' % srcDir)
            self.fail(result[0], result[1])
            if not '%s' % (self.bundleArchive) in result[1]:
                self.fail('ERROR', 'The ComSa bundle archive was not found in the expected directory. Exiting!\n%s' % result[1])
            if not '%s' % (self.deplTemplArchive) in result[1]:
                self.fail('ERROR', 'The ComSa deployment archive was not found in the expected directory. Exiting!\n%s' % result[1])

            self.setTestStep('Copy the COMSA installation files to the target')

        # create directory on the target to copy the BFU archive files
        cmd = 'mkdir -p %s' % (self.temp_bfu)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        cmd = 'mkdir -p %s' % (self.temp_dir)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # copy the BFU archives to the target.
        self.myLogger.debug('Copying the BFU archive files to the target')

        file = '%s%s' % (srcDir, self.bundleArchive)
        result = self.sshLib.remoteCopy(file, self.temp_bfu, timeout=60)
        self.fail(result[0], result[1])
        file = '%s%s' % (srcDir, self.deplTemplArchive)
        result = self.sshLib.remoteCopy(file, self.temp_bfu, timeout=60)
        self.fail(result[0], result[1])

        # Release the build token
        if bundleFound == True and deplPackageFound == True:
            self.myLogger.debug('Skip removing the build Tokens available.')
        else:
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            self.fail(result[0], result[1])

        self.setTestStep('Unpack the COMSA installation archives on the target')
        self.myLogger.debug('Unpacking the BFU archives on the target')
        cmd = 'cd %s ; tar xf %s' % (self.temp_bfu, self.bundleArchive)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        cmd = 'cd %s ; tar xf %s' % (self.temp_bfu, self.deplTemplArchive)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.setTestStep('Import the COMSA BFU campaign and bundle SDPs to CoreMW repository')
        self.myLogger.debug('Importing the COMSA BFU campaign and bundle SDPs to CoreMW repository')

        bfuBundleSdp = '%s%s' % (self.temp_bfu, self.bfu_bundle_name)

        # copy to /home/coremw/incoming because importSwBundle() uses this dir !
        cmd = '\cp -f %s %s' % (bfuBundleSdp, self.temp_dir)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # determine the BFU campaign SDP name with full path
        cmd = 'find %s  -type f | grep sdp | grep UBFU' % (self.temp_bfu)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        upgradeCampaignSdp = result[1]

        # copy to /home/coremw/incoming because importSwBundle() uses this dir !
        cmd = '\cp %s %s' % (upgradeCampaignSdp, self.temp_dir)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # obtain only the filename of the campaign SDP
        cmd = 'ls -lR %s | grep \'C+P\' | awk \'{print $9}\'' % (self.temp_bfu)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        upgradeCampaignSdp = result[1]
        # Run the upgrade campaign

        self.setTestStep('Run the COMSA upgrade campaign')
        self.myLogger.debug('Run the COMSA upgrade campaign')

        result = self.comsa_lib.installComp(self.temp_dir, self.bfu_bundle_name, upgradeCampaignSdp, 'comsa', createBackup=False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])

        cmd = 'rm -rf %s %s' % (self.temp_dir, self.temp_bfu)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.logger.info('upgradeComSa: exit')

    def tearDown(self):
        self.setTestStep('tearDown')
        if self.skip_test == False:
            self.myLogger.info('Teardown')

            if self.testcase_tag == 'TC-SUGAR-004' or self.testcase_tag == 'TC-SUGAR-005' or self.testcase_tag == 'TC-SUGAR-006' or self.testcase_tag == 'TC-SUGAR-007':
                # 6.Restore
                self.replaceCopiedBackupFiles(self.backupName)
                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup=False)
                self.fail(result[0], result[1])
                command = '\\cmw-partial-backup-remove %s' % self.backupName
                result = self.sshLib.sendCommand(command)
                self.fail(result[0], result[1])
                #self.checkSugarSupported()
            if self.testcase_tag == 'TC-SUGAR-002':
                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup=False)
                self.fail(result[0], result[1])
            command = '\\rm -rf /home/tempSugarMR/'
            result = self.sshLib.sendCommand(command)
            self.fail(result[0], result[1])
            command = '\\rm -rf %s' % self.storedBackupFilesLocation
            result = self.sshLib.sendCommand(command)
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
