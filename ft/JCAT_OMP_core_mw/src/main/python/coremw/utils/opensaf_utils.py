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


   Description:

'''

import re
import  common.target.common_lib.ssh_lib as ssh_lib
from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System

#############GLOBALS##################
logger = None
######################################

def setUp():

    global logger
    
    logLevel = System.getProperty("jcat.logging")
    logger = Logger.getLogger('opensaf_utils logging')
    logger.setLevel(Level.toLevel(logLevel))
    logger.info("opensaf_utils: Initiating")
    return


def tearDown():
    logger.info("opensaf_utils: Bye, bye!")
    return


def _lockAmfNode(subrack, slot):
  
    logger.debug('enter _lockAmfNode')
    
    result = ssh_lib.sendCommand('swm -n')
    if result[0] == 'ERROR':
        logger.error('No response from swm -n, see ssh log') 
    elif result[1] == '':
        errorInfo = 'swm -n returned an empty string'
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)       
    else:
        logger.debug(result) 
        
    logger.debug('leave _lockAmfNode')
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


