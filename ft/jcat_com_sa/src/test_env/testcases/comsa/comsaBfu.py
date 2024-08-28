#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
###############################################################################
#
# © Ericsson AB 2007 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################


'''File information:
   ===================================================


   Slogan:
   upgrade COM-SA on target using BFU campaign template

   Description:
   This script upgrades COMSA. (restoring COM backup, rebooting the cluster, and installing "old" COMSA, then upgrading to the current COMSA using BFU campaign template)

   Priority:
   Not applicable

   Precondition:
   At least one controller must be up and running with LOTC, CMW, (COM-EA), COM with "com" backup.

   Action:

   1. Restore partial backup of COM

   2. Check CMW status, and wait for status ok

   3. Reboot the cluster

   4. Wait until controller 1 is up

   5. Check and wait until all tipc links are up

   6. Wait for CMW status ok

   7. Install "old" COMSA

       # Upload COMSA runtime SDP and COMSA deployment template SDP to target from specified location

       # Import all SDPs to repository

       # Start COMSA installation

       # Check and wait until the installation finishes

       # Wait for CMW status ok

       # Commit the installation

       # Check if the installation is commited

       # Wait for CMW status ok

   8. Upgrade COM-SA using BFU campaign from the current build

       # Build COMSA by doing "comsabuild clean; comsabuild all"

       # Upload COMSA runtime SDP and COMSA deployment template SDP to target from specified location

       # Import all SDPs to repository

       # Start COMSA installation

       # Check and wait until the installation finishes

       # Wait for CMW status ok

       # Commit the installation

       # Check if the installation is commited

       # Wait for CMW status ok

?   8. Remove old COM-SA backup

?   9. Create COM-SA backup

  10. Wait for CMW status ok

  11. Remove all existing installation campaigns


   Result:
   System dependent

   Restore:
   Not applicable

   Configuration:
   Not applicable

'''

import test_env.fw.coreTestCase as coreTestCase
import time

import os,sys,re
from java.lang import System

class UpgradeCOMSA(coreTestCase.CoreTestCase):


    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.testcase_tag = tag
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        # parameters from the config files
        self.com_backup_name = ''
        self.default_com_backup_name = 'com'
        self.comsa_old_version = ''
        self.old_comsa = ''    # must be provided in the parameter file
        self.reqComSaMajorVersion = "3"
        self.reqComSaRelease = "3"
        self.reqComSaVersion = "R3A14"
        self.reqCmwRelease = "1"
        self.reqCmwVersion = "R6A12"
        self.reqComRelease = "2"
        self.reqComVersion = "R6A15"

        self.BfuCL5_reqCmwRelease = "1"
        self.BfuCL5_reqCmwVersion = "P1A99"    # CoreMW 3.2 latest
        self.BfuCL5_reqComRelease = "2"
        self.BfuCL5_reqComVersion = "R7A08"    # COM 3.2 PRA

        self.old_comsa_major_version = '2'
        self.backupName = "bfuBackup"
        self.backupName9 = "bfuBackup_TC-009"
        self.upgradeType = "bfu"
        self.storedBackupFilesLocation = {}
        self.comsaBackupLocation = {}
        self.lotcBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}
        self.removeCoreMW = 'False'
        self.upgradePRA = 'False'

    def id(self):
        return "Upgrade COMSA on the cluster"


    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.path_to_bfu = dict.get("PATH_TO_BFU")
        self.resourceFilesLocation = dict.get("PATH_TO_BFU")
        if self.testcase_tag != 'TC-BFU-020':
            self.path_of_old_comsa = '%s%s' %(self.path_to_bfu, self.old_comsa)
        self.cxpArchive = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.absDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER_RHEL')
        else:
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER')
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        self.swDir = System.getProperty("swDirNumber")
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')
        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        self.bfuLocation = '/home/bfu/'

        self.pathToCmwInstallation = '%s/coremw/' %self.bfuLocation
        self.pathToComInstallation = '%s/com/' %self.bfuLocation
        self.pathToComsaInstallation = '%s/comsa/' %self.bfuLocation

        self.CoreMW = "%s/coremw3.2_latest" %self.resourceFilesLocation
        self.CoreMWSdp = 'COREMW_RUNTIME-CXP9020355_1.tar'

        self.COM_latest = "%s%s/com" %(self.installRoot, self.swDir)
        self.ComSABuild = "%s/comsa" %self.resourceFilesLocation

        #Temporary fix using coremw3.2 latest blackbuild to work with COMSA3.6. There is no plan to deliver new CP CMW 3.2 package yet
        self.CMW_Sdp_for_BFUCL5 = "COREMW_RUNTIME-CXP9020355_1.tar"
        self.CMW_for_BFUCL5 = "%scoremw3.2_latest/%s" %(self.resourceFilesLocation, self.CMW_Sdp_for_BFUCL5)
        self.COM_for_BFUCL5 = "%s/com3.2pra" %self.resourceFilesLocation

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)

        try:
            self.removeCoreMW = eval(self.removeCoreMW)
        except NameError:
            self.fail('ERROR', 'self.removeCoreMW must be a string "True" or "False." Current value: %s' %self.removeCoreMW)

        self.restoreSnapshot = False
        self.runUninstallationScript = False
        if self.removeCoreMW:
            self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        """
        Stress Tool option
        """
        self.installStressTool = eval(System.getProperty("runStressTool"))

        #self.super__setUp()
        self.currentTestCase = self


    def runTest(self):
        ''' upgrade COM-SA on the cluster
        '''

        ComsaOK = ('SUCCESS', True)
        ComsaMajorOK = ('SUCCESS', True)
        ComOK = ('SUCCESS', True)
        CmwOK = ('SUCCESS', True)
        #BfuCL5_ComOK = ['', False]
        #BfuCL5_CmwOK = ['', False]
        ComsaU2TestValid = False
        self.skip_test = False

        self.temp_dir = '/home/coremw/incoming/'
        self.temp_bfu = '/home/bfu/'

        offlineVersionComSa = ['','','']
        offlineVersionCom = ['','','']
        offlineVersionCoreMW = ['','','']

        # Temporary fix latest COMSA 3.2 CP install failed with COM version >= 4.1 (4-R2A01)
        if self.testcase_tag == 'TC-BFU-009' or self.testcase_tag == 'TC-BFU-010':
            tmpComRelease = '4'
            tmpComVersion = 'R2A01'
            ComOK = self.lib.checkComponentVersion('com', tmpComRelease, tmpComVersion)

            if ComOK[1] == True:
                self.logger.info('Skipped BFU tests because of COM version not compatible! (Temporary)')
                self.setAdditionalResultInfo('Test skipped; version not compatible')
                self.skip_test = True
                return

        if self.upgradeType == "bfu" and self.upgradePRA == 'False':

            if self.restoreSnapshot:
                ComsaMajorOK = ['', False]
                result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'comsa')
                if result[0] == "REGTEST":
                    offlineVersionComSa[0] = result[1] #COMSA_release
                    offlineVersionComSa[1] = result[2] #COMSA_release
                    offlineVersionComSa[2] = result[3] #COMSA_majorVersion
                    ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion, offlineVersion = offlineVersionComSa)
                    ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion, offlineVersion = offlineVersionComSa)
                else:
                    ComsaMajorOK[1] = True

                ComOK = ['', False]
                result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'com')
                if result[0] == "REGTEST":
                    offlineVersionCom[0] = result[1]
                    offlineVersionCom[1] = result[2]
                    offlineVersionCom[2] = result[3]
                    ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion, offlineVersion = offlineVersionCom)
                else:
                    ComOK[1] = True
                    #BfuCL5_ComOK[1] = True

                CmwOK = ['', False]
                result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'coremw')
                if result[0] == "REGTEST":
                    offlineVersionCoreMW[0] = result[1]
                    offlineVersionCoreMW[1] = result[2]
                    offlineVersionCoreMW[2] = result[3]
                    CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion, offlineVersion = offlineVersionCoreMW)
                else:
                    CmwOK[1] = True
                    #BfuCL5_CmwOK[1] = True

            if self.runUninstallationScript or self.removeCoreMW == False:
                self.setTestStep('Check the required versions of ComSA, Com and CMW are installed for BFU tests')
                ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
                self.fail(ComsaOK[0],ComsaOK[1])
                ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion)
                self.fail(ComsaMajorOK[0],ComsaMajorOK[1])
                ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion )
                self.fail(ComOK[0],ComOK[1])
                CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
                self.fail(CmwOK[0],CmwOK[1])


        if self.upgradeType == 'u2' and self.upgradePRA == 'False':
            """
            U2 upgrade is supported only from [(Current release) - 1] to current release and
            from previous version of same release.
            Example upgrade to COM SA 3.4 is only supported from COM SA 3.3 and COM SA 3.4
            """
            if self.restoreSnapshot:
                result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'comsa')
                if result[0] == "REGTEST":
                    currentComsaMajor = result[3]
                else:
                    result = self.lib.getComponentVersion(self.comsaCxpNumber)
                    self.fail(result[0], result[1])
                    currentComsaMajor = result[3]
            elif self.runUninstallationScript or self.removeCoreMW == False:
                result = self.lib.getComponentVersion(self.comsaCxpNumber)
                self.fail(result[0], result[1])
                currentComsaMajor = result[3]
            if (int(self.old_comsa_major_version) >= int(currentComsaMajor) - 1) and \
                (int(self.old_comsa_major_version) <= int(currentComsaMajor)):
                ComsaU2TestValid = True
            ComsaMajorOK = ('SUCCESS', ComsaU2TestValid & ComsaMajorOK[1])

        if self.upgradePRA == 'True':
            """
            Upgrade from PRA to latest CP of the same COMSA major version
            """
            self.logger.info('UpgradePRA called')
            if self.restoreSnapshot:
                result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'comsa')
                if result[0] == "REGTEST":
                    currentComsaMajor = result[3]
                else:
                    result = self.lib.getComponentVersion(self.comsaCxpNumber)
                    self.fail(result[0], result[1])
                    currentComsaMajor = result[3]
            elif self.runUninstallationScript or self.removeCoreMW == False:
                result = self.lib.getComponentVersion(self.comsaCxpNumber)
                self.fail(result[0], result[1])
                currentComsaMajor = result[3]
            if (int(self.old_comsa_major_version) == int(currentComsaMajor)):
                ComsaU2TestValid = True
            ComsaMajorOK = ('SUCCESS', ComsaU2TestValid & ComsaMajorOK[1])
        # This check XxxOK is not needed for BFU CL5 tests as we will install later
        # the required CoreMW and COM versions if needed
        if (ComsaOK[1] and ComsaMajorOK[1] and ComOK[1] and CmwOK[1] and self.testcase_tag == 'TC-BFU-020'):
            ###########################################################################
            # Upgrade to the current COMSA
            ###########################################################################

            dict = self.comsa_lib.getGlobalConfig(self)
            self.bfu_bundle_name = dict.get('CXP_SDP_NAME_OFFICIAL')
            self.setTestStep('Build the current COMSA')
            self.logger.info('buildAndStoreCOMSA Called ')
            BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
            if BuildPath[0] != 'SUCCESS':
                self.logger.error(result[1])
                self.logger.debug('Build COMSA failed : Exit')
                return (BuildPath[0], 'Build COM SA failed')

            # Create COM-SA temp directory
            cmd = 'mkdir -p %s' %self.temp_dir
            self.myLogger.debug('Create COM-SA temp directory by: %s' %cmd)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # create directory on the target to copy the BFU archive files
            cmd = 'rm -f %s/*' %(self.temp_dir)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            cmd = 'mkdir -p %s' %(self.temp_bfu)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            # copy the BFU archives to the target.
            self.myLogger.debug('Copying the BFU archive files to the target')
            # BuildPath[9] is the file name with absolute path of Template tar file
            # BuildPath[10] is the file name with absolute path of Runtime tar file
            result = self.comsa_lib.copyFilesToTarget(['%s/' %BuildPath[9], '%s/' %BuildPath[10]], self.temp_bfu, False)
            self.fail(result[0], result[1])

            self.setTestStep('Unpack the COMSA installation archives on the target')
            self.myLogger.debug('Unpacking the BFU archives on the target')
            cmd = 'cd %s ; tar xf %s' %(self.temp_bfu, BuildPath[5])
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            cmd = 'cd %s ; tar xf %s' %(self.temp_bfu, BuildPath[4])
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            self.setTestStep('Import the COMSA BFU campaign to CoreMW repository')
            self.myLogger.debug('Importing the COMSA BFU campaign to CoreMW repository')

            bfuBundleSdp = '%s%s' %(self.temp_bfu, self.bfu_bundle_name)

            # copy to /home/coremw/incoming because importSwBundle() uses this dir !
            cmd = '\cp -f %s %s' %(bfuBundleSdp, self.temp_dir)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            if self.upgradeType == "bfu":

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

            result = self.comsa_lib.installComp(self.temp_dir, self.bfu_bundle_name, upgradeCampaignSdp, 'comsa', createBackup = False, backupRpms = self.backupRpmScript, supportBfuSameVer = True)
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

            # Cleanup
            self.setTestStep('Removing all existing installation campaigns')
            self.myLogger.debug('Removing all existing installation campaigns')
            result = self.safLib.getImportedCampaigns()
            if result[0] == 'SUCCESS' and result[1] != '':
                campaigns = result[1].split('\n')
                for campaign in campaigns:
                    self.safLib.removeSwBundle(campaign)
                    while None != re.search('SA_AIS_ERR_TRY_AGAIN', result[1]):
                        self.miscLib.waitTime(2)
                        result=self.safLib.removeSwBundle(campaign)

            coreTestCase.CoreTestCase.runTest(self)
        elif ((ComsaOK[1] and ComsaMajorOK[1] and ComOK[1] and CmwOK[1]) or
            (self.testcase_tag == 'TC-BFUCL5-001' or
             self.testcase_tag == 'TC-BFUCL5-002' or
             self.testcase_tag == 'TC-BFUCL5-003' or
             self.testcase_tag == 'TC-BFUCL5-004' or
             self.testcase_tag == 'TC-BFUCL5-005' or
             self.testcase_tag == 'TC-BFUCL5-006' or
             self.testcase_tag == 'TC-BFUCL5-007' or
             self.testcase_tag == 'TC-BFUCL5-008' or
             self.testcase_tag == 'TC-BFUCL5-009' or
             self.testcase_tag == 'TC-BFUCL5-010' or
             self.testcase_tag == 'TC-BFUCL5-011' or
             self.testcase_tag == 'TC-BFUCL5-012')):

            self.setTestStep('runTest')

            # Variables needed for the build token management
            dirName = System.getProperty("logdir")
            user = os.environ['USER']
            self.tokenPattern = 'buildToken-%s' %user
            self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
            self.numberOfGetTokenRetries = 5

            skipCreateBackup = False
            if self.testSuiteConfig.has_key('restoreBackup'):
                result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
                if result == ('SUCCESS', 'EXIST'):
                    self.backupName = self.testSuiteConfig['restoreBackup']
                    skipCreateBackup = True
                    self.myLogger.info('Standard COM SA backup exists. Skip creating identical backup.')
            if not skipCreateBackup:
                result = self.safLib.isBackup(self.backupName)
                if result[0] != 'SUCCESS':
                    #self.testSuiteConfig['failedSetUpTestCase'] = 'True'
                    self.fail(result[0], result[1])
                elif result != ('SUCCESS','NOT EXIST'):
                    result = self.safLib.backupRemove(self.backupName)
                    if result[0] != 'SUCCESS':
                        #self.testSuiteConfig['failedSetUpTestCase'] = 'True'
                        self.fail(result[0], result[1])
                result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
                # The backup system in RHEL is very sensitive and we do not want to
                # fail the test case due to not creating the backup at this stage. There
                # is a work-around in the comsa_lib.restoreSystem for RHEL systems if the
                # backup does not exist
                if self.linuxDistro != self.distroTypes[1]:
                    self.fail(result[0], result[1])


            # Some tests can not be run on a single-node cluster, so detect and skip
            tcSingleNodeCompatible = False

            if (self.testcase_tag != 'TC-BFU-003' and
                self.testcase_tag != 'TC-BFUCL5-001' and
                self.testcase_tag != 'TC-BFUCL5-002' and
                self.testcase_tag != 'TC-BFUCL5-003'):

                tcSingleNodeCompatible = True

            noOfScs = len(self.testConfig['controllers'])
            if noOfScs == 1 and tcSingleNodeCompatible == False:
                # skip the test
                self.logger.info('Skipped test because it can not be run on a single-node cluster')
                self.setAdditionalResultInfo('Test skipped; can not be run on a single node cluster')
                self.skip_test = True

            else:
                #########################################################################################################
                #
                # For TC-BFU-009 we need to install COM SA 3.1 as the old COM SA before upgrading to the latest
                # But this old COM SA can not be used together with CoreMW 3.4 - it will cause coredump. So, in
                # the preparation for this specific TC we need to install an older CoreMW, too - the latest CoreMW 3.2 CP
                #
                # For TC-BFUCL5-xxx we need to install CoreMW 3.2 PRA and COM 3.2 PRA.
                #

                # Check if the required versions of CoreMW and COM for the BFU CL5 tests are already installed in
                # the system and skip the installation
                self.setTestStep('Check if the required versions of CoreMW and COM for BFU CL5 tests are installed')
                BfuCL5_ComOK = self.lib.checkExactComponentVersion('com', self.BfuCL5_reqComRelease, self.BfuCL5_reqComVersion)
                BfuCL5_CmwOK = self.lib.checkExactComponentVersion('cmw', self.BfuCL5_reqCmwRelease, self.BfuCL5_reqCmwVersion)
                self.myLogger.info("self.removeCoreMW: %s"%str(self.removeCoreMW))
                self.myLogger.info("BfuCL5_ComOK[1]: %s"%str(BfuCL5_ComOK[1]))
                self.myLogger.info("BfuCL5_CmwOK[1]: %s"%str(BfuCL5_CmwOK[1]))

                if self.removeCoreMW == True and (BfuCL5_ComOK[1] == False or BfuCL5_CmwOK[1] == False):
                    if not self.restoreSnapshot:
                        # 1.Create Backup and Copy backup files to stored location

                        self.setTestStep('======== Backup system ========')
                        self.backupCluster(self.backupName9)

                        # 2.Copy backup files to stored location
                        self.setTestStep('======== Copy backup files to stored location =========')

                        result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
                        self.fail(result[0], result[1])

                        result = self.sshLib.sendCommand('mkdir %s' %self.storedBackupFilesLocation)
                        self.fail(result[0], result[1])

                        command = '\cp %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.backupName9, self.storedBackupFilesLocation, self.backupName9)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.backupName9, self.storedBackupFilesLocation, self.backupName9)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.backupName9, self.storedBackupFilesLocation, self.backupName9)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.lotcBackupLocation, self.backupName9, self.storedBackupFilesLocation)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        # Going to uninstall cluster, we lose all our backups except for one
                        self.backupName = self.backupName9

                        # 3.Uninstall system

                        self.setTestStep('======== Uninstall system ========')

                        result = self.sshLib.sendCommand('mkdir %s' %self.bfuLocation)
                        self.fail(result[0],result[1])

                        result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                        self.fail(result[0], result[1])

                        result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                        self.fail(result[0], result[1])

                        # result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                        # self.fail(result[0], result[1])

                        # copy the unistall script to the cluster

                        result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName1), self.bfuLocation, timeout = 120)
                        self.fail(result[0], result[1])

                        result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName2), self.bfuLocation, timeout = 120)
                        self.fail(result[0],result[1])

                        result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.bfuLocation)
                        self.fail(result[0], result[1])

                    # run Uninstall
                    result = self.comsa_lib.unInstallSystem(self.bfuLocation, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
                    self.fail(result[0], result[1])

                    if not self.restoreSnapshot:
                        cmw_uninstall_command2 = '%s%s' %(self.bfuLocation, self.uninstallScriptName2)
                        result = self.sshLib.sendCommand (cmw_uninstall_command2)
                        self.fail(result[0], result[1])

                    self.lib.resetDumps()

                    # 4.Install the system with the 'old' COM SA

                    # Install CoreMW
                    self.setTestStep('======== Install CoreMW ========')
                    if self.restoreSnapshot:
                        result = self.sshLib.sendCommand('mkdir %s' %self.bfuLocation)
                        self.fail(result[0],result[1])

                        result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                        self.fail(result[0], result[1])

                        result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                        self.fail(result[0], result[1])

                    if (self.testcase_tag == 'TC-BFUCL5-001' or
                        self.testcase_tag == 'TC-BFUCL5-002' or
                        self.testcase_tag == 'TC-BFUCL5-003' or
                        self.testcase_tag == 'TC-BFUCL5-004' or
                        self.testcase_tag == 'TC-BFUCL5-005' or
                        self.testcase_tag == 'TC-BFUCL5-006' or
                        self.testcase_tag == 'TC-BFUCL5-007' or
                        self.testcase_tag == 'TC-BFUCL5-008' or
                        self.testcase_tag == 'TC-BFUCL5-009' or
                        self.testcase_tag == 'TC-BFUCL5-010' or
                        self.testcase_tag == 'TC-BFUCL5-011' or
                        self.testcase_tag == 'TC-BFUCL5-012'):

                        self.CoreMWSdp = self.CMW_Sdp_for_BFUCL5
                        result = self.sshLib.remoteCopy('%s' %(self.CMW_for_BFUCL5), self.pathToCmwInstallation, timeout = 120)
                        self.fail(result[0],result[1])
                    else:
                        result = self.sshLib.remoteCopy('%s/%s' %(self.CoreMW, self.CoreMWSdp), self.pathToCmwInstallation, timeout = 120)
                        self.fail(result[0],result[1])

                    result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp, backupRpms = self.backupRpmScript)
                    self.fail(result[0], result[1])

                    # Install COM
                    self.setTestStep('======== Install COM ========')

                    if (self.testcase_tag == 'TC-BFUCL5-001' or
                        self.testcase_tag == 'TC-BFUCL5-002' or
                        self.testcase_tag == 'TC-BFUCL5-003' or
                        self.testcase_tag == 'TC-BFUCL5-004' or
                        self.testcase_tag == 'TC-BFUCL5-005' or
                        self.testcase_tag == 'TC-BFUCL5-006' or
                        self.testcase_tag == 'TC-BFUCL5-007' or
                        self.testcase_tag == 'TC-BFUCL5-008' or
                        self.testcase_tag == 'TC-BFUCL5-009' or
                        self.testcase_tag == 'TC-BFUCL5-010' or
                        self.testcase_tag == 'TC-BFUCL5-011' or
                        self.testcase_tag == 'TC-BFUCL5-012'):

                        self.installCOM(self.COM_for_BFUCL5, self.pathToComInstallation)
                        self.fail(result[0], result[1])
                    else:
                        self.installCOM(self.COM_latest, self.pathToComInstallation)
                        self.fail(result[0], result[1])

                    if self.installStressTool:
                        self.bfuSetupStress()
                        stressTimeOut = 60
                        self.sshLib.setTimeout(stressTimeOut)

                    # Install COMSA
                    self.setTestStep('======== Install "old" COM SA ========')

                    self.setTestStep('Install "old" COMSA')

                    # Check COMSA deployment SDP under the given path
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

                else:

                    # Restore partial backup of COM
                    # If we define a backup name in the tc_....xml file, that backup will be restored.
                    # If not, we search for the latest com backup. We do this by listing the backups in order of creation. We search for backup names that contain com, but not comsa.
                    # If no backup is found, we use the default backup name for com, which is "com"
                    # The method is not bullet proof, but should find the suitable COM backup most of the times.
                    backupName = ''

                    if self.com_backup_name != '':
                        backupName = self.com_backup_name
                    else:
                        cmd = """cmw-partial-backup-list 2>&1 | sed 's/\[//g' | sed 's/\]//g' | grep -i com | egrep -iv '(comsa)|(com_sa)|(com-sa)' | tail -1 | awk '{print $NF}' """

                        # We search for the latest COM backup
                        result = self.sshLib.sendCommand(cmd)
                        self.fail(result[0], result[1])
                        if 'Usage: grep [OPTION]' in result[1] or result[1] == '':
                            backupName = self.default_com_backup_name
                        else:
                            backupName = result[1]

                        if backupName == '':
                            if self.linuxDistro != self.distroTypes[1]:
                                self.fail('ERROR', 'COM backup not found!')
                            elif self.linuxDistro == self.distroTypes[1]:
                                # For RHEL systems we try to reinstall COM instead of restoring a COM backup
                                backupName == 'com_autobackup'

                        self.setTestStep('Restore partial backup of COM')
                        self.myLogger.debug('Restore partial backup of COM: %s' %backupName)
                        result = self.safLib.isBackup(backupName)
                        self.fail(result[0], result[1])

                        if result == ('SUCCESS','NOT EXIST'):
                            if self.linuxDistro != self.distroTypes[1]:
                                self.fail('ERROR', 'Com backup not found. Nothing to restore, test case is aborted')

                        self.restoreBackup(backupName)

                    if self.installStressTool:
                        self.bfuSetupStress()
                        stressTimeOut = 60
                        self.sshLib.setTimeout(stressTimeOut)

                    ###########################################################################
                    # Install "old" COMSA
                    ###########################################################################

                    self.setTestStep('Install "old" COMSA')

                    # Check COMSA deployment SDP under the given path
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


                    # Remove old backup of COMSA
                    backupName = time.strftime("COMSA_BACKUP_%Y%m%d_%H%M%S",time.localtime())
                    self.setTestStep('Remove old backup: %s' %backupName)
                    self.myLogger.debug('Remove old backup of COMSA: %s' %backupName)
                    result = self.safLib.isBackup(backupName)
                    self.fail(result[0], result[1])
                    if result == ('SUCCESS','EXIST'):
                        result = self.safLib.backupRemove(backupName)
                        self.fail(result[0], result[1])

                    # Create a backup of COMSA
                    self.setTestStep('Create backup: %s' %backupName)
                    self.myLogger.debug('Create a backup of COMSA: %s' %backupName)
                    result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)

                    # Check CMW status, and wait for status ok
                    self.setTestStep('Check CMW status after creating old COMSA backup')
                    result = self.comsa_lib.waitForClusterStatusOk()
                    self.fail(result[0], result[1])

                    result = self.lib.getComponentVersion(self.comsaCxpNumber)
                    self.fail(result[0], result[1])
                    self.setAdditionalResultInfo('Upgraded COM SA from Release: %s, Version: %s' %(result[1], result[2]))

                ###########################################################################
                # Upgrade to the current COMSA
                ###########################################################################

                dict = self.comsa_lib.getGlobalConfig(self)
                self.bfu_bundle_name = dict.get('CXP_SDP_NAME_OFFICIAL')
                self.setTestStep('Build the current COMSA')
                self.logger.info('buildAndStoreCOMSA Called ')
                BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
                if BuildPath[0] != 'SUCCESS':
                    self.logger.error(result[1])
                    self.logger.debug('Build COMSA failed : Exit')
                    return (BuildPath[0], 'Build COM SA failed')

                # create directory on the target to copy the BFU archive files
                cmd = 'rm -f %s/*' %(self.temp_dir)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])
                cmd = 'mkdir -p %s' %(self.temp_bfu)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

                # copy the BFU archives to the target.
                self.myLogger.debug('Copying the BFU archive files to the target')
                # BuildPath[9] is the file name with absolute path of Template tar file
                # BuildPath[10] is the file name with absolute path of Runtime tar file
                result = self.comsa_lib.copyFilesToTarget(['%s/' %BuildPath[9], '%s/' %BuildPath[10]], self.temp_bfu, False)
                self.fail(result[0], result[1])

                self.setTestStep('Unpack the COMSA installation archives on the target')
                self.myLogger.debug('Unpacking the BFU archives on the target')
                cmd = 'cd %s ; tar xf %s' %(self.temp_bfu, BuildPath[5])
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])
                cmd = 'cd %s ; tar xf %s' %(self.temp_bfu, BuildPath[4])
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

                self.setTestStep('Import the COMSA BFU campaign and bundle SDPs to CoreMW repository')
                self.myLogger.debug('Importing the COMSA BFU campaign and bundle SDPs to CoreMW repository')

                bfuBundleSdp = '%s%s' %(self.temp_bfu, self.bfu_bundle_name)

                # copy to /home/coremw/incoming because importSwBundle() uses this dir !
                cmd = '\cp -f %s %s' %(bfuBundleSdp, self.temp_dir)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])

                if self.upgradeType == "bfu" or self.upgradeType == "bfucl5":

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

                elif self.upgradeType == "u2":

                    # find the name of the U2 directory
                    if noOfScs == 2:
                        result = self.sshLib.sendCommand('cd %s; ls | grep COM_SA_U2' %self.temp_bfu)
                        self.fail(result[0], result[1])
                    else:
                        result = self.sshLib.sendCommand('cd %s; ls | grep COM_SA_U3' %self.temp_bfu)
                        self.fail(result[0], result[1])
                    upgradeDir = result[1]

                    # generate the U2 campaign
                    result = self.sshLib.sendCommand('cd %s/%s; ./comsa-generate*' %(self.temp_bfu, upgradeDir))
                    self.fail(result[0], result[1])
                    expectedResponsePart = 'successfully generated campaign sdp'
                    if expectedResponsePart not in result[1]:
                        self.fail('ERROR', 'The following text was expected, but not received in the response of the command: %s' %expectedResponsePart)

                    # find the name of the upgrade campaign sdp
                    for line in result[1].splitlines():
                        if expectedResponsePart in line:
                            upgradeCampaignSdp = line.split(":")[1].strip()

                    # copy the upgrade campaign to /home/coremw/incoming
                    result = self.sshLib.sendCommand('\cp %s/%s/%s %s' %(self.temp_bfu, upgradeDir, upgradeCampaignSdp, self.temp_dir))
                    self.fail(result[0], result[1])

                # Run the upgrade campaign

                self.setTestStep('Run the COMSA upgrade campaign')
                self.myLogger.debug('Run the COMSA upgrade campaign')

                result = self.comsa_lib.installComp(self.temp_dir, self.bfu_bundle_name, upgradeCampaignSdp, 'comsa', createBackup = False, backupRpms = self.backupRpmScript)
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

                # TR HS79484: Some old versions of COM SA may cause coredump in PMT SA destructor when stopping COM after the upgrade.
                # PRA releases can not be corrected and therefore coredumps must be ignored.
                # Corrections are being prepared for some CP releases for this TR but not available yet.
                # Some lines can be removed later in the if statement below when 3.2 CP9, 3.3CP8, 3.4CP2 are released and used in these FT tests
                if (self.testcase_tag == 'TC-BFUCL5-001' or
                    self.testcase_tag == 'TC-BFUCL5-002' or
                    self.testcase_tag == 'TC-BFUCL5-003' or
                    self.testcase_tag == 'TC-BFUCL5-004' or
                    self.testcase_tag == 'TC-BFUCL5-005' or
                    self.testcase_tag == 'TC-BFUCL5-006' or
                    self.testcase_tag == 'TC-BFUCL5-007' or
                    self.testcase_tag == 'TC-BFUCL5-008' or
                    self.testcase_tag == 'TC-BFUCL5-009' or
                    self.testcase_tag == 'TC-BFUCL5-010'):

                    # Ignoring any coredumps caused by the upgrade when the OLD COM sa was stopped
                    # If there was a coredump during the upgrade caused by the newly installed COM SA then it will
                    # be detected by comsa_lib.installComp() so we are not hiding any failure of this kind here.
                    self.lib.resetDumps()

                # Cleanup
                self.setTestStep('Removing all existing installation campaigns')
                self.myLogger.debug('Removing all existing installation campaigns')
                result = self.safLib.getImportedCampaigns()
                if result[0] == 'SUCCESS' and result[1] != '':
                    campaigns = result[1].split('\n')
                    for campaign in campaigns:
                        self.safLib.removeSwBundle(campaign)
                        while None != re.search('SA_AIS_ERR_TRY_AGAIN', result[1]):
                            self.miscLib.waitTime(2)
                            result=self.safLib.removeSwBundle(campaign)

                if self.removeCoreMW and (BfuCL5_ComOK[1] == False or BfuCL5_CmwOK[1] == False):
                    if not self.restoreSnapshot:
                        # Restore the system to the original state it was in before running the test
                        self.setTestStep('======== Restore system ========')
                        #recopy the backup files
                        command = '\cp %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName9, self.comsaBackupLocation, self.backupName9)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        command = '\cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName9, self.comBackupLocation, self.backupName9)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName9, self.cmwBackupLocation, self.backupName9)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupName9, self.lotcBackupLocation)
                        result = self.sshLib.sendCommand (command)
                        self.fail(result[0], result[1])

                        result = self.comsa_lib.restoreSystem(self, self.backupName9, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                        self.fail(result[0],result[1])

                coreTestCase.CoreTestCase.runTest(self)
        else:
            self.logger.info('Skipped BFU tests because of COMSA/COM/CMW version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True


    def tearDown(self):
        self.logger.debug('enter tearDown')
        self.setTestStep('tearDown')

        #Removing check coredump for testcase BFUCL5-006 and 007
        if self.testcase_tag == 'TC-BFUCL5-006' or self.testcase_tag == 'TC-BFUCL5-007':
            self.lib.resetDumps()

        self.logger.info('self.failureFlag value: %s' %str(self.failureFlag))
        if self.skip_test == False or self.failureFlag == True:
            cmd = '\\rm -rf %s %s' %(self.temp_dir, self.temp_bfu)
            self.logger.debug('Removing the temp directories by: %s' %cmd)
            result = self.sshLib.sendCommand(cmd)
            self.restoreBackup(self.backupName, insatallationLevel = 3)

        coreTestCase.CoreTestCase.tearDown(self)
        self.logger.debug('leave tearDown')


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


    def restoreBackup(self, backupName, insatallationLevel = 2):
        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)


        self.setTestStep('Restore backup: %s' %backupName)
        result = self.comsa_lib.restoreSystem(self, backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = insatallationLevel, removeBackup = False)
        self.fail(result[0], result[1])


    ########################################################################################
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

    ########################################################################################
    def bfuSetupStress(self):
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

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
