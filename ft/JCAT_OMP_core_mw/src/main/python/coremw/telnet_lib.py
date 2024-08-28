#!/usr/bin/env python
#coding=iso-8859-1
###############################################################################
#
# © Ericsson AB 2006 All rights reserved.
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
   %CCaseFile:  telnet_lib.py %
   %CCaseRev:   /main/R1A/1 % 
   %CCaseDate:  2007-11-20 % 

   Description:
   This module acts as an interactive shell used for communication
   towards remote machines.

   The module creates objects of the class instance cTELNET 
   One instance is created per 
   hw. The handles are created the first time a user wants to open
   a telnet session. The handle is stored and reused upon a new request.
'''

import string
import os
import sys
import time
import re
import getopt
import telnetlib

############### NOTE ####################
# Changed by uabeber for RDA            #
# MUST  be brought back to TSPSAF       #
#########################################

########NODE CONFIGURATION DATA##########
#try:
    #import common.target.target_data as target_data
#except Exception, e:
import omp.target.target_data

#########COMMON USED RESOURCES##########  
from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System
#############GLOBALS##################
pDevice = {}    # a dictionary containing handles to the devices
pBlade = {}    # a dictionary containing handles to the blades
targetData = {}
logger = None

###############################################################################
# setUp / tearDown
###############################################################################

def setUp():
    """This function fetches required data that this library requires to work"""

    global targetData
    global logger
    
    logLevel = System.getProperty("jcat.logging")
    logger = Logger.getLogger('telnet_lib logging')
    logger.setLevel(Level.toLevel(logLevel))
    logger.debug("telnet_lib: Initiating!")
    targetData=target_data.data
    return
    

def tearDown():
    """This function removes handles"""
    tearDownHandles()
    logger.debug("telnet_lib: Bye bye !!")
    return

###############################################################################
#Lib methods
###############################################################################
def setUpSession(session, port):
    """This function will login on a selected device and put the created handle in 
    in the dictionary pBlade This handle will be used in the SendCommand function.
    Returns a tuple including status in first element and a description in second element"""

    global pBlade

    logger.debug('enter setUpSession')

    activeController = "ctrl%d" % (st_env_lib.activeController)  

    if (pBlade.has_key(session)==False): #handle already created?
        logger.info("Creating handle for %s!" % (session))
        pBlade[session] = cTELNET()
        if (pBlade[session]): 
            status = pBlade[session].openTelnetSession(targetData['ipAddress']['ctrl'][activeController], port, targetData['user'], targetData['pwd'])
            if (status[0] == 'ERROR' ):
                logger.error("Can not create a handle to: %s!" % (session))
                logger.debug('leave setUpSession')
                return ('ERROR', 'Can not create a handle to: ' +session)
            else:
                logger.debug("Logged in to blade: %s!" % (session))
                logger.debug('leave setUpSession')
                return ('SUCCESS','Handle to: ' +session+ ' created')
    else:
        logger.debug("Using existing handle: %s!" % (session))
        logger.debug('leave setUpSession')
        return ('SUCCESS','Using existing handle')

def setUpSessionRaw(session, address, port, user, password):
    """This function will login on a selected device and put the created handle in 
    in the dictionary pBlade This handle will be used in the SendCommand function.
    Returns a tuple including status in first element and a description in second element"""

    global pBlade

    logger.debug('enter setUpSessionRaw')

    activeController = "ctrl%d" % (st_env_lib.activeController)  

    if (pBlade.has_key(session)==False): #handle already created?
        logger.info("Creating handle for %s!" % (session))
        pBlade[session] = cTELNET()
        if (pBlade[session]): 
            status = pBlade[session].openTelnetSession(address, port, user, password)
            if (status[0] == 'ERROR' ):
                logger.error("Can not create a handle to: %s!" % (session))
                logger.debug('leave setUpSessionRaw')
                return ('ERROR', 'Can not create a handle to: ' +session)
            else:
                logger.debug("Logged in to blade: %s!" % (session))
                logger.debug('leave setUpSessionRaw')
                return ('SUCCESS','Handle to: ' +session+ ' created')
    else:
        logger.debug("Using existing handle: %s!" % (session))
        logger.debug('leave setUpSessionRaw')
        return ('SUCCESS','Using existing handle')

def setUpDevice(device):
    """This function will login on a selected device and put the created handle in 
    in the dictionary pDevice. This handle will be used in the SendCommandServer function.
    Returns a tuple including status in first element and a description in second element"""

    global pDevice

    logger.debug('enter setUpDevice')

    if (pDevice.has_key(device)==False): #handle already created?
        logger.info("Creating handle for %s!" % (device))
        pDevice[device] = cTELNET()
        if (pDevice[device]): 
            status = pDevice[device].openServerSession(targetData['ipAddress']['serial']['ip'], int(targetData['ipAddress']['serial'][device]),
            targetData['terminal_server_user'], targetData['terminal_server_pwd'],  targetData['user'], targetData['pwd'])
            if (status[0] == 'ERROR' ):
                logger.error("Can not create a handle to: %s!" % (device))
                logger.debug('leave setUpDevice')
                return ('ERROR', 'Can not create a handle to: ' +device)
            else:
                logger.debug("Logged in to device: %s!" % (device))
                logger.debug('leave setUpDevice')
                return ('SUCCESS','Handle to: ' +device+ ' created')
    else:
        logger.debug('leave setUpDevice')
        return ('SUCCESS','Using existing handle')

def tearDownHandles():
    """This function closes the all handles and removes it from the listed record.
    After a call to this function all the existing handles are destroyed.
    Returns a tuple including status in first element and a description in second element"""

    global pBlade
    global pDevice

    logger.debug('enter tearDownHandles')

    sessions=pBlade.keys()
    devices=pDevice.keys()

    for session in sessions :
        tearDownSession(session)
    for device in devices :
       tearDownDevice(device)
    logger.debug('leave tearDownHandles')
    return


def tearDownSession(session):
    """This function closes the handles and removes it from the listed record. 
    After a call to this function the handle is destroyed.
    Returns a tuple including status in first element and a description in second element"""

    global pBlade

    logger.debug('enter tearDownSession')

    sessions=pBlade.keys()
    regexp = re.compile(session)  

    for session in sessions :
        if regexp.search(session):
            try:
                pBlade[session].close()
                del pBlade[session]
                logger.debug("Removed %s from created handles!" % (session))
            except :
                logger.error("Could not remove %s from created handles!" % (session))
    logger.debug('leave tearDownSession')
    return        

def tearDownDevice(device):
    """This function closes the handles and removes it from the listed record. 
    After a call to this function the handle is destroyed.
    Returns a tuple including status in first element and a description in second element"""

    global pDevice

    logger.debug('enter tearDownDevice')

    try:
        pDevice[device].close()
        del pDevice[device]
        logger.debug("Removed %s from created handles!" % (device))
        logger.debug('leave tearDownDevice')
        return ('SUCCESS','Device handle %s removed' % device)      
    except :
        logger.error("Could not remove %s from created handles!" % (device))
        logger.debug('leave tearDownDevice')
        return ('ERROR','Device handle %s could not be removed' % device)  

def sendCommand(command, port = 23):
    """This function is the exported function for others to call when communication towards a 
    interactive remote shell is required.

    First: The function checks wether a handle is created for the remote machine accessing.
    If not a new handle is created.(Login sequense initiated!)
    Secondly: We execute the command. 

    Returns a tuple including status in first element and the response in the second element"""

    global pBlade

    logger.debug('enter sendCommand')

    session = 'telnet_port_%s' %  (port)    

    result = setUpSession(session, port)
    if (result[0] == 'ERROR' ): # could we setup new handle
        tearDownSession(session)
        return result
    else:
        logger.info("Sending command: %s, Session %s!" % (command, session))
        regexp1 = re.compile('reboot')
        regexp2 = re.compile('shutdown')
        if (regexp1.search(command) or regexp2.search(command) ):
            response = pBlade[session].Send(command) # On correct host
            tearDownSession(session)
        else:
            response = pBlade[session].senceive(command) 
            if (response[0]== 'ERROR'): # have we received anything
                logger.error('Failed to send command: %s on host: %s' %  (command, session))
                logger.debug('leave sendCommand')
                return  ('ERROR', 'Failed to send command: %s, Session: %s' %  (command, session))
            logger.debug("Command response: %s" % response)
            response = response.pop() 
            response = response.split(command,1) #remove command from response
            response = response.pop()
            #eolnans: Added for Jython
            # Platform independent split of lines
            response = os.linesep.join(response.splitlines()[1:])
            #response = response.split('\r\n', 1)
            #response = response.pop()
            logger.info("Command response: %s" % response)
        logger.debug('leave sendCommand')
        return ('SUCCESS', response)

def sendCommandRaw(command, user, passwd, address = '127.0.0.1', port = 23):
    """This function is the exported function for others to call when communication towards a 
    interactive remote shell is required.

    First: The function checks wether a handle is created for the remote machine accessing.
    If not a new handle is created.(Login sequense initiated!)
    Secondly: We execute the command. 

    Returns a tuple including status in first element and the response in the second element"""

    global pBlade

    logger.debug('enter sendCommandRaw')

    session = 'telnet_port_%s' %  (port)    

    result = setUpSessionRaw(session, address, port, user, passwd)
    if (result[0] == 'ERROR' ): # could we setup new handle
        tearDownSession(session)
        return result
    else:
        logger.info("Sending command: %s, Session %s!" % (command, session))
        regexp1 = re.compile('reboot')
        regexp2 = re.compile('shutdown')
        if (regexp1.search(command) or regexp2.search(command) ):
            response = pBlade[session].Send(command) # On correct host
            tearDownSession(session)
        else:
            response = pBlade[session].senceive(command) 
            if (response[0]== 'ERROR'): # have we received anything
                logger.error('Failed to send command: %s on host: %s' %  (command, session))
                logger.debug('leave sendCommandRaw')
                return  ('ERROR', 'Failed to send command: %s, Session: %s' %  (command, session))
            logger.debug("Command response: %s" % response)
            response = response.pop() 
            response = response.split(command,1) #remove command from response
            response = response.pop()
            #eolnans: Added for Jython
            # Platform independent split of lines
            response = os.linesep.join(response.splitlines()[1:])
            #response = response.split('\r\n', 1)
            #response = response.pop()
            logger.info("Command response: %s" % response)
        logger.debug('leave sendCommandRaw')
        return ('SUCCESS', response)

def sendCommandServer(command, device):
    """This function is the exported function for others to call when communication towards a 
    interactive remote shell is required.

    First: The function checks wether a handle is created for the remote machine accessing.
    If not a new handle is created.(Login sequense initiated!)
    Secondly: We execute the command. 

    Returns a tuple including status in first element and the response in the second element"""

    global pDevice

    logger.debug('enter sendCommandServer')

    result = setUpDevice(device)
    if (result[0] == 'ERROR' ): # could we setup new handle
        tearDownDevice(device)
        return result
    else:
        logger.info("Sending command:  %s to %s!" % (command, device))
        regexp1 = re.compile('reboot')
        regexp2 = re.compile('shutdown')
        if (regexp1.search(command) or regexp2.search(command) ):
            response = pDevice[device].Send(command) # On correct host
            tearDownDevice(device)
        else:
            response = pDevice[device].senceive(command) 
            if (response[0]== 'ERROR'): # have we received anything
                logger.error('Failed to send command: %s on host: %s' %  (command, device))
                logger.debug('leave sendCommandServer')
                return  ('ERROR', 'Failed to send command: %s on host: %s' %  (command, device))
            logger.debug("Command response: %s" % response)
            response = response.pop() 
            response = response.split(command,1) #remove command from response
            response = response.pop()
            #eolnans: Added for Jython
            # Platform independent split of lines
            response = os.linesep.join(response.splitlines()[1:])
            #response = response.split('\r\n', 1)
            #response = response.pop()
            logger.info("Command response: %s" % response)
        logger.debug('leave sendCommandServer')    
        return ('SUCCESS', response)

def listenOnDevice(device):
    """This function is the exported function for others to call when communication towards a 
    interactive remote shell is required.

    First: The function checks wether a handle is created for the remote machine accessing.
    If not a new handle is created.(Login sequense initiated!)
    Secondly: We execute the command. 

    Returns a tuple including status in first element and the response in the second element"""

    global pDevice

    logger.debug('enter listenOnDevice')

    result = setUpDevice(device)
    if (result[0] == 'ERROR' ): # could we setup new handle
        tearDownDevice(device)
        return result
    else:
        response = pDevice[device].receive() 
        if (response[0]== 'ERROR'): # have we received anything
            logger.error('Failed to listen on device: %s' %  (device))
            logger.debug('leave listenOnDevice')
            return  ('ERROR', 'Failed to listen on device: %s' %  (device))

        logger.debug("Device %s returns: %s" % (device,response[1]))
        logger.debug('leave listenOnDevice')    
        return response

###############################################################################
# cTELNET implementation
###############################################################################

class cTELNET:

    # Construction
    def __init__(self, timeOut = 30) :
        self.timeOut = timeOut
        self.tn_socket = None

    def openServerSession(self, strIpAddr, intPort, strServerUsr, strServerPwd, strUsr, strPwd, timeout = 10)  :

        logger.debug('enter openServerSession')
        
        pattern=(["""(Unknown host)""","""(Login :)""","""(login:)""","""(Password :)""","""(Password:)"""])
        loggedInPattern = ([targetData['ctrlBladePattern'], targetData['payloadBladePattern'], targetData['testPcPattern'], targetData['switchDevicePattern'], 
        """( Entering server port, ..... type \^z for port menu.)""", """Last login:"""])
        
        logger.info("Logging in to %s using port %s." % (strIpAddr, intPort))

        try : 
            self.tn_socket = telnetlib.Telnet(strIpAddr, intPort)
            idx, idy, idz = self.tn_socket.expect(pattern, timeout)
            if (idx == 1 or idx ==2  ):
                cmd = strServerUsr.strip()+'\n'
                self.tn_socket.write(cmd)
                idx, idy, idz = self.tn_socket.expect(pattern, timeout)
                logger.debug("Command: %s, Trigger pattern:%s, return: %s " % (cmd, idz, idx))
            if (idx == 3 or idx == 4):
                cmd = strServerPwd.strip()+'\n'
                self.tn_socket.write(cmd)
                idx, idy, idz = self.tn_socket.expect(loggedInPattern, timeout)
                logger.debug("Command: %s, Trigger pattern:%s, return: %s " % (cmd, idz, idx))
            if (idx == -1):
                logger.debug("Received unexpected pattern: %s, Could not log in to %s" % (idz, strIpAddr))
                return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")
            cmd = '\n'
            self.tn_socket.write(cmd)
            idx, idy, idz = self.tn_socket.expect(pattern, timeout)
            logger.debug("Command: %s, Trigger pattern:%s, return: %s " % (cmd, idz, idx))
            cmd = strUsr.strip()+'\n'
            self.tn_socket.write(cmd)
            idx, idy, idz = self.tn_socket.expect(pattern, timeout)
            logger.debug("Command: %s, Trigger pattern:%s, return: %s " % (cmd, idz, idx))
            if (idx == 3 or idx == 4):
                cmd = strPwd.strip()+'\n'
                self.tn_socket.write(cmd)
                idx, idy, idz = self.tn_socket.expect(loggedInPattern, timeout)
                logger.debug("Command: %s, Trigger pattern:%s, return: %s " % (cmd, idz, idx))
            if (idx == -1):
                logger.error("Received unexpected pattern: %s, Could not log in to %s" % (idz, strIpAddr)) 
                return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")
            logger.debug("Assumed logged in getting match for pattern %s using terminal server: %s port: %d " % (loggedInPattern[idx], strIpAddr, intPort))
            logger.debug('leave openServerSession')
            return ('SUCCESS','Device @'+strIpAddr+ ' connected!!') 
        except :
            logger.error('Can\'t connect to '+ strIpAddr+ "!!")
            logger.debug('leave openServerSession')
            return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")

    def openTelnetSession(self, strIpAddr, intPort, strUsr, strPwd,  timeout = 10)  :

        logger.debug('enter openTelnetSession')

        pattern=(["""(Login :)""","""(login:)""","""(Password)""","""(password)""", """(# )""", """(VIP Config CLI>)"""])
        loggedInPattern = ([targetData['ctrlBladePattern'], targetData['payloadBladePattern'], targetData['testPcPattern'], targetData['switchDevicePattern'],"""(# )""", """(VIP Config CLI>)"""])
        logger.info("Logging in to %s using port %s." % (strIpAddr, intPort))
        try :
            self.tn_socket = telnetlib.Telnet(strIpAddr, intPort)
            idx, idy, idz = self.tn_socket.expect(pattern, timeout)
            if (idx == 1 or idx ==2): 
                cmd=strUsr
                self.tn_socket.write(cmd)
                idx, idy, idz = self.tn_socket.expect(pattern, timeout)
                logger.debug("Command: %s, Trigger pattern:%s, return: %s " % (cmd, idz, idx))
            if (idx == 3 or idx ==4): 
                cmd = strPwd
                self.tn_socket.write(cmd)
                idx. idy, idz = self.tn_socket.expect(loggedInPattern, timeout)
                logger.debug("Command: %s, Trigger pattern:%s, return: %s " % (cmd, idz, idx))
            if (idx == -1):
                logger.error("Received unexpected pattern: %s, Could not log in to %s" % (idz, strIpAddr))
                logger.debug('leave openTelnetSession')
                return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")
            logger.debug("Assumed logged in getting match for pattern %s using IP address: %s port: %d " % (loggedInPattern[idx], strIpAddr, intPort))
            logger.debug('leave openTelnetSession')
            return ('SUCCESS','Device @'+strIpAddr+ ' connected!!') 
        except :
            logger.error('Can\'t connect to '+ strIpAddr+ "!!")
            logger.debug('leave openTelnetSession')
            return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")

    def senceive(self, strCmd) :

        logger.debug('enter senceive')
        
        pattern = ( [targetData['ctrlBladePattern'], targetData['payloadBladePattern'], targetData['testPcPattern'], targetData['switchDevicePattern'],"""(# )""", """(VIP Config CLI>)"""])
        try :
            cmd = strCmd.strip()+'\n'
            self.tn_socket.write(strCmd)
            idx, idy, idz = self.tn_socket.expect(pattern, self.timeOut)
            if idx == -1:
                logger.error("Matched data: %s" % (idz))
                logger.debug('leave senceive')
                return ('ERROR', 'Timeout or no match after executing: '+ strCmd + '!!')
            logger.debug("Command: %s, Trigger pattern: %s " %  (strCmd, pattern[idx])) 
            ret = idz
            ret = ret.strip()
            logger.debug('leave senceive')
            return ['SUCCESS', ret] 
        except :
            logger.debug('leave senceive')
            return ('ERROR', 'Error after executing: '+ strCmd + '!!')

    def receive(self) :

        logger.debug('enter receive')
        try : 
            ret = self.tn_socket.read_until('\n', self.timeOut)
            logger.debug('leave receive')
            return ('SUCCESS', ret) 
        except :
            logger.debug('leave receive')
            return ('ERROR', '')
        
    def Send(self, strCmd):
        
        logger.debug('enter Send')
        try:
            self.tn_socket.write(strCmd)
            logger.debug('leave Send')
            return ['SUCCESS', ''] 
        except:
            logger.debug('leave Send')
            return ('ERROR', 'Error sending data!!')

    def setTimeOut (self, timeOut):

        logger.debug('enter setTimeOut')

        try:
            logger.debug("Timeout changed from: %s  to: %s" % (self.timeOut, timeOut))
            self.timeOut = timeOut
            logger.debug('leave setTimeOut')
            return ('SUCCESS', 'Timeout changed')
        except :
            logger.debug('leave setTimeOut')
            return ('ERROR', 'New timeout could not be set')   

    def getTimeOut (self):
                
        logger.debug('enter getTimeOut')

        try:
            logger.debug("Returning timeout" % (self.timeOut))
            logger.debug('leave getTimeOut')    
            return ('SUCCESS', self.timeOut)
        except :
            logger.debug('leave getTimeOut')
            return ('ERROR', 'Could not return timeout')
        
    def close (self):
        if self.tn_socket:
            self.tn_socket.close()


##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':

    import common.target.target_data as target_data
    import common.target.common_lib.booking_lib as booking_lib
    node=booking_lib.checkBooking()
    targetData=target_data.setTargetHwData(node)    
    st_env_lib.executeFunction(sys.argv)

    st_env_lib.setUp()
    ###########TEST AREA START###############

    #device = 'SC_2_1'
    port = 7700
    #print sendCommandServer('ps', device)
    #print sendCommandServer('ls /', device)
  
    print sendCommand('info', port)
    print sendCommand('help', port)

    ###########TEST AREA END###############
    st_env_lib.tearDown()




