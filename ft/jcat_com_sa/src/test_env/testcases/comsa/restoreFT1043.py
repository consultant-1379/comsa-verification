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
    TC-FT1043-005    FT for SDP 1043 - restoring the cluster


    Sensitivity:
    Low

    Description:

    Restrictions:
    This test case has to the last in the test suite testing SDP1043 and be run at least after TC-FT1043-001

    Test tools:

    Help:
    The test script is driven by the following parameters:





    TEST CASE SPECIFICATION:

    Tag:
    TC-FT1043-005


    Id:
    FunctionTestSdp1043


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
import os
import re
import time

from java.lang import System

class FTSdp1043Restore(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )

        # parameters from the config files
        self.testOIFile = 'testOI'
        self.immClassesFile = 'imm_classes.xml'
        self.mpFile = 'mp.xml'
        self.pathOnTargetSystem = '/home/coremw/incoming/'
        self.modelFile = '/home/com/etc/model/model_file_list.cfg'
        self.tmpModelFile = '/home/com/etc/model/model_file_list.cfg.old'
        self.testOIRunParams = 'ObjImpTestRoot objImpTestRootId=1'
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.backupName = 'FT1043_initialBackup'

    def id(self):
        return self.name

    def setUp(self):
        self.setTestcase(self.tag, self.name)
        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        #self.pathToModelFiles = dict.get("FT763_MODELFILE_PATH")
        self.pathToTestOI = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("PATH_TO_TESTOI"))

        #self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.installStressTool = eval(System.getProperty("runStressTool"))
        coreTestCase.CoreTestCase.setUp(self)
        #cli_script_name = self.cli_tester_script This name is missing from this file I guess.


        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

    def runTest(self):

        self.setTestStep('runTest')
        self.myLogger.info('enter runTest')

# Clean the files used in the test and restore those that have been modified

        result = self.sshLib.sendCommand('\\rm -f %s%s' %(self.pathOnTargetSystem, self.testOIFile))
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('\\rm -f %s%s' %(self.pathOnTargetSystem, self.immClassesFile))
        self.fail(result[0], result[1])

        result = self.sshLib.sendCommand('\\rm -f %s%s' %(self.pathOnTargetSystem, self.mpFile))
        self.fail(result[0], result[1])

        cmd = '\mv -f %s %s' %(self.tmpModelFile, self.modelFile) #make a copy of the original model file. This will be restored by the end of the test
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        if self.memoryCheck:
            for controller in self.testConfig['controllers']:
                result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                self.fail(result[0],result[1])

        removeBackup = True
        if self.testSuiteConfig.has_key('restoreBackup'):
            result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
            if result == ('SUCCESS', 'EXIST'):
                self.backupName = self.testSuiteConfig['restoreBackup']
                removeBackup = False
            elif result == ('SUCCESS','NOT EXIST'):
                self.testSuiteConfig.__delitem__('restoreBackup')
        result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = removeBackup)
        self.fail(result[0],result[1])

        if self.memoryCheck:
            self.setTestStep('Activating Valgrind')
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0],result[1])

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.myLogger.info('tearDown')
        coreTestCase.CoreTestCase.tearDown(self)
        self.myLogger.info('exit tearDown')



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
