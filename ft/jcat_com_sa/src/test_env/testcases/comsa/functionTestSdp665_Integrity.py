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

    Tag: TC-FT665-002

    Id:
    ""
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
import copy
import os
from java.lang import System


class FT665_Integrity(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']

        self.comsaArea = ''
        self.comsaRepository = ''
        self.comsaBackup = ''
        self.reqCmwRelease = '1'
        self.reqCmwVersion = 'R7A10'
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        # parameters from the config files


    def id(self):
        return self.name


    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)

        self.modelFileList = dict.get("COM_MODEL_FILE_LIST")
        self.PERSISTENT_STORAGE_API = dict.get("PERSISTENT_STORAGE_API")
        coreTestCase.CoreTestCase.setUp(self)

        PERSISTENT_STORAGE_API_CONFIG="%s/config" %self.PERSISTENT_STORAGE_API
        PERSISTENT_STORAGE_API_SOFTWARE="%s/software" %self.PERSISTENT_STORAGE_API
        PERSISTENT_STORAGE_API_CLEAR="%s/clear" %self.PERSISTENT_STORAGE_API
        PERSISTENT_STORAGE_API_NO_BACKUP="%s/no-backup" %self.PERSISTENT_STORAGE_API
        self.getClearLocationCmd = 'cat %s' %PERSISTENT_STORAGE_API_CLEAR
        self.getConfigLocationCmd = 'cat %s' %PERSISTENT_STORAGE_API_CONFIG
        self.getNoBackupLocationCmd = 'cat %s' %PERSISTENT_STORAGE_API_NO_BACKUP
        self.getSfotwareLocationCmd = 'cat %s' %PERSISTENT_STORAGE_API_SOFTWARE
        self.comsaDirUnderPso = 'comsa_for_coremw-apr9010555'
        self.comModelConfigFileName = 'com-model.config'

        # Stress Tool option
        self.installStressTool = eval(System.getProperty("runStressTool"))

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        if self.installStressTool:
            self.setTestStep('======== Install the stress tool ========')
            self.comsa_lib.installStressToolOnTarget(self)
            self.setTestStep('======== Start the stress tool ========')

            # Determine the number of processor cores in the node
            result = self.comsa_lib.getNumOfCPUsOnNode(self)
            self.fail(result[0],result[1])
            numOfCpuCores = result[1];
            self.myLogger.debug('Found %s CPU cores' %numOfCpuCores)

            # Determine the total physical RAM in the node
            result = self.comsa_lib.getBytesOfRamOnNode(self)
            self.fail(result[0],result[1])
            totalRamBytes = result[1];
            tenPercentOfTotalRam = int(totalRamBytes) // 10
            self.myLogger.debug('Found total %s bytes of RAM, 10 percent is %s' %(totalRamBytes, tenPercentOfTotalRam))

            # set the stress tool to occupy all CPU cores and 90% of the physical RAM
            # 2 local disk tasks writing 4 MB, NFS disk stress 1 task writing 64K bytes
            result = self.comsa_lib.startStressToolOnTarget(self, numOfCpuCores, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            # No CPU, only local and NFS disk
            #result = self.comsa_lib.startStressToolOnTarget(self, 0, 0, 9, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            # 50% CPU, 50% memory plus local and NFS disk stress
            #result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 2, 4194304, 1, 65536)

            # 50% CPU, 50% memory plus NFS disk stress
            #result = self.comsa_lib.startStressToolOnTarget(self, 1, 0, 5, tenPercentOfTotalRam, 60*60*60, 0, 0, 1, 65536)

        """
         Starting with CoreMW 3.3 Sh9 Core MW delivers its own models through MDF.
         The effect is that the model file list provided by COM SA is not used.
         For testing with Core MW 3.3 Sh9 or later, the models delivered by COM SA will be ignored.
        """
        CoreMwModelsDeliveredByCoreMw = self.lib.checkComponentVersion('cmw', self.reqCmwRelease, self.reqCmwVersion )[1]


        self.setTestStep('### check if PSO is running on the cluster ###')
        result = self.comsa_lib.checkPso()
        self.fail(result[0],result[1])
        if result[1] == False:
            self.myLogger.info('The test system does not have PSO.')
            self.comsaArea = '/home/comsa'
            self.comsaRepository = '/home/comsa/repository'
            self.coreMwRepository = '/home/coremw/repository'
            self.comsaBackup = '/home/comsa/backup'
            self.modelFileList = '/cluster/home/com/etc/model/model_file_list.cfg'
            self.origModelFileList = '/cluster/home/com/etc/model/model_file_list.cfg.orig'
        elif result[1] == True:
            self.myLogger.info('The test system has PSO.')
            self.setTestStep('# Getting the PSO locations')
            # Getting the clear location:
            result = self.sshLib.sendCommand(self.getClearLocationCmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            clearLocation = result[1]
            self.comsaArea = '%s/%s' %(clearLocation, self.comsaDirUnderPso)

            # Getting the software location:
            result = self.sshLib.sendCommand(self.getSfotwareLocationCmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            softwareLocation = result[1]
            self.coreMwRepository = '%s/coremw/repository' %softwareLocation

            # Getting the no-backup location:
            result = self.sshLib.sendCommand(self.getNoBackupLocationCmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            noBackupLocation = result[1]
            self.comsaBackup = '%s/%s/backup' %(noBackupLocation, self.comsaDirUnderPso)

            # Getting the config location
            result = self.sshLib.sendCommand(self.getConfigLocationCmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.fail('ERROR', result[1])
            configLocation = result[1]
            self.modelFileList='%s/com-apr9010443/etc/model/model_file_list.cfg' %result[1]
            self.origModelFileList='%s/com-apr9010443/etc/model/model_file_list.cfg.orig' %result[1]
            self.comsaRepository = '%s/%s/repository' %(configLocation, self.comsaDirUnderPso)
        else:
            self.fail('ERROR', 'Unknown response from the checkPso function. Expected either True or False. Received: %s' %str(result[1]))


        self.setTestStep('### Check the existence of the COM SA directories')
        cmd = 'ls %s' %self.comsaArea
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0],result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', '%s not found on the target system.' %self.comsaArea)

        cmd = 'ls %s' %self.comsaRepository
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0],result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', '%s not found on the target system.' %self.comsaRepository)

        cmd = 'ls %s' %self.comsaBackup
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0],result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', '%s not found on the target system.' %self.comsaBackup)


        self.setTestStep('### check Installed SDPs except LOTC, COREMW and COM and see if they are in place... ###')
        if CoreMwModelsDeliveredByCoreMw == False:
            cmd = """cmw-repository-list | grep -v '\-COREMW\_' | grep -iv lotc | grep -v '\-COM\-' | grep -v NotUsed | awk '{print $1}'"""
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            sdpList = result[1].splitlines()
            if len(sdpList) == 0:
                self.fail('ERROR', 'No SDP found with cmw-repository-list not considering LOTC, CoreMW or COM')
        elif CoreMwModelsDeliveredByCoreMw == True:
            cmd = """cmw-repository-list | grep -v '\-COREMW\_' | grep -iv lotc | grep -v '\-COM\-' | grep -iv comsa | grep -v NotUsed | awk '{print $1}'"""
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            sdpList = result[1].splitlines()
        else:
            self.fail('ERROR', 'Variable CoreMwModelsDeliveredByCoreMw should be either True or False. It was %s' %CoreMwModelsDeliveredByCoreMw)

        coreMwSdpsWithComModels = []
        expectedModelsInComModelFileList = []
        for sdp in sdpList:
            cmd = 'ls %s/%s/%s' %(self.coreMwRepository, sdp, self.comModelConfigFileName)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            if 'No such file or directory' in result[1]:
                self.logger.info('The SDP %s does not contain any COM model. It is expected that this SDP will not be listed in the COM SA repository' %sdp)
            else:
                coreMwSdpsWithComModels.append(sdp)
                cmd = 'cat %s/%s/%s' %(self.coreMwRepository, sdp, self.comModelConfigFileName)
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                modelFiles = result[1].splitlines()
                if len(modelFiles) == 0:
                    self.fail('ERROR', 'There is no model file listed in the com-model.cfg file in SDP %s' %sdp)
                for modelFile in modelFiles:
                    expectedModelsInComModelFileList.append('%s/%s/%s' %(self.comsaRepository, sdp, modelFile.split('/')[1]))
        if CoreMwModelsDeliveredByCoreMw == False:
            if len(coreMwSdpsWithComModels) == 0:
                self.fail('ERROR', 'No SDP found with cmw-repository-list not considering LOTC, CoreMW or COM that has a COM model')


        self.setTestStep('# Listing SDPs under comsa Repository')
        # Listing SDPs under clearLocation/comsa.../mim-files
        if CoreMwModelsDeliveredByCoreMw == False:
            cmd = 'ls %s | grep ^ERIC' %(self.comsaRepository)
        else:
            cmd = 'ls %s | grep ^ERIC | grep -iv comsa' %(self.comsaRepository)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0],result[1])
        sdpListComSa = result[1].split()
        if len(sdpListComSa) == 0 and CoreMwModelsDeliveredByCoreMw == False:
            self.fail('ERROR', 'No SDP found in COM SA software repository!')
        if len(coreMwSdpsWithComModels) != len(sdpListComSa):
            self.fail('ERROR', 'The number of SDPs found with cmw-repository-list not considering LOTC, CoreMW or COM does not match the number of SDPs under the clear location.')

        copyOfSdpListComSa = copy.deepcopy(sdpListComSa)
        for sdp in coreMwSdpsWithComModels:
            for sdpClear in sdpListComSa:
                if sdp == sdpClear:
                    copyOfSdpListComSa.pop(copyOfSdpListComSa.index(sdp))

        if len(copyOfSdpListComSa) != 0:
            self.fail('ERROR', 'There is not a one-to-one match between the list of SDPs provided by cmw-repository-list and those listed in the clear location. \
            SDPs found with cmw-repository list: %s. SDPs under clear location: %s. ' %(str(coreMwSdpsWithComModels), str(sdpListComSa)))


        self.setTestStep('### For each SDP found check the matching between the com-model.config and the list of MOM files under the SDP directory ###')
        # Checking the content of the COM model file list
        cmd = 'cat %s' %(self.modelFileList)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0],result[1])
        modelFileListContent = result[1]


        for sdp in coreMwSdpsWithComModels:
            self.setTestStep('# We check SDP %s if all files in the com-model.config file are in place' %sdp)
            cmd = 'cat %s/%s/%s' %(self.comsaRepository, sdp, self.comModelConfigFileName)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            momFiles = result[1].splitlines()

            cmd = 'ls %s/%s/models' %(self.coreMwRepository, sdp)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            cmwModelFiles = result[1]


            # First we check if all files in the com-model.config file are in place
            cmd = 'ls %s/%s/ | grep -v com-model.config' %(self.comsaRepository, sdp)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0],result[1])
            for file in momFiles:
                if file not in result[1]:
                    self.fail('ERROR', '%s not found under %s/%s/' %(file, self.comsaRepository, sdp))
                if '%s/%s/%s' %(self.comsaRepository, sdp, file) not in modelFileListContent:
                    self.fail('ERROR', '%s not listed in COM model file list file %s' %(file, self.modelFileList))
                if file not in cmwModelFiles:
                    self.fail('ERROR', '%s not under %s/%s/models' %(file, self.coreMwRepository, sdp))


        # Here we check if the expected model files found in the Core MW repository do end up in the com model list file and in the COM SA repository
        self.setTestStep('Check if the expected model files found in the Core MW repository do end up in the com model list file and in the COM SA repository')
        modelFilesNotInComModelFileList = []
        for modelFile in expectedModelsInComModelFileList:
            if modelFile not in modelFileListContent:
                modelFilesNotInComModelFileList.append(modelFile)

        if len(modelFilesNotInComModelFileList) != 0:
            self.fail('ERROR', 'The following expected model files were not found in the COM model file list: %s' %str(modelFilesNotInComModelFileList))

        modelFileListFiles = modelFileListContent.splitlines()
        for modelFileListFile in modelFileListFiles:
            if self.comsaDirUnderPso in modelFileListFile:
                cmd = 'ls %s' %modelFileListFile
                result = self.sshLib.sendCommand(cmd)
                self.fail(result[0],result[1])
                if 'No such file or directory' in result[1]:
                    self.fail('ERROR', 'The following model file is listed in the COM model file list, but the file does not exist in the COM SA repository: %s' %modelFileListFile)

        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")


    def tearDown(self):
        self.setTestStep('tearDown')

        if self.installStressTool:
            self.setTestStep('======== Stopping the stress tool on target ========')
            self.comsa_lib.stopStressToolOnTarget(self)

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')


def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
