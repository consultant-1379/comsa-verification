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
import copy
import os
from java.lang import System


class FT665_Trace(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.comsaArea = ''
        self.comsaRepository = ''
        self.comsaBackup = ''
        self.comsaArea = ''
        self.comsaRepository = ''
        self.comsaConfig = ''
        self.comsaBackup = ''
        self.comConfig = ''
        self.enableOnly = ''
        self.disableOnly = ''
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        # parameters from the config files


    def id(self):
        return self.name


    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        coreTestCase.CoreTestCase.setUp(self)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.PERSISTENT_STORAGE_API= dict.get ("PERSISTENT_STORAGE_API")
        PERSISTENT_STORAGE_API_CONFIG="%s/config" %self.PERSISTENT_STORAGE_API
        PERSISTENT_STORAGE_API_CLEAR="%s/clear" %self.PERSISTENT_STORAGE_API
        PERSISTENT_STORAGE_API_NO_BACKUP="%s/no-backup" %self.PERSISTENT_STORAGE_API
        self.getClearLocationCmd = 'cat %s' %PERSISTENT_STORAGE_API_CLEAR
        self.getConfigLocationCmd = 'cat %s' %PERSISTENT_STORAGE_API_CONFIG
        self.getNoBackupLocationCmd = 'cat %s' %PERSISTENT_STORAGE_API_NO_BACKUP
        self.comsaDirUnderPso = 'comsa_for_coremw-apr9010555'
        self.comDirUnderConfig = 'com-apr9010443'
        self.comSaTraceConfig = 'com_sa_trace.conf'
        self.comSaTraceFile = 'com_sa.trace'
        self.comDebugFile = 'etc/com.debug'
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        if self.installStressTool:
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
            result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            # No CPU, only local and NFS disk
            #result = self.comsa_lib.startStressToolOnTarget(self, 0, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            # 50% CPU, 50% memory plus local and NFS disk stress
            #result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            # 50% CPU, 50% memory plus NFS disk stress
            #result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

            stressTimeOut = 60
            self.sshLib.setTimeout(stressTimeOut)

        self.setTestStep('### check if PSO is running on the cluster ###')
        result = self.comsa_lib.checkPso()
        self.fail(result[0],result[1])
        if result[1] == False:
            self.myLogger.info('The test system does not have PSO.')
            self.setAdditionalResultInfo('The test system does not have PSO. The test is not relevant.')
        elif result[1] == True:
            self.myLogger.info('The test system has PSO.')
            self.setTestStep('# Getting the PSO locations')
            # Getting the clear location:
            result = self.sshLib.sendCommand(self.getClearLocationCmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            clearLocation = result[1]
            self.comsaArea = '%s/%s' %(clearLocation, self.comsaDirUnderPso)


            # Getting the config location
            result = self.sshLib.sendCommand(self.getConfigLocationCmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            configLocation = result[1]
            self.comsaConfig = '%s/%s' %(configLocation, self.comsaDirUnderPso)
            self.comConfig = '%s/%s' %(configLocation, self.comDirUnderConfig)
            self.comSaTraceFileBackup = '%s/%s/%s' %(configLocation, self.comsaDirUnderPso, self.comSaTraceConfig)



            # Getting the no-backup location:
            result = self.sshLib.sendCommand(self.getNoBackupLocationCmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            noBackupLocation = result[1]
            self.comsaBackup = '%s/%s/backup' %(noBackupLocation, self.comsaDirUnderPso)

            # Check that the original (backup) com_sa_trace.conf file is in the system.
            cmd = 'ls %s' %self.comSaTraceFileBackup
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.setAdditionalResultInfo('######## WARNING ######## %s/%s not found on the target system.' %(self.comsaRepository, self.comSaTraceConfig))
                #self.fail('ERROR', '%s/%s not found on the target system.' %(self.comsaRepository, self.comSaTraceConfig))

            self.setTestStep('# Find active COM controller')
            # Find active COM controller
            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0],result[1])
            activeController = result[1]
            originalTraceConfigFile = '%s.orig' %self.comSaTraceConfig

            if self.disableOnly != 'True':
                self.setTestStep('### ENABLING TRACES ###')
                self.setTestStep('# Save the original trace config file')
                # Copy original trace config file
                cmd = '\cp %s/%s %s/%s' %(self.comsaArea, self.comSaTraceConfig, self.comsaArea, originalTraceConfigFile)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.setTestStep('# Create file with traces enabled')
                # Create file with traces enabled
                tracesEnabledConfigFile = '%s.enableAll' %(self.comSaTraceConfig)
                cmd = "sed 's/=disable/=enable/g' %s/%s > %s/%s" %(self.comsaArea, self.comSaTraceConfig, self.comsaArea, tracesEnabledConfigFile)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.setTestStep('# Replace original config file with file that has all traces on')
                # Replace original config file with file that has all traces on
                cmd = '\mv -f %s/%s %s/%s' %(self.comsaArea, tracesEnabledConfigFile, self.comsaArea, self.comSaTraceConfig)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])


                self.setTestStep('# Create com.debug file')
                # Create com.debug file
                cmd = 'touch %s/%s' %(self.comConfig, self.comDebugFile)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.setTestStep('# Save the time before restarting COM')
                # Save the time before restarting COM
                cmd = 'date +\%s'
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                timeBeforeComRestart = int(result[1])

                self.setTestStep('# Restart COM')
                # Restart COM
                result = self.comsa_lib.comRestart(self, activeController[0], activeController[1], self.memoryCheck)
                self.fail(result[0],result[1])

                self.setTestStep('# Wait a few seconds and then check that the com_sa.trace file is created.')
                # Wait a few seconds and then check that the com_sa.trace file is created.
                self.miscLib.waitTime(10)
                cmd = 'ls %s' %(self.comsaArea)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                if self.comSaTraceFile not in result[1]:
                    self.fail('ERROR', 'COM SA trace file not found under clear location.')

                self.setTestStep('# Check that there are new log entries in the COM SA trace file')
                # Check that there are new log entries in the COM SA trace file
                cmd = """tail -1 %s/%s | awk '{print $1" "$2}'""" %(self.comsaArea, self.comSaTraceFile)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                result = self.lib.timeConv(result[1])
                self.fail(result[0],result[1])
                timeOfLatestLog = result[1]
                if timeBeforeComRestart >= timeOfLatestLog:
                    self.fail('ERROR', 'The latest log entry in the COM SA trace file is not newer than the time the trace was enabled!')

            if self.enableOnly != 'True':
                self.setTestStep('### DISABLING TRACES ###')
                self.setTestStep('# Create file with traces disabled')
                # Create file with traces disabled
                tracesDisabledConfigFile = '%s.disableAll' %(self.comSaTraceConfig)
                cmd = "sed 's/=enable/=disable/g' %s/%s > %s/%s" %(self.comsaArea, self.comSaTraceConfig, self.comsaArea, tracesDisabledConfigFile)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.setTestStep('# Replace original config file with file that has all traces off')
                # Replace original config file with file that has all traces off
                cmd = '\mv -f %s/%s %s/%s' %(self.comsaArea, tracesDisabledConfigFile, self.comsaArea, self.comSaTraceConfig)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.setTestStep('# Wait some time. Check the time of the latest log and then wait again. Make sure that the time of the latest log is not greater (i.e. the file is not updated)')
                # Wait some time. Check the time of the latest log and then wait again. Make sure that the time of the latest log is not greater (i.e. the file is not updated)
                waitTimeAfterTraceDisabled = 30
                self.miscLib.waitTime(waitTimeAfterTraceDisabled)
                cmd = """tail -1 %s/%s | awk '{print $1" "$2}'""" %(self.comsaArea, self.comSaTraceFile)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                result = self.lib.timeConv(result[1])
                self.fail(result[0],result[1])
                timeOfLatestLog = result[1]
                timeAfterLogsDisabled1 = int(timeOfLatestLog)

                self.miscLib.waitTime(waitTimeAfterTraceDisabled)
                cmd = """tail -1 %s/%s | awk '{print $1" "$2}'""" %(self.comsaArea, self.comSaTraceFile)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                result = self.lib.timeConv(result[1])
                self.fail(result[0],result[1])
                timeOfLatestLog = result[1]
                timeAfterLogsDisabled2 = int(timeOfLatestLog)

                if timeAfterLogsDisabled1 != timeAfterLogsDisabled2:
                    self.fail('ERROR', 'The COM SA trace file was changed between %d and %d seconds after being disabled' %(waitTimeAfterTraceDisabled, 2*waitTimeAfterTraceDisabled))

                self.setTestStep('# Replace current COM SA trace file with original')
                # Replace current COM SA trace file with original
                cmd = '\mv -f %s/%s %s/%s' %(self.comsaArea, originalTraceConfigFile, self.comsaArea, self.comSaTraceConfig)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                self.setTestStep('# Restart COM. Do we need this?')
                # Restart COM
                result = self.comsa_lib.comRestart(self, activeController[0], activeController[1], self.memoryCheck)
                self.fail(result[0],result[1])
        else:
            self.fail('ERROR', 'Unknown response from the checkPso function. Expected either True or False. Received: %s' %str(result[1]))

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
