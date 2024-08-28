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

    Tag: TC-MR40274-001

    Id:
    "Install the RPM on cbaserv01/02 which installed SLES 12 without LDE"
    ==================================

"""


import test_env.fw.coreTestCase as coreTestCase
import time

import os,sys,re
from java.lang import System
import omp.tf.misc_lib as misc_lib


class InstallRPM(coreTestCase.CoreTestCase):

    def __init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance):
        coreTestCase.CoreTestCase.__init__(self, tag, name, testConfig, testSuiteConfig, testCaseConfig, instance)

        # parameters from the config files

        self.MY_REPOSITORY = os.environ['MY_REPOSITORY']

        # defautle is the lowest version
        self.reqComSaVersion = "R1A01"
        self.reqComSaRelease = "3"
        self.RPMName=''



    def id(self):
        return self.name

    def setUp(self):
        self.setTestStep('setUp')
        self.setTestcase(self.tag, self.name)
        coreTestCase.CoreTestCase.setUp(self)

        dict = self.comsa_lib.getGlobalConfig(self)
        self.pathToConfigFiles = dict.get("PATH_TO_CONFIG_FILES")


        self.myLogger.info('Exit setUp')

    def runTest(self):


        self.skip_test = False

        #Step 0
        #The TC only running on cbaserv01/cbaserv02
        self.setTestStep('Checking the enviroment run FT')

        # get current user's ID
        currentUser = os.environ['USER']
        hostName    = os.environ['HOST']
        self.myLogger.debug('currentUser: (%s)' %currentUser)
        self.myLogger.debug('hostName: (%s)' %hostName)
        dek_server = "cbaserv"

        self.myLogger.debug('The Test Case is running on  (%s) ' %hostName)
        if hostName[:len(dek_server)] == dek_server:
            self.skip_test = False
        else:
            self.logger.info('Running on server: %s.Test skipped because it can only run on cbaserv01/02' %hostName)
            self.setAdditionalResultInfo('Test skipped. The TC only running on cbaserv01/02')
            self.skip_test = True

        # add to check version
        ComsaOK = self.lib.checkComponentVersion('comsa', self.reqComSaRelease, self.reqComSaVersion)
        self.fail(ComsaOK[0],ComsaOK[1])



        if ComsaOK[1] and self.skip_test == False:
            self.logger.info('runTest')

            #Step 1
            self.setTestStep('get COM SA Packgage')

            #create tmp folder
            cmd = "test -d /tmp/testRPM/;echo $?"
            result = misc_lib.execCommand(cmd)
            if result[1] == '1\n':
                cmd = "mkdir -m 777 /tmp/testRPM/"
                result = misc_lib.execCommand(cmd)
                if result[0] == 'ERROR':
                    result = ('ERROR', 'create directory /tmp/testRPM/ FAILED')
                    logger.error(result[1])

            # Use function from library comsa_lib
            BuildPath = self.comsa_lib.buildAndStoreCOMSA(self)

            # Copy CXP SDP file to Temp RPM directory
            self.logger.info('copy SPD package to Temp RPM directory')
            if BuildPath[6] != '':
                cmd = "\cp %s /tmp/testRPM/" %BuildPath[6]
                result = misc_lib.execCommand(cmd)
                self.fail(result[0], result[1])
            else:
                self.logger.info('installCOMSAFromStream: The absolute filename of cxp sdp file is empty')


            #step 2
            self.setTestStep('install RPM and checking')
            self.logger.info('Untar SDP package')
            cmd = "cd /tmp/testRPM/; tar xf *.sdp"
            result = misc_lib.execCommand(cmd)

            self.logger.info('copy to /data/sles12/home/')
            cmd = "find /tmp/testRPM/ -name *rpm -printf '%f\n'"
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])
            if result[0] != 'SUCCESS':
                self.logger.info('The RPM file does not exist')
            else:
                self.RPMName = result[1]

            cmd = "\cp /tmp/testRPM/*.rpm /data/sles12/home/"
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])

            #step 3
            self.setTestStep('copy the "install_RPM.sh" and "remove_RPM.sh" script to /data/sles12/home/')
            cmd = "\cp %s%s/install_RPM.sh /data/sles12/home/" %(self.MY_REPOSITORY,self.pathToConfigFiles)
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])

            cmd = "\cp %s%s/remove_RPM.sh /data/sles12/home/" %(self.MY_REPOSITORY,self.pathToConfigFiles)
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])

            #step 4
            self.setTestStep('Logining schroot and install RPM')
            cmd = "schroot -u root -c sles12 -d /home ./install_RPM.sh %s" %self.RPMName
            result = misc_lib.execCommand(cmd)
            if 'FAILED' in result[1]:
                self.fail('ERROR', 'The RPM of COM SA install FAILED')
            else :
                self.logger.info('The RPM of COM SA install successfully ')

            coreTestCase.CoreTestCase.runTest(self)

        else:
            if ComsaOK[1] == False:
                self.logger.info('Skipped tests because of COMSA version not compatible!')
                self.setAdditionalResultInfo('Test skipped, COMSA version not compatible')
            self.skip_test = True
        self.myLogger.info("exit runTest")



    def tearDown(self):
        self.setTestStep('tearDown')
        if self.skip_test == False :

            self.logger.info('Remove RPM out of SLES 12')
            cmd = "schroot -u root -c sles12 -d /home ./remove_RPM.sh"
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])

            cmd = "\\rm -rf /tmp/testRPM/*"
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])

            cmd = "\\rm /data/sles12/home/*.rpm"
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])

            cmd = "\\rm /data/sles12/home/*RPM.sh"
            result = misc_lib.execCommand(cmd)
            self.fail(result[0], result[1])

        coreTestCase.CoreTestCase.tearDown(self)
        self.setTestStep('leave tearDown')



def getSuite(tag, name, testConfig, testSuiteConfig, testCaseConfig, instances, currentClass):
    testcases = []
    testcases.append(currentClass(tag, name, testConfig, testSuiteConfig, testCaseConfig, 0))
    return testcases
