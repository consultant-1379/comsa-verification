#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2014 All rights reserved.
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

   Description: A collection of methods specific to COM SA Trace CC adaptation.

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
import test_env.lib.comsa_lib as comsa_lib
import coremw.saf_lib as saf_lib
import re
import time
import copy

#############GLOBALS##################
logger = None
targetData = None
MY_REPOSITORY = os.environ['MY_REPOSITORY']

#############setUp / tearDown#############
def setUp(logLevel,currentSut):

    global logger
    global targetData

    # Variables needed for the build token management
    global dirName
    global user
    global tokenPattern
    global suiteLogDir
    global numberOfGetTokenRetries
    global traceEaDtCxpNum
    global traceCcDtCxpNum

    dirName = System.getProperty("logdir")
    user = os.environ['USER']
    tokenPattern = 'buildToken-%s' %user
    suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
    numberOfGetTokenRetries = 5

    traceEaDtCxpNum = 'CXP9021071'
    traceCcDtCxpNum = 'CXP9021956'

    logger = Logger.getLogger('trace_lib')
    logger.setLevel(logLevel)

    logger.info("trace_lib: Initiating!")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    return


def tearDown():
    logger.debug("trace_lib: bye, bye!")
    return


#############lib functions#############

def installTraceComp(testConfig, localPathToBinaries, pathOnTarget, cxpNumbers, compName, rollingUpgrade = False):
    """
    - cxpNumbers is a list as follows: [COMMON_CXP_NUMBER, SC_CXP_NUMBER, DeploymentTemplates_CXP_NUMBER]
        Example: for Trace EA:
        ['CXP9040232', 'CXP9040241', 'CXP9021071'], where
            CXP9040232 = TRACE_EA_COMMON_CXP_NUMBER
            CXP9040241 = TRACE_EA_SC_CXP_NUMBER
            CXP9021071 = TRACE_EA_DeploymentTemplates_CXP_NUMBER
    - localPathToBinaries is the path where the installation SDP files are stored on the local file system.
        If it is set to None, it means that the files do not need to be copied to the target.
    """
    logger.debug('enter installTraceComp')

    global traceEaDtCxpNum
    global traceCcDtCxpNum

    if localPathToBinaries != None:
        # Copy files to target
        result = misc_lib.execCommand('ls %s/*' %localPathToBinaries)
        if result[0] != 'SUCCESS':
            logger.debug('leave installTraceComp')
            return result

        fileList = result[1].split()
        result = comsa_lib.copyFilesToTarget(fileList, pathOnTarget)
        if result[0] != 'SUCCESS':
            logger.debug('leave installTraceComp')
            return result

    result = generateTraceCampaigns(pathOnTarget, cxpNumbers, testConfig)
    if result[0] != 'SUCCESS':
        logger.debug('leave installTraceComp')
        return result

    if cxpNumbers[2] == traceEaDtCxpNum:
        fileNameSubstringInstall = '_Install' # Trace EA
        fileNameSubstringCommon = '_Common' # Trace EA
    elif cxpNumbers[2] == traceCcDtCxpNum:
        fileNameSubstringInstall = '-INSTALL' # Trace CC
        fileNameSubstringCommon = '-COMMON' # Trace CC
    fileNameSubstringSc = 'SC'

    pattern = '%s-%s' %(fileNameSubstringInstall, cxpNumbers[2])
    result = findSdpFileMatchingPattern(pathOnTarget, pattern, 1)
    if result[0] != 'SUCCESS':
        logger.debug('leave installTraceComp')
        return result
    installSdp = result[1]

    pattern = '%s-%s' %(fileNameSubstringCommon, cxpNumbers[0])
    result = findSdpFileMatchingPattern(pathOnTarget, pattern, 1)
    if result[0] != 'SUCCESS':
        logger.debug('leave installTraceComp')
        return result
    commonSdp = result[1]

    pattern = '%s-%s' %(fileNameSubstringSc, cxpNumbers[1])
    result = findSdpFileMatchingPattern(pathOnTarget, pattern, 1)
    if result[0] != 'SUCCESS':
        logger.debug('leave installTraceComp')
        return result
    scSdp = result[1]

    result = comsa_lib.importSdpPackage('%s/%s' %(pathOnTarget, commonSdp))
    if result[0] != 'SUCCESS':
        logger.debug('leave installTraceComp')
        return result

    result = comsa_lib.installComp(pathOnTarget, scSdp, installSdp, compName, createBackup = False, rollingUpgrade = rollingUpgrade)
    if result[0] != 'SUCCESS':
        logger.debug('leave installTraceComp')
        return result

    logger.debug('leave installTraceComp')
    return ('SUCCESS', 'Trace component %s installed' %compName)

def generateTraceCampaigns(pathOnTarget, cxpNumbers, testConfig):
    logger.debug('enter generateTraceCampaigns')

    global traceEaDtCxpNum
    global traceCcDtCxpNum

    numberOfSCs = len(testConfig['controllers'])
    numberOfPLs = len(testConfig['payloads'])

    fileNameSubstring = ''
    # This hard-coding is needed to not have separate installation methods for Trace EA and Trace CC
    if cxpNumbers[2] == traceEaDtCxpNum:
        fileNameSubstring = '_All' # Trace EA
    elif cxpNumbers[2] == traceCcDtCxpNum:
        fileNameSubstring = '-ALL' # Trace CC

    cmd = 'chmod +x %s/*.sh' %pathOnTarget
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave generateTraceCampaigns')
        return result

    cmd = 'cd %s; ls *%s-%s*.sdp.sh' %(pathOnTarget, fileNameSubstring, cxpNumbers[2])
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave generateTraceCampaigns')
        return result
    if len(result[1].splitlines()) != 1:
        logger.debug('leave generateTraceCampaigns')
        return ('ERROR', 'Expected exactly one match when searching for deployment template generator script. Found: %s' %result[1])
    deplTemplateScript = result[1]

    cmd = 'cd %s && ./%s %d %d' %(pathOnTarget, deplTemplateScript, numberOfSCs, numberOfPLs)
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave generateTraceCampaigns')
        return result
    elif result[1] != '':
        logger.debug('leave generateTraceCampaigns')
        return ('ERROR', 'Expected an empty response to the generate campaign command. Received: %s' %result[1])

    logger.debug('leave generateTraceCampaigns')
    return ('SUCCESS', 'OK')

def findSdpFileMatchingPattern(pathOnTarget, pattern, expectedNumMatches = None):
    logger.debug('enter findSdpFileMatchingPattern')

    cmd = 'cd %s && ls *%s*.sdp' %(pathOnTarget, pattern)
    result = ssh_lib.sendCommand(cmd)
    if result[0] != 'SUCCESS':
        logger.debug('leave findSdpFileMatchingPattern')
        return result

    if 'ls: cannot access' in result[1]:
        logger.debug('leave findSdpFileMatchingPattern')
        return ('ERROR', 'No file found matching pattern %s under %s.' %(pattern, pathOnTarget))


    if expectedNumMatches == None:
        logger.debug('leave findSdpFileMatchingPattern')
        return (result[0], result[1].splitlines())
    else:
        if len(result[1].splitlines()) == expectedNumMatches:
            if expectedNumMatches == 1:
                logger.debug('leave findSdpFileMatchingPattern')
                return (result[0], result[1])
            else:
                logger.debug('leave findSdpFileMatchingPattern')
                return (result[0], result[1].splitlines())
        else:
            logger.debug('leave findSdpFileMatchingPattern')
            return ('ERROR', 'Expected exactly %d matches for the file pattern "%s" under %s. Found: %d.' \
                    %(expectedNumMatches, pattern, pathOnTarget, len(result[1].splitlines())))


def uninstallTraceComp(testConfig, localPathToBinaries, pathOnTarget, cxpNumbers, compName, skipGeneratingCampaign = False, rollingUpgrade = False):
    logger.debug('enter uninstallTraceComp')
    """
    - cxpNumbers is a list as follows: [COMMON_CXP_NUMBER, SC_CXP_NUMBER, DeploymentTemplates_CXP_NUMBER]
        Example: for Trace EA:
        ['CXP9040232', 'CXP9040241', 'CXP9021071'], where
            CXP9040232 = TRACE_EA_COMMON_CXP_NUMBER
            CXP9040241 = TRACE_EA_SC_CXP_NUMBER
            CXP9021071 = TRACE_EA_DeploymentTemplates_CXP_NUMBER
    localPathToBinaries is the path where the installation SDP files are stored on the local file system.
        If it is set to None, it means that the files do not need to be copied to the target.
    """


    global traceEaDtCxpNum
    global traceCcDtCxpNum

    if localPathToBinaries != None:
        # Copy files to target
        result = misc_lib.execCommand('ls %s/*' %localPathToBinaries)
        if result[0] != 'SUCCESS':
            logger.debug('leave uninstallTraceComp')
            return result

        fileList = result[1].split()
        result = comsa_lib.copyFilesToTarget(fileList, pathOnTarget)
        if result[0] != 'SUCCESS':
            logger.debug('leave uninstallTraceComp')
            return result

    if skipGeneratingCampaign == False:
        result = generateTraceCampaigns(pathOnTarget, cxpNumbers, testConfig)
        if result[0] != 'SUCCESS':
            logger.debug('leave uninstallTraceComp')
            return result

    if cxpNumbers[2] == traceEaDtCxpNum:
        fileNameSubstring = '_Remove' # Trace EA
    elif cxpNumbers[2] == traceCcDtCxpNum:
        fileNameSubstring = '-REMOVE' # Trace CC
    pattern = '%s-%s' %(fileNameSubstring, cxpNumbers[2])
    result = findSdpFileMatchingPattern(pathOnTarget, pattern, 1)
    if result[0] != 'SUCCESS':
        logger.debug('leave uninstallTraceComp')
        return result
    removeSdp = result[1]

    result = comsa_lib.installComp(pathOnTarget, '', removeSdp, compName, createBackup = False, removeCampaign = True, rollingUpgrade = rollingUpgrade)
    if result[0] != 'SUCCESS':
        logger.debug('leave uninstallTraceComp')
        return result

    logger.debug('leave ununinstallTraceComp')
    return ('SUCCESS', 'Trace component %s uninstalled' %compName)

