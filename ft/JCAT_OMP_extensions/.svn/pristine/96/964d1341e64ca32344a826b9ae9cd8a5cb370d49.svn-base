#!/usr/bin/env python
#coding=iso-8859-1
###############################################################################
#
# Ericsson AB 2006 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson, the receiver of this
# document shall keep the information contained herein confidential and shall protect
# the same in whole or in part from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################


'''File information:
   ===================================================
   %CCaseFile:    main.py %
   %CCaseRev:    /main/R1B/11 % 
   %CCaseDate:    2006-12-05 % 

   Description:
   This module Contains hw independent functions.
   
'''

import time
import sys, os
import re
#import pysnmp
from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System

########NODE CONFIGURATION DATA##########
import omp.target.target_data as target_data

#########COMMON USED RESOURCES##########
import ssh_lib as ssh_lib
import misc_lib as misc_lib

#############GLOBALS##################
pHandles = {}
lineNumber = 0 

#############################################################################################
# setUp / tearDown
#############################################################################################

def setUp():
    
    # Removed to work for RDA since we dont use test_config
    #global testConfig
    #testConfig = st_env_lib.getConfig() 

    global logString 
    global confFile
    global mibDirs
    global mibs
    global trapd_FD

    global logger
    global logLevel
    logger = Logger.getLogger('snmp_lib')
    logLevel = System.getProperty("jcat.logging")
    logger.setLevel(Level.toLevel(logLevel))

    logString = "%04y-%02m-%02l %02h:%02j:%02k %b %w %v\n"
    #confFile = os.path.join( os.environ['TEST_ROOT'], 'st/config/snmptrapd.conf')
    #mibDirs = os.path.join( os.environ['TEST_ROOT'], 'common/MIBS')
    mibs = 'ALL'
    trapd_FD = None

    logger.debug("snmp_lib: Initiating!")
    #Changed by RDA to only use imported target_data name
    snmpVersion = target_data.data['snmp']['version'] 
    community = 'public'

    ipAddress = 'primary_sc'
    instantiate('opensaf', ipAddress, snmpVersion, community)
    #Changed by RDA to only use imported target_data name
    community =target_data.data['snmp']['community']

    # TODO - Update to count switches from target_data, with any name, not just switch_x
    caughtE = 0
    switch = 0
    while caughtE == 0:
        switch = switch + 1
        try:
            ipAddress = eval("target_data.data['ipAddress']['switches']['switch_%d']" % switch)
            instantiate(('switch_%d' % switch), ipAddress, snmpVersion, community)
            logger.debug('Instantiate switch %d' % switch)
        except Exception, e:
            logger.debug('No more switches found for this cluster')
            caughtE = 1

    return

def tearDown():
    if trapd_FD:
        trapd_FD.close()

    pHandles = {} # erase all handles
    logger.debug("snmp_lib: Bye, bye!")
    return

#############################################################################################
# SNMP lib functions - called by user
#############################################################################################
def instantiate(target, ipAddress, snmpVersion, snmpCommunity ):

    global pHandles
    try:
        pHandles[target] = cSNMP(ipAddress, snmpVersion, snmpCommunity)
    except :
        logger.error('SNMP Handle to: ' + target + ' could not be created')
        return ('ERROR','SNMP Handle to: ' + target + ' could not be created')
    logger.debug('SNMP Handle to: ' + target + ' created')
    return ('SUCCESS','SNMP Handle to: ' + target + ' created')


def snmpGet(target, command, printOut = '-Oqv'):

    global pHandles
    if (pHandles.has_key(target)==True):
        result = pHandles[target].get(command, printOut)
        if (re.search("Timeout: No Response",result[1])):
            logger.error('Timeout: No response from: ' + target)
            return ('ERROR', result[1], command)
        logger.debug("snmpget successfully executed")
        return result
    else:
        logger.error(' No handle to: ' + target + ' exists')
        return ('ERROR',' No handle to: ' + target + ' exists')

def snmpSet(target, command, printOut = '-Oqv'):

    global pHandles
    if (pHandles.has_key(target)==True):
        result = pHandles[target].set(command, printOut)
        if (re.search("Timeout: No Response",result[1])):
            logger.error('Timeout: No response from: ' + target)
            return ('ERROR', result[1], command)
        logger.debug("snmpset successfully executed")
        return result
    else:
    #Eget
        logger.error('!No handle to: ' + target + ' exists')
        return ('ERROR',' No handle to: ' + target + ' exists')

def snmpWalk(target, command, printOut = '-Oqv'):

    global pHandles
    if (pHandles.has_key(target)==True): 
        result = pHandles[target].walk(command, printOut)
        if (re.search("Timeout: No Response",result[1])):
            logger.error('Timeout: No response from: ' + target)
            return ('ERROR', result[1], command)
        logger.debug("snmpset successfully executed")
        return result
    else:
        logger.error('No handle to: ' + target + ' exists')
        #Removed by RDA since we dont use st_env_lib
        #st_env_lib.updateActiveController()
        return ('ERROR',' No handle to: ' + target + ' exists')


#############################################################################################
# SNMP classes - implements linux executable commands
#############################################################################################

class cSNMP(object):

    def __init__(self, ipAddress, snmpVersion, snmpCommunity):
        self.Destination =ipAddress
        self.Community = snmpCommunity
        self.Version = snmpVersion
        self.cSnmpLogger = Logger.getLogger('cSnmp')
        logLevel = System.getProperty("jcat.logging")
        self.cSnmpLogger.setLevel(Level.toLevel(logLevel))

    def get(self, command, printOut):

        self.cSnmpLogger.debug("snmpget: %s issued!" % command)
        command = "snmpget %s -c %s %s %s %s" %  (self.Version,
                                                   self.Community,
                                                   printOut,
                                                   self.Destination,
                                                   command)
        if (self.Destination != 'primary_sc'):
            result = misc_lib.execCommand(command)
            r=result[0]
        else:
            result = ssh_lib.sendCommand(command)
            if result[1].find('Cannot find module') != -1: # if the ssh login before MIB environment data is set
                ssh_lib.tearDownHandles() # fix because we dont know which handle used,
                r='ERROR'
            else:
                r=result[0]
        self.cSnmpLogger.debug("Response: %s" % result[1])
        result = [r,result[1],command]
        return result

    def set(self, command, printOut):

        self.cSnmpLogger.info("snmpset: %s issued!" % command)
        command = "snmpset %s -c %s %s %s %s" %  (self.Version,
                                                   self.Community,
                                                   printOut,
                                                   self.Destination,
                                                   command)
        if (self.Destination != 'primary_sc'): 
            result = misc_lib.execCommand(command)
        else:
            result = ssh_lib.sendCommand(command)
        self.cSnmpLogger.debug("Response: %s" % result[1])
        result = [result[0],result[1],command]
        return result

    def walk(self, command, printOut):
        self.cSnmpLogger.info("snmpwalk: %s issued!" % command)
        command = "snmpwalk %s -c %s %s %s %s" %  (self.Version,
                                                    self.Community,
                                                    printOut,
                                                    self.Destination,
                                                    command)
        if (self.Destination != 'primary_sc'): 
            result = misc_lib.execCommand(command)
        else:
            result = ssh_lib.sendCommand(command)
        self.cSnmpLogger.debug("Response: %s" % result[1])
        result = [result[0],result[1],command]
        return result

#############################################################################################
# SNMPdaemon implements trap daemon handling
#############################################################################################
def startDaemon(trapPort, logDirectory):

    global logString 
    global confFile
    global mibDirs 
    global mibs
    global logFile
    global trapd_FD

    

    logFile = logDirectory+"traps.log"
    logger.info("Start SNMP Trap daemon")
    #eolnans: Added for Jython
    #if (os.access(logFile, os.F_OK)): #remove file if exists
    #    os.remove(logFile)
    try:
        os.remove(logFile)
    except:
        pass
    
    command = "snmptrapd -c %s -F \"%s\" -M %s -m %s -Lf %s udp:%s" % (
        confFile, logString, mibDirs, mibs, logFile, trapPort )
    result = misc_lib.execCommand(command)
    result = [result[0],result[1],command]
    return result

def stopDaemon():
    command = "pkill snmptrapd"
    logger.info("SNMPTRAPD: %s" % (command))
    result = misc_lib.execCommand(command)
    result = [result[0],result[1],command]
    return result

def readTraps():

    global trapd_FD
    global logFile 
    global lineNumber
    traps = []
    try:
        trapd_FD = open(logFile, 'r')
        traps = trapd_FD.readlines()
        traps.pop(0) # remove the header in the trap file
        trapd_FD.close()
    except Exception, e:
        return ('ERROR', e) 
    newTraps = traps[lineNumber:]
    lineNumber = len(traps)
    logger.debug('Traps received:\n %s ' % newTraps)
    return ('SUCCESS', newTraps) 

#############################################################################################
# Moved temporarily here from lib to work in RDA auto environment.
#############################################################################################
def execCommand(command):
    
    logger.info("Executing linux command: %s" % command)
    output = []
    child_stdin, child_stdout, child_stderr = os.popen3(command)

    stdoutString = child_stdout.read()
    stderrString = child_stderr.read()
    child_stdin.close()
    child_stdout.close()
    child_stderr.close()

    if stderrString != "":
        logger.error("Error: Linux command result: %s" % stderrString.strip())
        return ("ERROR", stderrString)
    logger.info("Linux command result: %s" % stderrString.strip())
    return ("SUCCESS", stdoutString)

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print "Can not run stand alone at the moment"


