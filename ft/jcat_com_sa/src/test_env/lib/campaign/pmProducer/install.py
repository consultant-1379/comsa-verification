#!/usr/bin/env jython

""" This module creates a campaign.xml to install pmProducerApp.
Number of PL nodes of target node must be given.
Number of SIs and SGs is optional, default value is 100 SIs and 1 SG.
"""
import re

class pmProducerInstallCampaignCreator():
    def __init__(self, fileName, blades, appVer='P1A01'):
        self.appVer     = appVer
        self.noOfBlades = int(blades)
        self.camp       = "";
        self.fileName   = fileName

    def create(self):
        self.CampaignHead()
        self.BaseTypes()

        self.UpgradeProcedureMethod()
        self.UpgradeProcedureTail()
        self.CampaignWrapup()
        self.CampaignTail()

        self.camp = re.sub('APPVER', self.appVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'pmProducerApp install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:///tmp/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-PmProducerAppInstall">
  <campaignInfo>
    <campaignPeriod saSmfCmpgExpectedTime="600000000" />
  </campaignInfo>"""

    def BaseTypes(self):
        self.camp=self.camp+"""
  <campaignInitialization>
    <addToImm>
      <amfEntityTypes>
        <AppBaseType safAppType="safAppType=pmProducerAppAppType">
          <AppType safVersion="safVersion=1.0.0">
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=pmProducerAppSgType" />
          </AppType>
        </AppBaseType>

        <SGBaseType safSgType="safSgType=pmProducerAppSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=pmProducerAppSuType" />
            <redundancy saAmfSgtRedundancyModel="3" />
            <compRestart saAmfSgtDefCompRestartMax="10" saAmfSgtDefCompRestartProb="3600000000000" />
            <suRestart saAmfSgtDefSuRestartMax="10" saAmfSgtDefSuRestartProb="43200000000000" />
            <autoAttrs saAmfSgtDefAutoAdjustProb="10000000" safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" />
          </SGType>
        </SGBaseType>

        <ServiceBaseType safSvcType="safSvcType=pmProducerAppSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=pmProducerAppCsType" />
          </ServiceType>
        </ServiceBaseType>

        <CSBaseType safCSType="safCSType=pmProducerAppCsType">
          <CSType safVersion="safVersion=1.0.0" />
        </CSBaseType>

        <SUBaseType safSuType="safSuType=pmProducerAppSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="0" />
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=APPVER\,safCompType=pmProducerAppCompType" />
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=pmProducerAppSvcType" />
          </SUType>
        </SUBaseType>

        <CompBaseType safCompType="safCompType=pmProducerAppCompType">
          <CompType safVersion="safVersion=APPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=pmProducerAppCsType" saAmfCtCompCapability="3" />
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="6000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="pmsv_producer_testapp_script">
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="pmsv_producer_testapp_script">
              <cmdArgv>cleanup</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-PMPRODUCER-CXP9010005_1-APPVER" />
          </CompType>
        </CompBaseType>
      </amfEntityTypes>
    </addToImm>
  </campaignInitialization>

  <upgradeProcedure safSmfProcedure="safSmfProc=SingleStepProc">
    <outageInfo>
      <acceptableServiceOutage>
        <all />
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000" />
    </outageInfo>

    <!-- safApp -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfApplication" parentObjectDN="=">
          <attribute name="safApp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safApp=pmProducerApp</value>
          </attribute>
          <attribute name="saAmfAppType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safAppType=pmProducerAppAppType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <!-- safSg -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSG" parentObjectDN="safApp=pmProducerApp">
          <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSg=NWayActive</value>
          </attribute>
          <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSgType=pmProducerAppSgType</value>
          </attribute>
          <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
            <value>safAmfNodeGroup=AllNodes,safAmfCluster=myAmfCluster</value>
          </attribute>
          <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>0</value>
          </attribute>
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>%d</value>
          </attribute>
          <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>%d</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>""" % (self.noOfBlades, self.noOfBlades)

        self.camp=self.camp+"""

    <!-- safSi -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSI" parentObjectDN="safApp=pmProducerApp">
          <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSi=All-NWayActive</value>
          </attribute>
          <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSvcType=pmProducerAppSvcType</value>
          </attribute>
          <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
            <value>safSg=NWayActive,safApp=pmProducerApp</value>
          </attribute>
          <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>0</value>
          </attribute>
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <!-- safCsi -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCSI" parentObjectDN="safSi=All-NWayActive,safApp=pmProducerApp">
          <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
            <value>safCsi=pmProducerApp</value>
          </attribute>
          <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safCSType=pmProducerAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>""" 


        i = 0
        while i < self.noOfBlades:
            if i < 2:
                bladeName = "SC-%d" % (i + 1)
            else:
                bladeName = "PL-%d" % (i + 1)

            self.camp=self.camp+"""

    <!-- safSu -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSU" parentObjectDN="safSg=NWayActive,safApp=pmProducerApp">
          <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
            <value>safSu=%s</value>
          </attribute>
          <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=1.0.0,safSuType=pmProducerAppSuType</value>
          </attribute>
          <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
          <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
            <value>safAmfNode=%s,safAmfCluster=myAmfCluster</value>
          </attribute>
          <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
            <value>0</value>
          </attribute>
          <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
            <value>3</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <!-- safComp -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfComp" parentObjectDN="safSu=%s,safSg=NWayActive,safApp=pmProducerApp">
          <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
            <value>safComp=pmProducerApp</value>
          </attribute>
          <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safVersion=APPVER,safCompType=pmProducerAppCompType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <!-- safSupportedCsType -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfCompCsType" parentObjectDN="safComp=pmProducerApp,safSu=%s,safSg=NWayActive,safApp=pmProducerApp">
          <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
            <value>safSupportedCsType=safVersion=1.0.0\,safCSType=pmProducerAppCsType</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>

    <!-- safHealthCheckKey -->
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=pmProducerApp,safSu=%s,safSg=NWayActive,safApp=pmProducerApp">
          <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
            <value>safHealthcheckKey=PmsvProducerTestapp</value>
          </attribute>
          <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
          <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
            <value>10000000000</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>""" % (bladeName, bladeName, bladeName, bladeName, bladeName)
            i = i + 1


          
    def UpgradeProcedureMethod(self):
        self.camp=self.camp+"""
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit/>
            <activationUnit>
              <actedOn>
"""
        i=0
        while i < self.noOfBlades:
            if i < 2:
                bladeName = "SC-%d" % (i + 1)
            else:
                bladeName = "PL-%d" % (i + 1)
                
           
            self.camp=self.camp+'                <byName objectDN="safSu=%s,safSg=NWayActive,safApp=pmProducerApp" />\n' % bladeName
            i = i + 1
            
        self.camp=self.camp+"""
              </actedOn>
              <swAdd bundleDN="safSmfBundle=ERIC-PMPRODUCER-CXP9010005_1-APPVER" pathnamePrefix="/opt/PMPRODUCER/bin">
"""
        i=0
        while i < self.noOfBlades:
            if i < 2:
                bladeName = "SC-%d" % (i + 1)
            else:
                bladeName = "PL-%d" % (i + 1)
            self.camp=self.camp+'                <plmExecEnv amfNode="safAmfNode=%s,safAmfCluster=myAmfCluster" />\n' % bladeName
            i = i + 1

        self.camp=self.camp+"""
              </swAdd>
            </activationUnit>
          </forAddRemove>
        </upgradeScope>
        <upgradeStep/>
      </singleStepUpgrade>
    </upgradeMethod>"""

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


def campaignCreator(fileName, noOfBlades, appVer):
    camp  = pmProducerInstallCampaignCreator(fileName, noOfBlades, appVer)
    result = pmProducerInstallCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-n", "--NoOfBlades", 
                      type="int", dest="noOfBlades", default=2,
                      help="Number of Blades, default 2")

    parser.add_option("-v", "--version",
                      dest="appVer", default="P1A01",
                      help="application version, default = P1A01")

    (options, args) = parser.parse_args()
        
    if 2 < options.noOfBlades:
        print "Number of blades (%d) must NOT be more than 2" % options.noOfBlades
        sys.exit(1)
    
    camp  = pmProducerInstallCampaignCreator("campaign.xml", options.noOfBlades, options.appVer)
    pmProducerInstallCampaignCreator.create(camp)
