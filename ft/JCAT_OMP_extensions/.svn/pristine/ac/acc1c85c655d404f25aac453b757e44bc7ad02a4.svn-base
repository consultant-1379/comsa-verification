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
   %CCaseFile:  essim_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2009-03-23 %

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

def setUp():
    logger_lib.logMessage("_essim_utils: Initiating", logLevel='debug')
    createConfig()
    return


def tearDown():
    logger_lib.logMessage("_essim_utils: Bye, bye!", logLevel='debug')
    return

def createConfig():

    file = os.path.join(os.environ['ESSIM_WORKSPACE'], 'essim.conf')
    try:
        os.remove(file) #remove file if exists
    except:
        pass

    content="""controllers=2
controller_mem=512
payloads=2
payload_mem=512
    """

    try:
        fd=open(file, 'w')    
        fd.write(content)
        fd.close()
    except:
        logger_lib.logMessage("Failed to create essim.conf file", logLevel='error')


class Essim(object):

    def __init__(self, timeOut = 30) :
        self.nodeTypes = ['SC', 'SC', 'PL', 'PL' ]
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
    
        '''
        logger_lib.enter()
        if slot > len(self.nodeTypes):
            return ('ERROR', 'Unsupported number of nodes for essim')  
        node = self.nodeTypes[slot-1]
        expected = 'Chassis Power is on'
        command = "essim --start %s_%d_%d" % (node, subrack, slot)
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
    
        '''

        logger_lib.enter()
        if slot > len(self.nodeTypes):
            return ('ERROR', 'Unsupported number of nodes for essim')  
        node = self.nodeTypes[slot-1]
        expected = 'Chassis Power is off'
        command = "essim --stop %s_%d_%d" % (node, subrack, slot)
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
        node = self.nodeTypes[slot-1]
        expected = 'Chassis Power is on'
        command = "essim --restart %s_%d_%d" % (node, subrack, slot)
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
    
            '''
   
        logger_lib.enter()
        if slot > len(self.nodeTypes):
            return ('ERROR', 'Unsupported number of nodes for essim')  
        node = self.nodeTypes[slot-1]
        onPattern = ["%s_%d_%d" % (node, subrack, slot), 'power: on', 'Network: up', 'SAF: running']
        #offPattern = ["%s_%d_%d" % (node, subrack, slot), 'power: off', 'network: down', 'SAF: not running']
        command = "essim --status %s_%d_%d" % (node, subrack, slot)
        result, reply =self._sendCommand(command, timeout=10)
        logger_lib.logMessage(reply, logLevel = 'debug')
        if result == 'SUCCESS':
            reply=reply.split('\t')
            if reply==onPattern:
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
    
##############################################################################
# private method
#############################################################################

    # This is not compatible with Jython 

    #def _sendCommand(self, command, timeout=10, retries = 5):
    #    """
    #        Arguments:
    #        (string command, string expected, int timeout, int subrack, int slot)
    #    """
    #    logger_lib.enter()
    
    #    finished = False
    #    p = None
    #    child_stdout=''
    #    child_stderr=''
        #send command
    #    for r in range(retries): # retry loop
    #        if finished == True:
    #            break
    #        if p != None: #VMware script are hanging
    #            os.kill(p.pid, signal.SIGKILL)
    
    #       logger_lib.logMessage("Executing Essim command: %s" % command)
    #        p = subprocess.Popen(command, shell=True, bufsize=0,
    #            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)  
    #        misc_lib.waitTime(1)   
    #        cmdTryTime = int(time.time()) + int(timeout)
    #        while(int(time.time()) < cmdTryTime): # this wait for program to finish
    #            if p.poll() != None:
    #                (child_stdout, child_stderr) = p.communicate()
    #                if child_stderr == '': #No errors reported 
    #                    finished = True
    #                    break
    #            misc_lib.waitTime(1)        
             
    #    if child_stderr != "":
    #        logger_lib.logMessage("Essim error result: %s" % child_stderr.strip(), logLevel = 'error')
    #        logger_lib.leave()
    #        return ("ERROR", child_stderr.strip())
    #    logger_lib.logMessage("Essim result: %s" % child_stdout.strip())
    #    logger_lib.leave()
    #    return ("SUCCESS", child_stdout.strip())

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
        
            logger_lib.logMessage("Executing Essim command: %s" % command)
            child_stdin, child_stdout, child_stderr = os.popen3(command)

            cmdTryTime = int(time.time()) + int(timeout)
            while(int(time.time()) < cmdTryTime): # this wait for program to finish
                #pid_stdin, pid_stdout, pid_stderr = os.popen3('pidof %s' % argv[0])
                pid_stdin, pid_stdout, pid_stderr = os.popen3('pidof essim')
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
            logger_lib.logMessage("Essim error result: %s" % stderrString.strip(), logLevel = 'error')
            logger_lib.leave()
            return ("ERROR", stderrString.strip())
        logger_lib.logMessage("Essim result: %s" % stdoutString.strip())
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

    e=Essim()
    print e.powerStatus(2,3) 
  
    ###########TEST AREA END###############
    st_env_lib.tearDown()



