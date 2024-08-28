#!/usr/bin/env jython

""" This module creates a campaign.xml to install testApp.
Number of nodes of target node must be given.

# redundancy saAmfSgtRedundancyModel=
SA_AMF_2N_REDUNDANCY_MODEL=1
SA_AMF_NPM_REDUNDANCY_MODEL=2
SA_AMF_N_WAY_REDUNDANCY_MODEL=3
SA_AMF_N_WAY_ACTIVE_REDUNDANCY_MODEL=4
SA_AMF_NO_REDUNDANCY_MODEL=5

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

class testAppExpandCampaignCreator():
    def __init__(self, fileName, fromNumOfNodes, toNumOfNodes, verTapp):
        self.fileName       = fileName
        self.fromNumOfNodes = int(fromNumOfNodes)
        self.toNumOfNodes   = int(toNumOfNodes)
        self.verTapp        = verTapp
        self.camp           = ""
        self.noActSC        = 0
        self.noActPL        = 0

    def create(self):
        scAct = "2"
        scSb  = "1"
        siAct = "1"
        siSb = "1"
        self.noActSC    = 2
                    
        if 2 < self.toNumOfNodes:
            self.noActPL    = self.toNumOfNodes - 2
        
        self.CampaignHead()
        self.CampaignInit()
        self.UpgradeProcedureHead()
        self.ProcInitAction()
        self.UpgradeProcedureMethod()

        if 1 == self.fromNumOfNodes:
            self.ProcWrapupAction1()



        if 4 == self.toNumOfNodes:
            self.ProcWrapupAction3()

        if 3 < self.toNumOfNodes:
            self.ProcWrapupAction4()

        if (3 == self.toNumOfNodes):
            self.ProcWrapupActionUnlock()
#        if 3 == self.toNumOfNodes:
#            self.ProcWrapupActionUnlock()

            
        #if 3 != self.fromNumOfNodes and 3 < self.toNumOfNodes:
        #    self.ProcWrapupActionUnlock()

        self.CampaignWrapup()
        
        self.camp = re.sub('TAPPVER', self.verTapp, self.camp)
      
        if 2 < self.toNumOfNodes:
            inSvcSu = "2"
            if 3 == self.toNumOfNodes:
                inSvcSu = "1"
                
            self.camp = re.sub('CHANGE-PL-2N-InSvcSu',   inSvcSu, self.camp)
            self.camp = re.sub('CHANGE-PL-NWay-PlNodes', '%d' % self.noActPL, self.camp)



        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'testApp install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-TestAppExpand">
  <campaignInfo>
    <campaignPeriod/>
  </campaignInfo>"""

    def CampaignInit(self):
        self.camp = self.camp + """
  <campaignInitialization>
    <addToImm/>
  </campaignInitialization>"""


    def UpgradeProcedureHead(self):
        self.camp = self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=Expand">
    <outageInfo>
      <acceptableServiceOutage>
        <all/>
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000"/>
    </outageInfo>"""
    
    def ProcInitAction(self):
        if 4 > self.fromNumOfNodes:
            self.camp = self.camp + """
    <procInitAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safAmfNodeGroup=TGCs,safAmfCluster=myAmfCluster" operation = "SA_IMM_ATTR_VALUES_ADD" >
          <attribute name="saAmfNGNodeList" type="SA_IMM_ATTR_SANAMET">"""
            if 2 > self.fromNumOfNodes:
                self.camp = self.camp + """
            <value>safAmfNode=SC-2,safAmfCluster=myAmfCluster</value>"""
            
            if 3 > self.fromNumOfNodes and 2 < self.toNumOfNodes:
                self.camp = self.camp + """
            <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>"""
            
            if 4 > self.fromNumOfNodes and 3 < self.toNumOfNodes:
                self.camp = self.camp + """
            <value>safAmfNode=PL-4,safAmfCluster=myAmfCluster</value>"""

            self.camp = self.camp + """
          </attribute>
        </modify>
      </immCCB>  
    </procInitAction>"""

    def UpgradeProcedureMethod(self):
        self.camp = self.camp + """
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit/>
            <activationUnit>
              <actedOn>"""
    
        if 1 == self.fromNumOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global"/>"""

        if 3 > self.fromNumOfNodes and 2 < self.toNumOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global"/>"""
               
        if 4 > self.fromNumOfNodes and 3 < self.toNumOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global"/>"""

        if 5 > self.fromNumOfNodes:
            i = 5
        else:
            i = self.fromNumOfNodes + 1
        while i <= self.toNumOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global"/>""" % (i,i,i)
            i = i +1


        self.camp = self.camp + """
              </actedOn>"""

        if 1 == self.fromNumOfNodes:
            self.camp = self.camp + """
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_sc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-2</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_scSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_sc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_scCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-2</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_allSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_sc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-2</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_scSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_sc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_scCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-2</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgen_scSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgen_sc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgen_scCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType</value>
                </attribute>
              </added>"""

        if 3 > self.fromNumOfNodes and 2 < self.toNumOfNodes:
            self.camp = self.camp + """
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tapp_all</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tapp_allSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=PLs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1000</value>
                </attribute>
                <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1000</value>
                </attribute>
                <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxStandbySIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-PL-NWay-PlNodes</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tapp_all</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tapp_allSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tapp_all,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-PL-NWay-PlNodes</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tapp_all,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tapp_all</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tapp_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tapp_pl</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tapp_plSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=PLs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1000</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1000</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxStandbySIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-PL-NWay-PlNodes</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tapp_pl</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tapp_plSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tapp_pl,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-PL-NWay-PlNodes</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tapp_pl,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tapp_pl</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tapp_plCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tapp_onepl</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tapp_oneplSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=PLs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxStandbySIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tapp_onepl</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tapp_oneplSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tapp_onepl,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tapp_onepl,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tapp_onepl</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tapp_oneplCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgc_pl</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgc_plSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=PLs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-PL-2N-InSvcSu</value> <!-- 2 CHANGE PL-2N-InSvcSu -->
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tgc_pl</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgc_plSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgc_pl,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgc_pl,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgc_pl</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgc_plCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgc_onepl</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgc_oneplSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=PLs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxStandbySIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tgc_onepl</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgc_oneplSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgc_onepl,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgc_onepl,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgc_onepl</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgc_oneplCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgen_all</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgen_allSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=PLs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1000</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1000</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxStandbySIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-PL-NWay-PlNodes</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tgen_all</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgen_allSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgen_all,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-PL-NWay-PlNodes</value> <!-- 2 CHANGE PL-NWay-PlNodes -->
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgen_all,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgen_all</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgen_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgen_onepl</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgen_oneplSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=PLs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxStandbySIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tgen_onepl</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgen_oneplSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgen_onepl,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgen_onepl,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgen_onepl</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgen_oneplCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-3</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_allSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_all,safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_all,safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-3</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_plSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_pl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_plCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_pl,safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_pl,safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_onepl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-3</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_oneplSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_onepl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_oneplCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_onepl,safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_onepl,safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-3</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_plSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_pl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_plCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_onepl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-3</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_oneplSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_onepl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_oneplCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-3</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgen_allSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgen_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgen_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgen_all,safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgen_all,safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgen_onepl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-3</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgen_oneplSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgen_onepl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgen_oneplCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgen_onepl,safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgen_onepl,safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType</value>
                </attribute>
              </added>"""


        if 4 > self.fromNumOfNodes and 3 < self.toNumOfNodes:
            self.camp = self.camp + """
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-4</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_allSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>4</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-4,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_all,safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_all,safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-4</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_plSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-4,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_pl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_plCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_pl,safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_pl,safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-4</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_plSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-4,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_pl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_plCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-4</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgen_allSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-4,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgen_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgen_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgen_all,safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgen_all,safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType</value>
                </attribute>
              </added>"""


        if self.fromNumOfNodes > 5:
            i = self.fromNumOfNodes
        else:
            i = 4
        while i < self.toNumOfNodes:
            i = i +1
            self.camp = self.camp + """
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-%d</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_allSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>4</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-%d,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_all,safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_all,safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-%d</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_plSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-%d,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_pl</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_plCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_pl,safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_pl,safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=PL-%d</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgen_allSuType</value>
                </attribute>
                <attribute name="saAmfSURank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
                <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=PL-%d,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSUFailover" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>3</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgen_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgen_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safHealthcheckKey" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safHealthcheckKey=A9FD64E12C</value>
                </attribute>
                <attribute name="saAmfHealthcheckPeriod" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
                <attribute name="saAmfHealthcheckMaxDuration" type="SA_IMM_ATTR_SATIMET">
                  <value>10000000000</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType</value>
                </attribute>
              </added>
""" % (i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)

        self.camp = self.camp + """
              <swAdd bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin">"""

        i = self.fromNumOfNodes
        if 1 == self.fromNumOfNodes:
            i = 2
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster"/>"""
            
        while i < self.toNumOfNodes:
            i = i + 1
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=PL-%d,safAmfCluster=myAmfCluster"/>""" % i
        self.camp = self.camp + """
              </swAdd>
            </activationUnit>
          </forAddRemove>
        </upgradeScope>
        <upgradeStep/>
      </singleStepUpgrade>
    </upgradeMethod>"""



    def ProcWrapupAction1(self):
        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tapp_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tapp_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tapp_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgc_all,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgc_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgen_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>"""


    def ProcWrapupAction3(self):
        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgc_pl,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tgc_pl,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
"""

    def ProcWrapupAction4(self):
        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tapp_all,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>CHANGE-PL-NWay-PlNodes</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tapp_all,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>CHANGE-PL-NWay-PlNodes</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tapp_pl,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>CHANGE-PL-NWay-PlNodes</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tapp_pl,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>CHANGE-PL-NWay-PlNodes</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgen_all,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>CHANGE-PL-NWay-PlNodes</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tgen_all,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>CHANGE-PL-NWay-PlNodes</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
"""




    def ProcWrapupActionUnlock4(self):
        self.camp = self.camp + """
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tapp_all,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tapp_all,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tapp_pl,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tapp_pl,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgen_all,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgen_all,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction>"""

    def ProcWrapupActionUnlock(self):
        self.camp = self.camp + """
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tapp_all,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tapp_all,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tapp_pl,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tapp_pl,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tapp_onepl,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tapp_onepl,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgc_pl,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgc_pl,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgc_onepl,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgc_onepl,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgen_all,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgen_all,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgen_onepl,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgen_onepl,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction>"""


    def CampaignWrapup(self):
        self.camp = self.camp + """
  </upgradeProcedure>
  <campaignWrapup>
    <waitToCommit/>
    <waitToAllowNewCampaign/>
    <removeFromImm/>
  </campaignWrapup>
</upgradeCampaign>
"""



        


def campaignCreator(fileName, fromNumOfNodes, toNumOfNodes, verTapp):
    camp  = testAppExpandCampaignCreator(fileName, fromNumOfNodes, toNumOfNodes, verTapp)
    result = testAppExpandCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-f", "--fromNumberOfNodes",
                      dest="fromNodes", default="1",
                      help="From number of nodes, default = 1")


    parser.add_option("-t", "--toNumberOfNodes",
                      dest="toNodes", default="2",
                      help="To number of nodes, default = 2")
    
    parser.add_option("-a", "--verTapp",
                      dest="verTapp", default="P1A01",
                      help="tapp application version, default = P1A01")
    parser.add_option("-g", "--verTgen",
                      dest="verTgen", default="P1A01",
                      help="tgen application version, default = P1A01")
    parser.add_option("-c", "--verTgc",
                      dest="verTgc", default="P1A01",
                      help="tgc application version, default = P1A01")


    (options, args) = parser.parse_args()

    if int(options.fromNodes) > int(options.toNodes):
        print "Not possible to expand to a lower number of blades!"
        exit(1)
        
    camp  = testAppExpandCampaignCreator("TappExpandCampaign.xml", options.fromNodes, options.toNodes, options.verTapp, options.verTgen, options.verTgc)
    testAppExpandCampaignCreator.create(camp)
