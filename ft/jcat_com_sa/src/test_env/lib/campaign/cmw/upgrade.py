#!/usr/bin/env jython

import re

class coreMwUpgradeCampaignCreator():
    def __init__(self, fileName, upgradeMethod, oldCommonVer, newCommonVer, oldOpensafVer, newOpensafVer, oldScVer, newScVer, safVer, noOfNodes):
        self.fileName      = fileName
        self.upgradeMethod = upgradeMethod
        self.oldCommonVer  = oldCommonVer
        self.newCommonVer     = newCommonVer   
        self.oldOpensafVer = oldOpensafVer
        self.newOpensafVer    = newOpensafVer
        self.oldScVer      = oldScVer
        self.newScVer         = newScVer
        self.safVer        = safVer
        self.noOfNodes     = int(noOfNodes)
        if 2 < self.noOfNodes:
            self.noOfPLs   = self.noOfNodes - 2
        else:
            self.noOfPLs   = 0
        self.camp          = ""
        #print "In __init__: fromVer = '%s', tover = %d" % (self.fromVer, self.toVer)

    def create(self):
        procedureName = ""
        campaignName = ""

        if "RoNo" == self.upgradeMethod:
            procedureName = "CoreMWRollingOverNode"
            campaignName  = "CMWRollingOverNode"
        elif "SsNo1" == self.upgradeMethod:
            procedureName = "CoreMWSinglestepOverNode1"
            campaignName  = "CMWSinglestepOverNode1"
        elif "SsNo2" == self.upgradeMethod:
            procedureName = "CoreMWSinglestepOverNode2"
            campaignName  = "CMWSinglestepOverNode2"
        elif "RoTe" == self.upgradeMethod:
            procedureName = "CoreMWRollingOverNodeWithTemplate"
            campaignName  = "CMWRollingOverNodeWithTemplate"
        else:
            procedureName = "Not Supported: %s" % self.upgradeMethod
            campaignName  = "Not Supported: %s" % self.upgradeMethod
            
        self.CampaignHead(campaignName)

        self.CampaignInitializationCompBaseType()
        self.CampaignInitializationCampInitAction()        
        
        if   "RoNo" == self.upgradeMethod or "RoTe" == self.upgradeMethod:
            self.ProcInit("%s_SCs" % procedureName, 1)
            self.RollingProcedure("SC")
            if self.noOfPLs != 0:
                self.ProcInit("%s_PLs" % procedureName, 2)
                self.RollingProcedure("PL")
            
        elif "SsNo1" == self.upgradeMethod:
            self.ProcInit("%s_SCs" % procedureName, 1)
            self.SinglestepProcedure()
        elif "SsNo2" == self.upgradeMethod:
            self.ProcInit("%s_PLs" % procedureName, 1)
            self.SinglestepProcedure()
            

        if "RoTe" == self.upgradeMethod:
            self.CampaignTailTemplate()
        else:
            self.CampaignTail()


        self.camp = re.sub('OLDCOMMONVER',  self.oldCommonVer, self.camp)
        self.camp = re.sub('NEWCOMMONVER',  self.newCommonVer, self.camp)
        self.camp = re.sub('OLDOPENSAFVER', self.oldOpensafVer, self.camp)
        self.camp = re.sub('NEWOPENSAFVER', self.newOpensafVer, self.camp)
        self.camp = re.sub('OLDSCVER',      self.oldScVer, self.camp)
        self.camp = re.sub('NEWSCVER',      self.newScVer, self.camp)
        self.camp = re.sub('OLDSAFVER',     self.safVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'Core MW update campaign created')

    def CampaignHead(self, campaignName):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-%s">
  <campaignInfo>
    <campaignPeriod />
  </campaignInfo>
  <campaignInitialization>""" % campaignName

    def CampaignInitializationCompBaseType(self):
        if  "SsNo2" != self.upgradeMethod:
            self.camp=self.camp + """
    <addToImm>
      <amfEntityTypes>
        <CompBaseType safCompType="safCompType=ERIC-ClusterMonitor" >
          <CompType safVersion="safVersion=NEWSCVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-ClusterMonitor" saAmfCtCompCapability="4" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="clustermonitor.sh" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="clustermonitor.sh" >
              <cmdArgv>cleanup</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="10000000000" saAmfHealthcheckMaxDuration="6000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-NEWSCVER" />
          </CompType>
        </CompBaseType>        
        <CompBaseType safCompType="safCompType=ERIC-EcimSwm">
            <CompType safVersion="safVersion=NEWSCVER">
                <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-EcimSwm" saAmfCtCompCapability="1" />
                <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
                <instantiateCmd saAmfCtRelPathInstantiateCmd="ecimswm.sh">
                    <cmdArgv>instantiate</cmdArgv>
                </instantiateCmd>
                <cleanupCmd saAmfCtRelPathCleanupCmd="ecimswm.sh">
                    <cmdArgv>cleanup</cmdArgv>
                </cleanupCmd>
                <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="10000000000" saAmfHealthcheckMaxDuration="6000000000" />
                <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-NEWSCVER" />
            </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ERIC-EcimPm">
            <CompType safVersion="safVersion=NEWSCVER">
                <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-EcimPm" saAmfCtCompCapability="1" />
                <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefDisableRestart="0" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
                <instantiateCmd saAmfCtRelPathInstantiateCmd="cmwpm.sh">
                    <cmdArgv>instantiate</cmdArgv>
                </instantiateCmd>
                <cleanupCmd saAmfCtRelPathCleanupCmd="cmwpm.sh">
                    <cmdArgv>cleanup</cmdArgv>
                </cleanupCmd>
                <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="10000000000" saAmfHealthcheckMaxDuration="6000000000" />
                <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-NEWSCVER" />
            </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ERIC-MdfImmCC" >
          <CompType safVersion="safVersion=NEWSCVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-MdfImmCC" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="cmwmdf_immcc.sh" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <!-- Missing in mdf_objects.xml
            <terminateCmd saAmfCtRelPathTerminateCmd="cmwmdf_immcc.sh" >
              <cmdArgv>cleanup</cmdArgv>
            </terminateCmd>
            -->
            <cleanupCmd saAmfCtRelPathCleanupCmd="cmwmdf_immcc.sh" >
              <cmdArgv>cleanup</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="10000000000" saAmfHealthcheckMaxDuration="6000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-NEWSCVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ERIC-OSAlarmBridge" >
          <CompType safVersion="safVersion=NEWCOMMONVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-OSAlarmBridge" saAmfCtCompCapability="7" />
            <compTypeDefaults saAmfCtDefDisableRestart="0" saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="8" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="3" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osalarmbridge.sh" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <terminateCmd saAmfCtRelPathTerminateCmd="osalarmbridge.sh" >
              <cmdArgv>cleanup</cmdArgv>
            </terminateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osalarmbridge.sh" >
              <cmdArgv>cleanup</cmdArgv>
            </cleanupCmd>
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_COMMON-CXP9017566_1-NEWCOMMONVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeAMFWDOG" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=AMFWDOG-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-amfwd" >
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-amfwd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="10000000000" saAmfHealthcheckMaxDuration="6000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeCLM" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=CLM-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="6" saAmfCtDefInstantiationLevel="2" saAmfCtDefDisableRestart="1" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-clmd" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-clmd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeCPD" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=CPD-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="6" saAmfCtDefInstantiationLevel="2" saAmfCtDefDisableRestart="1" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-ckptd" >
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-ckptd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeCPND" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=CPND-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-ckptnd" >
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-ckptnd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeDTS" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=DTS-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="360000000000" saAmfCtDefCallbackTimeout="360000000000" saAmfCtDefRecoveryOnError="6" saAmfCtDefDisableRestart="1" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-dtd" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-dtd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=A9FD64E12C12" saAmfHealthcheckPeriod="480000000000" saAmfHealthcheckMaxDuration="360000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeFMS" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=FMS-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="6" saAmfCtDefDisableRestart="1" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-fmd" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-fmd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeIMMD" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=IMMD-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="6" saAmfCtDefDisableRestart="1" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-immd" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-immd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeIMMND" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=IMMND-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-immnd" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-immnd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeLOG" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=LOG-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="360000000000" saAmfCtDefCallbackTimeout="360000000000" saAmfCtDefRecoveryOnError="6" saAmfCtDefDisableRestart="1" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-logd" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-logd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="480000000000" saAmfHealthcheckMaxDuration="360000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeNTF" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=NTF-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="6" saAmfCtDefInstantiationLevel="2" saAmfCtDefDisableRestart="1" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-ntfd" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-ntfd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeRDE" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=RDE-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="6" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-rded" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-rded" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeSMF" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=SMF-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="100000000000" saAmfCtDefRecoveryOnError="6" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-smfd" >
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-smfd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=A1B2" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypeSMFND" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=SMFND-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-smfnd" >
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-smfnd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=A1B2" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=ERIC-MdfGCC" >
          <CompType safVersion="safVersion=NEWCOMMONVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-MdfGCC" saAmfCtCompCapability="5" />
            <compTypeDefaults saAmfCtDefQuiescingCompleteTimeout="10000000000" saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="cmwmdf_gcc.sh" >
              <cmdArgv>instantiate</cmdArgv>
            </instantiateCmd>
            <!-- Missing in mdf_objects.xml
            <terminateCmd saAmfCtRelPathTerminateCmd="cmwmdf_gcc.sh" >
              <cmdArgv>cleanup</cmdArgv>
            </terminateCmd>
            -->
            <cleanupCmd saAmfCtRelPathCleanupCmd="cmwmdf_gcc.sh" >
              <cmdArgv>cleanup</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="10000000000" saAmfHealthcheckMaxDuration="6000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_COMMON-CXP9017566_1-NEWCOMMONVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypePMD" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=PMD-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="100000000000" saAmfCtDefRecoveryOnError="6" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-pmd" >
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-pmd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
        <CompBaseType safCompType="safCompType=OpenSafCompTypePMND" >
          <CompType safVersion="safVersion=NEWOPENSAFVER" >
            <providesCSType safSupportedCsType="safSupportedCsType=safVersion=4.0.0\,safCSType=PMND-OpenSAF" saAmfCtCompCapability="1" />
            <compTypeDefaults saAmfCtCompCategory="1" saAmfCtDefClcCliTimeout="10000000000" saAmfCtDefCallbackTimeout="10000000000" saAmfCtDefRecoveryOnError="2" />
            <instantiateCmd saAmfCtRelPathInstantiateCmd="osaf-pmnd" >
              <cmdArgv>start</cmdArgv>
            </instantiateCmd>
            <cleanupCmd saAmfCtRelPathCleanupCmd="osaf-pmnd" >
              <cmdArgv>stop</cmdArgv>
            </cleanupCmd>
            <healthCheck safHealthcheckKey="safHealthcheckKey=Default" saAmfHealthcheckPeriod="240000000000" saAmfHealthcheckMaxDuration="180000000000" />
            <swBundle saAmfCtSwBundle="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" />
          </CompType>
        </CompBaseType>
      </amfEntityTypes>
    </addToImm>"""
        else:
            self.camp=self.camp + """
    <addToImm/>"""



    def CampaignInitializationCampInitAction(self):
        if  "SsNo2" != self.upgradeMethod:
            self.camp=self.camp + """
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWSCVER\,safCompType=ERIC-ClusterMonitor</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWSCVER\,safCompType=ERIC-EcimSwm</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWSCVER\,safCompType=ERIC-EcimPm</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWSCVER\,safCompType=ERIC-MdfImmCC</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0,safSuType=ERIC-CoreMWSuTypeAll" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWCOMMONVER\,safCompType=ERIC-OSAlarmBridge</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeND" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeAMFWDOG</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeND" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeCPND</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeND" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeIMMND</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeND" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeSMFND</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeCLM</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeCPD</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeDTS</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeFMS</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeIMMD</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeLOG</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeNTF</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeRDE</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypeSMF</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=1.0,safSuType=ERIC-CoreMWSuTypeAll" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWCOMMONVER\,safCompType=ERIC-MdfGCC</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeND" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypePMND</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>
    <campInitAction>
      <immCCB ccbFlags="0" >
        <create objectClassName="SaAmfSutCompType" parentObjectDN="safVersion=4.0.0,safSuType=OpenSafSuTypeServer" >
          <attribute name="safMemberCompType" type="SA_IMM_ATTR_SANAMET" >
            <value>safMemberCompType=safVersion=NEWOPENSAFVER\,safCompType=OpenSafCompTypePMD</value>
          </attribute>
          <attribute name="saAmfSutMinNumComponents" type="SA_IMM_ATTR_SAUINT32T" >
            <value>1</value>
          </attribute>
        </create>
      </immCCB>
    </campInitAction>"""
        self.camp=self.camp + """
  </campaignInitialization>"""

    def ProcInit(self, procedureName, execLevel):
        self.camp=self.camp + """
  <upgradeProcedure safSmfProcedure="safSmfProc=%s" saSmfExecLevel="%s">
    <outageInfo>
      <acceptableServiceOutage>
        <all />
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000" />
    </outageInfo>""" % (procedureName, execLevel)

    def RollingProcedure(self, nodeGroup):
        self.camp=self.camp + """
    <upgradeMethod>
      <rollingUpgrade>
        <upgradeScope>
          <byTemplate>
            <targetNodeTemplate objectDN="safAmfNodeGroup=%ss,safAmfCluster=myAmfCluster" >""" % nodeGroup
        
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <swRemove bundleDN="CMW_GETDN(^safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-OLDOPENSAFVER$)" pathnamePrefix="/usr/lib64/opensaf/clc-cli" />
              <swRemove bundleDN="CMW_GETDN(^safSmfBundle=ERIC-COREMW_COMMON-CXP9017566_1-OLDCOMMONVER$)" pathnamePrefix="/opt/coremw/clc-cli" />"""
            if "SC" == nodeGroup:
                self.camp=self.camp + """
          <swRemove bundleDN="CMW_GETDN(^safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-OLDSCVER$)" pathnamePrefix="/opt/coremw/clc-cli" />"""
        else:
            self.camp=self.camp + """
              <swRemove bundleDN="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-OLDOPENSAFVER" pathnamePrefix="/usr/lib64/opensaf/clc-cli" />
              <swRemove bundleDN="safSmfBundle=ERIC-COREMW_COMMON-CXP9017566_1-OLDCOMMONVER" pathnamePrefix="/opt/coremw/clc-cli" />"""
            if "SC" == nodeGroup:
                self.camp=self.camp + """
          <swRemove bundleDN="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-OLDSCVER" pathnamePrefix="/opt/coremw/clc-cli" />"""
            
        self.camp=self.camp + """
              <swAdd bundleDN="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" pathnamePrefix="/usr/lib64/opensaf/clc-cli" />
              <swAdd bundleDN="safSmfBundle=ERIC-COREMW_COMMON-CXP9017566_1-NEWCOMMONVER" pathnamePrefix="/opt/coremw/clc-cli" />"""
         

        if "SC" == nodeGroup:
            self.camp=self.camp + """
              <swAdd bundleDN="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-NEWSCVER" pathnamePrefix="/opt/coremw/clc-cli" />
            </targetNodeTemplate>
            <targetEntityTemplate>"""
            if "RoTe" == self.upgradeMethod:
                self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-ClusterMonitor$)" />"""
            else:
                self.camp=self.camp + """
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-ClusterMonitor" />"""
            self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-ClusterMonitor</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>"""
            
            self.camp=self.camp + """
            <targetEntityTemplate>"""
            if "RoTe" == self.upgradeMethod:
                self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-EcimSwm$)" />"""
            else:
                self.camp=self.camp + """
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-EcimSwm" />"""
            self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-EcimSwm</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>"""

            self.camp=self.camp + """
            <targetEntityTemplate>"""
            if "RoTe" == self.upgradeMethod:
                self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-EcimPm$)" />"""
            else:
                self.camp=self.camp + """
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-EcimPm" />"""
            self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-EcimPm</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>"""

            self.camp=self.camp + """
            <targetEntityTemplate>"""
            if "RoTe" == self.upgradeMethod:
                self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-MdfImmCC$)" />"""
            else:
                self.camp=self.camp + """
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-MdfImmCC" />"""
            self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-MdfImmCC</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>"""      
        else:
            self.camp=self.camp + """
            </targetNodeTemplate>"""
                      
        self.camp=self.camp + """
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
                self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeAMFWDOG$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeAMFWDOG" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeAMFWDOG</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeCLM$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCLM" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeCLM</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeCPD$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPD" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeCPD</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeCPND$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPND" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeCPND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeDTS$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeDTS" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeDTS</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""       
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeFMS$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeFMS" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeFMS</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeIMMD$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMD" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeIMMD</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeIMMND$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMND" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeIMMND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeLOG$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeLOG" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeLOG</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeNTF$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeNTF" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeNTF</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeRDE$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeRDE" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeRDE</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeSMF$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMF" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeSMF</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeSMFND$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMFND" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeSMFND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-OSAlarmBridge$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDCOMMONVER,safCompType=ERIC-OSAlarmBridge" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWCOMMONVER,safCompType=ERIC-OSAlarmBridge</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""
        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-MdfGCC$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDCOMMONVER,safCompType=ERIC-MdfGCC" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWCOMMONVER,safCompType=ERIC-MdfGCC</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""

        if "SC" == nodeGroup:

            if "RoTe" == self.upgradeMethod:
                self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypePMD$)" />"""
            else:
                self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMD" />"""
            self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypePMD</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>"""

        if "RoTe" == self.upgradeMethod:
            self.camp=self.camp + """
              <type objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypePMND$)" />"""
        else:
            self.camp=self.camp + """
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMND" />"""
        self.camp=self.camp + """
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypePMND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </byTemplate>
        </upgradeScope>
        <upgradeStep />
      </rollingUpgrade>
    </upgradeMethod>
  </upgradeProcedure>"""

        
    def SinglestepProcedure(self):
        self.camp=self.camp + """
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>
          <forModify>
            <activationUnit>
              <actedOn>"""
        if "SsNo1" == self.upgradeMethod:
            self.camp=self.camp + """
                  <byName objectDN="safAmfNode=SC-1,safAmfCluster=myAmfCluster"/>"""
            if 1 < self.noOfNodes:
                self.camp=self.camp + """
                  <byName objectDN="safAmfNode=SC-2,safAmfCluster=myAmfCluster"/>"""
        else:
            noOfPLs=int(self.noOfPLs)
            i = 0
            while i < noOfPLs:
                self.camp=self.camp + """\n                  <byName objectDN="safAmfNode=PL-%d,safAmfCluster=myAmfCluster"/>""" % (i + 3)
                i = i + 1

        self.camp=self.camp + """
              </actedOn>
              <swRemove bundleDN="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-OLDOPENSAFVER" pathnamePrefix="/usr/lib64/opensaf/clc-cli" />
              <swRemove bundleDN="safSmfBundle=ERIC-COREMW_COMMON-CXP9017566_1-OLDCOMMONVER" pathnamePrefix="/opt/coremw/clc-cli" />"""
        if "SsNo1" == self.upgradeMethod:
            self.camp=self.camp + """
          <swRemove bundleDN="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-OLDSCVER" pathnamePrefix="/opt/coremw/clc-cli" />"""
            
        self.camp=self.camp + """
              <swAdd bundleDN="safSmfBundle=ERIC-COREMW_OPENSAF-CXP9017656_1-NEWOPENSAFVER" pathnamePrefix="/usr/lib64/opensaf/clc-cli" />
              <swAdd bundleDN="safSmfBundle=ERIC-COREMW_COMMON-CXP9017566_1-NEWCOMMONVER" pathnamePrefix="/opt/coremw/clc-cli" />"""
         

        if "SsNo1" == self.upgradeMethod:
            self.camp=self.camp + """
              <swAdd bundleDN="safSmfBundle=ERIC-COREMW_SC-CXP9017565_1-NEWSCVER" pathnamePrefix="/opt/coremw/clc-cli" />
            </activationUnit>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-ClusterMonitor" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-ClusterMonitor</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-EcimSwm" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-EcimSwm</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-EcimPm" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-EcimPm</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
             <targetEntityTemplate>
              <type objectDN="safVersion=OLDSCVER,safCompType=ERIC-MdfImmCC" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWSCVER,safCompType=ERIC-MdfImmCC</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>"""
        else:
            self.camp=self.camp + """
            </activationUnit>"""
                
        self.camp=self.camp + """
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeAMFWDOG" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeAMFWDOG</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCLM" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeCLM</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPD" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeCPD</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPND" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeCPND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
              <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeDTS" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeDTS</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeFMS" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeFMS</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMD" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeIMMD</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMND" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeIMMND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeLOG" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeLOG</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeNTF" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeNTF</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeRDE" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeRDE</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMF" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeSMF</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMFND" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypeSMFND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDCOMMONVER,safCompType=ERIC-OSAlarmBridge" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWCOMMONVER,safCompType=ERIC-OSAlarmBridge</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDCOMMONVER,safCompType=ERIC-MdfGCC" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWCOMMONVER,safCompType=ERIC-MdfGCC</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMD" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypePMD</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
            <targetEntityTemplate>
              <type objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMND" />
              <modifyOperation operation="SA_IMM_ATTR_VALUES_REPLACE" >
                <attribute name="saAmfCompType" type="SA_IMM_ATTR_SANAMET" >
                  <value>safVersion=NEWOPENSAFVER,safCompType=OpenSafCompTypePMND</value>
                </attribute>
              </modifyOperation>
            </targetEntityTemplate>
          </forModify>
        </upgradeScope>
        <upgradeStep />
      </singleStepUpgrade>
    </upgradeMethod>
  </upgradeProcedure>"""

        
    def CampaignTail(self):
        
        self.camp=self.camp + """
  <campaignWrapup>"""
        if "SsNo1" != self.upgradeMethod:
            self.camp=self.camp + """
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSCVER,safCompType=ERIC-ClusterMonitor" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSCVER,safCompType=ERIC-EcimSwm" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSCVER,safCompType=ERIC-EcimPm" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSCVER,safCompType=ERIC-MdfImmCC" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDCOMMONVER,safCompType=ERIC-MdfGCC" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=A1B2,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMF" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=A1B2,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMFND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=A9FD64E12C12,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeDTS" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeAMFWDOG" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCLM" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeFMS" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeLOG" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeNTF" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeRDE" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safHealthcheckKey=Default,safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSCVER\,safCompType=ERIC-ClusterMonitor,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSCVER\,safCompType=ERIC-EcimSwm,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSCVER\,safCompType=ERIC-EcimPm,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSCVER\,safCompType=ERIC-MdfImmCC,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDCOMMONVER\,safCompType=ERIC-MdfGCC,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeAll" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDCOMMONVER\,safCompType=ERIC-OSAlarmBridge,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeAll" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeAMFWDOG,safVersion=4.0.0,safSuType=OpenSafSuTypeND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeCLM,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeCPD,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeCPND,safVersion=4.0.0,safSuType=OpenSafSuTypeND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeDTS,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeFMS,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeIMMD,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeIMMND,safVersion=4.0.0,safSuType=OpenSafSuTypeND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeLOG,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeNTF,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeRDE,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeSMF,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypeSMFND,safVersion=4.0.0,safSuType=OpenSafSuTypeND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypePMD,safVersion=4.0.0,safSuType=OpenSafSuTypeServer" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safMemberCompType=safVersion=OLDSAFVER\,safCompType=OpenSafCompTypePMND,safVersion=4.0.0,safSuType=OpenSafSuTypeND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=AMFWDOG-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeAMFWDOG" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-ClusterMonitor,safVersion=OLDSCVER,safCompType=ERIC-ClusterMonitor" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-EcimSwm,safVersion=OLDSCVER,safCompType=ERIC-EcimSwm" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-MdfImmCC,safVersion=OLDSCVER,safCompType=ERIC-MdfImmCC" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-EcimPm,safVersion=OLDSCVER,safCompType=ERIC-EcimPm" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-MdfGCC,safVersion=OLDCOMMONVER,safCompType=ERIC-MdfGCC" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=1.0\,safCSType=ERIC-OSAlarmBridge,safVersion=OLDCOMMONVER,safCompType=ERIC-OSAlarmBridge" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=CLM-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCLM" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=CPD-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=CPND-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=DTS-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeDTS" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=FMS-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeFMS" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=IMMD-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=IMMND-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=LOG-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeLOG" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=NTF-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeNTF" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=RDE-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeRDE" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=SMF-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMF" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=SMFND-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMFND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=PMD-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safSupportedCsType=safVersion=4.0.0\,safCSType=PMND-OpenSAF,safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSCVER,safCompType=ERIC-ClusterMonitor" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSCVER,safCompType=ERIC-EcimSwm" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSCVER,safCompType=ERIC-EcimPm" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSCVER,safCompType=ERIC-MdfImmCC" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDCOMMONVER,safCompType=ERIC-MdfGCC" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDCOMMONVER,safCompType=ERIC-OSAlarmBridge" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeAMFWDOG" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCLM" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeCPND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeDTS" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeFMS" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeIMMND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeLOG" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeNTF" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeRDE" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMF" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypeSMFND" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMD" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="safVersion=OLDSAFVER,safCompType=OpenSafCompTypePMND" />
      </immCCB>
    </campCompleteAction>"""
        self.camp=self.camp + """
    <waitToCommit />
    <waitToAllowNewCampaign />
    <removeFromImm />
  </campaignWrapup>
</upgradeCampaign>
"""

    def CampaignTailTemplate(self):
        
        self.camp=self.camp + """
  <campaignWrapup>"""
        if  "SsNo1" != self.upgradeMethod:
            self.camp=self.camp + """

    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=ERIC-ClusterMonitor$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=ERIC-EcimSwm$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=ERIC-EcimPm$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=ERIC-MdfImmCC$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=ERIC-MdfGCC$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=A1B2,safVersion=.*,safCompType=OpenSafCompTypeSMF$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=A1B2,safVersion=.*,safCompType=OpenSafCompTypeSMFND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=A9FD64E12C12,safVersion=.*,safCompType=OpenSafCompTypeDTS$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeAMFWDOG$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeCLM$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeCPD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeCPND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeFMS$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeIMMD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeIMMND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeLOG$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeNTF$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypeRDE$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypePMD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safHealthcheckKey=Default,safVersion=.*,safCompType=OpenSafCompTypePMND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=ERIC-ClusterMonitor,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=ERIC-EcimSwm,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=ERIC-EcimPm,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=ERIC-MdfImmCC,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=ERIC-MdfImmCC,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeController$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=ERIC-MdfGCC,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeAll$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=ERIC-OSAlarmBridge,safVersion=1.0,safSuType=ERIC-CoreMWSuTypeAll$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeAMFWDOG,safVersion=4.0.0,safSuType=OpenSafSuTypeND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeCLM,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeCPD,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeCPND,safVersion=4.0.0,safSuType=OpenSafSuTypeND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeDTS,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeFMS,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeIMMD,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeIMMND,safVersion=4.0.0,safSuType=OpenSafSuTypeND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeLOG,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeNTF,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeRDE,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeSMF,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypeSMFND,safVersion=4.0.0,safSuType=OpenSafSuTypeND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypePMD,safVersion=4.0.0,safSuType=OpenSafSuTypeServer$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safMemberCompType=safVersion=.*[\\\\],safCompType=OpenSafCompTypePMND,safVersion=4.0.0,safSuType=OpenSafSuTypeND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=1.0[\\\\],safCSType=ERIC-ClusterMonitor,safVersion=.*,safCompType=ERIC-ClusterMonitor$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=1.0[\\\\],safCSType=ERIC-EcimSwm,safVersion=.*,safCompType=ERIC-EcimSwm$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=1.0[\\\\],safCSType=ERIC-EcimPm,safVersion=.*,safCompType=ERIC-EcimPm$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=1.0[\\\\],safCSType=ERIC-MdfImmCC,safVersion=.*,safCompType=ERIC-MdfImmCC$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=1.0[\\\\],safCSType=ERIC-MdfGCC,safVersion=.*,safCompType=ERIC-MdfGCC$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=1.0[\\\\],safCSType=ERIC-OSAlarmBridge,safVersion=.*,safCompType=ERIC-OSAlarmBridge$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=AMFWDOG-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeAMFWDOG$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=CLM-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeCLM$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=CPD-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeCPD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=CPND-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeCPND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=DTS-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeDTS$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=FMS-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeFMS$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=IMMD-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeIMMD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=IMMND-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeIMMND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=LOG-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeLOG$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=NTF-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeNTF$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=RDE-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeRDE$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=SMF-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeSMF$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=SMFND-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypeSMFND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=PMD-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypePMD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safSupportedCsType=safVersion=4.0.0[\\\\],safCSType=PMND-OpenSAF,safVersion=.*,safCompType=OpenSafCompTypePMND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-ClusterMonitor$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-EcimSwm$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-EcimPm$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-MdfImmCC$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-MdfGCC$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=ERIC-OSAlarmBridge$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeAMFWDOG$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeCLM$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeCPD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeCPND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeDTS$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeFMS$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeIMMD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeIMMND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeLOG$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeNTF$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeRDE$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeSMF$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypeSMFND$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypePMD$)" />
      </immCCB>
    </campCompleteAction>
    <campCompleteAction>
      <immCCB ccbFlags="0" >
        <delete objectDN="CMW_GETDN(^safVersion=.*,safCompType=OpenSafCompTypePMND$)" />
      </immCCB>
    </campCompleteAction>
    <waitToCommit />
    <waitToAllowNewCampaign />
    <removeFromImm />
  </campaignWrapup>
</upgradeCampaign>
"""

def campaignCreator(fileName, upgradeMethod, oldCommonVer, newCommonVer, oldOpensafVer, newOpensafVer, oldScVer, newScVer, safVer, numOfNodes):
    camp  = coreMwUpgradeCampaignCreator(fileName, upgradeMethod, oldCommonVer, newCommonVer, oldOpensafVer, newOpensafVer, oldScVer, newScVer, safVer, numOfNodes)
    result = coreMwUpgradeCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-u", "--UpgradeMethod",
                      dest="upgradeMethod", default="RoNo",
                      help="Upgrade method, one of RollingOverNode (RoNo), RollingOverNodeWithTemplate (RoTe), SinglestepOverNode First Campaign (SsNo1), SinglestepOverNode Second Campaign (SsNo2). Default = RoNo")

    parser.add_option("-c", "--oldCommonVer",
                      dest="oldCommonVer", default="P1A01",
                      help="COREMW_COMMON version updating from, default = P1A01")
    parser.add_option("-C", "--newCommonVer",
                      dest="newCommonVer", default="R1A01",
                      help="COREMW_COMMON version updating to, default = R1A01")
    parser.add_option("-o", "--oldOpensafVer",
                      dest="oldOpensafVer", default="P2A02",
                      help="COREMW_OPENSAF version updating from, default = P2A02")
    parser.add_option("-O", "--newOpensafVer",
                      dest="newOpensafVer", default="R2A02",
                      help="COREMW_OPENSAF version updating to, default = R2A02")
    parser.add_option("-s", "--oldScVer",
                      dest="oldScVer", default="P3A03",
                      help="COREMW_SC version updating from, default = P3A03")
    parser.add_option("-S", "--newScVer",
                      dest="newScVer", default="R3A03",
                      help="COREMW_SC version updating from, to = R3A03")
    parser.add_option("-x", "--safVer",
                      dest="safVer", default="4.X.X",
                      help="opensaf version updating from, default = 4.X.X")

    parser.add_option("-n", "--NoOfNodes",
                      dest="numOfNodes", default="4",
                      help="Number of nodes. This is to decide if it is a 1 SC + 0, 2 SC + 0 PL or 2 SC + N PL system")

    (options, args) = parser.parse_args()

    if "RoNo" != options.upgradeMethod and "RoTe" != options.upgradeMethod and "SsNo1" != options.upgradeMethod and "SsNo2" != options.upgradeMethod:
        print "Upgrade method not supported: %s" % options.upgradeMethod
        sys.exit(1)
        
    campaignName = "%s.xml" % options.upgradeMethod
    
    camp  = coreMwUpgradeCampaignCreator(campaignName, options.upgradeMethod, options.oldCommonVer, options.newCommonVer, options.oldOpensafVer, options.newOpensafVer, options.oldScVer, options.newScVer, options.safVer, options.noOfNodes)
    coreMwUpgradeCampaignCreator.create(camp)
