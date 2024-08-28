#!/vobs/tsp_saf/tools/Python/linux/bin/python
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

import string
import os
import sys
import time
import re
import getopt
import pexpect

########NODE CONFIGURATION DATA##########
import common.target.target_data as target_data
global targetData
targetData=target_data.data

#########COMMON USED RESOURCES##########
import logger_lib as logger_lib

###############################################################################
# cSCP implementation
###############################################################################
class cSCP (pexpect.spawn, pexpect.ExceptionPexpect) :

    # Construction
    def __init__(self, timeout) :
        self.timeout = timeout

    def copyFileRemoteFrom(self, strIpAddr, strUsr, strPwd, file, destination)  :
        logger_lib.enter()
        
        cmd = "scp "+strUsr+"@" + strIpAddr+":"+file+" "+destination
        pattern = (["""(No route to host)""", """(yes/no)""",  """(Password:)""", pexpect.EOF, pexpect.TIMEOUT])
        logger_lib.logMessage("Copying file from %s." % strIpAddr)
        try : 
            pexpect.spawn.__init__(self, cmd,[], self.timeout)
            idx = self.expect(pattern, self.timeout)
            logger_lib.logMessage("Command: %s, Trigger pattern: %s " %  (cmd, pattern[idx]), logLevel = 'debug')

            if (idx == 1): 
                cmd='yes'
                self.sendline(cmd)
                idx = self.expect(pattern, self.timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]), logLevel = 'debug')
            if (idx == 2):
                cmd = strPwd
                self.sendline(cmd)
                idx=self.expect(pattern, self.timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]), logLevel = 'debug')
            if (idx == 0 or idx == 4):
                logger_lib.logMessage("Recieved unexpected pattern: %s " % (pattern[idx]) , logLevel = 'error')
                logger_lib.leave()
                return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")
            if (idx == 3) :
                logger_lib.logMessage("Filed assumed copied getting match for pattern %s " % (pattern[idx]))
                logger_lib.leave()
                return ('SUCCESS','File success fully copied from '+strIpAddr) 
        except :
            logger_lib.logMessage('Can\'t connect to %s !!' % strIpAddr, logLevel = 'error')
            logger_lib.leave()
            return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")

    def copyFileRemoteTo(self, strIpAddr, strUsr, strPwd, file, destination)  :
        logger_lib.enter()

        cmd = "scp "+file+" "+strUsr+"@" + strIpAddr+":"+destination
        pattern = (["""(No route to host)""", """(yes/no)""",  """(Password:)""", pexpect.EOF, pexpect.TIMEOUT])
        logger_lib.logMessage("Copying file to %s." % strIpAddr)
        try : 
            pexpect.spawn.__init__(self, cmd,[], self.timeout)
            idx = self.expect(pattern, self.timeout)
            logger_lib.logMessage("Command: %s, Trigger pattern: %s " %  (cmd, pattern[idx]), logLevel = 'debug')
            if (idx == 1): 
                cmd='yes'
                self.sendline(cmd)
                idx = self.expect(pattern, self.timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]), logLevel = 'debug')
            if (idx == 2):
                cmd = strPwd
                self.sendline(cmd)
                idx=self.expect(pattern, self.timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]), logLevel = 'debug')
            if (idx == 0 or idx == 4):
                logger_lib.logMessage("Recieved unexpected pattern: %s " % (pattern[idx]) , logLevel = 'error')
                logger_lib.leave()
                return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")
            if (idx == 3) :
                logger_lib.logMessage("Filed assumed copied getting match for pattern %s " % (pattern[idx]))
                logger_lib.leave()
                return ('SUCCESS','File success fully copied to '+strIpAddr) 
        except :
            logger_lib.logMessage('Can\'t connect to '+ strIpAddr+ "!!")
            logger_lib.leave()
            return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")
        
###############################################################################
# cSSH implementation
###############################################################################

class cSSH (pexpect.spawn, pexpect.ExceptionPexpect) :

    # Construction
    def __init__(self, timeOut = 30) :
        self.timeOut = timeOut

    def openSystemController(self, strIpAddr, strUsr, strPwd, attempts=1, timeout = 10)  :

        logger_lib.enter()

        cmd = "ssh -o UserKnownHostsFile=dev/null -o StrictHostKeyChecking=no "+strUsr+"@" + strIpAddr 
        pattern = (["""(Password:)""","""(yes/no)""","""(sis\d:.*)""","""(saf\d\dlinux\d.\~)""","""(SC_2_\d#)""", """(gwhost\d+:~ #)""", """(safTg\d+:~ #)""", pexpect.EOF, pexpect.TIMEOUT])
        logger_lib.logMessage("Logging in to: %s" % (strIpAddr), logLevel = 'debug')

        try : 
            pexpect.spawn.__init__(self, cmd,[], timeout)
            idx = self.expect(pattern, timeout)
            logger_lib.logMessage("Command: %s, Trigger pattern: %s " %  (cmd, pattern[idx]), logLevel = 'debug')
            if (idx == 1): 
                cmd='yes'
                self.sendline(cmd)
                idx = self.expect(pattern, timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]), logLevel = 'debug')
            if (idx == 0):
                for i in range(attempts):
                    cmd = strPwd
                    self.sendline(cmd)
                    idx=self.expect(pattern, timeout)
                    logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]), logLevel = 'debug')
                    if (idx == 0):
                        continue
                    else:
                        break
            if (idx == 0 or idx == 1 or idx > 6):
                logger_lib.logMessage("Recieved unexpected pattern: %s " % (pattern[idx]), logLevel='error')
                logger_lib.leave()
                return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")
            logger_lib.logMessage("Assumed logged in getting match for pattern %s " % (pattern[idx]), logLevel = 'debug')
            logger_lib.leave()
            return ('SUCCESS','SystemController @'+strIpAddr+ ' connected!!') 
        except :
            logger_lib.logMessage('Can\'t connect to '+ strIpAddr+ "!!", logLevel='error')
            logger_lib.leave()
            return ('ERROR', 'Can\'t connect to '+ strIpAddr+ "!!")


    def connectToBlade(self, strIpAddr, timeout=5):

        logger_lib.enter()

        command = 'ssh %s' % strIpAddr
        logger_lib.logMessage("Logging in to: %s" % (strIpAddr), logLevel = 'debug')

        pattern = (["""(No route to host)""", """(Password:)""","""(password:)""","""(blade_\d_\d:.)""", """(blade_\d_\d.\~)""", """(root@xxb:.*)""",\
        """(yes/no)""","""(PL_2_\d+#)""", """(SC_2_\d#)""", pexpect.EOF, pexpect.TIMEOUT])

        try : 
            self.sendline(command)
            idx = self.expect(pattern, timeout)
            logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (command, pattern[idx]), logLevel = 'debug')
            if (idx == 6):
                command = 'yes'
                self.sendline(command)
                idx = self.expect(pattern, timeout) 
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (command, pattern[idx]), logLevel = 'debug')
            if (idx == 1 or idx == 2):
                command=targetData['pwd']
                self.sendline(command)     
                idx=self.expect(pattern, timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (command, pattern[idx]), logLevel = 'debug')
            if (idx==0 or idx > 8):
                logger_lib.logMessage("Recieved unexpected pattern :%s " % (pattern[idx]), logLevel ='error')
                logger_lib.leave()
                return ('ERROR', 'Can\'t connect to blade @ '+ strIpAddr+ "!!")
            logger_lib.logMessage("Assumed logged in getting match for pattern:%s " % (pattern[idx]), logLevel = 'debug')
            logger_lib.leave()
            return ('SUCCESS','Blade @'+strIpAddr+ ' connected!!') 
        except :
            logger_lib.logMessage("Can't connect to "+ strIpAddr+ "!!", logLevel ='error')
            logger_lib.leave()
            return ('ERROR', "Can't connect to "+ strIpAddr+ "!!")

    def disconnectFromBlade(self)  :

        logger_lib.enter()
        
        pattern = targetData['ctrlBladePattern']

        logger_lib.logMessage("Disconnecting from blade.")

        try :   
            self.sendline('exit') 
            self.expect(pattern)  
            logger_lib.leave()
            return ('SUCCESS','Blade disconnected!!') 
        except :
            logger_lib.leave()
            return ('ERROR', "Can't disconnect from blade!!")

    def createTunnel(self, externalAddress, internalAddress, localPort, destinationPort,  timeout = 20):
        ''' Create tunnels (bind adresses) to an internal node.'''

        logger_lib.enter()

        pattern = (["""(No route to host)""","""(Password:)""","""(yes/no)""",\
                    targetData['ctrlBladePattern'], targetData['payloadBladePattern'],\
                    targetData['testPcPattern'], pexpect.EOF, pexpect.TIMEOUT])
        cmd = 'ssh root@%s -L %d:%s:%d' % (externalAddress, localPort, internalAddress, destinationPort)

        try : 
            pexpect.spawn.__init__(self, cmd,[], timeout)
            idx= self.expect(pattern) # Password promt

            logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]))
            if (idx == 2):
                command = 'yes'
                self.sendline(command)
                idx = self.expect(pattern, timeout) 
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (command, pattern[idx]), logLevel = 'debug')
            if (idx == 1):
                command=targetData['pwd']
                self.sendline(command)     
                idx=self.expect(pattern, timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (command, pattern[idx]), logLevel = 'debug')
            if (idx==0 or idx > 5):
                logger_lib.logMessage("Recieved unexpected pattern :%s " % (pattern[idx]), logLevel = 'error')
                logger_lib.leave()
                return ('ERROR', 'Can\'t connect to localhost!!')
            self.sendline( 'cat -' )
            logger_lib.logMessage("Connect to localhost:%s for ssh to target" % localPort)
            logger_lib.leave()
            return ['SUCCESS', "SSH tunnel set up!!"]
        except:
            logger_lib.logMessage("Could not setup tunnel connection.", logLevel = 'error')
            logger_lib.leave()
            return ['ERROR', 'Could not setup tunnel connection']

    def useTunnel(self,localPort, request,  timeout = 20):
        ''' Create tunnels (bind adresses) to an internal node.''' 

        logger_lib.enter()
        pattern = (["""(No route to host)""","""(Password:)""","""(yes/no)""", targetData['ctrlBladePattern'], targetData['payloadBladePattern'],\
        targetData['testPcPattern'], pexpect.EOF, pexpect.TIMEOUT, """(Host key verification failed)"""])
        cmd = 'ssh -l root -p %d localhost' % localPort

        try : 
            pexpect.spawn.__init__(self, cmd,[], timeout)   
            idx = self.expect(pattern, timeout)
            logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (cmd, pattern[idx]))
            if (idx == 2):
                command = 'yes'
                self.sendline(command)
                idx = self.expect(pattern, timeout) 
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (command, pattern[idx]), logLevel = 'debug')
            if (idx == 1):
                command=targetData['pwd']
                self.sendline(command)     
                idx=self.expect(pattern, timeout)
                logger_lib.logMessage("Command: %s, Trigger pattern:%s " % (command, pattern[idx]), logLevel = 'debug')
            if (idx==0 or idx > 5):
                logger_lib.logMessage("Recieved unexpected pattern :%s " % (pattern[idx]), logLevel = 'error')
                logger_lib.leave()
                return ('ERROR', 'Can\'t connect to localhost!!')
            self.sendline( request )
            retval = self.expect(pattern)
            response=self.before
            logger_lib.leave()
            return ['SUCCESS', response] 
        except:
            logger_lib.logMessage("Could not send request", logLevel = 'error')
            logger_lib.leave()
            return ['ERROR', 'Could not send request']

    def senceive(self, strCmd) :

        logger_lib.enter()

        if (len(strCmd) == 72):
            strCmd = strCmd + ' '

        pattern = ( [targetData['ctrlBladePattern'], targetData['payloadBladePattern'], targetData['testPcPattern'], targetData['vipTgPattern']])
        try:
            self.sendline(strCmd)
            idx=self.expect(pattern, self.timeOut)
            logger_lib.logMessage("Command: %s, Trigger pattern: %s " %  (strCmd, pattern[idx]), logLevel = 'debug') 
            ret = self.before
            ret = ret.strip()
            #eolnans: Added for Jython
            #Does the command and prompt stripping in the Class
            ret2 = ret.split(strCmd,1) #remove command from response
            ret2 = ret2.pop()
            ret2 = ret2.split('\r\n', 1)
            ret2 = ret2.pop()
            logger_lib.leave()
            return ['SUCCESS', ret2] 
        except Exception, error:
            logger_lib.logMessage("Error sending command: %s Error: %s " %  (strCmd, str(error)), logLevel='error') 
            logger_lib.leave()
            return ['ERROR', str(error)]

    def receive(self) :

        logger_lib.enter()
        try : 
            self.readline()
            self.expect('\r\n')       
            ret = self.before
            logger_lib.leave()
            return ('SUCCESS', ret) 
        except :
            logger_lib.leave()
            return ('ERROR', 'Error receiving data!!')

    def Send (self, strCmd ):

        logger_lib.enter()
        try:
            bytes=self.send(strCmd+ '\n\r')
            logger_lib.leave()
            return ['SUCCESS', bytes] 
        except :
            return ['ERROR', 'Error sending data!!']

    def interact(self) :

        logger_lib.enter()
        try : 
            self.interact()  
        except :
            logger_lib.leave()
            return ('ERROR', 'Error releasing control!!')

    def Close(self) :
        logger_lib.enter()
        try : 
            self.close()
            logger_lib.logMessage('ssh connection succesfully terminated', logLevel = 'debug')
            logger_lib.leave()
            return ('SUCCESS', ' ssh handle closed!!')
        except :
            return ('ERROR', 'Error closing ssh handle!!')

    def setTimeOut (self, timeOut):
        logger_lib.enter()
        try:
            timeOut=int(timeOut)
            logger_lib.logMessage("Timeout changed from: %d  to: %d" % (self.timeOut, timeOut), logLevel = 'debug')
            self.timeOut = timeOut
            logger_lib.leave()
            return ('SUCCESS', 'Timeout changed')
        except :
            logger_lib.leave()
            return ('ERROR', 'New timeout could not be set')   

    def getTimeOut (self):
        logger_lib.enter()
        try:
            logger_lib.logMessage("Returning timeout: %d" % (self.timeOut), logLevel = 'debug')
            logger_lib.leave()
            return ('SUCCESS', int(self.timeOut))
        except :
            logger_lib.leave()
            return ('ERROR', 'Could not return timeout')   