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
   %CCaseFile:  misc.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2007-11-01 %

   Author:
   
   Description:

'''



import os
import time

import omp.tf.ssh_lib as ssh_lib

from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System  
  
def setUp():

    global logger
    global logLevel
    logger = Logger.getLogger('misc_lib')
    logLevel = System.getProperty("jcat.logging")
    logger.setLevel(Level.toLevel(logLevel))

    logger.debug("misc_lib: Initiating!")
    return
    

def tearDown():
    logger.debug("misc_lib: Bye bye !!")
    return


def execCommand(command):
    '''
    Executes linux command
    
    Arguments:
    (str <linux command>)
        
    Returns:
    tuple('SUCCESS', stdoutString) or 
    tuple('ERROR', stderrString)
        
    NOTE:
    
    Dependencies:

    
    '''
    logger.info("Executing linux command: %s" % command)
    output = []
    child_stdin, child_stdout, child_stderr = os.popen3(command)

    stdoutString = child_stdout.read()
    stderrString = child_stderr.read()
    child_stdin.close()
    child_stdout.close()
    child_stderr.close()

    if stderrString != "":
        logger.error("Linux command result: %s" % stderrString.strip())
        return ("ERROR", stderrString)
    logger.info("Linux command result: %s" % stdoutString.strip())
    
    return ("SUCCESS", stdoutString)
    
   
def copyFilesToSystem(filePaths, destination):
    '''
    copy one or several files to the system.
    
    Arguments:
    for single copy
    (str <absolute file path>, str <absolute directory path>)
    for multi copy
    (list <absolute file path>, list <absolute directory path>)
        
    Returns:
    tuple('SUCCES','All file(s) copied to the system') or 
    tuple('ERROR', 'Copy file(s) failed')
        
    NOTE:
    
    Dependencies:
    ssh_lib
    
    '''
    
    
        
    fileList = []
    destList = []
    errorInfo = []
    result = ('SUCCESS', 'All file(s) copied to the system')
        
    if isinstance(filePaths, str):
        fileList.append(filePaths)
        destList.append(destination)
    else:  fileList, destList = filePaths, destination
    
    errorFlag = False    
    for i, filePath in enumerate(fileList):
        tempResult = ssh_lib.remoteCopy(filePath, destList[i])
        if tempResult != ('SUCCESS','File copied'):
            errorInfo.append(tempResult[1])
            errorFlag = True
            
    if errorFlag == True:       
        logger.error(errorInfo)
        result = ('ERROR','Copy file(s) failed')
    else:
        logger.debug('All file(s) copied to the system')
            
    
    return result       
            
        
def removeFilesFromSystem(filePaths):
    '''
    remove one or several files from the system.
    
    Arguments:
    for single remove
    (str <absolute file path>)
    for multi remove
    (list <absolute file path>)
        
    Returns:
    tuple('SUCCES','All file(s) removed from the system') or
    tuple('ERROR', 'Remove file(s) failed')
        
    NOTE:
    
    Dependencies:
    ssh_lib
    
    '''
        
    fileList = []
    errorInfo = []
    result = ('SUCCESS', 'All file(s) removed from the system')
       
    if isinstance(filePaths, str):
        fileList.append(filePaths)
    else:  fileList = filePaths
     
    errorFlag = False        
    for filePath in fileList:
        tempResult = ssh_lib.sendCommand('rm -vf %s' % filePath)
        compRes =  ('SUCCESS','removed `%s\'' % filePath)
        if tempResult != compRes:
            errorInfo.append(tempResult[1])
            errorFlag = True
    
    if errorFlag == True:       
        logger.error(errorInfo)
        result = ('ERROR','Remove file(s) failed')
    else:
        logger.debug('All file(s) removed from the system')
    return result


def getChecksum(fileName, subrack, slot):
    '''
    This method returns the checksum a file given as first argument on the target specified by subrack and slot.
    The fileName argument must also contain the full path the to the file.

    If subrack == 0 and slot == 0
    then the checksum will be executed on the local (linux) machine

    The method returns ('SUCCESS', 'checksum') or ('ERROR', 'error message')
    '''

    if (subrack == 0 and slot == 0): # local machine
        result = execCommand("cksum %s | awk '{print $1}'" %fileName)
        if result[0] == 'SUCCESS':
            return (result[0], result[1][:-1]) #this is because we have \n at the end of the string
        else:
            logger.error("Failed to execute cksum command on local machine.")
            return ('ERROR', result[1])
    else:
        result = ssh_lib.sendCommand("""cksum %s | awk '{print $1}'""" %fileName, subrack, slot)
        if result[0] == 'SUCCESS':
            return (result[0], result[1])
        else:
            logger.error("Failed to execute cksum command on local machine.")
            return ('ERROR', result[1])


def waitTime(sleep_time):
    '''
    Suspend execution for the given number of seconds.
    
    Arguments:
    int(sleep_time) -- sleep time in seconds
    
    Returns:
    int(sleep_time) -- the input parameter
        
    NOTE:
    
    '''
    
    

    timeSecA = float(time.mktime(time.localtime()))
    timePrnA = time.strftime("%H:%M:%S",time.localtime(float(timeSecA)))
    sleep_time = int(round(sleep_time))
    timeSecB = float(time.mktime(time.localtime(float(timeSecA) + float(sleep_time))))
    timePrnB = time.strftime("%H:%M:%S",time.localtime(float(timeSecB)))
    logger.debug('waitTime(%u), %s -> %s' % (sleep_time,timePrnA,timePrnB))

    time.sleep(sleep_time)

    return ('SUCCESS',sleep_time)


##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print "Can not run stand alone at the moment"

    


