#! /usr/bin/env python

########################################################################
# This GENERAL hardware file makes it possible for testcases to do
# operations towards the hardware without knowing which hardware it
# is operating on.
#
# The variable 'targetLib' contains the name of the target specific
# file currently used. It can today have three different values: 'is_lib',
# 'uml_lib' or 'cots_lib'. All calls to the functions in this file will
# be forwarded to the corresponding functions in the selected target
# lib file.
#
# All functions return two strings:
# - one result slogan: SUCCESS or ERROR
# - one result string containing the value read or the error message
#
# THINGS TO IMPROVE:
#
#
########################################################################
# Short description of parameters for a test cluster
#---------------------------------------------------
# 'ipAddress'	IP address definitions
#      'ctrl'		Management addresses
#         'NB'			North bound (official OAM) interface  (ought to be moved out from this file)
#         'ctrl1'		Management address for System Controller 1
#         'ctrl2'		Management address for System Controller 2
#         'ctrl_if'             Management network interface
#         'ctrl_net'            Management IP network
#         'ctrl_gw'             Management routing Gateway IP address
#         'testpc'		Management address of gateway server that also can act as an external traffic host for test application clients and servers
#         'external'		Management addresse(s) of any external hosts for external test application clients and servers
#     'traffic'		Traffic addresses of external servers
#         'gateway_IPv4'	IPv4 traffic addresse(s) of gateway server that also can act as an external traffic host for test application clients and servers
#         'gateway_IPv6'	IPv6 traffic addresse(s) of gateway server that also can act as an external traffic host for test application clients and servers
#         'external_IPv4'	IPv4 traffic addresse(s) of external hosts for external test application clients and servers
#         'external_IPv6'	IPv6 traffic addresse(s) of external hosts for external test application clients and servers
#     'testApp'		Depricated testApp settings only kept for backward compatibility reasons. Don't use these any longer.
#         'test_app'		TestApp server address for incoming external traffic (to PLs)
#         'external_tg'		Management addresses of external hosts for external testApp clients
#         'tg_coord'		TestApp coordinator address to be used from test framework and testApp clients
#     'vip'		VIP addresses and VIP frontend address information
#         'vip_1'		VIP traffic address 1
#         'vip_2'		VIP traffic address 2,
#         'vip_3'		VIP O&M address, can also be used for test application traffic, default source address for outgoing IPv4 traffic
#         'vip_IPv6_OAM'	VIP IPv6 OAM addresses and default source address for outgoing IPv6 traffic
#         'vip_IPv6_traffic'	VIP IPv6 traffic addresses
#         'vip_load_balancer'	VIP processors with or without load balancer
#         'vip_link_type'	VIP frontend link interface type
#         'vip_link_net'	VIP frontend link ip net
#         'vip_link_addr'	VIP frontend link local address
#         'vip_link_gw'		VIP IPv4 frontend OSPF V2 gateway address
#         'vip_IPv6_link_gw'	VIP IPv6 frontend OSPF V3 gateway address
#         'vip_area'		VIP OSPF V2 & V3 area
#
# to be continued ..
########################################################################

import os

data = {}

### Common COTS data structures ###
COTS_TARGET_TYPE="cots_target"
SIMULATOR_TARGET_TYPE="simulator_target"

COTS_TARGET_USER =  "root"
COTS_TARGET_PWD =  "rootroot"
COTS_TERMINAL_SERVER_USER =  "root"
COTS_TERMINAL_SERVER_PWD =  "dbps"
COTS_TARGET_SNMP = {'prefix' : "1.3.6.1", 'community': "tspsaf", 'version' : '-v2c', 'trapDaemonPort' : '50000' }
COTS_CTRL_PATTERNS =  """(SC[_-]2[_-][12](:~ |(:~/|:/)[^\s]* )?# )"""
COTS_PL_PATTERNS  =  """(PL[_-]2[_-]\d+(:~ |(:~/|:/)[^\s]* )?# )"""
COTS_HOSTNAME_SEPARTOR_PATTERNS = """([_|-])"""
COTS_TEST_PC_PATTERNS = """(gwhost\d+:~ #)"""
COTS_VIP_TG_PATTERNS = """(safTg\d+:~ #)"""
COTS_SWITCH_DEVICE_PATTERNS = """(console>)"""
SIMULATOR_TARGET_BLADES= {  'blade_2_1'    : "192.168.0.1",
                            'blade_2_2'    : "192.168.0.2",
                            'blade_2_3'    : "192.168.0.3",
                            'blade_2_4'    : "192.168.0.4"
                         }


SIMULATOR_TARGET = { 'blade_2_1'     : "192.168.73.2",
                                         'blade_2_2'    : "192.168.73.3",
                                         'blade_2_3'    : "192.168.73.4",
                                         'blade_2_4'    : "192.168.73.5"
                                         }

QEMU_TARGET_TYPE="qemu_target"


defaultQEmuSettings="""
{
    'physical_size': "NUMBER OF BLADES, PLEASE CHANGE",
    'execution_capacity_factor': "0.2",
    'watchdog' : '',
    'target' : 'qemu_target_CHANGE ME'
    'ipAddress' : {
        'blades' : {
            'blade_2_1' : "192.168.0.1",
            'blade_2_2' : "192.168.0.2",
            #'blade_2_3' : "192.168.0.3", # REMOVE THE COMMENT IF USED
            #'blade_2_4' : "192.168.0.4"  # REMOVE THE COMMENT IF USED
        },
        'ctrl' : {
            'NB'        :"",
            'ctrl1'     : "IP ADDRESS TO SC-1, PLEASE CHANGE",
            'ctrl2'     : "IP ADDRESS TO SC-2, PLEASE CHANGE",
            'testpc'    :'',
            'ipmi_base' : '192.168.0.101'
        },
        'ipmi' : {
            'blade_2_1'     : "192.168.73.2",
            'blade_2_2'    : "192.168.73.3",
            #'blade_2_3'    : "192.168.73.4",
            #'blade_2_4'    : "192.168.73.5"
        },
        'testApp'  : {
            'external_tg': '',
            'test_app'   : '',
            'tg_coord'   : ''
        },
        'traffic' : {
            'network_IPv4' : '0.0.0.0/24',
            'gateway_IPv4' : ['0.0.0.0'],
            'gateway_IPv6' : ['0:0:0:0:0:0:0:0'],
            'external_IPv4': [],
            'external_IPv6': []
        },
        'vip'  : {
            'vip_1'    : '0.0.0.0',
            'vip_2'    : '0.0.0.0',
            'vip_3'    : '0.0.0.0'
        },
        'serial' : {
            'ip'      : '',
            'SC_2_1'  : '',
            'SC_2_2'  : '',
            # 'PL_2_3'  : '', # REMOVE THE COMMENT IF USED
            # 'PL_2_4'  : '', # REMOVE THE COMMENT IF USED
            'switch_1': '',
            'switch_2': ''
        },
        'switches' : {
            'switch_1'     : '',
            'switch_2'     : '',
            'portsInOrder' : []
        }
    },
    'ports' : {
        'snmptrapd': "50050"
    }
}
"""

# Only for being backward compatible with the dummy? imports in the TSPSAF3.0 test environment
targetData = -1

def _setTargetHwData(targetHw):

    targetData =  {
     # Specific SIMULATOR system information:
        'essim_target' :
        {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'ipAddress' :
            {
                'ctrl' :
                {
                 'NB'  :"192.168.73.12",
                 'ctrl1':"192.168.73.2",
                 'ctrl2' :"192.168.73.3",
                 'testpc':'192.168.73.1'
                },
                'testApp'  :
                {
                 'test_app'   : '192.168.236.7',
                 'external_tg': 'To be defined later'
                },
                'vip'  :
                {
                 'vip_gw':  '192.168.73.1',
                 'vip_1'    : '192.168.236.7',
                 'vip_3'    : '192.168.73.7',
                },
                'serial' :
                {
                 'ip': '',
                 'SC_2_1': '',
                 'SC_2_2': '',
                 'PL_2_3': '',
                 'PL_2_4': '',
                 'switch_1': '',
                 'switch_2': ''
                },
                'switches' :
                {
                 'switch_1' : '',
                'switch_2' : '',
                 'portsInOrder' : []
                }
             },
            'ports' :
            {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_151' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.5",
                    'ctrl2' :"10.172.15.6",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_152' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.10",
                    'ctrl2' :"10.172.15.11",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_153' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.15",
                    'ctrl2' :"10.172.15.16",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_154' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.20",
                    'ctrl2' :"10.172.15.21",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_155' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.25",
                    'ctrl2' :"10.172.15.26",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_156' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.30",
                    'ctrl2' :"10.172.15.31",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_157' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.35",
                    'ctrl2' :"10.172.15.36",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_158' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.40",
                    'ctrl2' :"10.172.15.41",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_159' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.45",
                    'ctrl2' :"10.172.15.46",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_160' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.50",
                    'ctrl2' :"10.172.15.51",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_161' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.55",
                    'ctrl2' :"10.172.15.56",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_162' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.60",
                    'ctrl2' :"10.172.15.61",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_163' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.65",
                    'ctrl2' :"10.172.15.66",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_164' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.70",
                    'ctrl2' :"10.172.15.71",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_165' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.75",
                    'ctrl2' :"10.172.15.76",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_166' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.80",
                    'ctrl2' :"10.172.15.81",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_167' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.85",
                    'ctrl2' :"10.172.15.86",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_168' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.90",
                    'ctrl2' :"10.172.15.91",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_169' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.95",
                    'ctrl2' :"10.172.15.96",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_170' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.100",
                    'ctrl2' :"10.172.15.101",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_171' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.105",
                    'ctrl2' :"10.172.15.106",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_172' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.110",
                    'ctrl2' :"10.172.15.111",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_173' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.115",
                    'ctrl2' :"10.172.15.116",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_174' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.120",
                    'ctrl2' :"10.172.15.121",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_175' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.125",
                    'ctrl2' :"10.172.15.126",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_176' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.130",
                    'ctrl2' :"10.172.15.131",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_177' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.135",
                    'ctrl2' :"10.172.15.136",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_178' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.140",
                    'ctrl2' :"10.172.15.141",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_179' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.145",
                    'ctrl2' :"10.172.15.146",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_180' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.150",
                    'ctrl2' :"10.172.15.151",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_181' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.155",
                    'ctrl2' :"10.172.15.156",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_182' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.160",
                    'ctrl2' :"10.172.15.161",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_183' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.165",
                    'ctrl2' :"10.172.15.166",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_184' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.170",
                    'ctrl2' :"10.172.15.171",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_185' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.175",
                    'ctrl2' :"10.172.15.176",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_186' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.180",
                    'ctrl2' :"10.172.15.181",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_187' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.185",
                    'ctrl2' :"10.172.15.186",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_188' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.190",
                    'ctrl2' :"10.172.15.191",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_189' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.195",
                    'ctrl2' :"10.172.15.196",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_190' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.200",
                    'ctrl2' :"10.172.15.201",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_191' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.205",
                    'ctrl2' :"10.172.15.206",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_192' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.210",
                    'ctrl2' :"10.172.15.211",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_193' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.215",
                    'ctrl2' :"10.172.15.216",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_194' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.220",
                    'ctrl2' :"10.172.15.221",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_195' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.225",
                    'ctrl2' :"10.172.15.226",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_196' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.230",
                    'ctrl2' :"10.172.15.231",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_197' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.235",
                    'ctrl2' :"10.172.15.236",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_198' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.240",
                    'ctrl2' :"10.172.15.241",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_199' :  {
            'physical_size': "4",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.172.15.245",
                    'ctrl2' :"10.172.15.246",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },
        'qemu_target_vn_18' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.36",
                    'ctrl2' :"10.3.2.37",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_19' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.38",
                    'ctrl2' :"10.3.2.39",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_20' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.40",
                    'ctrl2' :"10.3.2.41",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_21' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.42",
                    'ctrl2' :"10.3.2.43",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_22' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.44",
                    'ctrl2' :"10.3.2.45",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_23' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.46",
                    'ctrl2' :"10.3.2.47",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_24' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.48",
                    'ctrl2' :"10.3.2.49",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_25' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.50",
                    'ctrl2' :"10.3.2.51",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_26' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.52",
                    'ctrl2' :"10.3.2.53",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_27' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.54",
                    'ctrl2' :"10.3.2.55",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_28' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.56",
                    'ctrl2' :"10.3.2.57",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        },

        'qemu_target_vn_29' :  {
            'physical_size': "2",
            'execution_capacity_factor': "0.2",
            'watchdog' : '',
            'ipAddress' : {
                'ctrl' : {
                    'NB'  :"",
                    'ctrl1':"10.3.2.58",
                    'ctrl2' :"10.3.2.59",
                    'testpc':'',
                    'ipmi_base' : '192.168.0.100'
                },
                'testApp'  : {
                    'test_app'   : '',
                    'external_tg': 'To be defined later'
                },
                'traffic' : {
                    'network_IPv4' :'0.0.0.0/24',
                    'gateway_IPv4' :['0.0.0.0'],
                    'gateway_IPv6' :['0:0:0:0:0:0:0:0'],
                    'external_IPv4':[],
                    'external_IPv6':[]
                },
                'vip'  : {
                    'vip_1'    : '0.0.0.0',
                    'vip_2'    : '0.0.0.0',
                    'vip_3'    : '134.138.99.56'
                },
                'serial' : {
                    'ip': '',
                    'SC_2_1': '',
                    'SC_2_2': '',
                    'PL_2_3': '',
                    'PL_2_4': '',
                    'switch_1': '',
                    'switch_2': ''
                },
                'switches' : {
                    'switch_1' : '',
                    'switch_2' : '',
                    'portsInOrder' : []
                }
            },
            'ports' : {
                'snmptrapd': "50050"
            }
        }
    }

    if targetHw in targetData:
        return targetData[targetHw]
    else:
        return -1





def setTargetHwData(targetHw):
    global data

    targetHwData = _setTargetHwData(targetHw)
    if targetHwData == -1:
        hw = targetHw.split('_')[0]
        if (hw == 'qemu' ):
            fileName='%s/%s' %(os.environ.get("HOME"), targetHw)
            if not os.path.isfile(fileName):
                f = open(fileName, 'w')
                f.write(defaultQEmuSettings % targetHw)
                f.close()
                print "\n\n\nPlease update file with correct settings: %s\n\n\n" % fileName
                print "ERROR: " + targetHw + " does not exist"
                return -1
            else:
                fileName='%s/%s' %(os.environ.get("HOME"), targetHw)
                f = open(fileName, 'r')
                fileContent = f.read()
                targetHwData = eval(fileContent)
        else:
            print "ERROR: " + targetHw + " does not exist"
            return -1

    data['physical_size']  = targetHwData['physical_size']
    data['execution_capacity_factor']  = targetHwData['execution_capacity_factor']
    data['watchdog']  = targetHwData['watchdog']
    data['ipAddress']  = targetHwData['ipAddress']
    data['target'] = targetHw
    data['targetType'] = QEMU_TARGET_TYPE
    data['ipAddress']['blades'] = SIMULATOR_TARGET_BLADES
    data['ipAddress']['ipmi'] = SIMULATOR_TARGET

    data['user'] = COTS_TARGET_USER
    data['pwd'] = COTS_TARGET_PWD
    data['terminal_server_user'] = COTS_TERMINAL_SERVER_USER
    data['terminal_server_pwd'] = COTS_TERMINAL_SERVER_PWD
    data['ctrlBladePattern'] = COTS_CTRL_PATTERNS
    data['payloadBladePattern'] = COTS_PL_PATTERNS
    data['hostnameSeparatorPatterns'] = COTS_HOSTNAME_SEPARTOR_PATTERNS
    data['testPcPattern'] = COTS_TEST_PC_PATTERNS
    data['vipTgPattern'] = COTS_VIP_TG_PATTERNS
    data['switchDevicePattern'] = COTS_SWITCH_DEVICE_PATTERNS
    data['snmp'] = COTS_TARGET_SNMP
    data['ports'] =  targetHwData['ports']

    return data

def getTargetHwData():
    return data


#############################################################################################
# Main program - for testing
#############################################################################################
if __name__ == "__main__":
    print setTargetHwData("qemu_target_2plus2")






