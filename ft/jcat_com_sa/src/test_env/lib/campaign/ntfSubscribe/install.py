#!/usr/bin/env jython

""" This module creates a campaign.xml to install ntfSubscribeApp.
Number of PL nodes of target node must be given.
Number of SIs and SGs is optional, default value is 100 SIs and 1 SG.
"""
import re

class ntfSubscribeInstallCampaignCreator():
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
        return ('SUCCESS', 'ntfSubscribeApp install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:///tmp/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-NtfSubscribeAppInstall">
  <campaignInfo>
    <campaignPeriod saSmfCmpgExpectedTime="600000000"/>
  </campaignInfo>"""

    def BaseTypes(self):
        self.camp=self.camp+"""
  <campaignInitialization> 
    <addToImm>
      <amfEntityTypes>
        <AppBaseType safAppType="safAppType=ntfSubscribeAppAppType">
          <AppType safVersion="safVersion=1.0.0">
            <serviceGroupType
              saAmfApptSGTypes="safVersion=1.0.0,safSgType=ntfSubscribeAppSgType" />
          </AppType>
        </AppBaseType>

        <SGBaseType safSgType="safSgType=ntfSubscribeAppSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ntfSubscribeAppSuType" />
            <redundancy saAmfSgtRedundancyModel="4" />
            <compRestart saAmfSgtDefCompRestartProb="100000"
              saAmfSgtDefCompRestartMax="3" />
            <suRestart saAmfSgtDefSuRestartProb="20000"
              saAmfSgtDefSuRestartMax="3" />
            <autoAttrs safAmfSgtDefAutoAdjust="0"
              safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000" />
          </SGType>
        </SGBaseType>

        <ServiceBaseType safSvcType="safSvcType=ntfSubscribeAppSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType
              safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType" />
          </ServiceType>
        </ServiceBaseType>

        <CSBaseType safCSType="safCSType=ntfSubscribeAppCsType">
          <CSType safVersion="safVersion=1.0.0" />
        </CSBaseType>

        <SUBaseType safSuType="safSuType=ntfSubscribeAppSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0"
              saAmfSutDefSUFailover="1" />
            <componentType saAmfSutMinNumComponents="1"
              safMemberCompType="safMemberCompType=safVersion=APPVER\,safCompType=ntfSubscribeAppCompType" />
            <supportedSvcType
              saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ntfSubscribeAppSvcType" />
          </SUType>
        </SUBaseType>

        <CompBaseType safCompType="safCompType=ntfSubscribeAppCompType">
          <CompType safVersion="safVersion=APPVER">
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
              saAmfHealthcheckMaxDuration="60000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-APPVER" />
          </CompType>
        </CompBaseType>
      </amfEntityTypes>
    </addToImm>
    <!--campInitAction>
      <doCliCommand   command="cmw-partial-backup-register" args="<SDP-NAME> <backup-script>" />
      <undoCliCommand command="cmw-partial-backup-unregister" args="<SDP-NAME> <backup-script>"/>
      <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster"/>
    </campInitAction -->
  </campaignInitialization>
"""

    def UpgradeProcedureHead(self):
        self.camp=self.camp+"""
  <upgradeProcedure safSmfProcedure="safSmfProc=SingleStepProc">
    <outageInfo>
      <acceptableServiceOutage>
        <all />
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000" />
    </outageInfo>
"""

    def UpgradeProcInitAction(self):
        self.camp=self.camp+"""
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfApplication" parentObjectDN="=">
          <attribute name="safApp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safApp=ntfSubscribeApp</value>
          </attribute>
          <attribute name="saAmfAppType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safAppType=ntfSubscribeAppAppType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSG" parentObjectDN="safApp=ntfSubscribeApp">
          <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSg=ntfSubscribeApp</value>
          </attribute>
          <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSgType=ntfSubscribeAppSgType</value>
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
        <create objectClassName="SaAmfSI" parentObjectDN="safApp=ntfSubscribeApp">
          <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSi=SC-NWayActive</value>
          </attribute>
          <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSvcType=ntfSubscribeAppSvcType</value>
          </attribute>
          <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
            <value>safSg=ntfSubscribeApp,safApp=ntfSubscribeApp</value>
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
          parentObjectDN="safSi=SC-NWayActive,safApp=ntfSubscribeApp">
          <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
            <value>safCsi=ntfSubscribeApp</value>
          </attribute>
          <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safCSType=ntfSubscribeAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCSIAttribute"
          parentObjectDN="safCsi=ntfSubscribeApp,safSi=SC-NWayActive,safApp=ntfSubscribeApp">
          <attribute name="safCsiAttr" type="SA_IMM_ATTR_SASTRINGT">
            <value>safCsiAttr=logFile</value>
          </attribute>
          <attribute name="saAmfCSIAttriValue" type="SA_IMM_ATTR_SASTRINGT">
            <value>/home/test/ntfSubscribeApp/notif.log</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSU"
          parentObjectDN="safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSu=SC-1</value>
          </attribute>
          <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSuType=ntfSubscribeAppSuType</value>
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
          parentObjectDN="safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safComp=ntfSubscribeApp</value>
          </attribute>
          <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=APPVER,safCompType=ntfSubscribeAppCompType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCompCsType"
          parentObjectDN="safComp=ntfSubscribeApp,safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
            <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfHealthcheck"
          parentObjectDN="safComp=ntfSubscribeApp,safSu=SC-1,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
            <value>safHealthcheckKey=ABC123</value>
          </attribute>
          <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
          <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
            <value>60000000000</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>""" % (self.noNodes, self.noNodes)

        if 2 == self.noNodes:
            self.camp = self.camp + """
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSU"
          parentObjectDN="safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSu=SC-2</value>
          </attribute>
          <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSuType=ntfSubscribeAppSuType</value>
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
          parentObjectDN="safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safComp=ntfSubscribeApp</value>
          </attribute>
          <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=APPVER,safCompType=ntfSubscribeAppCompType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCompCsType"
          parentObjectDN="safComp=ntfSubscribeApp,safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
            <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ntfSubscribeAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfHealthcheck"
          parentObjectDN="safComp=ntfSubscribeApp,safSu=SC-2,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp">
          <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
            <value>safHealthcheckKey=ABC123</value>
          </attribute>
          <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
          <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
            <value>60000000000</value>
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
                <byName objectDN="safSu=SC-%d,safSg=ntfSubscribeApp,safApp=ntfSubscribeApp" />""" % i
            i = i + 1
        self.camp=self.camp+"""
              </actedOn>
              <swAdd bundleDN="safSmfBundle=ERIC-NTFSUBSCRIBE-CXP9010000_1-APPVER"  pathnamePrefix="/opt/NTFSUBSCRIBE/bin">"""
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
      <doAdminOperation   objectDN="safSi=SC-NWayActive,safApp=ntfSubscribeApp" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=SC-NWayActive,safApp=ntfSubscribeApp" operationID="SA_AMF_ADMIN_LOCK" />
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


def campaignCreator(fileName, appVer, noNodes ):
    camp   = ntfSubscribeInstallCampaignCreator(fileName, appVer, noNodes)
    result = ntfSubscribeInstallCampaignCreator.create(camp)
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
        
    
    camp  = ntfSubscribeInstallCampaignCreator("NtfSubscribeInstallCampaign.xml", options.appVer, options.noNodes)
    ntfSubscribeInstallCampaignCreator.create(camp)
