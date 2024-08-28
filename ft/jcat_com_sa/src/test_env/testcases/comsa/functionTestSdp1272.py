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
import re
import time
import os
from org.apache.log4j import Logger
from java.lang import System


logger = None

class FTSdp1272(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.test_config= testConfig
        self.testcase_tag = tag

        self.expectedModelFile1 = ""
        self.expectedModelFile2 = ""
        self.expectedModelFile3 = ""
        self.expectedModelFile4 = ""
        self.expectedModelFile5 = ""
        self.expectedModelFile6 = ""
        self.expectedModelFile7 = ""
        self.expectedModelFile8 = ""
        self.expectedModelFile9 = ""
        self.expectedModelFile10 = ""

        self.expectedStatusOutput_line1 = ""
        self.expectedStatusOutput_line2 = ""
        self.expectedStatusOutput_line3 = ""
        self.expectedStatusOutput_line4 = ""
        self.expectedStatusOutput_line5 = ""

        self.expectedStatusOutput2_line1 = "Consumer Location: <Empty> on node <Empty>"
        self.expectedStatusOutput2_line2 = "SDP: ERIC-CONFIGPKG-CXP9013822_3-R1B01"
        self.expectedStatusOutput2_line3 = "Action: add"
        self.expectedStatusOutput2_line4 = "State: Waiting for consumer"
        self.expectedStatusOutput2_line5 = ""

        self.expectedStatusOutput_shift1 = 0
        self.expectedStatusOutput_shift2 = 0
        self.expectedStatusOutput_shift3 = 0
        self.expectedStatusOutput_shift4 = 0
        self.expectedStatusOutput_shift5 = 0

        self.modelCommentText = ""
        self.modelCommentTextIsInPlace = ""
        self.modelFile_to_check_Comment = ""

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        path_1 = dict.get("COM_MODEL_FILE_LIST")
        path_2 = dict.get("COM_MODEL_FILE_CFG")
        self.COM_model_file_list = path_1 + path_2
        self.comsaRepository = dict.get("COMSA_REPOSITORY")
        self.comsaConfig = dict.get("COMSA_CONFIG")
        self.testAppPath = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("TEST_APPLICATION_PATH"))
        self.comsaSrcDir = '%s%s' %(self.COMSA_REPO_PATH, dict.get ("SRC"))
        self.localPathToSwComSaDir = dict.get("JENKINUSER_R_INSTALL")
        self.buildDir = dict.get('BUILD_TOKENS')
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        global logger
        #self.logger = Logger.getLogger('comsa_lib')
        logger = Logger.getLogger('comsa_lib')
        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        self.tempDir = "/home/FT1272/"
        comsaCampaignName = "ERIC-ComSaInstall"
        self.swDir = System.getProperty("swDirNumber")
        self.localPathToSwComSa = '%s%s/comsa/' %(self.localPathToSwComSaDir, self.swDir)


        modelType = "COM_R1"
        testApp1 = "CONFIGPKG_COM_R1-CXP9013822_3.sdp"
        testApp1_sdpName = "ERIC-CONFIGPKG-CXP9013822_3-R1B01"

        testApp2 = "CONFIGPKG_COM_R1_M-CXP9013822_3.sdp"
        testApp2_sdpName = "ERIC-CONFIGPKG-CXP9013822_3-R1B02"

        testApp3 = "JAVACAF_x86_64-CXP9013050_4.sdp"
        testApp3_sdpName = "ERIC-JAVACAF_x86_64-CXP9013050_4-R1A03"

        testApp4 = "JAVACAF_M_x86_64-CXP9013050_4.sdp"
        testApp4_sdpName = "ERIC-JAVACAF_x86_64-CXP9013050_4-R1A04"

        testApp5 = "JAVACAF_x86_64-CXP9013050_5.sdp"
        testApp5_sdpName = "ERIC-JAVACAF_x86_64-CXP9013050_5-R1A03"

        self.expectedModelTypeText = "Model Type: '%s'" %modelType
        consumerLocation_part1 = "Consumer Location:      %scomsa_mdf_consumeronnodeSC-" %self.comsaConfig
        consumerLocation_part2 = "/comsa_mdf_consumer on node SC-"

        expectedModelFileList = self.createExpectedModelFileList()
        expectedComModelList = self.createExpectedComModelList(self.comsaRepository)
        expectedModelStatusOutput_lineText_list = self.createExpectedStatusOutput_lineText_List()
        expectedModelStatusOutput_lineText_list2 = self.createExpectedStatusOutput_lineText_List2()
        expectedModelStatusOutput_lineShift_list = self.createExpectedStatusOutput_lineShift_List()

####################################################################################################################
##########################     Test cases: from TC-FT1272-001 to TC-FT1272-005    ##################################
####################################################################################################################

        # Setup TC
        if self.testcase_tag == 'TC-FT1272-001':
            self.restoreBackupCOM()
            self.createTempDir()
            self.copyTestApp(self.testAppPath + testApp1)
            self.copyTestApp(self.testAppPath + testApp2)
            self.copyTestApp(self.testAppPath + testApp3)
            self.copyTestApp(self.testAppPath + testApp4)
            self.copyTestApp(self.testAppPath + testApp5)

####################################################################################################################

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

####################################################################################################################

        if self.testcase_tag == 'TC-FT1272-002':
            self.installCOMSA(comsaCampaignName)
            self.cmw_model_status(modelType, [], [], consumerLocation_part1, consumerLocation_part2)

            self.cmw_sdp_import(testApp1, testApp1_sdpName)
            self.checkComModelFileList(expectedComModelList,False)

            add_cmd = self.cmw_model_add(testApp1_sdpName,modelType)
            self.cmw_model_done(add_cmd)
#            self.cmw_model_status(modelType, expectedModelStatusOutput_lineText_list, expectedModelStatusOutput_lineShift_list)

            self.checkComSaRepository(expectedModelFileList)
            self.checkComModelFileList(expectedComModelList)

####################################################################################################################

        if self.testcase_tag == 'TC-FT1272-003':
            self.cmw_sdp_import(testApp2, testApp2_sdpName)

            modify_cmd = self.cmw_model_modify(testApp2_sdpName,modelType)
            self.cmw_model_done(modify_cmd)
            self.cmw_model_status(modelType, [], [], consumerLocation_part1, consumerLocation_part2)

            self.checkComSaRepository(expectedModelFileList)
            self.checkComModelFileList(expectedComModelList)

####################################################################################################################

        if self.testcase_tag == 'TC-FT1272-004':
            delete_cmd = self.cmw_model_delete(testApp2_sdpName,modelType)
            self.cmw_model_done(delete_cmd)
            self.cmw_model_status(modelType, [], [], consumerLocation_part1, consumerLocation_part2)

            self.checkComSaRepository(expectedModelFileList,False)
            self.checkComModelFileList(expectedComModelList,False)

####################################################################################################################

        if self.testcase_tag == 'TC-FT1272-005':
            self.cmw_sdp_import(testApp3, testApp3_sdpName)
            self.cmw_sdp_import(testApp4, testApp4_sdpName)
            self.cmw_sdp_import(testApp5, testApp5_sdpName)
            # prepare for the one-step test (add-modify-delete)
            add_cmd = self.cmw_model_add(testApp1_sdpName,modelType)
            add_cmd2 = self.cmw_model_add(testApp3_sdpName,modelType)
            self.cmw_model_done(add_cmd + add_cmd2)
            # Add-modify-delete in one step here:
            add_cmd = self.cmw_model_add(testApp5_sdpName,modelType)
            modify_cmd = self.cmw_model_modify(testApp4_sdpName,modelType)
            delete_cmd = self.cmw_model_delete(testApp1_sdpName,modelType)
            self.cmw_model_done(add_cmd + modify_cmd + delete_cmd)
            #self.cmw_model_status(modelType, expectedModelStatusOutput_lineText_list, expectedModelStatusOutput_lineShift_list)

            self.checkComSaRepository(expectedModelFileList)
            self.checkComModelFileList(expectedComModelList)

####################################################################################################################

        if self.testcase_tag == 'TC-FT1272-006':
            delete_cmd = self.cmw_model_delete(testApp1_sdpName,modelType)
            self.cmw_model_done(delete_cmd)
            self.cmw_model_status(modelType, [], [], consumerLocation_part1, consumerLocation_part2)
            self.checkComSaRepository(expectedModelFileList,False)
            self.checkComModelFileList(expectedComModelList,False)

####################################################################################################################

        if self.testcase_tag == 'TC-FT1272-007':
            modify_cmd = self.cmw_model_modify(testApp1_sdpName,modelType)
            self.cmw_model_done(modify_cmd)
            self.cmw_model_status(modelType, [], [], consumerLocation_part1, consumerLocation_part2)

            self.checkComSaRepository(expectedModelFileList)
            self.checkComModelFileList(expectedComModelList)

            delete_cmd = self.cmw_model_delete(testApp1_sdpName,modelType)
            self.cmw_model_done(delete_cmd)
            self.cmw_model_status(modelType, [], [], consumerLocation_part1, consumerLocation_part2)

####################################################################################################################

        # Cleanup TC
        if self.testcase_tag == 'TC-FT1272-010':
            d1 = self.cmw_model_delete(testApp1_sdpName,modelType)
            d2 = self.cmw_model_delete(testApp2_sdpName,modelType)
            d3 = self.cmw_model_delete(testApp3_sdpName,modelType)
            d4 = self.cmw_model_delete(testApp4_sdpName,modelType)
            d5 = self.cmw_model_delete(testApp5_sdpName,modelType)
            self.cmw_model_done(d1 + d2 + d3 + d4 + d5)

            self.checkComSaRepository(expectedModelFileList,False)
            self.checkComModelFileList(expectedComModelList,False)

            self.cmw_sdp_remove(testApp1_sdpName)
            self.cmw_sdp_remove(testApp2_sdpName)
            self.cmw_sdp_remove(testApp3_sdpName)
            self.cmw_sdp_remove(testApp4_sdpName)
            self.cmw_sdp_remove(testApp5_sdpName)
            self.removeTempDir()

####################################################################################################################

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")

    def tearDown(self):
        self.setTestStep('tearDown')
        '''
        Here we don't do anything.
        We do the cleaning in cleanup-testcase.
        The reason is, we don't want to remove test models:
            -we need to check the test cases by sequence
            -this solution results faster TS run(e.g. don't need to import and remove models tc-by-tc)
        '''
        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

    def cmw_model_add(self, bundleName, modelType):
        self.setTestStep('cmw_model_add')
        cmd = 'cmw-model-add %s --mt %s;' %(bundleName,modelType)
        '''
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        if result[1] != "":
            self.fail('ERROR', 'cmw_model_add (%s) returned: (%s)' %(bundleName,result[1]))
        return'''
        return cmd

    def cmw_model_modify(self, bundleName, modelType):
        self.setTestStep('cmw_model_modify')
        cmd = 'cmw-model-modify %s --mt %s;' %(bundleName,modelType)
        '''
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        if result[1] != "":
            self.fail('ERROR', 'cmw_model_modify (%s) returned: (%s)' %(bundleName,result[1]))
        return
        '''
        return cmd

    def cmw_model_delete(self, bundleName, modelType):
        self.setTestStep('cmw_model_delete')
        cmd = 'cmw-model-delete %s --mt %s;' %(bundleName,modelType)
        '''
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        if result[1] != "":
            self.fail('ERROR', 'cmw_model_delete (%s) returned: (%s)' %(bundleName,result[1]))
        return
        '''
        return cmd

    def cmw_model_done(self,command = ""):
        self.setTestStep('cmw_model_done')
        self.myLogger.debug('save default ssh timeout')
        default_timeout = self.sshLib.getTimeout()
        if self.installStressTool:
            modelDoneTimeout = 200
        else:
            modelDoneTimeout = 60
        self.myLogger.debug('Setting the ssh timeout to %s sec' %modelDoneTimeout)
        self.sshLib.setTimeout(modelDoneTimeout)
        done_cmd = 'cmw-model-done'
        result = self.sshLib.sendCommand(command + done_cmd)
        self.myLogger.debug('restore default ssh timeout')
        self.sshLib.setTimeout(default_timeout)
        self.fail(result[0], result[1])
        if result[1] != "":
            self.fail('ERROR', 'cmw_model_done returned: (%s)' %result[1])
        self.miscLib.waitTime(15)
        switchover_cmd = 'comsa-mim-tool com_switchover'
        result = self.sshLib.sendCommand(switchover_cmd)
        self.fail(result[0], result[1])
        return

    def cmw_model_status(self, modelType, lineList = [], shiftList = [], consumerLocationPart1 = "", consumerLocationPart2 = ""):
        self.setTestStep('cmw_model_status')
        cmd = 'cmw-model-status'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        receivedLines = result[1].splitlines()

        num = 0
        # the line number of the first interesting line (which is the model type)
        firstLine = -1
        self.expectedModelTypeText = self.whiteSpaceFilter(self.expectedModelTypeText)
        self.myLogger.debug('self.expectedModelTypeText: (%s) length: (%s)' %(self.expectedModelTypeText,str(len(self.expectedModelTypeText))))

        # line-by-line check which line is the first one (model type)
        for line in receivedLines:
            line = self.whiteSpaceFilter(line)
            self.myLogger.debug('checking line[%s]: (%s) length: (%s)' %(str(num), line, str(len(line))))
            if line == self.expectedModelTypeText:
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
                received_Line = self.whiteSpaceFilter(receivedLines[firstLine + 1])
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
            self.myLogger.debug('checking line (%s) == (%s)' %(receivedLine,expectedOutput))

            if receivedLine == expectedOutput:
                self.myLogger.info('Found expected output (%s)' %expectedOutput)
            else:
                self.fail('ERROR', 'expected output not found: (%s)' %expectedOutput)

        self.myLogger.debug('checkModelStatusOutput leave')
        return

    def cmw_sdp_import(self, testAppName, sdpName):
        # testAppName e.g. "CONFIGPKG_COM_R1-CXP9013822_3.sdp"
        # sdpName e.g. "testAppName"
        self.setTestStep('cmw_sdp_import')
        self.myLogger.debug('cmw_sdp_import: importing (%s%s)' %(self.tempDir,testAppName))
        cmd = 'cmw-sdp-import %s%s' %(self.tempDir,testAppName)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        expectedOutput = "%s imported (type=Bundle)" %sdpName
        self.myLogger.debug('received text (%s)' %result[1])
        self.myLogger.debug('expected text (%s)' %expectedOutput)
        if result[1] != expectedOutput:
            self.fail('ERROR', 'SDP bundle (%s) not imported: %s' %(sdpName,result[1]))
        else:
            self.myLogger.info('text matching')
        return

    def cmw_sdp_remove(self,sdpName, checkNeeded = True):
        self.setTestStep('cmw_sdp_remove')
        self.myLogger.debug('cmw_sdp_remove: removing SDP (%s)' %sdpName)
        cmd = 'cmw-sdp-remove %s' %sdpName
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        if checkNeeded:
            expectedOutput = "Bundle SDP removed [%s]" %sdpName
            self.myLogger.debug('received text (%s)' %result[1])
            self.myLogger.debug('expected text (%s)' %expectedOutput)
            if result[1] != expectedOutput:
                self.fail('ERROR', 'SDP bundle (%s) not removed: %s' %(sdpName,result[1]))
            else:
                self.myLogger.info('text matching')
        return

    # mustContain = True  means that we expect the files are in COMSA repository
    # mustContain = False means that we expect the files are NOT in COMSA repository
    def checkComSaRepository(self, list, mustContain = True):
        self.setTestStep('Check COM SA repository')
        for expectedModelFile in list:
            self.myLogger.debug('checkComSaRepository: checking (%s) in COM SA repository' %expectedModelFile)
            self.checkComSaRepository_onePattern(expectedModelFile, mustContain)
        return

    # mustContain = True  means that we expect the files are in COMSA repository
    # mustContain = False means that we expect the files are NOT in COMSA repository
    def checkComSaRepository_onePattern(self, pattern, mustContain = True):
        cmd = 'ls -1 %s' %self.comsaRepository
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        # receivedLines is a list that contains the filenames which are under COMSA repository
        receivedLines = result[1].splitlines()
        matchCount = 0
        # check each filename and count the matches
        for line in receivedLines:
            self.myLogger.debug('checking line: (%s)' %line)
            if pattern == line:
                matchCount += 1
                self.myLogger.debug('found')

                # either we check all or we check only the given model files!
                # that means:
                #             1. if model file not specified, then check all model files
                #             2. if model file specified, then check only that model file
                if mustContain and (self.modelFile_to_check_Comment == "" or self.modelFile_to_check_Comment == line):
                    # checking the model comment which identifies model files
                    commentCount = -1
                    if self.modelCommentTextIsInPlace == "NO":
                        commentCount = 0
                    elif self.modelCommentTextIsInPlace == "YES":
                        commentCount = 1
                    cmd = 'grep -c "%s" %s%s' %(self.modelCommentText, self.comsaRepository, line)
                    self.myLogger.debug('checking the model comment which identifies model files: (%s)' %cmd)
                    result = self.sshLib.sendCommand(cmd)

                    if result[1] == str(commentCount):
                        self.myLogger.info('Found the expected number (%s) of comments in model file' %result[1])
                    else:
                        self.fail('ERROR', 'Comment not found in model file')

        if mustContain:
            if matchCount == 1:
                self.myLogger.info('Found (%s) in COM SA repository' %pattern)
            elif matchCount == 0:
                self.fail('ERROR', '(%s) not found in COM SA repository' %pattern)
            else:
                self.fail('ERROR', 'Found (%s) more than one times in COM SA repository: found %s times' %(pattern,str(matchCount)))
        else:
            if matchCount == 0:
                self.myLogger.info('Not found (%s) in COM SA repository as expected' %pattern)
            elif matchCount == 1:
                self.fail('ERROR', 'Not expected (%s) found in COM SA repository' %pattern)
            else:
                self.fail('ERROR', 'Not expected (%s) found more than one times in COM SA repository: found %s times' %(pattern,str(matchCount)))

        return

    def checkComModelFileList(self, list, mustContain = True):
        self.setTestStep('Check COM model file list')
        for expectedComModel in list:
            self.myLogger.debug('checkComModelFileList: checking COM model: (%s)' %expectedComModel)
            self.checkComModelFileList_onePattern(expectedComModel, mustContain)
        return

    def checkComModelFileList_onePattern(self, pattern, mustContain = True):
        cmd = 'cat %s' %self.COM_model_file_list
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        receivedLines = result[1].splitlines()
        matchCount = 0
        for line in receivedLines:
            self.myLogger.debug('checking line: (%s)' %line)
            if pattern == line:
                matchCount += 1
                self.myLogger.debug('found')
        if mustContain:
            if matchCount == 1:
                self.myLogger.info('Found (%s) in model file list' %pattern)
            elif matchCount == 0:
                self.fail('ERROR', '(%s) not found in model file list' %pattern)
            else:
                self.fail('ERROR', 'Found (%s) more than one times in model file list: found %s times' %(pattern,str(matchCount)))
        else:
            if matchCount == 0:
                self.myLogger.info('Not found (%s) in model file list as expected' %pattern)
            elif matchCount == 1:
                self.fail('ERROR', 'Not expected (%s) found in model file list' %pattern)
            else:
                self.fail('ERROR', 'Not expected (%s) found more than one times in model file list: found %s times' %(pattern,str(matchCount)))

        return

    def createTempDir(self):
        #Create temporary directory on target
        self.setTestStep('Create temporary directory on target')
        cmd = 'mkdir %s' %self.tempDir
        self.myLogger.debug('Create temporary directory on target: %s' %cmd)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0],result[1])
        return

    def copyTestApp(self,testAppPath):
        self.setTestStep('Copy test app to target')
        result = self.sshLib.remoteCopy(testAppPath, self.tempDir, timeout = 60)
        self.fail(result[0],result[1])
        return

    def removeTempDir(self):
        #Remove temporary directory from target
        cmd = '\\rm -rf %s' %self.tempDir
        self.myLogger.debug('Remove temporary directory from target: %s' %cmd)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0],result[1])
        return

    def createExpectedModelFileList(self):
        self.myLogger.debug('createExpectedModelFileList() enter')
        modelList = []

        if self.expectedModelFile1 != "":
            modelList.append(self.expectedModelFile1)
        if self.expectedModelFile2 != "":
            modelList.append(self.expectedModelFile2)
        if self.expectedModelFile3 != "":
            modelList.append(self.expectedModelFile3)
        if self.expectedModelFile4 != "":
            modelList.append(self.expectedModelFile4)
        if self.expectedModelFile5 != "":
            modelList.append(self.expectedModelFile5)
        if self.expectedModelFile6 != "":
            modelList.append(self.expectedModelFile6)
        if self.expectedModelFile7 != "":
            modelList.append(self.expectedModelFile7)
        if self.expectedModelFile8 != "":
            modelList.append(self.expectedModelFile8)
        if self.expectedModelFile9 != "":
            modelList.append(self.expectedModelFile9)
        if self.expectedModelFile10 != "":
            modelList.append(self.expectedModelFile10)
        count = 0
        for model in modelList:
            count += 1
            self.myLogger.debug('Expected modelFileList[%s]= (%s)' %(str(count),model))
        self.myLogger.debug('createExpectedModelFileList() leave')
        return modelList

    def createExpectedComModelList(self, comsaRepository):
        self.myLogger.debug('createExpectedComModelList() enter')
        modelList = []

        if self.expectedModelFile1 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile1))
        if self.expectedModelFile2 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile2))
        if self.expectedModelFile3 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile3))
        if self.expectedModelFile4 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile4))
        if self.expectedModelFile5 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile5))
        if self.expectedModelFile6 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile6))
        if self.expectedModelFile7 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile7))
        if self.expectedModelFile8 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile8))
        if self.expectedModelFile9 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile9))
        if self.expectedModelFile10 != "":
            modelList.append('%s%s'%(comsaRepository, self.expectedModelFile10))
        count = 0
        for model in modelList:
            count += 1
            self.myLogger.debug('Expected COM modelList[%s]= (%s)' %(str(count),model))
        self.myLogger.debug('createExpectedComModelList() leave')
        return modelList

    def createExpectedStatusOutput_lineText_List(self):
        self.myLogger.debug('createExpectedStatusOutput_lineText_List() enter')
        lineList = []

        if self.expectedStatusOutput_line1 != "":
            if self.expectedStatusOutput_line1 == "Consumer Location: Empty on node Empty":
                lineList.append("Consumer Location: <Empty> on node <Empty>")
            else:
                lineList.append(self.expectedStatusOutput_line1)
        if self.expectedStatusOutput_line2 != "":
            lineList.append(self.expectedStatusOutput_line2)
        if self.expectedStatusOutput_line3 != "":
            lineList.append(self.expectedStatusOutput_line3)
        if self.expectedStatusOutput_line4 != "":
            lineList.append(self.expectedStatusOutput_line4)
        if self.expectedStatusOutput_line5 != "":
            lineList.append(self.expectedStatusOutput_line5)

        count = 0
        for line in lineList:
            count += 1
            self.myLogger.debug('Expected model status line[%s]= (%s)' %(str(count),line))
        self.myLogger.debug('createExpectedStatusOutput_lineText_List() leave')
        return lineList

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
        if self.expectedStatusOutput2_line5 != "":
            lineList.append(self.expectedStatusOutput2_line5)

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
        if self.expectedStatusOutput_shift5 != "":
            shiftList.append(self.expectedStatusOutput_shift5)

        count = 0
        for line in shiftList:
            count += 1
            self.myLogger.debug('Expected model status line shift[%s]= (%s)' %(str(count),line))
        self.myLogger.debug('createExpectedStatusOutput_lineShift_List() leave')
        return shiftList

    def installCOMSA(self,campaignName):
        comsaSdpList = self.makeComsa_and_copyToTarget()
        self.cmw_sdp_import_COMSA(comsaSdpList)
        self.start_COMSA_installCampaign(campaignName)
        self.cmw_sdp_remove_COMSA_campaign(campaignName)
        return

    def start_COMSA_installCampaign(self,campaignName):
        # campaign start
        self.setTestStep('start COM SA install-campaign')
        self.myLogger.debug('Install campaign: %s' %campaignName)
        result = self.safLib.upgradeStart(campaignName)
        self.fail(result[0], result[1])
        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(campaignName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            elif 'failed' in result[1]:
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COMSA')

        # Check CMW status, and wait for status ok
        self.setTestStep('Check CMW status, and wait for status ok')
        self.check_CMW_status('Failed to install COMSA')

        # Commit COMSA installation campaign
        self.setTestStep('Commit COMSA installation campaign')
        self.myLogger.debug('Commit campaign: %s' %campaignName)
        result = self.safLib.upgradeCommit(campaignName)
        if result[0] == 'ERROR':
            self.fail('ERROR','failed to commit')

        # Check CMW status, and wait for status ok
        self.setTestStep('Check CMW status after committing COMSA install')
        self.check_CMW_status('Failed to commit COMSA installation')
        return

    def check_CMW_status(self, errorText):
        okFlag = False
        for i in range(30):
           result = self.safLib.checkClusterStatus('off', 'su node comp')
           self.myLogger.info(result[1])
           if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
           else:
                if re.search('cmw-status: command not found', result[1]):
                        self.sshLib.tearDownHandles()
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR',errorText)
        return

    def restoreBackupCOM(self):
        self.setTestStep('Restore partial backup of COM')
        cmd = """cmw-partial-backup-list 2>&1 | sed 's/\[//g' | sed 's/\]//g' | grep -i com | egrep -iv '(comsa)|(com_sa)|(com-sa)' | tail -1 | awk '{print $NF}' """
        # We search for the latest COM backup
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        backupName = result[1]

        if backupName == '':
            if self.linuxDistro != self.distroTypes[1]:
                self.fail('ERROR', 'COM backup not found!')
            elif self.linuxDistro == self.distroTypes[1]:
                # For RHEL systems we try to reinstall COM instead of restoring a COM backup
                backupName == 'com_autobackup'

        result = self.comsa_lib.restoreSystem(self, backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = 2, removeBackup = False)
        self.fail(result[0], result[1])


    def makeComsa_and_copyToTarget(self):
        self.setTestStep('Make COM SA and copy to target')

        # it is better to remove manually, not just do "make clean" - sometimes the SDP names change and not cleaning the old one
        buildFlag = False
        swChangeFlag = False

        if self.swDir == 'undef':
            buildFlag = True
        else:
            cmd = 'ls %s' %self.localPathToSwComSa
            result = self.miscLib.execCommand(cmd)
            if 'No such file or directory' in result[1]:
                buildFlag = True
            else:
                swChangeFlag = True
                origComsaReleaseDir = self.buildRelease
                self.buildRelease = self.localPathToSwComSa


        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        if buildFlag == True:

            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0],result[1])

            self.myLogger.debug('clean release dir')
            cmd = '\\rm -f %s*.sdp' %self.buildRelease
            result = self.miscLib.execCommand(cmd)
            swChangeFlag = False
            self.swDir = System.getProperty("swDirNumber")

            self.myLogger.debug('make clean COM SA')
            cmd = 'cd %s ; make clean' %self.comsaSrcDir
            self.myLogger.debug('cmd: (%s)' %cmd)
            result = self.miscLib.execCommand(cmd)
            self.fail(result[0], result[1])

            self.myLogger.debug('make COM SA')
            cmd = 'cd %s ; make' %self.comsaSrcDir
            self.myLogger.debug('cmd: (%s)' %cmd)
            result = self.miscLib.execCommand(cmd)

        self.myLogger.debug('read SDP file names')
        cmd = 'cd %s; ls *.sdp | grep -i cxp' %self.buildRelease
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if len(result[1].splitlines()) != 1:
            self.fail('ERROR', 'Expected exactly one match while searching for the COM SA CXP package. Received: %s' %result[1])
        sdp1 = result[1].splitlines()[0]

        noOfScs = len(self.testConfig['controllers'])
        if noOfScs == 2:
            installSdp = '*install.sdp'
        elif noOfScs == 1:
            installSdp = '*install_Single.sdp'
        else:
            self.fail('ERROR', 'Currently supported configurations are with one or two system controllers. System controllers defined: %s' %str(noOfScs))

        cmd = 'cd %s; ls %s' %(self.buildRelease, installSdp)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if len(result[1].splitlines()) != 1:
            self.fail('ERROR', 'Expected exactly one match while searching for the COM SA CXP package. Received: %s' %result[1])
        sdp2 = result[1].splitlines()[0]

        self.myLogger.debug('sdp1: (%s)' %sdp1)
        self.myLogger.debug('sdp2: (%s)' %sdp2)

        self.myLogger.debug('copy COM SA SDPs to target')
        result = self.sshLib.remoteCopy('%s%s' %(self.buildRelease,sdp1), self.tempDir, timeout = 60)
        self.fail(result[0],result[1])
        result = self.sshLib.remoteCopy('%s%s' %(self.buildRelease,sdp2), self.tempDir, timeout = 60)
        self.fail(result[0],result[1])

        if buildFlag == True:
            # Release the build token
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            self.fail(result[0],result[1])

        if swChangeFlag == True:
            self.buildRelease = origComsaReleaseDir

        return [sdp1,sdp2]

    def cmw_sdp_import_COMSA(self, sdpList):
        self.setTestStep('cmw_sdp_import_COMSA')
        self.myLogger.debug('cmw_sdp_import_COMSA: importing (%s) and (%s)' %(sdpList[0],sdpList[1]))
        # After campaign import (ComSa_install.sdp)
        expectedText1 = "ERIC-ComSaInstall imported (type=Campaign)"
        # after CXP import (ComSa-CXP9017697_3.sdp)
        expectedText2 = "ERIC-ComSa-CXP9017697_3-P2A61 imported (type=Bundle)"

        cmd = 'cmw-sdp-import %s%s' %(self.tempDir,sdpList[0])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        cmd = 'cmw-sdp-import %s%s' %(self.tempDir,sdpList[1])
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        return

    def cmw_sdp_remove_COMSA_campaign(self, campaignName):
        self.setTestStep('Remove COM SA campaign')
        self.myLogger.debug('cmw_sdp_remove_COMSA_campaign: removing COM SA campaign: (%s)' %campaignName)

        cmd = 'cmw-sdp-remove %s' %campaignName
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        return

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
