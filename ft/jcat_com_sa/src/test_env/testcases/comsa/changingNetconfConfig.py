#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
###############################################################################
#
# Copyright Ericsson AB 2010 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################


''' GENERAL INFORMATION:

    Tags:
    TC-COMSA-NCONF-005    Configuration using Netconf - Changing configuratipn - Changing an attribute value
    TC-COMSA-NCONF-006    Configuration using Netconf - Changing configuratipn - Creating a new object and deleting it

    Sensitivity:
    Low

    Description:

    Restrictions:
    -

    Test tools:

    Help:
    The test script is driven by the following parameters:

    self.pathToConfigFiles - the location where all the files below are located
    self.scriptFile - not used as of 2011.07.21, but it basically sends a netconf message to the cluster and redirects the output to a logfile
    self.pwdFreeScript - the name of the script which creates the authorized keys on the system controller so that when sending the netconfimessages, no password is required
    self.helloFile - name of the neconf file which opens the connection
    self.actionFile - name of the first netconf message that does an action/modification in the configuration of the cluster
    self.actionFile2 - name of the second netconf message that does an action/modification in the configuration of the cluster - typically a check of the previous action
    self.actionFile3 - name of the third netconf message that does an action/modification in the configuration of the cluster - typically a restore of the first action
    self.actionFile4 - name of the fourth netconf message that does an action/modification in the configuration of the cluster - typically a check of the previous action
    self.closeFile - name of the neconf file which closes the connection - could be interpreted as a commit
    self.logFile - name of the file which will store the result of the execution of the action files above
    self.respFile - a list of strings that will be matched against the result returned be the execution of actionFile
    self.respFile2 - a list of strings that will be matched against the result returned be the execution of actionFile2
    self.respFile3 - a list of strings that will be matched against the result returned be the execution of actionFile3
    self.respFile4 - a list of strings that will be matched against the result returned be the execution of actionFile4
    self.serviceInstanceName - the name of the service instance who's HA status is checked in determining the active controller
    self.amfNodePattern - pattern used in the amf configuration for the controllers
    self.forbiddenContent - this is a list of strings containing elements that may not be part of the response when executing the actionFile4





    TEST CASE SPECIFICATION:

    Tag:
    TC-NCONF-005
    TC-NCONF-006
    TC-NCONF-007

    Id:
    Configuration using netconf


    Priority:
    High


    Requirement:


    Test script:
    N/A


    Configuration:
    2SC+nPL


    Action:


    Result:


    Restore:
    N/A


    Other:     TC-NCONF-006 and TC-NCONF-007 are executed together (within the same execution of the test script, with the execution of the TC-NCONF-006)

==================================

'''

import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib

from java.lang import System

class changingNetconfConfig(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )

        self.testcase_tag = tag
        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        self.scriptFile = {}
        self.pwdFreeScript = {}
        self.helloFile = {}
        self.actionFile = {}
        self.actionFile2 = {}
        self.actionFile3 = {}
        self.actionFile4 = {}
        self.actionFile5 = {}
        self.actionFile6 = {}
        self.closeFile = {}
        self.logFile = {}
        self.respFile = {}
        self.respFile2 = {}
        self.respFile3 = {}
        self.respFile4 = {}
        self.respFile5 = {}
        self.respFile6 = {}
        self.createBackup = {}
        self.forbiddenContent = {}
        self.useExternalModels = {}
        self.modelFilePathOnTarget = {}
        self.momFile = {}
        self.immClassesFile = {}
        self.immObjectsFile = {}
        self.momFile2 = {}
        self.immClassesFile2 = {}
        self.immObjectsFile2 = {}
        self.immObjPattern = '[]'
        self.modelFileType = ''
        self.actionTest_file = 'actionTestAppl'
        self.actionTest_tempdir = '/home/actiontest/'
        self.reqComSaRelease = "3"
        self.reqComSaMajorVersion = "1"
        self.longDn = ""

        # defautle is the lowest version
        if self.longDn != 'True':
            self.reqCmwVersion = "R1A01"
        else:
            self.reqCmwVersion = "R10A01"

        self.reqComSaVersion = "R1A01"
        self.reqComVersion = "R1A01"
        self.reqComSaRelease = "3"
        self.reqComRelease = "2"
        self.reqCmwRelease = "1"

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.myLogger.info('enter setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.actionTest_path = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("ACTION_TEST_PATH"))
        self.buildDir = dict.get('BUILD_TOKENS')

        if self.modelFileType == '763':
            self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("FT763_MODELFILE_PATH"))
        elif self.modelFileType == 'CDT':
            self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("EXAMPLE_MODELFILE_PATH"))
        elif self.modelFileType == '975':
            self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MODEL_FILE_PATH"))
        elif self.modelFileType == 'MR24146':
            self.pathToModelFiles = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("MR24146_MODELFILE_PATH"))
        else:
            self.pathToModelFiles = ''

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPattern = 'buildToken-actionTest-%s' %user
        self.tokenPatternNetconf = 'buildToken-netconf-%s' %user
        self.tokenPatternSshSetup = 'buildToken-ssh-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5


        self.myLogger.info('exit setUp')

    def runTest(self):

        self.setTestStep('runTest')
        self.myLogger.info('enter runTest')

        CmwMajorOK = ('SUCCESS', True)
        ComMajorOK = ('SUCCESS', True)
        ComsaMajorOK = ('SUCCESS', True)
        self.skip_test = False
        self.isRunningComSa3_2Bwd = False

        CmwMajorOK = self.lib.checkComponentMajorVersion('cmw', "1", "6", [], True )
        ComMajorOK = self.lib.checkComponentMajorVersion('com', "2" , "7", [], True )
        ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', self.reqComSaRelease, self.reqComSaMajorVersion)
        self.fail(ComsaMajorOK[0],ComsaMajorOK[1])
        # add to check version for TC-MR35347-012
        self.setTestStep('Check the required versions of ComSA, Com and CMW is installed')
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion )
        self.fail(ComsaOK[0],ComsaOK[1])
        ComOK = self.lib.checkComponentVersion('com', self.reqComRelease, self.reqComVersion )
        self.fail(ComOK[0],ComOK[1])
        CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )
        self.fail(CmwOK[0],CmwOK[1])

        if CmwMajorOK[1] == False and ComMajorOK[1] == False:
            self.isRunningComSa3_2Bwd = True

        if ComsaMajorOK[1] == True and ComsaOK[1] and ComOK[1] and CmwOK[1]:

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

                # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
                #res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

                stressTimeOut = 60
                self.sshLib.setTimeout(stressTimeOut)

            self.setTestStep('runTest find active comSa node')

            self.activeController = (0,0)
            activeController = 0

            controllers = self.testConfig['controllers']
            self.myLogger.info('Checking HA state for Com SA on the controllers')
            for controller in controllers:
                result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                if result[1] == 'ACTIVE':
                    activeController = controller[1]
                    self.myLogger.info('Found active controller: %s' %str(controller))

            if activeController == 0:
                self.fail('ERROR', 'No controller found with active instance of ComSa')

            self.activeController = (controller[0], activeController)
            activeCtrlAddr = self. targetData['ipAddress']['ctrl']['ctrl%d'%activeController]

            if self.useExternalModels == 'yes':

                self.setTestStep('Upload model files to the target')
                cmd = 'mkdir -p %s' %self.modelFilePathOnTarget
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])

                #Copy actionTest application to target
                self.myLogger.debug('Copy model files to target')
                if self.pathToModelFiles == '':
                    self.fail('ERROR', 'Model file type has to be defined in the xml file of the test case.')
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])
                result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile), self.modelFilePathOnTarget, timeout = 60)
                self.fail(result[0],result[1])
                if self.immObjectsFile != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immObjectsFile), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])

                if self.momFile2 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.momFile2), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                if self.immClassesFile2 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immClassesFile2), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])
                if self.immObjectsFile2 != {}:
                    result = self.sshLib.remoteCopy('%s/%s' %(self.pathToModelFiles, self.immObjectsFile2), self.modelFilePathOnTarget, timeout = 60)
                    self.fail(result[0],result[1])


                result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                self.fail(result[0],result[1])
                if self.momFile2 != {}:
                    result = self.comsa_lib.addMomFileToCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2))
                    self.fail(result[0],result[1])

                self.setTestStep('### Loading model files to IMM')

                #Loading model files
                self.myLogger.debug('Loading model files')
                cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])
                if self.immClassesFile2 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immClassesFile2)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])

                if self.immObjectsFile != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immObjectsFile)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])
                if self.immObjectsFile2 != {}:
                    cmd = 'immcfg -f %s%s' %(self.modelFilePathOnTarget, self.immObjectsFile2)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])

            if self.longDn == 'True':
                cmd = 'immlist -a longDnsAllowed opensafImm=opensafImm,safApp=safImmService'
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                if result[1] != 'longDnsAllowed=1':
                    self.setTestStep('###Set attribute longDnsAllowed=1###')
                    cmd = 'immcfg --admin-owner-clear opensafImm=opensafImm,safApp=safImmService'
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])

                    cmd = 'immcfg -m -a longDnsAllowed=1 opensafImm=opensafImm,safApp=safImmService'
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.fail(result[0],result[1])
                    if result[1] != '':
                        self.fail('ERROR', result[1])


            # Restart COM
            self.myLogger.debug('Restart COM')
            result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
            self.fail(result[0],result[1])

############################################################################################
            if self.testcase_tag == 'TC-FT975-001' or self.testcase_tag == 'TC-FT872-003' or self.testcase_tag == 'TC-MR24146-002' or self.testcase_tag == 'TC-MR35347-012':

                id = ''
                if self.longDn == 'True':
                    id = 'This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_1'
                else:
                    id = '1'
                cmd = 'immcfg -c Sdp617ActiontestRoot sdp617ActiontestRootId=%s' %id
                self.myLogger.debug('Creating IMM objects: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

                cmd = 'immcfg -c ActionTest actionTestId=1,sdp617ActiontestRootId=%s' %id
                self.myLogger.debug('Creating IMM objects: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])
                if result[1] != '':
                    self.fail('ERROR', result[1])

                #Create temporary directory on target
                cmd = 'mkdir %s' %self.actionTest_tempdir
                self.myLogger.debug('Create temporary directory on target: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])

                self.setTestStep('### Building the test-application')

                # Get a build token
                for i in range(self.numberOfGetTokenRetries):
                    result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                    if result[0] == 'SUCCESS':
                        break
                self.fail(result[0],result[1])

                #Do make clean before building the test-application
                cmd = 'cd %s;make clean' %self.actionTest_path
                self.myLogger.debug('Do make clean before building the test-application by: %s' %cmd)
                result = self.miscLib.execCommand(cmd)
                self.fail(result[0],result[1])
                cmd = 'ls %s | grep -c %s' %(self.actionTest_path, self.actionTest_file)
                result = self.miscLib.execCommand(cmd)
                self.fail(result[0],result[1])
                if result[1].split()[0] != '0':
                    self.fail('ERROR', 'File is not removed after make clean!')

                #Build the test-application
                if self.longDn == "True":
                    cmd = 'cd %s;make CFLAGS="-g -O2 -Wall -fPIC -DTEST_FOR_LONG_DN -DSA_EXTENDED_NAME_SOURCE"' %self.actionTest_path
                else:
                    # check for COMSA 3.4 and below
                    ComsaMajorOK = self.lib.checkComponentMajorVersion('comsa', '3', '6', [], True)
                    if ComsaMajorOK[1] == False: #COMSA 3.4 and below
                        cmd = 'cd %s;make -f Makefile.old' %self.actionTest_path
                    else:
                        cmd = 'cd %s;make' %self.actionTest_path
                self.myLogger.debug('Building the test-application by: %s' %cmd)
                result = self.miscLib.execCommand(cmd)
                self.fail(result[0],result[1])
                cmd = 'ls %s | grep -c %s' %(self.actionTest_path, self.actionTest_file)
                result = self.miscLib.execCommand(cmd)
                self.fail(result[0],result[1])
                if result[1].split()[0] != '1':
                    self.fail('ERROR', 'Building was unsuccessful!')

                self.setTestStep('### Copy the test-application to target')
                #Copy actionTest application to target
                self.myLogger.debug('Copy actionTest application to target')
                result = self.sshLib.remoteCopy('%s%s' %(self.actionTest_path, self.actionTest_file), self.actionTest_tempdir, timeout = 60)
                self.fail(result[0],result[1])

                # Release the build token
                result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                self.fail(result[0],result[1])

                self.setTestStep('### Running the test-application')
                #Giving permission for execution
                cmd = 'chmod u+x %s%s' %(self.actionTest_tempdir, self.actionTest_file)
                self.myLogger.debug('Giving permission for execution by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])

                #Start actionTest application
                save_default_timeout = self.sshLib.getTimeout(self.activeController[0], self.activeController[1])
                self.sshLib.setTimeout(8, self.activeController[0], self.activeController[1])
                if self.longDn == "True":
                    cmd = 'export SA_ENABLE_EXTENDED_NAMES=1;nohup %s%s >>nohup.out 2>&1 &' %(self.actionTest_tempdir, self.actionTest_file)
                else:
                    cmd = 'nohup %s%s >>nohup.out 2>&1 &' %(self.actionTest_tempdir, self.actionTest_file)
                self.myLogger.debug('Start actionTest application by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])

                self.sshLib.setTimeout(save_default_timeout, self.activeController[0], self.activeController[1])
                actiontest_pid = result[1].split()[1]

                self.setTestStep('### Enable the trace')
                #Enable trace
                cmd = 'kill -usr2 %s' %actiontest_pid
                self.myLogger.debug('Enable trace by: %s' %cmd)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                self.fail(result[0],result[1])

            self.setTestStep('runTest creating authorized key to active controller')

            self.pathToConfigFiles = '%s%s'%(self.MY_REPOSITORY, self.pathToConfigFiles)
            cmd = '%s%s %s  -k ~/.ssh/id_rsa' %(self.pathToConfigFiles, self.pwdFreeScript, activeCtrlAddr)

            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPatternSshSetup)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0],result[1])

            result = self.miscLib.execCommand(cmd)
            self.fail(result[0], result[1])
            if 'Passwordless setup is done and persistent' or 'Passwordless is already setup' in result[1]:
                self.myLogger.debug('pwdfree script execution OK.')
            else:
                self.fail('ERROR', 'Unexpected return from execution of pwdfree script: %s' %result[1])

            # Release the build token
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPatternSshSetup)
            self.fail(result[0],result[1])


            self.setTestStep('execute netconf action1 command and parsing the interim result')

            if self.testcase_tag == 'TC-FT975-001':
                self.setTestStep('SDP975 TC-1 Testing action with struct parameter')

            if self.testcase_tag == 'TC-FT872-003' or self.testcase_tag == 'TC-MR35347-012':
                self.setTestStep('SDP872 TC-1 Testing any return type from action')

            if self.testcase_tag == 'TC-MR24146-002':
                self.setTestStep('MR24146 Testing return structure  from action')

            execScript = '%s%s' %(self.pathToConfigFiles, self.scriptFile)
            hello = '%s%s' %(self.pathToConfigFiles, self.helloFile)
            close = '%s%s' %(self.pathToConfigFiles, self.closeFile)
            logFile = '%s%s' %(self.pathToConfigFiles, self.logFile)
            actionFiles = self.actionFile
            respFile = '%s%s' %(self.pathToConfigFiles, self.respFile)


            result = self.executeNetconfSession(execScript, hello, actionFiles, close, activeCtrlAddr, logFile, respFile)
            self.fail(result[0], result[1])

            #
            #  The following section is for the extra testcases for SDP975
            #

            if self.testcase_tag == 'TC-FT975-001':

                self.setTestStep('SDP975 TC-2 Testing action with multivalue parameter')

                actionFiles = self.actionFile2
                respFile = '%s%s' %(self.pathToConfigFiles, self.respFile)

                result = self.executeNetconfSession(execScript, hello, actionFiles, close, activeCtrlAddr, logFile, respFile)
                self.fail(result[0], result[1])


                self.setTestStep('SDP975 TC-3 Testing action with struct parameter with multivalue elements')

                actionFiles = self.actionFile3
                respFile = '%s%s' %(self.pathToConfigFiles, self.respFile)

                result = self.executeNetconfSession(execScript, hello, actionFiles, close, activeCtrlAddr, logFile, respFile)
                self.fail(result[0], result[1])


                self.setTestStep('SDP975 TC-4 Testing action with multivalue parameter with struct elements')

                actionFiles = self.actionFile4
                respFile = '%s%s' %(self.pathToConfigFiles, self.respFile)

                result = self.executeNetconfSession(execScript, hello, actionFiles, close, activeCtrlAddr, logFile, respFile)
                self.fail(result[0], result[1])
                xmlMessage = result[1]


            #
            #  The following section is for the original testcases TC-NCONF-xxx
            #

            if self.testcase_tag != 'TC-FT975-001' and self.testcase_tag != 'TC-FT872-003' and  self.testcase_tag != 'TC-MR24146-002' and self.testcase_tag != 'TC-MR35347-012':

                self.setTestStep('Checking the modified configuration')

                action = self.actionFile2
                respFile = '%s%s' %(self.pathToConfigFiles, self.respFile2)
                result = self.executeNetconfSession(execScript, hello, action, close, activeCtrlAddr, logFile, respFile)
                self.fail(result[0], result[1])


                self.setTestStep('Second set of netconf sessions. Normally to revert the original configuration. For TC-NCONF-009 here we modify one more time')

                actionFiles = self.actionFile3
                respFile = '%s%s' %(self.pathToConfigFiles, self.respFile3)
                result = self.executeNetconfSession(execScript, hello, actionFiles, close, activeCtrlAddr, logFile, respFile)
                self.fail(result[0], result[1])


                self.setTestStep('Checking that the revert configuration operation succeeded')

                action= self.actionFile4
                respFile = '%s%s' %(self.pathToConfigFiles, self.respFile4)
                result = self.executeNetconfSession(execScript, hello, action, close, activeCtrlAddr, logFile, respFile)
                self.fail(result[0], result[1])
                xmlMessage = result[1]


                self.setTestStep('Third set of netconf sessions. Revert the original configuration.')

                if self.actionFile5 != {} and self.respFile5 != {} and self.actionFile6 != {} and self.respFile6 != {}:
                    actionFiles = self.actionFile5
                    respFile = '%s%s' %(self.pathToConfigFiles, self.respFile5)
                    result = self.executeNetconfSession(execScript, hello, actionFiles, close, activeCtrlAddr, logFile, respFile)
                    self.fail(result[0], result[1])


                    self.setTestStep('Checking that the revert configuration operation succeeded')

                    action = self.actionFile6
                    respFile = '%s%s' %(self.pathToConfigFiles, self.respFile6)
                    result = self.executeNetconfSession(execScript, hello, action, close, activeCtrlAddr, logFile, respFile)
                    self.fail(result[0], result[1])
                    xmlMessage = result[1]

                # This is a final verification that there is no undesired content left in the configuration.
                # The last session has to be a get-config type which is evaluated below.

                if 'list' in str(type(eval(self.forbiddenContent))) :
                    forbiddenContent = eval(self.forbiddenContent)
                    matches = []
                    for element in forbiddenContent:
                        if element in xmlMessage:
                            self.myLogger.error('Forbidden string %s found in xml response.' %element)
                            matches.append(element)
                    if len(matches) != 0:
                        self.fail('ERROR', 'Forbidden elements were found in the xml response message: %s' %str(matches))

        else:
            if CmwOK[1] == False:
                self.logger.info('Skipped tests because of CMW version not compatible!')
                self.setAdditionalResultInfo('Test skipped, CMW version not compatible')
            if ComsaOK[1] == False or ComsaMajorOK[1] == False:
                self.logger.info('Skipped tests because of COMSA version not compatible!')
                self.setAdditionalResultInfo('Test skipped, COMSA version not compatible')
            if ComOK[1] == False:
                self.logger.info('Skipped tests because of COM version not compatible!')
                self.setAdditionalResultInfo('Test skipped, COM version not compatible')
            self.skip_test = True


        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')
        self.myLogger.info("enter tearDown")

        if self.skip_test == False:

            if self.installStressTool:
                self.setTestStep('======== Stopping the stress tool on target ========')
                self.comsa_lib.stopStressToolOnTarget(self)

            tdFailures = []

            self.setTestStep('remove authorized keys from the cluster')
            self.comsa_lib.removeAuthorizedKey(self.testConfig)

            if self.useExternalModels == 'yes':

                self.setTestStep('### Removing COM models')
                result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile))
                if result[0] != 'SUCCESS':
                    tdFailures.append(result[1])
                if self.momFile2 != {}:
                    result = self.comsa_lib.removeMomFileFromCom(self.activeController[0], self.activeController[1], '%s%s' %(self.modelFilePathOnTarget, self.momFile2))
                    if result[0] != 'SUCCESS':
                        tdFailures.append(result[1])

                # Restart COM
                self.myLogger.debug('Restart COM')
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
                if result[0] != 'SUCCESS':
                    tdFailures.append(result[1])


                self.setTestStep('### Removing model files from IMM')
                #All three TCs use external models
                if self.testcase_tag == 'TC-FT975-001' or self.testcase_tag == 'TC-FT872-003' or self.testcase_tag == 'TC-MR24146-002' or self.testcase_tag == 'TC-MR35347-012':

                    #Kill actionTest application
                    cmd = 'kill -9 `ps aux | grep %s%s | grep -v grep | awk \'{printf $2}\'`' %(self.actionTest_tempdir, self.actionTest_file)
                    self.myLogger.debug('Kill actionTest application by: %s' %cmd)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

                    #Delete objects
                    id = ''
                    if self.longDn == 'True':
                        id = 'This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_1'
                    else:
                        id = '1'
                    cmd = 'immcfg -d -u actionTestId=1,sdp617ActiontestRootId=%s' %id
                    self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
                    self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    cmd = 'immcfg -d -u sdp617ActiontestRootId=%s' %id
                    self.myLogger.debug('tearDown: Delete test object: %s' %cmd)
                    self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])

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
                        if result[0] != 'SUCCESS':
                            tdFailures.append(result[1])
                        """ Normally the objects should be removed as part of the test case.
                        It is OK that no object is found, thus the response is not an empty string."""
                        #if result[1] != '':
                        #    tdFailures.append('The following issue occurred during removal of IMM objects. Command: %s. Result: %s' %(cmd, result[1]))

                # Below we remove all the classes imported from the imm_classes model file
                cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile)
                result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                if result[0] != 'SUCCESS':
                    tdFailures.append(result[1])
                if result[1] != '':
                    tdFailures.append('The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))
                if self.immClassesFile2 != {}:
                    cmd = """grep "<class" %s/%s | grep name | awk -F'\"' '{ print $2 }' | xargs immcfg --delete-class""" %(self.modelFilePathOnTarget, self.immClassesFile2)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS':
                        tdFailures.append(result[1])
                    if result[1] != '':
                        tdFailures.append('The following issue occurred during removal of IMM classes. Command: %s. Result: %s' %(cmd, result[1]))

                #All three TCs use external models
                if self.testcase_tag == 'TC-FT975-001' or self.testcase_tag == 'TC-FT872-003' or self.testcase_tag == 'TC-MR24146-002' or self.testcase_tag == 'TC-MR35347-012':
                    #Remove temporary directory from target
                    if self.memoryCheck:
                        self.setTestStep('Activating Valgrind')
                        result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
                        if result[0] != 'SUCCESS':
                            self.myLogger.error('Failed to activate Valgrind. %s' %result[1])
                            tdFailures.append('Failed to activate Valgrind. %s' %result[1])

                    #Delete actionTest application
                    cmd = '\\rm -f %s%s' %(self.actionTest_path, self.actionTest_file)
                    self.myLogger.debug('tearDown: Delete %s from %s by: %s' %(self.actionTest_file, self.actionTest_path, cmd))
                    self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    self.miscLib.waitTime(3)

                    cmd = '\\rm -rf %s' %self.actionTest_tempdir
                    self.myLogger.debug('Remove temporary directory from target by: %s' %cmd)
                    result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
                    if result[0] != 'SUCCESS' or result[1] != '':
                        self.myLogger.error('Failed to remove actionTest temp dir')
                        tdFailures.append((cmd, result))

            if tdFailures != []:
                ### Restore testBackup, if available.
                if self.testSuiteConfig.has_key('restoreBackup'):
                    backupName = self.testSuiteConfig['restoreBackup']
                    result = self.comsa_lib.restoreSystem(self, backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
                    if result[0] != 'SUCCESS':
                        self.myLogger.error('Failed to restore backup %s. %s' %(backupName, result[1]))
                        tdFailures.append('Failed to restore backup %s. %s' %(backupName, result[1]))
                    self.setAdditionalResultInfo('Problem detected in tearDown. Restored backup %s' %backupName)
                self.fail('ERROR', 'The following issues happened during tearDown(): %s' %str(tdFailures))

        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info("exit tearDown")



        #########################
        #### SUPPORT METHODS ####
        #########################


    def readFile(self, logFile):
        try:
            fd = open(logFile, 'r')
        except:
            self.myLogger.error('Open file %s FAILED' % logFile)
            return ('ERROR', 'Could not read file: %s' %logFile)
        fileContent = fd.read()
        fd.close()
        return ('SUCCESS', fileContent)

    def sendNetconfMessage(self, execScript, hello, action, close, activeCtrlAddr, logFile):

        #result = self.miscLib.execCommand('%s %s %s  %s %s %s' %(execScript, hello, action, close, activeCtrlAddr, logFile))
        #result = self.miscLib.execCommand('cat %s %s %s | ssh root@%s -s -t -t netconf > %s' %(hello, action, close, activeCtrlAddr, logFile))
        if self.isRunningComSa3_2Bwd == True:
            result = self.miscLib.execCommand('cat %s %s %s | ssh root@%s -s -t -t netconf > %s' %(hello, action, close, activeCtrlAddr, logFile))
        else:
            result = self.miscLib.execCommand('cat %s %s %s | ssh root@%s -s -t netconf > %s' %(hello, action, close, activeCtrlAddr, logFile))
        #this will fail for some reason, but the output is saved in the log file and this is what matters

        result = self.readFile(logFile)
        if result[0] != 'SUCCESS':
            return result
        xmlMessage = result[1]
        return ('SUCCESS', xmlMessage)


    def executeNetconfSession(self, execScript, hello, actionFiles, close, activeCtrlAddr, logFile, expectedResp):

        self.myLogger.debug('enter executeNetconfSession')
        if 'list' in str(type(eval(actionFiles))):
            actionFiles = eval(actionFiles)
            action = ''
            if len(actionFiles) == 0:
                self.myLogger.debug('leave executeNetconfSession')
                return ('ERROR', 'No action file defined for the netconf operation! Edit the actionFile parameter in the xml config file of the test case.')
            for i in range(len(actionFiles)):
                action += ' %s%s' %(self.pathToConfigFiles, actionFiles[i])
        elif 'str' in str(type(actionFiles)):
            action = '%s/%s' %(self.pathToConfigFiles, actionFiles)
        else:
            self.myLogger.debug('leave executeNetconfSession')
            return ('ERROR', 'Unsupported variable type for actionFiles: %s' %str(type(actionFiles)))

        self.myLogger.debug('action: %s' %action)

        # Get a build token
        for i in range(self.numberOfGetTokenRetries):
            result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPatternNetconf)
            if result[0] == 'SUCCESS':
                break
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result

        result = self.sendNetconfMessage(execScript, hello, action, close, activeCtrlAddr, logFile)
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result
        xmlMessage = result[1]
        self.myLogger.info('The replied xml message is: \n%s' %xmlMessage)

        # Release the build token
        result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPatternNetconf)
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result

        result = self.readFile(expectedResp)
        if result[0] != 'SUCCESS':
            self.myLogger.debug('leave executeNetconfSession')
            return result
        expectedResponses = result[1]

        #print 'expectedResponses: ',expectedResponses

        if xmlMessage.count('error') > expectedResponses.count('error') or xmlMessage.count('failed') > expectedResponses.count('failed'):
            self.myLogger.debug('leave executeNetconfSession')
            return ('ERROR', 'The xml response contained an unexpected error. \n%s' %xmlMessage)

        expectedResponses = eval(expectedResponses)
        if not 'list' in str(type(expectedResponses)):
            self.myLogger.debug('leave executeNetconfSession')
            return ('ERROR', 'The expected responses provided have to be in a list format in the %s text file.' %respFile)
        elementsNotFound = []
        for message in expectedResponses:
            if message in xmlMessage:
                self.myLogger.debug('%s found in xml response.' %message)
            else:
                elementsNotFound.append(message)
        if len(elementsNotFound) != 0:
            self.myLogger.debug('leave executeNetconfSession')
            return('ERROR', 'The following elements were not found in the xml response message: %s' %str(elementsNotFound))

        self.myLogger.debug('leave executeNetconfSession')
        return ('SUCCESS', xmlMessage)

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
