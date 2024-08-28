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
   %CCaseFile:  ssh_lib.py %
   %CCaseRev:   /main/R1A/1 % 
   %CCaseDate:  2007-11-21 % 

   Description:
   This module acts as an interactive shell used for communication
   towards remote machines.

   The module creates objects of the class instance cSSH in ssh_utility.
   One instance is created per 
   hw. The handles are created the first time a user wants to open
   a ssh tunnel. The handle is stored and reused upon a new request.
'''

import string
import os
import sys
import time
import re
import getopt

from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System
from se.ericsson.jcat.omp.util import Tools

import omp.tf.dataprovider.sshlibdata as sshdata

#######PLATFORM DEPENDENT IMPLEMENTATION CLASSES########
if sys.platform[:4] == 'java':
    from _ssh_lib_impl_j import cSSH, cSCP

#This means ordinary CPython
else:
     from _ssh_lib_impl_c import cSSH, cSCP

#############GLOBALS##################
pBlades = {}    # a dictionary containing handles to the blades
regexps={} # a dictionary containing all used regexps in compiled form
data = sshdata.sshlibdata()


###############################################################################
# setUp / tearDown
###############################################################################

def setData(datap):
    global data
    data = datap
    _ssh_lib_impl_j.setData(data)

def setUp(subrack, slot, number, sut):
    """This function fetches required data that this library requires to work"""

    global logger
    global logLevel
    logger = Logger.getLogger('ssh_lib')
    logLevel = System.getProperty("jcat.logging")
    logger.setLevel(Level.toLevel(logLevel))
    global node2prompt
    node2prompt = {}
    global clearNode2prompt
    clearNode2prompt = True
    
    setConfig(subrack, slot, number)
    global currentSut
    currentSut = sut
    data.initialize()
    global regexps
    regexps={'gwhost':re.compile(data.getTargetPcPattern()),
         'NBI':re.compile('NBI'),
         'reboot -f':re.compile('reboot -f'),
         'nohup reboot -f':re.compile('nohup reboot -f'),
         'reboot':re.compile('reboot'),
         'shutdown':re.compile('shutdown')}
    
    logger.debug("ssh_lib: Initiating!")
    
    return
    
def tearDown():
    """This function removes handles"""
    tearDownHandles()
    logger.debug("ssh_lib: Bye bye !!")
    return

def setConfig(subrack, slot, number, useVipOam=False):
    logger.debug("Starting setConfig")
    global activeControllerSubRack
    global activeControllerSlot
    global activeControllerNumber
    global vipOam
    
    tearDownHandles()
    activeControllerSlot = slot
    activeControllerSubRack = subrack
    activeControllerNumber = number
    vipOam = useVipOam
    logger.debug("SetConfig completed")
    
def getConfig():
    return (activeControllerSubRack, activeControllerSlot, activeControllerNumber)

def setClearNode2prompt(action):
    global clearNode2prompt
    clearNode2prompt = action

def getClearNode2prompt():
    return clearNode2prompt

def getUseVipOam():
    return vipOam

def getSeparator():
    return currentSut.getSeparator()

def getPrompt(subrack, slot):
    logger.debug("Starting getPrompt")
    
    activeController = "ctrl%d" % (getConfig()[2])
    node = 'blade_%s_%s' % (subrack, slot)
    if node in node2prompt.keys():
        logger.debug("Prompt already known")
        return node2prompt[node]
    else:
        logger.debug("Prompt not known")
        if vipOam:
            activeControllerIpAdress=data.getOamVip()
        else:
            activeControllerIpAdress=data.getScIp(activeController)
        
        if ":" in activeControllerIpAdress :
            activeControllerIpAdress, activeControllerIpPort = data.getScIp(activeController).split(":")
        else :
            activeControllerIpPort=22
            
        handle = cSSH()
        result = handle.openSystemController(activeControllerIpAdress, activeControllerIpPort, data.getUsername(), data.getPassword())
        logger.debug("result0 = %s" % (result[0]))
        logger.debug("result1 = %s" % (result[1]))
        if result[0] == 'SUCCESS':
            result = handle.connectToBlade(data.getInternalIp(node))
            logger.debug("result0 = %s" % (result[0]))
            logger.debug("result1 = %s" % (result[1]))
        else:
            logger.debug("leave getPrompt - Could not access %s" % activeControllerIpAdress)
            handle.close()
            return None

        if result[0] == 'SUCCESS':
            # TODO:
            # Uncomment the line below when we know for sure that
            # Everybody is using R2D10 or higher of JCAT_extensions
            #prompt = handle.getMatchedPrompt()
            result = handle.senceive('hostname')

        if result[0] == 'SUCCESS':
            node2prompt[node] = result[1]
            logger.debug("GetPrompt completed")
            handle.close()
            return node2prompt[node]
        else:
            logger.debug("GetPrompt completed")
            handle.close()
            return None
        
def tearDownHandles():
    """This function closes the all handles and removes it from the listed record.
    After a call to this function all the existing handles are destroyed.
    Returns a tuple including status in first element and a description in second element"""

    global pBlades
    global node2prompt
    global clearNode2prompt

    logger.debug("Starting tearDownHandles")

    #Check if we should clear node2prompt or not.
    if (clearNode2prompt):
        logger.debug('We want to clear the node2prompt list in tearDownHandles.')
        node2prompt = {}

    blades=pBlades.keys()
    blades.sort() # Sort the blades
    
    for blade in blades :
        try:
            logger.debug('Removing blade : %s' % (blade))
            logger.debug('tearDownHandles: Sending pkill to the rlogin sessions on blade : %s '  % (blade))
            try:
                 pBlades[blade].setTimeOut(10)
                 result=pBlades[blade].Send('hostname; pkill rlogin; ps -ef | grep rlogin | grep -v grep')
                 logger.debug('Command result --> %s <--' % result[1])
            except:
                 logger.warn("ssh_lib: Unable to close rlogin sessions. Connection could already be closed.")
            
            try:
                pBlades[blade].close()
            except:
                logger.warn("ssh_lib: Unable to close connection. Just removing its handle.")

        except:
            logger.error("ssh_lib: Could not remove %s from created handles!" % (blade))
            
    #Clear the pBlades dictionary        
    pBlades = {}

    logger.debug("TearDownHandles completed")
    return

###############################################################################
#Lib methods
###############################################################################

def setUpBlade(blade):
    """This function will login on a selected blade and put the created handle in 
    in the dictionary pBlades. This handle will be used in thr SendCommand function.
    Returns a tuple including status in first element and a description in second element"""

    global pBlades

    logger.debug("Starting bladeSetup")
    activeController = "ctrl%d" % (getConfig()[2])  
        
    if (pBlades.has_key(blade)==False): #handle already created?
        logger.debug("Connection to  %s!" % (blade))
        pBlades[blade] = cSSH()
        if(blade == 'blade_9_9'): # log in to testpc
            logger.debug("setUpBlade - testpc")
            # Handle ports in target.xml
            activeControllerIpAdress=data.getTestPcIp()
            if ":" in activeControllerIpAdress :
                activeControllerIpAdress, activeControllerIpPort = data.getTestPcIp().split(":")
            else :
                activeControllerIpPort=22
            status = pBlades[blade].openSystemController(activeControllerIpAdress, activeControllerIpPort, data.getUsername(), data.getPassword())
            if (status[0] == 'ERROR' ):
                logger.error("Can not connect to IP: %s! Verify system" % (data.getTestPcIp()))
                logger.debug("Terminating setUpBlade")
                return ('ERROR', 'Can not connect to testpc')
            logger.debug("SetUpBlade completed.")    
            return ('SUCCESS','Connection to testpc created') 
        if (pBlades[blade]): # log in to external IP interface
            # Handle ports in target.xml
            if vipOam:
                activeControllerIpAdress = data.getOamVip()
            else:
                activeControllerIpAdress=data.getScIp(activeController)
            if ":" in activeControllerIpAdress :
                activeControllerIpAdress, activeControllerIpPort = activeControllerIpAdress.split(":")
            else :
                activeControllerIpPort=22
            logger.debug("setUpBlade - log in to external IP interface: %s" % activeControllerIpAdress)
            status = pBlades[blade].openSystemController(activeControllerIpAdress, activeControllerIpPort, data.getUsername(), data.getPassword())
            if (status[0] == 'ERROR' ):
                logger.error("Can not connect to: %s! Verify system" % (blade))
                pBlades[blade].Close()
                del pBlades[blade]
                logger.debug("Terminating setUpBlade")
                return ('ERROR', 'Can not connect to: ' +blade+ '. Verify system')
            else:
                logger.debug("Logged in to ip address: %s!" % (activeControllerIpAdress))        
                logger.debug("setUpBlade - log in to internal IP interface: %s" % data.getInternalIp(blade))
                status=pBlades[blade].connectToBlade(data.getInternalIp(blade)) # log in internal IP interface
                if (status[0] == 'ERROR' ):
                    pBlades[blade].Close()
                    del pBlades[blade]
                    logger.error("Can not log in to ip address: %s!" % (data.getInternalIp(blade)))
                    logger.debug("Terminating setUpBlade")
                    return ('ERROR', 'Can not connect to: ' +blade+ '. Verify system')
                else:
                    logger.debug("Logged in to ip address: %s!" % (blade))
                    logger.debug("SetupBlade Completed")
                    return ('SUCCESS','Connected to : ' +blade)
    else:
        logger.debug("SetUpBlade completed.")
        return ('SUCCESS','Using existing connection.')

def setUpNBI ():
    """
    NOTE: This function is not updated to work with vip_oam and cannot be tested at this time
    Will not work as is, needs to be updated with the samae 'pattern' as setUpBlade().
      
    This function will login on the North Bound interface and put the created handle in 
    in the dictionary pBlades. This handle will be used in the SendCommandNBI function.
    Returns a tuple including status in first element and a description in second element
    """

    global pBlades

    logger.debug("Starting setUpNBI")

    blades=pBlades.keys()
    regexp = re.compile('NBI')  

    nbi = 'nbi'

    for pBlade in blades :
        if regexp.search(pBlade):
            nbi = pBlade    

    if (pBlades.has_key(nbi)==False): #handle already created?
        logger.debug("Connecting to NBI!")
        handle = cSSH()
        if (handle): # log in NBI interface
            # Handle ports in target.xml
            NBIpAdress=data.getNbIp()
            if ":" in activeControllerIpAdress :
                NBIpAdress, NBIpAdressPort = data.getNbIp().split(":")
            else :
                NBIpAdressPort=22
            status = handle.openSystemController(NBIpAdress, NBIpAdressPort, data.getUsername(), data.getPassword())

            if (status[0] == 'ERROR' ):
                logger.debug("Terminating setUpNBI")
                return ('ERROR', 'Can not create a connection to NBI. Verify system.')
            else:
                try:
                    result = handle.senceive('hostname')
                    if (result[0] == 'SUCCESS' ) :
                        logger.debug("NBI active on blade: %s" % (result[1]))
                except:
                    handle.Close()
                    logger.error("Can not log in to IP address: %s" % (data.getNbIp()))
                    logger.debug("Terminating setUpNBI")
                    return ('ERROR', 'Can not create a connection to NBI. Verify system.')
                else:
                    subrack, slot = result[1].split(getSeparator())[1:]
                    blade = 'blade_%s_%s_NBI' %  (subrack, slot)
                    pBlades[blade] = handle
                    logger.debug("Connection successful to IP address: %s" % (data.getNbIp()))
                    logger.debug("SetUpNBI Completed.")
                    return ('SUCCESS','Connection successful to NBI')
    else:
        logger.debug("SetUpNBI completed.")
        return ('SUCCESS','Using existing connection.')


def tearDownBlade(blade):
    """This function closes the handles and removes it from the listed record. 
    After a call to this function the handle is destroyed.
    Returns a tuple including status in first element and a description in second element"""

    global pBlades

    logger.debug("Starting tearDownBlade")

    subrack, slot = blade.split('_')[1:] 
    a_subrack, a_slot = getConfig()[:2]
    if (int(subrack) == a_subrack and int(slot) == a_slot ): # if the blade is the active controller remove all handles
        logger.debug("the blade is the active controller remove all handles")
        tearDownHandles()

    blades=pBlades.keys()
    regexp = re.compile(blade)  

    for pBlade in blades :
        if regexp.search(pBlade):
            try:
                logger.debug("We remove the connection for blade %s " % (pBlade))
                logger.debug('tearDownBlade: Sending pkill to the rlogin sessions on blade : %s '  % (blade))
                try:
                     pBlades[blade].setTimeOut(10)
                     result=pBlades[blade].Send('hostname; pkill rlogin; ps -ef | grep rlogin | grep -v grep')
                     logger.debug('Command result --> %s <--' % result[1])
                except:
                     logger.warn("ssh_lib: Unable to close rlogin sessions. Connection could already be closed.")            

                try:
                    pBlades[blade].close()
                except:
                    logger.warn("ssh_lib: Unable to close connection.")
                    
                del pBlades[blade]
                logger.debug("ssh_lib: Removed %s from created handles!" % (blade))
            except :
                logger.error("Could not remove %s from created handles!" % (pBlade))
    logger.debug("Terminating tearDownBlade")
    return        

def tearDownBladeIPMI(command):

    global pBlades

    logger.debug("Starting tearDownBladeIPMI")

    m =  re.findall('([0-9.])', command)
    ipBlade = string.join(m,'')
    blade = data.getIpmiAddress(ipBlade)

    tearDownBlade(blade)
    logger.debug("TearDownBladeIPMI completed.")
    return   

def setTimeout(timeout, subrack=0, slot=0):
    """This function is used to change the timeout used when using SendCommand()
    This will be the new timeout setting valid for the handle """

    global pBlades

    logger.debug("Starting setTimeout")
    if (subrack==0 and slot==0): # redirect 
        subrack, slot = getConfig()[:2]

    blade = 'blade_%s_%s' %  (subrack, slot)

    result = setUpBlade(blade)
    if (result[0] == 'ERROR' ): # could we setup new handle
        return result

    if (pBlades.has_key(blade)):
        response = pBlades[blade].setTimeOut(timeout)
        logger.debug("SetTimeout Completed.")
        return response
    else:
        logger.debug("Terminating setTimeout")
        return ('ERROR', 'No existing connection to: '+blade) 

def getTimeout(subrack=0, slot=0):
    """This function is used to fetch the timeout used when using SendCommand() """
    global pBlades

    logger.debug("enter getTimeout")

    if (subrack==0 and slot==0): # redirect 
        subrack, slot = getConfig()[:2]

    blade = 'blade_%s_%s' %  (subrack, slot)

    result = setUpBlade(blade)
    if (result[0] == 'ERROR' ): # could we setup new handle
        return result

    if (pBlades.has_key(blade)):
        response = pBlades[blade].getTimeOut()
        logger.debug("leave getTimeout")
        return response
    else:
        logger.debug("leave getTimeout")
        return ('ERROR', 'No existing connection to: '+blade) 

def getHostName (blade):
    """This function is used internaly as a validation that correct blade is accessed 
    before sending the command wanted.
    Returns a tuple including status in first element and a description in second element"""

    global pBlades
    global regexps

    logger.debug("Starting getHostName")

    if (pBlades.has_key(blade)):
        b_subrack, b_slot = blade.split('_')[1:]  
        oldTimeout = getTimeout(b_subrack, b_slot)
        setTimeout(5, b_subrack, b_slot )
        response = pBlades[blade].senceive('hostname')
        if (response[0] =='SUCCESS'):
            if (response[1] == ""):
                time.sleep(1)
                response = pBlades[blade].senceive('hostname')
                if (response[0] =='SUCCESS'):
                    if (response[1] == ""):
                        time.sleep(1)
                        response = pBlades[blade].senceive('hostname')
            #response[1] = response[1].split('\r\n',1) #remove command from response
            #response[1] = response[1].pop()
        if (response[0] =='SUCCESS'):
            logger.debug("Getting hostname on: %s response: %s" % (blade, response[1]))
        setTimeout(oldTimeout[1], b_subrack, b_slot )
        if (b_subrack == '9' and b_slot == '9'): # if  'blade_9_9'
            if ((response[0] == 'SUCCESS') and regexps['gwhost'].search(response[1])):
                logger.debug("GethostName Completed")
                return ('SUCCESS', blade)
            else:
                logger.debug("Terminating getHostName")
                return ('ERROR', 'Validation of host failed: ' +blade)

        prompt = getPrompt(b_subrack, b_slot) # get the prompt por the blade
        logger.debug("prompt = %s" % (prompt))
        # Verify that the hostname returned can be found in the prompt
        # This is to avoid executing a command on another blade than the 
        # desired one.
        if ((response[0] == 'ERROR' or prompt ==  None ) or not re.search(prompt ,response[1])):    
            logger.error("Unexpected or empty response from: %s!" % (blade))
            logger.debug("Terminating getHostName")
            return ('ERROR', 'No response from: ' +blade+'. Verify system.')       
        else:
            logger.debug("Success validating hostname on: %s!" % (blade))
            logger.debug("GetHostName completed")
            return ('SUCCESS', blade)
    else:
        logger.debug("Terminating getHostName")
        return ('ERROR', 'No existing connection to: '+blade) 

def sendCommandNBI (command):
    """This function is the exported function for others to call when communication towards a 
    interactive remote shell is required. """

    global pBlades
    global regexps

    logger.debug("enter sendCommandNBI")

    result = setUpNBI()
    if (result[0] == 'ERROR' ): # could we setup new handle
        return result

    blades=pBlades.keys()
    for pBlade in blades :
        if regexps['NBI'].search(pBlade):
            nbi = pBlade

    subrack, slot = nbi.split('_')[1:3] 
    blade ='blade_%s_%s' % (subrack, slot)
  
    logger.debug("Sending command:  %s on North Bound Interface active on %s!" % (command, blade)) 
    if (regexps['reboot -f'].search(command) or regexps['nohup reboot -f'].search(command) ):
        response = pBlades[nbi].Send(command)
        response = response.pop()
        logger.debug("Bytes written: %s" % response)
        tearDownBlade(blade)
        logger.debug("leave sendCommandNBI")
        return ('SUCCESS', response)

    response = pBlades[nbi].senceive(command)
    if (response[0]== 'ERROR'): # have we received anything
        logger.error('Failed to send command: %s on host: %s. Verify system.' %  (command, blade))
        tearDownBlade(blade)
        logger.debug("leave sendCommandNBI")
        return  ('ERROR', 'Failed to send command: %s on NBI. Verify system' %  (command))
    logger.debug("Command response: %s" % response)
    response = response.pop() # Remove SUCCESS 
    #eolnans: Added for Jython
    # The stripping of command and prompt is now done in cSSH
    #response = response.split(command,1) #remove command from response
    #response = response.pop()
    #response = str(response.splitlines()[1:])#split('\r\n', 1)
    #response = response.pop()

    logger.debug("Command response: %s" % response)
 
    if (regexps['reboot'].search(command) or regexps['shutdown'].search(command)):
        tearDownBlade(blade)

    logger.debug("leave sendCommandNBI")
    return ('SUCCESS', response)

def resetInternalConnectionCommand():
    activeController = "ctrl%d" % (getConfig()[2])
    if vipOam:
        activeControllerIpAdress = data.getOamVip()
    else:
        activeControllerIpAdress=data.getScIp(activeController)
    if ":" in activeControllerIpAdress :
        activeControllerIpAdress, activeControllerIpPort = activeControllerIpAdress.split(":")
    else :
        activeControllerIpPort=22
    ssh_j = cSSH()
    status = ssh_j.openSystemController(activeControllerIpAdress, activeControllerIpPort, data.getUsername(), data.getPassword())
    if (status[0] == 'ERROR' ):
        logger.error("Can not create a connection to: %s!" % (activeControllerIpAdress))
        ssh_j.Close()
    else:
        ssh_j.resetInternalConnectionCommand()
        logger.info("Internal connection command renewed!")
        ssh_j.Close()
        tearDownHandles()

def sendCommand(command, subrack=0, slot=0):
    """This function is the exported function for others to call when communication towards a 
    interactive remote shell is required.

    First: The function checks wether a handle is created for the remote machine accessing.
    If not a new handle is created.(Login sequense initiated!)
    Secondly: We validate that we are logged in to the correct blade.
    Third: We execute the command. 

    Returns a tuple including status in first element and the response in the second element"""

    global pBlades
    global regexps

    logger.debug("enter sendCommand")

    if (subrack==0 and slot==0): # redirect 
        subrack, slot = getConfig()[:2]

    blade = 'blade_%s_%s' %  (subrack, slot)

    result = setUpBlade(blade)
    if (result[0] == 'ERROR' ): # could we setup new handle
        return result
    logger.debug("Sending command: hostname to %s!" %  blade)
    hostname=getHostName(blade) # Is the shell active on the correct blade
    logger.debug("Command response: %s" % hostname[1])
    if (hostname[0] == 'ERROR' or hostname[1] != blade):
        tearDownBlade(blade)
        logger.error('Trying to execute: %s on host: %s' %  (command, hostname[1]))
        logger.debug("leave sendCommand")
        return  ('ERROR', 'Trying to execute: %s on host: %s' %  (command, hostname[1]))
    else:
        logger.info("Sending command: %s to %s!" % (command, blade))
        if (regexps['reboot -f'].search(command) or regexps['nohup reboot -f'].search(command) ):
            response = pBlades[blade].Send(command)
            response = response.pop()
            logger.debug("Bytes written: %s" % response)
            tearDownBlade(blade)
            logger.debug("leave sendCommand")
            return ('SUCCESS', response)
        response = pBlades[blade].senceive(command)
	
        if (response[0]== 'ERROR'): # have we received anything
            logger.error('Failed to send command: %s on host: %s' %  (command, blade))
            tearDownBlade(blade)
            logger.debug("leave sendCommand")
            return  ('ERROR', 'Failed to send command: %s on host: %s. Verify system' %  (command, blade))
        logger.info("Command response: %s" % response)
        response = response.pop() # Remove 'SUCCESS'
	
	logger.debug("Command response: %s" % response)

        if (regexps['reboot'].search(command) or regexps['shutdown'].search(command) ):
            tearDownBlade(blade)

        logger.debug("leave sendCommand")
        return ('SUCCESS', response)


def sendRawCommand(host, cmd, user, psw,timeout = 30, port = 22):
    """
    This function is the exported function for others to call when
    communication towards an interactive remote shell is required.

    Returns a tuple including status in first element and the response
    in the second element
    """
    logger.debug("enter sendRawCommand")

    pHandle = cSSH(timeout)

    result = pHandle.openSystemController(host, port, user, psw)
    if result[0] == 'ERROR':
       pHandle.close()
       logger.error("Could not log in on : %s@%s" % (user, host))
       logger.debug("leave sendRawCommand")
       return result

    logger.info("Sending Raw command: %s to %s!" % (cmd, host))
    result = pHandle.senceive(cmd)
    if result[0] == 'ERROR':
       pHandle.close()
       logger.error("Could not execute remote command: %s" % (cmd))
       logger.debug("leave sendRawCommand")
       return result

    logger.info("Command response: %s" % result)
    result = result.pop() # Remove 'SUCCESS'
    #eolnans: Added for Jython
    # The stripping of command and prompt is now done in cSSH
    #result = result.split(cmd,1) #remove command from response
    #result = result.pop()
    #result = result.split('\r\n', 1)
    #result = result.pop()
    
    logger.debug("Command response: %s" % result)

    pHandle.close()
    logger.debug("leave sendRawCommand")
    return ('SUCCESS', result)


def loginTest (subrack, slot, attempts = 1, user = '' , pwd = '' ):
    logger.debug("enter loginTest")

    if user =='':
        user=data.getUsername() 

    if pwd =='':
        pwd=data.getPassword() 

    activeController = "ctrl%d" % (slot)  

    logger.info('Logging in using user: %s, password: %s on controller SC_%s_%s' % (user, pwd, subrack, slot))

    if vipOam:
        activeControllerIpAdress = data.getOamVip()
    else:
        activeControllerIpAdress=data.getScIp(activeController)
    # Handle ports in target.xml
    if ":" in activeControllerIpAdress :
        activeControllerIpAdress, activeControllerIpPort = activeControllerIpAdress.split(":")
    else :
        activeControllerIpPort=22

    handle = cSSH() 
    connectionTimeout = 15
    result = handle.openSystemController(activeControllerIpAdress, activeControllerIpPort, user,  pwd, attempts, connectionTimeout)
    handle.close()

    logger.debug("leave loginTest")
    return result

###############################################################################
# Method for binding payload addresses to controller ports
###############################################################################

def bindAddresses(blade ,localPort, destinationPort):
    """This function will set up a ssh tunnel to an internal adress (via one of the controller nodes) directly from the test machine
       This is needed for communicating with the LoadClient. """

    global pBlades

    logger.debug("enter bindAddresses")

    activeController = "ctrl%d" % (getConfig()[2]) 

    tunnelKey = '%s_%s' % (blade, destinationPort)

    if (pBlades.has_key(tunnelKey)==False): #handle already created?
        pBlades[tunnelKey] = cSSH()
        if (pBlades[tunnelKey]): 
            externalAddress=data.getScIp(activeController)
            try: 
                internalAddress = data.getInternalIp(blade)
            except:
                internalAddress = blade
            
            status = pBlades[tunnelKey].createTunnel(externalAddress, internalAddress, localPort, destinationPort,  timeout = 20)
            if (status[0] == 'ERROR' ):
                logger.error("SSH tunnel unsuccessfully created for: %s" % (tunnelKey))
                logger.debug("leave bindAddresses")
                return ('ERROR', 'Can not set up ssh tunnel for ' + blade)
            logger.debug("SSH tunnel successfully created for: %s" % (tunnelKey))
            logger.debug("leave bindAddresses")
            return ('SUCCESS','SSH tunnel set up!!!')
    else:
        logger.debug("Using existing ssh tunnel: %s" % (tunnelKey))
        logger.debug("leave bindAddresses")
        return ('SUCCESS','Tunnel already successfully set up')


###############################################################################
# Method for reading a file within the cluster using tunnel
###############################################################################

def readFile(blade, localPort, fileName, request='cat'):

    logger.debug("enter readFile")

    result = setUpBlade(blade)
    if (result[0] == 'ERROR' ): # could we setup new handle
        return result
    command='cat %s' % (fileName)
    response = pBlades[blade].senceive(command)
    
    # added by enavnac for JCat (cat command returns nothing if the expected result is a single line text)
    #(in for ex,tc_06006. just  a work around, not the best fix)	
    if (response[1]== ''): # have we received anything
        command='more %s' % (fileName)
	response = pBlades[blade].senceive(command)

    if (response[0]== 'ERROR'): # have we received anything
        logger.error('Can not read file: %s on subrack: %s' % (fileName, blade))
        tearDownBlade(blade)
        logger.debug("leave readFile")
        return ('ERROR', 'Can not read file: %s on blade: %s  ' % (fileName, blade))
    logger.debug("Command response: %s" % response)
    logger.debug("leave readFile")
    return ['SUCCESS', response[1]]
        
def remoteCopy(file, destination, timeout = 30, numberOfRetries = 5):
    logger.debug("enter remoteCopy")
    
    activeController = "ctrl%d" % (getConfig()[2])
    if vipOam:
        activeControllerIpAdress = data.getOamVip()
    else:
        activeControllerIpAdress=data.getScIp(activeController)  

    logger.info("Copying file: %s to %s @ %s!" % \
    (file, destination, activeControllerIpAdress))
    pBlades = cSCP(timeout)
    # Handle ports in target.xml
    if ":" in activeControllerIpAdress :
        activeControllerIpAdress, activeControllerIpPort = activeControllerIpAdress.split(":")
    else :
        activeControllerIpPort=22

    for i in range(numberOfRetries):
        status = pBlades.copyFileRemoteTo(activeControllerIpAdress, activeControllerIpPort , data.getUsername(), data.getPassword(), file, destination)
        if (status[0] != 'SUCCESS'):
            logger.error("Could not copy file: %s @ %s to %s! Trying again" % (file, destination, activeControllerIpAdress))  
            logger.debug("leave remoteCopy")
        else:
            break            
    if (status[0] != 'SUCCESS'):
        return ('ERROR', 'Can not copy file to '+ activeController)
    pBlades.close()
    logger.debug('File copied')
    logger.debug("leave remoteCopy")
    return ('SUCCESS','File copied')

def remoteCopyFrom(file, destination, timeout = 30):
    logger.debug("enter remoteCopyFrom")

    activeController = "ctrl%d" % (getConfig()[2])  
    if vipOam:
        activeControllerIpAdress = data.getOamVip()
    else:
        activeControllerIpAdress=data.getScIp(activeController)
    
    logger.info("Copying file: %s @ %s to %s!" % \
    (file, activeControllerIpAdress,  destination))
    pBlades = cSCP(timeout)
    # Handle ports in target.xml
    if ":" in activeControllerIpAdress :
        activeControllerIpAdress, activeControllerIpPort = activeControllerIpAdress.split(":")
    else :
        activeControllerIpPort=22

    status = pBlades.copyFileRemoteFrom(activeControllerIpAdress, activeControllerIpPort , data.getUsername(), data.getPassword(), file, destination)
    pBlades.close()
    if (status[0] == 'ERROR' ):
        logger.error("Could not copy file: %s @ %s to %s!" % (file, activeControllerIpAdress, destination))    
        logger.debug("leave remoteCopyFrom")
        return ('ERROR', 'Can not copy file from '+ activeController)
    logger.debug('File copied')
    logger.debug("leave remoteCopyFrom")
    return ('SUCCESS','File copied')

def sCopy(file, host, destpath, user, passwd, timeout = 30):
    logger.debug("enter sCopy")

    logger.debug("Copying file: %s to %s @ %s!" % (file, destpath, host))
    pBlades = cSCP(timeout)
    status = pBlades.copyFileRemoteTo(host ,22 , user, passwd, file, destpath)
    pBlades.close()
    if (status[0] == 'ERROR' ):
        logger.error("Could not copy file: %s to %s @ %s!" % (file, destpath, host))
        logger.debug("leave sCopy")
        return ('ERROR', 'Can not copy file to '+ host)
    logger.debug('File copied')
    logger.debug("leave sCopy")
    return ('SUCCESS','File copied')

def sCopyHere(file, host, destpath, user, passwd, timeout = 30):
    logger.debug("enter sCopyHere")

    logger.debug("Copying file: %s @ %s to %s !" % (file, host, destpath))
    pBlades = cSCP(timeout)
    status = pBlades.copyFileRemoteFrom(host ,22 , user, passwd, file, destpath)
    pBlades.close()
    if (status[0] == 'ERROR' ):
        logger.error("Could not copy file: %s @ %s to %s!" % (file, host,destpath))
        logger.debug("leave sCopyHere")
        return ('ERROR', 'Can not copy file to '+ host)
    logger.debug('File copied')
    logger.debug("leave sCopyHere")
    return ('SUCCESS','File copied')

def waitForConnection(subrack, slot, timeout):
    logger.debug("enter waitForConnection")
    timeToTimeout = time.time() + timeout
    while True:
        if isSshPortOpen(subrack, slot):
            setTimeout(5)
            cmdResult = sendCommand("hostname", subrack, slot)
            if cmdResult[0] == 'SUCCESS':
                result = ['SUCCESS', True]
                break
            else:
                if time.time() < timeToTimeout:
                    time.sleep(10)
                else:
                    result = ['SUCCESS', False]
                    break
        else:
            if time.time() < timeToTimeout:
                time.sleep(10)
            else:
                result = ['SUCCESS', False]
                break
            
    tearDownHandles()
    logger.debug("leave waitForConnection")
    return result

def waitForNoConnection(subrack, slot, timeout):
    logger.debug("enter waitForNoConnection")
    timeToTimeout = time.time() + timeout
    while True:
        if isSshPortOpen(subrack, slot):
            if time.time() < timeToTimeout:
                time.sleep(10)
            else:
                result = ['SUCCESS', False]
                break
        else:
            result = ['SUCCESS', True]
            break
    tearDownHandles()
    logger.debug("leave waitForNoConnection")
    return result

def isSshPortOpen(subrack, slot):
    if slot <= 2:
        return Tools.isPortOpen(data.getScIp('ctrl' + str(slot)), 22)
    else:
        result = sendCommand("netcat -z " + 'blade_' + data.getInternalIp(str(subrack) + '_' + str(slot)) + " 22 ; echo $?")
        return result[1] == '0'

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print "Can not run stand alone at the moment"



