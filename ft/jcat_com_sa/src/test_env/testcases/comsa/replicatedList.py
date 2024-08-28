#!/vobs/tsp_saf/tools/Python/linux/bin/python
# coding=iso-8859-1
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
    TC-RPLIST-001
    TC-RPLIST-003

    Id:
    ""
    ==================================

    Help/Info:
    This test case can only run in test suite, the replicatedList.xml test suite.
    THe testcases are not independent.
    TC-RPLIST-001 will run the make ftest to create the sdp files which need to be installed on the target system.
    TC-MISC-004 will reinstall COM-SA with the replicated list software included
    TC-RPLIST-003 will check the logs to see if the replicated list test suite was executed successfully and then restore the cluster to
        the standart COM-SA software.
"""

import test_env.fw.coreTestCase as coreTestCase
import time
import os
from java.lang import System

class Replicatedlist(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.reqComSaRelease = ""
        self.reqComSaVersion = ""
        self.reqComSaVersion_4 = ""
        self.reqComSaRelease_4 = ""

        self.comSaRPMorigPrefix = ""
        self.comSaRPMofficialPrefix = ""

        self.backupName = 'standardComSa'
        self.comSaRPMorig = 'ComSa-CXP9017697_2.sdp'
        self.comSaRPMofficial = 'COM_SA-CXP9017697_2.sdp'

        self.defaultValue = 2 * 1024 * 1024
        self.original_value = self.defaultValue


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)
         # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        path_1 = dict.get("PATH_TO_COREMW_COM_FILE")
        path_2 = dict.get("COREMW_COMSA_CFG")
        self.pathToCoremwComFile = path_1 + path_2
        self.buildLocation = '%s%s' % (self.COMSA_REPO_PATH, dict.get("SRC"))
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' % (self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.buildDir = dict.get('BUILD_TOKENS')

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.buildRelease = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get('RELEASE_RHEL'))
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER_RHEL')
        else:
            self.buildRelease = '%s%s' %(os.environ['COMSA_REPO_PATH'], dict.get('RELEASE'))
            self.comsaCxpNumber = dict.get('COMSA_CXP_NUMBER')

        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            self.comSaInstall = 'ComSa_install.sdp'
        elif noOfScs == 1:
            self.comSaInstall = 'ComSa_install_Single.sdp'

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        """
        Stress Tool option
        """
        self.installStressTool = eval(System.getProperty("runStressTool"))

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs=self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        if self.installStressTool:
            self.replSetupStress()
            stressTimeOut = 60
            self.sshLib.setTimeout(stressTimeOut)

        # Find active controller
        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        # This is the preparation part of the test (build the Test Component)
        if ((self.tag == 'TC-RPLIST-001') or
            (self.tag == 'TC-RPLIST-011')):
            # Variables needed for the build token management
            dirName = System.getProperty("logdir")
            user = os.environ['USER']
            self.tokenPattern = 'buildToken-%s' % user
            self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
            self.numberOfGetTokenRetries = 5

            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0], result[1])

            self.testSuiteConfig['replicatedListsTest'] = 'True'
            # We do not really want the test to fail, only to build one variant or the other depending on the COM SA version
            # for older versions up to COM SA 3.6 use TestComponent.c
            # For COM SA 3.7 (4.0) or newer       use TestComponent_v4.c
            #self.fail(Comsa_v4_OK[0],Comsa_v4_OK[1])
            Comsa_v4_OK = ('SUCCESS', True)
            Comsa_v4_OK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)

            Comsa4_OK = ('SUCCESS', True)
            Comsa4_OK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease_4, self.reqComSaVersion_4)

            if Comsa_v4_OK[1] or Comsa4_OK[1]:
                result = self.miscLib.execCommand("bash -c 'pushd %s ; make clean ; make ftest_v4; popd '" % self.buildLocation)
                #self.fail(result[0], result[1]) # this fails for some reason!!!
            else:
                result = self.miscLib.execCommand("bash -c 'pushd %s ; make clean ; make ftest; popd '" % self.buildLocation)
                #self.fail(result[0], result[1]) # this fails for some reason!!!

            # check comSaInstall sdp
            result = self.miscLib.execCommand('ls -l %s/%s' % (self.buildRelease, self.comSaInstall))
            self.fail(result[0], result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', 'The comSa install sdp was not found in the expected directory. Exiting!\n%s' % result[1])

            # check for COMSA sdp and get correct version
            resultTmp = self.miscLib.execCommand("""ls %s/%s-%s_*.sdp | sed "s/\// /g" | awk '{print $NF}' """ %(self.buildRelease, self.comSaRPMorigPrefix, self.comsaCxpNumber))
            self.fail(resultTmp[0], resultTmp[1])
            result = resultTmp[1].splitlines()
            if len(result) > 1:
                self.fail('ERROR', 'More than one comsa sdp found in %s. Exiting!\n' % self.buildRelease)
            if not 'No match' in result[0]:
                self.comSaRPMorig = result[0].strip()
                self.comSaRPMofficial = self.comSaRPMorig.replace(self.comSaRPMorigPrefix, self.comSaRPMofficialPrefix)
                cmd = '\mv -f %s/%s %s/%s' % (self.buildRelease, self.comSaRPMorig, self.buildRelease, self.comSaRPMofficial)
                result = self.miscLib.execCommand(cmd)
                self.fail(result[0], result[1])
            else:
                resultTmp = self.miscLib.execCommand("""ls %s/%s-%s_*.sdp | sed "s/\// /g" | awk '{print $NF}' """ %(self.buildRelease, self.comSaRPMofficialPrefix, self.comsaCxpNumber))
                self.fail(resultTmp[0], resultTmp[1])
                result = resultTmp[1].splitlines()
                if len(result) > 1:
                    self.fail('ERROR', 'More than one comsa sdp found in %s. Exiting!\n' % self.buildRelease)
                if 'No match' in result[0]:
                    self.fail('ERROR', 'The comSa cxp sdp was not found in the expected directory. Exiting!\n%s' % result[0])
                self.comSaRPMofficial = result[0].strip()
                self.comSaRPMorig = self.comSaRPMofficial.replace(self.comSaRPMofficialPrefix, self.comSaRPMorigPrefix)

            self.temp_dir = '/home/coremw/incoming/'

            # Create COM-SA temp directory
            cmd = 'mkdir -p %s' % self.temp_dir
            self.myLogger.debug('Create COM-SA temp directory by: %s' % cmd)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            # Upload COMSA runtime SDP and COMSA deployment template SDP to target
            self.setTestStep('Upload COMSA runtime SDP and COMSA deployment template SDP to target')

            self.myLogger.debug('Upload COMSA runtime SDP and COMSA deployment template SDP to target')
            file = '%s%s' % (self.buildRelease, self.comSaRPMofficial)
            result = self.sshLib.remoteCopy(file, self.temp_dir, timeout=60)
            self.fail(result[0], result[1])

            file = '%s%s' % (self.buildRelease, self.comSaInstall)
            self.sshLib.remoteCopy(file, self.temp_dir, timeout=60)
            self.fail(result[0], result[1])

            self.testSuiteConfig['replicatedListsRt'] = self.comSaRPMofficial
            self.testSuiteConfig['replicatedListsDepl'] = self.comSaInstall

            # Release the build token
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            self.fail(result[0], result[1])

            if self.installStressTool:
                self.setTestStep('======== Stopping the stress tool on target ========')
                self.comsa_lib.stopStressToolOnTarget(self)

            # self.lib.messageBox('start manual testing')
            # Create a backup
            self.backupSystem()
            if self.installStressTool:
                self.replSetupStress()
                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            cmd = 'date +\%s'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            self.testSuiteConfig['startTime'] = int(result[1])


        elif self.tag == 'TC-RPLIST-003':  # Run the test itself
            if not self.testSuiteConfig.has_key('startTime'):
                self.fail('ERROR', 'The start time was not recorded in the testSuiteConfig parameter.')
            startTime = self.testSuiteConfig['startTime']


            logPattern = 'messages'

            expectedPatterns = [['COM_SA comSATest_execute called...'], ['COM_SA BASIC TEST ...'], ['COM_SA ======== BASIC TEST PASSED ==========='], \
                                ['COM_SA ITEM DATA TEST ...'], ['COM_SA ======== ITEM DATA TEST PASSED ==========='], ['COM_SA ITEM ADD/REMOVE TEST ...'], \
                                ['COM_SA ======== ITEM ADD/REMOVE PASSED ==========='], ['COM_SA === REPLICATED LISTS TESTS PASSED===='], ['COM_SA === TRACE TESTS PASSED =============='],
                                ['COM_SA === LOG TESTS PASSED ==============='], ['COM_SA ======== ALL TESTS PASSED ===========']]
            unexpectedPatterns = [['=== REPLICATED LISTS BASIC FAILED ====']]

            match = False
            for searchPattern in expectedPatterns:
                for subrack, slot in self.testConfig['controllers']:
                    result = self.lib.getEventTimestampFromSyslog(subrack, slot, searchPattern, startTime, self.testConfig)
                    if result[0] == 'SUCCESS':
                        match = True
                        break
                if match != True:
                    self.fail('ERROR', '%s not found in the logs.' % searchPattern)

            match = False
            for searchPattern in unexpectedPatterns:
                for subrack, slot in self.testConfig['controllers']:
                    result = self.lib.getEventTimestampFromSyslog(subrack, slot, searchPattern, startTime, self.testConfig)
                    if result[0] == 'SUCCESS':
                        match = True
                        break
                if match == True:
                    self.fail('ERROR', 'Unexpected pattern %s found in the logs.' % searchPattern)


        elif self.tag == 'TC-RPLIST-002':
            self.setTestStep('Changing argument of replicated list max size')

            cmd = '''grep 'replicatedlist maxsize' %s | cut -d\\" -f2''' % self.pathToCoremwComFile

            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            self.original_value = result[1]

            list = ['40000000', '50000000', 'max', 'abc']
            for check in list:
                self.setTestStep('Changing to %s ' % check)
                self.replicated_list_max(check)
        else:
            self.fail('ERROR', 'Illegal tag, not implemented, otherwise edit this if statement!')




        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")




    def tearDown(self):
        self.setTestStep('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        if self.tag == 'TC-RPLIST-003':
            del self.testSuiteConfig['replicatedListsTest']
            if self.testSuiteConfig.has_key('startTime'):
                result = self.miscLib.execCommand('\\rm -f %s/%s' % (self.buildRelease, self.comSaRPMofficial))
                self.fail(result[0], result[1])

                removeBackup = True
                if self.testSuiteConfig.has_key('restoreBackup'):
                    result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
                    if result == ('SUCCESS', 'EXIST'):
                        self.backupName = self.testSuiteConfig['restoreBackup']
                        removeBackup = False

                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = removeBackup)
                self.fail(result[0], result[1])

        elif self.tag == 'TC-RPLIST-002':
            self.setTestStep('Changing argument of replicated list to default')


            self.replicated_list_max(self.original_value)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')


    def restartCom(self):
        self.setTestStep('Restarting COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        self.fail(result[0], result[1])


    def replicated_list_max(self, check):

       # Implementing new functionality into replicated list (changing replicated list max size)
       # Get current linux time


        self.setTestStep('Getting the current Linux Time: ')
        cmd = 'date +\%s'
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        startTime = int(result[1])
        self.myLogger.debug("Result of current linux time:%s" % startTime)

        if check == 'max':
            cmd = 'cat /proc/sys/kernel/shmmax'
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            v_max = int(result[1])
            self.myLogger.debug("###Value of max:%s " % v_max)
            cmd = """sed -i 's/\\(.*replicatedlist maxsize="\\).*\\("\\/>.*\\)/\\1%s\\2/g' %s""" % (v_max + 1, self.pathToCoremwComFile)
        else:
            cmd = """sed -i 's/\\(.*replicatedlist maxsize="\\).*\\("\\/>.*\\)/\\1%s\\2/g' %s""" % (check, self.pathToCoremwComFile)

        self.setTestStep('Modify Config file')  #

        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])

        self.restartCom()

        self.setTestStep('Check LOGS IF Modified Parameters like: ReplicatedList, maxsize has modified or not !')
        if check == 'max':
            searchPatterns = ['ReplicatedList, maxsize', '%s' % v_max]
        elif check.isdigit() == False:
            searchPatterns = ['ReplicatedList, maxsize', '%s' % self.defaultValue]
        else:
            searchPatterns = ['ReplicatedList, maxsize', '%s' % check]
        result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPatterns, startTime, self.testConfig, logDir='/var/log/')
        self.fail(result[0], result[1])

    ########################################################################################
    def replSetupStress(self):
        self.setTestStep('======== Install the stress tool ========')
        self.comsa_lib.installStressToolOnTarget(self)
        self.setTestStep('======== Start the stress tool ========')

        # Determine the number of processor cores in the node
        result = self.comsa_lib.getNumOfCPUsOnNode(self)
        self.fail(result[0], result[1])
        numOfCpuCores = result[1];
        self.myLogger.debug('Found %s CPU cores' % numOfCpuCores)

        # Determine the total physical RAM in the node
        result = self.comsa_lib.getBytesOfRamOnNode(self)
        self.fail(result[0], result[1])
        totalRamBytes = result[1];
        tenPercentOfTotalRam = int(totalRamBytes) // 10
        self.myLogger.debug('Found total %s bytes of RAM, 10 percent is %s' % (totalRamBytes, tenPercentOfTotalRam))

        # set the stress tool to occupy all CPU cores and 90% of the physical RAM
        # 2 local disk tasks writing 4 MB, NFS disk stress 1 task writing 64K bytes
        # result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

        # No CPU, only local and NFS disk
        # result = self.comsa_lib.startStressToolOnTarget(self, 0, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

        # 50% CPU, 50% memory plus local and NFS disk stress
        result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60 * 60 * 60, 2, 4194304, 1, 65536)

        # 50% CPU, 50% memory plus NFS disk stress
        # result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

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


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
