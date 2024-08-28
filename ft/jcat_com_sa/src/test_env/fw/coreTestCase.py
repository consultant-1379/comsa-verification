#!/usr/bin/env python
#coding=iso-8859-1
###############################################################################
#
# © Ericsson AB 2009 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################

'''File information:
   ===================================================
   File:  coreTestCase
   Rev:   P1A01
   Date:  2009-11-12

   Description:


'''
###############################################################################
# Python common resources imports
###############################################################################
import os
import sys
import time
import datetime
import random
import re
import test_env.lib.lib as lib
import test_env.lib.comsa_lib as comsa_lib
import test_env.lib.utils as utils
import test_env.lib.trace_lib as trace_lib
import test_env.lib.trace_cc_lib as trace_cc_lib
import test_env.lib.campaign_lib as campaign_lib
import test_env.lib.pm_lib as pm_lib
import test_env.lib.amfmeas_lib as amfmeas_lib
import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException
import omp.tf.misc_lib as misc_lib
import omp.tf.ssh_lib as ssh_lib
import omp.tf.hw_lib as hw_lib
import omp.tf.os_lib as os_lib
import omp.tf.ethswitch_lib as ethswitch_lib
import atexit

import coremw.notification_lib as notification_lib
import coremw.testapp_lib as testapp_lib
import coremw.saf_lib as saf_lib


###############################################################################
# FW imports
###############################################################################
import test_env.bin.lib.parameterHandler as ph
#from se.ericsson.jcat.omp.fw import OmpJythonTestCase
from se.ericsson.jcat.fw import NonUnitTestCase
from se.ericsson.jcat.fw import SUTHolder
from java.lang import System
from org.apache.log4j import Logger
from org.apache.log4j import Level




###############################################################################
# This is the parent class inherited by all testcases
###############################################################################
class CoreTestCase(NonUnitTestCase):

    def __init__(self, tag, name, config, testSuiteConfig, testCaseConfig, instance):
        NonUnitTestCase.__init__(self, name)
        self.myLogger = Logger.getLogger('coreTestCase logging')#use this only in this module
        logLevel = System.getProperty("jcat.logging")
        self.loadPl = System.getProperty("loadpl")
        self.loadSc = System.getProperty("loadsc")
        self.loadProfile = System.getProperty("loadprofile")
        self.setUpCheck = System.getProperty("setUpCheck")
        self.runTestCheck = System.getProperty("runTestCheck")
        self.tearDownCheck = System.getProperty("tearDownCheck")
        self.targetName = str(System.getProperty("###__TARGET_SYSTEM__###"))
        self.nrOfPlNodes = int(System.getProperty("nrOfPlNodes"))
        self.nrOfScNodes = int(System.getProperty("nrOfScNodes"))
        self.myLogger.setLevel(Level.toLevel(logLevel))
        self.tag = tag #TC tag
        self.name = name #TC name
        self.testConfig = config
        self.testSuiteConfig = testSuiteConfig
        self.testCaseConfig = testCaseConfig
        self.instance = instance
        self.iteration = None

        #paths
        self.workspace = os.environ.get("MY_WORKSPACE")
        self.repository = os.environ.get("MY_REPOSITORY")
        self.cxpArchive = '/vobs/coremw/release/cxp_archive/'

        #get library handles
        self.sshLib = ssh_lib
        self.hwLib = hw_lib
        self.miscLib = misc_lib
        self.osLib = os_lib
        self.testAppLib = testapp_lib
        self.notificationLib = notification_lib
        self.safLib = saf_lib
        self.comsa_lib = comsa_lib
        self.utils = utils
        self.trace_lib = trace_lib
        self.trace_cc_lib = trace_cc_lib
        self.lib = lib
        self.campaignLib = campaign_lib
        self.pmLib = pm_lib
        self.amfmeasLib = amfmeas_lib
        self.ethswitchLib = ethswitch_lib

        self.lib.setXmlParams(self.testCaseConfig, self.testSuiteConfig)
        self.currentSut = None
        self.currentTestCase = None
        self.logger = Logger.getLogger(self.__class__) #use this in the test cases
        self.logger.info("Test Description: " + self.id())
        self.logger.info("Test Requirement: " + self.tag)
        self.logger.setLevel(Level.toLevel(logLevel))
        self.OmpLibraryException = OmpLibraryException
        self.testApplicationLoadDeviation =  {'sc': 400, 'pl' : 100} #hur ska denna hanteras, xml-config param?
        self.testApplicationAcceptedLostCalls = 100 # 100 % loss ???
        self.expectedNotifications = []
        self.ignoredNotifications= []
        self.alarmNotifs = 'alarmNotifications'
        self.stateChangeNotifs = 'stateChangeNotifications'
        self.successors = ['SUCCESS', 'OK', '0', 0, True]
        self.failures = ['ERROR', 'NOK', '1', 1, False]
        self.endTime = 0
        self.collectInfo = True
        self.nodeRepTime = ph.getData(self.testSuiteConfig, 'timingParams:nodeRepTime')
        self.clusterRepTime = ph.getData(self.testSuiteConfig, 'timingParams:clusterRepTime')
        self.failureFlag = False
        self.failBeforeCoreDumpCheck = True
        self.failBeforeTrapCheck = True
        self.hostNameList = []

        #specific parameters for characteristic measurements
        self.storeMeas = System.getProperty("storeMeas")
        self.compareMeas = System.getProperty("compareMeas")

#        self.setUpCheckMode = lib.getXmlParams('')

        tempConfig = {}
        for key in self.testSuiteConfig.keys():
            if 'testcase' in key:
                if self.testSuiteConfig[key]['tag']['tag'] == self.testCaseConfig['info']['tag']['tag']:
                    tempConfig = self.testSuiteConfig[key]


        if tempConfig['useDefaultSuiteCheck']['useDefaultSuiteCheck'] == 'False':
            self.setUpHw = ph.getData(tempConfig, 'tcSpecificChecks:setup:hw')
            self.setUpOs = ph.getData(tempConfig, 'tcSpecificChecks:setup:os')
            self.setUpMw = ph.getData(tempConfig, 'tcSpecificChecks:setup:mw')
            self.setUpAppl = ph.getData(tempConfig, 'tcSpecificChecks:setup:appl')
            self.setUpInterfaces = ph.getData(tempConfig, 'tcSpecificChecks:setup:interfaces')
            self.setUpEvents = ph.getData(tempConfig, 'tcSpecificChecks:setup:events')
            self.setUpInfo = ph.getData(tempConfig, 'tcSpecificChecks:setup:info')
            self.setUpCleanup = ph.getData(tempConfig, 'tcSpecificChecks:setup:cleanup')

            self.runTestHw = ph.getData(tempConfig, 'tcSpecificChecks:runtest:hw')
            self.runTestOs = ph.getData(tempConfig, 'tcSpecificChecks:runtest:os')
            self.runTestMw = ph.getData(tempConfig, 'tcSpecificChecks:runtest:mw')
            self.runTestAppl = ph.getData(tempConfig, 'tcSpecificChecks:runtest:appl')
            self.runTestInterfaces = ph.getData(tempConfig, 'tcSpecificChecks:runtest:interfaces')
            self.runTestEvents = ph.getData(tempConfig, 'tcSpecificChecks:runtest:events')
            self.runTestInfo = ph.getData(tempConfig, 'tcSpecificChecks:runtest:info')
            self.runTestCleanup = ph.getData(tempConfig, 'tcSpecificChecks:runtest:cleanup')

            self.tearDownHw = ph.getData(tempConfig, 'tcSpecificChecks:teardown:hw')
            self.tearDownOs = ph.getData(tempConfig, 'tcSpecificChecks:teardown:os')
            self.tearDownMw = ph.getData(tempConfig, 'tcSpecificChecks:teardown:mw')
            self.tearDownAppl = ph.getData(tempConfig, 'tcSpecificChecks:teardown:appl')
            self.tearDownInterfaces = ph.getData(tempConfig, 'tcSpecificChecks:teardown:interfaces')
            self.tearDownEvents = ph.getData(tempConfig, 'tcSpecificChecks:teardown:events')
            self.tearDownInfo = ph.getData(tempConfig, 'tcSpecificChecks:teardown:info')
            self.tearDownCleanup = ph.getData(tempConfig, 'tcSpecificChecks:teardown:cleanup')
        else:
            self.setUpHw = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:hw')
            self.setUpOs = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:os')
            self.setUpMw = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:mw')
            self.setUpAppl = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:appl')
            self.setUpInterfaces = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:interfaces')
            self.setUpEvents = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:events')
            self.setUpInfo = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:info')
            self.setUpCleanup = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:setup:cleanup')

            self.runTestHw = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:hw')
            self.runTestOs = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:os')
            self.runTestMw = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:mw')
            self.runTestAppl = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:appl')
            self.runTestInterfaces = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:interfaces')
            self.runTestEvents = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:events')
            self.runTestInfo = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:info')
            self.runTestCleanup = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:runtest:cleanup')

            self.tearDownHw = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:hw')
            self.tearDownOs = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:os')
            self.tearDownMw = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:mw')
            self.tearDownAppl = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:appl')
            self.tearDownInterfaces = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:interfaces')
            self.tearDownEvents = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:events')
            self.tearDownInfo = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:info')
            self.tearDownCleanup = ph.getData(self.testSuiteConfig, 'defaultSuiteCheck:teardown:cleanup')

        #Create a dictionary template for characteristic measurements, assign tag, name and date
        now = datetime.datetime.now()
        date = '%s-%s-%s' % (now.year,now.month,now.day)
        nrOfNodes = str(int(self.nrOfPlNodes) + int(self.nrOfScNodes))
        self.charMeasRecord = {'tcTag' : self.tag, 'tcName' : self.name, 'value' : '', 'cmwTag' : self.storeMeas, 'lotcVer' : '', 'vipVer' : '', 'hw' : self.targetName, 'nrOfNodes' : nrOfNodes, 'date' : date}

    def setUp(self):

        #logger = Logger.getLogger('TC setUp logging')
        self.myLogger.info('enter TC setUp')
        self.super__setUp()
        self.currentTestCase = self

        self.sutholder = SUTHolder.getInstance()
        self.currentSut = self.sutholder.zones[0]

        self.ignoredNotifications.append(["Previous raised alarm of safSi=", "SA_NTF_SEVERITY_CLEARED", "SA_NTF_SOFTWARE_ERROR"])
        self.ignoredNotifications.append(["ERIC-LINUX_", "SA_NTF_SEVERITY_CLEARED", "SA_NTF_TIMING_PROBLEM"])
        self.ignoredNotifications.append(["ERIC-LINUX_", "SA_NTF_SEVERITY_CLEARED", "SA_NTF_CONFIGURATION_OR_CUSTOMIZATION_ERROR"])
        self.ignoredNotifications.append(["Contact lost with an external GateWay", "SA_NTF_SEVERITY_CLEARED", "SA_NTF_UNSPECIFIED_REASON"])
        self.ignoredNotifications.append(["ERIC-LINUX_", "SA_NTF_SEVERITY_MAJOR", "SA_NTF_TIMING_PROBLEM"])
        self.ignoredNotifications.append(["ERIC-LINUX_", "SA_NTF_SEVERITY_MAJOR", "SA_NTF_CONFIGURATION_OR_CUSTOMIZATION_ERROR"])
        self.ignoredNotifications.append(["SI designated by safSi=AllNodesNWayActive,safApp=AmfMeasureApp has no current active assignments to any SU", "SA_NTF_SEVERITY_MAJOR"])
        self.ignoredNotifications.append(["SI designated by safSi=PLNoRed,safApp=AmfMeasureApp has no current active assignments to any SU", "SA_NTF_SEVERITY_MAJOR"])


        #get library broker handles
        self.TargetDataLib = self.currentSut.getLibrary("TargetDataLib")
        self.targetData = self.TargetDataLib.getTargetData()

        #We should not clear node2prompt
        self.myLogger.info('We will not clear node2prompt in ssh_lib')
        self.sshLib.setClearNode2prompt(False)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.distroTypes = eval(dict.get("LINUX_DISTRO_TYPES"))
        result = self.lib.updateLinuxDistroInDictionary(self.testSuiteConfig, self.distroTypes)
        self.fail(result[0], result[1])
        self.linuxDistro = self.testSuiteConfig['linuxDistro']['value']
        backupRpmScriptLocal = "%s%s%s" %(os.environ['MY_REPOSITORY'], dict.get("PATH_TO_CONFIG_FILES"), dict.get("BACKUP_RPMS_SCRIPT"))
        self.backupRpmScript = "/home/%s" % dict.get("BACKUP_RPMS_SCRIPT")

        # copy backup rpms script to cluster
        result = ssh_lib.remoteCopy(backupRpmScriptLocal, '/home/', timeout = 60)
        self.fail(result[0], result[1])

        cmd = 'chmod +x %s' % self.backupRpmScript
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        cmd = 'cmw-repository-list'
        result = self.sshLib.sendCommand(cmd)
        #result = cmw_utils._getInstalledSwOnRepository()
        temp = result[1].split('\n')
        for line in temp:
            self.myLogger.info(line)


        if 'qemu' == self.targetData['targetType'].split('_')[0]:
            if self.setUpCheck == 'True':
                print "Qemu is the target remove setup checks"
                """
                <setup>
                    <hw>['system','switches','network']</hw>
                    <os>['lotc','vip']</os>
                    <mw>['coreMw']</mw>
                    <appl>['testApp','ntfsub']</appl>
                    <interfaces>['ctrl1','ctrl2','vip']</interfaces>
                    <events>['load','traps','dumps','statistics','address','log','actCtrl']</events>
                    <info>['amf-state node']</info>
                    <cleanup>['imm','swm_lock']</cleanup>
                </setup>
                """
                if 'switches' in self.setUpHw:
                    self.setUpHw.remove('switches')
                if 'system' in self.setUpHw:
                    self.setUpHw.remove('system')
                if 'network' in self.setUpHw:
                    self.setUpHw.remove('network')

                if 'lotc' in self.setUpOs:
                    self.setUpOs.remove('lotc')
                if 'vip' in self.setUpOs:
                    self.setUpOs.remove('vip')

                if 'testApp' in self.setUpAppl:
                    self.setUpAppl.remove('testApp')

                if 'vip' in self.setUpInterfaces:
                    self.setUpInterfaces.remove('vip')

                if 'statistics' in self.setUpEvents:
                    self.setUpEvents.remove('statistics')
                if 'load' in self.setUpEvents:
                    self.setUpEvents.remove('load')
                if 'traps' in self.setUpEvents:
                    self.setUpEvents.remove('traps')

            if self.runTestCheck == 'True':
                """
                <runtest>
                    <hw>['system','switches','network']</hw>
                    <os>['lotc','vip']</os>
                    <mw>['coreMw']</mw>
                    <appl>['testApp','ntfsub']</appl>
                    <interfaces>['ctrl1','ctrl2','vip']</interfaces>
                    <events>['load','traps','dumps','statistics','address','log']</events>
                    <info>['amf-state node']</info>
                    <cleanup>['imm','swm_lock']</cleanup>
                </runtest>
                """
                print "Qemu is the target remove run test checks"
                if 'switches' in self.runTestHw:
                    self.runTestHw.remove('switches')
                if 'system' in self.runTestHw:
                    self.runTestHw.remove('system')
                if 'network' in self.runTestHw:
                    self.runTestHw.remove('network')

                if 'lotc' in self.runTestOs:
                    self.runTestOs.remove('lotc')
                if 'vip' in self.runTestOs:
                    self.runTestOs.remove('vip')

                if 'testApp' in self.runTestAppl:
                    self.runTestAppl.remove('testApp')

                if 'vip' in self.runTestInterfaces:
                    self.runTestInterfaces.remove('vip')

                if 'statistics' in self.runTestEvents:
                    self.runTestEvents.remove('statistics')
                if 'load' in self.runTestEvents:
                    self.runTestEvents.remove('load')
                if 'traps' in self.runTestEvents:
                    self.runTestEvents.remove('traps')

            if self.tearDownCheck == 'True':
                """
                <teardown>
                    <hw>['system','switches','network']</hw>
                    <os>['lotc','vip']</os>
                    <mw>['coreMw']</mw>
                    <appl>['testApp','ntfsub']</appl>
                    <interfaces>['ctrl1','ctrl2','vip']</interfaces>
                    <events>['load','traps','dumps','statistics','address','log']</events>
                    <info>['amf-state node']</info>
                    <cleanup>['imm','swm_lock']</cleanup>
                </teardown>
                """
                print "Qemu is the target remove tear down checks"

                if 'switches' in self.tearDownHw:
                    self.tearDownHw.remove('switches')
                if 'system' in self.tearDownHw:
                    self.tearDownHw.remove('system')
                if 'network' in self.tearDownHw:
                    self.tearDownHw.remove('network')

                if 'lotc' in self.tearDownOs:
                    self.tearDownOs.remove('lotc')
                if 'vip' in self.tearDownOs:
                    self.tearDownOs.remove('vip')

                if 'testApp' in self.tearDownAppl:
                    self.tearDownAppl.remove('testApp')

                if 'vip' in self.tearDownInterfaces:
                    self.tearDownInterfaces.remove('vip')

                if 'statistics' in self.tearDownEvents:
                    self.tearDownEvents.remove('statistics')
                if 'load' in self.tearDownEvents:
                    self.tearDownEvents.remove('load')
                if 'traps' in self.tearDownEvents:
                    self.tearDownEvents.remove('traps')

        if self.setUpCheck == 'True':
            #System checks
                #if a repair is performed we need to ensure correct active controller
            repairHwFlag = False

            if 'vbox' == self.targetData['targetType'].split('_')[0] or 'qemu' == self.targetData['targetType'].split('_')[0]:
                print "Vbox/KVM is the target. Remove some checks"
                if self.setUpCheck == 'True':
                    if 'switches' in self.setUpHw:
                        self.setUpHw.remove('switches')
                    if 'system' in self.setUpHw:
                        self.setUpHw.remove('system')
                    if 'network' in self.setUpHw:
                        self.setUpHw.remove('network')

            self.setTestStep('HW check: setUp check')

            #checks switches and repair if necessary
            self.myLogger.info('check switches in TC setUp')

            if 'switches' in self.setUpHw:
                result = self.safCheckSwitches()
                if result[0] == 'ERROR':
                    self.myLogger.warn('check switches failed, try to repair')
                    for switch in result[1]:
                        result = self.safRepairSwitch(switch)
                        if result[0] in self.failures:
                            self.fail(result,'repair switch %s failed' % switch)

            #check hw and repair if necessary
            if 'system' in self.setUpHw:
                result, nodes = self.safCheckSystemNodes()
                if result in self.failures:
                    self.myLogger.warn('check nodes failed, try to repair')
                    for subrack,slot in nodes:
                        self.myLogger.warn('repair node_%s_%s' % (subrack,slot))
                        result = self.safRepairHW(subrack, slot)
                        if result[0] in self.failures:
                            self.fail('ERROR',result[1])
                    self.miscLib.waitTime(self.nodeRepTime)
                    result, nodes = self.safCheckSystemNodes()
                    if result in self.failures:
                        self.fail(result, nodes)
                    repairHwFlag = True

            #hmm, LOTC specific?
            self.myLogger.info('check for FS problem in the sys.log')
            hostname1 = self.safLib.getHostName(2, 1)
            if int(self.nrOfScNodes) > 1:
                hostname2 = self.safLib.getHostName(2, 2)
            if hostname1[0] == 'SUCCESS' and (int(self.nrOfScNodes) == 1 or hostname2[0] == 'SUCCESS'):
                cmd = 'cat /var/log/%s/messages* | grep "warning: mounting fs with errors"' %  hostname1[1]
                result1 =  self.sshLib.sendCommand(cmd)
                fsErrors = result1[1]
                if int(self.nrOfScNodes) > 1:
                    cmd = 'cat /var/log/%s/messages* | grep "warning: mounting fs with errors"' %  hostname2[1]
                    result2 =  self.sshLib.sendCommand(cmd)
                    fsErrors += result2[1]
                if fsErrors != '':
                    self.myLogger.warn('Problem with the file system:')
                    fsErrorsList = fsErrors.split('\n')
                    for fsErr in fsErrorsList:
                        self.myLogger.warn('%s' % fsErr)
            else:
                self.myLogger.info('No FS problems found in the sys.log')


            #When the HW is OK we try to get active controller
            if 'coreMw' in self.setUpMw:
                self.setTestStep('Get active SC: setUp check')
                self.myLogger.info("Querying for active controller")
                self.myLogger.debug('check active controller')
                result, (subrack, slot) = lib.updateActiveController(self.testConfig)
                if result in self.failures:
                    self.myLogger.warn('failed to get active controller, try to repair the cluster')
                    result = self.safRepairCluster((subrack, slot))
                    if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])
                    self.miscLib.waitTime(self.clusterRepTime)
                    result, (subrack, slot) = lib.updateActiveController(self.testConfig)
                    if result in self.failures and self.testSuiteConfig.has_key('restoreBackup'):
                        self.myLogger.warn('cluster reboot did not fix the cluster, try to backup restore')
                        result = self.comsa_lib.restoreSystem(self, self.testSuiteConfig['restoreBackup'], self.testConfig, self.testSuiteConfig, self.distroTypes)
                        self.fail(result[0], result[1])
                        result, (subrack, slot) = lib.updateActiveController(self.testConfig)
                        if result in self.failures:
                            self.fail('ERROR' , 'Failed to get active controller.')
                    elif result in self.failures and self.testSuiteConfig.has_key('restoreBackup') == False:
                        self.fail('ERROR' , 'Failed to get active controller.')
                else:
                    self.myLogger.info("Active controller: SC_%d_%d" % (subrack, slot))


            self.setTestStep('Check sw: setUp check')
            if 'coreMw' in self.setUpMw:
                self.myLogger.debug('check Core MW in TC setUp')
                result = self.safCheckSw('mw')
                if result[0] in self.failures:
                    self.myLogger.warn('check Core MW failed, try to repair the cluster')
                    result = self.safRepairCluster(result[2])
                    if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])
                    self.miscLib.waitTime(self.clusterRepTime)
                    result = self.safCheckSw('mw')
                    if result[0] in self.failures and self.testSuiteConfig.has_key('restoreBackup'):
                        self.myLogger.warn('cluster reboot did not fix the cluster, try to backup restore')
                        result = self.comsa_lib.restoreSystem(self, self.testSuiteConfig['restoreBackup'], self.testConfig, self.testSuiteConfig, self.distroTypes)
                        self.fail(result[0], result[1])
                        result = self.safCheckSw('mw')
                        if result[0] in self.failures:
                            self.fail('ERROR',result[1])
                    elif result[0] in self.failures and self.testSuiteConfig.has_key('restoreBackup') == False:
                        self.fail('ERROR',result[1])
                    repairHwFlag = True




            if repairHwFlag:
                #When the HW has been repaired and OK we retry to get active controller
                self.myLogger.warn("Updating active controller after repair has been performed")
                result, (subrack, slot) = lib.updateActiveController(self.testConfig)
                if result in self.failures:
                    self.myLogger.error('failed to get active controller')
                else:
                    self.myLogger.warn("Active controller after repair has been performed: SC_%d_%d" % (subrack, slot))

            #checks SUTs interfaces#
            self.setTestStep('Check interfaces: setUp check')
            if self.setUpInterfaces !=['']:
                for interface in self.setUpInterfaces:
                    response = ''
                    if interface == 'vip':
                        result = self.miscLib.execCommand(" ping -c 10 %s" % (self.targetData['ipAddress']['vip']['vip_3']))
                        if result[0] in self.failures:
                            self.fail('ERROR',result[1])
                    else:
                        result = self.miscLib.execCommand(" ping -c 10 %s" % (self.targetData['ipAddress']['ctrl'][interface]))
                        if result[0] in self.failures:
                            self.fail('ERROR',result[1])

                    if not re.search('100% packet loss',result[1]):
                        self.myLogger.info('%s Connection established' % interface)
                    else:
                        self.fail('ERROR','Unable to ping %s interface' % interface)

            #prepare for testing
            self.setTestStep('prepare for testing: setUp check')
            if self.setUpEvents != ['']:
                self.myLogger.info('Setup: Preparing for testing')
                if 'log' in self.setUpEvents:
                    self.myLogger.info('set testcase entry in sys.log')
                    result = self.safSetSysLogEntry(self.testConfig,'setup',self.currentTestCase)
                    if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])
                    else:
                        self.hostNameList =  result[2]

                if 'address' in self.setUpEvents:
                    self.myLogger.info('set target address NOT EXECUTED, for COM?')
                    #result  = self.safSetTargetAddress(default=False)
                    #if result[0] == 'ERROR':
                    #    self.fail('ERROR',result[1])

                if 'dumps' in self.setUpEvents:
                    self.myLogger.info('reset dumps')
                    result = self.safResetDumps()
                    if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])

                if 'statistics' in self.setUpEvents:
                    result = self.safResetTestAppStatistics()
                    if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])

                if 'load' in self.setUpEvents:
                    if self.nrOfPlNodes == 0:
                        self.testAppLib.removeAllInstances()
                        instances = ['SC','ALL','ONESC']
                        self.testAppLib.createInstances(instances)
                    result = self.safSetProcessorLoadTestApplication()
                    if result[0] == 'ERROR':
                        ########### TEMP FIX FOR EVIP PROBLEM #############
                        # sometime after SC reboot the sockets testApp using are lost. The only way to
                        # fix it is to reboot the system
                        #self.safLib.clusterReboot()
                        #self.miscLib.waitTime(300)
                        ########### TEMP FIX FOR EVIP PROBLEM END #############
                        self.fail('ERROR',result[1])

            #invoke cleanups
            self.setTestStep('cleanup: setUp check')
            #enable this when Janos has delivered

            if self.setUpCleanup != ['']:
                if 'alarm' in  self.setUpCleanup:
                    result = self.safCleanActiveAlarms()
                    if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])
                    # some special treatment for the amfMeasureApp, we have to ignore all alarms from the amfMeasureApp
                    #after cluster reboot
                    cmd = 'cmw-status -v si | grep AmfMeasureAppNway | wc -l'
                    result = self.sshLib.sendCommand(cmd)
                    nrOfAmfMeasureSIs = 0
                    if result[0] == 'SUCCESS' and result[1] != '':
                        nrOfAmfMeasureSIs = int(result[1])
                        for i in range(nrOfAmfMeasureSIs):
                            str="SI designated by safSi=Nway-%s,safApp=AmfMeasureAppNway has no current active assignments to any SU" % (i)
                            self.ignoredNotifications.append([str, "SA_NTF_SEVERITY_MAJOR"])


            #Finally reset the "trap reader"
            if 'traps' in self.setUpEvents:
                result = self.safResetTraps()
                if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])

                #Reset the smfMonitor app log files
                self.sshLib.sendCommand('/opt/SMFMONITOR/bin/rotate_log.sh',2,1)
                if int(self.nrOfScNodes) > 1:
                    self.sshLib.sendCommand('/opt/SMFMONITOR/bin/rotate_log.sh',2,2)

            #update the characteristic measurement record with LOTC and VIP versions
            result = self.sshLib.sendCommand('cat /etc/cluster/product/version')
            if result[0] == 'SUCCESS' and  result[1] != '':
                tempString = result[1].encode('iso-8859-1')
                self.charMeasRecord['lotcVer'] = tempString
            else:
                self.charMeasRecord['lotcVer'] = 'UNKNOWN'
            result = self.sshLib.sendCommand('rpm -qa | grep -i vip')
            if result[0] == 'SUCCESS' and  result[1] != '':
                tempString = result[1].encode('iso-8859-1')
                self.charMeasRecord['vipVer'] = tempString
            else:
                self.charMeasRecord['vipVer'] = 'UNKNOWN'

        # register atexit function (check coredumps)
        atexit.register(self.goodbye)

        self.myLogger.info('leave setUp check')



    def runTest(self, ignoreFailList = ['']):

        self.myLogger.info('enter TC runTest check')

        if self.runTestCheck == 'True':

            if 'vbox' == self.targetData['targetType'].split('_')[0] or 'qemu' == self.targetData['targetType'].split('_')[0]:
                print "Vbox/KVM is the target. Remove some checks"
                if self.runTestCheck == 'True':
                    if 'switches' in self.runTestHw:
                        self.runTestHw.remove('switches')
                    if 'system' in self.runTestHw:
                        self.runTestHw.remove('system')
                    if 'network' in self.runTestHw:
                        self.runTestHw.remove('network')

            #checks HW
            if self.runTestHw != ['']:
                self.setTestStep('HW check: runTest check')
                self.myLogger.info('Runtest: Checking system HW')
                if 'switches' in self.runTestHw:
                    self.myLogger.info('Checking system switches')
                    result = self.safCheckSwitches()
                    if result[0] in self.failures:
                        if 'switches' in ignoreFailList:
                            self.myLogger.warn('System switch failure: %s, but the test continues'  % result[1])
                            self.setAdditionalResultInfo('System switch failure: %s, but the test continues'  % result[1])
                        else:
                            self.fail('ERROR' , 'System switch failure: %s' % result[1])


                if 'system' in self.runTestHw:
                    self.myLogger.info('Checking system nodes')
                    result = self.safCheckSystemNodes()
                    if result[0] in self.failures:
                        if 'system' in ignoreFailList:
                            self.myLogger.warn('System nodes failure: %s, but the test continues'  % result[1])
                            self.setAdditionalResultInfo('System nodes failure: %s, but the test continues'  % result[1])
                        else:
                            self.fail('ERROR' , 'System nodes failure: %s' % result[1])

                    self.myLogger.info('check for FS problem in the sys.log')
                    hostname1 = self.safLib.getHostName(2, 1)
                    if int(self.nrOfScNodes) > 1:
                        hostname2 = self.safLib.getHostName(2, 2)
                    if hostname1[0] == 'SUCCESS' and (int(self.nrOfScNodes) == 1 or hostname2[0] == 'SUCCESS'):
                        cmd = 'cat /var/log/%s/messages* | grep "warning: mounting fs with errors"' %  hostname1[1]
                        result1 =  self.sshLib.sendCommand(cmd)
                        fsErrors = result1[1]
                        if int(self.nrOfScNodes) > 1:
                            cmd = 'cat /var/log/%s/messages* | grep "warning: mounting fs with errors"' %  hostname2[1]
                            result2 =  self.sshLib.sendCommand(cmd)
                            fsErrors += result2[1]
                        if fsErrors != '':
                            self.myLogger.warn('Problem with the file system:')
                            fsErrorsList = fsErrors.split('\n')
                            for fsErr in fsErrorsList:
                                self.myLogger.warn('%s' % fsErr)
                    else:
                        self.myLogger.info('No FS problems found in the sys.log')


            #check MW components
            if 'coreMw' in self.runTestMw:
                self.myLogger.debug('check Core MW in TC runTest')
                result = self.safCheckSw('mw')
                if result[0] in self.failures:
                    if 'coreMw' in ignoreFailList:
                        self.myLogger.warn('coreMw failure: %s, but the test continues'  % result[1])
                        self.setAdditionalResultInfo('coreMw failure: %s, but the test continues'  % result[1])
                    else:
                        self.fail('ERROR',result[1])


            #checks SUTs interfaces
            self.setTestStep('Check interfaces: runTest check')
            if self.runTestInterfaces !=['']:
                for interface in self.runTestInterfaces:
                    result = ''
                    if interface == 'vip':
                        result = self.miscLib.execCommand(" ping -c 10 %s" % (self.targetData['ipAddress']['vip']['vip_3']))
                        if result[0] in self.failures:
                            if 'vip' in ignoreFailList:
                                self.myLogger.warn('Failure : %s, but the test continues'  % result[1])
                                self.setAdditionalResultInfo('Failure : %s, but the test continues'  % result[1])
                            else:
                                self.fail('ERROR',result[1])
                    else:
                        result = self.miscLib.execCommand(" ping -c 10 %s" % (self.targetData['ipAddress']['ctrl'][interface]))
                        if result[0] in self.failures:
                            if 'ctrl1' in ignoreFailList or 'ctrl2' in ignoreFailList:
                                self.myLogger.warn('Failure : %s, but the test continues'  % result[1])
                                self.setAdditionalResultInfo('Failure : %s, but the test continues'  % result[1])
                            else:
                                self.fail('ERROR',result[1])
                    if not re.search('100% packet loss',result[1]):
                        self.myLogger.info('%s Connection established' % interface)
                    else:
                        if 'ctrl1' in ignoreFailList or 'ctrl2' in ignoreFailList or 'vip' in ignoreFailList:
                            self.myLogger.warn('Unable to ping interface : %s, but the test continues'  % interface)
                            self.setAdditionalResultInfo('Unable to ping interface : %s, but the test continues'  % interface)
                        else:
                            self.fail('ERROR','Unable to ping interface: %s' % interface)

            #validate system after testing (setup/runtest)
            self.setTestStep('Check events: runTest check')
            if self.runTestEvents !=['']:
                if 'statistics' in self.runTestEvents:
                    self.myLogger.info('check testApp statistics (lost calls)')
                    result = self.safCheckTestAppStatistics()
                    if result[0] in self.failures:
                        if 'statistics' in ignoreFailList:
                            self.myLogger.warn('check testApp statistics failed, but the test continues')
                            self.setAdditionalResultInfo('check testApp statistics failed, but the test continues')
                        else:
                            self.fail('ERROR' , 'Test Application statistics fails, see log for details')

                if 'load' in self.runTestEvents:
                    self.myLogger.info('check testApp load')
                    result = self.safCheckTestAppLoad()
                    if result[0] in self.failures:
                        if 'load' in ignoreFailList:
                            self.myLogger.warn('check testApp load failed, but the test continues')
                            self.setAdditionalResultInfo('check testApp load failed, but the test continues')
                        else:
                            self.fail('ERROR' , 'Test Application check load fails. %s' %result[1])

                if 'dumps' in self.runTestEvents:
                    self.myLogger.info('check system dumps')
                    result = self.safCheckDumps()
                    if result[0] != 'SUCCESS':
                        self.failBeforeCoreDumpCheck = False
                        self.myLogger.error('System dumps generated')
                        for dump in result[1]:
                            self.setAdditionalResultInfo('system dumps: %s generated' % dump)
                        for btInfo in result[2]:
                            btInfoArray = btInfo.split('\n')
                            for line in btInfoArray:
                                self.myLogger.error(line)
                        if 'dumps' in ignoreFailList:
                            self.myLogger.warn('System dumps generated, but the test continues')
                            self.safResetDumps()
                        else:
                            self.fail('ERROR','System dumps generated, see log for details')

                if 'traps' in self.runTestEvents:
                    self.failBeforeTrapCheck = False
                    self.myLogger.info('check traps')
                    result = self.safCheckTraps()
                    if result[0] in self.failures:
                        if 'traps' in ignoreFailList:
                            self.setAdditionalResultInfo('alarms generated, but the test continues, see log for more info')
                            self.safResetTraps()
                        else:
                            self.fail('ERROR' , 'check traps failed, see log for details')



        self.myLogger.info('leave TC runTest check')

    def tearDown(self):

        self.myLogger.info('enter TC tearDown check')

        if self.tearDownCheck == 'True':

            #run test end time
            self.endTime=time.localtime() # End time of RunTest
            self.setTestStep('stop traffic: tearDown check')
            if self.tearDownEvents !=['']:
                if 'load' in self.tearDownEvents:
                    result = self.safStopTestAppLoad()
                    if result[0] in self.failures:
                        self.fail('ERROR' , 'stop testApp load failed, see log for details')

                if 'log' in self.tearDownEvents:
                    self.myLogger.info('set test case exit in sys.log')
                    result = self.safSetSysLogEntry(self.testConfig,'tearDown',self.currentTestCase)
                    if result[0] == 'ERROR':
                        self.fail('ERROR',result[1])

            if self.failBeforeCoreDumpCheck:
                if 'dumps' in self.tearDownEvents:
                    self.myLogger.info('check system dumps')
                    result = self.safCheckDumps()
                    if result[0] != 'SUCCESS':
                        self.failBeforeCoreDumpCheck = False
                        self.myLogger.error('System dumps generated')
                        for dump in result[1]:
                            self.setAdditionalResultInfo('system dumps: %s generated' % dump)
                        for btInfo in result[2]:
                            btInfoArray = btInfo.split('\n')
                            for line in btInfoArray:
                                self.myLogger.error(line)
                        self.fail('ERROR','System dumps generated, see log for details')


            if self.failureFlag == True:
                collectInfoFileName = '%s_%s.tar' % (self.tag,self.instance)
                self.myLogger.warn('tc failed, try to collect info from the system')
                res, response = self.lib.collectInfo(collectInfoFileName, self.testConfig)
                if res != 'SUCCESS':
                    self.myLogger.warn('Failed to execute collect_info')
                self.failureFlag = False

            self.super__tearDown()
            self.myLogger.info('remove all ssh handles')
            self.tearDownHandles()


        self.myLogger.info('leave TC tearDown check')


    def safCheckSystemNodes(self):
        """This function tests hardware used in System under test. It includes checks for nodes used.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        self.myLogger.info("Checking cluster nodes ")
        return lib.checkSystemNodes(self.testConfig)


    def safCheckSwitches(self):
        """This function tests hardware used in System under test. It includes checks for switches used.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        self.myLogger.info("Checking system switches")
        return lib.checkSwitches(self.testConfig)


    def safCheckDumps(self):
        """This function will check that no new dumps are created since the last reset (see stResetDumps() function)
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        list of new dumps in index 1"""
        self.myLogger.info("Checking dumps")
        return lib.checkDumps(self.tag)


    def safCheckTraps(self):
        """This function will check the traps (alarms/notifications) generated by SUT during test execution.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        list of new traps in index 1"""
        self.myLogger.info("Checking alarms and notifications")
        result= self.notificationLib.checkNotifications (self.expectedNotifications, self.ignoredNotifications, self.alarmNotifs, self.nrOfScNodes)
        if result[0] in self.failures:
            searchString = 'has no current active assignments to any SU'
            doubleCheck='OK'
            for errorMsg in result[1]:
                if re.search(searchString, errorMsg):
                    additionalTextString=errorMsg.split('\n')[13]
                    applicationName=additionalTextString.split(' ')[5] # extract the application name that caused the notification
                    timeOfAlarm=int(errorMsg.split('\n')[11].split(' ')[2])/1000000000 # extract the linux time of the notification in seconds
                    self.myLogger.info('Alarm: "%s" received at Linux second: %d' %(additionalTextString,timeOfAlarm))
                    expectedClearedAlarm="Previous raised alarm of %s is now cleared"%applicationName
                    self.myLogger.info('expectedClearedAlarm: %s' %expectedClearedAlarm)

                    allNotifications = self.notificationLib.readNotification(expectedClearedAlarm, self.alarmNotifs, self.nrOfScNodes)[1]
                    for notification in allNotifications:
                        if re.search(expectedClearedAlarm, notification):
                            clearedAlarmString = notification.split('\n')[13]
                            timeOfClearedAlarm=int(notification.split('\n')[11].split(' ')[2])/1000000000 # extract the linux time of the notification in seconds
                            self.myLogger.info('Cleared alarm: "%s" received at Linux second: %d' %(clearedAlarmString,timeOfClearedAlarm))

                            if timeOfClearedAlarm <= (timeOfAlarm + 5):
                                self.myLogger.info('ignoring the alarm: "%s" at %d since the Cleared alarm: "%s" is received at %d'%(additionalTextString,timeOfAlarm,clearedAlarmString,timeOfClearedAlarm))
                            else:
                                self.myLogger.error('The Cleared alarm: %s was not raised with in 5 seconds after the alarm: %s'%(clearedAlarmString,additionalTextString))
                                doubleCheck='notOK'
                else:
                    doubleCheck='notOK'
            if doubleCheck=='OK':
                #return ('SUCCESS' , 'no unexpected alarms found')
                result =  ('SUCCESS' , 'no unexpected alarms found')
        #else:
        return result



    def safCheckTestAppLoad(self):
        """This function will validate current test application load for all
        blades
        """
        self.myLogger.info("Check Test Application load")
        return lib.checkTestAppLoad(self.testConfig, self.testApplicationLoadDeviation)

    def safCheckTestAppStatistics(self):
        """This function will store the current statistics for all test application
        instances"""
        self.myLogger.info("Check Test Application statisics")
        return lib.checkTestAppStatistic(self.testConfig, self.testApplicationAcceptedLostCalls)

    def safCheckSw(self, swType):
        """This function tests that SAF MW are up and running. The test is done by sending snmp messages
        quering states of the SU's that are instantiated in the cluster.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        self.myLogger.info('Check %s status' % swType)
        return lib.checkSwCompStates(self.testConfig, swType)

    def safSetProcessorLoadTestApplication(self):
        """This function repairs hardware used in System under test.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and result string
        in index 1 used for fault analysing, the string will implicity be written to the log"""
        self.myLogger.info("Set the load on test application instances")
        result, reply = lib.setProcessorLoad(self.testConfig, self.loadSc, self.loadPl, self.loadProfile)
        self.miscLib.waitTime(5)
        return result, reply

    def safStopTestAppLoad (self):
        self.myLogger.info('Stop the load on test application instances')
        return self.testAppLib.stopTraffic()

    def safResetTestAppStatistics(self):
        """This function will store the reset the current statistics for all test application
        instances"""
        self.myLogger.info("Reset statisics")
        return lib.resetTestAppStatistics(self.testConfig)

    def safResetDumps(self):
        """This function will store the latest dump created are created sincce the last reset (see stResetDumps() function)
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        fault message in index 1"""
        self.myLogger.info("Reset system dump directory")
        return lib.resetDumps()


    def safResetTraps(self):
        """This function will store the latest dump created are created sincce the last reset (see stResetDumps() function)
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        fault message in index 1"""
        self.myLogger.info("Reset alarms and notifications")
        return self.notificationLib.clearNotifications(self.nrOfScNodes)

    def safRepairHW(self, subrack, slot ):
            """This function repairs hardware used in System under test.
            The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
            diagnose in index 1 used for fault analysing"""
            idx = self.testConfig['testNodes'].index((subrack,slot))
            blade = '%s_%s_%s' % (self.testConfig['testNodesTypes'][idx], subrack, slot)
            self.myLogger.info('Repairing system node: %s' % blade)
            self.sshLib.tearDownHandles()
            return self.hwLib.powerReset(subrack, slot)


    def safRepairSwitch(self, switch):
        """This function repairs hardware used in System under test.
        The return of the function is the corresponding action result (SUCCESS or ERROR)"""
        self.myLogger.info("Repairing switch: %s" % switch)
        return lib.repairSwitch(switch)

    def safRepairCluster(self, faultyNodes):
        """This function repairs cluster on System under test by invoking cluster restart command.
        The return of the function will be a tuple with the result (SUCCESS or ERROR)"""
        self.myLogger.info("Repairing cluster ")
        if 'vbox' == self.targetData['targetType'].split('_')[0] or 'qemu' == self.targetData['targetType'].split('_')[0]:
            result =  self.safLib.clusterReboot()
        else:
            result = self.hwLib.clusterPowerReset()

        return result

    def safRestoreBackup(self, backupName):
        """This function initiates the repair of the cluster on System under test by invoking
        backup restore of a known stable backup.
        The return of the function will be a tuple with the result (SUCCESS || ERROR, result string)"""

        result = self.safLib.isBackup(backupName)
        if result == ('SUCCESS','NOT EXIST'):
            return ('ERROR', '%s backup not found. Nothing to restore' %backupName)
        elif result[0] != 'SUCCESS':
            return result

        result = self.comsa_lib.backupRestoreWrapper(backupName, backupRpms = self.backupRpmScript)
        return result


    def safSetSysLogEntry(self, testConfig, entry, myID):
        """This function repairs hardware used in System under test.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and result string
        in index 1 used for fault analysing, the string will implicity be written to the log"""
        self.myLogger.info("Log system information")
        #return ('SUCCESS','vad bra')
        return lib.setSyslogEntry(testConfig, entry, self.tag+' - '+self.id())

    def tearDownHandles(self):
        """This function removes all ssh handles to the system
        There is no return value from this function"""
        try:
            self.sshLib.tearDownHandles()
        except self.OmpLibraryException, e:
            self.myLogger.warn(e.getMessage())

    #def safCleanSwmLock(self):
    #    """This function will remove the swm lock file if that is still left in the cluster."""
    #    self.myLogger.info("Removing swm_lock file if it exists")
    #    return self.safLib.removeSwmLockFile()

###############################################################################
# Asserts handling
###############################################################################

    def fail(self, result,  msg = ''):
        """This function overrides the pyUnit function fail and works as the
        system test default fail function used if not overrided by the test case itself
        """
        self.tearDownHandles()

        msg = str(msg)


        if result not in self.successors:
            if msg != '':
                self.myLogger.error('fail assert message: %s' % msg)
                self.setAdditionalResultInfo(msg)
            else:
                self.myLogger.error('fail assert with no message')

            if self.failBeforeCoreDumpCheck:
                self.failBeforeCoreDumpCheck = False
                if 'dumps' in self.runTestEvents:
                    self.myLogger.info('check system dumps')
                    result = self.safCheckDumps()
                    if result[0] != 'SUCCESS':
                        for dump in result[1]:
                            self.setAdditionalResultInfo('system dumps: %s generated' % dump)
                        for btInfo in result[2]:
                            btInfoArray = btInfo.split('\n')
                            for line in btInfoArray:
                                self.myLogger.error(line)
                        self.fail('ERROR','System dumps generated, see log for details')

            if self.failBeforeTrapCheck:
                if 'traps' in self.runTestEvents:
                    self.myLogger.info('check traps')
                    result = self.safCheckTraps()
                    if result[0] != 'SUCCESS':
                        self.myLogger.error('check traps failed, see log for details')


            #if self.collectInfo:
            #    collectInfoFileName = '%s_%s.tar' % (self.tag,self.instance)
            #    self.myLogger.warn('tc failed, try to collect info from the system')
            #    res, response = self.lib.collectInfo(collectInfoFileName, self.testConfig)
            #    if res != 'SUCCESS':
            #        self.myLogger.warn('Failed to execute collect_info')

            self.failureFlag = True
            #self.collectInfo = False
            NonUnitTestCase.fail(msg)


    def failOnly(self, msg = ''):
        """This function overrides the pyUnit function fail and works as the
        system test default fail function used if not overrided by the test case itself
        Use this instead of fail in manually test cases
        """

        msg = str(msg)


        NonUnitTestCase.fail(msg)

    def goodbye(self):
        result = self.safCheckDumps()
        print '\n'





