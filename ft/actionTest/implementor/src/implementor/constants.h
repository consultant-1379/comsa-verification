/*
 * Copyright (C) 2010 by Ericsson AB
 * S - 125 26  STOCKHOLM
 * SWEDEN, tel int + 46 10 719 0000
 *
 * The copyright to the computer program herein is the property of
 * Ericsson AB. The program may be used and/or copied only with the
 * written permission from Ericsson AB, or in accordance with the terms
 * and conditions stipulated in the agreement/contract under which the
 * program has been supplied.
 *
 * All rights reserved.
 *
 * Author: qjalars
 * Reviewed: -
 *
 * These constants are related to IMM implementor, class names, object names, ECIM naming and implementor name.
 * Any change in ECIM will be reflected here or/and in ConfigInterface.h
*/
#include <string.h>

#ifndef CONSTANTS_H_
#define CONSTANTS_H_

#define IMPLEMENTOR_NAME "ActionTestApplImpl"
//Set empty, but in case the class become more unique they might be prefixed with ECIM prefix
#define ECIM_PREFIX ""
#define AUTH_CLASS_NAME ECIM_PREFIX "ActionTest"
#define RDN_LDAP "actionTestId=1"
#define DELIM ","
#ifdef TEST_FOR_LONG_DN
#define DN_ROOT "sdp617ActiontestRootId=This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_1"
const SaVersionT IMM_VERSION = { 'A', 2, 11 };
#else
#define DN_ROOT "sdp617ActiontestRootId=1"
const SaVersionT IMM_VERSION = { 'A', 1, 2 };
//static SaNameT LDAP_OBJECT_NAME = { strlen(RDN_LDAP DELIM DN_ROOT), RDN_LDAP DELIM DN_ROOT };
#endif

#endif /* CONSTANTS_H_ */
