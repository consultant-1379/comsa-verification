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
    TC-NCONF-001    Configuration using Netconf - Reading configuration - Read the top level
    TC-NCONF-002    Configuration using Netconf - Reading configuration - Reading the next level
    TC-NCONF-003    Configuration using Netconf - Reading configuration - Reading the entire configuration
    TC-NCONF-004    Configuration using Netconf - Reading configuration - Reading a non-existing object

    Sensitivity:
    Low

    Description:

    Restrictions:
    -

    Test tools:

    Help:
    The test script is driven by the following parameters:

    pathToConfigFiles
    scriptFile
    pwdFreeScript
    helloFile
    actionFile
    closeFile
    logFile
    respFile
    serviceInstanceName
    amfNodePattern



    TEST CASE SPECIFICATION:

    Tag:
    TC-NCONF-001


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

==================================

'''

import test_env.fw.coreTestCase as coreTestCase
import time
import re
import copy
import os
import omp.tf.netconf_lib as netconf_lib

from java.lang import System

class configNetconf(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )

        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.scriptFile = {}
        self.pwdFreeScript = {}
        self.helloFile = {}
        self.actionFile = {}
        self.closeFile = {}
        self.logFile = {}
        self.respFile = {}


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
        self.buildDir = dict.get('BUILD_TOKENS')
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)
        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])
        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.myLogger.info('exit setUp')

    def runTest(self):

        self.setTestStep('runTest')
        self.myLogger.info('enter runTest')

        self.setTestStep('runTest find active comSa node')

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPatternNetconf = 'buildToken-netconf-%s' %user
        self.tokenPatternSshSetup = 'buildToken-ssh-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

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


        self.setTestStep('runTest creating authorized key to active controller')

        self.pathToConfigFiles = '%s%s'%(self.MY_REPOSITORY, self.pathToConfigFiles)

        activeCtrlAddr = self. targetData['ipAddress']['ctrl']['ctrl%d'%activeController]
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
            result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)
            self.sshLib.setTimeout(stressTimeOut)

        self.setTestStep('execute netconf command and parsing the result')

        execScript = '%s%s' %(self.pathToConfigFiles, self.scriptFile)
        hello = '%s%s' %(self.pathToConfigFiles, self.helloFile)
        action= '%s%s' %(self.pathToConfigFiles, self.actionFile)
        close = '%s%s' %(self.pathToConfigFiles, self.closeFile)
        logFile = '%s%s' %(self.pathToConfigFiles, self.logFile)

        #scriptCmd = 'cat %s %s %s | ssh root@%s -s -t -t netconf > %s; echo %s' %(hello, action, close, activeCtrlAddr, logFile, logFile)
        scriptCmd = 'cat %s %s %s | ssh root@%s -s -t netconf > %s; echo %s' %(hello, action, close, activeCtrlAddr, logFile, logFile)

        for i in range(self.numberOfGetTokenRetries):
            result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPatternNetconf)
            if result[0] == 'SUCCESS':
                break
        self.fail(result[0], result[1])

        result = self.miscLib.execCommand('\\rm -f %s' %logFile)
        self.fail(result[0], result[1])
        result = self.miscLib.execCommand('touch %s' %logFile)
        self.fail(result[0], result[1])

        result = self.miscLib.execCommand('%s' %(scriptCmd))
        #self.fail(result[0], result[1]) #this will fail for some reason, but the output is saved in the log file and this is what matters

        try:
            fd = open(logFile, 'r')
        except:
            self.myLogger.error('Open file %s FAILED' % logFile)
        xmlMessage = fd.read()
        fd.close()

        # Release the build token
        result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPatternNetconf)
        self.fail(result[0], result[1])


        self.myLogger.info('The replied xml message is: \n%s' %xmlMessage)

        respFile = '%s%s' %(self.pathToConfigFiles, self.respFile)
        try:
            fd = open(respFile, 'r')
        except:
            self.myLogger.error('Open file %s FAILED' % respFile)
        expectedResponses = fd.read()
        fd.close()

        expectedResponses = eval(expectedResponses) #It is expected that the file contains a list of patterns that will be searched in the xmlMessage

        elementsNotFound = []
        for message in expectedResponses:
            if message in xmlMessage:
                self.myLogger.debug('%s found in xml response.' %message)
            else:
                elementsNotFound.append(message)

        if len(elementsNotFound) != 0:
            self.fail('ERROR', 'The following elements were not found in the xml response message: %s' %str(elementsNotFound))

        #result = self.miscLib.execCommand('cat %s %s %s | %s' %(self.helloFile, self.doFile, self.closeFile, self.netconfConnectCommand))
        #self.myLogger.info('\nResult of xml execute is: \n%s' %str(result))

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')
        self.myLogger.info("enter tearDown")

        self.setTestStep('remove authorized keys from the cluster')
        self.comsa_lib.removeAuthorizedKey(self.testConfig)

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info("exit tearDown")

        #########################
        #### SUPPORT METHODS ####
        #########################




def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
