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

    TC-MR29333-001 : Import models with no EcimRootMoClass and multiple EcimContribution children, using the latest COM that supports MAF MR SPI v3
    TC-MR29333-002 : Import models with EcimRootMoClass using the latest COM that supports MAF MR SPI v3
    TC-MR29333-003 : Import models with no EcimRootMoClass and multiple EcimContribution children, using COM 3.1 CP1 that does not support MAF MR SPI v3
    TC-MR29333-004 : Perform CLI change configurations using COM 3.1 CP1 that does not support MAF MR SPI v3.
    TC-MR29333-006 : Test using invalid No Root Classes model and observe the expected errors logged
    TC-MR29333-007 : Test using invalid No Root Classes model and observe the expected errors logged

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
    TC-MR29333-001

    Id:
    "Create, modify and delete objects in models with multiple EcimContributions in CLI and check the objects in IMM"
    ==================================

"""
import test_env.fw.coreTestCase as coreTestCase
import os
from java.lang import System


class functiontestMR29333(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        self.testcase_tag = tag

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)

        self.resourceFilesLocation = dict.get("PATH_TO_MR29333")
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')

        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.pathToPmtSaFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("PATH_TO_PMTSA_FILES"))
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.comNoBackup = dict.get("COM_NO_BACKUP")

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]

        self.CoreMW34CP11 = "%s/coremw3.4cp11"%self.resourceFilesLocation
        self.COM31CP1 = "%s/com3.1cp1"%self.resourceFilesLocation
        self.ComSABuild = "%s/comsa"%self.resourceFilesLocation

        self.MR29333 = '/home/MR29333/'
        self.pathToCmwInstallation = '%s/coremw/' %self.MR29333
        self.pathToComInstallation = '%s/com/' %self.MR29333
        self.pathToComsaInstallation = '%s/comsa/' %self.MR29333
        self.pathtoIMMFilesAtTarget = '%s/model/' %self.MR29333

        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
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

        self.useExternalModels = {}
        self.pathToModelFiles = {}
        self.momFile = {}
        self.momFile2 = {}
        self.momFile3 = {}
        self.immClassesFile = {}
        self.immClassesFile2 = {}
        self.immClassesFile3 = {}
        self.immClassesFile4 = {}
        self.immClassesFile5 = {}
        self.immClassesFile6 = {}
        self.immClassesFile7 = {}
        self.immObjectsFile = {}
        self.immObjectsFile2 = {}
        self.modelFileType = ''
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.immObjPattern = '[]'
        self.immObjPattern2 = '[]'
        self.immObjPattern3 = '[]'
        self.immObjPattern4 = '[]'

        self.reqComVersion = "R8A06"
        self.reqComRelease = "2"
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        self.reqComSaVersion = "R5A07"
        self.reqComSaMajorVersion = "3"
        self.reqComSaRelease = "3"

	# Two test cases MR29333 003 and 004 will not need after 3_R6A01
        # The version values have been initialised high, so all test cases are valid unless the test specifies an obsolete version in the xml file.
        #self.obsoleteComSaVersion = "R9A99"
        #self.obsoleteComSaRelease = "9"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        self.numberOfGetTokenRetries = 5
        coreTestCase.CoreTestCase.setUp(self)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MR29333_MODELFILE_PATH"))
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
        self.restoreSnapshot = False

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.runUninstallationScript = False
        if self.testcase_tag == 'TC-MR29333-003' or self.testcase_tag == 'TC-MR29333-004':
            self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.logger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        waitTime = 300

        ComsaOK = ['SUCCESS', True]
        self.skip_test = False

        if self.restoreSnapshot:
            offlineVersionComSa = ['','','']
            result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'comsa')
            if result[0] == "REGTEST":
                offlineVersionComSa[0] = result[1] #COMSA_release
                offlineVersionComSa[1] = result[2] #COMSA_release
                offlineVersionComSa[2] = result[3] #COMSA_majorVersion
                ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion, offlineVersion = offlineVersionComSa)
            else:
                # The test case is run without the setup test case (probably as stand-alone) and
                # it is presumed that the tester knows the configuration is valid
                ComsaOK[1] = True
        else:
            ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
            self.fail(ComsaOK[0],ComsaOK[1])

	#ComsaObsolete = self.lib.checkObsoleteComponentVersion('comsa', self.obsoleteComSaRelease, self.obsoleteComSaVersion)
	#self.fail(ComsaObsolete[0], ComsaObsolete[1])
	#if ComsaObsolete[1] == False:
	#	self.logger.info('Test is only applied for Comsa verison lower than ( %s, %s )' %(self.obsoleteComSaRelease, self.obsoleteComSaVersion))

        if ComsaOK[1] == True :

            ############################################################################################
            if self.testcase_tag == 'TC-MR29333-003' or self.testcase_tag == 'TC-MR29333-004':
                # 1.Create Backup and Copy backup files to stored location
                if not self.restoreSnapshot:
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

                    result = self.sshLib.sendCommand('rm -rf %s' %self.MR29333)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.MR29333)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                    self.fail(result[0], result[1])

                    # copy uninstall script to cluster

                    result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName1), self.MR29333, timeout = 120)
                    self.fail(result[0], result[1])

                    result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName2), self.MR29333, timeout = 120)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.MR29333)
                    self.fail(result[0], result[1])

                # run Uninstall

                result = self.comsa_lib.unInstallSystem(self.MR29333, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
                self.fail(result[0], result[1])

                if not self.restoreSnapshot:
                    cmw_uninstall_command2 = '%s%s' %(self.MR29333, self.uninstallScriptName2)
                    result = self.sshLib.sendCommand (cmw_uninstall_command2)
                    self.fail(result[0], result[1])

                self.lib.resetDumps()

                # 4.Install

                # Install CoreMW
                self.setTestStep('======== Install CoreMW ========')
                if self.restoreSnapshot:
                    result = self.sshLib.sendCommand('mkdir %s' %self.MR29333)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                    self.fail(result[0], result[1])

                    result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                    self.fail(result[0], result[1])

                cmd = 'ls %s/%s' %(self.CoreMW34CP11, self.CoreMWSdp)
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

                self.installCOM(self.COM31CP1, self.pathToComInstallation)
                self.fail(result[0], result[1])

                # Install COMSA
                self.setTestStep('======== Install COM SA ========')

                self.installCOMSA(self.ComSABuild, self.pathToComsaInstallation)
                self.fail(result[0], result[1])

                # Set 1000 restarts before failover
                self.setTestStep('======== setComSaSuRestartMax to 1000 restarts before failover ========')
                result = self.comsa_lib.setComSaSuRestartMax(False, 1000)
                self.fail(result[0], result[1])

            ############################################################################################

            # Check again for active controller .
            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            self.activeController = result[1]

            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                        self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

            self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

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

            self.setTestStep('Upload model files to the target')
            cmd = 'mkdir -p %s' %self.modelFilePathOnTarget
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

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

            if self.momFile3 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile3), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])
            if self.immClassesFile3 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile3), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

            if self.immClassesFile4 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile4), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

            if self.immClassesFile5 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile5), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

            if self.immClassesFile6 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile6), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

            if self.immClassesFile7 != {}:
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile7), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])

            # Add model file to COM
            if self.momFile != {}:
                commit = (self.momFile2 == {})
                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile), 'MW_OAM', commit)
                self.fail(result[0],result[1])
            if self.momFile2 != {}:
                commit = (self.momFile3 == {})
                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2), 'MW_OAM', commit)
                self.fail(result[0],result[1])
            if self.momFile3 != {}:
                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile3), 'MW_OAM', True)
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
            if self.immClassesFile3 != {}:
                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile3)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            if self.immClassesFile4 != {}:
                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile4)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            if self.immClassesFile5 != {}:
                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile5)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            if self.immClassesFile6 != {}:
                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile6)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
            if self.immClassesFile7 != {}:
                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile7)
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

            ########################################################################################
            # Workaround for TR HS33871 - COM 3.1 can have core dumps when restarting.
            if self.testcase_tag == 'TC-MR29333-003' or self.testcase_tag == 'TC-MR29333-004':
                self.lib.resetDumps()

            #########################################################################################

            # Check object in IMM
            self.setTestStep('###Check objects in IMM###')

            # Send the IMM commands and process the results element-by-element
            #One element of the list is one imm session.
            for list_index1 in range(0,len(lists1[0])):
                result = self.comsa_lib.runImmSession(lists1, list_index1)
                self.fail(result[0], result[1])

        else:
            self.logger.info('Skipped tests because of COMSA version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True

            self.myLogger.info("exit runTest")

            coreTestCase.CoreTestCase.runTest(self)


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

        #Use function from library comsa_lib
        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)

        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])
        # Copy CXP SDP file to Installation directory
        if BuildPath[6] != '':
            result = self.sshLib.remoteCopy(BuildPath[6], self.pathToComsaInstallation, timeout = 120)
            self.fail(result[0],result[1])
        else:
            self.logger.info('installCOMSAFromStream: The absolute filename of cxp sdp file is empty')

        # Copy Install SDP file to Installation directory
        if BuildPath[7] != '':
            result = self.sshLib.remoteCopy(BuildPath[7], self.pathToComsaInstallation, timeout = 120)
            self.fail(result[0],result[1])
        else:
            self.logger.info('installCOMSAFromStream: The absolute filename of cxp sdp file is empty')

        #BuildPath[1] : cxp Sdp file name
        #BuildPath[2] : install Sdp file name
        result = self.comsa_lib.installComp(pathToComsaInstallation, BuildPath[1], BuildPath[2], 'comsa', backupRpms = self.backupRpmScript)
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

            ############################################################################################
            if self.testcase_tag == 'TC-MR29333-003' or self.testcase_tag == 'TC-MR29333-004':
                if not self.restoreSnapshot:
                    # 6.Restore system
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
                ############################################################################################

            if self.momFile != {}:
                commit = (self.momFile2 == {})
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile), 'MW_OAM', commit)
                self.fail(result[0],result[1])
            if self.momFile2 != {}:
                commit = (self.momFile3 == {})
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2), 'MW_OAM', commit)
                self.fail(result[0],result[1])
            if self.momFile3 != {}:
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile3), 'MW_OAM', True)
                self.fail(result[0],result[1])

            # Restart COM
            self.myLogger.debug('Restart COM')
            result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
            self.fail(result[0],result[1])

            ############################################################################################
            # Workaround for TR HS33871 - COM 3.1 can have core dumps when restarting.
            if self.testcase_tag == 'TC-MR29333-003' or self.testcase_tag == 'TC-MR29333-004':
                self.lib.resetDumps()

            #########################################################################################

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
            if len(eval(self.immObjPattern2)) > 0:
                immObjPatterns2 = eval(self.immObjPattern2)
                for immObjPattern2 in immObjPatterns2:
                    self.myLogger.debug('Removing the object %s' %immObjPattern2)
                    cmd = 'immfind | grep -i %s | xargs immcfg -d' %immObjPattern2
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))
            if len(eval(self.immObjPattern3)) > 0:
                immObjPatterns3 = eval(self.immObjPattern3)
                for immObjPattern3 in immObjPatterns3:
                    self.myLogger.debug('Removing the object %s' %immObjPattern3)
                    cmd = 'immfind | grep -i %s | xargs immcfg -d' %immObjPattern3
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))
            if len(eval(self.immObjPattern4)) > 0:
                immObjPatterns4 = eval(self.immObjPattern4)
                for immObjPattern4 in immObjPatterns4:
                    self.myLogger.debug('Removing the object %s' %immObjPattern4)
                    cmd = 'immfind | grep -i %s | xargs immcfg -d' %immObjPattern4
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))


            if (self.testcase_tag != 'TC-MR29333-003'):
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
                if self.immClassesFile3 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile3)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile4 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile4)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile5 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile5)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile6 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile6)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile7 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile7)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))

            self.setTestStep('Remove model folder')
            cmd = '\\rm -rf  %s' %self.modelFilePathOnTarget
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

        else:
            coreTestCase.CoreTestCase.tearDown(self)
            self.setTestStep('leave tearDown')

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
