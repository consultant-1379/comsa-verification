#!/usr/bin/env jython

import re

class testAppUpgradeCampaignCreator():
    def __init__(self, fileName, fromTapp, toTapp, upgradeMethod, numNodes):
        self.fileName       = fileName
        self.fromTapp       = fromTapp
        self.toTapp         = toTapp
        self.upgradeMethod  = upgradeMethod
        self.noOfNodes      = int(numNodes)
        self.camp           = ""
        
        #print "In __init__: fromVer = '%s', tover = %d" % (self.fromVer, self.toVer)

    def create(self):
        procedureName = ""
        campaignName = ""
        if "RoNo" == self.upgradeMethod:
            procedureName = "TestAppRollingOverNode"
            campaignName  = "TappUpgradeRollingNode"
        elif "SsNo" == self.upgradeMethod:
            procedureName = "TestAppSinglestepOverNode"
            campaignName  = "TappUpgradeSingleNode"
        elif "SsSu" == self.upgradeMethod:
            procedureName = "TestAppSinglestepOverSU"
            campaignName  = "TappUpgradeSingleSU"
        else:
            procedureName = "Not Supported: %s" % self.upgradeMethod
            

        self.CampaignHead(campaignName)
        self.CampaignInitialization()

        self.UpgradeProcedure("%s_PLs" % procedureName, 1)
        self.ProcInitActionTappTgenTgc()
        if  "RoNo" == self.upgradeMethod:
            self.RollingProcedureTappTgenTgc()
        elif "SsNo" == self.upgradeMethod or "SsSu" == self.upgradeMethod:
            self.SinglestepProcedureTappTgen()
        self.ProcWrapupTappTgenTgc()

        self.CampaignTail()

        self.camp = re.sub('OLDTAPPVER', self.fromTapp, self.camp)
        self.camp = re.sub('NEWTAPPVER', self.toTapp, self.camp)
       
        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'testAppApp update campaign created')

    def CampaignHead(self, campaignName):
        self.camp = """<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file:/SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-%s">
  <campaignInfo>
    <campaignPeriod />
  </campaignInfo>""" % campaignName

    def CampaignInitialization(self):
        self.camp = self.camp + """
    <campaignInitialization>
    <addToImm>
      <amfEntityTypes>
        <CompBaseType safCompType="safCompType=ta_tapp_allCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
              <cmdArgv>instantiate 4301</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 4301</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 4301</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_scCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
              <cmdArgv>instantiate 8301</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 8301</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 8301</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_plCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
              <cmdArgv>instantiate 8001</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 8001</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 8001</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_oneplCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType"
              saAmfCtCompCapability="6" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
              <cmdArgv>instantiate 7101</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 7101</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 7101</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tapp_onescCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType"
              saAmfCtCompCapability="6" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tapp.sh">
              <cmdArgv>instantiate 7201 --response-time-implementer</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tapp.sh">
              <cmdArgv>terminate 7201 --response-time-implementer</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tapp.sh">
              <cmdArgv>cleanup 7201 --response-time-implementer</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_allCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
              <cmdArgv>instantiate 4302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 4302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 4302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_scCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
              <cmdArgv>instantiate 8302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 8302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 8302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_plCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="1" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
              <cmdArgv>instantiate 8002</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 8002</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 8002</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_oneplCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType"
              saAmfCtCompCapability="6" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
              <cmdArgv>instantiate 7102</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 7102</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 7102</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgc_onescCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType"
              saAmfCtCompCapability="6" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgc.sh">
              <cmdArgv>instantiate 7202</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgc.sh">
              <cmdArgv>terminate 7202</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgc.sh">
              <cmdArgv>cleanup 7202</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_allCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
              <cmdArgv>instantiate 4302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 4302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 4302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_scCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType"
              saAmfCtCompCapability="2" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
              <cmdArgv>instantiate 8302</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 8302</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 8302</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_oneplCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType"
              saAmfCtCompCapability="6" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
              <cmdArgv>instantiate 7102</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 7102</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 7102</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ta_tgen_onescCompType">
          <CompType safVersion="safVersion=NEWTAPPVER">
            <providesCSType
              safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType"
              saAmfCtCompCapability="6" />
            <compTypeDefaults saAmfCtCompCategory="1"
              saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="60000000000"
              saAmfCtDefCallbackTimeout="120000000000"
              saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="ta_tgen.sh">
              <cmdArgv>instantiate 7202</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="ta_tgen.sh">
              <cmdArgv>terminate 7202</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="ta_tgen.sh">
              <cmdArgv>cleanup 7202</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default"
              saAmfHealthcheckPeriod="240000000000"
              saAmfHealthcheckMaxDuration="10000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" />
          </CompType>
        </CompBaseType>
      </amfEntityTypes>
    </addToImm>
  </campaignInitialization>"""

    def UpgradeProcedure(self, procedureName, level):
        self.camp=self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=%s" saSmfExecLevel="%d">
    <outageInfo>
      <acceptableServiceOutage>
        <all />
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000" />
    </outageInfo>""" % (procedureName, level)

    def ProcInitActionTappTgenTgc(self):
        self.camp=self.camp + """
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tapp_allSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tapp_allCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tapp_scSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tapp_scCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tapp_plSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tapp_plCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tapp_oneplSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tapp_oneplCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tapp_onescSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tapp_onescCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgen_allSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgen_allCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgen_scSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgen_scCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgen_oneplSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgen_oneplCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgen_onescSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgen_onescCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgc_allSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgc_allCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgc_scSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgc_scCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgc_plSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgc_plCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgc_oneplSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgc_oneplCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType"
          parentObjectDN="safVersion=1.0.0,safSuType=ta_tgc_onescSuType">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWTAPPVER\,safCompType=ta_tgc_onescCompType</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>"""


    def RollingProcedureTappTgenTgc(self):
        self.camp=self.camp + """
    <upgradeMethod>
      <rollingUpgrade>
        <upgradeScope>
          <byTemplate>
            <targetNodeTemplate objectDN="safAmfNodeGroup=AllNodes,safAmfCluster=myAmfCluster">
              <swRemove bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-OLDTAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin" />
              <swAdd bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin" />
            </targetNodeTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_allCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_allCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_scCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_scCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_plCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_plCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_oneplCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_oneplCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_onescCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_onescCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_allCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_allCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_scCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_scCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_oneplCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_oneplCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_onescCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_onescCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_allCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_allCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_scCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_scCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_plCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_plCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_oneplCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_oneplCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_onescCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_onescCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </byTemplate>
        </upgradeScope>
        <upgradeStep saSmfStepRestartOption="1" saSmfStepMaxRetry="8" />
      </rollingUpgrade>
    </upgradeMethod>
"""
        
    def SinglestepProcedureTappTgen(self):
        self.camp=self.camp + """
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forModify>
            <activationUnit>
              <actedOn>"""

        if "SsNo" == self.upgradeMethod:
            self.camp=self.camp + """
                 <byName objectDN="safAmfNode=SC-1,safAmfCluster=myAmfCluster"/>"""

            i = self.noOfNodes
            if 1 < self.noOfNodes:
                i = 3
                self.camp=self.camp + """
                 <byName objectDN="safAmfNode=SC-2,safAmfCluster=myAmfCluster"/>"""

            while i <= self.noOfNodes:
                self.camp=self.camp + """
                 <byName objectDN="safAmfNode=PL-%d,safAmfCluster=myAmfCluster"/>""" % i
                i = i + 1

        if "SsSu" == self.upgradeMethod:
            self.camp=self.camp + """
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tapp_allSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tapp_scSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tapp_plSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tapp_oneplSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tapp_onescSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgen_allSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgen_scSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgen_oneplSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgen_onescSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgc_allSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgc_scSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgc_plSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgc_oneplSuType" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=ta_tgc_onescSuType" />
                 </byTemplate>"""  
        self.camp=self.camp + """
              </actedOn>           
              <swRemove bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-OLDTAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin"/>
              <swAdd bundleDN="safSmfBundle=ERIC-Test_App-CXP9013968_3-NEWTAPPVER" pathnamePrefix="/opt/ericsson.se/testapp/bin" />
            </activationUnit>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_allCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_allCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_scCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_scCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_plCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_plCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_oneplCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_oneplCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_onescCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tapp_onescCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_allCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_allCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_scCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_scCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_oneplCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_oneplCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_onescCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgen_onescCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
              <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_allCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_allCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_scCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_scCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_plCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_plCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_oneplCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_oneplCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_onescCompType" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWTAPPVER,safCompType=ta_tgc_onescCompType</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </forModify>
        </upgradeScope>
        <upgradeStep />
      </singleStepUpgrade>
    </upgradeMethod>"""

    def ProcWrapupTappTgenTgc(self):
        self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tapp_allCompType,safVersion=1.0.0,safSuType=ta_tapp_allSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tapp_scCompType,safVersion=1.0.0,safSuType=ta_tapp_scSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tapp_plCompType,safVersion=1.0.0,safSuType=ta_tapp_plSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tapp_oneplCompType,safVersion=1.0.0,safSuType=ta_tapp_oneplSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tapp_onescCompType,safVersion=1.0.0,safSuType=ta_tapp_onescSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgen_allCompType,safVersion=1.0.0,safSuType=ta_tgen_allSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgen_scCompType,safVersion=1.0.0,safSuType=ta_tgen_scSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgen_oneplCompType,safVersion=1.0.0,safSuType=ta_tgen_oneplSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgen_onescCompType,safVersion=1.0.0,safSuType=ta_tgen_onescSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tapp_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tapp_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tapp_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tapp_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tapp_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgen_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgen_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgen_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgen_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_allCsType,safVersion=OLDTAPPVER,safCompType=ta_tapp_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_scCsType,safVersion=OLDTAPPVER,safCompType=ta_tapp_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_plCsType,safVersion=OLDTAPPVER,safCompType=ta_tapp_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_oneplCsType,safVersion=OLDTAPPVER,safCompType=ta_tapp_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tapp_onescCsType,safVersion=OLDTAPPVER,safCompType=ta_tapp_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_allCsType,safVersion=OLDTAPPVER,safCompType=ta_tgen_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_scCsType,safVersion=OLDTAPPVER,safCompType=ta_tgen_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_oneplCsType,safVersion=OLDTAPPVER,safCompType=ta_tgen_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgen_onescCsType,safVersion=OLDTAPPVER,safCompType=ta_tgen_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgc_allCompType,safVersion=1.0.0,safSuType=ta_tgc_allSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgc_scCompType,safVersion=1.0.0,safSuType=ta_tgc_scSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgc_plCompType,safVersion=1.0.0,safSuType=ta_tgc_plSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgc_oneplCompType,safVersion=1.0.0,safSuType=ta_tgc_oneplSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDTAPPVER\,safCompType=ta_tgc_onescCompType,safVersion=1.0.0,safSuType=ta_tgc_onescSuType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgc_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgc_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgc_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgc_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDTAPPVER,safCompType=ta_tgc_onescCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_allCsType,safVersion=OLDTAPPVER,safCompType=ta_tgc_allCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_scCsType,safVersion=OLDTAPPVER,safCompType=ta_tgc_scCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_plCsType,safVersion=OLDTAPPVER,safCompType=ta_tgc_plCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_oneplCsType,safVersion=OLDTAPPVER,safCompType=ta_tgc_oneplCompType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=ta_tgc_onescCsType,safVersion=OLDTAPPVER,safCompType=ta_tgc_onescCompType" />
      </immCCB>
    </procWrapupAction>
  </upgradeProcedure>
"""

    def CampaignTail(self):
        self.camp=self.camp + """
  <campaignWrapup>
    <waitToCommit />
    <waitToAllowNewCampaign />
    <removeFromImm>
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_allCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_scCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_plCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_oneplCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tapp_onescCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_allCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_scCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_plCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_oneplCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgc_onescCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_allCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_scCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_oneplCompType" />
      <amfEntityTypeDN objectDN="safVersion=OLDTAPPVER,safCompType=ta_tgen_onescCompType" />
    </removeFromImm>
  </campaignWrapup>
</upgradeCampaign>
"""



def campaignCreator(fileName, fromTapp, toTapp,  upgradeMethod, numNodes=0):
    camp  = testAppUpgradeCampaignCreator(fileName,fromTapp, toTapp, upgradeMethod, numNodes)
    result = testAppUpgradeCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-u", "--UpgradeMethod",
                      dest="upgradeMethod", default="RoNo",
                      help="Upgrade method, one of RollingOverNode (RoNo), SinglestepOverNode (SsNo), SinglestepOverSU (SsSu). Default = RoNo")

    parser.add_option("-a", "--fromVerTapp",
                      dest="fromTapp", default="P1A01",
                      help="tapp application from version, default = P1A01")
    parser.add_option("-g", "--fromVerTgen",
                      dest="fromTgen", default="P1A01",
                      help="tgen application from version, default = P1A01")
    parser.add_option("-c", "--fromVerTgc",
                      dest="fromTgc", default="P1A01",
                      help="tgc application from version, default = P1A01")

    parser.add_option("-b", "--toVerTapp",
                      dest="toTapp", default="P1A01",
                      help="tapp application to version, default = P1A01")
    parser.add_option("-e", "--toVerTgen",
                      dest="toTgen", default="P1A01",
                      help="tgen application to version, default = P1A01")
    parser.add_option("-d", "--toVerTgc",
                      dest="toTgc", default="P1A01",
                      help="tgc application to version, default = P1A01")

    parser.add_option("-n", "--numOfNodes",
                      dest="numNodes", default="4",
                      help="tgc application to version, default = P1A01")

    (options, args) = parser.parse_args()

    if "RoNo" != options.upgradeMethod and "SsNo" != options.upgradeMethod and "SsSu" != options.upgradeMethod:
        print "Upgrade method not supported: %s" % options.upgradeMethod
        sys.exit(1)
        
    #if 2 > options.noOfPLs:
    #    print "Number of PLs(%d) must be at least 2" % options.noOfPLs
    #    sys.exit(1)


    fileName = "%s.xml" % options.upgradeMethod
    camp  = testAppUpgradeCampaignCreator(fileName, options.fromTapp, options.fromTgen, options.fromTgc, options.toTapp, options.toTgen, options.toTgc, options.upgradeMethod, options.numNodes)
    testAppUpgradeCampaignCreator.create(camp)
