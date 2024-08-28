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
   reinstall COM-SA on target

   Description:
   This script reinstalls COM-SA. (restoring COM backup, rebooting the cluster and installing COM-SA)

   Priority:
   Not applicable

   Precondition:
   At least two controllers must be up and running with LOTC, CMW, (COM-EA), COM with "com" backup.

   Action:

   1. Restore partial backup of COM

   2. Check CMW status, and wait for status ok

   3. Reboot the cluster

   4. Wait until controller 1 is up

   5. Check and wait until all tipc links are up

   6. Wait for CMW status ok

   7. Install COMSA

       # Upload COMSA runtime SDP and COMSA deployment template SDP to target

       # Import all SDPs to repository

       # Start COMSA installation

       # Check and wait until the installation finishes

       # Wait for CMW status ok

       # Commit the installation

       # Check if the installation is commited

       # Wait for CMW status ok

   8. Remove old COM-SA backup

   9. Create COM-SA backup

  10. Wait for CMW status ok

  11. Removing all existing installation campaigns


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

class ReInstallCOMSA(coreTestCase.CoreTestCase):


    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        # parameters from the config files
        self.com_backup_name = ''
        self.default_com_backup_name = 'com'
        self.coverageEnabled = False
    def id(self):
        return "reinstall sw on the cluster"

    def setUp(self):
        self.setTestStep('setUp')
        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        #self.super__setUp()
        self.currentTestCase = self

    def runTest(self):
        '''reinstall COM-SA on the cluster
        '''
        if self.testSuiteConfig.has_key('replicatedListsTest'):
            if not self.testSuiteConfig.has_key('startTime'):
                self.fail('ERROR', 'The start time was not recorded in the testSuiteConfig parameter.')

        if self.testSuiteConfig.has_key('codeCoveredCheck'):
            self.coverageEnabled = eval(self.testSuiteConfig['codeCoveredCheck']['codeCoveredCheck'])

        self.setTestStep('runTest')
        self.setTestcase(self.tag, self.name)

        # Restore partial backup of COM
            # If we define a backup name in the tc_MISC_004_....xml file, that backup will be restored.
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
            self.fail('ERROR', 'COM backup not found!')

        self.setTestStep('Restore partial backup of COM')

        result = self.comsa_lib.restoreSystem(self, backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 2, removeBackup = False)
        self.fail(result[0], result[1])


        ###########################################################################
        # Install COMSA
        ###########################################################################

        self.setTestStep('Install COMSA')
        # The following path is hardcoded in many Core MW method
        self.temp_dir = '/home/coremw/incoming/'


        if self.testSuiteConfig.has_key('replicatedListsTest') and self.testSuiteConfig['replicatedListsTest'] == 'True' \
        and self.testSuiteConfig.has_key('replicatedListsRt') and self.testSuiteConfig.has_key('replicatedListsDepl'):
            self.myLogger.debug('COMSA installation binaries already copied to the target')
            comsaRuntimeSDP = self.testSuiteConfig['replicatedListsRt']
            comsaDeploymentTemplateSDP = self.testSuiteConfig['replicatedListsDepl']
        else:
            # Check COMSA runtime SDP under the given path
            noOfScs = len(self.testConfig['controllers'])
            if noOfScs == 2:
                installSdp = 'ComSa_install.sdp'
            elif noOfScs == 1:
                installSdp = 'ComSa_install_Single.sdp'
            else:
                self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' %str(noOfScs))

            cmd = 'ls %s | grep "%s"' %(self.buildRelease, installSdp)
            self.myLogger.debug('Check COMSA runtime SDP under the given path by: %s' %cmd)
            result = self.miscLib.execCommand(cmd)
            if result[1] == '':
                self.fail('ERROR','No %s found under: %s' %(self.buildRelease, installSdp))
            comsaRuntimeSDP = result[1].strip()

            # Check COMSA deployment template SDP under the given path
            cmd = 'ls %s | grep -i com | grep -i sa | grep -i cxp | grep -i sdp' %self.buildRelease
            self.myLogger.debug('Check COMSA deployment template SDP under the given path by: %s' %cmd)
            result = self.miscLib.execCommand(cmd)
            if result[1] == '':
                self.fail('ERROR','No COM_SA-CXPxxxxxxxx.sdp found under: %s' %self.buildRelease)
            comsaDeploymentTemplateSDP = result[1].strip()

            # Create COM-SA temp directory
            cmd = 'mkdir -p %s' %self.temp_dir
            self.myLogger.debug('Create COM-SA temp directory by: %s' %cmd)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])

            # Upload COMSA runtime SDP and COMSA deployment template SDP to target
            self.setTestStep('Upload COMSA runtime SDP and COMSA deployment template SDP to target')
            self.myLogger.debug('Upload COMSA runtime SDP and COMSA deployment template SDP to target')
            try:
                file = '%s%s' %(self.buildRelease, comsaRuntimeSDP)
                self.sshLib.remoteCopy(file, '%s' %(self.temp_dir), timeout = 60)
                file = '%s%s' %(self.buildRelease, comsaDeploymentTemplateSDP)
                self.sshLib.remoteCopy(file, '%s' %(self.temp_dir), timeout = 60)
            except:
                self.fail('ERROR','failed to upload SDPs')

        # Import all SDPs to repository
        self.setTestStep('Import all SDPs to repository')
        self.myLogger.debug('Import all SDPs to repository')
        try:
            self.safLib.importSwBundle(comsaRuntimeSDP)
            self.safLib.importSwBundle(comsaDeploymentTemplateSDP)
        except:
            self.fail('ERROR','failed to import SDPs')

        # Start COMSA installation campaign
        self.setTestStep('Start COMSA installation')
        campaignName = 'ERIC-ComSaInstall'
        self.myLogger.debug('Install campaign: %s' %campaignName)
        result = self.safLib.upgradeStart(campaignName)
        self.fail(result[0], result[1])
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
            self.fail('ERROR','failed to install COMSA')

        # Check CMW status, and wait for status ok
        self.setTestStep('Check CMW status, and wait for status ok')
        self.myLogger.debug('Commit campaign: %s' %campaignName)
        okFlag = False
        for i in range(30):
            result = self.safLib.checkClusterStatus('off', 'su node comp')
            if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
            else:
                if re.search('cmw-status: command not found', result[1]):
                        self.sshLib.tearDownHandles()
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','Failed to install COMSA')

        # Commit COMSA installation campaign
        self.setTestStep('Commit COMSA installation campaign')
        self.myLogger.debug('Commit campaign: %s' %campaignName)
        result = self.safLib.upgradeCommit(campaignName)
        if result[0] == 'ERROR':
            self.fail('ERROR','failed to commit')

        # Check CMW status, and wait for status ok
        self.setTestStep('Check CMW status after committing COMSA install')
        self.myLogger.debug('Check CMW status after committing COMSA install')
        okFlag = False
        for i in range(30):
           result = self.safLib.checkClusterStatus('off', 'su node comp')
           if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
           else:
                if re.search('cmw-status: command not found', result[1]):
                        self.sshLib.tearDownHandles()
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','Failed to commit COMSA installation')

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
        #fix for code coverage
        if self.coverageEnabled:
            self.testSuiteConfig['restoreBackup'] = backupName

        # Check CMW status, and wait for status ok
        self.setTestStep('Check CMW status after creating COMSA backup')
        self.myLogger.debug('Check CMW status, and wait for status ok')
        okFlag = False
        for i in range(30):
            result = self.safLib.checkClusterStatus('off', 'su node comp')
            if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
            else:
                if re.search('cmw-status: command not found', result[1]):
                        self.sshLib.tearDownHandles()
                self.miscLib.waitTime(30)
        if okFlag == False:
            self.fail('ERROR','Failed to create backup for COMSA')

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

    def tearDown(self):
        self.setTestStep('tearDown')

        # Removing temp directory
        cmd = '\\rm -rf %s' %self.temp_dir
        self.myLogger.debug('Removing temp directory by: %s' %cmd)
        result = self.sshLib.sendCommand(cmd)

        coreTestCase.CoreTestCase.tearDown(self)


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
