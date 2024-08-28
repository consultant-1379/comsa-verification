#!/usr/bin/env jython

""" This module creates a campaign.xml to remove ntfSubscribeApp.
"""
import re

class ntfSubscribeRemoveCampaignCreator():
    def __init__(self, fileName, appVer='P1A01'):
        self.appVer  = appVer
        self.camp    = "";
        self.fileName = fileName
        #print "In __init__: noOfPLs = %d, appVer = '%s', SIs = %d, SGs = %d" % (self.noOfPLs, self.appVer, self.SIs, self.SGs)

    def create(self):
        self.Campaign()

        self.camp = re.sub('APPVER', self.appVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'ntfSubscribeApp remove campaign created')


    def Campaign(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file://SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-NtfSubscribeAppRemove">
  <campaignInfo>
    <campaignPeriod />
  </campaignInfo>
  <campaignInitialization>
    <addToImm />
  </campaignInitialization>
  <upgradeProcedure safSmfProcedure="safSmfProc=Remove" saSmfExecLevel="1">
    <outageInfo>
      <acceptableServiceOutage>
        <all />
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000" />
    </outageInfo>
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit>
              <actedOn>
                <byName objectDN="safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
                <byName objectDN="safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
              </actedOn>
              <swRemove bundleDN="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-APPVER" pathnamePrefix="/opt/NTFSUBSCRIBE/bin">
                <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster" />
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster" />
              </swRemove>
            </deactivationUnit>
            <activationUnit />
          </forAddRemove>
         </upgradeScope>
        <upgradeStep />
      </singleStepUpgrade>
    </upgradeMethod>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=ABC123,safComp=ntfSubscribeApp,safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=ABC123,safComp=ntfSubscribeApp,safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=APPVER,safCompType=ntfSubscribeAppCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType,safComp=ntfSubscribeApp,safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType,safComp=ntfSubscribeApp,safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType,safVersion=APPVER,safCompType=ntfSubscribeAppCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ntfSubscribeApp,safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ntfSubscribeApp,safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsiAttr=logFile,safCsi=ntfSubscribeApp,safSi=SC-NWayActive,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ntfSubscribeApp,safSi=SC-NWayActive,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=SC-NWayActive,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safApp=ntfSubscribeApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType,safVersion=1.0.0,safSvcType=ntfSubscribeAppSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=APPVER\,safCompType=ntfSubscribeAppCompType,safVersion=1.0.0,safSuType=ntfSubscribeAppSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safAppType=ntfSubscribeAppAppType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safCSType=ntfSubscribeAppCsType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSgType=ntfSubscribeAppSgType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSuType=ntfSubscribeAppSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSvcType=ntfSubscribeAppSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=APPVER,safCompType=ntfSubscribeAppCompType" />
      </immCCB>
    </procWrapupAction>
    
  </upgradeProcedure>
  <campaignWrapup>
    <!--campCompleteAction>
      <doCliCommand   command="cmw-partial-backup-unregister" args="<SDP-NAME> <backup-script>"/>
      <undoCliCommand command="cmw-partial-backup-register"   args="<SDP-NAME> <backup-script>" />
      <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster"/>
    </campCompleteAction -->
   <waitToCommit />
    <waitToAllowNewCampaign />
    <removeFromImm>
      <!-- amfEntityTypeDN objectDN="safAppType=ntfSubscribeAppAppType" />
      <amfEntityTypeDN objectDN="safCSType=ntfSubscribeAppCsType" />
      <amfEntityTypeDN objectDN="safCompType=ntfSubscribeAppCompType" />
      <amfEntityTypeDN objectDN="safSgType=ntfSubscribeAppSgType" />
      <amfEntityTypeDN objectDN="safSuType=ntfSubscribeAppSuType" />
      <amfEntityTypeDN objectDN="safSvcType=ntfSubscribeAppSvcType" / -->  
    </removeFromImm>
 
  </campaignWrapup>
</upgradeCampaign>"""



def campaignCreator(fileName, appVer):
    camp  = ntfSubscribeRemoveCampaignCreator(fileName, appVer)
    result = ntfSubscribeRemoveCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-v", "--version",
                      dest="appVer", default="P1A01",
                      help="application version, default = P1A01")


    (options, args) = parser.parse_args()
        
    
    camp  = ntfSubscribeRemoveCampaignCreator("ntfSubscribeRemoveCampaign.xml", options.appVer)
    ntfSubscribeRemoveCampaignCreator.create(camp)
