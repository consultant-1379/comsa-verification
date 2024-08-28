/******************************************************************************
 *   Copyright (C) 2014 by Ericsson AB
 *   S - 125 26  STOCKHOLM
 *   SWEDEN, tel int + 46 10 719 0000
 *
 *   The copyright to the computer program herein is the property of
 *   Ericsson AB. The program may be used and/or copied only with the
 *   written permission from Ericsson AB, or in accordance with the terms
 *   and conditions stipulated in the agreement/contract under which the
 *   program has been supplied.
 *
 *   All rights reserved.
 *
 *
 *   File:   saname_utils.h
 *
 *   Author: xadaleg
 *
 *   Date:   2014-08-02
 *
 *   This file implements the helper functions to use when converting between
 *   SaNameT and char*.
 *
 *****************************************************************************/
#ifndef SANAMEUTILS_h
#define SANAMEUTILS_h

#include <stdbool.h>
#include "saAis.h"

#define extNameReleaseCode 'A'
#define extNameMajorVersion 2
#define extNameMinorVersion 14

/**
*  Maximum length of a distinguished name, not counting the terminating NUL
*  character.
*/
#ifdef SA_EXTENDED_NAME_SOURCE
	#define MAX_DN_LENGTH 2048
#else
	#define MAX_DN_LENGTH 256
	#define SA_MAX_UNEXTENDED_NAME_LENGTH 256
	typedef const char* SaConstStringT;
#endif

#ifdef __cplusplus
extern "C" {
#endif
	extern void saNameInit(void);

	extern bool saNameSet(SaConstStringT value, SaNameT* name);

	extern SaConstStringT saNameGet(const SaNameT* name);

	extern void saNameDelete(SaNameT* name, bool deleteName);

	extern unsigned saNameLen(const SaNameT* name);

	extern unsigned saNameMaxLen();

	extern unsigned saNameMaxLenNtf();

	extern char* makeCString(const SaNameT* saName);

	extern SaNameT* makeSaNameT(const char* cstr);

	extern bool isFunctionalitySupported(const SaVersionT currentVersion, const SaUint8T reqReleaseCode, const SaUint8T reqMajorVersion, SaUint8T reqMinorVersion);

#ifdef __cplusplus
}
#endif
#endif
