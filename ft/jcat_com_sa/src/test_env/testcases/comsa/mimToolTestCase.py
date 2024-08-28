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
    TC-MIM-001 Add Model Files with Rollback
    TC-MIM-002 Add Model FIles with Commit
    TC-MIM-003 Remove Model Files with Rollback
    TC-MIM-004 Remove Model Files with Commit


    ==================================
    Help:
    If you would like to test a new SDP either create new config xml files based on tc_MIM_00[1-4]_*.xml (more complicated)
    or change the self.sdpPathLocalMachine and self.MimSdpName variables in __init__ below (easier) so that they point to
    your new SDP file. In the first case you need to add the new test cases to the mimToolTestSuite.xml test suite file.
    In the second case you can run the current test cases (with unchanged test suite file) against the new test SDP.

    To run the MIM tool test suite run the command below:
    executive.py --config cots_target_??? --pl ? --suite mimToolTestSuite.xml --productSettings comsa

    To run a stand-alone MIM tool test case run the command:
    executive.py --config cots_target_??? --pl ? --productSettings comsa --runSingleTestCase TC-MIM-001

    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
import os

class MimTool(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.MimSdpName = 'CONFIGPKG-CXP9013822_3.sdp'
        self.targetIncomingLocation = '/home/coremw/incoming/MIM_tool_test/'
        self.defaultCoreMwSdpImportDir = '/home/coremw/incoming/'
        self.mimToolCommand = 'comsa-mim-tool'
        self.mimToolParams1 = {}
        self.expectedResponses1 = {}
        self.diffResult1 = {}
        self.appendSdpBundleName1 = {}
        self.appendExtraArgs1 = {}
        self.extraArgs1 = {}

        self.mimToolParams2 = {}
        self.expectedResponses2 = {}
        self.diffResult2 = {}
        self.appendSdpBundleName2 = {}
        self.appendExtraArgs2 = {}
        self.extraArgs2 = {}

        self.mimToolParams3 = {}
        self.expectedResponses3 = {}
        self.diffResult3 = {}
        self.appendSdpBundleName3 = {}
        self.appendExtraArgs3 = {}
        self.extraArgs3 = {}

        self.mimToolParams4 = {}
        self.expectedResponses4 = {}
        self.diffResult4 = {}
        self.appendSdpBundleName4 = {}
        self.appendExtraArgs4 = {}
        self.extraArgs4 = {}

        self.mimToolParams5 = {}
        self.expectedResponses5 = {}
        self.diffResult5 = {}
        self.appendSdpBundleName5 = {}
        self.appendExtraArgs5 = {}
        self.extraArgs5 = {}

        self.expectedComSA_debug = {}

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.sdpPathLocalMachine = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("EXAMPLE_MODELFILE_PATH"))
        self.PERSISTENT_STORAGE_API = dict.get("PERSISTENT_STORAGE_API")
        self.serviceInstanceName = dict.get('SERVICE_INSTANCE_NAME')
        self.amfNodePattern = dict.get('AMF_NODE_PATTERN')

        coreTestCase.CoreTestCase.setUp(self)

        #print '####### EJNOLSZ: appextra2: ', self.appendExtraArgs2, ', extraArg2: ', self.extraArgs2
        #print '####### EJNOLSZ: appextra4: ', self.appendExtraArgs4, ', extraArg4: ', self.extraArgs4


        if self.tag == 'TC-MIM-005':
            print 'COM SA MIM Tool Switchover'
            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            self.activeController = result[1]
        else:
            PERSISTENT_STORAGE_API_CONFIG="%s/config" %self.PERSISTENT_STORAGE_API
            cmd = "cat %s" %PERSISTENT_STORAGE_API_CONFIG
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            if 'No such file or directory' in result[1]:
                self.comSaRepository = '/home/comsa/repository/'
                self.modelFileList = '/cluster/home/com/etc/model/model_file_list.cfg'
                self.origModelFileList = '/cluster/home/com/etc/model/model_file_list.cfg.orig'
            else:
                self.comSaRepository = '%s/comsa_for_coremw-apr9010555/repository/' %result[1]
                self.modelFileList='%s/com-apr9010443/etc/model/model_file_list.cfg' %result[1]
                self.origModelFileList='%s/com-apr9010443/etc/model/model_file_list.cfg.orig' %result[1]

            cmd = '\mkdir -p %s' %self.targetIncomingLocation
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            cmd = '\\rm -rf %s/*' %self.targetIncomingLocation
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            result = self.sshLib.remoteCopy('%s%s' %(self.sdpPathLocalMachine, self.MimSdpName) , self.targetIncomingLocation)
            self.fail(result[0], result[1])

            cmd = 'tar xf %s%s -C %s' %(self.targetIncomingLocation, self.MimSdpName, self.targetIncomingLocation)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            cmd = '\mv -f %s%s %s' %(self.targetIncomingLocation, self.MimSdpName, self.defaultCoreMwSdpImportDir)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            cmd = '\cp %s %s' %(self.modelFileList, self.origModelFileList)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            result = self.safLib.importSwBundle(self.MimSdpName)
            self.fail(result[0], result[1])

            cmd = 'grep safSmfBundle %s/ETF.xml' %self.targetIncomingLocation
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            self.safBundle = result[1].splitlines()[1].split('safSmfBundle=')[1][:-2]

            cmd = 'cat %s/com-model.config ' %self.targetIncomingLocation
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            mpFiles = result[1].splitlines()
            self.mpFiles =[]
            for i in range(len(mpFiles)):
                self.mpFiles.append('%s'%mpFiles[i].split('/')[1])
            if len(self.mpFiles) == 0:
                self.fail('ERROR', 'No mpFiles found in the com-model.config file in %s' %self.targetIncomingLocation)
            self.myLogger.info('The mpFiles are: %s' %str(self.mpFiles))


        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        if self.tag == 'TC-MIM-005':
            # Getting Linux Time for matching the string in syslog
            dateCommandSyslog = "date +%s"
            result = self.sshLib.sendCommand(dateCommandSyslog)
            self.fail(result[0],result[1])
            self.startTimeSyslog = int(result[1])
            self.myLogger.info("Linux System Time for matching string in syslog is: %s" %(self.startTimeSyslog))

            cmd = "pgrep -f 'etc/com.cfg'"
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            comPid1=result[1]

            cmd = 'comsa-mim-tool com_switchover'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            cmd = "pgrep -f 'etc/com.cfg'"
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            comPid2=result[1]

            if comPid1 == comPid2:
                self.fail('ERROR', 'COM has same PID before and after the comsa-mim-tool com_switchover')
            result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], [self.expectedComSA_debug], self.startTimeSyslog, self.testConfig)
            self.sshLib.tearDownHandles()
            self.fail(result[0],result[1])
            self.myLogger.debug('Found %s in log at: %s' %(self.expectedComSA_debug,result[1]))

        else:
            mim_input_list, mim_expected_response_list, mim_diff_result_list, append_sdpBundle_name_list, appendExtraArgs, extraArgs = self.load_MIM_config()
            print '########## EJNOLSZ mim_input_list:', mim_input_list
            print '########## EJNOLSZ mim_expected_response_list: ', mim_expected_response_list
            print '########## EJNOLSZ mim_diff_result_list: ', mim_diff_result_list
            print '########## EJNOLSZ append_sdpBundle_name_list: ', append_sdpBundle_name_list
            print '########## EJNOLSZ appendExtraArgs: ', appendExtraArgs
            print '########## EJNOLSZ extraArgs: ', extraArgs

            for i in range(len(mim_input_list)):
                if append_sdpBundle_name_list[i] == 'yes':
                    cmd = '%s %s %s' %(self.mimToolCommand, mim_input_list[i], self.safBundle)
                else:
                    cmd = '%s %s' %(self.mimToolCommand, mim_input_list[i])
                if appendExtraArgs[i] == 'yes':
                    cmd+=extraArgs[i]
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])
                expectedResponses = eval(mim_expected_response_list[i])
                missingExpectedResponses = []
                for j in range(len(expectedResponses)):
                    if expectedResponses[j] not in result[1]:
                        missingExpectedResponses.append(expectedResponses[j])
                if len(missingExpectedResponses) > 0:
                    self.fail('ERROR', 'The following expected %s string(s) was/were not found in the comsa-mim-tool response, which is: %s' %(str(missingExpectedResponses), result[1]))

                cmd = 'diff %s %s' %(self.modelFileList, self.origModelFileList)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])
                expectedDifferencesNotFound = []
                if mim_diff_result_list[i] == 'yes':
                    for mpFile in self.mpFiles:
                        if not mpFile in result[1]:
                            expectedDifferencesNotFound.append(mpFile)
                    if len(expectedDifferencesNotFound) > 0:
                        self.fail('ERROR', '%s not found in the diff between the current and original model_file_list.cfg files. The diff result is: %s' %(str(expectedDifferencesNotFound), result[1]))
                else:
                    if 'xml' in result[1]: # This is a workaround for the issue that COM leaves an empty line in the modelFileList after 'com_mim_tool --remove'. The if statement should be: "if result[1]!= '':"
                        self.fail('ERROR', 'Unexpected difference between the current and original model_file_list.cfg files. The diff result is: %s' %result[1])


        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")



    def tearDown(self):
        self.setTestStep('tearDown')

        if self.tag == 'TC-MIM-005':
            print 'tearDown in COM SA MIM Tool Switchover'
        else:
            failures = []
            result = self.safLib.removeSwBundle(self.safBundle)
            if result[0] != 'SUCCESS':
                failures.append(result[1])

            cmd = '\mv -f %s %s' %(self.origModelFileList, self.modelFileList)
            result = self.sshLib.sendCommand(cmd)
            if result[0] != 'SUCCESS':
                failures.append(result[1])

            cmd = '\\rm -rf %s' %self.targetIncomingLocation
            result = self.sshLib.sendCommand(cmd)
            if result[0] != 'SUCCESS':
                failures.append(result[1])

            cmd = '\\rm -rf %s/%s' %(self.comSaRepository, self.safBundle)
            result = self.sshLib.sendCommand(cmd)
            if result[0] != 'SUCCESS':
                failures.append(result[1])

            if len(failures) != 0:
                self.fail('ERROR', 'Failures happened during tearDown: %s' %str(failures))


        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

    def load_MIM_config(self):
        '''
        This method loads the configs from the data received from the xml,
         and creates a list of the comsa-mim-tool inputs, expected outputs and consequences.
        1. Checking the data received from the xml
        2. Create list
        3. return list

        The method returns 3 lists:
         (mim_input_list, mim_expected_response_list, mim_diff_result_list, append_sdpBundle_name_list)

        '''

        self.myLogger.debug('enter load_TC_cli_config function')
        mim_input_list = []
        mim_expected_response_list = []
        mim_diff_result_list = []
        append_sdpBundle_name_list = []
        appendExtraArgs = []
        extraArgs = []

        if self.mimToolParams1 != {} and self.expectedResponses1 != {} and self.diffResult1 != {} and self.appendSdpBundleName1 != {} and self.appendExtraArgs1 != {} and self.extraArgs1 != {}:
            mim_input_list.append(self.mimToolParams1)
            mim_expected_response_list.append(self.expectedResponses1)
            mim_diff_result_list.append(self.diffResult1)
            append_sdpBundle_name_list.append(self.appendSdpBundleName1)
            appendExtraArgs.append(self.appendExtraArgs1)
            extraArgs.append(self.extraArgs1)
        print
        if self.mimToolParams2 != {} and self.expectedResponses2 != {} and self.diffResult2 != {} and self.appendSdpBundleName2 != {} and self.appendExtraArgs2 != {} and self.extraArgs2 != {}:
            mim_input_list.append(self.mimToolParams2)
            mim_expected_response_list.append(self.expectedResponses2)
            mim_diff_result_list.append(self.diffResult2)
            append_sdpBundle_name_list.append(self.appendSdpBundleName2)
            appendExtraArgs.append(self.appendExtraArgs2)
            extraArgs.append(self.extraArgs2)
        if self.mimToolParams3 != {} and self.expectedResponses3 != {} and self.diffResult3 != {} and self.appendSdpBundleName3 != {} and self.appendExtraArgs3 != {} and self.extraArgs3 != {}:
            mim_input_list.append(self.mimToolParams3)
            mim_expected_response_list.append(self.expectedResponses3)
            mim_diff_result_list.append(self.diffResult3)
            append_sdpBundle_name_list.append(self.appendSdpBundleName3)
            appendExtraArgs.append(self.appendExtraArgs3)
            extraArgs.append(self.extraArgs3)
        if self.mimToolParams4 != {} and self.expectedResponses4 != {} and self.diffResult4 != {} and self.appendSdpBundleName4 != {} and self.appendExtraArgs4 != {} and self.extraArgs4 != {}:
            mim_input_list.append(self.mimToolParams4)
            mim_expected_response_list.append(self.expectedResponses4)
            mim_diff_result_list.append(self.diffResult4)
            append_sdpBundle_name_list.append(self.appendSdpBundleName4)
            appendExtraArgs.append(self.appendExtraArgs4)
            extraArgs.append(self.extraArgs4)
        if self.mimToolParams5 != {} and self.expectedResponses5 != {} and self.diffResult5 != {} and self.appendSdpBundleName5 != {} and self.appendExtraArgs5 != {} and self.extraArgs5 != {}:
            mim_input_list.append(self.mimToolParams5)
            mim_expected_response_list.append(self.expectedResponses5)
            mim_diff_result_list.append(self.diffResult5)
            append_sdpBundle_name_list.append(self.appendSdpBundleName5)
            appendExtraArgs.append(self.appendExtraArgs5)
            extraArgs.append(self.extraArgs5)
        self.myLogger.debug('leave load_TC_cli_config function')
        return (mim_input_list, mim_expected_response_list, mim_diff_result_list, append_sdpBundle_name_list, appendExtraArgs, extraArgs)


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
