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
import time
import os

class RestoreBackup(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.backupName = {}
        self.takeStandardBackup = 'False'
        # If you need to use this test case to restore a backup that is not consisting of Core MW, COM, COM SA
        # you need to define the installationLevel argument in the test case xml file. The default value is 3.
        # See the help for restoreSystem() for more information
        self.installationLevel = '3'

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        try:
            self.installationLevel = int(self.installationLevel)
        except ValueError:
            self.fail('ERROR', 'self.installationLevel must be a string representation of an int. Instead it is: %s' %self.installationLevel)

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' %(self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        if self.memoryCheck:
            for controller in self.testConfig['controllers']:
                result = self.comsa_lib.comRestart(self, controller[0], controller[1], self.memoryCheck)
                self.fail(result[0],result[1])

        if self.takeStandardBackup == "True":
            if self.testSuiteConfig.has_key('restoreBackup'):
                backupName = self.testSuiteConfig['restoreBackup']
                result = self.safLib.isBackup(backupName)
                if result == ('SUCCESS', 'EXIST'):
                    self.backupName = backupName
        self.myLogger.info("self.backupName: %s" %self.backupName)
        result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, desiredInstallationLevel = self.installationLevel, removeBackup = False)
        self.fail(result[0],result[1])

        if self.memoryCheck:
            self.setTestStep('Activating Valgrind')
            pathToRpms = ''
            installRpms = False
            result = self.comsa_lib.activateValgrind(self, self.testConfig, pathToRpms, self.replaceComScript, self.pathOnTarget, self.serviceInstanceName, self.amfNodePattern, installRpms)
            self.fail(result[0], result[1])


        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")



    def tearDown(self):
        self.setTestStep('tearDown')



        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
