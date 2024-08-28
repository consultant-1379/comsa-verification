#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2008 All rights reserved.
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
   %CCaseFile:  netconf_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2008-03-18 %

   Description:
   This module acts as an interface used for communication
   towards the netconf interface available on the movable IP (MIP) address.

   The module exports functions for running command on the remote machine

'''

import sys
import os
import socket
import re
import struct
import time
import string
import base64
import xml.dom.minidom as dom 

########NODE CONFIGURATION DATA##########
try:
    import common.target.target_data as target_data
except Exception, e:
    import omp.target.target_data as target_data
    
#########COMMON USED RESOURCES##########
#import common.target.common_lib.lib as lib
#import st_env_lib as st_env_lib

try:
    import common.target.common_lib.logger_lib as logger_lib
except Exception, e:
    import omp.tf.logger_lib as logger_lib

    
if sys.platform[:4] == 'java':
    import _netconf_lib_impl_j as netconf_lib_impl
else:
    import _netconf_lib_impl_c as netconf_lib_impl
    

    
#############GLOBALS##################
targetData=target_data.data    # a dictionary containing hardware specific information
eod = ']]>]]>'
#############################################################################################
# setUp / tearDown
#############################################################################################

def setUp():

    logger_lib.logMessage("netconf_lib: Initiating!", logLevel='debug')
    return
    

def tearDown():
 
    logger_lib.logMessage("netconf_lib: Bye bye !!", logLevel='debug')
    return

#*********************************************************************************#
# resources level 
#*********************************************************************************#

def setXmlLength ( xmlRequest):
    """ This function will calculate and add the header appended in the beginning of the message
    defining xml length
    """

    xmlLen = len(xmlRequest)+4
    header = struct.pack(">L", xmlLen)
    xmlRequest = header + xmlRequest
    return xmlRequest

def getXmlLength (xmlHeader):
    """ This function will read  the header information in  the beginning of the message and return message lenght """
    return struct.unpack(">L", xmlHeader)[0]

##############################################################################
# Library common execute functions
##############################################################################
def  execute(xmlMessage, dns=None,  user= '' , pwd= ''):
    """This function executes a xml string which sets up an executes a command through netconf communication towards netconf 
    server at a given host and port    
    """
    global targetData

    if user =='':
        user=targetData['user'] 

    if pwd =='':
        pwd=targetData['pwd'] 
    
    xmlCapabilities = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<capabilities>
<capability>urn:ietf:params:netconf:base:1.0</capability>
</capabilities>
</hello>"""

    xmlTail = """
<?xml version="1.0" encoding="UTF-8"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="2">
<close-session/>
</rpc>""" 

    xmlMessage = """%s\n%s%s\n%s%s\n%s""" % (xmlCapabilities, eod, xmlMessage, eod, xmlTail, eod)
    host = targetData['ipAddress']['ctrl']['ctrl1']
    port = 2022

    xmlMessage = setXmlLength(xmlMessage)
    result = netconf_lib_impl.sendXmlReq(host, port, xmlMessage, user, pwd)

    if result[0] == 'ERROR':
        # Try with second sc
        host = targetData['ipAddress']['ctrl']['ctrl2']
        result = netconf_lib_impl.sendXmlReq(host, port, xmlMessage, user, pwd)

    if result[0] == 'ERROR':
        logger_lib.logMessage('%s' % result[1], logLevel='error')
        return result

    xmlResponse, xmlReply =  result[1].split(eod)[1:3]


    #Validate response
    result = netconf_lib_impl.parseReply(xmlReply)

    if result[0] != 'SUCCESS':
        return result


    t = str(type(dns))
    if re.search('NoneType', t):  #Linux command
        result= netconf_lib_impl.parseLinuxResponse(xmlResponse)
    elif re.search('str', t): #Set Object
        result = netconf_lib_impl.parseReply(xmlResponse)
    elif re.search('list', t): #Get Object
        result = netconf_lib_impl.parseObjectResponse(xmlResponse, dns)
    else:
        logger_lib.logMessage('Unrecognised type in dns: %s' % dns, logLevel='error')

    return result


##############################################################################
# Netconf low level functions/methods --> Confd
##############################################################################
def getObject(dns):
    """This function gets a value in a imm object defined by the dns (distinguish name) trough netconf interface.
    """

    xmlMessage = """ <?xml version="1.0" encoding="UTF-8"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
    <get>
        <filter xmlns="http://ericsson.com/ns/tspsaf_cm/1.0">
            <Me><Common>
                
            </Common></Me>
        </filter>
  </get>
</rpc>"""

    if dns[0] != 'data':
        dns.insert(0, 'data') # insert the first node
    response = execute(xmlMessage,dns=dns)
    

    return response


def  setObject(xmlString):
    """This function sets a value in a imm object defined by the dns (distinguish name) trough netconf interface.
    """

    xmlMessage = """<?xml version="1.0" encoding="UTF-8"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
<edit-config>
    <target>
      <running/>
    </target>
    <config>
      <Me xmlns="http://ericsson.com/ns/tspsaf_cm/1.0" >
        <MeId>1</MeId>
            <Common>
                <CommonId>1</CommonId>
                    %s  
            </Common>
        </Me>
    </config>
  </edit-config>
</rpc>""" %  (xmlString)

    response = execute(xmlMessage, 'rpc-reply')


    return response

##############################################################################
# Netconf functions/methods --> Linux 
##############################################################################
def sendCommand(command, user= '' , pwd= ''):
    """This function executes a Linux command trough netconf interface.
    """
    logger_lib.enter()

    xmlMessage = """
    <?xml version="1.0" encoding="UTF-8"?>
    <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
     <cmdWrapper xmlns="http://ericsson.com/tspsaf/cmdWrapper/1.0">
        <cmd>
        <operand>%s</operand>
        </cmd>
    </cmdWrapper>
    </rpc>""" % command
    
    logger_lib.leave()
    response = execute(xmlMessage, user=user, pwd=pwd)
    if response[0] == 'ERROR':
        logger_lib.logMessage('Failed to send command using Netconf interface', logLevel='error')
    else:
        logger_lib.logMessage('Successful send command using Netconf interface', logLevel = 'debug')
    logger_lib.leave()
    return response

def  executeLinuxCommandFile(xmlFile):
    """This function executes a xml file which sets up an executes a command through netconf communication towards netconf 
    server at a given host and port    
    """
    logger_lib.enter()
    global targetData

    user=targetData['user'] 
    pwd=targetData['pwd'] 

    if (os.access(xmlFile, os.F_OK)):
        try:
            fd=open(xmlFile, 'r')
            xmlMessage=fd.read()
        except:
            logger_lib.logMessage('Failed to read file')
            logger_lib.leave()
            return ('ERROR','Failed to read the file')
    else:
        logger_lib.logMessage('File does not exist')
        logger_lib.leave()
        return ('ERROR','File does not exist')

    host = targetData['ipAddress']['ctrl']['NB']
    port = 2022
    expression = 'SUCCESS'

    logger_lib.logMessage('Sending command using Netconf to host: %s Port: %s' %  (host, port))
    result = netconf_lib_impl.sendXmlReq(host, port, xmlMessage, user, pwd)

    if result[0] == 'ERROR':
        logger_lib.logMessage('%s' % result[1], logLevel='error')
        logger_lib.leave()
        return result

    logger_lib.logMessage('%s' % result[1], logLevel='debug')
    xmlResponse, xmlReply =  result[1].split(eod)[1:3]

    #Validate response
    result = netconf_lib_impl.parseReply(xmlReply)

    if result[0] != 'SUCCESS':
        logger_lib.logMessage('%s' % result[1], logLevel='error')
        logger_lib.leave()
        return result

    logger_lib.logMessage('%s' % result[1], logLevel='debug')

    logger_lib.leave()
    return xmlResponse, xmlReply

if __name__ == "__main__":

    import sys
    import common.target.common_lib.st_env_lib as st_env_lib
    st_env_lib.executeFunction(sys.argv)

    st_env_lib.setUp()

    ###########TEST AREA START###############


    ###########TEST AREA END###############
    st_env_lib.tearDown()

    

