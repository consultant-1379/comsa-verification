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
# 'ipAddress'   IP address definitions
#      'ctrl'           Management addresses
#         'NB'                  North bound (official OAM) interface  (ought to be moved out from this file)
#         'ctrl1'               Management address for System Controller 1
#         'ctrl2'               Management address for System Controller 2
#         'ctrl_if'             Management network interface
#         'ctrl_net'            Management IP network
#         'ctrl_gw'             Management routing Gateway IP address
#         'testpc'              Management address of gateway server that also can act as an external traffic host for test application clients and servers
#         'external'            Management addresse(s) of any external hosts for external test application clients and servers
#     'traffic'         Traffic addresses of external servers
#         'gateway_IPv4'        IPv4 traffic addresse(s) of gateway server that also can act as an external traffic host for test application clients and servers
#         'gateway_IPv6'        IPv6 traffic addresse(s) of gateway server that also can act as an external traffic host for test application clients and servers
#         'external_IPv4'       IPv4 traffic addresse(s) of external hosts for external test application clients and servers
#         'external_IPv6'       IPv6 traffic addresse(s) of external hosts for external test application clients and servers
#     'testApp'         Depricated testApp settings only kept for backward compatibility reasons. Don't use these any longer.
#         'test_app'            TestApp server address for incoming external traffic (to PLs)
#         'external_tg'         Management addresses of external hosts for external testApp clients
#         'tg_coord'            TestApp coordinator address to be used from test framework and testApp clients
#     'vip'             VIP addresses and VIP frontend address information
#         'vip_1'               VIP traffic address 1
#         'vip_2'               VIP traffic address 2,
#         'vip_3'               VIP O&M address, can also be used for test application traffic, default source address for outgoing IPv4 traffic
#         'vip_IPv6_traffic'    VIP IPv6 traffic addresses
#         'vip_link_type'       VIP frontend link interface type
#         'vip_link_net'        VIP frontend link ip net
#         'vip_link_addr'       VIP frontend link local address
#         'vip_link_gw'         VIP IPv4 frontend OSPF V2 gateway address
#         'vip_IPv6_link_gw'    VIP IPv6 frontend OSPF V3 gateway address
#
# to be continued ..
#########################################################################

data = {}

### Common COTS data structures ###
COTS_TARGET_TYPE="cots_target"
EBS_TARGET_TYPE="ebs_target"
SIMULATOR_TARGET_TYPE="simulator_target"
VIRTUAL_TARGET_TYPE="vbox_target"

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
SIMULATOR_TARGET_BLADES= { 'blade_2_1'     : "192.168.0.1",
                                         'blade_2_2'    : "192.168.0.2",
                                         'blade_2_3'    : "192.168.0.3",
                                         'blade_2_4'    : "192.168.0.4"
                                         }


SIMULATOR_TARGET = { 'blade_2_1'     : "192.168.73.2",
                                         'blade_2_2'    : "192.168.73.3",
                                         'blade_2_3'    : "192.168.73.4",
                                         'blade_2_4'    : "192.168.73.5"
                                         }

# Only for being backward compatible with the dummy? imports in the TSPSAF3.0 test environment
targetData = -1

def _setTargetHwData(targetHw):

        targetData = {

        # Specific SIMULATOR system information:
        'essim_target' :  {
                'physical_size': "4",
                'execution_capacity_factor': "0.2",
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"192.168.73.12",
                        'ctrl1':"192.168.73.2",
                        'ctrl2' :"192.168.73.3",
                        'testpc':'192.168.73.1'
                },
                'testApp'  : {
                        'test_app'   : '192.168.236.7',
                        'external_tg': 'To be defined later'
                },
                'vip'  : {
                        'vip_gw':  '192.168.73.1',
                        'vip_1'    : '192.168.236.7',
                        'vip_3'    : '192.168.73.7',
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

        # Specific COTS system information:
        'cots_target_4' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.4",
                        'ctrl1':"10.35.26.41",
                        'ctrl2' :"10.35.26.42",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.45',
                        'external':['10.35.26.49'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.45'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fec9:7255'],
                        'external_IPv4':['192.168.15.49'],
                        'external_IPv6':['fd41:4580:3405:15:21b:21ff:fe23:af8d']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.4',
                        'external_tg': ['10.35.26.45','10.35.26.49'],
                        'tg_coord' : '10.35.42.4'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.4',
                        'vip_2'    : '192.168.66.4',
                        'vip_3'    : '10.35.42.4',
                        'vip_IPv4_OAM'     : '10.35.42.4',
                        'vip_IPv4_traffic' : ['172.16.0.4','192.168.66.4'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:4','fd41:4580:3405::2:4'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.24/30','192.168.21.28/30']],[2,['192.168.22.24/30','192.168.22.28/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.26','192.168.21.30']],[2,['192.168.22.26','192.168.22.30']]],
                        'vip_link_gw'      : [[1,['192.168.21.25','192.168.21.29']],[2,['192.168.22.25','192.168.22.29']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'PL_2_5': '7017',
                        'PL_2_6': '7018',
                        'PL_2_7': '7019',
                        'PL_2_8': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.43",
                        'switch_2' : "10.35.26.44",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50004"
                }
        },

        'cots_target_4A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.4",
                        'ctrl1':"10.35.26.41",
                        'ctrl2' :"10.35.26.42",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.45',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.45'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fec9:7255'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.4',
                        'external_tg': ['10.35.26.45'],
                        'tg_coord' : '10.35.42.4'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.4',
                        'vip_2'    : '192.168.66.4',
                        'vip_3'    : '10.35.42.4',
                        'vip_IPv4_OAM'     : '10.35.42.4',
                        'vip_IPv4_traffic' : ['172.16.0.4','192.168.66.4'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:4','fd41:4580:3405::2:4'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.24/30','192.168.21.28/30']],[2,['192.168.22.24/30','192.168.22.28/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.26','192.168.21.30']],[2,['192.168.22.26','192.168.22.30']]],
                        'vip_link_gw'      : [[1,['192.168.21.25','192.168.21.29']],[2,['192.168.22.25','192.168.22.29']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.43",
                        'switch_2' : "10.35.26.44",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50004"
                }
        },

        'cots_target_4B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.104",
                        'ctrl1':"10.35.26.46",
                        'ctrl2' :"10.35.26.47",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.49',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.49'],
                        'gateway_IPv6' :['fd41:4580:3405:15:21b:21ff:fe23:af8d'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.104',
                        'external_tg': ['10.35.26.49'],
                        'tg_coord' : '10.35.42.104'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.104',
                        'vip_2'    : '192.168.66.104',
                        'vip_3'    : '10.35.42.104',
                        'vip_IPv4_OAM'     : '10.35.42.104',
                        'vip_IPv4_traffic' : ['172.16.0.104','192.168.66.104'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:104','fd41:4580:3405::2:104'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.32/30','192.168.21.36/30']],[2,['192.168.22.32/30','192.168.22.36/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.34','192.168.21.38']],[2,['192.168.22.34','192.168.22.38']]],
                        'vip_link_gw'      : [[1,['192.168.21.33','192.168.21.37']],[2,['192.168.22.33','192.168.22.37']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7017',
                        'SC_2_2': '7018',
                        'PL_2_3': '7019',
                        'PL_2_4': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.43",
                        'switch_2' : "10.35.26.44",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50028"
                }
        },

        'cots_target_5' :  {
                'physical_size': "10",
                'execution_capacity_factor': "5.2",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.5",
                        'ctrl1':"10.35.26.51",
                        'ctrl2' :"10.35.26.52",
                        'ctrl_if'  : ['bond_vlan',3],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.55',
                        'external':['10.35.24.101'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.55'],
                        'gateway_IPv6' :['fd41:4580:3405:16:204:23ff:fecb:9f5d'],
                        'external_IPv4':['192.168.16.18'],
                        'external_IPv6':['fd41:4580:3405:16:210:18ff:fe33:1bc']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.5',
                        'external_tg': ['10.35.26.55','10.35.24.101'],
                        'tg_coord' : '10.35.42.5'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.5',
                        'vip_2'    : '192.168.66.5',
                        'vip_3'    : '10.35.42.5',
                        'vip_IPv4_OAM'     : '10.35.42.5',
                        'vip_IPv4_traffic' : ['172.16.0.5','192.168.66.5'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:5','fd41:4580:3405::2:5'],
                        'vip_link_type'    : [[1,'bond_vlan',200],[2,'bond_vlan',201]],
                        'vip_link_net'     : [[1,['192.168.21.32/29']],[2,['192.168.22.32/29']]],
                        'vip_link_addr'    : [[1,['192.168.21.35']],[2,['192.168.22.35']]],
                        'vip_link_gw'      : [[1,['192.168.21.33','192.168.21.34']],[2,['192.168.22.34','192.168.22.33']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::226:CBFF:FE95:BCA8','FE80::225:84FF:FE92:F858']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.5',
                        'SC_2_1': '7019',
                        'SC_2_2': '7020',
                        'PL_2_3': '7021',
                        'PL_2_4': '7022',
                        'switch_1': '7017',
                        'switch_2': '7018'
                },
                'switches' : {
                        'switch_1' : "10.35.26.53",
                        'switch_2' : "10.35.26.54",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,9,10,17,\
                                        18,19,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50005"
                }
        },

        'cots_target_7' :  {
                'physical_size': "10",
                'execution_capacity_factor': "5.2",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.7",
                        'ctrl1':"10.35.26.71",
                        'ctrl2' :"10.35.26.72",
                        'ctrl_if'  : ['bond_vlan',3],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.75',
                        'external':['10.35.24.102'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.75'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fe78:69d'],
                        'external_IPv4':['192.168.16.28'],
                        'external_IPv6':['fd41:4580:3405:16:210:18ff:fe33:3cc']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.7',
                        'external_tg': ['10.35.26.75','10.35.24.102'],
                        'tg_coord' : '10.35.42.7'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.7',
                        'vip_2'    : '192.168.66.7',
                        'vip_3'    : '10.35.42.7',
                        'vip_IPv4_OAM'     : '10.35.42.7',
                        'vip_IPv4_traffic' : ['172.16.0.7','192.168.66.7'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:7','fd41:4580:3405::2:7'],
                        'vip_link_type'    : [[1,'bond_vlan',200],[2,'bond_vlan',201]],
                        'vip_link_net'     : [[1,['192.168.21.48/29']],[2,['192.168.22.48/29']]],
                        'vip_link_addr'    : [[1,['192.168.21.51']],[2,['192.168.22.51']]],
                        'vip_link_gw'      : [[1,['192.168.21.49','192.168.21.50']],[2,['192.168.22.50','192.168.22.49']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::226:CBFF:FE95:BCA8','FE80::225:84FF:FE92:F858']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.5',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'PL_2_5': '7007',
                        'PL_2_6': '7008',
                        'PL_2_7': '7009',
                        'PL_2_8': '7010',
                        'PL_2_9': '7011',
                        'PL_2_10': '7012',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.73",
                        'switch_2' : "10.35.26.74",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,9,10,17,\
                                        18,19,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50007"
                }
        },

        'cots_target_8' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.8",
                        'ctrl1':"10.35.26.81",
                        'ctrl2' :"10.35.26.82",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.85',
                        'external':['10.35.26.89'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',           'PL_2_4': '7006',
                        'switch_1': '7001',

                        'gateway_IPv4' :['192.168.15.85'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fecb:b7f5'],
                        'external_IPv4':['192.168.15.89'],
                        'external_IPv6':['fd41:4580:3405:15:204:23ff:fede:b15b']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.8',
                        'external_tg': ['10.35.26.85','10.35.26.89'],
                        'tg_coord' : '10.35.42.8'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.8',
                        'vip_2'    : '192.168.66.8',
                        'vip_3'    : '10.35.42.8',
                        'vip_IPv4_OAM'     : '10.35.42.8',
                        'vip_IPv4_traffic' : ['172.16.0.8','192.168.66.8'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:8','fd41:4580:3405::2:8'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.56/30','192.168.21.60/30']],[2,['192.168.22.56/30','192.168.22.60/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.58','192.168.21.62']],[2,['192.168.22.58','192.168.22.62']]],
                        'vip_link_gw'      : [[1,['192.168.21.57','192.168.21.61']],[2,['192.168.22.57','192.168.22.61']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'PL_2_5': '7007',
                        'PL_2_6': '7008',
                        'PL_2_7': '7009',
                        'PL_2_8': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.83",
                        'switch_2' : "10.35.26.84",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50008"
                }
        },

        'cots_target_8A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.8",
                        'ctrl1':"10.35.26.81",
                        'ctrl2' :"10.35.26.82",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.85',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.85'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fecb:b7f5'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.8',
                        'external_tg': ['10.35.26.85'],
                        'tg_coord' : '10.35.42.8'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.8',
                        'vip_2'    : '192.168.66.8',
                        'vip_3'    : '10.35.42.8',
                        'vip_IPv4_OAM'     : '10.35.42.8',
                        'vip_IPv4_traffic' : ['172.16.0.8','192.168.66.8'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:8','fd41:4580:3405::2:8'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.56/30','192.168.21.60/30']],[2,['192.168.22.56/30','192.168.22.60/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.58','192.168.21.62']],[2,['192.168.22.58','192.168.22.62']]],
                        'vip_link_gw'      : [[1,['192.168.21.57','192.168.21.61']],[2,['192.168.22.57','192.168.22.61']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.83",
                        'switch_2' : "10.35.26.84",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50008"
                }
        },

        'cots_target_8B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.108",
                        'ctrl1':"10.35.26.86",
                        'ctrl2' :"10.35.26.87",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.89',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.89'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fede:b15b'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.108',
                        'external_tg': ['10.35.26.89'],
                        'tg_coord' : '10.35.42.108'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.108',
                        'vip_2'    : '192.168.66.108',
                        'vip_3'    : '10.35.42.108',
                        'vip_IPv4_OAM'     : '10.35.42.108',
                        'vip_IPv4_traffic' : ['172.16.0.108','192.168.66.108'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:108','fd41:4580:3405::2:108'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.64/30','192.168.21.68/30']],[2,['192.168.22.64/30','192.168.22.68/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.66','192.168.21.70']],[2,['192.168.22.66','192.168.22.70']]],
                        'vip_link_gw'      : [[1,['192.168.21.65','192.168.21.69']],[2,['192.168.22.65','192.168.22.69']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7007',
                        'SC_2_2': '7008',
                        'PL_2_3': '7009',
                        'PL_2_4': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.83",
                        'switch_2' : "10.35.26.84",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50032"
                }
        },

        'cots_target_10' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.10",
                        'ctrl1' : "10.35.26.101",
                        'ctrl2' : "10.35.26.102",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc': '10.35.26.105',
                        'external':['10.35.26.109'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.105'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe8b:14cb'],
                        'external_IPv4':['192.168.15.109'],
                        'external_IPv6':['fd41:4580:3405:15:21b:21ff:fe23:508b']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.10',
                        'external_tg': ['10.35.26.105','10.35.26.109'],
                        'tg_coord' : '10.35.42.10'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.10',
                        'vip_2'    : '192.168.66.10',
                        'vip_3'    : '10.35.42.10',
                        'vip_IPv4_OAM'     : '10.35.42.10',
                        'vip_IPv4_traffic' : ['172.16.0.10','192.168.66.10'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:10','fd41:4580:3405::2:10'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.72/30','192.168.21.76/30']],[2,['192.168.22.72/30','192.168.22.76/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.74','192.168.21.78']],[2,['192.168.22.74','192.168.22.78']]],
                        'vip_link_gw'      : [[1,['192.168.21.73','192.168.21.77']],[2,['192.168.22.73','192.168.22.77']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'PL_2_5': '7007',
                        'PL_2_6': '7008',
                        'PL_2_7': '7009',
                        'PL_2_8': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.103",
                        'switch_2' : "10.35.26.104",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50010"
                }
        },

        'cots_target_10A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.10",
                        'ctrl1' : "10.35.26.101",
                        'ctrl2' : "10.35.26.102",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc': '10.35.26.105',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.105'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe8b:14cb'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.10',
                        'external_tg': ['10.35.26.105'],
                        'tg_coord' : '10.35.42.10'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.10',
                        'vip_2'    : '192.168.66.10',
                        'vip_3'    : '10.35.42.10',
                        'vip_IPv4_OAM'     : '10.35.42.10',
                        'vip_IPv4_traffic' : ['172.16.0.10','192.168.66.10'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:10','fd41:4580:3405::2:10'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.72/30','192.168.21.76/30']],[2,['192.168.22.72/30','192.168.22.76/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.74','192.168.21.78']],[2,['192.168.22.74','192.168.22.78']]],
                        'vip_link_gw'      : [[1,['192.168.21.73','192.168.21.77']],[2,['192.168.22.73','192.168.22.77']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.103",
                        'switch_2' : "10.35.26.104",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50010"
                }
        },

        'cots_target_10B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.110",
                        'ctrl1' : "10.35.26.106",
                        'ctrl2' : "10.35.26.107",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc': '10.35.26.109',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.109'],
                        'gateway_IPv6' :['fd41:4580:3405:15:21b:21ff:fe23:508b'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.110',
                        'external_tg': ['10.35.26.109'],
                        'tg_coord' : '10.35.42.110'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.110',
                        'vip_2'    : '192.168.66.110',
                        'vip_3'    : '10.35.42.110',
                        'vip_IPv4_OAM'     : '10.35.42.110',
                        'vip_IPv4_traffic' : ['172.16.0.110','192.168.66.110'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:110','fd41:4580:3405::2:110'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.80/30','192.168.21.84/30']],[2,['192.168.22.80/30','192.168.22.84/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.82','192.168.21.86']],[2,['192.168.22.82','192.168.22.86']]],
                        'vip_link_gw'      : [[1,['192.168.21.81','192.168.21.85']],[2,['192.168.22.81','192.168.22.85']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7007',
                        'SC_2_2': '7008',
                        'PL_2_3': '7009',
                        'PL_2_4': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.103",
                        'switch_2' : "10.35.26.104",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50034"
                }
        },

        'cots_target_11' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.11",
                        'ctrl1':"10.35.26.111",
                        'ctrl2' :"10.35.26.112",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.115',
                        'external':['10.35.26.119'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.115'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fe8b:2213'],
                        'external_IPv4':['192.168.16.119'],
                        'external_IPv6':['fd41:4580:3405:16:204:23ff:fed2:50c3']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.11',
                        'external_tg': ['10.35.26.115','10.35.26.119'],
                        'tg_coord' : '10.35.42.11'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.11',
                        'vip_2'    : '192.168.66.11',
                        'vip_3'    : '10.35.42.11',
                        'vip_IPv4_OAM'     : '10.35.42.11',
                        'vip_IPv4_traffic' : ['172.16.0.11','192.168.66.11'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:11','fd41:4580:3405::2:11'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.80/30','192.168.21.84/30']],[2,['192.168.22.80/30','192.168.22.84/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.82','192.168.21.86']],[2,['192.168.22.82','192.168.22.86']]],
                        'vip_link_gw'      : [[1,['192.168.21.81','192.168.21.85']],[2,['192.168.22.81','192.168.22.85']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.5',
                        'SC_2_1': '7025',
                        'SC_2_2': '7026',
                        'PL_2_3': '7027',
                        'PL_2_4': '7028',
                        'PL_2_5': '7029',
                        'PL_2_6': '7030',
                        'PL_2_7': '7031',
                        'PL_2_8': '7032',
                        'switch_1': '7023',
                        'switch_2': '7024'
                },
                'switches' : {
                        'switch_1' : "10.35.26.113",
                        'switch_2' : "10.35.26.114",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50011"
                }
        },

        'cots_target_11A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.11",
                        'ctrl1':"10.35.26.111",
                        'ctrl2' :"10.35.26.112",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.115',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.115'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fe8b:2213'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.11',
                        'external_tg': ['10.35.26.115'],
                        'tg_coord' : '10.35.42.11'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.11',
                        'vip_2'    : '192.168.66.11',
                        'vip_3'    : '10.35.42.11',
                        'vip_IPv4_OAM'     : '10.35.42.11',
                        'vip_IPv4_traffic' : ['172.16.0.11','192.168.66.11'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:11','fd41:4580:3405::2:11'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.80/30','192.168.21.84/30']],[2,['192.168.22.80/30','192.168.22.84/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.82','192.168.21.86']],[2,['192.168.22.82','192.168.22.86']]],
                        'vip_link_gw'      : [[1,['192.168.21.81','192.168.21.85']],[2,['192.168.22.81','192.168.22.85']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.5',
                        'SC_2_1': '7025',
                        'SC_2_2': '7026',
                        'PL_2_3': '7027',
                        'PL_2_4': '7028',
                        'switch_1': '7023',
                        'switch_2': '7024'
                },
                'switches' : {
                        'switch_1' : "10.35.26.113",
                        'switch_2' : "10.35.26.114",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50011"
                }
        },

        'cots_target_11B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.111",
                        'ctrl1':"10.35.26.116",
                        'ctrl2' :"10.35.26.117",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.119',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.119'],
                        'gateway_IPv6' :['fd41:4580:3405:16:204:23ff:fed2:50c3'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.111',
                        'external_tg': ['10.35.26.119'],
                        'tg_coord' : '10.35.42.111'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.111',
                        'vip_2'    : '192.168.66.111',
                        'vip_3'    : '10.35.42.111',
                        'vip_IPv4_OAM'     : '10.35.42.111',
                        'vip_IPv4_traffic' : ['172.16.0.111','192.168.66.111'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:111','fd41:4580:3405::2:111'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.88/30','192.168.21.92/30']],[2,['192.168.22.88/30','192.168.22.92/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.90','192.168.21.94']],[2,['192.168.22.90','192.168.22.94']]],
                        'vip_link_gw'      : [[1,['192.168.21.89','192.168.21.93']],[2,['192.168.22.89','192.168.22.93']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.5',
                        'SC_2_1': '7029',
                        'SC_2_2': '7030',
                        'PL_2_3': '7031',
                        'PL_2_4': '7032',
                        'switch_1': '7023',
                        'switch_2': '7024'
                },
                'switches' : {
                        'switch_1' : "10.35.26.113",
                        'switch_2' : "10.35.26.114",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50035"
                }
        }
        }


        if targetHw in targetData:
                return targetData[targetHw]
        else:
                return -1


def _setTargetHwData2(targetHw):

        targetData2 = {

        'cots_target_14' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.141",
                        'ctrl2' :"10.35.26.142",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.145',
                        'external':['10.35.26.149'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.145'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe91:790f'],
                        'external_IPv4':['192.168.15.149'],
                        'external_IPv6':['fd41:4580:3405:15:215:17ff:fea6:e3fd']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.14',
                        'vip_IPv4_traffic' : ['172.16.0.14','192.168.66.14'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:14','fd41:4580:3405::2:14'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.104/30','192.168.21.108/30']],[2,['192.168.22.104/30','192.168.22.108/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.106','192.168.21.110']],[2,['192.168.22.106','192.168.22.110']]],
                        'vip_link_gw'      : [[1,['192.168.21.105','192.168.21.109']],[2,['192.168.22.105','192.168.22.109']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'PL_2_5': '7007',
                        'PL_2_6': '7008',
                        'PL_2_7': '7009',
                        'PL_2_8': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.143",
                        'switch_2' : "10.35.26.144",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50014"
                }
        },

        'cots_target_14A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.141",
                        'ctrl2' :"10.35.26.142",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.145',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.145'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe91:790f'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.14',
                        'vip_IPv4_traffic' : ['172.16.0.14','192.168.66.14'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:14','fd41:4580:3405::2:14'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.104/30','192.168.21.108/30']],[2,['192.168.22.104/30','192.168.22.108/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.106','192.168.21.110']],[2,['192.168.22.106','192.168.22.110']]],
                        'vip_link_gw'      : [[1,['192.168.21.105','192.168.21.109']],[2,['192.168.22.105','192.168.22.109']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.143",
                        'switch_2' : "10.35.26.144",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50014"
                }
        },

        'cots_target_14B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.146",
                        'ctrl2' :"10.35.26.147",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.149',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.149'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fea6:e3fd'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.114',
                        'vip_IPv4_traffic' : ['172.16.0.114','192.168.66.114'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:114','fd41:4580:3405::2:114'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.112/30','192.168.21.116/30']],[2,['192.168.22.112/30','192.168.22.116/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.114','192.168.21.118']],[2,['192.168.22.114','192.168.22.118']]],
                        'vip_link_gw'      : [[1,['192.168.21.113','192.168.21.117']],[2,['192.168.22.113','192.168.22.117']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7007',
                        'SC_2_2': '7008',
                        'PL_2_3': '7009',
                        'PL_2_4': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.143",
                        'switch_2' : "10.35.26.144",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50038"
                }
        },

        'hp_target_15' : {
                'physical_size': "10",
                'execution_capacity_factor': "2",
                'watchdog' : 'soft',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.151",
                        'ctrl2' :"10.35.26.152",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.155',
                        'external':['10.35.26.159','10.35.24.103'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.1.0',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.155'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:febf:7f3c'],
                        'external_IPv4':['192.168.16.159','192.168.16.38'],
                        'external_IPv6':['fd41:4580:3405:16:21b:21ff:fe9f:263c','fd41:4580:3405:16:210:18ff:fe33:3af']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.15',
                        'vip_IPv4_traffic' : ['172.16.0.15','192.168.66.15'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:15','fd41:4580:3405::2:15'],
                        'vip_link_type'    : [[1,'eth',2,3,4],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.112/30','192.168.21.116/30','192.168.20.112/30']],[2,['192.168.22.112/30','192.168.22.116/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.114','192.168.21.118','192.168.20.114']],[2,['192.168.22.114','192.168.22.118']]],
                        'vip_link_gw'      : [[1,['192.168.21.113','192.168.21.117','192.168.20.113']],[2,['192.168.22.113','192.168.22.117']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8','FE80::021B:21FF:FE59:5344']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.250',
                        'SC_2_1': '7001',
                        'SC_2_2': '7002',
                        'PL_2_3': '7003',
                        'PL_2_4': '7004',
                        'PL_2_5': '7005',
                        'PL_2_6': '7006',
                        'PL_2_7': '7007',
                        'PL_2_8': '7008',
                        'PL_2_9': '7009',
                        'PL_2_10':'7010',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.153",
                        'switch_2' : "10.35.26.154",
                        'portsInOrder' : [5,6,7,8,9,10,11,12,13,14,\
                                        1,2,3,4]
                }
                },
        'ports' : {
                'snmptrapd': "50015"
                }
        },

        'hp_target_15A' : {
                'physical_size': "5",
                'execution_capacity_factor': "2",
                'watchdog' : 'soft',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.151",
                        'ctrl2' :"10.35.26.152",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.155',
                        'external':['10.35.24.103'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.1.0',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.155'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:febf:7f3c'],
                        'external_IPv4':['192.168.16.38'],
                        'external_IPv6':['fd41:4580:3405:16:210:18ff:fe33:3af']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.15',
                        'vip_IPv4_traffic' : ['172.16.0.15','192.168.66.15'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:15','fd41:4580:3405::2:15'],
                        'vip_link_type'    : [[1,'eth',2,3,4],[2,'eth',2,3],[3,'eth',2,3],[4,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.112/30','192.168.21.116/30','192.168.20.112/30']],[2,['192.168.22.112/30','192.168.22.116/30']],
                                              [3,['192.168.23.112/30','192.168.23.116/30']],[4,['192.168.24.112/30','192.168.24.116/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.114','192.168.21.118','192.168.20.114']],[2,['192.168.22.114','192.168.22.118']],
                                              [3,['192.168.23.114','192.168.23.118']],[4,['192.168.24.114','192.168.24.118']]],
                        'vip_link_gw'      : [[1,['192.168.21.113','192.168.21.117','192.168.20.113']],[2,['192.168.22.113','192.168.22.117']],[3,[]],[4,[]]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8','FE80::021B:21FF:FE59:5344']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],[3,[]],[4,[]]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.250',
                        'SC_2_1': '7001',
                        'SC_2_2': '7002',
                        'PL_2_3': '7003',
                        'PL_2_4': '7004',
                        'PL_2_5': '7005',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.153",
                        'switch_2' : "10.35.26.154",
                        'portsInOrder' : [5,6,7,8,9,\
                                        1,2]
                }
                },
        'ports' : {
                'snmptrapd': "50015"
                }
        },

        'hp_target_15B' : {
                'physical_size': "5",
                'execution_capacity_factor': "2",
                'watchdog' : 'soft',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.156",
                        'ctrl2' :"10.35.26.157",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.159',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.1.5',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.159'],
                        'gateway_IPv6' :['fd41:4580:3405:16:21b:21ff:fe9f:263c'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.115',
                        'vip_IPv4_traffic' : ['172.16.0.115','192.168.66.115'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:115','fd41:4580:3405::2:115'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.120/30','192.168.21.124/30']],[2,['192.168.22.120/30','192.168.22.124/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.122','192.168.21.126']],[2,['192.168.22.122','192.168.22.126']]],
                        'vip_link_gw'      : [[1,['192.168.21.121','192.168.21.125']],[2,['192.168.22.121','192.168.22.125']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.250',
                        'SC_2_1': '7006',
                        'SC_2_2': '7007',
                        'PL_2_3': '7008',
                        'PL_2_4': '7009',
                        'PL_2_5': '7010',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.153",
                        'switch_2' : "10.35.26.154",
                        'portsInOrder' : [10,11,12,13,14,\
                                        3]
                }
                },
        'ports' : {
                'snmptrapd': "50039"
                }
        },

        'cots_target_16' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.161",
                        'ctrl2' :"10.35.26.162",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.165',
                        'external':['10.35.26.169'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.165'],
                        'gateway_IPv6' :['fd41:4580:3405:15:21b:21ff:fe9f:fd99'],
                        'external_IPv4':['192.168.15.169'],
                        'external_IPv6':['fd41:4580:3405:15:21b:21ff:fe9c:9861']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.16',
                        'vip_IPv4_traffic' : ['172.16.0.16','192.168.66.16'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:16','fd41:4580:3405::2:16'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.120/30','192.168.21.124/30']],[2,['192.168.22.120/30','192.168.22.124/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.122','192.168.21.126']],[2,['192.168.22.122','192.168.22.126']]],
                        'vip_link_gw'      : [[1,['192.168.21.121','192.168.21.125']],[2,['192.168.22.121','192.168.22.125']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'PL_2_5': '7017',
                        'PL_2_6': '7018',
                        'PL_2_7': '7019',
                        'PL_2_8': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.163",
                        'switch_2' : "10.35.26.164",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50016"
                }
        },

        'cots_target_16A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.161",
                        'ctrl2' :"10.35.26.162",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.165',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.165'],
                        'gateway_IPv6' :['fd41:4580:3405:15:21b:21ff:fe9f:fd99'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.16',
                        'vip_IPv4_traffic' : ['172.16.0.16','192.168.66.16'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:16','fd41:4580:3405::2:16'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.120/30','192.168.21.124/30']],[2,['192.168.22.120/30','192.168.22.124/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.122','192.168.21.126']],[2,['192.168.22.122','192.168.22.126']]],
                        'vip_link_gw'      : [[1,['192.168.21.121','192.168.21.125']],[2,['192.168.22.121','192.168.22.125']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.163",
                        'switch_2' : "10.35.26.164",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50016"
                }
        },

        'cots_target_16B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.166",
                        'ctrl2' :"10.35.26.167",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.169',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.169'],
                        'gateway_IPv6' :['fd41:4580:3405:15:21b:21ff:fe9c:9861'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.116',
                        'vip_IPv4_traffic' : ['172.16.0.116','192.168.66.116'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:116','fd41:4580:3405::2:116'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.128/30','192.168.21.132/30']],[2,['192.168.22.128/30','192.168.22.132/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.130','192.168.21.134']],[2,['192.168.22.130','192.168.22.134']]],
                        'vip_link_gw'      : [[1,['192.168.21.129','192.168.21.133']],[2,['192.168.22.129','192.168.22.133']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7017',
                        'SC_2_2': '7018',
                        'PL_2_3': '7019',
                        'PL_2_4': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.163",
                        'switch_2' : "10.35.26.164",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50040"
                }
        },

        'cots_target_18' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.181",
                        'ctrl2' :"10.35.26.182",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.185',
                        'external':['10.35.26.189'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.185'],
                        'gateway_IPv6' :['fd41:4580:3405:15:0215:17FF:FE91:78c7'],
                        'external_IPv4':['192.168.15.189'],
                        'external_IPv6':['fd41:4580:3405:15:021b:21FF:FE9c:97dd']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.18',
                        'vip_IPv4_traffic' : ['172.16.0.18','192.168.66.18'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:18','fd41:4580:3405::2:18'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.136/30','192.168.21.140/30']],[2,['192.168.22.136/30','192.168.22.140/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.138','192.168.21.142']],[2,['192.168.22.138','192.168.22.142']]],
                        'vip_link_gw'      : [[1,['192.168.21.137','192.168.21.141']],[2,['192.168.22.137','192.168.22.141']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7023',
                        'SC_2_2': '7024',
                        'PL_2_3': '7025',
                        'PL_2_4': '7026',
                        'PL_2_5': '7027',
                        'PL_2_6': '7028',
                        'PL_2_7': '7029',
                        'PL_2_8': '7030',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.183",
                        'switch_2' : "10.35.26.184",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50018"
                }
        },

        'cots_target_18A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.181",
                        'ctrl2' :"10.35.26.182",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.185',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.185'],
                        'gateway_IPv6' :['fd41:4580:3405:15:0215:17FF:FE91:78c7'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.18',
                        'vip_IPv4_traffic' : ['172.16.0.18','192.168.66.18'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:18','fd41:4580:3405::2:18'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.136/30','192.168.21.140/30']],[2,['192.168.22.136/30','192.168.22.140/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.138','192.168.21.142']],[2,['192.168.22.138','192.168.22.142']]],
                        'vip_link_gw'      : [[1,['192.168.21.137','192.168.21.141']],[2,['192.168.22.137','192.168.22.141']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7023',
                        'SC_2_2': '7024',
                        'PL_2_3': '7025',
                        'PL_2_4': '7026',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.183",
                        'switch_2' : "10.35.26.184",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50018"
                }
        },

        'cots_target_18B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.26.186",
                        'ctrl2' :"10.35.26.187",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.189',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.189'],
                        'gateway_IPv6' :['fd41:4580:3405:15:021b:21FF:FE9c:97dd'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.118',
                        'vip_IPv4_traffic' : ['172.16.0.118','192.168.66.118'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:118','fd41:4580:3405::2:118'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.144/30','192.168.21.148/30']],[2,['192.168.22.144/30','192.168.22.148/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.146','192.168.21.150']],[2,['192.168.22.146','192.168.22.150']]],
                        'vip_link_gw'      : [[1,['192.168.21.145','192.168.21.149']],[2,['192.168.22.145','192.168.22.149']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.2',
                        'SC_2_1': '7027',
                        'SC_2_2': '7028',
                        'PL_2_3': '7029',
                        'PL_2_4': '7030',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.183",
                        'switch_2' : "10.35.26.184",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50042"
                }
        },

        'cots_target_19' : {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.19",
                        'ctrl1':"10.35.26.191",
                        'ctrl2' :"10.35.26.192",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.195',
                        'external':['10.35.26.199'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.195'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fe91:792f'],
                        'external_IPv4':['192.168.16.199'],
                        'external_IPv6':['fd41:4580:3405:16:204.23ff.fece.86ed']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.19',
                        'external_tg': ['10.35.26.195','10.35.26.199'],
                        'tg_coord' : '10.35.42.19'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.19',
                        'vip_2'    : '192.168.66.19',
                        'vip_3'    : '10.35.42.19',
                        'vip_IPv4_OAM'     : '10.35.42.19',
                        'vip_IPv4_traffic' : ['172.16.0.19','192.168.66.19'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:19','fd41:4580:3405::2:19'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.144/30','192.168.21.148/30']],[2,['192.168.22.144/30','192.168.22.148/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.146','192.168.21.150']],[2,['192.168.22.146','192.168.22.150']]],
                        'vip_link_gw'      : [[1,['192.168.21.145','192.168.21.149']],[2,['192.168.22.145','192.168.22.149']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'PL_2_5': '7007',
                        'PL_2_6': '7008',
                        'PL_2_7': '7009',
                        'PL_2_8': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.193",
                        'switch_2' : "10.35.26.194",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50019"
                }
        },

        'cots_target_19A' : {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.19",
                        'ctrl1':"10.35.26.191",
                        'ctrl2' :"10.35.26.192",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.195',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.195'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fe91:792f'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.19',
                        'external_tg': ['10.35.26.195'],
                        'tg_coord' : '10.35.42.19'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.19',
                        'vip_2'    : '192.168.66.19',
                        'vip_3'    : '10.35.42.19',
                        'vip_IPv4_OAM'     : '10.35.42.19',
                        'vip_IPv4_traffic' : ['172.16.0.19','192.168.66.19'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:19','fd41:4580:3405::2:19'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.144/30','192.168.21.148/30']],[2,['192.168.22.144/30','192.168.22.148/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.146','192.168.21.150']],[2,['192.168.22.146','192.168.22.150']]],
                        'vip_link_gw'      : [[1,['192.168.21.145','192.168.21.149']],[2,['192.168.22.145','192.168.22.149']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.193",
                        'switch_2' : "10.35.26.194",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50019"
                }
        },

        'cots_target_19B' : {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.119",
                        'ctrl1':"10.35.26.196",
                        'ctrl2' :"10.35.26.197",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.199',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.199'],
                        'gateway_IPv6' :['fd41:4580:3405:16:204.23ff.fece.86ed'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.119',
                        'external_tg': ['10.35.26.199'],
                        'tg_coord' : '10.35.42.119'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.119',
                        'vip_2'    : '192.168.66.119',
                        'vip_3'    : '10.35.42.119',
                        'vip_IPv4_OAM'     : '10.35.42.119',
                        'vip_IPv4_traffic' : ['172.16.0.119','192.168.66.119'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:119','fd41:4580:3405::2:119'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.152/30','192.168.21.156/30']],[2,['192.168.22.152/30','192.168.22.156/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.154','192.168.21.158']],[2,['192.168.22.154','192.168.22.158']]],
                        'vip_link_gw'      : [[1,['192.168.21.153','192.168.21.157']],[2,['192.168.22.153','192.168.22.157']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7007',
                        'SC_2_2': '7008',
                        'PL_2_3': '7009',
                        'PL_2_4': '7010',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.193",
                        'switch_2' : "10.35.26.194",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50043"
                }
        }
        }

        if targetHw in targetData2:
                return targetData2[targetHw]
        else:
                return -1


def _setTargetHwData3(targetHw):

        targetData3 = {

        'cots_target_20' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.20",
                        'ctrl1':"10.35.26.201",
                        'ctrl2' :"10.35.26.202",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.205',
                        'external':['10.35.26.209'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.205'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fec5:d403'],
                        'external_IPv4':['192.168.15.209'],
                        'external_IPv6':['fd41:4580:3405:15:204:23ff:fed5:5419']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.20',
                        'external_tg': ['10.35.26.205','10.35.26.209'],
                        'tg_coord' : '10.35.42.20'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.20',
                        'vip_2'    : '192.168.66.20',
                        'vip_3'    : '10.35.42.20',
                        'vip_IPv4_OAM'     : '10.35.42.20',
                        'vip_IPv4_traffic' : ['172.16.0.20','192.168.66.20'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:20','fd41:4580:3405::2:20'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.152/30','192.168.21.156/30']],[2,['192.168.22.152/30','192.168.22.156/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.154','192.168.21.158']],[2,['192.168.22.154','192.168.22.158']]],
                        'vip_link_gw'      : [[1,['192.168.21.153','192.168.21.157']],[2,['192.168.22.153','192.168.22.157']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7021',
                        'SC_2_2': '7022',
                        'PL_2_3': '7023',
                        'PL_2_4': '7024',
                        'PL_2_5': '7025',
                        'PL_2_6': '7026',
                        'PL_2_7': '7027',
                        'PL_2_8': '7028',
                        'switch_1': '7029',
                        'switch_2': '7030'
                },
                'switches' : {
                        'switch_1' : "10.35.26.203",
                        'switch_2' : "10.35.26.204",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50020"
                }
        },

        'cots_target_20A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.20",
                        'ctrl1':"10.35.26.201",
                        'ctrl2' :"10.35.26.202",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.205',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.205'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fec5:d403'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.20',
                        'external_tg': ['10.35.26.205'],
                        'tg_coord' : '10.35.42.20'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.20',
                        'vip_2'    : '192.168.66.20',
                        'vip_3'    : '10.35.42.20',
                        'vip_IPv4_OAM'     : '10.35.42.20',
                        'vip_IPv4_traffic' : ['172.16.0.20','192.168.66.20'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:20','fd41:4580:3405::2:20'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.152/30','192.168.21.156/30']],[2,['192.168.22.152/30','192.168.22.156/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.154','192.168.21.158']],[2,['192.168.22.154','192.168.22.158']]],
                        'vip_link_gw'      : [[1,['192.168.21.153','192.168.21.157']],[2,['192.168.22.153','192.168.22.157']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7021',
                        'SC_2_2': '7022',
                        'PL_2_3': '7023',
                        'PL_2_4': '7024',
                        'switch_1': '7029',
                        'switch_2': '7030'
                },
                'switches' : {
                        'switch_1' : "10.35.26.203",
                        'switch_2' : "10.35.26.204",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50020"
                }
        },

        'cots_target_20B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.120",
                        'ctrl1':"10.35.26.206",
                        'ctrl2' :"10.35.26.207",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.209',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.209'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fed5:5419'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.120',
                        'external_tg': ['10.35.26.209'],
                        'tg_coord' : '10.35.42.120'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.120',
                        'vip_2'    : '192.168.66.120',
                        'vip_3'    : '10.35.42.120',
                        'vip_IPv4_OAM'     : '10.35.42.120',
                        'vip_IPv4_traffic' : ['172.16.0.120','192.168.66.120'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:120','fd41:4580:3405::2:120'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.160/30','192.168.21.164/30']],[2,['192.168.22.160/30','192.168.22.164/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.162','192.168.21.166']],[2,['192.168.22.162','192.168.22.166']]],
                        'vip_link_gw'      : [[1,['192.168.21.161','192.168.21.165']],[2,['192.168.22.161','192.168.22.165']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.4',
                        'SC_2_1': '7025',
                        'SC_2_2': '7026',
                        'PL_2_3': '7027',
                        'PL_2_4': '7028',
                        'switch_1': '7029',
                        'switch_2': '7030'
                },
                'switches' : {
                        'switch_1' : "10.35.26.203",
                        'switch_2' : "10.35.26.204",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50044"
                }
        },

        'cots_target_21' : {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.21",
                        'ctrl1':"10.35.26.211",
                        'ctrl2' :"10.35.26.212",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.215',
                        'external':['10.35.26.219'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.215'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fe91:7925'],
                        'external_IPv4':['192.168.16.219'],
                        'external_IPv6':['fd41:4580:3405:16:204:23ff:fec9:6e4d']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.21',
                        'external_tg': ['10.35.26.215','10.35.26.219'],
                        'tg_coord' : '10.35.42.21'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.21',
                        'vip_2'    : '192.168.66.21',
                        'vip_3'    : '10.35.42.21',
                        'vip_IPv4_OAM'     : '10.35.42.21',
                        'vip_IPv4_traffic' : ['172.16.0.21','192.168.66.21'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:21','fd41:4580:3405::2:21'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.160/30','192.168.21.164/30']],[2,['192.168.22.160/30','192.168.22.164/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.162','192.168.21.166']],[2,['192.168.22.162','192.168.22.166']]],
                        'vip_link_gw'      : [[1,['192.168.21.161','192.168.21.165']],[2,['192.168.22.161','192.168.22.165']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'PL_2_5': '7017',
                        'PL_2_6': '7018',
                        'PL_2_7': '7019',
                        'PL_2_8': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.213",
                        'switch_2' : "10.35.26.214",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50021"
                }
        },

        'cots_target_21A' : {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.21",
                        'ctrl1':"10.35.26.211",
                        'ctrl2' :"10.35.26.212",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.215',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.215'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fe91:7925'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.21',
                        'external_tg': ['10.35.26.215'],
                        'tg_coord' : '10.35.42.21'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.21',
                        'vip_2'    : '192.168.66.21',
                        'vip_3'    : '10.35.42.21',
                        'vip_IPv4_OAM'     : '10.35.42.21',
                        'vip_IPv4_traffic' : ['172.16.0.21','192.168.66.21'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:21','fd41:4580:3405::2:21'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.160/30','192.168.21.164/30']],[2,['192.168.22.160/30','192.168.22.164/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.162','192.168.21.166']],[2,['192.168.22.162','192.168.22.166']]],
                        'vip_link_gw'      : [[1,['192.168.21.161','192.168.21.165']],[2,['192.168.22.161','192.168.22.165']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.213",
                        'switch_2' : "10.35.26.214",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50021"
                }
        },

        'cots_target_21B' : {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.121",
                        'ctrl1':"10.35.26.216",
                        'ctrl2' :"10.35.26.217",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.219',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.219'],
                        'gateway_IPv6' :['fd41:4580:3405:16:204:23ff:fec9:6e4d'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.121',
                        'external_tg': ['10.35.26.219'],
                        'tg_coord' : '10.35.42.121'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.121',
                        'vip_2'    : '192.168.66.121',
                        'vip_3'    : '10.35.42.121',
                        'vip_IPv4_OAM'     : '10.35.42.121',
                        'vip_IPv4_traffic' : ['172.16.0.121','192.168.66.121'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:121','fd41:4580:3405::2:121'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.168/30','192.168.21.172/30']],[2,['192.168.22.168/30','192.168.22.172/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.170','192.168.21.174']],[2,['192.168.22.170','192.168.22.174']]],
                        'vip_link_gw'      : [[1,['192.168.21.169','192.168.21.173']],[2,['192.168.22.169','192.168.22.173']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7017',
                        'SC_2_2': '7018',
                        'PL_2_3': '7019',
                        'PL_2_4': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.213",
                        'switch_2' : "10.35.26.214",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50045"
                }
        },

        'cots_target_22' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.22",
                        'ctrl1':"10.35.26.221",
                        'ctrl2' :"10.35.26.222",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.225',
                        'external':['10.35.26.229'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.225'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe8e:eb9f'],
                        'external_IPv4':['192.168.15.229'],
                        'external_IPv6':['fd41:4580:3405:15:204:23ff:fec5:d7d3']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.22',
                        'external_tg': ['10.35.26.225','10.35.26.229'],
                        'tg_coord' : '10.35.42.22'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.22',
                        'vip_2'    : '192.168.66.22',
                        'vip_3'    : '10.35.42.22',
                        'vip_IPv4_OAM'     : '10.35.42.22',
                        'vip_IPv4_traffic' : ['172.16.0.22','192.168.66.22'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:22','fd41:4580:3405::2:22'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.168/30','192.168.21.172/30']],[2,['192.168.22.168/30','192.168.22.172/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.170','192.168.21.174']],[2,['192.168.22.170','192.168.22.174']]],
                        'vip_link_gw'      : [[1,['192.168.21.169','192.168.21.173']],[2,['192.168.22.169','192.168.22.173']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'PL_2_5': '7017',
                        'PL_2_6': '7018',
                        'PL_2_7': '7019',
                        'PL_2_8': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.223",
                        'switch_2' : "10.35.26.224",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50022"
                }
        },

        'cots_target_22A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.22",
                        'ctrl1':"10.35.26.221",
                        'ctrl2' :"10.35.26.222",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.225',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.225'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe8e:eb9f'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.22',
                        'external_tg': ['10.35.26.225'],
                        'tg_coord' : '10.35.42.22'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.22',
                        'vip_2'    : '192.168.66.22',
                        'vip_3'    : '10.35.42.22',
                        'vip_IPv4_OAM'     : '10.35.42.22',
                        'vip_IPv4_traffic' : ['172.16.0.22','192.168.66.22'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:22','fd41:4580:3405::2:22'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.168/30','192.168.21.172/30']],[2,['192.168.22.168/30','192.168.22.172/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.170','192.168.21.174']],[2,['192.168.22.170','192.168.22.174']]],
                        'vip_link_gw'      : [[1,['192.168.21.169','192.168.21.173']],[2,['192.168.22.169','192.168.22.173']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7013',
                        'SC_2_2': '7014',
                        'PL_2_3': '7015',
                        'PL_2_4': '7016',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.223",
                        'switch_2' : "10.35.26.224",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50022"
                }
        },

        'cots_target_22B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.122",
                        'ctrl1':"10.35.26.226",
                        'ctrl2' :"10.35.26.227",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.229',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.229'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fec5:d7d3'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.122',
                        'external_tg': ['10.35.26.229'],
                        'tg_coord' : '10.35.42.122'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.122',
                        'vip_2'    : '192.168.66.122',
                        'vip_3'    : '10.35.42.122',
                        'vip_IPv4_OAM'     : '10.35.42.122',
                        'vip_IPv4_traffic' : ['172.16.0.122','192.168.66.122'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:122','fd41:4580:3405::2:122'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.176/30','192.168.21.180/30']],[2,['192.168.22.176/30','192.168.22.180/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.178','192.168.21.182']],[2,['192.168.22.178','192.168.22.182']]],
                        'vip_link_gw'      : [[1,['192.168.21.177','192.168.21.181']],[2,['192.168.22.177','192.168.22.181']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7017',
                        'SC_2_2': '7018',
                        'PL_2_3': '7019',
                        'PL_2_4': '7020',
                        'switch_1': '7011',
                        'switch_2': '7012'
                },
                'switches' : {
                        'switch_1' : "10.35.26.223",
                        'switch_2' : "10.35.26.224",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50046"
                }
        },

        'cots_target_23' :  {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.23",
                        'ctrl1':"10.35.26.231",
                        'ctrl2' :"10.35.26.232",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.235',
                        'external':['192.168.16.239'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.235'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fea6:e83f'],
                        'external_IPv4':['192.168.16.239'],
                        'external_IPv6':['fd41:4580:3405:16:204:23ff:fede:b181']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.23',
                        'external_tg': ['10.35.26.235'],
                        'tg_coord' : '10.35.42.23'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.23',
                        'vip_2'    : '192.168.66.23',
                        'vip_3'    : '10.35.42.23',
                        'vip_IPv4_OAM'     : '10.35.42.23',
                        'vip_IPv4_traffic' : ['172.16.0.23','192.168.66.23'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:23','fd41:4580:3405::2:23'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.176/30','192.168.21.180/30']],[2,['192.168.22.176/30','192.168.22.180/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.178','192.168.21.182']],[2,['192.168.22.178','192.168.22.182']]],
                        'vip_link_gw'      : [[1,['192.168.21.177','192.168.21.181']],[2,['192.168.22.177','192.168.22.181']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7023',
                        'SC_2_2': '7024',
                        'PL_2_3': '7025',
                        'PL_2_4': '7026',
                        'PL_2_5': '7027',
                        'PL_2_6': '7028',
                        'PL_2_7': '7029',
                        'PL_2_8': '7030',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.233",
                        'switch_2' : "10.35.26.234",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,\
                                        18,19,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50023"
                }
        },

        'cots_target_23A' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.23",
                        'ctrl1':"10.35.26.231",
                        'ctrl2' :"10.35.26.232",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.235',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.235'],
                        'gateway_IPv6' :['fd41:4580:3405:16:215:17ff:fea6:e83f'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.23',
                        'external_tg': ['10.35.26.235'],
                        'tg_coord' : '10.35.42.23'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.23',
                        'vip_2'    : '192.168.66.23',
                        'vip_3'    : '10.35.42.23',
                        'vip_IPv4_OAM'     : '10.35.42.23',
                        'vip_IPv4_traffic' : ['172.16.0.23','192.168.66.23'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:23','fd41:4580:3405::2:23'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.176/30','192.168.21.180/30']],[2,['192.168.22.176/30','192.168.22.180/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.178','192.168.21.182']],[2,['192.168.22.178','192.168.22.182']]],
                        'vip_link_gw'      : [[1,['192.168.21.177','192.168.21.181']],[2,['192.168.22.177','192.168.22.181']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7023',
                        'SC_2_2': '7024',
                        'PL_2_3': '7025',
                        'PL_2_4': '7026',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.233",
                        'switch_2' : "10.35.26.234",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50023"
                }
        },

        'cots_target_23B' :  {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.123",
                        'ctrl1':"10.35.26.236",
                        'ctrl2' :"10.35.26.237",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.239',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.16.0/24',
                        'gateway_IPv4' :['192.168.16.239'],
                        'gateway_IPv6' :['fd41:4580:3405:16:204:23ff:fede:b181'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.123',
                        'external_tg': ['10.35.26.239'],
                        'tg_coord' : '10.35.42.123'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.123',
                        'vip_2'    : '192.168.66.123',
                        'vip_3'    : '10.35.42.123',
                        'vip_IPv4_OAM'     : '10.35.42.123',
                        'vip_IPv4_traffic' : ['172.16.0.123','192.168.66.123'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:123','fd41:4580:3405::2:123'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.184/30','192.168.21.188/30']],[2,['192.168.22.184/30','192.168.22.188/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.186','192.168.21.190']],[2,['192.168.22.186','192.168.22.190']]],
                        'vip_link_gw'      : [[1,['192.168.21.185','192.168.21.189']],[2,['192.168.22.185','192.168.22.189']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']],\
                                              [2,['FE80::225:84FF:FE92:F858','FE80::226:CBFF:FE95:BCA8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial' : {
                        'ip': '10.35.26.9',
                        'SC_2_1': '7027',
                        'SC_2_2': '7028',
                        'PL_2_3': '7029',
                        'PL_2_4': '7030',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.233",
                        'switch_2' : "10.35.26.234",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50047"
                }
        },

        'cots_target_24' : {
                'physical_size': "8",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.24",
                        'ctrl1' :"10.35.26.241",
                        'ctrl2' :"10.35.26.242",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.245',
                        'external':['10.35.26.249'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.245'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe78:6a3'],
                        'external_IPv4':['192.168.15.249'],
                        'external_IPv6':['fd41:4580:3405:15:204:23ff:fed5:5401']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.24',
                        'external_tg': ['10.35.26.245'],
                        'tg_coord' : '10.35.42.24'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.24',
                        'vip_2'    : '192.168.66.24',
                        'vip_3'    : '10.35.42.24',
                        'vip_IPv4_OAM'     : '10.35.42.24',
                        'vip_IPv4_traffic' : ['172.16.0.24','192.168.66.24'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:24','fd41:4580:3405::2:24'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.184/30','192.168.21.188/30']],[2,['192.168.22.184/30','192.168.22.188/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.186','192.168.21.190']],[2,['192.168.22.186','192.168.22.190']]],
                        'vip_link_gw'      : [[1,['192.168.21.185','192.168.21.189']],[2,['192.168.22.185','192.168.22.189']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial': {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7023',
                        'SC_2_2': '7024',
                        'PL_2_3': '7025',
                        'PL_2_4': '7026',
                        'PL_2_5': '7027',
                        'PL_2_6': '7028',
                        'PL_2_7': '7029',
                        'PL_2_8': '7030',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.243",
                        'switch_2' : "10.35.26.244",
                        'portsInOrder' : [1,2,3,4,5,6,7,8,17,18,20,21,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50024"
                }
        },

        'cots_target_24A' : {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.24",
                        'ctrl1' :"10.35.26.241",
                        'ctrl2' :"10.35.26.242",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.245',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.245'],
                        'gateway_IPv6' :['fd41:4580:3405:15:215:17ff:fe78:6a3'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.24',
                        'external_tg': ['10.35.26.245'],
                        'tg_coord' : '10.35.42.24'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.24',
                        'vip_2'    : '192.168.66.24',
                        'vip_3'    : '10.35.42.24',
                        'vip_IPv4_OAM'     : '10.35.42.24',
                        'vip_IPv4_traffic' : ['172.16.0.24','192.168.66.24'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:24','fd41:4580:3405::2:24'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.184/30','192.168.21.188/30']],[2,['192.168.22.184/30','192.168.22.188/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.186','192.168.21.190']],[2,['192.168.22.186','192.168.22.190']]],
                        'vip_link_gw'      : [[1,['192.168.21.185','192.168.21.189']],[2,['192.168.22.185','192.168.22.189']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial': {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7023',
                        'SC_2_2': '7024',
                        'PL_2_3': '7025',
                        'PL_2_4': '7026',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.243",
                        'switch_2' : "10.35.26.244",
                        'portsInOrder' : [1,2,3,4,17,22,23]
                }
                },
        'ports' : {
                'snmptrapd': "50024"
                }
        },

        'cots_target_24B' : {
                'physical_size': "4",
                'execution_capacity_factor': "1",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'NB'  :"10.35.42.124",
                        'ctrl1' :"10.35.26.246",
                        'ctrl2' :"10.35.26.247",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.249',
                        'external':[],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.104',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.15.0/24',
                        'gateway_IPv4' :['192.168.15.249'],
                        'gateway_IPv6' :['fd41:4580:3405:15:204:23ff:fed5:5401'],
                        'external_IPv4':[],
                        'external_IPv6':[]
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.124',
                        'external_tg': ['10.35.26.249'],
                        'tg_coord' : '10.35.42.124'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.124',
                        'vip_2'    : '192.168.66.124',
                        'vip_3'    : '10.35.42.124',
                        'vip_IPv4_OAM'     : '10.35.42.124',
                        'vip_IPv4_traffic' : ['172.16.0.124','192.168.66.124'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:124','fd41:4580:3405::2:124'],
                        'vip_link_type'    : [[1,'eth',2,3],[2,'eth',2,3]],
                        'vip_link_net'     : [[1,['192.168.21.192/30','192.168.21.196/30']],[2,['192.168.22.192/30','192.168.22.196/30']]],
                        'vip_link_addr'    : [[1,['192.168.21.194','192.168.21.198']],[2,['192.168.22.194','192.168.22.198']]],
                        'vip_link_gw'      : [[1,['192.168.21.193','192.168.21.197']],[2,['192.168.22.193','192.168.22.197']]],
                        'vip_IPv6_link_gw' : [[1,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']],\
                                              [2,['FE80::21B:D5FF:FEB2:86E8','FE80::21B:D5FF:FEB9:59B8']]],
                        'IPv6_accept_ra_disable': 'yes'
                },
                'serial': {
                        'ip': '10.35.26.8',
                        'SC_2_1': '7027',
                        'SC_2_2': '7028',
                        'PL_2_3': '7029',
                        'PL_2_4': '7030',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.26.243",
                        'switch_2' : "10.35.26.244",
                        'portsInOrder' : [5,6,7,8,18,20]
                }
                },
        'ports' : {
                'snmptrapd': "50048"
                }
        }
        }

        if targetHw in targetData3:
                return targetData3[targetHw]
        else:
                return -1


def _setTargetHwData4(targetHw):

        targetData4 = {

        'sun_target_1' : {
                'physical_size': "10",
                'execution_capacity_factor': "6",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.1",
                        'ctrl1':"10.35.26.11",
                        'ctrl2' :"10.35.26.12",
                        'ctrl_if'  : ['bond_vlan',3],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.15',
                        'external':['10.35.24.117','10.35.24.118'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.12.0/24',
                        'gateway_IPv4' :['192.168.12.15'],
                        'gateway_IPv6' :['2011:4580:3405:12::215:17ff:fe98:9457'],
                        'external_IPv4':['192.168.12.178','192.168.12.188'],
                        'external_IPv6':['2011:4580:3405:12:222:19ff:fe2c:a023','2011:4580:3405:12:215:17ff:feae:e80c']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.1',
                        'external_tg': ['10.35.26.15','10.35.24.117','10.35.24.118'],
                        'tg_coord' : '10.35.42.1'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.1',
                        'vip_2'    : '192.168.66.1',
                        'vip_3'    : '10.35.42.1',
                        'vip_IPv4_OAM'     : '10.35.42.1',
                        'vip_IPv4_traffic' : ['172.16.0.1','192.168.66.1','192.168.103.1','192.168.104.1','192.168.105.1',\
                                              '192.168.106.1','192.168.107.1','192.168.108.1','192.168.109.1','192.168.110.1',\
                                              '192.168.111.1','192.168.112.1','192.168.113.1','192.168.114.1','192.168.115.1',\
                                              '192.168.116.1'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:1','fd41:4580:3405::2:1','fd41:4580:3405::3:1','fd41:4580:3405::4:1','fd41:4580:3405::5:1',\
                                              'fd41:4580:3405::6:1','fd41:4580:3405::7:1','fd41:4580:3405::8:1','fd41:4580:3405::9:1','fd41:4580:3405::10:1',\
                                              'fd41:4580:3405::11:1','fd41:4580:3405::12:1','fd41:4580:3405::13:1','fd41:4580:3405::14:1','fd41:4580:3405::15:1',\
                                              'fd41:4580:3405::16:1'],
                        'vip_link_type'    : [[1,'bond_vlan',20],[2,'bond_vlan',21],\
                                        [3,'bond_vlan',22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172],\
                                        [4,'bond_vlan',23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173],\
                                        [5,'bond_vlan',24,34,44,54,64,74,84,94,104,114,124,134,144,154,164,174],\
                                        [6,'bond_vlan',25,35,45,55,65,75,85,95,105,115,125,135,145,155,165,175],\
                                        [7,'bond_vlan',26,36,46,56,66,76,86,96,106,116,126,136,146,156,166,176],\
                                        [8,'bond_vlan',27,37,47,57,67,77,87,97,107,117,127,137,147,157,167,177],\
                                        [9,'bond_vlan',28,38,48,58,68,78,88,98,108,118,128,138,148,158,168,178],\
                                        [10,'bond_vlan',29,39,49,59,69,79,89,99,109,119,129,139,149,159,169,179],\
                                        ['vrrp','bond_vlan',1400]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29']],\
                                        [5,['192.168.24.0/29','192.168.24.8/29','192.168.24.16/29','192.168.24.24/29','192.168.24.32/29',\
                                            '192.168.24.40/29','192.168.24.48/29','192.168.24.56/29','192.168.24.64/29','192.168.24.72/29',\
                                            '192.168.24.80/29','192.168.24.88/29','192.168.24.96/29','192.168.24.104/29','192.168.24.112/29',\
                                            '192.168.24.120/29']],\
                                        [6,['192.168.25.0/29','192.168.25.8/29','192.168.25.16/29','192.168.25.24/29','192.168.25.32/29',\
                                            '192.168.25.40/29','192.168.25.48/29','192.168.25.56/29','192.168.25.64/29','192.168.25.72/29',\
                                            '192.168.25.80/29','192.168.25.88/29','192.168.25.96/29','192.168.25.104/29','192.168.25.112/29',\
                                            '192.168.25.120/29']],\
                                        [7,['192.168.26.0/29','192.168.26.8/29','192.168.26.16/29','192.168.26.24/29','192.168.26.32/29',\
                                            '192.168.26.40/29','192.168.26.48/29','192.168.26.56/29','192.168.26.64/29','192.168.26.72/29',\
                                            '192.168.26.80/29','192.168.26.88/29','192.168.26.96/29','192.168.26.104/29','192.168.26.112/29',\
                                            '192.168.26.120/29']],\
                                        [8,['192.168.27.0/29','192.168.27.8/29','192.168.27.16/29','192.168.27.24/29','192.168.27.32/29',\
                                            '192.168.27.40/29','192.168.27.48/29','192.168.27.56/29','192.168.27.64/29','192.168.27.72/29',\
                                            '192.168.27.80/29','192.168.27.88/29','192.168.27.96/29','192.168.27.104/29','192.168.27.112/29',\
                                            '192.168.27.120/29']],\
                                        [9,['192.168.28.0/29','192.168.28.8/29','192.168.28.16/29','192.168.28.24/29','192.168.28.32/29',\
                                            '192.168.28.40/29','192.168.28.48/29','192.168.28.56/29','192.168.28.64/29','192.168.28.72/29',\
                                            '192.168.28.80/29','192.168.28.88/29','192.168.28.96/29','192.168.28.104/29','192.168.28.112/29',\
                                            '192.168.28.120/29']],\
                                        [10,['192.168.29.0/29','192.168.29.8/29','192.168.29.16/29','192.168.29.24/29','192.168.29.32/29',\
                                            '192.168.29.40/29','192.168.29.48/29','192.168.29.56/29','192.168.29.64/29','192.168.29.72/29',\
                                            '192.168.29.80/29','192.168.29.88/29','192.168.29.96/29','192.168.29.104/29','192.168.29.112/29',\
                                            '192.168.29.120/29']],\
                                        ['vrrp',['192.168.60.0/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123']],\
                                        [5,['192.168.24.3','192.168.24.11','192.168.24.19','192.168.24.27','192.168.24.35',\
                                            '192.168.24.43','192.168.24.51','192.168.24.59','192.168.24.67','192.168.24.75',\
                                            '192.168.24.83','192.168.24.91','192.168.24.99','192.168.24.107','192.168.24.115',\
                                            '192.168.24.123']],\
                                        [6,['192.168.25.3','192.168.25.11','192.168.25.19','192.168.25.27','192.168.25.35',\
                                            '192.168.25.43','192.168.25.51','192.168.25.59','192.168.25.67','192.168.25.75',\
                                            '192.168.25.83','192.168.25.91','192.168.25.99','192.168.25.107','192.168.25.115',\
                                            '192.168.25.123']],\
                                        [7,['192.168.26.3','192.168.26.11','192.168.26.19','192.168.26.27','192.168.26.35',\
                                            '192.168.26.43','192.168.26.51','192.168.26.59','192.168.26.67','192.168.26.75',\
                                            '192.168.26.83','192.168.26.91','192.168.26.99','192.168.26.107','192.168.26.115',\
                                            '192.168.26.123']],\
                                        [8,['192.168.27.3','192.168.27.11','192.168.27.19','192.168.27.27','192.168.27.35',\
                                            '192.168.27.43','192.168.27.51','192.168.27.59','192.168.27.67','192.168.27.75',\
                                            '192.168.27.83','192.168.27.91','192.168.27.99','192.168.27.107','192.168.27.115',\
                                            '192.168.27.123']],\
                                        [9,['192.168.28.3','192.168.28.11','192.168.28.19','192.168.28.27','192.168.28.35',\
                                            '192.168.28.43','192.168.28.51','192.168.28.59','192.168.28.67','192.168.28.75',\
                                            '192.168.28.83','192.168.28.91','192.168.28.99','192.168.28.107','192.168.28.115',\
                                            '192.168.28.123']],\
                                        [10,['192.168.29.3','192.168.29.11','192.168.29.19','192.168.29.27','192.168.29.35',\
                                            '192.168.29.43','192.168.29.51','192.168.29.59','192.168.29.67','192.168.29.75',\
                                            '192.168.29.83','192.168.29.91','192.168.29.99','192.168.29.107','192.168.29.115',\
                                            '192.168.29.123']],\
                                        ['vrrp',['192.168.60.3/29','192.168.60.4/29','192.168.60.6']]],
                        'vip_link_gw'      : [[1,['192.168.20.1','192.168.20.2']],[2,['192.168.21.2','192.168.21.1']],[3,['192.168.22.9','192.168.22.10']],\
                                        [4,['192.168.23.10','192.168.23.9']],[5,['192.168.24.9','192.168.24.10']],[6,['192.168.25.10','192.168.25.9']],\
                                        [7,['192.168.26.9','192.168.26.10']],[8,['192.168.27.10','192.168.27.9']],[9,['192.168.28.9','192.168.28.10']],\
                                        [10,['192.168.29.10','192.168.29.9']],\
                                        ['vrrp',['192.168.60.1','192.168.60.2','192.168.60.5']]],
                        'vip_IPv6_link_gw' : [[1,['fe80::204:96ff:fe27:8dab','fe80::204:96ff:fe27:c4e1']],\
                                        [2,['fe80::204:96ff:fe27:c4e1','fe80::204:96ff:fe27:8dab']],\
                                        [3,['fe80::204:96ff:fe27:8dab','fe80::204:96ff:fe27:c4e1']],\
                                        [4,['fe80::204:96ff:fe27:c4e1','fe80::204:96ff:fe27:8dab']],\
                                        [5,['fe80::204:96ff:fe27:8dab','fe80::204:96ff:fe27:c4e1']],\
                                        [6,['fe80::204:96ff:fe27:c4e1','fe80::204:96ff:fe27:8dab']],\
                                        [7,['fe80::204:96ff:fe27:8dab','fe80::204:96ff:fe27:c4e1']],\
                                        [8,['fe80::204:96ff:fe27:c4e1','fe80::204:96ff:fe27:8dab']],\
                                        [9,['fe80::204:96ff:fe27:8dab','fe80::204:96ff:fe27:c4e1']],\
                                        [10,['fe80::204:96ff:fe27:c4e1','fe80::204:96ff:fe27:8dab']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.26.251',
                        'SC_2_1': '7004',
                        'SC_2_2': '7005',
                        'PL_2_3': '7006',
                        'PL_2_4': '7007',
                        'switch_1': '7001',
                        'switch_2': '7002',
                        'chassis_cmm': '7003'
                },
                'switches' : {
                        'switch_1' : "10.35.26.13",
                        'switch_2' : "10.35.26.14",
                        'portsInOrder' : [1005,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1037,\
                                        1006,1008,1010,1012,1014,1016,1018,1020,1022,1024,\
                                        1004,1003,1002,1001]
                }
                },
        'ports' : {
                'snmptrapd': "50001"
                }
        },

        'sun_target_2' : {
                'physical_size': "10",
                'execution_capacity_factor': "6",
                'watchdog' : 'ipmi',
                'ipAddress' :  {
                'ctrl' : {
                        'NB'  :"10.35.42.2",
                        'ctrl1':"10.35.26.21",
                        'ctrl2' :"10.35.26.22",
                        'ctrl_if'  : ['bond_vlan',3],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.25',
                        'external':['10.35.24.119','10.35.24.120'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.13.0/24',
                        'gateway_IPv4' :['192.168.13.25'],
                        'gateway_IPv6' :['2011:4580:3405:13:215:17ff:fe98:954b'],
                        'external_IPv4':['192.168.13.198','192.168.13.208'],
                        'external_IPv6':['2011:4580:3405:13:215:17ff:feae:e33c','2011:4580:3405:13:215:17ff:feae:e7fe']
                },
                'testApp'  : {
                        'test_app'   : '172.16.0.2',
                        'external_tg': ['10.35.26.25','10.35.24.119','10.35.24.120'],
                        'tg_coord' : '10.35.42.2'
                },
                'vip'  : {
                        'vip_1'    : '172.16.0.2',
                        'vip_2'    : '192.168.66.2',
                        'vip_3'    : '10.35.42.2',
                        'vip_IPv4_OAM'     : '10.35.42.2',
                        'vip_IPv4_traffic' : ['172.16.0.2','192.168.66.2','192.168.103.2','192.168.104.2','192.168.105.2',\
                                              '192.168.106.2','192.168.107.2','192.168.108.2','192.168.109.2','192.168.110.2',\
                                              '192.168.111.2','192.168.112.2','192.168.113.2','192.168.114.2','192.168.115.2',\
                                              '192.168.116.2'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:2','fd41:4580:3405::2:2','fd41:4580:3405::3:2','fd41:4580:3405::4:2','fd41:4580:3405::5:2',\
                                              'fd41:4580:3405::6:2','fd41:4580:3405::7:2','fd41:4580:3405::8:2','fd41:4580:3405::9:2','fd41:4580:3405::10:2',\
                                              'fd41:4580:3405::11:2','fd41:4580:3405::12:2','fd41:4580:3405::13:2','fd41:4580:3405::14:2','fd41:4580:3405::15:2',\
                                              'fd41:4580:3405::16:2'],
                        'vip_link_type'    : [[1,'bond_vlan',20],[2,'bond_vlan',21],\
                                        [3,'bond_vlan',22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172],\
                                        [4,'bond_vlan',23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173],\
                                        [5,'bond_vlan',24,34,44,54,64,74,84,94,104,114,124,134,144,154,164,174],\
                                        [6,'bond_vlan',25,35,45,55,65,75,85,95,105,115,125,135,145,155,165,175],\
                                        [7,'bond_vlan',26,36,46,56,66,76,86,96,106,116,126,136,146,156,166,176],\
                                        [8,'bond_vlan',27,37,47,57,67,77,87,97,107,117,127,137,147,157,167,177],\
                                        [9,'bond_vlan',28,38,48,58,68,78,88,98,108,118,128,138,148,158,168,178],\
                                        [10,'bond_vlan',29,39,49,59,69,79,89,99,109,119,129,139,149,159,169,179],\
                                        ['vrrp','bond_vlan',1400]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29']],\
                                        [5,['192.168.24.0/29','192.168.24.8/29','192.168.24.16/29','192.168.24.24/29','192.168.24.32/29',\
                                            '192.168.24.40/29','192.168.24.48/29','192.168.24.56/29','192.168.24.64/29','192.168.24.72/29',\
                                            '192.168.24.80/29','192.168.24.88/29','192.168.24.96/29','192.168.24.104/29','192.168.24.112/29',\
                                            '192.168.24.120/29']],\
                                        [6,['192.168.25.0/29','192.168.25.8/29','192.168.25.16/29','192.168.25.24/29','192.168.25.32/29',\
                                            '192.168.25.40/29','192.168.25.48/29','192.168.25.56/29','192.168.25.64/29','192.168.25.72/29',\
                                            '192.168.25.80/29','192.168.25.88/29','192.168.25.96/29','192.168.25.104/29','192.168.25.112/29',\
                                            '192.168.25.120/29']],\
                                        [7,['192.168.26.0/29','192.168.26.8/29','192.168.26.16/29','192.168.26.24/29','192.168.26.32/29',\
                                            '192.168.26.40/29','192.168.26.48/29','192.168.26.56/29','192.168.26.64/29','192.168.26.72/29',\
                                            '192.168.26.80/29','192.168.26.88/29','192.168.26.96/29','192.168.26.104/29','192.168.26.112/29',\
                                            '192.168.26.120/29']],\
                                        [8,['192.168.27.0/29','192.168.27.8/29','192.168.27.16/29','192.168.27.24/29','192.168.27.32/29',\
                                            '192.168.27.40/29','192.168.27.48/29','192.168.27.56/29','192.168.27.64/29','192.168.27.72/29',\
                                            '192.168.27.80/29','192.168.27.88/29','192.168.27.96/29','192.168.27.104/29','192.168.27.112/29',\
                                            '192.168.27.120/29']],\
                                        [9,['192.168.28.0/29','192.168.28.8/29','192.168.28.16/29','192.168.28.24/29','192.168.28.32/29',\
                                            '192.168.28.40/29','192.168.28.48/29','192.168.28.56/29','192.168.28.64/29','192.168.28.72/29',\
                                            '192.168.28.80/29','192.168.28.88/29','192.168.28.96/29','192.168.28.104/29','192.168.28.112/29',\
                                            '192.168.28.120/29']],\
                                        [10,['192.168.29.0/29','192.168.29.8/29','192.168.29.16/29','192.168.29.24/29','192.168.29.32/29',\
                                            '192.168.29.40/29','192.168.29.48/29','192.168.29.56/29','192.168.29.64/29','192.168.29.72/29',\
                                            '192.168.29.80/29','192.168.29.88/29','192.168.29.96/29','192.168.29.104/29','192.168.29.112/29',\
                                            '192.168.29.120/29']],\
                                        ['vrrp',['192.168.60.0/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123']],\
                                        [5,['192.168.24.3','192.168.24.11','192.168.24.19','192.168.24.27','192.168.24.35',\
                                            '192.168.24.43','192.168.24.51','192.168.24.59','192.168.24.67','192.168.24.75',\
                                            '192.168.24.83','192.168.24.91','192.168.24.99','192.168.24.107','192.168.24.115',\
                                            '192.168.24.123']],\
                                        [6,['192.168.25.3','192.168.25.11','192.168.25.19','192.168.25.27','192.168.25.35',\
                                            '192.168.25.43','192.168.25.51','192.168.25.59','192.168.25.67','192.168.25.75',\
                                            '192.168.25.83','192.168.25.91','192.168.25.99','192.168.25.107','192.168.25.115',\
                                            '192.168.25.123']],\
                                        [7,['192.168.26.3','192.168.26.11','192.168.26.19','192.168.26.27','192.168.26.35',\
                                            '192.168.26.43','192.168.26.51','192.168.26.59','192.168.26.67','192.168.26.75',\
                                            '192.168.26.83','192.168.26.91','192.168.26.99','192.168.26.107','192.168.26.115',\
                                            '192.168.26.123']],\
                                        [8,['192.168.27.3','192.168.27.11','192.168.27.19','192.168.27.27','192.168.27.35',\
                                            '192.168.27.43','192.168.27.51','192.168.27.59','192.168.27.67','192.168.27.75',\
                                            '192.168.27.83','192.168.27.91','192.168.27.99','192.168.27.107','192.168.27.115',\
                                            '192.168.27.123']],\
                                        [9,['192.168.28.3','192.168.28.11','192.168.28.19','192.168.28.27','192.168.28.35',\
                                            '192.168.28.43','192.168.28.51','192.168.28.59','192.168.28.67','192.168.28.75',\
                                            '192.168.28.83','192.168.28.91','192.168.28.99','192.168.28.107','192.168.28.115',\
                                            '192.168.28.123']],\
                                        [10,['192.168.29.3','192.168.29.11','192.168.29.19','192.168.29.27','192.168.29.35',\
                                            '192.168.29.43','192.168.29.51','192.168.29.59','192.168.29.67','192.168.29.75',\
                                            '192.168.29.83','192.168.29.91','192.168.29.99','192.168.29.107','192.168.29.115',\
                                            '192.168.29.123']],\
                                        ['vrrp',['192.168.60.3/29','192.168.60.4/29','192.168.60.6']]],
                        'vip_link_gw'      : [[1,['192.168.20.1','192.168.20.2']],[2,['192.168.21.2','192.168.21.1']],[3,['192.168.22.9','192.168.22.10']],\
                                        [4,['192.168.23.10','192.168.23.9']],[5,['192.168.24.9','192.168.24.10']],[6,['192.168.25.10','192.168.25.9']],\
                                        [7,['192.168.26.9','192.168.26.10']],[8,['192.168.27.10','192.168.27.9']],[9,['192.168.28.9','192.168.28.10']],\
                                        [10,['192.168.29.10','192.168.29.9']],\
                                        ['vrrp',['192.168.60.1','192.168.60.2','192.168.60.5']]],
                        'vip_IPv6_link_gw' : [[1,['fe80::204:96ff:fe34:a63b','fe80::204:96ff:fe27:8ec8']],\
                                        [2,['fe80::204:96ff:fe27:8ec8','fe80::204:96ff:fe34:a63b']],\
                                        [3,['fe80::204:96ff:fe34:a63b','fe80::204:96ff:fe27:8ec8']],\
                                        [4,['fe80::204:96ff:fe27:8ec8','fe80::204:96ff:fe34:a63b']],\
                                        [5,['fe80::204:96ff:fe34:a63b','fe80::204:96ff:fe27:8ec8']],\
                                        [6,['fe80::204:96ff:fe27:8ec8','fe80::204:96ff:fe34:a63b']],\
                                        [7,['fe80::204:96ff:fe34:a63b','fe80::204:96ff:fe27:8ec8']],\
                                        [8,['fe80::204:96ff:fe27:8ec8','fe80::204:96ff:fe34:a63b']],\
                                        [9,['fe80::204:96ff:fe34:a63b','fe80::204:96ff:fe27:8ec8']],\
                                        [10,['fe80::204:96ff:fe27:8ec8','fe80::204:96ff:fe34:a63b']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.26.251',
                        'SC_2_1': '7011',
                        'SC_2_2': '7012',
                        'PL_2_3': '7013',
                        'PL_2_4': '7014',
                        'PL_2_6': '7015',
                        'PL_2_7': '7016',
                        'PL_2_8': '7017',
                        'PL_2_9': '7018',
                        'switch_1': '7008',
                        'switch_2': '7009',
                        'chassis_cmm': '7010'
                },
                'switches' : {
                        'switch_1' : "10.35.26.23",
                        'switch_2' : "10.35.26.24",
                        'portsInOrder' : [1005,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1037,\
                                        1006,1008,1010,1012,1014,1016,1018,1020,1022,1024,\
                                        1004,1003,1002,1001]
                }
                },
        'ports' : {
                'snmptrapd': "50002"
                }
        },

        'sun_target_3' : {
                'physical_size': "10",
                'execution_capacity_factor': "8",
                'watchdog' : 'soft',
                'ipAddress' :  {
                'ctrl' : {
                        'ctrl1':"10.35.26.31",
                        'ctrl2' :"10.35.26.32",
                        'ctrl_if'  : ['bond_vlan',3],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc':'10.35.26.35',
                        'external':['10.35.24.121','10.35.24.122','10.35.24.123','10.35.24.124'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '192.168.0.100',
                        'bond_arp' : []
                },
                'traffic' : {
                        'network_IPv4' :'192.168.14.0/24',
                        'gateway_IPv4' :['192.168.14.35'],
                        'gateway_IPv6' :['2011:4580:3405:14:215:17ff:fea8:e3c3'],
                        'external_IPv4':['192.168.14.218','192.168.14.228','192.168.14.238','192.168.14.248'],
                        'external_IPv6':['2011:4580:3405:14:215:17ff:feae:e35e','2011:4580:3405:14:215:17ff:feae:e33e',\
                                        '2011:4580:3405:14:215:17ff:feae:e3bc','2011:4580:3405:14:215:17ff:feae:e478']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.3',
                        'vip_IPv4_traffic' : ['172.16.0.3','192.168.66.3','192.168.103.3','192.168.104.3','192.168.105.3',\
                                              '192.168.106.3','192.168.107.3','192.168.108.3','192.168.109.3','192.168.110.3',\
                                              '192.168.111.3','192.168.112.3','192.168.113.3','192.168.114.3','192.168.115.3',\
                                              '192.168.116.3','192.168.117.3','192.168.118.3','192.168.119.3','192.168.120.3',\
                                              '192.168.121.3','192.168.122.3','192.168.123.3','192.168.124.3','192.168.125.3',\
                                              '192.168.126.3','192.168.127.3','192.168.128.3','192.168.129.3','192.168.130.3',\
                                              '192.168.131.3','192.168.132.3','192.168.133.3','192.168.134.3','192.168.135.3',\
                                              '192.168.136.3','192.168.137.3','192.168.138.3','192.168.139.3','192.168.140.3',\
                                              '192.168.141.3','192.168.142.3','192.168.143.3','192.168.144.3','192.168.145.3',\
                                              '192.168.146.3','192.168.147.3','192.168.148.3','192.168.149.3','192.168.150.3',\
                                              '192.168.151.3','192.168.152.3','192.168.153.3','192.168.154.3','192.168.155.3',\
                                              '192.168.156.3','192.168.157.3','192.168.158.3','192.168.159.3','192.168.160.3',\
                                              '192.168.161.3','192.168.162.3','192.168.163.3','192.168.164.3'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:3','fd41:4580:3405::2:3','fd41:4580:3405::3:3','fd41:4580:3405::4:3','fd41:4580:3405::5:3',\
                                              'fd41:4580:3405::6:3','fd41:4580:3405::7:3','fd41:4580:3405::8:3','fd41:4580:3405::9:3','fd41:4580:3405::10:3',\
                                              'fd41:4580:3405::11:3','fd41:4580:3405::12:3','fd41:4580:3405::13:3','fd41:4580:3405::14:3','fd41:4580:3405::15:3',\
                                              'fd41:4580:3405::16:3','fd41:4580:3405::17:3','fd41:4580:3405::18:3','fd41:4580:3405::19:3','fd41:4580:3405::20:3',\
                                              'fd41:4580:3405::21:3','fd41:4580:3405::22:3','fd41:4580:3405::23:3','fd41:4580:3405::24:3','fd41:4580:3405::25:3',\
                                              'fd41:4580:3405::26:3','fd41:4580:3405::27:3','fd41:4580:3405::28:3','fd41:4580:3405::29:3','fd41:4580:3405::30:3',\
                                              'fd41:4580:3405::31:3','fd41:4580:3405::32:3','fd41:4580:3405::33:3','fd41:4580:3405::34:3','fd41:4580:3405::35:3',\
                                              'fd41:4580:3405::36:3','fd41:4580:3405::37:3','fd41:4580:3405::38:3','fd41:4580:3405::39:3','fd41:4580:3405::40:3',\
                                              'fd41:4580:3405::41:3','fd41:4580:3405::42:3','fd41:4580:3405::43:3','fd41:4580:3405::44:3','fd41:4580:3405::45:3',\
                                              'fd41:4580:3405::46:3','fd41:4580:3405::47:3','fd41:4580:3405::48:3','fd41:4580:3405::49:3','fd41:4580:3405::50:3',\
                                              'fd41:4580:3405::51:3','fd41:4580:3405::52:3','fd41:4580:3405::53:3','fd41:4580:3405::54:3','fd41:4580:3405::55:3',\
                                              'fd41:4580:3405::56:3','fd41:4580:3405::57:3','fd41:4580:3405::58:3','fd41:4580:3405::59:3','fd41:4580:3405::60:3',\
                                              'fd41:4580:3405::61:3','fd41:4580:3405::62:3','fd41:4580:3405::63:3','fd41:4580:3405::64:3'],
                        'vip_link_type'    : [[1,'bond_vlan',20],[2,'bond_vlan',21],\
                                        [3,'bond_vlan',22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172,182,192,202,\
                                           212,222,232,242,252,262,272,282,293,302,312,322,332,342,352,362,372,382,392,402,\
                                           412,422,432,442,452,462,472,482,492,502,512,522,532,542,552,562,572,582,592,602,\
                                           612,622,632,642,652],\
                                        [4,'bond_vlan',23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173,183,193,203,\
                                           213,223,233,243,253,263,273,283,293,303,313,323,333,343,353,363,373,383,393,403,\
                                           413,423,433,443,453,463,473,483,493,503,513,523,533,543,553,563,573,583,593,603,\
                                           613,623,633,643,653],\
                                        [5,'bond_vlan',24,34,44,54,64,74,84,94,104,114,124,134,144,154,164,174,184,194,204,\
                                           214,224,234,244,254,264,274,284,294,304,314,324,334,344,354,364,374,384,394,404,\
                                           414,424,434,444,454,464,474,484,494,504,514,524,534,544,554,564,574,584,594,604,\
                                           614,624,634,644,654],\
                                        [6,'bond_vlan',25,35,45,55,65,75,85,95,105,115,125,135,145,155,165,175,185,195,205,\
                                           215,225,235,245,255,265,275,285,295,305,315,325,335,345,355,365,375,385,395,405,\
                                           415,425,435,445,455,465,475,485,495,505,515,525,535,545,555,565,575,585,595,605,\
                                           615,625,635,645,655],\
                                        [7,'bond_vlan',26,36,46,56,66,76,86,96,106,116,126,136,146,156,166,176,186,196,206,\
                                           216,226,236,246,256,266,276,286,296,306,316,326,336,346,356,366,376,386,396,406,\
                                           416,426,436,446,456,466,476,486,496,506,516,526,536,546,556,566,576,586,596,606,\
                                           616,626,636,646,656],\
                                        [8,'bond_vlan',27,37,47,57,67,77,87,97,107,117,127,137,147,157,167,177,187,197,207,\
                                           217,227,237,247,257,267,277,287,297,307,317,327,337,347,357,367,377,387,397,407,\
                                           417,427,437,447,457,467,477,487,497,507,517,527,537,547,557,567,577,587,597,607,\
                                           617,627,637,647,657],\
                                        [9,'bond_vlan',28,38,48,58,68,78,88,98,108,118,128,138,148,158,168,178,188,198,208,\
                                           218,228,238,248,258,268,278,288,298,308,318,328,338,348,358,368,378,388,398,408,\
                                           418,428,438,448,458,468,478,488,498,508,518,528,538,548,558,568,578,588,598,608,\
                                           618,628,638,648,658],\
                                        [10,'bond_vlan',29,39,49,59,69,79,89,99,109,119,129,139,149,159,169,179,189,199,209,\
                                           219,229,239,249,259,269,279,289,299,309,319,329,339,349,359,369,379,389,399,409,\
                                           419,429,439,449,459,469,479,489,499,509,519,529,539,549,559,569,579,589,599,609,\
                                           619,629,639,649,659],\
                                        ['vrrp','bond_vlan',1400]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29','192.168.22.128/29','192.168.22.136/29','192.168.22.144/29','192.168.22.152/29',\
                                            '192.168.22.160/29','192.168.22.168/29','192.168.22.176/29','192.168.22.184/29','192.168.22.192/29',\
                                            '192.168.22.200/29','192.168.22.208/29','192.168.22.216/29','192.168.22.224/29','192.168.22.232/29',\
                                            '192.168.22.240/29','192.168.22.248/29',\
                                            '192.168.32.0/29','192.168.32.8/29','192.168.32.16/29','192.168.32.24/29','192.168.32.32/29',\
                                            '192.168.32.40/29','192.168.32.48/29','192.168.32.56/29','192.168.32.64/29','192.168.32.72/29',\
                                            '192.168.32.80/29','192.168.32.88/29','192.168.32.96/29','192.168.32.104/29','192.168.32.112/29',\
                                            '192.168.32.120/29','192.168.32.128/29','192.168.32.136/29','192.168.32.144/29','192.168.32.152/29',\
                                            '192.168.32.160/29','192.168.32.168/29','192.168.32.176/29','192.168.32.184/29','192.168.32.192/29',\
                                            '192.168.32.200/29','192.168.32.208/29','192.168.32.216/29','192.168.32.224/29','192.168.32.232/29',\
                                            '192.168.32.240/29','192.168.32.248/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29','192.168.23.128/29','192.168.23.136/29','192.168.23.144/29','192.168.23.152/29',\
                                            '192.168.23.160/29','192.168.23.168/29','192.168.23.176/29','192.168.23.184/29','192.168.23.192/29',\
                                            '192.168.23.200/29','192.168.23.208/29','192.168.23.216/29','192.168.23.224/29','192.168.23.232/29',\
                                            '192.168.23.240/29','192.168.23.248/29',\
                                            '192.168.33.0/29','192.168.33.8/29','192.168.33.16/29','192.168.33.24/29','192.168.33.32/29',\
                                            '192.168.33.40/29','192.168.33.48/29','192.168.33.56/29','192.168.33.64/29','192.168.33.72/29',\
                                            '192.168.33.80/29','192.168.33.88/29','192.168.33.96/29','192.168.33.104/29','192.168.33.112/29',\
                                            '192.168.33.120/29','192.168.33.128/29','192.168.33.136/29','192.168.33.144/29','192.168.33.152/29',\
                                            '192.168.33.160/29','192.168.33.168/29','192.168.33.176/29','192.168.33.184/29','192.168.33.192/29',\
                                            '192.168.33.200/29','192.168.33.208/29','192.168.33.216/29','192.168.33.224/29','192.168.33.232/29',\
                                            '192.168.33.240/29','192.168.33.248/29']],\
                                        [5,['192.168.24.0/29','192.168.24.8/29','192.168.24.16/29','192.168.24.24/29','192.168.24.32/29',\
                                            '192.168.24.40/29','192.168.24.48/29','192.168.24.56/29','192.168.24.64/29','192.168.24.72/29',\
                                            '192.168.24.80/29','192.168.24.88/29','192.168.24.96/29','192.168.24.104/29','192.168.24.112/29',\
                                            '192.168.24.120/29','192.168.24.128/29','192.168.24.136/29','192.168.24.144/29','192.168.24.152/29',\
                                            '192.168.24.160/29','192.168.24.168/29','192.168.24.176/29','192.168.24.184/29','192.168.24.192/29',\
                                            '192.168.24.200/29','192.168.24.208/29','192.168.24.216/29','192.168.24.224/29','192.168.24.232/29',\
                                            '192.168.24.240/29','192.168.24.248/29',\
                                            '192.168.34.0/29','192.168.34.8/29','192.168.34.16/29','192.168.34.24/29','192.168.34.32/29',\
                                            '192.168.34.40/29','192.168.34.48/29','192.168.34.56/29','192.168.34.64/29','192.168.34.72/29',\
                                            '192.168.34.80/29','192.168.34.88/29','192.168.34.96/29','192.168.34.104/29','192.168.34.112/29',\
                                            '192.168.34.120/29','192.168.34.128/29','192.168.34.136/29','192.168.34.144/29','192.168.34.152/29',\
                                            '192.168.34.160/29','192.168.34.168/29','192.168.34.176/29','192.168.34.184/29','192.168.34.192/29',\
                                            '192.168.34.200/29','192.168.34.208/29','192.168.34.216/29','192.168.34.224/29','192.168.34.232/29',\
                                            '192.168.34.240/29','192.168.34.248/29']],\
                                        [6,['192.168.25.0/29','192.168.25.8/29','192.168.25.16/29','192.168.25.24/29','192.168.25.32/29',\
                                            '192.168.25.40/29','192.168.25.48/29','192.168.25.56/29','192.168.25.64/29','192.168.25.72/29',\
                                            '192.168.25.80/29','192.168.25.88/29','192.168.25.96/29','192.168.25.104/29','192.168.25.112/29',\
                                            '192.168.25.120/29','192.168.25.128/29','192.168.25.136/29','192.168.25.144/29','192.168.25.152/29',\
                                            '192.168.25.160/29','192.168.25.168/29','192.168.25.176/29','192.168.25.184/29','192.168.25.192/29',\
                                            '192.168.25.200/29','192.168.25.208/29','192.168.25.216/29','192.168.25.224/29','192.168.25.232/29',\
                                            '192.168.25.240/29','192.168.25.248/29',\
                                            '192.168.35.0/29','192.168.35.8/29','192.168.35.16/29','192.168.35.24/29','192.168.35.32/29',\
                                            '192.168.35.40/29','192.168.35.48/29','192.168.35.56/29','192.168.35.64/29','192.168.35.72/29',\
                                            '192.168.35.80/29','192.168.35.88/29','192.168.35.96/29','192.168.35.104/29','192.168.35.112/29',\
                                            '192.168.35.120/29','192.168.35.128/29','192.168.35.136/29','192.168.35.144/29','192.168.35.152/29',\
                                            '192.168.35.160/29','192.168.35.168/29','192.168.35.176/29','192.168.35.184/29','192.168.35.192/29',\
                                            '192.168.35.200/29','192.168.35.208/29','192.168.35.216/29','192.168.35.224/29','192.168.35.232/29',\
                                            '192.168.35.240/29','192.168.35.248/29']],\
                                        [7,['192.168.26.0/29','192.168.26.8/29','192.168.26.16/29','192.168.26.24/29','192.168.26.32/29',\
                                            '192.168.26.40/29','192.168.26.48/29','192.168.26.56/29','192.168.26.64/29','192.168.26.72/29',\
                                            '192.168.26.80/29','192.168.26.88/29','192.168.26.96/29','192.168.26.104/29','192.168.26.112/29',\
                                            '192.168.26.120/29','192.168.26.128/29','192.168.26.136/29','192.168.26.144/29','192.168.26.152/29',\
                                            '192.168.26.160/29','192.168.26.168/29','192.168.26.176/29','192.168.26.184/29','192.168.26.192/29',\
                                            '192.168.26.200/29','192.168.26.208/29','192.168.26.216/29','192.168.26.224/29','192.168.26.232/29',\
                                            '192.168.26.240/29','192.168.26.248/29',\
                                            '192.168.36.0/29','192.168.36.8/29','192.168.36.16/29','192.168.36.24/29','192.168.36.32/29',\
                                            '192.168.36.40/29','192.168.36.48/29','192.168.36.56/29','192.168.36.64/29','192.168.36.72/29',\
                                            '192.168.36.80/29','192.168.36.88/29','192.168.36.96/29','192.168.36.104/29','192.168.36.112/29',\
                                            '192.168.36.120/29','192.168.36.128/29','192.168.36.136/29','192.168.36.144/29','192.168.36.152/29',\
                                            '192.168.36.160/29','192.168.36.168/29','192.168.36.176/29','192.168.36.184/29','192.168.36.192/29',\
                                            '192.168.36.200/29','192.168.36.208/29','192.168.36.216/29','192.168.36.224/29','192.168.36.232/29',\
                                            '192.168.36.240/29','192.168.36.248/29']],\
                                        [8,['192.168.27.0/29','192.168.27.8/29','192.168.27.16/29','192.168.27.24/29','192.168.27.32/29',\
                                            '192.168.27.40/29','192.168.27.48/29','192.168.27.56/29','192.168.27.64/29','192.168.27.72/29',\
                                            '192.168.27.80/29','192.168.27.88/29','192.168.27.96/29','192.168.27.104/29','192.168.27.112/29',\
                                            '192.168.27.120/29','192.168.27.128/29','192.168.27.136/29','192.168.27.144/29','192.168.27.152/29',\
                                            '192.168.27.160/29','192.168.27.168/29','192.168.27.176/29','192.168.27.184/29','192.168.27.192/29',\
                                            '192.168.27.200/29','192.168.27.208/29','192.168.27.216/29','192.168.27.224/29','192.168.27.232/29',\
                                            '192.168.27.240/29','192.168.27.248/29',\
                                            '192.168.37.0/29','192.168.37.8/29','192.168.37.16/29','192.168.37.24/29','192.168.37.32/29',\
                                            '192.168.37.40/29','192.168.37.48/29','192.168.37.56/29','192.168.37.64/29','192.168.37.72/29',\
                                            '192.168.37.80/29','192.168.37.88/29','192.168.37.96/29','192.168.37.104/29','192.168.37.112/29',\
                                            '192.168.37.120/29','192.168.37.128/29','192.168.37.136/29','192.168.37.144/29','192.168.37.152/29',\
                                            '192.168.37.160/29','192.168.37.168/29','192.168.37.176/29','192.168.37.184/29','192.168.37.192/29',\
                                            '192.168.37.200/29','192.168.37.208/29','192.168.37.216/29','192.168.37.224/29','192.168.37.232/29',\
                                            '192.168.37.240/29','192.168.37.248/29']],\
                                        [9,['192.168.28.0/29','192.168.28.8/29','192.168.28.16/29','192.168.28.24/29','192.168.28.32/29',\
                                            '192.168.28.40/29','192.168.28.48/29','192.168.28.56/29','192.168.28.64/29','192.168.28.72/29',\
                                            '192.168.28.80/29','192.168.28.88/29','192.168.28.96/29','192.168.28.104/29','192.168.28.112/29',\
                                            '192.168.28.120/29','192.168.28.128/29','192.168.28.136/29','192.168.28.144/29','192.168.28.152/29',\
                                            '192.168.28.160/29','192.168.28.168/29','192.168.28.176/29','192.168.28.184/29','192.168.28.192/29',\
                                            '192.168.28.200/29','192.168.28.208/29','192.168.28.216/29','192.168.28.224/29','192.168.28.232/29',\
                                            '192.168.28.240/29','192.168.28.248/29',\
                                            '192.168.38.0/29','192.168.38.8/29','192.168.38.16/29','192.168.38.24/29','192.168.38.32/29',\
                                            '192.168.38.40/29','192.168.38.48/29','192.168.38.56/29','192.168.38.64/29','192.168.38.72/29',\
                                            '192.168.38.80/29','192.168.38.88/29','192.168.38.96/29','192.168.38.104/29','192.168.38.112/29',\
                                            '192.168.38.120/29','192.168.38.128/29','192.168.38.136/29','192.168.38.144/29','192.168.38.152/29',\
                                            '192.168.38.160/29','192.168.38.168/29','192.168.38.176/29','192.168.38.184/29','192.168.38.192/29',\
                                            '192.168.38.200/29','192.168.38.208/29','192.168.38.216/29','192.168.38.224/29','192.168.38.232/29',\
                                            '192.168.38.240/29','192.168.38.248/29']],\
                                        [10,['192.168.29.0/29','192.168.29.8/29','192.168.29.16/29','192.168.29.24/29','192.168.29.32/29',\
                                            '192.168.29.40/29','192.168.29.48/29','192.168.29.56/29','192.168.29.64/29','192.168.29.72/29',\
                                            '192.168.29.80/29','192.168.29.88/29','192.168.29.96/29','192.168.29.104/29','192.168.29.112/29',\
                                            '192.168.29.120/29','192.168.29.128/29','192.168.29.136/29','192.168.29.144/29','192.168.29.152/29',\
                                            '192.168.29.160/29','192.168.29.168/29','192.168.29.176/29','192.168.29.184/29','192.168.29.192/29',\
                                            '192.168.29.200/29','192.168.29.208/29','192.168.29.216/29','192.168.29.224/29','192.168.29.232/29',\
                                            '192.168.29.240/29','192.168.29.248/29',\
                                            '192.168.39.0/29','192.168.39.8/29','192.168.39.16/29','192.168.39.24/29','192.168.39.32/29',\
                                            '192.168.39.40/29','192.168.39.48/29','192.168.39.56/29','192.168.39.64/29','192.168.39.72/29',\
                                            '192.168.39.80/29','192.168.39.88/29','192.168.39.96/29','192.168.39.104/29','192.168.39.112/29',\
                                            '192.168.39.120/29','192.168.39.128/29','192.168.39.136/29','192.168.39.144/29','192.168.39.152/29',\
                                            '192.168.39.160/29','192.168.39.168/29','192.168.39.176/29','192.168.39.184/29','192.168.39.192/29',\
                                            '192.168.39.200/29','192.168.39.208/29','192.168.39.216/29','192.168.39.224/29','192.168.39.232/29',\
                                            '192.168.39.240/29','192.168.39.248/29']],\
                                        ['vrrp',['192.168.60.0/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123','192.168.22.131','192.168.22.139','192.168.22.147','192.168.22.155',\
                                            '192.168.22.163','192.168.22.171','192.168.22.179','192.168.22.187','192.168.22.195',\
                                            '192.168.22.203','192.168.22.211','192.168.22.219','192.168.22.227','192.168.22.235',\
                                            '192.168.22.243','192.168.22.251',\
                                            '192.168.32.3','192.168.32.11','192.168.32.19','192.168.32.27','192.168.32.35',\
                                            '192.168.32.43','192.168.32.51','192.168.32.59','192.168.32.67','192.168.32.75',\
                                            '192.168.32.83','192.168.32.91','192.168.32.99','192.168.32.107','192.168.32.115',\
                                            '192.168.32.123','192.168.32.131','192.168.32.139','192.168.32.147','192.168.32.155',\
                                            '192.168.32.163','192.168.32.171','192.168.32.179','192.168.32.187','192.168.32.195',\
                                            '192.168.32.203','192.168.32.211','192.168.32.219','192.168.32.227','192.168.32.235',\
                                            '192.168.32.243','192.168.32.251']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123','192.168.23.131','192.168.23.139','192.168.23.147','192.168.23.155',\
                                            '192.168.23.163','192.168.23.171','192.168.23.179','192.168.23.187','192.168.23.195',\
                                            '192.168.23.203','192.168.23.211','192.168.23.219','192.168.23.227','192.168.23.235',\
                                            '192.168.23.243','192.168.23.251',\
                                            '192.168.33.3','192.168.33.11','192.168.33.19','192.168.33.27','192.168.33.35',\
                                            '192.168.33.43','192.168.33.51','192.168.33.59','192.168.33.67','192.168.33.75',\
                                            '192.168.33.83','192.168.33.91','192.168.33.99','192.168.33.107','192.168.33.115',\
                                            '192.168.33.123','192.168.33.131','192.168.33.139','192.168.33.147','192.168.33.155',\
                                            '192.168.33.163','192.168.33.171','192.168.33.179','192.168.33.187','192.168.33.195',\
                                            '192.168.33.203','192.168.33.211','192.168.33.219','192.168.33.227','192.168.33.235',\
                                            '192.168.33.243','192.168.33.251']],\
                                        [5,['192.168.24.3','192.168.24.11','192.168.24.19','192.168.24.27','192.168.24.35',\
                                            '192.168.24.43','192.168.24.51','192.168.24.59','192.168.24.67','192.168.24.75',\
                                            '192.168.24.83','192.168.24.91','192.168.24.99','192.168.24.107','192.168.24.115',\
                                            '192.168.24.123','192.168.24.131','192.168.24.139','192.168.24.147','192.168.24.155',\
                                            '192.168.24.163','192.168.24.171','192.168.24.179','192.168.24.187','192.168.24.195',\
                                            '192.168.24.203','192.168.24.211','192.168.24.219','192.168.24.227','192.168.24.235',\
                                            '192.168.24.243','192.168.24.251',\
                                            '192.168.34.3','192.168.34.11','192.168.34.19','192.168.34.27','192.168.34.35',\
                                            '192.168.34.43','192.168.34.51','192.168.34.59','192.168.34.67','192.168.34.75',\
                                            '192.168.34.83','192.168.34.91','192.168.34.99','192.168.34.107','192.168.34.115',\
                                            '192.168.34.123','192.168.34.131','192.168.34.139','192.168.34.147','192.168.34.155',\
                                            '192.168.34.163','192.168.34.171','192.168.34.179','192.168.34.187','192.168.34.195',\
                                            '192.168.34.203','192.168.34.211','192.168.34.219','192.168.34.227','192.168.34.235',\
                                            '192.168.34.243','192.168.34.251']],\
                                        [6,['192.168.25.3','192.168.25.11','192.168.25.19','192.168.25.27','192.168.25.35',\
                                            '192.168.25.43','192.168.25.51','192.168.25.59','192.168.25.67','192.168.25.75',\
                                            '192.168.25.83','192.168.25.91','192.168.25.99','192.168.25.107','192.168.25.115',\
                                            '192.168.25.123','192.168.25.131','192.168.25.139','192.168.25.147','192.168.25.155',\
                                            '192.168.25.163','192.168.25.171','192.168.25.179','192.168.25.187','192.168.25.195',\
                                            '192.168.25.203','192.168.25.211','192.168.25.219','192.168.25.227','192.168.25.235',\
                                            '192.168.25.243','192.168.25.251',\
                                            '192.168.35.3','192.168.35.11','192.168.35.19','192.168.35.27','192.168.35.35',\
                                            '192.168.35.43','192.168.35.51','192.168.35.59','192.168.35.67','192.168.35.75',\
                                            '192.168.35.83','192.168.35.91','192.168.35.99','192.168.35.107','192.168.35.115',\
                                            '192.168.35.123','192.168.35.131','192.168.35.139','192.168.35.147','192.168.35.155',\
                                            '192.168.35.163','192.168.35.171','192.168.35.179','192.168.35.187','192.168.35.195',\
                                            '192.168.35.203','192.168.35.211','192.168.35.219','192.168.35.227','192.168.35.235',\
                                            '192.168.35.243','192.168.35.251']],\
                                        [7,['192.168.26.3','192.168.26.11','192.168.26.19','192.168.26.27','192.168.26.35',\
                                            '192.168.26.43','192.168.26.51','192.168.26.59','192.168.26.67','192.168.26.75',\
                                            '192.168.26.83','192.168.26.91','192.168.26.99','192.168.26.107','192.168.26.115',\
                                            '192.168.26.123','192.168.26.131','192.168.26.139','192.168.26.147','192.168.26.155',\
                                            '192.168.26.163','192.168.26.171','192.168.26.179','192.168.26.187','192.168.26.195',\
                                            '192.168.26.203','192.168.26.211','192.168.26.219','192.168.26.227','192.168.26.235',\
                                            '192.168.26.243','192.168.26.251',\
                                            '192.168.36.3','192.168.36.11','192.168.36.19','192.168.36.27','192.168.36.35',\
                                            '192.168.36.43','192.168.36.51','192.168.36.59','192.168.36.67','192.168.36.75',\
                                            '192.168.36.83','192.168.36.91','192.168.36.99','192.168.36.107','192.168.36.115',\
                                            '192.168.36.123','192.168.36.131','192.168.36.139','192.168.36.147','192.168.36.155',\
                                            '192.168.36.163','192.168.36.171','192.168.36.179','192.168.36.187','192.168.36.195',\
                                            '192.168.36.203','192.168.36.211','192.168.36.219','192.168.36.227','192.168.36.235',\
                                            '192.168.36.243','192.168.36.251']],\
                                        [8,['192.168.27.3','192.168.27.11','192.168.27.19','192.168.27.27','192.168.27.35',\
                                            '192.168.27.43','192.168.27.51','192.168.27.59','192.168.27.67','192.168.27.75',\
                                            '192.168.27.83','192.168.27.91','192.168.27.99','192.168.27.107','192.168.27.115',\
                                            '192.168.27.123','192.168.27.131','192.168.27.139','192.168.27.147','192.168.27.155',\
                                            '192.168.27.163','192.168.27.171','192.168.27.179','192.168.27.187','192.168.27.195',\
                                            '192.168.27.203','192.168.27.211','192.168.27.219','192.168.27.227','192.168.27.235',\
                                            '192.168.27.243','192.168.27.251',\
                                            '192.168.37.3','192.168.37.11','192.168.37.19','192.168.37.27','192.168.37.35',\
                                            '192.168.37.43','192.168.37.51','192.168.37.59','192.168.37.67','192.168.37.75',\
                                            '192.168.37.83','192.168.37.91','192.168.37.99','192.168.37.107','192.168.37.115',\
                                            '192.168.37.123','192.168.37.131','192.168.37.139','192.168.37.147','192.168.37.155',\
                                            '192.168.37.163','192.168.37.171','192.168.37.179','192.168.37.187','192.168.37.195',\
                                            '192.168.37.203','192.168.37.211','192.168.37.219','192.168.37.227','192.168.37.235',\
                                            '192.168.37.243','192.168.37.251']],\
                                        [9,['192.168.28.3','192.168.28.11','192.168.28.19','192.168.28.27','192.168.28.35',\
                                            '192.168.28.43','192.168.28.51','192.168.28.59','192.168.28.67','192.168.28.75',\
                                            '192.168.28.83','192.168.28.91','192.168.28.99','192.168.28.107','192.168.28.115',\
                                            '192.168.28.123','192.168.28.131','192.168.28.139','192.168.28.147','192.168.28.155',\
                                            '192.168.28.163','192.168.28.171','192.168.28.179','192.168.28.187','192.168.28.195',\
                                            '192.168.28.203','192.168.28.211','192.168.28.219','192.168.28.227','192.168.28.235',\
                                            '192.168.28.243','192.168.28.251',\
                                            '192.168.38.3','192.168.38.11','192.168.38.19','192.168.38.27','192.168.38.35',\
                                            '192.168.38.43','192.168.38.51','192.168.38.59','192.168.38.67','192.168.38.75',\
                                            '192.168.38.83','192.168.38.91','192.168.38.99','192.168.38.107','192.168.38.115',\
                                            '192.168.38.123','192.168.38.131','192.168.38.139','192.168.38.147','192.168.38.155',\
                                            '192.168.38.163','192.168.38.171','192.168.38.179','192.168.38.187','192.168.38.195',\
                                            '192.168.38.203','192.168.38.211','192.168.38.219','192.168.38.227','192.168.38.235',\
                                            '192.168.38.243','192.168.38.251']],\
                                        [10,['192.168.29.3','192.168.29.11','192.168.29.19','192.168.29.27','192.168.29.35',\
                                            '192.168.29.43','192.168.29.51','192.168.29.59','192.168.29.67','192.168.29.75',\
                                            '192.168.29.83','192.168.29.91','192.168.29.99','192.168.29.107','192.168.29.115',\
                                            '192.168.29.123','192.168.29.131','192.168.29.139','192.168.29.147','192.168.29.155',\
                                            '192.168.29.163','192.168.29.171','192.168.29.179','192.168.29.187','192.168.29.195',\
                                            '192.168.29.203','192.168.29.211','192.168.29.219','192.168.29.227','192.168.29.235',\
                                            '192.168.29.243','192.168.29.251',\
                                            '192.168.39.3','192.168.39.11','192.168.39.19','192.168.39.27','192.168.39.35',\
                                            '192.168.39.43','192.168.39.51','192.168.39.59','192.168.39.67','192.168.39.75',\
                                            '192.168.39.83','192.168.39.91','192.168.39.99','192.168.39.107','192.168.39.115',\
                                            '192.168.39.123','192.168.39.131','192.168.39.139','192.168.39.147','192.168.39.155',\
                                            '192.168.39.163','192.168.39.171','192.168.39.179','192.168.39.187','192.168.39.195',\
                                            '192.168.39.203','192.168.39.211','192.168.39.219','192.168.39.227','192.168.39.235',\
                                            '192.168.39.243','192.168.39.251']],\
                                        ['vrrp',['192.168.60.3/29','192.168.60.4/29','192.168.60.6']]],
                        'vip_link_gw'      : [[1,['192.168.20.1','192.168.20.2']],[2,['192.168.21.2','192.168.21.1']],[3,['192.168.22.9','192.168.22.10']],\
                                        [4,['192.168.23.10','192.168.23.9']],[5,['192.168.24.9','192.168.24.10']],[6,['192.168.25.10','192.168.25.9']],\
                                        [7,['192.168.26.9','192.168.26.10']],[8,['192.168.27.10','192.168.27.9']],[9,['192.168.28.9','192.168.28.10']],\
                                        [10,['192.168.29.10','192.168.29.9']],\
                                        ['vrrp',['192.168.60.1','192.168.60.2','192.168.60.5']]],
                        'vip_IPv6_link_gw' : [[1,['fe80::204:96ff:fe27:8743','fe80::204:96ff:fe27:891f']],\
                                        [2,['fe80::204:96ff:fe27:891f','fe80::204:96ff:fe27:8743']],\
                                        [3,['fe80::204:96ff:fe27:8743','fe80::204:96ff:fe27:891f']],\
                                        [4,['fe80::204:96ff:fe27:891f','fe80::204:96ff:fe27:8743']],\
                                        [5,['fe80::204:96ff:fe27:8743','fe80::204:96ff:fe27:891f']],\
                                        [6,['fe80::204:96ff:fe27:891f','fe80::204:96ff:fe27:8743']],\
                                        [7,['fe80::204:96ff:fe27:8743','fe80::204:96ff:fe27:891f']],\
                                        [8,['fe80::204:96ff:fe27:891f','fe80::204:96ff:fe27:8743']],\
                                        [9,['fe80::204:96ff:fe27:8743','fe80::204:96ff:fe27:891f']],\
                                        [10,['fe80::204:96ff:fe27:891f','fe80::204:96ff:fe27:8743']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.26.252',
                        'SC_2_1': '7004',
                        'SC_2_2': '7005',
                        'PL_2_3': '7006',
                        'PL_2_4': '7007',
                        'PL_2_6': '7008',
                        'PL_2_7': '7009',
                        'PL_2_8': '7010',
                        'PL_2_9': '7011',
                        'switch_1': '7001',
                        'switch_2': '7002',
                        'chassis_cmm': '7003'
                },
                'switches' : {
                        'switch_1' : "10.35.26.33",
                        'switch_2' : "10.35.26.34",
                        'portsInOrder' : [1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,\
                                        1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,\
                                        1028,1029,1030,1031,\
                                        1001,1002,1003,1004,1037,1038,1039,1040]
                }
                },
        'ports' : {
                'snmptrapd': "50003"
                }
        },

        'ebs_target_25' :  {
                'physical_size': "36",
                'execution_capacity_factor': "5.2",
                'watchdog' : 'soft',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.27.11",
                        'ctrl2' :"10.35.27.12",
                        'ctrl_if'  : ['eth',0],
                        'ctrl_net' : '10.35.27.0/24',
                        'ctrl_gw'  : '10.35.27.1',
                        'testpc':'10.35.27.15',
                        'external':['10.35.24.125','10.35.24.126','10.35.24.127','10.35.24.128'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '',
                        'bond_arp' : [['192.168.0.1','192.168.0.2']]
                },
                'traffic' : {
                        'network_IPv4' :'192.168.18.0/28',
                        'gateway_IPv4' :['192.168.18.5'],
                        'gateway_IPv6' :['fd41:4580:3405:1825:21b:21ff:fecc:ae79'],
                        'external_IPv4':['192.168.18.6','192.168.18.7','192.168.18.8','192.168.18.9'],
                        'external_IPv6':['fd41:4580:3405:1825:21b:21ff:fecc:a9f0','fd41:4580:3405:1825:21b:21ff:fecc:a778',\
                                         'fd41:4580:3405:1825:21b:21ff:fecc:a860','fd41:4580:3405:1825:21b:21ff:fecc:a560']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.25',
                        'vip_IPv4_traffic' : ['172.16.0.25','192.168.66.25','192.168.103.25','192.168.104.25','192.168.105.25',\
                                              '192.168.106.25','192.168.107.25','192.168.108.25','192.168.109.25','192.168.110.25',\
                                              '192.168.111.25','192.168.112.25','192.168.113.25','192.168.114.25','192.168.115.25',\
                                              '192.168.116.25','192.168.117.25','192.168.118.25','192.168.119.25','192.168.120.25',\
                                              '192.168.121.25','192.168.122.25','192.168.123.25','192.168.124.25','192.168.125.25',\
                                              '192.168.126.25','192.168.127.25','192.168.128.25','192.168.129.25','192.168.130.25',\
                                              '192.168.131.25','192.168.132.25','192.168.133.25','192.168.134.25','192.168.135.25',\
                                              '192.168.136.25','192.168.137.25','192.168.138.25','192.168.139.25','192.168.140.25',\
                                              '192.168.141.25','192.168.142.25','192.168.143.25','192.168.144.25','192.168.145.25',\
                                              '192.168.146.25','192.168.147.25','192.168.148.25','192.168.149.25','192.168.150.25',\
                                              '192.168.151.25','192.168.152.25','192.168.153.25','192.168.154.25','192.168.155.25',\
                                              '192.168.156.25','192.168.157.25','192.168.158.25','192.168.159.25','192.168.160.25',\
                                              '192.168.161.25','192.168.162.25','192.168.163.25','192.168.164.25'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:25','fd41:4580:3405::2:25','fd41:4580:3405::3:25','fd41:4580:3405::4:25','fd41:4580:3405::5:25',\
                                              'fd41:4580:3405::6:25','fd41:4580:3405::7:25','fd41:4580:3405::8:25','fd41:4580:3405::9:25','fd41:4580:3405::10:25',\
                                              'fd41:4580:3405::11:25','fd41:4580:3405::12:25','fd41:4580:3405::13:25','fd41:4580:3405::14:25','fd41:4580:3405::15:25',\
                                              'fd41:4580:3405::16:25','fd41:4580:3405::17:25','fd41:4580:3405::18:25','fd41:4580:3405::19:25','fd41:4580:3405::20:25',\
                                              'fd41:4580:3405::21:25','fd41:4580:3405::22:25','fd41:4580:3405::23:25','fd41:4580:3405::24:25','fd41:4580:3405::25:25',\
                                              'fd41:4580:3405::26:25','fd41:4580:3405::27:25','fd41:4580:3405::28:25','fd41:4580:3405::29:25','fd41:4580:3405::30:25',\
                                              'fd41:4580:3405::31:25','fd41:4580:3405::32:25','fd41:4580:3405::33:25','fd41:4580:3405::34:25','fd41:4580:3405::35:25',\
                                              'fd41:4580:3405::36:25','fd41:4580:3405::37:25','fd41:4580:3405::38:25','fd41:4580:3405::39:25','fd41:4580:3405::40:25',\
                                              'fd41:4580:3405::41:25','fd41:4580:3405::42:25','fd41:4580:3405::43:25','fd41:4580:3405::44:25','fd41:4580:3405::45:25',\
                                              'fd41:4580:3405::46:25','fd41:4580:3405::47:25','fd41:4580:3405::48:25','fd41:4580:3405::49:25','fd41:4580:3405::50:25',\
                                              'fd41:4580:3405::51:25','fd41:4580:3405::52:25','fd41:4580:3405::53:25','fd41:4580:3405::54:25','fd41:4580:3405::55:25',\
                                              'fd41:4580:3405::56:25','fd41:4580:3405::57:25','fd41:4580:3405::58:25','fd41:4580:3405::59:25','fd41:4580:3405::60:25',\
                                              'fd41:4580:3405::61:25','fd41:4580:3405::62:25','fd41:4580:3405::63:25','fd41:4580:3405::64:25'],
                        'vip_link_type'    : [[1,'eth_vlan',1,20],[2,'eth_vlan',1,21],\
                                        [3,'eth_vlan',1,22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172,182,192,202,\
                                           212,222,232,242,252,262,272,282,293,302,312,322,332,342,352,362,372,382,392,402,\
                                           412,422,432,442,452,462,472,482,492,502,512,522,532,542,552,562,572,582,592,602,\
                                           612,622,632,642,652],\
                                        [4,'eth_vlan',1,23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173,183,193,203,\
                                           213,223,233,243,253,263,273,283,293,303,313,323,333,343,353,363,373,383,393,403,\
                                           413,423,433,443,453,463,473,483,493,503,513,523,533,543,553,563,573,583,593,603,\
                                           613,623,633,643,653]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29','192.168.22.128/29','192.168.22.136/29','192.168.22.144/29','192.168.22.152/29',\
                                            '192.168.22.160/29','192.168.22.168/29','192.168.22.176/29','192.168.22.184/29','192.168.22.192/29',\
                                            '192.168.22.200/29','192.168.22.208/29','192.168.22.216/29','192.168.22.224/29','192.168.22.232/29',\
                                            '192.168.22.240/29','192.168.22.248/29',\
                                            '192.168.32.0/29','192.168.32.8/29','192.168.32.16/29','192.168.32.24/29','192.168.32.32/29',\
                                            '192.168.32.40/29','192.168.32.48/29','192.168.32.56/29','192.168.32.64/29','192.168.32.72/29',\
                                            '192.168.32.80/29','192.168.32.88/29','192.168.32.96/29','192.168.32.104/29','192.168.32.112/29',\
                                            '192.168.32.120/29','192.168.32.128/29','192.168.32.136/29','192.168.32.144/29','192.168.32.152/29',\
                                            '192.168.32.160/29','192.168.32.168/29','192.168.32.176/29','192.168.32.184/29','192.168.32.192/29',\
                                            '192.168.32.200/29','192.168.32.208/29','192.168.32.216/29','192.168.32.224/29','192.168.32.232/29',\
                                            '192.168.32.240/29','192.168.32.248/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29','192.168.23.128/29','192.168.23.136/29','192.168.23.144/29','192.168.23.152/29',\
                                            '192.168.23.160/29','192.168.23.168/29','192.168.23.176/29','192.168.23.184/29','192.168.23.192/29',\
                                            '192.168.23.200/29','192.168.23.208/29','192.168.23.216/29','192.168.23.224/29','192.168.23.232/29',\
                                            '192.168.23.240/29','192.168.23.248/29',\
                                            '192.168.33.0/29','192.168.33.8/29','192.168.33.16/29','192.168.33.24/29','192.168.33.32/29',\
                                            '192.168.33.40/29','192.168.33.48/29','192.168.33.56/29','192.168.33.64/29','192.168.33.72/29',\
                                            '192.168.33.80/29','192.168.33.88/29','192.168.33.96/29','192.168.33.104/29','192.168.33.112/29',\
                                            '192.168.33.120/29','192.168.33.128/29','192.168.33.136/29','192.168.33.144/29','192.168.33.152/29',\
                                            '192.168.33.160/29','192.168.33.168/29','192.168.33.176/29','192.168.33.184/29','192.168.33.192/29',\
                                            '192.168.33.200/29','192.168.33.208/29','192.168.33.216/29','192.168.33.224/29','192.168.33.232/29',\
                                            '192.168.33.240/29','192.168.33.248/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123','192.168.22.131','192.168.22.139','192.168.22.147','192.168.22.155',\
                                            '192.168.22.163','192.168.22.171','192.168.22.179','192.168.22.187','192.168.22.195',\
                                            '192.168.22.203','192.168.22.211','192.168.22.219','192.168.22.227','192.168.22.235',\
                                            '192.168.22.243','192.168.22.251',\
                                            '192.168.32.3','192.168.32.11','192.168.32.19','192.168.32.27','192.168.32.35',\
                                            '192.168.32.43','192.168.32.51','192.168.32.59','192.168.32.67','192.168.32.75',\
                                            '192.168.32.83','192.168.32.91','192.168.32.99','192.168.32.107','192.168.32.115',\
                                            '192.168.32.123','192.168.32.131','192.168.32.139','192.168.32.147','192.168.32.155',\
                                            '192.168.32.163','192.168.32.171','192.168.32.179','192.168.32.187','192.168.32.195',\
                                            '192.168.32.203','192.168.32.211','192.168.32.219','192.168.32.227','192.168.32.235',\
                                            '192.168.32.243','192.168.32.251']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123','192.168.23.131','192.168.23.139','192.168.23.147','192.168.23.155',\
                                            '192.168.23.163','192.168.23.171','192.168.23.179','192.168.23.187','192.168.23.195',\
                                            '192.168.23.203','192.168.23.211','192.168.23.219','192.168.23.227','192.168.23.235',\
                                            '192.168.23.243','192.168.23.251',\
                                            '192.168.33.3','192.168.33.11','192.168.33.19','192.168.33.27','192.168.33.35',\
                                            '192.168.33.43','192.168.33.51','192.168.33.59','192.168.33.67','192.168.33.75',\
                                            '192.168.33.83','192.168.33.91','192.168.33.99','192.168.33.107','192.168.33.115',\
                                            '192.168.33.123','192.168.33.131','192.168.33.139','192.168.33.147','192.168.33.155',\
                                            '192.168.33.163','192.168.33.171','192.168.33.179','192.168.33.187','192.168.33.195',\
                                            '192.168.33.203','192.168.33.211','192.168.33.219','192.168.33.227','192.168.33.235',\
                                            '192.168.33.243','192.168.33.251']]],
                        'vip_link_gw'      : [[1,['192.168.20.1']],[2,['192.168.21.1']],[3,['192.168.22.9']],[4,['192.168.23.9']]],
                        'vip_IPv6_link_gw' : [[1,[]],[2,[]],[3,['fe80::b']],[4,['fe80::c']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.27.2',
                        'SC_2_1': '7003',
                        'SC_2_2': '7004',
                        'PL_2_3': '7005',
                        'PL_2_4': '7006',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.27.13",
                        'switch_2' : "",
                        'portsInOrder' : []
                }
                },
        'ports' : {
                'snmptrapd': "50025"
                }
        }
        }

        if targetHw in targetData4:
                return targetData4[targetHw]
        else:
                return -1


def _setTargetHwData5(targetHw):

        targetData5 = {

        'ebs_target_26' :  {
                'physical_size': "12",
                'execution_capacity_factor': "5.2",
                'watchdog' : 'soft',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.27.21",
                        'ctrl2' :"10.35.27.22",
                        'ctrl_if'  : ['eth',0],
                        'ctrl_net' : '10.35.27.0/24',
                        'ctrl_gw'  : '10.35.27.1',
                        'testpc':'10.35.27.25',
                        'external':['10.35.24.129'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '',
                        'bond_arp' : [['192.168.0.1','192.168.0.2']]
                },
                'traffic' : {
                        'network_IPv4' :'192.168.18.16/28',
                        'gateway_IPv4' :['192.168.18.21'],
                        'gateway_IPv6' :['fd41:4580:3405:1826:a236:9fff:fe0a:60b1'],
                        'external_IPv4':['192.168.18.22'],
                        'external_IPv6':['fd41:4580:3405:1826:a236:9fff:fe0a:6a60']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.26',
                        'vip_IPv4_traffic' : ['172.16.0.26','192.168.66.26','192.168.103.26','192.168.104.26','192.168.105.26',\
                                              '192.168.106.26','192.168.107.26','192.168.108.26','192.168.109.26','192.168.110.26',\
                                              '192.168.111.26','192.168.112.26','192.168.113.26','192.168.114.26','192.168.115.26',\
                                              '192.168.116.26','192.168.117.26','192.168.118.26','192.168.119.26','192.168.120.26',\
                                              '192.168.121.26','192.168.122.26','192.168.123.26','192.168.124.26','192.168.125.26',\
                                              '192.168.126.26','192.168.127.26','192.168.128.26','192.168.129.26','192.168.130.26',\
                                              '192.168.131.26','192.168.132.26','192.168.133.26','192.168.134.26','192.168.135.26',\
                                              '192.168.136.26','192.168.137.26','192.168.138.26','192.168.139.26','192.168.140.26',\
                                              '192.168.141.26','192.168.142.26','192.168.143.26','192.168.144.26','192.168.145.26',\
                                              '192.168.146.26','192.168.147.26','192.168.148.26','192.168.149.26','192.168.150.26',\
                                              '192.168.151.26','192.168.152.26','192.168.153.26','192.168.154.26','192.168.155.26',\
                                              '192.168.156.26','192.168.157.26','192.168.158.26','192.168.159.26','192.168.160.26',\
                                              '192.168.161.26','192.168.162.26','192.168.163.26','192.168.164.26'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:26','fd41:4580:3405::2:26','fd41:4580:3405::3:26','fd41:4580:3405::4:26','fd41:4580:3405::5:26',\
                                              'fd41:4580:3405::6:26','fd41:4580:3405::7:26','fd41:4580:3405::8:26','fd41:4580:3405::9:26','fd41:4580:3405::10:26',\
                                              'fd41:4580:3405::11:26','fd41:4580:3405::12:26','fd41:4580:3405::13:26','fd41:4580:3405::14:26','fd41:4580:3405::15:26',\
                                              'fd41:4580:3405::16:26','fd41:4580:3405::17:26','fd41:4580:3405::18:26','fd41:4580:3405::19:26','fd41:4580:3405::20:26',\
                                              'fd41:4580:3405::21:26','fd41:4580:3405::22:26','fd41:4580:3405::23:26','fd41:4580:3405::24:26','fd41:4580:3405::25:26',\
                                              'fd41:4580:3405::26:26','fd41:4580:3405::27:26','fd41:4580:3405::28:26','fd41:4580:3405::29:26','fd41:4580:3405::30:26',\
                                              'fd41:4580:3405::31:26','fd41:4580:3405::32:26','fd41:4580:3405::33:26','fd41:4580:3405::34:26','fd41:4580:3405::35:26',\
                                              'fd41:4580:3405::36:26','fd41:4580:3405::37:26','fd41:4580:3405::38:26','fd41:4580:3405::39:26','fd41:4580:3405::40:26',\
                                              'fd41:4580:3405::41:26','fd41:4580:3405::42:26','fd41:4580:3405::43:26','fd41:4580:3405::44:26','fd41:4580:3405::45:26',\
                                              'fd41:4580:3405::46:26','fd41:4580:3405::47:26','fd41:4580:3405::48:26','fd41:4580:3405::49:26','fd41:4580:3405::50:26',\
                                              'fd41:4580:3405::51:26','fd41:4580:3405::52:26','fd41:4580:3405::53:26','fd41:4580:3405::54:26','fd41:4580:3405::55:26',\
                                              'fd41:4580:3405::56:26','fd41:4580:3405::57:26','fd41:4580:3405::58:26','fd41:4580:3405::59:26','fd41:4580:3405::60:26',\
                                              'fd41:4580:3405::61:26','fd41:4580:3405::62:26','fd41:4580:3405::63:26','fd41:4580:3405::64:26'],
                        'vip_link_type'    : [[1,'eth_vlan',1,20],[2,'eth_vlan',1,21],\
                                        [3,'eth_vlan',1,22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172,182,192,202,\
                                           212,222,232,242,252,262,272,282,293,302,312,322,332,342,352,362,372,382,392,402,\
                                           412,422,432,442,452,462,472,482,492,502,512,522,532,542,552,562,572,582,592,602,\
                                           612,622,632,642,652],\
                                        [4,'eth_vlan',1,23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173,183,193,203,\
                                           213,223,233,243,253,263,273,283,293,303,313,323,333,343,353,363,373,383,393,403,\
                                           413,423,433,443,453,463,473,483,493,503,513,523,533,543,553,563,573,583,593,603,\
                                           613,623,633,643,653]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29','192.168.22.128/29','192.168.22.136/29','192.168.22.144/29','192.168.22.152/29',\
                                            '192.168.22.160/29','192.168.22.168/29','192.168.22.176/29','192.168.22.184/29','192.168.22.192/29',\
                                            '192.168.22.200/29','192.168.22.208/29','192.168.22.216/29','192.168.22.224/29','192.168.22.232/29',\
                                            '192.168.22.240/29','192.168.22.248/29',\
                                            '192.168.32.0/29','192.168.32.8/29','192.168.32.16/29','192.168.32.24/29','192.168.32.32/29',\
                                            '192.168.32.40/29','192.168.32.48/29','192.168.32.56/29','192.168.32.64/29','192.168.32.72/29',\
                                            '192.168.32.80/29','192.168.32.88/29','192.168.32.96/29','192.168.32.104/29','192.168.32.112/29',\
                                            '192.168.32.120/29','192.168.32.128/29','192.168.32.136/29','192.168.32.144/29','192.168.32.152/29',\
                                            '192.168.32.160/29','192.168.32.168/29','192.168.32.176/29','192.168.32.184/29','192.168.32.192/29',\
                                            '192.168.32.200/29','192.168.32.208/29','192.168.32.216/29','192.168.32.224/29','192.168.32.232/29',\
                                            '192.168.32.240/29','192.168.32.248/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29','192.168.23.128/29','192.168.23.136/29','192.168.23.144/29','192.168.23.152/29',\
                                            '192.168.23.160/29','192.168.23.168/29','192.168.23.176/29','192.168.23.184/29','192.168.23.192/29',\
                                            '192.168.23.200/29','192.168.23.208/29','192.168.23.216/29','192.168.23.224/29','192.168.23.232/29',\
                                            '192.168.23.240/29','192.168.23.248/29',\
                                            '192.168.33.0/29','192.168.33.8/29','192.168.33.16/29','192.168.33.24/29','192.168.33.32/29',\
                                            '192.168.33.40/29','192.168.33.48/29','192.168.33.56/29','192.168.33.64/29','192.168.33.72/29',\
                                            '192.168.33.80/29','192.168.33.88/29','192.168.33.96/29','192.168.33.104/29','192.168.33.112/29',\
                                            '192.168.33.120/29','192.168.33.128/29','192.168.33.136/29','192.168.33.144/29','192.168.33.152/29',\
                                            '192.168.33.160/29','192.168.33.168/29','192.168.33.176/29','192.168.33.184/29','192.168.33.192/29',\
                                            '192.168.33.200/29','192.168.33.208/29','192.168.33.216/29','192.168.33.224/29','192.168.33.232/29',\
                                            '192.168.33.240/29','192.168.33.248/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123','192.168.22.131','192.168.22.139','192.168.22.147','192.168.22.155',\
                                            '192.168.22.163','192.168.22.171','192.168.22.179','192.168.22.187','192.168.22.195',\
                                            '192.168.22.203','192.168.22.211','192.168.22.219','192.168.22.227','192.168.22.235',\
                                            '192.168.22.243','192.168.22.251',\
                                            '192.168.32.3','192.168.32.11','192.168.32.19','192.168.32.27','192.168.32.35',\
                                            '192.168.32.43','192.168.32.51','192.168.32.59','192.168.32.67','192.168.32.75',\
                                            '192.168.32.83','192.168.32.91','192.168.32.99','192.168.32.107','192.168.32.115',\
                                            '192.168.32.123','192.168.32.131','192.168.32.139','192.168.32.147','192.168.32.155',\
                                            '192.168.32.163','192.168.32.171','192.168.32.179','192.168.32.187','192.168.32.195',\
                                            '192.168.32.203','192.168.32.211','192.168.32.219','192.168.32.227','192.168.32.235',\
                                            '192.168.32.243','192.168.32.251']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123','192.168.23.131','192.168.23.139','192.168.23.147','192.168.23.155',\
                                            '192.168.23.163','192.168.23.171','192.168.23.179','192.168.23.187','192.168.23.195',\
                                            '192.168.23.203','192.168.23.211','192.168.23.219','192.168.23.227','192.168.23.235',\
                                            '192.168.23.243','192.168.23.251',\
                                            '192.168.33.3','192.168.33.11','192.168.33.19','192.168.33.27','192.168.33.35',\
                                            '192.168.33.43','192.168.33.51','192.168.33.59','192.168.33.67','192.168.33.75',\
                                            '192.168.33.83','192.168.33.91','192.168.33.99','192.168.33.107','192.168.33.115',\
                                            '192.168.33.123','192.168.33.131','192.168.33.139','192.168.33.147','192.168.33.155',\
                                            '192.168.33.163','192.168.33.171','192.168.33.179','192.168.33.187','192.168.33.195',\
                                            '192.168.33.203','192.168.33.211','192.168.33.219','192.168.33.227','192.168.33.235',\
                                            '192.168.33.243','192.168.33.251']]],
                        'vip_link_gw'      : [[1,['192.168.20.1']],[2,['192.168.21.1']],[3,['192.168.22.9']],[4,['192.168.23.9']]],
                        'vip_IPv6_link_gw' : [[1,[]],[2,[]],[3,['fe80::b']],[4,['fe80::c']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.27.2',
                        'SC_2_1': '7015',
                        'SC_2_2': '7016',
                        'PL_2_3': '7017',
                        'PL_2_4': '7018',
                        'switch_1': '7013',
                        'switch_2': '7014'
                },
                'switches' : {
                        'switch_1' : "10.35.27.23",
                        'switch_2' : "",
                        'portsInOrder' : []
                }
                },
        'ports' : {
                'snmptrapd': "50026"
                }
        },

        'ebs_target_27' :  {
                'physical_size': "12",
                'execution_capacity_factor': "5.2",
                'watchdog' : 'soft',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.27.31",
                        'ctrl2' :"10.35.27.32",
                        'ctrl_if'  : ['eth',0],
                        'ctrl_net' : '10.35.27.0/24',
                        'ctrl_gw'  : '10.35.27.1',
                        'testpc':'10.35.27.35',
                        'external':['10.35.24.130'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '',
                        'bond_arp' : [['192.168.0.1','192.168.0.2']]
                },
                'traffic' : {
                        'network_IPv4' :'192.168.18.32/28',
                        'gateway_IPv4' :['192.168.18.37'],
                        'gateway_IPv6' :['fd41:4580:3405:1827:a236:9fff:fe0a:6541'],
                        'external_IPv4':['192.168.18.38'],
                        'external_IPv6':['fd41:4580:3405:1827:a236:9fff:fe0a:655c']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.27',
                        'vip_IPv4_traffic' : ['172.16.0.27','192.168.66.27','192.168.103.27','192.168.104.27','192.168.105.27',\
                                              '192.168.106.27','192.168.107.27','192.168.108.27','192.168.109.27','192.168.110.27',\
                                              '192.168.111.27','192.168.112.27','192.168.113.27','192.168.114.27','192.168.115.27',\
                                              '192.168.116.27','192.168.117.27','192.168.118.27','192.168.119.27','192.168.120.27',\
                                              '192.168.121.27','192.168.122.27','192.168.123.27','192.168.124.27','192.168.125.27',\
                                              '192.168.126.27','192.168.127.27','192.168.128.27','192.168.129.27','192.168.130.27',\
                                              '192.168.131.27','192.168.132.27','192.168.133.27','192.168.134.27','192.168.135.27',\
                                              '192.168.136.27','192.168.137.27','192.168.138.27','192.168.139.27','192.168.140.27',\
                                              '192.168.141.27','192.168.142.27','192.168.143.27','192.168.144.27','192.168.145.27',\
                                              '192.168.146.27','192.168.147.27','192.168.148.27','192.168.149.27','192.168.150.27',\
                                              '192.168.151.27','192.168.152.27','192.168.153.27','192.168.154.27','192.168.155.27',\
                                              '192.168.156.27','192.168.157.27','192.168.158.27','192.168.159.27','192.168.160.27',\
                                              '192.168.161.27','192.168.162.27','192.168.163.27','192.168.164.27'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:27','fd41:4580:3405::2:27','fd41:4580:3405::3:27','fd41:4580:3405::4:27','fd41:4580:3405::5:27',\
                                              'fd41:4580:3405::6:27','fd41:4580:3405::7:27','fd41:4580:3405::8:27','fd41:4580:3405::9:27','fd41:4580:3405::10:27',\
                                              'fd41:4580:3405::11:27','fd41:4580:3405::12:27','fd41:4580:3405::13:27','fd41:4580:3405::14:27','fd41:4580:3405::15:27',\
                                              'fd41:4580:3405::16:27','fd41:4580:3405::17:27','fd41:4580:3405::18:27','fd41:4580:3405::19:27','fd41:4580:3405::20:27',\
                                              'fd41:4580:3405::21:27','fd41:4580:3405::22:27','fd41:4580:3405::23:27','fd41:4580:3405::24:27','fd41:4580:3405::25:27',\
                                              'fd41:4580:3405::26:27','fd41:4580:3405::27:27','fd41:4580:3405::28:27','fd41:4580:3405::29:27','fd41:4580:3405::30:27',\
                                              'fd41:4580:3405::31:27','fd41:4580:3405::32:27','fd41:4580:3405::33:27','fd41:4580:3405::34:27','fd41:4580:3405::35:27',\
                                              'fd41:4580:3405::36:27','fd41:4580:3405::37:27','fd41:4580:3405::38:27','fd41:4580:3405::39:27','fd41:4580:3405::40:27',\
                                              'fd41:4580:3405::41:27','fd41:4580:3405::42:27','fd41:4580:3405::43:27','fd41:4580:3405::44:27','fd41:4580:3405::45:27',\
                                              'fd41:4580:3405::46:27','fd41:4580:3405::47:27','fd41:4580:3405::48:27','fd41:4580:3405::49:27','fd41:4580:3405::50:27',\
                                              'fd41:4580:3405::51:27','fd41:4580:3405::52:27','fd41:4580:3405::53:27','fd41:4580:3405::54:27','fd41:4580:3405::55:27',\
                                              'fd41:4580:3405::56:27','fd41:4580:3405::57:27','fd41:4580:3405::58:27','fd41:4580:3405::59:27','fd41:4580:3405::60:27',\
                                              'fd41:4580:3405::61:27','fd41:4580:3405::62:27','fd41:4580:3405::63:27','fd41:4580:3405::64:27'],
                        'vip_link_type'    : [[1,'eth_vlan',1,20],[2,'eth_vlan',1,21],\
                                        [3,'eth_vlan',1,22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172,182,192,202,\
                                           212,222,232,242,252,262,272,282,293,302,312,322,332,342,352,362,372,382,392,402,\
                                           412,422,432,442,452,462,472,482,492,502,512,522,532,542,552,562,572,582,592,602,\
                                           612,622,632,642,652],\
                                        [4,'eth_vlan',1,23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173,183,193,203,\
                                           213,223,233,243,253,263,273,283,293,303,313,323,333,343,353,363,373,383,393,403,\
                                           413,423,433,443,453,463,473,483,493,503,513,523,533,543,553,563,573,583,593,603,\
                                           613,623,633,643,653]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29','192.168.22.128/29','192.168.22.136/29','192.168.22.144/29','192.168.22.152/29',\
                                            '192.168.22.160/29','192.168.22.168/29','192.168.22.176/29','192.168.22.184/29','192.168.22.192/29',\
                                            '192.168.22.200/29','192.168.22.208/29','192.168.22.216/29','192.168.22.224/29','192.168.22.232/29',\
                                            '192.168.22.240/29','192.168.22.248/29',\
                                            '192.168.32.0/29','192.168.32.8/29','192.168.32.16/29','192.168.32.24/29','192.168.32.32/29',\
                                            '192.168.32.40/29','192.168.32.48/29','192.168.32.56/29','192.168.32.64/29','192.168.32.72/29',\
                                            '192.168.32.80/29','192.168.32.88/29','192.168.32.96/29','192.168.32.104/29','192.168.32.112/29',\
                                            '192.168.32.120/29','192.168.32.128/29','192.168.32.136/29','192.168.32.144/29','192.168.32.152/29',\
                                            '192.168.32.160/29','192.168.32.168/29','192.168.32.176/29','192.168.32.184/29','192.168.32.192/29',\
                                            '192.168.32.200/29','192.168.32.208/29','192.168.32.216/29','192.168.32.224/29','192.168.32.232/29',\
                                            '192.168.32.240/29','192.168.32.248/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29','192.168.23.128/29','192.168.23.136/29','192.168.23.144/29','192.168.23.152/29',\
                                            '192.168.23.160/29','192.168.23.168/29','192.168.23.176/29','192.168.23.184/29','192.168.23.192/29',\
                                            '192.168.23.200/29','192.168.23.208/29','192.168.23.216/29','192.168.23.224/29','192.168.23.232/29',\
                                            '192.168.23.240/29','192.168.23.248/29',\
                                            '192.168.33.0/29','192.168.33.8/29','192.168.33.16/29','192.168.33.24/29','192.168.33.32/29',\
                                            '192.168.33.40/29','192.168.33.48/29','192.168.33.56/29','192.168.33.64/29','192.168.33.72/29',\
                                            '192.168.33.80/29','192.168.33.88/29','192.168.33.96/29','192.168.33.104/29','192.168.33.112/29',\
                                            '192.168.33.120/29','192.168.33.128/29','192.168.33.136/29','192.168.33.144/29','192.168.33.152/29',\
                                            '192.168.33.160/29','192.168.33.168/29','192.168.33.176/29','192.168.33.184/29','192.168.33.192/29',\
                                            '192.168.33.200/29','192.168.33.208/29','192.168.33.216/29','192.168.33.224/29','192.168.33.232/29',\
                                            '192.168.33.240/29','192.168.33.248/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123','192.168.22.131','192.168.22.139','192.168.22.147','192.168.22.155',\
                                            '192.168.22.163','192.168.22.171','192.168.22.179','192.168.22.187','192.168.22.195',\
                                            '192.168.22.203','192.168.22.211','192.168.22.219','192.168.22.227','192.168.22.235',\
                                            '192.168.22.243','192.168.22.251',\
                                            '192.168.32.3','192.168.32.11','192.168.32.19','192.168.32.27','192.168.32.35',\
                                            '192.168.32.43','192.168.32.51','192.168.32.59','192.168.32.67','192.168.32.75',\
                                            '192.168.32.83','192.168.32.91','192.168.32.99','192.168.32.107','192.168.32.115',\
                                            '192.168.32.123','192.168.32.131','192.168.32.139','192.168.32.147','192.168.32.155',\
                                            '192.168.32.163','192.168.32.171','192.168.32.179','192.168.32.187','192.168.32.195',\
                                            '192.168.32.203','192.168.32.211','192.168.32.219','192.168.32.227','192.168.32.235',\
                                            '192.168.32.243','192.168.32.251']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123','192.168.23.131','192.168.23.139','192.168.23.147','192.168.23.155',\
                                            '192.168.23.163','192.168.23.171','192.168.23.179','192.168.23.187','192.168.23.195',\
                                            '192.168.23.203','192.168.23.211','192.168.23.219','192.168.23.227','192.168.23.235',\
                                            '192.168.23.243','192.168.23.251',\
                                            '192.168.33.3','192.168.33.11','192.168.33.19','192.168.33.27','192.168.33.35',\
                                            '192.168.33.43','192.168.33.51','192.168.33.59','192.168.33.67','192.168.33.75',\
                                            '192.168.33.83','192.168.33.91','192.168.33.99','192.168.33.107','192.168.33.115',\
                                            '192.168.33.123','192.168.33.131','192.168.33.139','192.168.33.147','192.168.33.155',\
                                            '192.168.33.163','192.168.33.171','192.168.33.179','192.168.33.187','192.168.33.195',\
                                            '192.168.33.203','192.168.33.211','192.168.33.219','192.168.33.227','192.168.33.235',\
                                            '192.168.33.243','192.168.33.251']]],
                        'vip_link_gw'      : [[1,['192.168.20.1']],[2,['192.168.21.1']],[3,['192.168.22.9']],[4,['192.168.23.9']]],
                        'vip_IPv6_link_gw' : [[1,[]],[2,[]],[3,['fe80::b']],[4,['fe80::c']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.27.2',
                        'SC_2_1': '7023',
                        'SC_2_2': '7024',
                        'PL_2_3': '7025',
                        'PL_2_4': '7026',
                        'switch_1': '7021',
                        'switch_2': '7022'
                },
                'switches' : {
                        'switch_1' : "10.35.27.33",
                        'switch_2' : "",
                        'portsInOrder' : []
                }
                },
        'ports' : {
                'snmptrapd': "50027"
                }
        },

        'ebs_target_28' :  {
                'physical_size': "12",
                'execution_capacity_factor': "5.2",
                'watchdog' : 'soft',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1':"10.35.27.41",
                        'ctrl2' :"10.35.27.42",
                        'ctrl_if'  : ['eth',0],
                        'ctrl_net' : '10.35.27.0/24',
                        'ctrl_gw'  : '10.35.27.1',
                        'testpc':'10.35.27.45',
                        'external':['10.35.24.131'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base' : '',
                        'bond_arp' : [['192.168.0.1','192.168.0.2']]
                },
                'traffic' : {
                        'network_IPv4' :'192.168.18.48/28',
                        'gateway_IPv4' :['192.168.18.53'],
                        'gateway_IPv6' :['fd41:4580:3405:1828:a236:9fff:fe0a:60ad'],
                        'external_IPv4':['192.168.18.54'],
                        'external_IPv6':['fd41:4580:3405:1828:a236:9fff:fe0a:64c0']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.28',
                        'vip_IPv4_traffic' : ['172.16.0.28','192.168.66.28','192.168.103.28','192.168.104.28','192.168.105.28',\
                                              '192.168.106.28','192.168.107.28','192.168.108.28','192.168.109.28','192.168.110.28',\
                                              '192.168.111.28','192.168.112.28','192.168.113.28','192.168.114.28','192.168.115.28',\
                                              '192.168.116.28','192.168.117.28','192.168.118.28','192.168.119.28','192.168.120.28',\
                                              '192.168.121.28','192.168.122.28','192.168.123.28','192.168.124.28','192.168.125.28',\
                                              '192.168.126.28','192.168.127.28','192.168.128.28','192.168.129.28','192.168.130.28',\
                                              '192.168.131.28','192.168.132.28','192.168.133.28','192.168.134.28','192.168.135.28',\
                                              '192.168.136.28','192.168.137.28','192.168.138.28','192.168.139.28','192.168.140.28',\
                                              '192.168.141.28','192.168.142.28','192.168.143.28','192.168.144.28','192.168.145.28',\
                                              '192.168.146.28','192.168.147.28','192.168.148.28','192.168.149.28','192.168.150.28',\
                                              '192.168.151.28','192.168.152.28','192.168.153.28','192.168.154.28','192.168.155.28',\
                                              '192.168.156.28','192.168.157.28','192.168.158.28','192.168.159.28','192.168.160.28',\
                                              '192.168.161.28','192.168.162.28','192.168.163.28','192.168.164.28'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:28','fd41:4580:3405::2:28','fd41:4580:3405::3:28','fd41:4580:3405::4:28','fd41:4580:3405::5:28',\
                                              'fd41:4580:3405::6:28','fd41:4580:3405::7:28','fd41:4580:3405::8:28','fd41:4580:3405::9:28','fd41:4580:3405::10:28',\
                                              'fd41:4580:3405::11:28','fd41:4580:3405::12:28','fd41:4580:3405::13:28','fd41:4580:3405::14:28','fd41:4580:3405::15:28',\
                                              'fd41:4580:3405::16:28','fd41:4580:3405::17:28','fd41:4580:3405::18:28','fd41:4580:3405::19:28','fd41:4580:3405::20:28',\
                                              'fd41:4580:3405::21:28','fd41:4580:3405::22:28','fd41:4580:3405::23:28','fd41:4580:3405::24:28','fd41:4580:3405::25:28',\
                                              'fd41:4580:3405::26:28','fd41:4580:3405::27:28','fd41:4580:3405::28:28','fd41:4580:3405::29:28','fd41:4580:3405::30:28',\
                                              'fd41:4580:3405::31:28','fd41:4580:3405::32:28','fd41:4580:3405::33:28','fd41:4580:3405::34:28','fd41:4580:3405::35:28',\
                                              'fd41:4580:3405::36:28','fd41:4580:3405::37:28','fd41:4580:3405::38:28','fd41:4580:3405::39:28','fd41:4580:3405::40:28',\
                                              'fd41:4580:3405::41:28','fd41:4580:3405::42:28','fd41:4580:3405::43:28','fd41:4580:3405::44:28','fd41:4580:3405::45:28',\
                                              'fd41:4580:3405::46:28','fd41:4580:3405::47:28','fd41:4580:3405::48:28','fd41:4580:3405::49:28','fd41:4580:3405::50:28',\
                                              'fd41:4580:3405::51:28','fd41:4580:3405::52:28','fd41:4580:3405::53:28','fd41:4580:3405::54:28','fd41:4580:3405::55:28',\
                                              'fd41:4580:3405::56:28','fd41:4580:3405::57:28','fd41:4580:3405::58:28','fd41:4580:3405::59:28','fd41:4580:3405::60:28',\
                                              'fd41:4580:3405::61:28','fd41:4580:3405::62:28','fd41:4580:3405::63:28','fd41:4580:3405::64:28'],
                        'vip_link_type'    : [[1,'eth_vlan',1,20],[2,'eth_vlan',1,21],\
                                        [3,'eth_vlan',1,22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172,182,192,202,\
                                           212,222,232,242,252,262,272,282,293,302,312,322,332,342,352,362,372,382,392,402,\
                                           412,422,432,442,452,462,472,482,492,502,512,522,532,542,552,562,572,582,592,602,\
                                           612,622,632,642,652],\
                                        [4,'eth_vlan',1,23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173,183,193,203,\
                                           213,223,233,243,253,263,273,283,293,303,313,323,333,343,353,363,373,383,393,403,\
                                           413,423,433,443,453,463,473,483,493,503,513,523,533,543,553,563,573,583,593,603,\
                                           613,623,633,643,653]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29','192.168.22.128/29','192.168.22.136/29','192.168.22.144/29','192.168.22.152/29',\
                                            '192.168.22.160/29','192.168.22.168/29','192.168.22.176/29','192.168.22.184/29','192.168.22.192/29',\
                                            '192.168.22.200/29','192.168.22.208/29','192.168.22.216/29','192.168.22.224/29','192.168.22.232/29',\
                                            '192.168.22.240/29','192.168.22.248/29',\
                                            '192.168.32.0/29','192.168.32.8/29','192.168.32.16/29','192.168.32.24/29','192.168.32.32/29',\
                                            '192.168.32.40/29','192.168.32.48/29','192.168.32.56/29','192.168.32.64/29','192.168.32.72/29',\
                                            '192.168.32.80/29','192.168.32.88/29','192.168.32.96/29','192.168.32.104/29','192.168.32.112/29',\
                                            '192.168.32.120/29','192.168.32.128/29','192.168.32.136/29','192.168.32.144/29','192.168.32.152/29',\
                                            '192.168.32.160/29','192.168.32.168/29','192.168.32.176/29','192.168.32.184/29','192.168.32.192/29',\
                                            '192.168.32.200/29','192.168.32.208/29','192.168.32.216/29','192.168.32.224/29','192.168.32.232/29',\
                                            '192.168.32.240/29','192.168.32.248/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29','192.168.23.128/29','192.168.23.136/29','192.168.23.144/29','192.168.23.152/29',\
                                            '192.168.23.160/29','192.168.23.168/29','192.168.23.176/29','192.168.23.184/29','192.168.23.192/29',\
                                            '192.168.23.200/29','192.168.23.208/29','192.168.23.216/29','192.168.23.224/29','192.168.23.232/29',\
                                            '192.168.23.240/29','192.168.23.248/29',\
                                            '192.168.33.0/29','192.168.33.8/29','192.168.33.16/29','192.168.33.24/29','192.168.33.32/29',\
                                            '192.168.33.40/29','192.168.33.48/29','192.168.33.56/29','192.168.33.64/29','192.168.33.72/29',\
                                            '192.168.33.80/29','192.168.33.88/29','192.168.33.96/29','192.168.33.104/29','192.168.33.112/29',\
                                            '192.168.33.120/29','192.168.33.128/29','192.168.33.136/29','192.168.33.144/29','192.168.33.152/29',\
                                            '192.168.33.160/29','192.168.33.168/29','192.168.33.176/29','192.168.33.184/29','192.168.33.192/29',\
                                            '192.168.33.200/29','192.168.33.208/29','192.168.33.216/29','192.168.33.224/29','192.168.33.232/29',\
                                            '192.168.33.240/29','192.168.33.248/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123','192.168.22.131','192.168.22.139','192.168.22.147','192.168.22.155',\
                                            '192.168.22.163','192.168.22.171','192.168.22.179','192.168.22.187','192.168.22.195',\
                                            '192.168.22.203','192.168.22.211','192.168.22.219','192.168.22.227','192.168.22.235',\
                                            '192.168.22.243','192.168.22.251',\
                                            '192.168.32.3','192.168.32.11','192.168.32.19','192.168.32.27','192.168.32.35',\
                                            '192.168.32.43','192.168.32.51','192.168.32.59','192.168.32.67','192.168.32.75',\
                                            '192.168.32.83','192.168.32.91','192.168.32.99','192.168.32.107','192.168.32.115',\
                                            '192.168.32.123','192.168.32.131','192.168.32.139','192.168.32.147','192.168.32.155',\
                                            '192.168.32.163','192.168.32.171','192.168.32.179','192.168.32.187','192.168.32.195',\
                                            '192.168.32.203','192.168.32.211','192.168.32.219','192.168.32.227','192.168.32.235',\
                                            '192.168.32.243','192.168.32.251']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123','192.168.23.131','192.168.23.139','192.168.23.147','192.168.23.155',\
                                            '192.168.23.163','192.168.23.171','192.168.23.179','192.168.23.187','192.168.23.195',\
                                            '192.168.23.203','192.168.23.211','192.168.23.219','192.168.23.227','192.168.23.235',\
                                            '192.168.23.243','192.168.23.251',\
                                            '192.168.33.3','192.168.33.11','192.168.33.19','192.168.33.27','192.168.33.35',\
                                            '192.168.33.43','192.168.33.51','192.168.33.59','192.168.33.67','192.168.33.75',\
                                            '192.168.33.83','192.168.33.91','192.168.33.99','192.168.33.107','192.168.33.115',\
                                            '192.168.33.123','192.168.33.131','192.168.33.139','192.168.33.147','192.168.33.155',\
                                            '192.168.33.163','192.168.33.171','192.168.33.179','192.168.33.187','192.168.33.195',\
                                            '192.168.33.203','192.168.33.211','192.168.33.219','192.168.33.227','192.168.33.235',\
                                            '192.168.33.243','192.168.33.251']]],
                        'vip_link_gw'      : [[1,['192.168.20.1']],[2,['192.168.21.1']],[3,['192.168.22.9']],[4,['192.168.23.9']]],
                        'vip_IPv6_link_gw' : [[1,[]],[2,[]],[3,['fe80::b']],[4,['fe80::c']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.27.2',
                        'SC_2_1': '7031',
                        'SC_2_2': '7032',
                        'PL_2_3': '7033',
                        'PL_2_4': '7034',
                        'switch_1': '7029',
                        'switch_2': '7030'
                },
                'switches' : {
                        'switch_1' : "10.35.27.43",
                        'switch_2' : "",
                        'portsInOrder' : []
                }
                },
        'ports' : {
                'snmptrapd': "50028"
                }
        },

        'cots_target_12' :  {
                'physical_size': "70",
                'execution_capacity_factor': "1.8",
                'watchdog' : 'ipmi',
                'ipAddress' : {
                'ctrl' : {
                        'ctrl1' :"10.35.26.121",
                        'ctrl2' :"10.35.26.122",
                        'ctrl_if'  : ['eth',5],
                        'ctrl_net' : '10.35.26.0/24',
                        'ctrl_gw'  : '10.35.26.1',
                        'testpc': '10.35.26.125',
                        'external':['10.35.24.113','10.35.24.114','10.35.24.115','10.35.24.116'],
                        'internal_net': ['192.168.0.0','24'],
                        'ipmi_base': '192.168.0.100',
                        'bond_arp' : [['192.168.0.243','192.168.0.244']]
                },
                'traffic' : {
                        'network_IPv4' :'192.168.17.0/24',
                        'gateway_IPv4' :['192.168.17.125'],
                        'gateway_IPv6' :['2011:4580:3405:17:215:17ff:fea9:c9ff'],
                        'external_IPv4':['192.168.17.138','192.168.17.148','192.168.17.158','192.168.17.168'],
                        'external_IPv6':['2011:4580:3405:17:210:18ff:fe33:364','2011:4580:3405:17:210:18ff:fe33:3c6',\
                                        '2011:4580:3405:17:210:18ff:fe33:36a','2011:4580:3405:17:210:18ff:fe33:36b']
                },
                'vip'  : {
                        'vip_IPv4_OAM'     : '10.35.42.12',
                        'vip_IPv4_traffic' : ['172.16.0.12','192.168.66.12','192.168.103.12','192.168.104.12','192.168.105.12',\
                                              '192.168.106.12','192.168.107.12','192.168.108.12','192.168.109.12','192.168.110.12',\
                                              '192.168.111.12','192.168.112.12','192.168.113.12','192.168.114.12','192.168.115.12',\
                                              '192.168.116.12','192.168.117.12','192.168.118.12','192.168.119.12','192.168.120.12',\
                                              '192.168.121.12','192.168.122.12','192.168.123.12','192.168.124.12','192.168.125.12',\
                                              '192.168.126.12','192.168.127.12','192.168.128.12','192.168.129.12','192.168.130.12',\
                                              '192.168.131.12','192.168.132.12','192.168.133.12','192.168.134.12','192.168.135.12',\
                                              '192.168.136.12','192.168.137.12','192.168.138.12','192.168.139.12','192.168.140.12',\
                                              '192.168.141.12','192.168.142.12','192.168.143.12','192.168.144.12','192.168.145.12',\
                                              '192.168.146.12','192.168.147.12','192.168.148.12','192.168.149.12','192.168.150.12',\
                                              '192.168.151.12','192.168.152.12','192.168.153.12','192.168.154.12','192.168.155.12',\
                                              '192.168.156.12','192.168.157.12','192.168.158.12','192.168.159.12','192.168.160.12',\
                                              '192.168.161.12','192.168.162.12','192.168.163.12','192.168.164.12'],
                        'vip_IPv6_traffic' : ['fd41:4580:3405::1:12','fd41:4580:3405::2:12','fd41:4580:3405::3:12','fd41:4580:3405::4:12','fd41:4580:3405::5:12',\
                                              'fd41:4580:3405::6:12','fd41:4580:3405::7:12','fd41:4580:3405::8:12','fd41:4580:3405::9:12','fd41:4580:3405::10:12',\
                                              'fd41:4580:3405::11:12','fd41:4580:3405::12:12','fd41:4580:3405::13:12','fd41:4580:3405::14:12','fd41:4580:3405::15:12',\
                                              'fd41:4580:3405::16:12','fd41:4580:3405::17:12','fd41:4580:3405::18:12','fd41:4580:3405::19:12','fd41:4580:3405::20:12',\
                                              'fd41:4580:3405::21:12','fd41:4580:3405::22:12','fd41:4580:3405::23:12','fd41:4580:3405::24:12','fd41:4580:3405::25:12',\
                                              'fd41:4580:3405::26:12','fd41:4580:3405::27:12','fd41:4580:3405::28:12','fd41:4580:3405::29:12','fd41:4580:3405::30:12',\
                                              'fd41:4580:3405::31:12','fd41:4580:3405::32:12','fd41:4580:3405::33:12','fd41:4580:3405::34:12','fd41:4580:3405::35:12',\
                                              'fd41:4580:3405::36:12','fd41:4580:3405::37:12','fd41:4580:3405::38:12','fd41:4580:3405::39:12','fd41:4580:3405::40:12',\
                                              'fd41:4580:3405::41:12','fd41:4580:3405::42:12','fd41:4580:3405::43:12','fd41:4580:3405::44:12','fd41:4580:3405::45:12',\
                                              'fd41:4580:3405::46:12','fd41:4580:3405::47:12','fd41:4580:3405::48:12','fd41:4580:3405::49:12','fd41:4580:3405::50:12',\
                                              'fd41:4580:3405::51:12','fd41:4580:3405::52:12','fd41:4580:3405::53:12','fd41:4580:3405::54:12','fd41:4580:3405::55:12',\
                                              'fd41:4580:3405::56:12','fd41:4580:3405::57:12','fd41:4580:3405::58:12','fd41:4580:3405::59:12','fd41:4580:3405::60:12',\
                                              'fd41:4580:3405::61:12','fd41:4580:3405::62:12','fd41:4580:3405::63:12','fd41:4580:3405::64:12'],
                        'vip_link_type'    : [[1,'bond_vlan',20],[2,'bond_vlan',21],\
                                        [3,'bond_vlan',22,32,42,52,62,72,82,92,102,112,122,132,142,152,162,172,182,192,202,\
                                           212,222,232,242,252,262,272,282,293,302,312,322,332,342,352,362,372,382,392,402,\
                                           412,422,432,442,452,462,472,482,492,502,512,522,532,542,552,562,572,582,592,602,\
                                           612,622,632,642,652],\
                                        [4,'bond_vlan',23,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173,183,193,203,\
                                           213,223,233,243,253,263,273,283,293,303,313,323,333,343,353,363,373,383,393,403,\
                                           413,423,433,443,453,463,473,483,493,503,513,523,533,543,553,563,573,583,593,603,\
                                           613,623,633,643,653],\
                                        [5,'bond_vlan',24,34,44,54,64,74,84,94,104,114,124,134,144,154,164,174,184,194,204,\
                                           214,224,234,244,254,264,274,284,294,304,314,324,334,344,354,364,374,384,394,404,\
                                           414,424,434,444,454,464,474,484,494,504,514,524,534,544,554,564,574,584,594,604,\
                                           614,624,634,644,654],\
                                        [30,'bond_vlan',25,35,45,55,65,75,85,95,105,115,125,135,145,155,165,175,185,195,205,\
                                           215,225,235,245,255,265,275,285,295,305,315,325,335,345,355,365,375,385,395,405,\
                                           415,425,435,445,455,465,475,485,495,505,515,525,535,545,555,565,575,585,595,605,\
                                           615,625,635,645,655],\
                                        [31,'bond_vlan',26,36,46,56,66,76,86,96,106,116,126,136,146,156,166,176,186,196,206,\
                                           216,226,236,246,256,266,276,286,296,306,316,326,336,346,356,366,376,386,396,406,\
                                           416,426,436,446,456,466,476,486,496,506,516,526,536,546,556,566,576,586,596,606,\
                                           616,626,636,646,656],\
                                        [32,'bond_vlan',27,37,47,57,67,77,87,97,107,117,127,137,147,157,167,177,187,197,207,\
                                           217,227,237,247,257,267,277,287,297,307,317,327,337,347,357,367,377,387,397,407,\
                                           417,427,437,447,457,467,477,487,497,507,517,527,537,547,557,567,577,587,597,607,\
                                           617,627,637,647,657],\
                                        ['vrrp','bond_vlan',1400]],
                        'vip_link_net'     : [[1,['192.168.20.0/29']],[2,['192.168.21.0/29']],\
                                        [3,['192.168.22.0/29','192.168.22.8/29','192.168.22.16/29','192.168.22.24/29','192.168.22.32/29',\
                                            '192.168.22.40/29','192.168.22.48/29','192.168.22.56/29','192.168.22.64/29','192.168.22.72/29',\
                                            '192.168.22.80/29','192.168.22.88/29','192.168.22.96/29','192.168.22.104/29','192.168.22.112/29',\
                                            '192.168.22.120/29','192.168.22.128/29','192.168.22.136/29','192.168.22.144/29','192.168.22.152/29',\
                                            '192.168.22.160/29','192.168.22.168/29','192.168.22.176/29','192.168.22.184/29','192.168.22.192/29',\
                                            '192.168.22.200/29','192.168.22.208/29','192.168.22.216/29','192.168.22.224/29','192.168.22.232/29',\
                                            '192.168.22.240/29','192.168.22.248/29',\
                                            '192.168.32.0/29','192.168.32.8/29','192.168.32.16/29','192.168.32.24/29','192.168.32.32/29',\
                                            '192.168.32.40/29','192.168.32.48/29','192.168.32.56/29','192.168.32.64/29','192.168.32.72/29',\
                                            '192.168.32.80/29','192.168.32.88/29','192.168.32.96/29','192.168.32.104/29','192.168.32.112/29',\
                                            '192.168.32.120/29','192.168.32.128/29','192.168.32.136/29','192.168.32.144/29','192.168.32.152/29',\
                                            '192.168.32.160/29','192.168.32.168/29','192.168.32.176/29','192.168.32.184/29','192.168.32.192/29',\
                                            '192.168.32.200/29','192.168.32.208/29','192.168.32.216/29','192.168.32.224/29','192.168.32.232/29',\
                                            '192.168.32.240/29','192.168.32.248/29']],\
                                        [4,['192.168.23.0/29','192.168.23.8/29','192.168.23.16/29','192.168.23.24/29','192.168.23.32/29',\
                                            '192.168.23.40/29','192.168.23.48/29','192.168.23.56/29','192.168.23.64/29','192.168.23.72/29',\
                                            '192.168.23.80/29','192.168.23.88/29','192.168.23.96/29','192.168.23.104/29','192.168.23.112/29',\
                                            '192.168.23.120/29','192.168.23.128/29','192.168.23.136/29','192.168.23.144/29','192.168.23.152/29',\
                                            '192.168.23.160/29','192.168.23.168/29','192.168.23.176/29','192.168.23.184/29','192.168.23.192/29',\
                                            '192.168.23.200/29','192.168.23.208/29','192.168.23.216/29','192.168.23.224/29','192.168.23.232/29',\
                                            '192.168.23.240/29','192.168.23.248/29',\
                                            '192.168.33.0/29','192.168.33.8/29','192.168.33.16/29','192.168.33.24/29','192.168.33.32/29',\
                                            '192.168.33.40/29','192.168.33.48/29','192.168.33.56/29','192.168.33.64/29','192.168.33.72/29',\
                                            '192.168.33.80/29','192.168.33.88/29','192.168.33.96/29','192.168.33.104/29','192.168.33.112/29',\
                                            '192.168.33.120/29','192.168.33.128/29','192.168.33.136/29','192.168.33.144/29','192.168.33.152/29',\
                                            '192.168.33.160/29','192.168.33.168/29','192.168.33.176/29','192.168.33.184/29','192.168.33.192/29',\
                                            '192.168.33.200/29','192.168.33.208/29','192.168.33.216/29','192.168.33.224/29','192.168.33.232/29',\
                                            '192.168.33.240/29','192.168.33.248/29']],\
                                        [5,['192.168.24.0/29','192.168.24.8/29','192.168.24.16/29','192.168.24.24/29','192.168.24.32/29',\
                                            '192.168.24.40/29','192.168.24.48/29','192.168.24.56/29','192.168.24.64/29','192.168.24.72/29',\
                                            '192.168.24.80/29','192.168.24.88/29','192.168.24.96/29','192.168.24.104/29','192.168.24.112/29',\
                                            '192.168.24.120/29','192.168.24.128/29','192.168.24.136/29','192.168.24.144/29','192.168.24.152/29',\
                                            '192.168.24.160/29','192.168.24.168/29','192.168.24.176/29','192.168.24.184/29','192.168.24.192/29',\
                                            '192.168.24.200/29','192.168.24.208/29','192.168.24.216/29','192.168.24.224/29','192.168.24.232/29',\
                                            '192.168.24.240/29','192.168.24.248/29',\
                                            '192.168.34.0/29','192.168.34.8/29','192.168.34.16/29','192.168.34.24/29','192.168.34.32/29',\
                                            '192.168.34.40/29','192.168.34.48/29','192.168.34.56/29','192.168.34.64/29','192.168.34.72/29',\
                                            '192.168.34.80/29','192.168.34.88/29','192.168.34.96/29','192.168.34.104/29','192.168.34.112/29',\
                                            '192.168.34.120/29','192.168.34.128/29','192.168.34.136/29','192.168.34.144/29','192.168.34.152/29',\
                                            '192.168.34.160/29','192.168.34.168/29','192.168.34.176/29','192.168.34.184/29','192.168.34.192/29',\
                                            '192.168.34.200/29','192.168.34.208/29','192.168.34.216/29','192.168.34.224/29','192.168.34.232/29',\
                                            '192.168.34.240/29','192.168.34.248/29']],\
                                        [30,['192.168.25.0/29','192.168.25.8/29','192.168.25.16/29','192.168.25.24/29','192.168.25.32/29',\
                                            '192.168.25.40/29','192.168.25.48/29','192.168.25.56/29','192.168.25.64/29','192.168.25.72/29',\
                                            '192.168.25.80/29','192.168.25.88/29','192.168.25.96/29','192.168.25.104/29','192.168.25.112/29',\
                                            '192.168.25.120/29','192.168.25.128/29','192.168.25.136/29','192.168.25.144/29','192.168.25.152/29',\
                                            '192.168.25.160/29','192.168.25.168/29','192.168.25.176/29','192.168.25.184/29','192.168.25.192/29',\
                                            '192.168.25.200/29','192.168.25.208/29','192.168.25.216/29','192.168.25.224/29','192.168.25.232/29',\
                                            '192.168.25.240/29','192.168.25.248/29',\
                                            '192.168.35.0/29','192.168.35.8/29','192.168.35.16/29','192.168.35.24/29','192.168.35.32/29',\
                                            '192.168.35.40/29','192.168.35.48/29','192.168.35.56/29','192.168.35.64/29','192.168.35.72/29',\
                                            '192.168.35.80/29','192.168.35.88/29','192.168.35.96/29','192.168.35.104/29','192.168.35.112/29',\
                                            '192.168.35.120/29','192.168.35.128/29','192.168.35.136/29','192.168.35.144/29','192.168.35.152/29',\
                                            '192.168.35.160/29','192.168.35.168/29','192.168.35.176/29','192.168.35.184/29','192.168.35.192/29',\
                                            '192.168.35.200/29','192.168.35.208/29','192.168.35.216/29','192.168.35.224/29','192.168.35.232/29',\
                                            '192.168.35.240/29','192.168.35.248/29']],\
                                        [31,['192.168.26.0/29','192.168.26.8/29','192.168.26.16/29','192.168.26.24/29','192.168.26.32/29',\
                                            '192.168.26.40/29','192.168.26.48/29','192.168.26.56/29','192.168.26.64/29','192.168.26.72/29',\
                                            '192.168.26.80/29','192.168.26.88/29','192.168.26.96/29','192.168.26.104/29','192.168.26.112/29',\
                                            '192.168.26.120/29','192.168.26.128/29','192.168.26.136/29','192.168.26.144/29','192.168.26.152/29',\
                                            '192.168.26.160/29','192.168.26.168/29','192.168.26.176/29','192.168.26.184/29','192.168.26.192/29',\
                                            '192.168.26.200/29','192.168.26.208/29','192.168.26.216/29','192.168.26.224/29','192.168.26.232/29',\
                                            '192.168.26.240/29','192.168.26.248/29',\
                                            '192.168.36.0/29','192.168.36.8/29','192.168.36.16/29','192.168.36.24/29','192.168.36.32/29',\
                                            '192.168.36.40/29','192.168.36.48/29','192.168.36.56/29','192.168.36.64/29','192.168.36.72/29',\
                                            '192.168.36.80/29','192.168.36.88/29','192.168.36.96/29','192.168.36.104/29','192.168.36.112/29',\
                                            '192.168.36.120/29','192.168.36.128/29','192.168.36.136/29','192.168.36.144/29','192.168.36.152/29',\
                                            '192.168.36.160/29','192.168.36.168/29','192.168.36.176/29','192.168.36.184/29','192.168.36.192/29',\
                                            '192.168.36.200/29','192.168.36.208/29','192.168.36.216/29','192.168.36.224/29','192.168.36.232/29',\
                                            '192.168.36.240/29','192.168.36.248/29']],\
                                        [32,['192.168.27.0/29','192.168.27.8/29','192.168.27.16/29','192.168.27.24/29','192.168.27.32/29',\
                                            '192.168.27.40/29','192.168.27.48/29','192.168.27.56/29','192.168.27.64/29','192.168.27.72/29',\
                                            '192.168.27.80/29','192.168.27.88/29','192.168.27.96/29','192.168.27.104/29','192.168.27.112/29',\
                                            '192.168.27.120/29','192.168.27.128/29','192.168.27.136/29','192.168.27.144/29','192.168.27.152/29',\
                                            '192.168.27.160/29','192.168.27.168/29','192.168.27.176/29','192.168.27.184/29','192.168.27.192/29',\
                                            '192.168.27.200/29','192.168.27.208/29','192.168.27.216/29','192.168.27.224/29','192.168.27.232/29',\
                                            '192.168.27.240/29','192.168.27.248/29',\
                                            '192.168.37.0/29','192.168.37.8/29','192.168.37.16/29','192.168.37.24/29','192.168.37.32/29',\
                                            '192.168.37.40/29','192.168.37.48/29','192.168.37.56/29','192.168.37.64/29','192.168.37.72/29',\
                                            '192.168.37.80/29','192.168.37.88/29','192.168.37.96/29','192.168.37.104/29','192.168.37.112/29',\
                                            '192.168.37.120/29','192.168.37.128/29','192.168.37.136/29','192.168.37.144/29','192.168.37.152/29',\
                                            '192.168.37.160/29','192.168.37.168/29','192.168.37.176/29','192.168.37.184/29','192.168.37.192/29',\
                                            '192.168.37.200/29','192.168.37.208/29','192.168.37.216/29','192.168.37.224/29','192.168.37.232/29',\
                                            '192.168.37.240/29','192.168.37.248/29']],\
                                        ['vrrp',['192.168.60.0/29']]],
                        'vip_link_addr'    : [[1,['192.168.20.3']],[2,['192.168.21.3']],\
                                        [3,['192.168.22.3','192.168.22.11','192.168.22.19','192.168.22.27','192.168.22.35',\
                                            '192.168.22.43','192.168.22.51','192.168.22.59','192.168.22.67','192.168.22.75',\
                                            '192.168.22.83','192.168.22.91','192.168.22.99','192.168.22.107','192.168.22.115',\
                                            '192.168.22.123','192.168.22.131','192.168.22.139','192.168.22.147','192.168.22.155',\
                                            '192.168.22.163','192.168.22.171','192.168.22.179','192.168.22.187','192.168.22.195',\
                                            '192.168.22.203','192.168.22.211','192.168.22.219','192.168.22.227','192.168.22.235',\
                                            '192.168.22.243','192.168.22.251',\
                                            '192.168.32.3','192.168.32.11','192.168.32.19','192.168.32.27','192.168.32.35',\
                                            '192.168.32.43','192.168.32.51','192.168.32.59','192.168.32.67','192.168.32.75',\
                                            '192.168.32.83','192.168.32.91','192.168.32.99','192.168.32.107','192.168.32.115',\
                                            '192.168.32.123','192.168.32.131','192.168.32.139','192.168.32.147','192.168.32.155',\
                                            '192.168.32.163','192.168.32.171','192.168.32.179','192.168.32.187','192.168.32.195',\
                                            '192.168.32.203','192.168.32.211','192.168.32.219','192.168.32.227','192.168.32.235',\
                                            '192.168.32.243','192.168.32.251']],\
                                        [4,['192.168.23.3','192.168.23.11','192.168.23.19','192.168.23.27','192.168.23.35',\
                                            '192.168.23.43','192.168.23.51','192.168.23.59','192.168.23.67','192.168.23.75',\
                                            '192.168.23.83','192.168.23.91','192.168.23.99','192.168.23.107','192.168.23.115',\
                                            '192.168.23.123','192.168.23.131','192.168.23.139','192.168.23.147','192.168.23.155',\
                                            '192.168.23.163','192.168.23.171','192.168.23.179','192.168.23.187','192.168.23.195',\
                                            '192.168.23.203','192.168.23.211','192.168.23.219','192.168.23.227','192.168.23.235',\
                                            '192.168.23.243','192.168.23.251',\
                                            '192.168.33.3','192.168.33.11','192.168.33.19','192.168.33.27','192.168.33.35',\
                                            '192.168.33.43','192.168.33.51','192.168.33.59','192.168.33.67','192.168.33.75',\
                                            '192.168.33.83','192.168.33.91','192.168.33.99','192.168.33.107','192.168.33.115',\
                                            '192.168.33.123','192.168.33.131','192.168.33.139','192.168.33.147','192.168.33.155',\
                                            '192.168.33.163','192.168.33.171','192.168.33.179','192.168.33.187','192.168.33.195',\
                                            '192.168.33.203','192.168.33.211','192.168.33.219','192.168.33.227','192.168.33.235',\
                                            '192.168.33.243','192.168.33.251']],\
                                        [5,['192.168.24.3','192.168.24.11','192.168.24.19','192.168.24.27','192.168.24.35',\
                                            '192.168.24.43','192.168.24.51','192.168.24.59','192.168.24.67','192.168.24.75',\
                                            '192.168.24.83','192.168.24.91','192.168.24.99','192.168.24.107','192.168.24.115',\
                                            '192.168.24.123','192.168.24.131','192.168.24.139','192.168.24.147','192.168.24.155',\
                                            '192.168.24.163','192.168.24.171','192.168.24.179','192.168.24.187','192.168.24.195',\
                                            '192.168.24.203','192.168.24.211','192.168.24.219','192.168.24.227','192.168.24.235',\
                                            '192.168.24.243','192.168.24.251',\
                                            '192.168.34.3','192.168.34.11','192.168.34.19','192.168.34.27','192.168.34.35',\
                                            '192.168.34.43','192.168.34.51','192.168.34.59','192.168.34.67','192.168.34.75',\
                                            '192.168.34.83','192.168.34.91','192.168.34.99','192.168.34.107','192.168.34.115',\
                                            '192.168.34.123','192.168.34.131','192.168.34.139','192.168.34.147','192.168.34.155',\
                                            '192.168.34.163','192.168.34.171','192.168.34.179','192.168.34.187','192.168.34.195',\
                                            '192.168.34.203','192.168.34.211','192.168.34.219','192.168.34.227','192.168.34.235',\
                                            '192.168.34.243','192.168.34.251']],\
                                        [30,['192.168.25.3','192.168.25.11','192.168.25.19','192.168.25.27','192.168.25.35',\
                                            '192.168.25.43','192.168.25.51','192.168.25.59','192.168.25.67','192.168.25.75',\
                                            '192.168.25.83','192.168.25.91','192.168.25.99','192.168.25.107','192.168.25.115',\
                                            '192.168.25.123','192.168.25.131','192.168.25.139','192.168.25.147','192.168.25.155',\
                                            '192.168.25.163','192.168.25.171','192.168.25.179','192.168.25.187','192.168.25.195',\
                                            '192.168.25.203','192.168.25.211','192.168.25.219','192.168.25.227','192.168.25.235',\
                                            '192.168.25.243','192.168.25.251',\
                                            '192.168.35.3','192.168.35.11','192.168.35.19','192.168.35.27','192.168.35.35',\
                                            '192.168.35.43','192.168.35.51','192.168.35.59','192.168.35.67','192.168.35.75',\
                                            '192.168.35.83','192.168.35.91','192.168.35.99','192.168.35.107','192.168.35.115',\
                                            '192.168.35.123','192.168.35.131','192.168.35.139','192.168.35.147','192.168.35.155',\
                                            '192.168.35.163','192.168.35.171','192.168.35.179','192.168.35.187','192.168.35.195',\
                                            '192.168.35.203','192.168.35.211','192.168.35.219','192.168.35.227','192.168.35.235',\
                                            '192.168.35.243','192.168.35.251']],\
                                        [31,['192.168.26.3','192.168.26.11','192.168.26.19','192.168.26.27','192.168.26.35',\
                                            '192.168.26.43','192.168.26.51','192.168.26.59','192.168.26.67','192.168.26.75',\
                                            '192.168.26.83','192.168.26.91','192.168.26.99','192.168.26.107','192.168.26.115',\
                                            '192.168.26.123','192.168.26.131','192.168.26.139','192.168.26.147','192.168.26.155',\
                                            '192.168.26.163','192.168.26.171','192.168.26.179','192.168.26.187','192.168.26.195',\
                                            '192.168.26.203','192.168.26.211','192.168.26.219','192.168.26.227','192.168.26.235',\
                                            '192.168.26.243','192.168.26.251',\
                                            '192.168.36.3','192.168.36.11','192.168.36.19','192.168.36.27','192.168.36.35',\
                                            '192.168.36.43','192.168.36.51','192.168.36.59','192.168.36.67','192.168.36.75',\
                                            '192.168.36.83','192.168.36.91','192.168.36.99','192.168.36.107','192.168.36.115',\
                                            '192.168.36.123','192.168.36.131','192.168.36.139','192.168.36.147','192.168.36.155',\
                                            '192.168.36.163','192.168.36.171','192.168.36.179','192.168.36.187','192.168.36.195',\
                                            '192.168.36.203','192.168.36.211','192.168.36.219','192.168.36.227','192.168.36.235',\
                                            '192.168.36.243','192.168.36.251']],\
                                        [32,['192.168.27.3','192.168.27.11','192.168.27.19','192.168.27.27','192.168.27.35',\
                                            '192.168.27.43','192.168.27.51','192.168.27.59','192.168.27.67','192.168.27.75',\
                                            '192.168.27.83','192.168.27.91','192.168.27.99','192.168.27.107','192.168.27.115',\
                                            '192.168.27.123','192.168.27.131','192.168.27.139','192.168.27.147','192.168.27.155',\
                                            '192.168.27.163','192.168.27.171','192.168.27.179','192.168.27.187','192.168.27.195',\
                                            '192.168.27.203','192.168.27.211','192.168.27.219','192.168.27.227','192.168.27.235',\
                                            '192.168.27.243','192.168.27.251',\
                                            '192.168.37.3','192.168.37.11','192.168.37.19','192.168.37.27','192.168.37.35',\
                                            '192.168.37.43','192.168.37.51','192.168.37.59','192.168.37.67','192.168.37.75',\
                                            '192.168.37.83','192.168.37.91','192.168.37.99','192.168.37.107','192.168.37.115',\
                                            '192.168.37.123','192.168.37.131','192.168.37.139','192.168.37.147','192.168.37.155',\
                                            '192.168.37.163','192.168.37.171','192.168.37.179','192.168.37.187','192.168.37.195',\
                                            '192.168.37.203','192.168.37.211','192.168.37.219','192.168.37.227','192.168.37.235',\
                                            '192.168.37.243','192.168.37.251']],\
                                        ['vrrp',['192.168.60.3/29','192.168.60.4/29','192.168.60.6']]],
                        'vip_link_gw'      : [[1,['192.168.20.1','192.168.20.2']],[2,['192.168.21.2','192.168.21.1']],\
                                        [3,['192.168.22.9','192.168.22.10']],[4,['192.168.23.10','192.168.23.9']],[5,['192.168.24.9','192.168.24.10']],\
                                        [30,['192.168.25.10','192.168.25.9']],[31,['192.168.26.9','192.168.26.10']],[32,['192.168.27.10','192.168.27.9']],\
                                        ['vrrp',['192.168.60.1','192.168.60.2','192.168.60.5']]],
                        'vip_IPv6_link_gw' : [[1,['fe80::204:96ff:fe27:9089','fe80::204:96ff:fe35:2973']],\
                                        [2,['fe80::204:96ff:fe35:2973','fe80::204:96ff:fe27:9089']],\
                                        [3,['fe80::204:96ff:fe27:9089','fe80::204:96ff:fe35:2973']],\
                                        [4,['fe80::204:96ff:fe35:2973','fe80::204:96ff:fe27:9089']],\
                                        [5,['fe80::204:96ff:fe27:9089','fe80::204:96ff:fe35:2973']],\
                                        [30,['fe80::204:96ff:fe35:2973','fe80::204:96ff:fe27:9089']],\
                                        [31,['fe80::204:96ff:fe27:9089','fe80::204:96ff:fe35:2973']],\
                                        [32,['fe80::204:96ff:fe35:2973','fe80::204:96ff:fe27:9089']]],
                        'IPv6_accept_ra_disable': 'no'
                },
                'serial' : {
                        'ip': '10.35.26.3',
                        'SC_2_1': '7005',
                        'SC_2_2': '7013',
                        'PL_2_3': '7006',
                        'PL_2_4': '7007',
                        'PL_2_5': '7008',
                        'PL_2_30': '7014',
                        'PL_2_31': '7015',
                        'PL_2_32': '7016',
                        'switch_1': '7001',
                        'switch_2': '7002'
                },
                'switches' : {
                        'switch_1' : "10.35.26.123",
                        'switch_2' : "10.35.26.124",
                        'portsInOrder' : [1009,1010,1011,1012,1013,1014,1015,1016,\
                                        1017,1018,1019,1020,1021,1022,1023,1024,\
                                        1025,1026,1027,1028,1029,1031,1032,1033,\
                                        1034,1035,1036,1037,1038,1039,1040,1041,\
                                        1042,1043,1044,1001,1002,1003,1004,\
                                        1006,1007,1008]
                }
                },
        'ports' : {
                'snmptrapd': "50012"
                }
        }
        }

        if targetHw in targetData5:
                return targetData5[targetHw]
        else:
                return -1



def _setTargetHwData6(targetHw):

    targetData6 = {

    'vbox_target_00' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.2",
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

    'vbox_target_01' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.3",
            'ctrl2' :"10.64.88.4",
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

    'vbox_target_02' :  {
        'physical_size': "4",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.5",
            'ctrl2' :"10.64.88.6",
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


    'vbox_target_03' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.7",
            'ctrl2' :"10.64.88.8",
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

    'vbox_target_04' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.9",
            'ctrl2' :"10.64.88.10",
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

    'vbox_target_05' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.11",
            'ctrl2' :"10.64.88.12",
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

    'vbox_target_06' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.34",
            'ctrl2' :"10.64.88.35",
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

    'vbox_target_07' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.36",
            'ctrl2' :"10.64.88.37",
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

    'vbox_target_08' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.38",
            'ctrl2' :"10.64.88.39",
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

    'vbox_target_09' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.40",
            'ctrl2' :"10.64.88.41",
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

    'vbox_target_10' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.42",
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

    'vbox_target_11' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.44",
            'ctrl2' :"10.64.88.45",
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

    'vbox_target_12' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.46",
            'ctrl2' :"10.64.88.47",
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

    'vbox_target_13' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.48",
            'ctrl2' :"10.64.88.49",
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

    'vbox_target_14' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.50",
            'ctrl2' :"10.64.88.51",
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

    'vbox_target_15' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.64.88.52",
            'ctrl2' :"10.64.88.53",
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

    'vbox_target_16' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.172.12.80",
            'ctrl2':"10.172.12.81",
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


    'vbox_target_29' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.145",
            'ctrl2' :"10.172.12.146",
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


    'vbox_target_30' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.150",
            'ctrl2' :"10.172.12.151",
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


    'vbox_target_31' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.155",
            'ctrl2' :"10.172.12.156",
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


    'vbox_target_32' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.160",
            'ctrl2' :"10.172.12.161",
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


    'vbox_target_33' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.165",
            'ctrl2' :"10.172.12.166",
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

    'vbox_target_34' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.170",
            'ctrl2' :"10.172.12.171",
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

    'vbox_target_40' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.200",
            'ctrl2' :"10.172.12.201",
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

    'vbox_target_41' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.12.205",
            'ctrl2' :"",
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

    'vbox_target_42' :  {
         'physical_size': "2",
         'execution_capacity_factor': "0.2",
         'watchdog' : '',
         'ipAddress' : {
         'ctrl' : {
             'NB'  :"",
             'ctrl1' :"10.172.12.210",
             'ctrl2' :"10.172.12.211",
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

     'vbox_target_43' :  {
         'physical_size': "1",
         'execution_capacity_factor': "0.2",
         'watchdog' : '',
         'ipAddress' : {
         'ctrl' : {
             'NB'  :"",
             'ctrl1' :"10.172.12.215",
             'ctrl2' :"",
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

    'vbox_target_53' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.15",
            'ctrl2' :"10.172.13.16",
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

    'vbox_target_59' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.45",
            'ctrl2' :"10.172.13.46",
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

    'vbox_target_70' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.100",
            'ctrl2' :"",
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

    'vbox_target_71' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.105",
            'ctrl2' :"10.172.13.106",
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

    'vbox_target_72' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.110",
            'ctrl2' :"",
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

    'vbox_target_73' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.115",
            'ctrl2' :"10.172.13.116",
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

    'vbox_target_74' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.120",
            'ctrl2' :"",
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

    'vbox_target_75' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.125",
            'ctrl2' :"10.172.13.126",
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

    'vbox_target_76' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.130",
            'ctrl2' :"",
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

    'vbox_target_77' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.135",
            'ctrl2' :"10.172.13.136",
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

    'vbox_target_78' :  {
        'physical_size': "4",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.140",
            'ctrl2' :"10.172.13.141",
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

    'vbox_target_79' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.145",
            'ctrl2' :"",
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

    'vbox_target_80' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.172.13.150",
            'ctrl2' :"10.172.13.151",
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
            'vip_3'    : '0.0.0.0'
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

    'vbox_target_81' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1':"10.172.13.155",
            'ctrl2' :"",
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
            'vip_3'    : '0.0.0.0'
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

    'vbox_target_84' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.170",
            'ctrl2' :"10.172.13.171",
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

    'vbox_target_85' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.175",
            'ctrl2' :"10.172.13.176",
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

    'vbox_target_86' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.180",
            'ctrl2' :"10.172.13.181",
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

    'vbox_target_87' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.185",
            'ctrl2' :"",
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

    'vbox_target_88' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.190",
            'ctrl2' :"",
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
    'vbox_target_89' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.195",
            'ctrl2' :"",
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
    'vbox_target_90' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.200",
            'ctrl2' :"10.172.13.201",
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
    'vbox_target_91' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.205",
            'ctrl2' :"",
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
    'vbox_target_92' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.210",
            'ctrl2' :"10.172.13.211",
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
    'vbox_target_93' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.215",
            'ctrl2' :"",
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
    'vbox_target_94' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.220",
            'ctrl2' :"10.172.13.221",
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
    'vbox_target_95' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.225",
            'ctrl2' :"",
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
    'vbox_target_96' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.230",
            'ctrl2' :"10.172.13.231",
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
    'vbox_target_97' :  {
        'physical_size': "1",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.235",
            'ctrl2' :"",
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
    'vbox_target_99' :  {
        'physical_size': "2",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.13.245",
            'ctrl2' :"10.172.13.246",
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
    'vbox_target_166' :  {
        'physical_size': "4",
        'execution_capacity_factor': "0.2",
        'watchdog' : '',
        'ipAddress' : {
        'ctrl' : {
            'NB'  :"",
            'ctrl1' :"10.172.15.80",
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
}

    if targetHw in targetData6:
        return targetData6[targetHw]
    else:
        return -1



def setTargetHwData(targetHw):
    global data

    targetHwData = _setTargetHwData(targetHw)
    if targetHwData == -1:
        targetHwData = _setTargetHwData2(targetHw)
        if targetHwData == -1:
            targetHwData = _setTargetHwData3(targetHw)
            if targetHwData == -1:
                targetHwData = _setTargetHwData4(targetHw)
                if targetHwData == -1:
                    targetHwData = _setTargetHwData5(targetHw)
                    if targetHwData == -1:
                        targetHwData = _setTargetHwData6(targetHw)
                        if targetHwData == -1:
                            print "ERROR: " + targetHw + " does not exist"
                            return -1

    data['physical_size']  = targetHwData['physical_size']
    data['execution_capacity_factor']  = targetHwData['execution_capacity_factor']
    data['watchdog']  = targetHwData['watchdog']
    data['ipAddress']  = targetHwData['ipAddress']
    data['target'] = targetHw
    hw = targetHw.split('_')[0]
    if (hw == 'essim' ):
        data['targetType'] = SIMULATOR_TARGET_TYPE
        data['ipAddress']['blades'] = SIMULATOR_TARGET_BLADES
        data['ipAddress']['ipmi'] = SIMULATOR_TARGET
    elif (hw == 'vbox' ):
        data['targetType'] = VIRTUAL_TARGET_TYPE
        data['ipAddress']['blades'] = SIMULATOR_TARGET_BLADES
        data['ipAddress']['ipmi'] = SIMULATOR_TARGET
    else:
        if (hw == 'ebs' ):
            data['targetType'] = EBS_TARGET_TYPE
            internal_start_addr = 8
        else:
            data['targetType'] = COTS_TARGET_TYPE
            internal_start_addr = 1
        temp_blades = []
        temp_ipmi = []
        ipmiBaseSplitted = targetHwData['ipAddress']['ctrl']['ipmi_base'].split('.')
        internalSplitted = targetHwData['ipAddress']['ctrl']['internal_net'][0].split('.')
        for bladeNumber in range (int(targetHwData['physical_size'])):
            internalAddrTemp = str(int(internalSplitted[3]) + internal_start_addr + bladeNumber)
            internalAddress = internalSplitted[0]+'.'+internalSplitted[1]+'.'+internalSplitted[2]+'.'+internalAddrTemp
            temp_blades.append(('blade_2_%s'%str (bladeNumber+1), internalAddress))
            ipmiAddrTemp = str(int(ipmiBaseSplitted[3]) + 1 + bladeNumber)
            ipmiAddress = ipmiBaseSplitted[0]+'.'+ipmiBaseSplitted[1]+'.'+ipmiBaseSplitted[2]+'.'+ipmiAddrTemp
            temp_ipmi.append(('blade_2_%s'%str (bladeNumber+1), ipmiAddress))
        data['ipAddress']['blades'] = dict(temp_blades)
        data['ipAddress']['ipmi'] = dict(temp_ipmi)
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
    print setTargetHwData("cots_target_4")
