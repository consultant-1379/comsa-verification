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

class CreateBackup(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.backupName = {}
        self.standardComSaBackup = 'False'

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        dict = self.comsa_lib.getGlobalConfig(self)

        coreTestCase.CoreTestCase.setUp(self)

        try:
            self.standardComSaBackup = eval(self.standardComSaBackup)
        except NameError:
            self.fail('ERROR', 'self.standardComSaBackup must be a string "True" or "False." Current value: %s' %self.standardComSaBackup)

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        skipCreateBackup = False
        if self.standardComSaBackup and self.testSuiteConfig.has_key('restoreBackup'):
            result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
            if result == ('SUCCESS', 'EXIST'):
                skipCreateBackup = True
                self.myLogger.info('Standard COM SA backup exists. Skip creating identical backup.')
        if skipCreateBackup == False:
            result = self.safLib.isBackup(self.backupName)
            if result[0] != 'SUCCESS':
                self.fail(result[0], result[1])
            elif result != ('SUCCESS','NOT EXIST'):
                result = self.safLib.backupRemove(self.backupName)
                if result[0] != 'SUCCESS':
                    self.fail(result[0], result[1])
            result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
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
