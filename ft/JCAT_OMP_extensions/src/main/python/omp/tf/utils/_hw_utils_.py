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
   %CCaseFile:  hw_lib.py %
   %CCaseRev:   /main/0 %
   %CCaseDate:  2007-08-10 %

   Author:
   EAB/FTI/SD Ulf Olofsson (ETXULFO)

   Description:
  
'''
import sys
import re
import time
import commands
import omp.target.target_data as target_data
import omp.tf.logger_lib as logger_lib
import omp.tf.ssh_lib as ssh_lib

def setUp():
    logger_lib.logMessage("_hw_utils: Initiating", logLevel='debug')
    return

def tearDown():
    logger_lib.logMessage("_hw_utils: Bye, bye!", logLevel='debug')
    return

class Hw(object):

    def powerOn(self, subrack, slot):
        '''
        power on node(IPMI).
        
        Arguments:
        (int subrack, int slot)
        
        Returns:
        tuple('SUCCESS','Power on blade_<subrack>_<slot> succeeded') or
        tuple('ERROR', 'Power on blade_<subrack>_<slot> failed')   
        NOTE:
        When running on SunBlades, there seems to be problems sometimes with ipmi commands,
        if they are executed too fast. We need a sleep(5) to let the HW settle.
        
        Dependencies:
        ssh_lib, target_data
        
        '''
        logger_lib.enter()
      
        gw_subrack = 9
        gw_slot = 9
        searchString = "Chassis Power Control: Up/On"
        checkString = "on"
        blade = 'blade_%s_%s' %  (subrack, slot)
        info = 'Power on %s' % blade
        #ipmiAddress = target_data.data['ipAddress']['ipmi'][blade]
        ipmiAddress = self.getIpmiAddress(slot, blade)

        ipmiPasswd = target_data.data['ipmiPwd']
        command = "ipmitool -I lanplus -U root -P %s -H %s chassis power on" % (ipmiPasswd, ipmiAddress)
        stopTryTime = int(time.time()) + 120
        if target_data.data['ipAddress']['ctrl']['testpc'] == 'localhost':
            result = ('SUCCESS', commands.getoutput(command))
        else:
            result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)
        time.sleep(5)
        check = self.powerStatus(subrack,slot)
        while((not re.search(searchString,result[1]) or \
              not re.search(checkString,check[1])) and \
                int(time.time()) < stopTryTime):
            if target_data.data['ipAddress']['ctrl']['testpc'] == 'localhost':
                result = ('SUCCESS', commands.getoutput(command))
            else:
                result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)
            time.sleep(5)
            check = self.powerStatus(subrack,slot)
        if (re.search(checkString,check[1])) and check[0] == 'SUCCESS':
            info =  '%s succeeded' % info
            logger_lib.logMessage(info, logLevel = 'debug')
            result = ('SUCCESS',info)
        else:
            info =  '%s failed' % info
            logger_lib.logMessage(info, logLevel = 'error')
            result = ('ERROR',info)
      
        logger_lib.leave()
        return result
    
    
    def powerOff(self, subrack, slot):
        '''
        power off node(IPMI).
        
        Arguments:
        (int subrack, int slot)
        
        Returns:
        tuple('SUCCESS','Power off blade_<subrack>_<slot> succeeded') or
        tuple('ERROR', 'Power off blade_<subrack>_<slot> failed')
            
        NOTE:
        When running on SunBlades, there seems to be problems sometimes with ipmi commands,
        if they are executed too fast. We need a sleep(5) to let the HW settle.

        Dependencies:
        ssh_lib, target_data
        
        '''
        logger_lib.enter()
        
        gw_subrack = 9
        gw_slot = 9
        searchString = 'Chassis Power Control: Down/Off'
        checkString = 'off'
        blade = 'blade_%s_%s' %  (subrack, slot)
        ssh_lib.tearDownBlade(blade) #tear down the blade before power reset via gw-pc
     
        info = 'Power off %s' % blade
        #ipmiAddress = target_data.data['ipAddress']['ipmi'][blade]
        ipmiAddress = self.getIpmiAddress(slot, blade)

        ipmiPasswd = target_data.data['ipmiPwd']
        command = "ipmitool -I lanplus -U root -P %s -H %s chassis power off" % (ipmiPasswd, ipmiAddress)
        stopTryTime = int(time.time()) + 120
        if target_data.data['ipAddress']['ctrl']['testpc'] == 'localhost':
            result = ('SUCCESS', commands.getoutput(command))
        else:
            result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)
        time.sleep(5)
        check = self.powerStatus(subrack,slot)
        while((not re.search(searchString,result[1]) or \
              not re.search(checkString,check[1])) and \
                int(time.time()) < stopTryTime):
            if target_data.data['ipAddress']['ctrl']['testpc'] == 'localhost':
                result = ('SUCCESS', commands.getoutput(command))
            else:
                result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)
            logger_lib.logMessage(result, logLevel = 'info')
            time.sleep(5)
            check = self.powerStatus(subrack,slot)
        if (re.search(checkString,check[1])) and check[0] == 'SUCCESS':
            info =  '%s succeeded' % info
            logger_lib.logMessage(info, logLevel = 'debug')
            result = ('SUCCESS',info)
        else:
            info =  '%s failed' % info
            logger_lib.logMessage(check, logLevel = 'error')
            result = ('ERROR',check[1])
      
        logger_lib.leave()
        return result
    
    
    def powerStatus(self, subrack, slot):
        '''
        Get power status for node(IPMI).
        
        Arguments:
        (int subrack, int slot)
        
        Returns:
        tuple('SUCCESS','Chassis Power is on|off') or 
        tuple('ERROR', 'Get power status for blade_<subrack>_<slot> failed')
            
        NOTE:
        
        Dependencies:
        ssh_lib, target_data
        
        '''
        logger_lib.enter()
        
        gw_subrack = 9
        gw_slot = 9
        blade = 'blade_%s_%s' %  (subrack, slot)
        errorInfo = 'Get power status for %s failed' % blade
        #ipmiAddress = target_data.data['ipAddress']['ipmi'][blade]
        ipmiAddress = self.getIpmiAddress(slot, blade)	

        ipmiPasswd = target_data.data['ipmiPwd']
        command = "ipmitool -I lanplus -U root -P %s -H %s chassis power status" % (ipmiPasswd, ipmiAddress)
        if target_data.data['ipAddress']['ctrl']['testpc'] == 'localhost':
            logger_lib.logMessage("Powerstatus command is %s" %(command), logLevel = 'info')
            result = ('SUCCESS', commands.getoutput(command))
        else:
            result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)

        stopTryTime = int(time.time()) + 120
        while(not re.search("Chassis Power is (on|off)", result[1]) and int(time.time()) < stopTryTime):
            time.sleep(5)
            if target_data.data['ipAddress']['ctrl']['testpc'] == 'localhost':
                result = ('SUCCESS', commands.getoutput(command))
            else:
                result = ssh_lib.sendCommand(command,gw_subrack,gw_slot) 
            
        if result[0] == 'SUCCESS':
            logger_lib.logMessage('%s on %s' % (result[1], blade), logLevel = 'info')
        elif result[0] == 'ERROR': 
            logger_lib.logMessage(errorInfo, logLevel = 'error')
            result = ('ERROR',errorInfo)
        else:
            logger_lib.logMessage(errorInfo, logLevel = 'error')
            result = ('ERROR',errorInfo)
        ### New
        
        logger_lib.leave()
        return result      

    def powerReset(self, subrack, slot, ControlType='OffOn'):
        #
        # ControlType should either be 'OffOn' or 'Reset'
        # Note! 'Reset' should normally work with IPMI, this 'OffOn' is a temporary soultion to secure a RESET.
        #       When all works well, change default value to 'Reset' for ControlType
        #       When running on SunBlades, there seems to be problems sometimes with ipmi commands,
        #       if they are executed too fast. We need a sleep(5) to let the HW settle.

        logger_lib.enter()
        
        gw_subrack = 9
        gw_slot = 9
        blade = 'blade_%s_%s' %  (subrack, slot)
        ssh_lib.tearDownBlade(blade) #tear down the blade before power reset via gw-pc
        #ipmiAddress = target_data.data['ipAddress']['ipmi'][blade]
        ipmiAddress = self.getIpmiAddress(slot, blade)

        ipmiPasswd = target_data.data['ipmiPwd']
        command = "ipmitool -I lanplus -U root -P %s -H %s chassis power reset" % (ipmiPasswd, ipmiAddress)
        stopTryTime = int(time.time()) + 120
        if (ControlType == 'Reset'):
            if target_data.data['ipAddress']['ctrl']['testpc'] == 'localhost':
                result = ('SUCCESS', commands.getoutput(command))
            else:
                result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)
            time.sleep(5)
        elif (ControlType == 'OffOn'):
            result = self.powerOff(subrack, slot)
            result = self.powerOn(subrack, slot)
        else:
            logger_lib.logMessage("IPMI Power command %s unknown..."\
                                  % (ControlType),logLevel='error')
            ssh_lib.tearDownBlade(blade) #tear down the blade after power reset via gw-pc
            logger_lib.leave()
            return ('ERROR','IPMI Power command %s unknown...' % (ControlType))
        while(result[0] != 'SUCCESS' and int(time.time()) < stopTryTime):
            if (ControlType == 'Reset'):
                result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)
                time.sleep(5)
            else:
                while(not re.search('Reset',result[1]) and int(time.time()) < stopTryTime):
                    result = self.powerOff(subrack, slot)
                    result = self.powerOn(subrack, slot)
        check = self.powerStatus(subrack,slot)
        while((not re.search('Reset',result[1]) or \
              not re.search('on',check[1])) and \
              int(time.time()) < stopTryTime ):
            result = ssh_lib.sendCommand(command,gw_subrack,gw_slot)
            time.sleep(5)
            check = self.powerStatus(subrack,slot)
        if (re.search('on',check[1])) and result[0] == 'SUCCESS':
            logger_lib.logMessage("IPMI Power %s command to blade_%s_%s succeeded"\
                                  % (ControlType,subrack,slot))
            ssh_lib.tearDownBlade(blade) #tear down the blade after power reset via gw-pc
            logger_lib.leave()
            return ( 'SUCCESS', check[1] )
        else:
            logger_lib.logMessage("IPMI Power %s command to blade_%s_%s failed"\
                                  % (ControlType,subrack,slot), logLevel = 'error')
            ssh_lib.tearDownBlade(blade) #tear down the blade after power reset via gw-pc
            logger_lib.leave()
            return ('ERROR', check[1])       

    def clusterPowerReset(self):
        '''
        Reset the cluster, power off/on on all valid blades(IPMI).
        
        Arguments:
        None
        
        Returns:
        tuple('SUCCESS','cluster power reset succeeded') or 
        tuple('ERROR', 'cluster power reset failed')
            
        NOTE:
        if blade already is in power off state, it's never powered on.
        dynamic generated target data solves this problem 
        
        Dependencies:
        target_data
        powerOff/On/Status
        
        '''
        logger_lib.enter()
        
        blades = target_data.data['ipAddress']['ipmi'].keys()
        powerOnNodes = []
        errorInfo = []
        errorFlag = False
        result = ('SUCCESS','cluster power reset succeeded')
        
        for blade in blades:
            subrack, slot = int(blade.split('_')[1]), int(blade.split('_')[2])
            if self.powerStatus(subrack, slot) == ('SUCCESS','Chassis Power is on'):
                powerOnNodes.append((subrack, slot))
                tempResult = self.powerOff(subrack, slot)
                if tempResult != ('SUCCESS','Power off %s succeeded' % blade):
                    errorInfo.append(tempResult[1])
                    errorFlag = True
                    
        for node in powerOnNodes:
            subrack, slot = node[0], node[1]
            tempResult = self.powerOn(subrack, slot)
            if tempResult != ('SUCCESS','Power on blade_%s_%s succeeded' % (subrack, slot)):
                errorInfo.append(tempResult[1])
                errorFlag = True
                
        if errorFlag == True:
            result = ('ERROR','cluster power reset failed')
            logger_lib.logMessage(errorInfo, logLevel = 'error')
        else: 
            logger_lib.logMessage('cluster power reset succeeded', logLevel = 'debug')
            
        logger_lib.leave()
 
        return result          
    
    def getIpmiAddress(self,slot,blade):
        try:
            ipmiBaseSplitted = target_data.data['ipAddress']['ctrl']['ipmi_base'].split('.')
            ipmiAddrTemp = str(int(ipmiBaseSplitted[3]) + int(slot))
            ipmiAddress = ipmiBaseSplitted[0]+'.'+ipmiBaseSplitted[1]+'.'+ipmiBaseSplitted[2]+'.'+ipmiAddrTemp
            return ipmiAddress
        except:
            ipmiAddress = target_data.data['ipAddress']['ipmi'][blade]
            return ipmiAddress
     	    

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
    
