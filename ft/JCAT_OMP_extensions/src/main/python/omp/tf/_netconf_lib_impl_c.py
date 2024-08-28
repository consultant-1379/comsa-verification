#!/vobs/tsp_saf/tools/Python/linux/bin/python
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
import common.target.target_data

#########COMMON USED RESOURCES##########
import lib as lib
import logger_lib as logger_lib
import st_env_lib as st_env_lib

import xml.xpath as xpath
#############GLOBALS##################
targetData=common.target.target_data.data    # a dictionary containing hardware specific information
eod = ']]>]]>'

#*********************************************************************************#
# interaction level 
#*********************************************************************************#
def sendXmlReq(host, port, xmlRequest, user, passw, publicKey='', 
        publicKeyType= '', privateKeyFile='', privateKeyType='' , timeOut=30):
    logger_lib.enter()
    import paramiko

    logger_lib.logMessage('Message: %s  blade: %s Port: %s' %  (xmlRequest, host, port))
    try:    
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
    
            ssh = paramiko.Transport(s)
            ssh.set_log_channel('') #make paramiko write on std:err
    
            #xmlRequest = setXmlLength(xmlRequest)
    
            if publicKeyType == 'rsa':
                agent_public_key = paramiko.RSAKey(
                    data=base64.decodestring(publicKey))
            elif publicKeyType == 'dss':
                agent_public_key = paramiko.DSSKey(
                    data=base64.decodestring(publicKey))
            else:
                agent_public_key = None
    
            if not privateKeyFile == '':
                if privateKeyType == "rsa":
                    user_private_key = paramiko.RSAKey.from_private_key_file(privateKeyFile)
                else:
                    user_private_key = paramiko.DSSKey.from_private_key_file(privateKeyFile)
    
                ssh.connect(hostkey=agent_public_key,
                                 username=user,
                                 pkey=user_private_key)
    
            else:
                ssh.connect(hostkey=agent_public_key,
                                 username=user,
                                 password=passw)    
    
            chan = ssh.open_session()
            chan.invoke_subsystem("netconf")
            chan.send(xmlRequest)
    
            rec=''
            lenOfRec= 0
            while True:
               try:
                   chan.settimeout(timeOut)
                   rec = rec + chan.recv(1024)
                   if len(rec) == lenOfRec:
                       break
                   lenOfRec = len(rec)
               except Exception, e1:
                   logger_lib.logMessage('ERROR Could not receive xml message from Host: %s Port: %s (%s)' %  (host, port, str(e1)), logLevel = 'error')
                   return ('ERROR','Could not recive xml message from Host: %s Port: %s (%s)' % (host, port, str(e1)))
            logger_lib.logMessage('Response: %s  Host: %s Port: %s' %  (rec, host, port))
            ssh.close()
            if rec == '':
                return ('ERROR', rec)
            return ('SUCCESS', rec)
        except Exception, e:
            logger_lib.logMessage('ERROR Could not send xml message to Host: %s Port: %s (%s)' %  (host, port, str(e)), logLevel = 'error')
            return ('ERROR','Could not send xml message to Host: %s Port: %s (%s)' % (host, port, str(e)))
    
    finally:
        logger_lib.leave()

#*********************************************************************************#
# xml functions for parsing response
#*********************************************************************************#
def parseObjectResponse (xmlString, dnsList):
    """This method will parse the response part of message received from netconf interface on the
    controller  
    """
    doc = dom.parseString(xmlString)
    dns = string.join(dnsList, '/')
    dns = dns+'/child::*/text()'

    retList= []
    h = xpath.Evaluate(dns, doc.documentElement)
    for entry in h :
        retDict = {}
        retDict[entry.parentNode.nodeName.encode()]= entry.nodeValue.encode()
        retList.append(retDict)

    if retList !=[]:
        response = 'SUCCESS'
    else:
        response = 'ERROR'
    return response, retList

def parseLinuxResponse (xmlString):
    """This method will parse the response part of message received from netconf interface on the
    controller  
    """
    doc = dom.parseString(xmlString)
    retDict = {}
    h = xpath.Evaluate('*', doc.documentElement)
    for entry in h :
        retDict[entry.nodeName.encode()]= string.strip(entry.firstChild.nodeValue.encode())

    if retDict.has_key('exitStatus'):
        if retDict['exitStatus'] == '0':
            response = 'SUCCESS'
        else:
            response = 'ERROR'
    else:
        response = 'ERROR'
    return response, retDict['result']

def parseReply (xmlString):
    """This method will parse the reply part of message received from netconf interface on the
    controller  
    """
    doc = dom.parseString(xmlString)
    h = xpath.Evaluate('*', doc.documentElement)
    for entry in h :
        result = entry.parentNode.firstChild.nodeName.encode()

    if result == 'ok':
        response = 'SUCCESS'
    else:
        response = 'ERROR'
    return (response, result)
