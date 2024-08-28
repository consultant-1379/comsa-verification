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

class YourClassNameHere(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files        
        

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')   
        self.setTestcase(self.tag, self.name)    
        coreTestCase.CoreTestCase.setUp(self)
        
        
        
        self.myLogger.info('Exit setUp')
      
    def runTest(self):
        self.logger.info('runTest')        
        self.setTestStep('runTest')
           

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
