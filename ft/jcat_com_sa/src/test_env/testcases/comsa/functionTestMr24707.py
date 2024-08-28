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

    TC-MR24760-001 Install COMSA with campaign which is generated from AMF CGS tool
    TC-MR24760-002 Upgrade COMSA with campaign which is generated from AMF CGS tool



    ""
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
from se.ericsson.jcat.fw import SUTHolder
import time
import os,sys,re
import copy
import omp.tf.netconf_lib as netconf_lib
from java.lang import System



class GenerateCampaign(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']

        # parameters from the config files

        self.comBackupName = {}

        self.restoreComBackup = 'False'
        self.installGenerate = 'False'
        self.upgradeGenerate = 'False'
        self.installComsa = 'False'
        self.upgradeComsa = 'False'

        self.MR24707 = '/home/MR24707'
        self.temp = '/home/MR24707/temp'
        self.install = '/home/MR24707/temp/install_campaign'
        self.upgrade = '/home/MR24707/temp/upgrade_campaign'
        self.software_dir = '/home/software/'

        self.reqComSaRelease = "3"
        self.reqComSaMajorVersion = "5"


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        self.singleBundle = "ComSa_install_Single.sdp"
        self.dualBundle = "ComSa_install.sdp"
        self.upgradeBundle = "comsa_upgrade.sdp"

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.buildLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("SRC"))
        self.resourceFilesLocation = dict.get("PATH_TO_MR24707")
        self.absDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.buildDir = dict.get('BUILD_TOKENS')
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')

        self.tmpBackupName = 'MR24707_tmpBackup'
        self.restoreSystemOK = False

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.template = "*%s*.tar.gz" %(dict.get('COM_SA_TMPL_CXP_RHEL'))
            self.runtime =  "*%s*.tar" %(dict.get('COM_SA_RUNTIME_CXP_RHEL'))
            self.bundleArchive = "COM_SA-CXP9028073_1.sdp"
        else:
            self.template = "*%s*.tar.gz" %(dict.get('COM_SA_TMPL_CXP'))
            self.runtime =  "*%s*.tar" %(dict.get('COM_SA_RUNTIME_CXP'))
            self.bundleArchive = dict.get('CXP_SDP_NAME_OFFICIAL')

        self.myLogger.info('Exit setUp')

    def runTest(self):

        self.setTestStep('runTest')

        ComsaMajorOK = ('SUCCESS', True)
        self.skip_test = False

        ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion)
        self.fail(ComsaMajorOK[0],ComsaMajorOK[1])

        if ComsaMajorOK[1] == True:

            # Variables needed for the build token management
            dirName = System.getProperty("logdir")
            user = os.environ['USER']
            self.tokenPattern = 'buildToken-%s' %user
            self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
            self.numberOfGetTokenRetries = 5

            self.memoryCheck = False
            if self.testSuiteConfig.has_key('memoryCheck'):
                self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

            # 0. Create temporary backup
            self.backupSystem()

            # 1.Restore COM backup
            if self.restoreComBackup == 'True':
                self.myLogger.debug('Restore the COM backup ')
                self.setTestStep('Restore the COM backup')
                self.comBackupName = self.findComBackup(self.comBackupName)

                result = self.comsa_lib.restoreSystem(self, self.comBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 2, removeBackup = False)
                self.fail(result[0],result[1])

            ##copy software to cluster and install them
            result = self.sshLib.sendCommand('mkdir -p %s' %self.software_dir)
            self.fail(result[0],result[1])

            result = self.sshLib.remoteCopy('%s/amf-cgs-R8A-1.noarch.rpm' %self.resourceFilesLocation, '%s/' %self.software_dir, timeout=60)
            self.fail(result[0],result[1])
            result = self.sshLib.remoteCopy('%s/jre-7-linux-x64.rpm' %self.resourceFilesLocation, '%s/' %self.software_dir, timeout=60)
            self.fail(result[0],result[1])

            #install java and CGS tool
            result = self.sshLib.sendCommand('rpm -i %s/jre-7-linux-x64.rpm' %self.software_dir)
            self.fail(result[0],result[1])
            self.miscLib.waitTime(10)

            result = self.sshLib.sendCommand('rpm -i %s/amf-cgs-R8A-1.noarch.rpm' %self.software_dir)
            self.fail(result[0],result[1])
            self.miscLib.waitTime(10)
            result = self.sshLib.sendCommand('amf-cgs -v')
            self.fail(result[0],result[1])

            # 2. Prepare COMSA package
            self.setTestStep('Prepare COMSA package')
            BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
            if BuildPath[0] != 'SUCCESS':
                self.logger.error(result[1])
                self.logger.debug('upgradeCOMSAFromStream: Exit')
                return (BuildPath[0], 'Build COM SA failed')
            result = self.comsa_lib.copyFilesToTarget(['%s' %BuildPath[9], '%s' %BuildPath[10]], self.MR24707, True)
            self.fail(result[0],result[1])

            #create /home/MR24707/temp directory
            result = self.sshLib.sendCommand('mkdir -p %s' %self.temp)
            self.fail(result[0],result[1])

            #untar and copy ETF to self.temp
            result = self.sshLib.sendCommand('cd %s; tar xvf %s' %(self.MR24707, self.runtime))
            self.fail(result[0],result[1])
            #self.miscLib.waitTime(10)

            result = self.sshLib.sendCommand('cd %s; tar xvf %s' %(self.MR24707, self.template))
            self.fail(result[0],result[1])
            #self.miscLib.waitTime(10)

            result = self.sshLib.sendCommand('cd %s; tar xvf %s' %(self.MR24707, self.bundleArchive))  #untar sdp bundle
            self.fail(result[0],result[1])
            #self.miscLib.waitTime(10)

            result = self.sshLib.sendCommand('\cp %s/ETF.xml %s' %(self.MR24707, self.temp))  #copy ETF new to temp/
            self.fail(result[0],result[1])


            # 3.Generate campaign
            self.setTestStep('Start generate campaign')
            #a. Install campaign
            if self.installGenerate == 'True':
                self.logger.info('Generate the install camapign ')

                result = self.sshLib.sendCommand('cd %s; mkdir install_campaign' %self.temp)
                self.fail(result[0],result[1])

                noOfScs = len(self.testConfig['controllers'])
                if noOfScs == 2:
                    result = self.sshLib.sendCommand('\cp %s/COM_SA_I1*/%s %s' %(self.MR24707, self.dualBundle, self.install))
                    self.fail(result[0],result[1])

                elif noOfScs == 1:
                    result = self.sshLib.sendCommand('\cp %s/COM_SA_I2*/%s %s/' %(self.MR24707, self.singleBundle, self.install))
                    self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('cd %s; tar xvf *sdp' %self.install)  #untar campaign sdp
                self.fail(result[0],result[1])
                self.miscLib.waitTime(10)

                result = self.sshLib.remoteCopy('%s%s/install-campaign-generate.sh' %(self.MY_REPOSITORY,self.pathToConfigFiles), '%s/' %self.temp, timeout=60)
                self.fail(result[0],result[1])

                #b. Upgrade camapign
            if self.upgradeGenerate == 'True':
                self.logger.info('Generate the upgrade camapign ')
                result = self.sshLib.sendCommand('cd %s; mkdir upgrade_campaign' %self.temp)  #for upgrade
                self.fail(result[0],result[1])

                noOfScs = len(self.testConfig['controllers'])
                if noOfScs == 2:
                    result = self.sshLib.sendCommand('cd %s/COM_SA_U2*/ ; ./comsa-generate-campaign-sdp' %self.MR24707)    #generate comsa_upgrade.sdp
                    self.fail(result[0],result[1])
                    #self.miscLib.waitTime(10)

                    result = self.sshLib.sendCommand('\cp %s/COM_SA_U2*/comsa_upgrade.sdp %s/' %(self.MR24707, self.upgrade))  #copy to upgrade_campaign folder
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('\cp %s/COM_SA_U2*/campaign*.xml %s' %(self.MR24707, self.temp))  #copy to campaignxml to temp/ folder
                    self.fail(result[0],result[1])

                elif noOfScs == 1:
                    result = self.sshLib.sendCommand('cd %s/COM_SA_U3*/ ; ./comsa-generate-single-campaign-sdp' %self.MR24707)    #generate comsa_upgrade.sdp  and campaign for input generate
                    self.fail(result[0],result[1])
                    #self.miscLib.waitTime(10)

                    result = self.sshLib.sendCommand('\cp %s/COM_SA_U3*/comsa_upgrade.sdp %s/' %(self.MR24707, self.upgrade))  #copy to upgrade_campaign folder
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('\cp %s/COM_SA_U3*/campaign*.xml %s' %(self.MR24707, self.temp))  #copy to campaignxml to temp/ folder
                    self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('cd %s; tar xvf *sdp' %self.upgrade)  #untar campaign sdp
                self.fail(result[0],result[1])
                result = self.sshLib.remoteCopy('%s%s/upgrade-campaign-generate.sh' %(self.MY_REPOSITORY,self.pathToConfigFiles), '%s/' %self.temp, timeout=60)
                self.fail(result[0],result[1])

            #run script
            result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.temp)
            self.fail(result[0],result[1])

            result = self.sshLib.sendCommand('cd %s;./*sh' %self.temp)
            self.fail(result[0],result[1])
            self.miscLib.waitTime(10)


            # 4. Install or upgrade COMSA
            # Import all SDPs to repository
            self.setTestStep('Import all SDPs to repository')
            self.myLogger.debug('Import all run time SDPs to repository')
            result = self.comsa_lib.importSdpPackage('%s/%s' %(self.MR24707, self.bundleArchive))
            self.fail(result[0], result[1])

            # Check COMSA deployment template SDP
            #for install
            if self.installComsa == 'True':
                noOfScs = len(self.testConfig['controllers'])
                if noOfScs == 2:
                    result = self.comsa_lib.importSdpPackage('%s/%s' %(self.install, self.dualBundle))
                    self.fail(result[0], result[1])

                elif noOfScs == 1:
                    result = self.comsa_lib.importSdpPackage('%s/%s' %(self.install, self.singleBundle))
                    self.fail(result[0], result[1])

                # Start COMSA install campaign
                self.setTestStep('Start COMSA installation')
                campaignName = 'ERIC-ComSaInstall'
                self.myLogger.debug('Install campaign: %s' %campaignName)
                result = self.safLib.upgradeStart(campaignName)
                self.fail(result[0], result[1])

            #for upgrade
            if self.upgradeComsa == 'True':
                #remove old campaign before test
                self.myLogger.debug('enter remove old campaign ')
                cmd = 'cmw-repository-list --campaign | grep ERIC-ComSa-upgrade'
                result = self.sshLib.sendCommand(cmd)
                if result[1] and result[0] == 'SUCCESS':
                    fileName = result[1]
                    cmd = 'cmw-sdp-remove %s' %fileName
                    result = self.sshLib.getTimeout()
                    if result[0] != 'SUCCESS':
                        self.myLogger.error(result[1])
                        self.myLogger.debug('Fail to remove old campaign ')
                    self.sshLib.setTimeout(60)
                    result = self.sshLib.sendCommand(cmd)

                result = self.comsa_lib.importSdpPackage('%s/%s' %(self.upgrade, self.upgradeBundle))
                self.fail(result[0], result[1])

                # Start COMSA upgrade campaign
                self.setTestStep('Start COMSA upgrade')
                campaignName = 'ERIC-ComSa-upgrade'
                self.myLogger.debug('Upgrade campaign: %s' %campaignName)
                result = self.safLib.upgradeStart(campaignName)
                self.fail(result[0], result[1])

            # Waiting until campaign complete
            result = self.comsa_lib.waitForCampaignReady(campaignName)
            self.fail(result[0], result[1])

             # Commit COMSA installation campaign
            self.setTestStep('Commit COMSA installation campaign')
            self.myLogger.debug('Commit campaign: %s' %campaignName)
            result = self.safLib.upgradeCommit(campaignName)
            if result[0] == 'ERROR':
                self.fail('ERROR','failed to commit')

            # Check CMW status, and wait for status ok

            self.setTestStep('Check CMW status after committing COMSA install')
            self.myLogger.debug('Check CMW status after committing COMSA install')
            result = self.comsa_lib.waitForClusterStatusOk()
            self.fail(result[0], result[1])

#            self.setTestStep('Restore system')
#
#            result = self.comsa_lib.restoreSystem(self, self.tmpBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
#            self.fail(result[0],result[1])
#            self.restoreSystemOK = True
#
#            coreTestCase.CoreTestCase.runTest(self)

        else:
            self.logger.info('Skipped tests because of COMSA version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True


    def findComBackup(self, comBackupName):
        """
        We search for the latest COM backup which's name contains COM (case insensitive),
        but does not contain comsa, com_sa, com-sa (case insensitive)
        """
        self.logger.info('findComBackup: Called')
        cmd = """cmw-partial-backup-list 2>&1 | sed 's/\[//g' | sed 's/\]//g' | grep -i com | egrep -iv '(comsa)|(com_sa)|(com-sa)' | tail -1 | awk '{print $NF}' """
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        combackupName = result[1]
        if combackupName == '':
            if self.linuxDistro != self.distroTypes[1]:
                self.logger.info('findComBackup: Exit')
                self.fail('ERROR', 'findComBackup: COM backup not found!')
            elif self.linuxDistro == self.distroTypes[1]:
                # For RHEL systems we try to reinstall COM instead of restoring a COM backup
                combackupName == 'com_autobackup'

        self.logger.info('findComBackup: Exit')
        return combackupName

    def findComSaBackup(self, backupName):
        """
        We search for the latest COMSA backup which's name
        contain comsa, com_sa, com-sa (case insensitive)
        """
        cmd = """cmw-partial-backup-list 2>&1 | sed 's/\[//g' | sed 's/\]//g' | egrep -i '(comsa)|(com_sa)|(com-sa)' | tail -1 | awk '{print $NF}' """
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        backupName = result[1]
        if backupName == '':
            self.logger.warn('findComSaBackup: COMSA backup not found!')
            self.logger.info('ERROR , COMSA backup not found!')
            return {}
        self.logger.info('findComSaBackup: Exit')
        return backupName

    def backupSystem(self):
        # Skip creating the backup if there is a safe backup created at the beginning of the test suite
        self.myLogger.debug('enter backupSystem')
        backupFound = False
        if self.testSuiteConfig.has_key('restoreBackup'):
            result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
            if result == ('SUCCESS', 'EXIST'):
                self.tmpBackupName = self.testSuiteConfig['restoreBackup']
                backupFound = True
        if backupFound == False:
            result = self.safLib.isBackup(self.tmpBackupName)
            self.fail(result[0], result[1])
            if result != ('SUCCESS','NOT EXIST'):
                result = self.safLib.backupRemove(self.tmpBackupName)
                self.fail(result[0], result[1])
            result = self.comsa_lib.backupCreateWrapper(self.tmpBackupName, backupRpms = self.backupRpmScript)
            if result[0] != 'SUCCESS' and self.linuxDistro == self.distroTypes[1]:
                self.myLogger.warn('Could not create backup on RHEL system. This is not a critical fault')
            else:
                self.fail(result[0], result[1])
        self.myLogger.debug('leave backupSystem')


    def tearDown(self):
        self.setTestStep('tearDown')
        if self.skip_test == False:
            if self.restoreSystemOK == False:
                result = self.comsa_lib.restoreSystem(self, self.tmpBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                self.fail(result[0],result[1])

            self.logger.debug('Removing the temp directories ' )
            command = '\\rm -rf /home/MR24707/'
            self.sshLib.sendCommand(command)

            command = '\\rm -rf /home/software'
            self.sshLib.sendCommand(command)

            self.sshLib.tearDownHandles()
        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
