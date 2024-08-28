#!/vobs/tsp_saf/tools/Python/linux/bin/python
# coding=iso-8859-1
###############################################################################
#
# Ericsson AB 2010 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and dissemination to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################
"""
GENERAL INFORMATION:

    Test cases:

    ==================================
    TEST CASE SPECIFICATION:

    Tag:

    Id:
    ""

    This test case shall work on the latest components starting at least from CMW 3.1 (for new components) and CMW 3.0 for the backward compatibility.
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
import xml.etree.ElementTree as ET
import os
import time
import re
import copy

from java.lang import System

class pmtSa(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.reqCmwVersion = "R4A10"  # this value is overwritten by a value from the tc_PMTSA_001.xml file
        self.reqCmwRelease = "1"

        self.PdfCmwVersion = "R8A08"  # CMW support PDF counter
        self.PdfCmwRelease = "1"

        self.reqComVerGP1min = "R1A03"  # COM version that supports PM Jobs with GP 1 minute (COM 4.0 Sh.13)
        self.reqComRelGP1min = "4"

        # COM, COMSA and CMW version which support "Always generate Pm result"
        self.reqComVerPmResult = "R2A11"
        self.reqComRelPmResult  = "5"
        self.reqCmwVerPmResult = "R10A15"
        self.reqCmwRelPmResult = "1"
        self.reqComSaVerPmResult = "R7A07"
        self.reqComSaRelPmResult = "3"

        self.test_config = testConfig
        self.job_description = {}
        self.measTypes = {}
        # We are not sure yet whether we are going to use CLI  or not, so just have it for the time being.

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.cli_input_1 = {}
        self.cli_expected_output_1 = {}
        self.cli_nonexpected_output_1 = {}
        self.cli_input_2 = {}
        self.cli_expected_output_2 = {}
        self.cli_nonexpected_output_2 = {}
        self.cli_input_3 = {}
        self.cli_expected_output_3 = {}
        self.cli_nonexpected_output_3 = {}
        self.cli_input_4 = {}
        self.cli_expected_output_4 = {}
        self.cli_nonexpected_output_4 = {}
        self.cli_input_5 = {}
        self.cli_expected_output_5 = {}
        self.cli_nonexpected_output_5 = {}
        self.cli_input_6 = {}
        self.cli_expected_output_6 = {}
        self.cli_nonexpected_output_6 = {}
        self.cli_input_7 = {}
        self.cli_expected_output_7 = {}
        self.cli_nonexpected_output_7 = {}
        self.cli_input_8 = {}
        self.cli_expected_output_8 = {}
        self.cli_nonexpected_output_8 = {}
        self.cli_input_9 = {}
        self.cli_expected_output_9 = {}
        self.cli_nonexpected_output_9 = {}
        self.cli_input_10 = {}
        self.cli_expected_output_10 = {}
        self.cli_nonexpected_output_10 = {}
        self.cli_input_11 = {}
        self.cli_expected_output_11 = {}
        self.cli_nonexpected_output_11 = {}
        self.cli_input_12 = {}
        self.cli_expected_output_12 = {}
        self.cli_nonexpected_output_12 = {}
        self.cli_input_13 = {}
        self.cli_expected_output_13 = {}
        self.cli_nonexpected_output_13 = {}
        self.cli_input_14 = {}
        self.cli_expected_output_14 = {}
        self.cli_nonexpected_output_14 = {}
        self.cli_input_15 = {}
        self.cli_expected_output_15 = {}
        self.cli_nonexpected_output_15 = {}
        self.cli_input_16 = {}
        self.cli_expected_output_16 = {}
        self.cli_nonexpected_output_16 = {}
        self.cli_input_17 = {}
        self.cli_expected_output_17 = {}
        self.cli_nonexpected_output_17 = {}
        self.cli_input_18 = {}
        self.cli_expected_output_18 = {}
        self.cli_nonexpected_output_18 = {}
        self.cli_input_19 = {}
        self.cli_expected_output_19 = {}
        self.cli_nonexpected_output_19 = {}
        self.cli_input_20 = {}
        self.cli_expected_output_20 = {}
        self.cli_nonexpected_output_20 = {}
        self.cli_input_21 = {}
        self.cli_expected_output_21 = {}
        self.cli_nonexpected_output_21 = {}
        self.cli_input_22 = {}
        self.cli_expected_output_22 = {}
        self.cli_nonexpected_output_22 = {}
        self.cli_input_23 = {}
        self.cli_expected_output_23 = {}
        self.cli_nonexpected_output_23 = {}
        self.cli_input_24 = {}
        self.cli_expected_output_24 = {}
        self.cli_nonexpected_output_24 = {}
        self.cli_input_25 = {}
        self.cli_expected_output_25 = {}
        self.cli_nonexpected_output_25 = {}
        self.cli_input_26 = {}
        self.cli_expected_output_26 = {}
        self.cli_nonexpected_output_26 = {}
        self.cli_input_27 = {}
        self.cli_expected_output_27 = {}
        self.cli_nonexpected_output_27 = {}
        self.cli_input_28 = {}
        self.cli_expected_output_28 = {}
        self.cli_nonexpected_output_28 = {}
        self.cli_input_29 = {}
        self.cli_expected_output_29 = {}
        self.cli_nonexpected_output_29 = {}
        self.cli_input_30 = {}
        self.cli_expected_output_30 = {}
        self.cli_nonexpected_output_30 = {}
        self.cli_input_31 = {}
        self.cli_expected_output_31 = {}
        self.cli_nonexpected_output_31 = {}
        self.cli_input_32 = {}
        self.cli_expected_output_32 = {}
        self.cli_nonexpected_output_32 = {}

        self.useExternalModels = {}
        self.pathToModelFiles = {}
        self.momFile = {}
        self.immClassesFile = {}
        self.immObjectsFile = {}
        self.momFile2 = {}
        self.immClassesFile2 = {}
        self.immObjectsFile2 = {}
        self.modelFilePathOnTarget = '/home/modelFilesCliTest/'
        self.immObjPattern = '[]'


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        self.cli_tester_script = dict.get("CLI_TESTER_SCRIPT")
        self.pathToPmtSaFiles = '%s%s' % (self.COMSA_VERIF_PATH, dict.get("PATH_TO_PMTSA_FILES"))
        self.pathToPmtSaPdfFiles = '%s%s' % (self.COMSA_VERIF_PATH, dict.get("PATH_TO_PMTSA_PDF_FILES"))
        self.pathToPmtSaMr40135 = '%s%s' % (self.COMSA_VERIF_PATH, dict.get("PATH_TO_PMTSA_MR40135"))
        self.pathToRpms = dict.get('PATH_TO_VALGRIND_RPMS')
        self.replaceComScript = '%s%s' % (self.COMSA_VERIF_PATH, dict.get('REPLACE_COM_SCRIPT_VALGRIND'))
        self.pathOnTarget = dict.get('PATH_ON_TARGET_VALGRIND')
        self.serviceInstanceName = dict.get("SERVICE_INSTANCE_NAME")
        self.amfNodePattern = dict.get("AMF_NODE_PATTERN")
        self.comNoBackup = dict.get("COM_NO_BACKUP")

        self.memoryCheck = False
        if self.testSuiteConfig.has_key('memoryCheck'):
            self.memoryCheck = eval(self.testSuiteConfig['memoryCheck']['memoryCheck'])

        """
        Stress Tool option
        """
        self.installStressTool = eval(System.getProperty("runStressTool"))

        coreTestCase.CoreTestCase.setUp(self)

        if self.memoryCheck:
            result = self.comsa_lib.activateValgrind(self, self.testConfig, self.pathToRpms, self.replaceComScript, self.pathOnTarget, pathToValgrindLogs=self.testSuiteConfig['memoryCheck']['valgrindLogsOnTarget'])
            self.fail(result[0], result[1])

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        if self.installStressTool:
            self.setTestStep('======== Install the stress tool ========')
            self.comsa_lib.installStressToolOnTarget(self)
            self.setTestStep('======== Start the stress tool ========')

            # Determine the number of processor cores in the node
            res = self.comsa_lib.getNumOfCPUsOnNode(self)
            self.fail(res[0], res[1])
            numOfCpuCores = res[1];
            self.myLogger.debug('Found %s CPU cores' % numOfCpuCores)

            # Determine the total physical RAM in the node
            res = self.comsa_lib.getBytesOfRamOnNode(self)
            self.fail(res[0], res[1])
            totalRamBytes = res[1];
            tenPercentOfTotalRam = int(totalRamBytes) // 10
            self.myLogger.debug('Found total %s bytes of RAM, 10 percent is %s' % (totalRamBytes, tenPercentOfTotalRam))

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM, plus local and NFS disk stress
            res = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60 * 60 * 60, 2, 4194304, 1, 65536)

            stressTimeOut = 60
            self.sshLib.setTimeout(stressTimeOut)

        self.setTestStep('Check the required versions of CMW Because some commands are supported on at least CMW == 3.1 and higher \
                          and some commands are supported on at older than CMW 3.1')
        self.doTearDown = False
        self.FirstXMLfile = 'IMM1.xml'
        self.SecondXMLfile = 'IMM2.xml'
        self.ThirdXMLfile = 'IMM3.xml'
        applicationBinary = 'pmsv_producer_cmd'
        self.pathtoIMMFilesAtTarget = '/home/PMT-SA/'
        pm_data_storage = '%sPerformanceManagementReportFiles/' % self.comNoBackup
        pmJobGpInSeconds = 300  # Granularity Period in seconds (5 minutes)

        #################  Check which CMW Version is installed  #############################################
        self.setTestStep('Check the installed version of CMW in the system')
        self.CmwOK = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion)

        if self.CmwOK[1] == False:
            self.myLogger.info("There is a CMW version installed which is older than CMW 3.1 so that it returns False:")  # False

        elif self.CmwOK[1] == True:
            self.myLogger.info("There is a CMW version installed which is at least CMW 3.1 so that it returns True:")  # True

        #################  Check if the CMW Version supports PDF counters  #############################################
        self.setTestStep('Check if the installed version of CMW in the system supports PDF counters')
        self.CmwSupportPdf = self.lib.checkComponentVersion('cmw', self.PdfCmwRelease, self.PdfCmwVersion)

        if self.CmwSupportPdf[1] == False:
            self.myLogger.info("The installed CMW version does not support PDF counters.")

        elif self.CmwSupportPdf[1] == True:
            self.myLogger.info("The installed CMW version does support PDF counters")

        #################  Check if the COM Version supports PM Jobs with GP 1 minute  #############################################
        self.setTestStep('Check if the installed version of COM in the system supports PM Jobs with GP 1 minute')
        self.ComSupportsOneMinJobs = self.lib.checkComponentVersion('com', self.reqComRelGP1min, self.reqComVerGP1min)

        if self.ComSupportsOneMinJobs[1] == False:
            self.myLogger.info("The installed COM version does not support PM Jobs with GP 1 minute.")

        elif self.ComSupportsOneMinJobs[1] == True:
            self.myLogger.info("The installed COM version does support PM Jobs with GP 1 minute.")
            self.FirstXMLfile = 'pmjob.gp1min.IMM1.xml'
            self.SecondXMLfile = 'pmjob.gp1min.IMM2.xml'
            self.ThirdXMLfile = 'pmjob.gp1min.IMM3.xml'
            self.FourthXMLFile = 'mr35881-RO.xml'
            pmJobGpInSeconds = 60  # Granularity Period in seconds (1 minute)

        #################  Check if the CMW, COMSA, COM Version supports always generate Pm result  #############################################
        self.setTestStep('Check if the installed version of COM, COMSA, CMW in the system supports Always generate Pm result')
        self.PmResultSupport = self.lib.checkComponentVersion('com', self.reqComRelPmResult, self.reqComVerPmResult)
        if self.PmResultSupport[1] == True:
            self.PmResultSupport = self.lib.checkComponentVersion('cmw', self.reqCmwRelPmResult, self.reqCmwVerPmResult)
            if self.PmResultSupport[1] == True:
                self.PmResultSupport = self.lib.checkComponentVersion('comsa', self.reqComSaRelPmResult, self.reqComSaVerPmResult)
                if self.PmResultSupport[1] == True:
                    self.myLogger.info("The installed components support Always generate Pm result")
                    self.FourthXMLFile = 'mr40135-RO.xml'
                else:
                    self.myLogger.info("The installed COMSA version does not support Always generate Pm result")
            else:
                self.myLogger.info("The installed CMW version does not support Always generate Pm result")
        else:
            self.myLogger.info("The installed COM version does not support Always generate Pm result")

        ##########         4.17.1 Backwards compatibility: TC-PMT-BWC-001      ##################
        self.setTestStep('TC-PMT-BWC-001 - Backwards compatibility- Verify that COM starts up without problems')
        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        cmd = 'date +\%s'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        currTime = int(result[1])
        currTime_minus1day = currTime - 86400

        okFlag = False
        searchPattern = ['PMT-SA', 'PmComComponent::pmtsa_start() started OK']
        for controller in self.testConfig['controllers']:
            result = self.lib.getEventTimestampFromSyslog(controller[0], controller[1], searchPattern, currTime_minus1day, self.testConfig)
            if result[0] == 'SUCCESS':
                latestTime = result[1][len(result[1]) - 1]
                result = self.lib.timeConvUnixToReadable(latestTime)
                self.fail(result[0], result[1])
                readableTime = result[1]
                self.setAdditionalResultInfo("Latest syslog entry from the past 24 hours on controller %s containing 'PmComComponent::pmtsa_start() \
                started OK' found at: %s" % (str(controller), readableTime))
            else:
                if 'No entry found in the syslog after the start time':
                    self.setAdditionalResultInfo('WARNING: The string "PmComComponent::pmtsa_start() started OK" not found in controller %s \
                    syslog for the past 24 hours. This can be still OK' % str(controller))
                else:
                    self.fail(result[0], result[1])

        #############################################################################################################################
        self.setTestStep('Start and Stop of PMT SA')

        self.myLogger.debug('Resetting the timer')
        cmd = 'date +\%s'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        startTime = int(result[1])
        self.myLogger.debug("Result of first time:%s" % startTime)

        self.restartCom()

        # Two checks on Active SC: 1. Start PMTSA 2.Stop PMTSA
        # 1. Start PMTSA
        self.myLogger.info('Grepping on Active SC: PmComComponent::pmtsa_start() started OK')
        searchPatterns = ['PmComComponent::pmtsa_start() started OK']
        result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPatterns, startTime, self.testConfig, logDir='/var/log/')
        self.fail(result[0], result[1])

        # 2. Stop PMTSA
        self.myLogger.info('Grepping on Active SC: pmtsa_stop() stop call')
        searchPatterns = ['pmtsa_stop() stop call']
        result = self.lib.getEventTimestampFromSyslog(self.activeController[0], self.activeController[1], searchPatterns, startTime, self.testConfig, logDir='/var/log/')
        self.fail(result[0], result[1])

        # The build machine at DEK (Ubuntu Vbox) appears to be slower than the one used at EAB (SuSE)
        # Determine on which server we run using the same method as in 'sourceme.tcsh'
        self.myLogger.debug('Get the host type')
        cmd = 'test -f /etc/SuSE-release ; echo $?'
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        eabHost = int(result[1])
        if eabHost == 0:
            self.myLogger.info('This test is running at EAB SuSE server')
        else:
            self.myLogger.info('This test is NOT running at EAB SuSE server')

        # Skip the switchover test if running at DEK server
        if eabHost == 1:
            self.myLogger.info('Skipping the Switchover test because NOT running at EAB SuSE server')
        else:

            ##################################### TC-PMT-PM-002 - Switchover  ###########################################################################
            self.setTestStep('TC-PMT-PM-002 - Switchover')
            self.myLogger.info('1. Start COM:verify that PMT-SA should not be loaded on the passive SC but loaded on active SC, There is no need to do this step since we have done it before')


            ################# Switchover Test case Starts from  here  ############################################################################
            self.myLogger.debug('We need to take this time since we have to use this time to grep PMT-SA Start, after switchover')
            self.myLogger.debug('Resetting the timer')
            cmd = 'date +\%s'
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            new_startTime = int(result[1])
            self.myLogger.debug("Result of second time:%s" % new_startTime)

            noOfScs = len(self.testConfig['controllers'])
            if noOfScs == 2:
                self.setTestStep('Switchover - Make a COM-SA Switchover')

                activeController = 0
                standbyController = 0

                controllers = self.testConfig['controllers']
                self.myLogger.info('Checking HA state for Com SA on the controllers')
                for controller in controllers:
                    result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], controller[1], self.serviceInstanceName, self.amfNodePattern)
                    self.fail(result[0], result[1])
                    if result[1] == 'ACTIVE':
                        activeController = controller[1]
                        activeController_param = controller
                        self.myLogger.info('Found active controller: %s' % str(controller))

                    elif result[1] == 'STANDBY':
                        standbyController = controller[1]
                        standbyController_param = controller
                        self.myLogger.info('Found standby controller: %s' % str(controller))

                if activeController == 0:
                    self.fail('ERROR', 'No controller found with active instance of ComSa')
                elif standbyController == 0:
                    self.fail('ERROR', 'No controller found with standby instance of ComSa.')


                self.setTestStep('Get ComSa DN and lock ')

                result = self.comsa_lib.lockSu(controller[0], activeController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck)
                self.fail(result[0], result[1])


                self.setTestStep('Verify that the former standby SC became active ')

                result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], standbyController, self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                if result[1] != 'ACTIVE':
                    self.fail(result[0], 'The former standby controller did not become active after the former active controller was locked.')

                self.myLogger.info('The former standby controller became active')

                oldActiveController = activeController
                activeController = standbyController

                standbyController = 0
                self.setTestStep('Unlock the locked SC')

                result = self.comsa_lib.unlockSu(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern, self.memoryCheck)
                self.fail(result[0], result[1])
                self.myLogger.info('%s' % str(result[1]))


                self.setTestStep('Verify that the former active SC becomes standby.')

                result = self.comsa_lib.getComSaServiceInstanceHaState(controller[0], oldActiveController, self.serviceInstanceName, self.amfNodePattern)
                self.fail(result[0], result[1])
                if result[1] != 'STANDBY':
                    self.fail(result[0], 'The former active controller did not become standby after the sericeUnit was unlocked.')

                self.myLogger.info('The former active controller became standby')
                # standbyController = oldActiveController


                ###################### Verify PMT-SA is loaded on new active SC : Inside Switchover Test Case - Tag: TC-PMT-PM-002  ################

                self.myLogger.info('After Switch over,Verify PMT-SA is loaded on new active SC ')


                # Grep pmtsa_start

                self.myLogger.debug('Grepping 2nd time, on New Active SC: PmComComponent::pmtsa_start() started OK')
                searchPatterns_2 = ['PmComComponent::pmtsa_start() started OK']

                result = self.lib.getEventTimestampFromSyslog(standbyController_param[0], standbyController_param[1], searchPatterns_2, new_startTime, self.testConfig, logDir='/var/log/')
                self.fail(result[0], result[1])


                self.myLogger.info('After Switch over,Verify that shutdown of PMT-SA on the former active (Previously Active, currently Passive)SC was performed correctly')

                # Grep pmtsa_stop

                self.myLogger.debug('Grepping on New Standby SC (former Active SC): pmtsa_stop() stop call')
                searchPatterns_2 = ['pmtsa_stop() stop call']

                result = self.lib.getEventTimestampFromSyslog(activeController_param[0], activeController_param[1], searchPatterns_2, new_startTime, self.testConfig, logDir='/var/log/')
                self.fail(result[0], result[1])

        #################   Test Case TC-PMT-PM-003. Single measurement starts here  ##############################################################

        if self.CmwSupportPdf[1] == True:
            self.setTestStep('Test Case TC-PMT-PM-003. Multi-value measurement (PDF counter)')
        else:
            self.setTestStep('Test Case TC-PMT-PM-003. Single measurement')

        result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
        self.fail(result[0], result[1])
        self.activeController = result[1]

        self.setTestStep('Creating a Directory at target and Copying these "IMM*.xml" files at target.')

        result = self.sshLib.sendCommand('\\rm -rf %s' % self.pathtoIMMFilesAtTarget, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('mkdir -p %s' % self.pathtoIMMFilesAtTarget, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])

        result = self.sshLib.remoteCopy('%s%s' % (self.pathToPmtSaFiles, self.FirstXMLfile), self.pathtoIMMFilesAtTarget , timeout=120, numberOfRetries=2)
        self.fail(result[0], result[1])
        result = self.sshLib.remoteCopy('%s%s' % (self.pathToPmtSaFiles, self.SecondXMLfile), self.pathtoIMMFilesAtTarget , timeout=120, numberOfRetries=2)
        self.fail(result[0], result[1])
        result = self.sshLib.remoteCopy('%s%s' % (self.pathToPmtSaFiles, self.ThirdXMLfile), self.pathtoIMMFilesAtTarget , timeout=120, numberOfRetries=2)
        self.fail(result[0], result[1])

        self.setTestStep('Importing the files with command "immcfg -f <filename>')

        result = self.sshLib.sendCommand ('immcfg -f %s%s' % (self.pathtoIMMFilesAtTarget, self.FirstXMLfile), self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if result[1] != "":
           self.fail('ERROR', 'Importing %s%s failed: %s' % (self.pathtoIMMFilesAtTarget, self.FirstXMLfile, result[1]))

        result = self.sshLib.sendCommand ('immcfg -f %s%s' % (self.pathtoIMMFilesAtTarget, self.SecondXMLfile), self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if result[1] != "":
           self.fail('ERROR', 'Importing %s%s failed: %s' % (self.pathtoIMMFilesAtTarget, self.SecondXMLfile, result[1]))

        result = self.sshLib.sendCommand ('immcfg -f %s%s' % (self.pathtoIMMFilesAtTarget, self.ThirdXMLfile), self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if result[1] != "":
           self.fail('ERROR', 'Importing %s%s failed: %s' % (self.pathtoIMMFilesAtTarget, self.ThirdXMLfile, result[1]))

        if self.CmwSupportPdf[1] == True:
            self.setTestStep('Copy the PM Producer for PDF counter %s to %s on the target' % (applicationBinary, self.pathtoIMMFilesAtTarget))
            self.logger.info('Copying the PM Producer for PDF counter - spmsv_producer_cmd to target to %s' % self.pathtoIMMFilesAtTarget)
            result = self.sshLib.remoteCopy('%s%s' % (self.pathToPmtSaPdfFiles, applicationBinary), self.pathtoIMMFilesAtTarget , timeout=120, numberOfRetries=2)
            self.fail(result[0], result[1])
        else:
            self.setTestStep('Copy the PM Producer %s to %s on the target' % (applicationBinary, self.pathtoIMMFilesAtTarget))
            self.logger.info('Copying the PM Producer - spmsv_producer_cmd to target to %s' % self.pathtoIMMFilesAtTarget)
            result = self.sshLib.remoteCopy('%s%s' % (self.pathToPmtSaFiles, applicationBinary), self.pathtoIMMFilesAtTarget , timeout=120, numberOfRetries=2)
            self.fail(result[0], result[1])

        executableBinary = 'chmod +x %s%s' % (self.pathtoIMMFilesAtTarget, applicationBinary)
        result = self.sshLib.sendCommand(executableBinary, self.activeController[0], self.activeController[1])  # works on the target
        self.fail(result[0], result[1])

        # Clear the PM strorage area
        cmd = '\\rm -rf %s/*.xml' % pm_data_storage
        result = self.sshLib.sendCommand (cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])

        # Determine the next GP boundary moment in time and wait until: (then + 15 sec)
        # The GP is aligned to the system time, for example:
        # For GP 1 min the GP boundaries are (h:m:s) 1:17:00, 1:18:00, etc.
        # For GP 5 min the GP boundaries are (h:m:s) 1:15:00, 1:20:00, etc.

        cmd = 'date +\%M'  # get the minutes of the current time
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        minutesPastExactHour = int(result[1])

        minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
        minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary
        if minutesToWaitTo5MinGpBoundary > 0:
            minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1

        cmd = 'date +\%S'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        secondsPastExactMinute = int(result[1])

        counterWriteTargetTime = 45  # seconds past the exact minute

        # Align the counter writing time to GP

        if secondsPastExactMinute < counterWriteTargetTime:
            newWaitBeforeTime = counterWriteTargetTime - secondsPastExactMinute
        else:
            newWaitBeforeTime = 60 - secondsPastExactMinute + counterWriteTargetTime

        if pmJobGpInSeconds == 300:  # for GP 5 minutes
            newWaitBeforeTime = (minutesToWaitTo5MinGpBoundary * 60) + newWaitBeforeTime

        secondsBeforeGp = 60 - counterWriteTargetTime
        self.logger.info('Wait for %s seconds before starting the counter job at %s seconds before the GP boundary...' % (newWaitBeforeTime, secondsBeforeGp))
        self.miscLib.waitTime(newWaitBeforeTime)

        if self.CmwOK[1] == True:
            cmd = 'cmw-pmjob-start CcJob1'
        elif self.CmwOK[1] == False:
            cmd = 'immcfg -a requestedJobState=1 pmJobId=CcJob1,CmwPmpmId=1'

        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if 'command not found' in result[1]:
            self.fail('ERROR', result[1])
        elif 'error' in result[1] or 'FAILED' in result[1]:
            self.fail('ERROR', result[1])

        if self.ComSupportsOneMinJobs[1] == True:
            self.logger.info('Current Date and Time : %s  The granularity period for the job is one minute' % result[1])
        else:
            self.logger.info('Current Date and Time : %s  The granularity period for the job is five minutes' % result[1])

        if self.CmwSupportPdf[1] == True:
            cmd = '%s%s cc:CcGroup1:PDFcounter:counter:1,2,3' % (self.pathtoIMMFilesAtTarget, applicationBinary)  # for PDF
            self.logger.info('Increment a PDF counter values')
        else:
            cmd = '%s%s cc:CcGroup1:CcMT-1:AnyCounterName:1' % (self.pathtoIMMFilesAtTarget, applicationBinary)
            self.logger.info('Increase a counter value with one')

        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if result[1] != '':
            self.fail('ERROR', 'Expected empty string as result. Received %s' % result[1])

        # Determine the next GP boundary moment in time and wait until: (then + 15 sec)
        # The GP is aligned to the system time, for example:
        # For GP 1 min the GP boundaries are (h:m:s) 1:17:00, 1:18:00, etc.
        # For GP 5 min the GP boundaries are (h:m:s) 1:15:00, 1:20:00, etc.

        cmd = 'date +\%M'  # get the minutes of the current time
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        minutesPastExactHour = int(result[1])

        minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
        minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary
        if minutesToWaitTo5MinGpBoundary > 0:
            minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1

        cmd = 'date +\%S'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        secondsPastExactMinute = int(result[1])

        if secondsPastExactMinute < counterWriteTargetTime:
            waitAfterEndOfGpTime = counterWriteTargetTime - secondsPastExactMinute
        else:
            waitAfterEndOfGpTime = 60 - secondsPastExactMinute + counterWriteTargetTime

        if pmJobGpInSeconds == 300:  # for GP 5 minutes
            waitAfterEndOfGpTime = (minutesToWaitTo5MinGpBoundary * 60) + waitAfterEndOfGpTime

        waitAfterEndOfGpTime += 30

        self.logger.info('Wait for %s seconds to cross a GP boundary ...' % (waitAfterEndOfGpTime))
        self.miscLib.waitTime(waitAfterEndOfGpTime)

        # Align the counter writing time to GP

        cmd = 'date +\%M'  # get the minutes of the current time
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        minutesPastExactHour = int(result[1])

        minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
        minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary
        if minutesToWaitTo5MinGpBoundary > 0:
            minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1

        cmd = 'date +\%S'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        secondsPastExactMinute = int(result[1])

        if secondsPastExactMinute < counterWriteTargetTime:
            newWaitBeforeTime = counterWriteTargetTime - secondsPastExactMinute
        else:
            newWaitBeforeTime = 60 - secondsPastExactMinute + counterWriteTargetTime

        if pmJobGpInSeconds == 300:  # for GP 5 minutes
            newWaitBeforeTime = (minutesToWaitTo5MinGpBoundary * 60) + newWaitBeforeTime

        self.logger.info('Wait for %s seconds to write to the counter at %s seconds before the GP boundary...' % (newWaitBeforeTime, secondsBeforeGp))
        self.miscLib.waitTime(newWaitBeforeTime)

        if self.CmwSupportPdf[1] == True:
            cmd = '%s%s cc:CcGroup1:PDFcounter:counter:1,2,3' % (self.pathtoIMMFilesAtTarget, applicationBinary)  # for PDF
            self.logger.info('Increment again the PDF counter values')
        else:
            cmd = '%s%s cc:CcGroup1:CcMT-1:AnyCounterName:1' % (self.pathtoIMMFilesAtTarget, applicationBinary)
            self.logger.info('Increase again the counter value with one')

        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if result[1] != '':
            self.fail('ERROR', 'Expected empty string as result. Received %s' % result[1])

        cmd = 'date +\%S'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        secondsPastExactMinute = int(result[1])

        #
        # Note: 25 Seconds is not enough on a 2+N cots cluster. In this case COM SA is active
        #       on one SC and PMD is active on the other SC and takes longer
        # waitForComToWriteTheResult = 25
        waitForComToWriteTheResult = 35  # Seconds to wait after the GP for COM to write the result into a file
        if eabHost == 1:
            waitForComToWriteTheResult = 20  # Different wait period for DEK server

        waitForGpEnd = (60 - counterWriteTargetTime) + waitForComToWriteTheResult

        self.logger.info('Wait for %s seconds to cross a GP boundary including extra %s seconds for COM to write the result...'
                         % (waitForGpEnd, waitForComToWriteTheResult))
        self.miscLib.waitTime(waitForGpEnd)

        # Align the counter writing time to GP

        cmd = 'date +\%M'  # get the minutes of the current time
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        minutesPastExactHour = int(result[1])

        minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
        minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary
        if minutesToWaitTo5MinGpBoundary > 0:
            minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1

        cmd = 'date +\%S'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        secondsPastExactMinute = int(result[1])

        if secondsPastExactMinute < counterWriteTargetTime:
            newWaitBeforeTime = counterWriteTargetTime - secondsPastExactMinute
        else:
            newWaitBeforeTime = 60 - secondsPastExactMinute + counterWriteTargetTime

        if pmJobGpInSeconds == 300:  # for GP 5 minutes
            newWaitBeforeTime = (minutesToWaitTo5MinGpBoundary * 60) + newWaitBeforeTime

        self.logger.info('Wait for %s seconds to stop the job at %s seconds before the GP boundary...' % (newWaitBeforeTime, secondsBeforeGp))
        self.miscLib.waitTime(newWaitBeforeTime)

        self.logger.info('Stop the job')

        if self.CmwOK[1] == True:
            cmd = 'cmw-pmjob-stop CcJob1'
        elif self.CmwOK[1] == False:
            cmd = 'immcfg -a requestedJobState=2 pmJobId=CcJob1,CmwPmpmId=1'

        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if 'command not found' in result[1]:
            self.fail('ERROR', result[1])
        elif 'error' in result[1] or 'FAILED' in result[1]:
            self.fail('ERROR', result[1])

        # Here we need to wait for a full GP
        self.logger.info('Wait for %s seconds (one full GP) after the PM Job was stopped ...' % (pmJobGpInSeconds))
        self.miscLib.waitTime(pmJobGpInSeconds)

        self.logger.info('Verify that there is correct PM-data in /cluster/storage/no-backup/com-apr9010443/PerformanceManagementReportFiles/')
        # We expect to have two files which contain the string 'AnyCounterName'
        # From these two files one should contain a tag <suspect> with the value true
        # The other file should either not contain the tag or have its value as false

        if self.CmwSupportPdf[1] == True:
            cmd = 'cd %s; grep -l counter *.xml' % pm_data_storage
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
        else:
            cmd = 'cd %s; grep -l AnyCounterName *.xml' % pm_data_storage
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'Problem checking PM-data in %s. %s' % (pm_data_storage, result[1]))

        pmFiles = result[1].split()

        if len(pmFiles) != 2:
            self.fail('ERROR', 'Expected exactly 2 files to contain the string AnyCounterName under %s. Found: %d' % (pm_data_storage, len(pmFiles)))
        suspectCounter = 0
        notSuspectCounter = 0

        for file in pmFiles:
            cmd = 'grep suspect %s%s' % (pm_data_storage, file)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            if result[1] == '':
                notSuspectCounter += 1
            elif 'alse' in result[1]:
                notSuspectCounter += 1
            else:
                suspectCounter += 1
        if suspectCounter != 1:
            self.fail('ERROR', 'Expected exactly one match for suspectCounter. Got %d instead' % suspectCounter)
        if notSuspectCounter != 1:
            self.fail('ERROR', 'Expected exactly one match for notSuspectCounter. Got %d instead' % notSuspectCounter)

        #################################      Alarm Mapping- TC-PMT-PM-004      ##################################

        self.setTestStep('Alarm Mapping --- TC-PMT-PM-004  --- ')

        if self.CmwOK[1] == True:
            cmd = 'cmw-pmjob-start ThresJob1'
        elif self.CmwOK[1] == False:
            cmd = 'immcfg -a requestedJobState=1 pmJobId=ThresJob1,CmwPmpmId=1'
            # Creates the login params according to which controller runs the CLI
            self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                        self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)

        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if 'command not found' in result[1]:
            self.fail('ERROR', result[1])
        elif 'error' in result[1] or 'FAILED' in result[1]:
            self.fail('ERROR', result[1])

        if self.ComSupportsOneMinJobs[1] == True:
            sequence = [ 2639, 2640, 2160, 2159, 3239, 3240, 2760, 2159, 3900, 3360, 3359, 3899, 3901, 2159]
        else:
            sequence = [13199, 13200, 10800, 10799, 16199, 16200, 13800, 10799, 19500, 16800, 16799, 19499, 19501, 10799]

        """ This is the sequence of values AnyCounterName goes through for GP 5 minutes.
            For GP 1 minute the values are divided by 5 and rounded as appropriate

        Expected behavior:

        13199 - nothing happens
        13200 - (new) warning is raised
        10800 - nothing happens (warning is kept)
        10799 - warning is cleared
        16199 - (new) warning is raised
        16200 - warning changes to major alarm
        13800 - nothing happens (major alarm is kept)
        10799 - major alarm is cleared
        19500 - (new) critical alarm is raised
        16800 - nothing happens (critical alarm is kept)
        16799 - critical alarm changes to major alarm
        19499 - nothing happens (major alarm is kept)
        19501 - major alarm changes to critical alarm
        10799 - critical alarm is cleared
        """
        defaultSearchPattern = ['AnyCounterName', 'MDF Detected Model Error']

        if self.ComSupportsOneMinJobs[1] == True:
            threshDict = { 2639: [[], 0], 2640: [['WARNING'], 1], 2160: [[], 0], 2159: [['CLEARED'], 3], 3239: [['WARNING'], 1], \
                               3240: [['MAJOR'], 2], 2760: [[], 0], 3900: [['CRITICAL'], 1], 3360: [[], 0], 3359: [['MAJOR'], 2], \
                               3899: [[], 0], 3901: [['CRITICAL'], 2]}
        else:
            threshDict = {13199: [[], 0], 13200: [['WARNING'], 1], 10800: [[], 0], 10799: [['CLEARED'], 3], 16199: [['WARNING'], 1], \
                              16200: [['MAJOR'], 2], 13800: [[], 0], 19500: [['CRITICAL'], 1], 16800: [[], 0], 16799: [['MAJOR'], 2], \
                              19499: [[], 0], 19501: [['CRITICAL'], 2]}

        """
        In the dictionary the key is the counter value.
        The values associated to the keys are lists with 2 elements.
            The first element is for alarm log patterns
            The second element is for testing with CLI. The following codes are used:
            0 - no change expected
            1 - new alarm expected
            2 - changed alarm expected
            3 - cleared alarm expected
        """

        dateCmd = 'date +\%s'

        if self.CmwOK[1] == False:
            activeAlarms = self.getAlarmListFromCli()
            currentAlarm = ''

        newWaitBeforeTime = 0
        #Variables are used to adjust delay time for Vbox cluster
        timeDelayBeforeStart = True
        isVboxOrKvmCluster = self.comsa_lib.getVboxKvmClusterConfig(self)
        if isVboxOrKvmCluster == True:
            counterWriteTargetTime = 30

        for value in sequence:
            # Align the counter writing time to GP

            cmd = 'date +\%M\%S'  # get the minutes of the current time
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
            minutesPastExactHour = int(result[1][0:2])
            secondsPastExactMinute = int(result[1][2:4])
            # This code will make sure that the there is no more than one change of counter value in a GP.
            tmpMinutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
            # Time is so tight, so let's skip this GP, wait til next GP :)
            if tmpMinutesPast5minGpBoundary == 4 and secondsPastExactMinute > 45:
                self.miscLib.waitTime(20)
                cmd = 'date +\%M\%S'  # get the minutes of the current time
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0], result[1])
                minutesPastExactHour = int(result[1][0:2])
                secondsPastExactMinute = int(result[1][2:4])

            minutesPast5minGpBoundary = minutesPastExactHour - 5 * (minutesPastExactHour // 5)
            minutesToWaitTo5MinGpBoundary = 5 - minutesPast5minGpBoundary

            if minutesToWaitTo5MinGpBoundary > 0:
                minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - 1

            self.myLogger.debug('minutesPastExactHour: %s ' % minutesPastExactHour)
            self.myLogger.debug('secondsPastExactMinute: %s ' % secondsPastExactMinute)
            self.myLogger.debug('minutesPast5minGpBoundary: %s ' % minutesPast5minGpBoundary)
            self.myLogger.debug('minutesToWaitTo5MinGpBoundary: %s ' % minutesToWaitTo5MinGpBoundary)
            self.myLogger.debug('secondsToWaitTo5MinGpBoundary: %s ' % ((minutesToWaitTo5MinGpBoundary * 60) + newWaitBeforeTime))

            if secondsPastExactMinute < counterWriteTargetTime:
                timeDelayBeforeStart = True
                newWaitBeforeTime = counterWriteTargetTime - secondsPastExactMinute
                addedMinute = 0  # False (using number, so it can be easily added later)
            else:
                newWaitBeforeTime = 60 - secondsPastExactMinute + counterWriteTargetTime
                addedMinute = 1  # True (using number, so it can be added)

            # if it is still positive then take out the added minute, otherwise add a whole GP
            if minutesToWaitTo5MinGpBoundary > 0:
                minutesToWaitTo5MinGpBoundary = minutesToWaitTo5MinGpBoundary - addedMinute
            else:
                minutesToWaitTo5MinGpBoundary = 5 - addedMinute

            if pmJobGpInSeconds == 300:  # for GP 5 minutes
                newWaitBeforeTime = (minutesToWaitTo5MinGpBoundary * 60) + newWaitBeforeTime

            self.logger.info('Wait for %s seconds to write to the counter at %s seconds before the GP boundary...' % (newWaitBeforeTime, secondsBeforeGp))
            if timeDelayBeforeStart == True:
                self.miscLib.waitTime(newWaitBeforeTime)
                timeDelayBeforeStart = False
            self.logger.info('Setting the threshold job counter value to %d' % value)
            if self.CmwOK[1] == True:
                result = self.sshLib.sendCommand(dateCmd, self.activeController[0], self.activeController[1])
                self.fail(result[0], result[1])
                eventTime = result[1]

            cmd = '%s%s cc:CcGroup1:CcMT-1:AnyCounterName:%s' % (self.pathtoIMMFilesAtTarget, applicationBinary, value)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            if result[1] != '':
                self.logger.error('Expected empty string as result. Received %s' % result[1])
            self.logger.info('Wait for %s seconds to cross a GP boundary including extra %s seconds for COM to write the result in file...'
                             % (waitForGpEnd, waitForComToWriteTheResult))
            if isVboxOrKvmCluster == False:
                self.miscLib.waitTime(waitForGpEnd)
            else:
                #Only should wait for 35 seconds due to low performance of Vbox and KVM cluster
                #And retry checking alarm in log
                if self.CmwOK[1] == True:
                    self.miscLib.waitTime(35)
                else:
                    #Check alarm from COM CLI should have less time than log file
                    self.miscLib.waitTime(45)

            if threshDict[value][0] == []:
                self.logger.info('It is expected that there is no new alarm')

                if self.CmwOK[1] == True:
                    result = self.comsa_lib.getEventTimestampFromAlarmAlertLog(self.activeController[0], self.activeController[1], defaultSearchPattern, eventTime, self.testConfig)
                    if 'No entry found in the' and 'log for the following search pattern' not in result[1]:
                        self.fail('ERROR', 'It was expected that there is no new event in the alarm log. Search method returned: %s' % str(result))

                elif self.CmwOK[1] == False:
                    currentAlarms = self.getAlarmListFromCli()
                    if len(currentAlarms) != len(activeAlarms):
                        self.fail('ERROR', 'Expected the same number of alarms as before changing the counter value')
                    for alarm in currentAlarms:
                        if alarm not in activeAlarms:
                            self.fail('ERROR', 'Expected to find %s in %s' % (alarm, str(activeAlarms)))

            else:
                localSearchPattern = copy.deepcopy(defaultSearchPattern)
                for element in threshDict[value][0]:
                    localSearchPattern.append(element)
                if self.CmwOK[1] == True:
                    result = self.comsa_lib.getEventTimestampFromAlarmAlertLog(self.activeController[0], self.activeController[1], localSearchPattern, eventTime, self.testConfig)
                    self.fail(result[0], result[1])
                elif self.CmwOK[1] == False:
                    currentAlarms = self.getAlarmListFromCli()

                    # unchanged alarm
                    if threshDict[value][1] == 0:
                        if len(currentAlarms) != len(activeAlarms):
                            self.fail('ERROR', 'Expected the same number of alarms as before changing the counter value')
                        for alarm in currentAlarms:
                            if alarm not in activeAlarms:
                                self.fail('ERROR', 'Expected to find %s in %s' % (alarm, str(activeAlarms)))

                    # new alarm
                    elif threshDict[value][1] == 1:
                        if len(currentAlarms) <= len(activeAlarms):
                            self.fail('ERROR', 'Expected greater number of alarms as before changing the counter value')

                        copyOfCurrentAlarms = copy.deepcopy(currentAlarms)
                        if len(activeAlarms) > 0:
                            for alarm in currentAlarms:
                                for activeAlarm in activeAlarms:
                                    if alarm == activeAlarm:
                                        copyOfCurrentAlarms.pop(copyOfCurrentAlarms.index(alarm))

                        if len(copyOfCurrentAlarms) != 1:  # we expect one new alarm compared to the start of the test
                            self.fail('ERROR', 'We expected exactly one new alarm. Received: %d' % len(currentAlarms))
                        currentAlarm = copyOfCurrentAlarms[0]
                        self.showAlarmFromCli(currentAlarm, cli_expected_output=localSearchPattern)
                        activeAlarms = copy.deepcopy(currentAlarms)

                    # changed alarm
                    elif threshDict[value][1] == 2:
                        if len(currentAlarms) != len(activeAlarms):
                            self.fail('ERROR', 'Expected the same number of alarms as before changing the counter value')
                        for alarm in currentAlarms:
                            if alarm not in activeAlarms:
                                self.fail('ERROR', 'Expected to find %s in %s' % (alarm, str(activeAlarms)))
                        if currentAlarm == '':
                            self.fail('ERROR', 'We expected variable currentAlarm to be set.')
                        self.showAlarmFromCli(currentAlarm, cli_expected_output=localSearchPattern)

                    # cleared alarm
                    elif threshDict[value][1] == 3:
                        if len(currentAlarms) >= len(activeAlarms):
                            self.fail('ERROR', 'Expected smaller number of alarms as before changing the counter value')
                        if currentAlarm == '':
                            self.fail('ERROR', 'We expected variable currentAlarm to be set.')
                        self.showAlarmFromCli(currentAlarm, cli_expected_output='ERROR: Specific element not found')
                        currentAlarm = ''
                        activeAlarms = copy.deepcopy(currentAlarms)


        self.logger.info('Stop the job')

        if self.CmwOK[1] == True:
            cmd = 'cmw-pmjob-stop ThresJob1'
        elif self.CmwOK[1] == False:
            cmd = 'immcfg -a requestedJobState=2 pmJobId=ThresJob1,CmwPmpmId=1'

        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if 'command not found' in result[1]:
            self.fail('ERROR', result[1])
        elif 'error' in result[1] or 'FAILED' in result[1]:
            self.fail('ERROR', result[1])

        #################################      Always generate PM Measurement Results- TC-PMT-PM-005      ##################################

        if self.PmResultSupport[1] == True:
            self.setTestStep('--- Always generate PM Measurement Results TC-PMT-PM-005  --- ')

            #Clear obsolete report files
            cmd = '\\rm -rf %s/*.xml' % pm_data_storage
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

            #Parse config xml file into list
            #Request string input must be followed as list format ([element1, element2, ..])
            jobDescList = self.parseStringsToList(self.job_description)
            measTypeDict = self.parseStringsToList(self.measTypes)
            self.myLogger.debug('JobDescList is %s'  %jobDescList)

            jobName = jobDescList[0]
            pmGroup = jobDescList[1]
            granularityPeriod = jobDescList[2]
            reportingPeriod = jobDescList[3]
            jobPriority = jobDescList[4]
            reportContentGeneration = jobDescList[5]
            measReaders = jobDescList[6:]
            measTypesMapValueDict = {'CC': '0' , 'CC-I': '77', 'Gauge': '70', 'FTG': '0', 'DER': 'NIL', 'SI': '0'}

            #Add model file
            result = self.comsa_lib.findActiveController(self.testConfig, self.serviceInstanceName, self.amfNodePattern)
            self.fail(result[0], result[1])
            self.activeController = result[1]

            self.logger.info('Copying model files and add them to target.')
            result = self.sshLib.remoteCopy('%s%s' % (self.pathToPmtSaFiles, self.FourthXMLFile), self.pathtoIMMFilesAtTarget , timeout=120, numberOfRetries=2)
            self.fail(result[0], result[1])
            result = self.sshLib.sendCommand ('immcfg -f %s%s' % (self.pathtoIMMFilesAtTarget, self.FourthXMLFile), self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            if result[1] != "":
                self.fail('ERROR', 'Importing %s%s failed: %s' % (self.pathtoIMMFilesAtTarget, self.FourthXMLFile, result[1]))

            self.logger.info('Copying the PM Producer - spmsv_producer_cmd to target to %s' % self.pathtoIMMFilesAtTarget)
            result = self.sshLib.remoteCopy('%s%s' % (self.pathToPmtSaMr40135, applicationBinary), self.pathtoIMMFilesAtTarget , timeout=120, numberOfRetries=2)
            self.fail(result[0], result[1])

            self.logger.info('Create the PmJob')
            self.createMeasurementJob(jobName, pmGroup, measReaders, measTypeDict, granularityPeriod , reportingPeriod, jobPriority, reportContentGeneration)
            self.logger.info('Starting the job')
            self.changeStateJob(jobName, 'ACTIVE')

            #Sending any counter value for Gauge MeasType having resetAtGranPeriod(False) to check last written value
            cmd = '%s%s gauge:%s:Gauge:PmInstance:70' % (self.pathtoIMMFilesAtTarget, applicationBinary, pmGroup)
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])

            if reportingPeriod == 'ONE_MIN':
                waitForReportFile = 180
            elif reportingPeriod == 'FIVE_MIN':
                waitForReportFile = 900

            #should wait for 3 reporting periods to make sure result captured for 2 consecutive GPs
            self.miscLib.waitTime(waitForReportFile)
            self.logger.info('Verify PM measurement Result Files reported by COM')

            #Verify PM meas results in report file as description below
            ### collectionMethod   resetAtGranPeriod   initialValue   'empty'value
            ###       CC                  NA               Set             initialValue
            ###       CC                  NA               Not set         0
            ###       Gauge               TRUE             NA              0
            ###       Gauge               FALSE            NA              Last written value
            ###       DER                 NA               NA              NIL
            ###       SI                  NA               NA              0

            res = self.checkPmMeasFilesReportedByCom(measTypesMapValueDict)

            #Stop PmJob
            self.changeStateJob(jobName, 'STOPPED')
            #Delele PmJob
            self.logger.info('Delete the PmJob')
            self.deleteMeasurementJob(jobName)
            if 'ERROR' in res[0]:
                self.fail('ERROR','%s' % res[1])
        else:
            self.setTestStep('--- Skipped Always generate PM Measurement Results TC-PMT-PM-005  --- ')



        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")



    def tearDown(self):
        self.setTestStep('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        if self.CmwOK[1] == True:
            cmd = 'cmw-pmjob-stop CcJob1'
        elif self.CmwOK[1] == False:
            cmd = 'immcfg -a requestedJobState=2 pmJobId=CcJob1,CmwPmpmId=1'
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])

        if self.CmwOK[1] == True:
            cmd = 'cmw-pmjob-stop ThresJob1'
        elif self.CmwOK[1] == False:
            cmd = 'immcfg -a requestedJobState=2 pmJobId=ThresJob1,CmwPmpmId=1'
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])

        # clean IMM
        immObjPattern = 'CmwPm'
        excludedObjects = "| grep -v '^CmwPmpmId=1' | grep -v '^pmMeasurementCapabilitiesId=1,CmwPmpmId=1'"
        cmd = 'immfind | grep -i %s %s | xargs immcfg -d' % (immObjPattern, excludedObjects)
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])
        if result[1] != '':
            self.setAdditionalResultInfo('######## WARNING: The following issue occurred during removal of IMM objects. Command: %s. Result: %s' % (cmd, result[1]))

        # remove files from target
        cmd = '\\rm -rf %s' % self.pathtoIMMFilesAtTarget
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        #Remove measurementReport Files
        cmd = '\\rm -rf /storage/no-backup/com-apr9010443/PerformanceManagementReportFiles/A*'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')

        #########################
        #### SUPPORT METHODS ####
        #########################


    def getAlarmListFromCli(self, cli_input='"show ManagedElement=1, SystemFunctions=1, Fm=1" "exit"', cli_expected_output=[], \
                            cli_nonexpected_output=['closed connection', 'Connection to COM failed']):

        cmd_cli = '%s %s' % (self.cli_active_controller_login_params, cli_input)
        result = self.comsa_lib.executeCliSession(cmd_cli)
        self.fail(result[0], result[1])
        cli_output_lines = result[1].splitlines()
        self.comsa_lib.debug_logger_line_by_line(cli_output_lines)

        # Compare cli output to the expected output
        self.myLogger.debug('Checking CLI output')
        if cli_expected_output == []:
            cli_expected_output.append(cli_input.split('"')[1].strip())
        result = self.comsa_lib.check_CLI_output(cli_output_lines, cli_expected_output, cli_nonexpected_output)
        self.fail(result[0], result[1])

        activeAlarms = []
        for line in cli_output_lines:
            if 'FmAlarm=' in line:
                activeAlarms.append(line.strip())

        return activeAlarms

    def showAlarmFromCli(self, alarmId, cli_input='"show ManagedElement=1, SystemFunctions=1, Fm=1" "exit"', cli_expected_output=[], \
                         cli_nonexpected_output=['closed connection', 'Connection to COM failed']):

        cli_input = cli_input.split('"')[1].strip() + ', %s' % alarmId
        cli_input = '"%s" "exit"' % cli_input
        cmd_cli = '%s %s' % (self.cli_active_controller_login_params, cli_input)
        result = self.comsa_lib.executeCliSession(cmd_cli)
        self.fail(result[0], result[1])
        cli_output_lines = result[1].splitlines()
        self.comsa_lib.debug_logger_line_by_line(cli_output_lines)

        # Compare cli output to the expected output
        self.myLogger.debug('Checking CLI output')
        result = self.comsa_lib.check_CLI_output(cli_output_lines, cli_expected_output, cli_nonexpected_output)
        self.fail(result[0], result[1])


    def restartCom(self):
        self.setTestStep('Restarting COM')
        result = self.comsa_lib.comRestart(self, self.activeController[0], self.activeController[1], self.memoryCheck)
        self.fail(result[0], result[1])

    def createMeasurementJob (self, jobName, pmGroup, measurementReaders, measTypes, granularityPeriod, reportingPeriod, jobPriority, reportContentGeneration):
        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)
        strCmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, Pm=1, PmJob=%s"' %(self.cli_active_controller_login_params, jobName)
        self.myLogger.debug('Configure to create PmJob %s' %jobName)
        strCmd += ' "jobType=MEASUREMENTJOB" "requestedJobState=STOPPED" "granularityPeriod=%s" "reportingPeriod=%s" "jobPriority=%s" "reportContentGeneration=%s"' %(\
                    granularityPeriod, reportingPeriod, jobPriority, reportContentGeneration)
        it = iter(measTypes)
        for ref in measurementReaders:
            measRef = 'ManagedElement=1,SystemFunctions=1,Pm=1,PmGroup=%s,MeasurementType=%s' %(pmGroup,it.next())
            strCmd += ' "MeasurementReader=%s" "measurementSpecification" "measurementTypeRef=\\\"%s\\\"" "up" "up"' %(ref, measRef)
        strCmd += ' "commit"'
        result = self.comsa_lib.executeCliSession(strCmd)
        self.fail(result[0], result[1])
        if 'ERROR' in result[1]:
            self.fail('ERROR', result[1])

    def deleteMeasurementJob(self, jobName):
        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)
        strCmd = '%s "configure" "no ManagedElement=1, SystemFunctions=1, Pm=1, PmJob=%s" "commit"' %(self.cli_active_controller_login_params, jobName)
        result = self.comsa_lib.executeCliSession(strCmd)
        self.fail(result[0], result[1])
        if 'ERROR' in result[1]:
            self.fail('ERROR',result[1])
        self.myLogger.debug('Job has deleted successfully')

    def changeStateJob(self, jobName, state):
        #State should be "ACTIVE or STOPPED"
        self.cli_active_controller_login_params = self.comsa_lib.create_active_controller_login_params(\
                    self.activeController, self.testConfig, self.targetData, self.pathToConfigFiles, self.cli_tester_script)
        strCmd = '%s "configure" "ManagedElement=1, SystemFunctions=1, Pm=1, PmJob=%s" "requestedJobState=%s" "commit"' %(\
                    self.cli_active_controller_login_params, jobName, state)
        result = self.comsa_lib.executeCliSession(strCmd)
        self.fail(result[0], result[1])
        if 'ERROR' in result[1]:
            self.fail('ERROR',result[1])
        self.myLogger.debug('Job has %s successful' %state)

    def parseAndVerifyXmlReportFile(self, root, pattern):
        #Get measInfoNode
        measInfoChildNode = None
        measTypeList = []
        measValueList = []
        measTypeDict = {}

        #Find measInfo tag
        for node in root:
            if 'measInfo' in node.tag:
                self.myLogger.debug('Standing at %s element' %node.tag)
                measInfoChildNode = node
            else:
                continue

        if measInfoChildNode != None:
            for node in measInfoChildNode:
                if 'measValue' in node.tag:
                    #Go here measValue to get value counter
                    for valueTag in node:
                        measValueList.append(valueTag.text)
                elif 'measType' in node.tag:
                    measTypeList.append(node.text)
                else:
                    continue
        else:
            return ('SUCCESS', 'empty report files')

        #Update measType and measValue into dictionary
        it = iter(measValueList)
        for obj in measTypeList:
            measTypeDict[obj] = it.next()
        self.myLogger.debug('[measType : measValue]: %s' %measTypeDict)

        #Compare values in report file
        for obj in measTypeList:
            if measTypeDict[obj] != pattern[obj]:
               return ('ERROR', "Data value is reported incorrectly")

        return ('SUCCESS', '')

    def checkPmMeasFilesReportedByCom (self, pattern, reportDir='/storage/no-backup/com-apr9010443/PerformanceManagementReportFiles/'):
        cmd = 'ls %s*.xml' %reportDir
        result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
        self.fail(result[0], result[1])

        xmlfiles = result[1].split()
        self.myLogger.debug('Start parsing and verifying the xml report file')
        for file in xmlfiles:
            self.myLogger.debug('Report file: %s' %file)
            cmd = 'cat %s' %file
            result = self.sshLib.sendCommand(cmd, self.activeController[0], self.activeController[1])
            self.fail(result[0], result[1])
            outputfile = result[1]
            root = ET.fromstring(outputfile)
            self.myLogger.debug('Standing at %s as root element' %root.tag)
            #Find the measInfo tag
            for child in root:
                if 'measData' in child.tag:
                    result = self.parseAndVerifyXmlReportFile(child, pattern)
                    self.fail(result[0], result[1])
                else:
                    continue
        if 'empty' in result[1]:
            return ('ERROR', 'No counter is updated in report files')
        return result

    def parseStringsToList(self, str):
        #Ignore extra characters in list
        str = str.replace(' ', '')
        str = str.strip('[]\'')
        return str.split('\',\'')


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
