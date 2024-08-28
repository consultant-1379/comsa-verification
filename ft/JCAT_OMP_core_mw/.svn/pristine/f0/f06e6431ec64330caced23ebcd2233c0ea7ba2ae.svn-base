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
 

   Author:
   
   Description:

'''



#import os
#import time


from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System
import omp.tf.ssh_lib as ssh_lib
import utils._ntf_utils_ as _ntf_utils_
#import omp.tf.utils._hw_utils_ as _hw_utils_ for some COM interface instead

#############GLOBALS##################
logger = None
pUtil = None  
######################################
  
def setUp():
    
    global logger
    global pUtil
    
    logLevel = System.getProperty("jcat.logging")
    logger = Logger.getLogger('notification_lib logging')
    logger.setLevel(Level.toLevel(logLevel))
    logger.info("notification_lib: Initiating!")

    
    

    """
    try:
        logger_lib.logMessage('Instaniating notification interface xxx')
        if notifInterface == 'com':
            pUtil = _com_utils_.Com()
        else:
            pUtil = _ntf_utils_.Ntf()
    except:
        logger_lib.logMessage('Failed to bla bla')
    """
    #hardcoded to day
    logger.info('Instaniating notification interface: NTF')
    
    pUtil = _ntf_utils_.Ntf()
    
    pUtil.setUp()
    
    return
    

def tearDown():
    logger.info("notification_lib: Bye bye !!")
    
    pUtil.tearDown()
    
    return


def storeNotifications():
    
    logger.debug('enter storeNotifications')
    
    result = pUtil._storeNotifications()
    
    logger.debug('leave storeNotifications')
    
    return result
    
    
def clearNotifications(nrOfSc = 2):
    '''
     clear all notifications.
        
    Arguments:
    (none)
    
    Returns:
    tuple('SUCCESS','clear all notifications succeeded') or
    tuple('ERROR', 'clear all notifications failed')   
    NOTE:
    
    Dependencies:
    _ntf_utils_ or _com_utils
    
    '''
        
    logger.debug('enter clearNotifications')
    
    
    logger.debug('clear all notifications')
    result = pUtil._clearNotifications(nrOfSc)
    logger.debug('leave clearNotifications')
    
    return result
    
    
def checkNotifications(expectedPatternList, ignoredPatternList, notifType, nrOfSC = 2):
    '''
    check the notifications, received from the system.
       
    Arguments:
    (list expectedPatternList, list ignoredPatternList)
       
    Returns:
    tuple('SUCCESS','no unexpected notifications/traps found') or
    tuple('ERROR', 'unexpected notifications/traps found')   
            
    NOTE:
        
    Dependencies:
    _ntf_utils_ or _com_utils_
       
    '''
    logger.debug('enter checkNotifications')
    return pUtil._checkNotifications(expectedPatternList, ignoredPatternList, notifType, nrOfSC )
    
    
def readAllNotifications(nrOfSC = 2):
    '''
    Get notifications direct from NTF or via COM as SNMP traps.
       
    Arguments:
    (none)
       
    Returns:
    tuple('SUCCESS','') or 
    tuple('ERROR', '')
            
    NOTE:
        
    Dependencies:
    _ntf_utils_ or _com_utils_
    
    '''   
    
    logger.debug('enter readAllNotifications')
    
    result = pUtil._readNotifications(nrOfSC)
    
    logger.debug('leave readAllNotifications')
    
    return result
    

def readNotification(bodyPattern = '', notifType = 'stateChangeNotifications', nrOfSC = 2):
    '''
    Get notifications.
    
    Arguments:
    (str <vendorId>, str <bodyPattern>, str <notifType>)
    
    Returns:
    tuple('SUCCESS', True, <heartBeatsRecieved>) or
    tuple('SUCCESS', False, <heartBeatsRecieved>)or
    tuple('ERROR', <notificationList>, <heartBeatsRecieved>)
        
    NOTE:
    Split this functions, 2 functions
    
    Dependencies:
    ntf_utils
    
    '''

    logger.debug('enter readNotification')
    
    result = pUtil._notificationReceived(bodyPattern, notifType, nrOfSC)
    if result[0] == 'SUCCESS':
        logger.debug('Notification(s) matching the search pattern found')
    else:
        logger.warn('Notification(s) matching the search pattern: %s not found' % bodyPattern)
        logger.debug(result[1])
   
    logger.debug('leave readNotification')
    return result

def getAttributeFromNotification(notification, element):
    '''
    Get the value assigned to an element (or parameter or variable or...).
    
    Arguments:
    (str <notification>, str <name of the element>)
    
    Returns:
    tuple('SUCCESS', ['value(s) of the element']) or
    tuple('ERROR', 'requested element not defined in notification')
        
    NOTE:
    
    Dependencies:
    -
    '''
        
    logger.debug('enter getAttributeFromNotification')
    logger.debug('Searching for the value of %s in a notification.' %element)
    matches = []
    lines = notification.splitlines()
    for i in range(len(lines)):
        fields = lines[i].split(" = ")
        if fields[0] == element:
            matches = fields[1:]
            
    if len(matches) == 0:
        logger.error('requested element not defined in notification')
        result = ('ERROR', 'requested element not defined in notification')
    else:
        logger.debug('getAttributeFromNotification found following match(es) for %s: %s' %(element, str(matches)))
        result = ('SUCCESS', matches)
   
    logger.debug('leave getAttributeFromNotification')
    return result
    
    
##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':

    import sys
    import common.target.common_lib.st_env_lib as st_env_lib
    st_env_lib.executeFunction(sys.argv)

    st_env_lib.setUp()
    
    ###########
   
  
    ###########TEST AREA END###############
    st_env_lib.tearDown()



