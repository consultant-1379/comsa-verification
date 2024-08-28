import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib
import omp.tf.ssh_lib as ssh_lib
import coremw.saf_lib as saf_lib
import omp.tf.hw_lib as hw_lib
import test_env.lib.lib as lib
from java.lang import System
from org.apache.log4j import Logger

class RPListImm(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )
        self.testcase_tag = tag
        # parameters from the config files
        self.pathToConfigFiles = {}
        self.useExternalModels = {}
        self.momFile = {}
        self.immClassesFile = {}
        self.immObjectsFile = {}
        self.immObjPattern = '[]'
        self.serviceInstanceName = 'ComSa'
        self.amfNodePattern = 'Cmw'
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.ntfsendMsg1 = ""
        self.ntfsendMsg2 = ""
        self.ntfsendMsg3 = ""
        self.ntfsendMsg4 = ""
        self.ntfsendMsg5 = ""
        self.ntfsendMsg1a = ""
        self.ntfsendMsg2a = ""
        self.ntfsendMsg3a = ""
        self.ntfsendMsg4a = ""
        self.ntfsendMsg5a = ""
        self.expectedDN1 = ""
        self.expectedDN2 = ""
        self.expectedDN3 = ""
        self.expectedDN4 = ""
        self.expectedDN5 = ""
        self.expectedMajorType = ""
        self.expectedMinorType = ""
        self.expectedAlarmMsg1 = ""
        self.expectedAlarmMsg2 = ""
        self.expectedAlarmMsg3 = ""
        self.expectedAlarmMsg4 = ""
        self.expectedAlarmMsg5 = ""
        self.expectedAddInfo = ""
        self.raisedAlarm = ""
        self.pathToProcess = '/usr/lib64/opensaf/'
        self.processName = 'osafckptnd'
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.reqCmwRelease = ""
        self.reqCmwVersion = ""
        self.reqComRelease = ""
        self.reqComVersion = ""
        self.reqComSaRelease = ""
        self.reqComSaVersion = ""
        self.backupName = "rpListBackup"
        self.backupName023 = "rpListBackup023"
        self.searchPattern = ""
        self.old_comsa = ''    # must be provided in the parameter file
        self.comBackupName = {}
        self.testHT70246 = ''
        self.fileName = ''
        self.fileStatus = ''
        self.alarmsTestScript = {}
        self.alarmsClearScript = {}
        self.totalAlarms = {}
        self.cliTimeout = {}
        self.sendAlarmsTimeout = {}

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

        self.cli_alt_input_1 = {}
        self.cli_alt_expected_output_1 = {}
        self.cli_alt_nonexpected_output_1 = {}
        self.cli_alt_input_2 = {}
        self.cli_alt_expected_output_2 = {}
        self.cli_alt_nonexpected_output_2 = {}
        self.cli_alt_input_3 = {}
        self.cli_alt_expected_output_3 = {}
        self.cli_alt_nonexpected_output_3 = {}
        self.cli_alt_input_4 = {}
        self.cli_alt_expected_output_4 = {}
        self.cli_alt_nonexpected_output_4 = {}
        self.cli_alt_input_5 = {}
        self.cli_alt_expected_output_5 = {}
        self.cli_alt_nonexpected_output_5 = {}
        self.cli_alt_input_6 = {}
        self.cli_alt_expected_output_6 = {}
        self.cli_alt_nonexpected_output_6 = {}
        self.cli_alt_input_7 = {}
        self.cli_alt_expected_output_7 = {}
        self.cli_alt_nonexpected_output_7 = {}
        self.cli_alt_input_8 = {}
        self.cli_alt_expected_output_8 = {}
        self.cli_alt_nonexpected_output_8 = {}
        self.cli_alt_input_9 = {}
        self.cli_alt_expected_output_9 = {}
        self.cli_alt_nonexpected_output_9 = {}
        self.cli_alt_input_10 = {}
        self.cli_alt_expected_output_10 = {}
        self.cli_alt_nonexpected_output_10 = {}
        self.cli_alt_input_11 = {}
        self.cli_alt_expected_output_11 = {}
        self.cli_alt_nonexpected_output_11 = {}
        self.cli_alt_input_12 = {}
        self.cli_alt_expected_output_12 = {}
        self.cli_alt_nonexpected_output_12 = {}
        self.cli_alt_input_13 = {}
        self.cli_alt_expected_output_13 = {}
        self.cli_alt_nonexpected_output_13 = {}
        self.cli_alt_input_14 = {}
        self.cli_alt_expected_output_14 = {}
        self.cli_alt_nonexpected_output_14 = {}
        self.cli_alt_input_15 = {}
        self.cli_alt_expected_output_15 = {}
        self.cli_alt_nonexpected_output_15 = {}
        self.cli_alt_input_16 = {}
        self.cli_alt_expected_output_16 = {}
        self.cli_alt_nonexpected_output_16 = {}
        self.cli_alt_input_17 = {}
        self.cli_alt_expected_output_17 = {}
        self.cli_alt_nonexpected_output_17 = {}
        self.cli_alt_input_18 = {}
        self.cli_alt_expected_output_18 = {}
        self.cli_alt_nonexpected_output_18 = {}
        self.cli_alt_input_19 = {}
        self.cli_alt_expected_output_19 = {}
        self.cli_alt_nonexpected_output_19 = {}
        self.cli_alt_input_20 = {}
        self.cli_alt_expected_output_20 = {}
        self.cli_alt_nonexpected_output_20 = {}
        self.cli_alt_input_21 = {}
        self.cli_alt_expected_output_21 = {}
        self.cli_alt_nonexpected_output_21 = {}
        self.cli_alt_input_22 = {}
        self.cli_alt_expected_output_22 = {}
        self.cli_alt_nonexpected_output_22 = {}
        self.cli_alt_input_23 = {}
        self.cli_alt_expected_output_23 = {}
        self.cli_alt_nonexpected_output_23 = {}
        self.cli_alt_input_24 = {}
        self.cli_alt_expected_output_24 = {}
        self.cli_alt_nonexpected_output_24 = {}
        self.cli_alt_input_25 = {}
        self.cli_alt_expected_output_25 = {}
        self.cli_alt_nonexpected_output_25 = {}
        self.cli_alt_input_26 = {}
        self.cli_alt_expected_output_26 = {}
        self.cli_alt_nonexpected_output_26 = {}
        self.cli_alt_input_27 = {}
        self.cli_alt_expected_output_27 = {}
        self.cli_alt_nonexpected_output_27 = {}
        self.cli_alt_input_28 = {}
        self.cli_alt_expected_output_28 = {}
        self.cli_alt_nonexpected_output_28 = {}
        self.cli_alt_input_29 = {}
        self.cli_alt_expected_output_29 = {}
        self.cli_alt_nonexpected_output_29 = {}
        self.cli_alt_input_30 = {}
        self.cli_alt_expected_output_30 = {}
        self.cli_alt_nonexpected_output_30 = {}
        self.cli_alt_input_31 = {}
        self.cli_alt_expected_output_31 = {}
        self.cli_alt_nonexpected_output_31 = {}
        self.cli_alt_input_32 = {}
        self.cli_alt_expected_output_32 = {}
        self.cli_alt_nonexpected_output_32 = {}


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
        self.pathToSrc = dict.get("JCAT_COM_SA_SRC")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT763_MODELFILE_PATH"))
        self.installStressTool = eval(System.getProperty("runStressTool"))
        self.rlistLocation = "/cluster/storage/clear/comsa_for_coremw-apr9010555/rplist/"
        self.statusSection = "FmStatusSection"
        self.alarmsListName = "FmActiveAlarmList2"

        self.path_to_bfu = dict.get("PATH_TO_BFU")
        self.resourceFilesLocation = dict.get("PATH_TO_BFU")
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.temp_dir = '/home/coremw/incoming/'
        self.temp_bfu = '/home/bfu/'
        self.nbc_dir = '/home/nbc_dir/'
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        self.cxpArchive = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.absDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.deplTemplArchive = dict.get('COM_SA_DEPL_TEMPL_ARCHIVE_RHEL')
            self.bundleArchive = dict.get('COM_SA_BUNDLE_ARCHIVE_RHEL')
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER_RHEL')
        else:
            self.deplTemplArchive = dict.get('COM_SA_DEPL_TEMPL_ARCHIVE')
            self.bundleArchive = dict.get('COM_SA_BUNDLE_ARCHIVE')
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER')
        self.numberOfGetTokenRetries = 5
        self.path_of_old_comsa = '%s%s' %(self.path_to_bfu, self.old_comsa)
        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5
        self.buildDir = dict.get('BUILD_TOKENS')

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        self.myLogger.info('Exit setUp')

    def runTest(self):
	self.setTestStep('runTest')
        ComsaOK = ('SUCCESS', True)
        ComOK = ('SUCCESS', True)
        CmwOK = ('SUCCESS', True)
        self.skip_test = False

        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
        self.fail(ComsaOK[0],ComsaOK[1])
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
        self.fail(CmwOK[0],CmwOK[1])

        if ComsaOK[1] and CmwOK[1]:
            self.skip_test = False
            if self.testcase_tag == 'TC-RPLIST-022' and len(self.testConfig['payloads']) == 0:
                self.skip_test = True
        else:
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
            # Test cases from TC-RPLIST-030 to TC-RPLIST-032 intend to test for TR HR70246
            if self.testHT70246 == 'True':
                # Create the temporary directory
                cmd = 'mkdir -p /home/HT70246'
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                # Copy the file in the FmStatusSection into created temporary directory
                cmd = 'cp %s%s/%s /home/HT70246' %(self.rlistLocation,self.statusSection,self.fileName)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                # Testing for size of file is 0 byte case
                if self.fileStatus == '0Byte':
                    cmd = 'cat /dev/null > %s%s/%s' %(self.rlistLocation,self.statusSection,self.fileName)

                # Testing for size of file is 20 bytes case
                if self.fileStatus == '20Byte':
                    cmd = 'truncate -s 20 %s%s/%s' %(self.rlistLocation,self.statusSection,self.fileName)

                # Testing for removed file case
                if self.fileStatus == 'deleted':
                    cmd = 'rm %s%s/%s' %(self.rlistLocation,self.statusSection,self.fileName)

                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                # Getting Linux Time
                dateCommandSyslog = "date +%s"
                result = self.sshLib.sendCommand(dateCommandSyslog)
                self.fail(result[0],result[1])
                startTimeSyslog = int(result[1])
                self.myLogger.info("Linux System Time for matching string in syslog is: %s" %(startTimeSyslog))

                # Restart com
                cmd = 'comsa-mim-tool com_switchover'
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.miscLib.waitTime(15)

                self.checkSystemStatus([self.searchPattern], startTimeSyslog)
            elif self.testcase_tag == 'TC-RPLIST-023':

                self.setTestStep('Create a backup of the system')
                self.myLogger.debug('Create a backup of the system: rpListBackup023')
                result = self.safLib.isBackup(self.backupName023)
                self.fail(result[0], result[1])
                if result == ('SUCCESS','EXIST'):
                    result = self.safLib.backupRemove(self.backupName023)
                    self.fail(result[0], result[1])
                result = self.comsa_lib.backupCreateWrapper(self.backupName023, backupRpms = self.backupRpmScript)
                self.fail(result[0], result[1])
                # Check CMW status, and wait for status ok
                self.setTestStep('Check CMW status after creating backup')
                result = self.comsa_lib.waitForClusterStatusOk()
                self.fail(result[0], result[1])

                self.myLogger.debug('Restore the COM backup ')
                self.setTestStep('Restore the COM backup')
                self.comBackupName = self.findComBackup(self.comBackupName)
                result = self.comsa_lib.restoreSystem(self, self.comBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 2, removeBackup = False)
                self.fail(result[0],result[1])

                # Install COMSA
                self.setTestStep('======== Install "old" COM SA ========')

                # Check COMSA deployment SDP under the given path
                noOfScs = len(self.testConfig['controllers'])
                if noOfScs == 2:
                    installSdp = self.installSdpName
                elif noOfScs == 1:
                    installSdp = self.installSdpNameSingle
                else:
                    self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' %str(noOfScs))

                cmd = 'ls %s | grep "%s"' %(self.path_of_old_comsa, installSdp)
                self.myLogger.debug('Check COMSA deployment SDP under the given path by: %s' %cmd)
                result = self.miscLib.execCommand(cmd)
                if result[1] == '':
                    self.fail('ERROR','No %s found under: %s' %(installSdp, self.path_of_old_comsa))
                comsaDeploymentTemplateSDP = result[1].strip()

                # Check COMSA runtime SDP under the given path
                cmd = 'ls %s | grep -i com | grep -i sa | grep -i cxp | grep -i sdp' %self.path_of_old_comsa
                self.myLogger.debug('Check COMSA runtime SDP under the given path by: %s' %cmd)
                result = self.miscLib.execCommand(cmd)
                if result[1] == '':
                    self.fail('ERROR','No COM_SA-CXPxxxxxxxx.sdp found under: %s' %self.path_of_old_comsa)
                comsaRuntimeSDP = result[1].strip()

                # Create COM-SA temp directory
                cmd = 'mkdir -p %s' %self.temp_dir
                self.myLogger.debug('Create COM-SA temp directory by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                # Upload the old COMSA runtime SDP and COMSA deployment template SDP to target
                self.setTestStep('Upload the old COMSA runtime SDP and COMSA deployment template SDP to target')
                self.myLogger.debug('Upload the old COMSA runtime SDP and COMSA deployment template SDP to target')

                file = '%s%s' %(self.path_of_old_comsa, comsaRuntimeSDP)
                result = self.sshLib.remoteCopy(file, self.temp_dir, timeout = 60)
                self.fail(result[0],result[1])
                file = '%s%s' %(self.path_of_old_comsa, comsaDeploymentTemplateSDP)
                result = self.sshLib.remoteCopy(file, self.temp_dir, timeout = 60)
                self.fail(result[0],result[1])

                result = self.comsa_lib.installComp(self.temp_dir, comsaRuntimeSDP, comsaDeploymentTemplateSDP, 'comsa', createBackup = False, backupRpms = self.backupRpmScript)
                self.fail(result[0], result[1])

                campaignStartTime = result[2]
                campaignName = result[3]
                result = self.comsa_lib.calculateComponentInstallationTime(campaignStartTime, campaignName, self.testConfig)
                self.fail(result[0], result[1])
                comsaInstallationTime = result[1]
                self.setAdditionalResultInfo('Old COM SA installation time: %d' %comsaInstallationTime)
                self.comsa_lib.addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'Previous COM SA installation', comsaInstallationTime)
                self.myLogger.info('charMeasurements - Previous COM SA installation: %s' %str(comsaInstallationTime))

                result = self.lib.getComponentVersion(self.comsaCxpNumber)
                self.fail(result[0], result[1])
                self.setAdditionalResultInfo('Upgraded COM SA from Release: %s, Version: %s' %(result[1], result[2]))

                self.send5alarmstothetarget()

                #
                # Check if the alarms can be seen in CLI
                #

                #Create the input, the expected output and the non-expected output lists
                lists = self.comsa_lib.load_TC_cli_config(self)
                #Send the cli commands and process the results element-by-element
                #One element of the list is one cli session.
                self.checkCliAlarmList(lists)

                ##############################################################################
                # Upgrade to the current COMSA
                ###########################################################################

                self.setTestStep('Build the current COMSA with comsabuild all')
                # Remove the tmp directory to cleanup
                cmd = 'rm -rf %s' %self.temp_dir
                self.myLogger.debug('Remove the COM-SA temp directory by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                # Create COM-SA temp directory
                cmd = 'mkdir -p %s' %self.temp_dir
                self.myLogger.debug('Create COM-SA temp directory by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                # Remove the BFU directory on the target to cleanup
                cmd = 'rm -rf %s' %(self.temp_bfu)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

                # create directory on the target to copy the BFU archive files
                cmd = 'mkdir -p %s' %(self.temp_bfu)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])
                # Build comsa first

                BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
                if BuildPath[0] != 'SUCCESS':
                    self.logger.error(result[1])
                    self.logger.debug('upgradeCOMSAFromStream: Exit')
                    return (BuildPath[0], 'Build COM SA failed')
                # copy the BFU archives to the target.
                self.myLogger.debug('Copying the BFU archive files to the target')
                # BuildPath[6] is the file name with absolute path of Runtime sdp file
                # BuildPath[9] is the file name with absolute path of Template tar file
                result = self.comsa_lib.copyFilesToTarget([BuildPath[6], BuildPath[9]], self.temp_bfu, True)
                self.fail(result[0],result[1])
                self.myLogger.debug('Unpacking the BFU archives on the target')
                # BuildPath[4] is the name of Template tar file
                cmd = 'cd %s ; tar xf %s' %(self.temp_bfu, BuildPath[4])
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

                self.myLogger.debug('Importing the COMSA BFU campaign and bundle SDPs to CoreMW repository')

                # copy to /home/coremw/incoming because importSwBundle() uses this dir !
                # BuildPath[1] is the name of Runtime sdp file
                cmd = '\cp -f %s/%s %s' %(self.temp_bfu, BuildPath[1], self.temp_dir)
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

                self.setTestStep('Run the COMSA upgrade campaign')
                self.myLogger.debug('Run the COMSA upgrade campaign')

                result = self.comsa_lib.installComp(self.temp_dir, BuildPath[1] , upgradeCampaignSdp, 'comsa', createBackup = False, backupRpms = self.backupRpmScript)
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

                #
                # Check if the alarms appear in the file system
                #
                self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/")
                self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='5')

                self.setTestStep("Checking for the alarms using CLI")

                #
                # Check if the alarms can be seen in CLI
                #
                #Create the input, the expected output and the non-expected output lists
                lists = self.comsa_lib.load_TC_cli_config(self)
                #Send the cli commands and process the results element-by-element
                #One element of the list is one cli session.
                self.checkCliAlarmList(lists)

            else:
                if self.testcase_tag == 'TC-RPLIST-022':
                    #enable resilience flag for CMW
                    self.setTestStep("Checking status of the resilience on cluster,make sure the  SC_ABSENCE_ALLOWED flag is enable before testing")
                    cmd = 'cmw-configuration --status SC_ABSENCE_ALLOWED'
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0], result[1])
                    if result[1] == 'Disable':
                        self.myLogger.info('Enable the SC_ABSENCE_ALLOWED flag')
                        cmd = 'cmw-configuration --enable SC_ABSENCE_ALLOWED --reboot'
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0], result[1])

                        #waitting for cluster already
                        self.miscLib.waitTime(150)
                        result = self.comsa_lib.waitForClusterStatusOk()
                        self.fail(result[0], result[1])

                # measure the CLI delay for ~500 alarms at ~35 alarms per second
                if self.testcase_tag == 'TC-RPLIST-026' or self.testcase_tag == 'TC-RPLIST-027':
                    self.setTestStep("Registering %s alarms on the target" %self.totalAlarms)
                    # create a directory on the target to copy the tests scripts
                    cmd = 'mkdir -p %s' %(self.nbc_dir)
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0], result[1])

                    # copy the test scripts to the target.
                    self.myLogger.debug('Copying the alarms test script to the target')
                    file = '%s%s%s%s' %(self.COMSA_VERIF_PATH, self.pathToSrc, self.pathToConfigFiles, self.alarmsTestScript)
                    result = self.sshLib.remoteCopy(file, self.nbc_dir, timeout = 60)
                    self.fail(result[0],result[1])
                    file = '%s%s%s%s' %(self.COMSA_VERIF_PATH, self.pathToSrc, self.pathToConfigFiles, self.alarmsClearScript)
                    result = self.sshLib.remoteCopy(file, self.nbc_dir, timeout = 60)
                    self.fail(result[0],result[1])
                    cmd = 'chmod a+x %s*' %(self.nbc_dir)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0], result[1])

                    #
                    # Raise many (e.g. 500) alarms to the target at rate ~35 alarms per second using a script
                    #
                    isVboxCluster = self.comsa_lib.getVboxKvmClusterConfig(self)
                    if isVboxCluster == True:
                        isVbox = 1
                    else:
                        isVbox = 0

                    cmd = '%s%s %s %s' %(self.nbc_dir, self.alarmsTestScript, self.totalAlarms, isVbox)
                    raiseAlarmsStartTime = int(time.time())
                    activeScIpAddr = self.comsa_lib.get_active_controller_ip(self.activeController, self.targetData)
                    result = self.sshLib.sendRawCommand(activeScIpAddr, cmd, "root", "rootroot", int(self.sendAlarmsTimeout))
                    raiseAlarmsEndTime = int(time.time())
                    self.fail(result[0], result[1])
                    self.myLogger.info('Linux time when the last alarm was raised: %s' % result[1])
                    raiseAlarmsElapsedTime = raiseAlarmsEndTime - raiseAlarmsStartTime
                    alarmRate = float(self.totalAlarms) / int(raiseAlarmsElapsedTime)
                    alRate = "%.2f" %alarmRate
                    self.myLogger.info('It took %s seconds to raise %s alarms. Alarm rate: %s alarms per second.' %(raiseAlarmsElapsedTime, self.totalAlarms, alarmRate))
                    self.setAdditionalResultInfo('The actual alarm rate was %s alarms per second.' %(alRate))

                    #
                    # Keep checking the total number of active alarms in CLI in a loop until 500 are shown
                    # Measure the delay since the last alarm of the 500 alarms was raised
                    #
                    self.setTestStep("Checking when the total alarms will be displayed correctly in CLI")
                    timeNow = int(time.time())
                    startTime = timeNow
                    endTime = timeNow + int(self.cliTimeout)
                    timeoutFlag = True
                    cliExpectedString = 'totalActive=%s' %self.totalAlarms

                    while timeNow < endTime:
                        cmd = '%s "show ManagedElement=1,SystemFunctions=1,Fm=1,totalActive" "exit"' %self.cli_active_controller_login_params
                        result = self.comsa_lib.executeCliSession(cmd)
                        self.fail(result[0], result[1])
                        if cliExpectedString in result[1]:
                            timeNow = int(time.time())
                            timeoutFlag = False
                            break
                        timeNow = int(time.time())

                    if timeoutFlag == True:
                        self.setAdditionalResultInfo('Timeout of %s seconds expired while checking totalActive in CLI' %self.cliTimeout)
                        self.myLogger.info('Timeout of %s seconds expired while checking totalActive in CLI' %self.cliTimeout)
                        self.fail('ERROR', 'Timeout of %s seconds expired while checking totalActive in CLI' %self.cliTimeout)
                    else:
                        elapsedTime = timeNow - startTime
                        self.setAdditionalResultInfo('It took %s seconds for the %s alarms to be updated in CLI' %(elapsedTime, cliExpectedString))
                        self.myLogger.info('It took %s seconds for the %s alarms to be updated in CLI' %(elapsedTime, cliExpectedString))
                else:
                    # At this point there should be no alarms in the system. If there are any this could be some leftover
                    # from previous tests. In this case the alarms must be cleared (removed).
                    # FIXME: One way to clear the alarms is to reboot the cluster.
                    # There could be better ways to do this.
                    self.setTestStep("Checking that the system is clean - no alarms files from before in ~/rplist/FmActiveAlarmList2/")
                    cmd = 'ls -1 %s%s/ | wc -l' %(self.rlistLocation, self.alarmsListName)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0], result[1])
                    numAlarmsFound = int(result[1])
                    if numAlarmsFound != 0:
                        self.setTestStep("Restart opensafd service in order to clear any outstanding alarms...")
                        result = self.comsa_lib.stopOpensafService(self.testConfig)
                        self.fail(result[0], result[1])

                        self.logger.info('Remove outstanding alarm')
                        cmd = '//rm -f %s/%s/*' %( self.rlistLocation, self.alarmsListName)
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0], result[1])

                        result = self.comsa_lib.startOpensafService(self.testConfig)
                        self.fail(result[0], result[1])

                    if self.testcase_tag == 'TC-RPLIST-029':
                        # Remove the ~/rplist/ Folder and send alarm to check for TR HT94210
                        self.setTestStep("Removing rplist folder...")
                        cmd = 'rm -rf %s/*' % self.rlistLocation
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0], result[1])

                    # Send alarms to the target
                    self.send5alarmstothetarget()

                    #
                    # Check if the alarms appear in the file system
                    #
                    self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/")
                    self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='5')

                    self.setTestStep("Checking for the alarms using CLI")

                    #
                    # Check if the alarms can be seen in CLI
                    #
                    #Create the input, the expected output and the non-expected output lists
                    lists = self.comsa_lib.load_TC_cli_config(self)
                    #Send the cli commands and process the results element-by-element
                    #One element of the list is one cli session.
                    self.checkCliAlarmList(lists)

                    #
                    # Restart COM and check again that the alarms are in ~/rplist/FmActiveAlarmList2/ and can be seen in CLI
                    #

                    self.setTestStep("Restarting COM")
                    result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                    self.fail(result[0],result[1])

                    self.miscLib.waitTime(20)

                    self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/ after COM restart")
                    self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='5')

                    self.setTestStep("Checking for the alarms using CLI after COM restart")

                    #
                    # Check if the alarms can be seen in CLI
                    #

                    #Create the input, the expected output and the non-expected output lists
                    lists = self.comsa_lib.load_TC_cli_config(self)
                    #Send the cli commands and process the results element-by-element
                    #One element of the list is one cli session.
                    self.checkCliAlarmList(lists)

                    if self.testcase_tag == 'TC-RPLIST-021':
                        self.setTestStep("Clearing the Third Alarm to the target")
                        result = self.sshLib.sendCommand('%s"' %self.ntfsendMsg3a)
                        if self.installStressTool:
                            self.miscLib.waitTime(200)
                            self.fail(result[0], result[1])

                        # need to wait a little (3 seconds was not always enough) otherwise the files might not be there yet
                        self.miscLib.waitTime(20)

                        #
                        # Check if the alarms appear in the file system
                        #
                        self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/")
                        self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='4')

                        #
                        # Check if the alarms can be seen in CLI
                        #
                        self.setTestStep("Checking for the alarms again using CLI after an alarm was cleared")
                        #Create the input, the expected output and the non-expected output lists
                        lists = self.comsa_lib.load_TC_cli_alt_config(self)
                        #Send the cli commands and process the results element-by-element
                        #One element of the list is one cli session.
                        self.checkCliAlarmList(lists)

                        #
                        # Restart COM and check again that the alarms are in ~/rplist/FmActiveAlarmList2/ and can be seen in CLI
                        #
                        self.setTestStep("Restarting again COM")
                        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                        self.fail(result[0],result[1])

                        self.miscLib.waitTime(20)

                        self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/ after COM restart")
                        self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='4')

                        #
                        # Check if the alarms can be seen in CLI
                        #

                        self.setTestStep("Checking for the alarms using CLI after COM restart")
                        #Create the input, the expected output and the non-expected output lists
                        lists = self.comsa_lib.load_TC_cli_alt_config(self)
                        #Send the cli commands and process the results element-by-element
                        #One element of the list is one cli session.
                        self.checkCliAlarmList(lists)

                    if self.testcase_tag == 'TC-RPLIST-022':
                        self.setTestStep("Powering OFF both SCs")

                        if self.installStressTool:
                            self.miscLib.waitTime(200)
                            #self.fail(result[0], result[1])

                        ## Check the uptime of PLs
                        self.setTestStep("Checking the uptime of the PLs before powering the SCs down")
                        result = self.calculatePayloadStartup(2,3)
                        self.fail(result[0], result[1])
                        T3 = result[1] + 390
                        self.myLogger.info('PL 3 is up for %s seconds' %result[1])

                        result = self.calculatePayloadStartup(2,4)
                        self.fail(result[0], result[1])
                        T4 = result[1] + 390
                        self.myLogger.info('PL 4 is up for %s seconds' %result[1])

                        # Turn off both SC

                        result = hw_lib.powerOff(2, 1)
                        self.fail(result[0], result[1])
                        result = hw_lib.powerOff(2, 2)
                        self.fail(result[0], result[1])

                        self.miscLib.waitTime(180)

                        #####################################
                        self.setTestStep("Powering ON both SCs")

                        ## Turn on both SCs
                        result = hw_lib.powerOn(2, 1)
                        self.fail(result[0], result[1])
                        result = hw_lib.powerOn(2, 2)
                        self.fail(result[0], result[1])

                        self.miscLib.waitTime(360)
                        self.setTestStep("Checking the uptime of PLs to see if the PLs stayed up while the SCs were down")
                        self.myLogger.debug('Wait for cmw-status to return Status OK')
                        result = self.comsa_lib.waitForClusterStatusOk()
                        self.fail(result[0], result[1])

                        result = self.calculatePayloadStartup(2,3)
                        self.fail(result[0], result[1])
                        self.myLogger.info('After SC(s) came up PL 3 is already up for %s seconds' %result[1])
                        if result[1] < T3:
                            self.fail('ERROR', 'PL 3 rebooted when SCs were down')

                        result = self.calculatePayloadStartup(2,4)
                        self.fail(result[0], result[1])
                        self.myLogger.info('After SC(s) came up PL 4 is already up for %s seconds' %result[1])
                        if result[1] < T4:
                            self.fail('ERROR', 'Payload 4 rebooted when SCs were down')

                        #
                        # Check if the alarms appear in the file system
                        #
                        self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/")
                        self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='5')

                        self.miscLib.waitTime(30)
                        #
                        # Check if the alarms can be seen in CLI
                        #

                        self.setTestStep("Checking for the alarms using CLI after both SC node up")
                        #Create the input, the expected output and the non-expected output lists
                        lists = self.comsa_lib.load_TC_cli_config(self)
                        #Send the cli commands and process the results element-by-element
                        #One element of the list is one cli session.
                        self.checkCliAlarmList(lists)

                    if self.testcase_tag == 'TC-RPLIST-024':
                        # Create backup after sending 5 alarms
                        self.setTestStep('Create backup rpListBackup')
                        self.myLogger.debug('Create a backup of system after sending 5 alarms: rpListBackup')
                        result = self.safLib.isBackup(self.backupName)
                        self.fail(result[0], result[1])
                        if result == ('SUCCESS','EXIST'):
                            result = self.safLib.backupRemove(self.backupName)
                            self.fail(result[0], result[1])
                        result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
                        self.fail(result[0], result[1])
                        # Check CMW status, and wait for status ok
                        self.setTestStep('Check CMW status after creating old COMSA backup')
                        result = self.comsa_lib.waitForClusterStatusOk()
                        self.fail(result[0], result[1])

                        self.myLogger.debug('Sending 5 more alarms after %s created: rpListBackup')
                        self.send5alarmstothetarget()
                        self.miscLib.waitTime(10)

                        # Restore the system from the rpListBackup and verify that there is no alarms on the system
                        self.setTestStep('Restoring the system from the COMSA rpListBackup')
                        result = self.comsa_lib.backupRestoreWrapper(self.backupName, backupRpms = self.backupRpmScript)
                        self.fail(result[0], result[1])

                        self.sshLib.tearDownHandles()

                        result = lib.updateLinuxDistroInDictionary(self.testSuiteConfig, self.distroTypes)
                        self.fail(result[0], result[1])
                        linuxDistro = self.testSuiteConfig['linuxDistro']['value']

                        result = self.comsa_lib.calculateLatestSystemStartup(self.testConfig, linuxDistro, self.distroTypes)
                        self.fail(result[0], result[1])
                        currentStartUpTimes = result[1]

                        self.setTestStep('Reboot the cluster and wait for all tipc up and then wait for for cmw-status to return Status OK')
                        result = ssh_lib.sendCommand('cluster reboot -a')
                        self.fail(result[0], result[1])

                        self.miscLib.waitTime(150)

                        result = self.comsa_lib.waitForMoreRecentStartUpTime(currentStartUpTimes, self.testConfig, linuxDistro, self.distroTypes)
                        self.fail(result[0], result[1])

                        result = self.comsa_lib.waitForTipcUp(self.testConfig)
                        self.fail(result[0], result[1])

                        # Check CMW status, and wait for status ok
                        self.setTestStep('Wait for cmw-status to return Status OK')
                        result = self.comsa_lib.waitForClusterStatusOk()
                        self.fail(result[0], result[1])

                        #
                        # Check if the alarms appear in the file system
                        #
                        self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/")
                        self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='0')

                        #
                        # Check if the alarms can be seen in CLI
                        #
                        self.setTestStep("Checking for the alarms again after an alarm was cleared using CLI")
                        #Create the input, the expected output and the non-expected output lists

                        lists = self.comsa_lib.load_TC_cli_alt_config(self)
                        #Send the cli commands and process the results element-by-element
                        #One element of the list is one cli session.
                        self.checkCliAlarmList(lists)

                        #
                        # Restart COM and check again that the alarms are in ~/rplist/FmActiveAlarmList2/ and can be seen in CLI
                        #
                        self.setTestStep("Restarting again COM")
                        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                        self.fail(result[0],result[1])

                        self.miscLib.waitTime(10)

                        self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/ after COM restart")
                        self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='0')

                        #
                        # Check if the alarms can be seen in CLI
                        #

                        self.setTestStep("Checking for the alarms using CLI after COM restart")
                        #Create the input, the expected output and the non-expected output lists
                        lists = self.comsa_lib.load_TC_cli_alt_config(self)
                        #Send the cli commands and process the results element-by-element
                        #One element of the list is one cli session.
                        self.checkCliAlarmList(lists)

                    if self.testcase_tag == 'TC-RPLIST-025':
                        # Try to restart all nodes
                        self.setTestStep('Reboot cluster')
                        result = self.comsa_lib.restartCluster(self.testConfig, self.linuxDistro, self.distroTypes)
                        self.fail(result[0], result[1])

                        #
                        # Check if the alarms appear in the file system
                        #
                        self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/")
                        self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='0')

                        #
                        # Check if the alarms can be seen in CLI
                        #
                        self.setTestStep("Checking for the alarms again after an alarm was cleared using CLI")
                        #Create the input, the expected output and the non-expected output lists

                        lists = self.comsa_lib.load_TC_cli_alt_config(self)
                        #Send the cli commands and process the results element-by-element
                        #One element of the list is one cli session.
                        self.checkCliAlarmList(lists)

                        #
                        # Restart COM and check again that the alarms are in ~/rplist/FmActiveAlarmList2/ and can be seen in CLI
                        #
                        self.setTestStep("Restarting again COM")
                        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                        self.fail(result[0],result[1])

                        self.miscLib.waitTime(10)

                        self.setTestStep("Checking for the correct number of Replicated List item files in ~/rplist/FmActiveAlarmList2/ after COM restart")
                        self.checkAlarmList(self.rlistLocation, self.alarmsListName, numberOfAlarm='0')

                        #
                        # Check if the alarms can be seen in CLI
                        #

                        self.setTestStep("Checking for the alarms using CLI after COM restart")
                        #Create the input, the expected output and the non-expected output lists
                        lists = self.comsa_lib.load_TC_cli_alt_config(self)
                        #Send the cli commands and process the results element-by-element
                        #One element of the list is one cli session.
                        self.checkCliAlarmList(lists)

        else:
            if self.testcase_tag == 'TC-RPLIST-022' and len(self.testConfig['payloads']) == 0:
                self.myLogger.info('Skipped the test because there are no payloads!')
                self.setAdditionalResultInfo('Test skipped; no payloads')
            if ComsaOK[1] == False:
                self.myLogger.info('Skipped the test because the COM SA version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; COM SA version is not compatible')
            if CmwOK[1] == False:
                self.myLogger.info('Skipped the test because the CMW version is not compatible!')
                self.setAdditionalResultInfo('Test skipped; CMW version is not compatible')

        self.myLogger.info("exit runTest")

        coreTestCase.CoreTestCase.runTest(self)
    def checkCliAlarmList(self, lists):
        self.myLogger.info('checkCliAlarmList: Called')
        timeOut= 100
        waitTime= 10

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(
            self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)
        for i in range(int(timeOut/waitTime)):
            for list_index in range(0,len(lists[0])):
                result = self.comsa_lib.runCliSession(lists, list_index, cli_active_controller_login_params)
                if result[0]== 'SUCCESS':
                    self.myLogger.info('Leave checkCliAlarmList')
                    return result[0]
                self.miscLib.waitTime(waitTime)
        self.fail(result[0], 'TimeOut: %s' %result[1])

    def checkAlarmList(self, rlistLocation, alarmListName, numberOfAlarm):
        self.myLogger.info('checkAlarmList: Called')
        timeOut= 100
        waitTime= 10

        for i in range(int(timeOut/waitTime)):
            cmd = 'ls -1 %s%s/' %(self.rlistLocation, self.alarmsListName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            cmd = 'ls -1 %s%s/ | wc -l' %(self.rlistLocation, self.alarmsListName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            if result[1] == numberOfAlarm:
               self.myLogger.info('Leave checkAlarmList')
               return result[1]
            self.miscLib.waitTime(waitTime)
        self.fail('ERROR', 'TimeOut: Expected exactly %s RP List files. Found %s instead' % (numberOfAlarm, result[1]))

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

    def send5alarmstothetarget(self):
        linuxTimeText = "Linux Time:"

        self.setTestStep("Getting Linux System Time")
        dateCommand = "date +%s"
        result = self.sshLib.sendCommand(dateCommand)
        self.fail(result[0], result[1])
        startTime = int(result[1])
        self.myLogger.info("Linux System Time is : %s" % (startTime))

        if self.installStressTool:
            self.miscLib.waitTime(150)
        self.setTestStep("Sending the First Alarm to the target")

        result = self.sshLib.sendCommand('%s %s%s"' % (self.ntfsendMsg1, linuxTimeText, startTime))
        if self.installStressTool:
            self.miscLib.waitTime(200)
        self.fail(result[0], result[1])
        if self.installStressTool:
            self.miscLib.waitTime(150)
        self.setTestStep("Sending the Second Alarm to the target")

        result = self.sshLib.sendCommand('%s %s%s"' % (self.ntfsendMsg2, linuxTimeText, startTime))
        if self.installStressTool:
            self.miscLib.waitTime(200)
        self.fail(result[0], result[1])

        if self.installStressTool:
            self.miscLib.waitTime(150)
        self.setTestStep("Sending the Third Alarm to the target")

        result = self.sshLib.sendCommand('%s %s%s"' % (self.ntfsendMsg3, linuxTimeText, startTime))
        if self.installStressTool:
            self.miscLib.waitTime(200)
        self.fail(result[0], result[1])

        if self.installStressTool:
            self.miscLib.waitTime(150)
        self.setTestStep("Sending the Fourth Alarm to the target")

        result = self.sshLib.sendCommand('%s %s%s"' % (self.ntfsendMsg4, linuxTimeText, startTime))
        if self.installStressTool:
            self.miscLib.waitTime(200)
        self.fail(result[0], result[1])

        if self.installStressTool:
            self.miscLib.waitTime(150)
        self.setTestStep("Sending the Fifth Alarm to the target")

        result = self.sshLib.sendCommand('%s %s%s"' % (self.ntfsendMsg5, linuxTimeText, startTime))
        if self.installStressTool:
            self.miscLib.waitTime(200)
        self.fail(result[0], result[1])

        # need to wait a little (3 seconds was not always enough) otherwise the files might not be there yet
        self.miscLib.waitTime(20)

    #
    # This method returns the uptime of a node in seconds
    #
    def calculatePayloadStartup(self, subrack, slot):

        result = self.sshLib.sendCommand("date +%s; uptime", subrack, slot)
        if result[0] != 'SUCCESS':
            self.myLogger.error(result[1])
            self.myLogger.debug('leave calculatePayloadStartup')
            return result
        if len(result[1].splitlines()) != 2:
            self.myLogger.debug('leave calculatePayloadStartup')
            return ('ERROR', 'Expected a response that has exacly two lines. Received: %s' %result[1])
        unixTimeOnTarget = result[1].splitlines()[0]
        if unixTimeOnTarget.isdigit() == True:
            unixTimeOnTarget = int(unixTimeOnTarget)
        else:
            self.myLogger.debug('leave calculatePayloadStartup')
            return ('ERROR', 'Expected a number representing the unix time on target. Received: %s' %result[1].splitlines()[0])
        uptimeLine = result[1].splitlines()[1]
        if 'day' in uptimeLine:
            days = uptimeLine.split()[2]
            if days.isdigit() == True:
                days = int(days)
            else:
                self.myLogger.debug('leave calculatePayloadStartup')
                return ('ERROR', 'Expected a number representing the days of uptime of the blade. Received: %s' %result[1].splitlines()[1])
            if len(uptimeLine.split()) > 3 and ':' in uptimeLine.split()[4]:
                uptimeLine = uptimeLine.split()[4]
                hours = uptimeLine.split(':')[0]
                if hours.isdigit():
                    hours = int(hours)
                else:
                    self.myLogger.debug('leave calculatePayloadStartup')
                    return ('ERROR', 'Expected a number representing the hours of uptime of the blade. Received: %s' %result[1].splitlines()[1])
                minutes = uptimeLine.split(':')[1][:-1]
                if minutes.isdigit() == True:
                    minutes = int(minutes)
                else:
                    self.myLogger.debug('leave calculatePayloadStartup')
                    return ('ERROR', 'Expected a number representing the minutes of uptime of the blade. Received: %s' %result[1].splitlines()[1])
            else:
                self.myLogger.debug('leave calculatePayloadStartup')
                return ('ERROR', 'Expected a field representing the hours:minutes of uptime of the blade. Received: %s' %result[1].splitlines()[1])
            uptimeSeconds = days*24*60*60 + hours*60*60 + minutes*60
        else:
            if uptimeLine.split()[3].strip() == "min,":
                minutes = uptimeLine.split()[2]
                if minutes.isdigit() == True:
                    minutes = int(minutes)
                uptimeSeconds = minutes*60
            else:
                uptimeLine = uptimeLine.split()[2]
                if ':' in uptimeLine:
                    hours = uptimeLine.split(':')[0]
                    if hours.isdigit():
                        hours = int(hours)
                    else:
                        self.myLogger.debug('leave calculatePayloadStartup')
                        return ('ERROR', 'Expected a number representing the hours of uptime of the blade. Received: %s' %result[1].splitlines()[1])
                    minutes = uptimeLine.split(':')[1][:-1]
                    if minutes.isdigit() == True:
                        minutes = int(minutes)
                    else:
                        self.myLogger.debug('leave calculatePayloadStartup')
                        return ('ERROR', 'Expected a number representing the minutes of uptime of the blade. Received: %s' %result[1].splitlines()[1])
                else:
                    self.myLogger.debug('leave calculatePayloadStartup')
                    return ('ERROR', 'Expected uptime information of the blade in the format hours:minutes. Received: %s' %uptimeLine)
                uptimeSeconds = hours*3600 + minutes*60

        #controllerDict = unixTimeOnTarget - uptimeSeconds
        self.myLogger.debug('leave calculatePayloadStartup')
        return ('SUCCESS', uptimeSeconds)
    def checkSystemStatus(self, searchPattern, startTimeSyslog):
        for i in range(10):
            result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, startTimeSyslog,self.testConfig)
            numOfMatchedPattern = len(result[1])
            if result[0] == 'SUCCESS' and numOfMatchedPattern > 2:
                result = self.safLib.clusterRebootNode(self.activeController[0],self.activeController[1])
                self.fail(result[0], result[1])
                self.miscLib.waitTime(70)
                self.fail('ERROR', 'The system is not OK after com restart')
                break
            else:
                self.miscLib.waitTime(20)
        return

    def tearDown(self):
        self.setTestStep('tearDown')

        if self.skip_test == False:
            if self.testHT70246 == 'True':
                # Copy the file back to original directory
                cmd = 'cp /home/HT70246/%s %s%s' %(self.fileName, self.rlistLocation,self.statusSection)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

                # Remove the temporary directory
                cmd = 'rm -rf /home/HT70246/'
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

                # Restart com
                cmd = 'comsa-mim-tool com_switchover'
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.miscLib.waitTime(15)
            else:
                if self.testcase_tag == 'TC-RPLIST-024':
                    # remove the previously created backup for this TC.
                    result = saf_lib.isBackup(self.backupName)
                    self.fail(result[0], result[1])
                    if result == ('SUCCESS','EXIST'):
                        result = saf_lib.backupRemove(self.backupName)
                        self.fail(result[0], result[1])

                if self.testcase_tag == 'TC-RPLIST-026' or self.testcase_tag == 'TC-RPLIST-027':
                    # Clear the alarms used for the test from the target
                    cmd = '%s%s %s' %(self.nbc_dir, self.alarmsClearScript, self.totalAlarms)
                    activeScIpAddr = self.comsa_lib.get_active_controller_ip(self.activeController, self.targetData)
                    result = self.sshLib.sendRawCommand(activeScIpAddr, cmd, "root", "rootroot", int(self.sendAlarmsTimeout))

                    self.fail(result[0], result[1])

                    self.setTestStep("Checking when the total alarms will be all cleared in CLI")
                    timeNow = int(time.time())
                    startTime = timeNow
                    endTime = timeNow + int(self.cliTimeout)
                    timeoutFlag = True
                    cliExpectedString = 'totalActive=0'

                    while timeNow < endTime:
                        cmd = '%s "show ManagedElement=1,SystemFunctions=1,Fm=1,totalActive" "exit"' %self.cli_active_controller_login_params
                        result = self.comsa_lib.executeCliSession(cmd)
                        self.fail(result[0], result[1])
                        if cliExpectedString in result[1]:
                            timeNow = int(time.time())
                            timeoutFlag = False
                            break
                        timeNow = int(time.time())

                    if timeoutFlag == True:
                        self.fail('ERROR', 'Timeout of %s seconds expired while waiting totalActive in CLIto become 0' %self.cliTimeout)
                    else:
                        elapsedTime = timeNow - startTime
                        self.myLogger.info('It took %s seconds for the %s alarms to be cleared in CLI' %(elapsedTime, cliExpectedString))

                    # Remove the scripts used for the test from the target
                    cmd = 'rm -rf %s' %(self.nbc_dir)
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0], result[1])

                else:
                    if self.testcase_tag == 'TC-RPLIST-023':
                        self.setTestStep("Restoring the system from backup")
                        result = self.comsa_lib.restoreSystem(self, self.backupName023, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                        self.fail(result[0], result[1])
                    else:
                        self.setTestStep("Clearing the 5 Alarms from the target")
                        result = self.sshLib.sendCommand('%s"' %self.ntfsendMsg1a)
                        self.fail(result[0], result[1])
                        result = self.sshLib.sendCommand('%s"' %self.ntfsendMsg2a)
                        self.fail(result[0], result[1])
                        result = self.sshLib.sendCommand('%s"' %self.ntfsendMsg3a)
                        self.fail(result[0], result[1])
                        result = self.sshLib.sendCommand('%s"' %self.ntfsendMsg4a)
                        self.fail(result[0], result[1])
                        result = self.sshLib.sendCommand('%s"' %self.ntfsendMsg5a)
                        self.fail(result[0], result[1])
                        if self.testcase_tag == 'TC-RPLIST-022':
                            self.setTestStep("Disable the SC_ABSENCE_ALLOWED flag after testing TC-RPLIST-022 ")
                            cmd = 'cmw-configuration --disable SC_ABSENCE_ALLOWED --reboot'
                            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                            self.fail(result[0], result[1])
                            self.miscLib.waitTime(120)

        else:
            self.myLogger.info('Teardown skipped')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

        #########################
        #### SUPPORT METHODS ####
        #########################

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
