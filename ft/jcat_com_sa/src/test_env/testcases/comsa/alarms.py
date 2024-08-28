import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib
from java.lang import System

class Alarms(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )
        # parameters from the config files
        self.pathToConfigFiles = {}
        self.useExternalModels = {}
        self.momFile = {}
        self.immClassesFile = {}
        self.immObjectsFile = {}
        self.comsaConfigFile = {}
        self.immObjPattern = '[]'
        self.serviceInstanceName = 'ComSa'
        self.amfNodePattern = 'Cmw'
        self.syslogDir = '/var/log/'
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.comsaConfigFilePathOnTarget = '/storage/system/config/comsa_for_coremw-apr9010555/etc/'
        self.MR38690 = '/home/MR38690/'
        self.mapUUIDToAddTextFlag = ''
        self.ntfsendMsg = ""
        self.ntfsendMsg2 = ""
        self.expectedDN = ""
        self.expectedMajorType = ""
        self.expectedMinorType = ""
        self.expectedAlarmMsg = ""
        self.expectedAlarmMsg_2 = ""
        self.expectedAddInfo = ""
        self.expectedAddInfo_2 = ""
        self.expectedAddInfo_3 = ""
        self.expectedAddInfo_4 = ""
        self.expectedAddText = ""
        self.expectedAddText_2 = ""
        self.expectedErrorLog = ""
        self.raisedAlarm = ""
        self.mr38690Flag = ""
        self.checkAlarmLogsAlertLogs = ""
        self.userDefinedPath = ""
        self.numOfFolder = ""
        self.nbiRootDir = '/var/filem/nbi_root/'
        self.internalRootDir = '/var/filem/internal_root'
        self.pathToProcess = '/usr/lib64/opensaf/'
        self.processName = 'osafckptnd'
        self.fileMconfFile = '/usr/share/filem/internal_filem_root.conf'
        self.nbiConfigPath = '/usr/share/ericsson/cba/nbi-root-dir'
        self.nbiConfigPathBck = '/home/HU39667/nbi-root-dir.bak'
        self.nbiConfigValue = '/storage/tmp/HU39667'
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.reqCmwRelease = ""
        self.reqCmwVersion = ""
        self.reqComRelease = ""
        self.reqComVersion = ""
        self.reqComSaRelease = ""
        self.reqComSaVersion = ""


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
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT763_MODELFILE_PATH"))
        self.installStressTool = eval(System.getProperty("runStressTool"))
        self.testDir =  '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST"))
        self.rlistLocation = "/cluster/storage/clear/comsa_for_coremw-apr9010555/rplist/"
        self.alarmsListName = "FmActiveAlarmList2"

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        self.sshLib.setConfig(self.activeController[0], self.activeController[1], self.activeController[1])

        self.logger.info('Exit setUp')

    def runTest(self):
        self.setTestStep('runTest')
        ComsaOK = ('SUCCESS', True)
        ComOK = ('SUCCESS', True)
        CmwOK = ('SUCCESS', True)
        self.skip_test = False

        if self.raisedAlarm == "True" or self.mr38690Flag == "True":
            self.setTestStep('Check the required versions of ComSA, COM and CMW is installed')
            ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
            self.fail(ComsaOK[0],ComsaOK[1])
            # Check the coremw and com version in case TR HS54955
            if self.raisedAlarm == "True":
                ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion )
                self.fail(ComOK[0],ComOK[1])
                CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
                self.fail(CmwOK[0],CmwOK[1])
            # Check the number of payload in case TR HS54955
            if ComsaOK[1] and ComOK[1] and CmwOK[1]:
                if self.raisedAlarm == "True":
                    if len(self.testConfig['payloads']) == 0:
                        self.skip_test = True
            else:
                self.skip_test = True

        if self.installStressTool:
            self.setTestStep('======== Install the stress tool ========')
            self.comsa_lib.installStressToolOnTarget(self)
            stressTimeOut = 60
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

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, no disk stress
            #result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 0, 0)

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM
            # plus NFS disk stress 1 task 64K bytes blocks plus local disk stress 2 tasks 4M bytes blocks
            result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)
            self.sshLib.setTimeout(stressTimeOut)

        if self.skip_test == False:
            if self.checkAlarmLogsAlertLogs == "True":
                #checking the existence of Alarm and Alert logs in the NBI root directory
                self.myLogger.info('Check the existence of AlarmLogs and AlertLogs in the NBI root directory')
                cmd = "ls -l %s | grep -w 'AlarmLogs\|AlertLogs' | wc -l" %self.nbiRootDir
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0], result[1])
                if result[1] != self.numOfFolder:
                    self.fail('ERROR', 'AlarmLogs or AlertLogs is not exist in the %s' %self.nbiRootDir)
                #checking the existence of Alarm and Alert logs links in internalRoot directory
                #checking the existence in user defined directory
                self.myLogger.info('Check the existence of AlarmLogs and AlertLogs links in the user defined directory')
                cmd = 'mkdir -p %s' %self.userDefinedPath
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                cmd = "echo %s > %s" %(self.userDefinedPath,self.fileMconfFile)
                result=self.sshLib.sendCommand(cmd,self.activeController[0], self.activeController[1])
                #restarting COM to reflect changes
                self.comRestartTimeout = 10
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                self.fail(result[0],result[1])
                self.myLogger.info('Check the existence of AlarmLogs and AlertLogs links in the %s directory' %self.userDefinedPath)
                cmd = "ls -l %s | grep -w 'AlarmLogs\|AlertLogs' | wc -l" %self.userDefinedPath
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0], result[1])
                if result[1] != self.numOfFolder:
                    self.fail('ERROR', 'AlarmLogs or AlertLogs links is not exist in the %s' %self.userDefinedPath)
                cmd = 'rm -rf %s' %self.userDefinedPath
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                cmd = 'rm -f %s' %self.fileMconfFile
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                cmd = 'cp %s %s' %(self.nbiConfigPath,self.nbiConfigPathBck)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                cmd = 'echo %s > %s' %(self.nbiConfigValue,self.nbiConfigPath)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                cmd = 'mkdir -p %s' %self.nbiConfigValue
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                #Restarting COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                self.fail(result[0],result[1])
                self.myLogger.info('Check the existence of AlarmLogs and AlertLogs links in the in %s directory' %self.nbiConfigValue)
                cmd = "ls -l %s | grep -w 'AlarmLogs\|AlertLogs' | wc -l" %self.nbiConfigValue
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0], result[1])
                if result[1] != self.numOfFolder:
                    self.fail('ERROR', 'AlarmLogs or AlertLogs links is not exist in the %s' %self.nbiConfigValue)
                #checking the existence of Alarm and Alert logs links in /var/filem/internal_root
                cmd = 'rm %s' %self.nbiConfigPath
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                #Restarting COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                self.fail(result[0],result[1])
                self.myLogger.info('Check the existence of AlarmLogs and AlertLogs links in the in %s directory' %self.internalRootDir)
                cmd = "ls -l %s | grep -w 'AlarmLogs\|AlertLogs' | wc -l" %self.internalRootDir
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0], result[1])
                if result[1] != self.numOfFolder:
                    self.fail('ERROR', 'AlarmLogs or AlertLogs links is not exist in the %s' %self.internalRootDir)
                # Restoring the backup
                cmd = 'cp %s %s' %(self.nbiConfigPathBck,self.nbiConfigPath)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                cmd = 'rm -rf %s' %self.nbiConfigValue
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                #Restarting COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                self.fail(result[0],result[1])
            else:
                if self.useExternalModels == 'yes' or self.mapUUIDToAddTextFlag == "NotANumber":
                    result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
                    self.fail(result[0], result[1])
                    self.activeController = result[1]
                    if self.useExternalModels == 'yes':
                        self.comRestartTimeout = 10

                        self.setTestStep('Upload model files to the target')
                        cmd = 'mkdir -p %s' %self.modelFilePathOnTarget
                        result = self.sshLib.sendCommand(cmd)
                        self.fail(result[0],result[1])

                        #Copying model files to target for case_1
                        self.myLogger.debug('Copy model files to target')
                        result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile), self.modelFilePathOnTarget, timeout = 60)
                        self.fail(result[0],result[1])
                        result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile), self.modelFilePathOnTarget, timeout = 60)
                        self.fail(result[0],result[1])
                        result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immObjectsFile), self.modelFilePathOnTarget, timeout = 60)
                        self.fail(result[0],result[1])

                        self.setTestStep('### Loading model files to IMM - (Load classes and create objects in IMM)')

                        #Change permissions of model files before loading model files
                        self.myLogger.debug('Change permission of all model files')
                        cmd = 'chmod -R 777 %s'%self.modelFilePathOnTarget
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0], result[1])

                        self.myLogger.debug('Loading model files')
                        cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile)
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0],result[1])
                        if result[1] != '':
                            self.fail('ERROR', result[1])

                        cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immObjectsFile)
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0],result[1])
                        if result[1] != '':
                            self.fail('ERROR', result[1])

                        self.myLogger.debug('Loading mp (MOM) files')
                        cmd = '/opt/com/bin/com_mim_tool --addModelFile=%s%s'%(self.modelFilePathOnTarget,self.momFile)
                        self.fail(result[0], result[1])
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        cmd = '/opt/com/bin/com_mim_tool --commit'
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0], result[1])

                        # Restart COM
                        self.myLogger.debug('Restart COM')
                        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                        self.fail(result[0],result[1])

                if self.mr38690Flag == "True":
                    # Create MR38690 folder
                    result = self.sshLib.sendCommand('mkdir %s' %self.MR38690)
                    self.fail(result[0],result[1])

                    # Copy the ntfsend executable to target cluster
                    result = self.sshLib.remoteCopy('%s/ntfsend/ntfsend' %self.testDir, self.MR38690, timeout = 120)
                    self.fail(result[0],result[1])

                    result = self.sshLib.sendCommand('chmod +x %s/ntfsend' %self.MR38690)
                    self.fail(result[0],result[1])

                    # Copy the comsa.cfg to temporary directory
                    cmd = '\cp %s%s %s' %(self.comsaConfigFilePathOnTarget,self.comsaConfigFile, self.MR38690)
                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0],result[1])

                    # Set the uuidmapping variable to 0
                    if self.mapUUIDToAddTextFlag == "0":
                        cmd = "sed -i 's/uuidmapping=.*/uuidmapping=0/' %s%s" %(self.comsaConfigFilePathOnTarget,self.comsaConfigFile)

                    # Set the uuidmapping variable to 0
                    elif self.mapUUIDToAddTextFlag == "1":
                        cmd = "sed -i 's/uuidmapping=.*/uuidmapping=1/' %s%s" %(self.comsaConfigFilePathOnTarget,self.comsaConfigFile)

                    # Set the uuidmapping variable to 0
                    elif self.mapUUIDToAddTextFlag == "2":
                        cmd = "sed -i 's/uuidmapping=.*/uuidmapping=2/' %s%s" %(self.comsaConfigFilePathOnTarget,self.comsaConfigFile)

                    # Set the uuidmapping variable to value is different to 0; 1 or 2
                    else:
                        cmd = "sed -i 's/uuidmapping=.*/uuidmapping=m/' %s%s" %(self.comsaConfigFilePathOnTarget,self.comsaConfigFile)

                    result = self.sshLib.sendCommand(cmd)
                    self.fail(result[0],result[1])

                self.startUnixTime = 0

                linuxTimeText = "Linux Time:"

                self.setTestStep("Getting Linux System Time")
                dateCommand = "date +%s"
                result = self.sshLib.sendCommand(dateCommand)
                self.fail(result[0],result[1])
                self.startTime = int(result[1])
                self.myLogger.info("Linux System Time is : %s" %(self.startTime))

                if self.raisedAlarm == "True":
                        self.setTestStep("Sending the Alarm to the target")
                        if self.installStressTool:
                            self.miscLib.waitTime(150)
                        noOfSCs = len(self.testConfig['controllers'])
                        plHostname = self.testConfig['testNodesNames'][noOfSCs] # this is the first payload
                        removeProcessCommand = "ssh %s '\\rm -rf %s%s'" %(plHostname, self.pathToProcess,self.processName)
                        result = self.sshLib.sendCommand(removeProcessCommand)
                        self.fail(result[0],result[1])
                        getProcessId = "ssh %s 'pgrep -f %s%s'" %(plHostname, self.pathToProcess,self.processName)
                        result = self.sshLib.sendCommand(getProcessId)
                        self.fail(result[0],result[1])
                        processId = int(result[1])
                        killProcessIdCommand = "ssh %s 'kill -9 %d'" %(plHostname, processId)
                        result = self.sshLib.sendCommand(killProcessIdCommand)
                        self.fail(result[0],result[1])
                        self.miscLib.waitTime(150)
                else:
                    self.setTestStep("Sending the Alarm to the target")
                    if self.installStressTool:
                        self.miscLib.waitTime(150)

                    if self.mr38690Flag == "True":
                        # Restart com
                        cmd = 'comsa-mim-tool com_switchover'
                        result = self.sshLib.sendCommand(cmd)
                        self.fail(result[0], result[1])
                        self.miscLib.waitTime(20)

                        result = self.sshLib.sendCommand('%s%s %s%s"' %(self.MR38690, self.ntfsendMsg, linuxTimeText, self.startTime))
                    else:
                        result = self.sshLib.sendCommand('%s %s%s"' %(self.ntfsendMsg, linuxTimeText, self.startTime))
                    if self.installStressTool:
                        self.miscLib.waitTime(200)
                    self.fail(result[0], result[1])

                allowedIterations=15
                waitBetweenIterations=10
                self.setTestStep('Search for the new alarm in the alarm log')
                expected_List = self.createExpectedList('%s%s' %(linuxTimeText, str(self.startTime)))
                subrack = 0
                slot = 0

                #check for COMSA 3.2
                tmpComSaRelease = "3"
                tmpComSaMajorVersion = "4"
                ComSaMajorOK = ('SUCCESS', True)
                ComSaMajorOK = self.lib.checkComponentMajorVersion('comsa', tmpComSaRelease, tmpComSaMajorVersion, [], True)

                if ComSaMajorOK[1] == False:
                    expected_List[0] = expected_List[0].replace('CmwIdPmp', 'CmwPmpId')

                for iteration in range(allowedIterations):
                    if self.installStressTool:
                        self.miscLib.waitTime(200)
                    result = self.comsa_lib.getEventTimestampFromAlarmAlertLog(subrack, slot, expected_List, self.startTime, self.testConfig)
                    if result[0] == 'SUCCESS':
                        break
                    else:
                        self.miscLib.waitTime(waitBetweenIterations)
                self.fail(result[0], result[1])

                if self.mapUUIDToAddTextFlag == "NotANumber":
                    self.setTestStep('Search for the error log in the syslog')
                    self.expectedErrorlog()

        else:
            if len(self.testConfig['payloads']) == 0:
                self.logger.info('Skipped trace tests because of no payloads!')
                self.setAdditionalResultInfo('Test skipped; no payloads')
            if ComsaOK[1] == False or ComOK[1] == False or CmwOK[1] == False:
                self.logger.info('Skipped trace tests because of CMW/COM/COMSA version not compatible!')
                self.setAdditionalResultInfo('Test skipped; version not compatible')

        self.myLogger.info("exit runTest")

        coreTestCase.CoreTestCase.runTest(self)

    def tearDown(self):
        self.setTestStep('tearDown')
        if self.skip_test == False:
            if self.checkAlarmLogsAlertLogs == "True":
                self.myLogger.info('Teardown completed')
            else:
                if self.raisedAlarm == "True":
                    self.setTestStep("Clear Alarm from the target")
                    result = self.comsa_lib.stopOpensafService(self.testConfig)
                    self.fail(result[0],result[1])
                    cmd='//rm -f %s/%s/*' %(self.rlistLocation, self.alarmsListName)
                    self.fail(result[0],result[1])
                    result = self.comsa_lib.startOpensafService(self.testConfig)
                    self.fail(result[0],result[1])

                else:
                    self.setTestStep("Clear Alarm from the target")
                    if self.mr38690Flag == "True":
                        result = self.sshLib.sendCommand('%s%s"' %(self.MR38690, self.ntfsendMsg2))
                    else:
                        result = self.sshLib.sendCommand('%s"' %self.ntfsendMsg2)
                    self.fail(result[0], result[1])

                    if self.useExternalModels == 'yes':

                        result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                        self.fail(result[0],result[1])

                        # Restart COM
                        self.myLogger.debug('Restart COM')
                        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, self.comRestartTimeout)
                        self.fail(result[0],result[1])

                        self.setTestStep('### Removing model files from IMM')

                        #Removing model files
                        self.myLogger.debug('Removing the IMM models')
                        help = """ In order to clean the IMM from the objects and classes in a dynamic way we need to define a list of patterns
                        of the imm_objects which should be searched for with immlist and all the matches will be removed with immcfg -d.
                        We have to be careful what we provide and should always test manually before automating, to make sure that we
                        do not remove something that should remain!
                        """
                        if len(eval(self.immObjPattern)) > 0:
                            immObjPatterns = eval(self.immObjPattern)
                            for immObjPattern in immObjPatterns:
                                cmd = 'immfind | grep -i %s | xargs immcfg -d' %immObjPattern
                                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                                self.fail(result[0],result[1])
                                if result[1] != '':
                                    self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))

                        # Below we remove all the classes imported from the imm_classes model file
                        cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile)
                        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                        self.fail(result[0],result[1])
                        if result[1] != '':
                            self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))

                        cmd = "\\rm -rf %s" %self.modelFilePathOnTarget
                        result = self.sshLib.sendCommand(cmd)
                        self.fail(result[0], result[1])
                    if self.mr38690Flag == "True":
                        # Copy the comsa.cfg file to old position
                        cmd = '\cp %s%s %s' %(self.MR38690,self.comsaConfigFile, self.comsaConfigFilePathOnTarget)
                        result = self.sshLib.sendCommand(cmd)
                        self.fail(result[0],result[1])

                        # Restart com
                        cmd = 'comsa-mim-tool com_switchover'
                        result = self.sshLib.sendCommand(cmd)
                        self.fail(result[0], result[1])
                        self.miscLib.waitTime(20)

                        # Remove test directory
                        command = '\\rm -rf /home/MR38690/'
                        self.sshLib.sendCommand(command)

        else:
            self.myLogger.info('Teardown skipped')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

        #########################
        #### SUPPORT METHODS ####
        #########################

    def createExpectedList(self, unixTimeString):
        self.myLogger.debug('createExpectedList() enter')
        expectedList = []

        if self.expectedDN != "":
            expectedList.append(self.expectedDN)
        if self.expectedMajorType != "":
            expectedList.append(self.expectedMajorType)
        if self.expectedMinorType != "":
            expectedList.append(self.expectedMinorType)
        if self.expectedAlarmMsg != "":
            expectedList.append(self.expectedAlarmMsg)
        if self.expectedAlarmMsg_2 != "":
            expectedList.append(self.expectedAlarmMsg_2)
        if self.expectedAddText != "":
            expectedList.append(self.expectedAddText)
        if self.expectedAddText_2 != "":
            expectedList.append(self.expectedAddText_2)
        if self.expectedAddInfo != "":
            expectedList.append(self.expectedAddInfo)
        if self.expectedAddInfo_2 != "":
            expectedList.append(self.expectedAddInfo_2)
        if self.expectedAddInfo_3 != "":
            expectedList.append(self.expectedAddInfo_3)
        if self.expectedAddInfo_4 != "":
            expectedList.append(self.expectedAddInfo_4)
        if self.raisedAlarm != "True":
            expectedList.append(unixTimeString)

        for i in range (0, len(expectedList)):
            self.myLogger.info('ExpectedList[%s]: (%s)' %(str(i), expectedList[i]))

        self.myLogger.debug('createExpectedList() leave')
        return expectedList

    def expectedErrorlog(self):
        if self.expectedErrorLog != {}:
            self.evaluateExpectedSearchPattern([self.expectedErrorLog], self.startTime, self.syslogDir)

    def evaluateExpectedSearchPattern(self, searchPattern, startSearchTime, logDir):
        result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPattern, startSearchTime, self.testConfig, logDir)
        self.sshLib.tearDownHandles()
        self.fail(result[0],result[1])
        self.myLogger.debug('Found %s in log at: %s' %(searchPattern,result[1]))

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases

