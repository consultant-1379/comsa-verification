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
   Prepare the cluster for BFU CL5 testing (install the required CoreMW and COM versions). Restore at the end of testing.

   Description:
   Create a backup and store it. Install the required CoreMw and COM for BFU CL5 testing. Restore at the end of the testing.

   Priority:
   Not applicable

   Precondition:
   At least one controller must be up and running with LOTC

   Actions:

   -----------------------------
   TC-BFUCL5-MISC-001:
   Prepare the cluster for BFU CL5 testing (uninstall CoreMW, then install the required CoreMW and COM versions)

   1. Create Cluster Backup

   2. Copy the backup files to stored location

   3. Uninstall CoreMw

   4. Reboot the cluster

   5. Run the uninstall script again

   6. Install the requested CoreMW version

   7. Install the requested COM version

   -----------------------------
   TC-BFUCL5-MISC-002:
   Restore the system to the original state it was in before running the BFU tests

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

class SetupForBfuCL5(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.testcase_tag = tag

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        # parameters from the config files
        self.BfuCL5_reqCmwRelease = {} # "1"
        self.BfuCL5_reqCmwVersion = {} # "P1A99"    # CoreMW 3.2 latest
        self.BfuCL5_reqComRelease = {} # "2"
        self.BfuCL5_reqComVersion = {} # "R7A08"    # COM 3.2 PRA

        self.backupName = "bfuBackup"
        self.backupNameCl5 = "bfuCl5Backup"
        self.storedBackupFilesLocation = {}
        self.comsaBackupLocation = {}
        self.lotcBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}
        self.rpmBackupLocation = "/home/backup_rpms"


    def id(self):
        return "Prepare the cluster for COMSA BFU CL5 testing"


    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        dict = self.comsa_lib.getGlobalConfig(self)
        self.resourceFilesLocation = dict.get("PATH_TO_BFU")
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        self.swDir = System.getProperty("swDirNumber")
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')
        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        self.bfuLocation = '/home/bfu/'

        self.pathToCmwInstallation = '%s/coremw/' %self.bfuLocation
        self.pathToComInstallation = '%s/com/' %self.bfuLocation

        #Temporary fix using coremw3.2 latest blackbuild to work with COMSA3.6. There is no plan to deliver new CP CMW package yet
        self.CMW_Sdp_for_BFUCL5 = "COREMW_RUNTIME-CXP9020355_1.tar"
        self.CMW_for_BFUCL5 = "%scoremw3.2_latest/%s" %(self.resourceFilesLocation, self.CMW_Sdp_for_BFUCL5)
        self.COM_for_BFUCL5 = "%s/com3.2_latest" %self.resourceFilesLocation

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
        coreTestCase.CoreTestCase.setUp(self)
        self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        #self.super__setUp()
        self.currentTestCase = self

    def runTest(self):
        ''' Prepare the cluster for COM SA BFU CL5 testing
        '''

        self.skip_test = False

        self.temp_dir = '/home/coremw/incoming/'
        self.temp_bfu = '/home/bfu/'

        if self.testcase_tag == 'TC-BFUCL5MISC-001':

            self.setTestStep('runTest')

            #
            # For TC-BFUCL5-xxx we need to install CoreMW 3.2 PRA and COM 3.2 PRA.
            #

            '''
            This is not implemented yet - left for future improvements if ever needed

            # Check if the required versions of CoreMW and COM for the BFU CL5 tests are already installed in
            # the system and skip the installation
            self.setTestStep('Check if the required versions of CoreMW and COM for BFU CL5 tests are installed')
            BfuCL5_CmwOK = self.lib.checkExactComponentVersion('cmw', self.BfuCL5_reqCmwRelease, self.BfuCL5_reqCmwVersion )
            BfuCL5_ComOK = self.lib.checkExactComponentVersion('com', self.BfuCL5_reqComRelease, self.BfuCL5_reqComVersion )

            if BfuCL5_ComOK[1] == False or BfuCL5_CmwOK[1] == False:
            '''

            # 1. Create Cluster Backup
            if not self.restoreSnapshot:
                self.setTestStep('======== Backup system ========')
                self.backupCluster(self.backupNameCl5)

                # 2. Copy the cluster backup files to stored location
                self.setTestStep('======== Copy the backup files to the stored location =========')

                result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.storedBackupFilesLocation)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.backupNameCl5, self.storedBackupFilesLocation, self.backupNameCl5)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.backupNameCl5, self.storedBackupFilesLocation, self.backupNameCl5)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.backupNameCl5, self.storedBackupFilesLocation, self.backupNameCl5)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                if self.linuxDistro != "RhelType":
                    command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.lotcBackupLocation, self.backupNameCl5, self.storedBackupFilesLocation)
                else:
                    command = '\mv %s/rpms_%s.tar.gz %s' %(self.rpmBackupLocation, self.backupNameCl5, self.storedBackupFilesLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                # 3. Uninstall the CoreMW in the system

                self.setTestStep('======== Uninstall CoreMW  ========')

                result = self.sshLib.sendCommand('mkdir %s' %self.bfuLocation)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

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

            # Remove any core dumps caused by the uninstallation process
            self.lib.resetDumps()

            # 4. Install the requested CoreMW
            self.setTestStep('======== Install CoreMW ========')

            if self.restoreSnapshot:
                result = self.sshLib.sendCommand('mkdir %s' %self.bfuLocation)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

            self.CoreMWSdp = self.CMW_Sdp_for_BFUCL5
            result = self.sshLib.remoteCopy('%s' %(self.CMW_for_BFUCL5), self.pathToCmwInstallation, timeout = 120)
            self.fail(result[0],result[1])

            result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp, backupRpms = self.backupRpmScript)
            self.fail(result[0], result[1])

            # 5. Install the requested COM
            self.setTestStep('======== Install COM ========')

            self.installCOM(self.COM_for_BFUCL5, self.pathToComInstallation)
            self.fail(result[0], result[1])

            '''
            This is not implemented yet - left for future improvements if ever needed
            See the commented out beginning of the 'if' statement above

            else:
                # Need to set some flag that the system was already prepared as needed to be used by the 'Restore System' test case to skip the restoration
                #
                #  ##############    T B D    ##################
                #
                self.logger.info('Need to set some TBD flag to be used by the restore TC-BFUCL5-MISC-002 !!!!!!!')
            '''

        elif self.testcase_tag == 'TC-BFUCL5MISC-002':
            if not self.restoreSnapshot:

                # Restore the system to the original state it was in before running the test
                self.setTestStep('======== Restore the system to the original CoreMW and COM ========')
                #recopy the backup files
                command = '\mv %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupNameCl5, self.comsaBackupLocation, self.backupNameCl5)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupNameCl5, self.comBackupLocation, self.backupNameCl5)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\mv %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupNameCl5, self.cmwBackupLocation, self.backupNameCl5)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                if self.linuxDistro != "RhelType":
                    command = '\mv %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupNameCl5, self.lotcBackupLocation)
                else:
                    command = '\mv %s/rpms_%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupNameCl5, self.rpmBackupLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

            # On a RHEL system if the backup is not found, than installation procedures are used
            # to get to the desired installation level
            result = self.comsa_lib.restoreSystem(self, self.backupNameCl5, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
            self.fail(result[0],result[1])

            coreTestCase.CoreTestCase.runTest(self)

        else:
            self.logger.info('Expecting TC-BFUCL5MISC-00x but %s was given instead' %(self.testcase_tag))
            self.setAdditionalResultInfo('Test skipped.')
            self.skip_test = True


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

        coreTestCase.CoreTestCase.tearDown(self)
        self.logger.debug('leave tearDown')


    def restoreBackup(self, backupName, insatallationLevel = 3):

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

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
