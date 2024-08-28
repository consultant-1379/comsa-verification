#!/usr/bin/env python
# coding: iso-8859-1
#
###############################################################################
#
# © Ericsson AB 2006 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson, the receiver of this
# document sif not line : breakhall keep the information contained herein
# confidential and shall protect the same in whole or in part from disclosure
# and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################


'''File information:
   ===================================================
   %CCaseFile: testapp_lib.py %
   %CCaseRev:   /main/1 %
   %CCaseDate:  2007-03-13 %

   Description:
    Implements a class for controlling/communicating with the test application


'''

import sys
import socket
import errno
import re
import time
import copy

from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System

import omp.tf.misc_lib as misc_lib
import omp.target.target_data as target_data
import omp.tf.ssh_lib as ssh_lib
#############GLOBALS##################
targetData = {} # A dictionary containing hardware specific information
testApps = {}
logger = None

################################################################################
# setUp / tearDown
################################################################################

def setUp():

    global targetData
    global testApps
    global logger
    global globalDestinationProfile

    logger = Logger.getLogger('testapp_lib logging')
    logLevel = System.getProperty("jcat.logging")
    logger.setLevel(Level.toLevel(logLevel))
    logger.debug("testapp_lib: Initiating!")

    globalDestinationProfile = System.getProperty("destinationProfile")
    if globalDestinationProfile is None:
        globalDestinationProfile = 'IPv4'
    # globalDestinationProfile determines the combination of network protocols
    # (IPv4 and IPv6) to be used in generated traffic. Test cases that call
    # setConfigurationNew can specify a destination profile themselves,
    # overriding this one.

    targetData = target_data.getTargetHwData()
    testApps = createInstances()
    return testApps

def tearDown():
    logger.debug("testapp_lib: Bye bye !!")
    return

def removeAllInstances():
    logger.debug('enter removeAllInstances')
    global testApps
    for instance in testApps.keys():
        removeInstance(instance)
    logger.debug('leave removeAllInstances')

def removeInstance(instance):
    logger.debug('enter removeInstance')
    global testApps
    try:
        testApps.pop(instance)
    except Exception, e:
        pass

    logger.debug('leave removeInstance')

def addInstance(instance, tappPort, coordPort, minSes, maxSes):
    logger.debug('enter addInstance')
    global testApps
    if instance in testApps:
        raise Exception('Instance already exists')
    else:
        testApps[instance] =  c_testapp(tappPort, coordPort, minSes, maxSes)
    logger.debug('leave addInstance')

def createInstances(instances = ['SC','ALL','ONESC','PL','ONEPL']):

    tapps = {}
    if System.getProperty("loadBalancer")=='EVIP':
        # The IN, OUT and INTRA instances are used for eVIP testing.
        # Define them cautiously to be compatible with old hardware data files.
        extTGC  = targetData['ipAddress']['ctrl']['testpc']
        vip     = targetData['ipAddress']['vip']
        intIPv4 = [vip['vip_1'], vip['vip_2']]
        try:
            traffic = targetData['ipAddress']['traffic']
            extIPv4 = traffic['gateway_IPv4'] + traffic['external_IPv4']
            extIPv6 = traffic['gateway_IPv6'] + traffic['external_IPv6']
            intIPv6 = vip['vip_IPv6_traffic']
        except KeyError:
            extIPv4 = []
            extIPv6 = []
            intIPv6 = []
    
        tapps['IN']    = c_testapp(
            tappPort = 8201, coordPort = 8202, minSes = 5000000, maxSes = 5999999,
            TGC = extTGC, tappsIPv4 = intIPv4, tappsIPv6 = intIPv6)
        tapps['OUT']   = c_testapp(
            tappPort = 8101, coordPort = 8102, minSes = 6000000, maxSes = 6999999,
            TGC = extTGC, tappsIPv4 = extIPv4, tappsIPv6 = extIPv6)
        tapps['INTRA'] = c_testapp(
            tappPort = 8401, coordPort = 8402, minSes = 7000000, maxSes = 7999999,
            TGC = extTGC, tappsIPv4 = intIPv4, tappsIPv6 = intIPv6)
        
    else: 
        for instance in instances:
            if instance == 'PL':
                tapps['PL']    = c_testapp(tappPort = 8001, coordPort = 8002, minSes =       0, maxSes =  999999)
            if instance == 'ONEPL':
                tapps['ONEPL'] = c_testapp( tappPort = 7101, coordPort = 7102, minSes = 3000000, maxSes = 3999999)
            if instance == 'SC':
                tapps['SC']    = c_testapp(tappPort = 8301, coordPort = 8302, minSes = 1000000, maxSes = 1999999)
            if instance == 'ALL':
                tapps['ALL']   = c_testapp(tappPort = 4301, coordPort = 4302, minSes = 2000000, maxSes = 2999999)
            if instance == 'ONESC':
                tapps['ONESC'] = c_testapp(tappPort = 7201, coordPort = 7202, minSes = 4000000, maxSes = 4999999)
    
    testApps = tapps
    return tapps

def getInstances ():
    return testApps

def stopTrafficInstance (instance = 'pl'):
    """stopTrafficInstance tells the named Test App instance to stop sending
       requests. It's an error if the named instance isn't running."""
    logger.debug('enter stopTrafficInstance')

    result = setConfiguration(instance = instance, intensity = 0, tcpConn = 0)

    logger.debug('leave stopTrafficInstance')
    return result

def stopTraffic ():
    """stopTraffic tells all the known Test App instances to stop sending
       requests. It's OK if some instances aren't running."""
    logger.debug('enter stopTraffic')
    result = ["SUCCESS", []]
    for instanceName, instance in testApps.iteritems():
        try:
            description = 'Test App instance ' + instanceName
            # Send a CONFIG message with intensity set to zero, and with enough
            # additional parameters to prevent old versions of the Test App
            # from complaining.
            instance.msg = ('CONFIG\n' +
                            'intensity: 0\n' +
                            'destination: address=0.0.0.0 port=0\n' +
                            'call-type: id=nop label=dummy dist=100\n' +
                            'transport: connections=0\n\n')
            instance.sendMessage()
            res = instance.isConfigReplyOK(
                          instance.parseConfigResponse(instance.getReply()))
            if res[0] == 'SUCCESS':
                log = logger.debug
            else:
                result[0] = 'ERROR'
                log = logger.error
            result[1].append(res[0])
            log(description + ' replied: ' + res[1])
        except (IOError, socket.error), ex:
            exceptionType, value = sys.exc_info()[:2]
            if (exceptionType == socket.error and
                type(value[0]) is int and
                value[0] == errno.ECONNREFUSED):
                result[1].append('SUCCESS')
                logger.debug(description + ' is down, which is OK.')
            else:
                result[0] = 'ERROR'
                result[1].append('ERROR')
                logger.error('Error when talking to ' + description + ': ' +
                             str(ex))
    logger.debug('leave stopTraffic')
    return result

def populateIMM(objectCount, timeOut = 60):
    """populateIMM tells the Test App to create IMM runtime objects for schema
       upgrade testing."""
    instance = testApps["ONESC"]
    result = ssh_lib.getTimeout()
    defTimeout = result[1]
    ssh_lib.setTimeout(timeOut)
    result = ssh_lib.sendCommand(
                 r'echo -e "REQUEST\ncall-type: imm-populate\nwrite-count: ' +
                 str(objectCount) + r'\n" | netcat ' +
                 instance.getTappAddresses()[0] + ' ' +
                 str(instance.getTappPort()))
    ssh_lib.setTimeout(defTimeout)
    if result[0] != "SUCCESS":
        return result
    reply = instance.parseConfigResponse(result[1])
    if ("ANSWER" in reply and
        "result-code" in reply and reply["result-code"] == "0"):
        return ["SUCCESS", ""]
    else:
        return ["ERROR", result[1]]

class c_testapp(object):

    # Construction
    def __init__ (self, tappPort, coordPort, minSes, maxSes,
                  TGC = None, tappsIPv4 = None, tappsIPv6 = None):
        self.tappPort  = tappPort
        self.coordPort = coordPort
        self.minSes    = minSes
        self.maxSes    = maxSes
        # Take the addresses from targetData if none were passed in. Do it
        # cautiously to be compatible with old hardware data files.
        data = targetData['ipAddress']
        if TGC is None:
            try:
                self.targetHost = data['vip']['vip_3']
            except KeyError:
                self.targetHost = data['testApp']['tg_coord']
        else:
            self.targetHost = TGC
        if tappsIPv4 is None:
            try:
                self.tappsIPv4 = [data['vip']['vip_1']]
            except KeyError:
                self.tappsIPv4 = [data['testApp']['test_app']]
        else:
            self.tappsIPv4 = tappsIPv4
        if tappsIPv6 is None:
            try:
                self.tappsIPv6 = data['vip']['vip_IPv6_traffic']
            except KeyError:
                self.tappsIPv6 = []
        else:
            self.tappsIPv6 = tappsIPv6

        self.msg       = ''
        self.reply     = ''

        self.config    = 'CONFIG'
        self.query     = 'QUERY'
        self.report    = 'REPORT'
        self.answer    = 'ANSWER'

        self.startTime = 'start-time'
        self.stopTime  = 'stop-time'
        self.total     = 'total'
        self.callTypes = 'callTypes'

        self.typ       = 'type'
        self.resultc   = 'result-code'
        self.resultStr = 'result-string'

    def getCoordHost(self):
        return self.targetHost

    def getTappIPv4Addresses(self):
        return self.tappsIPv4

    def getTappIPv6Addresses(self):
        return self.tappsIPv6

    def getTappAddresses(self):
        return self.tappsIPv4 + self.tappsIPv6

    def getCoordPort (self):
        return self.coordPort

    def getTappPort (self):
        return self.tappPort

    def getMsg (self):
        return self.msg

    def getReply (self):
        return self.reply

    def getAnswer (self):
        return self.answer

    def getConfig (self):
        return self.config

    def getReport (self):
        return self.report

    def getQuery (self):
        return self.query

    def getResult (self):
        return self.resultc

    def getResultStr (self):
        return self.resultStr

    def getType (self):
        return self.typ

    def getStartTime (self):
        return self.startTime

    def getStopTime (self):
        return self.stopTime

    def getTotal (self):
        return self.total

    def getCallTypes (self):
        return self.callTypes

    def addMsgType (self, typ):
        self.msg = '%s\n' % (typ)

    def addIntensity (self, intensity = 100):
        self.msg = self.msg + 'intensity: %i\n' % (intensity)

    def addSessionIdRange (self):
        self.msg = self.msg + 'session-id-range: min=%i max=%i\n' % (self.minSes, self.maxSes)

    def addSource (self, sources):
        self.msg = self.msg + 'source: %s\n' % (sources)

    def addDestination (self, host, port):
        self.msg = self.msg + 'destination: address=%s port=%i\n' % (host, port)

    def addTransport (self, default='udp', connections=0, timer=0):
        self.msg = self.msg + 'transport: default=%s connections=%i timer=%i\n' % (default, connections, timer)

    def addUdpInfo (self, sockets=20):
        self.msg = self.msg + 'udp: sockets=%d\n' % (sockets)

    def addLogLevel (self, level = 'debug'):
        self.msg = self.msg + 'log-level: %s\n' % (level)

    def addMeasure (self, measure = 0):
        self.msg = self.msg + 'measure: %i\n' % (measure)

    def addStatsReset (self, val = 'yes'):
        self.msg = self.msg + 'stats-reset: %s\n' % (val)

    def addNopCallType (self, label = 'nop', dist = 49, mem = 1000000, loop = 1000000, timeout = 3000, protocol = 'udp'):
        self.msg = self.msg + \
            'call-type: id=nop label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i protocol=%s\n' % \
            (                  label,   dist,     timeout,   mem,              loop,           protocol)

    def addEchoCallType (self, label = 'echo', dist = 49, mem = 1000000, loop = 1000000, timeout = 3000, payload = 1000, protocol = 'udp'):
        self.msg = self.msg + \
            'call-type: id=echo label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i payload-size=%i protocol=%s\n' % \
            (                   label,   dist,     timeout,   mem,              loop,         payload,          protocol)

    def addFcdCallType (self, label = 'fcd', dist = 1, mem = 1000000, loop = 1000000, timeout = 20000, path = '/home/coremw/var/testapp', size = 3000, protocol = 'udp'):
        self.msg = self.msg + \
            'call-type: id=file-create-delete label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i path=%s file-size=%i protocol=%s\n' % \
            (                                 label,   dist,     timeout,   mem,              loop,         path,   size,          protocol)

    def addCkptCallType (self, label = 'ckpt', dist = 1, mem = 10000, loop = 100000, timeout = 3000,
        writeCount = 100, otime = 200, chain = 'no', protocol = 'udp'):
        self.msg = self.msg + \
            'call-type: id=checkpoint label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i write-count=%i chaining=%s open-time=%s protocol=%s\n' % \
            (                         label,   dist,     timeout,   mem,              loop,         writeCount,    chain,      otime,       protocol)

    def addCkptSectCallType (self, label = 'ckpt-sect', dist = 1, mem = 10000, loop = 100000, timeout = 3000,
        writeCount = 50, otime = 200, chain = 'no', protocol = 'udp'):
        self.msg = self.msg + \
            'call-type: id=checkpoint-section label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i write-count=%i chaining=%s open-time=%s protocol=%s\n' % \
            (                         label,   dist,     timeout,   mem,              loop,         writeCount,    chain,      otime,       protocol)

    def addImmCallType (self, label = 'imm', dist = 1, mem = 1000000, loop = 1000000, timeout = 3000, chain = 'yes', otime = 50, protocol = 'udp'):
        self.msg = self.msg + \
            'call-type: id=imm label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i chaining=%s open-time=%s protocol=%s\n' % \
            (                  label,   dist,     timeout,   mem,              loop,         chain,      otime,       protocol)

    def addImmCheckCallType (self, label = 'imm-check', dist = 1, mem = 1000000, loop = 1000000, timeout = 3000, chain = 'no', otime = 0, protocol = 'udp'):
        self.msg = self.msg + \
            'call-type: id=imm-check label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i chaining=%s open-time=%s protocol=%s\n' % \
            (                  label,   dist,     timeout,   mem,              loop,         chain,      otime,       protocol)

    def addImmCleanCallType (self, label = 'imm-clean', dist = 1, mem = 1000000, loop = 1000000, timeout = 30000, protocol = 'tcp'):
        self.msg = self.msg + \
            'call-type: id=imm-clean label=%s dist=%.4f timeout=%i mem-alloc-size=%i loop-count=%i protocol=%s\n' % \
            (                  label,   dist,     timeout,   mem,              loop,         protocol)

    def addEndOfMsg (self):
        self.msg = self.msg + '\n'

    def clearMsg (self):
        self.msg = ''

    def clearReply (self):
        self.reply = ''

    def isConfigReplyOK(self, message):
        logger.debug('enter isConfigReplyOK')
        result = ['SUCCESS', 'Report Response is OK']

        if message[self.getAnswer()] != self.getAnswer():
            print message[self.getAnswer()], self.getAnswer()
            result = ['ERROR', '%s' % (message[self.getAnswer()])]

        if result[0] == 'SUCCESS':
            if message[self.getType()].upper() != self.getConfig():
                result = ['ERROR', '%s' % (message[self.getType()])]

        if result[0] == 'SUCCESS':
            if message['result-code'] != '0' and message['result-code'] != '1':
                result = ['ERROR', 'result-code not 0 or 1: %s' % (message['result-code'])]

        if result[0] == 'SUCCESS':
            if message['result-string'] != 'OK' and message['result-string'] != 'No TGen registered':
                result = ['ERROR', 'result-code not OK: %s' % (message['result-string'])]

        result[1] = self.getReply()
        logger.debug('leave isConfigReplyOK')
        return result

    def isReportReplyOK(self, message):
        logger.debug('enter isReportReplyOK')
        result = ['SUCCESS', 'Report Response is OK']
        if message[self.getAnswer()] != self.getAnswer():
            result = ['ERROR', '%s' % (message[self.getAnswer()])]

        if result[0] == 'SUCCESS':
            if message[self.getType()].upper() != self.getReport():
                result = ['ERROR', '%s' % (message[self.getReport()])]

        #if result[0] == 'SUCCESS':
            #scallsTot = int(message[self.getTotal()]['send'])
            #scallsCt  = self.getStats(message, 'send')
            #if scallsTot != scallsCt:
               #result = ['ERROR', 'send attribute not summed up correctly: %i %i' % (scallsTot, scallsCt)]

        #if result[0] == 'SUCCESS':
            #rcallsTot = int(message[self.getTotal()]['recv'])
            #rcallsCt  = self.getStats(message, 'recv')
            #if rcallsTot != rcallsCt:
                #result = ['ERROR', 'recv attribute not summed up correctly: %i %i' % (rcallsTot, rcallsCt)]

        #if result[0] == 'SUCCESS':
            #fcallsTot = int(message[self.getTotal()]['fail'])
            #fcallsCt  = self.getStats(message, 'fail')
            #if fcallsTot != fcallsCt:
                #result = ['ERROR', 'fail attribute not summed up correctly: %i %i' % (fcallsTot, fcallsCt)]

        #if result[0] == 'SUCCESS':
            #tcallsTot = int(message[self.getTotal()]['timeout'])
            #tcallsCt  = self.getStats(message, 'timeout')
            #if tcallsTot != tcallsCt:
                #result = ['ERROR', 'timeout attribute not summed up correctly: %i %i' % (fcallsTot, fcallsCt)]

        if result[0] == 'SUCCESS':
            result[1] = self.getReply()

        logger.debug('leave isReportReplyOK')
        return result

    def isCallTypesEqual(self, wantedCts, actualCts):
        logger.debug('enter isCallTypesEqual')
        r = []
        for wantedCt in wantedCts:
            result = self.isCallTypeIn(wantedCt, actualCts)
            if result[0] == 'SUCCESS':
                r.append('')
            else:
                break

        if len(r) == len(wantedCts):
            result = ['SUCCESS', 'All CallTypes are correct']
        else:
            result = ['ERROR', 'All CallTypes are not correct (%s)' % (result[1])]

        logger.debug('leave isCallTypesEqual')
        return result

    def isCallTypeIn(self, wantedCt, actualCts):
        logger.debug('enter isCallTypeIn')
        result = ['ERROR', 'Calltype not in list: %s' % (wantedCt)]
        for actualCt in actualCts:
            r = []
            k = wantedCt.keys()
            for attr in k:
                try:
                    if wantedCt[attr] == actualCt[attr]:
                        r.append('')
                except Exception:
                    continue

            if len(r) == len(wantedCt.keys()):
                result = ['SUCCESS', 'Calltype in list']
                break
            else:
                continue

        logger.debug('leave isCallTypeIn')
        return result

    def isConfiguredActualConfiguration(self, wc):
        logger.debug('enter isConfiguredActualConfiguration')
        result = ['SUCCESS', 'Actual config is equal to wanted config']

        self.createDefaultQueryMsg()
        result = self.sendMsg()
        if (result[0] == 'SUCCESS'):
            actualConf = self.parseQueryResponse(self.getReply())
            wantedConf = self.parseQueryResponse(wc)

        for par in wantedConf.keys():
            try:
                if par == 'CONFIG':
                    pass
                elif par == 'stats-reset' or par == 'intensity' or par == 'log-level':
                    if par != 'log-level':
                        if actualConf[par] != wantedConf[par]:
                            result = ['ERROR', '%s: wanted: %s, actual: %s' % (par, actualConf[par], wantedConf[par])]
                elif par == 'callTypes':
                    result = self.isCallTypesEqual(wantedConf[par], actualConf[par])
                else:
                    for attr in wantedConf[par]:
                        if wantedConf[par][attr] != actualConf[par][attr]:
                            result = ['ERROR', '%s: wanted: %s, actual: %s' % (par, actualConf[par], wantedConf[par])]

            except Exception, e:
                result = ['ERROR', '%s: exception: %s,' % (par, e)]

        logger.debug('leave isConfiguredActualConfiguration')
        return result

    def parseQueryResponse(self, response):
        logger.debug('enter parseQueryResponse')
        message = {}
        message['callTypes'] = []
        for line in response.splitlines():
            parameter = line.split(':')[0]
            if len(line.split(':')) > 1:
                attributes = line.split(':')[1]
                attributes = attributes.lstrip()
                attributes = attributes.rstrip()
                attributes = attributes.split()
                if parameter == 'stats-reset' or parameter == 'intensity' or parameter == 'log-level':
                    message[parameter] = attributes[0]
                else:
                    if parameter == 'call-type':
                        message['callTypes'].append({})
                        for attribute in attributes:
                            attr, value = attribute.split('=')
                            listLen  = len(message['callTypes'])
                            message['callTypes'][listLen - 1][attr] = value
                    else:
                        message[parameter] = {}
                        for attribute in attributes:
                            attr, value = attribute.split('=')
                            message[parameter][attr] = value
            else:
                message[parameter] = parameter

        logger.debug('leave parseQueryResponse')
        return message

    def parseReportResponse(self, response):
        logger.debug('enter parseReportResponse')
        payloadFlag = False
        message = {}
        message['callTypes'] = []
        message['payload'] = []
        for line in response.splitlines():

            if not line:
                # empty line means end-of-header
                payloadFlag = True
                continue

            if payloadFlag:
                message['payload'] = line
                break

            parameter = line.split(':')[0]

            if len(line.split(':')) > 1:
                attributes = line.split(':')[1]
                attributes = attributes.lstrip()
                attributes = attributes.rstrip()
                attributes = attributes.split()

                if parameter == 'type' or parameter == 'start-time' or parameter == 'stop-time' or parameter == 'send-count' or parameter == 'receive-count' or parameter == 'fail-count' or parameter == 'timeout-count' or parameter =='active-sessions' or parameter =='payload-size':
                    message[parameter] = attributes[0]
                else:
                    if parameter == 'call-type':
                        message['callTypes'].append({})
                        for attribute in attributes:
                            attr, value = attribute.split('=')
                            listLen  = len(message['callTypes'])
                            message['callTypes'][listLen - 1][attr] = value
                    else:
                        message[parameter] = {}
                        for attribute in attributes:
                            attr, value = attribute.split('=')
                            message[parameter][attr] = value
            else:
                message[parameter] = parameter

        logger.debug('leave parseReportResponse')
        return message

    def parseConfigResponse(self, response):
        logger.debug('enter parseConfigResponse')
        message = {}
        for line in response.splitlines():
            parameter = line.split(':')[0]
            if len(line.split(':')) > 1:
                attributes = line.split(':')[1]
                attributes = attributes.strip()
                if parameter == 'type' or parameter == 'result-code' or parameter == 'result-string':
                    message[parameter] = attributes
            else:
                message[parameter] = parameter

        logger.debug('leave parseConfigResponse')
        return message

    def getTotalStats(self, message, attribute):
        logger.debug('enter getTotalStats')
        if attribute != 'all':
            rv = message['total'][attribute]
        else:
            rv = message['total']

        logger.debug('leave getTotalStats')
        return rv

    def getCalltypeStats(self, message, ct, attr):
        logger.debug('enter getCalltypeStats')
        counter = 0
        callTypes = message['callTypes']
        for callType in callTypes:
            if callType['id'] == ct:
                counter = counter + int(callType[attr])
        logger.debug('leave getCalltypeStats')
        return counter

    def getProtocolStats(self, message, proto, attr):
        logger.info ('enter getProtocolStats')
        counter = 0
        callTypes = message['callTypes']
        for callType in callTypes:
            if callType['protocol'] == proto:
                counter = counter + int(callType[attr])
        logger.debug('leave getProtocolStats')
        return counter

    def getStats(self, message, attr):
        logger.debug('enter getStats')

        counter = 0
        callTypes = message['callTypes']
        for callType in callTypes:
            counter = counter + int(callType[attr])

        logger.debug('leave getStats')
        return counter


    def createConfigBase(self, intensity, tcpConn, tcpTime, udpSockets,
                         measure):
        """createConfigBase composes a partial CONFIG message and stores it in
           self. Some destination and call-type parameters should be added
           before the message is sent."""

        self.addMsgType(self.getConfig())
        self.addIntensity(intensity)
        self.addSessionIdRange()
        self.addTransport(connections = tcpConn, timer = tcpTime)
        self.addUdpInfo(sockets=udpSockets)
        self.addMeasure(measure)


    def addCallTypeProfile(self, profile):
        """addCallTypeProfile adds call-type parameters to the message in self,
           controlled by the named profile."""

	""" Here we set different profile for EVIP and CoreMW. 
	We prefer not to have CoreMW specific traffic on EVIP since we do not test coreMW and also when we run the FW against standalone EVIP we can't have coreWM load. 
	So we remove the coreMW specific load and create a pure USP/TCP load for EVIP testing. """

	if System.getProperty("loadBalancer")=='EVIP':
		logger.debug('adding traffic profile for EVIP')
		if profile == 'normal':
			self.addNopCallType( label = 'nop-udp',  dist = 25.0, protocol = 'udp', loop=1000, mem=8)
            		self.addNopCallType( label = 'nop-tcp',  dist = 25.0, protocol = 'tcp', loop=1000, mem=8)
            		self.addNopCallType( label = 'echo-udp',  dist = 25.0, protocol = 'udp', loop=1000, mem=8)
            		self.addNopCallType( label = 'echo-tcp',  dist = 25.0, protocol = 'tcp', loop=1000, mem=8)
			
		elif profile == 'high':
			self.addNopCallType( label = 'nop-udp',  dist = 25.0, protocol = 'udp', loop=100000, mem=1024)
            		self.addNopCallType( label = 'nop-tcp',  dist = 25.0, protocol = 'tcp', loop=100000, mem=1024)
            		self.addNopCallType( label = 'echo-udp',  dist = 25.0, protocol = 'udp', loop=100000, mem=1024)
            		self.addNopCallType( label = 'echo-tcp',  dist = 25.0, protocol = 'tcp', loop=100000, mem=1024)
		
		elif profile == 'ultra':
			self.addNopCallType( label = 'nop-tcp',  dist = 25.0, protocol = 'tcp', loop=2600000, mem=8192, timeout=3000)
			self.addNopCallType( label = 'nop-udp',  dist = 25.0, protocol = 'udp', loop=2600000, mem=8192, timeout=3000)
			self.addEchoCallType( label = 'echo-tcp', dist = 25.0, protocol = 'tcp', loop=2600000, mem=8192, timeout=3000)
			self.addEchoCallType( label = 'echo-udp', dist = 25.0, protocol = 'udp', loop=2600000, mem=8192, timeout=3000)
			
		elif profile == 'nop':
			self.addNopCallType( label = 'nop-udp',  dist = 50, mem = 0, loop = 0, timeout = 3000, protocol = 'udp')
			self.addNopCallType( label = 'nop-tcp',  dist = 50, mem = 0, loop = 0, timeout = 3000, protocol = 'tcp')

		else:
			logger.error('Profile: %s undefined' % (profile))


	else: 
		if profile == 'normal':
			self.addNopCallType( label = 'nop-udp',  dist = 24.959, protocol = 'udp')
			self.addNopCallType( label = 'nop-tcp',  dist = 24.923, protocol = 'tcp')
			#self.addNopCallType( label = 'nop-udp',  dist = 25.1, protocol = 'udp')
			#self.addNopCallType( label = 'nop-tcp',  dist = 25.1, protocol = 'tcp')
			self.addEchoCallType(label = 'echo-udp', dist = 24.941, protocol = 'udp')
			self.addEchoCallType(label = 'echo-tcp', dist = 24.941, protocol = 'tcp')
			self.addFcdCallType( label = 'fcd-tcp',  dist = 0.1, path = '/tmp/testapp', protocol = 'tcp')
			self.addFcdCallType( label = 'fcd-udp',  dist = 0.1, path = '/tmp/testapp', protocol = 'udp')
			#self.addCkptCallType(label = 'ckpt-tcp', dist = 0.1, chain = 'yes', protocol = 'tcp')
			#self.addCkptCallType(label = 'ckpt-udp', dist = 0.1, chain = 'yes', protocol = 'udp')
			#self.addCkptSectCallType(label = 'ckpt-sect-tcp', dist = 0.2, chain = 'yes', protocol = 'tcp')
			#self.addCkptSectCallType(label = 'ckpt-sect-udp', dist = 0.2, chain = 'yes', protocol = 'udp')
			self.addImmCallType( label = 'imm-tcp',  dist = 0.018, chain = 'yes', protocol = 'tcp')
			#self.addImmCallType( label = 'imm-udp',  dist = 0.009, chain = 'yes', protocol = 'udp')
			self.addImmCheckCallType( label = 'imm-ck-tcp',  dist = 0.018, protocol = 'tcp')
			#self.addImmCheckCallType( label = 'imm-ck-udp',  dist = 0.009, protocol = 'udp')
			#self.addImmCleanCallType(dist = 0.0001)
		elif profile == 'high':
			self.addNopCallType( label = 'nop-udp',  dist = 47.95,  loop = 2000000, protocol = 'udp')
			self.addNopCallType( label = 'nop-tcp',  dist = 1.932, protocol = 'tcp')
			self.addEchoCallType(label = 'echo-udp', dist = 47.95, loop = 2000000, protocol = 'udp')
			self.addEchoCallType(label = 'echo-tcp', dist = 1.932, protocol = 'tcp')
			self.addFcdCallType( label = 'fcd-tcp',  dist = 0.1, path = '/tmp/testapp', protocol = 'tcp')
			self.addFcdCallType( label = 'fcd-udp',  dist = 0.1, path = '/tmp/testapp', protocol = 'udp')
			#self.addCkptCallType(label = 'ckpt-tcp', dist = 0.1, chain = 'yes', protocol = 'tcp')
			#self.addCkptCallType(label = 'ckpt-udp', dist = 0.1, chain = 'yes', protocol = 'udp')
			#self.addCkptSectCallType(label = 'ckpt-sect-tcp', dist = 0.2, chain = 'yes', protocol = 'tcp')
			#self.addCkptSectCallType(label = 'ckpt-sect-udp', dist = 0.2, chain = 'yes', protocol = 'udp')
			self.addImmCallType( label = 'imm-tcp',  dist = 0.018, chain = 'yes', protocol = 'tcp')
			#self.addImmCallType( label = 'imm-udp',  dist = 0.009, chain = 'yes', protocol = 'udp')
			self.addImmCheckCallType( label = 'imm-ck-tcp',  dist = 0.018, protocol = 'tcp')
			#self.addImmCheckCallType( label = 'imm-ck-udp',  dist = 0.009, protocol = 'udp')
		elif profile == 'ultra':
			self.addNopCallType( label = 'nop-tcp',  dist = 29.3, protocol = 'tcp', loop=2600000, mem=8192, timeout=3000)
			self.addNopCallType( label = 'nop-udp',  dist = 20.7, protocol = 'udp', loop=2600000, mem=8192, timeout=3000)
			self.addEchoCallType( label = 'echo-tcp', dist = 29.47, protocol = 'tcp', loop=2600000, mem=8192, timeout=3000)
			self.addEchoCallType( label = 'echo-udp', dist = 20.33, protocol = 'udp', loop=2600000, mem=8192, timeout=3000)
			#self.addNopCallType( label = 'nop-tcp',  dist = 45.9, protocol = 'tcp', loop=3000000, timeout=2000)
			#self.addNopCallType( label = 'nop-udp',  dist = 45.9, protocol = 'udp', loop=1000000, timeout=1500)
			#self.addEchoCallType(label = 'echo-udp', dist = 3.9, protocol = 'udp', timeout=1000)
			#self.addEchoCallType(label = 'echo-tcp', dist = 3.8, protocol = 'tcp', timeout=1000)
			self.addFcdCallType( label = 'fcd-tcp',  dist = 0.05, path = '/tmp/testapp', protocol = 'tcp', timeout=5000)
			self.addFcdCallType( label = 'fcd-udp',  dist = 0.05, path = '/tmp/testapp', protocol = 'udp', timeout=5000)
			#self.addCkptCallType(label = 'ckpt-tcp', dist = 0.05, chain = 'yes', protocol = 'tcp', timeout=3000)
			#self.addCkptCallType(label = 'ckpt-udp', dist = 0.05, chain = 'yes', protocol = 'udp', timeout=3000)
			#self.addCkptSectCallType(label = 'ckpt-sect-tcp', dist = 0.1, chain = 'yes', protocol = 'tcp', timeout=3000)
			#self.addCkptSectCallType(label = 'ckpt-sect-udp', dist = 0.1, chain = 'yes', protocol = 'udp', timeout=3000)
			self.addImmCallType( label = 'imm-tcp',  dist = 0.04, chain = 'yes', protocol = 'tcp', timeout=3000)
			#self.addImmCallType( label = 'imm-udp',  dist = 0.02, chain = 'yes', protocol = 'udp', timeout=3000)
			self.addImmCheckCallType( label = 'imm-ck-tcp',  dist = 0.06, protocol = 'tcp', timeout=3000)
			#self.addImmCheckCallType( label = 'imm-ck-udp',  dist = 0.03, protocol = 'udp', timeout=3000)
		elif profile == 'nop':
			#self.addNopCallType( label = 'nop-udp',  dist = 100, mem = 0, loop = 0, timeout = 3000, protocol = 'udp')
			#self.addNopCallType( label = 'nop-tcp',  dist = 100, mem = 0, loop = 0, timeout = 3000, protocol = 'tcp')
			#self.addEchoCallType(label = 'echo-udp', dist = 100, mem = 0, loop = 0, timeout = 3000, payload = 100, protocol = 'udp')
			self.addEchoCallType(label = 'echo-tcp', dist = 100, mem = 0, loop = 0, timeout = 3000, payload = 100, protocol = 'tcp')
		else:
			logger.error('Profile: %s undefined' % (profile))


    def TappAddressesForProfile(self, profile):
        """TappAddressesForProfile returns a list with a subset of the Tapp
           addresses set in self, controlled by the specified destination
           profile."""

        if profile == 'IPv4':
            addresses = self.getTappIPv4Addresses()
        elif profile == 'IPv6':
            addresses = self.getTappIPv6Addresses()
        elif profile == 'equal':
            addresses = self.getTappAddresses()
        else:
            raise ValueError(repr(profile) + ' is not a destination profile.')

        if len(addresses) == 0:
            raise ValueError('There are no addresses defined for the ' +
                             'destination profile "' + profile + '".')

        return addresses


    def addDestinationProfile(self, profile):
        """addDestinationProfile adds destination parameters to the message in
           self, controlled by the specified destination profile."""

        for address in self.TappAddressesForProfile(profile):
            self.addDestination(address, self.getTappPort())


    def createDefaultConfigMsg (self, intensity, sources = None,  profile='normal', level = 'debug',  tcpConn = 101, tcpTime = 1000, udpSockets = 20, minSession = 0, maxSession = 999999, measure = 0, destHost = [], destPort = None):
        """destHost may be a string or a list of strings, where each string is
           the textual representation of an IPv4 or IPv6 address. If it's an
           empty list, a subset of the Tapp addresses set in self will be used,
           controlled by the global destination profile."""

        self.createConfigBase(intensity = intensity, tcpConn = tcpConn,
                              tcpTime = tcpTime, udpSockets = udpSockets,
                              measure = measure)

        self.addCallTypeProfile(profile)

        if sources != None:
            self.addSource(sources)
        if type(destHost) is str:
            destHost = [destHost]  # It needs to be a list.
        elif len(destHost) == 0:
            destHost = self.TappAddressesForProfile(globalDestinationProfile)
        if destPort is None:
            destPort = self.getTappPort()
        for address in destHost:
            self.addDestination(address, destPort)

        self.addLogLevel(level = level)
        self.addStatsReset()
        self.addEndOfMsg()


    def createConfigNew(self, intensity, destinationProfile, callTypeProfile,
                        tcpConn, tcpTime, udpSockets, measure):
        """createConfigNew composes a CONFIG message and stores it in self. It
           uses the destination addresses and port set in self.
           destinationProfile determines the combination of network protocols
           (IPv4 and IPv6). callTypeProfile determines the combination of
           transaction types ("call-types"), and also the combination of
           transport protocols (such as TCP and UDP)."""

        self.createConfigBase(intensity = intensity, tcpConn = tcpConn,
                              tcpTime = tcpTime, udpSockets = udpSockets,
                              measure = measure)

        self.addCallTypeProfile(callTypeProfile)

        self.addDestinationProfile(destinationProfile)

        self.addStatsReset()
        self.addEndOfMsg()


    def createDefaultStatsMsg (self):
        typ = self.getReport()
        self.addMsgType(typ = typ)
        self.addEndOfMsg()

    def createDefaultQueryMsg (self):
        typ = self.getQuery()
        self.addMsgType(typ = typ)
        self.addEndOfMsg()

    def createResetStats(self):
        typ = self.getConfig()
        self.addMsgType(typ)
        self.addStatsReset()
        self.addEndOfMsg()


    def sendMessage(self, timeOut = 120, coordHost = '', port = None):
        """sendMessage connects to the host specified in coordHost, or to the
           target host set in self if coordHost is empty, and then sends the
           message set in self, waits for a reply and stores the reply in self.
           It propagates exceptions when errors occur."""
        logger.debug('enter sendMessage')

        if not coordHost:
            coordHost = self.getCoordHost()
        if port is None:
            port = self.getCoordPort()

        try:
            logger.debug('Message:\n%stargetHost: %s Port: %s' %
                         (self.getMsg(), coordHost, port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((coordHost, port))
            s.send(self.getMsg())
            self.reply = ''
            pattern = re.compile('\n\n')
            timeOut = int(time.time()) + timeOut
            while True:
                tmpReply = s.recv(1024)
                self.reply = self.reply + tmpReply
                if pattern.search(self.reply):
                    break
                if int(time.time()) > timeOut:
                    raise Timeout('No reply was received for ' +
                                  str(timeOut) + ' seconds.')
            logger.debug('Message:\n%sreceived from targetHost: %s Port: %s' %
                         (self.reply, coordHost, port))
        finally:
            s.close()
            logger.debug('leave sendMessage')


    def sendMsg(self, timeOut = 120, coordHost = '', port = None):
        """sendMsg is like sendMessage except that instead of propagating
           exceptions it indicates success or error in its result."""
        logger.debug('enter sendMsg')

        if not coordHost:
            coordHost = self.getCoordHost()
        if port is None:
            port = self.getCoordPort()

        try:
            self.sendMessage(timeOut = timeOut, coordHost = coordHost,
                             port = port)
            result = ['SUCCESS',
                      'Message sent to host: %s port: %i' % (coordHost, port)]
        except (IOError, socket.error), e:
            result = ['ERROR',
                      'Could not send message to host: %s port: %i (%s)' %
                      (coordHost, port, str(e))]
            logger.warn(result[1])

        logger.debug('leave sendMsg')
        return result


    def sendConfigAndCheck(self, timeOut = 120, coordHost = '', port = None):
        result = self.sendMsg(timeOut = timeOut, coordHost = coordHost,
                              port = port)
        if(result[0] == 'SUCCESS'):
            result = self.isConfigReplyOK(
                         self.parseConfigResponse(self.getReply()))
            if(result[0] == 'SUCCESS'):
                log = logger.debug
            else:
                log = logger.error
            log('The Test App replied: ' + result[1])
        return result


#*********************************************************************************#
# Configure test application traffic intensity
#*********************************************************************************#
def configure (instance = 'PL', profile = 'normal', intensity = 0, level = 'debug', tcpConn = 499, tcpTime = 200, tgen_sources = None):
    return setConfiguration(instance, profile, intensity, level, tcpConn, tcpTime, tgen_sources)

#*********************************************************************************#
# Configure test application traffic intensity
#*********************************************************************************#
def setConfigurationString(instance, message):
    logger.debug('enter setConfigurationString')
    print message
    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]
    try:
        ptestapp = getInstances()[key]
        ptestapp.msg = message
        result = ptestapp.sendConfigAndCheck()
    except Exception, e:
        result = ['ERROR', 'Exception: %s' % (e)]
        logger.error("result: %s exeception: %s " % (result[1], e))

    logger.debug('leave setConfigurationString')
    return result

#*********************************************************************************#
# Configure test application traffic intensity
#*********************************************************************************#
def setConfiguration(instance = 'ALL', profile = 'normal', intensity = 1000, level = 'debug', tcpConn = 499, tcpTime = 200, udpSockets=20, tgen_sources = None, measure = 0, destHost=[], destPort=None, coordHost=None):

    logger.debug('enter setConfiguration')

    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]

    for i in range(20):
        if i > 0:
            misc_lib.waitTime(6)
        try:
            ptestapp = getInstances()[key]
            logger.debug('Instance = %s'%str(key))
            logger.debug('profile = %s'%str(profile))
            if key=='OUT' :
                # This OUT traffic is a special case because the traffic flows in the opposite direction. 
                # So we define the destination addresses here itself. 
                destination_addresses= []
                
                if globalDestinationProfile == 'IPv4':
                    gateway_address_IPv4=targetData['ipAddress']['traffic']['gateway_IPv4']
                    external_tgs_IPv4=[]
                    #uncomment the following line external_tgs_IPv4 when we can run multiple vip addresses for UDP traffic in testApp
                    #external_tgs_IPv4=targetData['ipAddress']['traffic']['external_IPv4']
                    for address in gateway_address_IPv4:
                        destination_addresses.append(address)
                    for address in external_tgs_IPv4:
                        destination_addresses.append(address)
                
                elif globalDestinationProfile == 'IPv6':
                    gateway_address_IPv6=targetData['ipAddress']['traffic']['gateway_IPv6']
                    external_tgs_IPv6=[]
                    #uncomment the following line external_tgs_IPv6 when we can run multiple vip addresses for UDP traffic in testApp
                    #external_tgs_IPv6=targetData['ipAddress']['traffic']['external_IPv6']
                    for address in gateway_address_IPv6:
                        destination_addresses.append(address)
                    for address in external_tgs_IPv6:
                        destination_addresses.append(address)
                
                elif globalDestinationProfile == 'equal':
                    gateway_address_IPv4=targetData['ipAddress']['traffic']['gateway_IPv4']
                    external_tgs_IPv4=[]
                    #uncomment the following line external_tgs_IPv4 when we can run multiple vip addresses for UDP traffic in testApp
                    #external_tgs_IPv4=targetData['ipAddress']['traffic']['external_IPv4']
                    for address in gateway_address_IPv4:
                        destination_addresses.append(address)
                    for address in external_tgs_IPv4:
                        destination_addresses.append(address)
                    
                    gateway_address_IPv6=targetData['ipAddress']['traffic']['gateway_IPv6']
                    external_tgs_IPv6=[]
                    #uncomment the following line external_tgs_IPv6 when we can run multiple vip addresses for UDP traffic in testApp
                    #external_tgs_IPv6=targetData['ipAddress']['traffic']['external_IPv6']
                    for address in gateway_address_IPv6:
                        destination_addresses.append(address)
                    for address in external_tgs_IPv6:
                        destination_addresses.append(address)                    
                    
                else:
                    raise ValueError(repr(profile) + ' is not a destination profile.')
                
                destHost=destination_addresses
                #ptestapp.createDefaultConfigMsgNew(profile=profile,intensity=intensity, sources=None,tcpConn = tcpConn, tcpTime = tcpTime, udpSockets=udpSockets, level=level, measure=measure, destHost=destHost, destPort=destPort)
                ptestapp.createDefaultConfigMsg(profile=profile,intensity=intensity, sources=None,tcpConn = tcpConn, tcpTime = tcpTime, udpSockets=udpSockets, level=level, measure=measure, destHost=destHost, destPort=destPort)
                result = ptestapp.sendMsg(coordHost=coordHost)
                      
            elif key=='IN':
                
                destination_addresses=[]
                
                if globalDestinationProfile == 'IPv4':
                    #uncomment vip_1, vip_2 if we can run traffic to different ALBs, don't think this is a possibility with our FW.
                    #vip_1=targetData['ipAddress']['vip']['vip_1']
                    #vip_2=targetData['ipAddress']['vip']['vip_2']
                    vip_3=targetData['ipAddress']['vip']['vip_3']
                    #destination_addresses.append(vip_1)#
                    #destination_addresses.append(vip_2)
                    destination_addresses.append(vip_3)
 
                if globalDestinationProfile == 'IPv6':
                    vip_3_ipv6=targetData['ipAddress']['vip']['vip_IPv6_OAM']
                    destination_addresses.append(vip_3_ipv6)
                
                if globalDestinationProfile == 'equal':
                    vip_3=targetData['ipAddress']['vip']['vip_3']
                    destination_addresses.append(vip_3)
                    vip_3_ipv6=targetData['ipAddress']['vip']['vip_IPv6_OAM']
                    destination_addresses.append(vip_3_ipv6)
                
                destHost = destination_addresses
                #ptestapp.createDefaultConfigMsgNew(profile=profile,intensity=intensity, sources=None,tcpConn = tcpConn, tcpTime = tcpTime, udpSockets=udpSockets, level=level, measure=measure, destHost=destHost, destPort=destPort)
                ptestapp.createDefaultConfigMsg(profile=profile,intensity=intensity, sources=None,tcpConn = tcpConn, tcpTime = tcpTime, udpSockets=udpSockets, level=level, measure=measure, destHost=destHost, destPort=destPort)
                result = ptestapp.sendMsg(coordHost=coordHost)
            
            elif key=='INTRA':
                
                destination_addresses=[]
                
                if globalDestinationProfile == 'IPv4':
                    vip_3=targetData['ipAddress']['vip']['vip_3']
                    destination_addresses.append(vip_3)
                
                if globalDestinationProfile == 'IPv6':
                    vip_3_ipv6=targetData['ipAddress']['vip']['vip_IPv6_OAM']
                    destination_addresses.append(vip_3_ipv6)
                
                if globalDestinationProfile == 'equal':
                    vip_3=targetData['ipAddress']['vip']['vip_3']
                    destination_addresses.append(vip_3)
                    vip_3_ipv6=targetData['ipAddress']['vip']['vip_IPv6_OAM']
                    destination_addresses.append(vip_3_ipv6)
                
                destHost = destination_addresses
                ptestapp.createDefaultConfigMsg(profile=profile,intensity=intensity, sources=None,tcpConn = tcpConn, tcpTime = tcpTime, udpSockets=udpSockets, level=level, measure=measure, destHost=destHost, destPort=destPort)
                result = ptestapp.sendMsg(coordHost=coordHost)
                    
            else:
                ptestapp.createDefaultConfigMsg(profile=profile,intensity=intensity, sources=tgen_sources,tcpConn = tcpConn, tcpTime = tcpTime, udpSockets=udpSockets, level=level, measure=measure, destHost=destHost, destPort=destPort)
                result = ptestapp.sendMsg(coordHost=coordHost)
                
            if (result[0] == 'SUCCESS'):
                result = ptestapp.isConfigReplyOK(ptestapp.parseConfigResponse(ptestapp.getReply()))
                if (result[0] == 'SUCCESS'):
                    logger.debug('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))
                else:
                    logger.error('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))            

        except Exception, e:
            result = ['ERROR', 'Exception: %s' % (e)]
            logger.error("result: %s exeception: %s " % (result[1], e))
        if result[0] == 'SUCCESS':
            break

    logger.debug('leave setConfiguration')
    return result


def setConfigurationNew(instance = 'ALL', destinationProfile = None,
                        callTypeProfile = 'normal', intensity = 1000,
                        tcpConn = 499, tcpTime = 200, udpSockets = 20,
                        measure = 0):
    """setConfigurationNew composes a CONFIG message and sends it to the Test
       App. It uses the  target host address, destination addresses and port
       set in self. destinationProfile determines the combination of network
       protocols (IPv4 and IPv6). If it is None or not specified, the global
       destination profile will be used. callTypeProfile determines the
       combination of transaction types ("call-types"), and also the combination
       of transport protocols (such as TCP and UDP)."""

    logger.debug('enter setConfigurationNew')
    ptestapp = getInstances()[instance.upper()]
    if destinationProfile is None:
        destinationProfile = globalDestinationProfile
    ptestapp.createConfigNew(intensity = intensity,
                             destinationProfile = destinationProfile,
                             callTypeProfile = callTypeProfile,
                             tcpConn = tcpConn, tcpTime = tcpTime,
                             udpSockets = udpSockets, measure = measure)
    result = ptestapp.sendConfigAndCheck()
    logger.debug('leave setConfigurationNew')
    return result


#*********************************************************************************#
# Query test application configuration
#*********************************************************************************#
def getConfiguration(instance = 'PL'):
    """
    This will query the testapp configuration
    """
    logger.debug('enter getConfiguration')

    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]
    try:
        ptestapp = getInstances()[key]
        ptestapp.createDefaultQueryMsg()
        result = ptestapp.sendMsg()
        if (result[0] == 'SUCCESS'):
            message = ptestapp.parseQueryResponse(ptestapp.getReply())
            result[1] = ptestapp.getReply()
    except Exception, e:
        logger.error(result[1])

    logger.debug('leave getConfiguration')
    return result

#*********************************************************************************#
# Get test application call statistics
#*********************************************************************************#

def getTotalStatistics (instance = 'PL'):
    """ This will return call statistics
    """
    logger.debug('enter getTotalStatistics')

    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]
    try:
        ptestapp = getInstances()[key]
        ptestapp.createDefaultStatsMsg()
        result = ptestapp.sendMsg()
        if (result[0] == 'SUCCESS'):
            result = ptestapp.isReportReplyOK(ptestapp.parseReportResponse(ptestapp.getReply()))
            if (result[0] == 'SUCCESS'):
                logger.debug('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))
            else:
                logger.error('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))
        if result[0] == 'SUCCESS':
            message = ptestapp.parseReportResponse(ptestapp.getReply())
            stats = ptestapp.getTotalStats(message, 'all')
            result[1] = stats

    except Exception, e:
        result = ['ERROR', 'Exception: %s' % (e)]
        logger.error(e)

    logger.debug('leave getTotalStatistics')
    return result

def resetStatistics (instance = 'PL', coordHost=''):
    """ This will return reset the statistics
    """
    logger.debug('enter resetStatistics')

    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]
    try:
        ptestapp = getInstances()[key]
        ptestapp.createResetStats()
        result = ptestapp.sendMsg(coordHost=coordHost)
        if (result[0] == 'SUCCESS'):
            result = ptestapp.isConfigReplyOK(ptestapp.parseConfigResponse(ptestapp.getReply()))
            if (result[0] == 'SUCCESS'):
                logger.debug('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))
            else:
                logger.error('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))
    except Exception, e:
        result = ['ERROR', 'Exception: %s' % (e)]
        logger.error("result: %s exeception: %s " % (result[1], e))

    logger.debug('leave resetStatistics')

    return result

def getStatistics(instance = 'PL', coordHost=''):
    """ This will return call statistics
    """
    logger.debug('enter getStatistics')

    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]
    try:
        ptestapp = getInstances()[key]
        ptestapp.createDefaultStatsMsg()

        result = ptestapp.sendMsg(coordHost=coordHost)
        if (result[0] == 'SUCCESS'):
            result = ptestapp.isReportReplyOK(ptestapp.parseReportResponse(ptestapp.getReply()))
            if (result[0] == 'SUCCESS'):
                logger.debug('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))
            else:
                logger.error('testapp returned %s: %s' % (ptestapp.getResult(), result[1]))
    except Exception, e:
        result = ['ERROR', 'Exception: %s' % (e)]
        logger.error(e)

    if result[0] == 'SUCCESS':
        payloadFlag = False
        # Don't care about success
        lst = copy.deepcopy(result)
        str = lst[1]
        ret = {'call-type' : {}}

        # First line contains ANSWER which we don't care about
        lst = str.split( '\n' )[1:]

        for line in lst:
            #print 'Line is "%s"' % line

            if line == "":
                    payloadFlag = True

            elif payloadFlag:
                    ret[ 'payload' ] = line.strip()
                    result[1] = ret

            elif line.startswith( 'call-type' ):
                # foreach calltype
                line_lst = [ s.split( '=' ) for s in line.split( ' ' )[1:] ]
                label = line_lst[0][1]
                line_lst = line_lst[1:]

                line_dict = {}
                for key, val in line_lst:
                    line_dict[ key ] = val

                ret['call-type'][ label ] = line_dict
            elif line.startswith( 'total' ):
                # foreach calltype
                line_lst = line.split( ' ' )
                label = line_lst[0][:-1] # Don't want ':'
                line_lst = line_lst[1:]

                line_dict = {}
                for str in line_lst:
                    key, val = str.split( '=' )
                    line_dict[ key ] = val

                ret[ label ] = line_dict

            elif line:
                key, val = line.split( ':' )
                ret[ key ] = val.strip()

            result[1] = ret

    logger.debug('leave getStatistics')
    return result

def getConfiguredIntensity(instance = 'PL'):
    logger.debug('enter getConfiguredIntensity')

    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]
    try:
        ptestapp = getInstances()[key]
        ptestapp.createDefaultQueryMsg()
        result = ptestapp.sendMsg()
        if (result[0] == 'SUCCESS'):
            message = ptestapp.parseQueryResponse(ptestapp.getReply())
            result[1] = message['intensity']
    except Exception, e:
        result = ['ERROR', 'Exception: %s' % (e)]
        logger.error(result[1])

    logger.debug('leave getConfiguredIntensity')
    return result

def getActualIntensity(instance = 'PL', interval = 10):
    logger.debug('enter getActualIntensity')

    key = instance.upper()
    result = ['ERROR', 'Instance not valid: %s' % (instance)]
    try:
        ptestapp = getInstances()[key]
        ptestapp.createDefaultStatsMsg()
        result = ptestapp.sendMsg()
        if (result[0] == 'SUCCESS'):
            result = ptestapp.getTotalStats(ptestapp.parseReportResponse(ptestapp.getReply()), 'send')
            calls1 = result

            ptestapp.clearReply()
            time.sleep(interval)

            result = ptestapp.sendMsg()

        if (result[0] == 'SUCCESS'):
            result = ptestapp.getTotalStats(ptestapp.parseReportResponse(ptestapp.getReply()), 'send')
            calls2 = result

            calls       = int(calls2) - int(calls1)
            intensity   = calls/interval
            result      = ['SUCCESS', intensity]

        if (result[0] == 'SUCCESS'):
            logger.debug('Actual intensity: %s' % (result[1]))
        else:
            logger.error('%s' % (result[1]))

    except Exception, e:
        logger.error('Exception: %s, %s' %(e, result[1]))

    logger.debug('leave getActualIntensity')
    return result

class Timeout(IOError):
    pass

def main():
    pass

##### Module test ####
if __name__ == '__main__':

    import sys
    import common.target.common_lib.st_env_lib as st_env_lib
    st_env_lib.executeFunction(sys.argv)

    st_env_lib.setUp()
    ###########TEST AREA START###############

    ###########TEST AREA END###############
    st_env_lib.tearDown()
