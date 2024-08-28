#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2009 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained
# herein confidential and shall protect the same in whole or in partF
# from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################
from java.lang import System
import parameterHandler as ph


def getConfig(controllers, payloads, testConfigFile):


    #controllers = int(readFromFile('nodes', 'SC')[0])
    #payloads = int(readFromFile('nodes','PL')[0])
    #configuration = readFromFile('configuration','CONFIG')[0]
    #controllers = 2
    #payloads = 6
    subrack = 2
    hostNameSeparator = str(System.getProperty("hostnameSeparator"))
    config = ph.getXmlConfig(testConfigFile)
                  
    testConfig = {'testNodes': ph.getData(config, 'testNodes'),
                  'testNodesTypes': ph.getData(config, 'testNodesTypes'),
                  'testNodesNames': ph.getData(config, 'testNodesNames'),
                  'controllers': ph.getData(config, 'controllers'),
                  'payloads': ph.getData(config, 'payloads'),
                  'testAppEnabledBlades': {'sc': ph.getData(config, 'testAppEnabledBlades:sc'), 
                                           'pl': ph.getData(config, 'testAppEnabledBlades:pl'),
                                           'all': ph.getData(config, 'testAppEnabledBlades:all'),
                                           'onesc': ph.getData(config, 'testAppEnabledBlades:onesc'),
                                           'onepl': ph.getData(config, 'testAppEnabledBlades:onepl')},
                  'testCoordEnabledBlades': {'sc': ph.getData(config, 'testCoordEnabledBlades:sc'),
                                             'pl': ph.getData(config, 'testCoordEnabledBlades:pl'),
                                             'all': ph.getData(config, 'testCoordEnabledBlades:all'),
                                             'onesc': ph.getData(config, 'testCoordEnabledBlades:onesc'),
                                             'onepl': ph.getData(config, 'testCoordEnabledBlades:onepl')},
                  'testGenEnabledBlades': {'sc': ph.getData(config, 'testGenEnabledBlades:sc'),
                                           'pl': ph.getData(config, 'testGenEnabledBlades:pl'),
                                           'all': ph.getData(config, 'testGenEnabledBlades:all'),
                                           'onesc': ph.getData(config, 'testGenEnabledBlades:onesc'),
                                           'onepl': ph.getData(config, 'testGenEnabledBlades:onepl')},
                  'testInstanceConfiguration': {'sc': { 'load' : ph.getData(config, 'testInstanceConfiguration:sc:load'), 
                                                       'profile': ph.getData(config, 'testInstanceConfiguration:sc:profile')},
                                                'pl': { 'load' : ph.getData(config, 'testInstanceConfiguration:pl:load'),
                                                       'profile': ph.getData(config, 'testInstanceConfiguration:pl:profile')},
                                                'all': { 'load' : ph.getData(config, 'testInstanceConfiguration:all:load'),
                                                         'profile': ph.getData(config, 'testInstanceConfiguration:all:profile')},
                                                'onesc':{ 'load' : ph.getData(config, 'testInstanceConfiguration:onesc:load'),
                                                         'profile': ph.getData(config, 'testInstanceConfiguration:onesc:profile')}, 
                                                'onepl': { 'load' : ph.getData(config, 'testInstanceConfiguration:onepl:load'),
                                                           'profile': ph.getData(config, 'testInstanceConfiguration:onepl:profile')}},
                  'testNodesNames':ph.getData(config, 'testNodesNames'),
                  'vipEnabledBlades':ph.getData(config, 'vipEnabledBlades'),
                  'switches':  ph.getData(config, 'switches'),
                  'configCode': ph.getData(config, 'configCode') }

    
    nodes = int(controllers) + int(payloads)

    for i in range(controllers) :       
        testConfig['testNodesTypes'].append('SC')
        testConfig['controllers'].append((subrack, i+1))
        testConfig['testAppEnabledBlades']['sc'].append((subrack, i+1))
        testConfig['testAppEnabledBlades']['all'].append((subrack, i+1))
        
    for i in range(payloads) :
        testConfig['testNodesTypes'].append('PL')
        testConfig['payloads'].append((subrack, i+3))
        testConfig['testAppEnabledBlades']['pl'].append((subrack, i+3))
        testConfig['testAppEnabledBlades']['all'].append((subrack, i+3))

    for i in range(nodes) :
        testConfig['testNodes'].append((subrack, i+1))
        testConfig['testNodesNames'].append('%s%s%d%s%d' % (testConfig['testNodesTypes'][i],
            hostNameSeparator, subrack,hostNameSeparator, i+1 ))
    
    return testConfig
