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

    Tag:

    Id:
    ""
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
import os
from java.lang import System

class UninstallComSa(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.createBackup = 'False'
        self.backupName = 'backupBeforeComSaUninstall'
        self.restoreBackup = 'False'
        self.installComSa = 'False'
        self.uninstallComSa = 'True'

        self.allowedPsoDir1 = '/storage/no-backup/comsa_for_coremw-apr9010555'
        self.allowedPsoDir2 = '/storage/system/config/comsa_for_coremw-apr9010555'
        self.allowedPsoDir3 = '/storage/system/software/comsa_for_coremw-apr9010555'

        self.dir3AllowedFromRelease = '3'
        self.dir3AllowedFromVersion = 'R5A09'
        self.dir3AllowedFromMajorVersion = '5'

        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.tmpDirOnTarget = dict.get('AUTOINSTALL_DIR_TARGET')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        self.comsaAprNumber = dict.get('COMSA_APR_NUMBER')
        self.psoBaseArea = dict.get('PSO_BASE_AREA')

        self.swDir = System.getProperty("swDirNumber")
        self.noOfScs = len(self.testConfig['controllers'])
        self.sdpNames = [self.cxpSdpName, self.installSdpName, self.installSdpNameSingle, self.removeSdpName, self.removeSdpNameSingle]
        self.neededFiles = [None, None, None] #[CXP.sdp, install.sdp, remove.sdp]
        self.sdpFilesAlreadyOnTarget = False

        # Variables needed for the build token management
        self.buildTokenCreated = False
        self.backupRestoreOk = False
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.myLogger.info('runTest')
        self.setTestStep('runTest')

        # Check that COM SA is installed and in use
        result = self.lib.getComponentVersion(self.comsaCxpNumber)
        if self.installComSa == 'True' and self.uninstallComSa == 'False':
            # We expect 'ERROR' because COM SA should not be installed
            if result[0] == 'SUCCESS':
                self.fail('ERROR', 'Expected lib.getComponentVersion() not to find COM SA on the target. The method returned: %s' %str(result))
        else:
            self.fail(result[0], result[1])

        if self.createBackup == 'True':
            self.setTestStep('Create initial backup')
            self.backupSystem()


        self.setTestStep('Identify and optionally copy needed files to target')

        self.identifyNeededFiles()
        if self.sdpFilesAlreadyOnTarget == False:
            result = self.comsa_lib.copyFilesToTarget(self.neededFiles, self.tmpDirOnTarget)
            self.fail(result[0],result[1])

        # Remove build token in case it was created
        if self.buildTokenCreated == True:
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildTokenDir, self.tokenPattern)
            self.fail(result[0],result[1])
            self.buildTokenCreated = False

        if self.uninstallComSa == 'True' and self.neededFiles[2] != None:
            self.setTestStep('Run un-installation campaign')

            # /storage/system/software/comsa-... is allowed from these versions
            self.ComsaOK = self.lib.checkComponentVersion('comsa', self.dir3AllowedFromRelease, self.dir3AllowedFromVersion)
            self.fail(self.ComsaOK[0],self.ComsaOK[1])
            self.ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.dir3AllowedFromRelease, self.dir3AllowedFromMajorVersion)
            self.fail(self.ComsaMajorOK[0], self.ComsaMajorOK[1])

            uninstallSdpFileName = self.neededFiles[2].split('/')[len(self.neededFiles[2].split('/')) - 1]
            result = self.comsa_lib.installComp(self.tmpDirOnTarget, '', uninstallSdpFileName, createBackup = False, removeCampaign = True, backupRpms = self.backupRpmScript)
            self.fail(result[0], result[1])

            self.setTestStep('Verify that COM SA was successfully removed from the system')
            result = self.lib.getComponentVersion(self.comsaCxpNumber)
            if result[0] != 'ERROR' and 'Not possible to interpret result for checking version of component' not in result[1]:
                self.fail('ERROR', 'Expected lib.getComponentVersion() not to find COM SA on the target. The method returned: %s' %str(result))

            allowedDirsInPsoArea = self.createAllowedDirsInPso()
            self.verifyPsoArea(self.psoBaseArea, self.comsaAprNumber, allowedDirsInPsoArea)

        # Optionally re-install COM SA with installation campaign
        if self.installComSa == 'True' and self.neededFiles[0] != None and self.neededFiles[1] != None:
            self.setTestStep('Run COM SA installation campaign')
            cxpSdpFileName = self.neededFiles[0].split('/')[len(self.neededFiles[0].split('/')) - 1]
            installSdpFileName = self.neededFiles[1].split('/')[len(self.neededFiles[1].split('/')) - 1]
            result = self.comsa_lib.installComp(self.tmpDirOnTarget, cxpSdpFileName, installSdpFileName, createBackup = False, backupRpms = self.backupRpmScript)
            self.fail(result[0], result[1])
            result = self.lib.getComponentVersion(self.comsaCxpNumber)
            self.fail(result[0], result[1])

        # Optionally restore the system
        if self.restoreBackup == 'True':
            self.setTestStep('Restore system')
            self.removeBackup = True
            if self.testSuiteConfig.has_key('restoreBackup') and self.backupName == self.testSuiteConfig['restoreBackup']:
                self.removeBackup = False
            result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = self.removeBackup)
            self.fail(result[0],result[1])
            self.backupRestoreOk = True

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')

        if self.buildTokenCreated == True:
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildTokenDir, self.tokenPattern)
            self.fail(result[0],result[1])

        if self.restoreBackup == 'True' and self.backupRestoreOk == False:
            self.setTestStep('Restore system')
            result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = self.removeBackup)
            self.fail(result[0],result[1])

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')



    def identifyNeededFiles(self):
        """
        If files already on the target (copied there by the setup test case), we just identify and save the file names in self.neededFiles
        If swDirNumber is not defined, we build COM SA and save the absolute file names in self.neededFiles
        If swDirNumber is defined, we search for the binaries in the specified directory and save the absolute file names in self.neededFiles
        """
        self.myLogger.debug("enter identifyNeededFiles")

        localPathToSw = ''
        if self.testSuiteConfig.has_key('sdpFilesOnTarget') and self.testSuiteConfig['sdpFilesOnTarget'] == True:
            self.sdpFilesAlreadyOnTarget = True
            if self.installComSa == 'True':
                result = self.comsa_lib.findFilesMatchingPattern('%s/*%s*sdp' %(self.tmpDirOnTarget, self.comsaCxpNumber), onTarget = True)
                self.fail(result[0], result[1])
                if len(result[1]) == 1:
                    self.neededFiles[0] = result[1][0]
                else:
                    self.fail('ERROR', 'Expected to find exactly one file matching pattern "%s" under %s. Instead found: %s' \
                              %(self.comsaCxpNumber, self.tmpDirOnTarget, str(result[1])))
                result = self.comsa_lib.findFilesMatchingPattern('%s/*install*sdp' %(self.tmpDirOnTarget), onTarget = True)
                self.fail(result[0], result[1])
                if len(result[1]) == 1:
                    self.neededFiles[1] = result[1][0]
                else:
                    self.fail('ERROR', 'Expected to find exactly one file matching pattern "install" under %s. Instead found: %s' \
                              %(self.comsaCxpNumber, str(result[1])))
            if self.uninstallComSa == 'True':
                result = self.comsa_lib.findFilesMatchingPattern('%s/*remove*sdp' %(self.tmpDirOnTarget), onTarget = True)
                self.fail(result[0], result[1])
                if len(result[1]) == 1:
                    self.neededFiles[2] = result[1][0]
                else:
                    self.fail('ERROR', 'Expected to find exactly one file matching pattern "remove" under %s. Instead found: %s' \
                              %(self.comsaCxpNumber, str(result[1])))
        else:
            if self.swDir == 'undef':
                # Get a build token
                for i in range(self.numberOfGetTokenRetries):
                    result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildTokenDir, self.tokenPattern)
                    if result[0] == 'SUCCESS':
                        break
                self.fail(result[0],result[1])
                self.buildTokenCreated = True

                makeOption = ''
                if self.linuxDistro == self.distroTypes[1]: # rhel
                    makeOption = 'rhel_sdp'
                result = self.comsa_lib.buildCOMSA(self.buildSrc, self.buildRelease, self.noOfScs, self.sdpNames, makeOption)
                self.fail(result[0], result[1])
                localPathToSw = self.buildRelease
            else:
                localPathToSw = '%s%s/comsa/' %(self.installRoot, self.swDir)

            if self.installComSa == 'True':
                result = self.comsa_lib.findFilesMatchingPattern('%s/*%s*sdp' %(localPathToSw, self.comsaCxpNumber))
                self.fail(result[0], result[1])
                if len(result[1]) == 1:
                    self.neededFiles[0] = result[1][0]
                else:
                    self.fail('ERROR', 'Expected to find exactly one file matching pattern "%s" under %s. Instead found: %s' \
                              %(self.comsaCxpNumber, self.tmpDirOnTarget, str(result[1])))
            if self.noOfScs == 2:
                if self.installComSa == 'True':
                    self.neededFiles[1] = '%s%s' %(localPathToSw, self.installSdpName)
                if self.uninstallComSa == 'True':
                    self.neededFiles[2] = '%s%s' %(localPathToSw, self.removeSdpName)
            elif self.noOfScs == 1:
                if self.installComSa == 'True':
                    self.neededFiles[1] = '%s%s' %(localPathToSw, self.installSdpNameSingle)
                if self.uninstallComSa == 'True':
                    self.neededFiles[2] = '%s%s' %(localPathToSw, self.removeSdpNameSingle)
            else:
                self.myLogger.debug("leave identifyNeededFiles")
                self.fail('ERROR', 'Currently only handling systems with 1 or 2 system controllers')

        self.myLogger.debug('leave identifyNeededFiles')


    def backupSystem(self):
        # Skip creating the backup if there is a safe backup created at the beginning of the test suite
        self.myLogger.debug('enter backupSystem')
        backupFound = False
        if self.testSuiteConfig.has_key('restoreBackup'):
            result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
            if result == ('SUCCESS', 'EXIST'):
                self.backupName = self.testSuiteConfig['restoreBackup']
                backupFound = True
        if backupFound == False:
            result = self.safLib.isBackup(self.backupName)
            self.fail(result[0], result[1])
            if result != ('SUCCESS','NOT EXIST'):
                result = self.safLib.backupRemove(self.backupName)
                self.fail(result[0], result[1])
            result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
            if result[0] != 'SUCCESS' and self.linuxDistro == self.distroTypes[1]:
                self.myLogger.warn('Could not create backup on RHEL system. This is not a critical fault')
            else:
                self.fail(result[0], result[1])
        self.myLogger.debug('leave backupSystem')


    def createAllowedDirsInPso(self):
        self.myLogger.debug('enter createAllowedDirsInPso')

        allowedDirsInPsoArea = []
        if self.allowedPsoDir1 != '':
            allowedDirsInPsoArea.append(self.allowedPsoDir1)
        if self.allowedPsoDir2 != '':
            allowedDirsInPsoArea.append(self.allowedPsoDir2)
        if self.allowedPsoDir3 != '' and self.ComsaOK[1] == True and self.ComsaMajorOK[1] == True:
            allowedDirsInPsoArea.append(self.allowedPsoDir3)

        self.myLogger.debug('leave createAllowedDirsInPso')
        return allowedDirsInPsoArea


    def verifyPsoArea(self, psoArea, aprNumber, allowedDirectories):
        self.myLogger.debug('enter verifyPsoArea')
        notAllowdDirectories = []
        result = self.sshLib.sendCommand('find %s -name *%s' %(psoArea, aprNumber))
        self.fail(result[0], result[1])
        for line in result[1].splitlines():
            if line not in allowedDirectories:
                notAllowdDirectories.append(line)
        if len(notAllowdDirectories) != 0:
            self.myLogger.debug('leave verifyPsoArea')
            self.fail('ERROR', 'The following directories were not expected to be found in the PSO area: %s' %str(notAllowdDirectories))

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
