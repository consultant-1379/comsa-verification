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

   Author:

   Description:

'''

#############IMPORT##################

from org.apache.log4j import Logger
import se.ericsson.jcat.omp.fw.OmpLibraryException as OmpLibraryException
import omp.tf.ssh_lib as ssh_lib

#############GLOBALS##################


logger = None
targetData = None


#############exceptions#############

class NoExternalTgen(Exception):
    pass


#############setUp / tearDown#############

def setUp(logLevel,currentSut):

    global logger
    global targetData

    logger = Logger.getLogger('tg_lib')
    logger.setLevel(logLevel)

    logger.info("tg_lib: Initiating!")

    targetDataLib = currentSut.getLibrary("TargetDataLib")
    targetData = targetDataLib.getTargetData()

    return


def tearDown():
    #logger_lib.logMessage("lib: Bye bye !!", logLevel='debug')
    logger.debug("tg_lib: bye, bye!")
    return


#############lib functions#############

def externalTgenAddresses():
    """externalTgenAddresses finds the address data needed for managing the
       external Tgen processes of the PL instance. It returns a pair where the
       first element is a list of management addresses of hosts where Tgen
       should run, and the second element is the address that Tgen should use
       to connect to TGC."""

    data = targetData['ipAddress']
    try:
        TgenHosts = [data['ctrl']['testpc']] + data['ctrl']['external']
        TGC = data['vip']['vip_3']
    except KeyError:
        TgenHosts = data['testApp']['external_tg']
        TGC = data['testApp']['tg_coord']
    # Be compatible with old hardware data files where 'external_tg' may be a
    # string when no addresses are configured.
    if type(TgenHosts) != list or len(TgenHosts) == 0:
        raise NoExternalTgen
    return (TgenHosts, TGC)


def instantiateExternalTG():
    """Instantiates the external traffic generator

        Return ('SUCCESS','info') or ('ERROR','info').
    """

    global targetData

    logger.info('enter instantiateExternalTG')

    (hosts, TGC) = externalTgenAddresses()
    result = ['SUCCESS', 'To be defined later']

    if type(hosts) == list:
        # Instantiate all defined external_tg.
        for host in hosts:

            # Find the external Tgen binary and wrapper script.
            cmd = ("for dir in /opt/ericsson.se/testapp/bin " +
                              "/opt/TA_EXT_TGEN/bin /opt/TA_TAPP/bin ; " +
                   "do " +
                       "file=${dir}/ta_tgen; " +
                       "if [ -f ${file} -a -f ${file}.sh ] ; then " +
                           "echo ${file}.sh; " +
                           "break; " +
                       "fi; " +
                   "done")
            result = ssh_lib.sendRawCommand(host, cmd, targetData['user'],
                                            targetData['pwd'], 30)

            if result[0] == 'SUCCESS':
                wrapper = result[1]
                if len(wrapper) == 0:
                    message = 'No external Tgen was found on ' + host + '.'
                    logger.error(message)
                    result = ['ERROR', message]
                else:
                    cmd = ('TA_TGEN_ADDR=' + TGC + ' ' + wrapper +
                           ' terminate 8002')
                    result = ssh_lib.sendRawCommand(host, cmd,
                                                    targetData['user'],
                                                    targetData['pwd'], 30)
                    if result[0] == 'SUCCESS':
                        logger.debug('Command executed: %s on %s' % (cmd, host))
                    else:
                        logger.error('Could not execute: %s' % cmd)

                    # Set environment variables and start two Tgen processes
                    numHostGen = 2

                    for n in range(numHostGen):
                        cmd = ('ulimit -c unlimited; TA_TGEN_ADDR=' + TGC +
                               ' ' + wrapper + ' instantiate 8002 ' +
                               '--instance PL-E' + str(n))
                        result = ssh_lib.sendRawCommand(host, cmd,
                                                        targetData['user'],
                                                        targetData['pwd'], 30)
                        if result[0] == 'SUCCESS':
                            logger.debug('Command executed: %s on %s' % (cmd,
                                                                         host))
                        else:
                            logger.error('Could not execute: %s on %s' % (cmd,
                                                                          host))

    logger.info('leave instantiateExternalTG')
    return result


def terminateExternalTG():
    """Terminates the external traffic generator

        Return ('SUCCESS','info') or ('ERROR','info').
    """

    global targetData

    (hosts, TGC) = externalTgenAddresses()
    result = ['SUCCESS', 'To be defined later']

    if type(hosts) == list:
        # Terminate all defined external_tg.
        for host in hosts:

            logger.info('enter terminateExternalTG')

            # Stop generator
            cmd = ('TA_TGEN_ADDR=' + TGC +
                   ' /opt/TA_TAPP/bin/ta_tgen.sh terminate 8002')
            result = ssh_lib.sendRawCommand(host,cmd, targetData['user'], targetData['pwd'])

            if result[0] == 'SUCCESS':
                logger.debug( 'Command executed: %s on %s' % (cmd, host))
            else:
                logger.error( 'Could not execute: %s on %s' % (cmd, host))

            logger.info('leave terminateExternalTG')

    return result
