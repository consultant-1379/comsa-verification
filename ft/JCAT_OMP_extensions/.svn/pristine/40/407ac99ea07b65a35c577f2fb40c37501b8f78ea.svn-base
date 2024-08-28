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
   %CCaseFile:  cleartool_lib.py %
   %CCaseRev:   /main/R1A/1 % 
   %CCaseDate:  2008-02-27 % 

   Description:
   This module acts as clearcase interface for the test environment

'''
import re
import os
import commands
import popen2
import time

import org.apache.log4j.Logger as Logger

import se.ericsson.jcat.omp.library.CleartoolLib as CleartoolLib
import se.ericsson.commonlibrary.CommonLibrary as CommonLibrary
import se.ericsson.commonlibrary.CommonLibraryDataProvider as CommonLibraryDataProvider
import java.util.ArrayList as ArrayList

class cleartool(CleartoolLib, CommonLibrary):
    '''
    classdocs
    '''
    logger = Logger.getLogger('cleartool')
    CC = None
    
    def setLibraryDataProvider(self, data):
        self.data = data;

    def getLibraryDataProvider(self):
        return self.data;

    def getLibraryInterface(self):
        return CleartoolLib;

    def getUniqueIdentifier(self):
        return "cleartool";

    def initialize(self):
        self.logger.debug('CleartoolLib initialize')
        self.CC = cClearCase() 

    def shutdown(self):
        pass

    def getRuntimeDependencyList(self):
        a = ArrayList();
        return a;

    def getSetupDependencyList(self):
        a = ArrayList();
        return a;

    def getClearcaseCommand(self):
        return '/usr/atria/bin/cleartool'
    
    def isElement(self, file):
        self.logger.trace('entering isElement')
    
        result = ['ERROR', False]
        cmd = 'cleartool ls -d %s' % (file)
    
        if not os.path.exists(file):
            self.logger.error('%s' % result[1])
            
        else:
            result = self.CC.executeCommand(cmd)
            output = result[1].split('\n', 1)
            fileName = output[0]
            expression = '^(.*)@@(.*)$'
            pattern = re.compile(expression)
            mo = pattern.search(fileName)
            if (mo):
                result = ['SUCCESS', True]
            else:
                result = ['SUCCESS', False]
                self.logger.debug('File is not an element %s' % (file))
            
        self.logger.trace('leaving isElement: %s' % (result))
        return result

    def getStreamData(self, stream):
    
        self.logger.trace('entering getStreamData')
        streamData = {}
        state = ''
    
        cmd = 'cleartool lsstream -l %s' % (stream)
        result = self.CC.executeCommand(cmd)
    
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'SUCCESS':
            output = new_result[1].split('\n')
            for line in output[:-2]:
                pattern0 = re.compile('^(stream).*$|^\s*(\d.*)$|^.*UCM4E Stream.*$|^.*ICE release.*$')
                pattern1 = re.compile('\s*(contains activities:|foundation baselines:|recommended baselines:|development streams:|views:|policies:|policies \(effective\):)')
                pattern2 = re.compile('(owner:|group:|project:|default deliver stream:|baseline naming template:|master replica:)\s*(.*)')
                pattern3 = re.compile('^\s*(\S*)\s*(.*)$')
    
                if line <> '':
                    mo0 = pattern0.search(line)
                    if (mo0):
                        state = ''
                    else:
                        mo1 = pattern1.search(line)
                        if (mo1):
                            state = mo1.group(1)
                            streamData[state] = []
                        else:
                            mo2 = pattern2.search(line)
                            if (mo2):
                                state = ''
                                streamData[mo2.group(1)] = mo2.group(2)
                            else:
                                mo3 = pattern3.search(line)
                                if (mo3):
                                    if state <> '':
                                        list = streamData[state]
                                        list.append(mo3.group(1))
                                        streamData[state] = list
    
            new_result[1] = streamData
        else:
            self.logger.error('ClearCase command failed with: %s' % new_result[1])
    
        self.logger.trace('leaving getStreamData')
        return new_result

    def getCurrentStream(self):
    
        self.logger.trace('entering getCurrentStream')
    
        cmd = 'cleartool lsstream'
    
        result = self.CC.executeCommand(cmd)
        
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'SUCCESS':
            new_result[1] = new_result[1].split(' ')[2]
        else:
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        self.logger.trace('leaving getCurrentStream')
        return new_result    

    def catcs(self):
        self.logger.trace('entering catcs')
        cmd = 'cleartool catcs'
    
        result = self.CC.executeCommand(cmd)
        self.logger.trace('leaving catcs')
        return result

    def setcs(self, cs):
        self.logger.trace('entering setcs')
        cmd = 'cleartool setcs %s' % (cs)
    
        result = self.CC.executeCommand(cmd)
        self.logger.trace('leaving setcs')
        return result
    
    def refresh(self):
        self.logger.trace('entering refresh')
        cmd = 'u4e chview -cview -refresh'
    
        result = self.CC.executeCommand(cmd)
        self.logger.trace('leaving refresh')
        return result

    def getCheckedOutFiles(self, stream, recursive = True):
        self.logger.trace('entering getCheckedOutFiles1')
        coFiles = []
        result = self.getStreamChangeSet(stream, recursive)
        if result[0] == 'SUCCESS':
            changeSet = result[1][0]
            for file in changeSet:
                pattern = re.compile('CHECKEDOUT')
                mo = pattern.search(file)
                if (mo):
                    coFiles.append(file)
            result[1] = coFiles
    
        self.logger.trace('leaving getCheckedOutFiles')
        return result

    def getStreamChangeSet(self, stream, recursive = True):
        self.logger.trace('entering getStreamChangeSet')
        changeSet = []
        vqChangeSet = []
        result = self.getStreamData(stream)
        if result[0] == 'SUCCESS':
            streamData = result[1]
    
            activities = streamData['contains activities:']
            for activity in activities:
                result = self.getActivityData(activity)
                if result[0] == 'SUCCESS':
                    files = result[1]['change set versions:']
                    for file in files:
                        pattern = re.compile('(.*)@@(.*)')
                        mo = pattern.search(file)
                        if (mo):
                            vqFile = mo.group(1)
                            if file not in changeSet:
                                changeSet.append(file)
                            if vqFile not in vqChangeSet:
                                vqChangeSet.append(vqFile)
                        elif file <> '':
                            result[0] = 'ERROR'
                            logger.error('Pattern not matching: %s' % (file))
            result[1] = []
            result[1].append(changeSet)
            result[1].append(vqChangeSet)
    
        if result[0] == 'SUCCESS':
            if recursive:
                for subStream in streamData['development streams:']:
                    result = self.getStreamChangeSet(subStream, recursive)
                    if result[0] == 'SUCCESS':
                        for file in result[1][0]:
                            pattern = re.compile('(.*)@@(.*)')
                            mo = pattern.search(file)
                            if (mo):
                                vqFile = mo.group(1)
                                if file not in changeSet:
                                    changeSet.append(file)
                                if vqFile not in vqChangeSet:
                                    vqChangeSet.append(vqFile)
                            else:
                                result[0] = 'ERROR'
                                self.logger.error('Pattern not matching: %s' % (file))
                result[1][0] = changeSet
                result[1][1] = vqChangeSet
    
        self.logger.trace('leaving getStreamChangeSet')
        return result

    def getActivityData(self, activity):
        self.logger.trace('entering getActivityData')
        activityData = {}
        state = ''
    
        cmd = 'cleartool lsact -l %s' % (activity)
    
        result = self.CC.executeCommand(cmd)
    
        if result[0] == 'SUCCESS':
            output = result[1].split('\n', 1)[1]
            output = output.split('\n')
            state = ''
            for line in output:
                pattern0 = re.compile('^(activity).*$|^\s*(\d.*)$|^\s*".*$|^\s*$')
                pattern1 = re.compile('\s*(change set versions:)')
                pattern2 = re.compile('(master replica:|owner:|group:|stream:|project:|title:|:)\s*(.*)')
                pattern3 = re.compile('^\s*(\S*)\s*(.*)$')
    
                mo0 = pattern0.search(line)
                if (mo0):
                    state = ''
                else:
                    mo1 = pattern1.search(line)
                    if (mo1):
                        state = mo1.group(1)
                        activityData[state] = []
                    else:
                        mo2 = pattern2.search(line)
                        if (mo2):
                            state = ''
                            activityData[mo2.group(1)] = mo2.group(2)
                        else:
                            mo3 = pattern3.search(line)
                            if (mo3):
                                list = activityData[state]
                                list.append(mo3.group(1))
                                activityData[state] = list
                result = ['SUCCESS', activityData]
    
        self.logger.debug("Activity Data = %s" % (result[1]))
        self.logger.trace('leaving getActivityData')
        return result

    def getCurrentView(self):
        self.logger.trace('entering getCurrentView')
    
        cmd = 'cleartool pwv -short'
    
        result = self.CC.executeCommand(cmd)
        if result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
            self.logger.trace('leaving getCurrentView')
            return (result)
        else:
            result = ('SUCCESS', result[1].strip())
    
        self.logger.trace('leaving getCurrentView')
        return result

    def isCheckedOut(self, file):
        self.logger.trace('entering isCheckedOut')
    
        result = ['ERROR', False]
        cmd = 'cleartool ls -d -s %s' % (file)
    
        if not os.path.exists(file):
            self.logger.debug('%s does not exist' % file)
        else:
            result = self.CC.executeCommand(cmd)
    
            output = result[1].split('\n', 1)
            fileName = output[0]
            expression = '^(.*)@@.*(CHECKEDOUT).*$'
            pattern = re.compile(expression)
            mo = pattern.search(fileName)
            if (mo):
                result = ['SUCCESS', True]
                self.logger.debug('%s' % result[1])
    
            else:
                result = ['SUCCESS', False]
                self.logger.debug('%s' % result[1])
            
        self.logger.trace('leaving isCheckedOut')
        return result

    def getBranchHistory1Day(self, branch = 'main', vobPath = '/vobs/tsp*saf/*'):
        self.logger.trace('entering getBranchHiostory1Day')
        result = self.getBranchHistory(branch = branch, since = 86400, vobPath = vobPath)
        self.logger.trace('leaving getBranchHistory1Day')
        return result
    
    def getBranchHistory1Hour(self, branch = 'main', vobPath = '/vobs/tsp*saf/*'):
        self.logger.trace('entering getBranchHistory1Hour')
        result = self.getBranchHistory(branch = branch, since = 3600, vobPath = vobPath)
        self.logger.trace('leaving getBranchHistory1Day')
        return result
    
    def getBranchHistory1Week(self, branch = 'main', vobPath = '/vobs/tsp*saf/*'):
        self.logger.trace('entering getBranchHistory1Week')
        result = self.getBranchHistory(branch = branch, since = 604800, vobPath = vobPath)
        self.logger.trace('leaving getBranchHistory1Week')
        return result
    
    def getBranchHistory1Month(self, branch = 'main', vobPath = '/vobs/tsp*saf/*'):
        self.logger.trace('entering getBranchHistory1Month')
        result = self.getBranchHistory(branch = branch, since = 2592000, vobPath = vobPath)
        self.logger.trace('leaving getBranchHistory1Month')
        return result
    
    def getBranchHistory(self, branch = 'main', since = 86400, vobPath = '/vobs/tsp*saf/*'):
        self.logger.trace('entering getBranchHistory')
    
        now = time.time()
        historyFrom = now - since
        timeString = time.strftime('%d-%b-%Y.%H:%M:%S', time.gmtime(historyFrom))
        
        cmd = 'cleartool lshistory -s -r -branch %s -since %s %s' % (branch, timeString, vobPath)
        
        result = self.CC.executeCommand(cmd, timeout = 3600)
        if result[0] == 'SUCCESS':
            output = result[1].splitlines()
    
        vobObjects = []
        vobObjects2 = []
        for object in output:
            file = re.sub('@@.*', '', object)
            if ((file.find('lost+found') < 0) and (file.find('cleartool: Error') < 0)) :
                vobObjects2.append(object)
                if file not in vobObjects:
                    vobObjects.append(file)
    
        result = ['SUCCESS', [vobObjects, vobObjects2]]
        self.logger.trace('leaving getBranchHistory')
        return result

    def getAllStreams(self, stream):
        self.logger.trace('entering getAllStreams')
        openStreams = []
        result = self.getStreamData(stream)
        if result[0] == 'SUCCESS':
            streamData = result[1]
            streams = streamData['development streams:']
            result[1] = streams
        
        self.logger.trace('leaving getAllStreams')
        return result
    
    def getAllOpenStreams(self, stream):
        self.logger.trace('entering getAllOpenStreams')
        openStreams = []
        result = self.getAllStreams(stream)
        if result[0] == 'SUCCESS':
            streams = result[1]
            for stream in streams:
                if self.isStreamOpen(stream):
                    openStreams.append(stream)
            result[1] = openStreams
        
        self.logger.trace('leaving getAllOpenStreams')
        return result

    def isStreamOpen(self, stream):
        self.logger.trace('entering isStreamopen')
        cmd = 'cleartool lsstream -l %s' % (stream) 
        result = self.CC.executeCommand(cmd)
    
        output = result[1].split('\n', 1)
        streamData = output[0]
        streamData = streamData.split()
        if len(streamData) > 2:
            state = streamData[2]
            if state == '(obsolete)':
                result = ['ERROR','Stream is obsolete: %s' % (stream)]
            else:
                result = ['ERROR','Stream has state: %s' % (state)]
        else:
            result = ['SUCCESS','Stream is open: %s' % (stream)]
    
        self.logger.trace('leaving isStreamOpen')
        return result

    def getStreamActivities(self, stream):
        self.logger.trace('entering getStreamActivities')
        result = self.getStreamData(stream)
        if result[0] == 'SUCCESS':
            streamData = result[1]['contains activities:']
            result[1] = streamData
        self.logger.trace('leaving getStreamActivities')
        return result
    
    def getStreamRebaseActivities(self, stream):
        self.logger.trace('entering getStreamActivities')
        rebaseActs = []
        result = self.getStreamActivities(stream)
        if result[0] == 'SUCCESS':
            for activity in result[1]:
                if activity.find('rebase') >= 0:
                    rebaseActs.append(activity)
            result[1] = rebaseActs
    
        self.logger.trace('leaving getStreamActivities')
        return result
        
    def getStreamDeliverActivities(self, stream):
        self.logger.trace('entering getStreamDeliverActivities')
        rebaseActs = []
        result = self.getStreamActivities(stream)
        if result[0] == 'SUCCESS':
            for activity in result[1]:
                if activity.find('deliver') >= 0:
                    rebaseActs.append(activity)
            result[1] = rebaseActs
    
        self.logger.trace('leaving getStreamDeliverActivities')
        return result

    def getActivityChangeSet(self, activity):
        self.logger.trace('entering getActivityChangeSet')
        changeSet = []
        result = self.getActivityData(activity)
        if result[0] == 'SUCCESS':
            activityData = result[1]
            vqChangeSet = activityData['change set versions:']
    
            for vqFileName in vqChangeSet:
                pattern = re.compile('(.*)@@(.*)')
                mo = pattern.search(vqFileName)
                if (mo):
                    fileName = mo.group(1)
                    if file not in changeSet:
                        changeSet.append(fileName)
                else:
                    result[0] = 'ERROR'
                    self.logger.error('Pattern not matching: %s' % (file))
            result[1] = [vqChangeSet, changeSet]
        
        self.logger.trace('leaving getActivityChangeSet')
        return result

    def getAllVobObjects(self, vobPath = '/vobs/tsp*saf/*'):
        self.logger.trace('entering getAllVobObjects')
    
        cmd = 'cleartool ls -vob -recurse -s %s' % (vobPath)
    
        result = self.CC.executeCommand(cmd, timeout = 3600)
        if result[0] == 'SUCCESS':
            vobObjects = result[1].splitlines()
            fileNames = []
            for vobObject in vobObjects:
                fileName = re.sub('@@.*', '', vobObject)
                if vobObject.find('lost+found') < 0:
                    fileNames.append(fileName)
    
            result = ['SUCCESS', fileNames]
    
        self.logger.trace('leaving getAllVobObjects')
        return result

    def getBranchesWithZeroVersionOnly(self, fileName):
        self.logger.trace('entering getBranchesWithZeroVersionsOnly')
    
        result = self.getBranches(fileName)
        zeroBranches = []
        coBranches   = []
    
        if result[0] == 'SUCCESS':
            branch2versions = result[1]
            for branch in branch2versions.keys():
                versions = branch2versions[branch]
                if branch != "/main":
                    if len(versions) == 1 and versions['0'] == '':
                        #print "%s: Branch %s has only 0-element" % (fileName, branch)
                        zeroBranches.append('%s' % (branch))
        
                    if len(versions) == 2 and "CHECKEDOUT" in versions.keys():
                        #print "%s: Branch %s has only CHECKEDOUT-element" % (fileName, branch)
                        coBranches.append('%s' % (branch))
    
        self.logger.trace('leaving getBranchesWithZeroVersionOnly')
        return ('SUCCES', [zeroBranches, coBranches])

    def getBranches(self, fileName):
        # return a dictionary with the branches as keys and the versions as a list
        # accesed by the key.
        self.logger.trace('entering getBranches')
        result = ['ERROR', 'File is not an element: %s' % (fileName)]
    
        if self.isElement(fileName):
    
            cmd = 'cleartool lsvtree -a %s' % (fileName)
    
            result = self.CC.executeCommand(cmd, timeout = 600)
            if result[0] == 'SUCCESS':
                output = result[1].splitlines()
                branch2versions = {}
                for line in output:
                    expression = '^(\S*)@@(/main)$'
                    pattern = re.compile(expression)
                    
                    mo = pattern.search(line)
                    if (mo):
                        branch2versions[mo.group(2)] = {}
                        continue
                        
                    expression = '^(\S*)@@(\S*)/([0-9]+|CHECKEDOUT)\s+\((.*)\)'
                    pattern = re.compile(expression)
                    mo = pattern.search(line)
                    if (mo):
                        labels = mo.group(4).strip().split(', ')
                        if mo.group(2) in branch2versions:
                            versions = branch2versions[mo.group(2)]
                            versions[mo.group(3)] = labels
                            branch2versions[mo.group(2)] = versions
                            continue
                        else:
                            versions = {}
                            versions[mo.group(3)] = labels
                            branch2versions[mo.group(2)] = versions
                    
                    expression = '^(\S*)@@(\S*)/([0-9]+|CHECKEDOUT)'
                    pattern = re.compile(expression)
                    
                    mo = pattern.search(line)
                    if (mo):
                        if mo.group(2) in branch2versions:
                            versions = branch2versions[mo.group(2)]
                            versions[mo.group(3)] = ''
                            branch2versions[mo.group(2)] = versions
                        else:
                            versions = {}
                            versions[mo.group(3)] = ''
                            branch2versions[mo.group(2)] = versions
                        continue
                    
                result = ['SUCCESS', branch2versions ]
    
        self.logger.trace('leaving getBranches')
        return result

    def isLabelOnVersion(self, fileName, version, label):
        self.logger.trace('entering isLabelOnVersion')
        fileNameFiltered = re.sub('\$', '\$', fileName)
        result = self.getBranches(fileNameFiltered)
        if result[0] == 'SUCCESS':
            tree = result[1]
            expression = '(.*)/([0-9]+|CHECKEDOUT)'
            pattern = re.compile(expression)
            mo = pattern.search(version)
            if mo:
                branch = mo.group(1)
                version = mo.group(2)
                labels = tree[branch][version]

                if label in labels:
                    result = True
                else:
                    result = False
            else:
                result = False
        self.logger.trace('leaving isLabelOnVersion')
        return result
    
    def getFileVersion(self, fileName):
        self.logger.trace('entering getFileVersion')
        fileNameFiltered = re.sub('\$', '\$', fileName)
        command = '/usr/atria/bin/cleartool ls -long -d %s' % (fileNameFiltered)
        output = self.CC.executeCommand(command)[1]
        expression = '^.*version\s*(\S*)@@(\S*).*$'
        pattern = re.compile(expression)
        mo = pattern.search(output)
        if (mo):
            result = ['SUCCESS', '%s' % (mo.group(2))]
        else:
            result = ['ERROR', 'version not found']
    
        self.logger.trace('leaving getFileVersion')
        return result
    
    def checkOut(self,  file, comment = '.', reserved = True):
     
        self.logger.trace('entering checkOut')
    
        try:
            os.access(file, os.F_OK)
        except:
            return ('ERROR','File not found')
    
        if (reserved):
            cmd = 'cleartool checkout -reserved -c '+comment+' '+file
        else:
            cmd = 'cleartool checkout -unreserved -c '+comment+' '+file
        result = self.CC.executeCommand(cmd)
    
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(new_result[1].splitlines()[1:])
        self.logger.trace('leaving checkOut')
        return (new_result)
    
    def checkIn(self, file, comment = '.'):
        self.logger.trace('entering checkIn')
    
        try:
            os.access(file, os.F_OK)
        except:
            return ('ERROR','File not found')
    
        cmd = 'cleartool checkin -c '+comment+' '+file
        result = self.CC.executeCommand(cmd)
    
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(new_result[1].splitlines()[1:])
    
        self.logger.trace('leaving checkIn')
        return (new_result)
    
    def mkelem(self, file, comment = '.'):
        self.logger.trace('entering mkelem')
    
        cmd = 'cleartool mkelem -c '+comment+' '+file
        result = self.CC.executeCommand(cmd)
    
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'ERROR':
            logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(new_result[1].splitlines()[1:])
    
        logger.trace('leaving mkelem')
        return (new_result)
    
    def mkdir(self, directory, comment = '.'):
        self.logger.trace('entering mkdir')
    
        if os.path.exists(directory):
            return ('ERROR','%s already exists' % (directory))
    
        cmd = 'cleartool mkdir -c '+comment+' '+directory
        result = self.CC.executeCommand(cmd)
    
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(new_result[1].splitlines()[1:])
    
        self.logger.trace('leaving mkdir')
        return (new_result)
    
    def rmname(self, fileName, comment = '.'):
        self.logger.trace('entering rmname')
    
        if not os.path.exists(fileName):
            return ('ERROR','%s does not exists' % (fileName))
    
        cmd = 'cleartool rmname -c '+comment+' '+fileName
        result = self.CC.executeCommand(cmd)
    
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(new_result[1].splitlines()[1:])
    
        self.logger.trace('leaving mkdir')
        return (new_result)
    
    def unCheckOut(self, file, saveCopy= 'no'):
        logger.trace('entering unCheckOut')
    
        try:
            os.access(file, os.F_OK)
        except:
            return ('ERROR','File not found')
    
        cmd = 'cleartool uncheckout -rm '+file
    
        result = self.CC.executeCommand(cmd, saveCopy)
    
        new_result = []
        new_result.append(result[0])
        new_result.append(result[1])
        
        if new_result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(new_result[1].splitlines()[1:])
    
        self.logger.trace('leaving unCheckOut')
        return (new_result)
    
    
    def mkActivity(self, prefix ='GA', headline= 'ORBIT activity' ):
    
        self.logger.trace('entering mkActivity')
    
        cmd = 'cleartool lsactivity -me -short'
    
        result = self.CC.executeCommand(cmd)
    
        if result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
        else:
            activities = result[1].splitlines()
            act = '%s:%s' % (prefix, headline)
            for activity in activities:
                cmd = 'cleartool lsactivity %s' % activity
                result = self.CC.executeCommand(cmd)
    
                if(re.search(act, result[1])):
                    result = self.setActivity(activity)
                    self.logger.trace('leaving mkActivity')
                    return (result)                   
            
        cmd = 'cleartool mkactivity -headline %s:"%s"' % (prefix, headline)
        result = self.CC.executeCommand(cmd, arg= 'yes')
    
        if result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(result[1].splitlines()[1:])
            
        self.logger.trace('leaving mkActivity')
        return (result)
    
    
    def rmActivity(self, activity= 'ORBIT activity' ):
    
        self.logger.trace('entering rmActivity')
    
        cmd = 'cleartool lsactivity -me -short'
    
        result = self.getActivity(activity)
        
        if result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
            self.logger.trace('leaving rmActivity')
            return (result)     
        else:
            cmd = 'cleartool rmactivity -force %s' % result[1]
            result = self.CC.executeCommand(cmd, arg= 'yes')
    
            if result[0] == 'ERROR':
                self.logger.error('ClearCase command failed with: %s' % result[1])
                os.linesep.join(result[1].splitlines()[1:])
                self.logger.trace('leaving rmActivity')
                return result
            else:
                os.linesep.join(result[1].splitlines()[1:])
                self.logger.trace('leaving rmActivity')
                return (result)
    
    def getActivity(self, activity = 'ORBIT activity' ):
    
        self.logger.trace('entering getActivity')
    
        cmd = 'cleartool lsactivity -me -short'
    
        result = self.CC.executeCommand(cmd)
        if result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
        else:
            activities = result[1].splitlines()
            for act in activities:
                cmd = 'cleartool lsactivity %s' % act
                result = self.CC.executeCommand(cmd)
                
                if(re.search(activity, result[1])):
                    os.linesep.join(result[1].splitlines()[1:])
                    self.logger.trace('leaving getActivity')
                    return ('SUCCESS', act)
        return('ERROR','No activity found')
                    
    def setActivity(self, activity):
        self.logger.trace('entering setActivity')
    
        cmd = 'cleartool setactivity %s' % activity
        result = self.CC.executeCommand(cmd, arg= 'yes')
    
        if result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
    
        os.linesep.join(result[1].splitlines()[1:])
    
        self.logger.trace('leaving setActivity')
        return (result)
    
    
    def getCurrentActivity(self):
    
        self.logger.trace('entering getCurrentActivity')
    
        cmd = 'cleartool lsactivity -cact -short'
    
        result = self.CC.executeCommand(cmd)
    
        if result[0] == 'ERROR':
            self.logger.error('ClearCase command failed with: %s' % result[1])
            self.logger.trace('leaving getCurrentActivity')
            return (result)
    
        os.linesep.join(result[1].splitlines()[1:])
    
        self.logger.trace('leaving getCurrentActivity')
        return (result)
    
    def getChanges(self, fromVersion, toVersion, fileName):
        self.logger.trace('entering getChanges')
        cmd = 'cleartool diff -dif %s@@%s %s@@%s' % (fileName, fromVersion, fileName, toVersion)
    
        result = self.CC.executeCommand(cmd)
        
        self.logger.trace('leaving getChanges')
        return (result)


class cleartool_dp(CommonLibraryDataProvider):
    '''
    classdocs
    '''

    def setLibraryDataProvider(self, data):
        self.data = data;

    def getLibraryDataProvider(self):
        return self.data;

    def getLibraryInterface(self):
        return CommonLibrary;

    def getUniqueIdentifier(self):
        return "cleartool_dp";

    def initialize(self):
        pass

    def shutdown(self):
        pass

    def getRuntimeDependencyList(self):
        a = ArrayList();
        return a;

    def getSetupDependencyList(self):
        a = ArrayList();
        return a;

###############################################################################
# setUp / tearDown
###############################################################################

def setUp():
    """This function fetches required data that this library requires to work"""

    global logger
    global ClearCase
    logger = Logger.getLogger('cleartool_lib')
    logger.debug("cleartool_lib: Initiating!")
    ClearCase = cleartool()
    ClearCase.initialize()
    return
    
def tearDown():
    """This function teminates all"""

    ClearCase.shutdown()
    logger.info("cleartool_lib: Bye bye !!")
    return

###############################################################################
#Lib methods
###############################################################################
def checkOut( file, comment = '.', reserved = True):
    logger.trace('entering checkOut')
    new_result = ClearCase.checkOut( file, comment, reserved)
    logger.trace('leaving checkOut')
    return (new_result)


def checkIn(file, comment = '.'):
    logger.trace('entering checkIn')
    new_result = ClearCase.checkIn(file, comment)
    logger.trace('leaving checkIn')
    return (new_result)

def mkelem(file, comment = '.'):
    logger.trace('entering mkelem')
    new_result = ClearCase.mkelem(file, comment)
    logger.trace('leaving mkelem')
    return (new_result)

def mkdir(directory, comment = '.'):
    logger.trace('entering mkdir')
    new_result = ClearCase.mkdir(directory, comment) 
    logger.trace('leaving mkdir')
    return (new_result)

def rmname(fileName, comment = '.'):
    logger.trace('entering rmname')
    new_result = ClearCase.rmname(fileName, comment)
    logger.trace('leaving mkdir')
    return (new_result)

def unCheckOut(file, saveCopy= 'no'):
    logger.trace('entering unCheckOut')
    new_result = ClearCase.unCheckOut(file, saveCopy)
    logger.trace('leaving unCheckOut')
    return (new_result)

def mkActivity( prefix ='GA', headline= 'ORBIT activity' ):
    logger.trace('entering mkActivity')
    result = ClearCase.mkActivity(prefix, headline)
    logger.trace('leaving mkActivity')
    return (result)

def rmActivity(activity= 'ORBIT activity' ):
    logger.trace('entering rmActivity')
    result = ClearCase.rmActivity(activity)
    logger.trace('leaving rmActivity')
    return (result)

def getActivity(activity = 'ORBIT activity' ):
    logger.trace('entering getActivity')
    result = ClearCase.getActivity(activity)
    logger.trace('leaving getActivity')
    return result

def setActivity(activity):
    logger.trace('entering setActivity')
    result = ClearCase.setActivity(activity)
    logger.trace('leaving setActivity')
    return (result)

def getCurrentActivity():
    logger.trace('entering getCurrentActivity')
    result = ClearCase.getCurrentActivity()
    logger.trace('leaving getCurrentActivity')
    return (result)

def getCurrentView():
    logger.trace('entering getCurrentView')
    result = ClearCase.getCurrentView()
    logger.trace('leaving getCurrentView')
    return result

def getCurrentStream():
    logger.trace('entering getCurrentStream')
    result = ClearCase.getCurrentStream()
    logger.trace('leaving getCurrentStream')
    return result

def getStreamData(stream):
    logger.trace('entering getStreamData')
    result =  ClearCase.getStreamData(stream)
    logger.trace('leaving getStreamData')
    return result

def getAllStreams(stream):
    logger.trace('entering getAllStreams')
    result = ClearCase.getAllStreams(stream)
    logger.trace('leaving getAllStreams')
    return result

def getAllOpenStreams(stream):
    logger.trace('entering getAllOpenStreams')
    result = ClearCase.getAllOpenStreams(stream)
    logger.trace('leaving getAllOpenStreams')
    return result

def isStreamObsolete(stream):
    logger.trace('entering isStreamObsolete')
    result = ClearCase.isStreamObsolete(stream)
    logger.trace('leaving isStreamObsolete')
    return result

def isStreamOpen(stream):
    logger.trace('entering isStreamopen')
    result = isStreamOpen(stream)
    logger.trace('leaving isStreamOpen')
    return result

def isCheckedOut(file):
    logger.trace('entering isCheckedOut')
    result = ClearCase.isCheckedOut(file)
    logger.trace('leaving isCheckedOut')
    return result
    
def isElement(file):
    return ClearCase.isElement(file)

def getActivityData(activity):
    logger.trace('entering getActivityData')
    result = ClearCase.getActivityData(activity)
    logger.trace('leaving getActivityData')
    return result

def getActivityChangeSet(activity):
    logger.trace('entering getActivityChangeSet')
    result = ClearCase.getActivityChangeSet(activity)
    logger.trace('leaving getActivityChangeSet')
    return result

def getStreamActivities(stream):
    logger.trace('entering getStreamActivities')
    result = ClearCase.getStreamData(stream)
    logger.trace('leaving getStreamActivities')
    return result

def getStreamRebaseActivities(stream):
    logger.trace('entering getStreamActivities')
    result = ClearCase.getStreamActivities(stream)
    logger.trace('leaving getStreamActivities')
    return result
    
def getStreamDeliverActivities(stream):
    logger.trace('entering getStreamDeliverActivities')
    result = ClearCase.getStreamActivities(stream)
    logger.trace('leaving getStreamDeliverActivities')
    return result
    
def getStreamChangeSet(stream, recursive = True):
    logger.trace('entering getStreamChangeSet')
    result = ClearCase.getStreamChangeSet(stream, recursive)
    logger.trace('leaving getStreamChangeSet')
    return result

def getCheckedOutFiles(stream, recursive = True):
    logger.trace('entering getCheckedOutFiles')
    result = ClearCase.getCheckedOutFiles(stream, recursive)
    logger.trace('leaving getCheckedOutFiles')
    return result

def getAllVobObjects(vobPath = '/vobs/tsp*saf/*'):
    logger.trace('entering getAllVobObjects')
    result = ClearCase.getAllVobObjects(vobPath)
    logger.trace('leaving getAllVobObjects')
    return result

def getBranchesWithZeroVersionOnly(fileName):
    logger.trace('entering getBranchesWithZeroVersionsOnly')
    result = ClearCase.getBranchesWithZeroVersionOnly(fileName)
    logger.trace('leaving getBranchesWithZeroVersionOnly')
    return result

def getBranchHistory1Day(branch = 'main', vobPath = '/vobs/tsp*saf/*'):
    logger.trace('entering getBranchHiostory1Day')
    result = ClearCase.getBranchHistory(branch = branch, since = 86400, vobPath = vobPath)
    logger.trace('leaving getBranchHistory1Day')
    return result

def getBranchHistory1Hour(branch = 'main', vobPath = '/vobs/tsp*saf/*'):
    logger.trace('entering getBranchHistory1Hour')
    result = ClearCase.getBranchHistory(branch = branch, since = 3600, vobPath = vobPath)
    logger.trace('leaving getBranchHistory1Day')
    return result

def getBranchHistory1Week(branch = 'main', vobPath = '/vobs/tsp*saf/*'):
    logger.trace('entering getBranchHistory1Week')
    result = ClearCase.getBranchHistory(branch = branch, since = 604800, vobPath = vobPath)
    logger.trace('leaving getBranchHistory1Week')
    return result

def getBranchHistory1Month(branch = 'main', vobPath = '/vobs/tsp*saf/*'):
    logger.trace('entering getBranchHistory1Month')
    result = ClearCase.getBranchHistory(branch = branch, since = 2592000, vobPath = vobPath)
    logger.trace('leaving getBranchHistory1Month')
    return result

def getBranchHistory(branch = 'main', since = 86400, vobPath = '/vobs/tsp*saf/*'):
    logger.trace('entering getBranchHistory')
    result = ClearCase.getBranchHistory(branch, since, vobPath)
    logger.trace('leaving getBranchHistory')
    return result

def getBranches(fileName):
    logger.trace('entering getBranches')
    result = getBranches(fileName)
    logger.trace('leaving getBranches')
    return result
                                
def catcs():
    logger.trace('entering catcs')
    result = ClearCase.catcs()
    logger.trace('leaving catcs')
    return result

def setcs(cs):
    logger.trace('entering setcs')
    result = ClearCase.setcs(cs)
    logger.trace('leaving setcs')
    return result

def refresh():
    logger.trace('entering refresh')
    result = ClearCase.refresh()
    logger.trace('leaving refresh')
    return result

def isLabelOnVersion(fileName, version, label):
    logger.trace('entering isLabelOnVersion')
    result = ClearCase.isLabelOnVersion(fileName, version, label)
    logger.trace('leaving isLabelOnVersion')
    return result

def getFileVersion(fileName):
    logger.trace('entering getFileVersion')
    result = getFileVersion(fileName)
    logger.trace('leaving getFileVersion')
    return result

###############################################################################
# cC implementation
###############################################################################

class cClearCase :

    # Construction
    def __init__(self, timeout = 5) :
        self.logger = Logger.getLogger('cClearCase')

    def executeCommand(self, command, arg = 'no' , timeout = 10)  :

        self.logger.trace('entering executeCommand')
        self.logger.debug("Executing Clearcase command: %s" % (command))
        p = popen2.Popen3(command, 1)
        p.tochild.close()
        std_out_from_command = p.fromchild.read()
        std_err_from_command = p.childerr.read()
        err = p.wait()
        p.fromchild.close()
        p.childerr.close()
        
        # diff command only returns 0 if no diffs found!!!!!
        if 'cleartool diff' in command:
            err = 0;
            
        if (err == 0):
            return ('SUCCESS', std_out_from_command)
        else:
            return ('ERROR', std_err_from_command)

    def Close(self) :
        try:
            self.logger.trace('entering Close')
            self.logger.trace('leaving Close')
            return ('SUCCESS', 'Clearcase handle closed!!')
        except :
            self.logger.trace('leaving Close')
            return ('ERROR', 'Error closing clearcase handle!!')

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    setUp()
