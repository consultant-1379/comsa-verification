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


   Author: erapeik

   Description:

'''

from org.apache.log4j import Logger
from java.lang import System
import string
import lib
import shutil
import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException
import re


import omp.tf.ssh_lib as ssh_lib
import omp.tf.misc_lib as misc_lib
import coremw.notification_lib as notification_lib
import coremw.saf_lib as saf_lib

def setUp(logLevel, currentSut):
   
    global ssh_lib
    global misc_lib
    global logger
    global targetData

    logger = Logger.getLogger('amfmeas_lib')
    logger.setLevel(logLevel)
    logger.info("amfmeas_lib: Initiating!")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    return


def clearStateLog(testConfig, nodes = [(0, 0)], redModel = 'all'):
    '''
    resets the amfMeasureApp log files.

    Arguments:
    int(subrack), int(slot), str(redModel)

    Returns:
    ('SUCCESS',[]) or
    ('ERROR', Failed to clear log files on node(s) [(<subrack><slot>),...])
    
    NOTE:
    slot and subrack have the default value 0, means all nodes
    reset of specific log file is not implemented.
     
    Dependencies:
    ssh_lib, target_data

    '''
    
    logger.info('enter clearStateLog')
    
    nodes.sort()
    subrack = nodes[0][0]
    slot = nodes[0][1]
    
    accResult = []
    errorFlag = False
    if slot == 0 and subrack == 0:
        for subrack, slot in testConfig['testNodes']:
            cmd = '/opt/AMFMEASURE/bin/resetlog.sh; echo $?'
            result = ssh_lib.sendCommand(cmd,subrack, slot)
            if result[0] == 'ERROR' or result[1] != '0':
                accResult.append[(subrack,slot)]
                errorFlag = True
    else:
        for subrack, slot in nodes:
            cmd = '/opt/AMFMEASURE/bin/resetlog.sh; echo $?'
            result = ssh_lib.sendCommand(cmd,subrack, slot)
            if result[0] == 'ERROR' or result[1] != '0':
                accResult.append[(subrack,slot)]
                errorFlag = True
            
    if errorFlag:
        result = ('ERROR',accResult)
    else:
        result = ('SUCCESS',[])
                
       
    logger.info('leave clearStateLog')
    
    return result


def readStateLog(testConfig, hostNameList, nodes = [(0, 0)], redModel = 'all'):
    '''
    read the amfMeasureApp log files.

    Arguments:
    int(subrack), int(slot), str(redModel)

    Returns:
    ('SUCCESS',[]) or
    ('ERROR', Failed to read log files on node(s) [(<subrack><slot>),...])
    
    NOTE:
    slot and subrack have the default value 0, means all nodes.
    read of specific node log file is not implemented.
     
    Dependencies:
    ssh_lib, target_data

    '''
    
    logger.info('enter readStateLog')

    logfiles = {'SC-1' : ['NoRed-#.log','2N-#.log', 'NWayActive-#.log'],
                 'SC-2' : ['2N-#.log', 'NWayActive-#.log'],
                 'PL-3' : ['NoRed-#.log','2N-#.log', 'NWayActive-#.log'],
                 'PL-4' : ['2N-#.log', 'NWayActive-#.log'],
                 'PL-x' : ['NWayActive-#.log']}

    amfMeasAppStates = {'SC-1' : {'NoRed' : [], '2N' : [], 'NWayActive' : []},
                        'SC-2' : {'2N' : [], 'NWayActive' : []},
                        'PL-3' : {'NoRed' : [], '2N' : [], 'NWayActive' : []},
                        'PL-4' : {'2N' : [], 'NWayActive' : []}}
    
    nodes.sort()
    subrack = nodes[0][0]
    slot = nodes[0][1]
    
                #'PL-x' : {'NWayActive' : []}}
    #### FIXA, behövs inte 4 if satser
    pathToAmfMeasLog = '/home/test/amfMeasureApp/'             
    accResult = []
    try:
        if slot == 0 and subrack == 0:
            for subrack, slot in testConfig['testNodes']:
                hostname = hostNameList[slot - 1]
                if slot < 5:
                    if slot < 3:
                        keyName = 'SC-%s' % slot
                    else:
                        keyName = 'PL-%s' % slot                 
                    for i, redModel in enumerate(amfMeasAppStates[keyName]):
                        logFileName = '%s-%s.log' % (redModel, hostname)
                        cmd = 'cat %s%s' % (pathToAmfMeasLog, logFileName)
                        result = ssh_lib.sendCommand(cmd,subrack, slot)
                        temp = result[1].split('\n')
                        amfMeasAppStates[keyName][redModel] = temp
                else:
                    cmd = 'cat %sNWayActive-%s.log' % (pathToAmfMeasLog, hostname)
                    result = ssh_lib.sendCommand(cmd,subrack, slot)
                    temp = result[1].split('\n')
                    temp = {'NWayActive' : temp}
                    nodeName = 'PL-%s' % slot
                    amfMeasAppStates[nodeName]= temp
        else:
            for subrack, slot in nodes:
                hostname = hostNameList[slot - 1]
                if slot < 5:
                    if slot < 3:
                        keyName = 'SC-%s' % slot
                    else:
                        keyName = 'PL-%s' % slot                 
                    for i, redModel in enumerate(amfMeasAppStates[keyName]):
                        logFileName = '%s-%s.log' % (redModel, hostname)
                        cmd = 'cat %s%s' % (pathToAmfMeasLog, logFileName)
                        result = ssh_lib.sendCommand(cmd,subrack, slot)
                        temp = result[1].split('\n')
                        amfMeasAppStates[keyName][redModel] = temp
                else:
                    cmd = 'cat %sNWayActive-%s.log' % (pathToAmfMeasLog, hostname)
                    result = ssh_lib.sendCommand(cmd,subrack, slot)
                    temp = result[1].split('\n')
                    temp = {'NWayActive' : temp}
                    nodeName = 'PL-%s' % slot
                    amfMeasAppStates[nodeName]= temp
            
    except:
        return ('ERROR', 'Failed to read amfMeasureApp log files')
                
    
    logger.info('leave readStateLog')
    
    return ('SUCCESS',amfMeasAppStates)



#def getNodeRestartTime(testConfig, hostNameList, subrack = 0, slot = 0):
def getNodeRestartTime(amfMeasAppStates, subrack = 0, slot = 0):

    '''
    get the node(s) restart time by reading the log for amfMeasApp NWayActive.
    

    Arguments:
    dict(testConfig) list(hostNameList) int(subrack), int(slot)

    Returns:
    ('SUCCESS',dict(restartTimes)) or
    ('ERROR', 'Failed to read amfMeasureApp log files')
    
    NOTE:
    slot and subrack have the default value 0, means all nodes.
     
    Dependencies:
    ssh_lib, target_data

    '''
    
    logger.info('enter getNodeRestartTime')
    
    
    restartTimes = {}
    okFlag = False
    #result  = readStateLog(testConfig, hostNameList)
    #if result[0] == 'SUCCESS':
    #    amfMeasAppStates = result[1]
    if slot == 0 and subrack == 0:
        for key in amfMeasAppStates:
            if len(amfMeasAppStates[key]['NWayActive']) == 5:
                if re.search('Removed by callback',amfMeasAppStates[key]['NWayActive'][1]) and re.search('Active',amfMeasAppStates[key]['NWayActive'][4]):
                    temp = amfMeasAppStates[key]['NWayActive'][1]
                    temp = temp.split('\t')
                    stopTime = temp[0]
                    temp = amfMeasAppStates[key]['NWayActive'][4]
                    temp = temp.split('\t')
                    startTime = temp[0]
                    restartTime =  round(float(startTime) - float(stopTime))
                    restartTimes[key] = restartTime
                    okFlag = True
                    #result = ('SUCCESS',restartTimes)

            else:
                logger.error('Not enough data for calculating the restart time for: %s' % key)
                restartTimes[key] = 'Not enough data'
                result = ('ERROR',restartTimes)
    else:
        if slot < 3 :
            key = 'SC-%s' % slot
        else:
            key = 'PL-%s' % slot
            
        if len(amfMeasAppStates[key]['NWayActive']) == 5:
            if re.search('Removed by callback',amfMeasAppStates[key]['NWayActive'][1]) and re.search('Active',amfMeasAppStates[key]['NWayActive'][4]):
                temp = amfMeasAppStates[key]['NWayActive'][1]
                temp = temp.split('\t')
                stopTime = temp[0]
                temp = amfMeasAppStates[key]['NWayActive'][4]
                temp = temp.split('\t')
                startTime = temp[0]
                restartTime =  round(float(startTime) - float(stopTime))
                restartTimes[key] = restartTime
                okFlag = True
                #result = ('SUCCESS',restartTimes)
    
        else:
             logger.error('Not enough data for calculating the restart time for: %s' % key)
             restartTimes[key] = 'Not enough data'
             result = ('ERROR',restartTimes)
                 
    if okFlag == True:
        nodes = []
        nodeTypes = ''
        startTimes = []
        for key in restartTimes:
            nodes.append(key)
        nodes.sort() #PL is before SC
        nodes.reverse() # we want to have SC first
        if len(nodes) < 3: # max 2 nodes cluster or single node restart?
            for node in nodes:
                startTimes.append(restartTimes[node]) # get the restart times for 1 node or cluster > 3 nodes
        else:
            nodes.reverse()# ok, PL nodes first
            nodes.pop() # We have SC's and least one PL, we only want min&max start time for the PL's
            nodes.pop()
            for node in nodes:
               startTimes.append(restartTimes[node])
                
        minStartTime = min(startTimes)
        maxStartTime = max(startTimes)
        
        result = ('SUCCESS',restartTimes,minStartTime,maxStartTime,amfMeasAppStates)
             

             
    logger.info('leave getNodeRestartTime')
    
    return result

def getNodeStartTime(amfMeasAppStates, subrack = 0, slot = 0):
    '''
    get the node(s) start time by reading the log for amfMeasApp NWayActive.
    

    Arguments:
    dict(testConfig) list(hostNameList) int(subrack), int(slot)

    Returns:
    ('SUCCESS',dict(restartTimes)) or
    ('ERROR', 'Failed to read amfMeasureApp log files')
    
    NOTE:
    slot and subrack have the default value 0, means all nodes.
     
    Dependencies:
    ssh_lib, target_data

    '''
    
    logger.info('enter getNodeStartTime')
    
    
    startTimes = {}
    okFlag = False
    #result  = readStateLog(testConfig, hostNameList)
    #if result[0] == 'SUCCESS':
    #amfMeasAppStates = result[1]
    if slot == 0 and subrack == 0:
        for key in amfMeasAppStates:
            if len(amfMeasAppStates[key]['NWayActive']) == 2:
                if re.search('Active',amfMeasAppStates[key]['NWayActive'][1]):
                    temp = amfMeasAppStates[key]['NWayActive'][1]
                    temp = temp.split('\t')
                    startTime = temp[0]
                    startTimes[key] = round(float(startTime))
                    okFlag = True
            else:
                logger.error('Not enough data for calculating the restart time for: %s' % key)
                startTimes[key] = 'Not enough data'
                result = ('ERROR',startTimes)
    else:
        if slot < 3 :
            key = 'SC-%s' % slot
        else:
            key = 'PL-%s' % slot
            
        if len(amfMeasAppStates[key]['NWayActive']) == 2 and amfMeasAppStates[key]['NWayActive'] != ['']:
            if re.search('Active',amfMeasAppStates[key]['NWayActive'][1]):
                temp = amfMeasAppStates[key]['NWayActive'][1]
                temp = temp.split('\t')
                startTime = temp[0]
                startTimes[key] = round(float(startTime))
                okFlag = True        
        else:
             logger.error('Not enough data for calculating the restart time for: %s' % key)
             startTimes[key] = 'Not enough data'
             result = ('ERROR',startTimes)
                 
    if okFlag == True:
        nodes = []
        nodeTypes = ''
        nodeStartTimes = []
        for key in startTimes:
            nodes.append(key)
        nodes.sort() #PL is before SC
        nodes.reverse()  # we want to have SC first
        if len(nodes) < 3:# max 2 nodes cluster or single node restart
            for node in nodes:
                nodeStartTimes.append(startTimes[node])# get the restart times for 1 node or cluster > 3 nodes
        else:
            nodes.reverse()# ok, PL nodes first
            nodes.pop()# We have SC's and least one PL, we only want min&max start time for the PL's
            nodes.pop()
            for node in nodes:
                nodeStartTimes.append(startTimes[node])
                
        minStartTime = min(nodeStartTimes)
        maxStartTime = max(nodeStartTimes)
        result = ('SUCCESS',startTimes,minStartTime,maxStartTime,amfMeasAppStates)        

             
    logger.info('leave getNodeStartTime')
    
    return result


def getCompFailoverTime(amfMeasAppStates, compType = ''):
    '''
    get the node(s) restart time by reading the log for amfMeasApp NWayActive.
    

    Arguments:
    dict(testConfig) list(hostNameList) str(compType <SC or PL>)

    Returns:
    ('SUCCESS',?????) or
    ('ERROR', '?????')
    
    NOTE:
    the function clearStateLog shall be executed before this function is called
     
    Dependencies:
    ssh_lib, target_data

    '''
    
    logger.info('enter getNodeRestartTime')
    
    failoverTime = 0.000
    key1 = ''
    key2 = ''
    if compType == 'sc' or compType == 'SC':
        key1 = 'SC-1'
        key2 = 'SC-2'
    else: 
        key1 = 'PL-3'
        key2 = 'PL-4'
        
    #result  = readStateLog(testConfig, hostNameList)       
    #if result[0] == 'SUCCESS':
        #amfMeasAppStates = result[1]
    if re.search('Terminated by signal',amfMeasAppStates[key1]['2N'][0])  and re.search('Active',amfMeasAppStates[key2]['2N'][0]):
        temp = amfMeasAppStates[key1]['2N'][0]
        temp = temp.split('\t')
        fromTime = temp[0]
        temp = amfMeasAppStates[key2]['2N'][0]
        temp = temp.split('\t')
        toTime = temp[0]
        failoverTime =  float(toTime) - float(fromTime)
        result = 'SUCCESS',failoverTime
    elif re.search('Terminated by signal',amfMeasAppStates[key2]['2N'][0])  and re.search('Active',amfMeasAppStates[key1]['2N'][0]):
        temp = amfMeasAppStates[key2]['2N'][0]
        temp = temp.split('\t')
        fromTime = temp[0]
        temp = amfMeasAppStates[key1]['2N'][0]
        temp = temp.split('\t')
        toTime = temp[0]
        failoverTime =  float(toTime) - float(fromTime)
        result = 'SUCCESS',failoverTime
    else:
         logger.error('Not enough data for calculating the failover time between:  2N-%s and  2N-%s' %( key1,key2))
         failoverTime = 'Not enough data'
         result = 'ERROR',failoverTime
   
           
    logger.info('leave getNodeRestartTime')
    
    return result



def getsuFailoverTime(amfMeasAppStates, suType = ''):
    '''
    get the node(s) restart time by reading the log for amfMeasApp NWayActive.
    

    Arguments:
    dict(testConfig) list(hostNameList) str(suType <SC or PL>)

    Returns:
    ('SUCCESS',?????) or
    ('ERROR', '?????')
    
    NOTE:
    the function clearStateLog shall be executed before this function is called
     
    Dependencies:
    ssh_lib, target_data

    '''
    
    logger.info('enter getsuFailoverTime')
    
    failoverTime = 0.000
    key1 = ''
    key2 = ''
    if suType == 'sc' or suType == 'SC':
        key1 = 'SC-1'
        key2 = 'SC-2'
    else: 
        key1 = 'PL-3'
        key2 = 'PL-4'
        
    #result  = readStateLog(testConfig, hostNameList)       
    #if result[0] == 'SUCCESS':
        #amfMeasAppStates = result[1]
    if re.search('Active\(1\) -> Quiesced\(3\)',amfMeasAppStates[key1]['2N'][1])  and re.search('Standby\(2\) -> Active\(1\)',amfMeasAppStates[key2]['2N'][1]):
        temp = amfMeasAppStates[key1]['2N'][1]
        temp = temp.split('\t')
        fromTime = temp[0]
        temp = amfMeasAppStates[key2]['2N'][1]
        temp = temp.split('\t')
        toTime = temp[0]
        failoverTime =  float(toTime) - float(fromTime)
        result = 'SUCCESS',failoverTime
    elif re.search('Active\(1\) -> Quiesced\(3\)',amfMeasAppStates[key2]['2N'][1])  and re.search('Standby\(2\) -> Active\(1\)',amfMeasAppStates[key1]['2N'][1]):
        temp = amfMeasAppStates[key2]['2N'][1]
        temp = temp.split('\t')
        fromTime = temp[0]
        temp = amfMeasAppStates[key1]['2N'][1]
        temp = temp.split('\t')
        toTime = temp[0]
        failoverTime =  float(toTime) - float(fromTime)
        result = 'SUCCESS',failoverTime
    else:
         logger.error('Not enough data for calculating the su failover time between:  2N-%s and  2N-%s' %( key1,key2))
         failoverTime = 'Not enough data'
         result = 'ERROR',failoverTime
   
           
    logger.info('leave getsuFailoverTime')
    
    return result
 
 
def trigCompFailover(compType):
    '''
    get the node(s) restart time by reading the log for amfMeasApp NWayActive.
    

    Arguments:
    dict(testConfig) list(hostNameList) str(compType <sc|SC or pl|PL>)

    Returns:
    ('SUCCESS',?????) or
    ('ERROR', '?????')
    
    NOTE:
    the function clearStateLog shall be executed before this function is called
     
    Dependencies:
    ssh_lib, target_data
    '''
    
    logger.debug('enter trigCompFailover') 
    
    result = getActiveHaStateForAmfMeas2NComp(compType)
    slot = result[1]
    cmd = 'pgrep -f "amfMeasureApp instantiate 2N"'
    result = ssh_lib.sendCommand(cmd, 2, slot)
    pid = result[1]
    cmd = 'kill -15 %s' % pid
    result = ssh_lib.sendCommand(cmd, 2, slot)
    
    misc_lib.waitTime(20)
    logger.info('leave trigCompFailover')

    return ('SUCCESS', 'jadajda')


def getActiveHaStateForAmfMeas2NComp(compType = ''):
    

    comp1 = ''
    comp2 = ''
    ActSu = ''
    slot = 0
    
    if compType == 'SC':
        comp1 = 'SC-1'
        comp2 = 'SC-2'
    else:
        comp1 = 'PL-3'
        comp2 = 'PL-4'
    
    siName =   'safSi=%s2N,safApp=AmfMeasureApp' % compType
    cmd = 'cmw-status -v siass  | grep -A1  safSi=%s2N,safApp=AmfMeasureApp' % compType
    result = ssh_lib.sendCommand(cmd )
    if result[0] == 'ERROR' or result[1] == '':
        logger.error('incomplete outcome from cmd: %s outcome: %s' % (cmd, result[1]))
    else:
        siList = result[1].split('--')
        if re.search('HAState=ACTIVE',siList[0]):
            if re.search('safSu=%s' % comp1,siList[0]):
                ActSu = 'safSu=%s,safSg=%s2N,safApp=AmfMeasureApp' % (comp1,compType)
                slot = int(comp1.split('-')[1])
            else:
                 ActSu = 'safSu=%s,safSg=%s2N,safApp=AmfMeasureApp' % (comp2,compType)
                 slot = int(comp2.split('-')[1])
        else:
            if re.search('safSu=%s' % comp1,siList[1]):
                 ActSu = 'safSu=%s,safSg=%s2N,safApp=AmfMeasureApp' % (comp1,compType)
                 slot = int(comp1.split('-')[1])
            else:
                 ActSu = 'safSu=%s,safSg=%s2N,safApp=AmfMeasureApp' % (comp2,compType)
                 slot = int(comp2.split('-')[1])
                
    return ('SUCCESS',slot, ActSu, siName)


def prettyPrintOfamfMeasAppStates(amfMeasAppStates):
    '''
    writes the amfMeasureApp states to the test log in a readable way.

    Arguments:
    dict(amfMeasAppStates)

    Returns:
    ('SUCCESS','')
     
    Dependencies:
    None
    '''
    
    logger.debug('enter prettyPrintOfamfMeasAppStates')
    
    for key in amfMeasAppStates:
        logger.info('\t%s' % key)
        for subKey in amfMeasAppStates[key]:
            logger.info('\t\t%s' % subKey)
            for elem in  amfMeasAppStates[key][subKey]:
                logger.info('\t\t\t%s' % elem)   
    
    logger.debug('leave  prettyPrintOfamfMeasAppStates')

    

if __name__ == '__main__':
    print 'main'
