#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2007 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained
# herein confidential and shall protect the same in whole or in part
# from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################

'''File information:
   ===================================================
   %CCaseFile:  vbox_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2011-01-12 %

   Author:

   Description:

'''

import time
import re
import os


#import subprocess
#import signal

import omp.tf.logger_lib as logger_lib
import omp.tf.misc_lib as misc_lib
import omp.tf.ssh_lib as ssh_lib

def setUp():
    logger_lib.logMessage("_vbox_utils: Initiating", logLevel='debug')

    return


def tearDown():
    logger_lib.logMessage("_vbox_utils: Bye, bye!", logLevel='debug')
    return


class Vbox(object):

    global clusterWrapper
    clusterWrapper = '/home/comsaci/tools/cluster.py'
    global clusterWrapperDek
    clusterWrapperDek = 'ssh csa01 \'sudo -u csa /usr/local/tools/csa-cluster.sh'
    global noPasswdFileMsg
    noPasswdFileMsg = "make sure windows password file %s/.ssh/passwd existed with mode 600"
    global noPasswordlessLoginError
    noPasswordlessLoginError = "Password"


    def __init__(self, timeOut = 30) :
        self.nodeTypes = ['DES-1-SC-1', 'DES-1-SC-2', 'DES-1-PL-3', 'DES-1-PL-4' ]
        self.nodes = [(2,1),(2,2),(2,3),(2,4)]

    def powerOn(self, subrack, slot):
        '''
        Arguments:
        (int subrack, int slot)

        Returns:
        tuple('SUCCESS','Power on blade_<subrack>_<slot> succeeded') or
        tuple('ERROR', 'Power on blade_<subrack>_<slot> failed')
        NOTE:

        Dependencies:
        misc_lib, logger_lib

        seasc0863 (VirtualBox): VBoxManage startvm DES-1-PL-3
        Oracle VM VirtualBox Command Line Management Interface Version 3.2.8_OSE
        (C) 2005-2010 Oracle Corporation
        All rights reserved.

        Waiting for the VM to power on...
        VM has been successfully started.
        seasc0863 (VirtualBox):


        '''
        logger_lib.enter()
        if slot > len(self.nodeTypes):
            return ('ERROR', 'Unsupported number of nodes for Vbox')
        node = self.nodeTypes[slot-1]
        expected = 'Chassis Power is on'
        command = "VBoxManage startvm %s" % (node)
        result, reply = self._sendCommand(command, timeout=20)
        misc_lib.waitTime(2)
        result, reply=self.powerStatus(subrack, slot)
        stopTryTime = int(time.time()) + 180
        while (expected!=reply) and (int(time.time()) < stopTryTime):
            misc_lib.waitTime(10)
            result, reply=self.powerStatus(subrack, slot)

        if (expected!=reply):
            result = 'ERROR'

        logger_lib.leave()
        return (result, reply)

    def powerOff(self, subrack, slot):
        '''
        power off node().

        Arguments:
        (int subrack, int slot)

        Returns:
        tuple('SUCCESS','Power off blade_<subrack>_<slot> succeeded') or
        tuple('ERROR', 'Power off blade_<subrack>_<slot> failed')

        NOTE:

        Dependencies:
        misc_lib, logger_lib

        seasc0863 (VirtualBox): VBoxManage controlvm DES-1-PL-3 poweroff
        Oracle VM VirtualBox Command Line Management Interface Version 3.2.8_OSE
        (C) 2005-2010 Oracle Corporation
        All rights reserved.

        0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
        seasc0863 (VirtualBox):

        '''

        logger_lib.enter()
        if slot > len(self.nodeTypes):
            return ('ERROR', 'Unsupported number of nodes for Vbox')

        blade = 'blade_%s_%s' %  (subrack, slot)
        ssh_lib.tearDownBlade(blade) #tear down the blade before power reset via gw-pc

        node = self.nodeTypes[slot-1]
        expected = 'Chassis Power is off'
        command = "VBoxManage controlvm %s poweroff " % (node)
        result, reply = self._sendCommand(command, timeout=10)
        misc_lib.waitTime(2)
        result, reply=self.powerStatus(subrack, slot)
        stopTryTime = int(time.time()) + 10
        while (expected!=reply) and (int(time.time()) < stopTryTime):
            misc_lib.waitTime(2)
            result, reply=self.powerStatus(subrack, slot)

        if (expected!=reply):
            result = 'ERROR'

        logger_lib.leave()
        return (result, reply)


    def powerReset(self, subrack, slot, ControlType='OffOn'):
        '''
        power resetnode().

        Arguments:
        (int subrack, int slot)

        Returns:
        tuple('SUCCESS','Power off blade_<subrack>_<slot> succeeded') or
        tuple('ERROR', 'Power off blade_<subrack>_<slot> failed')

        NOTE:

        Dependencies:
        misc_lib, logger_lib

        '''

        logger_lib.enter()
        if slot > len(self.nodeTypes):
            return ('ERROR', 'Unsupported number of nodes for essim')

        blade = 'blade_%s_%s' %  (subrack, slot)
        ssh_lib.tearDownBlade(blade) #tear down the blade before power reset via gw-pc

        node = self.nodeTypes[slot-1]
        expected = 'Chassis Power is on'
        command = "VBoxManage controlvm %s reset " % (node)
        result, reply = self._sendCommand(command, timeout=10)
        misc_lib.waitTime(2)
        result, reply=self.powerStatus(subrack, slot)
        stopTryTime = int(time.time()) + 180
        while (expected!=reply) and (int(time.time()) < stopTryTime):
            misc_lib.waitTime(10)
            result, reply=self.powerStatus(subrack, slot)

        if (expected!=reply):
            result = 'ERROR'

        logger_lib.leave()
        return (result, reply)

    def powerStatus(self, subrack, slot):
        '''
            Get power status for node().

            Arguments:
            (int subrack, int slot)

            Returns:
            tuple('SUCCESS','Chassis Power is on|off') or
            tuple('ERROR', 'Get power status for blade_<subrack>_<slot> failed')

            NOTE:

            Dependencies:
            ssh_lib, target_data

            seasc0863 (VirtualBox): VBoxManage showvminfo DES-1-PL-3 | grep State:
            State:           running (since 2011-01-11T12:57:24.625000000)
            seasc0863 (VirtualBox):

            '''

        logger_lib.enter()
        if slot > len(self.nodeTypes):
            return ('ERROR', 'Unsupported number of nodes for VBox')
        node = self.nodeTypes[slot-1]
        #onPattern = ["%s_%d_%d" % (node, subrack, slot), 'power: on', 'Network: up', 'SAF: running']
        onPattern = 'running'
        command = "VBoxManage showvminfo %s | grep State:" % (node)
        result, reply =self._sendCommand(command, timeout=10)
        logger_lib.logMessage(reply, logLevel = 'debug')
        if result == 'SUCCESS':
                if (re.search(onPattern, reply)):
                    reply= 'Chassis Power is on'
                else:
                    reply= 'Chassis Power is off'
        else:
            reply = 'Get power status for %s_%d_%d failed' % (node, subrack, slot)

        logger_lib.leave()
        return (result, reply)

    def clusterPowerReset(self):
        '''
        Reset the cluster, power off/on on all valid blades().

        Arguments:
        None

        Returns:
        tuple('SUCCESS','cluster power reset succeeded') or
        tuple('ERROR', 'cluster power reset failed')

        NOTE:
        if blade already is in power off state, it's never powered on.
        dynamic generated target data solves this problem

        Dependencies:
        target_data
        powerOff/On/Status

        '''

        result = ('SUCCESS','cluster power reset succeeded')

        logger_lib.enter()
        for subrack,slot in self.nodes:
            res, reply = self.powerOff(subrack, slot)
            if res != 'SUCCESS':
                result = ('ERROR','cluster power reset failed')

        for subrack, slot in self.nodes:
            res, reply = self.powerOn(subrack, slot)
            if res != 'SUCCESS':
                result = ('ERROR','cluster power reset failed')

        logger_lib.leave()
        return result


    def virtualTargetPowerOnAll(self, targetData):
        '''
        Power on all valid blades of a vSphere virtual cluster.

        Arguments:
        targetData

        Returns:
        tuple('SUCCESS', 'a message detailing the operation') or
        tuple('ERROR', 'a relevant error message')

        NOTE:

        Dependencies:
        target_data
        cluster.py script that is a wrapper around pysphere
        '''

        logger_lib.enter()
        dekCtrlAddrDistinguisher = re.compile("^10\.172\..*\..*")

        if re.search(dekCtrlAddrDistinguisher, targetData['ipAddress']['ctrl']['ctrl1']):
            nodes = ""
            numberOfNodes = int(targetData['physical_size'])
            for i in range (1,numberOfNodes+1):
                nodes += str(i) + ' '
            command = '%s start --id %s --nodes \"%s\" 2> /dev/null \'' %(clusterWrapperDek, targetData['target'].split("_")[2], nodes)
        else:
            command = '%s --on --cluster_id=%s' %(clusterWrapper, targetData['target'].split("_")[2])

        result, reply = misc_lib.execCommand(command)
        misc_lib.waitTime(4)
        if noPasswdFileMsg in reply:
            result = 'ERROR'
        if noPasswordlessLoginError in reply:
            result = 'ERROR'
        logger_lib.leave()
        return (result, reply)

    def virtualTargetPowerOffAll(self, targetData):
        '''
        Power off all valid blades of a vSphere virtual cluster.

        Arguments:
        targetData

        Returns:
        tuple('SUCCESS', 'a message detailing the operation') or
        tuple('ERROR', 'a relevant error message')

        NOTE:

        Dependencies:
        target_data
        cluster.py script that is a wrapper around pysphere
        '''
        logger_lib.enter()
        dekCtrlAddrDistinguisher = re.compile("^10\.172\..*\..*")

        if re.search(dekCtrlAddrDistinguisher, targetData['ipAddress']['ctrl']['ctrl1']):
            nodes = ""
            numberOfNodes = int(targetData['physical_size'])
            for i in range (1,numberOfNodes+1):
                nodes += str(i) + ' '
            command = '%s stop --id %s --nodes \"%s\" 2> /dev/null \'' %(clusterWrapperDek, targetData['target'].split("_")[2], nodes)
        else:
            command = '%s --off --cluster_id=%s' %(clusterWrapper, targetData['target'].split("_")[2])

        result = misc_lib.execCommand(command)
        misc_lib.waitTime(4)
        if noPasswdFileMsg in reply:
            result = 'ERROR'
        if noPasswordlessLoginError in reply:
            result = 'ERROR'
        logger_lib.leave()
        return result

    def virtualTargetSnapCreate(self, targetData, snapshotName):
        '''
        Power on on all valid blades of a vSphere virtual cluster.

        Arguments:
        targetData

        Returns:
        tuple('SUCCESS', 'a message detailing the operation') or
        tuple('ERROR', 'a relevant error message')

        NOTE:

        Dependencies:
        target_data
        cluster.py script that is a wrapper around pysphere
        '''

        logger_lib.enter()
        dekCtrlAddrDistinguisher = re.compile("^10\.172\..*\..*")

        if re.search(dekCtrlAddrDistinguisher, targetData['ipAddress']['ctrl']['ctrl1']):
            nodes = ""
            numberOfNodes = int(targetData['physical_size'])
            for i in range (1,numberOfNodes+1):
                nodes += str(i) + ' '
            command = '%s snap --snapname %s --id %s --nodes \"%s\" 2> /dev/null \'' %(clusterWrapperDek, snapshotName, targetData['target'].split("_")[2], nodes)
        else:
            command = '%s --snap=%s --cluster_id=%s' %(clusterWrapper, snapshotName, targetData['target'].split("_")[2])

        result, reply = misc_lib.execCommand(command)
        misc_lib.waitTime(4)
        if noPasswdFileMsg in reply:
            result = 'ERROR'
        if noPasswordlessLoginError in reply:
            result = 'ERROR'
        logger_lib.leave()
        return (result, reply)

    def virtualTargetSnapRestore(self, targetData, snapshotName):
        '''
        Power on on all valid blades of a vSphere virtual cluster.

        Arguments:
        targetData

        Returns:
        tuple('SUCCESS', 'a message detailing the operation') or
        tuple('ERROR', 'a relevant error message')

        NOTE:

        Dependencies:
        target_data
        cluster.py script that is a wrapper around pysphere
        '''

        logger_lib.enter()
        dekCtrlAddrDistinguisher = re.compile("^10\.172\..*\..*")

        if re.search(dekCtrlAddrDistinguisher, targetData['ipAddress']['ctrl']['ctrl1']):
            nodes = ""
            numberOfNodes = int(targetData['physical_size'])
            for i in range (1,numberOfNodes+1):
                nodes += str(i) + ' '
            command = '%s snapback --snapname %s --id %s --nodes \"%s\" 2> /dev/null \'' %(clusterWrapperDek, snapshotName, targetData['target'].split("_")[2], nodes)
        else:
            command = '%s --snapback=%s --cluster_id=%s' %(clusterWrapper, snapshotName, targetData['target'].split("_")[2])

        result, reply = misc_lib.execCommand(command)
        misc_lib.waitTime(5)
        if noPasswdFileMsg in reply:
            result = 'ERROR'
        if noPasswordlessLoginError in reply:
            result = 'ERROR'
        else:
            if re.search(dekCtrlAddrDistinguisher, targetData['ipAddress']['ctrl']['ctrl1']):
                command = '%s start --id %s --nodes \"%s\" \'' %(clusterWrapperDek, targetData['target'].split("_")[2], nodes)
                result, reply = misc_lib.execCommand(command)
                misc_lib.waitTime(60)
        logger_lib.leave()
        return (result, reply)



##############################################################################
# private method
#############################################################################
    def _sendCommand(self, command, timeout=10, retries = 5):

        """
            Arguments:
            (string command, string expected, int timeout, int subrack, int slot)
        """
        logger_lib.enter()

        finished = False
        pid = None

        #send command
        for r in range(retries): # retry loop
            if finished == True:
                break
            if pid != None: #VMware script are hanging
                os.popen3("kill -9 %d" % int(pid))

            logger_lib.logMessage("Executing VBox command: %s" % command)
            child_stdin, child_stdout, child_stderr = os.popen3(command)

            cmdTryTime = int(time.time()) + int(timeout)
            while(int(time.time()) < cmdTryTime): # this wait for program to finish
                pid_stdin, pid_stdout, pid_stderr = os.popen3('pidof VBox')
                pid = pid_stdout.read()
                pid_stdin.close()
                pid_stdout.close()
                pid_stderr.close()

                stdoutString = child_stdout.read()
                stderrString = child_stderr.read()
                if stdoutString != '' :
                    finished = True
                    break
                if stderrString != '':
                    pid = None
                    finished = False
                    break
                try:
                    pid = int(pid.strip())
                except:
                    finished = True
                    break
                misc_lib.waitTime(1)

        child_stdin.close()
        child_stdout.close()
        child_stderr.close()

        if stderrString != "":
            logger_lib.logMessage("VBox error result: %s" % stderrString.strip(), logLevel = 'error')
            logger_lib.leave()
            return ("ERROR", stderrString.strip())
        logger_lib.logMessage("VBox result: %s" % stdoutString.strip())
        logger_lib.leave()
        return ("SUCCESS", stdoutString.strip())



##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':

    import sys
    import common.target.common_lib.st_env_lib as st_env_lib
    st_env_lib.executeFunction(sys.argv)

    st_env_lib.setUp()
    ###########TEST AREA START###############

    v=Vbox()
    print v.powerStatus(2,3)

    ###########TEST AREA END###############
    st_env_lib.tearDown()



