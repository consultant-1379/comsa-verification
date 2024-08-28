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

class testAppRemoveCampaignCreator():
    def __init__(self, fileName, numOfNodes, verTapp, verTgen, verTgc):
        self.fileName   = fileName
        self.numOfNodes = int(numOfNodes)
        self.verTapp    = verTapp
        self.verTgen    = verTgen
        self.verTgc     = verTgc
        self.camp       = ""
        self.noActSC    = 2
        self.noActPL    = 0

    def create(self):
        scNwayAct = "2"
        if 1 == self.numOfNodes:
            scNwayAct = "1"
        
        if 2 < self.numOfNodes:
            self.noActPL    = self.numOfNodes - 2
        
        self.CampaignHead()
        self.CampaignInit()
        self.UpgradeProcedure1()
        self.ProcWrapupAction1()
        self.UpgradeProcedure2()
        self.ProcWrapupAction2()
        self.CampaignWrapup()
        
        self.camp = re.sub('TAPPVER', self.verTapp, self.camp)
        self.camp = re.sub('TGENVER', self.verTgen, self.camp)
        self.camp = re.sub('TGCVER',  self.verTgc, self.camp)


        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'testApp install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-TestAppRemove">
  <campaignInfo>
    <campaignPeriod />
  </campaignInfo>"""

    def CampaignInit(self):
        self.camp = self.camp + """
  <campaignInitialization>
    <addToImm />
  </campaignInitialization>"""

    def UpgradeProcedure1(self):
        self.camp = self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=Remove1" saSmfExecLevel="1">
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
                <byName objectDN="safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global" />
                <byName objectDN="safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global" />
                <byName objectDN="safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global" />
                <byName objectDN="safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global" />"""
    
        if 1 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
                <byName objectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />"""
        if 2 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global" />
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global" />
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global" />
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global" />
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global" />"""
               
        if 3 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global" />
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global" />
                <byName objectDN="safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global" />"""
        i = 5
        while i < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global" />
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global" />
                <byName objectDN="safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />""" % (i,i,i)
            i = i +1

        self.camp = self.camp + """
              </actedOn>"""

        self.camp = self.camp + """
              <swRemove bundleDN="safSmfBundle=ERIC-TA_TAPP-CXP9013968_3-TAPPVER" pathnamePrefix="/opt/TA_TAPP/bin">
                <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster" />"""
        if 2 <= self.numOfNodes:
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster" />"""
        i = 2
        while i < self.numOfNodes:
            i = i + 1
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=PL-%d,safAmfCluster=myAmfCluster" />""" % i
        self.camp = self.camp + """
              </swRemove>
              <swRemove bundleDN="safSmfBundle=ERIC-TA_TGEN-CXP9013968_4-TGENVER" pathnamePrefix="/opt/TA_TGEN/bin">
                <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster" />"""
        if 2 <= self.numOfNodes:
                    self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster" />"""
        i = 2
        while i < self.numOfNodes:
            i = i + 1
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=PL-%d,safAmfCluster=myAmfCluster" />""" % i
        self.camp = self.camp + """
              </swRemove>
            </deactivationUnit>
            <activationUnit />
          </forAddRemove>
        </upgradeScope>
        <upgradeStep />
      </singleStepUpgrade>
    </upgradeMethod>"""

    def ProcWrapupAction1(self):
        if self.numOfNodes >= 1:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_onesc,safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_sc,safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_onesc,safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_sc,safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType,safComp=ta_tapp_onesc,safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType,safComp=ta_tapp_sc,safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType,safComp=ta_tgen_onesc,safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType,safComp=ta_tgen_sc,safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_onesc,safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_sc,safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_onesc,safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_sc,safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
"""            
        if self.numOfNodes > 1:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType,safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType,safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
"""
        if self.numOfNodes > 2:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_all,safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_pl,safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_all,safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_onepl,safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_onepl,safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType,safComp=ta_tapp_all,safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType,safComp=ta_tapp_onepl,safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType,safComp=ta_tapp_pl,safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType,safComp=ta_tgen_all,safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType,safComp=ta_tgen_onepl,safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_all,safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_onepl,safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_pl,safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_all,safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_onepl,safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
"""
        i = 4
        while i <= self.numOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_all,safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_pl,safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType,safComp=ta_tapp_all,safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType,safComp=ta_tapp_pl,safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType,safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_all,safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_pl,safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>""" % (i,i,i,i,i,i,i,i,i,i,i,i)
            i = i + 1    

        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType,safVersion=TAPPVER,safCompType=ta_tapp_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType,safVersion=TAPPVER,safCompType=ta_tapp_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType,safVersion=TAPPVER,safCompType=ta_tapp_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType,safVersion=TAPPVER,safCompType=ta_tapp_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType,safVersion=TAPPVER,safCompType=ta_tapp_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType,safVersion=TGENVER,safCompType=ta_tgen_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType,safVersion=TGENVER,safCompType=ta_tgen_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType,safVersion=TGENVER,safCompType=ta_tgen_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType,safVersion=TGENVER,safCompType=ta_tgen_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tapp_all,safSi=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tapp_onepl,safSi=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tapp_onesc,safSi=ta_tapp_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tapp_pl,safSi=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tapp_sc,safSi=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgen_all,safSi=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgen_onepl,safSi=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgen_onesc,safSi=ta_tgen_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgen_sc,safSi=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType,safVersion=1.0.0,safSvcType=ta_tapp_allSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType,safVersion=1.0.0,safSvcType=ta_tapp_oneplSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType,safVersion=1.0.0,safSvcType=ta_tapp_onescSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType,safVersion=1.0.0,safSvcType=ta_tapp_plSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType,safVersion=1.0.0,safSvcType=ta_tapp_scSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType,safVersion=1.0.0,safSvcType=ta_tgen_allSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType,safVersion=1.0.0,safSvcType=ta_tgen_oneplSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType,safVersion=1.0.0,safSvcType=ta_tgen_onescSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType,safVersion=1.0.0,safSvcType=ta_tgen_scSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGENVER\,safCompType=ta_tgen_allCompType,safVersion=1.0.0,safSuType=ta_tgen_allSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGENVER\,safCompType=ta_tgen_oneplCompType,safVersion=1.0.0,safSuType=ta_tgen_oneplSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGENVER\,safCompType=ta_tgen_onescCompType,safVersion=1.0.0,safSuType=ta_tgen_onescSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGENVER\,safCompType=ta_tgen_scCompType,safVersion=1.0.0,safSuType=ta_tgen_scSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_allCompType,safVersion=1.0.0,safSuType=ta_tapp_allSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_oneplCompType,safVersion=1.0.0,safSuType=ta_tapp_oneplSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_onescCompType,safVersion=1.0.0,safSuType=ta_tapp_onescSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_plCompType,safVersion=1.0.0,safSuType=ta_tapp_plSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_scCompType,safVersion=1.0.0,safSuType=ta_tapp_scSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGENVER,safCompType=ta_tgen_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGENVER,safCompType=ta_tgen_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGENVER,safCompType=ta_tgen_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGENVER,safCompType=ta_tgen_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TAPPVER,safCompType=ta_tapp_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TAPPVER,safCompType=ta_tapp_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TAPPVER,safCompType=ta_tapp_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TAPPVER,safCompType=ta_tapp_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TAPPVER,safCompType=ta_tapp_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgen_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgen_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
   </upgradeProcedure>
"""


    def UpgradeProcedure2(self):
        self.camp = self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=Remove2" saSmfExecLevel="2">
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
                <byName objectDN="safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global" />
                <byName objectDN="safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global" />
                <byName objectDN="safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global" />"""
    
        if 1 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />"""
        if 2 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />"""
               
        if 3 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />"""
        self.camp = self.camp + """
              </actedOn>"""

        self.camp = self.camp + """
              <swRemove bundleDN="safSmfBundle=ERIC-TA_TGC-CXP9013968_5-TGCVER" pathnamePrefix="/opt/TA_TGC/bin">
                <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster" />"""
        if 2 <= self.numOfNodes:
                    self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster" />"""
        i = 2
        while i < self.numOfNodes:
            i = i + 1
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=PL-%d,safAmfCluster=myAmfCluster" />""" % i
        self.camp = self.camp + """
              </swRemove>
            </deactivationUnit>
            <activationUnit />
          </forAddRemove>
        </upgradeScope>
        <upgradeStep />
      </singleStepUpgrade>
    </upgradeMethod>"""

    def ProcWrapupAction2(self):
        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_all,safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_onesc,safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_sc,safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType,safComp=ta_tgc_all,safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType,safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType,safVersion=TGCVER,safCompType=ta_tgc_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType,safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType,safVersion=TGCVER,safCompType=ta_tgc_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType,safComp=ta_tgc_onesc,safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType,safVersion=TGCVER,safCompType=ta_tgc_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType,safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType,safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType,safVersion=TGCVER,safCompType=ta_tgc_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType,safComp=ta_tgc_sc,safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType,safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType,safVersion=TGCVER,safCompType=ta_tgc_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_all,safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_onesc,safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_sc,safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgc_all,safSi=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgc_onepl,safSi=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgc_onesc,safSi=ta_tgc_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgc_pl,safSi=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgc_sc,safSi=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType,safVersion=1.0.0,safSvcType=ta_tgc_allSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType,safVersion=1.0.0,safSvcType=ta_tgc_oneplSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType,safVersion=1.0.0,safSvcType=ta_tgc_onescSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType,safVersion=1.0.0,safSvcType=ta_tgc_plSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType,safVersion=1.0.0,safSvcType=ta_tgc_scSvcType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGCVER\,safCompType=ta_tgc_allCompType,safVersion=1.0.0,safSuType=ta_tgc_allSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGCVER\,safCompType=ta_tgc_oneplCompType,safVersion=1.0.0,safSuType=ta_tgc_oneplSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGCVER\,safCompType=ta_tgc_onescCompType,safVersion=1.0.0,safSuType=ta_tgc_onescSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGCVER\,safCompType=ta_tgc_plCompType,safVersion=1.0.0,safSuType=ta_tgc_plSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=TGCVER\,safCompType=ta_tgc_scCompType,safVersion=1.0.0,safSuType=ta_tgc_scSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGCVER,safCompType=ta_tgc_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGCVER,safCompType=ta_tgc_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGCVER,safCompType=ta_tgc_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGCVER,safCompType=ta_tgc_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=TGCVER,safCompType=ta_tgc_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgc_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgc_onesc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
  </upgradeProcedure>
"""

    def CampaignWrapup(self):
        self.camp = self.camp + """
  <campaignWrapup>
    <waitToCommit />
    <waitToAllowNewCampaign />
    <removeFromImm>
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tapp_allCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tapp_oneplCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tapp_onescCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tapp_plCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tapp_scCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgen_allCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgen_oneplCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgen_onescCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgen_scCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tapp_allSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tapp_oneplSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tapp_onescSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tapp_plSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tapp_scSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgen_allSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgen_oneplSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgen_onescSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgen_scSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tapp_allSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tapp_oneplSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tapp_onescSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tapp_plSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tapp_scSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgen_allSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgen_oneplSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgen_onescSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgen_scSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tapp_allSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tapp_oneplSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tapp_onescSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tapp_plSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tapp_scSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgen_allSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgen_oneplSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgen_onescSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgen_scSvcType" />
      <amfEntityTypeDN objectDN="safVersion=TGENVER,safCompType=ta_tgen_allCompType" />
      <amfEntityTypeDN objectDN="safVersion=TGENVER,safCompType=ta_tgen_oneplCompType" />
      <amfEntityTypeDN objectDN="safVersion=TGENVER,safCompType=ta_tgen_onescCompType" />
      <amfEntityTypeDN objectDN="safVersion=TGENVER,safCompType=ta_tgen_scCompType" />
      <amfEntityTypeDN objectDN="safVersion=TAPPVER,safCompType=ta_tapp_allCompType" />
      <amfEntityTypeDN objectDN="safVersion=TAPPVER,safCompType=ta_tapp_oneplCompType" />
      <amfEntityTypeDN objectDN="safVersion=TAPPVER,safCompType=ta_tapp_onescCompType" />
      <amfEntityTypeDN objectDN="safVersion=TAPPVER,safCompType=ta_tapp_plCompType" />
      <amfEntityTypeDN objectDN="safVersion=TAPPVER,safCompType=ta_tapp_scCompType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgc_allCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgc_oneplCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgc_onescCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgc_plCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safCSType=ta_tgc_scCsType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgc_allSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgc_oneplSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgc_onescSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgc_plSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSgType=ta_tgc_scSgType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgc_allSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgc_oneplSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgc_onescSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgc_plSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSuType=ta_tgc_scSuType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgc_allSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgc_oneplSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgc_onescSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgc_plSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safSvcType=ta_tgc_scSvcType" />
      <amfEntityTypeDN objectDN="safVersion=TGCVER,safCompType=ta_tgc_allCompType" />
      <amfEntityTypeDN objectDN="safVersion=TGCVER,safCompType=ta_tgc_oneplCompType" />
      <amfEntityTypeDN objectDN="safVersion=TGCVER,safCompType=ta_tgc_onescCompType" />
      <amfEntityTypeDN objectDN="safVersion=TGCVER,safCompType=ta_tgc_plCompType" />
      <amfEntityTypeDN objectDN="safVersion=TGCVER,safCompType=ta_tgc_scCompType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tapp_allCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tapp_oneplCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tapp_onescCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tapp_plCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tapp_scCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgc_allCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgc_oneplCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgc_onescCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgc_plCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgc_scCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgen_allCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgen_oneplCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgen_onescCsType" />
      <amfEntityTypeDN objectDN="safCSType=ta_tgen_scCsType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tapp_allCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tapp_oneplCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tapp_onescCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tapp_plCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tapp_scCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgc_allCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgc_oneplCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgc_onescCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgc_plCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgc_scCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgen_allCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgen_oneplCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgen_onescCompType" />
      <amfEntityTypeDN objectDN="safCompType=ta_tgen_scCompType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tapp_allSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tapp_oneplSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tapp_onescSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tapp_plSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tapp_scSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgc_allSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgc_oneplSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgc_onescSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgc_plSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgc_scSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgen_allSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgen_oneplSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgen_onescSgType" />
      <amfEntityTypeDN objectDN="safSgType=ta_tgen_scSgType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tapp_allSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tapp_oneplSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tapp_onescSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tapp_plSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tapp_scSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgc_allSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgc_oneplSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgc_onescSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgc_plSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgc_scSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgen_allSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgen_oneplSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgen_onescSuType" />
      <amfEntityTypeDN objectDN="safSuType=ta_tgen_scSuType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tapp_allSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tapp_oneplSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tapp_onescSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tapp_plSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tapp_scSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgc_allSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgc_oneplSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgc_onescSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgc_plSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgc_scSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgen_allSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgen_oneplSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgen_onescSvcType" />
      <amfEntityTypeDN objectDN="safSvcType=ta_tgen_scSvcType" />
      <amfEntityTypeDN objectDN="safVersion=1.0.0,safAppType=ta_global_AppType" />
      <amfEntityTypeDN objectDN="safAppType=ta_global_AppType" /> 
      <amfEntityTypeDN objectDN="safAmfNodeGroup=TGCs,safAmfCluster=myAmfCluster" />
      <softwareBundleDN bundleDN="safSmfBundle=ERIC-TA_TAPP-CXP9013968_3-TAPPVER" />
      <softwareBundleDN bundleDN="safSmfBundle=ERIC-TA_TGEN-CXP9013968_4-TGENVER" />
      <softwareBundleDN bundleDN="safSmfBundle=ERIC-TA_TGC-CXP9013968_5-TGCVER" />
    </removeFromImm>
  </campaignWrapup>
</upgradeCampaign>
"""

def campaignCreator(fileName, numOfNodes, verTapp, verTgen, verTgc):
    camp  = testAppRemoveCampaignCreator(fileName, numOfNodes, verTapp, verTgen, verTgc)
    result = testAppRemoveCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()


    parser.add_option("-n", "--numberOfNodes",
                      dest="numOfNodes", default="4",
                      help="Number of nodes, default = 4")
    
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
        
    
    camp  = testAppRemoveCampaignCreator("TappRemoveCampaign.xml", options.numOfNodes, options.verTapp, options.verTgen, options.verTgc)
    testAppRemoveCampaignCreator.create(camp)
