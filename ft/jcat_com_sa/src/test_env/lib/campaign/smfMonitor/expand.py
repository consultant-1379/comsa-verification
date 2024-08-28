#!/usr/bin/env jython

""" This module creates a campaign.xml to expand smfMonitorApp.
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

class smfMonitorExpandCampaignCreator():
    def __init__(self, fileName, appVer):
        self.fileName      = fileName
        self.appVer        = appVer

    def create(self):
        
        self.CampaignHead()
        self.CampaignInit()
        self.UpgradeProcedureHead()
        self.ProcInitAction()
        self.UpgradeProcedureMethod()
        self.ProcWrapupAction()
        self.CampaignWrapup()

        self.camp = re.sub('APPVER', self.appVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'smfMonitor install campaign created')

    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-SmfMonitorAppExpand">
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
        self.camp = self.camp + """
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forAddRemove>
            <deactivationUnit/>
            <activationUnit>
              <actedOn>
                <byName objectDN="safSu=SC-2,safSg=smfMonitorApp,safApp=smfMonitorApp" />
              </actedOn>
              <swAdd bundleDN="safSmfBundle=ERIC-SMFMONITOR-CXP9010002_1-APPVER" pathnamePrefix="/opt/SMFMONITOR/bin">
                <plmExecEnv amfNode="safAmfNode=SC-2,safAmfCluster=myAmfCluster" />
              </swAdd>
            </activationUnit>
          </forAddRemove>
        </upgradeScope>
        <upgradeStep/>
      </singleStepUpgrade>
    </upgradeMethod>
"""



    def ProcWrapupAction(self):
        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <modify objectDN = "safSg=smfMonitorApp,safApp=smfMonitorApp" operation = "SA_IMM_ATTR_VALUES_REPLACE">
          <attribute name="saAmfSGNumPrefInserviceSUs" type="SA_IMM_ATTR_SAUINT32T">
            <value>2</value>
          </attribute>
        </modify>
      </immCCB>
    </procWrapupAction>
    <!--
    <procWrapupAction> 
      <doAdminOperation   objectDN="safSi=SC-NWayActive,safApp=smfMonitorApp" operationID="SA_AMF_ADMIN_UNLOCK" />
      <undoAdminOperation objectDN="safSi=SC-NWayActive,safApp=smfMonitorApp" operationID="SA_AMF_ADMIN_LOCK" />
    </procWrapupAction>
    -->
"""




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



        


def campaignCreator(fileName, appVer):
    camp  = smfMonitorExpandCampaignCreator(fileName, appVer)
    result = smfMonitorExpandCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    
    parser.add_option("-v", "--AppVer",
                      dest="appVer", default="APPVER",
                      help="tapp application version, default = P1A01")

    (options, args) = parser.parse_args()
    
    camp  = smfMonitorExpandCampaignCreator("SmfMonitorExpandCampaign.xml", options.appVer)
    smfMonitorExpandCampaignCreator.create(camp)
