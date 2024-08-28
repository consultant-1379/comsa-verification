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
   Prepare the cluster for mr-20275/MR-28515 backward compatibility testing (install the required CoreMW version). Restore at the end of testing.

   Description:
   Create a backup and store it. Install the required CoreMw for backward compatibility testing. Restore at the end of the testing.

   Priority:
   Not applicable

   Precondition:
   At least one controller must be up and running with LOTC

   Actions:

   -----------------------------
   TC-MR20275BKWCMISC-001:
   Prepare the cluster for MR-20275 backward comp testing (uninstall CoreMW, then install the required CoreMW)

   1. Create Cluster Backup

   2. Copy the backup files to stored location

   3. Uninstall CoreMw

   4. Reboot the cluster

   5. Run the uninstall script again

   6. Install the requested CoreMW version

   7. Install the requested COM version

   -----------------------------
   TC-MR20275BKWCMISC-002:
   Restore the system to the original state it was in before running the backward compatibility tests

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

class SetupForMr20275Bkwc(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.testcase_tag = tag

        # parameters from the config files
        self.MR20275BkwC_reqCmwRelease = {} # "1"
        self.MR20275BkwC_reqCmwVersion = {} # "R8A19"    # CoreMW 3.4 PRA
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']

        # defautle is the lowest version
        self.reqComSaVersion = "R1A01"
        self.reqComVersion = "R1A01"
        self.reqCmwVersion = "R1A01"
        self.reqComSaRelease = "3"
        self.reqComRelease = "2"
        self.reqCmwRelease = "1"

        self.backupNameMR20275 = "MR20275BkwCBackup"
        self.storedBackupFilesLocation = {}
        self.comsaBackupLocation = {}
        self.lotcBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}
        self.rpmBackupLocation = "/home/backup_rpms"


    def id(self):
        return "Prepare the cluster for COMSA MR20275 BkwC testing"


    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.resourceFilesLocation = dict.get("PATH_TO_MR20275")
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        self.swDir = System.getProperty("swDirNumber")
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        self.sdpImportCommand = 'cmw-sdp-import'
        self.campaignComsaInstallName ='ERIC-ComSaInstall'
        self.serviceInstanceName = 'ComSa'
        self.amfNodePattern = 'Cmw'

        self.cxpArchive = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.absDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.deplTemplArchive = dict.get('COM_SA_DEPL_TEMPL_ARCHIVE_RHEL')
            self.bundleArchive = dict.get('COM_SA_BUNDLE_ARCHIVE_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.deplTemplArchive = dict.get('COM_SA_DEPL_TEMPL_ARCHIVE')
            self.bundleArchive = dict.get('COM_SA_BUNDLE_ARCHIVE')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)

        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')
        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        self.mr20275Location = '/home/mr20275bkwc/'

        self.pathToCmwInstallation = '%s/coremw/' %self.mr20275Location
        self.pathToComInstallation = '%s/com/' %self.mr20275Location
        self.pathToComsaInstallation = '%s/comsa/' %self.mr20275Location


        self.pathToCom = "%s%s/com" %(self.installRoot, self.swDir)
        self.pathToComsa = "%s%s/comsa" %(self.installRoot, self.swDir)

        self.COMBuildPath = "%s/com"%self.resourceFilesLocation
        self.ComSABuildPath = "%s/comsa"%self.resourceFilesLocation
        self.CMW_Sdp_for_MR20275BkwC = "coremw_x86_64-3.4_CP11-runtime_CXP9020355_1_R8M.tar"
        self.CMW_for_MR20275BkwC = "%scoremw3.4cp11/%s" %(self.resourceFilesLocation, self.CMW_Sdp_for_MR20275BkwC)

        self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        #self.super__setUp()
        self.currentTestCase = self

    def runTest(self):
        ''' Prepare the cluster for COM SA MR-20275 BkwC testing
        '''

        self.skip_test = False

        self.temp_dir = '/home/coremw/incoming/'
        self.temp_mr2075 = '/home/mr20275bkwc/'

        Mr20275_BkwC_CmwOK = self.lib.checkExactComponentVersion('cmw', self.MR20275BkwC_reqCmwRelease, self.MR20275BkwC_reqCmwVersion )

        # add to check version
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
        self.fail(ComsaOK[0],ComsaOK[1])

        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion)
        self.fail(ComsaOK[0],ComsaOK[1])

        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion)
        self.fail(ComsaOK[0],ComsaOK[1])

        if (self.testcase_tag == 'TC-MR20275BKWCMISC-001') and (Mr20275_BkwC_CmwOK[1] == False or (Mr20275_BkwC_CmwOK[0] != 'SUCCESS' and self.restoreSnapshot)) and ComsaOK[1] and ComOK[1] and CmwOK[1]:

            # Need to uninstall and re-install with CoreMW 3.4 PRA to test backward compatibility for MR-20275
            self.setTestStep('runTest')

            # Variables needed for the build token management
            dirName = System.getProperty("logdir")
            user = os.environ['USER']
            self.tokenPattern = 'buildToken-%s' %user
            self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
            self.numberOfGetTokenRetries = 5
            if not self.restoreSnapshot:
                # 1. Create Cluster Backup

                self.setTestStep('======== Backup system ========')
                self.backupCluster(self.backupNameMR20275)

                # 2. Copy the cluster backup files to stored location
                self.setTestStep('======== Copy the backup files to the stored location =========')

                result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.storedBackupFilesLocation)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.backupNameMR20275, self.storedBackupFilesLocation, self.backupNameMR20275)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.backupNameMR20275, self.storedBackupFilesLocation, self.backupNameMR20275)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.backupNameMR20275, self.storedBackupFilesLocation, self.backupNameMR20275)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                if self.linuxDistro != "RhelType":
                    command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.lotcBackupLocation, self.backupNameMR20275, self.storedBackupFilesLocation)
                else:
                    command = '\mv %s/rpms_%s.tar.gz %s' %(self.rpmBackupLocation, self.backupNameMR20275, self.storedBackupFilesLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                # 3. Uninstall the CoreMW in the system

                self.setTestStep('======== Uninstall CoreMW  ========')

                result = self.sshLib.sendCommand('mkdir %s' %self.mr20275Location)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName1), self.mr20275Location, timeout = 120)
                self.fail(result[0], result[1])

                result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName2), self.mr20275Location, timeout = 120)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.mr20275Location)
                self.fail(result[0], result[1])

            # run Uninstall
            result = self.comsa_lib.unInstallSystem(self.mr20275Location, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
            self.fail(result[0], result[1])

            if not self.restoreSnapshot:
                cmw_uninstall_command2 = '%s%s' %(self.mr20275Location, self.uninstallScriptName2)
                result = self.sshLib.sendCommand (cmw_uninstall_command2)
                self.fail(result[0], result[1])

            # Remove any core dumps caused by the uninstallation process
            self.lib.resetDumps()

            # 4. Install the requested CoreMW
            self.setTestStep('======== Install CoreMW ========')
            if self.restoreSnapshot:
                result = self.sshLib.sendCommand('mkdir %s' %self.mr20275Location)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                self.fail(result[0], result[1])


            self.CoreMWSdp = self.CMW_Sdp_for_MR20275BkwC
            result = self.sshLib.remoteCopy('%s' %(self.CMW_for_MR20275BkwC), self.pathToCmwInstallation, timeout = 120)
            self.fail(result[0],result[1])

            result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp, backupRpms = self.backupRpmScript)
            self.fail(result[0], result[1])

            # 5. Install the requested COM
            self.setTestStep('======== Install COM ========')

            self.installCOM(self.pathToCom, self.pathToComInstallation)
            self.fail(result[0], result[1])

            #Install COMSA
            self.setTestStep('======== Install COM SA ========')
            self.installCOMSAFromStream(self.pathToComsaInstallation)

            # TBD- Check for Transaction SPI v1 being registered by reading syslog.
            # Need to check the latest entry only using timestamp method.
            self.setTestStep('======== Check syslogs for Transaction SPI v1 registered for backward comp ========')

            self.myLogger.debug('Resetting the timer')
            cmd = 'date +\%s'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            currTime = int(result[1])
            # Start to Calculate when install cmw3.4
            startTime = currTime - 517
            self.myLogger.debug("Result of first time:%s"%startTime)

            self.logger.info('Verify that COM starts up without problems')
            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            self.activeController = result[1]

            self.myLogger.info('Grepping on Active SC: ###Exporting TransactionalResource SPI v1')
            searchPatterns = ['###Exporting TransactionalResource SPI v1']
            result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1],searchPatterns, startTime, self.testConfig, logDir = '/var/log/')
            self.fail(result[0], result[1])

        elif self.testcase_tag == 'TC-MR20275BKWCMISC-002' and ComsaOK[1] and ComOK[1] and CmwOK[1]:
            if not self.restoreSnapshot:
                # Restore the system to the original state it was in before running the test
                self.setTestStep('======== Restore the system to the original CoreMW and COM ========')
                #recopy the backup files
                command = '\mv %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupNameMR20275, self.comsaBackupLocation, self.backupNameMR20275)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupNameMR20275, self.comBackupLocation, self.backupNameMR20275)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupNameMR20275, self.cmwBackupLocation, self.backupNameMR20275)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                if self.linuxDistro != "RhelType":
                    command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupNameMR20275, self.lotcBackupLocation)
                else:
                    command = '\mv %s/rpms_%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupNameMR20275, self.rpmBackupLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                result = self.comsa_lib.restoreSystem(self, self.backupNameMR20275, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                self.fail(result[0],result[1])

            coreTestCase.CoreTestCase.runTest(self)

        else:
            if ComsaOK[1] == False:
                self.logger.info('Skipped tests because of COMSA version not compatible!')
                self.setAdditionalResultInfo('Test skipped, COMSA version not compatible')
            if ComOK[1] == False:
                self.logger.info('Skipped tests because of COM version not compatible!')
                self.setAdditionalResultInfo('Test skipped, COM version not compatible')
            if CmwOK[1] == False:
                self.logger.info('Skipped tests because of CMW version not compatible!')
                self.setAdditionalResultInfo('Test skipped, CMW version not compatible')
            else:
                self.logger.info('Expecting TC-MR20275BKWCMISC-00x but %s was given instead' %(self.testcase_tag))
                self.setAdditionalResultInfo('Test skipped. Expecting TC-MR20275BKWCMISC-00x but %s was given instead' %(self.testcase_tag))
            self.skip_test = True

    def installCOMSAFromStream(self, pathToComsaInstallation):
        self.logger.info('installCOMSAFromStream: Called')

        result = self.sshLib.sendCommand('\\rm -rf %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Use function from library comsa_lib
        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)

        # BuildPath[10] is the file name with absolute path of Runtime tar file
        if BuildPath[10] != '':
            result = self.sshLib.remoteCopy(BuildPath[10], self.pathToComsaInstallation, timeout = 120)
            self.fail(result[0],result[1])
        else:
            self.logger.info('installCOMSAFromStream: The absolute filename of Runtime tar file is empty')

        # BuildPath[9] is the file name with absolute path of Runtime tar file
        if BuildPath[9] != '':
            result = self.sshLib.remoteCopy(BuildPath[9], self.pathToComsaInstallation, timeout = 120)
            self.fail(result[0],result[1])
        else:
            self.logger.info('installCOMSAFromStream: The absolute filename of Template tar file is empty')

        # Untar some files
        result = self.sshLib.sendCommand('tar xvf %s/COM_SA_RUNTIME*.tar -C %s' %(self.pathToComsaInstallation, self.pathToComsaInstallation)) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('tar xvf %s/COM_SA_D_TEMPLATE*.tar.gz -C %s' %(self.pathToComsaInstallation, self.pathToComsaInstallation)) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Import SDP package

        self.logger.info ('installCOMSAFromStream: Importing ComSa SDP')
        fileName = self.getAbsoluteFileNameCluster('ls -d %s/*.sdp' %(self.pathToComsaInstallation), self.pathToComsaInstallation)

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

        fileName = self.getAbsoluteFileNameCluster(cmd, self.pathToComsaInstallation)
        cmd = '%s %s' %(self.sdpImportCommand, fileName)
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


    def tearDown(self):
        self.logger.debug('enter tearDown')
        self.setTestStep('tearDown')

        if (self.testcase_tag == 'TC-MR20275BKWCMISC-002'):
            if self.skip_test == False:
                cmd = '\\rm -rf %s %s' %(self.temp_dir, self.temp_mr2075)
                self.logger.debug('Removing the temp directories by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd)
                self.restoreBackup(self.backupNameMR20275)

        coreTestCase.CoreTestCase.tearDown(self)
        self.logger.debug('leave tearDown')


    def restoreBackup(self, backupName):

        self.setTestStep('Restore backup: %s' %backupName)
        result = self.comsa_lib.restoreSystem(self, backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
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


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
