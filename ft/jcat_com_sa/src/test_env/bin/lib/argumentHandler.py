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

import os
import sys
# The line below is not needed anymore. The target_data file is located in $MY_REPOSITORY/test_env/bin/target_data_vCluster.py
#sys.path.append('/vobs/tspsaf/tools/targetconf/lib')

import booking_lib as booking_lib

from optparse import OptionParser


def setup_option_parser():
    """
    Creates a OptionParser with all necessary options.
    """

    home = os.environ['HOME']
    usage = """
 %prog [options]

 examples:
  executive.py -u
  executive.py -t """

    # find bookedNode to set it as default value for --config
    try :
        bookedNode = booking_lib.checkBooking()
    except:
        bookedNode = 'No target booked'




    parser = OptionParser( prog="executive.py", usage=usage )

    parser.add_option( "--repository" , "-r", dest="repository",
                     default='%s/' % os.environ['MY_REPOSITORY'],
                     help="This points to the repository location" )

    parser.add_option( "--suite" , "-s", dest="suite",
                     default="testsuite.xml",
                     help="This points to the SUITE XML configuration file" )

    parser.add_option( "--config_dir" , "--cd", dest="config_dir",
                     default="test_env/config/",
                     help="This points to the SUT configuration file directory" )

    parser.add_option( "--config" , "-c", dest="config",
                     default=bookedNode,
                     help="This points to the HW target" )

    parser.add_option( "--testconfig_dir" , "--td", dest="testConfig_dir",
                     default="test_env/config/",
                     help="This points to the test configuration file directory" )

    parser.add_option( "--testconfig" , "-t", dest="testConfig",
                     default="test_config.xml",
                     help="This points to the Test Config XML configuration file" )

    myUserName = os.environ['USER']
    
    parser.add_option( "--logdir" , "-d", dest="logdirectory",
                     default="/proj/coremw_scratch/%s/logs/" % myUserName,
                     help="This is the log directory used" )

    parser.add_option( "--loglevel" , "-l", dest="loglevel",
                     default="INFO",choices=[ "", "TRACE", "DEBUG", "INFO", "WARN", "ERROR" , "FATAL"],
                     help="This is the log level used ( default: %default )" )

    parser.add_option( "--name" , "-n", dest="suitename",
                     default="coremw",
                     help="This is the suitname used" )

    parser.add_option( '--sc', "--SC", dest="controllers", default=2,
                     type='int', help="Numbers of system controller blades" )

    parser.add_option( '--pl', "--PL", dest="payloads", default=2,
                     type='int', help=" Numbers of payload blades" )

    parser.add_option( '--hostnameSeparator', "--sep", dest="hostnameSeparator", default="-",
                     help=" This defines the separator used in the hostname" )

    parser.add_option( "--loadpl", dest="loadpl",type="choice", default="40", choices=[ "0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100" ],
                    help="Load levels on payload blades: 0, 10, 20, 30, 40, 50, 60,70, 80, 90, 100" )

    parser.add_option( "--loadsc", dest="loadsc", type="choice", default="20", choices=["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100" ],
                    help="Load levels on sc blades: 0, 10, 20, 30, 40, 50, 60,70, 80, 90, 100" )

    parser.add_option( "--loadprofile", dest="loadprofile", type="choice", default="normal", choices=["normal","high","ultra","nop"],
                    help="Load profiles: normal, high, ultra, nop" )

    parser.add_option( '--amfNodeNameSeparator', "--amfsep", dest="amfNodeNameSeparator", default="-",
                     help=" This defines the separator used for amf node names" )

    parser.add_option( '--clmNodeNameSeparator', "--clfsep", dest="clmNodeNameSeparator", default="-",
                     help=" This defines the separator used in the notifications" )

    parser.add_option("--runSingleTestCase", "--oneTC", dest="singleTestCase", default='',
                    help="This option allows to run a single test case. Give the test case tag as argument.")

    parser.add_option("--singleTestCaseIterations", "--oneTcIter", dest="singleTestCaseIterations", default="\'\'",
                    help="This option allows the number of iterations of the test case to be defined.")
    
    parser.add_option("--productSettings", dest="productSettings", choices=["coremw","comsa"], default="comsa", 
                      help="This option allows to select comsa default settings when running a single test case.")
    
    parser.add_option( '--currentRelease', dest="currentRelease", default="R6A10",
                     help=" This defines the current release used where default value is R6A10")

    parser.add_option( "--setUpCheck" , "--suc", dest="setUpCheck",choices=["True","False"],
                     default= 'True',
                     help="This option allows to override the setUpCheck, default is True(execute setUpCheck)" )

    parser.add_option( "--runTestCheck" , "--rtc", dest="runTestCheck",choices=["True","False"],
                     default= 'True',
                     help="This option allows to override the runTestCheck, default is True(execute runTestCheck)" )

    parser.add_option( "--tearDownCheck" , "--tdc", dest="tearDownCheck",choices=["True","False"],
                     default= 'True',
                     help="This option allows to override the tearDownCheck, default is True(execute tearDownCheck)" )

    parser.add_option( "--dbStore" , "--dbs", dest="dbStore",default= False,
                     help="This option enables the TestStatistics database. The choices are False or True, default is False" )

    parser.add_option( "--reinstall", dest="reinstall",type="choice", default="cmw", choices=[ "os", "cmw", "testApps", "comsa", "monitor",
                                                                                              "testapp","ntfsubscriber","smfmonitor","amfmeasure",
                                                                                              "testAppsWithPm", "pm", "pmconsumer", "pmproducer"],
                    help="reinstall levels: os = LOTC +vip, cmw = os + cmw, testApps = cmw + testapp + ntfsubscriber + smfmonitor + amfmeasure,\
                    comsa = testApps + COM SA + COM(not impl), monitor = testApps + monitor,\
                    testapp = cmw + testapp, ntfsubscriber = cmw + ntfsubscriber, smfmonitor = cmw + smfmonitor, amfmeasure = cmw + amfmeasure,\
                    pmconsumer = cmw + pmconsumer, pmproducer = cmw + pmproducer, pm = cmw + pmproducer + pmproducer,\
                    testAppsWithPm = cmw + testapp + ntfsubscriber + smfmonitor + amfmeasure + pmproducer + pmproducer" )

    parser.add_option("--testName", dest="definedTestName", default='',
                    help="use this to define a unique test name")

     #Start                
    parser.add_option("--nodename", dest="nodename", default='',
                    help="use this to define a node name")
    #End
    parser.add_option("--destinationProfile", dest="destinationProfile",
                      type="choice", choices=["IPv4", "IPv6", "equal"],
                      default="IPv4", metavar="IPv4|IPv6|equal",
                      help=("This option specifies the combination of " +
                            "network protocols to use: only IPv4, only IPv6, " +
                            "or equal distribution over all available IPv4 " +
                            "and IPv6 addresses. Test cases may override " +
                            "this with their own settings."))
    
    parser.add_option("--trace", dest="tracelogs",type="choice", default="off", choices=[ "off", "normal", "all" ], #"amfd", "amfnd", "ckptd", "ckptnd", "clmd", "dtmd","dtd","immd","immnd", "logd", "ntfd", "rded", "smfd", "smfnd"],
                    help="Enables/disables trace for an opensaf service on the node the command is executed on. \
                    The following services are possible to trace: \
                    amfd amfnd ckptd ckptnd clmd dtmd dtd immd immnd logd ntfd rded smfd smfnd")
    
    parser.add_option( "--randomSuite" , "--random", dest="randomSuite",default= False,
                     help="This option enables random execution of the given test suite. The choices are False or True, default is False" )
    
    parser.add_option( "--clcTestSuite" , "--clc", dest="clcTestSuite",default= False,
                     help="Compressed Life Cycle (CLC) testsuite option. The choices are False or True, default is False" )
    
    parser.add_option("--storeMeas", "--stm", dest="storeMeas", default="",
                     help="CMW tag name for characteristic measurements " )
    
    parser.add_option("--compareMeas", "--cmpm", dest="compareMeas", default="",
                     help="CMW tag name you want to compare against" )
    
    parser.add_option( "--openReport" , "--openreport", dest="openReport",default= True,
                     help="This option enable7disable the automatic openening of the test report. The choices are False or True, default is True " )

    parser.add_option( "--installSw" , "--inst", dest="installSw", choices=["True","False"], default= "False",
                     help="This parameter is used to decide if the setUpTest case should perform a clean installation of the test target. If True is selected, it is mandatory to also use the --swDirNumber argument." )

    parser.add_option( "--buildComSa" , "--build", dest="buildComSa", choices=["True","False"], default= "False",
                     help="This parameter is used to define whether COM SA should be build for this test run Alternatively a ready build can be used from /home/jenkinuser/release/install/.../comsa/" )

    parser.add_option( "--swDirNumber" , "--sdn", dest="swDirNumber",default= 'undef',
                     help="This parameter is used to define from which directory the cba cluster will be re-installed under /home/jenkinuser/release/install" )
    
    parser.add_option( "--runStressTool" , "--rst", dest="runStressTool", choices=["True","False"], default= "False",
                     help="This parameter is used to specify whether to install and run the stress tool during the test suite.")
    
    parser.add_option( "--checkCompilerWarn" , "--ccw", dest="checkCompilerWarn", choices=["True","False"], default= "True",
                     help="This parameter is used to specify whether to build COM SA in the setup test case and check for compiler warnings.")
    
    parser.add_option( "--displayFirefox" , "--firefox", dest="displayFirefox", choices=["True","False"], default= "True",
                     help="This parameter is used to specify whether reports are displayed in Firefox during execution.")

    parser.add_option( "--debug", action="store_true", dest="debug", 
                     help="This parameter is used to specify whether started in debug mode.")

    parser.add_option( "--resetCluster", "--rCl", dest="resetCluster", default = "undef",
                     help="This parameter is used to specify a snapshot name which will be restored in the setUp test case.")

    return parser


if __name__ == "__main__":
    setup_option_parser()
