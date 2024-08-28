#!/usr/bin/env jython

""" This module creates a campaign.xml to remove amfMeasureApp.
Number of PL nodes of target node must be given.
Number of SIs and SGs is optional, default value is 100 SIs and 1 SG.
"""
import re

class amfMeasureRemoveCampaignCreator():
    def __init__(self, fileName, noOfBlades, appVer='P1A01'):
        self.appVer     = appVer
        self.noOfBlades = noOfBlades      # Today only two supported noOfPLs
        self.camp       = "";
        self.fileName   = fileName
        #print "In __init__: fileName=%s, noOfBlades=%s, appVer=%s" % (fileName, noOfBlades, appVer)

    def create(self):
        self.CampaignHead()
        self.ForAddRemove()
        self.ProcWrapupAction()
        
        self.camp = re.sub('APPVER', self.appVer, self.camp)

        fd = open(self.fileName, 'w')
        fd.write(self.camp)
        fd.close()
        return ('SUCCESS', 'amfMeasureApp remove campaign created')


    def CampaignHead(self):
        self.camp="""<?xml version="1.0" encoding="utf-8"?>
<upgradeCampaign 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:noNamespaceSchemaLocation="file://SAI-AIS-SMF-UCS-A.01.01.04_modified.xsd" 
  safSmfCampaign="safSmfCampaign=ERIC-AmfMeasureAppRemove">
  <campaignInfo>
    <campaignPeriod />
  </campaignInfo>
  <campaignInitialization>
    <addToImm />
  </campaignInitialization>
  <upgradeProcedure safSmfProcedure="safSmfProc=Remove" saSmfExecLevel="1">
    <outageInfo>
      <acceptableServiceOutage>
        <all />
      </acceptableServiceOutage>
      <procedurePeriod saSmfProcPeriod="60000000000" />
    </outageInfo>
    <upgradeMethod>
      <singleStepUpgrade>
        <upgradeScope>"""

    def ForAddRemove(self):
        self.camp=self.camp + """
          <forAddRemove>
            <deactivationUnit>
              <actedOn>
"""
        
        self.camp=self.camp+'                <byName objectDN="safSu=SC-1,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />\n'
        self.camp=self.camp+'                <byName objectDN="safSu=SC-1,safSg=SC2N,safApp=AmfMeasureApp" />\n'
        self.camp=self.camp+'                <byName objectDN="safSu=SC-1,safSg=SCNoRed,safApp=AmfMeasureApp" />\n'

        
        if 2 <= self.noOfBlades:
            self.camp=self.camp+'                <byName objectDN="safSu=SC-2,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />\n'
            self.camp=self.camp+'                <byName objectDN="safSu=SC-2,safSg=SC2N,safApp=AmfMeasureApp" />\n'

        
        if 3 <= self.noOfBlades:
            self.camp=self.camp+'                <byName objectDN="safSu=PL-3,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />\n'
            self.camp=self.camp+'                <byName objectDN="safSu=PL-3,safSg=PL2N,safApp=AmfMeasureApp" />\n'
            self.camp=self.camp+'                <byName objectDN="safSu=PL-3,safSg=PLNoRed,safApp=AmfMeasureApp" />\n'

        if 3 <= self.noOfBlades:
            self.camp=self.camp+'                <byName objectDN="safSu=PL-4,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />\n'
            self.camp=self.camp+'                <byName objectDN="safSu=PL-4,safSg=PL2N,safApp=AmfMeasureApp" />\n'

        """
        i = 5
        while i <= self.noOfBlades:
            self.camp=self.camp+'                <byName objectDN="safSu=PL-%d,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />\n' % i
            i = i + 1

        self.camp=self.camp+'                <byName objectDN="safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />\n'
        self.camp=self.camp+'                <byName objectDN="safSg=SC2N,safApp=AmfMeasureApp" />\n'
        self.camp=self.camp+'                <byName objectDN="safSg=SCNoRed,safApp=AmfMeasureApp" />\n'

        if 3 <= self.noOfBlades:
            self.camp=self.camp+'                <byName objectDN="safSg=PL2N,safApp=AmfMeasureApp" />\n'
            self.camp=self.camp+'                <byName objectDN="safSg=PLNoRed,safApp=AmfMeasureApp" />\n'
        
                
        """
        self.camp=self.camp + """              </actedOn>
              <swRemove bundleDN="safSmfBundle=ERIC-AMFMEASURE-CXP9010004_1-APPVER" pathnamePrefix="/opt/AMFMEASURE/bin">
"""
        i=1
        while i <= self.noOfBlades:
            node = 'PL-%d' % i
            if 3 > i:
                node = 'SC-%d' % i
            self.camp=self.camp+'                <plmExecEnv amfNode="safAmfNode=%s,safAmfCluster=myAmfCluster" />\n' % node
            i = i + 1

        self.camp=self.camp + """              </swRemove>
            </deactivationUnit>
            <activationUnit />
          </forAddRemove>
         </upgradeScope>
        <upgradeStep />
      </singleStepUpgrade>
    </upgradeMethod>"""

    def ProcWrapupAction(self):
        self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=SC-1,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=SC-1,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=SC-1,safSg=SCNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        if 2 <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=SC-2,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=SC-2,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        if 3 <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=PL-3,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=PL-3,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=PL-3,safSg=PLNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        if 4 <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=PL-4,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=PL-4,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""
          
      
        i=5
        while i <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safComp=AmfMeasureApp,safSu=PL-%d,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>""" % i
            i = i + 1






        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N,safComp=AmfMeasureApp,safSu=SC-1,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safComp=AmfMeasureApp,safSu=SC-1,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed,safComp=AmfMeasureApp,safSu=SC-1,safSg=SCNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    """

        if 2 <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safComp=AmfMeasureApp,safSu=SC-2,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N,safComp=AmfMeasureApp,safSu=SC-2,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""
      
        if 3 <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N,safComp=AmfMeasureApp,safSu=PL-3,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safComp=AmfMeasureApp,safSu=PL-3,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed,safComp=AmfMeasureApp,safSu=PL-3,safSg=PLNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        if 4 <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N,safComp=AmfMeasureApp,safSu=PL-4,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safComp=AmfMeasureApp,safSu=PL-4,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        i=5
        while i <= self.noOfBlades:
            self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safComp=AmfMeasureApp,safSu=PL-%d,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>""" % i
            i = i + 1

        
        self.camp=self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safVersion=APPVER,safCompType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed,safVersion=APPVER,safCompType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSupportedCsType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N,safVersion=APPVER,safCompType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>"""
          

        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=SC-1,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=SC-1,safSg=SCNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=SC-1,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        if 2 <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=SC-2,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=SC-2,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""
        if 3 <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=PL-3,safSg=PLNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=PL-3,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=PL-3,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""
        if 4 <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=PL-4,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=PL-4,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        i = 5
        while i <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safComp=AmfMeasureApp,safSu=PL-%d,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>""" % i
            i = i + 1


        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-1,safSg=SCNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""
      
        if 2 <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=SC-2,safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        if 3 <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-3,safSg=PLNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        if 4 <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-4,safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-4,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>"""

        i = 5
        while i <= self.noOfBlades:
            self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSu=PL-%d,safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>""" % i
            i = i + 1



        self.camp = self.camp + """
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=AllNodesNWayActive,safSi=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=SC2N,safSi=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=SCNoRed,safSi=SCNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=PL2N,safSi=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safCsi=PLNoRed,safSi=PLNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=SCNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSi=PLNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=AllNodesNWayActive,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=PL2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=PLNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=SC2N,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safSg=SCNoRed,safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safApp=AmfMeasureApp" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=AmfMeasAppType2N,safVersion=1.0.0,safSvcType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNoRed,safVersion=1.0.0,safSvcType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCSType=safVersion=1.0.0\,safCSType=AmfMeasAppTypeNWayActive,safVersion=1.0.0,safSvcType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=APPVER\,safCompType=AmfMeasAppType2N,safVersion=1.0.0,safSuType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=APPVER\,safCompType=AmfMeasAppTypeNWayActive,safVersion=1.0.0,safSuType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safMemberCompType=safVersion=APPVER\,safCompType=AmfMeasAppTypeNoRed,safVersion=1.0.0,safSuType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safAppType=AmfMeasureAppType" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safCSType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safCSType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safCSType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSgType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSgType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSgType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSuType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSuType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSuType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSvcType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSvcType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=1.0.0,safSvcType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safVersion=APPVER,safCompType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safVersion=APPVER,safCompType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safHealthcheckKey=amfMeasureApp,safVersion=APPVER,safCompType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=APPVER,safCompType=AmfMeasAppType2N" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=APPVER,safCompType=AmfMeasAppTypeNWayActive" />
      </immCCB>
    </procWrapupAction>
    <procWrapupAction>
      <immCCB ccbFlags="0">
        <delete objectDN="safVersion=APPVER,safCompType=AmfMeasAppTypeNoRed" />
      </immCCB>
    </procWrapupAction>
  </upgradeProcedure>
  <campaignWrapup>
    <waitToCommit />
    <waitToAllowNewCampaign />
    <removeFromImm>
      <amfEntityTypeDN objectDN="safAppType=AmfMeasureAppType" />
      <amfEntityTypeDN objectDN="safCSType=AmfMeasAppType2N" />
      <amfEntityTypeDN objectDN="safCSType=AmfMeasAppTypeNoRed" />
      <amfEntityTypeDN objectDN="safCSType=AmfMeasAppTypeNWayActive" />
      <amfEntityTypeDN objectDN="safCompType=AmfMeasAppType2N" />
      <amfEntityTypeDN objectDN="safCompType=AmfMeasAppTypeNWayActive" />
      <amfEntityTypeDN objectDN="safCompType=AmfMeasAppTypeNoRed" />
      <amfEntityTypeDN objectDN="safSgType=AmfMeasAppType2N" />
      <amfEntityTypeDN objectDN="safSgType=AmfMeasAppTypeNWayActive" />
      <amfEntityTypeDN objectDN="safSgType=AmfMeasAppTypeNoRed" />
      <amfEntityTypeDN objectDN="safSuType=AmfMeasAppType2N" />
      <amfEntityTypeDN objectDN="safSuType=AmfMeasAppTypeNWayActive" />
      <amfEntityTypeDN objectDN="safSuType=AmfMeasAppTypeNoRed" />
      <amfEntityTypeDN objectDN="safSvcType=AmfMeasAppType2N" />
      <amfEntityTypeDN objectDN="safSvcType=AmfMeasAppTypeNoRed" />
      <amfEntityTypeDN objectDN="safSvcType=AmfMeasAppTypeNWayActive" />
    </removeFromImm>
  </campaignWrapup>
</upgradeCampaign>"""



def campaignCreator(fileName, noOfBlades, appVer):
    camp  = amfMeasureRemoveCampaignCreator(fileName, noOfBlades, appVer)
    result = amfMeasureRemoveCampaignCreator.create(camp)
    return result

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser()

    parser.add_option("-n", "--NoOfBlades", 
                      type="int", dest="noOfBlades", default=4,
                      help="Number of PLs, default 4")

    parser.add_option("-v", "--version",
                      dest="appVer", default="P1A01",
                      help="application version, default = P1A01")


    (options, args) = parser.parse_args()
        
    camp  = amfMeasureRemoveCampaignCreator("amfMeasureRemoveCampaign.xml", options.noOfBlades, options.appVer)
    amfMeasureRemoveCampaignCreator.create(camp)
