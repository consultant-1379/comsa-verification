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

class testAppInstallCampaignCreator():
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
        self.CampInitAction()
        self.UpgradeProcedure()
        self.ProcWrapupAction()
        self.CampaignWrapup()
        
        self.camp = re.sub('TAPPVER', self.verTapp, self.camp)

        self.camp = re.sub('CHANGE-SC-NWay-InSvcSu', scNwayAct, self.camp)

        if 2 < self.numOfNodes:
            inSvcSu = "2"
            if 3 == self.numOfNodes:
                inSvcSu = "1"
                
            self.camp = re.sub('CHANGE-PL-NWay-PlNodes', '%d' % self.noActPL, self.camp)
            self.camp = re.sub('CHANGE-PL-2N-SiAct', inSvcSu, self.camp)


        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'testApp install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-TestAppInstall">
  <campaignInfo>
    <campaignPeriod/>
  </campaignInfo>"""

    def CampaignInit(self):
        self.camp = self.camp + """
  <campaignInitialization>
    <addToImm>
      <amfEntityTypes>
        <AppBaseType safAppType="safAppType=ta_global_AppType">
          <AppType safVersion="safVersion=1.0.0">
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tapp_scSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tapp_onescSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgc_allSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgc_scSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgc_onescSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgen_scSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgen_onescSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tapp_allSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tapp_plSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tapp_oneplSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgc_plSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgc_oneplSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgen_allSgType"/>
            <serviceGroupType saAmfApptSGTypes="safVersion=1.0.0,safSgType=ta_tgen_oneplSgType"/>
          </AppType>
        </AppBaseType>
        <SGBaseType safSgType="safSgType=ta_tapp_scSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tapp_scSuType"/>
            <redundancy saAmfSgtRedundancyModel="4"/>
            <compRestart saAmfSgtDefCompRestartProb="3600000000000" saAmfSgtDefCompRestartMax="10"/>
            <suRestart saAmfSgtDefSuRestartProb="43200000000000" saAmfSgtDefSuRestartMax="10"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tapp_scSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tapp_scCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tapp_scSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_scCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tapp_scSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_scCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
    	      <cmdArgv>instantiate 8301</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 8301</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 8301</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tapp_onescSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tapp_onescSuType"/>
            <redundancy saAmfSgtRedundancyModel="5"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tapp_onescSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tapp_onescCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tapp_onescSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_onescCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tapp_onescSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_onescCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType" saAmfCtCompCapability="6"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
    	      <cmdArgv>instantiate 7201 --response-time-implementer</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 7201 --response-time-implementer</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 7201 --response-time-implementer</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgc_allSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgc_allSuType"/>
            <redundancy saAmfSgtRedundancyModel="1"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgc_allSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgc_allCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgc_allSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgc_allCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgc_allSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_allCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
    	      <cmdArgv>instantiate 4302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 4302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 4302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgc_scSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgc_scSuType"/>
            <redundancy saAmfSgtRedundancyModel="1"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgc_scSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgc_scCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgc_scSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgc_scCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgc_scSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_scCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
    	      <cmdArgv>instantiate 8302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 8302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 8302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgc_onescSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgc_onescSuType"/>
            <redundancy saAmfSgtRedundancyModel="5"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgc_onescSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgc_onescCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgc_onescSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgc_onescCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgc_onescSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_onescCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType" saAmfCtCompCapability="6"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
    	      <cmdArgv>instantiate 7202</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 7202</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 7202</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgen_scSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgen_scSuType"/>
            <redundancy saAmfSgtRedundancyModel="1"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgen_scSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgen_scCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgen_scSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgen_scCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgen_scSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_scCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
    	      <cmdArgv>instantiate 8302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 8302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 8302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgen_onescSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgen_onescSuType"/>
            <redundancy saAmfSgtRedundancyModel="5"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgen_onescSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgen_onescCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgen_onescSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgen_onescCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgen_onescSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_onescCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType" saAmfCtCompCapability="6"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
    	      <cmdArgv>instantiate 7202</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 7202</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 7202</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tapp_allSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tapp_allSuType"/>
            <redundancy saAmfSgtRedundancyModel="4"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tapp_allSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tapp_allCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tapp_allSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_allCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tapp_allSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_allCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
    	      <cmdArgv>instantiate 4301</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 4301</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 4301</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tapp_plSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tapp_plSuType"/>
            <redundancy saAmfSgtRedundancyModel="4"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tapp_plSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tapp_plCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tapp_plSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_plCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tapp_plSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_plCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
    	      <cmdArgv>instantiate 8001</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 8001</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 8001</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tapp_oneplSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tapp_oneplSuType"/>
            <redundancy saAmfSgtRedundancyModel="5"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tapp_oneplSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tapp_oneplCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tapp_oneplSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tapp_oneplCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tapp_oneplSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_oneplCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType" saAmfCtCompCapability="6"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
    	      <cmdArgv>instantiate 7101</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 7101</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 7101</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgc_plSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgc_plSuType"/>
            <redundancy saAmfSgtRedundancyModel="1"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="1"/> <!-- saAmfSgtDefSuRestartMax="3" -->
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgc_plSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgc_plCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgc_plSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgc_plCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgc_plSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_plCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="1" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>  <!--  saAmfCtDefDisableRestart was 0-->
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
    	      <cmdArgv>instantiate 8002</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 8002</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 8002</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgc_oneplSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgc_oneplSuType"/>
            <redundancy saAmfSgtRedundancyModel="5"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgc_oneplSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgc_oneplCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgc_oneplSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgc_oneplCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgc_oneplSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_oneplCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType" saAmfCtCompCapability="6"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
    	      <cmdArgv>instantiate 7102</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 7102</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 7102</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgen_allSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgen_allSuType"/>
            <redundancy saAmfSgtRedundancyModel="4"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgen_allSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgen_allCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgen_allSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgen_allCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgen_allSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_allCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType" saAmfCtCompCapability="2"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
    	      <cmdArgv>instantiate 4302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 4302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 4302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>
        <SGBaseType safSgType="safSgType=ta_tgen_oneplSgType">
          <SGType safVersion="safVersion=1.0.0">
            <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=ta_tgen_oneplSuType"/>
            <redundancy saAmfSgtRedundancyModel="5"/>
            <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3"/>
            <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3"/>
            <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000"/>
          </SGType>
        </SGBaseType>
        <ServiceBaseType safSvcType="safSvcType=ta_tgen_oneplSvcType">
          <ServiceType safVersion="safVersion=1.0.0">
            <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType"/>
          </ServiceType>
        </ServiceBaseType>
        <CSBaseType safCSType="safCSType=ta_tgen_oneplCsType">
          <CSType safVersion="safVersion=1.0.0"/>
        </CSBaseType>
        <SUBaseType safSuType="safSuType=ta_tgen_oneplSuType">
          <SUType safVersion="safVersion=1.0.0">
            <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1"/>
            <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=TAPPVER\,safCompType=ta_tgen_oneplCompType"/>
            <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=ta_tgen_oneplSvcType"/>
          </SUType>
        </SUBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_oneplCompType">
          <CompType safVersion="safVersion=TAPPVER">
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType" saAmfCtCompCapability="6"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
    	      <cmdArgv>instantiate 7102</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 7102</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 7102</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
          </CompType>
        </CompBaseType>"""

        self.camp = self.camp + """
      </amfEntityTypes>
    </addToImm>"""
        

    def CampInitAction(self):
        self.camp = self.camp + """
    <campInitAction>
      <doCliCommand  args="ERIC-Test_App-CXP9013968_3-TAPPVER" command="cmw-addToImm"/> 
      <undoCliCommand  args="" command="/bin/true"/> 
      <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster"/>
    </campInitAction>
  </campaignInitialization>"""

    def UpgradeProcedure(self):
        self.camp = self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=Install">
    <outageInfo>
      <acceptableServiceOutage>
        <all/>
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000"/>
    </outageInfo>
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit/>
            <activationUnit>
              <actedOn>
                <byName objectDN="safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global"/>
                <byName objectDN="safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global"/>"""
    
        if 1 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=SC-2,safSg=ta_tapp_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_all,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgc_sc,safApp=ta_global"/>
                <byName objectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global"/>"""
        if 2 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_onepl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_onepl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgc_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-3,safSg=ta_tgen_onepl,safApp=ta_global"/>"""
               
        if 3 < self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tgc_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-4,safSg=ta_tgen_all,safApp=ta_global"/>"""
        i = 5
        while i <= self.numOfNodes:
            self.camp = self.camp + """
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_all,safApp=ta_global"/>
                <byName objectDN="safSu=PL-%d,safSg=ta_tapp_pl,safApp=ta_global"/>
                <byName objectDN="safSu=PL-%d,safSg=ta_tgen_all,safApp=ta_global"/>""" % (i,i,i)
            i = i +1

        self.camp = self.camp + """
              </actedOn>
              <added objectClassName="SaAmfNodeGroup" parentObjectDN="safAmfCluster=myAmfCluster">
                <attribute name="safAmfNodeGroup" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safAmfNodeGroup=TGCs</value>
                </attribute>
                <attribute name="saAmfNGNodeList" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNode=SC-1,safAmfCluster=myAmfCluster</value>"""

        if 1 < self.numOfNodes:
            self.camp = self.camp + """
                  <value>safAmfNode=SC-2,safAmfCluster=myAmfCluster</value>"""
            
        if 2 < self.numOfNodes:
            self.camp = self.camp + """
                  <value>safAmfNode=PL-3,safAmfCluster=myAmfCluster</value>"""
            
        if 3 < self.numOfNodes:
            self.camp = self.camp + """
                  <value>safAmfNode=PL-4,safAmfCluster=myAmfCluster</value>"""

        self.camp = self.camp + """
                </attribute>
              </added>
              <added objectClassName="SaAmfApplication" parentObjectDN="=">
                <attribute name="safApp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfAppType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safAppType=ta_global_AppType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tapp_sc</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tapp_scSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefActiveSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
                <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
                <attribute name="saAmfSGMaxActiveSIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSGMaxStandbySIsperSU" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-SC-NWay-InSvcSu</value> <!-- CHANGE SC-NWay-InSvcSu -->
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tapp_sc</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tapp_scSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tapp_sc,safApp=ta_global</value>
                </attribute>
                <attribute name="saAmfSIPrefStandbyAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSIPrefActiveAssignments" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-SC-NWay-InSvcSu</value> <!-- CHANGE SC-NWay-InSvcSu -->
                </attribute>
                <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                  <value>2</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tapp_sc,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tapp_sc</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tapp_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tapp_onesc</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tapp_onescSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
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
                  <value>safSi=ta_tapp_onesc</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tapp_onescSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tapp_onesc,safApp=ta_global</value>
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
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tapp_onesc,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tapp_onesc</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tapp_onescCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgc_all</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgc_allSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=AllNodes,safAmfCluster=myAmfCluster</value>
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
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-SC-NWay-InSvcSu</value> <!-- CHANGE SC-NWay-InSvcSu -->
                </attribute>
                <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tgc_all</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgc_allSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgc_all,safApp=ta_global</value>
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
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgc_all,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgc_all</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgc_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgc_sc</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgc_scSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-SC-NWay-InSvcSu</value> <!-- CHANGE SC-NWay-InSvcSu -->
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tgc_sc</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgc_scSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgc_sc,safApp=ta_global</value>
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
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgc_sc,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgc_sc</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgc_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgc_onesc</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgc_onescSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
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
                  <value>safSi=ta_tgc_onesc</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgc_onescSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgc_onesc,safApp=ta_global</value>
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
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgc_onesc,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgc_onesc</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgc_onescCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgen_sc</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgen_scSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
                </attribute>
                <attribute name="saAmfSGAutoAdjust" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGAutoRepair" type="SA_IMM_ATTR_SAUINT32T">
                  <value>0</value>
                </attribute>
                <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                  <value>CHANGE-SC-NWay-InSvcSu</value> <!-- CHANGE SC-NWay-InSvcSu -->
                </attribute>
              </added>
              <added objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSi=ta_tgen_sc</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgen_scSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgen_sc,safApp=ta_global</value>
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
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgen_sc,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgen_sc</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgen_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSg=ta_tgen_onesc</value>
                </attribute>
                <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSgType=ta_tgen_onescSgType</value>
                </attribute>
                <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                  <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
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
                  <value>safSi=ta_tgen_onesc</value>
                </attribute>
                <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSvcType=ta_tgen_onescSvcType</value>
                </attribute>
                <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                  <value>1</value>
                </attribute>
                <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                  <value>safSg=ta_tgen_onesc,safApp=ta_global</value>
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
              <added objectClassName="SaAmfCSI" parentObjectDN="safSi=ta_tgen_onesc,safApp=ta_global">
                <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safCsi=ta_tgen_onesc</value>
                </attribute>
                <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safCSType=ta_tgen_onescCsType</value>
                </attribute>
              </added>"""

        if 2 < self.numOfNodes:
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
                  <value>2</value>
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
                  <value>CHANGE-PL-2N-SiAct</value> <!-- 1 CHANGE PL-2N-SiAct --> <!-- was 3 -->
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
              </added>"""


        self.camp = self.camp + """
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_sc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-1</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_scSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_sc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_scCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_sc,safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global">
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
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_sc,safSu=SC-1,safSg=ta_tapp_sc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tapp_onesc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-1</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tapp_onescSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tapp_onesc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tapp_onescCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tapp_onesc,safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global">
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
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tapp_onesc,safSu=SC-1,safSg=ta_tapp_onesc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_all,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-1</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_allSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_all</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_allCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_all,safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global">
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
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_all,safSu=SC-1,safSg=ta_tgc_all,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_sc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-1</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_scSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_sc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_scCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_sc,safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global">
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
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_sc,safSu=SC-1,safSg=ta_tgc_sc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgc_onesc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-1</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgc_onescSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgc_onesc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgc_onescCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgc_onesc,safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global">
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
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgc_onesc,safSu=SC-1,safSg=ta_tgc_onesc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-1</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgen_scSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgen_sc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgen_scCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgen_sc,safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global">
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
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgen_sc,safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfSU" parentObjectDN="safSg=ta_tgen_onesc,safApp=ta_global">
                <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safSu=SC-1</value>
                </attribute>
                <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=1.0.0,safSuType=ta_tgen_onescSuType</value>
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
              </added>
              <added objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                  <value>safComp=ta_tgen_onesc</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=TAPPVER,safCompType=ta_tgen_onescCompType</value>
                </attribute>
              </added>
              <added objectClassName="SaAmfHealthcheck" parentObjectDN="safComp=ta_tgen_onesc,safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global">
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
              <added objectClassName="SaAmfCompCsType" parentObjectDN="safComp=ta_tgen_onesc,safSu=SC-1,safSg=ta_tgen_onesc,safApp=ta_global">
                <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                  <value>safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType</value>
                </attribute>
              </added>"""
                
        if 1 < self.numOfNodes:
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
              
        if 2 < self.numOfNodes:
            self.camp = self.camp + """
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

        
        if 3 < self.numOfNodes:
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
              </added>
"""

        i = 4
        while i < self.numOfNodes:
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
                  <value>%d</value>
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
                  <value>%d</value>
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
""" % (i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)

        self.camp = self.camp + """
              <swAdd bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin/">
                <plmExecEnv amfNode="safAmfNode=SC-1,safAmfCluster=myAmfCluster"/>"""
        if 2 <= self.numOfNodes:
            self.camp = self.camp + """
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster"/>"""
        i = 2
        while i < self.numOfNodes :
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

    def ProcWrapupAction(self):
        self.camp = self.camp + """
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tapp_sc,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tapp_sc,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tapp_onesc,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tapp_onesc,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgc_all,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgc_all,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgc_sc,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgc_sc,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgc_onesc,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgc_onesc,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgen_sc,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgen_sc,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction> 
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=ta_tgen_onesc,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=ta_tgen_onesc,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction>"""
        if 2 < self.numOfNodes:
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

def campaignCreator(fileName, numOfNodes, verTapp, verTgen, verTgc):
    camp  = testAppInstallCampaignCreator(fileName, numOfNodes, verTapp, verTgen, verTgc)
    result = testAppInstallCampaignCreator.create(camp)
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
    
    camp  = testAppInstallCampaignCreator("TappInstallCampaign.xml", options.numOfNodes, options.verTapp, options.verTgen, options.verTgc)
    testAppInstallCampaignCreator.create(camp)
