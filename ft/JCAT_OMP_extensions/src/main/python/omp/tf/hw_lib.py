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
import sys
import re
import time



import omp.tf.ssh_lib as ssh_lib
import omp.tf.misc_lib as misc_lib
import omp.tf.utils._essim_utils_ as _essim_utils_
import omp.tf.utils._hw_utils_ as _hw_utils_
import omp.tf.utils._vbox_utils_ as _vbox_utils_

from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System

########NODE CONFIGURATION DATA##########
import omp.target.target_data as target_data


pUtil = None

def setUp():

    global logger
    global logLevel
    logger = Logger.getLogger('hw_lib')
    logLevel = System.getProperty("jcat.logging")
    logger.setLevel(Level.toLevel(logLevel))


    #targetType = 'hw_target' #future improvement: use target data to fetch the target type instead,
                             #use keyword nodeType in the xml config
    logger.debug("ssh_lib: Initiating!")

    global pUtil
    global targetData
    global targetType
    targetData=target_data.data
    targetType = targetData['targetType']

    try:
        logger.debug("Instantiating target type: %s" % (targetType))

        if targetType == 'vbox_target':
            pUtil = _vbox_utils_.Vbox()
        elif targetType == 'simulator_target':
            pUtil = _essim_utils_.Essim()
        else:
            targetType = 'hw_target'
            pUtil = _hw_utils_.Hw()
    except:
        logger.error("Failed to Instantiate target type: %s" % (targetType))

    #pUtil.setUp()

    return


def tearDown():
    logger.debug("hw_lib: Bye, bye!")
    return


def powerOn(subrack, slot):
    '''
    power on node().

    Arguments:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','Power on blade_<subrack>_<slot> succeeded') or
    tuple('ERROR', 'Power on blade_<subrack>_<slot> failed')
    NOTE:

    Dependencies:
    ssh_lib, target_data

    '''

    result = pUtil.powerOn(subrack, slot)
    logger.debug(result[1])
    return result


def powerOff(subrack, slot):
    '''
    power off node().

    Arguments:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','Power off blade_<subrack>_<slot> succeeded') or
    tuple('ERROR', 'Power off blade_<subrack>_<slot> failed')

    NOTE:

    Dependencies:
    ssh_lib, target_data

    '''

    result = pUtil.powerOff(subrack, slot)
    logger.debug(result[1])
    return result


def powerStatus(subrack, slot):
    '''
    Get power status for node().

    Arguments:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','Chassis Power is on|off') or
    tuple('ERROR', 'Get power status for blade_<subrack>_<slot> failed')

    NOTE:

    Dependencies:
    ssh_lib, target_data

    '''

    result = pUtil.powerStatus(subrack, slot)
    logger.debug(result[1])
    return result

def powerReset(subrack, slot):
    '''
    Get power status for node().

    Arguments:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','Chassis Power is on|off') or
    tuple('ERROR', 'Get power status for blade_<subrack>_<slot> failed')

    NOTE:

    Dependencies:
    ssh_lib, target_data

    '''

    result = pUtil.powerReset(subrack, slot)
    logger.debug(result[1])
    return result

def clusterPowerReset():
    '''
    Reset the cluster, power off/on on all valid blades().

    Arguments:
    None

    Returns:
    tuple('SUCCESS','cluster power reset succeeded') or
    tuple('ERROR', 'cluster power reset failed')

    Dependencies:
    target_data
    powerOff/On/Status

    '''

    result = pUtil.clusterPowerReset()
    logger.debug(result[1])
    return result


def pingBlade(subrack, slot, targetType = 'hw_target'):
    '''
    Ping a blade from the gateway.

    Argument:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','Blade_%subrack_%slot ping OK') or
    tuple('ERROR', 'Pinging blade_%subrack_%slot was not successful. %error message')

    Dependencies:
    ssh_lib
    '''


    blade = 'blade_%d_%d' %(subrack, slot)
    if targetType == 'hw_target':
        address = targetData['ipAddress']['ipmi'][blade]
        val = ssh_lib.sendCommand("ping -c 2 %s" %address, 9, 9)
    else:
        address = targetData['ipAddress']['ctrl']['ctrl%s'%slot]
        val = misc_lib.execCommand("ping -c 2 %s" %address)
    if ((re.search('2 packets transmitted, 2 received, 0% packet loss',val[1])) and val[0] == 'SUCCESS'):
        result = ('SUCCESS', 'Blade_%d_%d ping OK.' %(subrack, slot))
    else:
        result = ('ERROR', 'Pinging blade_%d_%d was not successful. %s' %(subrack, slot, val[1]))

    logger.debug(result[1])
    return result


def pingAllNodesInCluster():
    '''
    Ping all nodes in the cluster from the gateway and return OK if all nodes are ping-able and failure if at least one node does not respond

    Returns:
    tuple('SUCCESS', 'All nodes in the cluster respond to ping')
    tuple('ERROR', 'The following nodes did not respond to ping: %s' %str(notOkNodes))
    '''

    numberOfNodes = len(targetData['ipAddress']['ipmi'])
    j=0
    notOkNodes = []
    for i in range(numberOfNodes):
        subrack = 2
        slot = i + 1
        result = pingBlade(subrack, slot)
        if result[0] == 'SUCCESS':
            j = j+1
        else:
            notOkNodes.append('node_%d_%d' %(subrack, slot))

    if j != numberOfNodes:
        result = ('ERROR', 'The following nodes did not respond to ping: %s' %str(notOkNodes))
    else:
        result = ('SUCCESS', 'All nodes in the cluster respond to ping.')

    logger.debug(result[1])
    return result

def pingAllCtrlInCluster(testConfig):
    resultArray = []
    for controller in testConfig['controllers']:
        result = pingBlade(controller[0], controller[1], targetType = targetType)
        resultArray.append(result[0])
    return ('SUCCESS', resultArray)

def waitForPingAllCtrlInClusterOK(testConfig, timeout = 600):
    OkFlag = False
    stopTryTime = int(time.time()) + timeout
    while int(time.time()) < stopTryTime:
        result = pingAllCtrlInCluster(testConfig)
        if 'ERROR' not in result[1]:
            OkFlag = True
            break
        misc_lib.waitTime(10)
    if OkFlag == True:
        return ('SUCCESS', 'Ping all controllers OK')
    else:
        return ('ERROR', 'Ping all controllers not OK after %d seconds' %timeout)

def waitForPingAllNodesInClusterOk(timeout = 600):
    '''
    The method executes the pingAllNodesInCluster() several times until it returns SUCCESS or it times out.

    Returns:
    ('SUCCESS', 'All nodes in the cluster respond to ping.') or
    ('ERROR', 'The following nodes did not respond to ping: %s' %str(notOkNodes))
    '''


    stopTryTime = int(time.time()) + timeout
    while int(time.time()) < stopTryTime:
        val = pingAllNodesInCluster()
        if val[0] == 'SUCCESS':
            result = ('SUCCESS', 'All nodes in the cluster respond to ping.')
            break
        else:
            misc_lib.waitTime(5)

    if val[0] != 'SUCCESS':
        result = val


    return result


def virtualTargetPowerOnAll():
    """
    This method powers on all nodes in the virtual cluster.
    """
    logger.debug('hw_lib: virtualTargetPowerOnAll enter')
    result = pUtil.virtualTargetPowerOnAll(targetData)
    logger.debug('hw_lib: virtualTargetPowerOnAll leave')
    return result

def virtualTargetPowerOffAll():
    """
    This method powers off all nodes in the virtual cluster.
    """
    logger.debug('hw_lib: virtualTargetPowerOffAll enter')
    result = pUtil.virtualTargetPowerOffAll(targetData)
    logger.debug('hw_lib: virtualTargetPowerOffAll leave')
    return result

def virtualTargetSnapCreate(snapshotName):
    """
    This method powers off all nodes in the virtual cluster and
    takes a snapshot of all the nodes in the cluster.
    All nodes have the same snapshot name
    """
    logger.debug('hw_lib: virtualTargetSnapCreate enter')
    result = pUtil.virtualTargetSnapCreate(targetData, snapshotName)
    logger.debug('hw_lib: virtualTargetSnapCreate leave')
    return result

def virtualTargetSnapRestore(snapshotName):
    """
    This method restores the snapshot provided as argument to the method
    in all nodes of the virtual target
    The same snapshot name is expected on all nodes
    The method finally powers on the nodes in the cluster.
    """
    logger.debug('hw_lib: virtualTargetSnapRestore enter')
    result = pUtil.virtualTargetSnapRestore(targetData,snapshotName)
    logger.debug('hw_lib: virtualTargetSnapRestore leave')
    return result

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print "Can not run stand alone at the moment"
