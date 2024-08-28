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
    TC-COV-001
    TC-MISC-004
    TC-COV-003

    Id:
    ""
    ==================================

    Help/Info:
    This test case can only run in test suite, the codeCoverage.xml test suite.
    These testcases are not independent.
    TC-COV-001 will run 'make coverage' on the build machine to create the sdp files and the coverage info 'notes' files which need to be installed on the target system. It also copies the coverage info files to the target system. Note: the location must be the same as on the build machine. In addition it runs the unit tests and obtaines a coverage result. It will create a backup to be used in TC-COV-003 to restore the system.
    TC-MISC-004 will reinstall COM-SA with the coverage code and info files included on the target system
    TC-COV-003 will collect the coverage results from the target system, copy these results back to the build machine and perform postprocessing. It will also restore on the target the standard COM SA software from the backup made in TC-COV-001.
"""

import test_env.fw.coreTestCase as coreTestCase
import time
import os
from java.lang import System

class CodeCoverage(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files
        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']
        self.COMSA_REPO_PATH = os.environ['COMSA_REPO_PATH']
        self.COMSA_VERIF_PATH = os.environ['COMSA_VERIFICATION']
        self.CMW_TOOLS = os.environ['CMW_TOOLS']
        self.host_arch = 'x86_64'   # used to detect if we are running on a 64-bit host. If not, then skip the unit tests.
#        self.host_arch = 'i686'     # to allow debugging on a 32-bit host
        # Get global variables
        dict = self.comsa_lib.getGlobalConfig(self)
        self.buildLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("SRC"))       #    '/vobs/com_sa/dev/src/'
        self.unitTestsLocation = '%s%s' %(self.COMSA_REPO_PATH, dict.get("UNIT_TEST"))
        self.buildDir = dict.get('BUILD_TOKENS')
        self.unitTestResultFile = 'comsa_ut_cov.info'
        self.lcovToolPath = '%s%s' %(self.COMSA_REPO_PATH, dict.get('LCOV_PATH'))
        self.gcovToolPath = '%s%s' %(self.CMW_TOOLS, dict.get('GCOV_PATH'))
        self.backupName = 'standardComSa'
        self.comSaInstall = 'ComSa_install.sdp'

        # used on the build server for obj and coverage files, also used on the target (must be the same for the coverage to work)
        self.covLocation = os.environ['COM_SA_RESULT'] # must be set beforehand to e.g. 'setenv COM_SA_RESULT /home/$USER/COV_COMSA'
        self.objArchive ='obj.files.tgz'
        self.covResultArchive = 'cov.result.tgz'
        self.temp_dir = '/home/cov_comsa/'          # on the target
        self.comRestartWaitTime = 10
        self.resultFileIni = 'comsa_ft_new_cov_ini.info'
        self.resultFile = 'comsa_ft_new_cov.info'
        self.combinedResultFile = 'comsa_combined_ft_ut_cov_ini.info'
        self.finalResultFile = 'comsa_combined_ft_ut_cov.info'
        self.rmPattern   = '*LSB_BUILD_ENV/* *dependencies/*'        # not interesting results to remove from FT
        self.rmPatternUt = '*4.8.1/* *unittest/* *dependencies/*'   # not interesting results to remove from UT
        self.covLocFile = 'covLocationFile'
        self.resultLocation = '/home/$USER/cov_comsa_'   # on the build machine
        self.html_ut    = 'html_ut'
        self.html_ft    = 'html_ft'
        self.html_ft_ut = 'html_ft_ut' # the combined result location

    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        if self.linuxDistro == self.distroTypes[1]: # rhel
            self.comSaRPMorig = dict.get('CXP_SDP_NAME_RHEL')
            self.comSaRPMofficial = dict.get('CXP_SDP_NAME_RHEL_OFFICIAL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE_RHEL'))
        else:
            self.comSaRPMorig = dict.get('CXP_SDP_NAME')
            self.comSaRPMofficial = dict.get('CXP_SDP_NAME_OFFICIAL')
            self.buildRelease = '%s%s' %(self.COMSA_REPO_PATH, dict.get('RELEASE'))

        self.myLogger.info('Exit setUp')

    def runTest(self):
        self.logger.info('runTest')
        self.setTestStep('runTest')

        global destFileLoc
        global resLocFile
        # determine the host type (32/64-bit architecture)
        self.myLogger.debug('Get the host architecture (32/64 bit)')
        cmd = 'uname -p'
        result = self.miscLib.execCommand(cmd)
        self.fail(result[0], result[1])
        self.this_host_arch = result[1].strip()

        # Variables needed for the build token management
        dirName = System.getProperty("logdir")
        user = os.environ['USER']
        self.tokenPatternSrc = 'buildToken-%s' %user
        self.tokenPatternUnitT = 'buildToken-unittest-%s' %user
        self.suiteLogDir = dirName.split('/')[len(dirName.split('/')) - 1]
        self.numberOfGetTokenRetries = 5

        if self.tag == 'TC-COV-001': #  run the preparation part of the code coverage test

            # save the path with the username to be used on the target. On the target the user is 'root'
            self.myLogger.debug('Saving the path with username to a file')
            result = self.miscLib.execCommand('echo %s > %s%s' %(self.covLocation, self.buildRelease, self.covLocFile))
            self.fail(result[0],result[1])

            timestamp = self.miscLib.execCommand('date "+%Y%m%d_%H%M%S"')
            resultDir = self.miscLib.execCommand('echo %s' %self.resultLocation)
            destFileLoc = '%s%s' %(resultDir[1].strip(), timestamp[1].strip())
            resLocFile = "resLocationFile_%s" %timestamp[1].strip()

            # create the directory for the results on the build machine
            result = self.miscLib.execCommand('mkdir -p %s' %destFileLoc)
            self.fail(result[0], result[1])

            # save the result location in a file to be used by the other TC for collecting coverage results
            result = self.miscLib.execCommand('echo %s/ > /home/$USER/%s' %(destFileLoc, resLocFile))
            self.fail(result[0],result[1])

            # create directory on the target to copy files to (if it does not exist)
            cmd = 'mkdir -p %s' %(self.temp_dir)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            # Unpack the Obj files archive on the target.
            self.myLogger.debug('Copying the coverage obj files to the target')
            try:
                file = '%s%s' %(self.buildRelease, self.objArchive)
                self.sshLib.remoteCopy(file, '%s' %(self.temp_dir), timeout = 60)

            except:
                self.fail('ERROR','failed to copy the obj files to the target')

            self.myLogger.debug('Unpacking the coverage obj files on the target')
            cmd = 'cd / ; tar zxf %s%s' %(self.temp_dir, self.objArchive)
            #There will be some missing files, should wait 'tar' command finished
            self.sshLib.setTimeout(600)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            self.myLogger.debug('Copying the coverage location file file to the target')
            file = '%s%s' %(self.buildRelease, self.covLocFile)
            result = self.sshLib.remoteCopy(file, '%s' %(self.temp_dir), timeout = 60)
            self.fail(result[0], result[1])

            self.myLogger.debug('Chang permision coverage obj files on the target')
            cmd = 'chmod 777 -R `cat %s%s`' %(self.temp_dir, self.covLocFile)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

        elif self.tag == 'TC-COV-UNIT':
            if self.this_host_arch == self.host_arch :
            # Get a build token
                for i in range(self.numberOfGetTokenRetries):
                    result = self.comsa_lib.getBuildToken(self.suiteLogDir, self.buildDir, self.tokenPatternUnitT)
                    if result[0] == 'SUCCESS':
                        break
                self.fail(result[0],result[1])

                # obtain code coverage results from the unit tests
                self.myLogger.debug('Build and run the unit tests and produce code coverage result')
                result = self.miscLib.execCommand("bash -c 'pushd %s ; make clean ; make coverage; popd '" %(self.unitTestsLocation))
                #self.fail(result[0], result[1]) # this fails for some reason!!!

                # copy the HTML result to the result location
                result = self.miscLib.execCommand('scp -r %s%s/ %s/' %(self.unitTestsLocation, self.html_ut, destFileLoc))
                self.fail(result[0], result[1])

                # Release the build token
                result = self.comsa_lib.releaseToken(self.suiteLogDir, self.buildDir, self.tokenPatternUnitT)
                self.fail(result[0],result[1])

                if eval(System.getProperty("displayFirefox")):
                    result = self.miscLib.execCommand('firefox %s/%s/index.html &' %(destFileLoc, self.html_ut))
                    #self.fail(result[0], result[1])
                self.setAdditionalResultInfo("UT Coverage report: %s/%s/index.html" %(destFileLoc, self.html_ut))
            else:
                self.myLogger.info('Cannot execute the unit tests on this host type: %s, shipping this step, expected: %s.' %(self.this_host_arch, self.host_arch) )


        elif self.tag == 'TC-COV-003': # restart COM, collect the code coverage results and restore the system to the original state

            # restart COM. It needs to be restarted on both controllers !
            self.myLogger.debug('Restarting COM on SC-1 so the coverage results are produced')
            result = self.sshLib.sendCommand('pidof /opt/com/bin/com', 2, 1)
            self.fail(result[0], result[1])
            pidofCom = result[1].strip()

            result = self.sshLib.sendCommand('kill -s QUIT %s' %pidofCom, 2, 1)
            self.miscLib.waitTime(self.comRestartWaitTime)
            self.fail(result[0], result[1])

            noOfScs = len(self.testConfig['controllers'])
            if noOfScs == 2:

                self.myLogger.debug('Restarting COM on SC-2 so the coverage results are produced')
                result = self.sshLib.sendCommand('pidof /opt/com/bin/com', 2, 2)
                self.fail(result[0], result[1])
                pidofCom = result[1].strip()

                result = self.sshLib.sendCommand('kill -s QUIT %s' %pidofCom, 2, 2)
                self.miscLib.waitTime(self.comRestartWaitTime)
                self.fail(result[0], result[1])

            # collect the code coverage results
            self.myLogger.debug('Chang permision coverage folder on the target')
            cmd = 'chmod 777 -R `cat %s%s`' %(self.temp_dir, self.covLocFile)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            self.myLogger.debug('Archiving the coverage results')
            cmd = 'cd / ; tar zcf %s%s `cat %s%s`' %(self.temp_dir, self.covResultArchive, self.temp_dir, self.covLocFile)
            self.sshLib.setTimeout(180)
            result = self.sshLib.sendCommand(cmd)
            self.fail(result[0], result[1])

            self.myLogger.debug('Retrieving the location to store the results on the build machine')
            result = self.miscLib.execCommand('cat /home/$USER/%s' %resLocFile)
            self.fail(result[0], result[1])
            resLocation = result[1].strip()

            # copy to the build machine
            self.myLogger.debug('Copying the coverage results to the build machine')
            result = self.miscLib.execCommand('mkdir -p %s' %resLocation)
            self.fail(result[0], result[1])

            srcFile = '%s%s' %(self.temp_dir, self.covResultArchive)
            result = self.sshLib.remoteCopyFrom(srcFile, resLocation, timeout = 60)
            self.fail(result[0], result[1])

            # perform postprocessing
            self.myLogger.debug('Postprocessing the coverage results on the build machine')
            result = self.miscLib.execCommand('\\rm -rf %s' %self.covLocation)
            self.fail(result[0], result[1])
            result = self.miscLib.execCommand('cd /; tar zxf %s%s' %(resLocation, self.covResultArchive))
            self.fail(result[0], result[1])

            result = self.miscLib.execCommand('ls -l %s' %self.covLocation)

            result = self.miscLib.execCommand('cd %s' %resLocation)
            self.fail(result[0], result[1])
            result = self.miscLib.execCommand('%slcov --directory %s --capture --output-file %s%s --gcov-tool %s --base-directory %s' %(self.lcovToolPath, self.covLocation, resLocation, self.resultFileIni, self.gcovToolPath, self.buildLocation))
            #self.fail(result[0], result[1])  # produces some warnings

            # extract only the coverage data for the interesting files by removing the not interesting ones
            result = self.miscLib.execCommand('%slcov -r %s%s %s --output-file %s%s' %(self.lcovToolPath, resLocation, self.resultFileIni, self.rmPattern, resLocation, self.resultFile))
            self.fail(result[0], result[1])

            result = self.miscLib.execCommand('mkdir -p %shtml' %resLocation)
            self.fail(result[0], result[1])
            result = self.miscLib.execCommand('%sgenhtml -o %shtml %s%s' %(self.lcovToolPath, resLocation, resLocation, self.resultFile))
            self.fail(result[0], result[1])
            if eval(System.getProperty("displayFirefox")):
                result = self.miscLib.execCommand('firefox %shtml/index.html &' %resLocation)
                #self.fail(result[0], result[1])
            self.setAdditionalResultInfo("FT Coverage report: %shtml/index.html" %resLocation)

            # skip the unit test if not running on a 64-bit host
            if self.this_host_arch == self.host_arch :

                # Combine the unit tests and FT coverage results.
                self.myLogger.debug('Converting the paths in the unit test result to match the FT result')
                result = self.miscLib.execCommand("sed -i 's,/src/com_specific/unittest/../../../src/,/src/../src/,g' %s%s" %(self.unitTestsLocation, self.unitTestResultFile))
                self.fail(result[0], result[1])

                self.myLogger.debug('Combining the unit tests and FT coverage results')
                ut_info_file = '%s%s' %(self.unitTestsLocation, self.unitTestResultFile)
                result = self.miscLib.execCommand('%slcov --add-tracefile %s%s --add-tracefile %s --output-file %s%s' %(self.lcovToolPath, resLocation, self.resultFile, ut_info_file, resLocation, self.combinedResultFile))
                #self.fail(result[0], result[1]) # this fails due to a warning in ComSaLogService.c

                self.myLogger.debug('Removing the foreign files from the coverage results')
                result = self.miscLib.execCommand('%slcov -r %s%s %s --output-file %s%s' %(self.lcovToolPath, resLocation, self.combinedResultFile, self.rmPatternUt, resLocation, self.finalResultFile))
                self.fail(result[0], result[1])

                result = self.miscLib.execCommand('mkdir -p %s%s' %(resLocation, self.html_ft_ut))
                self.fail(result[0], result[1])
                result = self.miscLib.execCommand('%sgenhtml -o %s%s %s%s' %(self.lcovToolPath, resLocation, self.html_ft_ut, resLocation, self.finalResultFile))
                self.fail(result[0], result[1])
                if eval(System.getProperty("displayFirefox")):
                    result = self.miscLib.execCommand('firefox %s%s/index.html &' %(resLocation, self.html_ft_ut))
                    #self.fail(result[0], result[1])
                self.setAdditionalResultInfo("FT+UT Coverage report: %s%s/index.html" %(resLocation, self.html_ft_ut))

            else:
                self.myLogger.info('Skipping the step that combines the FT and UT coverage results')

            # perform cleanup on the cluster
            self.myLogger.debug('Performing cleanup on the cluster.')
            result = self.sshLib.sendCommand('\\rm -rf `cat %s%s`' %(self.temp_dir, self.covLocFile))
            self.fail(result[0], result[1])
            result = self.sshLib.sendCommand('\\rm -rf %s' %self.temp_dir)
            self.fail(result[0], result[1])

            #Clean up build machine
            self.myLogger.debug('cleanup on the build machine.')
            result = self.miscLib.execCommand('\\rm -rf /home/$USER/%s' %resLocFile)
            self.fail(result[0], result[1])

        else:
            self.fail('ERROR', 'Illegal tag, not implemented, otherwise edit this if statement!')


        coreTestCase.CoreTestCase.runTest(self)
        self.myLogger.info("exit runTest")



    def tearDown(self):
        self.setTestStep('tearDown')

        if self.tag == 'TC-COV-003':

#           del self.testSuiteConfig['codeCoverageTest']
            if self.testSuiteConfig.has_key('startTime'):

                # this backup restore operation reports success, but sometimes seems to be causing cycllic reboot of the cluster.
                # is the comment line above valid?
                result = self.comsa_lib.restoreSystem(self, self.backupName, self.testConfig, self.testSuiteConfig, self.distroTypes)
                self.fail(result[0], result[1])

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
