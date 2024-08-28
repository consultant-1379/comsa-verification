#!/usr/bin/env jython

import re

class amfMeasureUpgradeCampaign():
    def __init__(self, fileName, fromVer, toVer, upgradeMethod, numNodes):
        self.fileName       = fileName
        self.fromVer        = fromVer
        self.toVer          = toVer
        self.upgradeMethod  = upgradeMethod
        self.noOfNodes      = int(numNodes)
        self.camp           = ""
        
        #print "In __init__: fromVer = '%s', tover = %d" % (self.fromVer, self.toVer)

    def create(self):
        procedureName = ""
        campaignName = ""
        if "RoNo" == self.upgradeMethod:
            procedureName = "AmfMeasAppRollingOverNode"
            campaignName  = "AmfMeasUpgradeRollingOverNode"
        elif "SsNo" == self.upgradeMethod:
            procedureName = "AmfMeasAppSinglestepOverNode"
            campaignName  = "AmfMeasUpgradeSingleOverNode"
        elif "SsSu" == self.upgradeMethod:
            procedureName = "AmfMeasAppSinglestepOverSU"
            campaignName  = "AmfMeasUpgradeSingleOverSU"
        else:
            procedureName = "Not Supported: %s" % self.upgradeMethod
            

        self.CampaignHead(campaignName)
        self.CampaignInitialization()

        self.UpgradeProcedure(procedureName, 1)
        self.ProcInitAction()
        if  "RoNo" == self.upgradeMethod:
            self.RollingProcedure()
        elif "SsNo" == self.upgradeMethod or "SsSu" == self.upgradeMethod:
            self.SinglestepProcedure()
        self.ProcWrapup()

        self.CampaignTail()

        self.camp = re.sub('OLDVER', self.fromVer, self.camp)
        self.camp = re.sub('NEWVER', self.toVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'amfMeasureApp update campaign created')

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
        <CompBaseType safCompType="safCompType=AmfMeasAppTypeNoRed">
          <CompType safVersion="safVersion=NEWVER">
            <providesCSType saAmfCtCompCapability="6" saAmfCtDefNumMaxActiveCsi="0" saAmfCtDefNumMaxStandbyCsi="0" safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefDisableRestart="0" saAmfCtDefInstantiationLevel="0" saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtDefRecoveryOnError="1"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>instantiate NoRed</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>cleanup NoRed</cmdArgv>
            </cleanupCmd>
            <healthCheck saAmfHealthcheckMaxDuration="180000000000" saAmfHealthcheckPeriod="240000000" safHealthcheckKey="safHealthcheckKey=amfMeasureApp"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-NEWVER"/>
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=AmfMeasAppTypeNWayActive">
          <CompType safVersion="safVersion=NEWVER">
            <providesCSType saAmfCtCompCapability="2" saAmfCtDefNumMaxActiveCsi="0" saAmfCtDefNumMaxStandbyCsi="0" safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefDisableRestart="0" saAmfCtDefInstantiationLevel="0" saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtDefRecoveryOnError="1"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>instantiate NWayActive</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>cleanup NWayActive</cmdArgv>
            </cleanupCmd>
            <healthCheck saAmfHealthcheckMaxDuration="180000000000" saAmfHealthcheckPeriod="240000000" safHealthcheckKey="safHealthcheckKey=amfMeasureApp"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-NEWVER"/>
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=AmfMeasAppType2N">
          <CompType safVersion="safVersion=NEWVER">
            <providesCSType saAmfCtCompCapability="1" saAmfCtDefNumMaxActiveCsi="0" saAmfCtDefNumMaxStandbyCsi="0" safSupportedCsType="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N"/>
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefDisableRestart="0" saAmfCtDefInstantiationLevel="0" saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtDefRecoveryOnError="1"/>
            <instantiateCmd saAmfCtRelPathInstantiateCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>instantiate 2N</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="AMFMEASURE/bin/amfMeasureApp_script">
              <cmdArgv>cleanup 2N</cmdArgv>
            </cleanupCmd>
            <healthCheck saAmfHealthcheckMaxDuration="180000000000" saAmfHealthcheckPeriod="240000000" safHealthcheckKey="safHealthcheckKey=amfMeasureApp"/>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-NEWVER"/>
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

    def ProcInitAction(self):
        self.camp=self.camp + """
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0.0,safSuType=AmfMeasAppTypeNoRed">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWVER\,safCompType=AmfMeasAppTypeNoRed</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0.0,safSuType=AmfMeasAppType2N">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWVER\,safCompType=AmfMeasAppType2N</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>
    <procInitAction>
      <immCCB ccbFlags="0">
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0.0,safSuType=AmfMeasAppTypeNWayActive">
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET">
            <value>safMemberCompType=safVersion=NEWVER\,safCompType=AmfMeasAppTypeNWayActive</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T">
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </procInitAction>"""



    def RollingProcedure(self):
        self.camp=self.camp + """
    <upgradeMethod>
      <rollingUpgrade>
        <upgradeScope>
          <byTemplate>
            <targetNodeTemplate objectDN="safAmfNodeGroup=AllNodes,safAmfCluster=myAmfCluster">
              <swRemove bundleDN="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-OLDVER" pathnamePrefix="/opt" />
              <swAdd bundleDN="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-NEWVER" pathnamePrefix="/opt" />
            </targetNodeTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDVER,safCompType=AmfMeasAppTypeNWayActive" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=AmfMeasAppTypeNWayActive</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDVER,safCompType=AmfMeasAppTypeNoRed" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=AmfMeasAppTypeNoRed</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDVER,safCompType=AmfMeasAppType2N" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=AmfMeasAppType2N</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </byTemplate>
        </upgradeScope>
        <upgradeStep saSmfStepRestartOption="1" saSmfStepMaxRetry="8" />
      </rollingUpgrade>
    </upgradeMethod>
"""
        
    def SinglestepProcedure(self):
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
                   <type objectDN="safVersion=1.0.0,safSuType=AmfMeasAppTypeNWayActive" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=AmfMeasAppTypeNoRed" />
                 </byTemplate>
                 <byTemplate>
                   <type objectDN="safVersion=1.0.0,safSuType=AmfMeasAppType2N" />
                 </byTemplate>"""
        self.camp=self.camp + """
              </actedOn>
              <swRemove bundleDN="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-OLDVER" pathnamePrefix="/opt"/>
              <swAdd bundleDN="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1" pathnamePrefix="/opt" />
            </activationUnit>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDVER,safCompType=AmfMeasAppTypeNWayActive" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=AmfMeasAppTypeNWayActive</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDVER,safCompType=AmfMeasAppTypeNoRed" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=AmfMeasAppTypeNoRed</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDVER,safCompType=AmfMeasAppType2N" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE">
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET">
                  <value>safVersion=NEWVER,safCompType=AmfMeasAppType2N</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </forModify>
        </upgradeScope>
        <upgradeStep />
      </singleStepUpgrade>
    </upgradeMethod>"""


    def ProcWrapup(self):
        self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDVER\,safCompType=AmfMeasAppTypeNWayActive,safVersion=1.0.0,safSuType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDVER\,safCompType=AmfMeasAppTypeNoRed,safVersion=1.0.0,safSuType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=OLDVER\,safCompType=AmfMeasAppType2N,safVersion=1.0.0,safSuType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safVersion=OLDVER,safCompType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safVersion=OLDVER,safCompType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safVersion=OLDVER,safCompType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safVersion=OLDVER,safCompType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed,safVersion=OLDVER,safCompType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N,safVersion=OLDVER,safCompType=AmfMeasAppType2N" />
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
      <amfEntityTypeDN objectDN="safVersion=OLDVER,safCompType=AmfMeasAppTypeNWayActive" />
      <amfEntityTypeDN objectDN="safVersion=OLDVER,safCompType=AmfMeasAppTypeNoRed" />
      <amfEntityTypeDN objectDN="safVersion=OLDVER,safCompType=AmfMeasAppType2N" />
    </removeFromImm>
  </campaignWrapup>
</upgradeCampaign>
"""



def campaignCreator(fileName, fromVer, toVer, upgradeMethod, numNodes=0):
    camp  = amfMeasureUpgradeCampaign(fileName,fromVer, toVer, upgradeMethod, numNodes)
    result = amfMeasureUpgradeCampaign.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-u", "--UpgradeMethod",
                      dest="upgradeMethod", default="RoNo",
                      help="Upgrade method, one of RollingOverNode (RoNo), SinglestepOverNode (SsNo), SinglestepOverSU (SsSu). Default = RoNo")

    parser.add_option("-f", "--fromVer",
                      dest="fromVer", default="P1A01",
                      help="application from version, default = P1A01")

    parser.add_option("-b", "--toVer",
                      dest="toVer", default="P1A01",
                      help="application to version, default = P1A01")

    parser.add_option("-n", "--numOfNodes",
                      dest="numNodes", default="4",
                      help="number of nodes, default = 4")

    (options, args) = parser.parse_args()

    if "RoNo" != options.upgradeMethod and "SsNo" != options.upgradeMethod and "SsSu" != options.upgradeMethod:
        print "Upgrade method not supported: %s" % options.upgradeMethod
        sys.exit(1)
        

    fileName = "%s.xml" % options.upgradeMethod
    camp  = amfMeasureUpgradeCampaign(fileName, options.fromVer, options.toVer, options.upgradeMethod, options.numNodes)
    amfMeasureUpgradeCampaign.create(camp)
