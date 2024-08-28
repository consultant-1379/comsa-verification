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
   %CCaseFile:  os_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2007-08-10 %

   Author:


   Description:
  
'''

import re
import ssh_lib as ssh_lib
import logger_lib as logger_lib


def setUp():

    logger_lib.logMessage("os_lib: Initiating")
    return


def tearDown():
    logger_lib.logMessage("os_lib: Bye, bye!")
    return


def clusterRebootNode(subrack, slot):
    '''
    reboot one blade in the cluster.
    
    Arguments:
    (int subrack, int slot)
    
    Returns:
    tuple('SUCCESS','Rebooting blade_<subrack>_<slot> succeeded') or
    tuple('ERROR', 'Rebooting blade_<subrack>_<slot> failed')  
     
    NOTE:
    
    Dependencies:
    ssh_lib
    
    '''
  
    logger_lib.enter()
    pattern = 'Rebooting node %d' % slot
    result = ssh_lib.sendCommand('cluster reboot -n %d' % slot)
    info = 'Rebooting blade_%d_%d' % (subrack, slot)
    if result[0] == 'SUCCESS' and re.search(pattern, result[1]): 
        info = '%s succeeded' % info
        logger_lib.logMessage(info, logLevel = 'debug') 
        result = (result[0], info)
    else:
        info = '%s failed' % info
        logger_lib.logMessage(info, logLevel = 'error')
        result = (result[0], info)
    
    logger_lib.leave()
    return result
    
    
def clusterReboot():
    '''
    reboot all blades in the cluster.
    
    Arguments:
    (none)
    
    Returns:
    tuple('SUCCESS','Rebooting all blades succeeded') or
    tuple('ERROR', 'Rebooting all blades  failed')  
     
    NOTE:
    
    Dependencies:
    lotc_utils
    
    '''
  
    logger_lib.enter()
    info = 'Rebooting all blades'
    result = ssh_lib.sendCommand('cluster reboot -a')
    if result[0] == 'SUCCESS': 
        info = '%s succeeded' % info
        logger_lib.logMessage(info, logLevel = 'debug') 
        result = ('SUCCESS',info) 
    else:
        info = '%s failed' % info
        logger_lib.logMessage(info, logLevel = 'error')
        result = ('ERROR', info)  
  
    logger_lib.leave()
    return result

def clusterStart(subrack, slot):
    '''
    Start all registered init script in the application group
    (start opensaf) on one node 
    
    Arguments:
    (int subrack, int slot)
    
    Returns:
    tuple('SUCCESS','Start all registered init script on blade_<subrack>_<slot> succeeded') or
    tuple('ERROR', 'Start all registered init script on blade_<subrack>_<slot> failed')  
     
    NOTE:
    
    Dependencies:
    lotc_utils
    
    '''
  
    logger_lib.enter()
    
    info = 'Start all registered init script on blade_%d_%d' % (subrack, slot) 
    pattern = 'Node Initialization Successful'
    result = ssh_lib.sendCommand('cluster start --start', subrack, slot)
    if result[0] == 'SUCCESS' and re.search(pattern, result[1]): 
        info = '%s succeeded' % info 
        logger_lib.logMessage(info, logLevel = 'debug') 
        result = ('SUCCESS',info)
    else:
        info = '%s failed' % info 
        logger_lib.logMessage(info, logLevel = 'error')
        result = ('ERROR', info)  
        
    logger_lib.leave()
    return result  


def clusterStop(subrack, slot):
    '''
    Stop all registered init script in the application group
    (stop opensaf) on one node 
    
    Arguments:
    (int subrack, int slot)
    
    Returns:
    tuple('SUCCESS','Stop all registered init script on blade_<subrack>_<slot> succeeded') or
    tuple('ERROR', 'Stop all registered init script on blade_<subrack>_<slot> failed')  
     
    NOTE:
    
    Dependencies:
    lotc_utils
    
    '''
  
    logger_lib.enter()
    
    info = 'Stop all registered init script on blade_%d_%d' % (subrack, slot) 
    pattern = 'We break'
    result = ssh_lib.sendCommand('cluster start --stop', subrack, slot)
    if result[0] == 'SUCCESS' and re.search(pattern, result[1]): 
        info = '%s succeeded' % info 
        logger_lib.logMessage(info, logLevel = 'debug') 
        result = ('SUCCESS',info) 
    else:
        info = '%s failed' % info 
        logger_lib.logMessage(info, logLevel = 'error')
        result = ('ERROR', info)  
   
    logger_lib.leave()
    return result  


def syncRpmConfig(subrack, slot):
    '''
    Synchronize RPM configuration on a node
    
    Arguments:
    (int subrack, int slot)
    
    Returns:
    tuple('SUCCESS','synchronization of node <slot> succeeded') or
    tuple('ERROR', 'synchronization of node <slot> failed')  
     
    NOTE:
    
    Dependencies:
    
    
    '''
  
    logger_lib.enter()
    
    info = 'synchronization of node %s' % slot 
    
    result = ssh_lib.getTimeout()
    origTimeout = result[1]
    ssh_lib.setTimeout(60, subrack, slot)
    
    result = ssh_lib.sendCommand('cluster rpm -s -n %s' % slot, subrack, slot)
    if not re.search('Completed RPM synchronization of node %s' % slot, result[1]) or result[0] == 'ERROR':
        info = '%s failed' % info 
        logger_lib.logMessage(info, logLevel = 'error') 
        result = ('ERROR',info) 
    else:
        info = '%s succeeded' % info 
        logger_lib.logMessage(info, logLevel = 'debug') 
        result = ('SUCCESS',info)  
   
    ssh_lib.setTimeout(origTimeout, subrack, slot)
       
    logger_lib.leave()
   
    return result                  


##############################################################################
# Module test
##############################################################################
if __name__ == '__main__': 

    import common.target.target_data as target_data
    import common.target.common_lib.booking_lib as booking_lib
    import common.target.common_lib.st_env_lib as st_env_lib
    node=booking_lib.checkBooking()
    targetData=target_data.setTargetHwData(node)    
    #st_env_lib.executeFunction(sys.argv)

    st_env_lib.setUp()
    ###########TEST AREA START###############



    ###########TEST AREA END###############
    st_env_lib.tearDown()    
