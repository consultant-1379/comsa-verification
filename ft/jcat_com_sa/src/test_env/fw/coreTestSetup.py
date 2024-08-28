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
   File:  coreTestInfo 
   Rev:   P1A01
   Date:  2009-11-12 
 
   Description: 
    
'''


###############################################################################
# Python common resources imports
###############################################################################
import os
import sys

###############################################################################
# FW imports
###############################################################################
from se.ericsson.jcat.omp.fw import OmpTestSetup
from org.apache.log4j import Logger
from org.apache.log4j import LogManager

from se.ericsson.jcat.fw import SUTHolder

import test_env.lib.lib as lib
import test_env.lib.tg_lib as tg_lib
import test_env.lib.comsa_lib as comsa_lib
import test_env.lib.utils as utils
import test_env.lib.trace_lib as trace_lib
import test_env.lib.trace_cc_lib as trace_cc_lib
import test_env.lib.campaign_lib as campaign_lib
import test_env.lib.pm_lib as pm_lib
import test_env.lib.amfmeas_lib as amfmeas_lib



class CoreTestSetup(OmpTestSetup):

    def __init__(self, test, logLevel):
        OmpTestSetup.__init__(self, test)
        self.logger = Logger.getLogger(self.__class__)
        self.logLevel = logLevel
        
        try:
            import color_out as color_out
            color_out.tag_prints()
        except:
            pass
        
        
    def setUp(self):
        OmpTestSetup.setUp(self)
        currentSut = SUTHolder.getInstance().zones[0]
        
        lib.setUp(self.logLevel, currentSut)
        tg_lib.setUp(self.logLevel, currentSut)
        comsa_lib.setUp(self.logLevel, currentSut)
        utils.setUp(self.logLevel, currentSut)
        trace_lib.setUp(self.logLevel, currentSut)
        campaign_lib.setUp(self.logLevel, currentSut)
        pm_lib.setUp(self.logLevel, currentSut)
        amfmeas_lib.setUp(self.logLevel, currentSut)


            
    def tearDown(self):
       
        lib.tearDown()
        tg_lib.tearDown()
        comsa_lib.tearDown()
        utils.tearDown()
        trace_lib.tearDown()
        

        OmpTestSetup.tearDown(self)

