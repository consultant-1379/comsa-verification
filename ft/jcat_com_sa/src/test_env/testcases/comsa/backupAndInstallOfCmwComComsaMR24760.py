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

    Tag: backupandinstallationOfCmwComComsa

    TC-MR24760-001 Install CMW3.3SH6, COM3.3SH3, COMSA build
    TC-MR24760-002 Install CMW3.3SH9, COM3.3SH3, COMSA build
    TC-MR24760-003 Install CMW3.3SH6, COM3.3SH3, COMSA3.2 CP1 -> Upgrade to COMSA build
    TC-MR24760-004 Install CMW3.3SH6, COMSA3.2 CP1 -> Upgrade to CMW3.3SH9 and COMSA build

    Help:
    The script requires the following files (and formats):
    CORE MW: the runtime tar file (example for CMW3.3SH6)
    COM: the runtime sdp and the installation sdp

    ""
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
from se.ericsson.jcat.fw import SUTHolder
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib
from java.lang import System

class backupAndInstallOfCmwComComsa(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        # parameters from the config files
        self.backupName = {}
        self.comBackupName = {}
        self.storedBackupFilesLocation = {}

        self.tmpdirMR24760 = {}
        self.pathToModelConfigFile = {}

        self.comsaBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}
        self.loctBackupLocation = {}

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

        self.cli_active_controller_login_params = ''
        self.cli_active_SC = ''

        self.clusterTime = ''

        self.reqComSaRelease = "3"
        self.reqComSaVersion = "R1A01"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)
        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.buildLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("SRC"))
        self.pathOfReleases = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.pathToAbs = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        self.testDir =  '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST"))
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.buildDir = dict.get('BUILD_TOKENS')
        self.resourceFilesLocation = "%s/MR24760_stop_delivery_model/" %dict.get("FUNCTIONAL_USER_FT")

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
        self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.comsaTmplCxp = dict.get('COM_SA_TMPL_CXP_RHEL')
        else:
            self.comsaTmplCxp = dict.get('COM_SA_TMPL_CXP')

        self.myLogger.info('Exit setUp')

    def runTest(self):

        self.setTestStep('runTest')

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

        if ComSaOK[1] == True:
            self.uninstallScriptName1 = 'uninstall_cmw.sh'
            self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'

            self.pathToCmwsh6Files = '%s/coremw3.2_latest/' %self.resourceFilesLocation
            self.pathToCmwsh9Files = '%s/coremw3.3_latest/' %self.resourceFilesLocation
            self.pathToCOMFiles = '%s/com3.3cp9/' %self.resourceFilesLocation
            self.pathToCOMSA32CP1Files = '%s/comsa3.2cp9/' %self.resourceFilesLocation

            self.pathToCmwInstallation = '%s/coremw/' %self.tmpdirMR24760
            self.pathToComInstallation = '%s/com/' %self.tmpdirMR24760
            self.pathToComsaInstallation = '%s/comsa/' %self.tmpdirMR24760

            self.sdpImportCommand = 'cmw-sdp-import'
            self.listCampaignCommand = 'cmw-repository-list --campaign'
            self.campaignComsaInstallName ='ERIC-ComSaInstall'
            self.campaignComsaUgradeName ='ERIC-ComSa-upgrade'
            self.comsa32CP1revision = 'ERIC-ComSa-CXP9017697_3-R3K01'
            self.campaignCMWUgradeName = 'ERIC-CMWUpgrade'

            # Get global variables

            self.myLogger.info('Exit setUp')

            # Variables needed for the build token management
            dirName = System.getProperty("logdir")
            user = os.environ['USER']
            self.tokenPattern = 'buildToken-%s' %user
            self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
            self.numberOfGetTokenRetries = 5

            self.memoryCheck = False
            if self.testSuiteConfig.has_key('memoryCheck'):
                self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

            if self.runUninstallationScript:
                self.copyFilesToTarget()
                self.backupCluster(self.backupName)
                self.copyBackupFiles()

            self.cleanSystem()
            self.lib.resetDumps()

            if self.restoreSnapshot:
                self.copyFilesToTarget()

            # CORE MW installation
            if self.tag == 'TC-MR24760-002':
                self.setTestStep('======== Installation of CMW 3.3 SH9=========')
                self.installCMW(self.pathToCmwsh9Files, self.pathToCmwInstallation)
            else:
                self.setTestStep('======== Installation of CMW 3.3 SH6=========')
                self.installCMW(self.pathToCmwsh6Files, self.pathToCmwInstallation)

            # Com Installation

            self.setTestStep('======== Installation of COM ========')
            self.installCOM(self.pathToCOMFiles, self.pathToComInstallation)

            #Com_SA Installation

            if (self.tag == 'TC-MR24760-003') or (self.tag == 'TC-MR24760-004'):
                self.setTestStep('======== Installation of COMSA 3.2CP1 ========')
                self.logToSys()
                self.installCOMSA(self.pathToCOMSA32CP1Files, self.pathToComsaInstallation)
            else:
                self.setTestStep('======== Build and Install COMSA from stream ========')
                self.logToSys()
                self.installCOMSAFromStream(self.pathToComsaInstallation)


            # Check result for TC-MR24760-001 and TC-MR24760-002
            if (self.tag == 'TC-MR24760-001'):
                comsaUsedRevion = self.getComSaUsingRevion()
                self.setTestStep('======== Checking if COMSA %s models are used ========' %comsaUsedRevion)
                self.checkWhoDeliveredModel("COMSA", comsaUsedRevion)
            elif (self.tag == 'TC-MR24760-002'):
                self.setTestStep('======== Checking if CMW models are used ========')
                self.checkWhoDeliveredModel("CMW", '')
            elif (self.tag == 'TC-MR24760-003') or (self.tag == 'TC-MR24760-004'):
                self.setTestStep('======== Checking if COMSA %s models are used ========' %self.comsa32CP1revision)
                self.checkWhoDeliveredModel("COMSA", self.comsa32CP1revision)

            # TC-MR24760-003 and TC-MR24760-004 will continue going
            if (self.tag == 'TC-MR24760-003'):
                self.setTestStep('======== Upgrade COMSA ========')
                self.logToSys()
                self.upgradeCOMSAFromStream(self.pathToComsaInstallation)
                comsaUsedRevion = self.getComSaUsingRevion()
                self.setTestStep('======== Checking if COMSA %s models are used ========' %comsaUsedRevion)
                self.checkWhoDeliveredModel("COMSA", comsaUsedRevion)

            elif (self.tag == 'TC-MR24760-004'):
                self.setTestStep('======== Upgrade to CMW33SH9 ========')
                self.logToSys()
                self.upgradeCMW(self.pathToCmwsh9Files, self.pathToCmwInstallation)
                self.setTestStep('======== Checking if CMW models are used ========')
                self.checkWhoDeliveredModel("CMW", '')
                # Upgrade COMSA
                self.setTestStep('======== Upgrade COMSA ========')
                self.logToSys()
                self.upgradeCOMSAFromStream(self.pathToComsaInstallation)
                self.setTestStep('======== Checking if CMW models are used ========')
                self.checkWhoDeliveredModel("CMW", '')
            if self.runUninstallationScript:
                #restore the cluster
                self.setTestStep('======== Restore cluster =========')
                self.restoreCluster(self.backupName)
        else:
            self.logger.info('Skipped trace tests because of COMSA version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True

        coreTestCase.CoreTestCase.runTest(self)

    def tearDown(self):
        self.setTestStep('tearDown')

        if self.skip_test == False:
            command = '\\rm -rf /home/tmpdirMR24760/'
            self.sshLib.sendCommand(command)

            command = '\\rm -rf %s' %self.storedBackupFilesLocation
            self.sshLib.sendCommand(command)

            self.sshLib.tearDownHandles()
            coreTestCase.CoreTestCase.tearDown(self)

        self.setTestStep('leave tearDown')

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


    def getComSaUsingRevion(self):
        self.logger.info('getComSaUsingRevion: Called')

        command = 'cmw-repository-list |grep "ERIC-ComSa-.*-[RP][0-9]*[A-Z][0-9]* Used" | sed "s/\(ERIC-ComSa-.*-[RP][0-9]*[A-Z][0-9]*\) Used/\\1/g" '
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])
        self.logger.info('getComSaUsingRevion: Comsa Used revision %s' %result[1] )

        if result[1] == '':
            self.fail('ERROR', 'Cannot find any Comsa revion on cluster')

        self.logger.info('getComSaUsingRevion: Exit')
        return '%s' %result[1]

    def restoreCluster(self, backupName):
        self.logger.info('restoreCluster: Called')
        self.logger.info('restoreCluster: backupName = %s' %backupName)
        # create a backup having the same name first
        result = self.safLib.isBackup(backupName)
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])
        elif result != ('SUCCESS','NOT EXIST'):
            result = self.safLib.backupRemove(backupName)
            if result[0] != 'SUCCESS':
                self.fail(result[0], result[1])

        result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = "")
        self.fail(result[0], result[1])

        # create com backup too
        if self.comBackupName != {}:
            result = self.safLib.isBackup(self.comBackupName)
            if result[0] != 'SUCCESS':
                self.fail(result[0], result[1])
            elif result != ('SUCCESS','NOT EXIST'):
                result = self.safLib.backupRemove(self.comBackupName)
                if result[0] != 'SUCCESS':
                    self.fail(result[0], result[1])

            result = self.comsa_lib.backupCreateWrapper(self.comBackupName, backupRpms = "")
            self.fail(result[0], result[1])

        #replace the backup files

        command = '\cp %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comsaBackupLocation, self.backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comBackupLocation, self.backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.cmwBackupLocation, self.backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])
        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupName, self.loctBackupLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        #replace the com backup files
        if self.comBackupName != {}:
            #command = '\cp %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.comBackupName, self.comsaBackupLocation, self.comBackupName)
            #result = self.sshLib.sendCommand (command)
            #self.fail(result[0], result[1])

            command = '\cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.comBackupName, self.comBackupLocation, self.comBackupName)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

            command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.comBackupName, self.cmwBackupLocation, self.comBackupName)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

            command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.comBackupName, self.loctBackupLocation)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

        #restore it to the original

        result = self.comsa_lib.restoreSystem(self, backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
        self.fail(result[0], result[1])


        self.logger.info('restoreCluster: Exit')


    def checkWhoDeliveredModel(self, expectedDelivered, comsaRevision):
        #expectedDelivered: CMW or COMSA
        self.logger.info('checkWhoDeliveredModel: Called')
        self.logger.info('checkWhoDeliveredModel: expectedDelivered = %s' %expectedDelivered)
        self.logger.info('checkWhoDeliveredModel: comsaRevision = %s' %comsaRevision)


        # CHECKING IF COMSA DELIVER FM
        command = 'cat /var/log/messages |grep "logToSys: called at %s" -A10000 | grep "ComSa delivereing FM model to IMM"' %self.clusterTime

        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            result1 = self.sshLib.sendCommand(command,2,1)
            self.fail(result1[0], result1[1])

            result2 = self.sshLib.sendCommand(command,2,2)
            self.fail(result2[0], result2[1])
        elif noOfScs == 1:
            result1 = self.sshLib.sendCommand(command)
            self.fail(result1[0], result1[1])

            result2 = self.sshLib.sendCommand(command)
            self.fail(result2[0], result2[1])

        if result1[1]=='' and result2[1]=='' :
            modelFBDeliverBy = 'CMW'
            if expectedDelivered=='COMSA' and comsaRevision != self.comsa32CP1revision :
                self.fail('ERROR', 'FM must be delivered by COMSA')
        else:
            modelFBDeliverBy = 'COMSA'
            if expectedDelivered=='CMW':
                self.fail('ERROR', 'FM must be delivered by CMW')


        # CHECKING CLI OUPUT

        #Creates the login params according to which controller runs the CLI

        serviceInstanceName = 'ComSa'
        amfNodePattern = 'Cmw'
        result = self.comsa_lib.findActiveController(self.testConfig, serviceInstanceName, amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
        self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])


        #Create the input, the expected output and the non-expected output lists
        lists = self.comsa_lib.load_TC_cli_config(self)

        #Send the cli commands and process the results element-by-element
        #One element of the list is one cli session.
        for list_index in range(0,len(lists[0])):
            result = self.comsa_lib.runCliSession(lists, list_index, self.cli_active_controller_login_params)
            self.fail(result[0], result[1])


        command = 'cat %s |grep .*Pm_mp.xml | wc -l' %self.pathToModelConfigFile
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])
        if result[1] != '1':
            self.fail('ERROR', 'Number of Pm_mp.xml files is not equal to 1')

        # Counting CmwPm_mp.xml
        command = 'cat %s |grep .*Pm_mp.xml | wc -l' %self.pathToModelConfigFile
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])
        if result[1] != '1':
            self.fail('ERROR', 'Number of Pm_mp.xml files is not equal to 1')

        # Counting SwIM_mp.xml
        command = 'cat %s |grep .*SwIM_mp.xml | wc -l' %self.pathToModelConfigFile
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])
        if result[1] != '1':
            self.fail('ERROR', 'Number of SwIM_mp.xml files is not equal to 1')

        # Counting SwM_mp.xml
        command = 'cat %s |grep .*SwM_mp.xml | wc -l' %self.pathToModelConfigFile
        result = self.sshLib.sendCommand(command)
        self.fail(result[0], result[1])
        if result[1] != '1':
            self.fail('ERROR', 'Number of SwM_mp.xml files is not equal to 1')


        if expectedDelivered=='CMW':

            #CMW is expected to deliger models
            command = 'cat %s |grep /storage/system/config/comsa_for_coremw-apr9010555/repository/.*Pm_mp.xml | wc -l' %self.pathToModelConfigFile
            result = self.sshLib.sendCommand(command)
            if result[1] != '1':
                self.logger.info('checkWhoDeliveredModel: result[1] = %s' %result[1])
                self.fail('ERROR', 'Number of CmwPm_mp.xml files is not equal to 1')

            command = 'cat %s |grep /storage/system/config/comsa_for_coremw-apr9010555/repository/.*SwIM_mp.xml | wc -l' %self.pathToModelConfigFile
            result = self.sshLib.sendCommand(command)
            if result[1] != '1':
                self.logger.info('checkWhoDeliveredModel: result[1] = %s' %result[1])
                self.fail('ERROR', 'Number of SwIM_mp.xml files is not equal to 1')

            command = 'cat %s |grep /storage/system/config/comsa_for_coremw-apr9010555/repository/.*SwM_mp.xml | wc -l' %self.pathToModelConfigFile
            result = self.sshLib.sendCommand(command)
            if result[1] != '1':
                self.logger.info('checkWhoDeliveredModel: result[1] = %s' %result[1])
                self.fail('ERROR', 'Number of SwM_mp.xml  files is not equal to 1')

        elif expectedDelivered=='COMSA':
            #COMSA is expected to deliger models
            command = 'cat %s |grep /storage/system/config/comsa_for_coremw-apr9010555/repository/%s/.*Pm_mp.xml | wc -l' %(self.pathToModelConfigFile, comsaRevision)
            result = self.sshLib.sendCommand(command)
            if result[1] != '1':
                self.logger.info('checkWhoDeliveredModel: result[1] = %s' %result[1])
                self.fail('ERROR', 'Number of CmwPm_mp.xml files is not equal to 1')

            command = 'cat %s |grep /storage/system/config/comsa_for_coremw-apr9010555/repository/%s/.*SwIM_mp.xml | wc -l' %(self.pathToModelConfigFile, comsaRevision)
            result = self.sshLib.sendCommand(command)
            if result[1] != '1':
                self.logger.info('checkWhoDeliveredModel: result[1] = %s' %result[1])
                self.fail('ERROR', 'Number of SwIM_mp.xml files is not equal to 1')

            command = 'cat %s |grep /storage/system/config/comsa_for_coremw-apr9010555/repository/%s/.*SwM_mp.xml | wc -l' %(self.pathToModelConfigFile, comsaRevision)
            result = self.sshLib.sendCommand(command)
            if result[1] != '1':
                self.logger.info('checkWhoDeliveredModel: result[1] = %s' %result[1])
                self.fail('ERROR', 'Number of SwM_mp.xml  files is not equal to 1')

        else:
            # Wrong parameter
            self.fail('ERROR', 'Wrong parameter')

        self.logger.info('checkWhoDeliveredModel: Exit')

    def backupCluster(self, backupName):
        self.setTestStep('======== Backup cluster first =========')
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

    def installCMW(self, setupFilesDir, pathToCmwInstallation):
        self.logger.info('installCMW: Called')
        self.logger.info('installCMW: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCMW: pathToCmwInstallation = %s' %pathToCmwInstallation)
        self.logger.info('installCMW: Copying of File(s) for CMW installation to the target.')

        # Check and wait until all tipc links are up
        self.logger.info('installCMW: Check and wait until all tipc links are up')
        for i in range(30):
            cmd = 'tipc-config -n'
            result = self.sshLib.sendCommand(cmd)
            self.myLogger.info('###tipc link status: %s' % result[1])
            if result[1].count('up') == len(self.testConfig['testNodesTypes']) - 1 :
                self.myLogger.info('All tipc links are UP!')
                break
            else:
                self.miscLib.waitTime(30)

        # Cleaning the directory
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToCmwInstallation)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToCmwInstallation)
        self.fail(result[0], result[1])



        cmd = 'ls %s | grep -v depl.tar' %(setupFilesDir)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'Core MW tar file not found at specified location: %s/ .' %setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one Core MW tar file found at specified location: %s/: %s.' %(setupFilesDir, str(result[1])))

        name_list = result[1].strip()
        fileName = name_list.split('/')[len(name_list.split('/')) - 1]

        result = self.sshLib.remoteCopy('%s%s'%(setupFilesDir,name_list), pathToCmwInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('cd %s; tar xvf %s' %(pathToCmwInstallation, fileName))
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File not found: %s/%s.' %(pathToCmwInstallation, fileName))

        self.logger.info('installCMW: Installation of CMW ')
        cmw_install_command = 'chmod u+x %s/install' %pathToCmwInstallation
        result = self.sshLib.sendCommand (cmw_install_command)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File not found: %s/install.' %pathToCmwInstallation)

        self.logger.debug('installCMW: Getting Default Time out')
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            result = self.sshLib.getTimeout(2, 1)
            defTimeout = result[1]
            self.logger.debug('Setting Time Out to 3600 sec or one hour')
            self.sshLib.setTimeout(3600, 2, 1)
            self.sshLib.setTimeout(3600, 2, 2)
        elif noOfScs == 1:
            result = self.sshLib.getTimeout()
            defTimeout = result[1]
            self.logger.debug('Setting Time Out to 3600 sec or one hour')
            self.sshLib.setTimeout(3600)

        cmw_install_command = 'cd %s; ./install' %pathToCmwInstallation
        expectedPrintout = "Install script completed successfully"
        result = self.sshLib.sendCommand(cmw_install_command)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File not found: %s/install.' %pathToCmwInstallation)
        elif expectedPrintout not in result[1]:
            self.fail('ERROR', 'Expected printout "%s" not received. Installation log: %s' %(expectedPrintout, result[1]))
        self.logger.debug('installCMW: Setting back the default time out : %s' %(defTimeout))
        if noOfScs == 2:
            self.sshLib.setTimeout(defTimeout, 2, 1)
            self.sshLib.setTimeout(defTimeout, 2, 2)
        elif noOfScs == 1:
            self.sshLib.setTimeout(defTimeout)


        self.sshLib.tearDownHandles()


        self.logger.info('Checking cmw-status ......')

        okFlag = False
        for i in range(5):
            result = self.safLib.checkClusterStatus()
                # Get the system status and displays only the failed components Wrapped command:
            if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
            else:
                self.logger.debug("installCMW: status not ok waiting 30 seconds to re-check the status")
                self.miscLib.waitTime(30)
        if okFlag == False:
            self.fail('ERROR','Failed to install CMW')

        self.logger.info('installCMW: Exit')

    def upgradeCMW(self, setupFilesDir, pathToCmwInstallation):
        self.logger.info('upgradeCMW: Called')
        self.logger.info('upgradeCMW: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('upgradeCMW: pathToCmwInstallation = %s' %pathToCmwInstallation)
        self.logger.info('upgradeCMW: Copying of File(s) for CMW installation to the target.')

        # Check and wait until all tipc links are up
        self.logger.info('upgradeCMW: Check and wait until all tipc links are up')
        for i in range(30):
            cmd = 'tipc-config -n'
            result = self.sshLib.sendCommand(cmd)
            self.myLogger.info('###tipc link status: %s' % result[1])
            if result[1].count('up') == len(self.testConfig['testNodesTypes']) - 1 :
                self.myLogger.info('All tipc links are UP!')
                break
            else:
                self.miscLib.waitTime(30)

        # Cleaning the directory
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToCmwInstallation)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToCmwInstallation)
        self.fail(result[0], result[1])

        # Upload CMW setup file to cluster and untar these
        fileName = self.getAbsoluteFileNameClearCase('ls -d %s/* | grep -v depl.tar' %(setupFilesDir), setupFilesDir)
        result = self.sshLib.remoteCopy(fileName, pathToCmwInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('cd %s; tar xvf *.tar' %(pathToCmwInstallation))
        self.fail(result[0], result[1])

        fileName = self.getAbsoluteFileNameClearCase('ls -d %s/* | grep depl.tar' %(setupFilesDir), setupFilesDir)
        result = self.sshLib.remoteCopy(fileName, pathToCmwInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('cd %s; tar xvf *depl.tar' %(self.pathToCmwInstallation))
        self.fail(result[0], result[1])

        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File not found: %s/%s.' %(pathToCmwInstallation, fileName))

        # Upgrade of CMW
        self.logger.info('upgradeCMW: Upgrade of CMW ')

        # Import SDP package
        self.logger.info ('upgradeCMW: Importing SDP')
        cmd = 'cd %s; %s COREMW_*.sdp' %(self.pathToCmwInstallation, self.sdpImportCommand)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        cmd = 'cd %s; %s ERIC-COREMW-C+P*.sdp' %(self.pathToCmwInstallation, self.sdpImportCommand)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # Start campaign

        self.logger.info ('upgradeCMW: campaign start')
        self.safLib.upgradeStart(self.campaignCMWUgradeName, '')
        self.fail(result[0], result[1])

        result = self.comsa_lib.waitForCampaignReady(self.campaignCMWUgradeName, timeout = 2100, rollingUpgrade = True)
        self.fail(result[0], result[1])

        # Commiting the campaign
        self.logger.info ('upgradeCMW: Commiting')

        result = self.safLib.upgradeCommit(self.campaignCMWUgradeName)
        self.fail(result[0], result[1])

        result = self.safLib.removeSwBundle(self.campaignCMWUgradeName)
        self.fail(result[0], result[1])

        # Checking the cmw-status
        self.logger.info('upgradeCMW: Checking cmw-status ......')

        okFlag = False
        for i in range(5):
            result = self.safLib.checkClusterStatus()
                # Get the system status and displays only the failed components Wrapped command:
            if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
            else:
                self.logger.debug("upgradeCMW: status not ok waiting 30 seconds to re-check the status")
                self.miscLib.waitTime(30)
        if okFlag == False:
            self.fail('ERROR','Failed to install CMW')

        self.logger.info('upgradeCMW: Exit')

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
            self.fail('ERROR', 'More than one COM campaign sdp file found at specified location: %s/: %s.' %(localPathToSw, str(result[1])))
        name_list = result[1].strip()
        self.logger.info('name_list: (%s)'%name_list)

        result = self.sshLib.remoteCopy(name_list, self.pathToComInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])


        cmd = '%s %s*.sdp' %(self.sdpImportCommand, self.pathToComInstallation)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.logger.info ('installCOM: COM-Campaign-Start')

        result = self.sshLib.sendCommand(self.listCampaignCommand)
        self.fail(result[0], result[1])
        self.logger.info('Result of %s:(%s)'%(self.listCampaignCommand, str(result[1])))
        campaignName = result[1]

        result = self.safLib.upgradeStart(campaignName, '')
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Result of campaign_start:(%s)'%str(result))

        # Checking that the campaign has completed (Initial, Executing, Completed) or not !

        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(campaignName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COM')

        result = self.safLib.upgradeCommit(campaignName)
        self.fail(result[0], result[1])


        result = self.safLib.removeSwBundle(campaignName)
        self.fail(result[0], result[1])

        result = self.safLib.checkClusterStatus()
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')

    def installCOMSA(self, setupFilesDir, pathToComsaInstallation):
        self.logger.info('installCOMSA: Called')
        self.logger.info('installCOMSA: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCOMSA: pathToComsaInstallation = %s' %pathToComsaInstallation)

        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Upload COMSA setup file to cluster and untar these
        fileName = self.getAbsoluteFileNameClearCase('ls -d %s/* | grep -v depl.tar' %(setupFilesDir), setupFilesDir)
        result = self.sshLib.remoteCopy(fileName, pathToComsaInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('cd %s; tar xvf *.tar' %(pathToComsaInstallation))
        self.fail(result[0], result[1])

        fileName = self.getAbsoluteFileNameClearCase('ls -d %s/* | grep depl.tar' %(setupFilesDir), setupFilesDir)
        result = self.sshLib.remoteCopy(fileName, pathToComsaInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('cd %s; tar xvf *depl.tar' %(self.pathToComsaInstallation)) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])




        # Import SDP package

        self.logger.info ('installCOMSAFromStream: Importing ComSa SDP')
        fileName = self.getAbsoluteFileNameCluster('ls -d %s/*.sdp' %(self.pathToComsaInstallation), pathToComsaInstallation)
        cmd = '%s %s' %(self.sdpImportCommand, fileName)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # determine suitable package for 1 or 2 controller node
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            cmd = 'ls -d %s/COM_SA_I1_*/*.sdp' %(self.pathToComsaInstallation)
        elif noOfScs == 1:
            cmd = 'ls -d %s/COM_SA_I2_*/*.sdp' %(self.pathToComsaInstallation)
        else:
            self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' %str(noOfScs))


        fileName = self.getAbsoluteFileNameCluster(cmd, pathToComsaInstallation)
        cmd = '%s %s' %(self.sdpImportCommand, fileName)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # Start campaign

        self.logger.info ('installCOMSA: Install campaign start')
        self.safLib.upgradeStart(self.campaignComsaInstallName, '')
        self.fail(result[0], result[1])
        # Waiting until campaign complete
        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(self.campaignComsaInstallName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COM')

        # Commiting the campaign
        self.logger.info ('installCOMSA: commiting')

        result = self.safLib.upgradeCommit(self.campaignComsaInstallName)
        self.fail(result[0], result[1])

        result = self.safLib.removeSwBundle(self.campaignComsaInstallName)
        self.fail(result[0], result[1])

        result = self.safLib.checkClusterStatus()
        self.fail(result[0], result[1])

        self.logger.info('installCOMSA: Exit')

    def getAbsoluteFileNameClearCase(self, parternCommand, baseDir):
        self.logger.info('getAbsoluteFileNameClearCase: Called')
        self.logger.info('getAbsoluteFileNameClearCase: parternCommand = %s' %parternCommand)
        cmd = '%s' %(parternCommand)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'No such file or directory')
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one file found at specified location')
        name_list = result[1].strip()

        self.logger.info('getAbsoluteFileNameClearCase: Exit')
        return '%s' %( name_list)

    def getAbsoluteFileNameCluster(self, parternCommand, baseDir):
        self.logger.info('getAbsoluteFileNameCluster: Called')
        self.logger.info('getAbsoluteFileNameCluster: parternCommand = %s' %parternCommand)
        cmd = '%s' %(parternCommand)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'No such file or directory')
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one file found at specified location')
        name_list = result[1].strip()

        self.logger.info('getAbsoluteFileNameCluster: Exit')
        return '%s' %(name_list)

    def upgradeCOMSAFromStream(self, pathToComsaInstallation):
        self.logger.info('upgradeCOMSAFromStream: Called')

        result = self.sshLib.sendCommand('\\rm -rf %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Build comsa first

        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
        if BuildPath[0] != 'SUCCESS':
            self.logger.error(result[1])
            self.logger.debug('upgradeCOMSAFromStream: Exit')
            return (BuildPath[0], 'Build COM SA failed')
        result = self.comsa_lib.copyFilesToTarget(['%s/' %BuildPath[6], '%s/' %BuildPath[9]], self.pathToComsaInstallation, True)
        self.fail(result[0],result[1])

        # Untar some files
        result = self.sshLib.sendCommand('tar xvf %s/*%s*.tar* -C %s' %(self.pathToComsaInstallation, self.comsaTmplCxp, self.pathToComsaInstallation)) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Import SDP package

        self.logger.info ('upgradeCOMSAFromStream: Importing ComSa SDP')

        cmd = '%s %s%s' %(self.sdpImportCommand, self.pathToComsaInstallation, BuildPath[1])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # determine suitable package for 1 or 2 controller node
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            cmd1 = 'cd %s/COM_SA_U2_*/ ; ./comsa-generate-campaign-sdp' %(self.pathToComsaInstallation)
            cmd2 = 'cd %s/COM_SA_U2_*/ ; %s ./*.sdp' %(self.pathToComsaInstallation, self.sdpImportCommand)
        elif noOfScs == 1:
            cmd1 = 'cd %s/COM_SA_U3_*/ ; ./comsa-generate-single-campaign-sdp' %(self.pathToComsaInstallation)
            cmd2 = 'cd %s/COM_SA_U3_*/ ; %s ./*.sdp' %(self.pathToComsaInstallation, self.sdpImportCommand)
        else:
            self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' %str(noOfScs))

        result = self.sshLib.sendCommand(cmd1)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand(cmd2)
        self.fail(result[0], result[1])

        # Start campaign
        self.logger.info ('upgradeCOMSAFromStream: Install campaign start')
        self.safLib.upgradeStart(self.campaignComsaUgradeName, '')
        self.fail(result[0], result[1])
        # Waiting until campaign complete
        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(self.campaignComsaUgradeName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COM')

        # Commiting the campaign
        self.logger.info ('upgradeCOMSAFromStream: commiting')

        result = self.safLib.upgradeCommit(self.campaignComsaUgradeName)
        self.fail(result[0], result[1])

        result = self.safLib.removeSwBundle(self.campaignComsaUgradeName)
        self.fail(result[0], result[1])

        result = self.safLib.checkClusterStatus()
        self.fail(result[0], result[1])

        self.logger.info('upgradeCOMSAFromStream: Exit')

    def installCOMSAFromStream(self, pathToComsaInstallation):
        self.logger.info('installCOMSAFromStream: Called')

        result = self.sshLib.sendCommand('\\rm -rf %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Build comsa first
        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
        if BuildPath[0] != 'SUCCESS':
            self.logger.error(result[1])
            self.logger.debug('installCOMSAFromStream: Exit')
            return (BuildPath[0], 'Build COM SA failed')
        result = self.comsa_lib.copyFilesToTarget(['%s/' %BuildPath[6], '%s/' %BuildPath[7]], self.pathToComsaInstallation, True)
        self.fail(result[0],result[1])

        # Import SDP package

        self.logger.info ('installCOMSAFromStream: Importing ComSa SDP')

        cmd = '%s %s%s' %(self.sdpImportCommand, self.pathToComsaInstallation, BuildPath[1])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        cmd = '%s %s%s' %(self.sdpImportCommand, self.pathToComsaInstallation, BuildPath[2])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # Start campaign
        self.logger.info ('installCOMSAFromStream: Install campaign start')
        self.safLib.upgradeStart(self.campaignComsaInstallName, '')
        self.fail(result[0], result[1])
        # Waiting until campaign complete
        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(self.campaignComsaInstallName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COM')

        # Commiting the campaign
        self.logger.info ('installCOMSAFromStream: commiting')

        result = self.safLib.upgradeCommit(self.campaignComsaInstallName)
        self.fail(result[0], result[1])

        result = self.safLib.removeSwBundle(self.campaignComsaInstallName)
        self.fail(result[0], result[1])

        result = self.safLib.checkClusterStatus()
        self.fail(result[0], result[1])

        self.logger.info('installCOMSAFromStream: Exit')

    def cleanSystem(self):
        self.setTestStep('======== Clean the system =========')
        self.logger.info('cleanSystem: Called')

        if self.runUninstallationScript:
            cmw_uninstall_command1 = '%s%s' %(self.tmpdirMR24760, self.uninstallScriptName1)
            result = self.sshLib.sendCommand (cmw_uninstall_command1)

            self.logger.info('cleanSystem: Reboot cluster')
            reboot_cluster = 'cluster reboot -a'
            result = self.sshLib.sendCommand (reboot_cluster)
            self.fail(result[0], result[1])
            self.sshLib.tearDownHandles()

            self.miscLib.waitTime(200)
            self.logger.info('cleanSystem: Waiting until cluster up')
            for i in range(60):
                cmd = 'tipc-config -n'
                result = self.sshLib.sendCommand(cmd)
                self.myLogger.info('###tipc link status: %s' % result[1])
                ### This code is not working for 1-node clusters: len(self.testConfig['testNodesTypes']) - 1 is zero!
                if result[0] == 'SUCCESS' and result[1].count('up') == len(self.testConfig['testNodesTypes']) - 1 :
                    self.myLogger.info('All tipc links are UP!')
                    break
                else:
                    self.miscLib.waitTime(10)

            self.logger.info('cleanSystem: Run uninstall script again')

            cmw_uninstall_command2 = '%s%s' %(self.tmpdirMR24760, self.uninstallScriptName2)
            result = self.sshLib.sendCommand (cmw_uninstall_command2)
            self.fail(result[0], result[1])
        if self.restoreSnapshot:
            tmpDirOnTarget = 'notUsed'
            uninstallScriptName = 'notUsed'
            result = self.comsa_lib.unInstallSystem(tmpDirOnTarget, uninstallScriptName, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
            self.fail(result[0], result[1])

        self.logger.info('cleanSystem: Exit')

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

    def copyFilesToTarget(self):
        # 1.Copy Uninstallation CMW scripts to cluster
        self.setTestStep('======== Copy Uninstallation CMW scripts to cluster =========')
        result = self.sshLib.sendCommand('\\rm -rf %s' %self.tmpdirMR24760)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir %s' %self.tmpdirMR24760)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
        self.fail(result[0], result[1])


        result = self.sshLib.remoteCopy('%s/uninstall_cmw.sh' %(self.resourceFilesLocation), self.tmpdirMR24760, timeout = 120)
        self.fail(result[0],result[1])

        result = self.sshLib.remoteCopy('%s/cmw-rm-storage-dirs.sh' %(self.resourceFilesLocation), self.tmpdirMR24760, timeout = 120)
        self.fail(result[0],result[1])

        result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.tmpdirMR24760)
        self.fail(result[0], result[1])

    def copyBackupFiles(self):
        # 3.Copy backup files to stored location
        self.setTestStep('======== Copy backup files to stored location =========')

        result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir %s' %self.storedBackupFilesLocation)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.backupName, self.storedBackupFilesLocation)
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])

        # Copy com backup files to stored location
        self.comBackupName = self.findComBackup(self.comBackupName)
        if self.comBackupName != {}:
            # This is not needed because the COM backup does not contain COM SA elements
            #command = '\cp %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
            #result = self.sshLib.sendCommand (command)
            #self.fail(result[0], result[1])

            command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

            command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

            command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.comBackupName, self.storedBackupFilesLocation)
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases

