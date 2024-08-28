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
from java.lang import System

class ComRestart(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.numberOfRestarts = '20'


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs = self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0],result[1])
        self.activeController = result[1]


        if 'int' in str(type(eval(self.numberOfRestarts))):
            for i in range(eval(self.numberOfRestarts)):
                self.setTestStep('Com restart #%d' %i)
                result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck, calcStartStopTimes = True)
        else:
            self.fail("ERROR", "self.numberOfRestarts must be a string representation of an integer. self.numberOfRestarts is: %s" %str(self.numberOfRestarts))

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
