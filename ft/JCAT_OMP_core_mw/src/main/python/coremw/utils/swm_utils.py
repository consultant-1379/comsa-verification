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
import  omp.tf.ssh_lib as ssh_lib
from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System

#############GLOBALS##################
logger = None
######################################

def setUp():

    global logger
    
    logLevel = System.getProperty("jcat.logging")
    logger = Logger.getLogger('swm_utils logging')
    logger.setLevel(Level.toLevel(logLevel))
    logger.info("swm_utils: Initiating")
    return


def tearDown():
    logger.info("swm_utils: Bye, bye!")
    return


def _getInstalledSw():
  
    logger.debug('enter _getInstalledSw')
    
    result = ssh_lib.sendCommand('swm -n')
    if result[0] == 'ERROR':
        logger.error('No response from swm -n, see ssh log') 
    elif result[1] == '':
        errorInfo = 'swm -n returned an empty string'
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)       
    else:
        logger.debug(result) 
        
    logger.debug('leave _getInstalledSw')
    return result


def _getInstalledSwOnNode(safNode):
  
    logger.debug('enter _getInstalledSwOnNode')
    
    installedSwbundles = []
    result = ssh_lib.sendCommand('swm -n %s' % safNode)
    if result[0] == 'ERROR':
        logger.error('No response from swm -n %s, see ssh log' % safNode) 
    elif result[1] == '':
        errorInfo = 'swm -n %s returned an empty string' % safNode
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)       
    else:
        swBundles = result[1].split('\n')
        for bundle in swBundles:
            temp = bundle.split('/')
            temp = temp[0].split(': ')
            installedSwbundles.append(temp[1])
        result = ('SUCCESS', installedSwbundles)       
        logger.debug(result) 
        
    logger.debug('leave _getInstalledSwOnNode')
    return result    
    
def _importSwBundle(swBundleFileName = ''):

    logger.debug('enter _importSwBundle')
    
    result = ssh_lib.sendCommand('swm -i /home/tspsaf/incoming/%s' % swBundleFileName)
    if result[0] == 'ERROR' or result[1] == '':
        errorInfo = 'Import sw bundle file %s FAILED, see ssh log' %  swBundleFileName
        result =  ('ERROR',errorInfo)
        logger.error(errorInfo)
    else:
        swBundleName = result[1].split(' ')[1]
        if result[1] != 'Package %s imported to repository' % swBundleName:
            logger.error(result)
        else:
            result =  (result[0],swBundleName)
            logger.debug(result)
             
    logger.debug('leave _importSwBundle')
    return result   
    
    
def _upgradeSwOnNode(safNode, swBundleName = ''):
    
    logger.debug('enter _upgradeSwOnNode')
    
    pattern = 'Node %s upgraded with Package %s' %(safNode, swBundleName)
    result = ssh_lib.sendCommand('swm -u %s %s' % (safNode, swBundleName))
    if result[0] == 'SUCCESS' and re.search(pattern, result[1]): 
        logger.debug(result)
        result = (result[0], pattern)
    elif result[0] == 'ERROR': 
        errorInfo = 'Upgrade package %s on node %s failed, see ssh log' %  (swBundleName, safNode)
        logger.error(errorInfo) 
    else:
        result =  ('ERROR',result[1])
        logger.error(result)
        
    logger.debug('leave _upgradeSwOnNode')     
    return result  
    
def _removeAllSwFromCluster():
    
    logger.debug('enter _removeAllSwFromCluster')
    
    
    pattern = 'Package \'\' cleared for node ALL'
    result = ssh_lib.sendCommand('swm -c ALL')
    if result[0] == 'SUCCESS' and re.search(pattern, result[1]): 
        logger.debug(result) 
        result = (result[0], pattern)
    elif result[0] == 'ERROR': 
        errorInfo = 'remove all packages from the cluster failed, see ssh log'
        result =  ('ERROR',errorInfo)
        logger.error(errorInfo)
    else:
        result =  ('ERROR',result[1])
        logger.error(result)
        
    logger.debug('leave _removeAllSwFromCluster')
    
    return result      
     
def _removeSwFromNode(nodeType, subrack, slot, swBundleName = ''):
    
    logger.debug('enter _removeSwFromNode')
    
    safNode = '%s_%s_%s' % (nodeType, subrack, slot)
    pattern = 'Package \'%s\' cleared for node %s' % (swBundleName, safNode)
    result = ssh_lib.sendCommand('swm -c %s %s' % (safNode, swBundleName))
    if result[0] == 'SUCCESS' and re.search(pattern, result[1]): 
        logger.debug(result) 
        result = (result[0], pattern)
    elif result[0] == 'ERROR': 
        errorInfo = 'remove package %s from node %s failed, see ssh log' %  (swBundleName, safNode)
        result =  ('ERROR',errorInfo)
        logger.error(errorInfo) 
    else:
        result =  ('ERROR',result[1])
        logger.error(result)
        
    logger.debug('leave _removeSwFromNode')
    
    return result                     


def _installCmFiles(swBundleNames):
   
    logger.debug('enter _installCmFiles')
    
    cmd = 'cmFilesInstall'    
    packageList = []
        
    if isinstance(swBundleNames, str):
        packageList.append(swBundleNames)
    else:  packageList = swBundleNames
    
    for package in packageList:
        cmd = cmd + ' ' + package
        
    result =  ssh_lib.sendCommand(cmd)
    print result
    
    #more to do...
    #check if it exists fxs files for each package
    #ex) find /home/tspsaf/repository/<package name> -name *.fxs
    #check if the existing cm files are intalled
    #ex) CM file /home/tspsaf/var/lib/cm/SAF_SWM_x86_64-CXP9013626_3-R1A01_swm.fxs installed
                   
    logger.debug('leave _installCmFiles')
    return result   


def _removeCmFiles(swBundleNames):
   
    logger.debug('enter _removeCmFiles')
    
    cmd = 'cmFilesRemove'    
    packageList = []
        
    if isinstance(swBundleNames, str):
        packageList.append(swBundleNames)
    else:  packageList = swBundleNames
    
    for package in packageList:
        cmd = cmd + ' ' + package
        
    result =  ssh_lib.sendCommand(cmd)
    print result
        
    #more to do...
    #check if it exists fxs files for each package
    #ex) find /home/tspsaf/repository/<package name> -name *.fxs
    #check if the existing cm files are removed
    #ex) CM file /home/tspsaf/var/lib/cm/SAF_SWM_x86_64-CXP9013626_3-R1A01_swm.fxs removed
                   
    logger.debug('leave _removeCmFiles')
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


