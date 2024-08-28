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
from __builtin__ import True


''' GENERAL INFORMATION:

    Tags:
    TC-UNITT-001    Availability control - Switchover


    Sensitivity:
    Low

    Description:

    Restrictions:
    -

    Test tools:

    Help:
    The test script is driven by the following parameters:





    TEST CASE SPECIFICATION:

    Tag:
    TC-UNITT-001


    Id:
    Switchover


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
from java.lang import System

class UnitTest(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance )

        # parameters from the config files
        self.unitTestFile = {}
        self.unitTestValgrindFile = {}
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.host_arch = 'x86_64'   # used to detect if we are running on a 64-bit host. If not, then skip the unit tests


    def id(self):
        return self.name

    def setUp(self):
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        #self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        #self.pathToModelFiles = dict.get("FT763_MODELFILE_PATH")
        self.pathToUnitTestFile = '%s%s' %(self.COMSA_REPO_PATH, dict.get("UNIT_TEST"))
        self.pathToKnownValgrindLeaks = '%s%s' %(self.COMSA_VERIF_PATH, dict.get("VALGRIND_LEAKS_STORAGE"))
        self.pathToNewUTValgrindLeaks = '%s/valgrind_logs' %(self.pathToUnitTestFile)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.valgrindLogParser = '%s/%s/valgrindLogParser.sh' %(self.MY_REPOSITORY, self.pathToConfigFiles)
        self.buildDir = dict.get('BUILD_TOKENS')

    def runTest(self):
        self.setTestStep('runTest')
        self.myLogger.info('enter runTest')

        # determine the host type (32/64-bit architecture)
        self.myLogger.debug('Get the host architecture (32/64 bit)')
        cmd = 'uname -p'
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        self.this_host_arch = result[1].strip()

        # skip the unit test if not running on a 64-bit host
        if self.this_host_arch == self.host_arch :

            # Variables needed for the build token management
            dirName = System.getProperty("logdir")
            user = os.environ['USER']
            self.tokenPattern = 'buildToken-unittest-%s' %user
            self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
            self.numberOfGetTokenRetries = 5

            # Get a build token
            for i in range(self.numberOfGetTokenRetries):
                result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
                if result[0] == 'SUCCESS':
                    break
            self.fail(result[0],result[1])

            result = self.miscLib.execCommand("bash -c 'pushd %s ; make clean ; make; popd'" %self.pathToUnitTestFile)
            self.fail(result[0], result[1])
            if 'error' in result[1] or 'failed' in result[1]:
                self.fail('ERROR', 'Unexpected error or failure while running the make command.\n%s' %result[1])

            # check if comsa-source has UT valgrind scripts
            if os.path.exists("%s/%s" %(self.pathToUnitTestFile, self.unitTestValgrindFile)):
                self.myLogger.debug('Prefer valgrind unittest')
                runValgrind = True
            else:
                runValgrind = False

            if runValgrind == True:
                result = self.miscLib.execCommand("bash -c 'pushd %s; ./%s; popd'" %(self.pathToUnitTestFile, self.unitTestValgrindFile))
            else:
                result = self.miscLib.execCommand("bash -c 'pushd %s; ./%s; popd'" %(self.pathToUnitTestFile, self.unitTestFile))
            self.fail(result[0], result[1])
            if not '[  PASSED  ]' in result[1]:
                self.fail('ERROR', 'Running unit test did not pass.\n%s' %result[1])
            elif '[  FAILED  ]' in result[1] or 'FAILED TEST' in result[1]:
                error = result[1].find('[  FAILED  ]')
                if error == -1:
                    error = result[1].find('FAILED TEST')
                self.fail('ERROR', 'There was at least one error or failure during excution of the unit test.\n%s'%result[1][error-100:error+200])
            elif runValgrind == True:
                # if there is valgrind log
                if os.listdir(self.pathToNewUTValgrindLeaks):
                    # Check for valgrind results
                    # Copy parse script to valgrind_logs folder
                    cmd = "cp %s %s" %(self.valgrindLogParser, self.pathToNewUTValgrindLeaks)
                    result = self.miscLib.execCommand(cmd)

                    # Add executive permission
                    logParserFileName = self.valgrindLogParser.split("/")[len(self.valgrindLogParser.split("/")) - 1]
                    cmd = "chmod +x %s/%s" %(self.pathToNewUTValgrindLeaks, logParserFileName)
                    result = self.miscLib.execCommand(cmd)

                    # Execute parsing
                    cmd = "bash -c 'pushd %s/; ./%s; popd'"%(self.pathToNewUTValgrindLeaks, logParserFileName)
                    result = self.miscLib.execCommand(cmd)
                    self.fail(result[0],result[1])
                    if 'No such file or directory' in result[1]:
                        self.fail('ERROR', result[1])
                    elif 'Permission denied' in result[1]:
                        self.fail('ERROR', result[1])
                    self.setAdditionalResultInfo("Valgrind logs can be found under: %s." %self.pathToNewUTValgrindLeaks)
                    result = self.comsa_lib.findNewLeaks(self.pathToKnownValgrindLeaks, self.pathToNewUTValgrindLeaks, True)
                    self.fail(result[0], result[1])

            # Release the build token
            result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPattern)
            self.fail(result[0],result[1])

        else:
            self.myLogger.info('Cannot execute the unit tests on this host type: %s, shipping this step, expected: %s.' %(self.this_host_arch, self.host_arch) )
            self.setAdditionalResultInfo('Cannot execute the unit tests on this host type: %s, shipping this step, expected: %s arrchitecture.' %(self.this_host_arch, self.host_arch) )

        self.myLogger.info("exit runTest")

    def tearDown(self):
        self.myLogger.debug('tearDown is not needed')

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
