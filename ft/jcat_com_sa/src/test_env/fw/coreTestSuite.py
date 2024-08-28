#!/usr/bin/env python
#coding=iso-8859-1
###############################################################################
#
# © Ericsson AB 2009 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################
 
'''File information:
   ===================================================
   File:  coreTestSuite 
   Rev:   P1A01
   Date:  2009-11-12 
 
   Description: 

    
'''
###############################################################################
# Python common resources imports
###############################################################################
import os
import sys
from java.util import Properties
from java.lang import System 

###############################################################################
# FW imports
###############################################################################
from junit.framework import TestSuite
from org.apache.log4j import Logger

from coreTestSetup import CoreTestSetup
#from se.ericsson.jcat.omp.fw import OmpTestSetup

class CoreTestSuite(TestSuite):

    def __init__(self, logLevel):
        TestSuite.__init__(self, System.getProperty("suiteName"))
        self.logger = Logger.getLogger(self.__class__)
        self.logLevel = logLevel
        
    def suite(self, suite):
        for test in suite:
            self.addTest(test) 
        return CoreTestSetup(self, self.logLevel)  

    








