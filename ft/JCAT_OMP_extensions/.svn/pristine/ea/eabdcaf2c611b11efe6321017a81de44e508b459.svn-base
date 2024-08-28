#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2011 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained
# herein confidential and shall protect the same in whole or in part
# from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################

'''File information:
   ===================================================
   %CCaseFile:  smartedge_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2008-11-18 %

   Author:
   XTSRRPN 

   Description:
   Based on ethswitch_lib.py.
   This module handles the SmartEdge Router for the System Test by using of SNMP.
   It handle read out of data from the router, like if the port is up or down.
   It handle control to make a port open or closed for communication.
'''

import string
import os
import inspect
import sys
import time
import re
import getopt

import snmp_lib as snmp_lib

import omp.tf.ssh_lib as ssh_lib
import omp.target.target_data as target_data

from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System
    
#############GLOBALS##################


##############################################################################
# setUp / tearDown
##############################################################################
def setUp():
    global targetData
    global portList
    
    global logger
    global logLevel
    logger = Logger.getLogger('smartedge_lib')
    logLevel = System.getProperty("jcat.logging")
    logger.setLevel(Level.toLevel(logLevel))
    
    targetData=target_data.getTargetHwData()
    portList = targetData['ipAddress']['routers']['portsInOrder']
        
    caughtE = 0
    router = 0
    while caughtE == 0:
        router = router + 1
        try:
            ipAddress = eval("target_data.data['ipAddress']['routers']['ro-0%d']" % router)
            snmp_lib.instantiate(('ro-0%d' % router), ipAddress, snmpVersion, community)
            logger.debug('Instantiate router %d' % router)
        except Exception, e:
            logger.debug('No more routers found for this cluster')
            caughtE = 1
            
    logger.debug("smartedge_lib: Initiating!")
    return

def tearDown():
    logger.debug("smartedge_lib: Bye bye !!")
    return

##############################################################################
# Functions
##############################################################################
def portDown(router, port):

    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    result = ['ERROR','','']
    logger.debug("portDown(%s,%u)" %(router,port))
    result = setIfAdminStatus(router, port, 2)
    return result

def portUp(router, port):
    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    result = ['ERROR','','']
    logger.debug("portUp(%s,%u)" %(router,port))
    result = setIfAdminStatus(router, port, 1)
    return result

def getIfAdminStatus(router,PortNumber):
    "Returns the SNMP MIB 'ifAdminStatus' of a specific port"
    
    result = snmp_lib.snmpGet(router,"ifAdminStatus.%s" % (PortNumber))
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result

def setIfAdminStatus(router,PortNumber,Value):
    "Set the SNMP MIB 'ifAdminStatus' of a specific port."
    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    logger.debug("setIfAdminStatus(%s,%u,%u)"%(router,int(PortNumber),int(Value)))
    if (portList.count(PortNumber) == 0):
        errorStr = "Not allowed to change state for invalid port %u" % (PortNumber)
        logger.error(errorStr)
        result = (['ERROR',errorStr])
    else:
        result = snmp_lib.snmpSet(router,"ifAdminStatus.%s i %s" % (PortNumber,Value))
        result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    
    return result

def getIfName(router,PortNumber):
    "Returns the if name of a specific interface"

    result = snmp_lib.snmpGet(router,"ifName.%s" % (PortNumber))
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result

###########################################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print "Can not run stand alone at the moment"       
