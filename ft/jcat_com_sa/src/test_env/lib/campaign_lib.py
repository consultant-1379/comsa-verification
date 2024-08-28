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
#############IMPORT##################

from org.apache.log4j import Logger
from java.lang import System
import sys
import os
import string
import lib
import shutil


import campaign.amfMeasure.install   as amfMeasureInstallCampaign
import campaign.amfMeasure.upgrade   as amfMeasureUpgradeCampaign
import campaign.amfMeasure.remove    as amfMeasureRemoveCampaign
#import campaign.amfMeasure.expand    as amfMeasureExpandCampaign
#import campaign.amfMeasure.reduce    as amfMeasureReduceCampaign



import campaign.cmw.upgrade          as cmwUpgradeCampaign
import campaign.ntfSubscribe.install as ntfSubscribeInstallCampaign
import campaign.ntfSubscribe.remove  as ntfSubscribeRemoveCampaign
import campaign.ntfSubscribe.upgrade as ntfSubscribeUpgradeCampaign
import campaign.ntfSubscribe.expand  as ntfSubscribeExpandCampaign
import campaign.smfMonitor.install   as smfMonitorInstallCampaign
import campaign.smfMonitor.expand    as smfMonitorExpandCampaign
import campaign.testApp.install      as testAppInstallCampaign
import campaign.testApp.expand       as testAppExpandCampaign
import campaign.testApp.reduce       as testAppReduceCampaign
import campaign.testApp.remove       as testAppRemoveCampaign
import campaign.testApp.upgrade      as testAppUpgradeCampaign
import campaign.testApp.addcompandsg      as testAppAddCompAndSgCampaign
import campaign.pmConsumer.install   as pmConsumerInstallCampaign
import campaign.pmProducer.install   as pmProducerInstallCampaign

import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException


import omp.tf.ssh_lib as ssh_lib
import omp.tf.hw_lib as hw_lib
import omp.tf.ethswitch_lib as ethswitch_lib
import omp.tf.misc_lib as misc_lib
import coremw.notification_lib as notification_lib
import coremw.testapp_lib as testapp_lib
import coremw.saf_lib as saf_lib

def setUp(logLevel, currentSut):
    global ethswitch_lib
    global hw_lib
    global ssh_lib
    global misc_lib
    global testapp_lib
    global logger
    global targetData
    global logDir

    #global amfNodeNameSeparator

    logger = Logger.getLogger('campaign_lib')
    logger.setLevel(logLevel)
    logger.info("campaign_lib: Initiating!")
    logDir = System.getProperty("logdir")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    return


def tearDown():
    #logger_lib.logMessage("lib: Bye bye !!", logLevel='debug')
    logger.debug("campaign_lib: bye, bye!")
    return

#############################################################################################
# campaign_lib functions
#############################################################################################

def createSmfMonitorAppInstallSdp(numOfNodes, cxpArchive = ''):
#################################
    cxpToCopy=[]
    cxpToVerify=[]
    cxpNames = 'ERIC-SMFMONITOR-CXP9010002_1'

    campaignName = "ERIC-SmfMonitorAppInstall"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    cmd='packageinfo %s/ERIC-SMFMONITOR-CXP9010002_1.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9010002_1-')
        if -1 != res:
            ver=tmp[res+13:res+18]
            cxpToVerify.append('ERIC-SMFMONITOR-CXP9010002_1-%s Used' % ver)
            result = smfMonitorInstallCampaign.campaignCreator(pathToCampXmlfile, ver, numOfNodes)

            if 'SUCCESS' == result[0]:
                result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
                if 'SUCCESS' == result[0]:
                    result=('SUCCESS', '%s.sdp' % campaignName)
        else:
            result=('ERROR', 'Failed to extract version of SMFMONITOR')
    
    shutil.rmtree(campaignDir)
    return result

def createSmfMonitorAppExpandSdp(cxpArchive = ''):
#################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-SmfMonitorAppExpand"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    cmd='packageinfo %s/ERIC-SMFMONITOR-CXP9010002_1.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9010002_1-')
        if -1 != res:
            appVer=tmp[res+13:res+18]
   
    if 'SUCCESS' == result[0]:
        result = smfMonitorExpandCampaign.campaignCreator(pathToCampXmlfile, appVer)

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
        if 'SUCCESS' == result[0]:
            result=('SUCCESS', '%s.sdp' % campaignName)
    
    shutil.rmtree(campaignDir)
    return result

"""
    workspace =   os.environ['MY_REPOSITORY']
    cxpArchive = '/vobs/coremw/release/cxp_archive'
    cxpNames = 'ERIC-SMFMONITOR-CXP9010002_1'
    campaignName = 'ERIC-SmfMonitorApp'
    campaignScript = 'install/generate_smfMonitorApp_install_campaign.sh'
    
    cxpToCopy=[]
    cxpToVerify=[]

    cmd = 'if [ -e %s/%s.sdp ]; then rm %s/%s.sdp; fi' % (cxpArchive, campaignName, cxpArchive, campaignName)
    misc_lib.execCommand(cmd)

    cmd='packageinfo %s/ERIC-SMFMONITOR-CXP9010002_1.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9010002_1-')
        if -1 != res:
            ver=tmp[res+13:res+18]
            cxpToVerify.append('ERIC-SMFMONITOR-CXP9010002_1-%s Used' % ver)
            
        pathToCampXmlfile='/tmp/campaign.xml'
        cmd = '%s/apps/smfCampains/smfMonitorApp/%s' % (workspace, campaignScript) 
        cmd = '%s --ver %s' % (cmd, ver)
        cmd = '%s > %s' % ( cmd,  pathToCampXmlfile)
        
        result = misc_lib.execCommand(cmd)

        if 'SUCCESS' == result[0]:
            result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName)
            if 'SUCCESS' == result[0]:
                 result = ('SUCCESS','ERIC-SmfMonitorApp.sdp')
            else:
                 result = ('SUCCESS','Failed to create ERIC-SmfMonitorApp.sdp')

    
    
    return result
"""

def createNtfSubscribeAppInstallSdp(numOfNodes, cxpArchive = ''):
####################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-NtfSubscribeAppInstall"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    cmd='packageinfo %s/ERIC-NTFSUBSCRIBE-CXP9010000_1.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9010000_1-')
        if -1 != res:
            ver=tmp[res+13:res+18]
            cxpToVerify.append('ERIC-NTFSUBSCRIBE-CXP9010000_1-%s Used' % ver)
            result = ntfSubscribeInstallCampaign.campaignCreator(pathToCampXmlfile, ver, numOfNodes)
    
            if 'SUCCESS' == result[0]:
                result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
                if 'SUCCESS' == result[0]:
                    result=('SUCCESS', '%s.sdp' % campaignName)
        else:
            result=('ERROR', 'Failed to extract version of NTFSUBSCRIBE')
    
    shutil.rmtree(campaignDir)
    return result


def createTestAppInstallSdp(numOfNodes, cxpArchive = ''):
####################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-TestAppInstall"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)
        
    cmd='packageinfo %s/Test_App*sles11.x86_64.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9013968_3-')
        if -1 != res:
            tappVer=tmp[res+13:res+18]
       
        tgenVer = 'xxx'
        tgcVer = 'zzz'

        result = testAppInstallCampaign.campaignCreator(pathToCampXmlfile, numOfNodes, tappVer, tgenVer, tgcVer)
      
        
        cxpToVerify.append('/ERIC-Test_App-CXP9013968_3-%s Used' % tappVer)
       

        cxpToCopy.append('/ERIC-Test_App-CXP9013968_3')
      
        
        if 'SUCCESS' == result[0]:
            result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
            if 'SUCCESS' == result[0]:
                result=('SUCCESS', '%s.sdp' % campaignName)
    
    shutil.rmtree(campaignDir)
    return result, cxpToCopy, cxpToVerify
    
def createTestAppExpandSdp(fromNumOfNodes, toNumOfNodes, cxpArchive = ''):
####################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-TestAppExpand"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    result = ssh_lib.sendCommand('cmw-repository-list')
    try:
        tappVer=result[1].split('ERIC-Test_App-CXP9013968_3-')[1].split(' Used')[0]
    except:
        result = ('ERROR','Could not extract version of installed software')
    
    if 'SUCCESS' == result[0]:
        result = testAppExpandCampaign.campaignCreator(pathToCampXmlfile, fromNumOfNodes, toNumOfNodes, tappVer)

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
        if 'SUCCESS' == result[0]:
            result=('SUCCESS', '%s.sdp' % campaignName)
    
    shutil.rmtree(campaignDir)
    return result

def createTestAppReduceSdp(fromNumOfNodes, toNumOfNodes, cxpArchive = ''):
####################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-TestAppReduce"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    result = ssh_lib.sendCommand('cmw-repository-list')
    try:
        tappVer=result[1].split('ERIC-Test_App-CXP9013968_3-')[1].split(' Used')[0]
    except:
        result = ('ERROR','Could not extract version of installed software')
    
    if 'SUCCESS' == result[0]:
        result = testAppReduceCampaign.campaignCreator(pathToCampXmlfile, fromNumOfNodes, toNumOfNodes, tappVer)
    
    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
        if 'SUCCESS' == result[0]:
            result=('SUCCESS', '%s.sdp' % campaignName)

    shutil.rmtree(campaignDir)
    return result

def createTestAppRemoveSdp(numOfNodes, cxpArchive = ''):
####################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-TestAppRemove"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    result = ssh_lib.sendCommand('cmw-repository-list')
    try:
        tappVer=result[1].split('ERIC-TA_TAPP-CXP9013968_3-')[1].split(' Used')[0]
        tgenVer=result[1].split('ERIC-TA_TGEN-CXP9013968_4-')[1].split(' Used')[0]
        tgcVer=result[1].split('ERIC-TA_TGC-CXP9013968_5-')[1].split(' Used')[0]
    except:
        result = ('ERROR','Could not extract version of installed software')
    
    if 'SUCCESS' == result[0]:

        result = testAppRemoveCampaign.campaignCreator(pathToCampXmlfile, numOfNodes, tappVer, tgenVer, tgcVer)

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
        if 'SUCCESS' == result[0]:
            result=('SUCCESS', '%s.sdp' % campaignName)
    
    shutil.rmtree(campaignDir)
    return result

def createTestAppUpgradeSdp(upgradeMethod, noOfNodes, cxpArchive = ''):
#################################
    if "RoNo" == upgradeMethod:
        campaignName  = "ERIC-TappUpgradeRollingNode"
    elif "SsNo" == upgradeMethod:
        campaignName  = "ERIC-TappUpgradeSingleNode"
    elif "SsSu" == upgradeMethod:
        campaignName  = "ERIC-TappUpgradeSingleSU"

    cxpToVerify=[]
    cxpToCopy=[]
    bundlesToRemove=[] 

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
        
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # New version
    cmd='packageinfo %s/Test_App.sdp' % cxpArchive
    result = misc_lib.execCommand (cmd)
    if 'ERROR' == result[0]:
        return result, cxpToCopy, cxpToVerify, bundlesToRemove
        
    tmp=result[1]
    res=string.find(tmp, 'CXP9013968_3-')
    if 0 != res:
        tappVer=tmp[res+13:res+18]
   

    # old version
    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result, cxpToVerify, bundlesToRemove 

    try:
        oldTappVer=result[1].split('ERIC-Test_App-CXP9013968_3-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Failed to extract installed Test App revision numbers')

    if 'ERROR' == result[0]:
        return result, cxpToCopy, cxpToVerify, bundlesToRemove

    if oldTappVer == tappVer:
        result = ('ERROR', 'New version of testApp components are/is the same as old testApp component, forgot cmwbuild all?')
        return result, cxpToCopy, cxpToVerify, bundlesToRemove 

    # create campaign
    result = testAppUpgradeCampaign.campaignCreator(pathToCampXmlfile, oldTappVer, tappVer, upgradeMethod, noOfNodes)

    bundlesToRemove.append('ERIC-Test_App-CXP9013968_3-%s' % oldTappVer)
 

    cxpToVerify.append('ERIC-Test_App-CXP9013968_3-%s' % tappVer)
    
    cmd = 'ls %s/ | grep Test_App.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    temp = result[1].strip()
    temp = temp[0:len(temp) - 4]
    cxpToCopy.append(temp)
    
            
    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    return result, cxpToCopy, cxpToVerify, bundlesToRemove 
 
def createTestAppAddCompAndSgSdp(cxpArchive = '', numOfNodes = 4):
####################################
    
    campaignName = 'ERIC-TestAppAddCompAndSg'

    cxpToVerify=[]
    cxpToCopy=[]
    bundlesToRemove=[] 

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
        
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # New version
    cmd='packageinfo %s/Test_App.sdp' % cxpArchive
    result = misc_lib.execCommand (cmd)
    if 'ERROR' == result[0]:
        return result, cxpToCopy, cxpToVerify, bundlesToRemove
        
    tmp=result[1]
    res=string.find(tmp, 'CXP9013968_3-')
    if 0 != res:
        tappVer=tmp[res+13:res+18]
   
    # create campaign
    result = testAppAddCompAndSgCampaign.campaignCreator(pathToCampXmlfile, tappVer, numOfNodes)

    cxpToVerify.append('ERIC-Test_App-CXP9013968_3-%s' % tappVer)
    cmd = 'ls %s/ | grep Test_App.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    temp = result[1].strip()
    temp = temp[0:len(temp) - 4]
    cxpToCopy.append(temp)
    
            
    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    return result, cxpToCopy, cxpToVerify, bundlesToRemove 

def createAmfMeasureAppInstallSdp(numOfNodes, cxpArchive = ''):
#################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-AmfMeasureAppInstall"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    cmd='packageinfo %s/ERIC-AMFMEASURE-CXP9010004_1.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9010004_1-')
        if -1 != res:
            ver=tmp[res+13:res+18]
            cxpToVerify.append('ERIC-AMFMEASURE-CXP9010004_1-%s Used' % ver)
        #result = amfMeasureInstallCampaign.campaignCreator(pathToCampXmlfile, numOfNodes-2, ver, numOfSIs, numOfSGs)
        result = amfMeasureInstallCampaign.campaignCreator(pathToCampXmlfile, numOfNodes, ver)

        if 'SUCCESS' == result[0]:
            result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
            if 'SUCCESS' == result[0]:
                result=('SUCCESS', '%s.sdp' % campaignName)
                
    
    shutil.rmtree(campaignDir)
    return result

def createAmfMeasureAppUpgradeSdp(upgradeMethod , numOfNodes, cxpArchive = ''):
#################################
    cxpToVerify=[]
    bundlesToRemove=[] 

    campaignName = ""
    if "RoNo" == upgradeMethod:
        campaignName  = "ERIC-AmfMeasUpgradeRollingOverNode"
    elif "SsNo" == self.upgradeMethod:
        campaignName  = "ERIC-AmfMeasUpgradeSingleOverNode"
    elif "SsSu" == self.upgradeMethod:
        campaignName  = "ERIC-AmfMeasUpgradeSingleOverSU"

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # New version
    cmd='packageinfo %s/ERIC-AMFMEASURE*' % cxpArchive
    result = misc_lib.execCommand (cmd)
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 
        
    tmp=result[1]
    res=string.find(tmp, 'CXP9010004_1-')
    if 0 != res:
        newVer=tmp[res+13:res+18]
    cxpToVerify.append('ERIC-AMFMEASURE-CXP9010004_1-%s Used' % newVer)
    
    # old version
    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 

    try:
        oldVer=result[1].split('CXP9010004_1-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Exception occured')
    if 'ERROR' == result[0]:
        return result, cxpToVerify, bundlesToRemove 

    if newVer == oldVer:
        result = ('ERROR', 'New version of amfMeasureApp component is the same as old amfMeasureApp component, forgot cmwbuild all?')
        return result, cxpToVerify, bundlesToRemove 

    bundlesToRemove.append('ERIC-AMFMEASURE-CXP9010004_1-%s' % oldVer)

    # create campaign
    result = amfMeasureUpgradeCampaign.campaignCreator(pathToCampXmlfile, oldVer, newVer, upgradeMethod, numOfNodes)

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    return result, cxpToVerify, bundlesToRemove 

def createAmfMeasureAppRemoveSdp(numOfNodes, cxpArchive = ''):
#################################
    logger.debug('entering createAmfMeasureAppRemoveSdp(numOfNodes = %s, cxpArchive = %s)' % (numOfNodes, cxpArchive))
    bundlesToRemove=[] 
    campaignName = 'ERIC-AmfMeasureAppRemove'
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # old version
    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result, bundlesToRemove 
    try:
        oldVer=result[1].split('CXP9010004_1-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Exception occured')

    if 'ERROR' == result[0]:
        return result, bundlesToRemove 

    bundlesToRemove.append('ERIC-AMFMEASURE-CXP9010004_1-%s' % oldVer)
    
    logger.debug('before amfMeasureRemoveCampaign.campaignCreator(%s, %s, %s)' % (pathToCampXmlfile, numOfNodes, oldVer))
    # create campaign
    result = amfMeasureRemoveCampaign.campaignCreator(pathToCampXmlfile, numOfNodes, oldVer)
    logger.debug('after amfMeasureRemoveCampaign.campaignCreator')

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    logger.debug('leaving createAmfMeasureAppRemoveSdp(numOfNodes = %s, cxpArchive = %s)' % (numOfNodes, cxpArchive))
    return result, bundlesToRemove 

def createAmfMeasureAppExpandSdp(fromNumOfNodes, toNumOfNodes, cxpArchive = ''):
#################################
    logger.debug('entering createAmfMeasureAppExpandSdp(fromNumOfNodes = %s, toNumOfNodes = %s, cxpArchive = %s)' % (fromNumOfNodes, toNumOfNodes, cxpArchive))
    campaignName = 'ERIC-AmfMeasureAppExpand'
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # old version
    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result 

    try:
        oldVer=result[1].split('CXP9010004_1-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Exception occured')
    if 'ERROR' == result[0]:
        return result 

    bundlesToRemove=[] 
    bundlesToRemove.append('ERIC-AMFMEASURE-CXP9010004_1-%s' % oldVer)

    # create campaign
    result = amfMeasureRemoveCampaign.campaignCreator(pathToCampXmlfile, fromNumOfNodes, toNumOfNodes, oldVer)

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    logger.debug('leaving createAmfMeasureAppExpandSdp(fromNumOfNodes = %s, toNumOfNodes = %s, cxpArchive = %s)' % (fromNumOfNodes, toNumOfNodes, cxpArchive))
    return result 

def createAmfMeasureAppReduceSdp(fromNumOfNodes, toNumOfNodes, cxpArchive = ''):
#################################
    logger.debug('entering createAmfMeasureAppReduceSdp(fromNumOfNodes = %s, toNumOfNodes = %s, cxpArchive = %s)' % (fromNumOfNodes, toNumOfNodes, cxpArchive))
    campaignName = 'ERIC-AmfMeasureAppReduce'
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # old version
    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result 
    try:
        oldVer=result[1].split('CXP9010004_1-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Exception occured')
    if 'ERROR' == result[0]:
        return result 

    # create campaign
    result = amfMeasureReduceCampaign.campaignCreator(pathToCampXmlfile, fromNumOfNodes, toNumOfNodes, oldVer)

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    logger.debug('leaving createAmfMeasureAppReduceSdp(fromNumOfNodes = %s, toNumOfNodes = %s, cxpArchive = %s)' % (fromNumOfNodes, toNumOfNodes, cxpArchive))
    return result 




def createCmwUpgradeSdp(upgradeMethod, cxpArchive, numOfNodes=2):
#################################

    campaignName=""
    if "RoNo" == upgradeMethod:    
        campaignName = "ERIC-CMWRollingOverNode"
    elif "RoTe" == upgradeMethod:    
        campaignName = "ERIC-CMWRollingOverNodeWithTemplate"
    elif "SsNo1" == upgradeMethod:    
        campaignName = "ERIC-CMWSinglestepOverNode1"
    elif "SsNo2" == upgradeMethod:    
        campaignName = "ERIC-CMWSinglestepOverNode2"

    cxpToVerify=[]
    bundlesToRemove=[] 

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    if "RoTe" == upgradeMethod:
        pathToCampXmlfile='%s/campaign.template.xml' % campaignDir
    else:
        pathToCampXmlfile='%s/campaign.xml' % campaignDir
        
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # New versions
    cmd='packageinfo %s/COREMW* | grep ^PACKAGE ' % cxpArchive
    result = misc_lib.execCommand (cmd)
    if "ERROR" == result[0]:
        return ('ERROR', 'Failed to extract new opensaf version number'), campaignName, cxpToVerify, bundlesToRemove
    
    tmp=result[1]
    res=string.find(tmp, 'CXP9017566_1-')
    if 0 != res:
        commonVer=tmp[res+13:res+18]
    res=string.find(tmp, 'CXP9017656_1-')
    if 0 != res:
        opensafVer=tmp[res+13:res+18]
    res=string.find(tmp, 'CXP9017565_1-')
    if 0 != res:
        scVer=tmp[res+13:res+18]

    # Old versions
    result = ssh_lib.sendCommand('cmw-repository-list|grep COREMW')
    if "ERROR" == result[0]:
        return ('ERROR', 'Failed to extract installed opensaf version number'), campaignName, cxpToVerify, bundlesToRemove
    try:
        oldScVer=result[1].split('ERIC-COREMW_SC-CXP9017565_1-')[1].split(' Used')[0]
        oldOpensafVer=result[1].split('ERIC-COREMW_OPENSAF-CXP9017656_1-')[1].split(' Used')[0]
        oldCommonVer =result[1].split('ERIC-COREMW_COMMON-CXP9017566_1-')[1].split(' Used')[0]
    except:
        return ('ERROR', 'Failed to extract installed CMW revision numbers'), campaignName, cxpToVerify, bundlesToRemove
        
    oldSafVer="HEJ"
    result = ssh_lib.getTimeout()
    defTimeout = result[1]
    ssh_lib.setTimeout(120)
    result = ssh_lib.sendCommand('immfind | egrep "^safVersion=.*,safCompType=OpenSafCompTypeNTF"')
    ssh_lib.setTimeout(defTimeout)
    try:
        #safVersion=4.0.0,safCompType=OpenSafCompTypeNTF
        oldSafVer=result[1].split('=')[1].split(',')[0]
    except:
        return ('ERROR', 'Failed to extract installed opensaf version number'), campaignName, cxpToVerify, bundlesToRemove

    
    if oldCommonVer == commonVer or oldOpensafVer == opensafVer or oldScVer == scVer:
        return ('ERROR', 'New version of CMW component is the same as old CMW component, forgot cmwbuild all?'), "", [], []
    
    bundlesToRemove.append('ERIC-COREMW_COMMON-CXP9017566_1-%s' % oldCommonVer)
    bundlesToRemove.append('ERIC-COREMW_OPENSAF-CXP9017656_1-%s'% oldOpensafVer)
    bundlesToRemove.append('ERIC-COREMW_SC-CXP9017565_1-%s'     % oldScVer)

    cxpToVerify.append('ERIC-COREMW_COMMON-CXP9017566_1-%s' % commonVer)
    cxpToVerify.append('ERIC-COREMW_OPENSAF-CXP9017656_1-%s'% opensafVer)
    cxpToVerify.append('ERIC-COREMW_SC-CXP9017565_1-%s'     % scVer)
    
    # create campaign
    result = cmwUpgradeCampaign.campaignCreator(pathToCampXmlfile, upgradeMethod, oldCommonVer, commonVer, oldOpensafVer, opensafVer, oldScVer, scVer, oldSafVer, numOfNodes)
            
    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    return result, campaignName, cxpToVerify, bundlesToRemove 

def createNtfSubscribeAppUpgradeSdp(upgradeMethod, cxpArchive = ''):
#################################
    campaignName = "ERIC-NtfSubscribeAppUpgrade"

    cxpToVerify=[]
    bundlesToRemove=[] 

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    if "RoTe" == upgradeMethod:
        pathToCampXmlfile='%s/campaign.template.xml' % campaignDir
    else:
        pathToCampXmlfile='%s/campaign.xml' % campaignDir
        
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # New version
    cmd='packageinfo %s/ERIC-NTFSUBSCRIBE*' % cxpArchive
    result = misc_lib.execCommand (cmd)
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 
        
    tmp=result[1]
    res=string.find(tmp, 'CXP9010000_1')
    if 0 != res:
        newVer=tmp[res+13:res+18]
    cxpToVerify.append('ERIC-NTFSUBSCRIBE-CXP9010000_1-%s Used' % newVer)
    
    # old version
    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 

    try:
        oldVer=result[1].split('CXP9010000_1-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Exception occured')
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 

    if newVer == oldVer:
        result = ('ERROR', 'New version of ntfSubscribeApp component is the same as old ntfSubscribeApp component, forgot cmwbuild all?')
        return result, campaignName, cxpToVerify, bundlesToRemove 

    bundlesToRemove.append('ERIC-NTFSUBSCRIBE-CXP9010000_1-%s' % oldVer)

    # create campaign
    result = ntfSubscribeUpgradeCampaign.campaignCreator(pathToCampXmlfile, oldVer, newVer, upgradeMethod)
            
    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    return result, campaignName, cxpToVerify, bundlesToRemove 

def createNtfSubscribeAppExpandSdp(cxpArchive = ''):
#################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-NtfSubscribeAppExpand"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 
    try:
        appVer=result[1].split('CXP9010000_1-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Exception occured')
   
    if 'SUCCESS' == result[0]:
        result = ntfSubscribeExpandCampaign.campaignCreator(pathToCampXmlfile, appVer)

    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
        if 'SUCCESS' == result[0]:
            result=('SUCCESS', '%s.sdp' % campaignName)
    
    shutil.rmtree(campaignDir)
    return result

def createNtfSubscribeAppRemoveSdp(cxpArchive = ''):
###############################
    campaignName = "ERIC-NtfSubscribeAppRemove"

    cxpToVerify=[]
    bundlesToRemove=[] 

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    # old version
    result = ssh_lib.sendCommand('cmw-repository-list')
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 

    try:
        oldVer=result[1].split('CXP9010000_1-')[1].split(' Used')[0]
    except:
        result = ('ERROR', 'Exception occured')
    if 'ERROR' == result[0]:
        return result, campaignName, cxpToVerify, bundlesToRemove 


    bundlesToRemove.append('ERIC-AMFMEASURE-CXP9010004_1-%s' % oldVer)

    # create campaign
    result = ntfSubscribeRemoveCampaign.campaignCreator(pathToCampXmlfile, oldVer)
            
    if 'SUCCESS' == result[0]:
        result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)

    shutil.rmtree(campaignDir)

    return result, bundlesToRemove 

def testAppInstallSdp(numOfNodes, cxpArchive = '', campaignName = '', campaignScript = '', workspace = '', cxpNames = ''):
#####################
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)

    cxpToCopy=[]
    cxpToVerify=[]
    workspace =   os.environ['MY_REPOSITORY']
    cxpNames = 'ERIC-TA_TAPP-CXP9013968_3,ERIC-TA_TGC-CXP9013968_5,ERIC-TA_TGEN-CXP9013968_4'
    campaignScript = 'generate_testApp_install_campaign.sh'
    campaignName = 'ERIC-TestAppInstall'
    cxpArchive = '/vobs/coremw/release/cxp_archive'
    
    cmd = 'if [ -e %s/%s.sdp ]; then rm %s/%s.sdp; fi' % (cxpArchive, campaignName, cxpArchive, campaignName)
    misc_lib.execCommand(cmd)

    cmd='packageinfo %s/ERIC-TA_T*' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9013968_3-')
        if -1 != res:
            tappVer=tmp[res+13:res+18]
        res=string.find(tmp, 'CXP9013968_5-')
        if -1 != res:
            tgcVer=tmp[res+13:res+18]
        res=string.find(tmp, 'CXP9013968_4-')
        if -1 != res:
            tgenVer=tmp[res+13:res+18]

        pathToCampXmlfile='%s/campaign.xml' % campaignDir
        cmd = '%s/apps/smfCampains/testApp/%s' % (workspace, campaignScript) 
        cmd = '%s --verTapp %s' % (cmd, tappVer)
        cmd = '%s --verTgc %s' % ( cmd, tgcVer)
        cmd = '%s --verTgen %s' % ( cmd, tgenVer)
        cmd = '%s -n %d' % ( cmd,  numOfNodes)
        cmd = '%s > %s' % ( cmd,  pathToCampXmlfile)
        result = misc_lib.execCommand(cmd)

        if 'SUCCESS' == result[0]:
            result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
            if 'SUCCESS' == result[0]:
                result = ('SUCCESS','ERIC-TestAppInstall.sdp')
            else:
                result = ('ERROR','Failed to create ERIC-TestAppInstall.sdp')
                
    shutil.rmtree(campaignDir)
                        
    return result

def createPmConsumerAppInstallSdp(numOfNodes, cxpArchive = ''):
####################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-PmConsumerAppInstall"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    cmd='packageinfo %s/ERIC-PMCONSUMER-CXP9010006_1.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9010006_1-')
        if -1 != res:
            ver=tmp[res+13:res+18]
            cxpToVerify.append('ERIC-PMCONSUMER-CXP9010006_1-%s Used' % ver)
            result = pmConsumerInstallCampaign.campaignCreator(pathToCampXmlfile, ver, numOfNodes)
    
            if 'SUCCESS' == result[0]:
                result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
                if 'SUCCESS' == result[0]:
                    result=('SUCCESS', '%s.sdp' % campaignName)
        else:
            result=('ERROR', 'Failed to extract version of PMCONSUMER')
    
    shutil.rmtree(campaignDir)
    return result

def createPmProducerAppInstallSdp(numOfNodes, cxpArchive = ''):
####################################
    cxpToCopy=[]
    cxpToVerify=[]

    campaignName = "ERIC-PmProducerAppInstall"
    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    
    sdpFile="%s/%s.sdp" % (cxpArchive, campaignName)
    if os.path.exists(sdpFile):
        os.remove(sdpFile)

    pathToCampXmlfile='%s/campaign.xml' % campaignDir
    if os.path.exists(pathToCampXmlfile):
        os.remove(pathToCampXmlfile)

    cmd='packageinfo %s/ERIC-PMPRODUCER-CXP9010005_1.sdp' % cxpArchive
    result = misc_lib.execCommand(cmd)
    if 'SUCCESS' == result[0]:
        tmp=result[1]
        res=string.find(tmp, 'CXP9010005_1-')
        if -1 != res:
            ver=tmp[res+13:res+18]
            cxpToVerify.append('ERIC-PMPRODUCERAPP-CXP9010000_1-%s Used' % ver)
            result = pmProducerInstallCampaign.campaignCreator(pathToCampXmlfile, numOfNodes, ver)
    
            if 'SUCCESS' == result[0]:
                result = lib.createCampaignBundle(pathToCampXmlfile, '%s.sdp' % campaignName, cxpArchive)
                if 'SUCCESS' == result[0]:
                    result=('SUCCESS', '%s.sdp' % campaignName)
        else:
            result=('ERROR', 'Failed to extract version of PMPRODUCER')
    
    shutil.rmtree(campaignDir)
    return result

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print 'main'
