#! /vobs/tsp_saf/tools/Python/linux/bin/python

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
#
# NOTE! PLEASE UPDATE targetData AND switchData AT THE SAME TIME
#       REGARDING THE TARGET INFORMATION AS IP ADDRESSES ETC.
#
########################################################################

data = {}

### Common IS data structures ###
IS_NODE_TYPE= "is_node"
IS_TARGET_USER = "root" 
IS_TARGET_PWD =  "tre,14"
IS_TARGET_SNMP = {'prefix': "1.3.6.1.4.1.193.129.1.2.", 'community': "is-nb-community", 'version' : '-v2c', 'trapDaemonPort' : '1162'}
IS_CTRL_PATTERNS = """(\nsis\d:.*)"""
IS_PL_PATTERNS  =  """(\nblade_\d_\d.\~)""","""(blade_\d_\d.*)""", """(root@xxb:.*)"""
IS_TARGET_BLADES = { 'blade_0_1'    : "169.254.0.49",
                                    'blade_0_13'  : "169.254.0.49",
                                    'blade_0_3'    : "169.254.0.49",
                                    'blade_0_5'    : "169.254.0.81",
                                    'blade_0_7'    : "169.254.0.113",
                                    'blade_0_9'    : "169.254.0.145",
                                    }                                                                     
        
### Common COTS data structures ###
PCBOX_NODE_TYPE="pcbox_node"
UML_NODE_TYPE="uml_node"
COTS_NODE_TYPE="cots_node"
COTS_TARGET_USER =  "root" 
COTS_TARGET_PWD =  "rootroot"
COTS_TERMINAL_SERVER_USER =  "root" 
COTS_TERMINAL_SERVER_PWD =  "dbps" 
COTS_TARGET_SNMP = {'prefix' : "1.3.6.1", 'community': "tspsaf", 'version' : '-v2c', 'trapDaemonPort' : '1162' }
COTS_CTRL_PATTERNS =  """(SC_2_\d*#)"""
COTS_PL_PATTERNS  =  """(PL_2_\d*#)"""
COTS_TEST_PC_PATTERNS = """(gwhost\d+:~ #)"""
COTS_VIP_TG_PATTERNS = """(safTg\d+:~ #)"""
COTS_SWITCH_DEVICE_PATTERNS = """(console>)"""
COTS_TARGET_BLADES = { 'blade_2_1'     : "192.168.0.1",
                                         'blade_2_2'    : "192.168.0.2",
                                         'blade_2_3'    : "192.168.0.3",
                                         'blade_2_4'    : "192.168.0.4",
                                         'blade_2_5'    : "192.168.0.5",
                                         'blade_2_6'    : "192.168.0.6",
                                         'blade_2_7'    : "192.168.0.7",
                                         'blade_2_8'    : "192.168.0.8",
                                         'blade_2_9'    : "192.168.0.9",
                                         'blade_2_10'  : "192.168.0.10",
                                         'blade_2_11'  : "192.168.0.11",
                                         'blade_2_12'  : "192.168.0.12",
                                         'blade_2_13'  : "192.168.0.13",
                                         'blade_2_14'  : "192.168.0.14",
                                         'blade_2_15'  : "192.168.0.15",
                                         'blade_2_16'  : "192.168.0.16",
                                         'blade_2_17'  : "192.168.0.17",
                                         'blade_2_18'  : "192.168.0.18",
                                         'blade_2_19'  : "192.168.0.19",
                                         'blade_2_20'  : "192.168.0.20"
                                                                      }

COTS_TARGET_IPMI = { 'blade_2_1'    : "192.168.0.101",
                                         'blade_2_2'    : "192.168.0.102",
                                         'blade_2_3'    : "192.168.0.103",
                                         'blade_2_4'    : "192.168.0.104",
                                         'blade_2_5'    : "192.168.0.105",
                                         'blade_2_6'    : "192.168.0.106",
                                         'blade_2_7'    : "192.168.0.107",
                                         'blade_2_8'    : "192.168.0.108",
                                         'blade_2_9'    : "192.168.0.109",
                                         'blade_2_10'   : "192.168.0.110",
                                         'blade_2_11'   : "192.168.0.111",
                                         'blade_2_12'   : "192.168.0.112",
                                         'blade_2_13'   : "192.168.0.113",
                                         'blade_2_14'   : "192.168.0.114",
                                         'blade_2_15'   : "192.168.0.115",
                                         'blade_2_16'   : "192.168.0.116",
                                         'blade_2_17'   : "192.168.0.117",
                                         'blade_2_18'   : "192.168.0.118",
                                         'blade_2_19'   : "192.168.0.119",
                                         'blade_2_20'   : "192.168.0.120"
                                                                      }                                                            
targetData = {

# Specific IS system information:
'is_target_1' :  {'ipAddress' : {'ctrl' : {'NB'   :"nnn.nnn.nnn.nnn", 'ctrl1' :"134.138.66.11", 'ctrl2' :"134.138.66.12"}                              
                                               }
                              },
'uml_target' :  {
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"192.168.73.12",
                'ctrl1':"192.168.73.2",
                'ctrl2' :"192.168.73.3",
                'testpc':'testpc'
            },
            'testApp'  : {
                'test_app'   : '127.0.0.1',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '192.168.73.1',
                'vip_tg'   : 'vip_tg',
                'vip_1'    : '192.168.74.1',
                'vip_2'    : '192.168.74.2',
                'vip_3'    : '192.168.74.3',
                'vip_gw_1' : '192.168.73.2',
                'vip_gw_2' : '192.168.73.3',
                'vip_gw_3' : '192.168.73.4',
                'vip_gw_4' : '192.168.73.5',
                'vip_rtr_1': '192.168.73.1',
                'vip_rtr_2': '192.168.73.1',
                'vip_rtr_3': '192.168.73.1',
                'vip_rtr_4': '192.168.73.1',
                'vip_area' : '192.168.74.0'
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
                'managedPortNum' : '24'
            }
        },
    'ports' : {
        'snmptrapd': "10162"
    }
},
                             
# Specific COTS system information:
'cots_target_4' :  {
        'physical_size': "8",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.40",
                'ctrl1':"134.138.66.41",
                'ctrl2' :"134.138.66.42",
                'testpc':'134.138.66.45'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.4',
                'external_tg': '134.138.66.18'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.4',
                'vip_2'    : '192.168.66.4',
                'vip_3'    : '172.30.26.4',
                'vip_gw_1' : '192.168.11.25',
                'vip_gw_2' : '192.168.11.29',
                'vip_rtr_1': '192.168.11.26',
                'vip_rtr_2': '192.168.11.30',
                'VIP_gw_1' : '192.168.21.25',
                'VIP_gw_2' : '192.168.21.26',
                'VIP_gw_3' : '192.168.22.25',
                'VIP_gw_4' : '192.168.22.26',
                'VIP_rtr_1': '192.168.21.27',
                'VIP_rtr_2': '192.168.22.27',
                'vip_area' : '172.16.0.4'
            },
            'serial' : {
                'ip': '134.138.66.7',
                'SC_2_1': '7013',
                'SC_2_2': '7014',
                'PL_2_3': '7015',
                'PL_2_4': '7016',
                'switch_1': '7017',
                'switch_2': '7018'
            },
            'switches' : {
                'switch_1' : "134.138.66.43",
                'switch_2' : "134.138.66.44",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "4162"
        }
    },

'cots_target_5' :  {
        'physical_size': "10",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.50", 
                'ctrl1':"134.138.66.51",
                'ctrl2' :"134.138.66.52", 
                'testpc':'134.138.66.55'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.5',
                'external_tg': '134.138.66.28'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_tg'   : '172.16.0.5',
                'vip_1'    : '172.16.0.5',
                'vip_2'    : '192.168.66.5',
                'vip_3'    : '172.30.26.5',
                'vip_gw_1' : '192.168.11.33',
                'vip_gw_2' : '192.168.11.37',
                'vip_rtr_1': '192.168.11.34',
                'vip_rtr_2': '192.168.11.38',
                'VIP_gw_1' : '192.168.21.33',
                'VIP_gw_2' : '192.168.21.34',
                'VIP_gw_3' : '192.168.22.33',
                'VIP_gw_4' : '192.168.22.34',
                'VIP_rtr_1': '192.168.21.35',
                'VIP_rtr_2': '192.168.22.35',
                'vip_area' : '172.16.0.5'
            },
            'serial' : {
                'ip': '134.138.66.251',
                'SC_2_1': '7009',
                'SC_2_2': '7010',
                'PL_2_3': '7011',
                'PL_2_4': '7012',
                'switch_1': '7007',
                'switch_2': '7008'
            },
            'switches' : {
                'switch_1' : "134.138.66.53",
                'switch_2' : "134.138.66.54",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "5162"
        }
    },
    
'cots_target_6' :  {
        'physical_size': "20",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.60", 
                'ctrl1':"134.138.66.61",
                'ctrl2' :"134.138.66.62", 
                'testpc':'134.138.66.65'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.6',
                'external_tg': '134.138.66.38'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.6',
                'vip_2'    : '192.168.66.6',
                'vip_3'    : '172.30.26.6',
                'vip_gw_1' : '192.168.11.41',
                'vip_gw_2' : '192.168.11.45',
                'vip_rtr_1': '192.168.11.42',
                'vip_rtr_2': '192.168.11.46',
                'VIP_gw_1' : '192.168.21.41',
                'VIP_gw_2' : '192.168.21.42',
                'VIP_gw_3' : '192.168.22.41',
                'VIP_gw_4' : '192.168.22.42',
                'VIP_rtr_1': '192.168.21.43',
                'VIP_rtr_2': '192.168.22.43',
                'vip_area' : '172.16.0.6'
            },
            'serial' : {
                'ip': '134.138.66.251',
                'SC_2_1': '7003',
                'SC_2_2': '7004',
                'PL_2_3': '7005',
                'PL_2_4': '7006',
                'switch_1': '7001',
                'switch_2': '7002'
            },
            'switches' : {
                'switch_1' : "134.138.66.63",
                'switch_2' : "134.138.66.64",
                'managedPortNum' : '48'
            }
        },      
    'ports' : {
            'snmptrapd': "6162"
        }
    },    
    
'cots_target_7' :  {
        'physical_size': "10",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.70", 
                'ctrl1':"134.138.66.71",
                'ctrl2' :"134.138.66.72", 
                'testpc':'134.138.66.75'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.7',
                'external_tg': '134.138.66.48'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.7',
                'vip_2'    : '192.168.66.7',
                'vip_3'    : '172.30.26.7',
                'vip_gw_1' : '192.168.11.49',
                'vip_gw_2' : '192.168.11.53',
                'vip_rtr_1': '192.168.11.50',
                'vip_rtr_2': '192.168.11.54',
                'VIP_gw_1' : '192.168.21.49',
                'VIP_gw_2' : '192.168.21.50',
                'VIP_gw_3' : '192.168.22.49',
                'VIP_gw_4' : '192.168.22.50',
                'VIP_rtr_1': '192.168.21.51',
                'VIP_rtr_2': '192.168.22.51',
                'vip_area' : '172.16.0.7'
            },
            'serial' : {
                'ip': '134.138.66.6',
                'SC_2_1': '7015',
                'SC_2_2': '7016',
                'PL_2_3': '7017',
                'PL_2_4': '7018',
                'switch_1': '7013',
                'switch_2': '7014'
            },
            'switches' : {
                'switch_1' : "134.138.66.73",
                'switch_2' : "134.138.66.74",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "7162"
        }
    },

'cots_target_8' :  {
        'physical_size': "10",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.80", 
                'ctrl1':"134.138.66.81",
                'ctrl2' :"134.138.66.82", 
                'testpc':'134.138.66.85'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.8',
                'external_tg': '134.138.66.58'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.8',
                'vip_2'    : '192.168.66.8',
                'vip_3'    : '172.30.26.8',
                'vip_gw_1' : '192.168.11.57',
                'vip_gw_2' : '192.168.11.61',
                'vip_rtr_1': '192.168.11.58',
                'vip_rtr_2': '192.168.11.62',
                'VIP_gw_1' : '192.168.21.57',
                'VIP_gw_2' : '192.168.21.58',
                'VIP_gw_3' : '192.168.22.57',
                'VIP_gw_4' : '192.168.22.58',
                'VIP_rtr_1': '192.168.21.59',
                'VIP_rtr_2': '192.168.22.59',
                'vip_area' : '172.16.0.8'
            },
            'serial' : {
                'ip': '134.138.66.5',
                'SC_2_1': '7021',
                'SC_2_2': '7022',
                'PL_2_3': '7023',
                'PL_2_4': '7024',
                'PL_2_5': '7025',
                'PL_2_6': '7026',
                'PL_2_7': '7027',
                'PL_2_8': '7028',
                'switch_1': '7019',
                'switch_2': '7020'
            },
            'switches' : {
                'switch_1' : "134.138.66.83",
                'switch_2' : "134.138.66.84",
                'managedPortNum' : '24'
            }
        },
      'ports' : {
            'snmptrapd': "8162"
        }
    },


'pcbox_target_9' :  {
        'physical_size': "8",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.90", 
                'ctrl1' :"134.138.66.91",
                'ctrl2' :"134.138.66.92", 
                'testpc': '134.138.66.95' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.9',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.9',
                'vip_2'    : '192.168.66.9',
                'vip_3'    : '172.30.26.9',
                'vip_gw_1' : '192.168.11.65',
                'vip_gw_2' : '192.168.11.69',
                'vip_rtr_1': '192.168.11.66',
                'vip_rtr_2': '192.168.11.70',
                'VIP_gw_1' : '192.168.21.65',
                'VIP_gw_2' : '192.168.21.66',
                'VIP_gw_3' : '192.168.22.65',
                'VIP_gw_4' : '192.168.22.66',
                'VIP_rtr_1': '192.168.21.67',
                'VIP_rtr_2': '192.168.22.67',
                'vip_area' : '172.16.0.9'
            },
            'serial' : {
                'ip': '134.138.66.9',
                'SC_2_1': '2013',
                'SC_2_2': '2014',
                'PL_2_3': '2015',
                'PL_2_4': '2016',
            },
            'switches' : {
                'switch_1' : "134.138.66.93", 
                'switch_2' : "134.138.66.94",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "9162"
        }
    },
    
'cots_target_10' :  {
        'physical_size': "8",
        'ipAddress' : {
            'ctrl' : {
                'NB'      : "134.138.66.100", 
                'ctrl1'   : "134.138.66.101",
                'ctrl2'   : "134.138.66.102", 
                'testpc'  : '134.138.66.105'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.10',
                'external_tg': '134.138.66.68'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.10',
                'vip_2'    : '192.168.66.10',
                'vip_3'    : '172.30.26.10',
                'vip_gw_1' : '192.168.11.73',
                'vip_gw_2' : '192.168.11.77',
                'vip_rtr_1': '192.168.11.74',
                'vip_rtr_2': '192.168.11.78',
                'VIP_gw_1' : '192.168.21.73',
                'VIP_gw_2' : '192.168.21.74',
                'VIP_gw_3' : '192.168.22.73',
                'VIP_gw_4' : '192.168.22.74',
                'VIP_rtr_1': '192.168.21.75',
                'VIP_rtr_2': '192.168.22.75',
                'vip_area' : '172.16.0.10'
            },
            'serial' : {
                'ip': '134.138.66.8',
                'SC_2_1': '7003',
                'SC_2_2': '7004',
                'PL_2_3': '7005',
                'PL_2_4': '7006',
                'switch_1': '7001',
                'switch_2': '7002'
            },
            'switches' : {
                'switch_1' : "134.138.66.103", 
                'switch_2' : "134.138.66.104",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "10162"
        }
    },

'cots_target_11' :  {
        'physical_size': "8",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.110", 
                'ctrl1':"134.138.66.111",
                'ctrl2' :"134.138.66.112", 
                'testpc':'134.138.66.115' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.11',
                'external_tg': '134.138.66.78'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.11',
                'vip_2'    : '192.168.66.11',
                'vip_3'    : '172.30.26.11',
                'vip_gw_1' : '192.168.11.81',
                'vip_gw_2' : '192.168.11.85',
                'vip_rtr_1': '192.168.11.82',
                'vip_rtr_2': '192.168.11.86',
                'VIP_gw_1' : '192.168.21.81',
                'VIP_gw_2' : '192.168.21.82',
                'VIP_gw_3' : '192.168.22.81',
                'VIP_gw_4' : '192.168.22.82',
                'VIP_rtr_1': '192.168.21.83',
                'VIP_rtr_2': '192.168.22.83',
                'vip_area' : '172.16.0.11'
            },
            'serial' : {
                'ip': '134.138.66.7',
                'SC_2_1': '7003',
                'SC_2_2': '7004',
                'PL_2_3': '7005',
                'PL_2_4': '7006',
                'switch_1': '7001',
                'switch_2': '7002'
            },
            'switches' : {
                'switch_1' : "134.138.66.113", 
                'switch_2' : "134.138.66.114",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "11162"
        }
    },

'pcbox_target_12' :  {
        'physical_size': "8",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.120", 
                'ctrl1' :"134.138.66.121",
                'ctrl2' :"134.138.66.122", 
                'testpc': '134.138.66.125' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.12',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.12',
                'vip_2'    : '192.168.66.12',
                'vip_3'    : '172.30.26.12',
                'vip_gw_1' : '192.168.11.89',
                'vip_gw_2' : '192.168.11.93',
                'vip_rtr_1': '192.168.11.90',
                'vip_rtr_2': '192.168.11.94',
                'VIP_gw_1' : '192.168.21.89',
                'VIP_gw_2' : '192.168.21.90',
                'VIP_gw_3' : '192.168.22.89',
                'VIP_gw_4' : '192.168.22.90',
                'VIP_rtr_1': '192.168.21.91',
                'VIP_rtr_2': '192.168.22.91',
                'vip_area' : '172.16.0.12'
            },
            'serial' : {
                'ip': '134.138.66.9',
                'SC_2_1': '2001',
                'SC_2_2': '2002',
                'PL_2_3': '2003',
                'PL_2_4': '2004',
            },
            'switches' : {
                'switch_1' : "134.138.66.123", 
                'switch_2' : "134.138.66.124",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "12162"
        }
    },

'pcbox_target_13' : {
        'physical_size': "8",
        'ipAddress' :  {
            'ctrl' : {
                'NB'  :"134.138.66.130", 
                'ctrl1':"134.138.66.131",
                'ctrl2' :"134.138.66.132", 
                'testpc':'134.138.66.135' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.13',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.13',
                'vip_2'    : '192.168.66.13',
                'vip_3'    : '172.30.26.13',
                'vip_gw_1' : '192.168.11.97',
                'vip_gw_2' : '192.168.11.101',
                'vip_rtr_1': '192.168.11.98',
                'vip_rtr_2': '192.168.11.102',
                'VIP_gw_1' : '192.168.21.97',
                'VIP_gw_2' : '192.168.21.98',
                'VIP_gw_3' : '192.168.22.97',
                'VIP_gw_4' : '192.168.22.98',
                'VIP_rtr_1': '192.168.21.99',
                'VIP_rtr_2': '192.168.22.99',
                'vip_area' : '172.16.0.13'
            },
            'serial' : {
                'ip': '134.138.66.9',
                'SC_2_1': '2005',
                'SC_2_2': '2006',
                'PL_2_3': '2007',
                'PL_2_4': '2008',
            },
            'switches' : {
                'switch_1' : "134.138.66.133", 
                'switch_2' : "134.138.66.134",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "13162"
        }
    },

'pcbox_target_14' :  {
        'physical_size': "8",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.140", 
                'ctrl1':"134.138.66.141",
                'ctrl2' :"134.138.66.142", 
                'testpc':'134.138.66.145' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.14',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.14',
                'vip_2'    : '192.168.66.14',
                'vip_3'    : '172.30.26.14',
                'vip_gw_1' : '192.168.11.105',
                'vip_gw_2' : '192.168.11.109',
                'vip_rtr_1': '192.168.11.106',
                'vip_rtr_2': '192.168.11.110',
                'VIP_gw_1' : '192.168.21.105',
                'VIP_gw_2' : '192.168.21.106',
                'VIP_gw_3' : '192.168.22.105',
                'VIP_gw_4' : '192.168.22.106',
                'VIP_rtr_1': '192.168.21.107',
                'VIP_rtr_2': '192.168.22.107',
                'vip_area' : '172.16.0.14'
            },
            'serial' : {
                'ip': '134.138.66.9',
                'SC_2_1': '2009',
                'SC_2_2': '2010',
                'PL_2_3': '2011',
                'PL_2_4': '2012',
            },
            'switches' : {
                'switch_1' : "134.138.66.143", 
                'switch_2' : "134.138.66.144",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "14162"
        }
    },

'pcbox_target_15' : {
        'physical_size': "8",
        'ipAddress' :  {
            'ctrl' : {
                'NB'  :"134.138.66.150", 
                'ctrl1':"134.138.66.151",
                'ctrl2' :"134.138.66.152", 
                'testpc':'134.138.66.155' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.15',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.15',
                'vip_2'    : '192.168.66.15',
                'vip_3'    : '172.30.26.15',
                'vip_gw_1' : '192.168.11.113',
                'vip_gw_2' : '192.168.11.117',
                'vip_rtr_1': '192.168.11.114',
                'vip_rtr_2': '192.168.11.118',
                'VIP_gw_1' : '192.168.21.113',
                'VIP_gw_2' : '192.168.21.114',
                'VIP_gw_3' : '192.168.22.113',
                'VIP_gw_4' : '192.168.22.114',
                'VIP_rtr_1': '192.168.21.115',
                'VIP_rtr_2': '192.168.22.115',
                'vip_area' : '172.16.0.15'
            },
            'serial' : {
                'ip': '134.138.66.4',
                'SC_2_1': '7001',
                'SC_2_2': '7002',
                'PL_2_3': '7003',
                'PL_2_4': '7004',
            },
            'switches' : {
                'switch_1' : "134.138.66.153", 
                'switch_2' : "134.138.66.154",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "15162"
        }
    },

'pcbox_target_16' : {
        'physical_size': "8",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.160", 
                'ctrl1':"134.138.66.161",
                'ctrl2' :"134.138.66.162", 
                'testpc':'134.138.66.165' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.16',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.16',
                'vip_2'    : '192.168.66.16',
                'vip_3'    : '172.30.26.16',
                'vip_gw_1' : '192.168.11.121',
                'vip_gw_2' : '192.168.11.125',
                'vip_rtr_1': '192.168.11.122',
                'vip_rtr_2': '192.168.11.126',
                'VIP_gw_1' : '192.168.21.121',
                'VIP_gw_2' : '192.168.21.122',
                'VIP_gw_3' : '192.168.22.121',
                'VIP_gw_4' : '192.168.22.122',
                'VIP_rtr_1': '192.168.21.123',
                'VIP_rtr_2': '192.168.22.123',
                'vip_area' : '172.16.0.16'
            },
            'serial' : {
                'ip': '134.138.66.4',
                'SC_2_1': '7005',
                'SC_2_2': '7006',
                'PL_2_3': '7007',
                'PL_2_4': '7008',
            },
            'switches' : {
                'switch_1' : "134.138.66.163", 
                'switch_2' : "134.138.66.164",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "16162"
        }
    },

'pcbox_target_17' : {
        'physical_size': "8",
        'ipAddress' :  {
            'ctrl' : {
                'NB'  :"134.138.66.170", 
                'ctrl1':"134.138.66.171",
                'ctrl2' :"134.138.66.172", 
                'testpc':'134.138.66.175'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.17',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.17',
                'vip_2'    : '192.168.66.17',
                'vip_3'    : '172.30.26.17',
                'vip_gw_1' : '192.168.11.129',
                'vip_gw_2' : '192.168.11.133',
                'vip_rtr_1': '192.168.11.130',
                'vip_rtr_2': '192.168.11.134',
                'VIP_gw_1' : '192.168.21.129',
                'VIP_gw_2' : '192.168.21.130',
                'VIP_gw_3' : '192.168.22.129',
                'VIP_gw_4' : '192.168.22.130',
                'VIP_rtr_1': '192.168.21.131',
                'VIP_rtr_2': '192.168.22.131',
                'vip_area' : '172.16.0.17'
            },
            'serial' : {
                'ip': '134.138.66.4',
                'SC_2_1': '7009',
                'SC_2_2': '7010',
                'PL_2_3': '7011',
                'PL_2_4': '7012',
            },
            'switches' : {
                'switch_1' : "134.138.66.173", 
                'switch_2' : "134.138.66.174",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "17162"
        }
    },

'pcbox_target_18' : {
        'physical_size': "8",
        'ipAddress' :  {
            'ctrl' : {
                'NB'  :"134.138.66.180", 
                'ctrl1':"134.138.66.181",
                'ctrl2' :"134.138.66.182", 
                'testpc':'134.138.66.185'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.18',
                'external_tg': 'To be defined later'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.18',
                'vip_2'    : '192.168.66.18',
                'vip_3'    : '172.30.26.18',
                'vip_gw_1' : '192.168.11.137',
                'vip_gw_2' : '192.168.11.141',
                'vip_rtr_1': '192.168.11.138',
                'vip_rtr_2': '192.168.11.142',
                'VIP_gw_1' : '192.168.21.137',
                'VIP_gw_2' : '192.168.21.138',
                'VIP_gw_3' : '192.168.22.137',
                'VIP_gw_4' : '192.168.22.138',
                'VIP_rtr_1': '192.168.21.139',
                'VIP_rtr_2': '192.168.22.139',
                'vip_area' : '172.16.0.18'
            },
            'serial' : {
                'ip': '134.138.66.4',
                'SC_2_1': '7013',
                'SC_2_2': '7014',
                'PL_2_3': '7015',
                'PL_2_4': '7016',
            },
            'switches' : {
                'switch_1' : "134.138.66.183", 
                'switch_2' : "134.138.66.184",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "18162"
        }
    },

'cots_target_19' : {
        'physical_size': "8",
        'ipAddress' :  {
            'ctrl' : { 
                'NB'  :"134.138.66.190", 
                'ctrl1':"134.138.66.191",
                'ctrl2' :"134.138.66.192", 
                'testpc':'134.138.66.195' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.19',
                'external_tg': '134.138.66.88'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.19',
                'vip_2'    : '192.168.66.19',
                'vip_3'    : '172.30.26.19',
                'vip_gw_1' : '192.168.11.145',
                'vip_gw_2' : '192.168.11.149',
                'vip_rtr_1': '192.168.11.146',
                'vip_rtr_2': '192.168.11.150',
                'VIP_gw_1' : '192.168.21.145',
                'VIP_gw_2' : '192.168.21.146',
                'VIP_gw_3' : '192.168.22.145',
                'VIP_gw_4' : '192.168.22.146',
                'VIP_rtr_1': '192.168.21.147',
                'VIP_rtr_2': '192.168.22.147',
                'vip_area' : '172.16.0.19'
            },
            'serial' : {
                'ip': '134.138.66.7',
                'SC_2_1': '7009',
                'SC_2_2': '7010',
                'PL_2_3': '7011',
                'PL_2_4': '7012',
                'switch_1': '7007',
                'switch_2': '7008'
            },
            'switches' : {
                'switch_1' : "134.138.66.193", 
                'switch_2' : "134.138.66.194",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "19162"
        }
    },

'cots_target_20' :  {
        'physical_size': "10",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.200", 
                'ctrl1':"134.138.66.201",
                'ctrl2' :"134.138.66.202", 
                'testpc':'134.138.66.205' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.20',
                'external_tg': '134.138.66.98'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.20',
                'vip_2'    : '192.168.66.20',
                'vip_3'    : '172.30.26.20',
                'vip_gw_1' : '192.168.11.153',
                'vip_gw_2' : '192.168.11.157',
                'vip_rtr_1': '192.168.11.154',
                'vip_rtr_2': '192.168.11.158',
                'VIP_gw_1' : '192.168.21.153',
                'VIP_gw_2' : '192.168.21.154',
                'VIP_gw_3' : '192.168.22.153',
                'VIP_gw_4' : '192.168.22.154',
                'VIP_rtr_1': '192.168.21.155',
                'VIP_rtr_2': '192.168.22.155',
                'vip_area' : '172.16.0.20'
            },
            'serial' : {
                'ip': '134.138.66.6',
                'SC_2_1': '7003',
                'SC_2_2': '7004',
                'PL_2_3': '7005',
                'PL_2_4': '7006',
                'switch_1': '7001',
                'switch_2': '7002'
            },
            'switches' : {
                'switch_1' : "134.138.66.203", 
                'switch_2' : "134.138.66.204",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "20162"
        }
    },

'cots_target_21' : {
        'physical_size': "8",
        'ipAddress' :  {
            'ctrl' : {
                'NB'  :"134.138.66.210", 
                'ctrl1':"134.138.66.211",
                'ctrl2' :"134.138.66.212", 
                'testpc':'134.138.66.215' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.21',
                'external_tg': '134.138.66.108'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.21',
                'vip_2'    : '192.168.66.21',
                'vip_3'    : '172.30.26.21',
                'vip_gw_1' : '192.168.11.161',
                'vip_gw_2' : '192.168.11.165',
                'vip_rtr_1': '192.168.11.162',
                'vip_rtr_2': '192.168.11.166',
                'VIP_gw_1' : '192.168.21.161',
                'VIP_gw_2' : '192.168.21.162',
                'VIP_gw_3' : '192.168.22.161',
                'VIP_gw_4' : '192.168.22.162',
                'VIP_rtr_1': '192.168.21.163',
                'VIP_rtr_2': '192.168.22.163',
                'vip_area' : '172.16.0.21'
            },
            'serial' : {
                'ip': '134.138.66.6',
                'SC_2_1': '7009',
                'SC_2_2': '7010',
                'PL_2_3': '7011',
                'PL_2_4': '7012',
                'switch_1': '7007',
                'switch_2': '7008'
            },
            'switches' : {
                'switch_1' : "134.138.66.213", 
                'switch_2' : "134.138.66.214",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "21162"
        }
    },

'cots_target_22' :  {
        'physical_size': "10",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.220", 
                'ctrl1':"134.138.66.221",
                'ctrl2' :"134.138.66.222", 
                'testpc':'134.138.66.225' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.22',
                'external_tg': '134.138.66.118'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.22',
                'vip_2'    : '192.168.66.22',
                'vip_3'    : '172.30.26.22',
                'vip_gw_1' : '192.168.11.169',
                'vip_gw_2' : '192.168.11.173',
                'vip_rtr_1': '192.168.11.170',
                'vip_rtr_2': '192.168.11.174',
                'VIP_gw_1' : '192.168.21.169',
                'VIP_gw_2' : '192.168.21.170',
                'VIP_gw_3' : '192.168.22.169',
                'VIP_gw_4' : '192.168.22.170',
                'VIP_rtr_1': '192.168.21.171',
                'VIP_rtr_2': '192.168.22.171',
                'vip_area' : '172.16.0.22'
            },
            'serial' : {
                'ip': '134.138.66.5',
                'SC_2_1': '7003',
                'SC_2_2': '7004',
                'PL_2_3': '7005',
                'PL_2_4': '7006',
                'switch_1': '7001',
                'switch_2': '7002'
            },
            'switches' : {
                'switch_1' : "134.138.66.223", 
                'switch_2' : "134.138.66.224",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "22162"
        }
    }
,
'cots_target_23' :  {
        'physical_size': "10",
        'ipAddress' : {
            'ctrl' : {
                'NB'  :"134.138.66.230", 
                'ctrl1':"134.138.66.231",
                'ctrl2' :"134.138.66.232", 
                'testpc':'134.138.66.235'
            },
            'testApp'  : {
                'test_app'   : '172.30.26.23',
                'external_tg': '134.138.66.128'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.23',
                'vip_2'    : '192.168.66.23',
                'vip_3'    : '172.30.26.23',
                'vip_gw_1' : '192.168.11.177',
                'vip_gw_2' : '192.168.11.181',
                'vip_rtr_1': '192.168.11.178',
                'vip_rtr_2': '192.168.11.182',
                'VIP_gw_1' : '192.168.21.177',
                'VIP_gw_2' : '192.168.21.178',
                'VIP_gw_3' : '192.168.22.177',
                'VIP_gw_4' : '192.168.22.178',
                'VIP_rtr_1': '192.168.21.179',
                'VIP_rtr_2': '192.168.22.179',
                'vip_area' : '172.16.0.23'
            },
            'serial' : {
                'ip': '134.138.66.5',
                'SC_2_1': '7009',
                'SC_2_2': '7010',
                'PL_2_3': '7011',
                'PL_2_4': '7012',
                'switch_1': '7007',
                'switch_2': '7008'
            },
            'switches' : {
                'switch_1' : "134.138.66.233",
                'switch_2' : "134.138.66.234",
                'managedPortNum' : '24'
            }
        },      
    'ports' : {
            'snmptrapd': "23162"
        }
    },

'cots_target_24' : {
        'physical_size': "10",
        'ipAddress' : {
            'ctrl' : {
                'NB': "134.138.66.240", 
                'ctrl1': "134.138.66.241",
                'ctrl2': "134.138.66.242", 
                'testpc': '134.138.66.245' 
            },
            'testApp'  : {
                'test_app'   : '172.30.26.24',
                'external_tg': '134.138.66.138'
            },
            'vip'  : {
                'vip_default_route': '134.138.66.1',
                'vip_1'    : '172.16.0.24',
                'vip_2'    : '192.168.66.24',
                'vip_3'    : '172.30.26.24',
                'vip_gw_1' : '192.168.11.185',
                'vip_gw_2' : '192.168.11.189',
                'vip_rtr_1': '192.168.11.186',
                'vip_rtr_2': '192.168.11.190',
                'VIP_gw_1' : '192.168.21.185',
                'VIP_gw_2' : '192.168.21.186',
                'VIP_gw_3' : '192.168.22.185',
                'VIP_gw_4' : '192.168.22.186',
                'VIP_rtr_1': '192.168.21.187',
                'VIP_rtr_2': '192.168.22.187',
                'vip_area' : '172.16.0.24'
            },
            'serial': {
                'ip': '134.138.66.5',
                'SC_2_1': '7015',
                'SC_2_2': '7016',
                'PL_2_3': '7017',
                'PL_2_4': '7018',
                'switch_1': '7013',
                'switch_2': '7014'
            },
            'switches' : {
                'switch_1' : "134.138.66.243", 
                'switch_2' : "134.138.66.244",
                'managedPortNum' : '24'
            }
          },      
    'ports' : {
            'snmptrapd': "10162"
        }
    }
}

def setTargetHwData(targetHw):

    global targetData
    global data

    hw = targetHw.split('_')[0]

    if (hw == 'is'):
        data['ipAddress']  = targetData[targetHw]['ipAddress']
        data['nodeType']   = IS_NODE_TYPE
        data['ipAddress']['blades'] = IS_TARGET_BLADES
        data['user']       = IS_TARGET_USER
        data['pwd']        = IS_TARGET_PWD
        data['ctrlBladePattern']    = IS_CTRL_PATTERNS
        data['payloadBladePattern'] = IS_PL_PATTERNS
        data['snmp']       = IS_TARGET_SNMP     
        
    else:
        data['physical_size']  = targetData[targetHw]['physical_size']
        data['ipAddress']  = targetData[targetHw]['ipAddress']
        
        if (hw == 'cots' ) :
            data['nodeType'] = COTS_NODE_TYPE
        elif (hw == 'pcbox' ):
            data['nodeType'] = PCBOX_NODE_TYPE
        else:
            data['nodeType'] = UML_NODE_TYPE

        data['ipAddress']['blades'] = COTS_TARGET_BLADES
        data['ipAddress']['ipmi']      = COTS_TARGET_IPMI   
        data['user'] = COTS_TARGET_USER
        data['pwd'] = COTS_TARGET_PWD    
        data['terminal_server_user'] = COTS_TERMINAL_SERVER_USER
        data['terminal_server_pwd'] = COTS_TERMINAL_SERVER_PWD         
        data['ctrlBladePattern'] = COTS_CTRL_PATTERNS
        data['payloadBladePattern'] = COTS_PL_PATTERNS
        data['testPcPattern'] = COTS_TEST_PC_PATTERNS
        data['vipTgPattern'] = COTS_VIP_TG_PATTERNS
        data['switchDevicePattern'] = COTS_SWITCH_DEVICE_PATTERNS
        data['snmp'] = COTS_TARGET_SNMP
        data['ports'] =  targetData[targetHw]['ports']     
    return data

def setTargetXmlData(dict):
    global data
    data = dict
    
    return data

def getTargetHwData():
    return data
    

#############################################################################################
# Main program - for testing
#############################################################################################
if __name__ == "__main__":
    print setTargetHwData("pcbox_target_17")






