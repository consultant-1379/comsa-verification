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

class testAppReduceCampaignCreator():
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
            self.noActPL = self.toNumOfNodes - 2
            if 0> self.noActPL:
                self.noActPL = 0
                
        self.CampaignHead()
        self.CampaignInit()
        self.UpgradeProcedureHead()
        self.UpgradeProcedureMethod()

        self.ProcWrapupActionTapp()
        self.ProcWrapupActionTgen()
        self.ProcWrapupActionTgc()


        if self.toNumOfNodes >= 3:
            self.ProcWrapupAction4()

        #if 1 == self.toNumOfNodes:
        #    self.ProcWrapupAction1()

        #if 3 == self.toNumOfNodes:
        #    self.ProcWrapupAction3()


        self.CampaignWrapup()
        
        self.camp = re.sub('TAPPVER', self.verTapp, self.camp)
      
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
  safSmfCampaign="safSmfCampaign=ERIC-TestAppReduce">
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
  <upgradeProcedure safSmfProcedure="safSmfProc=Reduce">
    <outageInfo>
      <acceptableServiceOutage>
        <all/>
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000"/>
    </outageInfo>"""
    

    def UpgradeProcedureMethod(self):
        self.camp = self.camp + """
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit>
              <actedOn>"""
    
        if 1 == self.toNumOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global"/>"""

        if 3 > self.toNumOfNodes and 2 < self.fromNumOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global"/>"""
               
        if 4 > self.toNumOfNodes and 3 < self.fromNumOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global"/>"""

        if 4 < self.fromNumOfNodes:
            i = 5
            if self.toNumOfNodes > i:
                i = self.toNumOfNodes + 1
            while i <= self.fromNumOfNodes:
                self.camp = self.camp + """
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global"/>""" % (i,i,i)
                i = i + 1


        self.camp = self.camp + """
              </actedOn>"""


        # TAPP
        self.camp = self.camp + """
              <swRemove bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin">"""
        i = self.toNumOfNodes
        if 1 == self.toNumOfNodes:
            i = 2
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster"/>"""
        while i < self.fromNumOfNodes:
            i = i + 1
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=PL-%d,safAmfCluster=myAmfCluster"/>""" % i
        self.camp = self.camp + """
              </swRemove>
            </deactivationUnit>
            <activationUnit/>
          </forAddRemove>
        </upgradeScope>
        <upgradeStep/>
      </singleStepUpgrade>
    </upgradeMethod>"""



    def ProcWrapupActionTapp(self):
        if 4 < self.fromNumOfNodes:
            i = self.fromNumOfNodes
            while (i > self.toNumOfNodes) and ( i > 4):
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
        <delete objectDN="safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>""" % (i,i,i,i,i,i,i,i)
                i = i - 1
        
        if 4 > self.toNumOfNodes and 3 < self.fromNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_all,safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_pl,safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType,safComp=ta_tapp_all,safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType,safComp=ta_tapp_pl,safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_all,safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_pl,safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    """

        if 3 > self.toNumOfNodes and 2 < self.fromNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_all,safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_onepl,safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_pl,safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global" />
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
        <delete objectDN="safCsi=ta_tapp_all,safSi=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tapp_onepl,safSi=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tapp_pl,safSi=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tapp_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    """

        if 1 == self.toNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType,safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tapp_sc,safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>"""


    def ProcWrapupActionTgen(self):
        if 4 < self.fromNumOfNodes:
            i = self.fromNumOfNodes
            while (i > self.toNumOfNodes) and ( i > 4):
                self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType,safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_all,safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>""" % (i,i,i,i)
                i = i - 1

        if 4 > self.toNumOfNodes and 3 < self.fromNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_all,safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType,safComp=ta_tgen_all,safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_all,safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    """

        if 3 > self.toNumOfNodes and 2 < self.fromNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_all,safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_onepl,safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global" />
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
        <delete objectDN="safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global" />
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
        <delete objectDN="safSg=ta_tgen_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgen_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    """
            
        if 1 == self.toNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType,safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgen_sc,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>"""


    def ProcWrapupActionTgc(self):
           
        if 4 > self.toNumOfNodes and 3 < self.fromNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType,safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_pl,safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    """

        if 3 > self.toNumOfNodes and 2 < self.fromNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType,safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType,safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_onepl,safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_pl,safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global" />
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
        <delete objectDN="safCsi=ta_tgc_onepl,safSi=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=ta_tgc_pl,safSi=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgc_onepl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=ta_tgc_pl,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    """

        if 1 == self.toNumOfNodes:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=A9FD64E12C,safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType,safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType,safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_all,safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=ta_tgc_sc,safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global" />
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
    </procWrapupAction>"""


    def ProcWrapupAction1(self):
        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tapp_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tapp_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgc_all,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tgc_all,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgc_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tgc_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=ta_tgen_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tgen_sc,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
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
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSi=ta_tgc_pl,safApp=ta_global" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>"""

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
        <modify objectDN="safSi=ta_tapp_all,safApp=ta_global" operation="SA_IMM_ATTR_VALUES_REPLACE">
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
        <modify objectDN="safSi=ta_tapp_pl,safApp=ta_global" operation="SA_IMM_ATTR_VALUES_REPLACE">
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
        <modify objectDN="safSi=ta_tgen_all,safApp=ta_global" operation="SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
            <value>CHANGE-PL-NWay-PlNodes</value>
          </attribute>
        </modify>
      </immCCB>
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
    camp  = testAppReduceCampaignCreator(fileName, fromNumOfNodes, toNumOfNodes, verTapp)
    result = testAppReduceCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-f", "--fromNumberOfNodes",
                      dest="fromNode", default="10",
                      help="From number of nodes, default = 10")


    parser.add_option("-t", "--toNumberOfNodes",
                      dest="toNode", default="8",
                      help="To number of nodes, default = 8")
    
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


    
    if int(options.toNode) > int(options.fromNode):
        print " %d > %d " % (int(options.toNode), int(options.fromNode))
        print "Not possible to reduce to a higher number of blades!"
        exit(1)
        
    camp  = testAppReduceCampaignCreator("TappReduceCampaign.xml", options.fromNode, options.toNode, options.verTapp, options.verTgen, options.verTgc)
    testAppReduceCampaignCreator.create(camp)
