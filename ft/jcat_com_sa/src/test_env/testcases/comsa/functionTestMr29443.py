import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib

from java.lang import System

class FTMr29443(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )
        self.test_config = testConfig
        self.testcase_tag = tag
        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        dict = self.comsa_lib.getGlobalConfig(self)
        self.buildLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("SRC"))
        self.absDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        self.pathOfReleases = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.testDir =  '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST"))
        self.resourceFilesLocation = dict.get("PATH_TO_MR28452")
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')
        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]

        self.Com33Latest = "%s/com3.3_latest"%self.resourceFilesLocation
        self.CoreMWLatest = "%s/cmw3.4_latest"%self.resourceFilesLocation
        self.CoreMWSdp = 'coremw_x86_64-3.4_CP11-runtime_CXP9020355_1_R8M.tar'

        self.MR29443 = '/home/MR29443/'
        self.pathToCmwInstallation = '%s/coremw/' %self.MR29443
        self.pathToComInstallation = '%s/com/' %self.MR29443
        self.pathToComsaInstallation = '%s/comsa/' %self.MR29443
        self.pathtoIMMFilesAtTarget = '%s/model/' %self.MR29443
        self.ComSABuild = "%s/comsa"%self.resourceFilesLocation

        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'

        # parameters from the config files
        self.backupName = {}
        self.comBackupName = {}
        self.comsaBackupLocation = {}
        self.storedBackupFilesLocation = {}
        self.loctBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}

        self.pathToConfigFiles = {}
        self.useExternalModels = {}
        self.momFile = {}
        self.immClassesFile = {}
        self.immObjectsFile = {}
        self.immObjPattern = '[]'
        self.serviceInstanceName = 'ComSa'
        self.amfNodePattern = 'Cmw'
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.ntfsendMsg = ""
        self.ntfsendMsg2 = ""
        self.expectedDN = ""
        self.expectedMajorType = ""
        self.expectedMinorType = ""
        self.expectedAlarmMsg = ""
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
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        self.reqComSaRelease = "3"
        self.reqComSaVersion = "R1A01"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        self.numberOfGetTokenRetries = 5
        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT763_MODELFILE_PATH"))

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)
        self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.logger.info('Exit setUp')


    def runTest(self):
        self.logger.info('runTest')

        self.skip_test = False
        self.setTestStep('Check the required versions of ComSA is installed')

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

        if ComSaOK[1]:
            waitTime = 300
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

                command = '\mv %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.backupName, self.storedBackupFilesLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                # Copy com backup files to stored location
                self.comBackupName = self.findComBackup(self.comBackupName)
                if self.comBackupName != {}:

                    command = '\mv %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\mv %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.comBackupName, self.storedBackupFilesLocation)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                # 3.Uninstall system

                self.setTestStep('======== Uninstall system ========')

                result = self.sshLib.sendCommand('mkdir %s' %self.MR29443)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                self.fail(result[0], result[1])

                # copy unistall script to cluster

                result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName1), self.MR29443, timeout = 120)
                self.fail(result[0], result[1])

                result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName2), self.MR29443, timeout = 120)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.MR29443)
                self.fail(result[0], result[1])

            # run Uninstall

            result = self.comsa_lib.unInstallSystem(self.MR29443, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
            self.fail(result[0], result[1])

            self.lib.resetDumps()

            if not self.restoreSnapshot:
                cmw_uninstall_command2 = '%s%s' %(self.MR29443, self.uninstallScriptName2)
                result = self.sshLib.sendCommand (cmw_uninstall_command2)
                self.fail(result[0], result[1])


            # 4.Install

            # Install CoreMW
            self.setTestStep('======== Install CoreMW ========')
            if self.restoreSnapshot:
                result = self.sshLib.sendCommand('mkdir %s' %self.MR29443)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                self.fail(result[0], result[1])

            cmd = 'ls %s/%s' %(self.CoreMWLatest, self.CoreMWSdp)
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0], result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', 'COM runtime sdp file not found at specified location: %s/ .' %setupFilesDir)
            if len(result[1].splitlines()) > 1:
                self.fail('ERROR', 'More than one COM runtime sdp file found at specified location: %s/: %s.' %(setupFilesDir, str(result[1])))
            name_list = result[1].strip()

            result = self.sshLib.remoteCopy(name_list, self.pathToCmwInstallation, timeout = 120)
            self.fail(result[0],result[1])

            self.CoreMWSdp = name_list.split('/')[len(name_list.split('/')) - 1]

            result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp, backupRpms = self.backupRpmScript)
            self.fail(result[0], result[1])

            # Install COM
            self.setTestStep('======== Install COM ========')

            self.installCOM(self.Com33Latest, self.pathToComInstallation)
            self.fail(result[0], result[1])

            # Install COMSA
            self.setTestStep('======== Install COM SA ========')

            self.installCOMSA(self.ComSABuild, self.pathToComsaInstallation)
            self.fail(result[0], result[1])

            # start to send alarm
            result = self.sshLib.remoteCopy('%s/ntfsend/ntfsend' %self.testDir, self.MR29443, timeout = 120)
            self.fail(result[0],result[1])

            result = self.sshLib.sendCommand('chmod +x %s/ntfsend' %self.MR29443)
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

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
                #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            if self.useExternalModels == 'yes':
                self.comRestartTimeout = 10

                result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                self.activeController = result[1]

                self.setTestStep('Upload model files to the target')
                cmd = 'mkdir -p %s' %self.modelFilePathOnTarget
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                #Copying model files to target for case_1
                self.myLogger.debug('Copy model files to target')
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immObjectsFile), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

                self.setTestStep('### Loading model files to IMM - (Load classes and create objects in IMM)')

                #Loading model files
                self.myLogger.debug('Loading model files')
                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immObjectsFile)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

                self.myLogger.debug('Loading mp (MOM) files')
                cmd = '/opt/com/bin/com_mim_tool --addModelFile=%s%s'%(self.modelFilePathOnTarget,self.momFile)
                self.fail(result[0], result[1])
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                cmd = '/opt/com/bin/com_mim_tool --commit'
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0], result[1])

                # Restart COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                self.fail(result[0],result[1])

            self.startUnixTime = 0
            linuxTimeText = "Linux Time:"
            self.setTestStep("Getting Linux System Time")
            dateCommand = "date +%s"
            result = self.sshLib.sendCommand(dateCommand)
            self.fail(result[0],result[1])
            startTime = int(result[1])
            self.myLogger.info("Linux System Time is : %s" %(startTime))
            self.setTestStep("Sending the Alarm to the target")
            result = self.sshLib.sendCommand('%s/%s %s%s"' %(self.MR29443, self.ntfsendMsg, linuxTimeText, startTime))
            self.fail(result[0], result[1])
            self.setTestStep('Search for the new alarm in the alarm log')

            if self.installStressTool:
                allowedIterations = 25
                waitBetweenIterations = 60
            else:
                allowedIterations = 15
                waitBetweenIterations = 10

            expected_List = self.createExpectedList('%s%s' %(linuxTimeText, str(startTime)))
            subrack = 0
            slot = 0

            for iteration in range(allowedIterations):
                result = self.comsa_lib.getEventTimestampFromAlarmAlertLog(subrack, slot, expected_List, startTime, self.testConfig)
                if result[0] == 'SUCCESS':
                    break
                else:
                    self.miscLib.waitTime(waitBetweenIterations)
            self.fail(result[0], result[1])

            self.setTestStep('### Check which SC runs the CLI')
            #Creates the login params according to which controller runs the CLI

            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0],result[1])
            self.activeController = result[1]

            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

            self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])
            ###############################################################################
            ############################### CLI testing ###################################
            ###############################################################################

            #self.lib.messageBox('do some manual testing')
            #self.lib.messageBox('do some manual testing')

            self.setTestStep('### CLI testing')
            #Create the input, the expected output and the non-expected output lists
            lists = self.comsa_lib.load_TC_cli_config(self)

            #Send the cli commands and process the results element-by-element
            #One element of the list is one cli session.
            for list_index in range (0,len(lists[0])):
                self.setTestStep('### Running CLI test step %d' %list_index)
                result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
                self.fail(result[0], result[1])

            if not self.restoreSnapshot:
                if self.installStressTool:
                    self.setTestStep('======== Stopping the stress tool on target ========')
                    self.comsa_lib.stopStressToolOnTarget(self)

                # 6.Restore
                self.setTestStep('======== Restore system ========')
                #recopy the backup files
                command = '\mv %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comsaBackupLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comBackupLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.cmwBackupLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupName, self.loctBackupLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                self.fail(result[0],result[1])

                self.myLogger.info("exit runTest")
                coreTestCase.CoreTestCase.runTest(self)

                #replace the com backup files
                if self.comBackupName != {}:

                    command = '\mv  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.comBackupName, self.comBackupLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\mv %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.comBackupName, self.cmwBackupLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.comBackupName, self.loctBackupLocation)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

        else:
            self.logger.info('Skipped trace tests because of COMSA version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True

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
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comInstSdpName, 'com', False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')

    def installCOMSA(self, setupFilesDir, pathToComsaInstallation):
        self.logger.info('installCOMSA: Called')
        self.logger.info('installCOMSA: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCOMSA: pathToComsaInstallation = %s' %pathToComsaInstallation)

        # Install time
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Copy CXP SDP file and Install SDP file to Installation directory
        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
        result = self.comsa_lib.copyFilesToTarget([BuildPath[6], BuildPath[7]], pathToComsaInstallation, True)
        self.fail(result[0],result[1])

        result = self.comsa_lib.installComp(pathToComsaInstallation, BuildPath[1], BuildPath[2], 'comsa', False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])

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
                self.logger.info('findComBackup: Exit')
                self.fail('ERROR', 'findComBackup: COM backup not found!')
            self.logger.info('findComBackup: Exit')
            return backupName


    def tearDown(self):
        self.setTestStep('tearDown')

        if self.skip_test == False:

            if self.installStressTool:
                self.setTestStep('======== Stopping the stress tool on target ========')
                self.comsa_lib.stopStressToolOnTarget(self)

            self.setTestStep("Clear Alarm from the target")
            result = self.sshLib.sendCommand('%s/%s"' %(self.MR29443, self.ntfsendMsg2))
            self.fail(result[0], result[1])

            if self.useExternalModels == 'yes':

                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                self.fail(result[0],result[1])

                # Restart COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                self.fail(result[0],result[1])

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
                        cmd = 'immfind | grep -i %s | xargs immcfg -d' %immObjPattern
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0],result[1])
                        if result[1] != '':
                            self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))

                # Below we remove all the classes imported from the imm_classes model file
                cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))

                cmd = "\\rm -rf %s" %self.modelFilePathOnTarget
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

            command = '\\rm -rf /home/MR29443/'
            self.sshLib.sendCommand(command)

            command = '\\rm -rf %s' %self.storedBackupFilesLocation
            self.sshLib.sendCommand(command)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

        #########################
        #### SUPPORT METHODS ####
        #########################

    def createExpectedList(self, unixTimeString):
        self.myLogger.debug('createExpectedList() enter')
        expectedList = []

        if self.expectedDN != "":
            expectedList.append(self.expectedDN)
        if self.expectedMajorType != "":
            expectedList.append(self.expectedMajorType)
        if self.expectedMinorType != "":
            expectedList.append(self.expectedMinorType)
        if self.expectedAlarmMsg != "":
            expectedList.append(self.expectedAlarmMsg)

        expectedList.append(unixTimeString)

        if len(expectedList) != 5:
            self.fail('ERROR','failed to create expectedList, some parameter is missing')

        for i in range (0, len(expectedList)):
            self.myLogger.info('ExpectedList[%s]: (%s)' %(str(i), expectedList[i]))

        self.myLogger.debug('createExpectedList() leave')
        return expectedList

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
