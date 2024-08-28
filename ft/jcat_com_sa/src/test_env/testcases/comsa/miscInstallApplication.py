#!/vobs/tsp_saf/tools/Python/linux/bin/python
#coding=iso-8859-1
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
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
import time
import os

class InstallApplication(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']

        # parameters from the config files
        self.rtSdpName = 'JAVACAF_x86_64-CXP9013050_4.sdp'
        self.generateCampaign = 'True'
        self.generateCampaignFile = 'generatecampaign'
        self.generateCampaignArguments = 'generate'
        self.installationCampaignTemplate = 'ERIC-JAVACAF-I-TEMPLATE-CXP9013050_4-R1A03.sdp'
        self.installationSdpName = ''
        self.backupName = 'beforeApplication'
        self.createBackup = 'False'
        self.isStandardComSaBackup = 'True'
        self.pathOnTargetSystem = '/home/coremw/incoming/'
        self.maxInstallationTime = '900'
        self.restoreSystem = 'False'
        self.campExpectedToFail = 'False'
        self.serchPatternSyslog1 = ''
        self.rtSdpPath = ''
        self.deplSdpPath = ''


    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        #self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")
        #self.pathToModelFiles = dict.get("FT763_MODELFILE_PATH")
        self.rtSdpPathInRepository = '%s%s' %(self.COMSA_VERIF_PATH, dict.get(self.rtSdpPath))
        self.deplSdpPathInRepository = '%s%s' %(self.COMSA_VERIF_PATH, dict.get(self.deplSdpPath))


        coreTestCase.CoreTestCase.setUp(self)

        self.generateCampaign = eval(self.generateCampaign)
        self.createBackup = eval(self.createBackup)
        self.restoreSystem = eval(self.restoreSystem)
        self.campExpectedToFail = eval(self.campExpectedToFail)

        if self.createBackup == True:
            self.backupSystem()


        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        self.setTestStep('Upload installation files to the target system')
        result = self.sshLib.sendCommand('mkdir -p %s' %self.pathOnTargetSystem)
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('\\rm -rf %s/*' %self.pathOnTargetSystem)
        self.fail(result[0], result[1])

        result = self.sshLib.remoteCopy('%s/%s' %(self.rtSdpPathInRepository, self.rtSdpName), self.pathOnTargetSystem)
        self.fail(result[0], result[1])

        if self.generateCampaign == True:
            result = self.sshLib.remoteCopy('%s/%s' %(self.deplSdpPathInRepository, self.generateCampaignFile), self.pathOnTargetSystem)
            self.fail(result[0], result[1])
            result = self.sshLib.remoteCopy('%s/%s' %(self.deplSdpPathInRepository, self.installationCampaignTemplate), self.pathOnTargetSystem)
            self.fail(result[0], result[1])
            cmd = 'chmod +x %s/%s' %(self.pathOnTargetSystem, self.generateCampaignFile)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])
        else:
            result = self.sshLib.remoteCopy('%s/%s' %(self.deplSdpPathInRepository, self.installationSdpName), self.pathOnTargetSystem)
            self.fail(result[0], result[1])


        self.setTestStep('Generate campaign')
        numberOfControllers = len(self.testConfig['controllers'])
        numberOfPayoads = len(self.testConfig['payloads'])

        if numberOfControllers == 2:
            cmd = "bash -c 'pushd %s ;  ./%s %s %s PL=%d ; popd'" %(self.pathOnTargetSystem, self.generateCampaignFile, \
                            self.generateCampaignArguments, self.installationCampaignTemplate, numberOfPayoads)
        elif numberOfControllers != 0:
            cmd = "bash -c 'pushd %s ;  ./%s %s %s SC=%d PL=%d ; popd'" %(self.pathOnTargetSystem, self.generateCampaignFile, \
                            self.generateCampaignArguments, self.installationCampaignTemplate, numberOfControllers, numberOfPayoads)
        else:
            self.fail('ERROR', 'Number of controllers returned by testConfig is 0')
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        sdpLine = ''
        lines = result[1].splitlines()
        for line in lines:
            if 'Generating' in line:
                sdpLine = line
                break
        if sdpLine != '':
            self.installationSdpName = sdpLine.split()[1][1:-1]
        else:
            self.fail('ERROR', 'Installation SDP name not generated properly. Name length is zero')


        self.setTestStep('Import SDPs')

        result = self.safLib.importSwBundle('%s' %self.rtSdpName)
        self.fail(result[0], result[1])
        result = self.safLib.importSwBundle('%s' %self.installationSdpName)
        self.fail(result[0], result[1])


        self.setTestStep('Start installation campaign')

        cmd = 'date +\%s'
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])
        startTime = int(result[1])

        campaignName = self.installationSdpName.split('.')[0]
        result = self.safLib.upgradeStart(campaignName)
        self.fail(result[0], result[1])


        self.setTestStep('Monitor status of installation campaign')
        startTimeCamp = int(time.time())
        endTime = startTimeCamp + int(self.maxInstallationTime)

        campaignStatus = ''
        while time.time() < endTime:
            result = self.safLib.upgradeStatusCheck(campaignName)
            if self.campExpectedToFail==False:
                self.logger.info('We are in the self.campExpectedToFail==False branch')
                self.fail(result[0], result[1])
                cmdResult = result[1].splitlines()
                if len(cmdResult) != 1:
                    self.restoreSystem = True
                    self.fail('ERROR', 'Expected a response to the campaign status check that is exactly one line. Received: %s' %result[1])
                cmdResult = cmdResult[0].split('=')
                if len(cmdResult) != 2:
                    self.restoreSystem = True
                    self.fail('ERROR', 'Expected a response to the campaign status that has only one "=" sign in it. Received: %s' %cmdResult)
                elif cmdResult[0] != campaignName:
                    self.restoreSystem = True
                    self.fail('ERROR', 'Expected the campaign name to be on the left side of the "=" sign. Received: %s' %cmdResult[0])
                campaignStatus = cmdResult[1]
                if campaignStatus == 'COMPLETED':
                    break
                elif '=FAILED' in result[1]:
                    #self.restoreSystem = True
                    self.logger.info('The campaign failed. Exact status is: %s' %result[1])
                    break
                else:
                    self.miscLib.waitTime(10)
            elif self.campExpectedToFail==True:
                self.logger.info('We are in the self.campExpectedToFail==True branch')
                cmdResult = result[1].splitlines()
                if '=FAILED' in result[1]:
                    #self.restoreSystem = True
                    self.logger.info('The campaign failed. Exact status is: %s' %result[1])
                    break
                cmdResult = cmdResult[0].split('=')
                if len(cmdResult) != 2:
                    #self.restoreSystem = True
                    self.fail('ERROR', 'Expected a response to the campaign status that has only one "=" sign in it. Received: %s' %cmdResult)
                elif cmdResult[0] != campaignName:
                    self.restoreSystem = True
                    self.fail('ERROR', 'Expected the campaign name to be on the left side of the "=" sign. Received: %s' %cmdResult[0])
                campaignStatus = cmdResult[1]
                if campaignStatus == 'COMPLETED':
                    break
                else:
                    self.miscLib.waitTime(10)
            else:
                self.fail('ERROR', 'The self.campExpectedToFail has to be either True or False. Instead it is: %s' %self.campExpectedToFail)

        if self.campExpectedToFail==False:
            self.logger.info('After the campaign finished we are in the self.campExpectedToFail==False branch')
            if campaignStatus != 'COMPLETED':
                self.restoreSystem = True
                self.fail('ERROR', 'Campaign status is not COMPLETED %s seconds after start. Status is: %s' %(self.maxInstallationTime, campaignStatus))


            self.setTestStep('Commit campaign')
            result = self.safLib.upgradeCommit(campaignName)
            self.fail(result[0], result[1])


            self.setTestStep('Remove installation campaign')
            result = self.safLib.removeSwBundle(campaignName)
            self.fail(result[0], result[1])

            self.setTestStep('Save IMM')
            result = self.safLib.saveImmdata()
        else:
            self.logger.info('After the campaign finished we are in the self.campExpectedToFail==True branch')
            failures = []
            if self.serchPatternSyslog1 != '':
                match = []
                for controller in self.testConfig['controllers']:
                    result = self.lib.getEventTimestampFromSyslog(controller[0], controller[1], eval(self.serchPatternSyslog1), startTime, self.testConfig)
                    if result[0] == 'SUCCESS':
                        match.append(result[1])
                        self.myLogger.info('Match found in syslog at UNIX time: %s' %result[1])
                if len(match) == 0:
                    failures.append('No match found in the syslog for the following search pattern: %s' %eval(self.serchPatternSyslog1))

            result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
            if result[0] != 'SUCCESS':
                failures.append('restoreSystem failed. %s' %result[1])

            if len(failures) != 0:
                self.restoreSystem = True
                self.fail('ERROR', 'The following issues happened during runTest restore. %s' %str(failures))
            comment = """if (result[0] != 'SUCCESS') or ('Status OK' not in result[1]):
                self.restoreSystem = True"""


        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")



    def tearDown(self):
        self.setTestStep('tearDown')

        failures = []
        if self.restoreSystem == True:
            result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes, removeBackup = False)
            if result[0] != 'SUCCESS':
                failures.append('ERROR', 'backupRestore failed. %s' %result[1])

        self.setTestStep('Remove installation files from the target system')
        result = self.sshLib.sendCommand('\\rm -f %s/%s' %(self.pathOnTargetSystem, self.rtSdpName))
        if result[0] != 'SUCCESS':
            failures.append('ERROR', 'Remove rtSdpName from the target system failed. %s' %result[1])
        result = self.sshLib.sendCommand('\\rm -f %s/%s' %(self.pathOnTargetSystem, self.installationSdpName))
        if result[0] != 'SUCCESS':
            failures.append('ERROR', 'Remove installationSdpName from the target system failed. %s' %result[1])

        if self.generateCampaign == True:
            result = self.sshLib.sendCommand('\\rm -f %s/%s' %(self.pathOnTargetSystem, self.generateCampaignFile))
            if result[0] != 'SUCCESS':
                failures.append('ERROR', 'Remove  generateCampaignFile from the target system failed. %s' %result[1])
            result = self.sshLib.sendCommand('\\rm -f %s/%s' %(self.pathOnTargetSystem, self.installationCampaignTemplate))
            if result[0] != 'SUCCESS':
                failures.append('ERROR', 'Remove installationCampaignTemplate from the target system failed. %s' %result[1])

        if len(failures) != 0:
            self.fail('ERROR', 'The following issues happened during tearDown. %s' %str(failures))

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')


    def backupSystem(self):
        # Skip creating the backup if there is a safe backup created at the beginning of the test suite
        self.setTestStep('Create backup before installation')
        self.myLogger.debug('enter backupSystem')
        backupFound = False
        if eval(self.isStandardComSaBackup) and self.testSuiteConfig.has_key('restoreBackup'):
            result = self.safLib.isBackup(self.testSuiteConfig['restoreBackup'])
            if result == ('SUCCESS', 'EXIST'):
                self.backupName = self.testSuiteConfig['restoreBackup']
                backupFound = True
        if backupFound == False:
            result = self.safLib.isBackup(self.backupName)
            self.fail(result[0], result[1])
            if result != ('SUCCESS','NOT EXIST'):
                result = self.safLib.backupRemove(self.backupName)
                self.fail(result[0], result[1])
            result = self.comsa_lib.backupCreateWrapper(self.backupName, backupRpms = self.backupRpmScript)
            if result[0] != 'SUCCESS' and self.linuxDistro == self.distroTypes[1]:
                self.myLogger.warn('Could not create backup on RHEL system. This is not a critical fault')
            else:
                self.fail(result[0], result[1])
        self.myLogger.debug('leave backupSystem')

def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
