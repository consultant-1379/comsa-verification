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

    Tag: ReinstallationOfCmwComComsa

    Id:  TC-MISC-012

    Help:
    The script requires the following files (and formats):
    CORE MW: the runtime tar file (example for Core MW 3.0 CP1: 19010-CXP9020355_1_X_Y_TAR.tar)
    COM: the runtime sdp and the installation sdp
    COM-SA: the runtime sdp and the installation sdp

    First you have to decide where you want to put the files required for the installation. In the IT Hub under /home/jenkinuser/release/install/ there are 9 directories called '1', '2', ... '9'.
    Chose one of these directories, but make sure that there is no clash with other team-members. Inside the chosen direcotry there are 3 directories: coremw, com and comsa.
    Copy the SW files into their respective directory.

    Run the re-installation script with the following command:
    executive.py --config <targetName> --pl <number of payloads in the test cluster> --productSettings comsa --runSingleTestCase TC-MISC-012 --swDirNumber <the chosen directory number between 1 and 9> ...(plus other options you would like to add)

    Example:
    executive.py --config vbox_target_11 --pl 0 --productSettings comsa --runSingleTestCase TC-MISC-012 --suc False --rtc False --tdc False --swDirNumber 2

    If you do not specify the swDirNumber than the default number will be used, that is '1'.
    ""
    ==================================

"""

import test_env.fw.coreTestCase as coreTestCase
from se.ericsson.jcat.fw import SUTHolder
import re
import os



from java.lang import System

class AutoInstallationOfCmwComComsa(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)

        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.uninstallScriptLocation = dict.get("JENKINUSER_R_INSTALL")
        self.distroTypes = eval(dict.get("LINUX_DISTRO_TYPES"))
        result = self.lib.updateLinuxDistroInDictionary(self.testSuiteConfig, self.distroTypes)
        self.fail(result[0], result[1])
        self.linuxDistro = self.testSuiteConfig['linuxDistro']['value']
        backupRpmScriptLocal = "%s%s%s" %(os.environ['MY_REPOSITORY'], dict.get("PATH_TO_CONFIG_FILES"), dict.get("BACKUP_RPMS_SCRIPT"))
        self.backupRpmScript = "/home/%s" % dict.get("BACKUP_RPMS_SCRIPT")
        # copy backup rpms script to cluster
        result = self.sshLib.remoteCopy(backupRpmScriptLocal, '/home/', timeout = 60)
        self.fail(result[0], result[1])
        cmd = 'chmod +x %s' % self.backupRpmScript
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.super__setUp()
        self.sutholder = SUTHolder.getInstance()
        self.currentSut = self.sutholder.zones[0]
        self.TargetDataLib = self.currentSut.getLibrary("TargetDataLib")
        self.targetData = self.TargetDataLib.getTargetData()
        self.myLogger.info('Exit setUp')

    def runTest(self):

        self.setTestStep('runTest')

        self.swDir = System.getProperty("swDirNumber")
        localPathToSw = '%s%s/' %(self.uninstallScriptLocation, self.swDir)
        if self.linuxDistro == self.distroTypes[1]: # rhel
            uninstallScriptName = 'uninstall_rhel'
        else:
            uninstallScriptName = 'uninstall_all'

        pathToCmwInstallation = '/home/release/autoinstall/cmw/' # Creating a directory for cmw
        pathToComInstallation = '/home/release/autoinstall/com/' # Creating a directory for com
        pathToComSaInstallation = '/home/release/autoinstall/comsa/' # Creating a directory for com

        sdpImportCommand = 'cmw-sdp-import'
        listCampaignCommand = 'cmw-repository-list --campaign'


        # CORE MW installation


        self.setTestStep('======== Installation of CMW =========')


        self.setTestStep('Creating a Directory at target and Copying a file at target for Un-installation of CMW.')

        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToCmwInstallation)
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('mkdir -p %s' %pathToCmwInstallation)
        self.fail(result[0], result[1])

        result = self.sshLib.remoteCopy('%s%s' %(self.uninstallScriptLocation, uninstallScriptName), pathToCmwInstallation, timeout = 120,numberOfRetries = 5)
        self.fail(result[0], result[1])

        self.setTestStep('Run uninstall script')

        cmw_uninstall_command = 'chmod u+x %s%s' %(pathToCmwInstallation, uninstallScriptName)
        result = self.sshLib.sendCommand (cmw_uninstall_command) # works on the target
        cmw_uninstall_command = '%s%s' %(pathToCmwInstallation, uninstallScriptName)
        result = self.sshLib.sendCommand (cmw_uninstall_command) # works on the target
        self.fail(result[0], result[1])
        if 'Error: All nodes not up, Exiting' in result[1]:
            self.fail('ERROR', 'Execution of uninstallation script failed. %s' %result[1])

        self.setTestStep('Reboot cluster')
        reboot_cluster = 'cluster reboot -a'
        result = self.sshLib.sendCommand (reboot_cluster)
        self.fail(result[0], result[1])

        result = self.comsa_lib.waitForClusterUnavailable(self.testConfig)
        self.fail(result[0], result[1])

        self.sshLib.tearDownHandles()

        self.miscLib.waitTime(180)

        for i in range(60):
            cmd = 'tipc-config -n'
            result = self.sshLib.sendCommand(cmd,2,1)
            self.myLogger.info('###tipc link status: %s' % result[1])
            ### This code is not working for 1-node clusters: len(self.testConfig['testNodesTypes']) - 1 is zero!
            if result[0] == 'SUCCESS' and result[1].count('up') == len(self.testConfig['testNodesTypes']) - 1 :
                break
            else:
                self.miscLib.waitTime(10)

        self.setTestStep('Run uninstall script again')
        result = self.sshLib.sendCommand (cmw_uninstall_command) # works on the target
        self.fail(result[0], result[1])
        if 'Error: All nodes not up, Exiting' in result[1]:
            self.fail('ERROR', 'Execution of uninstallation script failed. %s' %result[1])


        self.setTestStep('Copying of File(s) for CMW installation to the target.')

        cmd = 'ls %scoremw/*.tar*' %(localPathToSw)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'Core MW tar file not found at specified location: %scoremw/ .' %localPathToSw)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one Core MW tar file found at specified location: %scoremw/: %s.' %(localPathToSw, str(result[1])))

        name_list = result[1].strip()
        fileName = name_list.split('/')[len(name_list.split('/')) - 1]

        result = self.sshLib.remoteCopy(name_list, pathToCmwInstallation, timeout = 60,numberOfRetries = 5)
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('cd %s; tar xvf %s' %(pathToCmwInstallation, fileName))
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File not found: %s/%s.' %(pathToCmwInstallation, fileName))

        self.setTestStep('Installation of CMW ')
        cmw_install_command = 'chmod u+x %s/install' %pathToCmwInstallation
        result = self.sshLib.sendCommand (cmw_install_command)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File not found: %s/install.' %pathToCmwInstallation)

        self.logger.debug('Getting Default Time out')
        result = self.sshLib.getTimeout(2, 1)
        defTimeout = result[1]
        self.logger.debug('Setting Time Out to 3600 sec or one hour')
        self.sshLib.setTimeout(3600, 2, 1)

        cmw_install_command = 'cd %s; ./install' %pathToCmwInstallation
        expectedPrintout = "Install script completed successfully"
        result = self.sshLib.sendCommand(cmw_install_command)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'File not found: %s/install.' %pathToCmwInstallation)
        elif expectedPrintout not in result[1]:
            self.fail('ERROR', 'Expected printout "%s" not received. Installation log: %s' %(expectedPrintout, result[1]))
        self.logger.debug('Setting back the default time out : %s' %(defTimeout))
        self.sshLib.setTimeout(defTimeout, 2, 1)
        self.sshLib.tearDownHandles()

        self.setTestStep('Checking cmw-status ......')

        okFlag = False
        for i in range(5):
            result = self.safLib.checkClusterStatus()
                # Get the system status and displays only the failed components Wrapped command:
            if result == ('SUCCESS', 'Status OK'):
                self.myLogger.info(result[1])
                okFlag = True
                break
            else:
                self.logger.debug("status not ok waiting 30 seconds to re-check the status")
                self.miscLib.waitTime(30)
        if okFlag == False:
            self.fail('ERROR','Failed to install CMW')


        self.setTestStep('Creating a CMW-Backup')
        backupName = 'cmw_autobackup_%s'%self.swDir
        result = self.safLib.isBackup(backupName)
        self.fail(result[0], result[1])
        if result == ('SUCCESS','EXIST'):
            result = self.safLib.backupRemove(backupName)
            self.fail(result[0], result[1])
        result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])

        # Com Installation
        self.setTestStep('======== Installation of COM ========')
        self.setTestStep ('Creating a Directory for COM')
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])

        self.setTestStep('Copying the COM file(s) from source to destination !')

        cmd = 'ls %scom/COM-*.sdp' %(localPathToSw)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM runtime sdp file not found at specified location: %scom/ .' %localPathToSw)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM runtime sdp file found at specified location: %scom/: %s.' %(localPathToSw, str(result[1])))
        name_list = result[1].strip()
        result = self.sshLib.remoteCopy(name_list, pathToComInstallation, timeout = 60,numberOfRetries = 5)
        self.fail(result[0], result[1])

        cmd = 'ls %scom/ERIC-COM-I*.sdp' %(localPathToSw)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM campaign sdp file not found at specified location: %scom/ .' %localPathToSw)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM campaign sdp file found at specified location: %scom/: %s.' %(localPathToSw, str(result[1])))
        name_list = result[1].strip()
        self.logger.info('name_list: (%s)'%name_list)

        result = self.sshLib.remoteCopy(name_list, pathToComInstallation, timeout = 60,numberOfRetries = 5)
        self.fail(result[0], result[1])

        self.setTestStep ('cmw-sdp-import.........Start')

        cmd = '%s %s*.sdp' %(sdpImportCommand, pathToComInstallation)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.setTestStep ('COM-Campaign-Start')

        result = self.sshLib.sendCommand(listCampaignCommand)
        self.fail(result[0], result[1])
        self.logger.info('Result of %s:(%s)'%(listCampaignCommand, str(result[1])))
        campaignName = result[1]

        result = self.safLib.upgradeStart(campaignName)
        self.fail(result[0], result[1])
        self.logger.info('Result of campaign_start:(%s)'%str(result))

        # Checking that the campaign has completed (Initial, Executing, Completed) or not !
        self.setTestStep ('COM-Campaign-Status Check')

        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(campaignName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COM')

        result = self.safLib.upgradeCommit(campaignName)
        self.fail(result[0], result[1])

        self.setTestStep ('Remove campaign')

        result = self.safLib.removeSwBundle(campaignName)
        self.fail(result[0], result[1])

        self.setTestStep('Checking cmw-status for COM')

        result = self.safLib.checkClusterStatus()
        self.fail(result[0], result[1])

        self.setTestStep('Creating a COM-Backup !')

        backupName = 'com_autobackup_%s'%self.swDir
        result = self.safLib.isBackup(backupName)
        self.fail(result[0], result[1])
        if result == ('SUCCESS','EXIST'):
            result = self.safLib.backupRemove(backupName)
            self.fail(result[0], result[1])
        result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])

        #Com_SA Installation
        self.setTestStep('========Installation of COM_SA=======')
        self.setTestStep ('Creating a Directory for COM_SA')
        result = self.sshLib.sendCommand('\\rm -rf %s' %pathToComSaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])
        result = self.sshLib.sendCommand('mkdir -p %s' %pathToComSaInstallation) #def sendCommand(command, subrack=0, slot=0):
        self.fail(result[0], result[1])


        self.setTestStep('Copying a COMSA file from source to destination')

        cmd = 'ls %scomsa/*CXP*sdp' %(localPathToSw)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM SA runtime sdp file not found at specified location: %scom/ .' %localPathToSw)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM SA runtime sdp file found at specified location: %scomsa/: %s.' %(localPathToSw, str(result[1])))
        file_1 = result[1].strip()

        result = self.sshLib.remoteCopy(file_1, pathToComSaInstallation, timeout = 60,numberOfRetries = 5)
        self.fail(result[0], result[1])

        cmd = 'ls %scomsa/*install*sdp' %(localPathToSw)
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        if 'No such file or directory' in result[1]:
            self.fail('ERROR', 'COM SA runtime sdp file not found at specified location: %scom/ .' %localPathToSw)
        if len(result[1].splitlines()) > 1:
            self.fail('ERROR', 'More than one COM SA installation sdp file found at specified location: %scomsa/: %s.' %(localPathToSw, str(result[1])))
        file_2 = result[1].strip()

        result = self.sshLib.remoteCopy(file_2, pathToComSaInstallation, timeout = 60,numberOfRetries = 5)
        self.fail(result[0], result[1])

        self.setTestStep ('cmw-sdp-import.........Start')

        cmd = '%s %s*.sdp' %(sdpImportCommand, pathToComSaInstallation)
        result = self.sshLib.sendCommand(cmd)
        self.fail(result[0], result[1])

        self.setTestStep ('cmw-repository-list --campaign')

        result = self.sshLib.sendCommand(listCampaignCommand)
        self.fail(result[0], result[1])
        campaignName = result[1]

        self.setTestStep ('cmw-campaign-start')
        result = self.safLib.upgradeStart(campaignName)
        self.fail(result[0], result[1])
        self.logger.info('Result of campaign_start:(%s)'%str(result))

        self.setTestStep ('Check campaign status')
        okFlag = False
        for i in range(30):
            result = self.safLib.upgradeStatusCheck(campaignName)
            self.myLogger.info(result[1])
            if result[0] == 'SUCCESS' and re.search('COMPLETED',result[1]):
                okFlag = True
                break
            elif result[0] == 'ERROR':
                self.myLogger.info(result[1])
                self.fail(result[0],result[1])
                break
            else:
                self.miscLib.waitTime(20)
        if okFlag == False:
            self.fail('ERROR','failed to install COMSA')


        self.setTestStep ('cmw-campaign-commit')
        result = self.safLib.upgradeCommit(campaignName)
        self.fail(result[0], result[1])

        self.setTestStep ('cmw-campaign-remove')
        result = self.safLib.removeSwBundle(campaignName)
        self.fail(result[0], result[1])

        result = self.safLib.checkClusterStatus()
        self.fail(result[0], result[1])

        self.setTestStep('Creating a COMSA-Backup !')

        backupName = 'comsa_autobackup_%s'%self.swDir
        result = self.safLib.isBackup(backupName)
        self.fail(result[0], result[1])
        if result == ('SUCCESS','EXIST'):
            result = self.safLib.backupRemove(backupName)
            self.fail(result[0], result[1])
        result = self.comsa_lib.backupCreateWrapper(backupName, backupRpms = self.backupRpmScript)
        self.fail(result[0], result[1])

        coreTestCase.CoreTestCase.runTest(self)


    def tearDown(self):
        self.setTestStep('tearDown')

        command = '\\rm -rf /home/release/autoinstall'
        self.sshLib.sendCommand(command)
        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
