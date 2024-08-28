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

    Tag: TC-MISC-005

    Id:  Setup test case
    Help: This is not a real test case, but a test case that prepares the cluster for testing, like setting the SuRestartMax to 1000, creating a backup \
    and copying some files needed for the core dumps backtrace
    ""
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
from se.ericsson.jcat.fw import SUTHolder
import os
import sys
import re

from java.lang import System

class SetUpTestCase(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.testcase_tag = tag
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.suRestartMaxSet = 'False'
        self.toDefault = ''
        self.value = ''
        self.operation = ''
        self.pathRelToRep = ''
        self.pathLocalMachine = ''
        self.createBackup = 'False'
        self.backupName = ''
        self.setUpTest = ''
        self.tearDownTestCase = 'False'
        self.emailList = 'COMSA_internal'
        self.swSource = 'COMSA_internal'

        self.comsaMr31872MajorVer = '5'
        self.comsaMr31872Release = '3'
        self.comsaMr31872Version = "R5A08"

        self.imm_input_1 = {}
        self.imm_expected_output_1 = {}
        self.imm_nonexpected_output_1 = {}
        self.imm_input_2 = {}
        self.imm_expected_output_2 = {}
        self.imm_nonexpected_output_2 = {}
        self.imm_input_3 = {}
        self.imm_expected_output_3 = {}
        self.imm_nonexpected_output_3 = {}

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        self.coverageEnabled = False
        if self.testSuiteConfig.has_key('codeCoveredCheck'):
            self.coverageEnabled = eval(self.testSuiteConfig['codeCoveredCheck']['codeCoveredCheck'])

        dict = self.comsa_lib.getGlobalConfig(self)
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.uninstallScriptPath =  '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST"))
        self.tmpDirOnTarget = dict.get('AUTOINSTALL_DIR_TARGET')
        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.buildAbs = '%s%s' %(self.COMSA_REPO_PATH, dict.get('ABS'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.emailListFilePath = dict.get("PATH_TO_CONFIG_FILES")
        self.pathToKnownValgrindLeaks = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("VALGRIND_LEAKS_STORAGE"))
        # Check what Linux distribution is deployed on the target and
        # add the information to the test suite configuration
        self.distroTypes = eval(dict.get("LINUX_DISTRO_TYPES"))
        result = self.lib.updateLinuxDistroInDictionary(self.testSuiteConfig, self.distroTypes)
        self.fail(result[0], result[1])
        self.linuxDistro = self.testSuiteConfig['linuxDistro']['value']
        self.noOfScs = len(self.testConfig['controllers'])
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.uninstallScriptName = dict.get('UNINSTALL_SCRIPT_NAME_RHEL')
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.uninstallScriptName = dict.get('UNINSTALL_SCRIPT_NAME')
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        backupRpmScriptLocal = "%s%s%s" %(os.environ['MY_REPOSITORY'], dict.get("PATH_TO_CONFIG_FILES"), dict.get("BACKUP_RPMS_SCRIPT"))
        self.backupRpmScript = "/home/%s" % dict.get("BACKUP_RPMS_SCRIPT")
        # copy backup rpms script to cluster
        result = self.sshLib.remoteCopy(backupRpmScriptLocal, '/home/', timeout = 60)
        self.fail(result[0], result[1])
        cmd = 'chmod +x %s' % self.backupRpmScript
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.emailListFileName = ''
        if self.emailList == 'CCC_CI':
            self.emailListFileName = dict.get("EMAIL_LIST_CCC_CI")
        elif self.emailList == 'COMSA_internal':
            self.emailListFileName = dict.get("EMAIL_LIST")
        else:
            self.fail('ERROR', 'Email list not handled')

        self.installRoot = ''
        if self.swSource == 'COMSA_internal':
            self.installRoot = dict.get('JENKINUSER_R_INSTALL')
        elif self.swSource == 'CCC_CI':
            self.installRoot = dict.get('CCC_CI_R_INSTALL')
        else:
            self.fail('ERROR', 'Specified swSource: %s is not handled' %self.swSource)

        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        if self.memoryCheck:
            self.valgrindLogParser = '%s/%s/valgrindLogParser.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)

            logdir = System.getProperty("logdir")
            self.logDir=logdir.split("/")[len(logdir.split("/")) - 1]
            # remove all special character ex: (,),...
            self.logDir = re.sub('[^a-zA-Z0-9-_*.]', '', self.logDir)
            self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'] = '/cluster/valgrind_log/%s/' %self.logDir

        self.installSw = System.getProperty("installSw")
        self.buildComsa = System.getProperty("buildComSa")
        if self.swSource == 'CCC_CI':
            self.swDir = ''
        else:
            self.swDir = System.getProperty("swDirNumber")

        if self.coverageEnabled:
            self.covLocation = os.environ['COM_SA_RESULT'] # must be set beforehand to e.g. 'setenv COM_SA_RESULT /home/$USER/COV_COMSA'


        self.super__setUp()
        self.sutholder = SUTHolder.getInstance()
        self.currentSut = self.sutholder.zones[0]
        self.TargetDataLib = self.currentSut.getLibrary("TargetDataLib")
        self.targetData = self.TargetDataLib.getTargetData()

        """
        Stress Tool parameters here
        """
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.sync = 1
        self.numberOfvm = 1
        self.timeToExecuteSec = 600
        self.cpuLoad = 1
        self.memoryBytes = 1000000000

        self.resetCluster = System.getProperty("resetCluster")

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        options = ["True", "False"]
        if self.installSw not in options:
            self.fail('ERROR', 'Unknown value for self.installSw. If should be either True or False. It is: %s' %self.installSw)
        if self.buildComsa not in options:
            self.fail('ERROR', 'Unknown value for self.buildComsa. If should be either True or False. It is: %s' %self.buildComsa)

        sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
        self.updateLocalSshKeys(sshKeyUpdater)
        # check for compile errors first before proceeding
        if self.coverageEnabled:
            if self.setUpTest == 'True' and eval(System.getProperty("checkCompilerWarn")):
                self.myLogger.debug('Compile COMSA with coverage')
                result = self.comsa_lib.checkCOMSACompileWarnings(self.buildSrc, self.buildTokenDir, makeOption = 'coverage')
                if result[0] != 'SUCCESS':
                    self.myLogger.error(result[1])
                    # send email
                    self.comsa_lib.emailReport(self, True).send("COMPILER WARNINGS", self.noOfScs)
                    """
                    We stop test execution here if the compilation gives warnings.
                    """
                    os._exit(1)
        else:
            if self.setUpTest == 'True' and eval(System.getProperty("checkCompilerWarn")):
                result = self.comsa_lib.checkCOMSACompileWarnings(self.buildSrc, self.buildTokenDir)
                if result[0] != 'SUCCESS':
                    self.myLogger.error(result[1])
                    # send email
                    self.comsa_lib.emailReport(self, True).send("COMPILER WARNINGS", self.noOfScs)
                    """
                    We stop test execution here if the compilation gives warnings.
                    """
                    os._exit(1)


        # email report of regtest
        if self.setUpTest == 'True':
            self.lib.refreshSshLibHandlesAllSCs(self.testConfig)
            if self.installSw == 'True' and self.coverageEnabled:
                self.localPathToSw = '%s%s/' %(self.installRoot, self.swDir)
                sdpNames = [self.cxpSdpName, self.installSdpName, self.installSdpNameSingle, self.removeSdpName, self.removeSdpNameSingle]
                # TODO: make coverage for rhel
                result = self.comsa_lib.reInstallComponents(self, self.buildComsa, self.buildSrc, self.buildRelease, sdpNames, self.localPathToSw, self.uninstallScriptPath, \
                                                            self.uninstallScriptName, self.testConfig, self.testSuiteConfig, self.buildTokenDir, sshKeyUpdater, \
                                                            destinationOnTarget = self.tmpDirOnTarget, resetCluster = self.resetCluster, makeOption='coverage')

                if result[0] != 'SUCCESS':
                    self.myLogger.error(result[1])
                    # send email
                    self.comsa_lib.emailReport(self, True).send("INSTALLATION FAILED", self.noOfScs)
                    """
                    We stop test execution here if the re-installation has failed.
                    It makes no sense to continue testing on a system that is not properly installed.
                    """
                    os._exit(1)
                else:
                    self.setAdditionalResultInfo('COM SA installation time was: %d seconds.' %result[1])
                    self.comsa_lib.addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'COM SA installation time', result[1])
                    self.logger.info('charMeasurements - COM SA installation time: %s' %str(result[1]))
                    self.testSuiteConfig['sdpFilesOnTarget'] = True

            elif self.installSw == 'True' and self.coverageEnabled == False:
                self.localPathToSw = '%s%s/' %(self.installRoot, self.swDir)
                sdpNames = [self.cxpSdpName, self.installSdpName, self.installSdpNameSingle, self.removeSdpName, self.removeSdpNameSingle]
                result = self.comsa_lib.reInstallComponents(self, self.buildComsa, self.buildAbs, self.buildRelease, sdpNames, self.localPathToSw, self.uninstallScriptPath, \
                                                            self.uninstallScriptName, self.testConfig, self.testSuiteConfig, self.buildTokenDir, sshKeyUpdater, \
                                                            destinationOnTarget = self.tmpDirOnTarget, resetCluster = self.resetCluster, useComsaBuild = True)

                if result[0] != 'SUCCESS':
                    self.myLogger.error(result[1])
                    # send email
                    self.comsa_lib.emailReport(self, True).send("INSTALLATION FAILED", self.noOfScs)
                    """
                    We stop test execution here if the re-installation has failed.
                    It makes no sense to continue testing on a system that is not properly installed.
                    """
                    os._exit(1)
                else:
                    self.setAdditionalResultInfo('COM SA installation time was: %d seconds.' %result[1])
                    self.comsa_lib.addDataToTestSuiteConfig(self.testSuiteConfig, 'charMeasurements', 'COM SA installation time', result[1])
                    self.logger.info('charMeasurements - COM SA installation time: %s' %str(result[1]))
                    self.testSuiteConfig['sdpFilesOnTarget'] = True
            """
            We want to send an email only in case of a real test suite.
            The test case can be used as a stand-alone test case to re-install the cluster
            and in that case we do not need to send an automatic email about a started test run.
            The if statement below checks if there are at least two test cases in the test suite.
            """
            if self.testSuiteConfig.has_key('testcase2'):
                self.comsa_lib.emailReport(self, True).send("STARTED", self.noOfScs)

        # Printout useful information to the JCAT report page:
        #    - Target name
        #    - SW configuration on the target

        if 2 == self.noOfScs:
            self.setAdditionalResultInfo("Target name: %s -Dual Node\n\n" %(self.targetData['target']))
        elif 1 == self.noOfScs:
            self.setAdditionalResultInfo("Target name: %s - One Node\n\n" %(self.targetData['target']))
        else:
            self.setAdditionalResultInfo("Target name: %s - Unknown Node\n\n" %(self.targetData['target']))

        self.setAdditionalResultInfo("Source commitID: %s\n\n" %os.environ['COMSA_REPO_PATH_COMMIT_ID'])
        self.setAdditionalResultInfo("Verification commitID: %s\n\n" %os.environ['COMSA_VERIFICATION_COMMIT_ID'])

        result = self.sshLib.sendCommand('cmw-repository-list')
        self.fail(result[0], result[1])
        self.setAdditionalResultInfo('SW configuration on the target:')
        for line in result[1].splitlines():
            self.setAdditionalResultInfo(line)
        result = self.sshLib.sendCommand("cluster info | egrep -v '(Installation Type:)|(Source info:)'")
        self.fail(result[0], result[1])
        self.setAdditionalResultInfo('Operating system information:')
        for line in result[1].splitlines():
            self.setAdditionalResultInfo(line)

        self.suRestartMaxSet = eval(self.suRestartMaxSet)
        if self.suRestartMaxSet == True:
            self.toDefault = eval(self.toDefault)
            if 'int' in str(type(eval(self.value))):
                self.value = eval(self.value)
            result = self.comsa_lib.setComSaSuRestartMax(self.toDefault, self.value)
            self.fail(result[0], result[1])

        # save the installed COM SA version for using it in other testcases in the regtest suite.
        result = self.lib.getComponentVersion(self.comsaCxpNumber)
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])

        if self.testSuiteConfig.has_key('releases'):
            self.testSuiteConfig['releases']['COMSA'] = {'release': str(result[1]), 'version': str(result[2]), 'majorVersion': str(result[3])}
        else:
            self.testSuiteConfig['releases'] = {}
            self.testSuiteConfig['releases']['COMSA'] = {'release': str(result[1]), 'version': str(result[2]), 'majorVersion': str(result[3])}

        # save the installed COM version for using it in other testcases in the regtest suite.
        if self.testSuiteConfig['linuxDistro']['value'] == 'RhelType':
            result = self.lib.getComponentVersion('CXP9026454')
        else:
            result = self.lib.getComponentVersion('CXP9017585')

        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])
        self.testSuiteConfig['releases']['COM']=  {'release': str(result[1]), 'version': str(result[2]), 'majorVersion': str(result[3])}

        # save the installed Core MW version for using it in other testcases in the regtest suite.
        result = self.lib.getComponentVersion('CXP9017566')
        if result[0] != 'SUCCESS':
            self.fail(result[0], result[1])
        self.testSuiteConfig['releases']['COREMW'] =  {'release': str(result[1]), 'version': str(result[2]), 'majorVersion': str(result[3])}

        if self.operation != '':
            if self.operation == 'copy':
                repo = ''
                if eval(self.pathRelToRep) == True:
                    repo = os.environ['MY_REPOSITORY']
                fileList = eval(self.pathLocalMachine)
                result = self.sshLib.sendCommand('mkdir -p %s' %self.pathOnTarget)
                self.fail(result[0], result[1])
                for file in fileList:
                    result = self.sshLib.remoteCopy('%s/%s' %(repo, file), self.pathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                    result = self.sshLib.sendCommand('chmod +x %s/%s' %(self.pathOnTarget, file.split('/')[len(file.split('/'))-1]))
                    self.fail(result[0], result[1])
            elif self.operation == 'remove':
                if 'list' in eval(self.pathOnTarget):
                    fileList = eval(self.pathOnTarget)
                    for file in fileList:
                        cmd = '\\rm -f %s' %file
                        self.sshLib.sendCommand(cmd)
                else:
                    self.fail('ERROR', 'self.pathOnTarget has to be a list. Received %s' %self.pathOnTarget)

                cmd = '\\rm -f %s' %self.pathOnTarget
                self.sshLib.sendCommand(cmd)

        if self.memoryCheck and self.setUpTest == 'True':
            self.setTestStep('Installing and activating Valgrind')
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])


        if self.createBackup == 'True':
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
            self.fail(result[0], result[1])
            self.testSuiteConfig['restoreBackup'] = self.backupName


        # Verification of MR 31872
        ComsaOK = self.lib.checkComponentVersion('comsa', self.comsaMr31872Release, self.comsaMr31872Version)
        self.fail(ComsaOK[0],ComsaOK[1])
        ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.comsaMr31872Release, self.comsaMr31872MajorVer)
        self.fail(ComsaMajorOK[0],ComsaMajorOK[1])

        if ComsaOK[1] and ComsaMajorOK[1]:
            self.verifySgAutoRepairValue()
        # End of verification of MR 31872

        if self.tearDownTestCase == 'True' and self.memoryCheck:
            for controller in self.testConfig['controllers']:
                result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                self.fail(result[0],result[1])

        if self.installStressTool:
            self.comsa_lib.installStressToolOnTarget(self)

        #coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")

    def tearDown(self):
        self.setTestStep('tearDown')
        if self.tearDownTestCase == 'True' and self.memoryCheck:
            result = self.sshLib.remoteCopy(self.valgrindLogParser, self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'], timeout = 60)
            self.fail(result[0],result[1])

            logParserFileName = self.valgrindLogParser.split("/")[len(self.valgrindLogParser.split("/")) - 1]
            result = self.sshLib.sendCommand('chmod +x %s/%s'%(self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'], logParserFileName))
            self.fail(result[0], result[1])

            origTimeout = self.sshLib.getTimeout()
            newTimeout=1800
            self.sshLib.setTimeout(newTimeout)
            result = self.sshLib.sendCommand("bash -c 'pushd %s/; ./%s; popd'"%(self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'], logParserFileName))
            self.fail(result[0], result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            elif 'Permission denied' in result[1]:
                self.fail('ERROR', result[1])
            self.setAdditionalResultInfo("Valgrind logs can be found under: %s." %self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.sshLib.setTimeout(origTimeout)

            result = self.comsa_lib.findNewLeaks(self.pathToKnownValgrindLeaks, self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        # email report of regtest
        if self.tearDownTestCase == 'True':
            self.displayCharMeasInfo()
            self.comsa_lib.emailReport(self, True).send("FINISHED", self.noOfScs)

        #coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

    def updateLocalSshKeys(self, sshKeyUpdater):
        self.logger.debug('enter updateLocalSshKeys')
        for controller in self.testConfig['controllers']:
            ipAddress = self.targetData['ipAddress']['ctrl']['ctrl%s'%str(self.testConfig['controllers'][self.testConfig['controllers'].index(controller)][1])]
            cmd = '%s %s' %(sshKeyUpdater, ipAddress)
            result = self.miscLib.execCommand(cmd)
        self.logger.debug('leave updateLocalSshKeys')

    def displayCharMeasInfo(self):
        self.logger.info('enter displayCharMeasInfo')

        if self.testSuiteConfig.has_key('charMeasurements'):
            self.setAdditionalResultInfo('=========================================================')
            self.setAdditionalResultInfo('Printing average characteristic time results for test report')
            self.setAdditionalResultInfo('==========================================================')
            for key in self.testSuiteConfig['charMeasurements']:
                self.logger.info('%s during the test suite: %s' %(key, str(self.testSuiteConfig['charMeasurements'][key])))
                ave_float=float((sum(self.testSuiteConfig['charMeasurements'][key]))/(float(len(self.testSuiteConfig['charMeasurements'][key]))))
                self.setAdditionalResultInfo('%s during the test suite: %0.2f' %(key, ave_float))

        self.logger.debug('leave displayCharMeasInfo')

    def verifySgAutoRepairValue(self):
        #Create the input, the expected output and the non-expected output lists for imm
        lists1 = self.comsa_lib.load_TC_imm_config(self)     #load imm_input
        if len(lists1) != 0:
            self.setTestStep('IMM Testing')

        #Send the imm commands and process the results element-by-element
        #One element of the list is one imm session.
        for list_index1 in range (0,len(lists1[0])):
           result = self.comsa_lib.runImmSession(lists1, list_index1)
           self.fail(result[0], result[1])

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
