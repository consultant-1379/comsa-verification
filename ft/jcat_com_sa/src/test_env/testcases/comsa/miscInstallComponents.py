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

    This testcase script can install only one component at a time.

    Test cases:

    ==================================
    TEST CASE SPECIFICATION:

    Tag: TC-MISC-029

    Id:  MISC - Install CoreMW

    ==================================
    TEST CASE SPECIFICATION:

    Tag: TC-MISC-030

    Id:  MISC - Install COM

    ==================================
    TEST CASE SPECIFICATION:

    Tag: TC-MISC-031

    Id:  MISC - Install COMSA

    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
from se.ericsson.jcat.fw import SUTHolder
import os
import sys

from java.lang import System

class InstallComponents(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.testcase_tag = tag
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.component_to_install = ''
        self.supported_components = ['CMW','COM','COMSA']

        # this flag enables the creation of a backup where the name of that backup can be configured
        self.createBackup = 'False'
        self.backupName = ''
        # this flag enables the creation of the "autobackup" which is built in the installComp function
        self.createAutoBackup = 'False'

        self.suRestartMaxSet = 'False'
        self.suRestartMaxValue = '1000'
        self.swSource = 'COMSA_internal'

        self.reqComSaRelease = "3"
        self.reqComSaVersion = "R2A01"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.uninstallScriptPath =  '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST"))
        self.tmpDirOnTarget = dict.get('AUTOINSTALL_DIR_TARGET')
        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.distroTypes = eval(dict.get("LINUX_DISTRO_TYPES"))
        result = self.lib.updateLinuxDistroInDictionary(self.testSuiteConfig, self.distroTypes)
        self.fail(result[0], result[1])
        self.linuxDistro = self.testSuiteConfig['linuxDistro']['value']
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.uninstallScriptName = dict.get('UNINSTALL_SCRIPT_NAME_RHEL')
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.uninstallScriptName = dict.get('UNINSTALL_SCRIPT_NAME')
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        backupRpmScriptLocal = "%s%s%s" %(os.environ['MY_REPOSITORY'], dict.get("PATH_TO_CONFIG_FILES"), dict.get("BACKUP_RPMS_SCRIPT"))
        self.backupRpmScript = "/home/%s" % dict.get("BACKUP_RPMS_SCRIPT")
        # copy backup rpms script to cluster
        result = self.sshLib.remoteCopy(backupRpmScriptLocal, '/home/', timeout = 60)
        self.fail(result[0], result[1])
        cmd = 'chmod +x %s' % self.backupRpmScript
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.installRoot = ''
        if self.swSource == 'COMSA_internal':
            self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        elif self.swSource == 'CCC_CI':
            self.installRoot = dict.get('CCC_CI_R_INSTALL')
        else:
            self.fail('ERROR', 'Specified swSource: %s is not handled' %self.swSource)

        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        self.buildComsa = System.getProperty("buildComSa")
        if self.swSource == 'CCC_CI':
            self.swDir = ''
        else:
            self.swDir = System.getProperty("swDirNumber")
            if self.swDir == 'undef':
                self.fail('ERROR', 'No directory specified where to fetch the software binaries from. Use the --swDirNumber option to executive.py')

        self.super__setUp()
        self.sutholder = SUTHolder.getInstance()
        self.currentSut = self.sutholder.zones[0]
        self.TargetDataLib = self.currentSut.getLibrary("TargetDataLib")
        self.targetData = self.TargetDataLib.getTargetData()

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.setTestStep('runTest')

        self.skip_test = False
        # The following "offlineVersion" solution is needed for the regtest runs:
        # In the regtest it is needed to check the COM SA version to be able to decide if the suite (containing this testcase) need to be run or not.
        # The offline version checking is needed because in some testcases COM SA is not installed on the system, but still it is needed to check its version.
        # To get the offline version, the offline values are read from a previous save (setUpTestcase).
        # If the offlineVersions is not available then it means that the current TC run is not part of the regtest (e.g. running the MR27359 suite separately).
        # Note: if running this TC separately (as single TC or in MR27359 suite, then the it is considered as a manual run where the user knows that the COM SA version is correct)
        #       that means: if not in regtest then do not check the COM SA versions.
        offlineVersion = ['','','']
        ComSaOK = ['', False]

        result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'comsa')
        if result[0] == "REGTEST":
            offlineVersion[0] = result[1]
            offlineVersion[1] = result[2]
            offlineVersion[2] = result[3]
            ComSaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion, offlineVersion)
            self.fail(ComSaOK[0],ComSaOK[1])
        else:
           ComSaOK[1] = True

        if ComSaOK[1]:
            if self.buildComsa not in ["True", "False"]:
                self.fail('ERROR', 'Unknown value for self.buildComsa. If should be either True or False. It is: %s' %self.buildComsa)

            self.lib.refreshSshLibHandlesAllSCs(self.testConfig)

            self.localPathToSw = '%s%s/' %(self.installRoot, self.swDir)
            sdpNames = [self.cxpSdpName, self.installSdpName, self.installSdpNameSingle, self.removeSdpName, self.removeSdpNameSingle]

            # Install the component
            if self.component_to_install in self.supported_components:
                self.myLogger.info('Install %s' %self.component_to_install)

                MakeOption = ''
                if self.linuxDistro == self.distroTypes[1]: # rhel
                    MakeOption = 'rhel_sdp'
                sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
                result = self.comsa_lib.reInstallComponents(self, self.buildComsa, self.buildSrc, self.buildRelease, sdpNames, self.localPathToSw, self.uninstallScriptPath, \
                                                        self.uninstallScriptName, self.testConfig, self.testSuiteConfig, self.buildTokenDir, sshKeyUpdater, \
                                                        [self.component_to_install], destinationOnTarget = self.tmpDirOnTarget, createBackup = eval(self.createAutoBackup), makeOption = MakeOption)
                self.fail(result[0], result[1])
                """
                if result[0] == 'SUCCESS':
                    self.myLogger.info('%s installed successfully' %self.component_to_install)
                else:
                    self.myLogger.error(result[1])
                """
            # Unknown component name set
            else:
                self.fail('ERROR', 'Unknown value for self.component_to_install: \'%s\'' %self.component_to_install)


            self.suRestartMaxSet = eval(self.suRestartMaxSet)
            if self.suRestartMaxSet == True:
                result = self.comsa_lib.setComSaSuRestartMax(False, int(self.suRestartMaxValue))
                self.fail(result[0], result[1])

            if self.createBackup == 'True':
                result = self.safLib.isBackup(self.backupName)
                if result[0] != 'SUCCESS':
                    self.fail(result[0], result[1])
                elif result != ('SUCCESS','NOT EXIST'):
                    result = self.safLib.backupRemove(self.backupName)
                    if result[0] != 'SUCCESS':
                        self.fail(result[0], result[1])
                result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
                self.fail(result[0], result[1])
                self.testSuiteConfig['restoreBackup'] = self.backupName
        else:
            self.logger.info('Skipped trace tests because of COMSA version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True
        #coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")

    def tearDown(self):
        self.setTestStep('tearDown')
        #coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
