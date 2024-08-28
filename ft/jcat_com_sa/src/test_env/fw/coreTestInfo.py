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
from se.ericsson.jcat.fw.utils import TestInfo
from org.apache.log4j import Logger

class CoreTestInfo(TestInfo):

    def __init__(self):
        TestInfo.__init__(self)
        self.logger = Logger.getLogger(self.__class__)





