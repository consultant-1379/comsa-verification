#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# Ericsson AB 2007 All rights reserved.
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
   %CCaseFile:  cmw_utils.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2010-04-20 %

   Author: ENAVNAC


   Description:
       The methods in this file wrap up the core mw commands
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
    logger = Logger.getLogger('cmw_utils')
    logger.setLevel(Level.toLevel(logLevel))
    logger.debug("cmw_utils: Initiating")
    return


def tearDown():
    logger.debug("cmw_utils: Bye, bye!")
    return



def _importSwBundle(swBundleFileName = ''):
    '''
    Import the software bundle and campaign to repository
    Wrapped command: cmw-sdp-import <sdpFile>

    Arguments:
    str swBundleFileName
    Returns:
    tuple('SUCCESS', swBundlePackageId) or
    tuple('ERROR', errorInfoString)

    NOTE:
    The bundle must be placed in /home/coremw/incoming before this function is executed
    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _importSwBundle')

    cmd = 'cmw-sdp-import /home/coremw/incoming/%s' % swBundleFileName
    result = ssh_lib.getTimeout()
    if result[0] == 'SUCCESS':
        initTimeout = result[1]
    else:
        logger.error(result[1])
        return result
    ssh_lib.setTimeout(600)
    result = ssh_lib.sendCommand(cmd)
    ssh_lib.setTimeout(initTimeout)
    if result[0] == 'SUCCESS' and 'command not found' not in result[1]:
        bundleStr = 'imported \(type=Bundle\)'
        campStr = 'imported \(type=Campaign\)'
        if re.search(bundleStr,result[1]) or re.search(campStr,result[1]):
            swBundlePackageId = result[1].split(' ')[0]
            result = ('SUCCESS', swBundlePackageId)
        elif re.search('Already imported', result[1]):
            logger.warn(result[1])
            swBundlePackageId = result[1].split('[')[1]
            swBundlePackageId = swBundlePackageId.split(']')[0]
            result = ('SUCCESS', swBundlePackageId)
        else:
            errorInfo = str(result[1])
            result =  ('ERROR',errorInfo)
            logger.error(errorInfo)
    else:
        errorInfo = 'Import sw bundle file %s FAILED: %s' %(swBundleFileName, result[1])
        result =  ('ERROR',errorInfo)
        logger.error(errorInfo)

    logger.debug('leave _importSwBundle')

    return result

def _removeSwBundle(swBundlePackageId = '' ):
    '''
    remove the software bundle from repository
    Wrapped command: cmw-sdp-remove <packageId>

    Arguments:
    swBundlePackageId

    Returns:
    tuple('SUCCESS', swBundlePackageIdString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
#Bundle SDP removed
    logger.debug('enter _removeSwBundle')
    cmd = 'cmw-sdp-remove %s' % swBundlePackageId
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS' and 'command not found' not in result[1]:
        bundleStr = 'Bundle SDP removed \[%s\]' % swBundlePackageId
        campStr = 'Campaign SDP removed \[%s\]' % swBundlePackageId
        if re.search(bundleStr,result[1]) or re.search(campStr,result[1]):
            swBundlePackageIdString = result[1].split(' ')[3]
            swBundlePackageIdString = swBundlePackageIdString.strip('[]')
            result = ('SUCCESS', swBundlePackageIdString)
        elif re.search('already removed', result[1]):
                logger.warn(result[1])
        else:
            errorInfo = str(result[1])
            result =  ('ERROR',errorInfo)
            logger.error(errorInfo)
    else:
        errorInfo = 'Import sw bundle file %s FAILED: %s' %(swBundlePackageId, result[1])
        result =  ('ERROR',errorInfo)
        logger.error(errorInfo)

    logger.debug('leave _removeSwBundle')

    return result


def _getInstalledSwOnRepository(listcampaigns = False):
    '''
    Get the list of all installed Sw from Repository
    Wrapped command: cmw-repository-list

    Arguments:
    -
    Returns:
    tuple('SUCCESS', resultString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _getInstalledSwOnRepository')
    if listcampaigns:
        cmd = 'cmw-repository-list --campaign'
        result = ssh_lib.sendCommand(cmd)
        if result[0] == 'ERROR':
            errorInfo = 'No response from %s: %s' %(cmd, result[1])
            logger.error(errorInfo)
            result = ('ERROR', errorInfo)
        elif result[1] == '':
            errorInfo = '%s returned an empty string'%cmd
            logger.error(errorInfo)
            result = ('ERROR', errorInfo)
        elif 'command not found' in result[1]:
            errorInfo = '%s command not found.'%cmd
            logger.error(errorInfo)
            result = ('ERROR', errorInfo)
    else:
        cmd = 'cmw-repository-list'
        result = ssh_lib.sendCommand(cmd)
        if result[0] == 'ERROR':
            errorInfo = 'No response from %s: %s' %(cmd, result[1])
            logger.error(errorInfo)
            result = ('ERROR', errorInfo)
        elif result[1] == '':
            errorInfo = '%s returned an empty string'%cmd
            logger.error(errorInfo)
            result = ('ERROR', errorInfo)
        elif 'command not found' in result[1]:
            errorInfo = '%s command not found.'%cmd
            logger.error(errorInfo)
            result = ('ERROR', errorInfo)


    logger.debug(str(result[1]))
    logger.debug('leave _getInstalledSwOnRepository')
    return result

def _getInstalledSwOnNode(hostname):
    '''
    Get the list of all installed packages on  a node
    Wrapped command: cmw-repository-list --node <hostname> (equivalent to 'swm -n <hostname> in SAF3.0)

    Arguments:
    -
    Returns:
    tuple('SUCCESS', resultString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _getInstalledSwOnNode')
    cmd = 'cmw-repository-list --node %s'%hostname
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR':
        errorInfo = 'No response from %s: %s' %(cmd, result[1])
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    elif result[1] == '':
        errorInfo = '%s returned an empty string'%cmd
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    elif 'command not found' in result[1]:
        errorInfo = '%s command not found.'%cmd
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)

    logger.debug(str(result[1]))
    logger.debug('leave _getInstalledSwOnNode')
    return result


def _getInstalledSwOnAllNodes():
    '''
    Get the list of all installed packages on  a node
    Wrapped command: cmw-repository-list --node (equivalent to 'swm -n' in SAF3.0)

    Arguments:
    -
    Returns:
    tuple('SUCCESS', resultString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _getInstalledSwOnAllNodes')
    cmd = 'cmw-repository-list --node'
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR':
        errorInfo = 'No response from %s: %s' %(cmd, result[1])
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    elif result[1] == '':
        errorInfo = '%s returned an empty string'%cmd
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    elif 'command not found' in result[1]:
        errorInfo = '%s command not found.'%cmd
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)

    logger.debug(str(result[1]))
    logger.debug('leave _getInstalledSwOnAllNodes')
    return result

def _startCampaign(campaignName = '', automaticBackup = True):
    '''
    start a campaign
    Wrapped command: cmw-campaign-start <campaign-name>

    Arguments: campaignName
    -
    Returns:
    tuple('SUCCESS', 'upgrade started successfully') or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _startCampaign')
    if automaticBackup:
        cmd = 'cmw-campaign-start %s'% campaignName
    else:
        cmd = 'cmw-campaign-start --disable-backup %s'% campaignName
    # When running an CoreMW template campaign the start will take awhile
    origTimeout = ssh_lib.getTimeout()[1]
    ssh_lib.setTimeout(300)

    result = ssh_lib.sendCommand('%s;echo ReturnCode=$?' % cmd)
    returnCode=result[1].split('ReturnCode=')
    if('0' == returnCode[1]):
        logger.debug(str(result[1]))
        result = ('SUCCESS','upgrade started successfully', 0)
    else:
        errorInfo = '%s failed: %s' %(cmd, result[1])
        logger.error(errorInfo)
        result = ('ERROR', result[1], int(returnCode[1]))

    ssh_lib.setTimeout(origTimeout)

    logger.debug(str(result[1]))
    logger.debug('leave _startCampaign')
    return result

def _checkCampaignStatus(campaignName = ''):
    '''
    check the campaign status
    Wrapped command: cmw-campaign-status <campaign-name>

    Arguments: campaignName
    -
    Returns:
    tuple('SUCCESS', <campaignName>=INITIAL|EXECUTING|COMPLETED) or
    tuple('ERROR',  <campaignName>=FAILED) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _checkCampaignStatus')
    cmd = 'cmw-campaign-status %s'%campaignName
    failString = '%s=FAILED' % campaignName
    rollbackFailedString = '%s=ROLLBACK_FAILED' % campaignName
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1] or 'ERROR' in result[1]:
        errorInfo = '%s failed: %s' %(cmd, result[1])
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    elif re.search(failString,result[1]):
        logger.error('%s: %s' %(failString, result[1]))
        result = ('ERROR', '%s: %s' %(failString, result[1]))
    elif re.search(rollbackFailedString,result[1]):
        logger.error('%s: %s' %(rollbackFailedString, result[1]))
        result = ('ERROR', '%s: %s' %(rollbackFailedString, result[1]))

    logger.debug(str(result[1]))
    logger.debug('leave _checkCampaignStatus')
    return result

def _stopCampaign(campaignName = ''):
    '''
    stop a campaign
    Wrapped command: cmw-campaign-stop <campaign-name>

    Arguments: campaignName
    -
    Returns:
    tuple('SUCCESS', resultString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib

    '''
    logger.debug('enter _stopCampaign')
    origTimeout = ssh_lib.getTimeout()[1]
    # 3 out of 31 fails with 30 sec timeout so let's increase it
    ssh_lib.setTimeout(300)

    cmd = 'cmw-campaign-stop %s'%campaignName
    result = ssh_lib.sendCommand(cmd)
    logger.info(result)
    if result[0] == 'ERROR' or 'command not found' in result[1] or 'ERROR' in result[1]:
        errorInfo = '%s failed: %s' %(cmd, result[1])
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)

    logger.debug(str(result[1]))
    ssh_lib.setTimeout(origTimeout)
    logger.debug('leave _stopCampaign')
    return result

def _commitCampaign(campaignName = '', timeout = 300):
    '''
    commit a campaign
    Wrapped command: cmw-campaign-commit <campaign-name>

    Arguments: campaignName
    -

    Returns:
    tuple('SUCCESS', 'Commit campaign succeeded') or
    tuple('ERROR',  'Commit campaign failed') or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _commitCampaign')
    origTimeout = ssh_lib.getTimeout()[1]
    # 3 out of 31 fails with 30 sec timeout so let's increase it
    ssh_lib.setTimeout(timeout)

    cmd = 'cmw-campaign-commit %s'% campaignName
    result = ssh_lib.sendCommand(cmd)
    logger.info(result)
    if result[0] == 'ERROR' or 'command not found' in result[1] or 'ERROR' in result[1]:
        errorInfo = '%s failed: %s' %(cmd, result[1])
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    elif 'IMM data persisted' in result[1]:
        logger.debug('Commit campaign succeeded')
        result = ('SUCCESS','Commit campaign succeeded')
    elif 'Performing one-time data migration' in result[1]:
        logger.debug('Commit campaign succeeded')
        result = ('SUCCESS','Commit campaign succeeded')
    elif result[1] != '':
        logger.error('Commit campaign failed')
        result = ('ERROR', result[1])
    else:
        logger.debug('Commit campaign succeeded')
        result = ('SUCCESS','Commit campaign succeeded')

    logger.debug(str(result[1]))
    ssh_lib.setTimeout(origTimeout)
    logger.debug('leave _commitCampaign')
    return result

def _getInstalledRpmOnNode(hostname):
    '''
    Get the list of all installed Rpm on a node
    Wrapped command: cmw-rpm-list <hostname>

    Arguments:
    -
    Returns:
    tuple('SUCCESS', resultList) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib

    '''

    logger.debug('enter _getInstalledRpmOnNode')
    cmd ='cmw-rpm-list %s'%hostname
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR':
        logger.error('No response from %s: %s'%(cmd, result[1]))
    elif result[1] == '':
        errorInfo = '%s returned an empty string'%cmd
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    elif 'command not found' in result[1]:
        errorInfo = '%s command not found.'%cmd
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)

    logger.debug(str(result[1]))
    logger.debug('leave _getInstalledRpmOnNode')
    return result

def _createPartialBackup(backupLabel, timeout, hostData):
    '''
    Create a partial cmw backup
    Wrapped command: cmw-partial-backup-create <label>
    Arguments:
    backupLabel
    Returns:
    tuple('SUCCESS', backupLabelString, 0) or
    tuple('ERROR', errorMsg, errorCode)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _createPartialBackup')

    backupTimes = {'CMW' : 0, 'OS' : 0, 'App' : 0, 'TOTAL': 0}
    if hostData == True:
        cmd ='cmw-partial-backup-create -v %s; echo resultCode=$?'%backupLabel
    else:
        cmd ='cmw-partial-backup-create -v --no-hostdata %s; echo resultCode=$?'%backupLabel
    origTimeout = ssh_lib.getTimeout()[1]
    ssh_lib.setTimeout( timeout)
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS':
        temp = result[1].split('resultCode=')
        resultString = temp[0]
        resultCode = int(temp[1])
        if resultCode == 0:
            temp = resultString.split('\n')
            for i in temp:
                if re.search('CMW:',i):
                    temp1 = i.split(':')[1]
                    backupTimes['CMW'] = int(temp1.strip())
                elif re.search('OS:',i):
                    temp1 = i.split(':')[1]
                    backupTimes['OS'] = int(temp1.strip())
                elif re.search('App:',i):
                    temp1 = i.split(':')[1]
                    backupTimes['App'] =  int(temp1.strip())
                elif re.search('TOTAL:',i):
                   temp1 = i.split(':')[1]
                   backupTimes['TOTAL'] = int(temp1.strip())
            result = ('SUCCESS',backupTimes,resultCode)
        else:
            result = ('ERROR', resultString, resultCode)
            logger.error('%s failed with error msg: %s and error code: %s' % (cmd, resultString, resultCode))
        #elif re.search('Backup already exist', result[1]):
        #    result = ('SUCCESS','Backup already exist')
        #    logger.debug(result)
    else:
        logger.error(result[1])
        result = ('ERROR',result[1],1)

    ssh_lib.setTimeout(origTimeout)

    logger.debug('leave  _createPartialBackup')
    return result

def _restorePartialBackup(backupLabel, timeout, hostData):
    '''
    Restore a partial cmw backup
    Wrapped command: cmw-partial-backup-restore <label>
    Arguments:
    backupLabel
    Returns:
    tuple('SUCCESS', backupLabelString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _restorePartialBackup')

    restoreTimes = {'CMW' : 0, 'OS' : 0, 'App' : 0, 'TOTAL': 0}
    if hostData == True:
        cmd ='cmw-partial-backup-restore -v %s --force' % backupLabel
    else:
        cmd ='cmw-partial-backup-restore -v --no-hostdata %s --force' % backupLabel
    origTimeout = ssh_lib.getTimeout()[1]
    ssh_lib.setTimeout(timeout)
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS':
        if re.search('Snapshot restore completed', result[1]) and re.search('Unpack the Core MW backup', result[1]):
            temp = result[1].split('\n')
            for i in temp:
                if re.search('CMW:',i):
                    temp1 = i.split(':')[1]
                    restoreTimes['CMW'] = int(temp1.strip())
                elif re.search('OS:',i):
                    temp1 = i.split(':')[1]
                    restoreTimes['OS'] = int(temp1.strip())
                elif re.search('App:',i):
                    temp1 = i.split(':')[1]
                    restoreTimes['App'] =  int(temp1.strip())
                elif re.search('TOTAL:',i):
                   temp1 = i.split(':')[1]
                   restoreTimes['TOTAL'] = int(temp1.strip())
            result = ('SUCCESS',restoreTimes)
    else:
        logger.error('%s failed: %s' %(cmd, result[1]))

    ssh_lib.setTimeout(origTimeout)

    logger.debug('leave  _restorePartialBackup')
    return result


def _registerPartialBackup(sdpFile= '', backupScript=''):
    '''
    Register a partial-backup script.
    Wrapped command: cmw-partial-backup-register <sdp> <backup-script>
    The backup-script path is relative within the SDP and may not contain spaces.

    Arguments:
    sdpFile, backupScript
    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _registerPartialBackup')
    cmd ='cmw-partial-backup-register %s %s'%(sdpFile, backupScript)

    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s' %(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave  _registerPartialBackup')
    return result


def _unregisterPartialBackup(sdpFile, backupScript):
    '''
    Unregister a partial-backup script.
    Wrapped command: cmw-partial-backup-unregister <sdp> <backup-script>
    The backup-script path is relative within the SDP and may not contain spaces.

    Arguments:
    sdpFile, backupScript

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _unregisterPartialBackup')
    cmd ='cmw-partial-backup-unregister %s %s'%(sdpFile, backupScript)

    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s'%(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave  _unregisterPartialBackup')
    return result


def _deletePartialBackup(backupLabel):
    '''
    Delete a partial cmw backup
    Wrapped command: cmw-partial-backup-delete <label>
    Arguments:
    backupLabel
    Returns:
    tuple('SUCCESS', backupLabelString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _deletePartialBackup')
    cmd ='cmw-partial-backup-remove %s' % backupLabel

    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s'%(cmd, result[1]))
    else:
        if result[1] == '':
            result = ('SUCCESS','remove of backup %s succeeded' % backupLabel)
        else:
            result = ('SUCCESS','backup %s does not exist' % backupLabel)
            logger.debug(str(result[1]))

    logger.debug('leave  _deletePartialBackup')

    return result

def _listPartialBackup():
    '''
    List partial cmw backups
    Wrapped command: cmw-partial-backup-list
    Arguments:

    Returns:
    tuple('SUCCESS', ListOfBackup) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _listPartialBackup')
    cmd ='cmw-partial-backup-list'
    backups = []
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s'%(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
        backups = result[1].split('\n')
        result = (result[0], backups)
    logger.debug('leave  _listPartialBackup')
    return result

def _deleteImmClass():
    '''
    Wraps opensaf command immcfg --delete-class
    Wrapped command: cmw-immClassDelete

    Arguments:

    Returns:
    tuple('SUCCESS',result[1] ) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _deleteImmClass')
    cmd ='cmw-immClassDelete'

    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s'%(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave _deleteImmClass')
    return result

def _checkClusterStatus( verbose, className):
    '''
    Get the system status and displays only the failed components
    Wrapped command:

    Arguments:
    verbose = 'off' or 'on' # Only failing items are printed unless the "-v" flag is specified.
    className =  app|csiass|comp|node|sg|si|siass|su
    Returns:
    tuple('SUCCESS', commandResultString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _checkClusterStatus')

    all = 'app csiass comp node sg si siass su'

    cmd = 'cmw-status'
    if verbose == 'on':
        cmd ='%s -v' % cmd
    if className == 'all':
        cmd = '%s %s' % (cmd, all)
    else:
        cmd = '%s %s' % (cmd, className )

    origTimeout = ssh_lib.getTimeout()[1]
    ssh_lib.setTimeout(900)
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS' and verbose == 'off':
        if re.search('Status OK', result[1]):
            logger.debug(str(result[1]))
        else:
            result = ('ERROR',result[1])
            logger.error('wrong cluster status: %s' % result[1])
    elif  result[0] == 'SUCCESS' and verbose == 'on':
        logger.debug(str(result[1]))

    else:
         logger.error('%s failed: %s'%(cmd, result[1]))

    ssh_lib.setTimeout(origTimeout)
    logger.debug('leave _checkClusterStatus')

    return result


def _forceRebootCluster():
    '''
    force reboot the cluster with the --yes tag.
    Wrapped command: cmw-cluster-reboot <--yes>

    Arguments:
    -

    Returns:
    tuple('SUCCESS', reboot cluster succeeded) or
    tuple('ERROR', reboot cluster failed)

    NOTE: ssh_lib.setTimeout is extended to 300 sec so command will not timeout to early

    Dependencies:
    ssh_lib
    '''


    logger.debug('enter _rebootCluster')

    #cmd ='cmw-cluster-reboot --yes'
    cmd ='cluster reboot -a'
    timeout = ssh_lib.getTimeout()
    ssh_lib.setTimeout(300)
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS' and 'command not found' not in result[1]:
        result = ('SUCCESS','reboot cluster succeeded')
    else:
        result = ('ERROR','reboot cluster failed: %s' %result[1])

    #ssh_lib.setTimeout(timeout)

    logger.debug('leave _rebootCluster')

    return result

def _clusterStopOpensaf():
    '''
    stop OpenSAF in the whole cluster. Not recommended for use other tahn in restore scenario.
    Wrapped command: cmw-cluster-stop
    Arguments:
    -

    Returns:
    tuple('SUCCESS', successInfoString) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _clusterStopOpensaf')
    cmd ='cmw-cluster-stop'
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        errorInfo = '%s failed: %s'%(cmd, result[1])
        logger.error(errorInfo)
        result[1] = errorInfo
    else:
        logger.debug(str(result[1]))
        successInfo = '%s succeeded'%cmd
        result[1] = successInfo
    logger.debug('leave _clusterStopOpensaf')
    return result

def _addToImm(packageId = ''):
    '''
    Info:
    Wrapped command:

    Arguments:

    Returns:
    tuple('SUCCESS', ) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _addToImm')
    cmd ='cmw-addToImm'

    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s'%(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave _addToImm')
    return result

def _immSave(persBackend):
    '''
    Info:
    Wrapped command:

    Arguments:

    Returns:
    tuple('SUCCESS','IMM data persisted' ) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _immSave')

    if persBackend:
        print 'persist IMM data to backend NOT IMPLEMENTED'
    else:
        cmd ='cmw-immSave'
        result = ssh_lib.sendCommand(cmd)
        if result[0] == 'ERROR' or 'command not found' in result[1]:
            logger.error('%s failed: %s'%(cmd, result[1]))
        else:
            logger.debug(str(result[1]))

    logger.debug('leave _immSave')
    return result

def _collectTraceLogs(subrack, slot, persistent, enable, traces):
    '''
    Info:
    Wrapped command:

    Arguments:

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _collectTraceLogs')

    cmd = 'cmw-trace'

    if persistent == True:
        cmd = cmd + ' -p'
    if enable == True:
        cmd = cmd + ' enable'
    else:
        cmd = cmd + ' disable'

    if slot > 2:
        tracelist = traces.split()
        for item in tracelist:
            if re.search('nd', item):
                cmd = cmd + ' ' + item
    else:
        cmd = cmd + ' ' + traces

    result = ssh_lib.sendCommand(cmd, subrack, slot)

    if result[0] != 'SUCCESS':
        logger.error(result[1])

    logger.debug('leave _collectTraceLogs')
    return result

def _unlockNode(hostname):
    '''
    unlock a node
    Wrapped command: cmw-node-unlock <hostname>

    Arguments:
    hostname

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _unlockNode')
    cmd ='cmw-node-unlock %s' %hostname
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s' %(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave _unlockNode')
    return result

def _lockNode(hostname):
    '''
    lock a node
    Wrapped command: cmw-node-lock

    Arguments:
    hostname

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _lockNode')
    cmd ='cmw-node-lock %s' %hostname
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s' %(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave _lockNode')
    return result

def _rebootNode(subrack, slot):
    '''
    reboot a node
    Wrapped command: cmw-node-reboot <hostname>

    Arguments: subrack, slot

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _rebootNode')

    result = ssh_lib.sendCommand('hostname',subrack, slot)
    if result[0] == 'ERROR':
        errorInfo = 'Is not possible to reboot the node, no connection to node %s %s. %s' % (subrack, slot, result[1])
        logger.warn( errorInfo)
        result = ('ERROR', errorInfo)
    else:
        hostname = result[1]
        cmd ='cmw-node-reboot %s' % hostname
        result = ssh_lib.sendCommand(cmd)
        if result[0] == 'ERROR' or 'command not found' in result[1]:
            logger.error('%s failed' % cmd)
        else:
            logger.debug(str(result[1]))

    logger.debug('leave _rebootNode')

    return result


def _addRpm(rpmFileName, hostname):
    '''
    add an rpm to linux
    Wrapped command: cmw-rpm-config-add <rpm-file> <hostname>

    Arguments: rpmFileName(packageId/rpmName.rpm), hostname

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _addRpm')
    cmd ='cmw-rpm-config-add %s %s'%(rpmFileName, hostname)

    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s' %(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave _addRpm')
    return result


def _deleteRpm(rpmFileName, hostname):
    '''
    delete an rpm from linux
    Wrapped command: cmw-rpm-config-delete <rpm-file> <hostname>

    Arguments: rpmFileName(packageId/rpmName.rpm), hostname

    Returns:
    tuple('SUCCESS', result[1]) or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _deleteRpm')
    cmd ='cmw-rpm-config-delete %s %s' %(rpmFileName, hostname)

    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1]:
        logger.error('%s failed: %s' %(cmd, result[1]))
    else:
        logger.debug(str(result[1]))
    logger.debug('leave _deleteRpm')
    return result

def _logsCollect(collectInfoFile, timeout):
    '''
    collect all logs on the cluster
    Wrapped command: cmw-logs-collect

    Arguments:
    str collectInfoFile

    Returns:
    tuple('SUCCESS','collect info succeeded) or
    tuple('ERROR', 'collect info failed')

    NOTE:

    Dependencies:
    ssh_lib
    '''
    logger.debug('enter _logsCollect')

    path = '/home/coremw/outgoing/'
    cmd = 'ls -1 /home/coremw/ | grep outgoing'
    result = ssh_lib.sendCommand(cmd)
    if result[1] == '':
        cmd = 'mkdir %s' % path
        result = ssh_lib.sendCommand(cmd)
    origTimeout = ssh_lib.getTimeout()[1]
    ssh_lib.setTimeout(timeout)
    cmd ='/opt/coremw/bin/cmw-collect-info %s%s' % (path, collectInfoFile)
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'SUCCESS' and re.search('Logs archived in %s%s' % (path, collectInfoFile),result[1]):
        info = '%s%s' % (path, collectInfoFile)
        logger.debug('file %s created' % info)
        result = ('SUCCESS',info)
    else:
        info = 'Create collect info file %s failed' % collectInfoFile
        logger.error('%s %s' % (info, result[1]))
        result = ('ERROR',info)
    ssh_lib.setTimeout(origTimeout)
    logger.debug('leave _logsCollect')

    return result

def _rollbackCampaign(campaignName = ''):
    '''
    rollback a campaign
    Wrapped command: cmw-campaign-rollback <campaign-name>

    Arguments: campaignName
    -

    Returns:
    tuple('SUCCESS', 'rollback campaign succeeded') or
    tuple('ERROR',  'rollback campaign failed') or
    tuple('ERROR', errorInfoString)

    NOTE:

    Dependencies:
    ssh_lib
    '''

    logger.debug('enter _rollbackCampaign')
    origTimeout = ssh_lib.getTimeout()[1]
    # 3 out of 31 fails with 30 sec timeout so let's increase it
    ssh_lib.setTimeout(300)

    cmd = 'cmw-campaign-rollback %s'% campaignName
    result = ssh_lib.sendCommand(cmd)
    if result[0] == 'ERROR' or 'command not found' in result[1] or 'error - ' in result[1]:
        errorInfo = '%s failed: %s' %(cmd, result[1])
        logger.error(errorInfo)
        result = ('ERROR', errorInfo)
    else:
        logger.debug('rollback campaign succeeded')
        result = ('SUCCESS','rollback campaign succeeded')

    logger.debug(str(result[1]))
    ssh_lib.setTimeout(origTimeout)
    logger.debug('leave _rollbackCampaign')
    return result

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print 'run in stand alone mode not supported in coreMW'


