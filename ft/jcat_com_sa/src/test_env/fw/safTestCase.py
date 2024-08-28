#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
#pylint: disable-msg=E1101 
###############################################################################
#
# Â© Ericsson AB 2008 All rights reserved.
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
   %CCaseFile:  safTestCase.py %
   %CCaseRev:   /main/1 %
   %CCaseDate:  2009-01-10 %
 

    
'''
###############################################################################
# Common libraries
###############################################################################
import string
import os
import sys
import time
import re
import random

###############################################################################
# PyUnit / Junit imports
###############################################################################
if sys.platform[:4] == 'java':
    from jcat.NonUnitJythonTestSuite import NonUnitJythonTestSuite as TestSuite
else:
    from unittest import TestSuite

###############################################################################
# System test libraries 
###############################################################################
import common.target.common_lib.lib as lib
import common.target.common_lib.misc_lib as misc_lib
import common.target.common_lib.ssh_lib as ssh_lib
import common.target.common_lib.notification_lib as notification_lib
import common.target.common_lib.opensaf_lib as opensaf_lib
import common.target.common_lib.st_env_lib as st_env_lib
import common.target.common_lib.bundle_lib as bundle_lib
import common.target.common_lib.logger_lib as logger_lib
import common.target.common_lib.ethswitch_lib as ethswitch_lib
import common.target.common_lib.logger_lib as logger_lib
import common.target.common_lib.testapp_lib as testapp_lib
import common.target.common_lib.oam_lib as oam_lib
import common.target.common_lib.saf_lib as saf_lib
import common.target.common_lib.hw_lib as hw_lib

###############################################################################
# inherited class imports 
###############################################################################
from nonUnitTestCase import NonUnitPythonTestCase  

###############################################################################
# This is the parent class inherited by the StTestCase class used for 
# system validations and checks
###############################################################################
class SafTestCase(coreTestCase.CoreTestCase):
    """This class is a collection of methods to be used in testcases
    to validate the system used under test"""  

    def __init__(self, testConfig):
        coreTestCase.CoreTestCase.__init__(self, tag, name)
        #General
        self.testConfig = testConfig
        self.startTime = 0
        self.endTime = 0
        self.failures = ['ERROR', 'NOK', '1', 1, False]
        self.successors = ['SUCCESS', 'OK', '0', 0, True]
        #test suit events
        self.testsuite_setup = {}
        self.testsuite_runtest = {}
        self.testsuite_teardown = {}
        self.testsuite_setup_teardown = {}
        self.testsuite_setup_runtest = {}
        #test case events
        self.testcase_setup = []
        self.testcase_runtest = []
        self.testcase_teardown = []
        self.testcase_setup_teardown = []
        self.testcase_setup_runtest = []
        #System
        self.collectInfo = False
        self.mostResentDump =''
        self.originalState = {} 
        self.clusterStatus = ''
        #Notifications
        self.expectedNotifications = []
        self.ignoredNotifications= []
        # The notification below is commented because we do not want to fail test cases because of LOTC problems
        self.ignoredNotifications.append(["ERICSSON-ALARM-MIB::eriAlarmActiveMajorType.0 = Gauge32: 193", "LOTC"])
        # The notification below is commented because we do not want to fail test cases because of trojan alarms
        self.ignoredNotifications.append(["safSu=SuT_trojan"]) # This was introduced by ejnolsz on Sep 2, 2009, before CP1 in the SAF 3.0 DFU 
        #TestApplication
        self.testApplicationAcceptedLostCalls = 100
        self.testApplicationLoadDeviation =  {'sc': 400, 'pl' : 100}


    #System checks
    #klar 
    def safCheckSystemNodes(self):
        """This function tests hardware used in System under test. It includes checks for nodes used.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Checking cluster nodes ", logLevel='debug')
        return lib.checkSystemNodes(self.testConfig)

    #System switches checks's
    #klar 
    def safCheckSwitches(self):
        """This function tests hardware used in System under test. It includes checks for switches used.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Checking system switches", logLevel='debug')
        return lib.checkSwitches(self.testConfig)
    
    #klar 
    def safCheckNetwork(self):
        """This function tests that network are up and running. The test is done by from test pc ping all internal addresses to ensure
        that the internal network is up.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Checking system network",  logLevel='debug')
        return lib.checkNetwork(self.testConfig)

     
    #måste anpassas till nya opensaf
    def safCheckSystemNodesState(self, clusterStatus):
        """This function tests that all nodes in the cluster are inservice. TThe test is done by sending snmp messages
        quering states of the SU's that are instantiated in the cluster.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Checking SAF NODES HA status", logLevel='debug')
        return lib.safCheckSystemNodesState(self.testConfig, clusterStatus)
     
    #måste anpassas till nya opensaf
    def safCheckMW(self, clusterStatus):
        """This function tests that SAF MW are up and running. The test is done by sending snmp messages
        quering states of the SU's that are instantiated in the cluster.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Checking SAF MW HA status", logLevel='debug')
        return lib.safCheckSafMw(self.testConfig, clusterStatus)
    
   #måste anpassas till nya opensaf
    def safCheckTAPP(self, clusterStatus):
        """This function tests that Test Application are up and running. The test is done by sending snmp messages
        quering states of the SU's that are instantiated in the cluster.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Checking Test application", logLevel='debug')
        return lib.safCheckTestApp(self.testConfig, clusterStatus)

    # behövs ej
    #def safCheckTROJAN(self, clusterStatus):
    #    """This function tests that Trojant Application are up and running. The test is done by sending snmp messages
    #    quering states of the SU's that are instantiated in the cluster.
    #    The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
    #    diagnose in index 1 used for fault analysing"""
    #    logger_lib.logMessage("Checking Trojan application", logLevel='debug')
    #    return lib.safCheckTrojanApp(self.testConfig, clusterStatus)

    #klar
    def safCheckDumps(self):
        """This function will check that no new dumps are created since the last reset (see stResetDumps() function)
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        list of new dumps in index 1"""
        logger_lib.logMessage("Checking dumps", logLevel='debug')
        return lib.checkDumps()
    
    #måste anpassas till nya opensaf (ntf)
    def safCheckTraps(self):
        """This function will check the traps (alarms/notifications) generated by SUT during test execution.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        list of new traps in index 1"""
        logger_lib.logMessage("Checking alarms and notifications", logLevel='debug')      
        return oam_lib.checkNotifications (self.expectedNotifications, self.ignoredNotifications)

    def safCheckInterface(self, interfaces):
        """This function will verify that all interfaces are up and running. The test is done by from test pc ping all internal aliases to ensure
        that the internal network is up.
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        fault message in index 1"""
        logger_lib.logMessage("Check interfaces", logLevel='debug')
        return lib.checkSystemInterface(interfaces)
 
    def safCheckTestAppLoad(self):
        """This function will validate current test application load for all
        blades
        """
        logger_lib.logMessage("Check Test Application load", logLevel='debug')
        return lib.checkTestAppLoad(self.testConfig, self.testApplicationLoadDeviation)

    def safCheckTestAppStatistics(self):
        """This function will store the current statistics for all test application
        instances"""
        logger_lib.logMessage("Check Test Application statisics", logLevel='debug')
        return lib.checkTestAppStatistic(self.testConfig, self.testApplicationAcceptedLostCalls)

    def safCheckSystemState(self):
        """This function will check all pid's of processes defined and do a diff from previosly performed check
        The function returns the deviation from last check"""
        logger_lib.logMessage("Check system process state", logLevel='debug')
        result, currentState = bundle_lib.readSystemState(self.testConfig)
        return bundle_lib.compareSystemState(self.originalState, currentState)

    #System repairs
    def safRepairHW(self, subrack, slot ):
        """This function repairs hardware used in System under test. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        idx = self.testConfig['testNodes'].index((subrack,slot))
        blade = '%s_%s_%s' % (self.testConfig['testNodesTypes'][idx], subrack, slot)
        logger_lib.logMessage("Repairing system node: %s" % (blade), logLevel='warning')
        ssh_lib.tearDownHandles()
        return hw_lib.powerReset(subrack, slot)

    def safRepairSwitch(self, switch):
        """This function repairs hardware used in System under test. 
        The return of the function is the corresponding action result (SUCCESS or ERROR)"""
        logger_lib.logMessage("Repairing switch: %s" % switch, logLevel='warning')
        return lib.repairSwitch(switch)

    def safRepairNetwork(self, subrack, slot):
        """This function repairs hardware used in System under test. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Repairing network", logLevel='warning')

    def safRepairMW(self, ):
        """This function repairs hardware used in System under test. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Repairing MW HA state", logLevel='warning')

    def safRepairTAPP(self, ):
        """This function repairs hardware used in System under test. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Repairing Test application", logLevel='warning')

    def safRepairTROJAN(self, ):
        """This function repairs hardware used in System under test. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Repairing Trojan application", logLevel='warning')

    def safRepairCluster(self):
        """This function repairs cluster on System under test by invoking cluster restart command. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        diagnose in index 1 used for fault analysing"""
        logger_lib.logMessage("Repairing cluster ", logLevel='warning')
        result, response, bootTime, uptime = bundle_lib.clusterRestart(CheckConfig=self.testConfig)
        ssh_lib.tearDownHandles()
        return result, response, bootTime, uptime 

    #System Information
    def safLogSystemInformation(self, cmds):
        """This function repairs hardware used in System under test. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and result string
        in index 1 used for fault analysing, the string will implicity be written to the log"""
        logger_lib.logMessage("Log system information", logLevel='debug')
        return lib.logSystemInformation(cmds) 

    #Environment settings
    def safSetProcessorLoadTestApplication(self):
        """This function repairs hardware used in System under test. 
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and result string
        in index 1 used for fault analysing, the string will implicity be written to the log"""
        logger_lib.logMessage("Set the load on test application instances", logLevel='debug')
        result, reply = lib.setProcessorLoad(self.testConfig)
        misc_lib.waitTime(5)
        return result, reply

    #Environment Resets
    def safResetSystemState(self):
        """This function will check all pid's of processes defined and do a diff from previosly performed check
        The function returns the deviation from last check"""
        logger_lib.logMessage("Reset system state (store current PID's)", logLevel='debug')
        result, self.originalState= bundle_lib.readSystemState(self.testConfig)
        return (result, self.originalState)

    def safResetDumps(self):
        """This function will store the latest dump created are created sincce the last reset (see stResetDumps() function)
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        fault message in index 1"""
        logger_lib.logMessage("Reset system dump directory", logLevel='debug')
        return lib.resetDumps()

    def safResetTraps(self):
        """This function will store the latest dump created are created sincce the last reset (see stResetDumps() function)
        The return of the function will be a tuple with the result (SUCCESS or ERROR) in index 0 and a corresponding
        fault message in index 1"""
        logger_lib.logMessage("Reset alarms and notifications", logLevel='debug')
        return oam_lib.notificationReceived()

    def safResetTestAppStatistics(self):
        """This function will store the reset the current statistics for all test application
        instances"""
        logger_lib.logMessage("Reset statisics", logLevel='debug')
        return lib.resetTestAppStatistics(self.testConfig)

    #Environment cleanup's
    def safCleanUpImm(self):
        logger_lib.logMessage("Clearing test application run time objects in IMM", logLevel='debug')
        return ssh_lib.sendCommand('/home/tspsaf/repository/TA_TAPP*/ta_tapp --mode imm-clean --instance xApp --syslog')

    def safCleanActiveAlarms(self):
        logger_lib.logMessage('Clearing the active alarm list', logLevel='debug')
        return oam_lib.clearActiveAlarms()

    def safCleanSwmLock(self):
        logger_lib.logMessage('Removing swm_lock', logLevel='debug')
        return st_env_lib.removeSwmLockFile()

    # Stop load
    def safStopTestAppLoad (self):
        logger_lib.logMessage('Stop the load on test application instances', logLevel='debug')
        return testapp_lib.stopTraffic()

    #Environment settings's
    def safSetTargetAddress(self, default):
        logger_lib.logMessage("Write the OSS target address", logLevel='debug')
        return oam_lib.setNorthBoundConfiguration(default)

    def safSetSysLogEntry(self, entry):
        logger_lib.logMessage("Write entry in SUT's syslog", logLevel='debug')
        return lib.setSysLogEntry(self.testConfig, entry, self.myId)


###############################################################################
# setUp
###############################################################################

    def setUp(self):
        '''TC_SUPER: This is the super class method setUp 
           TAG: TC-SUPER
           '''
        logger_lib.setLogFile(self.myId)
        #hand over control to unittest    
        NonUnitPythonTestCase.setUp(self)

        #if a repair is performed we need to ensure correct active controller 
        repairHwFlag = False

        #checks system HW and switches
        if self.testsuite_setup.has_key('hw'):
            if self.testsuite_setup['hw'] != [''] or 'system' in self.testcase_setup or 'switches' in self.testcase_setup:
                logger_lib.logMessage('Setup: Checking system HW')
            if ('switches' in self.testsuite_setup['hw']  and self.testcase_setup==[]) or 'switches' in self.testcase_setup:
                result, switches= self.safCheckSwitches()
                if result in self.failures:
                    for switch in switches:
                        result = self.safRepairSwitch(switch)
                        self.failUnlessEqual('SUCCESS' , result)
                        result, switches= self.safCheckSwitches()
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to repair switches: %s' % switches)
                        # No repair action for switch malfunction
            if ('system' in self.testsuite_setup['hw']  and self.testcase_setup==[]) or  'system' in self.testcase_setup:
                result, nodes = self.safCheckSystemNodes()
                if result in self.failures:
                    for subrack,slot in nodes:
                        result, reply = self.safRepairHW(subrack, slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    misc_lib.waitTime(240)
                    result, nodes = self.safCheckSystemNodes()
                    self.failUnlessEqual('SUCCESS' , result, nodes)
                    repairHwFlag = True

        #checks that network up and running
        if self.testsuite_setup.has_key('ip'):
            if self.testsuite_setup['ip'] != [''] or 'network' in self.testcase_setup:
                logger_lib.logMessage('Setup: Checking system internal network')
            if ('network' in self.testsuite_setup['ip'] and self.testcase_setup==[]) or 'network' in self.testcase_setup:
                result, nodes = self.safCheckNetwork()
                if result in self.failures:
                    for subrack,slot in nodes:
                        result, reply = self.safRepairHW(subrack, slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    misc_lib.waitTime(300)
                    for subrack,slot in nodes:
                        result, reply= lib.waitForBlade(subrack,slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    result, nodes = self.safCheckNetwork()
                    if result in self.failures:
                        result, response, bootTime, uptime  = self.safRepairCluster()
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to perform cluster restart: %s' % response)
                        result, nodes = self.safCheckNetwork()
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to repair nodes: %s' % nodes)
                    else:
                        repairHwFlag = True

        #When the HW is OK we try to get active controller 
        logger_lib.logMessage("Quering for active controller", logLevel='debug')
        result, (subrack, slot) = st_env_lib.updateActiveController()
        if result in self.failures:
           result, response, bootTime, uptime = self.safRepairCluster()
           self.failUnlessEqual('SUCCESS' , result, 'Failed to perform cluster restart: %s' % response)
           misc_lib.waitTime(300)
           result, subrack, slot = st_env_lib.updateActiveController()
           self.failUnlessEqual('SUCCESS' , result, 'Failed to get active controller')
        else:
            logger_lib.logMessage("Active controller: SC_%d_%d" % (subrack, slot), logLevel='debug')

        #checks MW SU's  
        result = saf_lib.checkSafClusterStatus()
        self.clusterStatus = result[len(result) - 1].splitlines()

        if self.testsuite_setup.has_key('mw'):
            if self.testsuite_setup['mw'] != [''] or 'saf' in self.testsuite_setup['mw'] or 'nodes' in self.testcase_setup:
                logger_lib.logMessage('Setup: Checking system SAF MW availability')
            if ('nodes' in self.testsuite_setup['mw']  and self.testcase_setup==[]) or 'nodes' in self.testcase_setup:
                result, nodes = self.safCheckSystemNodesState(self.clusterStatus) ###
                if result in self.failures:
                    for subrack,slot in nodes:
                        result, reply = self.safRepairHW(subrack, slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    misc_lib.waitTime(300)
                    for subrack,slot in nodes:
                        result, reply= lib.waitForBlade(subrack,slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    result = saf_lib.checkSafClusterStatus()
                    self.clusterStatus = result[len(result) - 1].splitlines()
                    result, nodes = self.safCheckSystemNodesState(self.clusterStatus) ###
                    if result in self.failures:
                        result, reply = self.safRepairCluster()
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to perform cluster restart: %s' % reply)
                        misc_lib.waitTime(300)
                        result = saf_lib.checkSafClusterStatus()
                        self.clusterStatus = result[len(result) - 1].splitlines()
                        result, nodes = self.safCheckSystemNodesState(self.clusterStatus) ###
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to get nodes state for: %s' % nodes)
                    else:
                        repairHwFlag = True

            if ('saf' in self.testsuite_setup['mw'] and self.testcase_setup==[]) or  'saf' in self.testcase_setup:
                result, nodes = self.safCheckMW(self.clusterStatus) ###
                if result in self.failures:
                    for subrack,slot in nodes:
                        result, reply = self.safRepairHW(subrack, slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    misc_lib.waitTime(300)
                    for subrack,slot in nodes:
                        result, reply= lib.waitForBlade(subrack,slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    result = saf_lib.checkSafClusterStatus()
                    self.clusterStatus = result[len(result) - 1].splitlines()
                    result, nodes = self.safCheckMW(self.clusterStatus) ###
                    if result in self.failures:
                        result, response, bootTime, uptime = self.safRepairCluster()
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to perform cluster restart: %s' % response)
                        misc_lib.waitTime(300)
                        result = saf_lib.checkSafClusterStatus()
                        self.clusterStatus = result[len(result) - 1].splitlines()
                        result, nodes = self.safCheckMW(self.clusterStatus) ###
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to repair SAF MW on: %s' % nodes)
                    else:
                        repairHwFlag = True
 
        #checks APPS SU's    
        if self.testsuite_setup.has_key('applications'):
            if self.testsuite_setup['applications'] != [''] or 'test_app' in self.testcase_setup or 'trojan' in self.testcase_setup:
                logger_lib.logMessage('Setup: Checking system applications availability')      
            if ('test_app' in self.testsuite_setup['applications'] and self.testcase_setup==[]) or 'test_app' in self.testcase_setup:
                result, info, nodes = self.safCheckTAPP(self.clusterStatus) ###
                if result in self.failures:
                    for subrack,slot in nodes:
                        result, reply = self.safRepairHW(subrack, slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    misc_lib.waitTime(300)
                    for subrack,slot in nodes:
                        result, reply= lib.waitForBlade(subrack,slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    result = saf_lib.checkSafClusterStatus()
                    self.clusterStatus = result[len(result) - 1].splitlines()
                    result, info, nodes  = self.safCheckTAPP(self.clusterStatus) ###
                    if result in self.failures:
                        result, response, bootTime, uptime= self.safRepairCluster()
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to perform cluster restart: %s' % response)
                        misc_lib.waitTime(300)
                        result = saf_lib.checkSafClusterStatus()
                        self.clusterStatus = result[len(result) - 1].splitlines()
                        result, info, nodes = self.safCheckTAPP(self.clusterStatus) ###
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to repair test application on: %s' % nodes)
                    else:
                        repairHwFlag = True
            if ('trojan' in self.testsuite_setup['applications'] and self.testcase_setup==[]) or 'trojan' in self.testcase_setup:
                result, nodes = self.safCheckTROJAN(self.clusterStatus) ###
                if result in self.failures:
                    for subrack,slot in nodes:
                        result, reply = self.safRepairHW(subrack, slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    misc_lib.waitTime(300)
                    for subrack,slot in nodes:
                        result, reply= lib.waitForBlade(subrack,slot)
                        self.failUnlessEqual('SUCCESS' , result, reply)
                    result = saf_lib.checkSafClusterStatus()
                    self.clusterStatus = result[len(result) - 1].splitlines()
                    result, nodes = self.safCheckTROJAN(self.clusterStatus) ###
                    if result in self.failures:
                        result, response, bootTime, uptime = self.safRepairCluster()
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to perform cluster restart: %s' % response)
                        misc_lib.waitTime(300)
                        result = saf_lib.checkSafClusterStatus()
                        self.clusterStatus = result[len(result) - 1].splitlines()
                        result, nodes = self.safCheckTROJAN(self.clusterStatus) ###
                        self.failUnlessEqual('SUCCESS' , result, 'Failed to repair trojan application on: %s' % nodes)                
                    else:
                        repairHwFlag = True

        if repairHwFlag:
            #When the HW has been repaired and OK we retry to get active controller 
            logger_lib.logMessage("Updating active controller after repair has been performed", logLevel='debug')
            result, (subrack, slot) = st_env_lib.updateActiveController()
            if result in self.failures:
                self.failUnlessEqual('SUCCESS' , result, 'Failed to get active controller')
            else:
                logger_lib.logMessage("Active controller after repair has been performed: SC_%d_%d" % (subrack, slot), logLevel='debug')             

        #checks SUTs interfaces#
        if self.testsuite_setup.has_key('interfaces'):
            if self.testsuite_setup['interfaces'] !=[''] or 'interfaces' in self.testcase_setup:
                logger_lib.logMessage('Setup: Checking system official interfaces availability') 
            if (self.testsuite_setup['interfaces'] !=[''] and self.testcase_setup==[]) or 'interfaces' in self.testcase_setup:
                result, reply = self.safCheckInterface(self.testsuite_setup['interfaces'])
                self.failUnlessEqual('SUCCESS', result, reply)                

        #collect current status of system(SUT)
        if self.testsuite_setup.has_key('info'):
            if self.testsuite_setup['info'] !=[''] or 'info' in self.testcase_setup:
                logger_lib.logMessage('Setup: Writing system information to log') 
            if (self.testsuite_setup['info'] !=[''] and self.testcase_setup==[]) or 'info' in self.testcase_setup:
                result, reply = self.safLogSystemInformation(self.testsuite_setup['info'])       
                if result in self.failures:
                    logger_lib.logMessage('Failed to log system information' , logLevel = 'warning')

        #prepare for testing
        if self.testsuite_setup_teardown.has_key('events'):                            
            if self.testsuite_setup_teardown['events'] != [''] or self.testcase_setup_teardown !=[] :
                logger_lib.logMessage('Setup: Preparing for testing') 
            #setup/teardown
            if ('log' in self.testsuite_setup_teardown['events'] and self.testcase_setup_teardown==[]) or 'log' in self.testcase_setup_teardown:
                result, reply = self.safSetSysLogEntry('setup')
                if result in self.failures:
                    logger_lib.logMessage('Failed to set testcase start entry in syslog ' , logLevel = 'warning')
            if ('address' in self.testsuite_setup_teardown['events'] and self.testcase_setup_teardown==[]) or 'address' in self.testcase_setup_teardown:
                result, address = self.safSetTargetAddress(default=False)
                self.failUnlessEqual('SUCCESS', result, 'Failed to set LMWP target address')  
            #setup/runtest
            if ('state' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'state' in self.testcase_setup_runtest:
                result, state = self.safResetSystemState()
                self.failUnlessEqual('SUCCESS', result, 'Failed to read sytem state')   
            if ('dumps' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'dumps' in self.testcase_setup_runtest:
                result, dumps = self.safResetDumps()
                self.failUnlessEqual('SUCCESS', result, 'Failed to reset dumps')   
            if ('statistics' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'statistics' in self.testcase_setup_runtest:
                result, statistics = self.safResetTestAppStatistics()
                self.failUnlessEqual('SUCCESS', result, 'Failed to reset statistics')
            if ('load' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'load' in self.testcase_setup_runtest:
                result, load = self.safSetProcessorLoadTestApplication()                    
                self.failUnlessEqual('SUCCESS', result, 'Failed to set Load')

        #invoke cleanups
        if self.testsuite_setup.has_key('cleanup'):
            if self.testsuite_setup['cleanup'] != [''] or 'imm' in self.testcase_setup or 'alarms' in self.testcase_setup or 'swm_lock' in self.testcase_setup:
                logger_lib.logMessage('Setup: Cleanup system') 
            if ('imm' in self.testsuite_setup['cleanup'] and self.testcase_setup==[]) or 'imm' in self.testcase_setup:
                result, reply = self.safCleanUpImm() 
                if result in self.failures:
                    logger_lib.logMessage('Failed to clean up Test application runtime objects in IMM ' , logLevel = 'warning')
            if ('alarms' in self.testsuite_setup['cleanup'] and self.testcase_setup==[]) or 'alarms' in self.testcase_setup:
                result, alarms = self.safCleanActiveAlarms()           
                self.failUnlessEqual('SUCCESS', result, 'Failed to clear active alarms in active alarm list (AAL)')  
            if ('swm_lock' in self.testsuite_setup['cleanup'] and self.testcase_setup==[]) or 'swm_lock' in self.testcase_setup:
                result, lock = self.safCleanSwmLock()           
                self.failUnlessEqual('SUCCESS', result, 'Remove the swm_lock fails with %s' % lock) 
    
        #Finally reset the "trap reader"
        if self.testsuite_setup_teardown.has_key('events'):  
            if ('traps' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'traps' in self.testcase_setup_runtest:           
                result, traps, heartbeats, heartbeatList = self.safResetTraps()
                self.failUnlessEqual('SUCCESS', result, 'Failed to Clear Notifications')

        #run test start time
        self.startTime=time.localtime() # Start time of RunTest


###############################################################################
# runTest
###############################################################################
    def runTest(self):
        '''TC_SUPER: This is the super class method runTest 
           TAG: TC-SUPER
           '''
        #checks HW 
        if self.testsuite_runtest.has_key('hw'):
            if self.testsuite_runtest['hw'] != [''] or 'system' in self.testcase_runtest or 'switches' in self.testcase_runtest:
                logger_lib.logMessage('Runtest: Checking system HW')
            if ('switches' in self.testsuite_runtest['hw']  and self.testcase_runtest==[]) or 'switches' in self.testcase_runtest:    
                result, switch = self.safCheckSwitches()
                self.failUnlessEqual('SUCCESS' , result, 'System switch failure: %s' % switch)
            if ('system' in self.testsuite_runtest['hw']  and self.testcase_runtest==[]) or 'system' in self.testcase_runtest:    
                result, nodes = self.safCheckSystemNodes()
                self.failUnlessEqual('SUCCESS' , result, 'System nodes failure: %s' % nodes)

        #checks OS 's utils
        if self.testsuite_runtest.has_key('ip'):
            if self.testsuite_runtest['ip'] != [''] or 'network' in self.testcase_runtest:
                logger_lib.logMessage('Runtest: Checking system internal network')
            if ('network' in self.testsuite_runtest['ip']  and self.testcase_runtest==[]) or 'network' in self.testcase_runtest:        
                    result, network = self.safCheckNetwork()
                    self.failUnlessEqual('SUCCESS' , result, 'System network failure: %s' % network)

        #checks MW SU's  
        result = saf_lib.checkSafClusterStatus()
        self.clusterStatus = result[len(result) - 1].splitlines()

        if self.testsuite_runtest.has_key('mw'):
            if self.testsuite_runtest['mw'] != [''] or 'saf' in self.testcase_runtest or 'nodes' in self.testcase_runtest:
                logger_lib.logMessage('Runtest: Checking system SAF MW availability')
            if ('nodes' in self.testsuite_runtest['mw'] and self.testcase_runtest==[]) or 'nodes' in self.testcase_runtest:        
                result, nodeState = self.safCheckSystemNodesState(self.clusterStatus) ###
                self.failUnlessEqual('SUCCESS' , result, 'SAF Node HA state failue: %s' % nodeState)
            if ('saf' in self.testsuite_runtest['mw']  and self.testcase_runtest==[]) or 'saf' in self.testcase_runtest:        
                result, safMw = self.safCheckMW(self.clusterStatus) ###
                self.failUnlessEqual('SUCCESS' , result, 'SAF MW HA state failue: %s' % safMw)

        #checks APPS SU's    
        if self.testsuite_runtest.has_key('applications'):
            if self.testsuite_runtest['applications'] != [''] or 'test_app' in self.testcase_runtest or 'trojan' in self.testcase_runtest:
                logger_lib.logMessage('Runtest: Checking system applications availability')      
            if ('test_app' in self.testsuite_runtest['applications'] and self.testcase_runtest==[]) or 'test_app' in self.testcase_runtest:
                result, info, nodes = self.safCheckTAPP(self.clusterStatus) ###
                self.failUnlessEqual('SUCCESS' , result, 'Test Application HA state failue: %s' % info)
            if ('trojan' in self.testsuite_runtest['applications'] and self.testcase_runtest==[]) or 'trojan' in self.testcase_runtest:
                result, trojan = self.safCheckTROJAN(self.clusterStatus) ###
                self.failUnlessEqual('SUCCESS' , result, 'Trojan HA state failue: %s' % trojan)

        #checks SUTs interfaces
        if self.testsuite_runtest.has_key('interfaces'):
            if self.testsuite_runtest['interfaces'] !=[''] or 'interfaces' in self.testcase_runtest:
                logger_lib.logMessage('Runtest: Checking system official interfaces availability') 
            if (self.testsuite_runtest['interfaces'] !=[''] and self.testcase_runtest==[]) or 'interfaces' in self.testcase_runtest:
                result, reply = self.safCheckInterface(self.testsuite_runtest['interfaces'])
                self.failUnlessEqual('SUCCESS' , result, 'System interface check fails, see log for details') 

        #validate system after testing (setup/runtest)
        if self.testsuite_setup_runtest.has_key('events'):
            if self.testsuite_setup_runtest['events'] != [''] or self.testcase_setup_runtest !=[] :
                logger_lib.logMessage('Runtest: Analysing system') 
            #measurements
            if ('statistics' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'statistics' in self.testcase_setup_runtest:
                result, statistics = self.safCheckTestAppStatistics() 
                self.failUnlessEqual('SUCCESS' , result,  'Test Application statistics fails, see log for details')
            if ('load' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'load' in self.testcase_setup_runtest:
                result, load = self.safCheckTestAppLoad()
                self.failUnlessEqual('SUCCESS' , result,  'Test Application check load fails, see log for details')
            if ('dumps' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'dumps' in self.testcase_setup_runtest:
                result, dumps = self.safCheckDumps()
                self.failUnlessEqual('SUCCESS' , result,  'System dumps fails, see log for details')
            if ('traps' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'traps' in self.testcase_setup_runtest:                
                result, traps, heartbeats, heartbeatList = self.safCheckTraps()
                self.failUnlessEqual('SUCCESS' , result,  'Check traps fails, see log for details')
            if ('state' in self.testsuite_setup_runtest['events'] and self.testcase_setup_runtest==[]) or 'state' in self.testcase_setup_runtest:
                result, state = self.safCheckSystemState()
                self.failUnlessEqual('SUCCESS' , result,  'System state fails, see log for details')

        #log information of current status of system(SUT)
        if self.testsuite_runtest.has_key('info'):
            if self.testsuite_runtest['info'] !=[''] or 'info' in self.testcase_runtest:
                logger_lib.logMessage('Runtest: Writing system information to log') 
            if (self.testsuite_runtest['info'] !=[''] and self.testcase_runtest==[]) or 'info' in self.testcase_runtest:
                result = self.safLogSystemInformation(self.testsuite_runtest['info'])       
                if result in self.failures:
                    logger_lib.logMessage('Failed to log system information' , logLevel = 'warning')

###############################################################################
# tearDown
###############################################################################
    def tearDown(self):
        '''TC_SUPER: This is the super class method tearDown 
           TAG: TC-SUPER
           '''
        #run test end time
        self.endTime=time.localtime() # End time of RunTest

        if self.testsuite_setup_teardown.has_key('events'):
            if self.testsuite_setup_teardown['events'] != [''] or self.testcase_setup_teardown !=[] :
                logger_lib.logMessage('Teardown: Restoring system') 
            if ('load' in self.testsuite_setup_teardown['events'] and self.testcase_setup_teardown==[]) or 'load' in self.testcase_setup_teardown:
                result, load = self.safStopTestAppLoad()
                self.failUnlessEqual('SUCCESS' , result,  'Test Application stop load fails see log for details')
            if ('address' in self.testsuite_setup_teardown['events'] and self.testcase_setup_teardown==[]) or 'address' in self.testcase_setup_teardown:
                result, address = self.safSetTargetAddress(default=True)
                self.failUnlessEqual('SUCCESS', result, 'Failed to set DEFAULT target address')  
            #write entry in SUT logger files            
            if ('log' in self.testsuite_setup_teardown['events'] and self.testcase_setup_teardown==[]) or 'log' in self.testcase_setup_teardown:
                result, reply = self.safSetSysLogEntry('teardown')
                if result in self.failures:
                    logger_lib.logMessage('Failed to set testcase end entry in syslog', logLevel = 'warning')

        #invoke cleanups
        if self.testsuite_teardown.has_key('cleanup'):
            if self.testsuite_teardown['cleanup'] != [''] or 'swm_lock' in self.testcase_teardown:
                logger_lib.logMessage('Teardown: Cleanup system') 
            if ('swm_lock' in self.testsuite_teardown['cleanup'] and self.testcase_teardown==[]) or 'swm_lock' in self.testcase_teardown:
                result, lock = self.safCleanSwmLock()           
                self.failUnlessEqual('SUCCESS', result, 'Remove the swm_lock fails with %s' % lock) 

        ssh_lib.tearDownHandles()
        NonUnitPythonTestCase.tearDown(self)

###############################################################################
# Suit handling -- Common used features
###############################################################################

    def exitOnError(self):
        if hasattr(NonUnitPythonTestCase, 'enableStopOnFailure') and self.exitIfError == True and self.status != 'Passed' : #JCAT feature
            NonUnitPythonTestCase.enableStopOnFailure(self)

    def exitOnFailure(self):
        if hasattr(NonUnitPythonTestCase, 'enableStopOnFailure') and self.exitIfFail == True and self.status != 'Passed' : #JCAT feature
            NonUnitPythonTestCase.enableStopOnFailure(self)

    def exitOnPass(self):
        if hasattr(NonUnitPythonTestCase, 'enableStopOnFailure') and self.exitIfPass == True and self.status == 'Passed' : #JCAT feature
            NonUnitPythonTestCase.enableStopOnFailure(self)

###############################################################################
# Asserts handling 
###############################################################################

    def fail(self, result,  msg = ''):
        """This function overrides the pyUnit function fail and works as the
        system test default fail function used if not overrided by the test case itself 
        """
        if result not in self.successors:
            if msg != '':
                logger_lib.logMessage('fail assert message: %s' % msg, logLevel = 'error')
            else:
                logger_lib.logMessage('fail assert with no message', logLevel = 'error')
            if self.collectInfo == False:
                res, response = lib.collectInfo()
                logger_lib.logMessage(response)
                self.collectInfo = True
            # Seems stupid to raise failIf but in the JCAT fail is a static 
            # method and in pyJunit it is a nonstatic member
            NonUnitPythonTestCase.failIf(self, True, msg)

    def failIf(self, expr, msg = ''):
        """This function overrides the pyUnit function failUnless and works as the
        system test default failUnless function used if not overrided by the test case itself 
        """    
        if expr:
            if msg != '':
                logger_lib.logMessage('failIf assert message: %s' % msg, logLevel = 'error')
            else:
                logger_lib.logMessage('failIf assert with no message', logLevel = 'error')
            if self.collectInfo == False:
                res, response = lib.collectInfo()
                logger_lib.logMessage(response)
                self.collectInfo = True
            NonUnitPythonTestCase.failIf(self, expr, msg)

    def failUnless(self, expr, msg = ''):
        """This function overrides the pyUnit function failUnless and works as the
        system test default failUnless function used if not overrided by the test case itself 
        """    
        if not expr:
            if msg != '':
                logger_lib.logMessage('failUnless assert message: %s' % msg, logLevel = 'error')
            else:
                logger_lib.logMessage('failUnless assert with no message', logLevel = 'error')
            if self.collectInfo == False: 
                res, response = lib.collectInfo()
                logger_lib.logMessage(response)
                self.collectInfo = True
            NonUnitPythonTestCase.failUnless(self, expr, msg)

    def failIfEqual(self, first, second, msg = ''):
        """This function overrides the pyUnit function failIfEqual and works as the
        system test default failIfEqual function used if not overrided by the test case itself 
        """    
        if not cmp(first, second):
            if msg != '':
                logger_lib.logMessage('failIfEqual assert message: %s' % msg, logLevel = 'error')
            else:
                logger_lib.logMessage('failIfEqual assert with no message', logLevel = 'error')
            if self.collectInfo == False:
                res, response = lib.collectInfo()
                logger_lib.logMessage(response)
                self.collectInfo = True
            NonUnitPythonTestCase.failIfEqual(self, first, second, msg)

    def failUnlessEqual(self, first, second, msg = ''):
        """This function overrides the pyUnit function failUnlessEqual and works as the
        system test default failUnlessEqual function used if not overrided by the test case itself 
        """    
        if cmp(first, second):
            if msg != '':
                logger_lib.logMessage('failUnlessEqual assert message: %s' % msg, logLevel = 'error')
            else:
                logger_lib.logMessage('failUnlessEqual assert with no message', logLevel = 'error')
            if self.collectInfo == False:
                res, response = lib.collectInfo()
                logger_lib.logMessage(response)
                self.collectInfo = True
            NonUnitPythonTestCase.failUnlessEqual(self, first, second, msg)

###############################################################################
# This is the exported function executing the testcases
###############################################################################
def getSuite(testcases):
    """This function acts as a layer where the possibility are made to manipulate 
    the list of testcases generated by the test suite itself""" 

    testSuitConfig = st_env_lib.getTestSuitConfig()

    # suite 
    if len(testcases) > 1:
        if testSuitConfig['testcase']['random'] == 'True': # randomize the testcase list
            random.shuffle(testcases)   
        if testSuitConfig['testcase']['instances'] != 0 and testSuitConfig['testcase']['instances'] < len(testcases) : # truncate the list
            testcases = testcases[:testSuitConfig['testcase']['instances']]

    # testcase
    for testcase in testcases :
        myId = testcase.runTest.__doc__.split(':')[0]
        testcase.setTestcase(myId.strip(), testcase.id())
        #suite

        if myId in testSuitConfig['events']['exitOnError']:
            testcase.exitIfError = True
        if myId in testSuitConfig['events']['exitOnError']:
            testcase.exitIfError = True        
        if myId in testSuitConfig['events']['exitOnPass']:
            testcase.exitIfPass = True

        #testsuite_setup/testsuite_teardown
        testcase.testsuite_setup_runtest = testSuitConfig['setup/runtest']
        #testsuite_setup/testsuite_teardown
        testcase.testsuite_setup_teardown = testSuitConfig['setup/teardown']
        #testsuite_setup
        testcase.testsuite_setup = testSuitConfig['setup']
        #testsuite_runtest
        testcase.testsuite_runtest = testSuitConfig['runtest']
        #testsuite_teardown
        testcase.testsuite_teardown = testSuitConfig['teardown']

    return TestSuite(testcases)
