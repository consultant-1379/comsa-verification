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
 * Modified: eozasaf 2011-07-22 removed unnecessary complexity
 * These constants are related to IMM version and the object implementor name.
 */
#include <string.h>

#ifndef CONSTANTS_H_
#define CONSTANTS_H_

#define IMPLEMENTOR_NAME "ErrorStringTestObjImp"
//Set empty, but in case the class become more unique they might be prefixed with ECIM prefix
#define ECIM_PREFIX ""

const SaVersionT IMM_VERSION = { 'A', 2, 11 };

#endif /* CONSTANTS_H_ */
