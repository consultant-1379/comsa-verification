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

import logging
import datetime
import re
import inspect
import sys
import string
from os.path import abspath, basename


class cLOGGER(logging.FileHandler):

    # Construction
    def __init__(self, handle, logFile, logLevel) :
        self.handle = handle
        self.fh = logging.FileHandler(logFile, mode='a')
        self.fh.flush()
        self.fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(filename)s line %(lineno)s %(message)s' ) )
        self.logLevels =  { 'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR, }
        self.logLevel = self.logLevels[logLevel]

    def log(self, message, filePath, lineNo, printConsole, printLog, logLevel):
        lvl=self.logLevels[logLevel]
        if printConsole==True and printLog==False and lvl >= self.logLevel:
            msg = "## %s(%s) %s --> %s\n" % (basename(filePath), lineNo,string.upper(logLevel), message )
            sys.stdout.write( msg)
        if printConsole==True and printLog==True and lvl >= self.logLevel:
            t = datetime.datetime.now() 
            msg = "## %s,%s %s --> %s\n" % (t.strftime("%Y-%m-%d %H:%M:%S"), str(t.microsecond)[:3] , string.upper(logLevel), message )
            sys.stdout.write( msg)
        if lvl >= self.logLevel and printLog==True:
            rec = logging.LogRecord(self.handle, lvl, filePath, lineNo, message, None, None )
            self.fh.emit(rec)

    def Close(self):
        self.fh.close()