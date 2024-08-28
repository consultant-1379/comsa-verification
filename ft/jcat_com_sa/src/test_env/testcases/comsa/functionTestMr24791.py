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



    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
from se.ericsson.jcat.fw import SUTHolder
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib
from java.lang import System

class pdfcounter(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.test_config = testConfig

        # parameters from the config files
        self.backupName = {}
        self.comBackupName = {}
        self.comsaBackupLocation = {}
        self.storedBackupFilesLocation = {}
        self.loctBackupLocation = {}
        self.comBackupLocation = {}
        self.cmwBackupLocation = {}

        self.reqComVerGP1min = "R1A03" # COM version that supports PM Jobs with GP 1 minute (COM 4.0 Sh.13)
#        self.reqComVerGP1min = "R1A99" # COM version that supports PM Jobs with GP 1 minute (COM 4.0 Sh.13)
        self.reqComRelGP1min = "4"

        self.reqComSaRelease = "3"
        self.reqComSaVersion = "R1A01"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)

        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        self.resourceFilesLocation = dict.get("PATH_TO_MR24791")
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')

        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.pathToPmtSaFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("PATH_TO_PMTSA_FILES"))
        self.pathToPmtSaPdfFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("PATH_TO_PMTSA_PDF_FILES"))
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.comNoBackup = dict.get("COM_NO_BACKUP")
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        self.CoreMW = "%s/coremw3.3_latest"%self.resourceFilesLocation
        self.COM40_latest = "%s/com4.0_latest"%self.resourceFilesLocation
        self.ComSABuild = "%s/comsa"%self.resourceFilesLocation

        self.MR24791 = '/home/MR24791/'
        self.pathToCmwInstallation = '%s/coremw/' %self.MR24791
        self.pathToComInstallation = '%s/com/' %self.MR24791
        self.pathToComsaInstallation = '%s/comsa/' %self.MR24791
        self.pathtoIMMFilesAtTarget = '%s/model/' %self.MR24791

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)

        self.uninstallScriptName1 = 'uninstall_cmw.sh'
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        self.CoreMWSdp = 'COREMW_RUNTIME-CXP9020355_1.tar'

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.myLogger.info('Exit setUp')

    def runTest(self):

        self.setTestStep('runTest')

        self.skip_test = False
        self.setTestStep('Check the required versions of ComSA is installed')

        if self.restoreSnapshot:
            offlineVersion = ['','','']
            ComSaOK = ['', False]

            result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'COMSA')
            if result[0] == "REGTEST":
                offlineVersion[0] = result[1]
                offlineVersion[1] = result[2]
                offlineVersion[2] = result[3]
                ComSaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion, offlineVersion)
            else:
                ComSaOK[1] = True
        elif self.runUninstallationScript:
            ComSaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
        else:
            self.fail('ERROR', 'Normally we should not have ended up here: either self.restoreSnapshot or self.runUninstallationScript should be True!')

        if ComSaOK[1] == True:
            self.FirstXMLfile='IMM1.xml'
            self.SecondXMLfile='IMM2.xml'
            self.applicationBinary = 'pmsv_producer_cmd'
            pm_data_storage = '%sPerformanceManagementReportFiles/' %self.comNoBackup
            pmJobGpInSeconds = 300

            if not self.restoreSnapshot:
                # 1.Create Backup and Copy backup files to stored location
                self.setTestStep('======== Backup system ========')
                self.backupCluster(self.backupName)

                # 2.Copy backup files to stored location
                self.setTestStep('======== Copy backup files to stored location =========')

                result = self.sshLib.sendCommand('\\rm -rf %s' %self.storedBackupFilesLocation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.storedBackupFilesLocation)
                self.fail(result[0], result[1])

                command = '\cp %s/%s.tar.gz %scomsa_%s.tar.gz' %(self.comsaBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.backupName, self.storedBackupFilesLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.backupName, self.storedBackupFilesLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                # Copy com backup files to stored location
                self.comBackupName = self.findComBackup(self.comBackupName)
                if self.comBackupName != {}:

                    command = '\cp %s/%s.tar.gz %scom_%s.tar.gz' %(self.comBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\cp %s/%s.tar.gz %scmw_%s.tar.gz' %(self.cmwBackupLocation, self.comBackupName, self.storedBackupFilesLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.loctBackupLocation, self.comBackupName, self.storedBackupFilesLocation)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])


                # 3.Uninstall system

                self.setTestStep('======== Uninstall system ========')

                result = self.sshLib.sendCommand('mkdir %s' %self.MR24791)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                self.fail(result[0], result[1])

                #copy unistall script to cluster
                result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName1), self.MR24791, timeout = 120)
                self.fail(result[0], result[1])

                result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName2), self.MR24791, timeout = 120)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.MR24791)
                self.fail(result[0], result[1])

            #run Uninstall
            result = self.comsa_lib.unInstallSystem(self.MR24791, self.uninstallScriptName1, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
            self.fail(result[0], result[1])

            if not self.restoreSnapshot:
                cmw_uninstall_command2 = '%s%s' %(self.MR24791, self.uninstallScriptName2)
                result = self.sshLib.sendCommand (cmw_uninstall_command2)
                self.fail(result[0], result[1])

            self.lib.resetDumps()

            # 4.Install
            if self.restoreSnapshot:
                result = self.sshLib.sendCommand('mkdir %s' %self.MR24791)
                self.fail(result[0],result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToCmwInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComInstallation)
                self.fail(result[0], result[1])

                result = self.sshLib.sendCommand('mkdir %s' %self.pathToComsaInstallation)
                self.fail(result[0], result[1])

            #Install CoreMW
            self.setTestStep('======== Install CoreMW ========')

            result = self.sshLib.remoteCopy('%s/%s' %(self.CoreMW, self.CoreMWSdp), self.pathToCmwInstallation, timeout = 120)
            self.fail(result[0],result[1])

            result = self.comsa_lib.installCoreMw(self.pathToCmwInstallation, self.CoreMWSdp, backupRpms = self.backupRpmScript)
            self.fail(result[0], result[1])

            #Install COM
            self.setTestStep('======== Install COM ========')

            self.installCOM(self.COM40_latest, self.pathToComInstallation)
            self.fail(result[0], result[1])

            #Install COMSA
            self.setTestStep('======== Install COM SA ========')

            self.installCOMSA(self.pathToComsaInstallation)
            self.fail(result[0], result[1])

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
                #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)
                # with the local disk stress (as above) TC-FT1272-002 and -006 did fail.

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
                res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            #################  Check if the COM Version supports PM Jobs with GP 1 minute  #############################################
            self.setTestStep('Check if the installed version of COM in the system supports PM Jobs with GP 1 minute')
            self.ComSupportsOneMinJobs = self.lib.checkComponentVersion('com', self.reqComRelGP1min, self.reqComVerGP1min)

            if self.ComSupportsOneMinJobs[1] == False:
                self.myLogger.info("The installed COM version does not support PM Jobs with GP 1 minute.")

            else:
                self.myLogger.info("The installed COM version does support PM Jobs with GP 1 minute.")
                self.FirstXMLfile='pmjob.gp1min.IMM1.xml'
                self.SecondXMLfile='pmjob.gp1min.IMM2.xml'
                pmJobGpInSeconds = 60     # 1 minute

            # 5.#################   Test Case Multi-value measurement (PDF counter) starts here  ##############################################################
            self.setTestStep('Test Case Multi-value measurement (PDF counter)')

            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            self.activeController = result[1]

            self.setTestStep('Creating a Directory at target and Copying these "IMM*.xml" files at target.')

            result = self.sshLib.sendCommand('\\rm -rf %s' %self.pathtoIMMFilesAtTarget, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            result = self.sshLib.sendCommand('mkdir -p %s' %self.pathtoIMMFilesAtTarget, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

            result = self.sshLib.remoteCopy('%s%s' %(self.pathToPmtSaFiles, self.FirstXMLfile),self.pathtoIMMFilesAtTarget , timeout = 120,numberOfRetries = 2)
            self.fail(result[0], result[1])
            result = self.sshLib.remoteCopy('%s%s' %(self.pathToPmtSaFiles, self.SecondXMLfile),self.pathtoIMMFilesAtTarget , timeout = 120,numberOfRetries = 2)
            self.fail(result[0], result[1])

            self.setTestStep('Importing the files with command "immcfg -f <filename>')

            result = self.sshLib.sendCommand ('immcfg -f %s%s' %(self.pathtoIMMFilesAtTarget, self.FirstXMLfile), self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if result[1] != "":
               self.fail('ERROR', 'Importing %s%s failed: %s' %(self.pathtoIMMFilesAtTarget, self.FirstXMLfile, result[1]))

            result = self.sshLib.sendCommand ('immcfg -f %s%s' %(self.pathtoIMMFilesAtTarget, self.SecondXMLfile), self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if result[1] != "":
               self.fail('ERROR', 'Importing %s%s failed: %s' %(self.pathtoIMMFilesAtTarget, self.SecondXMLfile, result[1]))

            self.setTestStep('Copy binary file %s to %s on the target' %(self.applicationBinary, self.pathtoIMMFilesAtTarget))
            self.logger.info('Copying existing binary file - spmsv_producer_cmd to target to %s' %self.pathtoIMMFilesAtTarget)
            result = self.sshLib.remoteCopy('%s%s' %(self.pathToPmtSaFiles, self.applicationBinary),self.pathtoIMMFilesAtTarget , timeout = 120,numberOfRetries = 2)
            self.fail(result[0], result[1])

            executableBinary = 'chmod +x %s%s' %(self.pathtoIMMFilesAtTarget, self.applicationBinary)
            result = self.sshLib.sendCommand(executableBinary, self.activeController[0], self.activeController[1]) # works on the target
            self.fail(result[0], result[1])

            # Clear the PM strorage area
            cmd = '\\rm -rf %s/*.xml' %pm_data_storage
            result = self.sshLib.sendCommand (cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])

            cmd = 'cmw-pmjob-start CcJob1'

            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if 'command not found' in result[1]:
                self.fail('ERROR', result[1])
            elif 'error' in result[1] or 'FAILED' in result[1]:
                self.fail('ERROR', result[1])
            if self.ComSupportsOneMinJobs[1] == True:
                self.logger.info('Current Date and Time : %s  The granularity period for the job is one minute' %result[1])
            else:
                self.logger.info('Current Date and Time : %s  The granularity period for the job is five minutes' %result[1])
            self.logger.info('Increment PDF counter (only the first counter element) value with one')
            cmd = '%s%s cc:CcGroup1:PDFcounter:counter:1'%(self.pathtoIMMFilesAtTarget, self.applicationBinary)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if result[1] != '':
                self.fail('ERROR', 'Expected empty string as result. Received %s' %result[1])

            # Determine the next GP boundary moment in time and wait until: (then + 15 sec)
            # The GP is aligned to the system time, for example:
            # For GP 1 min the GP boundaries are (h:m:s) 1:17:00, 1:18:00, etc.
            # For GP 5 min the GP boundaries are (h:m:s) 1:15:00, 1:20:00, etc.

            cmd = 'date +\%M'  # get the minutes of the current time
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            minutesPastExactHour = int(result[1])

            minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
            minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary
            if minutesToWaitTo5MinGpBoundary > 0:
                minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1
            cmd = 'date +\%S'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            secondsPastExactMinute = int(result[1])

            counterWriteTargetTime = 45   # seconds past the exact minute

            if secondsPastExactMinute < counterWriteTargetTime:
                waitAfterEndOfGpTime = counterWriteTargetTime - secondsPastExactMinute
            else:
                waitAfterEndOfGpTime = 60 - secondsPastExactMinute + counterWriteTargetTime

            if pmJobGpInSeconds == 300:   # for GP 5 minutes
                waitAfterEndOfGpTime = (minutesToWaitTo5MinGpBoundary * 60) + waitAfterEndOfGpTime

            waitAfterEndOfGpTime += 30

            self.logger.info('Wait for %s seconds to cross a GP boundary ...' %(waitAfterEndOfGpTime))
            self.miscLib.waitTime(waitAfterEndOfGpTime)

            # Align the counter writing time to GP

            cmd = 'date +\%M'  # get the minutes of the current time
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            minutesPastExactHour = int(result[1])

            minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
            minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary
            if minutesToWaitTo5MinGpBoundary > 0:
                minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1
            cmd = 'date +\%S'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            secondsPastExactMinute = int(result[1])

            counterWriteTargetTime = 45   # seconds past the exact minute

            if secondsPastExactMinute < counterWriteTargetTime:
                newWaitBeforeTime = counterWriteTargetTime - secondsPastExactMinute
            else:
                newWaitBeforeTime = 60 - secondsPastExactMinute + counterWriteTargetTime

            if pmJobGpInSeconds == 300:   # for GP 5 minutes
                newWaitBeforeTime = (minutesToWaitTo5MinGpBoundary * 60) + newWaitBeforeTime

            self.logger.info('Wait for %s seconds before writing to the counter at exactly 15 sec before the GP boundary...' %(newWaitBeforeTime))
            self.miscLib.waitTime(newWaitBeforeTime)

            self.logger.info('Increment again the PDF counter value (only the first counter element)')
            cmd = '%s%s cc:CcGroup1:PDFcounter:counter:1'%(self.pathtoIMMFilesAtTarget, self.applicationBinary)

            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if result[1] != '':
                self.fail('ERROR', 'Expected empty string as result. Received %s' %result[1])

            waitForGpEnd = 30    # this is 15 seconds after the GP moment (as writing was done 14 sec before the GP moment)

            self.logger.info('Wait for %s seconds to cross a GP boundary ...' %(waitForGpEnd))
            self.miscLib.waitTime(waitForGpEnd)

            # Align the counter writing time to GP

            cmd = 'date +\%M'  # get the minutes of the current time
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            minutesPastExactHour = int(result[1])

            minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
            minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary
            if minutesToWaitTo5MinGpBoundary > 0:
                minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1
            cmd = 'date +\%S'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            secondsPastExactMinute = int(result[1])

            if secondsPastExactMinute < counterWriteTargetTime:
                newWaitBeforeTime = counterWriteTargetTime - secondsPastExactMinute
            else:
                newWaitBeforeTime = 60 - secondsPastExactMinute + counterWriteTargetTime

            if pmJobGpInSeconds == 300:   # for GP 5 minutes
                newWaitBeforeTime = (minutesToWaitTo5MinGpBoundary * 60) + newWaitBeforeTime

            self.logger.info('Wait for %s seconds before Stopping the job at exactly 15 sec before the GP boundary...' %(newWaitBeforeTime))
            self.miscLib.waitTime(newWaitBeforeTime)
            self.logger.info('Stop the job')

            cmd = 'cmw-pmjob-stop CcJob1'

            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if 'command not found' in result[1]:
                self.fail('ERROR', result[1])
            elif 'error' in result[1] or 'FAILED' in result[1]:
                self.fail('ERROR', result[1])

            # Here we need to wait for a full GP
            self.logger.info('Wait for %s seconds (one GP) after the PM Job was stopped ...' %(pmJobGpInSeconds))
            self.miscLib.waitTime(pmJobGpInSeconds)

            self.logger.info('Verify that there is correct PM-data in /cluster/storage/no-backup/com-apr9010443/PerformanceManagementReportFiles/')
            # We expect to have two files which contain the string 'counter'
            # From these two files one should contain a tag <suspect> with the value true
            # The other file should either not contain the tag or have its value as false
            cmd = 'cd %s; grep -l counter *.xml' %pm_data_storage
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', 'Problem checking PM-data in %s. %s' %(pm_data_storage, result[1]))
            pmFiles = result[1].split()
            if len(pmFiles) != 2:
                self.fail('ERROR', 'Expected exactly 2 files to contain the string counter under %s. Found: %d' %(pm_data_storage, len(pmFiles)))
            suspectCounter = 0
            notSuspectCounter = 0
            for file in pmFiles:
                cmd = 'grep suspect %s%s' %(pm_data_storage, file)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] == '':
                    notSuspectCounter += 1
                elif 'alse' in result[1]:
                    notSuspectCounter += 1
                else:
                    suspectCounter += 1
            if suspectCounter != 1:
                self.fail('ERROR', 'Expected exactly one match for suspectCounter. Got %d instead' %suspectCounter)
            if notSuspectCounter != 1:
                self.fail('ERROR', 'Expected exactly one match for notSuspectCounter. Got %d instead' %notSuspectCounter)

            #Disable Stress Tool:
            if self.installStressTool:
                self.setTestStep('======== Stopping the stress tool on target ========')
                self.comsa_lib.stopStressToolOnTarget(self)
            if not self.restoreSnapshot:
                # 6.Restore
                self.setTestStep('======== Restore system ========')
                #recopy the backup files
                command = '\cp %scomsa_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comsaBackupLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.comBackupLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.backupName, self.cmwBackupLocation, self.backupName)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.backupName, self.loctBackupLocation)
                result = self.sshLib.sendCommand (command)
                self.fail(result[0], result[1])

                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                self.fail(result[0],result[1])

                #replace the com backup files
                if self.comBackupName != {}:

                    command = '\cp  %scom_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.comBackupName, self.comBackupLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\cp %scmw_%s.tar.gz %s/%s.tar.gz ' %(self.storedBackupFilesLocation, self.comBackupName, self.cmwBackupLocation, self.comBackupName)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])

                    command = '\cp %s/cmwea-snapshot-%s.tar.gz %s' %(self.storedBackupFilesLocation, self.comBackupName, self.loctBackupLocation)
                    result = self.sshLib.sendCommand (command)
                    self.fail(result[0], result[1])
        else:
            self.logger.info('Skipped trace tests because of COMSA version not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True


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
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comInstSdpName, 'com', False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')

    def installCOMSA(self, pathToComsaInstallation):
        self.logger.info('installCOMSA: Called')
        self.logger.info('installCOMSA: pathToComsaInstallation = %s' %pathToComsaInstallation)

        self.logger.info('installCOMSA: buildAndStoreCOMSA Called ')
        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
        if BuildPath[0] != 'SUCCESS':
            self.logger.error(result[1])
            self.logger.debug('Build COMSA failed : Exit')
            return (BuildPath[0], 'Build COM SA failed')

       # Install time

        result = self.comsa_lib.copyFilesToTarget(['%s/' %BuildPath[6], '%s/' %BuildPath[7]], self.pathToComsaInstallation, True)
        self.fail(result[0], result[1])

        result = self.comsa_lib.installComp(pathToComsaInstallation, BuildPath[1], BuildPath[2], 'comsa', False, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])

        self.logger.info('installCOMSA: Exit')

    def findComBackup(self, comBackupName):
        """
        If comBackupName is defined, the method simply returns the same name.
        If comBackupName is not defined, the method returns the latest backup which's name
        contains COM (case insensitive), but does not contain comsa, com_sa, com-sa (case insensitive)
        """
        self.logger.info('findComBackup: Called')
        if comBackupName != {}:
            self.logger.info('findComBackup: Exit')
            return comBackupName
        else:
            cmd = """cmw-partial-backup-list 2>&1 | sed 's/\[//g' | sed 's/\]//g' | grep -i com | egrep -iv '(comsa)|(com_sa)|(com-sa)' | tail -1 | awk '{print $NF}' """
            # We search for the latest COM backup
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            backupName = result[1]
            if backupName == '':
                self.logger.info('findComBackup: Exit')
                self.fail('ERROR', 'findComBackup: COM backup not found!')
            self.logger.info('findComBackup: Exit')
            return backupName


    def tearDown(self):
        self.setTestStep('tearDown')
        if self.skip_test == False:
            command = '\\rm -rf /home/MR24791/'
            self.sshLib.sendCommand(command)

            command = '\\rm -rf %s' %self.storedBackupFilesLocation
            self.sshLib.sendCommand(command)

            self.sshLib.tearDownHandles()
            coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
