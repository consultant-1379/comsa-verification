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

import sys
import string
from java.lang import System
import random
import os

import importHandler as ih
import parameterHandler as ph

def populateTestCases(testSuiteConfig, testConfig, randomSuite=False, clcTestSuite=False):
    
    #testCaseConfRepository = ph.getData(testSuiteConfig,'config:configRepository')
    #testCaseRepository = ph.getData(testSuiteConfig,'config:testcaseRepository')
    
    testCaseRepository = str(System.getProperty("testCaseRepository"))
    testCaseConfRepository = str(System.getProperty("testCaseConfRepository"))

    #get test cases
    testCases = []
    
    idx = 1   
    while testSuiteConfig.has_key('testcase'+str(idx)):
        testCases.append('testcase'+str(idx))
        idx = idx+1

    #will hold the list of populated test cases handed to unit test 
    testCasesInstances=[]
    #Handle the test cases  
    sys.path.insert(0, testCaseRepository)
    
    if clcTestSuite:
        testCaseList = []
        
        for testCase in testCases:
            testCaseTag = ph.getData(testSuiteConfig,'%s:tag' % testCase) 
            testCaseConfigName = ph.getData(testSuiteConfig,'%s:config' % testCase)
            testCaseInstances = ph.getData(testSuiteConfig,'%s:iter' % testCase)
            testCaseTest = ph.getData(testSuiteConfig,'%s:test' % testCase)
            for iter in range(1, testCaseTest+1):
                testCaseList.append([testCaseTag, testCaseConfigName])
            
        random.shuffle(testCaseList)
        
        filename = "%s/jcat_com_sa/src/test_env/testsuites/coremw/clcTestSuite2.xml" % (os.environ['MY_WORKSPACE'])
        file = open(filename,"w")
        file.close()
        file = open(filename,"a")        
        file.write("""<?xml version="1.0" encoding="utf-8"?>
<testsuite>
    <info>
        <id>testsuite</id>
        <version>P1A01</version>
        <description>Core middle ware test suite</description>        
    </info>
    <defaultSuiteCheck>    
        <setup>
            <hw>['system','switches','network']</hw>
            <os>['lotc','vip']</os>
            <mw>['coreMw']</mw>
            <appl>['testApp','ntfsub']</appl>
            <interfaces>['ctrl1','ctrl2','vip']</interfaces>
            <events>['load','traps','dumps','statistics','address','log']</events>
            <info>['amf-state node','immfind | wc -l']</info>
            <cleanup>['imm','swm_lock']</cleanup> 
        </setup>
        <runtest>
            <hw>['system','switches','network']</hw>
            <os>['lotc','vip']</os>
            <mw>['coreMw']</mw>
            <appl>['testApp','ntfsub']</appl>
            <interfaces>['ctrl1','ctrl2','vip']</interfaces>
            <events>['load','traps','dumps','statistics','address','log']</events>
            <info>['amf-state node','immfind | wc -l']</info>
            <cleanup>['imm','swm_lock']</cleanup> 
        </runtest>
        <teardown>
            <hw>['system','switches','network']</hw>
            <os>['lotc','vip']</os>
            <mw>['coreMw']</mw>
            <appl>['testApp','ntfsub']</appl>
            <interfaces>['ctrl1','ctrl2','vip']</interfaces>
            <events>['load','traps','dumps','statistics','address','log']</events>
            <info>['amf-state node','immfind | wc -l']</info>
            <cleanup>['imm','swm_lock']</cleanup> 
        </teardown>
    </defaultSuiteCheck>
    <timingParams>
        <nodeRepTime>420</nodeRepTime>
        <clusterRepTime>780</clusterRepTime>      
    </timingParams>
    <safcomponents>
        <mw>['CPD','CPND','DTS','EDS','FMS','GLD','GLND','IMMD','IMMND','LOG','MQD','MQND','NTF','PL_tspsaf_eam_Comp','RDE','SC_tspsaf_eam_Comp']</mw>
        <ntfsubscrib>['ntfSubscribeApp']</ntfsubscrib>
        <testapp>['ta_tapp_all','ta_tapp_onepl','ta_tapp_onesc','ta_tapp_pl','ta_tapp_sc','ta_tgc_all','ta_tgc_onepl','ta_tgc_onesc','ta_tgc_pl','ta_tgc_sc','ta_tgen_all','ta_tgen_onepl','ta_tgen_onesc','ta_tgen_sc']</testapp>      
    </safcomponents>""")
 
        i=1
        for testCase in testCaseList:
            testCaseTag = testCase[0];
            testCaseConfigName = testCase[1];
            file.write("""\n\t<testcase%s>
        <tag>%s</tag>    
        <config>%s</config>
        <useDefaultSuiteCheck>True</useDefaultSuiteCheck>
        <key>fgd</key>
        <iter>''</iter>    
        <assertOnError>true</assertOnError>
    </testcase%s>""" % (i, testCaseTag, testCaseConfigName, i))
            i=i+1
        file.write("""\n</testsuite>""")
        file.close()
    
        print '%s created' % filename
        exit(1)
    
    if randomSuite:
        random.shuffle(testCases)        
        #If testCases contains TC-MISC-002 - remove it and add it first
        for testCase in testCases:
            if 'TC-MISC-002' == ph.getData(testSuiteConfig,'%s:tag' % testCase):
                testCases.remove(testCase)
                testCases.insert(0, testCase)
        
        #If testCases contains TC-MAINT-017 - remove it and add it right after TC-MAINT-018
        for testCase in testCases:
            if 'TC-MAINT-017' == ph.getData(testSuiteConfig,'%s:tag' % testCase):
                testCases.remove(testCase)
                index = 0
                for item in testCases:
                    if 'TC-MAINT-018' == ph.getData(testSuiteConfig,'%s:tag' % item):
                        break
                    index = index + 1
                testCases.insert(index+1, testCase)
        
        #Create and save the suite in randomSuite
        filename = "%s/jcat_com_sa/src/test_env/testsuites/coremw/randomSuite.xml" % (os.environ['MY_WORKSPACE'])
        file = open(filename,"w")
        file.close()
        file = open(filename,"a")        
        file.write("""<?xml version="1.0" encoding="utf-8"?>
<testsuite>
    <info>
        <id>testsuite</id>
        <version>P1A01</version>
        <description>Core middle ware test suite</description>        
    </info>
    <defaultSuiteCheck>    
        <setup>
            <hw>['system','switches','network']</hw>
            <os>['lotc','vip']</os>
            <mw>['coreMw']</mw>
            <appl>['testApp','ntfsub']</appl>
            <interfaces>['ctrl1','ctrl2','vip']</interfaces>
            <events>['load','traps','dumps','statistics','address','log']</events>
            <info>['amf-state node','immfind | wc -l']</info>
            <cleanup>['imm','swm_lock']</cleanup> 
        </setup>
        <runtest>
            <hw>['system','switches','network']</hw>
            <os>['lotc','vip']</os>
            <mw>['coreMw']</mw>
            <appl>['testApp','ntfsub']</appl>
            <interfaces>['ctrl1','ctrl2','vip']</interfaces>
            <events>['load','traps','dumps','statistics','address','log']</events>
            <info>['amf-state node','immfind | wc -l']</info>
            <cleanup>['imm','swm_lock']</cleanup> 
        </runtest>
        <teardown>
            <hw>['system','switches','network']</hw>
            <os>['lotc','vip']</os>
            <mw>['coreMw']</mw>
            <appl>['testApp','ntfsub']</appl>
            <interfaces>['ctrl1','ctrl2','vip']</interfaces>
            <events>['load','traps','dumps','statistics','address','log']</events>
            <info>['amf-state node','immfind | wc -l']</info>
            <cleanup>['imm','swm_lock']</cleanup> 
        </teardown>
    </defaultSuiteCheck>
    <timingParams>
        <nodeRepTime>420</nodeRepTime>
        <clusterRepTime>780</clusterRepTime>      
    </timingParams>
    <safcomponents>
        <mw>['CPD','CPND','DTS','EDS','FMS','GLD','GLND','IMMD','IMMND','LOG','MQD','MQND','NTF','PL_tspsaf_eam_Comp','RDE','SC_tspsaf_eam_Comp']</mw>
        <ntfsubscrib>['ntfSubscribeApp']</ntfsubscrib>
        <testapp>['ta_tapp_all','ta_tapp_onepl','ta_tapp_onesc','ta_tapp_pl','ta_tapp_sc','ta_tgc_all','ta_tgc_onepl','ta_tgc_onesc','ta_tgc_pl','ta_tgc_sc','ta_tgen_all','ta_tgen_onepl','ta_tgen_onesc','ta_tgen_sc']</testapp>      
    </safcomponents>""")
        
        i=1
        for testCase in testCases:
            testCaseTag = ph.getData(testSuiteConfig,'%s:tag' % testCase) 
            testCaseConfigName = ph.getData(testSuiteConfig,'%s:config' % testCase)
            testCaseInstances = ph.getData(testSuiteConfig,'%s:iter' % testCase)
            if testCaseInstances == '':
                testCaseInstances = "''"
            file.write("""\n\t<testcase%s>
        <tag>%s</tag>    
        <config>%s</config>
        <useDefaultSuiteCheck>True</useDefaultSuiteCheck>
        <key>fgd</key>
        <iter>%s</iter>    
        <assertOnError>true</assertOnError>
    </testcase%s>""" % (i, testCaseTag, testCaseConfigName, testCaseInstances, i))
            i=i+1
        file.write("""\n</testsuite>""")
        file.close()
    
    for testCase in testCases:
        instances = []
        
        testCaseConfigName = ph.getData(testSuiteConfig,'%s:config' % testCase)
        testCaseTag = ph.getData(testSuiteConfig,'%s:tag' % testCase) 
        testCaseInstances = ph.getData(testSuiteConfig,'%s:iter' % testCase) 
        #get configuration
        testCaseConfig = ph.getXmlConfig(testCaseConfRepository+testCaseConfigName)     
        #import class
        testCaseName = ph.getData(testCaseConfig,'info:testcase')
        className = ph.getData(testCaseConfig,'info:class')
        tcName = ph.getData(testCaseConfig,'info:id')
        currentClass = ih.importName(testCaseName, className )
        getSuite = ih.importName(testCaseName, 'getSuite' )
        temp = getSuite(testCaseTag, tcName, testConfig, testSuiteConfig, testCaseConfig,testCaseInstances,currentClass)
        instances = instances + temp
      
        
        config = ph.getConfigData(testCaseConfig)
        #suite = getSuite('')
        # Add the condition "or (testCaseName == 'cmActionTestCaseNew' and c.startswith('expected_trace_value'))"
        # for improvement task43817, in case number of expected_trace_value > 20
        for s in instances:
            for c in config.keys():
                if hasattr(s,c) or (testCaseName == 'cmActionTestCaseNew' and c.startswith('expected_trace_value')):
                    try:
                        for k in config[c].keys():
                            setattr(s,c,(config[c][k]))
                    except Exception, e:
                        print e
        
        for instance in instances:

            try:
                print dir(instance.testProcessRestart)
            except:
                pass
            testCasesInstances.append(instance)
    sys.path.pop(0)           
    return testCasesInstances

if __name__ == "__main__":
    pass    
    
