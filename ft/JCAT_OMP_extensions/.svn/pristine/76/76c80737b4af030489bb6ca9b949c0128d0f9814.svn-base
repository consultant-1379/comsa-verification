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

import os
import logging
import datetime
import re
import inspect
import sys
import string
from os.path import abspath, basename
import se.ericsson.jcat.fw.utils.TestInfo as TestInfo
import org.apache.log4j.Logger as Logger
import org.apache.log4j.FileAppender as FileAppender
import org.apache.log4j.PatternLayout as PatternLayout
import java.lang.System as System


class cLOGGER:

    _logger = None
    _counter = 0
    _original_logdir = None

    # Construction
    def __init__(self, handle, logFile, logLevel) :
        self.logLevels =  { 'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR, }
        self.logLevel = self.logLevels[logLevel]

        if cLOGGER._original_logdir == None:
            try:
                os.unlink("%s/%s_events.out" %(cLOGGER._original_logdir,cLOGGER._counter))
            except:
                pass
            cLOGGER._original_logdir = System.getProperty("logdir")
            cLOGGER._logger = Logger.getLogger(self.__class__.__name__)
            cLOGGER._logger.removeAllAppenders()
            cLOGGER._logger.setAdditivity(0)
            cLOGGER._logger.addAppender(FileAppender(PatternLayout("(Time: %d{ISO8601}) %m %n"), 
                                                           "%s/%s_events.out" 
                                                           %(System.getProperty("logdir"), 
                                                             cLOGGER._counter), 
                                                             0))
            cLOGGER._counter += 1

    def log(self, message, filePath, lineNo, printConsole, printLog, logLevel):
        import se.ericsson.jcat.omp.fw.OmpTestCase as OmpTestCase
        #from ompjcat.OmpJythonTestCase import OmpJythonTestCase
        
        lvl=self.logLevels[logLevel]
        if printConsole==True and lvl >= self.logLevel:
            t = datetime.datetime.now() 
            msg = "## %s,%s %s --> %s\n" % (t.strftime("%Y-%m-%d %H:%M:%S"), str(t.microsecond)[:3] , string.upper(logLevel), message )
            sys.stdout.write( msg)        
    
        currentTC = OmpTestCase.currentTestCase()
        if currentTC != None and lvl >= self.logLevel:
            msg = "## %s %s line %s --> %s" % (string.upper(logLevel),basename(filePath),lineNo,message)
            currentTC.logMsg(msg)
        else:    
            #currentTC = OmpJythonTestCase.currentTestCase()
            if currentTC != None and lvl >= self.logLevel and printLog==True:
                if re.match('tc_',filePath[filePath.rfind('/')+1:len(filePath)]):
                    msg = "## line %s --> %s" % (lineNo, message)
                    currentTC.logMsg(msg, basename(filePath), lvl)
                msg = "## %s %s line %s --> %s" % (string.upper(logLevel),basename(filePath),lineNo,message)
                currentTC.logMsgToFile(msg)
        

        if currentTC == None and lvl >= self.logLevel and printLog==True:
            msg = "## %s %s line %s --> %s" % (string.upper(logLevel),basename(filePath),lineNo,message)
            cLOGGER._logger.info(msg) 

    def Close(self):
        try:
            os.rename("%s/%s_events.out" %(cLOGGER._original_logdir,cLOGGER._counter-1),
                      "%s/%s_events.out" %(TestInfo.getLogDir(),cLOGGER._counter-1))
        except:
            pass
