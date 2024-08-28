#!/usr/bin/env jython
""" This module creates a campaign.xml to install amfMeasureApp.
Number of PL nodes of target node must be given.
Number of SIs and SGs is optional, default value is 100 SIs and 1 SG.


# redundancy saAmfSgtRedundancyModel=
SA_AMF_2N_REDUNDANCY_MODEL=1
SA_AMF_NPM_REDUNDANCY_MODEL=2
SA_AMF_N_WAY_REDUNDANCY_MODEL=3
SA_AMF_N_WAY_ACTIVE_REDUNDANCY_MODEL=4
SA_AMF_NO_REDUNDANCY_MODEL=5

# SaAmfRecommendedRecoveryT;
SA_AMF_NO_RECOMMENDATION=1
SA_AMF_COMPONENT_RESTART=2
SA_AMF_COMPONENT_FAILOVER=3
SA_AMF_NODE_SWITCHOVER=4
SA_AMF_NODE_FAILOVER=5
SA_AMF_NODE_FAILFAST=6
SA_AMF_CLUSTER_RESET=7
SA_AMF_APPLICATION_RESTART=8
SA_AMF_CONTAINER_RESTART=9

# saAmfCtCompCapability=
SA_AMF_COMP_X_ACTIVE_AND_Y_STANDBY=1
SA_AMF_COMP_X_ACTIVE_OR_Y_STANDBY=2
SA_AMF_COMP_ONE_ACTIVE_OR_Y_STANDBY=3
SA_AMF_COMP_ONE_ACTIVE_OR_ONE_STANDBY=4
SA_AMF_COMP_X_ACTIVE=5
SA_AMF_COMP_1_ACTIVE=6
SA_AMF_COMP_NON_PRE_INSTANTIABLE=7

"""
import re

class amfMeasureInstallCampaignCreator():
    def __init__(self, fileName, noOfBlades, appVer='P1A01', SIs = 1, SGs=1):
        self.appVer  = appVer
        self.noOfBlades = noOfBlades
        self.SIs     = SIs
        self.SGs     = SGs
        self.camp    = "";
        self.fileName = fileName
        #print "In __init__: noOfPLs = %d, appVer = '%s', SIs = %d, SGs = %d" % (self.noOfPLs, self.appVer, self.SIs, self.SGs)

    def create(self):
        self.CampaignHead()
        self.BaseTypes()
        self.UpgradeProcedureHead()

        self.SafApp()

        self.SafSg("AllNodesNWayActive", "AllNodes", self.noOfBlades)

        self.SafSg("SCNoRed", "SCs", 1)
        if 1 < self.noOfBlades:
            self.SafSg("SC2N", "SCs", 2)
        else:
            self.SafSg("SC2N", "SCs", 1)
        
        if 2 < self.noOfBlades:
            self.SafSg("PLNoRed", "PLs", 1)
            if 3 < self.noOfBlades:
                self.SafSg("PL2N", "PLs", 2)
            else:
                self.SafSg("PL2N", "PLs", 1)

        i = 1
        while i <= self.noOfBlades:
            blade='PL-%d' % i
            if 3 > i:
                blade='SC-%d' % i

            if 1 == i:
                self.SafSu("SC-1", "SCNoRed", "AmfMeasAppTypeNoRed")
                self.SafSu("SC-1", "SC2N", "AmfMeasAppType2N")
            
            if 2 == i:
                self.SafSu("SC-2","SC2N", "AmfMeasAppType2N")
                
            if 3 == i:
                self.SafSu("PL-3","PLNoRed", "AmfMeasAppTypeNoRed")
                self.SafSu("PL-3","PL2N", "AmfMeasAppType2N")
                
            if 4 == i:
                self.SafSu("PL-4","PL2N", "AmfMeasAppType2N")

            self.SafSu(blade,"AllNodesNWayActive", "AmfMeasAppTypeNWayActive")
            i = i + 1



        self.SafSi("AllNodesNWayActive", "AllNodesNWayActive", self.noOfBlades)

        if 1 < self.noOfBlades:
            self.SafSi("SCNoRed", "SCNoRed")
            self.SafSi("SC2N", "SC2N")

        if 2 < self.noOfBlades:
            self.SafSi("PLNoRed", "PLNoRed")
            self.SafSi("PL2N", "PL2N")


        self.UpgradeProcedureMethodHead()
        i = 1
        while i <= self.noOfBlades:
            blade='PL-%d' % i
            if 3 > i:
                blade='SC-%d' % i

            if 1 == i:
                self.UpgradeProcedureMethodActOn("SC-1", "SCNoRed")
                self.UpgradeProcedureMethodActOn("SC-1", "SC2N")
            
            if 2 == i:
                self.UpgradeProcedureMethodActOn("SC-2","SC2N")
                
            if 3 == i:
                self.UpgradeProcedureMethodActOn("PL-3","PLNoRed")
                self.UpgradeProcedureMethodActOn("PL-3","PL2N")
                
            if 4 == i:
                self.UpgradeProcedureMethodActOn("PL-4","PL2N")

            self.UpgradeProcedureMethodActOn(blade,"AllNodesNWayActive")
            i = i + 1
        
        self.UpgradeProcedureMethodSwAdd()
        self.UpgradeProcedureMethodTail()
        self.UpgradeProcedureTail()
        self.CampaignWrapup()
        self.CampaignTail()

        self.camp = re.sub('APPVER', self.appVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'amfMeasureApp install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:///tmp/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-AmfMeasureAppInstall">
  <campaignInfo>
    <campaignPeriod saSmfCmpgExpectedTime="600000000"/>
  </campaignInfo>"""
  
    def BaseTypes(self):
        self.camp = self.camp + """
  <campaignInitialization>
    <addToImm>
      <amfEntityTypes>
        <AppBaseType safAppType="safAppType=AmfMeasureAppType">
          <AppType safVersion="safVersion=1.0.0">
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=AmfMeasAppTypeNoRed"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=AmfMeasAppTypeNWayActive"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=AmfMeasAppType2N"/>
          </AppType>
        </AppBaseType>
        <CSBaseType safCSType="safCSType=AmfMeasAppTypeNoRed">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <CSBaseType safCSType="safCSType=AmfMeasAppTypeNWayActive">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <CSBaseType safCSType="safCSType=AmfMeasAppType2N">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>

        <ServiceBaseType safSvcType="safSvcType=AmfMeasAppTypeNoRed">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType saAmfSvctMaxNumCSIs="0" safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed"/>
          </ServiceType>
        </ServiceBaseType>
        <ServiceBaseType safSvcType="safSvcType=AmfMeasAppTypeNWayActive">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType saAmfSvctMaxNumCSIs="0" safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive"/>
          </ServiceType>
        </ServiceBaseType>
        <ServiceBaseType safSvcType="safSvcType=AmfMeasAppType2N">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType saAmfSvctMaxNumCSIs="0" safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N"/>
          </ServiceType>
        </ServiceBaseType>

        <CompBaseType safCompType="safCompType=AmfMeasAppTypeNoRed">
          <CompType safVersion="safVersion=APPVER">
            <providesCSType saAmfCtCompCapability="6" saAmfCtDefNumMaxActiveCsi="0" saAmfCtDefNumMaxStandbyCsi="0" safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefDisableRestart="0" saAmfCtDefInstantiationLevel="0" saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>instantiate NoRed</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>cleanup NoRed</cmdArgv>
            </cleanupCmd>
            <healthCheck saAmfHealthcheckMaxDuration="180000000000" saAmfHealthcheckPeriod="240000000000" safHealthcheckKey="safHealthcheckKey=amfMeasureApp"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-APPVER"/>
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=AmfMeasAppTypeNWayActive">
          <CompType safVersion="safVersion=APPVER">
            <providesCSType saAmfCtCompCapability="2" saAmfCtDefNumMaxActiveCsi="0" saAmfCtDefNumMaxStandbyCsi="0" safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefDisableRestart="0" saAmfCtDefInstantiationLevel="0" saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>instantiate NWayActive</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>cleanup NWayActive</cmdArgv>
            </cleanupCmd>
            <healthCheck saAmfHealthcheckMaxDuration="180000000000" saAmfHealthcheckPeriod="240000000" safHealthcheckKey="safHealthcheckKey=amfMeasureApp"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-APPVER"/>
          </CompType>
        </CompBaseType>
       <CompBaseType safCompType="safCompType=AmfMeasAppType2N">
          <CompType safVersion="safVersion=APPVER">
            <providesCSType saAmfCtCompCapability="1" saAmfCtDefNumMaxActiveCsi="0" saAmfCtDefNumMaxStandbyCsi="0" safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefDisableRestart="1" saAmfCtDefInstantiationLevel="0" saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtDefRecoveryOnError="3"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>instantiate 2N</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>cleanup 2N</cmdArgv>
            </cleanupCmd>
            <healthCheck saAmfHealthcheckMaxDuration="10000000000" saAmfHealthcheckPeriod="240000000000" safHealthcheckKey="safHealthcheckKey=amfMeasureApp"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-APPVER"/>
          </CompType>
        </CompBaseType>

        <SUBaseType safSuType="safSuType=AmfMeasAppTypeNoRed">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutDefSUFailover="0" saAmfSutIsExternal="0"/>
            <componentType saAmfSutMaxNumComponents="0" saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=APPVER\,safCompType=AmfMeasAppTypeNoRed"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=AmfMeasAppTypeNoRed"/>
          </SUType>
        </SUBaseType>
        <SUBaseType safSuType="safSuType=AmfMeasAppTypeNWayActive">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutDefSUFailover="0" saAmfSutIsExternal="0"/>
            <componentType saAmfSutMaxNumComponents="0" saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=APPVER\,safCompType=AmfMeasAppTypeNWayActive"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=AmfMeasAppTypeNWayActive"/>
          </SUType>
        </SUBaseType>
       <SUBaseType safSuType="safSuType=AmfMeasAppType2N">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutDefSUFailover="1" saAmfSutIsExternal="0"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=APPVER\,safCompType=AmfMeasAppType2N"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=AmfMeasAppType2N"/>
          </SUType>
       </SUBaseType>

        <SGBaseType safSgType="safSgType=AmfMeasAppTypeNoRed">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=AmfMeasAppTypeNoRed"/>
            <redundancy saAmfSgtRedundancyModel="5"/>
            <compRestart saAmfSgtDefCompRestartMax="5" saAmfSgtDefCompRestartProb="100000"/>
            <suRestart saAmfSgtDefSuRestartMax="5" saAmfSgtDefSuRestartProb="100000"/>
            <autoAttrs saAmfSgtDefAutoAdjustProb="100000" safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="0"/>
          </SGType>
        </SGBaseType>
        <SGBaseType safSgType="safSgType=AmfMeasAppTypeNWayActive">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=AmfMeasAppTypeNWayActive"/>
            <redundancy saAmfSgtRedundancyModel="4"/>
            <compRestart saAmfSgtDefCompRestartMax="5" saAmfSgtDefCompRestartProb="100000"/>
            <suRestart saAmfSgtDefSuRestartMax="5" saAmfSgtDefSuRestartProb="100000"/>
            <autoAttrs saAmfSgtDefAutoAdjustProb="100000" safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="0"/>
          </SGType>
        </SGBaseType>
        <SGBaseType safSgType="safSgType=AmfMeasAppType2N">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=AmfMeasAppType2N"/>
            <redundancy saAmfSgtRedundancyModel="1"/>
            <compRestart saAmfSgtDefCompRestartMax="5" saAmfSgtDefCompRestartProb="100000"/>
            <suRestart saAmfSgtDefSuRestartMax="1" saAmfSgtDefSuRestartProb="20000"/>
            <autoAttrs saAmfSgtDefAutoAdjustProb="10000000" safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1"/>
          </SGType>
        </SGBaseType>
      </amfEntityTypes>
    </addToImm>
  </campaignInitialization>
"""

    def UpgradeProcedureHead(self):
        self.camp = self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=Install">
      <outageInfo>
        <acceptableServiceOutage>
          <all/>
        </acceptableServiceOutage>
        <procedurePeriod saSmfProcPeriod="600000000"/>
      </outageInfo>"""

    def SafApp(self):
        self.camp = self.camp + """
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfApplication" parentObjectDN="=">
            <attribute name="safApp" type="SA_IMM_ATTR_SASTRINGT">
              <value>safApp=AmfMeasureApp</value>
            </attribute>
            <attribute name="saAmfAppType" type="SA_IMM_ATTR_SANAMET">
              <value>safVersion=1.0.0,safAppType=AmfMeasureAppType</value>
            </attribute>
            <attribute name="saAmfApplicationAdminState" type="SA_IMM_ATTR_SAUINT32T">
              <value>1</value>
            </attribute>
          </create>
        </immCCB>
      </procInitAction>
"""

    def SafSg(self, safSg, safAmfNodeGroup, saAmfSGNumPrefInserviceSUs):

        safSgType = 'AmfMeasAppTypeNWayActive'
        if 'SC2N' == safSg or 'PL2N' == safSg:
            safSgType = 'AmfMeasAppType2N'
        elif 'SCNoRed' == safSg or 'PLNoRed' == safSg:
            safSgType = 'AmfMeasAppTypeNoRed'
            
        self.camp=self.camp + """
      <!-- safsg=%s -->
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfSG" parentObjectDN="safApp=AmfMeasureApp">
            <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
              <value>safSg=%s</value>
            </attribute>
            <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
              <value>safVersion=1.0.0,safSgType=%s</value>
           </attribute>
            <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
              <value>safAmfNodeGroup=%s,safAmfCluster=myAmfCluster</value>
            </attribute>
            <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
              <value>%d</value>
            </attribute>""" % (safSg, safSg, safSgType, safAmfNodeGroup, saAmfSGNumPrefInserviceSUs)

        if 'AllNodesNWayActive' == safSg:
            self.camp=self.camp + """
            <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
              <value>1000</value>
            </attribute>"""

        self.camp=self.camp + """
            <attribute name="saAmfSGAdminState" type="SA_IMM_ATTR_SAUINT32T">
              <value>1</value>
            </attribute>
          </create>
        </immCCB>
      </procInitAction>
"""

    def SafSu(self, safSu, safSg, safSuType):
        safSuType = 'AmfMeasAppTypeNWayActive'
        if 'SC2N' == safSg or 'PL2N' == safSg:
            safSuType = 'AmfMeasAppType2N'
        elif 'SCNoRed' == safSg or 'PLNoRed' == safSg:
            safSuType = 'AmfMeasAppTypeNoRed'

        self.camp = self.camp + """
      <!-- safSu=%s safSg=%s -->
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfSU" parentObjectDN="safSg=%s,safApp=AmfMeasureApp">
            <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
              <value>safSu=%s</value>
            </attribute>
            <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
              <value>safVersion=1.0.0,safSuType=%s</value>
            </attribute>
            <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
              <value>0</value>
            </attribute>
            <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
              <value>safAmfNode=%s,safAmfCluster=myAmfCluster</value>
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
""" % (safSu, safSg, safSg, safSu, safSuType, safSu)
            
        self.camp = self.camp + """
      <!-- safComp=AmfMeasureApp safSu=%s,safSg=%s -->
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfComp" parentObjectDN="safSu=%s,safSg=%s,safApp=AmfMeasureApp">
            <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
              <value>safComp=AmfMeasureApp</value>
            </attribute>
            <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
              <value>safVersion=%s,safCompType=%s</value>
            </attribute>
          </create>
        </immCCB>
      </procInitAction>
""" % (safSu, safSg, safSu, safSg, self.appVer, safSuType)
      
        self.camp = self.camp + """
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=AmfMeasureApp,safSu=%s,safSg=%s,safApp=AmfMeasureApp">
            <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
              <value>safHealthcheckKey=amfMeasureApp</value>
            </attribute>
            <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
              <value>240000000</value>
            </attribute>
            <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
              <value>180000000000</value>
            </attribute>
          </create>
        </immCCB>
      </procInitAction>
""" % (safSu, safSg)
      
        self.camp = self.camp + """
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfCompCsType" parentObjectDN="safComp=AmfMeasureApp,safSu=%s,safSg=%s,safApp=AmfMeasureApp">
            <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
              <value>safSupportedCsType=safVersion=1.0.0\,safCSType=%s</value>
            </attribute>
          </create>
        </immCCB>
      </procInitAction>
""" % (safSu, safSg, safSuType)


    def SafSi(self, safSi, safSg, saAmfSIPrefActiveAssignments=1):
        safSvcType = 'AmfMeasAppTypeNWayActive'
        if 'SC2N' == safSi or 'PL2N' == safSi:
            safSvcType = 'AmfMeasAppType2N'
        if 'SCNoRed' == safSi or 'PLNoRed' == safSi:
            safSvcType = 'AmfMeasAppTypeNoRed'

        self.camp = self.camp + """
      <!-- safSi=%s -->
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfSI" parentObjectDN="safApp=AmfMeasureApp">
            <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
              <value>safSi=%s</value>
            </attribute>
            <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
              <value>safVersion=1.0.0,safSvcType=%s</value>
            </attribute>
            <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
              <value>safSg=%s,safApp=AmfMeasureApp</value>
            </attribute>
            <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
              <value>1</value>
            </attribute>
            <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
              <value>%d</value>
            </attribute>
            <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
              <value>1</value>
            </attribute>
          </create>
        </immCCB>
      </procInitAction>
""" % (safSi, safSi, safSvcType, safSg, saAmfSIPrefActiveAssignments)
      
        self.camp = self.camp + """
      <!-- safCsi=%s safSi=%s -->
      <procInitAction>
        <immCCB ccbFlags="0">
          <create objectClassName="SaAmfCSI" parentObjectDN="safSi=%s,safApp=AmfMeasureApp">
            <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
              <value>safCsi=%s</value>
            </attribute>
            <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
              <value>safVersion=1.0.0,safCSType=%s</value>
            </attribute>
          </create>
        </immCCB>
      </procInitAction>
""" % (safSi, safSi, safSi, safSi, safSvcType)
          
    def UpgradeProcedureMethodHead(self):
        self.camp = self.camp + """
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit/>
            <activationUnit>
              <actedOn>"""

    def UpgradeProcedureMethodActOn(self, safSu, safSg):
        self.camp=self.camp+'\n                <byName objectDN="safSu=%s,safSg=%s,safApp=AmfMeasureApp"/>' % (safSu, safSg)

    def UpgradeProcedureMethodSwAdd(self):
        self.camp = self.camp + """
              </actedOn>
              <swAdd bundleDN="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-APPVER" pathnamePrefix="/opt">"""

        i=1
        while i <= self.noOfBlades:
            blade='PL-%d' % i
            if 3 > i:
                blade='SC-%d' % i
            self.camp=self.camp+'\n                <plmExecEnv amfNode="safAmfNode=%s,safAmfCluster=myAmfCluster"/>' % blade
            i = i + 1

    def UpgradeProcedureMethodTail(self):
        self.camp = self.camp + """
              </swAdd>
            </activationUnit>
          </forAddRemove>
        </upgradeScope>
        <upgradeStep/>
      </singleStepUpgrade>"""

    def UpgradeProcedureTail(self):
        self.camp = self.camp + """
    </upgradeMethod>"""

        self.camp = self.camp + """
  </upgradeProcedure>"""

    def CampaignWrapup(self):
        self.camp = self.camp + """
  <campaignWrapup>
    <waitToCommit/>
    <waitToAllowNewCampaign/>
    <removeFromImm/>
  </campaignWrapup>"""

    def CampaignTail(self):
        self.camp = self.camp + """
</upgradeCampaign>
"""


def campaignCreator(fileName, noOfBlades, appVer):
    camp  = amfMeasureInstallCampaignCreator(fileName, noOfBlades, appVer)
    result = amfMeasureInstallCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-n", "--NoOfBlades", 
                      type="int", dest="noOfBlades", default=4,
                      help="Number of blades, default 4")

    parser.add_option("-v", "--version",
                      dest="appVer", default="P1A01",
                      help="application version, default = P1A01")

    parser.add_option("-i", "--NoOfSIs",
                      type="int", dest="SIs", default=1,
                      help="Number of SIs, default = 1")

    parser.add_option("-g", "--NoOfSGs",
                      type="int", dest="SGs", default=1,
                      help="Number of SGs, default = 1")

    (options, args) = parser.parse_args()
        
    camp  = amfMeasureInstallCampaignCreator("amfMeasureInstallCampaign.xml", options.noOfBlades, options.appVer, options.SIs, options.SGs)
    amfMeasureInstallCampaignCreator.create(camp)
