#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
###############################################################################
#
# Ericsson AB 2014 All rights reserved.
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
import re
import os
from java.lang import System
import omp.tf.misc_lib as misc_lib


class FTMr27359(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.test_config = testConfig
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        self.testcase_tag = tag

        self.findActiveController = "True"
        self.doSwitchover = "False"

        self.reqComSaVersion = "R5A05"
        self.reqComSaMajorVersion = "5"
        self.reqComVersion = "R1A02"
        self.reqComSaRelease = "3"
        self.reqComRelease = "3"

        # Build and test a debug ComSA
        self.buildDebugComSA = "False"
        # Test all domaines after a com restart
        self.domainTest = "False"

        self.restoreCmwBackup = "False"
        self.restoreCmwBackupName = "cmw_autobackup"

        self.installTraceEA = "False"
        self.uninstallTraceEA = "False"
        self.installTraceCC = "False"
        self.uninstallTraceCC = "False"

        self.createInitBackup = "False"
        self.createBackupWithTrace = "False"
        self.createInitBackupWithTrace = "False"
        self.restoreInitBackup = "False"
        self.restoreBackupWithTrace = "False"

        self.initBackupName = 'Mr27359_init_backup'
        self.backupWithTrace = 'Mr27359_backup_with_trace'

        self.makeIndependentSwitchover = "False"

        self.disableComSaTrace = "False"

        self.comRestartToGenerateTraces = "False"

        self.testSkipped = False
        self.restoreBackupSucceeded = False
        self.tmpMrDirOnTarget = '/home/release/MR27359'
        self.traceEaBinOnTarget = '%s/trace_ea' %self.tmpMrDirOnTarget
        self.traceCcBinOnTarget = '%s/trace_cc' %self.tmpMrDirOnTarget
        self.comSaBinOnTarget = '%s/com_sa' %self.tmpMrDirOnTarget

        self.traceEaBinariesOnTarget = False
        self.traceCcBinariesOnTarget = False

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToTraceEa = dict.get('PATH_TO_TRACE_EA')
        self.pathToTraceCc = dict.get('PATH_TO_TRACE_CC')
        self.TRACE_EA_RT_COMMON_CXP_NUMBER = dict.get("TRACE_EA_RT_COMMON_CXP_NUMBER")
        self.TRACE_EA_RT_SC_CXP_NUMBER = dict.get("TRACE_EA_RT_SC_CXP_NUMBER")
        self.TRACE_EA_DT_CXP_NUMBER = dict.get("TRACE_EA_DT_CXP_NUMBER")
        self.TRACE_CC_RT_COMMON_CXP_NUMBER = dict.get("TRACE_CC_RT_COMMON_CXP_NUMBER")
        self.TRACE_CC_RT_SC_CXP_NUMBER = dict.get("TRACE_CC_RT_SC_CXP_NUMBER")
        self.TRACE_CC_DT_CXP_NUMBER = dict.get("TRACE_CC_DT_CXP_NUMBER")
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.resourceFilesLocation = dict.get("PATH_TO_MR27359")
        self.buildDir = dict.get('BUILD_TOKENS')
        self.buildLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("SRC"))
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.comSaRPMorig = dict.get('CXP_SDP_NAME_RHEL')
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get("RELEASE_RHEL"))
        else:
            self.comSaRPMorig = dict.get('CXP_SDP_NAME')
            self.cxpSdpName = dict.get('CXP_SDP_NAME')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get("RELEASE"))
        self.comBackupName = {}
        self.noOfScs = len(self.testConfig['controllers'])
        if self.noOfScs == 2:
            self.comSaInstall = self.installSdpName
        elif self.noOfScs == 1:
            self.comSaInstall = self.installSdpNameSingle

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.numberOfSCs = len(self.testConfig['controllers'])
        self.numberOfPLs = len(self.testConfig['payloads'])

        self.comsaDomainsShortListDebug = ['com_ericsson_common_comsa:', 'com_ericsson_common_comsa_imm_oi:', \
                                      'com_ericsson_common_comsa_imm_om:', 'com_ericsson_common_comsa_mwsa:', 'com_ericsson_common_comsa_mwsa_log:', \
                                      'com_ericsson_common_comsa_mwsa_general:', 'com_ericsson_common_comsa_mwsa_trace:', \
                                      'com_ericsson_common_comsa_mwsa_replist:', 'com_ericsson_common_comsa_imm:', 'com_ericsson_common_comsa_mwsa_ac:', \
                                      'com_ericsson_common_comsa_oamsa:', 'com_ericsson_common_comsa_oamsa_cmevent:', 'com_ericsson_common_comsa_oamsa_alarm:', \
                                      'com_ericsson_common_comsa_oamsa_translations:', 'com_ericsson_common_comsa_pmtsa_event:', 'com_ericsson_common_comsa_oiproxy:']

        self.comsaDomainsShortList = ['com_ericsson_common_comsa:', 'com_ericsson_common_comsa_imm_oi:', \
                                      'com_ericsson_common_comsa_imm_om:', 'com_ericsson_common_comsa_mwsa:', 'com_ericsson_common_comsa_mwsa_log:', \
                                      'com_ericsson_common_comsa_mwsa_replist:',  \
                                      'com_ericsson_common_comsa_oamsa:', 'com_ericsson_common_comsa_oamsa_cmevent:', \
                                      'com_ericsson_common_comsa_oamsa_translations:', 'com_ericsson_common_comsa_oiproxy:']

        self.comsaEventsShortList = ['COMSA_ERROR:', 'COMSA_WARNING:', 'COMSA_LOG:', 'COMSA_DEBUG:']

        self.comsaEventsShortListEnterLeave = ['COMSA_ENTER:', 'COMSA_LEAVE:']

        self.unUsedDomains =['com_ericsson_common_comsa_mwsa_general:', 'com_ericsson_common_comsa_imm:', \
                             'com_ericsson_common_comsa_mwsa_trace:', 'com_ericsson_common_comsa_oamsa_alarm:', 'com_ericsson_common_comsa_pmtsa_event:']

        self.unExpectedDomains = ['com_ericsson_common_comsa_undefined:']

        self.topTraceDomain = 'com_ericsson_common_comsa' # this is the most generic domain, which includes all COM SA sub-domains.
        self.lowestTraceLevel = '14'
        self.testString = "COMSA TEST:"
        self.testFunctionName = "mafLCMinit"

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        self.sdpNames = [self.cxpSdpName, self.installSdpName, self.installSdpNameSingle, self.removeSdpName, self.removeSdpNameSingle]

        self.restoreBackup = False
        if self.restoreInitBackup == "True":
            self.restoreBackupName = self.initBackupName
            self.restoreBackup = True
        elif self.restoreBackupWithTrace == "True":
            self.restoreBackupName = self.backupWithTrace
            self.restoreBackup = True

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.myLogger.info('Exit setUp')


    def runTest(self):
        self.setTestStep('runTest')

        if self.makeIndependentSwitchover == "True" and len(self.testConfig['controllers']) == 2:
            self.switchOver()


        # The following "offlineVersion" solution is needed for the regtest runs:
        # In the regtest it is needed to check the COM SA version to be able to decide if the suite (containing this testcase) need to be run or not.
        # The offline version checking is needed because in some testcases COM SA is not installed on the system, but still it is needed to check its version.
        # To get the offline version, the offline values are read from a previous save (setUpTestcase).
        # If the offlineVersions is not available then it means that the current TC run is not part of the regtest (e.g. running the MR27359 suite separately).
        # Note: if running this TC separately (as single TC or in MR27359 suite, then the it is considered as a manual run where the user knows that the COM SA version is correct)
        #       that means: if not in regtest then do not check the COM SA versions.
        offlineVersion = ['','','']
        ComsaOK = ['', False]
        ComsaMajorOK = ['', False]

        result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'COMSA')
        if result[0] == "REGTEST":
            offlineVersion[0] = result[1]
            offlineVersion[1] = result[2]
            offlineVersion[2] = result[3]
            ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion, offlineVersion)
            self.fail(ComsaOK[0],ComsaOK[1])
            ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion, offlineVersion)
            self.fail(ComsaMajorOK[0],ComsaMajorOK[1])
        else:
           ComsaOK[1] = True
           ComsaMajorOK[1] = True

        if ComsaOK[1] and ComsaMajorOK[1]:
            self.myLogger.info('Component versions OK, starting tests.')

            createBackup = False
            if self.createInitBackup == 'True':
                backupName = self.initBackupName
                createBackup = True
            elif self.createInitBackupWithTrace == 'True':
                backupName = self.backupWithTrace
                createBackup = True
            if createBackup:
                self.setTestStep('Create backup %s' %backupName)
                self.backupSystem(backupName)

            if self.restoreCmwBackup == 'True':
                result = self.comsa_lib.restoreSystem(self, self.restoreCmwBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 1, removeBackup = False)
                self.fail(result[0], result[1])

            # The tests will be executed here
            if self.buildDebugComSA == "True":
                self.installDebugComSa()

            sdpListTraceEa = [self.TRACE_EA_RT_COMMON_CXP_NUMBER, self.TRACE_EA_RT_SC_CXP_NUMBER, self.TRACE_EA_DT_CXP_NUMBER]
            sdpListTraceCc = [self.TRACE_CC_RT_COMMON_CXP_NUMBER, self.TRACE_CC_RT_SC_CXP_NUMBER, self.TRACE_CC_DT_CXP_NUMBER]

            if self.installTraceEA == "True":
                self.setTestStep('Install Trace EA')
                result = self.trace_lib.installTraceComp(self.testConfig, self.pathToTraceEa, self.traceEaBinOnTarget, sdpListTraceEa, 'traceEa', rollingUpgrade = True)
                self.fail(result[0], result[1])

            if self.installTraceCC == "True":
                self.setTestStep('Install Trace CC')
                result = self.trace_lib.installTraceComp(self.testConfig, self.pathToTraceCc, self.traceCcBinOnTarget, sdpListTraceCc, 'traceCc')
                self.fail(result[0], result[1])

            if self.createBackupWithTrace == "True":
                self.setTestStep('Backup system with Trace')
                self.backupSystem(self.backupWithTrace)

            # In some cases it is must to skip the active controller checking:
            #    when COM SA is not installed before this TC run e.g. this TC was run after installing CoreMW only.
            if self.findActiveController == "True":
                self.setTestStep('Find active controller')
                result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                self.activeController = result[1]

            if self.installStressTool:
                self.setTestStep('======== Install the stress tool ========')
                self.comsa_lib.installStressToolOnTarget(self)
                self.setTestStep('======== Start the stress tool ========')

                # Determine the number of processor cores in the node
                res = self.comsa_lib.getNumOfCPUsOnNode(self)
                self.fail(res[0],res[1])
                numOfCpuCores = res[1];
                self.myLogger.debug('Found %s CPU cores' %numOfCpuCores)

                # Determine the total physical RAM in the node
                res = self.comsa_lib.getBytesOfRamOnNode(self)
                self.fail(res[0],res[1])
                totalRamBytes = res[1];
                tenPercentOfTotalRam = int(totalRamBytes) // 10
                self.myLogger.debug('Found total %s bytes of RAM, 10 percent is %s' %(totalRamBytes, tenPercentOfTotalRam))

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, no disk stress
                #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 0, 0)

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
                res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus NFS disk stress, no local disk stress
                #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            # Test the special debug build of ComSA
            if self.buildDebugComSA == "True":
                self.testTraceDebug()
            # Test Domaines after a COMSA restart
            if self.domainTest == "True":
                self.testTraceDomaines()
            # Test Switchover
            if self.doSwitchover == "True" and len(self.testConfig['controllers']) == 2:
                self.testTraceSwitchOver()

            comment = """
            Uninstallation of Trace EA nd Trace CC is currently not working and therefore the uninstallation methods
            need to be changed to a backup restore.
            if self.uninstallTraceCC == "True":
                self.setTestStep('Un-Install Trace CC')
                result = self.trace_lib.uninstallTraceComp(self.testConfig, None, self.traceCcBinOnTarget, sdpListTraceCc, 'traceCc', skipGeneratingCampaign = True)
                self.fail(result[0], result[1])

            if self.uninstallTraceEA == "True":
                self.setTestStep('Un-Install Trace EA')
                result = self.trace_lib.uninstallTraceComp(self.testConfig, None, self.traceEaBinOnTarget, sdpListTraceEa, 'traceEa', skipGeneratingCampaign = True, rollingUpgrade = True)
                self.fail(result[0], result[1])
            """

            if self.installStressTool:
                self.setTestStep('======== Stopping the stress tool on target ========')
                self.comsa_lib.stopStressToolOnTarget(self)

            if self.restoreBackup:
                self.setTestStep('Restore system from backup %s' %self.restoreBackupName)
                if self.restoreBackupName == self.initBackupName:
                    result = self.comsa_lib.restoreSystem(self, self.restoreBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                elif self.restoreBackupName == self.backupWithTrace:
                    result = self.comsa_lib.restoreSystem(self, self.restoreBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 5, removeBackup = False)
                self.fail(result[0], result[1])
                self.restoreBackupSucceeded = True

            coreTestCase.CoreTestCase.runTest(self)

        else:
            self.logger.info('Skipped MR 27359 tests because of COMSA and/or COM version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.testSkipped = True

        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        if self.restoreBackup and self.restoreBackupSucceeded == False and self.testSkipped == False:
            if self.restoreBackupName == self.initBackupName:
                result = self.comsa_lib.restoreSystem(self, self.restoreBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
            elif self.restoreBackupName == self.backupWithTrace:
                result = self.comsa_lib.restoreSystem(self, self.restoreBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 5, removeBackup = False)
            self.fail(result[0], result[1])

        if self.doSwitchover == "True" and len(self.testConfig['controllers']) == 2:
            result = self.safLib.checkClusterStatus()
            if result != ('SUCCESS', 'Status OK'):
                result = self.comsa_lib.restoreSystem(self, self.backupWithTrace, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 5, removeBackup = False)
                self.fail(result[0], result[1])
                self.fail('ERROR', 'cmw-status command did not return Status OK. Restore to backup with enabled traces was performed.')

        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info("exit runTest")

        ###########################################################################################################################
        #######################                        Support Methods                  ###########################################
        ###########################################################################################################################

    def findComBackup(self):
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
            self.logger.info('findComBackup: Exit')
            self.fail('ERROR', 'findComBackup: COM backup not found!')
        self.logger.info('findComBackup: Exit')
        return combackupName

    def backupSystem(self, backupName):
        self.myLogger.debug('enter backupSystem')
        result = self.safLib.isBackup(backupName)
        self.fail(result[0], result[1])
        if result != ('SUCCESS','NOT EXIST'):
            result = self.safLib.backupRemove(backupName)
            self.fail(result[0], result[1])

        result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.myLogger.debug('leave backupSystem')

    def installDebugComSa(self):
        # Build ComSa debug version
        self.setTestStep('Build Debug ComSA')
        self.myLogger.info('Build Debug COMSA, starting.')

        # Get a build token
        for i in range(self.numberOfGetTokenRetries):
            result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            if result[0] == 'SUCCESS':
                break
        self.fail(result[0],result[1])

        makeOption = 'CFLAGS=-DBUILD_WITH_TRACE_TESTS CXXFLAGS=-DBUILD_WITH_TRACE_TESTS'
        if self.linuxDistro == self.distroTypes[1]: # rhel
            makeOption = 'CFLAGS=-DBUILD_WITH_TRACE_TESTS CXXFLAGS=-DBUILD_WITH_TRACE_TESTS rhel_sdp'
        result = self.comsa_lib.buildCOMSA(self.buildLocation, self.buildRelease, self.noOfScs, self.sdpNames, makeOption)
        self.fail(result[0], result[1])
        self.myLogger.info('Save the needed SDP files')
        # First create the directory comsa that is required
        cmd = 'mkdir -p %s/comsa' %self.resourceFilesLocation
        result = misc_lib.execCommand(cmd)
        self.fail(result[0], result[1])

        result = misc_lib.execCommand("ls %s/%s | awk -F'/' '{print $NF}'" %(self.buildRelease,self.comSaRPMorig))
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', result[1])
        self.comSaRPMorig = result[1].rstrip()
        result = self.comsa_lib.copyFilesToTarget( ['%s/%s' %(self.buildRelease, self.comSaInstall), \
                                                    '%s/%s' %(self.buildRelease,  self.comSaRPMorig) ], self.comSaBinOnTarget)
        self.fail(result[0], result[1])

        # Release the build token
        result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
        self.fail(result[0],result[1])

        # Find the latest COM backup
        self.myLogger.debug('Restore the COM backup ')
        self.setTestStep('Restore the COM backup')
        self.comBackupName = self.findComBackup()
        result = self.comsa_lib.restoreSystem(self, self.comBackupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 2, removeBackup = False)
        self.fail(result[0],result[1])

        # Install the sdp for ComSa on target
        self.setTestStep('Install Debug COMSA')
        result = self.comsa_lib.installComp(self.comSaBinOnTarget, self.comSaRPMorig, self.comSaInstall, backupRpms = self.backupRpmScript)
        self.fail(result[0],result[1])

    def testTraceDomaines(self):
        self.setTestStep('Test of All Domains in COMSA')
        traceDomain = self.topTraceDomain
        traceLevel = self.lowestTraceLevel
        traceObj = self.trace_cc_lib.TraceCC(traceDomain, traceLevel)
        # We restart COM in order to generate trace entries for COM SA.
        # Most domains should be touched by this operation
        self.setTestStep('Restart COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        self.fail(result[0], result[1])

        for domain in self.comsaDomainsShortList:
            self.setTestStep('Analyze %s '%domain)
            result = traceObj.matchDomainAndTestString('', '' , domain, '')
            self.fail(result[0], result[1])
        # Check for the unExpectedDomains domain
        for domain in self.unExpectedDomains:
            self.setTestStep('Analyze %s '%(domain))
            result = traceObj.matchNoDomain(domain)
            self.fail(result[0], result[1])


    def testTraceDebug(self):
        self.setTestStep('Enable COM SA trace')
        traceDomain = self.topTraceDomain
        traceLevel = self.lowestTraceLevel
        traceObj = self.trace_cc_lib.TraceCC(traceDomain, traceLevel)
        # We restart COM in order to generate trace entries for COM SA.
        # Most domains should be touched by this operation
        self.setTestStep('Restart COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        self.fail(result[0], result[1])

        string = self.testString
        functionName = self.testFunctionName
        for domain in self.comsaDomainsShortListDebug:
            for event in self.comsaEventsShortList:
                self.setTestStep('Analyze %s, %s '%(domain, event))
                result = traceObj.matchDomainAndTestString(string, event, domain, functionName)
                self.fail(result[0], result[1])
        # Now check the list comsaEventsShortListEnterLeave
        string = ""
        for domain in self.comsaDomainsShortListDebug:
            for event in self.comsaEventsShortListEnterLeave:
                self.setTestStep('Analyze %s, %s '%(domain, event))
                result = traceObj.matchDomainAndTestString(string, event, domain, functionName)
                self.fail(result[0], result[1])

        # Check for the unExpectedDomains domain
        comment = """ This is commented out because in the special build we even print the undefined domain.
        Either: 1. The special build does not produce the undefined trace
        Or:     2. The test cases does not fail if the undefined trace is produced.
        We chose case 2 and disable this code

        for domain in self.unExpectedDomains:
            self.setTestStep('Analyze %s '%(domain))
            result = traceObj.matchNoDomain(domain)
            self.fail(result[0], result[1])
        """

    def testTraceSwitchOver(self):
            """
            In case of a switchover we enable the traces, do a switchover and then re-run the same tests.
            """
            self.setTestStep('Enable COM SA trace')
            traceDomain = self.topTraceDomain
            traceLevel = self.lowestTraceLevel
            traceObj = self.trace_cc_lib.TraceCC(traceDomain, traceLevel)
            self.setTestStep('Do a switchover')
            self.switchOver()
            self.setAdditionalResultInfo('After COM SA switchover')
            # We restart COM in order to generate trace entries for COM SA.
            # Most domains should be touched by this operation
            self.setTestStep('Restart COM')
            result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
            self.fail(result[0], result[1])

            for domain in self.comsaDomainsShortList:
                self.setTestStep('Analyze %s '%domain)
                result = traceObj.matchDomainAndTestString('', '' , domain, '')
                self.fail(result[0], result[1])
            # Check for the unExpectedDomains domain
            for domain in self.unExpectedDomains:
                self.setTestStep('Analyze %s '%(domain))
                result = traceObj.matchNoDomain(domain)
                self.fail(result[0], result[1])


    def switchOver (self):
        self.setTestStep('Switch over')

        activeController = 0
        standbyController = 0

        controllers = self.testConfig['controllers']
        self.myLogger.info('Checking HA state for Com SA on the controllers')
        for controller in controllers:
            result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            if result[1] == 'ACTIVE':
                activeController = controller[1]
                self.myLogger.info('Found active controller: %s' %str(controller))
            elif result[1] == 'STANDBY':
                standbyController = controller[1]
                self.myLogger.info('Found standby controller: %s' %str(controller))

        if activeController == 0:
            self.fail('ERROR', 'No controller found with active instance of ComSa')
        elif standbyController == 0:
            self.fail('ERROR', 'No controller found with standby instance of ComSa.')


        self.setTestStep('Get ComSa DN and lock ')

        result = self.comsa_lib.lockSu(controller[0], activeController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck)
        self.fail(result[0], result[1])


        self.setTestStep('Verify that the former standby SC became active ')

        result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], standbyController, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        if result[1] != 'ACTIVE':
            self.fail(result[0], 'The former standby controller did not become active after the former active controller was locked.')

        self.myLogger.info('The former standby controller became active')
        oldActiveController = activeController
        activeController = standbyController
        standbyController = 0


        self.setTestStep('Unlock the locked SC')

        result = self.comsa_lib.unlockSu(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck)
        self.fail(result[0], result[1])
        self.myLogger.info('%s' %str(result[1]))


        self.setTestStep('Verify that the former active SC becomes standby.')

        result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        if result[1] != 'STANDBY':
            self.fail(result[0], 'The former active controller did not become standby after the sericeUnit was unlocked.')

        self.activeController = (controller[0], activeController)

        self.myLogger.info('The former active controller became standby')


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
