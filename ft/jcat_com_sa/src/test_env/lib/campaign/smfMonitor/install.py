#!/usr/bin/env jython

""" This module creates a campaign.xml to install smfMonitorApp.
Number of PL nodes of target node must be given.
Number of SIs and SGs is optional, default value is 100 SIs and 1 SG.
"""
import re

class smfMonitorInstallCampaignCreator():
    def __init__(self, fileName, appVer='P1A01', noNodes = 2):
        self.appVer  = appVer
        self.noNodes = noNodes
        self.camp    = "";
        self.fileName = fileName

    def create(self):

        if self.noNodes > 1:
            self.noNodes = 2
            
        self.CampaignHead()
        self.BaseTypes()
        self.UpgradeProcedureHead()
        self.UpgradeProcInitAction()
        self.UpgradeProcedureMethod()
        self.UpgradeProcWrapup()
        self.UpgradeProcedureTail()
        self.CampaignWrapup()
        self.CampaignTail()

        self.camp = re.sub('APPVER', self.appVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'smfMonitorApp install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:///tmp/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-SmfMonitorAppInstall">
  <campaignInfo>
    <campaignPeriod saSmfCmpgExpectedTime="600000000"/>
  </campaignInfo>"""

    def BaseTypes(self):
        self.camp=self.camp+"""
  <campaignInitialization>
    <addToImm>
      <amfEntityTypes>
        <AppBaseType safAppType="safAppType=smfMonitorAppAppType">
          <AppType safVersion="safVersion=1.0.0">
            <serviceGroupType
              saAmfApptSGTypes="safVersion=1.0.0,safSgType=smfMonitorAppSgType" />
          </AppType>
        </AppBaseType>

        <SGBaseType safSgType="safSgType=smfMonitorAppSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=smfMonitorAppSuType" />
            <redundancy saAmfSgtRedundancyModel="4" />
            <compRestart saAmfSgtDefCompRestartProb="100000"
              saAmfSgtDefCompRestartMax="3" />
            <suRestart saAmfSgtDefSuRestartProb="20000"
              saAmfSgtDefSuRestartMax="3" />
            <autoAttrs safAmfSgtDefAutoAdjust="0"
              safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000" />
          </SGType>
        </SGBaseType>

        <ServiceBaseType safSvcType="safSvcType=smfMonitorAppSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType
              safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=smfMonitorAppCsType" />
          </ServiceType>
        </ServiceBaseType>

        <CSBaseType safCSType="safCSType=smfMonitorAppCsType">
          <CSType safVersion="safVersion=1.0.0" />
        </CSBaseType>

        <SUBaseType safSuType="safSuType=smfMonitorAppSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0"
              saAmfSutDefSUFailover="1" />
            <componentType saAmfSutMinNumComponents="1"
              safMemberCompType="safMemberCompType=safVersion=APPVER\,safCompType=smfMonitorAppCompType" />
            <supportedSvcType
              saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=smfMonitorAppSvcType" />
          </SUType>
        </SUBaseType>

        <CompBaseType safCompType="safCompType=smfMonitorAppCompType">
          <CompType safVersion="safVersion=APPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=smfMonitorAppCsType"
              saAmfCtCompCapability="6" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="10000000000"
              saAmfCtDefCallbackTimeout="6000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="smfMonitorApp_init">
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="smfMonitorApp_init">
              <cmdArgv>cleanup</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-SMFMONITOR-CXP9010002_1-APPVER" />
          </CompType>
        </CompBaseType>
      </amfEntityTypes>
    </addToImm>
  </campaignInitialization>
"""

    def UpgradeProcedureHead(self):
        self.camp=self.camp+"""
  <upgradeProcedure safSmfProcedure="safSmfProc=SingleStepProc">
    <outageInfo>
      <acceptableServiceOutage>
        <all/>
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="600000000"/>
    </outageInfo>"""

    def UpgradeProcInitAction(self):
        self.camp=self.camp+"""
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfApplication" parentObjectDN="=">
          <attribute name="safApp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safApp=smfMonitorApp</value>
          </attribute>
          <attribute name="saAmfAppType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safAppType=smfMonitorAppAppType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSG" parentObjectDN="safApp=smfMonitorApp">
          <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSg=smfMonitorApp</value>
          </attribute>
          <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSgType=smfMonitorAppSgType</value>
          </attribute>
          <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
            <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
          </attribute>
          <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>%d</value>
          </attribute>
          <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
            <value>0</value>
          </attribute>
          <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
            <value>0</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSI" parentObjectDN="safApp=smfMonitorApp">
          <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSi=SC-NWayActive</value>
          </attribute>
          <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSvcType=smfMonitorAppSvcType</value>
          </attribute>
          <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
            <value>safSg=smfMonitorApp,safApp=smfMonitorApp</value>
          </attribute>
          <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>0</value>
          </attribute>
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>%d</value>
          </attribute>
          <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCSI"
          parentObjectDN="safSi=SC-NWayActive,safApp=smfMonitorApp">
          <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
            <value>safCsi=smfMonitorApp</value>
          </attribute>
          <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safCSType=smfMonitorAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCSIAttribute"
          parentObjectDN="safCsi=smfMonitorApp,safSi=SC-NWayActive,safApp=smfMonitorApp">
          <attribute name="safCsiAttr" type="SA_IMM_ATTR_SASTRINGT">
            <value>safCsiAttr=logFile</value>
          </attribute>
          <attribute name="saAmfCSIAttriValue" type="SA_IMM_ATTR_SASTRINGT">
            <value>/home/test/smfMonitorApp/smfmon.log</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSU"
          parentObjectDN="safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSu=SC-1</value>
          </attribute>
          <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSuType=smfMonitorAppSuType</value>
          </attribute>
          <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
            <value>safAmfNode=SC-1,safAmfCluster=myAmfCluster</value>
          </attribute>
          <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
            <value>3</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfComp"
          parentObjectDN="safSu=SC-1,safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safComp=smfMonitorApp</value>
          </attribute>
          <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=APPVER,safCompType=smfMonitorAppCompType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCompCsType"
          parentObjectDN="safComp=smfMonitorApp,safSu=SC-1,safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
            <value>safSupportedCsType=safVersion=1.0.0\,safCSType=smfMonitorAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfHealthcheck"
          parentObjectDN="safComp=smfMonitorApp,safSu=SC-1,safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
            <value>safHealthcheckKey=ABC123</value>
          </attribute>
          <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
          <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>""" % (self.noNodes, self.noNodes)

        if 2 == self.noNodes:
            self.camp = self.camp + """
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSU"
          parentObjectDN="safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSu=SC-2</value>
          </attribute>
          <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSuType=smfMonitorAppSuType</value>
          </attribute>
          <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
          <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
            <value>safAmfNode=SC-2,safAmfCluster=myAmfCluster</value>
          </attribute>
          <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
            <value>3</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfComp"
          parentObjectDN="safSu=SC-2,safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safComp=smfMonitorApp</value>
          </attribute>
          <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=APPVER,safCompType=smfMonitorAppCompType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCompCsType"
          parentObjectDN="safComp=smfMonitorApp,safSu=SC-2,safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
            <value>safSupportedCsType=safVersion=1.0.0\,safCSType=smfMonitorAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfHealthcheck"
          parentObjectDN="safComp=smfMonitorApp,safSu=SC-2,safSg=smfMonitorApp,safApp=smfMonitorApp">
          <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
            <value>safHealthcheckKey=ABC123</value>
          </attribute>
          <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
          <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
"""

    def UpgradeProcedureMethod(self):
        self.camp=self.camp+"""
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit/>
            <activationUnit>
              <actedOn>"""
        i=1
        while i <= self.noNodes:
            self.camp= self.camp + """
                <byName objectDN="safSu=SC-%d,safSg=smfMonitorApp,safApp=smfMonitorApp" />""" % i
            i = i + 1
        self.camp=self.camp+"""
              </actedOn>
              <swAdd bundleDN="safSmfBundle=ERIC-SMFMONITOR-CXP9010002_1-APPVER" pathnamePrefix="/opt/SMFMONITOR/bin">"""
        i=1
        while i <= self.noNodes:
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=SC-%d,safAmfCluster=myAmfCluster" />""" % i
            i = i + 1

        self.camp=self.camp+"""
              </swAdd>
            </activationUnit>
          </forAddRemove>
        </upgradeScope>
        <upgradeStep/>
      </singleStepUpgrade>
    </upgradeMethod>"""

    def UpgradeProcWrapup(self):
        self.camp = self.camp + """
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=SC-NWayActive,safApp=smfMonitorApp" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=SC-NWayActive,safApp=smfMonitorApp" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction>"""

    def UpgradeProcedureTail(self):
        self.camp=self.camp+"""
  </upgradeProcedure>"""

    def CampaignWrapup(self):
        self.camp=self.camp+"""
  <campaignWrapup>
    <waitToCommit/>
    <waitToAllowNewCampaign/>
    <removeFromImm/>
  </campaignWrapup>"""

    def CampaignTail(self):
        self.camp=self.camp+"""
</upgradeCampaign>
"""


def campaignCreator(fileName, appVer, noOfPLs ):
    camp  = smfMonitorInstallCampaignCreator(fileName, appVer, noOfPLs)
    result = smfMonitorInstallCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-n", "--NoNodes", 
                      type="int", dest="noNodes", default = 2,
                      help="Number of nodes, default = 2")

    parser.add_option("-v", "--version",
                      dest="appVer", default="P1A01",
                      help="application version, default = P1A01")


    (options, args) = parser.parse_args()
        
    
    camp  = smfMonitorInstallCampaignCreator("SmfMonitorInstallCampaign.xml", options.appVer, options.noNodes)
    smfMonitorInstallCampaignCreator.create(camp)
