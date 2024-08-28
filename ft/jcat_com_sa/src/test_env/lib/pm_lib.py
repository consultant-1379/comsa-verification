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


   Author: eanjoel

   Description:

'''
#############IMPORT##################

from org.apache.log4j import Logger
from java.lang import System
import sys
import os
import string
import lib
import shutil
import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException
import re
import math

import omp.tf.ssh_lib as ssh_lib
import omp.tf.hw_lib as hw_lib
import omp.tf.ethswitch_lib as ethswitch_lib
import omp.tf.misc_lib as misc_lib
import coremw.notification_lib as notification_lib
import coremw.testapp_lib as testapp_lib
import coremw.saf_lib as saf_lib

def setUp(logLevel, currentSut):
    global ethswitch_lib
    global hw_lib
    global ssh_lib
    global misc_lib
    global testapp_lib
    global logger
    global targetData
    global logDir

    #global amfNodeNameSeparator

    logger = Logger.getLogger('pm_lib')
    logger.setLevel(logLevel)
    logger.info("pm_lib: Initiating!")
    logDir = System.getProperty("logdir")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    campaignDir='/tmp/%s-%d' % (os.environ['USER'], os.getpid())
    if os.path.isdir(campaignDir):    
        shutil.rmtree(campaignDir)    
    os.mkdir(campaignDir)
    return


def tearDown():
    logger.debug("pm_lib: bye, bye!")
    return

#############################################################################################
# pm_lib functions
#############################################################################################

def startPm(numOfNodes):
#################################
    defaultTimeout = ssh_lib.getTimeout()
    ssh_lib.setTimeout(60)

    workspace = os.environ['MY_REPOSITORY']
    configDir = workspace + "/test_env/lib/config/"
    configFiles = ["RO.xml", "RW.xml", "config.txt"]
    destDir = "/home/test/pm/"
    
    # TODO: update install campaign for PmProducerApp instead
    ssh_lib.sendCommand("mkdir -p /cluster/isMeasured")
    ssh_lib.sendCommand("for i in `immfind -c SaAmfHealthcheck | grep PmsvProducerTestapp`; do immcfg -a saAmfHealthcheckPeriod=100000000000 $i; immcfg -a saAmfHealthcheckMaxDuration=100000000000 $i; done")

    for file in configFiles:
        ssh_lib.remoteCopy(configDir + file, destDir, 60)
    
    ssh_lib.sendCommand("immcfg -f %sRO.xml" % destDir)
    ssh_lib.sendCommand("immcfg -f %sRW.xml" % destDir)
    
    """
    ssh_lib.sendCommand("for cmd in lock lock-in ; do for su in SC-1 SC-2 ; do amf-adm $cmd safSu=$su,safSg=NWayActive,safApp=pmProducerApp;done;done")
    if (numOfNodes > 2):
        ssh_lib.sendCommand("for cmd in lock lock-in ; do for su in `seq 3 %s` ; do amf-adm $cmd safSu=PL-$su,safSg=NWayActive,safApp=pmProducerApp;done;done" % numOfNodes)
    """
    
    ssh_lib.sendCommand("sed 's/BladeX-/Blade1-/' /home/test/pm/config.txt > /home/test/pm/producer/SC-2-1/config.txt")
    ssh_lib.sendCommand("sed 's/BladeX-/Blade1-/' /home/test/pm/config.txt > /home/test/pm/producer/SC-2-2/config.txt")
    if (numOfNodes > 2):
        ssh_lib.sendCommand("for i in `seq 3 %s`; do sed 's/BladeX-/Blade1-/' /home/test/pm/config.txt > /home/test/pm/producer/PL-2-$i/config.txt; done" % numOfNodes)
    
    ssh_lib.sendCommand("echo bcast reload | netcat localhost 48820")
    
    misc_lib.waitTime(300)
    ssh_lib.sendCommand("echo bcast reload | netcat localhost 48820") 
    
    """
    ssh_lib.sendCommand("for cmd in unlock-in unlock ; do for su in SC-1 SC-2 ; do amf-adm $cmd safSu=$su,safSg=NWayActive,safApp=pmProducerApp;done;done")
    if (numOfNodes > 2):
        ssh_lib.sendCommand("for cmd in unlock-in unlock ; do for su in `seq 3 %s` ; do amf-adm $cmd safSu=PL-$su,safSg=NWayActive,safApp=pmProducerApp;done;done" % numOfNodes)
    """
    """
    ssh_lib.setTimeout(120)
    ssh_lib.sendCommand("for i in `immfind | grep ^pmJobId=`; do  echo immcfg -a requestedJobState=1 $i;immcfg -a requestedJobState=1 $i; done")
    """
    ssh_lib.setTimeout(300)
    ssh_lib.sendCommand("for i in `cmw-pmjob-list | sed 's/pmJobId=\(.*\), req.*/\\1/'` ; do cmw-pmjob-start $i;done")

    ssh_lib.setTimeout(60)
    ssh_lib.sendCommand("echo bcast enable | netcat localhost 48820")
    ssh_lib.sendCommand("echo bcast start  | netcat localhost 48820")
    
    ssh_lib.setTimeout(defaultTimeout)

def generateConfigTxt(numOfNodes):
    """
    generateConfigTxt(numOfNodes, MI=50000, MT=500, rate=100):
    Requirements:                               This TC:
    100 000 MI   (measurement instances)        50 000
      1 000 MT   (measurement types)               500
        100 jobs (measurement reports)              50
        
      1 000 updates per second on each blade       100
    """
    workspace = os.environ['MY_REPOSITORY']
    configDir = workspace + "/test_env/lib/config/"
    
    #y=ab^x
    #b^60=1/12,5 =>
    b=0.9587782345443288
    #a=25/b^10 and a=2/b^70 =>
    a=38.0853845
    
    myclass=100
    type=10
    y=a*(math.pow(b, numOfNodes))
    #print a, b, numOfNodes, y
    
    #y=kx+m
    k=1.0/60
    m=1-k*10
    y2=(k*numOfNodes)+m
    
    instance_min=(int)(round(y2))
    instance_max=(int)(y)
    
    #print instance_min, instance_max
    
    step=1
    
    temp=""
    for c in range(1, myclass+1):
        for t in range(1, type+1):
            for i in range(instance_min, instance_max+1):
                for s in range(1, step+1):
                    temp=temp+"add c,PM-%s,PM-%s-%s,InstanceBladeX-%s,%s\n" % (c, c, t, i, s)
    temp=temp+"disable\nrate 100"

    """
    """
    
    f = open("%sconfig.txt" % configDir, "w")
    f.write(temp)

def getCountersTicked():
    defaultTimeout = ssh_lib.getTimeout()
    ssh_lib.setTimeout(60)
    bcast_print = ssh_lib.sendCommand("echo bcast print  | netcat localhost 48820")
    tempList = bcast_print[1].split("\n")
    countersTickedList = []
    for item in tempList:
        logger.info(item)
        if (re.search('Counters ticked:', item)):
            tempStr = item.split(": ")
            countersTickedList.append(int(tempStr[1]))
    ssh_lib.setTimeout(defaultTimeout)
    return countersTickedList

def stopPm():
#################################
    defaultTimeout = ssh_lib.getTimeout()
    ssh_lib.setTimeout(60)
    ssh_lib.sendCommand("echo bcast stop | netcat localhost 48820")
    
    misc_lib.waitTime(3)
    
    tickedList = []
    res = ssh_lib.sendCommand("echo bcast print | netcat localhost 48820| grep ticked: | awk 'BEGIN {i=0} {i = i + $3} END{ print i}'")
    ticked = int(res[1])
    res = ssh_lib.sendCommand("echo bcast print | netcat localhost 48820| grep  overload:| awk 'BEGIN {i=0} {i = i + $7} END{ print i}'")
    overload = int(res[1])
    res = ssh_lib.sendCommand("echo bcast print | netcat localhost 48820| grep  errors:| awk 'BEGIN {i=0} {i = i + $6} END{ print i}'")
    errors = int(res[1])
    ssh_lib.setTimeout(180)
    res = ssh_lib.sendCommand("""egrep -h "InstanceBlade.*:" /home/test/pm/jobs/safJob\=*  | awk 'BEGIN {i=0} {i = i + $2} END{ print  i}'""")
    reportedTicked = int(res[1])
    
    tickedList.append(ticked)
    tickedList.append(overload)
    tickedList.append(errors)
    tickedList.append(reportedTicked)
    
    # return a list with [ticked, overload, errors, reportedTicked]
    ssh_lib.setTimeout(defaultTimeout)
    return tickedList
    
def cleanPm():
#################################
    defaultTimeout = ssh_lib.getTimeout()
    ssh_lib.setTimeout(600)
    # Remove RW parts
    ssh_lib.sendCommand("echo bcast stop  | netcat localhost 48820")
    ssh_lib.sendCommand("echo bcast clear | netcat localhost 48820")

    ssh_lib.sendCommand("for i in `cmw-pmjob-list | sed 's/pmJobId=\(.*\), req.*/\\1/'` ; do cmw-pmjob-stop $i;done")
    ssh_lib.sendCommand("for i in `cmw-pmjob-list | sed 's/pmJobId=\(.*\), req.*/\\1/'` ; do cmw-pmjob-delete $i;done")
    # Remove RO parts
    ssh_lib.sendCommand("for i in `immfind | grep ^pmThresholdMonitoringId=` ; do immcfg -d $i; done")
    ssh_lib.sendCommand("for i in `immfind | grep ^measurementReaderId=` ; do immcfg -d $i; done")
    ssh_lib.sendCommand("for i in `immfind | grep ^measurementTypeId=` ; do immcfg -d $i; done")
    ssh_lib.sendCommand("for i in `immfind | grep ^pmGroupId=` ; do immcfg -d $i; done")
    
    ssh_lib.sendCommand("\\rm -f /home/test/pm/jobs/*")
    ssh_lib.setTimeout(defaultTimeout)

##############################################################################
# Module test
##############################################################################
if __name__ == '__main__':
    print 'main'
