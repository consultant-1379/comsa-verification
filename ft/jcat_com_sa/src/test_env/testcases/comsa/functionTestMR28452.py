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
    Install, Upgrade, CmwComComSA
    Test cases:

    ==================================
    TEST CASE SPECIFICATION:

    Tag:
    TC-MR28452-001  UC1: Install CMW3.3, COM3.4, COMSA3.4 build
    TC-MR28452-002  UC6: Install CMW3.3, COM3.3, COMSA3.4 build -> upgrade to COM3.4
    TC-MR28452-003  UC5: Install CMW3.3, COM3.3, COMSA3.3 -> upgrade to COMSA3.4 build
    TC-MR28452-004  UC4: Install CMW3.3, COM3.3, COMSA3.3 -> upgrade to COM3.4 then COMSA3.4 build
    TC-MR28452-005  UC2: Install CMW3.3, COM3.3, COMSA3.3 -> upgrade to COMSA3.4 build then COM3.4



    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
from se.ericsson.jcat.fw import SUTHolder
import os
import sys
import re
import omp.tf.misc_lib as misc_lib
import omp.tf.ssh_lib as ssh_lib
from java.lang import System

class backupAndInstallOfCmwComComsaMR28452(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.testcase_tag = tag
        # parameters from the config files

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        self.tmpdirMR28452 = {}
        self.clusterTime = ''

        self.expectedStatusOutput1R1_line1 = "Linked To: 'IMM_R1'"
        self.expectedStatusOutput1R1_line2 = ""

        self.expectedStatusOutput1R2_line1 = "Linked To: 'IMM_R2'"
        self.expectedStatusOutput1R2_line2 = ""

        self.expectedStatusOutput1_shift1 = 1
        self.expectedStatusOutput1_shift2 = 2

        self.expectedStatusOutput2_line1 = "Consumer Location: <Empty> on node <Empty>"
        self.expectedStatusOutput2_line2 = "Action: modify"
        self.expectedStatusOutput2_line3 = "State: Waiting for consumer"
        self.expectedStatusOutput2_line4 = ""

        self.expectedStatusOutput_shift1 = 1
        self.expectedStatusOutput_shift2 = 5
        self.expectedStatusOutput_shift3 = 6
        self.expectedStatusOutput_shift4 = 7

        self.reqComSaRelease = "3"
        self.reqComSaMajorVersion = "5"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.buildLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("SRC"))
        self.absDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get("ABS"))
        self.pathOfReleases = '%s%s' %(self.COMSA_REPO_PATH, dict.get("CXP_ARCHIVE"))
        self.testDir =  '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST"))
        self.resourceFilesLocation = dict.get("PATH_TO_MR28452")
        self.uninstallScriptLocation = self.testDir
        self.uninstallScriptName = 'uninstall_cmw.sh'
        self.uninstallScriptLocation2 = dict.get('PATH_TO_MR24760')
        self.uninstallScriptName2 = 'cmw-rm-storage-dirs.sh'
        self.buildSrc = '%s%s' %(self.COMSA_REPO_PATH, dict.get('SRC'))
        self.installSdpName = dict.get('INSTALL_SDP_NAME')
        self.installSdpNameSingle = dict.get('INSTALL_SDP_NAME_SINGLE')
        self.removeSdpName = dict.get('REMOVE_SDP_NAME')
        self.removeSdpNameSingle = dict.get('REMOVE_SDP_NAME_SINGLE')
        self.buildTokenDir = dict.get('BUILD_TOKENS')
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")

        self.distroTypes = eval(dict.get("LINUX_DISTRO_TYPES"))
        result = self.lib.updateLinuxDistroInDictionary(self.testSuiteConfig, self.distroTypes)
        self.fail(result[0], result[1])
        self.linuxDistro = self.testSuiteConfig['linuxDistro']['value']
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.cxpSdpName = dict.get('CXP_SDP_NAME_RHEL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
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

        self.Com33Latest = "%s/com3.3_latest"%self.resourceFilesLocation
        self.Com34Latest = "%s/com3.4_latest"%self.resourceFilesLocation
        self.CoreMWLatest = "%s/cmw3.5_latest"%self.resourceFilesLocation
        self.ComSA34Latest = "%s/comsa"%self.resourceFilesLocation
        self.ComSA33Latest = "%s/comsa3.3_latest"%self.resourceFilesLocation

        self.tmpdirMR28452 = '/home/tmpdirMR28452/'

        self.super__setUp()
        self.sutholder = SUTHolder.getInstance()
        self.currentSut = self.sutholder.zones[0]
        self.TargetDataLib = self.currentSut.getLibrary("TargetDataLib")
        self.targetData = self.TargetDataLib.getTargetData()

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        self.sshKeyUpdater = '%s/%s/fix_known_hosts.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
        self.restoreSnapshot, self.runUninstallationScript = self.utils.snapRestOrUninstScr(self)
        """
        Stress Tool option
        """
        self.installStressTool = eval(System.getProperty("runStressTool"))
        self.myLogger.info('Exit setUp')

    def runTest(self):

        self.setTestStep('runTest')

        ComsaMajorOK = ('SUCCESS', True)
        self.skip_test = False

        if self.restoreSnapshot:
            offlineVersion = ['','','']
            ComsaMajorOK = ['', False]

            result = self.comsa_lib.getOfflineVersion(self.testSuiteConfig, 'COMSA')
            if result[0] == "REGTEST":
                offlineVersion[0] = result[1] #COMSA_release
                offlineVersion[1] = result[2] #COMSA_release
                offlineVersion[2] = result[3] #COMSA_majorVersion
                ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion, offlineVersion = offlineVersion)
            else:
                ComsaMajorOK[1] = True
        elif self.runUninstallationScript:
            ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion)
        else:
            self.fail('ERROR', 'Normally we should not have ended up here: either self.restoreSnapshot or self.runUninstallationScript should be True!')

        if ComsaMajorOK[1] == True:

            self.pathToCmwInstallation = '%s/coremw/' %self.tmpdirMR28452
            self.pathToComInstallation = '%s/com/' %self.tmpdirMR28452
            self.pathToComsaInstallation = '%s/comsa/' %self.tmpdirMR28452

            self.sdpImportCommand = 'cmw-sdp-import'
            self.campaignComsaUgradeName ='ERIC-ComSa-upgrade'

            self.modelTypeR1 = "IMM-I-COM_R1"
            self.modelTypeR2 = "IMM-I-COM_R2"

            self.expectedModelTypeR1Text = "Model Type: '%s'" %self.modelTypeR1
            self.expectedModelTypeR2Text = "Model Type: '%s'" %self.modelTypeR2

            self.cmwLibPath = "/opt/coremw/lib/"
            consumerLocation_part1 = "Consumer Location:      %simm-model-consumer on node SC-" %self.cmwLibPath
            consumerLocation_part2 = "/imm-model-consumer on node SC-"

            expectedModelStatusOutput_lineText_list2 = self.createExpectedStatusOutput_lineText_List2()
            expectedModelStatusOutput_lineShift_list = self.createExpectedStatusOutput_lineShift_List()

            expectedModelStatusOutput_lineTextR1_list1 = self.createExpectedStatusOutput_lineTextR1_List1()
            expectedModelStatusOutput_lineTextR2_list1 = self.createExpectedStatusOutput_lineTextR2_List1()
            expectedModelStatusOutput_lineShift_list1 = self.createExpectedStatusOutput_lineShift_List1()

            self.myLogger.info('Exit setUp')

            self.setTestStep('======== Uninstall system ========')
            # Uninstall system
            if self.runUninstallationScript:
                result = self.comsa_lib.copyFilesToTarget(['%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName)],self.tmpdirMR28452)
                self.fail(result[0], result[1])

                result = self.sshLib.remoteCopy('%s/%s' %(self.uninstallScriptLocation2, self.uninstallScriptName2), self.tmpdirMR28452, timeout = 120)
                self.fail(result[0],result[1])
                result = self.sshLib.sendCommand('chmod +x %s/*.sh' %self.tmpdirMR28452)
                self.fail(result[0], result[1])

            result = self.comsa_lib.unInstallSystem(self.tmpdirMR28452, self.uninstallScriptName, self.testConfig, self.testSuiteConfig, self.linuxDistro, self.distroTypes, self.sshKeyUpdater, resetCluster = self.resetCluster)
            self.fail(result[0], result[1])

            if self.runUninstallationScript:
                cmw_uninstall_command2 = '%s%s' %(self.tmpdirMR28452, self.uninstallScriptName2)
                result = self.sshLib.sendCommand (cmw_uninstall_command2)
                self.fail(result[0], result[1])

            self.lib.resetDumps()

            self.setTestStep('======== Install CoreMW ========')
            result = self.installCMW(self.CoreMWLatest, self.pathToCmwInstallation)
            self.fail(result[0], result[1])

    ############################################################################################
            if self.testcase_tag == 'TC-MR28452-001':
                self.setTestStep('======== Install Com 3.4 ========')
                self.installCOM(self.Com34Latest, self.pathToComInstallation)
                if self.installStressTool:
                    self.mr28452SetupStress()
                    stressTimeOut = 60
                    self.sshLib.setTimeout(stressTimeOut)
                self.setTestStep('======== Check cmw-model-status  ========')
                self.cmw_model_status(self.modelTypeR1, expectedModelStatusOutput_lineText_list2, expectedModelStatusOutput_lineShift_list)
                self.cmw_model_status(self.modelTypeR2, expectedModelStatusOutput_lineText_list2, expectedModelStatusOutput_lineShift_list)
                self.setTestStep('======== Install ComSa 3.4 ========')
                self.logToSys()
                self.installCOMSA(self.ComSA34Latest,  self.pathToComsaInstallation,'True')
                self.setTestStep('======== Check cmw-model-status  ========')
                self.cmw_model_status(self.modelTypeR1, expectedModelStatusOutput_lineTextR1_list1, expectedModelStatusOutput_lineShift_list1,consumerLocation_part1, consumerLocation_part2)
                self.cmw_model_status(self.modelTypeR2, expectedModelStatusOutput_lineTextR2_list1, expectedModelStatusOutput_lineShift_list1, consumerLocation_part1, consumerLocation_part2)
                self.setTestStep('======== Check syslog  ========')
                self.checkWhoDeliveredModel('COM','')

    ############################################################################################
            if self.testcase_tag == 'TC-MR28452-002' or self.testcase_tag == 'TC-MR28452-004':
                self.setTestStep('======== Install Com 3.3 ========')
                self.installCOM(self.Com33Latest, self.pathToComInstallation)
                if self.installStressTool:
                    self.mr28452SetupStress()
                    stressTimeOut = 60
                    self.sshLib.setTimeout(stressTimeOut)
                self.setTestStep('======== Install ComSA 3.3 ========')
                self.installCOMSA(self.ComSA33Latest,  self.pathToComsaInstallation,'False')
                self.setTestStep('======== Upgrade ComSA 3.4 ========')
                self.logToSys()
                self.upgradeCOMSAFromStream(self.pathToComsaInstallation)
                self.setTestStep('======== Check cmw-model-status  ========')
                self.cmw_model_status(self.modelTypeR1, expectedModelStatusOutput_lineTextR1_list1, expectedModelStatusOutput_lineShift_list1,consumerLocation_part1, consumerLocation_part2)
                self.cmw_model_status(self.modelTypeR2, expectedModelStatusOutput_lineTextR2_list1, expectedModelStatusOutput_lineShift_list1,  consumerLocation_part1, consumerLocation_part2)
                self.setTestStep('======== Check syslog  ========')
                self.checkWhoDeliveredModel('COMSA','')

            if self.testcase_tag == 'TC-MR28452-002' :
                self.setTestStep('======== Upgrade Com 3.4 ========')
                self.upgradeCOM(self.Com34Latest, self.pathToComInstallation)
                if self.installStressTool:
                    self.mr28452SetupStress()
                    stressTimeOut = 60
                    self.sshLib.setTimeout(stressTimeOut)
                self.setTestStep('======== Check cmw-model-status  ========')
                self.cmw_model_status(self.modelTypeR1, expectedModelStatusOutput_lineTextR1_list1, expectedModelStatusOutput_lineShift_list1, consumerLocation_part1, consumerLocation_part2)
                self.cmw_model_status(self.modelTypeR2, expectedModelStatusOutput_lineTextR2_list1, expectedModelStatusOutput_lineShift_list1, consumerLocation_part1, consumerLocation_part2)

    ############################################################################################
            if self.testcase_tag == 'TC-MR28452-003':
                self.setTestStep('======== Install Com 3.3 ========')
                self.installCOM(self.Com33Latest, self.pathToComInstallation)
                if self.installStressTool:
                    self.mr28452SetupStress()
                    stressTimeOut = 60
                    self.sshLib.setTimeout(stressTimeOut)
                self.setTestStep('======== Install ComSA 3.3 ========')
                self.installCOMSA(self.ComSA33Latest,  self.pathToComsaInstallation,'False')
                self.setTestStep('======== Upgrade Com 3.4 ========')
                self.upgradeCOM(self.Com34Latest, self.pathToComInstallation)
                self.setTestStep('======== Check cmw-model-status  ========')
                self.cmw_model_status(self.modelTypeR1, expectedModelStatusOutput_lineText_list2, expectedModelStatusOutput_lineShift_list)
                self.cmw_model_status(self.modelTypeR2, expectedModelStatusOutput_lineText_list2, expectedModelStatusOutput_lineShift_list)
                self.setTestStep('======== Upgrade ComSA 3.4 ========')
                self.logToSys()
                self.upgradeCOMSAFromStream(self.pathToComsaInstallation)
                self.setTestStep('======== Check syslog  ========')
                self.checkWhoDeliveredModel('COM','')
                self.setTestStep('======== Check cmw-model-status  ========')
                self.cmw_model_status(self.modelTypeR1, expectedModelStatusOutput_lineTextR1_list1, expectedModelStatusOutput_lineShift_list1,  consumerLocation_part1, consumerLocation_part2)
                self.cmw_model_status(self.modelTypeR2, expectedModelStatusOutput_lineTextR2_list1, expectedModelStatusOutput_lineShift_list1, consumerLocation_part1, consumerLocation_part2)
    ############################################################################################
            if self.testcase_tag == 'TC-MR28452-005':
                self.setTestStep('======== Install Com 3.3 ========')
                self.installCOM(self.Com33Latest, self.pathToComInstallation)
                if self.installStressTool:
                    self.mr28452SetupStress()
                    stressTimeOut = 60
                    self.sshLib.setTimeout(stressTimeOut)
                self.setTestStep('======== Install ComSa 3.4 ========')
                self.logToSys()
                self.installCOMSA(self.ComSA34Latest,  self.pathToComsaInstallation,'True')
                self.setTestStep('======== Check cmw-model-status  ========')
                self.cmw_model_status(self.modelTypeR1, expectedModelStatusOutput_lineTextR1_list1, expectedModelStatusOutput_lineShift_list1, consumerLocation_part1, consumerLocation_part2)
                self.cmw_model_status(self.modelTypeR2, expectedModelStatusOutput_lineTextR2_list1, expectedModelStatusOutput_lineShift_list1, consumerLocation_part1, consumerLocation_part2)
                self.setTestStep('======== Check syslog  ========')
                self.checkWhoDeliveredModel('COMSA','')

    ############################################################################################

                #coreTestCase.CoreTestCase.umerLocation_part1, consumerLocation_part2)unTest(self)
        else:
            self.logger.info('Skipped tests because of COMSA version is not compatible!')
            self.setAdditionalResultInfo('Test skipped; version not compatible')
            self.skip_test = True

        self.myLogger.info("exit runTest")


    def logToSys(self):
        self.logger.info('logToSys: Called')
        #get date time
        command = 'date +%s'
        result = self.sshLib.sendCommand (command)
        self.fail(result[0], result[1])
        self.clusterTime = result[1]

        #log to both SC
        command = 'logger "logToSys: called at %s"' %self.clusterTime
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            result = self.sshLib.sendCommand (command,2,1)
            self.fail(result[0], result[1])
            result = self.sshLib.sendCommand (command,2,2)
            self.fail(result[0], result[1])
        elif noOfScs == 1:
            result = self.sshLib.sendCommand (command)
            self.fail(result[0], result[1])

        self.logger.info('logToSys: exiting')




    def createExpectedStatusOutput_lineText_List2(self):
        self.myLogger.debug('createExpectedStatusOutput_lineText_List() enter')
        lineList = []

        if self.expectedStatusOutput2_line1 != "":
            lineList.append(self.expectedStatusOutput2_line1)
        if self.expectedStatusOutput2_line2 != "":
            lineList.append(self.expectedStatusOutput2_line2)
        if self.expectedStatusOutput2_line3 != "":
            lineList.append(self.expectedStatusOutput2_line3)
        if self.expectedStatusOutput2_line4 != "":
            lineList.append(self.expectedStatusOutput2_line4)

        count = 0
        for line in lineList:
            count += 1
            self.myLogger.debug('Expected model status line[%s]= (%s)' %(str(count),line))
        self.myLogger.debug('createExpectedStatusOutput_lineText_List() leave')
        return lineList


    def createExpectedStatusOutput_lineShift_List(self):
        self.myLogger.debug('createExpectedStatusOutput_lineShift_List() enter')
        shiftList = []

        if self.expectedStatusOutput_shift1 != "":
            shiftList.append(self.expectedStatusOutput_shift1)
        if self.expectedStatusOutput_shift2 != "":
            shiftList.append(self.expectedStatusOutput_shift2)
        if self.expectedStatusOutput_shift3 != "":
            shiftList.append(self.expectedStatusOutput_shift3)
        if self.expectedStatusOutput_shift4 != "":
            shiftList.append(self.expectedStatusOutput_shift4)

        count = 0
        for line in shiftList:
            count += 1
            self.myLogger.debug('Expected model status line shift[%s]= (%s)' %(str(count),line))
        self.myLogger.debug('createExpectedStatusOutput_lineShift_List() leave')
        return shiftList


    def cmw_model_status(self, modelType, lineList = [], shiftList = [], consumerLocationPart1 = "", consumerLocationPart2 = ""):
        self.setTestStep('cmw_model_status')
        self.expectedModelTypeR1Text = "Model Type: '%s'" %self.modelTypeR1
        self.expectedModelTypeR2Text = "Model Type: '%s'" %self.modelTypeR2
        cmd = 'cmw-model-status'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        receivedLines = result[1].splitlines()

        num = 0
        # the line number of the first interesting line (which is the model type)
        firstLine = -1
        if modelType == self.modelTypeR1:
                self.expectedModelTypeR1Text = self.whiteSpaceFilter(self.expectedModelTypeR1Text)
        if modelType == self.modelTypeR2:
                self.expectedModelTypeR2Text = self.whiteSpaceFilter(self.expectedModelTypeR2Text)
                self.expectedModelTypeR1Text ="Not avalable here"
        self.myLogger.debug('self.expectedModelTypeR1Text: (%s) length: (%s)' %(self.expectedModelTypeR1Text,str(len(self.expectedModelTypeR1Text))))
        self.myLogger.debug('self.expectedModelTypeR2Text: (%s) length: (%s)' %(self.expectedModelTypeR2Text,str(len(self.expectedModelTypeR2Text))))

        # line-by-line check which line is the first one (model type)
        for line in receivedLines:
            line = self.whiteSpaceFilter(line)
            self.myLogger.debug('checking line[%s]: (%s) length: (%s)' %(str(num), line, str(len(line))))
            if line == self.expectedModelTypeR1Text  or line == self.expectedModelTypeR2Text:
                # set as first line
                firstLine = num
                self.myLogger.info('Found (%s) in line[%s]: (%s)' %(modelType, str(firstLine), line))
                break
            num += 1

        # if found then check all the lines (compare with the expected lines)
        if firstLine != -1:
            lineNum = 0
            for line in lineList:
                self.checkModelStatusOutput(receivedLines, firstLine, lineList[lineNum], int(shiftList[lineNum]))
                lineNum += 1
            # here we only check the consumer location which expected to be right after the model type line
            if consumerLocationPart1 != "" and consumerLocationPart2 != "":
                received_Line = self.whiteSpaceFilter(receivedLines[firstLine + 2])
                consumerLocationPart1 = self.whiteSpaceFilter(consumerLocationPart1)
                consumerLocationPart2 = self.whiteSpaceFilter(consumerLocationPart2)

                self.myLogger.debug('checking line (%s)+(%s) == (%s)' %(consumerLocationPart1, consumerLocationPart2, received_Line))
                if (consumerLocationPart1 in received_Line) and (consumerLocationPart2 in received_Line):
                    self.myLogger.info('Found consumer location: (%s)+(%s) == (%s)' %(consumerLocationPart1, consumerLocationPart2,received_Line))
                else:
                    self.fail('ERROR', 'consumerLocation not found (%s) or (%s) by cmw_model_status: (%s)' %(consumerLocationPart1, consumerLocationPart2,received_Line))
        else:
            self.fail('ERROR', 'model type (%s) not found by cmw_model_status' %modelType)
        return

    # this function will delete the tabs and spaces from the given string
    def whiteSpaceFilter(self, text):
        #self.myLogger.debug('whiteSpaceFilter  input: (%s)' %text)
        text = text.replace(' ','').replace('\t','')
        #self.myLogger.debug('whiteSpaceFilter output: (%s)' %text)
        return text

    def checkModelStatusOutput(self, receivedLines, firstLine, expectedOutput = "", lineShift = 0):
        self.myLogger.debug('checkModelStatusOutput enter')

        if expectedOutput != "" and lineShift != 0:
            receivedLine = self.whiteSpaceFilter(receivedLines[firstLine + lineShift])
            expectedOutput = self.whiteSpaceFilter(expectedOutput)
            self.myLogger.info('firstLine=(%s), lineShift=(%s), receivedLine=(%s)' %(firstLine,lineShift,receivedLine))
            self.myLogger.debug('checking line (%s) == (%s)' %(receivedLine,expectedOutput))

            if receivedLine == expectedOutput:
                self.myLogger.info('Found expected output (%s)' %expectedOutput)
            else:
                self.fail('ERROR', 'expected output not found: (%s)' %expectedOutput)

        self.myLogger.debug('checkModelStatusOutput leave')
        return


    def checkWhoDeliveredModel(self, expectedDelivered, comsaRevision):
        #expectedDelivered: CMW or COMSA
        self.logger.info('checkWhoDeliveredModel: Called')
        self.logger.info('checkWhoDeliveredModel: expectedDelivered = %s' %expectedDelivered)
        self.logger.info('checkWhoDeliveredModel: comsaRevision = %s' %comsaRevision)


        # CHECKING IF COMSA OR COM DELIVER COM IMM MODEL
        if self.testcase_tag == "TC-MR28452-001":
            command = 'cat /var/log/messages |grep "logToSys: called at %s" -A10000 | grep "comsa_pso ComImm() COM will deliver ImmCom model"' %self.clusterTime
        elif self.testcase_tag == "TC-MR28452-002":
            command = 'cat /var/log/messages |grep "logToSys: called at %s" -A10000 | grep "model_update ComImm() COMSA will deliver ImmCom model"' %self.clusterTime
        elif self.testcase_tag == "TC-MR28452-003":
            command = 'cat /var/log/messages |grep "logToSys: called at %s" -A10000 | grep "model_update ComImm() COM will deliver ImmCom model"' %self.clusterTime
        elif self.testcase_tag == "TC-MR28452-004":
            command = 'cat /var/log/messages |grep "logToSys: called at %s" -A10000 | grep "comsa_pso ComImm() COMSA will deliver ImmCom model"' %self.clusterTime
        elif self.testcase_tag == "TC-MR28452-005":
            command = 'cat /var/log/messages |grep "logToSys: called at %s" -A10000 | grep "model_update ComImm() COM will deliver ImmCom model"' %self.clusterTime

        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            result1 = self.sshLib.sendCommand(command,2,1)
            self.fail(result1[0], result1[1])

            result2 = self.sshLib.sendCommand(command,2,2)
            self.fail(result2[0], result2[1])
        elif noOfScs == 1:
            result1 = self.sshLib.sendCommand(command)
            self.fail(result1[0], result1[1])

            result2 = self.sshLib.sendCommand(command)
            self.fail(result2[0], result2[1])


        self.logger.info('Check who deliver IMM model: exit')

    def installCMW(self, setupFilesDir, pathToCmwInstallation):
        self.logger.info('installCMW: Called')
        self.logger.info('installCMW: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCMW: pathToCmwInstallation = %s' %pathToCmwInstallation)
        self.logger.info('installCMW: Copying of File(s) for CMW installation to the target.')

        # Check and wait until all tipc links are up
        self.logger.info('installCMW: Check and wait until all tipc links are up')
        for i in range(30):
            cmd = 'tipc-config -n'
            result = self.sshLib.sendCommand(cmd)
            self.myLogger.info('###tipc link status: %s' % result[1])
            if result[1].count('up') == len(self.testConfig['testNodesTypes']) - 1 :
                self.myLogger.info('All tipc links are UP!')
                break
            else:
                self.miscLib.waitTime(30)

        # Cleaning the directory
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToCmwInstallation)

        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('mkdir -p %s' %pathToCmwInstallation)
        self.fail(result[0], result[1])
        cmd = 'ls %s | grep -v depl.tar' %(setupFilesDir)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'Core MW tar file not found at specified location: %s/ .' %setupFilesDir)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one Core MW tar file found at specified location: %s/: %s.' %(setupFilesDir, str(result[1])))

        name_list = result[1].strip()
        fileName = name_list.split('/')[len(name_list.split('/')) - 1]

        result = self.sshLib.remoteCopy('%s/%s'%(setupFilesDir,name_list), pathToCmwInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])

        result = self.comsa_lib.installCoreMw(pathToCmwInstallation, fileName, backupRpms = self.backupRpmScript)
        return result

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
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comInstSdpName, 'com', backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')



    def upgradeCOM(self, setupFilesDir, pathToComInstallation):
        self.logger.info('UpgradeCOM: Called')
        self.logger.info('upgradeCOM: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('upgradeCOM: pathToComInstallation = %s' %pathToComInstallation)
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
            cmd = 'ls %s/ERIC-COM-BFU*.sdp' %(setupFilesDir)
        elif noOfScs == 1:
            cmd = 'ls %s/ERIC-COM-BFU*.sdp' %(setupFilesDir)
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
        comUpgdSdpName = name_list.split('/')[len(name_list.split('/')) - 1]


        #Install to system
        result = self.comsa_lib.installComp(self.pathToComInstallation, comRtSdpname, comUpgdSdpName, 'com', backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])
        self.logger.info('installCOM: Exit')


    def installCOMSA(self, setupFilesDir, pathToComsaInstallation, buildComsa):
        self.logger.info('installCOMSA: Called')
        self.logger.info('installCOMSA: setupFilesDir = %s' %setupFilesDir)
        self.logger.info('installCOMSA: pathToComsaInstallation = %s' %pathToComsaInstallation)

        if buildComsa == 'True':
            self.logger.info('installCOMSA: buildAndStoreCOMSA Called ')
            BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
            if BuildPath[0] != 'SUCCESS':
               self.logger.error(result[1])
               self.logger.debug('Build COMSA failed : Exit')
               return (BuildPath[0], 'Build COM SA failed')
            result = misc_lib.execCommand('\\rm -f  %s/*.sdp' %setupFilesDir)
            self.fail(result[0], result[1])
            # BuildPath[6] is the file name with absolute path of runtime sdp file
            # BuildPath[7] is the file name with absolute path of install sdp file
            self.myLogger.debug('Copying the *.sdp files to setupFilesDir')
            result = misc_lib.execCommand('\cp %s  %s/%s' %(BuildPath[6], setupFilesDir, self.cxpSdpName)) #change name incase COM_SA-CXP9017697_3.sdp
            self.fail(result[0], result[1])
            result = misc_lib.execCommand('\cp %s  %s/' %(BuildPath[7], setupFilesDir))
            self.fail(result[0], result[1])

       # Install time

        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        noOfScs = len(self.testConfig['controllers'])
        result = self.miscLib.execCommand("ls %s/%s | awk -F'/' '{print $NF}'" %(setupFilesDir, self.cxpSdpName))
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', result[1])
        self.cxpSdpName = result[1].rstrip()
        if noOfScs == 2:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' %(setupFilesDir, self.cxpSdpName), '%s/%s' %(setupFilesDir, self.installSdpName)], self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpName, 'comsa', backupRpms = self.backupRpmScript)
        elif noOfScs == 1:
            result = self.comsa_lib.copyFilesToTarget(['%s/%s' %(setupFilesDir, self.cxpSdpName),\
                                                  '%s/%s' %(setupFilesDir, self.installSdpNameSingle)],self.pathToComsaInstallation)
            self.fail(result[0], result[1])
            result = self.comsa_lib.installComp(pathToComsaInstallation, self.cxpSdpName, self.installSdpNameSingle, 'comsa', backupRpms = self.backupRpmScript)

        self.fail(result[0], result[1])
        self.logger.info('installCOMSA: Exit')

    def getAbsoluteFileNameClearCase(self, parternCommand, baseDir):
        self.logger.info('getAbsoluteFileNameClearCase: Called')
        self.logger.info('getAbsoluteFileNameClearCase: parternCommand = %s' %parternCommand)
        cmd = '%s' %(parternCommand)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'No such file or directory')
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one file found at specified location')
        name_list = result[1].strip()

        self.logger.info('getAbsoluteFileNameClearCase: Exit')
        return '%s' %( name_list)

    def getAbsoluteFileNameCluster(self, parternCommand, baseDir):
        self.logger.info('getAbsoluteFileNameCluster: Called')
        self.logger.info('getAbsoluteFileNameCluster: parternCommand = %s' %parternCommand)
        cmd = '%s' %(parternCommand)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'No such file or directory')
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one file found at specified location')
        name_list = result[1].strip()

        self.logger.info('getAbsoluteFileNameCluster: Exit')
        return '%s' %(name_list)

    def upgradeCOMSAFromStream(self, pathToComsaInstallation):
        self.logger.info('upgradeCOMSAFromStream: Called')

        result = self.sshLib.sendCommand('\\rm -rf %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('mkdir -p %s' %self.pathToComsaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        self.logger.info('installCOMSA: buildAndStoreCOMSA Called ')
        BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)
        if BuildPath[0] != 'SUCCESS':
            self.logger.error(result[1])
            self.logger.debug('Build COMSA failed : Exit')
            return (BuildPath[0], 'Build COM SA failed')

        #Copy to the target
        # BuildPath[6] is the file name with absolute path of Runtime sdp file
        # BuildPath[9] is the file name with absolute path of Template tar file
        self.myLogger.debug('Copying the COM SA tar files to the target')
        result = self.comsa_lib.copyFilesToTarget(['%s' %BuildPath[6], '%s' %BuildPath[9]], self.pathToComsaInstallation,False)
        self.fail(result[0],result[1])

        # Untar some files
        result = self.sshLib.sendCommand('tar xvf %s/%s -C %s' %(self.pathToComsaInstallation, BuildPath[4], self.pathToComsaInstallation)) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        # Import SDP package

        self.logger.info ('upgradeCOMSAFromStream: Importing ComSa SDP')

        cmd = '%s %s/%s' %(self.sdpImportCommand, self.pathToComsaInstallation, BuildPath[1])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        # determine suitable package for 1 or 2 controller node
        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            cmd1 = 'cd %s/COM_SA_U2_*/ ; ./comsa-generate-campaign-sdp' %(self.pathToComsaInstallation)
            cmd2 = 'cd %s/COM_SA_U2_*/ ; %s ./*.sdp' %(self.pathToComsaInstallation, self.sdpImportCommand)
        elif noOfScs == 1:
            cmd1 = 'cd %s/COM_SA_U3_*/ ; ./comsa-generate-single-campaign-sdp' %(self.pathToComsaInstallation)
            cmd2 = 'cd %s/COM_SA_U3_*/ ; %s ./*.sdp' %(self.pathToComsaInstallation, self.sdpImportCommand)
        else:
            self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' %str(noOfScs))

        result = self.sshLib.sendCommand(cmd1)
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand(cmd2)
        self.fail(result[0], result[1])

        # Start campaign
        self.logger.info ('upgradeCOMSAFromStream: Install campaign start')
        self.safLib.upgradeStart(self.campaignComsaUgradeName, '')
        self.fail(result[0], result[1])
        # Waiting until campaign complete
        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(self.campaignComsaUgradeName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COM')

        # Commiting the campaign
        self.logger.info ('upgradeCOMSAFromStream: commiting')

        result = self.safLib.upgradeCommit(self.campaignComsaUgradeName)
        self.fail(result[0], result[1])

        result = self.safLib.removeSwBundle(self.campaignComsaUgradeName)
        self.fail(result[0], result[1])

        result = self.safLib.checkClusterStatus()
        self.fail(result[0], result[1])

        self.logger.info('upgradeCOMSAFromStream: Exit')


    def createExpectedStatusOutput_lineTextR1_List1(self):
        self.myLogger.debug('createExpectedStatusOutput_lineTextR1_List() enter')
        lineList = []

        if self.expectedStatusOutput1R1_line1 != "":
            lineList.append(self.expectedStatusOutput1R1_line1)
        if self.expectedStatusOutput1R1_line2 != "":
            lineList.append(self.expectedStatusOutput1R1_line2)
        count = 0
        for line in lineList:
            count += 1
            self.myLogger.debug('Expected model status line[%s]= (%s)' %(str(count),line))
        self.myLogger.debug('createExpectedStatusOutput_lineText_List() leave')
        return lineList

    def createExpectedStatusOutput_lineTextR2_List1(self):
        self.myLogger.debug('createExpectedStatusOutput_lineTextR2_List() enter')
        lineList = []

        if self.expectedStatusOutput1R2_line1 != "":
            lineList.append(self.expectedStatusOutput1R2_line1)
        if self.expectedStatusOutput1R2_line2 != "":
            lineList.append(self.expectedStatusOutput1R2_line2)
        count = 0
        for line in lineList:
            count += 1
            self.myLogger.debug('Expected model status line[%s]= (%s)' %(str(count),line))
        self.myLogger.debug('createExpectedStatusOutput_lineText_List() leave')
        return lineList


    def createExpectedStatusOutput_lineShift_List1(self):
        self.myLogger.debug('createExpectedStatusOutput_lineShift_List1() enter')
        shiftList = []

        if self.expectedStatusOutput1_shift1 != "":
            shiftList.append(self.expectedStatusOutput1_shift1)
        if self.expectedStatusOutput1_shift2 != "":
            shiftList.append(self.expectedStatusOutput1_shift2)

        count = 0
        for line in shiftList:
            count += 1
            self.myLogger.debug('Expected model status line shift[%s]= (%s)' %(str(count),line))
        self.myLogger.debug('createExpectedStatusOutput_lineShift_List1() leave')
        return shiftList


    def updateLocalSshKeys(self, sshKeyUpdater):
        self.logger.debug('enter updateLocalSshKeys')
        for controller in self.testConfig['controllers']:
            ipAddress = self.targetData['ipAddress']['ctrl']['ctrl%s'%str(self.testConfig['controllers'][self.testConfig['controllers'].index(controller)][1])]
            cmd = '%s %s' %(sshKeyUpdater, ipAddress)
            result = self.miscLib.execCommand(cmd)
        self.logger.debug('leave updateLocalSshKeys')



    def tearDown(self):
        self.setTestStep('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)
        if self.skip_test == False:
            command = '\\rm -rf /home/tmpdirMR28452/'
            self.sshLib.sendCommand(command)
            self.sshLib.tearDownHandles()

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

    ########################################################################################
    def mr28452SetupStress(self):
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
        #result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

        # No CPU, only local and NFS disk
        #result = self.comsa_lib.startStressToolOnTarget(self, 0, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

        # 50% CPU, 50% memory plus local and NFS disk stress
        result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 0, 0)

        # 50% CPU, 50% memory plus NFS disk stress
        #result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
