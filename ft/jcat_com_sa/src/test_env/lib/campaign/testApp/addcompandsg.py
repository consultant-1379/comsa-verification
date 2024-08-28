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

class testAppAddCompAndSgCampaignCreator():
    def __init__(self, fileName, verTapp, numOfNodes):
        self.fileName       = fileName
        self.verTapp        = verTapp
        self.camp           = ""
        self.numOfNodes = int(numOfNodes)
    

    def create(self):
       
        
        self.Campaign()
        
        self.camp = re.sub('TAPPVER', self.verTapp, self.camp)
      
        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'testApp upgrade campaign created')

    def Campaign(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="file://H:/xsd/SAI-AIS-SMF-UCS-A.01.02_modified.xsd"
    safSmfCampaign="safSmfCampaign=ERIC-TestAppAddCompAndSg">
    <campaignInfo>
        <campaignPeriod />
    </campaignInfo>
    <campaignInitialization>
        <addToImm>
            <amfEntityTypes>
                <CompBaseType safCompType="safCompType=LM">
                    <CompType safVersion="safVersion=1.0.0">
                        <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=LM" saAmfCtCompCapability="2"/>
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
                        <healthCheck safHealthcheckKey="safHealthcheckKey=A9FD64E12C" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
                        <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
                    </CompType>
                </CompBaseType>  
                <CSBaseType safCSType="safCSType=LM">
                    <CSType safVersion="safVersion=1.0.0" />
                </CSBaseType>
                <ServiceBaseType safSvcType="safSvcType=LM">
                    <ServiceType safVersion="safVersion=1.0.0">
                        <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=LM" />
                    </ServiceType>
                </ServiceBaseType>
                <SGBaseType safSgType="safSgType=APBM">
                    <SGType safVersion="safVersion=1.0.0">
                        <suType saAmfSgtValidSuTypes="safVersion=1.0.0,safSuType=APBM" />
                        <redundancy saAmfSgtRedundancyModel="5" />
                        <compRestart saAmfSgtDefCompRestartProb="100000" saAmfSgtDefCompRestartMax="3" />
                        <suRestart saAmfSgtDefSuRestartProb="20000" saAmfSgtDefSuRestartMax="3" />
                        <autoAttrs safAmfSgtDefAutoAdjust="0" safAmfSgtDefAutoRepair="1" saAmfSgtDefAutoAdjustProb="10000000" />
                    </SGType>           
                </SGBaseType>
                <SUBaseType safSuType="safSuType=APBM">
                    <SUType safVersion="safVersion=1.0.0">
                        <mandatoryAttrs saAmfSutIsExternal="0" saAmfSutDefSUFailover="1" />
                        <componentType saAmfSutMinNumComponents="1" safMemberCompType="safMemberCompType=safVersion=1.0.0\,safCompType=APBM" />
                        <supportedSvcType saAmfSutProvidesSvcType="safVersion=1.0.0,safSvcType=APBM" />
                    </SUType>
                </SUBaseType>                
                <CompBaseType safCompType="safCompType=APBM">
                    <CompType safVersion="safVersion=1.0.0">
                        <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=APBM" saAmfCtCompCapability="6" />
                        <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000" saAmfCtDefCallbackTimeout="120000000000" saAmfCtDefRecoveryOnError="2" />
                        <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
                           <cmdArgv>instantiate 7202</cmdArgv>
                        </instantiateCmd>
                        <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
                            <cmdArgv>terminate 7202</cmdArgv>
                        </terminateCmd>
                        <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
                            <cmdArgv>cleanup 7202</cmdArgv>
                        </cleanupCmd>
                        <healthCheck safHealthcheckKey="safHealthcheckKey=A9FD64E12C" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="10000000000"/>
                        <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER"/>
                    </CompType>
                </CompBaseType>                       
                <CSBaseType safCSType="safCSType=APBM">
                    <CSType safVersion="safVersion=1.0.0" />
                </CSBaseType>
                <ServiceBaseType safSvcType="safSvcType=APBM">
                    <ServiceType safVersion="safVersion=1.0.0">
                        <csType safMemberCSType="safMemberCSType=safVersion=1.0.0\,safCSType=APBM" />
                    </ServiceType>
                </ServiceBaseType>       
            </amfEntityTypes>
        </addToImm>
         <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfSG" parentObjectDN="safApp=ta_global">
                    <attribute name="safSg" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safSg=APBM</value>
                    </attribute>
                    <attribute name="saAmfSGType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safSgType=APBM</value>
                    </attribute>
                    <attribute name="saAmfSGSuHostNodeGroup" type="SA_IMM_ATTR_SANAMET">
                        <value>safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster</value>
                    </attribute>
                    <attribute name="saAmfSGNumPrefStandbySUs" type="SA_IMM_ATTR_SAUINT32T">
                        <value>1</value>
                    </attribute>
                    <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
                        <value>2</value>
                    </attribute>
                    <attribute name="saAmfSGNumPrefAssignedSUs" type="SA_IMM_ATTR_SAUINT32T">
                        <value>2</value>
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
        </campInitAction>
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfSU" parentObjectDN="safSg=APBM,safApp=ta_global">
                    <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safSu=SC-1</value>
                    </attribute>
                    <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safSuType=APBM</value>
                    </attribute>
                    <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                        <value>safAmfNode=SC-1,safAmfCluster=myAmfCluster</value>
                    </attribute>
                    <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                        <value>3</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfSU" parentObjectDN="safSg=APBM,safApp=ta_global">
                    <attribute name="safSu" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safSu=SC-2</value>
                    </attribute>
                    <attribute name="saAmfSUType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safSuType=APBM</value>
                    </attribute>
                    <attribute name="saAmfSUHostNodeOrNodeGroup" type="SA_IMM_ATTR_SANAMET">
                        <value>safAmfNode=SC-2,safAmfCluster=myAmfCluster</value>
                    </attribute>
                    <attribute name="saAmfSUAdminState" type="SA_IMM_ATTR_SAUINT32T">
                        <value>3</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction> """
        
        self.camp+="""
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=APBM,safApp=ta_global">
                    <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safComp=APBM</value>
                    </attribute>
                    <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safCompType=APBM</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction>
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfCompCsType" parentObjectDN="safComp=APBM,safSu=SC-1,safSg=APBM,safApp=ta_global">
                    <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                        <value>safSupportedCsType=safVersion=1.0.0\,safCSType=APBM</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfComp" parentObjectDN="safSu=SC-2,safSg=APBM,safApp=ta_global">
                    <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safComp=APBM</value>
                    </attribute>
                    <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safCompType=APBM</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction>
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfCompCsType" parentObjectDN="safComp=APBM,safSu=SC-2,safSg=APBM,safApp=ta_global">
                    <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                        <value>safSupportedCsType=safVersion=1.0.0\,safCSType=APBM</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction> """
        
        self.camp+="""
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                    <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safSi=APBM-1</value>
                    </attribute>
                    <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safSvcType=APBM</value>
                    </attribute>
                    <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                        <value>0</value>
                    </attribute>
                    <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                        <value>safSg=APBM,safApp=ta_global</value>
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
                </create>
            </immCCB>
        </campInitAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                    <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safSi=APBM-2</value>
                    </attribute>
                    <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safSvcType=APBM</value>
                    </attribute>
                    <attribute name="saAmfSIRank" type="SA_IMM_ATTR_SAUINT32T">
                        <value>0</value>
                    </attribute>
                    <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                        <value>safSg=APBM,safApp=ta_global</value>
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
                </create>
            </immCCB>
        </campInitAction> """
        
        self.camp+="""
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfCSI" parentObjectDN="safSi=APBM-1,safApp=ta_global">
                    <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safCsi=APBM</value>
                    </attribute>
                    <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safCSType=APBM</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <campInitAction>
            <immCCB ccbFlags="1">
                <create objectClassName="SaAmfCSI" parentObjectDN="safSi=APBM-2,safApp=ta_global">
                    <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safCsi=APBM</value>
                    </attribute>
                    <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safCSType=APBM</value>
                    </attribute>
                </create>
            </immCCB>
        </campInitAction> """
        
        self.camp+="""
    </campaignInitialization>
    <upgradeProcedure safSmfProcedure="safSmfProc=Add_LM_and_APBM" saSmfExecLevel="1">
        <outageInfo>
            <acceptableServiceOutage>
                <all />
            </acceptableServiceOutage>
            <procedurePeriod saSmfProcPeriod="60000000000" />
        </outageInfo>
        <procInitAction>
            <immCCB ccbFlags="0">
            <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0.0,safSuType=ta_tgen_scSuType">
                    <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
                        <value>safMemberCompType=safVersion=1.0.0\,safCompType=LM</value>
                    </attribute>
                </create>
            </immCCB>
        </procInitAction>
        <procInitAction>
            <immCCB ccbFlags="0">
            <create objectClassName="SaAmfComp" parentObjectDN="safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global">
                <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                    <value>safComp=LM</value>
                </attribute>
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                    <value>safVersion=1.0.0,safCompType=LM</value>
                </attribute>
        </create>
      </immCCB>
    </procInitAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <procInitAction>
            <immCCB ccbFlags="0">
                <create objectClassName="SaAmfComp" parentObjectDN="safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global">
                    <attribute name="safComp" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safComp=LM</value>
                    </attribute>
                    <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safCompType=LM</value>
                    </attribute>
                </create>
            </immCCB>
        </procInitAction> """
        
        self.camp+="""
        <upgradeMethod>
            <rollingUpgrade>
                <upgradeScope>
                    <byTemplate>
                        <targetNodeTemplate objectDN="safAmfNodeGroup=SCs,safAmfCluster=myAmfCluster">
                            <swAdd bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-TAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin" />
                        </targetNodeTemplate>
                    </byTemplate>
                </upgradeScope>
                <upgradeStep saSmfStepRestartOption="1" saSmfStepMaxRetry="0" />
            </rollingUpgrade>
        </upgradeMethod>
        <procWrapupAction>
            <immCCB ccbFlags="0">
                <create objectClassName="SaAmfSI" parentObjectDN="safApp=ta_global">
                    <attribute name="safSi" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safSi=LM</value>
                    </attribute>
                    <attribute name="saAmfSvcType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safSvcType=LM</value>
                    </attribute>
                    <attribute name="saAmfSIProtectedbySG" type="SA_IMM_ATTR_SANAMET">
                        <value>safSg=ta_tgen_sc,safApp=ta_global</value>
                    </attribute>
                    <attribute name="saAmfSIAdminState" type="SA_IMM_ATTR_SAUINT32T">
                        <value>2</value>
                    </attribute>
                </create>
            </immCCB>
        </procWrapupAction>
        <procWrapupAction>
            <immCCB ccbFlags="0">
                <create objectClassName="SaAmfCompCsType" parentObjectDN="safComp=LM,safSu=SC-1,safSg=ta_tgen_sc,safApp=ta_global">
                    <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                        <value>safSupportedCsType=safVersion=1.0.0\,safCSType=LM</value>
                    </attribute>
                </create>
            </immCCB>
        </procWrapupAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <procWrapupAction>
            <immCCB ccbFlags="0">
                <create objectClassName="SaAmfCompCsType" parentObjectDN="safComp=LM,safSu=SC-2,safSg=ta_tgen_sc,safApp=ta_global">
                    <attribute name="safSupportedCsType" type="SA_IMM_ATTR_SANAMET">
                        <value>safSupportedCsType=safVersion=1.0.0\,safCSType=LM</value>
                    </attribute>
                </create>
            </immCCB>
        </procWrapupAction> """
        
        self.camp+="""
        <procWrapupAction>
            <immCCB ccbFlags="0">
                <create objectClassName="SaAmfCSI" parentObjectDN="safSi=LM,safApp=ta_global">
                    <attribute name="safCsi" type="SA_IMM_ATTR_SASTRINGT">
                        <value>safCsi=LM</value>
                    </attribute>
                    <attribute name="saAmfCSType" type="SA_IMM_ATTR_SANAMET">
                        <value>safVersion=1.0.0,safCSType=LM</value>
                    </attribute>
                </create>
            </immCCB>
        </procWrapupAction>
        <procWrapupAction>
            <doAdminOperation objectDN="safSi=LM,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
            <undoAdminOperation objectDN="safSi=LM,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
        </procWrapupAction>
    </upgradeProcedure>
    <campaignWrapup>
        <campCompleteAction>
            <doAdminOperation objectDN="safSu=SC-1,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK_INSTANTIATION" />
            <undoAdminOperation objectDN="safSu=SC-1,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK_INSTANTIATION" />
        </campCompleteAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <campCompleteAction>
            <doAdminOperation objectDN="safSu=SC-2,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK_INSTANTIATION" />
            <undoAdminOperation objectDN="safSu=SC-2,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK_INSTANTIATION" />
        </campCompleteAction> """
        
        self.camp+="""
        <campCompleteAction>
            <doAdminOperation objectDN="safSu=SC-1,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
            <undoAdminOperation objectDN="safSu=SC-1,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
        </campCompleteAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <campCompleteAction>
            <doAdminOperation objectDN="safSu=SC-2,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
            <undoAdminOperation objectDN="safSu=SC-2,safSg=APBM,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
        </campCompleteAction> """
        
        self.camp+="""
        <campCompleteAction>
            <doAdminOperation objectDN="safSi=APBM-1,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
            <undoAdminOperation objectDN="safSi=APBM-1,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
        </campCompleteAction> """
        
        if 1 < self.numOfNodes:
            self.camp+="""
        <campCompleteAction>
            <doAdminOperation objectDN="safSi=APBM-2,safApp=ta_global" operationID="SA_AMF_ADMIN_UNLOCK" />
            <undoAdminOperation objectDN="safSi=APBM-2,safApp=ta_global" operationID="SA_AMF_ADMIN_LOCK" />
        </campCompleteAction> """
        
        self.camp+="""
        <waitToCommit />
        <waitToAllowNewCampaign />
        <removeFromImm />
    </campaignWrapup>
</upgradeCampaign>
"""



        


def campaignCreator(fileName, verTapp, numOfNodes = 4):
    camp  = testAppAddCompAndSgCampaignCreator(fileName, verTapp, numOfNodes)
    result = testAppAddCompAndSgCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()
    
    parser.add_option("-a", "--verTapp",
                      dest="verTapp", default="P1A01",
                      help="tapp application version, default = P1A01")
    parser.add_option("-n", "--numberOfNodes",
                      dest="numOfNodes", default="4",
                      help="Number of nodes, default = 4")


    (options, args) = parser.parse_args()

   
        
    camp  = testAppAddCompAndSgCampaignCreator("TappAddCompandSgCampaign.xml", options.verTapp, options.numOfNodes)
    testAppAddCompAndSgCampaignCreator.create(camp)
