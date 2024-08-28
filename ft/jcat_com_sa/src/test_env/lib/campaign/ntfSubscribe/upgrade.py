#!/usr/bin/env jython

import re

class ntfSubscribeUpgradeCampaignCreator():
    def __init__(self, fileName, fromVer, toVer, upgradeMethod):
        self.fileName      = fileName
        self.fromVer       = fromVer
        self.toVer         = toVer
        self.upgradeMethod = upgradeMethod
        self.camp          = "";
        
        #print "In __init__: fromVer = '%s', tover = %d" % (self.fromVer, self.toVer)

    def create(self):
        procedureName = ""
        if   "RoCo" == self.upgradeMethod:
            procedureName = "NtfSubscribeAppRollingOverComp"
        elif "RoNo" == self.upgradeMethod:
            procedureName = "NtfSubscribeAppRollingOverNode"
        elif "RoSu" == self.upgradeMethod:
            procedureName = "NtfSubscribeAppRollingOverSU"
        elif "SsCo" == self.upgradeMethod:
            procedureName = "NtfSubscribeAppSinglestepOverComp"
        elif "SsNo" == self.upgradeMethod:
            procedureName = "NtfSubscribeAppSinglestepOverNode"
        elif "SsSu" == self.upgradeMethod:
            procedureName = "NtfSubscribeAppSinglestepOverSU"
        elif "RoTe" == self.upgradeMethod:
            procedureName = "NtfSubscribeAppRollingOverSUWithTemplate"
        else:
            procedureName = "Not Supported: %s" % self.upgradeMethod
            
        self.Campaign("NtfSubscribeAppUpgrade")
        self.ProcInit(procedureName)
        
        if   "RoCo" == self.upgradeMethod or "RoNo" == self.upgradeMethod or "RoSu" == self.upgradeMethod or "RoTe" == self.upgradeMethod:
            self.RollingProcedure()
        elif "SsCo" == self.upgradeMethod or "SsNo" == self.upgradeMethod or "SsSu" == self.upgradeMethod:
            self.SinglestepProcedure()

        if "RoTe" == self.upgradeMethod:
            self.CampaignTailTemplate()
        else:
            self.CampaignTail()

        self.camp = re.sub('OLDVER', self.fromVer, self.camp)
        self.camp = re.sub('NEWVER', self.toVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'ntfSubscribeApp update campaign created')

    def Campaign(self, campaignName):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-%s">
  <campaignInfo>
    <campaignPeriod />
  </campaignInfo>
  <campaignInitialization>
    <addToImm>
      <amfEntityTypes>
        <CompBaseType safCompType="safCompType=ntfSubscribeAppCompType">
          <CompType safVersion="safVersion=NEWVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType"
              saAmfCtCompCapability="5" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="10000000000"
              saAmfCtDefCallbackTimeout="6000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ntfSubscribeApp_init">
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ntfSubscribeApp_init">
              <cmdArgv>cleanup</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-NEWVER" />
          </CompType>
        </CompBaseType>
      </amfEntityTypes>
    </addToImm>
    <callbackAtInit callbackLabel="init_callback" time="10000000000" stringToPass="CAI"></callbackAtInit>
    <callbackAtBackup callbackLabel="backup_callback" time="10000000000" stringToPass="CAB"></callbackAtBackup>
  </campaignInitialization>""" % campaignName

    def ProcInit(self, procedureName):

        self.camp=self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=%s" saSmfExecLevel="1">
    <outageInfo>
      <acceptableServiceOutage>
        <all />
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000" />
    </outageInfo>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ntfSubscribeAppSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWVER\,safCompType=ntfSubscribeAppCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
        <callback callbackLabel="procInitAction_callback" time="10000000000" stringToPass="PIA" />
    </procInitAction>""" % procedureName

    def RollingProcedure(self):
        self.camp=self.camp + """
    <upgradeMethod>
      <rollingUpgrade>
        <upgradeScope>
          <byTemplate>
            <targetNodeTemplate objectDN="safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster">\n"""
        
        if "RoCo" == self.upgradeMethod:
            self.camp=self.camp +"""              <activationUnitTemplate>
                <type objectDN="safVersion=OLDVER,safCompType=ntfSubscribeAppCompType"></type>
              </activationUnitTemplate>\n"""
        if "RoSu" == self.upgradeMethod or "RoTe" == self.upgradeMethod:
            self.camp=self.camp +"""              <activationUnitTemplate>
                <type objectDN="safVersion=1.0.0,safSuType=ntfSubscribeAppSuType" />
              </activationUnitTemplate>\n"""

        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """              <swRemove bundleDN="CMW_GETDN(^safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-OLDVER$)"  pathnamePrefix="/opt/NTFSUBSCRIBE/bin"/>\n"""
        else:
            self.camp=self.camp + """              <swRemove bundleDN="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-OLDVER"  pathnamePrefix="/opt/NTFSUBSCRIBE/bin" />\n"""
            
        self.camp=self.camp + """              <swAdd bundleDN="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-NEWVER" pathnamePrefix="/opt/NTFSUBSCRIBE/bin" />
            </targetNodeTemplate>
            <targetEntityTemplate>\n"""
        
        if "RoNo" == self.upgradeMethod:
            self.camp=self.camp + """              <type objectDN="safVersion=OLDVER,safCompType=ntfSubscribeAppCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">\n"""

        elif "RoCo" == self.upgradeMethod:
            self.camp=self.camp + """              <type objectDN="safVersion=OLDVER,safCompType=ntfSubscribeAppCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">\n"""

        elif "RoSu" == self.upgradeMethod or "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """              <type objectDN="safVersion=1.0.0,safSuType=ntfSubscribeAppSuType" />
              <modifyOperation objectRDN="safComp=ntfSubscribeApp" operation="SA_IMM_ATTR_VALUES_REPLACE">\n"""

        self.camp=self.camp + """                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=ntfSubscribeAppCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </byTemplate>
        </upgradeScope>
        <upgradeStep saSmfStepRestartOption="1" saSmfStepMaxRetry="8" />
      </rollingUpgrade>
    </upgradeMethod>\n"""
        
    def SinglestepProcedure(self):
        self.camp=self.camp + """
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forModify>
            <activationUnit>
              <actedOn>\n"""
        if "SsCo" == self.upgradeMethod:
            self.camp=self.camp + """                <byTemplate>
                  <type objectDN="safVersion=OLDVER,safCompType=ntfSubscribeAppCompType"></type>
                </byTemplate>\n"""

        if "SsSu" == self.upgradeMethod:
            self.camp=self.camp + """                <byTemplate>
                  <type objectDN="safVersion=1.0.0,safSuType=ntfSubscribeAppSuType" />
                </byTemplate>\n"""

        if "SsNo" == self.upgradeMethod:
            self.camp=self.camp + """                <byName objectDN="safAmfNode=SC-1,safAmfCluster=myAmfCluster"/>
                <byName objectDN="safAmfNode=SC-2,safAmfCluster=myAmfCluster"/>\n"""

        self.camp=self.camp + """              </actedOn>
              <swRemove bundleDN="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-OLDVER"  pathnamePrefix="/opt/NTFSUBSCRIBE/bin" />
              <swAdd bundleDN="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-NEWVER" pathnamePrefix="/opt/NTFSUBSCRIBE/bin" />
            </activationUnit>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDVER,safCompType=ntfSubscribeAppCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=ntfSubscribeAppCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </forModify>
        </upgradeScope>
        <upgradeStep saSmfStepRestartOption="1" saSmfStepMaxRetry="8" />
      </singleStepUpgrade>
    </upgradeMethod>\n"""

        
    def CampaignTail(self):
        
        self.camp=self.camp + """    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDVER\,safCompType=ntfSubscribeAppCompType,safVersion=1.0.0,safSuType=ntfSubscribeAppSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDVER,safCompType=ntfSubscribeAppCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType,safVersion=OLDVER,safCompType=ntfSubscribeAppCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=OLDVER,safCompType=ntfSubscribeAppCompType" />
      </immCCB>
    </procWrapupAction>
  </upgradeProcedure>
  <campaignWrapup>
    <campCompleteAction>
      <callback callbackLabel="campCompAction_callback" time="10000000000" stringToPass="CCA" />
    </campCompleteAction>
    <waitToCommit />
    <callbackAtCommit callbackLabel="commit_callback" />
    <campWrapupAction>
      <callback callbackLabel="campWrapupAction_callback" time="10000000000" stringToPass="CWA" />
    </campWrapupAction>
    <waitToAllowNewCampaign />
    <removeFromImm />
  </campaignWrapup>
</upgradeCampaign>
"""

    def CampaignTailTemplate(self):
        
        self.camp=self.camp + """    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=OLDVER[\\\\],safCompType=ntfSubscribeAppCompType,safVersion=1.0.0,safSuType=ntfSubscribeAppSuType$)" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=OLDVER,safCompType=ntfSubscribeAppCompType$)" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=1.0.0[\\\\],safCSType=ntfSubscribeAppCsType,safVersion=OLDVER,safCompType=ntfSubscribeAppCompType$)" />
      </immCCB>
    </procWrapupAction>
  </upgradeProcedure>
  <campaignWrapup>
    <waitToCommit />
    <waitToAllowNewCampaign />
    <removeFromImm />
  </campaignWrapup>
</upgradeCampaign>
"""


def campaignCreator(fileName, fromVer, toVer, upgradeMethod):
    camp  = ntfSubscribeUpgradeCampaignCreator(fileName, fromVer, toVer, upgradeMethod)
    result = ntfSubscribeUpgradeCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-u", "--UpgradeMethod",
                      dest="upgradeMethod", default="RoNo",
                      help="Upgrade method, one of RollingOverNode (RoNo), RollingOverSU (RoSu), RollingOverComp (RoCo), SinglestepOverNode (SsNo), SinglestepOverSU (SsSu), SinglestepOverComp (SsCo) & RollingOverSU with Template (RoTe). Default = RoNo")

    parser.add_option("-f", "--FromVersion",
                      dest="fromVer", default="P1A01",
                      help="application version updating from, default = P1A01")

    parser.add_option("-t", "--ToVersion",
                      dest="toVer", default="P1A02",
                      help="application version updating to, default = P1A02")

    (options, args) = parser.parse_args()

    if "RoCo" != options.upgradeMethod and "RoNo" != options.upgradeMethod and "RoSu" != options.upgradeMethod and "SsCo" != options.upgradeMethod and "SsNo" != options.upgradeMethod and "SsSu" != options.upgradeMethod and "RoTe" != options.upgradeMethod:
        print "Upgrade method not supported: %s" % options.upgradeMethod
        sys.exit(1)
        
    #if 2 > options.noOfPLs:
    #    print "Number of PLs(%d) must be at least 2" % options.noOfPLs
    #    sys.exit(1)


    if "RoTe" != options.upgradeMethod:
        fileName = "%s.template.xml" % options.upgradeMethod
    else:
        fileName = "%s.xml" % options.upgradeMethod
    camp  = ntfSubscribeUpgradeCampaignCreator(fileName, options.fromVer, options.toVer, options.upgradeMethod)
    ntfSubscribeUpgradeCampaignCreator.create(camp)
