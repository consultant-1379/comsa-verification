#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# � Ericsson AB 2007 All rights reserved.
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
import re, time
from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System
import omp.tf.ssh_lib as ssh_lib
import omp.tf.misc_lib as misc_lib
import utils.cmw_utils as cmw_utils

from se.ericsson.jcat.omp.fw import OmpLibraryException
from se.ericsson.jcat.omp.library import SafLib
from java.util import HashMap

#############GLOBALS##################
#############GLOBALS##################
logger = None
################################################################################
# setUp / tearDown
################################################################################

def setUp():

    global logger

    logLevel = System.getProperty("jcat.logging")
    logger = Logger.getLogger('saf_lib logging')
    logger.setLevel(Level.toLevel(logLevel))
    cmw_utils.setUp()
    logger.info("saf_lib: Initiating")
    return

def setSut(sut):
    global currentSut
    currentSut = sut

def tearDown():
    logger.info("saf_lib: Bye, bye!")
    return

def getAmfNodeName(subrack, slot):
    '''
    Get the amf node name for subrack/slot

    Returns:
    String 'amf node name'

    '''
    safLib = currentSut.getLibrary('SafLib')
    return safLib.getAmfNodeName(subrack, slot)

def getHostName(subrack, slot):
    '''
    Get the host name for subrack/slot

    Returns:
    tuple('SUCCESS', 'host name ) or
    tuple('ERROR', 'Error message')

    '''

    amfNodeName = getAmfNodeName(subrack, slot)
    cmd = 'cmw-hostname-get %s' % amfNodeName
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR':
        logger.error('Failed to send command %s' % cmd)

    result =  result[0],str(result[1])

    return result

def getSubrack(amfNodeName):
    '''
    Get the subrack from a amf node name

    Returns:
    integer subrack number
    '''
    safLib = currentSut.getLibrary('SafLib')
    return safLib.getSubrack(amfNodeName)

def getSlot(amfNodeName):
    '''
    Get the slot from a amf node name

    Returns:
    integer slot number
    '''
    safLib = currentSut.getLibrary('SafLib')
    return safLib.getSlot(amfNodeName)

def isPL(subrack, slot):
    '''
    Is the blade at subrack and slot a PL?

    Returns:
    True if the blade is a PL, False if not
    '''
    safLib = currentSut.getLibrary('SafLib')
    return safLib.isPL(subrack, slot)

def isSC(subrack, slot):
    '''
    Is the blade at subrack and slot a SC?

    Returns:
    True if the blade is a SC, False if not
    '''
    safLib = currentSut.getLibrary('SafLib')
    return safLib.isSC(subrack, slot)

def getAmfNodeAdminState():
    '''
    Get the current amf node name administrative state

    Returns:
    tuple('SUCCESS', dictionary with amf node names as keys and their states as values ) or
    tuple('ERROR', 'Error message')
    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        result = safLib.getAmfNodeAdminState()
        adminState = {}

        for nodekey in result.keySet():
            state = result.get(nodekey)
            adminState[nodekey] = state

        return ('SUCCESS', adminState)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def getAmfNodeOperState():
    '''
    Get the current amf node name operating state

    Returns:
    tuple('SUCCESS', dictionary with amf node names as keys and their states as values ) or
    tuple('ERROR', 'Error message')
    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        result = safLib.getAmfNodeOperState()

        operState = {}

        for nodekey in result.keySet():
            state = result.get(nodekey)
            operState[nodekey] = state

        return ('SUCCESS', operState)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def getWantedAmfNodeAdminState():
    '''
    Get the wanted amf node name administrative state

    Returns:
    tuple('SUCCESS', dictionary with amf node names as keys and their states as values ) or
    tuple('ERROR', 'Error message')
    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        result = safLib.getWantedAmfNodeAdminState()

        adminState = {}

        for nodekey in result.keySet():
            state = result.get(nodekey)
            adminState[nodekey] = state

        return ('SUCCESS', adminState)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def getWantedAmfNodeOperState():
    '''
    Get the wanted amf node name operating state

    Returns:
    tuple('SUCCESS', dictionary with amf node names as keys and their states as values ) or
    tuple('ERROR', 'Error message')
    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        result = safLib.getWantedAmfNodeOperState()

        operState = {}

        for nodekey in result.keySet():
            state = result.get(nodekey)
            operState[nodekey] = state

        return ('SUCCESS', operState)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def isAmfNodeAdminState(wantedState):
    '''
    Compare the actual amf node admin state with the wanted state

    Returns:
    tuple('SUCCESS', True if the states are equal, otherwise False ) or
    tuple('ERROR', 'Error message')
    '''

    ws = HashMap()
    for node in wantedState.keys():
        ws.put(node, wantedState[node])

    try:
        safLib = currentSut.getLibrary('SafLib')
        result = safLib.isAmfNodeAdminState(ws)

        return ('SUCCESS', result)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def isAmfNodeOperState(wantedState):
    '''
    Compare the actual amf node oper state with the wanted state

    Returns:
    tuple('SUCCESS', True if the states are equal, otherwise False ) or
    tuple('ERROR', 'Error message')
    '''

    ws = HashMap()
    for node in wantedState.keys():
        ws.put(node, wantedState[node])

    try:
        safLib = currentSut.getLibrary('SafLib')
        result = safLib.isAmfNodeOperState(ws)

        return ('SUCCESS', result)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def getClusterState(subrack=0, slot=0):
    '''
    Get the HA State of all CSI:s on the cluster.

    Arguments:
    None
    {'<node>': {'<CSI>': '<state>'}
    Returns:
    tuple('SUCCESS','a nested dictionary formatted {'<node>': {'<CSI>': '<state>'}}') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        if(subrack==0 and slot==0):
            result = safLib.getHAState()
        else:
            result = safLib.getHAState(subrack, slot)

        nodeCsiState = {}

        for nodekey in result.keySet():
            csis = {}
            csiMap = result.get(nodekey)
            for csiSet in csiMap.keySet():
                csis[csiSet] = csiMap.get(csiSet)
            nodeCsiState[nodekey] = csis

        return ('SUCCESS', nodeCsiState)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def getComponentHAState(csiList):
    '''
    Get the HA State of a specific component.

    Arguments:
    a list of CSI belonging to a specific component

    Returns:
    tuple('SUCCESS','a nested dictionary a nested dictionary formatted {'<node>': {'<CSI>': '<state>'}} ') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        result = safLib.getComponentHAState(csiList)

        nodeCsiState = {}

        for nodekey in result.keySet():
            csis = {}
            csiMap = result.get(nodekey)
            for csiSet in csiMap.keySet():
                csis[csiSet] = csiMap.get(csiSet)
            nodeCsiState[nodekey] = csis

        return ('SUCCESS', nodeCsiState)

    except OmpLibraryException, e:
        return ('ERROR', e.getMessage())

def getCompRedundancyModel(model='none'):
    '''
    Get the all components on the cluster and their redundancy model, or
    the components associated with a specific model

    Arguments:
    None or a specific model

    Returns:
    tuple('SUCCESS','a dictionary with CSI as key and its redundancy model as value') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        if(model=='none'):
            result = safLib.getCompRedundancyModel()
        else:
            result = safLib.getCompRedundancyModel(model)

        compRed = {}

        for nodekey in result.keySet():
            model = result.get(nodekey)
            compRed[nodekey] = model

        return ('SUCCESS', compRed)
    except OmpLibraryException, e :
        return ('ERROR', e.getMessage())

def getActiveSc():
    '''
    Get the SC that is active.

    Arguments:
    None

    Returns:
    tuple('SUCCESS','Active SC') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        amfnodename = safLib.getActiveSc()

        return ('SUCCESS', amfnodename)
    except OmpLibraryException, e :
        return ('ERROR', e.getMessage())

def getStandbySc():
    '''
    Get the SC that is standby.

    Arguments:
    None

    Returns:
    tuple('SUCCESS','Standby SC') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        amfnodename = safLib.getStandbySc()

        return ('SUCCESS', amfnodename)
    except OmpLibraryException, e :
        return ('ERROR', e.getMessage())

def getScStatus(subrack, slot):
    '''
    Get the status of a specific SC.

    Arguments:
    subrack, slot

    Returns:
    tuple('SUCCESS','SC status (active/standby)') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        status = safLib.getScStatus(subrack, slot)

        return ('SUCCESS', status)
    except OmpLibraryException, e :
        return ('ERROR', e.getMessage())

def getClusterNodes():
    '''
    Get a list of the nodes in the cluster.

    Arguments:
    none

    Returns:
    tuple('SUCCESS','a list of the cluster nodes AMF node names') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        nodes = safLib.getClusterNodes()

        return ('SUCCESS', nodes)
    except OmpLibraryException, e :
        return ('ERROR', e.getMessage())

def getClusterNodesPL():
    '''
    Get a list of the PL nodes in the cluster.

    Arguments:
    none

    Returns:
    tuple('SUCCESS','a list of the PL AMF node names') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        nodes = safLib.getClusterNodesPL()

        return ('SUCCESS', nodes)
    except OmpLibraryException, e :
        return ('ERROR', e.getMessage())

def getClusterNodesSC():
    '''
    Get a list of the SC nodes in the cluster.

    Arguments:
    none

    Returns:
    tuple('SUCCESS','a list of the SC AMF node names') or
    tuple('ERROR', 'Error message')

    '''
    try:
        safLib = currentSut.getLibrary('SafLib')
        nodes = safLib.getClusterNodesSC()

        return ('SUCCESS', nodes)
    except OmpLibraryException, e :
        return ('ERROR', e.getMessage())

def getInstalledSwOnRepository():
    '''
    Get installed software specified in repository

    Arguments:
    none

    Returns:
    tuple('SUCCES','<all installed packages in repository>') or
    tuple('ERROR', 'Get installed software from repository failed')

    NOTE:

    Dependencies:
    cmw_utils->ssh_lib

    '''

    logger.debug('enter getInstalledSw')

    info = 'Get installed packages from repository'
    result = cmw_utils._getInstalledSwOnRepository()
    if result[0] == 'SUCCESS':
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave getInstalledSw')
    return result


def getImportedCampaigns():
    '''
    Get imported campaigns in the repository

    Arguments:
    none

    Returns:
    tuple('SUCCES','<all imported campaigns in repository>') or
    tuple('ERROR', 'Get imported campaigns from repository failed')

    NOTE:

    Dependencies:
    cmw_utils->ssh_lib

    '''

    logger.debug('enter getImportedCampaigns')

    info = 'Get imported campaigns from repository'
    result = cmw_utils._getInstalledSwOnRepository(listcampaigns = True)
    if result[0] == 'SUCCESS':
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave getImportedCampaigns')
    return result


def getInstalledSwBundlesOnNode(hostname = 'SC-2-1'):
    '''

    This command lists the packageIds of software installed on repository
    and also says whether they are used or not

    Arguments:
    None

    Returns:
    tuple('SUCCESS', list[package1, ...]
    tuple('ERROR', string'Failed to get installed packages on the repository')

    NOTE:

    Dependencies:
    swm_utils->ssh_lib
    '''
    logger.debug("Enter getInstalledSwOnRepository")

    result = ('ERROR', 'Failed to get installed packages on the repository')

    ret = cmw_utils._getInstalledSwOnRepository(hostname)
    swBundles = []
    if ret[0] != 'ERROR':
        listPack = ret[1].splitlines()
        if len(listPack) != 0:
            for pack in listPack :
                temp = pack.split()
                if len(temp) != 2:
                    result = ('ERROR', 'Data received in an unexpected format. %s' %ret)
                    break
                swBundles.append(temp[1])

        result = ['SUCCESS', swBundles]
        logger.debug('SW bundles on %s: %s' %(hostname, swBundles))
    else:
        logger.error(str(result[1]))

    logger.debug("Exit getInstalledSwOnRepository")
    return result



def getInstalledSwOnNode(nodeType, subrack, slot):
    '''
    Get installed software for one saf node.

    Arguments:
    none

    Returns:
    tuple('SUCCES','<all installed packages on saf node>') or
    tuple('ERROR', 'Get installed packages on <saf node>  failed')

    NOTE:

    Dependencies:
    swm_utils->ssh_lib

    '''

    logger.debug('enter getInstalledSwOnNode')

    hostname = '%s-%s-%s' % (nodeType, subrack, slot) #NOTE hardcoded hostname separator
    info = 'Get installed packages on %s' % hostname
    result = cmw_utils._getInstalledSwOnNode(hostname)
    if result[0] == 'SUCCESS':
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave getInstalledSwOnNode')
    return result

def getInstalledSwOnAllNodes():
    '''
    Get installed software for all nodes.

    Arguments:
    none

    Returns:
    tuple('SUCCES','<all installed packages for each node>') or
    tuple('ERROR', 'Get installed packages from the system failed')

    NOTE:

    Dependencies:
    cmw_utils->ssh_lib

    '''

    logger.debug('enter getInstalledSwOnAllNodes')

    info = 'Get installed packages from the system'
    result = cmw_utils._getInstalledSwOnAllNodes()
    if result[0] == 'SUCCESS':
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave getInstalledSwOnAllNodes')
    return result

def copySwPackageToSystem(filePaths):
    '''
    copy one or several sw packages to the system.
    The packages are placed in the directory /home/coremw/incoming

    Arguments:
    for single copy
    (str <absolute file path>)
    for multi copy
    (list <absolute file path>)

    Returns:
    tuple('SUCCES','Copy packages to the system succeeded') or
    tuple('ERROR', 'Copy packages to the system failed')

    NOTE:
    the incoming directory is not created during installation core MW.
    If the incoming directory does not exist, then this function creates it.
    Dependencies:
    ssh_lib

    '''

    logger.debug('enter copySwPackageToSystem')

    fileList = []
    dest = '/home/coremw/incoming/'
    errorInfo = []
    info = 'Copy packages to the system'

    if isinstance(filePaths, str):
        fileList.append(filePaths)
    else:  fileList = filePaths

    createIncomingdirectory()

    errorFlag = False
    for i, filePath in enumerate(fileList):
        tempResult = ssh_lib.remoteCopy(filePath, dest)
        if tempResult != ('SUCCESS','File copied'):
            errorInfo.append(tempResult[1])
            errorFlag = True

    if errorFlag == True:
        logger.error(errorInfo)
        result = ('ERROR','%s failed' % info)
    else:
        info = '%s succeeded' % info
        logger.debug(info)
        result = ('SUCCESS',info)

    logger.debug('leave copySwPackageToSystem')
    return result


def importSwBundle(swBundleFileName = ''):
    '''
    Import the software bundle to the repository.

    Arguments:
    str(<the software bundle file name>)

    Returns:
    tuple('SUCCES','<swBundlePackageId>') or
    tuple('ERROR', 'Import <swBundleFileName> failed')

    NOTE:
    The file must be placed in /home/coremw/incoming directory

    Dependencies:
    swm_utils->ssh_lib

    '''

    logger.debug('enter importSwBundle')

    createIncomingdirectory()
    info = 'Import %s' % swBundleFileName
    result = cmw_utils._importSwBundle(swBundleFileName)
    if result[0] == 'SUCCESS':
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave importSwBundle')
    return result


def removeSwBundle(swBundlePackageId = ''):
    '''
    Remove the software bundle from the repository.

    Arguments:
    str(<the software bundle identity>)

    Returns:
    tuple('SUCCES','remove <swBundlePackageId> succeeded') or
    tuple('ERROR', 'remove <swBundlePackageId> failed')

    NOTE:


    Dependencies:
    swm_utils->ssh_lib

    '''

    logger.debug('enter removeSwBundle')


    info = 'Remove %s' % swBundlePackageId
    result = cmw_utils._removeSwBundle(swBundlePackageId)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        result = (result[0], info)
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        #result = (result[0], info)

    logger.debug('leave removeSwBundle')
    return result


 ###### This function is not valid for core mw ###########
def upgradeSwOnNode(nodeType, subrack, slot, swBundleName = ''):
    '''
    upgrade software bundle on node.

    Arguments:
    (str nodeType, int subrack, int slot, str <software bundle name>)

    Returns:
    tuple('SUCCES','Upgrade package <swBundleName> on <saf node> succeeded') or\
    tuple('ERROR', 'Upgrade package <swBundleName> on <saf node> failed')

    NOTE:

    Dependencies:
    swm_utils->ssh_lib

    '''

    logger.debug('enter upgradeSwOnNode')

    amfNode = getAmfNodeName(subrack,slot)
    info = 'Upgrade package %s on %s' % (swBundleName, amfNode)
    result = swm_utils._upgradeSwOnNode(amfNode, swBundleName)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = (result[0], info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave upgradeSwOnNode')
    return result


 ###### This function is not valid for core mw ###########
def removeAllSwFromCluster():
    '''
    remove all software from the cluster, except from LINUX.

    Arguments:
    none

    Returns:
    tuple('SUCCES','remove all packages from cluster succeeded') or\
    tuple('ERROR', 'remove all packages from cluster failed')

    NOTE:

    Dependencies:
    swm_utils->ssh_lib

    '''

    logger.debug('enter removeAllSwFromCluster')

    info = 'remove all packages from cluster'

    result = swm_utils._removeAllSwFromCluster()
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = (result[0], info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave removeAllSwFromCluster')
    return result


###### This function is not valid for core mw ###########
def removeAllSwFromNode(nodeType, subrack, slot):
    '''
    remove all software from node, except from LINUX.

    Arguments:
    (str nodeType, int subrack, int slot)

    Returns:
    tuple('SUCCES','remove all packages from <saf node> succeeded') or\
    tuple('ERROR', 'remove all packages from <saf node> failed')

    NOTE:

    Dependencies:
    swm_utils->ssh_lib

    '''

    logger.debug('enter removeAllSwFromNode')

    amfNode = getAmfNodeName(subrack,slot)
    info = 'remove all packages from %s' % amfNode
    okFlag = True
    result = getInstalledSwOnNode(nodeType, subrack, slot)
    if result[0] == 'ERROR':
        logger.error(result)
        okFlag = False
    else:
        for bundle in result[1]:
            if not re.search('LINUX', bundle):
                if removeSwFromNode(nodeType, subrack, slot, bundle)[0] == 'ERROR':
                    okFlag = False

    if okFlag == True:
        info = '%s succeeded' % info
        logger.debug(info)
        result = ('SUCCESS',info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = ('ERROR',info)


    logger.debug('leave removeAllSwFromNode')
    return result


###### This function is not valid for core mw ###########
def removeSwFromNode(nodeType, subrack, slot, swBundleName = ''):
    '''
    remove software bundle from node.

    Arguments:
    (str nodeType, int subrack, int slot, str <software bundle name>)

    Returns:
    tuple('SUCCES','remove package <swBundleName> from <saf node> succeeded') or\
    tuple('ERROR', 'remove package <swBundleName> from <saf node> failed')

    NOTE:

    Dependencies:
    swm_utils->ssh_lib

    '''

    logger.debug('enter removeSwFromNode')

    amfNode = getAmfNodeName(subrack,slot)
    info = 'remove package %s from %s' % (swBundleName, amfNode)
    result = swm_utils._removeSwFromNode(nodeType, subrack, slot, swBundleName)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = (result[0], info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave removeSwFromNode')
    return result


###### This function is not valid for core mw ###########
def installCmFiles(swBundleNames):
    '''
    install one or several CM files.

    Arguments:
    for single install
    (str <sw bundle name>)
    for multi install
    (list [str<sw bundle name>,str<sw bundle name>,..])

    Returns:
    tuple('SUCCES','Install CM file(s) succeeded') or
    tuple('ERROR', 'Install CM file(s) failed')

    NOTE:

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter installCmFiles')

    info = 'Install CM file(s)'

    result = swm_utils._installCmFiles(swBundleNames)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = (result[0], info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave installCmFiles')
    return result


###### This function is not valid for core mw ###########
def removeCmFiles(swBundleNames):
    '''
    remove one or several CM files.

    Arguments:
    for single remove
    (str <sw bundle name>)
    for multi remove
    (list [str<sw bundle name>,str<sw bundle name>,..])

    Returns:
    tuple('SUCCES','Remove CM file(s) succeeded') or
    tuple('ERROR', 'Remove CM file(s) failed')

    NOTE:

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter removeCmFiles')

    info = 'Remove CM file(s)'

    result = swm_utils._removeCmFiles(swBundleNames)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = (result[0], info)
    else:
        info = '%s failed' % info
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave removeCmFiles')
    return result


###### This function is not valid for core mw ###########
def removeSwmLockFile():
    """ check if swm_lock file exist in /home/tspsaf/var/lib and removes it.

        Return ('SUCCESS','info') or ('ERROR','info').
    """

    logger.debug('enter removeSwmLockFile')
    cmd = 'ls /home/tspsaf/var/lib/ | grep swm_lock'
    result = ssh_lib.sendCommand(cmd)
    if str(result[1]) == 'swm_lock':
        logger.info('Swm lock file found. Waiting max 5 minutes to see if it is removed by the system. If not, it will be removed after 5 minutes')
        for i in range(10):
            cmd = 'ls /home/tspsaf/var/lib/ | grep swm_lock'
            result = ssh_lib.sendCommand(cmd)
            if str(result[1]) == 'swm_lock':
                misc_lib.waitTime(30)
            else:
                logger.info('The swm lock file was removed by the system. Exiting.')
                result = ('SUCCESS', 'The swm lock file was removed by the system during the wait time.')
                logger.debug('leave removeSwmLockFile')
                return result

        cmd = 'ls /home/tspsaf/var/lib/ | grep swm_lock'
        result = ssh_lib.sendCommand(cmd)
        if str(result[1]) == 'swm_lock':
            cmd = 'rm -f /home/tspsaf/var/lib/swm_lock'
            logger.warning( 'Removing /home/tspsaf/var/lib/swm_lock')
            result = ssh_lib.sendCommand(cmd)
        else:
            logger.info('The swm lock file was removed by the system. Exiting.')
            result = ('SUCCESS', 'The swm lock file was removed by the system during the wait time.')

    logger.debug('leave removeSwmLockFile')
    return result



######
###### Under here we have methods from the OS lib
######

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

    logger.debug('enter clusterRebootNode')

    pattern = 'Rebooting node %d' % slot
    result = cmw_utils._rebootNode(subrack, slot)
    #result = ssh_lib.sendCommand('cmw_node_reboot  %d' % slot)
    info = 'Rebooting blade_%d_%d' % (subrack, slot)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = (result[0], info)
    else:
        info = '%s failed \n%s' % (info, result[1])
        logger.error(info)
        result = (result[0], info)

    logger.debug('leave clusterRebootNode')
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
    cmw_utils

    '''

    logger.debug('enter clusterReboot')
    info = 'Rebooting all blades'
    result = cmw_utils._forceRebootCluster()
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = ('SUCCESS',info)
    else:
        info = '%s failed \n%s' % (info, result[1])
        logger.error(info)
        result = ('ERROR', info)

    logger.debug('leave clusterReboot')
    return result


#not exposed as cmw command, should we this function in saf_lib?
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

    logger.debug('enter clusterStop')

    info = 'Stop all registered init script on blade_%d_%d' % (subrack, slot)
    pattern = 'We break'
    result = ssh_lib.sendCommand('cluster start --stop', subrack, slot)
    #result = ssh_lib.sendCommand('cmw_cluster_stop', subrack, slot)
    if result[0] == 'SUCCESS' and re.search(pattern, result[1]):
        info = '%s succeeded' % info
        logger.debug(info)
        result = ('SUCCESS',info)
    else:
        info = '%s failed. \n%s' % (info, result[1])
        logger.error(info)
        result = ('ERROR', info)

    logger.debug('leave clusterStop')
    return result

def getControllerState(subrack, slot):
    '''
    Get which controller that is active

    Arguments:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter getControllerState')




    amfNode = getAmfNodeName(subrack,slot)
    cmd = "amf-state su readi safSu=%s,safSg=2N,safApp=OpenSAF" %amfNode
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    lines = result[1].splitlines()[1]
    elements = lines.split('=')
    if len(elements) == 2 and 'saAmfSUReadinessState' in elements[0]:
        return ('SUCCESS', str(elements[1].split('(')[0]))
    else:
        logger.error(">>> failed to get %s readiness state." %amfNode)
        logger.debug('leave getControllerState')
        return ('ERROR', result[1])

def getPayloadState(subrack, slot):
    '''
    Get the state of a specific payload

    Arguments:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter getPayloadState')

    amfNode = getAmfNodeName(subrack,slot)
    cmd = "amf-state su readi safSu=%s,safSg=NoRed,safApp=OpenSAF" %amfNode
    result = ssh_lib.sendCommand(cmd)
    lines = result[1].splitlines()[1]
    elements = lines.split('=')
    if len(elements) == 2 and 'saAmfSUReadinessState' in elements[0]:
        logger.debug('leave getPayloadState')
        return ('SUCCESS', str(elements[1].split('(')[0]))
    else:
        logger.error(">>> failed to get %s readiness state." %amfNode)
        logger.debug('leave getPayloadState')
        return ('ERROR', result[1])

def getServiceInstanceHaState(subrack, slot , serviceInstances):
    '''
    Get the SI HA state of a specific payload

    Arguments:
    (int subrack, int slot, {string})
    Obs seviceInstance shall be a list

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
# subrack and slot have to be integers
# serviceInstances has to be a list of strings
    logger.debug('enter getServiceInstanceHaState')


    varType=type(serviceInstances)
    varType=str(varType)
    pattern = "list"
    serviceInstanceList = []
    if (re.search(pattern, varType)):  # is it a list or a scalar?
        serviceInstanceList = serviceInstances
    else:
        serviceInstanceList.append(serviceInstances)

    amfNode = getAmfNodeName(subrack,slot)

    resultList = []
    response = 'SUCCESS'

    for serviceInstance in serviceInstanceList:
        result = ssh_lib.sendCommand('amf-find csiass | grep %s | grep safSu=%s' %(serviceInstance, amfNode))
        lines = result[1].splitlines()
        if len(lines) != 1 :
            return ('ERROR', 'Ambiguous query, less or more than one match. \n%s' %result[1])
        DN = str(lines[0])
        cmd = "amf-state csiass ha '%s'" %DN
        result = ssh_lib.sendCommand(cmd)
        if len(result[1].splitlines()) < 0:
            logger.error(result)
            logger.error(">>> failed to get %s ha state." %serviceInstance)
            return ('ERROR', 'failed to get %s ha state' %serviceInstance)
        else:
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

def getCompOpState(subrack, slot , comp):
    '''
    Get operational state of a specific component, comp

    Arguments:
    (int subrack, int slot, {comp})
    Observation comp shall be a list

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
# subrack and slot have to be integers
# comp has to be a list of strings
    logger.debug('enter getCompOpState')


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

    amfNode = getAmfNodeName(subrack,slot)

    for comp in compList:
        result = ssh_lib.sendCommand('amf-find comp | grep -i %s | grep %s' %(comp, amfNode))
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

def getAllCompState():
    '''
    Get operational state of all components

    Arguments:

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter getAllCompState')

    compStates = ['oper','pres','readi']
    compStatesTranls = ['operational','presence','readiness']
    allCompStates = {'operational' : [], 'presence' : [], 'readiness' : []}
    totCheckFlag = True

    #result = ssh_lib.sendCommand('export IMMA_TRACE_PATHNAME=/tmp/imm.trace')#this line is a workaround, should be removed when IMM is more stable
    for k, state in enumerate(compStates):
        cmd = 'amf-state comp %s' % state
        okFlag = False

        for i in range(10):

            result = ssh_lib.sendCommand(cmd)
            if not re.search('MDS:ERR',result[1]): #n�gon mer check av returv�rde n�r amf-state funktionen funkar som den ska
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

def getSuReadinessState(subrack, slot , serviceUnit):
    '''
    getSuReadinessState

    Arguments:
    (int subrack, int slot, list serviceUnit)
    Observation serviceUnit shall be a list of strings

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
# subrack and slot have to be integers
# serviceUnit has to be a list of strings
    logger.debug('enter getSuReadinessState')


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

    amfNode = getAmfNodeName(subrack,slot)

    for serviceUnit in serviceUnitList:
        cmd = 'amf-find su | grep %s | grep %s' %(amfNode, serviceUnit)
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

def getCompReadiState(subrack, slot , comp):
    '''
    getCompReadiState

    Arguments:
    (int subrack, int slot, list comp)
    Observation comp shall be a list of strings

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
# subrack and slot have to be integers
# comp has to be a list of strings
    logger.debug('enter getCompReadiState')


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

    amfNode = getAmfNodeName(subrack,slot)

    for comp in compList:
        result = ssh_lib.sendCommand('amf-find comp | grep -i %s | grep %s' %(comp, amfNode))
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

def getControllerHAState(subrack, slot):
    '''
    getControllerHAState

    Arguments:
    (int subrack, int slot)

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter getControllerHAState')


    amfNode = getAmfNodeName(subrack,slot)
    cmd = "amf-state csiass ha 'safCSIComp=safComp=CPD\,safSu=%s\,safSg=2N\,safApp=OpenSAF,safCsi=CPD,safSi=SC-2N,safApp=OpenSAF'" %amfNode
    result = ssh_lib.sendCommand(cmd, subrack, slot)
    lines = result[1].splitlines()[1]
    elements = lines.split('=')
    if len(elements) == 2 and 'saAmfCSICompHAState' in elements[0]:
        return ('SUCCESS', str(elements[1].split('(')[0]))
    else:
        logger.error(">>> failed to get %s ha state." %amfNode)
        logger.debug('leave getControllerHAState')
        return ('ERROR', result[1])

def getRedPatternDNs(subrack, slot, appPatern = 'ta_', redundancyPattern = '2N'):
    '''
    getRedPatternDNs

    Arguments:
    (int subrack, int slot, string appPatern, string redundancyPattern)

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter get2NRedundantDNs')

    amfNode = getAmfNodeName(subrack,slot)

    cmd = 'amf-find csiass | grep -i %s' %amfNode
    if redundancyPattern != '':
        cmd += ' | grep %s' %redundancyPattern
    if appPatern != '':
        cmd += " | egrep '%s'" %appPatern

    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        return result
    DNs = result[1].splitlines()
    if len(DNs) == 0:
        return('ERROR', 'No component with 2N redundancy on the specified blade')
    else:
        return ('SUCCESS', DNs)

    logger.debug('leave get2NRedundantDNs')

def returnDnForSearchPatterns(searchPatterns):
    '''
    returnDnForSearchPatterns

    Arguments:
    (list searchPatterns)
    searchPatterns has to be a list of patterns to look after in the DN
    the method returns all the DNs which contain all the specified patterns

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter returnDnForSearchPatterns')

    varType = str(type(searchPatterns))
    if 'str' or 'unicode' in varType:
        searchPattern = [searchPatterns]
    elif 'list' in varType:
        searchPattern = searchPatterns
    else:
        logger.debug('leave returnDnForSearchPatterns')
        return('ERROR', 'Unsupported variable type specified as search pattern')

#build up the grep command
    grepCommand = 'amf-find csiass'
    for i in range(len(searchPattern)):
        grepCommand = grepCommand + ' | grep %s' %searchPattern[i]

    result = ssh_lib.sendCommand(grepCommand)
    if result[0] != 'SUCCESS':
        logger.debug('leave returnDnForSearchPatterns')
        return result
    DNs = result[1].splitlines()
    if len(DNs) == 0:
        logger.debug('leave returnDnForSearchPatterns')
        return('ERROR', 'No distinguished names found with the specified search patterns.')
    else:
        logger.debug('leave returnDnForSearchPatterns')
        return ('SUCCESS', DNs)


def backupCreate(backupName, timeout = 2400, hostData = True):
    '''
    Backup the cluster

    Arguments:
    (str backupName, int timeout)

    Returns:
    tuple('SUCCESS',{'CMW' : <backuptime for Core Mw>,
                     'OS'  : <backuptime for OS>,
                     'App' : <backuptime for application>,
                     'TOTAL': <total backuptime>},
                     0) or
    tuple('ERROR', <error msg>,<error code>)

    NOTE:

    Dependencies:
    cmw_utils

    '''

    logger.debug('enter backupCreate')
    info = 'Create backup'
    result = cmw_utils._createPartialBackup(backupName, timeout, hostData)
    #if result[0] == 'SUCCESS':
    #    info = '%s succeeded' % info
    #    logger.debug(info)
    #    result = ('SUCCESS',result[1])
    #else:
    #    info = '%s failed \n%s' % (info, result[1])
    #    logger.error(info)
    #    result = ('ERROR', info)

    logger.debug('leave backupCreate')
    return result

def backupRestore(backupName, timeout = 2400, hostData = True):
    '''
    Backup the node

    Arguments:
    (str backupName, int timeout)

    Returns:
    tuple('SUCCESS',{'CMW' : <restoretime for Core Mw>,
                     'OS'  : <restoretime for OS>,
                     'App' : <restoretime for application>,
                     'TOTAL': <total restoretime>}) or
    tuple('ERROR', 'Restore from backup failed <error info')

    NOTE:


    Dependencies:
    cmw_utils

    '''

    logger.debug('enter backupRestore')

    info = 'Restore from backup'

    result = cmw_utils._restorePartialBackup(backupName, timeout, hostData)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = ('SUCCESS',result[1])
    else:
        info = '%s failed \n%s' % (info, result[1])
        logger.error(info)
        result = ('ERROR', info)


    logger.debug('leave backupRestore')
    return result


def backupList():
    '''
    List the backups on the cluster

    Arguments:
    none

    Returns:
    tuple('SUCCESS',[list of backups]) or
    tuple('ERROR', 'list backups failed <error info')

    NOTE:


    Dependencies:
    cmw_utils

    '''

    logger.debug('enter backupList')

    info = 'List backups'

    result = cmw_utils._listPartialBackup()
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        logger.debug(info)
        result = ('SUCCESS',result[1])
    else:
        info = '%s failed \n%s' % (info, result[1])
        logger.error(info)
        result = ('ERROR', info)

    logger.debug('leave backupList')

    return result


def isBackup(backupName):
    '''
    Check if the backup exist

    Arguments:
    none

    Returns:
    tuple('SUCCESS','EXIST') or
    tuple('SUCCESS','NOT EXIST') or
    tuple('ERROR', 'error info')

    NOTE:


    Dependencies:
    cmw_utils

    '''

    logger.debug('enter isBackup')

    result = backupList()
    if result[0] == 'SUCCESS':
        okFlag = False
        for backup in result[1]:
            if backupName.strip() == backup.strip():
                result = ('SUCCESS', 'EXIST')
                okFlag = True
                break
            # in case we create backup without Host OS
            elif "No Host OS backup for [%s]" %backupName in backup:
                result = ('SUCCESS', 'EXIST')
                okFlag = True
                break
        if not okFlag:
            result = ('SUCCESS', 'NOT EXIST')
    else:
        result = ('ERROR','check if backup exist failed: %s' % result[1])

    return result


def backupRemove(backupName):
    '''
    Remove backup from the cluster

    Arguments:
    str backupName

    Returns:
    tuple('SUCCESS',remove of backup <backupName> succeeded) or
    tuple('SUCCESS','backup <backupName> does not exist') or
    tuple('ERROR', '<error info>')

    NOTE:


    Dependencies:
    cmw_utils

    '''

    logger.debug('enter backupRemove')

    result = cmw_utils._deletePartialBackup(backupName)

    logger.debug('leave backupRemove')

    return result



#not valid anymore, use importswbundle instead
def upgradeImmImport(upgradeCampaignXml):
    '''
    upgradeImmImport. Add the upgrade campaign to IMM.

    Arguments:
    (String upgradeCampaignXml)
    The upgrade CAMPAIGN file to import to the imm

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR', '')

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('Enter upgradeStart')

    if (upgradeCampaignXml.endswith('.xml')):
        str = upgradeCampaignXml.split('.xml')
    else:
        return ('ERROR', 'Not an xml as inparameter')

    commandStr = "immcfg -c SaSmfCampaign -a saSmfCmpgFileUri=/hostfs/%s  safSmfCampaign=%s,safApp=safSmfService" %(upgradeCampaignXml, str[0])
    result = ssh_lib.sendCommand(commandStr)

    logger.debug("Exit upgradeStart")
    return result

def upgradeStart(campaignName, automaticBackup = False):
    '''
    upgradeStart. Start executing the upgrade campaign.

    Arguments:
    (String campaignName)

    Returns:
    tuple('SUCCESS','upgrade started successfully') or
    tuple('ERROR', <error info>)

    NOTE:

    Dependencies:
    cmw_utils

    '''

    logger.debug('enter upgradeStart')

    result = cmw_utils._startCampaign(campaignName, automaticBackup)

    logger.debug('leave upgradeStart')

    return result

def upgradeStop(campaignName):
    '''
    upgradeStop. Stop (suspend) executing the upgrade campaign.

    Arguments:
    (String campaignName)

    Returns:
    tuple('SUCCESS','upgrade suspended successfully') or
    tuple('ERROR', <error info>)

    NOTE:

    Dependencies:
    cmw_utils

    '''

    logger.debug('enter upgradeStop')

    result = cmw_utils._stopCampaign(campaignName)

    logger.debug('leave upgradeStop')

    return result

def upgradeStatusCheck(campaignName):
    '''
    upgradeStatusCheck - Check the status of the upgrade campaing.

    Arguments:
    (String upgradeCampaignXml)
    The upgrade package to check the status on the ongoing upgrade.

    Returns:
    tuple('SUCCESS', <campaignName>=INITIAL|EXECUTING|COMPLETED) or
    tuple('ERROR',  <campaignName>=FAILED) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter upgradeStatusCheck')

    updateActivecontroller()

    result =  cmw_utils._checkCampaignStatus(campaignName)

    logger.debug('leave upgradeStatusCheck')

    return result

def upgradeCommit(campaignName, timeout = 300):
    '''
    commit a campaign

    Arguments: campaignName

    Returns:
    tuple('SUCCESS', 'Commit campaign succeeded') or
    tuple('ERROR',  'Commit campaign failed') or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter upgradeCommit')

    result =  cmw_utils._commitCampaign(campaignName, timeout)

    logger.debug('leave upgradeCommit')

    return result


def upgradeRollback(campaignName):
    '''
    Rollback a campaign

    Arguments: campaignName

    Returns:
    tuple('SUCCESS', 'Rollback campaign succeeded') or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter upgradeCommit')

    result =  cmw_utils._rollbackCampaign(campaignName)

    logger.debug('leave upgradeRollback')

    return result


def createIncomingdirectory():
    '''
    Create incoming directory in /home/coremw

    Arguments:
    none

    Returns:
    tuple('SUCCESS','') or
    tuple('ERROR','could not create the directory /home/coremw/incoming')


    NOTE:
    the incoming directory is not created during installation of core MW.
    If the incoming directory does not exist, then this function creates it.
    Dependencies:
    ssh_lib

    '''

    #chech if the incoming directory exist
    cmd = 'ls -1 /home/coremw/ | grep incoming | awk \'{print $9}\''
    result = ssh_lib.sendCommand(cmd)
    if result[1] != 'incoming':
        cmd = 'mkdir -p /home/coremw/incoming'
        result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR':
        info = 'could not create the directory /home/coremw/incoming'
        logger.error(info)
        result = ('ERROR',info)

    return result


def install(fileName):
    '''
    This method will install Core MW on a target system.
    It will take the software release from the location specified by pathToRepository

    !!! IMPORTANT
    It is a prerequisit for this methos that there is no installation of Core MW on the target system.
    The removal of the software has to be performed before calling this method.
    At this moment in time there is no

    Arguments:
    string fileName: the absolute path of the tar file on the local linux machine

    Returns:
    tuple ('SUCCESS', True) or
    tuple ('ERROR', string (error message))
    '''

    logger.debug("enter install")
    locationOnTargetSystem = '/home/test/installationTest'

# Copy the sw package to the target system and unpack it
    result = ssh_lib.sendCommand('mkdir -p %s' %locationOnTargetSystem)
    if result[0] != 'SUCCESS':
        logger.debug("leave install")
        return result

    result = ssh_lib.sendCommand('rm -rf %s/*' %locationOnTargetSystem)
    if result[0] != 'SUCCESS':
        logger.debug("leave install")
        return result

    result = ssh_lib.sendCommand('mkdir -p %s/d1' %locationOnTargetSystem)
    if result[0] != 'SUCCESS':
        logger.debug("leave install")
        return result

    result = ssh_lib.getTimeout()
    if result[0] != 'SUCCESS':
        logger.debug("leave install")
        return result
    initTimeout = result[1]

    # Calculate the new timeout value depending on the number of blades
    newTimeout = (int(currentSut.getConfigDataString("physical_size")) * 30) + 60
    ssh_lib.setTimeout(newTimeout)


    targetFileName = fileName.split('/')[len(fileName.split('/')) - 1]
    copyFileName = locationOnTargetSystem + '/' + targetFileName

    result = ssh_lib.remoteCopy(fileName, copyFileName)
    if result[0] != 'SUCCESS':
        ssh_lib.setTimeout(initTimeout)
        logger.debug("leave install")
        return result

    targetFileName = locationOnTargetSystem + '/' + targetFileName
    result = ssh_lib.sendCommand('tar xf %s -C %s/d1' %(targetFileName, locationOnTargetSystem))
    if result[0] != 'SUCCESS':
        logger.debug("leave install")
        ssh_lib.setTimeout(initTimeout)
        return result

# Install CoreMW

    result = ssh_lib.sendCommand('pushd %s/d1/ ; ./install ; popd ' %locationOnTargetSystem)
    if result[0] != 'SUCCESS':
        ssh_lib.setTimeout(initTimeout)
        logger.debug("leave install")
        return result

# Check result
    returnCode = ssh_lib.sendCommand('echo $?')
    if returnCode != ('SUCCESS', '0'):
        ssh_lib.setTimeout(initTimeout)
        logger.debug("leave install")
        return ('ERROR', 'Installation command execution not successful. Result is: %s' % str(result))

    if 'Install script completed successfully' not in result[1]:
        ssh_lib.setTimeout(initTimeout)
        logger.debug("leave install")
        return ('ERROR', 'The "Install script completed successfully" message not received. Returned result is: %s' %result[1])

    time.sleep(10)
    for i in range(currentSut.getSutSize()):
        ssh_lib.tearDownHandles()
        time.sleep(2)
        result = ssh_lib.sendCommand('cmw-status node su comp')
        if result[0] != 'SUCCESS' and i == 9:
            ssh_lib.setTimeout(initTimeout)
            logger.debug("leave install")
            return result

    returnCode = ssh_lib.sendCommand('echo $?')
    if returnCode != ('SUCCESS', '0'):
        ssh_lib.setTimeout(initTimeout)
        logger.debug("leave install")
        return ('ERROR', 'Installation command execution not successful. Result is: %' %str(result))

    if 'Status OK' not in result[1]:
        ssh_lib.setTimeout(initTimeout)
        logger.debug("leave install")
        return ('ERROR', 'Cluster status after installation is not OK. See returned message: %s' %result[1])

    ssh_lib.setTimeout(initTimeout)
    logger.debug("leave install")
    return ('SUCCESS', True)


def collectInfo(collectInfoFile, timeout = 600):
    '''
    Collects log information from the cluster and packs into <collectInfoFile>
    in tar.gz format.


    Arguments:
    str collectInfoFile

    Returns:
    tuple('SUCCESS','<absolute path/collectInfoFile>') or
    tuple('ERROR', 'Create collect info file <collectInfoFile> failed')

    NOTE:


    Dependencies:
    cmw_utils

    '''

    logger.debug('enter collectInfo')

    result = cmw_utils._logsCollect(collectInfoFile, timeout)
    if result[0] == 'ERROR':
        logger.error(result[1])
    logger.debug('leave collectInfo')

    return result




def checkClusterStatus(verbose = 'off', className = 'all'):
    '''
    Get the system status and displays only the failed components
    Wrapped command:

    Arguments:
    str verbose('off' or 'on', Only failing items are printed unless the verbose = 'on' then all items are listed
    but no validation of the outcome is performed)
    str className (app|csiass|comp|node|sg|si|siass|su, choose 'all' if all types should be checked)

    Returns:
    tuple('SUCCESS', commandResultString (if verbose = 'on')) or
    tuple('SUCCESS', 'Status OK' (if verbose = 'off')) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter checkClusterStatus')

    result = cmw_utils._checkClusterStatus( verbose, className)

    logger.debug('leave checkClusterStatus')

    return result


def saveImmdata(persBackend = False):
    '''
    Persist IMM data to disk or to persistent backend db.


    Arguments:
    bool True = store data to persistent backend db

    Returns:
    tuple('SUCCESS','IMM data persisted') or
    tuple('ERROR', 'persist IMM data failed')

    NOTE:


    Dependencies:
    cmw_utils

    '''

    logger.debug('enter saveImmdata')

    result = cmw_utils. _immSave(persBackend)
    if result[0] == 'ERROR':
        logger.error(result[1])
    logger.debug('leave saveImmdata')

    return result

def collectTraceLogs(subrack = 2, slot = 0, persistent = True, enable = True, traces = 'amfd amfnd ckptd ckptnd clmd dtmd dtd immd immnd logd ntfd rded smfd smfnd'):
    '''
    Enables/disables trace for an opensaf service on the node the command is executed on.
    The following services are possible to trace:
    amfd amfnd ckptd ckptnd clmd dtmd dtd immd immnd logd ntfd rded smfd smfnd".


    Arguments:
    int subrack = Subrack (example: PL-2-5 has subrack=2 and slot=5)
    int slot = Slot
    bool persistent = Make the trace setting persistent over node/cluster reboot
    bool enable = Enable trace for service(s)
    string trace = List locally and persistent active traces: all amfd amfnd ckptd ckptnd clmd dtmd dtd immd immnd logd ntfd rded smfd smfnd

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:


    Dependencies:
    cmw_utils

    '''

    logger.debug('enter collectTraceLogs')

    result = cmw_utils._collectTraceLogs(subrack, slot, persistent, enable, traces)
    if result[0] == 'ERROR':
        logger.error(result[1])

    logger.debug('leave collectTraceLogs')

    return result


def registerBackupScript(swBundlePackageId = '', backupScriptName = ''):
    '''
    Register application backup script.

    Arguments:
    str(<the software bundle identity>, <the backup script name>)

    Returns:
    tuple('SUCCES','register backup script:<backupScriptName> for <swBundlePackageId>  succeeded') or
    tuple('ERROR', 'register backup script:<backupScriptName> for <swBundlePackageId> failed')

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter registerBackupScript')

    swBundlePackageId = swBundlePackageId.strip()
    backupScriptName =  backupScriptName.strip()
    info = 'register backup script:%s for %s' % (swBundlePackageId, backupScriptName)
    cmd = 'cmw-partial-backup-register %s %s' % (swBundlePackageId, backupScriptName)
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        result = (result[0], info)
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        #result = (result[0], info)

    logger.debug('leave registerBackupScript')
    return result


def unregisterBackupScript(swBundlePackageId = '', backupScriptName = ''):
    '''
    unregister application backup script.

    Arguments:
    str(<the software bundle identity>, <the backup script name>)

    Returns:
    tuple('SUCCES','unregister backup script:<backupScriptName> for <swBundlePackageId>  succeeded') or
    tuple('ERROR', 'unregister backup script:<backupScriptName> for <swBundlePackageId> failed')

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter unregisterBackupScript')

    swBundlePackageId = swBundlePackageId.strip()
    backupScriptName =  backupScriptName.strip()
    info = 'unregister backup script:%s for %s' % (swBundlePackageId, backupScriptName)
    cmd = 'cmw-partial-backup-unregister %s %s' % (swBundlePackageId, backupScriptName)
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS':
        info = '%s succeeded' % info
        result = (result[0], info)
        logger.debug('%s succeeded' % info)
    else:
        info = '%s failed' % info
        logger.error(info)
        #result = (result[0], info)

    logger.debug('leave unregisterBackupScript')
    return result

def updateActivecontroller():
    '''
    update the ssh_lib internal control flag for active controller.
    Check if it has has been a switch between the controllers on the system.
    If it has, then update the ssh_lib internal control flag for active controller.

    Arguments:
    None

    Returns:
    tuple ('SUCCESS','active ssh controller matching active controller on the system')

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter updateActivecontroller')

    cmd = 'cmw-status -v siass | grep -A2 safSi=SC-2N,safApp=OpenSAF'
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS' and re.search('HAState=ACTIVE',result[1]):
        osafStatesOnSc = result[1]
        subrack, slot, nodeNr = ssh_lib.getConfig()
        amfNodeName = getAmfNodeName(subrack,slot)
        suName = 'safSu=' + amfNodeName
        temp = osafStatesOnSc[0:len(osafStatesOnSc)/2] + 'DELIMITER' + osafStatesOnSc[len(osafStatesOnSc)/2:len(osafStatesOnSc)]
        osafStatesOnSc = temp.split('DELIMITER')
        if (re.search('STANDBY',osafStatesOnSc[0]) and re.search(suName,osafStatesOnSc[0])):
            logger.warn('switch active ssh controller')
            if slot == 1:
                slot = 2
                nodeNr = 2
            else:
                slot = 1
                nodeNr = 1
            ssh_lib.setConfig(subrack, slot,nodeNr )
        elif (re.search('STANDBY',osafStatesOnSc[1]) and re.search(suName,osafStatesOnSc[1])):
            logger.warn('switch active ssh controller')
            if slot == 1:
                slot = 2
            else:
                slot = 1
            ssh_lib.setConfig(subrack, slot,nodeNr )
    else:
        result = getClusterNodesSC()
        if result[0] == 'SUCCESS' and len(result[1]) >= 2:
            logger.warn('No controller with HA state ACTIVE found, switch active ssh controller')
            subrack, slot, nodeNr = ssh_lib.getConfig()
            if slot == 1:
                slot = 2
                nodeNr = 2
            else:
                slot = 1
                nodeNr = 1
            ssh_lib.setConfig(subrack, slot,nodeNr )
        else:
            logger.warn('No controller with HA state ACTIVE found, cannot switch active ssh controller')


    return ('SUCCESS','active ssh controller matching active controller on the system')

    logger.debug('leave updateActivecontroller')

if __name__ == '__main__':
    print "Bye saf_lib __name__ == __main__"
