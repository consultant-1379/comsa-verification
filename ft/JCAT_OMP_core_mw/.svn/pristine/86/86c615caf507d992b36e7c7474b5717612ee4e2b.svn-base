#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2007 All rights reserved.
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
   %CCaseFile:  opensaf_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2007-08-10 %

   Author:


   Description:

'''
from org.apache.log4j import Logger
from org.apache.log4j import Level
from java.lang import System
import omp.tf.ssh_lib as ssh_lib
import omp.tf.misc_lib as misc_lib
import re
import copy

#############GLOBALS##################
logger = None
######################################

class Ntf(object):

    def setUp(self):

        global logger

        logLevel = System.getProperty("jcat.logging")
        logger = Logger.getLogger('_ntf_utils logging')
        logger.setLevel(Level.toLevel(logLevel))
        logger.info("_ntf_utils: Initiating")

        return


    def tearDown(self):

        logger.info("_ntf_utils: Bye, bye!")

        return


    def _readNotifications(self, nrOfSC):
        '''
        read notifications from NTF.

        Arguments:
        (none)

        Returns:
        tuple('SUCCESS',dict notifications) or
        tuple('ERROR', 'Failed to fetch notifications from the system')
        NOTE:

        Dependencies:
        ssh_lib

        '''
        logger.debug('enter _readNotifications')

        notifications = {}
        result = ('ERROR','Failed to fetch notifications from the system')

        ntfSubscibeAppDir = '/home/test/'
        result = ssh_lib.sendCommand('ls /home/test/ntfSubscribeApp')
        if None == re.search('No such file or directory',result[1]):
            ntfSubscibeAppDir = '/home/test/ntfSubscribeApp'
       
        result1, notificationList1 = ssh_lib.sendCommand('cat %s/notif.log-SC*-1' % ntfSubscibeAppDir) #read notif from first controller
        result2, notificationList2 = ('SUCCESS',"")
        if nrOfSC == 2:
            result2, notificationList2 = ssh_lib.sendCommand('cat %s/notif.log-SC*-2' % ntfSubscibeAppDir)#read notif from second controller

        if result1 == 'SUCCESS' and result2 == 'SUCCESS':
            notificationList1 = notificationList1.replace('\n===','\n<>===')
            notificationList1 = notificationList1.split('<>')
            if nrOfSC == 2:
                notificationList2 = notificationList2.replace('\n===','\n<>===')
                notificationList1.extend(notificationList2.split('<>'))
            notificationList = set(notificationList1) #remove duplicates
            notif = list(notificationList)

            eventTime = []
            for i in notif:
                j = i.split('\n')
                for n in j:
                    if re.search('eventTime',n):
                        eventTime.append(n)
            eventTime.sort()
            notifList = []

            for t in  eventTime:
                for n in notif:
                    if t in n:
                        notifList.append(n)

            #create a dict, where the key values are notification types
            notifications = {'alarmNotifications' : [], 'objectCreateDeleteNotifications' : [],
                             'attributeChangeNotifications' : [], 'stateChangeNotifications' : [],
                             'securityAlarmNotifications' : [],
                             'unknownType' : []
                            }

            #fill the dict with notifications
            for notif in notifList:
                if re.search('alarm notification',notif):
                    notifications['alarmNotifications'].append(notif)
                elif re.search('object create delete notification',notif):
                    notifications['objectCreateDeleteNotifications'].append(notif)
                elif re.search('attribute change notification',notif):
                    notifications['attributeChangeNotifications'].append(notif)
                elif re.search('state change notification',notif):
                    notifications['stateChangeNotifications'].append(notif)
                elif re.search('security alarm notification',notif):
                    notifications['securityAlarmNotifications'].append(notif)
                else:
                    notifications['unknownType'].append(notif)
            logger.debug('Fetch notifications from the system succeeded')
            result = ('SUCCESS',notifications)
        else:
            logger.error('Fetch notifications from the system failed')


        logger.debug('leave _readNotifications')

        #result =  notifications
        return result

    def _notificationReceived(self, bodyPattern = '', notifType = 'stateChangeNotifications', nrOfSC = 2):
        '''
        check if a specific notification is received

        Arguments:
        bodyPattern: a list of patterns

        Returns:
        tuple('SUCCESS', [list of notifications in which the pattern was found])
        tupple('ERROR', '<Error message>')
        '''
        logger.debug('enter  _notificationReceived')
        result = self._readNotifications(nrOfSC)
        if result[0] != 'SUCCESS':
            logger.debug('leave  _notificationReceived')
            return ('ERROR', result[1])
        matchedNotifications = []
        for notification in result[1][notifType]:
            if re.search(bodyPattern, notification):
                matchedNotifications.append(notification)

        logger.debug('leave  _notificationReceived')
        if len(matchedNotifications) == 0:
            logger.debug('leave  _notificationReceived')
            return ('ERROR', 'No notification found containing the searched pattern.')
        else:
            logger.debug('leave  _notificationReceived')
            return ('SUCCESS', matchedNotifications)



    def _clearNotifications(self, nrOfSC = 2):
        '''
        clear all notifications.

        Arguments:
        (none)

        Returns:
        tuple('SUCCESS','clear all notifications succeeded') or
        tuple('ERROR', 'clear all notifications failed')
        NOTE:

        Dependencies:
        ssh_lib

        '''
        logger.debug('enter _clearNotifications')

        okFlags = [False,False]

        cmdPath = '/opt/NTFSUBSCRIBE/bin/rotate_log.sh'

        ntfSubscibeAppDir = '/home/test/'
        result = ssh_lib.sendCommand('ls /home/test/ntfSubscribeApp')
        if None == re.search('No such file or directory',result[1]):
            ntfSubscibeAppDir = '/home/test/ntfSubscribeApp'

        timeStamp1="ls --full-time %s/notif.log-SC*-1 |awk '{print $7}'" % ntfSubscibeAppDir
        fileSize1="ls --full-time %s/notif.log-SC*-1 |awk '{print $5}'" % ntfSubscibeAppDir
        if nrOfSC == 2:
            timeStamp2="ls --full-time %s/notif.log-SC*-2 |awk '{print $7}'" % ntfSubscibeAppDir
            fileSize2="ls --full-time %s/notif.log-SC*-2 |awk '{print $5}'" % ntfSubscibeAppDir

        timeStamp_bfr1=ssh_lib.sendCommand(timeStamp1,2,1)
        if timeStamp_bfr1[0] != 'SUCCESS':
            logger.error('clear all notifications failed')
            return ('ERROR', timeStamp_bfr1[1])
        timeStamp_bfr1 = timeStamp_bfr1[1].strip()

        fileSize_bfr1=ssh_lib.sendCommand(fileSize1,2,1)
        if fileSize_bfr1[0] != 'SUCCESS':
            logger.error('clear all notifications failed')
            return ('ERROR', fileSize_bfr1[1])
        fileSize_bfr1 = fileSize_bfr1[1].strip()

        for i in range(5):
            result = ssh_lib.sendCommand(cmdPath,2,1)
            misc_lib.waitTime(1)
            if result[0]== 'SUCCESS':
                timeStamp_aft1=ssh_lib.sendCommand(timeStamp1,2,1)
                if timeStamp_aft1[0] != 'SUCCESS':
                    continue
                timeStamp_aft1 = timeStamp_aft1[1].strip()
                fileSize_aft1=ssh_lib.sendCommand(fileSize1,2,1)
                if fileSize_aft1[0] != 'SUCCESS':
                    continue
                try:
                    fileSize_aft1 = int(fileSize_aft1[1])
                except ValueError:
                    # The value isn't an integer.
                    continue
                if fileSize_aft1 == 0 and timeStamp_aft1 != timeStamp_bfr1:
                    logger.debug('clear notifications on controller 1 succeeded')
                    okFlags[0] = True
                    if nrOfSC == 1:
                        okFlags[1] = True
                    break

        if nrOfSC == 2:
            timeStamp_bfr2=ssh_lib.sendCommand(timeStamp2,2,1)
            if timeStamp_bfr2[0] != 'SUCCESS':
                logger.error('clear all notifications failed')
                return ('ERROR', timeStamp_bfr2[1])
            timeStamp_bfr2 = timeStamp_bfr2[1].strip()
    
            fileSize_bfr2=ssh_lib.sendCommand(fileSize2,2,1)
            if fileSize_bfr2[0] != 'SUCCESS':
                logger.error('clear all notifications failed')
                return ('ERROR', fileSize_bfr2[1])
            fileSize_bfr2 = fileSize_bfr2[1].strip()
    
            for i in range(5):
                result = ssh_lib.sendCommand(cmdPath,2,2)
                misc_lib.waitTime(1)
                if result[0]== 'SUCCESS':
                    timeStamp_aft2=ssh_lib.sendCommand(timeStamp2,2,2)
                    if timeStamp_aft2[0] != 'SUCCESS':
                        continue
                    timeStamp_aft2 = timeStamp_aft2[1].strip()
                    fileSize_aft2=ssh_lib.sendCommand(fileSize2,2,2)
                    if fileSize_aft2[0] != 'SUCCESS':
                        continue
                    try:
                        fileSize_aft2 = int(fileSize_aft2[1])
                    except ValueError:
                        # The value isn't an integer.
                        continue
                    if fileSize_aft2 == 0 and timeStamp_aft2 != timeStamp_bfr2:
                        logger.debug('clear notifications on controller 2 succeeded')
                        okFlags[1] = True
                        break

        if okFlags == [True,True]:
            logger.debug('clear all notifications succeeded')
            result = ('SUCCESS','clear all notifications succeeded')
        else:
            logger.error('clear all notifications failed')
            result = ('ERROR', 'clear all notifications failed')

        logger.debug('leave _clearNotifications')

        return result


    def _checkNotifications(self, expectedPatternList = [], ignoredPatternList = [], notifType = 'alarmNotifications', nrOfSC = 2):
        '''
        clear all notifications.

        Arguments:
        (none)

        Returns:
        tuple('SUCCESS','no unexpected notifications found') or
        tuple('ERROR', 'unexpected notifications found')
        NOTE:

        Dependencies:
        ssh_lib

        '''

        logger.debug('enter _checkNotifications')
        result = self._readNotifications(nrOfSC)
        unexpectedNotifs =  copy.deepcopy(result[1][notifType])
        allNotifications = copy.deepcopy(result[1][notifType])
        expectedNotifs= copy.deepcopy(expectedPatternList)

        nrOfElements = len(unexpectedNotifs)
        nrOfExpNotifs = len(expectedNotifs)
        for i, notifs in  enumerate(result[1][notifType]):
            for expectNotif in expectedPatternList:
                if re.search(expectNotif[1],notifs) and re.search(expectNotif[0],notifs):
                    #logger.info('Expected notification %s found'%(notifs))
                    unexpectedNotifs[i] = ''

            for ignoredNotif in ignoredPatternList:
                if re.search(ignoredNotif[1],notifs) and re.search(ignoredNotif[0],notifs):
                    #logger.warn('notification %s ignored'%(notifs))
                    unexpectedNotifs[i] = ''

        for j, expectedNotif in enumerate(expectedNotifs):
            for notification in allNotifications:
                if re.search(expectedNotif[1], notification) and re.search(expectedNotif[0], notification):
                    logger.info('Expected notification %s found'%(expectedNotif))
                    expectedNotifs[j] = ''

        nrOfEmptyElements = unexpectedNotifs.count('')
        nrOfEmptyExpNotifs = expectedNotifs.count('')

        okFlag = True
        returnNotifs = []

        if nrOfElements != nrOfEmptyElements:
            okFlag = False
            logger.error('unexpected notifications found')
            falseFlag = True
            for i in unexpectedNotifs:
                if i != '':
                    logger.error(i)
                    returnNotifs.append(str(i))
            result = ('ERROR', returnNotifs)
            logger.info(str(returnNotifs))
        if nrOfEmptyExpNotifs != nrOfExpNotifs:
            okFlag = False
            logger.error('expected notifications not found')
            for i in expectedNotifs:
                if i != '':
                    logger.error(i)
                    returnNotifs.append(str(i))
            result = ('ERROR', returnNotifs)
            logger.info(str(returnNotifs))
        if okFlag == True:
            logger.debug('no unexpected notifications found')
            result = ('SUCCESS', 'no unexpected notifications found')

        logger.debug('leave _checkNotifications')

        return result
##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':


    import target_data as target_data
    import booking_lib as booking_lib
    node=booking_lib.checkBooking()
    targetData=target_data.setTargetHwData(node)
    st_env_lib.executeFunction(sys.argv)

    st_env_lib.setUp()
    ###########TEST AREA START###############

    h=Hw()
    print h.powerStatus(2,3)


    ###########TEST AREA END###############
    st_env_lib.tearDown()
