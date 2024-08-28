import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib

from java.lang import System

class Stability(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )
        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.serviceInstanceName = 'ComSa'
        self.amfNodePattern = 'Cmw'
        self.hourlyCommand = ''
        self.numberOfHours = ''
        self.hoursPerLoop = 2
        self.cliLoaderScriptPathOnTarget = '/home/test/'
        self.cliLoaderScriptPathLocal = ''
        self.cliLoaderScriptName = 'cliLoader.sh'
        self.cliLoaderInputFilePathOnTarget = '/home/test/'
        self.cliLoaderInputFilePathLocal = ''
        self.cliLoaderInputFileName = 'inputToCliLoader.txt'

        # SDP1724 test case specific data
        self.modelfile_mp1 = ""
        self.modelfile_mp2 = ""
        self.modelfile_mp3 = ""
        self.modelfile_mp4 = ""
        self.modelfile_mp5 = ""

        self.modelfile_imm_classes1  = ""
        self.modelfile_imm_classes2  = ""
        self.modelfile_imm_classes3  = ""
        self.modelfile_imm_classes4  = ""
        self.modelfile_imm_classes5  = ""

        self.modelfile_imm_objects1 = ""
        self.modelfile_imm_objects2 = ""
        self.modelfile_imm_objects3 = ""
        self.modelfile_imm_objects4 = ""
        self.modelfile_imm_objects5 = ""

        self.test_consumer_1 = ""
        self.test_consumer_2 = ""
        self.test_consumer_3 = ""

        self.testCons1Regexp1 = ""
        self.testCons1Regexp2 = ""
        self.testCons1Regexp3 = ""
        self.testCons1Regexp4 = ""
        self.testCons1Regexp5 = ""
        self.testCons2Regexp1 = ""
        self.testCons2Regexp2 = ""
        self.testCons2Regexp3 = ""
        self.testCons2Regexp4 = ""
        self.testCons2Regexp5 = ""
        self.testCons3Regexp1 = ""
        self.testCons3Regexp2 = ""
        self.testCons3Regexp3 = ""
        self.testCons3Regexp4 = ""
        self.testCons3Regexp5 = ""

        self.testOIarg1 = ""
        self.testOIarg2 = ""
        self.testOIarg3 = ""
        self.testOIarg4 = ""
        self.testOIarg5= ""
        self.testOIarg6 = ""
        self.testOIarg7 = ""
        self.testOIarg8 = ""
        self.testOIarg9 = ""
        self.testOIarg10 = ""
        self.testOIarg11 = ""
        self.testOIarg12 = ""
        self.testOIarg13 = ""
        self.testOIarg14 = ""
        self.testOIarg15 = ""
        self.testOIarg16 = ""
        self.testOIarg17 = ""
        self.testOIarg18 = ""
        self.testOIarg19 = ""
        self.testOIarg20 = ""

        self.testOI_name = "imm-applier"

        self.disable_class_notify_1 = ""
        self.disable_objectOrAttr_1 = ""
        self.disable_class_notify_2 = ""
        self.disable_objectOrAttr_2 = ""
        self.disable_class_notify_3 = ""
        self.disable_objectOrAttr_3 = ""
        self.disable_class_notify_4 = ""
        self.disable_objectOrAttr_4 = ""
        self.disable_class_notify_5 = ""
        self.disable_objectOrAttr_5 = ""
        self.disable_class_notify_6 = ""
        self.disable_objectOrAttr_6 = ""
        self.disable_class_notify_7 = ""
        self.disable_objectOrAttr_7 = ""
        self.disable_class_notify_8 = ""
        self.disable_objectOrAttr_8 = ""
        self.disable_class_notify_9 = ""
        self.disable_objectOrAttr_9 = ""
        self.disable_class_notify_10 = ""
        self.disable_objectOrAttr_10 = ""
        self.disable_class_notify_11 = ""
        self.disable_objectOrAttr_11 = ""
        self.disable_class_notify_12 = ""
        self.disable_objectOrAttr_12 = ""
        self.disable_class_notify_13 = ""
        self.disable_objectOrAttr_13 = ""
        self.disable_class_notify_14 = ""
        self.disable_objectOrAttr_14 = ""
        self.disable_class_notify_15 = ""
        self.disable_objectOrAttr_15 = ""
        self.disable_class_notify_16 = ""
        self.disable_objectOrAttr_16 = ""
        self.disable_class_notify_17 = ""
        self.disable_objectOrAttr_17 = ""
        self.disable_class_notify_18 = ""
        self.disable_objectOrAttr_18 = ""
        self.disable_class_notify_19 = ""
        self.disable_objectOrAttr_19 = ""
        self.disable_class_notify_20 = ""
        self.disable_objectOrAttr_20 = ""
        self.disable_class_notify_21 = ""
        self.disable_objectOrAttr_21 = ""
        self.disable_class_notify_22 = ""
        self.disable_objectOrAttr_22 = ""
        self.disable_class_notify_23 = ""
        self.disable_objectOrAttr_23 = ""
        self.disable_class_notify_24 = ""
        self.disable_objectOrAttr_24 = ""
        self.disable_class_notify_25 = ""
        self.disable_objectOrAttr_25 = ""
        self.disable_class_notify_26 = ""
        self.disable_objectOrAttr_26 = ""
        self.disable_class_notify_27 = ""
        self.disable_objectOrAttr_27 = ""
        self.disable_class_notify_28 = ""
        self.disable_objectOrAttr_28 = ""
        self.disable_class_notify_29 = ""
        self.disable_objectOrAttr_29 = ""
        self.disable_class_notify_30 = ""
        self.disable_objectOrAttr_30 = ""

        self.enable_class_notify_1 = ""
        self.enable_objectOrAttr_1 = ""
        self.enable_class_notify_2 = ""
        self.enable_objectOrAttr_2 = ""
        self.enable_class_notify_3 = ""
        self.enable_objectOrAttr_3 = ""
        self.enable_class_notify_4 = ""
        self.enable_objectOrAttr_4 = ""
        self.enable_class_notify_5 = ""
        self.enable_objectOrAttr_5 = ""
        self.enable_class_notify_6 = ""
        self.enable_objectOrAttr_6 = ""
        self.enable_class_notify_7 = ""
        self.enable_objectOrAttr_7 = ""
        self.enable_class_notify_8 = ""
        self.enable_objectOrAttr_8 = ""
        self.enable_class_notify_9 = ""
        self.enable_objectOrAttr_9 = ""
        self.enable_class_notify_10 = ""
        self.enable_objectOrAttr_10 = ""
        self.enable_class_notify_11 = ""
        self.enable_objectOrAttr_11 = ""
        self.enable_class_notify_12 = ""
        self.enable_objectOrAttr_12 = ""
        self.enable_class_notify_13 = ""
        self.enable_objectOrAttr_13 = ""
        self.enable_class_notify_14 = ""
        self.enable_objectOrAttr_14 = ""
        self.enable_class_notify_15 = ""
        self.enable_objectOrAttr_15 = ""
        self.enable_class_notify_16 = ""
        self.enable_objectOrAttr_16 = ""
        self.enable_class_notify_17 = ""
        self.enable_objectOrAttr_17 = ""
        self.enable_class_notify_18 = ""
        self.enable_objectOrAttr_18 = ""
        self.enable_class_notify_19 = ""
        self.enable_objectOrAttr_19 = ""
        self.enable_class_notify_20 = ""
        self.enable_objectOrAttr_20 = ""
        self.enable_class_notify_21 = ""
        self.enable_objectOrAttr_21 = ""
        self.enable_class_notify_22 = ""
        self.enable_objectOrAttr_22 = ""
        self.enable_class_notify_23 = ""
        self.enable_objectOrAttr_23 = ""
        self.enable_class_notify_24 = ""
        self.enable_objectOrAttr_24 = ""
        self.enable_class_notify_25 = ""
        self.enable_objectOrAttr_25 = ""
        self.enable_class_notify_26 = ""
        self.enable_objectOrAttr_26 = ""
        self.enable_class_notify_27 = ""
        self.enable_objectOrAttr_27 = ""
        self.enable_class_notify_28 = ""
        self.enable_objectOrAttr_28 = ""
        self.enable_class_notify_29 = ""
        self.enable_objectOrAttr_29 = ""
        self.enable_class_notify_30 = ""
        self.enable_objectOrAttr_30 = ""

        self.pattern_1 = ""
        self.pattern_2 = ""
        self.pattern_3 = ""
        self.pattern_4 = ""
        self.pattern_5 = ""


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.modelfile_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_MODELFILE_PATH"))

        self.reqComSaReleaseV4 = "3"
        self.reqComSaVersionV4 = "R8A05"
        self.ComSa_v4 = ('SUCCESS', False)
        self.ComSa_v4 = self.lib.checkComponentVersion('comsa', self.reqComSaReleaseV4, self.reqComSaVersionV4)
        if self.ComSa_v4[1]:
            self.path_to_testConsumer = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_TESTCONSUMER_V4_PATH"))
        else:
            self.path_to_testConsumer = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_TESTCONSUMER_PATH"))

        self.testOI_path_in_fileSystem = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT1724_TESTOI_PATH"))
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.target_com_compdir = dict.get('COM_COMP_DIR')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')

        if self.cliLoaderScriptPathLocal == '':
            self.cliLoaderScriptPathLocal = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("EXAMPLE_MODELFILE_PATH"))
        if self.cliLoaderInputFilePathLocal == '':
            self.cliLoaderInputFilePathLocal = self.cliLoaderScriptPathLocal

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.logger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        self.controllers = self.testConfig['controllers']
        self.noOfScs = len(self.controllers)
        self.noOfPls = len(self.testConfig['payloads'])

        # Replace dynamic fields in test suite command
        self.hourlyCommand = self.hourlyCommand.replace('targetName', self.targetData['target'])
        self.hourlyCommand = self.hourlyCommand.replace('numberOfSCs', str(self.noOfScs))
        self.hourlyCommand = self.hourlyCommand.replace('numberOfPLs', str(self.noOfPls))

        # Copy CLI loader script to target
        self.copyFileToTarget(self.cliLoaderInputFileName, self.cliLoaderInputFilePathLocal, self.cliLoaderInputFilePathOnTarget)
        self.copyFileToTarget(self.cliLoaderScriptName, self.cliLoaderScriptPathLocal, self.cliLoaderScriptPathOnTarget, True)

        # Find active System Controller
        self.findActiveAndStandbyController()
        # Load CM notifications test case specific data
        self.prepareForCmNotificationsTesting()
        # Save the COM PID in the variable self.comPid
        self.getComPid()

        # Start looping over the measurement period
        testLoopsExecuted = 0
        self.startTime = int(time.time())
        endTime = self.startTime + int(self.numberOfHours)*3600
        timeNow = self.startTime

        # Get the initial memory usage
        self.comVmPeak = []
        self.comVmSize = []
        self.comVmRSS = []
        self.pmtSaLibsTotalOnDisk = []
        self.comSaLibsTotalOnDisk = []
        self.pmtSaLibsTotalDynamic = []
        self.comSaLibsTotalDynamic = []
        self.comsaFileDescriptorsOpen = []
        self.cpuLoad = []
        self.getPerformanceData()

        enableStressTool = eval(System.getProperty("runStressTool"))
        stressTimeOut = 60
        cliLoaderTimout = 900
        if enableStressTool:
            # Get the memory usage after enabling the stress tool
            self.getPerformanceData()

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
            result = self.comsa_lib.startlStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60)
            self.sshLib.setTimeout(stressTimeOut)

        while timeNow < endTime:
            self.setTestStep('Loop %d: ' %(testLoopsExecuted + 1))

            # Run the test suite defined in the xml test case and evaluate the test results at the end
            logPath = ''
            result = self.miscLib.execCommand('%s 2>&1' %self.hourlyCommand)
            for line in result[1].splitlines():
                if 'The HTML logs are in: ' in line:
                    # The second split() is needed because there are some garbage characters after index.html that we do not want to visualize
                    logPath = line.split('The HTML logs are in: ')[1].split('index.html')[0]
                    logPath = '%sindex.html' %logPath
                    currentReadableTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    self.setAdditionalResultInfo('Loop %d test suite logs at %s: %s' %(testLoopsExecuted + 1, currentReadableTime, logPath.strip()))
            self.evaluateNestedSuiteResults(logPath)

            self.myLogger.info('Check that COM process did not restart unexpectedly during the nested test suite and get performance data')
            self.checkComPidUnchanged()
            self.getPerformanceData()

            # Run the CLI loader script. Intention is to run 600 loops for approximately 10 minutes, but maximum 15 minutes (defined by cliLoaderTimeout).
            self.sshLib.setTimeout(cliLoaderTimout, self.activeController[0], self.activeController[1])
            result = self.sshLib.sendCommand('%s/%s %s/%s' %(self.cliLoaderScriptPathOnTarget, self.cliLoaderScriptName, self.cliLoaderInputFilePathOnTarget, self.cliLoaderInputFileName), self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            self.sshLib.setTimeout(stressTimeOut)

            self.myLogger.info('Check that COM process did not restart unexpectedly during the CLI loader script execution and get performance data')
            self.checkComPidUnchanged()
            self.getPerformanceData()
            testLoopsExecuted += 1
            timeNow = int(time.time())

        self.myLogger.info("exit runTest")
        coreTestCase.CoreTestCase.runTest(self)

    def tearDown(self):
        self.setTestStep('tearDown')

        timeNow = int(time.time())
        totalTestTime = timeNow - self.startTime

        self.logger.debug('Total test time: %d seconds (%f hours). ' %(totalTestTime, totalTestTime/float(3600)))
        self.logger.debug('COM SA static lib memory usage on disk array (in kB): %s' %str(self.comSaLibsTotalOnDisk))
        self.logger.debug('PMT SA static lib memory usage on disk array (in kB): %s' %str(self.pmtSaLibsTotalOnDisk))
        self.logger.debug('COM SA dynamic lib memory usage array (in kB): %s' %str(self.comSaLibsTotalDynamic))
        self.logger.debug('PMT SA dynamic lib memory usage array (in kB): %s' %str(self.pmtSaLibsTotalDynamic))
        self.logger.debug('COMSA open file descriptors array: %s' %str(self.comsaFileDescriptorsOpen))
        self.logger.debug('COM process VmRSS memory usage array (in kB): %s' %str(self.comVmRSS))
        self.logger.debug('COM process VmSize memory usage array (in kB): %s' %str(self.comVmSize))
        self.logger.debug('COM process VmPeak memory usage array (in kB): %s' %str(self.comVmPeak))
        self.logger.debug('CPU load percentage array: %s' %str(self.cpuLoad))

        self.setAdditionalResultInfo('===================================')
        self.setAdditionalResultInfo('Printing results for test report')
        self.setAdditionalResultInfo('===================================')
        self.setAdditionalResultInfo('COMSA open file descriptors (avg): %.0f' %(sum(self.comsaFileDescriptorsOpen)/float(len(self.comsaFileDescriptorsOpen))))
        self.setAdditionalResultInfo('COM process VmRSS memory usage array (in kB): %s' %str(self.comVmRSS))
        self.setAdditionalResultInfo('COM process VmSize memory usage array (in kB): %s' %str(self.comVmSize))
        self.setAdditionalResultInfo('COM SA dynamic lib memory usage array (in kB): %s' %str(self.comSaLibsTotalDynamic))
        self.setAdditionalResultInfo('PMT SA dynamic lib memory usage array (in kB): %s' %str(self.pmtSaLibsTotalDynamic))
        self.setAdditionalResultInfo('COM process VmPeak memory usage (in kB): %.0f' %max(self.comVmPeak))
        self.setAdditionalResultInfo('CPU load percentage (avg): %.2f' %(sum(self.cpuLoad)/float(len(self.cpuLoad))))
        self.setAdditionalResultInfo('COM SA static lib memory usage on disk (avg in kB): %.0f' %(sum(self.comSaLibsTotalOnDisk)/float(len(self.comSaLibsTotalOnDisk))))
        self.setAdditionalResultInfo('PMT SA static lib memory usage on disk (avg in kB): %.0f' %(sum(self.pmtSaLibsTotalOnDisk)/float(len(self.pmtSaLibsTotalOnDisk))))

        #Remove CLI loader script and input file from the target
        self.removeFileFromTarget(self.cliLoaderInputFilePathOnTarget, self.cliLoaderInputFileName)
        self.removeFileFromTarget(self.cliLoaderScriptPathOnTarget, self.cliLoaderScriptName)

        self.tearDownProcedureForCmNotificationsTest()

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

        #########################
        #### SUPPORT METHODS ####
        #########################

    def getComPid(self):
        self.myLogger.debug('enter getComPid')
        result = self.comsa_lib.getProcessId(self.activeController[0], self.activeController[1], 'com', '/etc/com.cfg')
        self.fail(result[0], result[1])
        if 'int' not in str(type(result[1])):
            self.myLogger.debug('leave getComPid')
            self.fail('ERROR', 'Expected exactly one COM process to be active. Found: %d: %s' %(len(result[1]), str(result[1])))
        self.comPid = result[1]
        self.myLogger.debug('leave getComPid')

    def checkComPidUnchanged(self):
        self.myLogger.debug('enter checkComPidUnchanged')
        result = self.comsa_lib.getProcessId(self.activeController[0], self.activeController[1], 'com', '/etc/com.cfg')
        self.fail(result[0], result[1])
        if 'int' not in str(type(result[1])):
            self.myLogger.debug('leave checkComPidUnchanged')
            self.fail('ERROR', 'Expected exactly one COM process to be active. Found: %d: %s' %(len(result[1]), str(result[1])))
        if result[1] != self.comPid:
            self.myLogger.debug('leave checkComPidUnchanged')
            self.fail('ERROR', 'COM process restarted unexpectedly. Current PID: %d. Expected PID: %d' %(result[1], self.comPid))
        self.myLogger.debug('leave checkComPidUnchanged')

    def copyFileToTarget(self, fileName, localPath, targetPath, makeFileExecutable = False):
        self.myLogger.debug('enter copyFileToTarget')
        result = self.sshLib.sendCommand('mkdir -p %s' %targetPath)
        self.fail(result[0], result[1])
        result = self.sshLib.remoteCopy('%s/%s' %(localPath, fileName), targetPath)
        self.fail(result[0], result[1])
        if makeFileExecutable:
            result = self.sshLib.sendCommand('chmod +x %s/%s' %(targetPath, fileName))
            self.fail(result[0], result[1])
        self.myLogger.debug('leave copyFileToTarget')

    def removeFileFromTarget(self, targetPath, fileName):
        self.myLogger.debug('enter removeFileFromTarget')
        result = self.sshLib.sendCommand('\\rm -f %s/%s' %(targetPath, fileName))
        self.fail(result[0], result[1])
        self.myLogger.debug('leave removeFileFromTarget')

    def findActiveAndStandbyController(self):
        self.setTestStep('Find active and standby controllers')
        self.myLogger.debug('enter findActiveAndStandbyController')
        activeController = 0
        standbyController = 0

        controllers = self.testConfig['controllers']
        self.myLogger.info('Checking HA state for Com SA on the controllers')
        for controller in controllers:
            result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            if result[1] == 'ACTIVE':
                activeController = controller
                self.myLogger.info('Found active controller: %s' %str(controller))
            elif result[1] == 'STANDBY':
                standbyController = controller
                self.myLogger.info('Found standby controller: %s' %str(controller))

        self.myLogger.info('findActiveController returns activeController: (%s) standbyController: (%s)' %(activeController,standbyController))

        self.activeSubrack =  activeController[0]
        self.activeSlot =     activeController[1]
        self.activeController = (self.activeSubrack, self.activeSlot)
        self.myLogger.info('active  controller param: (%s,%s)' %(str(self.activeSubrack),  str(self.activeSlot))  )

        if self.noOfScs == 2 and standbyController != 0:
            self.standbySubrack = standbyController[0]
            self.standbySlot = standbyController[1]
            self.standbyController = (self.standbySubrack, self.standbySlot)
            self.myLogger.info('standby controller param: (%s,%s)' %(str(self.standbySubrack), str(self.standbySlot)) )
        self.myLogger.debug('leave findActiveAndStandbyController')

    def evaluateNestedSuiteResults(self, logPath):
        self.myLogger.debug('enter evaluateNestedSuiteResults')
        if logPath == '':
            self.myLogger.debug('leave evaluateNestedSuiteResults')
            self.fail('ERROR', 'Empty log path provided for nested test suite logs.')
        path = logPath.split('/index.htm')[0]
        result = self.miscLib.execCommand('cat "%s/tpt.txt" | grep NP' %path)
        self.fail(result[0], result[1])
        failedTestCases = []
        for lines in result[1].splitlines():
            failedTestCases.append(lines.split(', ')[1])
        if len(failedTestCases) != 0:
            self.myLogger.error('The following test case(s) failed during the nested test suite: %s. Link to nested test suite logs: %s' %(str(failedTestCases), logPath))
            self.myLogger.debug('leave evaluateNestedSuiteResults')
            self.setAdditionalResultInfo('The following test case(s) failed during the nested test suite: %s.' %str(failedTestCases))
            """
            # Failing the stability test suite is temporarily disabled in case on test case fails during the nested test suites.
            if self.memoryCheck:
                self.setAdditionalResultInfo('The following test case(s) failed during the nested test suite: %s.' %str(failedTestCases))
            else:
                self.fail('ERROR', 'The following test case(s) failed during the nested test suite: %s. Link to nested test suite logs: %s' %(str(failedTestCases), logPath))
            """
        self.myLogger.debug('leave evaluateNestedSuiteResults')

    def getPerformanceData(self):
        self.myLogger.debug('enter evaluateNestedSuiteResults')
        self.getComProcessMemoryUsage()
        self.getComSaLibMemoryUsage()
        self.getCpuLoad()
        self.getNumberOfOpenFileDescriptors()
        self.myLogger.debug('leave evaluateNestedSuiteResults')

    def getComProcessMemoryUsage(self):
        self.myLogger.debug('enter getComProcessMemoryUsage')
        result = self.sshLib.sendCommand("""cat /proc/%s/status | egrep '(VmSize)|(VmPeak)|(VmRSS)'""" %self.comPid, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        VmSizeFound = False
        VmPeakFound = False
        VmRSSFound = False
        for line in result[1].splitlines():
            if 'VmSize' in line:
                VmSizeFound = True
                self.comVmSize.append(int(line.split()[1]))
            if 'VmPeak' in line:
                VmPeakFound = True
                self.comVmPeak.append(int(line.split()[1]))
            if 'VmRSS' in line:
                VmRSSFound = True
                self.comVmRSS.append(int(line.split()[1]))
        if VmSizeFound == False:
            self.myLogger.debug('leave getComProcessMemoryUsage')
            self.fail('ERROR', 'VmSize not found in the process status information.')
        if VmPeakFound == False:
            self.myLogger.debug('leave getComProcessMemoryUsage')
            self.fail('ERROR', 'VmPeak not found in the process status information.')
        if VmRSSFound == False:
            self.myLogger.debug('leave getComProcessMemoryUsage')
            self.fail('ERROR', 'VmRSS not found in the process status information.')
        self.myLogger.debug('leave getComProcessMemoryUsage')

    def getComSaLibMemoryUsage(self):
        self.myLogger.debug('enter getComSaLibMemoryUsage')
        comsaSizeOnDisk = 0
        pmtSaSizeOnDisk = 0
        comsaSizeDynamic = 0
        pmtSaSizeDynamic = 0
        result = self.sshLib.sendCommand('cat /proc/%s/smaps' %self.comPid, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        #example delimiter: '7f345e570000-7f345e57a000'
        blockDelimiterPattern = re.compile(r'\n[0-9a-fA-F]{4,}-[0-9a-fA-F]{4,}')
        blocks = re.split(blockDelimiterPattern, result[1])
        for block in blocks:
            if 'coremw-com-sa.so' in block.splitlines()[0]:
                comsaSizeOnDisk += int(block.splitlines()[1].split()[1])
                comsaSizeDynamic += int(block.splitlines()[2].split()[1])
            if 'coremw-pmt-sa.so' in block.splitlines()[0]:
                pmtSaSizeOnDisk += int(block.splitlines()[1].split()[1])
                pmtSaSizeDynamic += int(block.splitlines()[2].split()[1])
        self.comSaLibsTotalOnDisk.append(comsaSizeOnDisk)
        self.pmtSaLibsTotalOnDisk.append(pmtSaSizeOnDisk)
        self.comSaLibsTotalDynamic.append(comsaSizeDynamic)
        self.pmtSaLibsTotalDynamic.append(pmtSaSizeDynamic)
        self.myLogger.debug('leave getComSaLibMemoryUsage')

    def getCpuLoad(self):
        self.myLogger.debug('enter getCpuLoad')
        """
        Sleep is introduced in order to allow the CPU to release any tasks related to
        the ssh connection created by the test framework.
        Might not be needed?
        """
        result = self.sshLib.sendCommand('sleep 15; mpstat | grep all', self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        idleLoad = float(result[1].split()[len(result[1].split()) - 1])
        self.cpuLoad.append(round(100 - idleLoad, 2))
        self.myLogger.debug('leave getCpuLoad')

    def getNumberOfOpenFileDescriptors(self):
        self.myLogger.debug('enter getNumberOfOpenFileDescriptors')
        result = self.sshLib.sendCommand('ls -l /proc/%s/fd/ | wc -l' %self.comPid, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        self.comsaFileDescriptorsOpen.append(int(result[1]))
        self.myLogger.debug('leave getNumberOfOpenFileDescriptors')

    def prepareForCmNotificationsTesting(self):
        self.myLogger.debug('enter prepareForCmNotificationsTesting')

        self.tempdir_on_target = '/home/SDP1724_tempdir/'
        self.path_to_cfgFile = '/home/'
        result = self.sshLib.sendCommand('mkdir %s' %self.tempdir_on_target, self.activeController[0], self.activeController[1])
        self.fail(result[0],result[1])
        self.copyModelFilesToTarget()
        self.registeringModelFiles()
        self.loadingClassesToImm()
        self.loadingObjectsToImm()
        self.copyTestCompToActiveSC()
        self.populateTestConsumerConfigFiles()
        self.copyTestOiToTarget()
        self.ToggleNotifyingFlag()
        self.restartCom()

        self.myLogger.debug('leave prepareForCmNotificationsTesting')

    def copyModelFilesToTarget(self):
        if self.modelfile_mp1 != "":
            self.setTestStep('Copy model files to target')
            result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_mp1), self.tempdir_on_target, timeout = 60)
            self.fail(result[0],result[1])

        if self.modelfile_mp2 != "":
            result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_mp2), self.tempdir_on_target, timeout = 60)
            self.fail(result[0],result[1])

        if self.modelfile_mp3 != "":
            result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_mp3), self.tempdir_on_target, timeout = 60)
            self.fail(result[0],result[1])

        if self.modelfile_mp4 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_mp4), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_mp5 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_mp5), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_classes1 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_classes1), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_classes2 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_classes2), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_classes3 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_classes3), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_classes4 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_classes4), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_classes5 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_classes5), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_objects1 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_objects1), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_objects2 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_objects2), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_objects3 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_objects3), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_objects4 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_objects4), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

        if self.modelfile_imm_objects5 != "":
                result = self.sshLib.remoteCopy('%s%s' %(self.modelfile_path, self.modelfile_imm_objects5), self.tempdir_on_target, timeout = 60)
                self.fail(result[0],result[1])

    def registeringModelFiles(self):
        if self.modelfile_mp1 != "":
            self.setTestStep('Registering the model files:mp')
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp1))
            self.fail(result[0],result[1])

        if self.modelfile_mp2 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp2))
            self.fail(result[0],result[1])

        if self.modelfile_mp3 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp3))
            self.fail(result[0],result[1])

        if self.modelfile_mp4 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp4))
            self.fail(result[0],result[1])

        if self.modelfile_mp5 != "":
            result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp5))
            self.fail(result[0],result[1])

    def loadingClassesToImm(self):
        if self.modelfile_imm_classes1 != "":
            self.setTestStep('Loading classes to IMM')
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes1))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes2 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes2))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes3 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes3))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes4 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes4))
            self.fail(result[0],result[1])

        if self.modelfile_imm_classes5 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_classes5))
            self.fail(result[0],result[1])

    def loadingObjectsToImm(self):
        if self.modelfile_imm_objects1 != "":
            self.setTestStep("Loading Objects to IMM")
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects1))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects2 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects2))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects3 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects3))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects4 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects4))
            self.fail(result[0],result[1])

        if self.modelfile_imm_objects5 != "":
            result = self.comsa_lib.importImmClassOrObject(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_imm_objects5))
            self.fail(result[0],result[1])

    def restartCom(self):
        self.setTestStep('Restarting COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        self.fail(result[0], result[1])

    def copyTestCompToActiveSC(self):
        self.sshLib.setConfig(self.activeController[0], self.activeController[1],self.activeController[1])
        if self.test_consumer_1 != '':
            self.setTestStep('Copying the test consumer to the target and Registering to COM')
            self.myLogger.debug('Copying test_consumer to the target under: %s' %self.target_com_compdir)
            result = self.sshLib.remoteCopy('%s%s' %(self.path_to_testConsumer, self.test_consumer_1), self.target_com_compdir, timeout = 60)
            self.fail(result[0],result[1])

            self.miscLib.waitTime(5)
            cmd = "chmod 777 %s%s" %(self.target_com_compdir, self.test_consumer_1)
            result = self.sshLib.sendCommand(cmd);
            self.fail(result[0],result[1])

        if self.test_consumer_2 != '':
            self.myLogger.debug('Copying test_consumer to the target under: %s' %self.target_com_compdir)
            result = self.sshLib.remoteCopy('%s%s' %(self.path_to_testConsumer, self.test_consumer_2), self.target_com_compdir, timeout = 60)
            self.fail(result[0],result[1])

            self.miscLib.waitTime(5)
            cmd = "chmod 777 %s%s" %(self.target_com_compdir, self.test_consumer_2)
            result = self.sshLib.sendCommand(cmd);
            self.fail(result[0],result[1])

        if self.test_consumer_3 != '':
            self.myLogger.debug('Copying test_consumer to the target under: %s' %self.target_com_compdir)
            result = self.sshLib.remoteCopy('%s%s' %(self.path_to_testConsumer, self.test_consumer_3), self.target_com_compdir, timeout = 60)
            self.fail(result[0],result[1])

            self.miscLib.waitTime(5)
            cmd = "chmod 777 %s%s" %(self.target_com_compdir, self.test_consumer_3)
            result = self.sshLib.sendCommand(cmd);
            self.fail(result[0],result[1])

    def populateTestConsumerConfigFiles(self):
        testCons1CfgContent = ''
        testCons2CfgContent = ''
        testCons3CfgContent = ''
        if self.testCons1Regexp1 != '':
            self.setTestStep('Creation of test-consumer-config files and copying it to the target.')
            testCons1CfgContent += self.testCons1Regexp1 + '\n'
        if self.testCons1Regexp2 != '':
            testCons1CfgContent += self.testCons1Regexp2 + '\n'
        if self.testCons1Regexp3 != '':
            testCons1CfgContent += self.testCons1Regexp3 + '\n'
        if self.testCons1Regexp4 != '':
            testCons1CfgContent += self.testCons1Regexp4 + '\n'
        if self.testCons1Regexp5 != '':
            testCons1CfgContent += self.testCons1Regexp5 + '\n'
        if self.testCons2Regexp1 != '':
            testCons2CfgContent += self.testCons2Regexp1 + '\n'
        if self.testCons2Regexp2 != '':
            testCons2CfgContent += self.testCons2Regexp2 + '\n'
        if self.testCons2Regexp3 != '':
            testCons2CfgContent += self.testCons2Regexp3 + '\n'
        if self.testCons2Regexp4 != '':
            testCons2CfgContent += self.testCons2Regexp4 + '\n'
        if self.testCons2Regexp5 != '':
            testCons2CfgContent += self.testCons2Regexp5 + '\n'
        if self.testCons3Regexp1 != '':
            testCons3CfgContent += self.testCons3Regexp1 + '\n'
        if self.testCons3Regexp2 != '':
            testCons3CfgContent += self.testCons3Regexp2 + '\n'
        if self.testCons3Regexp3 != '':
            testCons3CfgContent += self.testCons3Regexp3 + '\n'
        if self.testCons3Regexp4 != '':
            testCons3CfgContent += self.testCons3Regexp4 + '\n'
        if self.testCons3Regexp5 != '':
            testCons3CfgContent += self.testCons3Regexp5 + '\n'

        if testCons1CfgContent != '':
            testCons1CfgFileName = '%s.cfg' %self.test_consumer_1.split('.')[0]
            cmd = 'echo "%s" > %s%s' %(testCons1CfgContent, self.path_to_cfgFile, testCons1CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

        if testCons2CfgContent != '':
            testCons2CfgFileName = '%s.cfg' %self.test_consumer_2.split('.')[0]
            cmd = 'echo "%s" > %s%s' %(testCons2CfgContent, self.path_to_cfgFile, testCons2CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

        if testCons3CfgContent != '':
            testCons3CfgFileName = '%s.cfg' %self.test_consumer_3.split('.')[0]
            cmd = 'echo "%s" > %s%s' %(testCons3CfgContent, self.path_to_cfgFile, testCons3CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

    def copyTestOiToTarget(self):
        if self.testOIarg1 != "":
            self.setTestStep("Copy test object implementer binary to target")
            result = self.sshLib.remoteCopy('%s%s' %(self.testOI_path_in_fileSystem, self.testOI_name), self.tempdir_on_target, timeout = 60)
            self.fail(result[0], result[1])
            result = self.sshLib.sendCommand('chmod +x %s%s' %(self.tempdir_on_target, self.testOI_name))
            self.fail(result[0], result[1])


    def ToggleNotifyingFlag(self):
        if self.enable_class_notify_1 != "" and self.enable_objectOrAttr_1 != "":
            self.setTestStep("Toggle Notify Flag")
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_1,self.enable_objectOrAttr_1)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.disable_class_notify_1 != "" and self.disable_objectOrAttr_1 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_1,self.disable_objectOrAttr_1)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_2 != "" and self.disable_objectOrAttr_2 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_2,self.disable_objectOrAttr_2)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_2 != "" and self.enable_objectOrAttr_2 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_2,self.enable_objectOrAttr_2)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_3 != "" and self.disable_objectOrAttr_3 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_3,self.disable_objectOrAttr_3)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_3 != "" and self.enable_objectOrAttr_3 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_3,self.enable_objectOrAttr_3)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_4 != "" and self.disable_objectOrAttr_4 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_4,self.disable_objectOrAttr_4)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_4 != "" and self.enable_objectOrAttr_4 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_4,self.enable_objectOrAttr_4)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_5 != "" and self.disable_objectOrAttr_5 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_5,self.disable_objectOrAttr_5)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_5 != "" and self.enable_objectOrAttr_5 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_5,self.enable_objectOrAttr_5)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_6 != "" and self.disable_objectOrAttr_6 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_6,self.disable_objectOrAttr_6)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_6 != "" and self.enable_objectOrAttr_6 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_6,self.enable_objectOrAttr_6)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_7 != "" and self.disable_objectOrAttr_7 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_7,self.disable_objectOrAttr_7)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_7 != "" and self.enable_objectOrAttr_7 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_7,self.enable_objectOrAttr_7)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_8 != "" and self.disable_objectOrAttr_8 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_8,self.disable_objectOrAttr_8)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_8 != "" and self.enable_objectOrAttr_8 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_8,self.enable_objectOrAttr_8)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_9!= "" and self.disable_objectOrAttr_9 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_9,self.disable_objectOrAttr_9)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_9 != "" and self.enable_objectOrAttr_9 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_9,self.enable_objectOrAttr_9)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_10 != "" and self.disable_objectOrAttr_10 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_10,self.disable_objectOrAttr_10)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_10 != "" and self.enable_objectOrAttr_10 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_10,self.enable_objectOrAttr_10)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_11 != "" and self.disable_objectOrAttr_11 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_11,self.disable_objectOrAttr_11)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_11 != "" and self.enable_objectOrAttr_11 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_11,self.enable_objectOrAttr_11)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_12 != "" and self.disable_objectOrAttr_12 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_12,self.disable_objectOrAttr_12)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_12 != "" and self.enable_objectOrAttr_12 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_12,self.enable_objectOrAttr_12)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_13 != "" and self.disable_objectOrAttr_13 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_13,self.disable_objectOrAttr_13)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_13 != "" and self.enable_objectOrAttr_13 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_13,self.enable_objectOrAttr_13)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_14 != "" and self.disable_objectOrAttr_14 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_14,self.disable_objectOrAttr_14)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_14 != "" and self.enable_objectOrAttr_14 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_14,self.enable_objectOrAttr_14)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_15 != "" and self.disable_objectOrAttr_15 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_15,self.disable_objectOrAttr_15)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_15 != "" and self.enable_objectOrAttr_15 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_15,self.enable_objectOrAttr_15)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_16 != "" and self.disable_objectOrAttr_16 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_16,self.disable_objectOrAttr_16)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_16 != "" and self.enable_objectOrAttr_16 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_16,self.enable_objectOrAttr_16)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_17 != "" and self.disable_objectOrAttr_17 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_17,self.disable_objectOrAttr_17)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_17 != "" and self.enable_objectOrAttr_17 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_17,self.enable_objectOrAttr_17)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_18 != "" and self.disable_objectOrAttr_18 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_18,self.disable_objectOrAttr_18)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_18 != "" and self.enable_objectOrAttr_18 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_18,self.enable_objectOrAttr_18)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_19 != "" and self.disable_objectOrAttr_19 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_19,self.disable_objectOrAttr_19)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_19 != "" and self.enable_objectOrAttr_19 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_19,self.enable_objectOrAttr_19)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_20 != "" and self.disable_objectOrAttr_20 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_20,self.disable_objectOrAttr_20)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_20 != "" and self.enable_objectOrAttr_20 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_20,self.enable_objectOrAttr_20)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.disable_class_notify_21 != "" and self.disable_objectOrAttr_21 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_21,self.disable_objectOrAttr_21)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_21 != "" and self.enable_objectOrAttr_21 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_21,self.enable_objectOrAttr_21)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_22 != "" and self.disable_objectOrAttr_22 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_22,self.disable_objectOrAttr_22)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_22 != "" and self.enable_objectOrAttr_22 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_22,self.enable_objectOrAttr_22)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_23 != "" and self.disable_objectOrAttr_23 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_23,self.disable_objectOrAttr_23)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_23 != "" and self.enable_objectOrAttr_23 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_23,self.enable_objectOrAttr_23)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_24 != "" and self.disable_objectOrAttr_24 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_24,self.disable_objectOrAttr_24)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_24 != "" and self.enable_objectOrAttr_24 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_24,self.enable_objectOrAttr_24)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_25 != "" and self.disable_objectOrAttr_25 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_25,self.disable_objectOrAttr_25)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_25 != "" and self.enable_objectOrAttr_25 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_25,self.enable_objectOrAttr_25)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_26 != "" and self.disable_objectOrAttr_26 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_26,self.disable_objectOrAttr_26)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_26 != "" and self.enable_objectOrAttr_26 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_26,self.enable_objectOrAttr_26)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_27 != "" and self.disable_objectOrAttr_27 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_27,self.disable_objectOrAttr_27)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_27 != "" and self.enable_objectOrAttr_27 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_27,self.enable_objectOrAttr_27)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_28 != "" and self.disable_objectOrAttr_28 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_28,self.disable_objectOrAttr_28)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_28 != "" and self.enable_objectOrAttr_28 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_28,self.enable_objectOrAttr_28)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_29 != "" and self.disable_objectOrAttr_29 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_29,self.disable_objectOrAttr_29)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_29 != "" and self.enable_objectOrAttr_29 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_19,self.enable_objectOrAttr_29)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

        if self.disable_class_notify_30 != "" and self.disable_objectOrAttr_30 != "":
            cmd = 'immcfg --class-name  %s --disable-attr-notify %s' %(self.disable_class_notify_30,self.disable_objectOrAttr_30)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])
        if self.enable_class_notify_30 != "" and self.enable_objectOrAttr_30 != "":
            self.myLogger.debug('Toggle Notify Flag, enable sending Notifications')
            cmd = 'immcfg --class-name  %s --enable-attr-notify %s' %(self.enable_class_notify_30,self.enable_objectOrAttr_30)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[1] != "":
                self.fail("ERROR", "The response of the command should be an empty response but it returned : %s" %result[1])

    def tearDownProcedureForCmNotificationsTest(self):
        failures = []

        if self.modelfile_mp1 != "":
            #Remove the loaded MOM files
            self.setTestStep("Remove the loaded MOM Files")
            result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp1))
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_mp2 != "":
            result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp2))
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_mp3 != "":
            result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp3))
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_mp4 != "":
            result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp4))
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_mp5 != "":
            result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.tempdir_on_target, self.modelfile_mp5))
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        # Remove the test consumers from target
        self.setTestStep('tearDown: Removing the used test_consumers')
        if self.test_consumer_1 != '':
            self.myLogger.debug('tearDown: Removing test_consumer_1 from the target under: %s' %self.target_com_compdir)
            cmd = '\\rm -f %s%s'%(self.target_com_compdir,self.test_consumer_1)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])
            testCons1CfgFileName = '%s.cfg' %self.test_consumer_1.split('.')[0]
            cmd = '\\rm -f %s%s'%(self.path_to_cfgFile, testCons1CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.test_consumer_2 != '':
            self.myLogger.debug('tearDown: Removing test_consumer_2 from the target under: %s' %self.target_com_compdir)
            cmd = '\\rm -f %s%s'%(self.target_com_compdir,self.test_consumer_2)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])
            testCons2CfgFileName = '%s.cfg' %self.test_consumer_2.split('.')[0]
            cmd = '\\rm -f %s%s'%(self.path_to_cfgFile, testCons2CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.test_consumer_3 != '':
            self.myLogger.debug('tearDown: Removing test_consumer_3 from the target under: %s' %self.target_com_compdir)
            cmd = '\\rm -f %s%s'%(self.target_com_compdir,self.test_consumer_3)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])
            testCons3CfgFileName = '%s.cfg' %self.test_consumer_3.split('.')[0]
            cmd = '\\rm -f %s%s'%(self.path_to_cfgFile, testCons3CfgFileName)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        #Restart COM
        #self.restartCom()
        for controller in self.controllers:
            result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
            self.fail(result[0], result[1])

        if self.pattern_1 != "":
            result = self.comsa_lib.removeImmObjects(self.pattern_1, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.pattern_2 != "":
            result = self.comsa_lib.removeImmObjects(self.pattern_2, self.activeController[0], self.activeController[1])
            if result [0] != 'SUCCESS':
                failures.append(result[1])

        if self.pattern_3 != "":
            result = self.comsa_lib.removeImmObjects(self.pattern_3, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.pattern_4 != "":
            result = self.comsa_lib.removeImmObjects(self.pattern_4, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.pattern_5 != "":
            result = self.comsa_lib.removeImmObjects(self.pattern_5, self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        #Remove the loaded classes
        self.setTestStep("Remove the loaded classes")

        if self.modelfile_imm_classes1 != "":
            result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes1), self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_imm_classes2 != "":
            result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes2), self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_imm_classes3 != "":
            result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes3), self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_imm_classes4 != "":
            result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes4), self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        if self.modelfile_imm_classes5 != "":
            result = self.comsa_lib.removeImmClassesFromImportedModelFile('%s%s'%(self.tempdir_on_target, self.modelfile_imm_classes5), self.activeController[0], self.activeController[1])
            if result[0] != 'SUCCESS':
                failures.append(result[1])

        # Remove temporary directory from target
        cmd = '\\rm -rf %s' %self.tempdir_on_target
        self.myLogger.debug('tearDown: Remove temporary directory from target by: %s' %cmd)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        if result[0] != 'SUCCESS':
            failures.append(result[1])

        # Workaround for TR HR10473
        pattern = '/usr/lib64/opensaf/osafntfimcnd active'
        if pattern != '':
           result = self.comsa_lib.findAndRestartActiveProcessFromPattern(pattern, self.testConfig)
        if result[0] != 'SUCCESS':
            failures.append(result[1])

        if len(failures) != 0:
            self.fail("Error", "The following issues appeared during the phase of teardown: %s"%str(failures))



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
