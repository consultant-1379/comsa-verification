#!/usr/bin/env python
#coding=iso-8859-1
###############################################################################
#
# © Ericsson AB 2006 All rights reserved.
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
   %CCaseFile:  loggert_lib.py %
   %CCaseRev:   /main/R1A/1 % 
   %CCaseDate:  2008-02-06 % 

   Description:
   This module handles all the logging for the System Test environment.

   The module creates logger objects and writes to a logfile using the logging filehandler class.
   One file is created and used per module/lib except for testcase files which ends up in the same file.

   The call to any lib function will instantiate a handle if required. Users should only use the libfunctions and the class is seen
   assert a private utility for the lib.

'''

import logging
import datetime
import re
import inspect
import sys
import string
from os.path import abspath, basename

########NODE CONFIGURATION DATA##########

#########COMMON USED RESOURCES##########
#This means Jython
if sys.platform[:4] == 'java':
    from _logger_lib_impl_j import cLOGGER

else:
     from _logger_lib_impl_c import cLOGGER

#############GLOBALS##################
pLoggers = {}    # dictionary containing handles to each logger created
logDir ='' # log directory 
level = '' # log level
logfile = '' # log file
file = '' # current logger
regexps={}
###############################################################################
# setUp / tearDown
###############################################################################

def setUp(logLevel, logDirectory):
    """This function fetches required data that this library requires to work"""
    global logDir
    global level
    global logfile

    tcFileList = []
    logfile = 'events.log'
    global regexps
    level = logLevel
    logDir = logDirectory
    regexps = {'.py':re.compile('.py'),
         '^tc_':re.compile('^tc_'),
         'tc_':re.compile('tc_')}
    logMessage("logger_lib: Initiating!", logLevel='debug')
    return

def tearDown():
    """This function removes the handles created during test executing"""
    tearDownFileHandlers()
    logMessage("logger_lib: Bye bye !!", logLevel='debug')
    return

###############################################################################
#Lib methods
###############################################################################
def setLogFile(logFile):
    global logfile
    global logDir
    global file
    file = string.lower(logFile)
    logfile = logDir+file+'.log'

def logMessage(message, logLevel = 'info'):
    """This function will write the log message to a file using the logging module. If no handle are associated 
    with the logging module a new log file handle are created."""

    global pLoggers
    global level
    global logfile
    global file
    global regexps

    stack = getStack()
    caller = stack[1][1]
    filePath = abspath(stack[1][1])
    lineNo = stack[1][2]

    caller = caller.split('/')[-1:]
    caller = regexps['.py'].sub("", caller[0])

    if file == caller  or re.search('safUnitTestCase' , caller):       
        printConsole = True
        printLog = True
    elif file == '': #Excuting functions 
        printConsole = True
        printLog = False        
    else:      
        printConsole = False
        printLog = True

    if (pLoggers.has_key(file) == False): #handle already exists?
        pLoggers[file] = cLOGGER(file, logfile, level)

    pLoggers[file].log(message, filePath, lineNo, printConsole, printLog, logLevel)
    return message

def getStack():
    """
    This gets the part of the stack we need, no nothing more
    """
    returnStack = []
    startFrame = inspect.currentframe()
    maxStackDepthTrav=3
    frame = startFrame
    
    while maxStackDepthTrav and frame.f_back:
        #We want to discard the first frame, since it belongs to this helper function
        frame = frame.f_back
        #A context=0 means we won't dig into the originating files
        #This is the proper way, it's even faster to dig out the info from the frame object manually
        returnStack.append((frame,)+inspect.getframeinfo(frame, 0) )
        maxStackDepthTrav -= 1

    #for frame in stack:
    #    if frame and None not in frame:
    #        returnStack.append(frame)
    return returnStack

def enter():
    """This function will write the enter message, ('caller') >>> 'enter' where 'caller' are the calling module
    and 'enter' are the function being called, to the log file . If no handle are associated 
    with the logging module a new log file handle are created."""

    global regexps

    stack = getStack()
    caller = stack[1][1]
    filePath = abspath(stack[1][1])
    lineNo = stack[1][2]
    method = stack[1][3]
    caller_method = stack[2][3]

    caller = caller.split('/')[-1:]
    caller = regexps['.py'].sub("", caller[0])

    message  = '(%s.%s) >>> %s' % (caller ,caller_method, method)
    logLevel = 'debug'
    return logMessage(message, logLevel)

def leave():
    """This function will write the leave message, ('caller') <<< 'enter' where 'caller' are the calling module
    and 'enter' are the function being called, to the log file . If no handle are associated 
    with the logging module a new log file handle are created."""

    global regexps

    stack = getStack()
    caller = stack[1][1]
    filePath = abspath(stack[1][1])
    lineNo = stack[1][2]
    method = stack[1][3]
    caller_method = stack[2][3]

    caller = caller.split('/')[-1:]
    caller = regexps['.py'].sub("", caller[0])
    message  = '(%s.%s)  <<< %s' % (caller, caller_method, method)
    logLevel = 'debug'
    return logMessage(message, logLevel)

def testCaseEnter(testCaseEnter, filePath, lineNo, current , event, instance ,logLevel='info'):

    global pLoggers
    printConsole=False
    printLog=True
    pLoggers[current].log(">>>>>>>>>>>>>> %s Instance %d <<<<<<<<<<<<<<" % (event, instance), filePath, lineNo, printConsole, printLog, logLevel='info')
    return         

def tearDownFileHandlers():
    """This function will remove all the handles created."""

    global pLoggers
    loggers=pLoggers.keys()

    for log in loggers :
        try:
            pLoggers[log].Close()
            del pLoggers[log]
        except :
             return ('ERROR','Handles could not be removed')
    return ('SUCCESS', 'Handles removed')

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    #import common.target.target_data as target_data
    #import common.target.common_lib.booking_lib as booking_lib
    import common.target.common_lib.st_env_lib as st_env_lib
    #node=booking_lib.checkBooking()
    #targetData=target_data.setTargetHwData(node)    
    st_env_lib.executeFunction(sys.argv)
    setUp('debug', '/tmp/test')
    ###########TEST AREA START###############

    enter()
    logMessage('test')
    leave()
    ###########TEST AREA END###############
    tearDown()






