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
   %CCaseFile:  opensaf_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2007-08-10 %

   Author:
   EAB/FLJ/GSF

   Description:
   This module handle the SAF modules from OpenSAF etc.. by using of SNMP.
'''
import sys
import re
import time

########NODE CONFIGURATION DATA##########

#########COMMON USED RESOURCES##########
import lib as lib
import omp.tf.ssh_lib as ssh_lib
#import snmp_lib as snmp_lib
#import omp.tf.st_env_lib as st_env_lib
from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System

#############GLOBALS##################
config={} # a dictionary containing cluster specific information
amfCommandsSeparator = '_' #As of December 2009 the nodes names are described using _ as separator in node names
logger = None
##############################################################################
# setUp / tearDown
##############################################################################
def setUp():

    global config
    global logger
    logLevel = System.getProperty("jcat.logging")
    logger = Logger.getLogger('opensaf_lib logging')
    logger.setLevel(Level.toLevel(logLevel))
    logger.debug("opensaf_lib: Initiating!")
    return


def tearDown():
    logger.debug("opensaf_lib: Bye, bye!")
    return


##############################################################################
# Lib Methods
##############################################################################
'''
Removed by Turesson
def getTestAppHAState(): # This is not working in the CoreMW project
#EJNOLSZ: This is not going to work with CoreMw for the time being, if it will ever???
    logger.debug('enter getTestAppHAState')
    global config

    nodeTypes = config['testNodesTypes']
    resultFinal = ['SUCCESS',{}]

    for instance in config['TestAppEnabledBlades'].keys():    
        blades = config['TestAppEnabledBlades'][instance]
        for subrack,slot in blades:
            process = 'ta_tapp_%s' % instance
            idx = config['testNodes'].index((subrack,slot))
            types=config['testNodesTypes']
            blade = '%s_%s_%s' % (types[idx], subrack, slot)
            if not resultFinal[1].has_key(blade):
                resultFinal[1][blade] = {}
            resultFinal[1][blade][instance]= getServiceInstanceHaState(subrack,slot, process)[1]
        
    logger.debug('leave getTestAppHAState')        
    return resultFinal
'''
'''
Removed by Turesson
def getTestCoordHAState(): # This is not working in the CoreMW project
#EJNOLSZ: This is not going to work with CoreMw for the time being, if it will ever???
    logger.debug('enter getTestCoordHAState')
    global config

    nodeTypes = config['testNodesTypes']

    resultFinal = ['SUCCESS',{}]
    
    for instance in config['TestCoordEnabledBlades'].keys():    
        blades = config['TestCoordEnabledBlades'][instance]
        for subrack,slot in blades:
            process = 'ta_tgc_%s' % instance
            idx = config['testNodes'].index((subrack,slot))
            types=config['testNodesTypes']
            blade = '%s_%s_%s' % (types[idx], subrack, slot)
            if not resultFinal[1].has_key(blade):
                resultFinal[1][blade] = {}
            resultFinal[1][blade][instance]= getServiceInstanceHaState(subrack,slot, process)[1]
        
    logger.debug('leave getTestCoordHAState')        
    return resultFinal
'''
'''
Removed by Turesson
def getTestGenHAState(): # This is not working in the CoreMW project
#EJNOLSZ: This is not going to work with CoreMw for the time being, if it will ever???
    logger.debug('enter getTestGenHAState')
    global config

    blades = config['TestGenEnabledBlades']
    nodeTypes = config['testNodesTypes']

    resultFinal = ['SUCCESS',{}]
    
    for instance in config['TestGenEnabledBlades'].keys():    
        blades = config['TestGenEnabledBlades'][instance]
        for subrack,slot in blades:
            process = 'ta_tgen_%s' % instance
            idx = config['testNodes'].index((subrack,slot))
            types=config['testNodesTypes']
            blade = '%s_%s_%s' % (types[idx], subrack, slot)
            if not resultFinal[1].has_key(blade):
                resultFinal[1][blade] = {}
            resultFinal[1][blade][instance]= getServiceInstanceHaState(subrack,slot, process)[1]
        
    logger.debug('leave getTestGenHAState')        
    return resultFinal 
'''

# Deprecated this method is moved to saf_lib instead. Will be removed in the future. 
def getControllerState(subrack, slot):
    
    logger.debug('enter getControllerState')

    global config
    global amfCommandsSeparator

    amfNodeName = 'SC' + amfCommandsSeparator + str(subrack) + amfCommandsSeparator + str(slot)
    cmd = "amf-state su readi safSu=%s,safSg=2N,safApp=OpenSAF" %amfNodeName
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    lines = result[1].splitlines()[1]
    elements = lines.split('=')
    if len(elements) == 2 and 'saAmfSUReadinessState' in elements[0]:
        return ('SUCCESS', str(elements[1].split('(')[0]))
    else:
        logger.error(">>> failed to get %s readiness state." %amfNodeName)
        logger.debug('leave getControllerState')
        return ('ERROR', result[1])

'''
Removed by Turesson
def getControllerStateList(TupleList,TimeOutSeconds=0): # This is not working in the CoreMW project
# EJNOLSZ: This is not prioritized at the moment and will not work until we define a nice new testConfig like variable    
     
    logger.debug('enter getControllerStateList')
    startTryTime = int(time.time())
    if TimeOutSeconds == 0:
        countDownTime = 300 # Default value is set to 5 minutes.
    else:
        countDownTime = TimeOutSeconds
    stopTryTime = startTryTime + countDownTime
    Service = 0
    while ((int(time.time()) < stopTryTime) and (Service != len(TupleList))):
        ServiceCount = 0
        if (Service < 0):
            Service = 0
        for cnt in range(len(TupleList)):
            result = getControllerState(TupleList[cnt][0],TupleList[cnt][1])
            if result[1] == 'inService':
                ServiceCount = ServiceCount + 1
            else:
                ServiceCount = ServiceCount - 1
        Service = ServiceCount
    if (Service == len(TupleList)):
        logger.debug('leave getControllerStateList')
        return ['SUCCESS','inService']
    else:
        logger.debug('leave getControllerStateList')
        return ['ERROR','outOfService']
'''

# Deprecated this method is moved to saf_lib instead. Will be removed in the future. 
def getPayloadState(subrack, slot):
    logger.debug('enter getPayloadState')

    global config
    global amfCommandsSeparator

    amfNodeName = 'PL' + amfCommandsSeparator + str(subrack) + amfCommandsSeparator + str(slot)
    cmd = "amf-state su readi safSu=%s,safSg=NoRed,safApp=OpenSAF" %amfNodeName
    result = ssh_lib.sendCommand(cmd, 2, 1)
    lines = result[1].splitlines()[1]
    elements = lines.split('=')
    if len(elements) == 2 and 'saAmfSUReadinessState' in elements[0]:
        logger.debug('leave getPayloadState')
        return ('SUCCESS', str(elements[1].split('(')[0]))
    else:
        logger.error(">>> failed to get %s readiness state." %amfNodeName)
        logger.debug('leave getPayloadState')
        return ('ERROR', result[1])

'''
Removed by Turesson
def getPayloadStateList(TupleList,TimeOutSeconds=0): # This is not working in the CoreMW project
# EJNOLSZ: This is not prioritized at the moment and will not work until we define a nice new testConfig like variable    
    
    logger.debug('enter getPayloadStateList')
    startTryTime = int(time.time())
    if TimeOutSeconds == 0:
        countDownTime = 300 # Default value is set to 5 minutes.
    else:
        countDownTime = TimeOutSeconds
    stopTryTime = startTryTime + countDownTime
    Service = 0
    while ((int(time.time()) < stopTryTime) and (Service != len(TupleList))):
        ServiceCount = 0
        if (Service < 0):
            Service = 0
        for cnt in range(len(TupleList)):
            result = getPayloadState(TupleList[cnt][0],TupleList[cnt][1])
            if result[1] == 'inService':
                ServiceCount = ServiceCount + 1
            else:
                ServiceCount = ServiceCount - 1
        Service = ServiceCount
    if (Service == len(TupleList)):
        logger.debug('leave getPayloadStateList')
        return ['SUCCESS','inService']
    else:
        logger.debug('leave getPayloadStateList')
        return ['ERROR','outOfService']
'''

# Deprecated this method is moved to saf_lib instead. Will be removed in the future. 
def getServiceInstanceHaState(subrack, slot , serviceInstances):
    
# subrack and slot have to be integers
# serviceInstances has to be a list of strings
    logger.debug('enter getServiceInstanceHaState')

    global config
    global amfCommandsSeparator

    varType=type(serviceInstances)
    varType=str(varType)
    pattern = "list"
    serviceInstanceList = []
    if (re.search(pattern, varType)):  # is it a list or a scalar?
        serviceInstanceList = serviceInstances
    else:
        serviceInstanceList.append(serviceInstances)
    
    amfNodeIdentifier = str(subrack) + amfCommandsSeparator + str(slot)
    
    resultList = []    
    response = 'SUCCESS'
    
    for serviceInstance in serviceInstanceList:
        result = ssh_lib.sendCommand('amf-find csiass | grep -i %s | grep %s' %(serviceInstance, amfNodeIdentifier))
        lines = result[1].splitlines()
        if len(lines) != 1 :
            return ('ERROR', 'Ambiguous query, less or more than one match. \n%s' %result[1])
        DN = str(lines[0])
        cmd = "amf-state csiass ha '%s'" %DN
        result = ssh_lib.sendCommand(cmd)
        lines = result[1].splitlines()[1]
        elements = lines.split('=')
        if len(elements) == 2 and 'saAmfCSICompHAState' in elements[0]:
            haState = elements[1].split('(')[0]
            resultList.append(str(haState))            
        else:
            logger.error(">>> failed to get %s ha state." %serviceInstance)
            return ('ERROR', 'failed to get %s ha state' %serviceInstance)

    if len(resultList) ==1:
        resultList = resultList[0]
    logger.debug('leave getServiceInstanceHaState')
    return (response,resultList)

# Deprecated this method is moved to saf_lib instead. Will be removed in the future.   
def getRedPatternDNs(subrack, slot, appPatern = 'ta_', redundancyPattern = '2N'):
    logger.debug('enter get2NRedundantDNs')
    
    global amfCommandsSeparator
    amfNodeIdentifier = str(subrack) + amfCommandsSeparator + str(slot)
    
    result = ssh_lib.sendCommand('amf-find csiass | grep -i %s | grep %s | grep %s' %(amfNodeIdentifier, redundancyPattern, appPatern))
    if result[0] != 'SUCCESS':
        return result
    DNs = result[1].splitlines()
    if len(DNs) == 0:
        return('ERROR', 'No component with one plus one redundancy on the specified blade')
    else:
        return ('SUCCESS', DNs)
        
    logger.debug('leave get2NRedundantDNs')
 
# Deprecated this method is moved to saf_lib instead. Will be removed in the future.    
def returnDnForSearchPatterns(searchPatterns):
    '''
    searchPatterns has to be a list of patterns to look after in the DN
    the method returns all the DNs which contain all the specified patterns
    '''
    logger.debug('enter returnDnForSearchPatterns')
    
    varType = str(type(searchPatterns))
    if 'str' or 'unicode' in varType:
        searchPattern = [searchPatterns]
    elif 'list' in varType:
        searchPattern = searchPatterns
    else: 
        return('ERROR', 'Unsupported variable type specified as search pattern')
    
#build up the grep command
    grepCommand = 'amf-find csiass'
    for i in range(len(searchPattern)):
        grepCommand = grepCommand + ' | grep %s' %searchPattern[i]
    
    result = ssh_lib.sendCommand(grepCommand)
    if result[0] != 'SUCCESS':
        return result
    DNs = result[1].splitlines()
    if len(DNs) == 0:
        return('ERROR', 'No distinguished names found with the specified search patterns.')
    else:
        return ('SUCCESS', DNs)
    
    logger.debug('leave returnDnForSearchPatterns')
    
# Deprecated this method is moved to saf_lib instead. Will be removed in the future.     
def getCompOpState(subrack, slot , comp):
# subrack and slot have to be integers
# comp has to be a list of strings
    logger.debug('enter getCompOpState')

    global config
    global amfCommandsSeparator

    varType=type(comp)
    varType=str(varType)
    pattern = "list"
    compList = []
    if (re.search(pattern, varType)):  # is it a list or a scalar?
        compList = comp
    else:
        compList.append(comp)

    response = 'SUCCESS'
    resultList = []

    amfNodeIdentifier = str(subrack) + amfCommandsSeparator + str(slot)

    for comp in compList:
        result = ssh_lib.sendCommand('amf-find comp | grep -i %s | grep %s' %(comp, amfNodeIdentifier))
        lines = result[1].splitlines()
        if len(lines) != 1 :
            return ('ERROR', 'Ambiguous query, less or more than one match for %s. \n%s' %(comp, result[1]))
        DN = str(lines[0])
        cmd = "amf-state comp oper '%s'" %DN
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        lines = result[1].splitlines()[1]
        elements = lines.split('=')
        if len(elements) == 2 and 'saAmfCompOperState' in elements[0]:
            operState = elements[1].split('(')[0]
            resultList.append(str(operState))
        else:
            logger.error(">>> failed to get %s operational state." %comp)
            return ('ERROR', 'failed to get %s operational state' %comp)

    if len(resultList) ==1:
        resultList = resultList[0]
    logger.debug('leave getCompOpState')
    return (response,resultList)

# Deprecated this method is moved to saf_lib instead. Will be removed in the future.
def getAllCompState():

    logger.debug('enter getAllCompState')
  
    compStates = ['oper','pres','readi']
    compStatesTranls = ['operational','presence','readiness']
    allCompStates = {'operational' : [], 'presence' : [], 'readiness' : []}
    totCheckFlag = True

    result = ssh_lib.sendCommand('export IMMA_TRACE_PATHNAME=/tmp/imm.trace')#this line is a workaround, should be removed when IMM is more stable
    for k, state in enumerate(compStates):
        cmd = 'amf-state comp %s' % state
        okFlag = False
       
        for i in range(10):
       
            result = ssh_lib.sendCommand(cmd)
            if not re.search('MDS:ERR',result[1]): #någon mer check av returvärde när amf-state funktionen funkar som den ska
                okFlag = True
                break
            else:
                logger.warn('Failed to get %s state for all saf components, try %s' % (compStatesTranls[k],i))       
     
        if okFlag:
            lines = result[1].splitlines()
            temp = []
            for i in lines:
                j = i.strip()
                temp.append(j)
            compStates = []
            listLength = len(temp)
            for i in range(0,listLength,2):
                tempStr = temp[i] + ':' + temp[i + 1]
                allCompStates[compStatesTranls[k]].append(tempStr)
        else:
            logger.error('Failed to get %s state for all saf components, tried 10 times' % compStatesTranls[k])
            totCheckFlag = False

        
            
    if totCheckFlag :
        logger.debug('get states for all saf components succeeded')
        result = ('SUCCESS',allCompStates)
    else:
        logger.error('Failed to get states for all saf components')
        result = ('ERROR',allCompStates)
        
    
    logger.debug('enter getAllCompState')
    
    return result


# Deprecated this method is moved to saf_lib instead. Will be removed in the future.
def getSuReadinessState(subrack, slot , serviceUnit):
# subrack and slot have to be integers
# serviceUnit has to be a list of strings
    logger.debug('enter getSuReadinessState')

    global config
    global amfCommandsSeparator

    varType=type(serviceUnit)
    varType=str(varType)
    pattern = "list"
    serviceUnitList = []
    if (re.search(pattern, varType)):  # is it a list or a scalar?
        serviceUnitList = serviceUnit
    else:
        serviceUnitList.append(serviceUnit)

    response = 'SUCCESS'
    resultList = []
    
    amfNodeIdentifier = str(subrack) + amfCommandsSeparator + str(slot)

    for serviceUnit in serviceUnitList:
        cmd = 'amf-find su | grep %s | grep %s' %(amfNodeIdentifier, serviceUnit)
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        lines = result[1].splitlines()
        if len(lines) != 1 :
            return ('ERROR', 'Ambiguous query, less or more than one match for %s. \n%s' %(serviceUnit, result[1]))
        DN = str(lines[0])
    
        cmd = 'amf-state su readi %s' %DN
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        lines = result[1].splitlines()[1]
        elements = lines.split('=')
        if len(elements) == 2 and 'saAmfSUReadinessState' in elements[0]:
            suReadiState = str(elements[1].split('(')[0])
            return('SUCCESS', suReadiState)
        else:
            logger.error(">>> failed to get %s Su radiness state." %serviceUnit)
            logger.debug('leave getSuReadinessState')
            return ('ERROR', 'failed to get %s Su readiness state' %serviceUnit)
    

# Deprecated this method is moved to saf_lib instead. Will be removed in the future.    
def getCompReadiState(subrack, slot , comp):    
# subrack and slot have to be integers
# comp has to be a list of strings
    logger.debug('enter getCompReadiState')

    global config
    global amfCommandsSeparator

    varType=type(comp)
    varType=str(varType)
    pattern = "list"
    compList = []
    if (re.search(pattern, varType)):  # is it a list or a scalar?
        compList = comp
    else:
        compList.append(comp)

    response = 'SUCCESS'
    resultList = []

    amfNodeIdentifier = str(subrack) + amfCommandsSeparator + str(slot)

    for comp in compList:
        result = ssh_lib.sendCommand('amf-find comp | grep -i %s | grep %s' %(comp, amfNodeIdentifier))
        lines = result[1].splitlines()
        if len(lines) != 1 :
            return ('ERROR', 'Ambiguous query, less or more than one match for %s. \n%s' %(comp, result[1]))
        DN = str(lines[0])
        cmd = "amf-state comp readi '%s'" %DN
        result = ssh_lib.sendCommand(cmd, subrack, slot)
        lines = result[1].splitlines()[1]
        elements = lines.split('=')
        if len(elements) == 2 and 'saAmfCompReadinessState' in elements[0]:
            readiState = elements[1].split('(')[0]
            resultList.append(str(readiState))
        else:
            logger.error(">>> failed to get %s readiness state." %comp)
            return ('ERROR', 'failed to get %s readiness state' %comp)

    if len(resultList) ==1:
        resultList = resultList[0]
    logger.debug('leave getCompReadiState')
    return (response,resultList)

# Deprecated this method is moved to saf_lib instead. Will be removed in the future.    
def getControllerHAState(subrack, slot):
    
    logger.debug('enter getControllerHAState')

    global config
    global amfCommandsSeparator

    amfNodeName = 'SC' + amfCommandsSeparator + str(subrack) + amfCommandsSeparator + str(slot)
    cmd = "amf-state csiass ha 'safCSIComp=safComp=CPD\,safSu=%s\,safSg=2N\,safApp=OpenSAF,safCsi=CPD,safSi=SC-2N,safApp=OpenSAF'" %amfNodeName
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    lines = result[1].splitlines()[1]
    elements = lines.split('=')
    if len(elements) == 2 and 'saAmfCSICompHAState' in elements[0]:
        return ('SUCCESS', str(elements[1].split('(')[0]))
    else:
        logger.error(">>> failed to get %s ha state." %amfNodeName)
        logger.debug('leave getControllerHAState')
        return ('ERROR', result[1])

'''
Remove by Turesson
def getSuRestartCount(subrack, slot , serviceUnit): # This is not working in the CoreMW proj
    logger.debug('enter getSuRestartCount')
    global config

    idx = config['testNodes'].index((subrack,slot))
    types=config['testNodesTypes']
    blade = '%s_%s_%s' % (types[idx], subrack, slot)

    cmd = 'NCS-AVSV-MIB::ncsSSUCompRestartCount.\\\"safSu=%s,safNode=%s\\\"' % (serviceUnit, blade)
    result, counter, c = get(cmd)
    if result =='SUCCESS' :
        logger_lib.leave()
        return (result, counter)
    else:
        logger.error("Failed to get restart count for %s on %s."\
                                                     % (serviceUnit, blade)) 
        logger.debug('leave getSuRestartCount')
        return ('ERROR', counter)
'''

'''
Removed by Turesson
def switchOverController ():
    logger.debug('enter switchOverController')
    cmd = 'NCS-AVM-MIB::ncsAvmAdmSwitch.0 = 1'
    result, response, cmd  = set(cmd)
    if result[0] == 'SUCCESS' :
        st_env_lib.switchActCtrlBlade()
    logger.debug('leave switchOverController')
    return (result, response)

def getSysDescr():
    logger.debug('enter getSysDescr')
    result = get("sysDescr.0")
    logger.debug('leave getSysDescr')
    return result

def getSysName():
    logger.debug('enter getSysName')
    result = get("sysName.0")
    logger.debug('leave getSysName')
    return result

def getSysUpTime():
    logger.debug('enter getSysUpTime')
    result = get("sysUpTime.0")
    logger.debug('leave getSysUpTime')
    return result

def getSysContact():
    logger.debug('enter getSysContact')
    result = get("sysContact.0")
    logger.debug('leave getSysContact')
    return result

def getSysLocation():
    logger.debug('enter getSysLocation')
    result =get("sysLocation.0")
    logger.debug('leave getSysLocation')
    return result

def setSysContact(string):
    logger.debug('enter setSysContact')
    result = set("sysContact.0 %s") % (string)
    logger.debug('leave setSysContact')
    return result

def setSaAmfAgentSpecVersion():
    logger.debug('enter setSaAmfAgentSpecVersion')
    result = set("saAmfAgentSpecVersion.0")
    logger.debug('leave setSaAmfAgentSpecVersion')
    return result

def getSaAmfAgentVendor():
    logger.debug('enter getSaAmfAgentVendor')
    result = get("saAmfAgentVendor.0")
    logger.debug('leave getSaAmfAgentVendor')
    return result

def getSaAmfAgentVendorProductRev():
    result = get("saAmfAgentVendorProductRev.0")
    return result

def getNcsAvmEntNodeNsetUp():
    logger.debug('enter getNcsAvmEntNodeNsetUp')
    result = walk("ncsAvmEntNodeName")
    result0 = result[0]
    result1 = result[1].splitlines()
    resultsvar = result0,result1
    logger.debug('leave getNcsAvmEntNodeNsetUp')
    return resultsvar

def getSaAmfNodeAdminState(node):
    logger.debug('enter getSaAmfNodeAdminState')
    """saAmfNodeAdminState."safNode=SC_2_1"  Input string example SC_2_1"""
    DoCommand = 'saAmfNodeAdminState.\\\"safNode=%s\\\"' % (node)
    result = get(DoCommand)
    logger.debug('leave getSaAmfNodeAdminState')
    return result

def getSafAmfCompCapabilityModel():
    logger.debug('enter getSafAmfCompCapabilityModel')
    result = get("safAmfCompCapabilityModel")
    logger.debug('leave getSafAmfCompCapabilityModel')
    return result

def getSaAmfAgentSpecVersion():
    logger.debug('enter getSaAmfAgentSpecVersion')
    result = get("saAmfAgentSpecVersion.0")
    logger.debug('leave getSaAmfAgentSpecVersion')
    return result

def getSaAmfServiceStartEnabled():
    logger.debug('enter getSaAmfServiceStartEnabled')
    result = get("saAmfServiceStartEnabled.0")
    logger.debug('leave getSaAmfServiceStartEnabled')
    return

def getSaAmfClusterStartupTimeout():
    logger.debug('enter getSaAmfClusterStartupTimeout')
    result =get("saAmfClusterStartupTimeout.0")
    logger.debug('leave getSaAmfClusterStartupTimeout')
    return

def getSaAmfNodeSuFailoverProb(node):
    logger.debug('enter getSaAmfNodeSuFailoverProb')
    """saAmfNodeSuFailoverProb."safNode=SC_2_1"  Input string example SC_2_1"""
    DoCommand = 'saAmfNodeSuFailoverProb.\\\"safNode=%s\\\"' % (node)
    result = get(DoCommand)
    logger.debug('leave getSaAmfNodeSuFailoverProb')
    return result

def getSaAmfNodeSuFailoverMax(node):
    logger.debug('enter getSaAmfNodeSuFailoverMax')
    """saAmfNodeSuFailoverMax."safNode=SC_2_1"  Input string example SC_2_1"""
    DoCommand = 'saAmfNodeSuFailoverMax.\\\"safNode=%s\\\"' % (node)
    result = get(DoCommand)
    logger.debug('leave getSaAmfNodeSuFailoverMax')
    return result

def getSaAmfNodeRowStatus(node):
    logger.debug('enter getSaAmfNodeRowStatus')
    """saAmfNodeRowStatus."safNode=SC_2_1"  Input string example SC_2_1"""
    DoCommand = 'saAmfNodeRowStatus.\\\"safNode=%s\\\"' % (node)
    result = get(DoCommand)
    logger.debug('leave getSaAmfNodeRowStatus')
    return result

def getSafCHKServiceStartEnabled():
    logger.debug('enter getSafCHKServiceStartEnabled')
    result =get("SAF-CHK-SVC-MIB::safServiceStartEnabled.0")
    logger.debug('leave getSafCHKServiceStartEnabled')
    return result

def getSafEVTServiceStartEnabled():
    logger.debug('enter getSafEVTServiceStartEnabled')
    result = get("SAF-EVENT-SVC-MIB::safServiceStartEnabled.0")
    logger.debug('leave getSafEVTServiceStartEnabled')
    return result

def getSafMSGServiceStartEnabled():
    logger.debug('enter getSafMSGServiceStartEnabled')
    result = get("SAF-MSG-SVC-MIB::safServiceStartEnabled.0")
    logger.debug('leave getSafMSGServiceStartEnabled')
    return result

def getSafLCKServiceStartEnabled():
    logger.debug('enter getSafLCKServiceStartEnabled')
    result =get("SAF-LCK-SVC-MIB::safServiceStartEnabled.0")
    logger.debug('leave getSafLCKServiceStartEnabled')
    return result

def getSafServiceStartEnabled(Service):
    logger.debug('enter getSafServiceStartEnabled')
    if (Service == "CHK"):
       result = get("SAF-CHK-SVC-MIB::safServiceStartEnabled.0")
    elif (Service == "EVT"):
       result =get("SAF-EVENT-SVC-MIB::safServiceStartEnabled.0")
    elif (Service == "MSG"):
       result = get("SAF-MSG-SVC-MIB::safServiceStartEnabled.0")
    elif (Service == "LCK"):
       result = get("SAF-LCK-SVC-MIB::safServiceStartEnabled.0")
    else:
       result = ("ERROR","Missing parameters...")
    logger.debug('leave getSafServiceStartEnabled')
    return result

def getSafCHKServiceState():
    logger.debug('enter getSafCHKServiceState')
    result = get("SAF-CHK-SVC-MIB::safServiceState.0")
    logger.debug('leave getSafCHKServiceState')
    return result

def getSafEVTServiceStatsetUp():
    logger.debug('enter getSafEVTServiceStatsetUp')
    result = get("SAF-EVENT-SVC-MIB::safServiceState.0")
    logger.debug('leave getSafEVTServiceStatsetUp')
    return result

def getSafMSGServiceState():
    logger.debug('enter getSafMSGServiceState')
    result = get("SAF-MSG-SVC-MIB::safServiceState.0")
    logger.debug('leave getSafMSGServiceState')
    return result

def getSafLCKServiceState():
    logger.debug('enter getSafLCKServiceState')
    result =get("SAF-LCK-SVC-MIB::safServiceState.0")
    logger.debug('leave getSafLCKServiceState')
    return result

def getSafServiceState(Service):
    logger.debug('enter getSafServiceState')
    if (Service == "CHK"):
        result = get("SAF-CHK-SVC-MIB::safServiceState.0")
    elif (Service == "EVT"):
        result = get("SAF-EVENT-SVC-MIB::safServiceState.0")
    elif (Service == "MSG"):
        result = get("SAF-MSG-SVC-MIB::safServiceState.0")
    elif (Service == "LCK"):
        result = get("SAF-LCK-SVC-MIB::safServiceState.0")
    else:
        result = ("ERROR","Missing parameters...")
    logger.debug('leave getSafServiceState')
    return result
'''



##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':

    print "Bye opensaf_lib __name__ == __main__"


