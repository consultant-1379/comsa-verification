#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2014 All rights reserved.
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

   Author: esaahas

   Description: An adapter to the tracecc command that makes it easy 
   to start tracing on a specific domain and level and parse the trace lines.
   
   Usage Steps 
   1. Create a TraceCC object (specify the trace domain and trace level)
   2. Do something that will make the system trace
   3. Call howManyLinesHaveThis to see how many lines matches your search criteria
      Send empty strings for the fields you don't care about
   4. Call howManyLinesHaveThis to see how many lines matches another search criteria and so on...
   
   Modify: uabjoy
   Adding a retry method to the tracecc commands access since the test cases using this class are unstable because of 
   the return value SA_AIS_ERR_TIMEOUT that quit frequently happens on some test clusters.
'''

from org.apache.log4j import Logger 
import omp.tf.ssh_lib as ssh_lib
from random import randint
from org.apache.log4j import Level
from java.lang import System
class TraceCC:
        def __init__(self, traceDomain, traceLevel):
            logLevel = System.getProperty("jcat.logging")
            global ssh_lib
            global logger
            logger = Logger.getLogger('trace_cc_lib')
            logger.setLevel(Level.toLevel(logLevel))
            logger.info("trace_lib_cc: Initiating!")

            self.domain = traceDomain
            self.level = traceLevel
            self.currentProfile = ""
            self.currentRecording = ""
            self.currentTraceLines = []
            
            self.cmdNotFound = 'command not found'
            
            # Control value for number of retries using the tracecc cli
            self.numberOfRetriesTraceCLI = 3
            
            self.__cleanOldProfiles()
            self.__cleanOldRecordings()
            self.__startTracing()
            
        def __sendTraceCCCommand(self, cmd):
            for retryNo in range(self.numberOfRetriesTraceCLI):
                result = ssh_lib.sendCommand(cmd)
                if result[0] == 'SUCCESS' and len(result[1])==0:
                    logger.info('Retry %s' %(cmd))
                    return result
            return result

            
        def __cleanOldProfiles(self):
            result = ssh_lib.sendCommand('tracecc-profile-list')
            if result[0] != 'SUCCESS' or ('ERROR' in ''.join(result)) or (self.cmdNotFound in result[1]):
                logger.error('Could not list profiles')
                return ('ERROR', result[1])
            profiles = result[1].splitlines();
            for profile in profiles:
                result = self.__sendTraceCCCommand('tracecc-profile-deactivate %s' %(profile))
                if result[0] != 'SUCCESS' or len(result[1])!=0:
                    logger.error('Execution of %s was not successful.' %('tracecc-profile-deactivate %s' %(profile)))
                    return ('ERROR', result[1])
                #result = ssh_lib.sendCommand('tracecc-profile-deactivate %s' %(profile))
                result = self.__sendTraceCCCommand('tracecc-profile-delete %s' %(profile))
                #result = ssh_lib.sendCommand('tracecc-profile-delete %s' %(profile))
                if result[0] != 'SUCCESS' or len(result[1])>0:
                    logger.error('Could not delete profile')
                    return ('ERROR', result[1])
            
        def __cleanOldRecordings(self):
            result = ssh_lib.sendCommand('tracecc-recording-list')
            if result[0] != 'SUCCESS' or ('ERROR' in ''.join(result)) or (self.cmdNotFound in result[1]):
                logger.error('Could not list recordings')
                return ('ERROR', result[1])
            recordings = result[1].splitlines();
            for recording in recordings:
                '''result = self.__sendTraceCCCommand('tracecc-profile-deactivate %s' %(recording))
                if result[0] != 'SUCCESS' or len(result[1])!=0:
                    logger.error('Execution of %s was not successful.' %('tracecc-profile-deactivate %s' %(recording)))
                    return ('ERROR', result[1])'''
                #result = ssh_lib.sendCommand('tracecc-recording-deactivate %s' %(recording))
                result = self.__sendTraceCCCommand('tracecc-recording-delete %s' %(recording))
                #result = ssh_lib.sendCommand('tracecc-recording-delete %s' %(recording))
                if result[0] != 'SUCCESS' or len(result[1])>0:
                    logger.error('Could not delete recording')
                    return ('ERROR', result[1])

        def __startTracing(self): 
            self.currentProfile = 'profile%u' %(randint(2,1000))
            result = self.__sendTraceCCCommand('tracecc-profile-create -t \"%s, %s\" %s' %(self.domain, self.level, self.currentProfile))
            # result = ssh_lib.sendCommand('tracecc-profile-create -t \"%s, %s\" %s' %(self.domain, self.level, self.currentProfile))
            if result[0] != 'SUCCESS' or len(result[1])>0:
                logger.error('Failed Creating profile')
                return ('ERROR', result[1])
            result = self.__sendTraceCCCommand('tracecc-profile-activate -f %s' %(self.currentProfile))
            #result = ssh_lib.sendCommand('tracecc-profile-activate -f %s' %(self.currentProfile))
            if result[0] != 'SUCCESS' or  len(result[1])>0:
                logger.error('Failed activating profile')
                return ('ERROR', result[1])
                
        def __stopTracing(self):
            result = self.__sendTraceCCCommand('tracecc-profile-deactivate %s' %(self.currentProfile))
            #result = ssh_lib.sendCommand('tracecc-profile-deactivate %s' %(self.currentProfile))
            if result[0] != 'SUCCESS' or  len(result[1])>0:
                logger.error('Failed deactivating profile')
                return ('ERROR', result[1])
                
        def __convertTrace(self):
            result = ssh_lib.sendCommand('tracecc-recording-list')
            if result[0] != 'SUCCESS' or ('ERROR' in ''.join(result)) or (self.cmdNotFound in result[1]):
                logger.error('Could not list recording')
                return ('ERROR', result[1])
            
            recordingList=result[1].splitlines()
            if len(recordingList)==0:
                logger.error('Could not find any recordings')
                return ('ERROR', result[1]) 
            
            foundRecording = False
            for recording in recordingList:
                if self.currentProfile in recording:
                    foundRecording = True
                    self.currentRecording = recording
                    result = ssh_lib.sendCommand('tracecc-recording-convert %s' %(recording))                    
                    # ejnolsz: why do we need this break here. The code below it will never be executed.
                    break
                    if result[0] != 'SUCCESS' or len(result[1])>0:
                        logger.error('Could not convert recording')
                        return ('ERROR', result[1])
            
            if foundRecording == False:
                logger.error('Could not find any recording for the profile %s' %(self.currentProfile))
                return ['ERROR','Could not find any recording for the profile %s' %(self.currentProfile)] 
            
            result = ssh_lib.sendCommand('cat /storage/no-backup/tracecc*/%s/Converted_logs/Node_SC*'  %(self.currentRecording))
            if result[0] != 'SUCCESS':
                logger.error('Could not read trace file')
                return ('ERROR', result[1])
            self.currentTraceLines = result[1].splitlines();
            
            #Use this when debugging, it will print all trace lines in the log
            #===================================================================
            # for line in self.currentTraceLines:
            #     logger.info(line)
            #===================================================================
                
    
        def howManyLinesHaveThis(self, domain, event, processName, string):
            if len(self.currentTraceLines) == 0:
                self.__stopTracing()
                self.__convertTrace()
            if len(self.currentTraceLines) == 0:
                logger.error('There are no trace lines to parse')
                return ['ERROR','There are no trace lines to parse']
            foundLines = 0
            domainString = "" if domain == "" else '] %s:' %(domain)
            eventString = "" if event == "" else ':%s: {' %(event)
            processString = "" if processName == "" else '}, { "%s",' %(processName)
            traceString = "" if string == "" else '}, { string = "%s" }' %(string)
            
            searchArray = [domainString, eventString, processString, traceString]
         
            for line in self.currentTraceLines:
                matches = 0
                for searchText in searchArray:
                    if searchText =="" or searchText in line:
                        matches +=1
                    else:
                        break
                if matches == len(searchArray):
                    foundLines +=1
            logger.info('found %u lines' %(foundLines))
            return ['SUCCESS',foundLines]
        
        def matchDomainAndTestString(self, stringMatch, traceLevelName, domaineName, functionName):
            if len(self.currentTraceLines) == 0:
                self.__stopTracing()
                self.__convertTrace()
            if len(self.currentTraceLines) == 0:
                logger.error('There are no trace lines to parse')
                return ['ERROR','There are no trace lines to parse']
            match = 0
            foundOneLine = False
            searchArray = [stringMatch, traceLevelName, domaineName, functionName]
            for line in self.currentTraceLines:
                match = 0
                for searchText in searchArray:
                    if searchText == "" or searchText in line:
                        match += 1
                    else:
                        match = 0
                    # Check that we do not have absolute paths in source line
                    if 'Source = "/' in line:
                        logger.info('absolute source path in trace')
                        return ['ERROR','absolute path in trace']
                if match == len(searchArray):
                    logger.info('match line %s' %(line))
                    foundOneLine = True
                    break # We are done, found the line
            if foundOneLine == True:
                logger.info('match line')
                return ['SUCCESS','match line']
            else:
                logger.info('no match line')
                return ['ERROR','no match line']
                
        def matchNoDomain(self, domaineName):
            if len(self.currentTraceLines) == 0:
                self.__stopTracing()
                self.__convertTrace()
            if len(self.currentTraceLines) == 0:
                logger.error('There are no trace lines to parse')
                return ['ERROR','There are no trace lines to parse']
            match = 0
            searchArray = [domaineName]
            for line in self.currentTraceLines:
                for searchText in searchArray:
                    if searchText == "" or searchText in line:
                        match += 1
            if match == 0:
                logger.info('no match line')
                return ['SUCCESS','no match line']
            else:
                logger.info('match line')
                return ['ERROR','match line']
            
