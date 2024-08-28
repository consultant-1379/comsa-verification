#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2007 All rights reserved.
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
   %CCaseFile:  ethswitch_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2008-11-18 %

   Author:
   EAB/FTI/SD Ulf Olofsson (ETXULFO)

   Description:
   This module handle the Ethernet Switch for the System Test by using of SNMP.
   It handle read out of data from the switch, like if the port is up or down.
   It handle to control to make a port open or closed for communication.
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
    logger = Logger.getLogger('ethswitch_lib')
    logLevel = System.getProperty("jcat.logging")
    logger.setLevel(Level.toLevel(logLevel))
    
    targetData=target_data.getTargetHwData()
    portList = targetData['ipAddress']['switches']['portsInOrder']
        
    logger.debug("ethswitch_lib: Initiating!")
    return

def tearDown():
    logger.debug("ethswitch_lib: Bye bye !!")
    return

##############################################################################
# Functions
##############################################################################
def portDown(switch, port):

    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    #caller = inspect.stack()[1][1]
    #caller = caller.split('/')[-1:]
    #caller = re.sub(".py","", caller[0])
    #caller_method = inspect.stack()[1][3]
    result = ['ERROR','','']
    logger.debug("portDown(%s,%s)" %(switch,port))
    result = setIfAdminStatus(switch, port, 2)
    return result

def portUp(switch, port):
    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    #caller = inspect.stack()[1][1]
    #caller = caller.split('/')[-1:]
    #caller = re.sub(".py","", caller[0])
    #caller_method = inspect.stack()[1][3]
    result = ['ERROR','','']
    logger.debug("portUp(%s,%s)" %(switch,port))
    result = setIfAdminStatus(switch, port, 1)
    return result

def checkAndFixAllPortToDown(switch):
    "This function secures that all ports is in a 'Down' state. Except the mangagement port."
    "This function accidentally brings down the inter-switch link (ISL) in the right order"
    "since it is last in a sequence ranging from 1 and up, ISL is port 23. Be cautious when"
    "bringing the switch back up."

    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    #caller = inspect.stack()[1][1]
    #caller = caller.split('/')[-1:]
    #caller = re.sub(".py","", caller[0])
    #caller_method = inspect.stack()[1][3]
    #logger.error("[%s.%s] checkAndFixAllPortToDown(%s)"\
    #                      % (caller,caller_method,switch))

    result = []
    for port in portList:
        result = snmp_lib.snmpGet(switch,"ifAdminStatus.%s" % (port))
        result[1] = result[1].replace("\n","")
        if (result[1] != "down"):
            result = portDown(switch,port)
            if (result[1].replace("\n","") != "down"):
                logger.error("Problem to fix Port %s to 'down' state!"%(port))
                result = ("ERROR","Port %s not working" % (port))
        if (result[0] != "SUCCESS"):
            logger.error("All port is NOT working properly")
            result = ("ERROR","All port is NOT working properly")
    return result

def checkAndFixAllPortToUp(switch):
    "This function secures that all ports is in an 'Up' state. Except the mangagement port"
    "which is skipped and left in an untouched state."
    "When bringing the switch back up again the inter-switch link must be brought back before"
    "the links to the nodes, otherwise the cluster will end up in a bad state. This is stupidly"
    "solved by simply reversing the order the ports are brought up"

    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    #caller = inspect.stack()[1][1]
    #caller = caller.split('/')[-1:]
    #caller = re.sub(".py","", caller[0])
    #caller_method = inspect.stack()[1][3]
    #logger.debug("[%s.%s] checkAndFixAllPortToUp(%s)"\
    #                      % (caller,caller_method,switch))
    result = []
    # for port in reversed(portList):	
    # python 2.2 Work around for the above: We reverse the list, use it in for loop and then rereverse.
    portList.reverse()	
    for port in portList:
        result = snmp_lib.snmpGet(switch,"ifAdminStatus.%s" % (port))
        result[1] = result[1].replace("\n","")
        if (result[1] != "up"):
            result = portUp(switch,port)
            if (result[1].replace("\n","") != "up"):
                logger.error("Problem to fix Port %s to 'up' state!" %(port))
                result = ("ERROR","Port %s not working" % (port))
        if (result[0] != "SUCCESS"):
            logger.error("All port is NOT working properly")
            result = ("ERROR","All port is NOT working properly")
    portList.reverse()	# new line added as part of workaround (rereverse)
    
    return result


def checkAndFixAllListedPortsToUp(switch,ports):
    "This function secures that all ports is in an 'Up' state. Except the mangagement port"
    "which is skipped and left in an untouched state."
    "When bringing the switch back up again the inter-switch link must be brought back before"
    "the links to the nodes, otherwise the cluster will end up in a bad state. This is stupidly"
    "solved by simply reversing the order the ports are brought up"

    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    #caller = inspect.stack()[1][1]
    #caller = caller.split('/')[-1:]
    #caller = re.sub(".py","", caller[0])
    #caller_method = inspect.stack()[1][3]
    #logger.debug("[%s.%s] checkAndFixAllPortToUp(%s)"\
    #                      % (caller,caller_method,switch))
    result = []
    # for port in reversed(ports):	
    # python 2.2 Work around for the above: We reverse the list, use it in for loop and then rereverse.
    ports.reverse()	
    for port in ports:
        result = snmp_lib.snmpGet(switch,"ifAdminStatus.%s" % (port))
        result[1] = result[1].replace("\n","")
        if (result[1] != "up"):
            result = portUp(switch,port)
            if (result[1].replace("\n","") != "up"):
                logger.error("Problem to fix Port %s to 'up' state!"%(port))    
                result = ("ERROR","Port %s not working" % (port))
        if (result[0] != "SUCCESS"):
            logger.error("All port is NOT working properly")
            result = ("ERROR","All port is NOT working properly")
    ports.reverse()	# new line added as part of workaround (rereverse)
    
    return result

def checkAndFixAllListedPortsToDown(switch,ports):
    "This function secures that all ports is in a 'Down' state. Except the mangagement port."
    "This function accidentally brings down the inter-switch link (ISL) in the right order"
    "since it is last in a sequence ranging from 1 and up, ISL is port 23. Be cautious when"
    "bringing the switch back up."

    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    #caller = inspect.stack()[1][1]
    #caller = caller.split('/')[-1:]
    #caller = re.sub(".py","", caller[0])
    #caller_method = inspect.stack()[1][3]
    #logger.debug("[%s.%s] checkAndFixAllListedPortsToDown(%s)"\
    #                      % (caller,caller_method,switch))
    result = []
    for port in ports:
        result = snmp_lib.snmpGet(switch,"ifAdminStatus.%s" % (port))
        result[1] = result[1].replace("\n","")
        if (result[1] != "down"):
            result = portDown(switch,port)
            if (result[1].replace("\n","") != "down"):
                
                logger.error("Problem to fix Port %s to 'down' state!"%(port))
                result = ("ERROR","Port %s not working" % (port))
        if (result[0] != "SUCCESS"):
            logger.error("All port is NOT working properly")
            result = ("ERROR","All port is NOT working properly")
    
    return result


def getListIfUpOperStatus(switch):
    "Return information of which port that are operational in 'Up' state."

    
    LIST1 = []
    LIST2 = []
    LISTA = snmp_lib.snmpWalk(switch,"ifIndex")
    if (LISTA[0] != "SUCCESS"):
        logger.error("Error while collecting data via SNMP command!")
        return ["ERROR","getListIfUpOperStatus: Error while collecting data via SNMP command!"]
    LISTA = LISTA[1].splitlines()
    LISTB = snmp_lib.snmpWalk(switch,"ifOperStatus")
    if LISTB[0] != "SUCCESS":
        logger.error("Error while collecting data via SNMP command!")
        return ["ERROR","getListIfUpOperStatus: Error while collecting data via SNMP command!"]
    LISTB = LISTB[1].splitlines()
    for port in portList:
        idx = LISTA.index(str(port))
        if (LISTB[idx] == "up"):
            LIST1.append(LISTA[idx])
            LIST2.append(LISTB[idx])
    
    return ["SUCCESS",LIST1,LIST2]


def getListIfUpAdminStatus(switch):
    "Return information of which port that are operational and active in 'Up' state."
    
    LIST1 = []
    LIST2 = []
    LISTA = snmp_lib.snmpWalk(switch,"ifIndex")
    if LISTA[0] != "SUCCESS":
        logger.error("Error while collecting data via SNMP command!")
        return ["ERROR","getListIfUpAdminStatus: Error while collecting data via SNMP command!"]
    LISTA = LISTA[1].splitlines()
    LISTB = snmp_lib.snmpWalk(switch,"ifAdminStatus")
    if LISTB[0] != "SUCCESS":
        logger.error("Error while collecting data via SNMP command!")
        return ["ERROR","getListIfUpAdminStatus: Error while collecting data via SNMP command!"]
    LISTB = LISTB[1].splitlines()
    for port in portList:
        idx = LISTA.index(str(port))
        if (LISTB[idx] == "up"):
            LIST1.append(LISTA[idx])
            LIST2.append(LISTB[idx])
    
    return ["SUCCESS",LIST1,LIST2]



def getListIfNotUpOperStatus(switch):
    "Return information of which port that are NOT operational in 'Up' state."
    
    LIST1 = []
    LIST2 = []
    LISTA = snmp_lib.snmpWalk(switch,"ifIndex")
    if LISTA[0] != "SUCCESS":
        logger.error("Error while collecting data via SNMP command!")
        return ["ERROR","getListIfNotUpOperStatus: Error while collecting data via SNMP command!"]
    LISTA = LISTA[1].splitlines()
    LISTB = snmp_lib.snmpWalk(switch,"ifOperStatus")
    if LISTB[0] != "SUCCESS":
        logger.error("Error while collecting data via SNMP command!")
        return ["ERROR","getListIfNotUpOperStatus: Error while collecting data via SNMP command!"]
    LISTB = LISTB[1].splitlines()
    for port in portList:
        idx = LISTA.index(str(port))
        if (LISTB[idx] != "up"):
            LIST1.append(LISTA[idx])
            LIST2.append(LISTB[idx])
    
    return ["SUCCESS",LIST1,LIST2]

def getListIfNotUpAdminStatus(switch):
    "Return information of which port that are operational and NOT active in 'Up' state."
    
    LIST1 = []
    LIST2 = []
    LISTA = snmp_lib.snmpWalk(switch,"ifIndex")
    if LISTA[0] != "SUCCESS":
        logger.error("getListIfNotUpAdminStatus: Error while collecting data via SNMP command!")
        return ["ERROR","getListIfNotUpAdminStatus: Error while collecting data via SNMP command!"]
    LISTA = LISTA[1].splitlines()
    LISTB = snmp_lib.snmpWalk(switch,"ifAdminStatus")
    if LISTB[0] != "SUCCESS":
        logger.error("getListIfNotUpAdminStatus: Error while collecting data via SNMP command!")
        return ["ERROR","getListIfNotUpAdminStatus: Error while collecting data via SNMP command!"]
    LISTB = LISTB[1].splitlines()
    for port in portList:
        idx = LISTA.index(str(port))
        if (LISTB[idx] != "up"):
            LIST1.append(LISTA[idx])
            LIST2.append(LISTB[idx])
    
    return ["SUCCESS",LIST1,LIST2]

###########################################################################################
def getListOutOctets(switch):
    "Return information per port with information of outgoing octets."
    
    LIST1 = []
    LIST2 = []
    LISTA = snmp_lib.snmpWalk(switch,"ifIndex")
    if LISTA[0] != "SUCCESS":
        logger.error("getListOutOctets: Error while collecting data via SNMP command!")
        return ["ERROR","getListOutOctets: Error while collecting data via SNMP command!"]
    LISTA = LISTA[1].splitlines()
    LISTB = snmp_lib.snmpWalk(switch,"ifOutOctets")
    if LISTB[0] != "SUCCESS":
        logger.error("getListOutOctets: Error while collecting data via SNMP command!")
        return ["ERROR","getListOutOctets: Error while collecting data via SNMP command!"]
    LISTB = LISTB[1].splitlines()
    for port in portList:
        idx = LISTA.index(str(port))
        if (int(LISTB[idx]) != 0):
            LIST1.append(LISTA[idx])
            LIST2.append(LISTB[idx])
    
    return ["SUCCESS",LIST1,LIST2]

def getListInOctets(switch):
    "Return information per port with information of incoming octets."

    
    LIST1 = []
    LIST2 = []
    LISTA = snmp_lib.snmpWalk(switch,"ifIndex")
    if LISTA[0] != "SUCCESS":
        logger.error("getListInOctets: Error while collecting data via SNMP command!")
        return ["ERROR","getListInOctets: Error while collecting data via SNMP command!"]
    LISTA = LISTA[1].splitlines()
    LISTB = snmp_lib.snmpWalk(switch,"ifInOctets")
    if LISTB[0] != "SUCCESS":
        logger.error("getListInOctets: Error while collecting data via SNMP command!")
        return ["ERROR","getListInOctets: Error while collecting data via SNMP command!"]
    LISTB = LISTB[1].splitlines()
    for port in portList:
        idx = LISTA.index(str(port))
        if (int(LISTB[idx]) != 0):
            LIST1.append(LISTA[idx])
            LIST2.append(LISTB[idx])
    
    return ["SUCCESS",LIST1,LIST2]

def getListIfType(switch):
    "Return information per port with information what interface type it is."
    
    LIST1 = []
    LIST2 = []
    LISTA = snmp_lib.snmpWalk(switch,"ifIndex")
    if LISTA[0] != "SUCCESS":
        logger.error("getListIfType: Error while collecting data via SNMP command!")
        return ["ERROR","getListInOctets: Error while collecting data via SNMP command!"]
    LISTA = LISTA[1].splitlines()
    LISTB = snmp_lib.snmpWalk(switch,"ifType")
    if LISTB[0] != "SUCCESS":
        logger.error("getListIfType: Error while collecting data via SNMP command!")
        return ["ERROR","getListInOctets: Error while collecting data via SNMP command!"]
    LISTB = LISTB[1].splitlines()
    for port in portList:
        idx = LISTA.index(str(port))
        LIST1.append(LISTA[idx])
        LIST2.append(LISTB[idx])
    
    return ["SUCCESS",LIST1,LIST2]

#####################################################################

def getEthSwSysDescr(switch):
    
    result = snmp_lib.snmpGet(switch,"sysDescr.0")
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result

def getEthSwSysUpTime(switch):
    
    result = snmp_lib.snmpGet(switch,"sysUpTime.0")
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result
    
def getEthSwSysName(switch):
    
    result = snmp_lib.snmpGet(switch,"sysName.0")
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result
    
def getEthSwSysContact(switch):
    
    result =snmp_lib.snmpGet(switch,"sysContact.0")
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result
    
def getEthSwSysLocation(switch):
    
    result = snmp_lib.snmpGet(switch,"sysLocation.0")
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result
    
def getIfAdminStatus(switch,PortNumber):
    "Returns the SNMP MIB 'ifAdminStatus' of a specific port"
    
    result = snmp_lib.snmpGet(switch,"ifAdminStatus.%s" % (PortNumber))
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result

def setIfAdminStatus(switch,PortNumber,Value):
    "Set the SNMP MIB 'ifAdminStatus' of a specific port. Not possible to set management port to 'Down'."
    
    filePath = inspect.stack()[1][1]
    lineNo = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    #caller = inspect.stack()[1][1]
    #caller = caller.split('/')[-1:]
    #caller = re.sub(".py","", caller[0])
    #caller_method = inspect.stack()[1][3]
    #logger.debug("[%s.%s] setIfAdminStatus(%s,%u,%u)"\
    #                      % (caller,caller_method,switch,int(PortNumber),int(Value)))
    logger.debug("setIfAdminStatus(%s,%u,%u)"%(switch,int(PortNumber),int(Value)))
    if (portList.count(PortNumber) == 0):
        errorStr = "Not allowed to change state for invalid port %s" % (PortNumber)
        logger.error(errorStr)
        result = (['ERROR',errorStr])
    else:
        result = snmp_lib.snmpSet(switch,"ifAdminStatus.%s i %s" % (PortNumber,Value))
        result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    
    return result

def getIfOperStatus(switch,PortNumber):
    "Returns the SNMP MIB 'ifOperStatus' of a specific port"
    
    result = snmp_lib.snmpGet(switch,"ifOperStatus.%s" % (PortNumber))
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result

####################################################################################
def getIfInOctets(switch,PortNumber):
    "Returns the SNMP MIB 'ifInOctets' of a specific port"
    
    result = snmp_lib.snmpGet(switch,"ifInOctets.%s" % (PortNumber))
    result = [result[0].replace("\n",""),result[1].replace("\n","")]
    return result


def getIfOutOctets(switch,PortNumber):
    "Returns the SNMP MIB 'ifOutOctets' of a specific port"
    
    result = snmp_lib.snmpGet(switch,"ifOutOctets.%s" % (PortNumber))
    result = [result[0].replace("\n",""),result[1].replace("\n",""),result[2].replace("\n","")]
    return result

###########################################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print "Can not run stand alone at the moment"       
