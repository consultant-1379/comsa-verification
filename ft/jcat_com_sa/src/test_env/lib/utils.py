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

   Author: ejnolsz

   Description: A collection of misc methods.

'''

#############IMPORT##################

from org.apache.log4j import Logger
from java.lang import System
from random import randint
import os
import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException
import omp.tf.ssh_lib as ssh_lib
import omp.tf.hw_lib as hw_lib
import omp.tf.misc_lib as misc_lib
import test_env.lib.lib as lib
import coremw.saf_lib as saf_lib
import re
import time
import copy
# add a comment line
#############GLOBALS##################


logger = None
targetData = None
MY_REPOSITORY = os.environ['MY_REPOSITORY']

#############exceptions#############



#############setUp / tearDown#############

def setUp(logLevel,currentSut):

    global logger
    global targetData

    logger = Logger.getLogger('utils')
    logger.setLevel(logLevel)

    logger.info("utils: Initiating!")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    return


def tearDown():
    logger.debug("utils: bye, bye!")
    return


#############lib functions#############
def checkBackupAreaConsistency(backgroundLocation = "/var/lib/lde/", noBackupArea = "/storage/no-backup/"):
    """
    On a test system with RHEL the handling of backups is different then on SLES systems and it can become inconsistent.

    The place where backups are stored in the background is: /var/lib/lde/. If a backup is here, then it is possible to use (restore) that backup.
    If it is not, even if cmw-partial-backup-list lists it, it will not be possible to use it.

    When restoring a backup and restarting the cluster we noticed that all backups that were created after the restored backup disappeared from /var/lib/lde/.

    The aim of this method is to make/keep the backup system consistent:
        - if cmw-partial-backup-list shows a backup, then that backup should be possible to use
        - if cmw-partial-backup-list does not show a backup, then that backup should be possible to be created
    """


    consistentBackups = []

    # First find the backups that are saved in the background location. These are possible to restore.
    result = getRhelOsBackup(backgroundLocation)
    if result[0] != "SUCCESS":
        logger.debug('leave checkBackupAreaConsistency')
        return result
    backupsInBackLocation = result[1]

    # Than find the backups shown by Core MW as existing
    result = getCmwBackupListFilterWarnings()
    if result[0] != "SUCCESS":
        logger.debug('leave checkBackupAreaConsistency')
        return result
    backupsListedByCmw = result[1]

    # Delete any backup that is not saved in the background area
    for backup in backupsListedByCmw:
        if backupsInBackLocation.__contains__(backup):
            consistentBackups.append(backup)
        else:
            logger.warn('utils.checkBackupAreaConsistency: Backup %s not found under %s. It will be removed from all other places.' %(backup, backgroundLocation))
            result = saf_lib.backupRemove(backup)
            if result[0] != "SUCCESS":
                logger.debug('leave checkBackupAreaConsistency')
                return result
    for backup in backupsInBackLocation:
        if backup not in consistentBackups:
            cmd = '\\rm %s/local-boot-snapshot-%s.tar.gz'%(backgroundLocation, backup)
            logger.warn('utils.checkBackupAreaConsistency: Backup %s not found with CMW backup list command. It will be removed from %s.' %(backup, backgroundLocation))
            result = ssh_lib.sendCommand(cmd)
            if result[0] != "SUCCESS":
                logger.debug('leave checkBackupAreaConsistency')
                return result
    logger.info("Consistent backups: %s" %str(consistentBackups))

    # Finally remove any left-overs under the no-backup area (excluding /storage/no-backup/coremw/var/log/SC-2-1/*)
    noBackupAreaBackupsCmd = "find %s -name *.tar.gz | grep -v 'coremw/var/log'" %noBackupArea
    result = ssh_lib.sendCommand(noBackupAreaBackupsCmd)
    if result[0] != "SUCCESS":
        logger.debug('leave checkBackupAreaConsistency')
        return result
    noBackupAreaFiles = result[1].splitlines()
    for file in noBackupAreaFiles:
        backupName = file.split("/")[len(file.split("/")) - 1].split(".")[0]
        if not consistentBackups.__contains__(backupName):
            logger.warn('utils.checkBackupAreaConsistency: Removing %s' %file)
            result = ssh_lib.sendCommand('\\rm -f %s' %file)
            if result[0] != "SUCCESS":
                logger.debug('leave checkBackupAreaConsistency')
                return result

    return ("SUCCESS", "Backup system should be consistent.")

def getRhelOsBackup(osBackup = "/var/lib/lde/"):
    backupsInBackLocation = ''
    osBackupGetCmd = "ls %s | sed 's/local-boot-snapshot-//' | sed 's/.tar.gz//'" %osBackup
    result = ssh_lib.sendCommand(osBackupGetCmd)
    if result[0] != "SUCCESS":
        logger.debug('leave getRhelOsBackup')
        return result
    elif "No such file or directory" in result[1]:
        logger.debug('leave getRhelOsBackup')
        return ('ERROR', 'The backup directory %s does not exist: %s' %(osBackup, result[1]))
    if result[1] != "":
        backupsInBackLocation = result[1].splitlines()
        logger.debug('utils.getRhelOsBackup: Backups under %s: %s' %(osBackup, str(backupsInBackLocation)))

    logger.debug('leave getRhelOsBackup')
    return ('SUCCESS', backupsInBackLocation)

def getCmwBackupListFilterWarnings():
    result = saf_lib.backupList()
    if result[0] != "SUCCESS":
        logger.debug('leave getCmwBackupListFilterWarnings')
        return result
    backupListWithWarnings = result[1]

    backupsListedByCmw = []
    for i in range(len(backupListWithWarnings)):
        if "CMW: WARNING:" not in backupListWithWarnings[i]:
            backupsListedByCmw.append(backupListWithWarnings[i])

    logger.debug('utils.getCmwBackupListFilterWarnings: backups listed by CMW: %s' %backupsListedByCmw)
    logger.debug('leave getCmwBackupListFilterWarnings')
    return ('SUCCESS', backupsListedByCmw)

def snapRestOrUninstScr(self):
    logger.debug('enter utils.snapRestOrUninstScr')
    result = self.lib.updateLinuxDistroInDictionary(self.testSuiteConfig, self.distroTypes)
    self.fail(result[0], result[1])
    self.linuxDistro = self.testSuiteConfig['linuxDistro']['value']

    self.resetCluster = System.getProperty("resetCluster")

    self.restoreSnapshot = False
    self.runUninstallationScript = False

    if self.resetCluster == 'undef' and self.linuxDistro == self.distroTypes[1]:
        logger.debug('leave utils.snapRestOrUninstScr')
        self.fail('ERROR', 'Running on a RHEL system but no snapshot was specified for a clean RHEL system. The test case cannot be executed.')
    elif self.resetCluster != 'undef':
        self.restoreSnapshot = True
    else:
        self.runUninstallationScript = True

    logger.debug('leave utils.snapRestOrUninstScr')
    return (self.restoreSnapshot, self.runUninstallationScript)

def updateLocalSshKeys(testConfig, sshKeyUpdater):
    logger.debug('enter updateLocalSshKeys')
    MY_REPOSITORY = os.environ['MY_REPOSITORY']
    for controller in testConfig['controllers']:
        ipAddress = targetData['ipAddress']['ctrl']['ctrl%s'%str(testConfig['controllers'][testConfig['controllers'].index(controller)][1])]
        cmd = '%s %s' %(sshKeyUpdater, ipAddress)
        result = misc_lib.execCommand(cmd)
    logger.debug('leave updateLocalSshKeys')
