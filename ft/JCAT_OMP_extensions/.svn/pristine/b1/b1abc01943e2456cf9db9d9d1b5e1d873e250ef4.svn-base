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
try:
    import common.target.target_data as target_data
except Exception, e:
    import omp.target.target_data as target_data

#########COMMON USED RESOURCES##########
#import lib as lib
import logger_lib as logger_lib
#import st_env_lib as st_env_lib

import se.ericsson.jcat.omp.util.Ssh2sessionUtil as Ssh2sessionUtil

from javax.xml.parsers import DocumentBuilderFactory
from javax.xml.xpath import XPathFactory, XPathConstants

#############GLOBALS##################
targetData=target_data.data    # a dictionary containing hardware specific information
eod = ']]>]]>'
timeFact = 1000

#*********************************************************************************#
# interaction level 
#*********************************************************************************#
def sendXmlReq(host, port, xmlRequest, user, passw, publicKey='', 
        publicKeyType= '', privateKeyFile='', privateKeyType='' , timeOut=30):
    global timeFact, eod
    # logger_lib.enter()

    # logger_lib.logMessage('Message: %s  blade: %s Port: %s' %  (xmlRequest, host, port)) 
    try:
        mySsh2sessionUtil = Ssh2sessionUtil("Netconf Ssh2sessionUtil")
        mySsh2sessionUtil.startNetconfSession(host, port, user, passw, timeOut*timeFact, 0)
        requests = str(xmlRequest).strip().split(eod)[:-1]
        result = ""
        for request in requests:
            reply = mySsh2sessionUtil.sendNetconfMsg(request+'\n'+eod+'\n')
            if len(reply) < 1:
                raise Exception, "Netconf reply of zero-size"
            #eolnans: A fix for a current bug in JCAT's SSH lib
            if not reply.startswith('<'):
                reply = '<'+reply
            result += reply
            #logger_lib.logMessage('Response: %s  Host: %s Port: %s' %  (reply, host, port))
        return ['SUCCESS', result]
    except Exception, e:
        logger_lib.logMessage('ERROR Could not send xml message to Host: %s Port: %s (%s)' %  (host, port, str(e)), logLevel = 'error')
        return ('ERROR','Could not send xml message to Host: %s Port: %s (%s)' % (host, port, str(e)))

#*********************************************************************************#
# xml functions for parsing response
#*********************************************************************************#
def parseObjectResponse (xmlString, dnsList):
    """This method will parse the response part of message received from netconf interface on the
    controller  
    """
    from java.lang import String
    from java.io import ByteArrayInputStream, BufferedReader, InputStreamReader
    domFactory = DocumentBuilderFactory.newInstance()
    builder = domFactory.newDocumentBuilder()
    xmlJavaString = String(xmlString)
    inputStream =  ByteArrayInputStream(xmlJavaString.getBytes())

    doc = builder.parse(inputStream)
    
    xpathFactory = XPathFactory.newInstance(XPathFactory.DEFAULT_OBJECT_MODEL_URI)
    xpath = xpathFactory.newXPath()
    dns = string.join(dnsList, '/')
    nodeExpr = xpath.compile("/rpc-reply/"+dns+'/child::node()')

    nodeResult = nodeExpr.evaluate(doc, XPathConstants.STRING)

    if nodeResult:
        response = 'SUCCESS'
        return (response, nodeResult)
    else:
        response = 'ERROR'
        return (response, '')

def parseLinuxResponse (xmlString):
    """This method will parse the response part of message received from netconf interface on the
    controller  
    """
    from java.lang import String
    from java.io import ByteArrayInputStream, BufferedReader, InputStreamReader
    domFactory = DocumentBuilderFactory.newInstance()
    builder = domFactory.newDocumentBuilder()
    xmlJavaString = String(xmlString)
    inputStream =  ByteArrayInputStream(xmlJavaString.getBytes())

    doc = builder.parse(inputStream)
    
    xpathFactory = XPathFactory.newInstance()
    xpath = xpathFactory.newXPath()
    exitExpr = xpath.compile("/rpc-reply/exitStatus")
    resultExpr = xpath.compile("/rpc-reply/result")
    
    exit = int(exitExpr.evaluate(doc, XPathConstants.NUMBER))
    result = resultExpr.evaluate(doc, XPathConstants.STRING)
    
    if exit == 0:
        response = 'SUCCESS'
    else:
        response = 'ERROR'
    return (response, result)

def parseReply (xmlString):
    """This method will parse the reply part of message received from netconf interface on the
    controller  
    """
    from java.lang import String
    from java.io import ByteArrayInputStream, BufferedReader, InputStreamReader
    domFactory = DocumentBuilderFactory.newInstance()
    builder = domFactory.newDocumentBuilder()
    xmlJavaString = String(xmlString)
    inputStream =  ByteArrayInputStream(xmlJavaString.getBytes())

    doc = builder.parse(inputStream)

    xpathFactory = XPathFactory.newInstance()
    xpath = xpathFactory.newXPath()
    expr = xpath.compile("/rpc-reply/ok")
    result = expr.evaluate(doc, XPathConstants.NODE)

    if result:
        response = 'SUCCESS'
    else:
        response = 'ERROR'
    return (response, result)
