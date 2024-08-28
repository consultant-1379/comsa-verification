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
 *   File:   saname_utils.cc
 *
 *   Author: xadaleg
 *
 *   Date:   2014-08-02
 *
 *   This file implements the helper functions to use when converting between
 *   SaNameT and char*.
 *
 *****************************************************************************/

#include <unistd.h>
#include <string.h>
#include "saname_utils.h"
//#include "ComSA.h"
#include "trace.h"
//#include "ImmCmd.h"
#include <dlfcn.h>

#define ENTER()
#define LEAVE()

bool bExtendedNamesInitialized = false;
bool bExtendedNameEnabled = false;

typedef struct {
	SaUint16T length;
	SaUint8T value[SA_MAX_UNEXTENDED_NAME_LENGTH];
} OldSaNameT;


bool checkLongDn()
{
	FILE *fp = popen("immlist -a longDnsAllowed opensafImm=opensafImm,safApp=safImmService", "r");
	char *out = new char[100];
	fread(out, 1, 100, fp);
	TRACE_INFO("immlist print out: %s", out);
	out[strlen("longDnsAllowed=1")] = 0;
	bool ret = strcmp(out, "longDnsAllowed=1") == 0 ? true : false;
	delete []out;
	return ret;
}

/**
 * Initialise the saName utility to determine if extended names are supported
 *
 * @param[in]   void
 * @return 		No return value.
 */
void saNameInit(void)
{
	ENTER();
	bExtendedNameEnabled = false;
	if (!bExtendedNamesInitialized) {
		bExtendedNameEnabled = checkLongDn();
		bExtendedNamesInitialized = true;
	}
	TRACE_INFO("saNameInit bExtendedNameEnabled %d bExtendedNamesInitialized %d", bExtendedNameEnabled, bExtendedNamesInitialized);
	TRACE_INFO("saNameInit LEAVE");
	LEAVE();
}

/**
 * Set the name variable from the value
 *
 * @param[in]	value - the name string
 * @param[out]	name - the name type
 * @return 		true, if the name was truncated
 */
bool saNameSet(SaConstStringT value, SaNameT* name)
{
	ENTER();
	TRACE_INFO("saNameSet [%s]", value);
	bool wasNameTruncated = false;
	unsigned len = strlen(value);
#ifdef SA_EXTENDED_NAME_SOURCE
	if (!bExtendedNameEnabled) {
#endif
		OldSaNameT* oldName = (OldSaNameT*) name;
		if (len > SA_MAX_UNEXTENDED_NAME_LENGTH) {
			len = SA_MAX_UNEXTENDED_NAME_LENGTH;
			TRACE_INFO("saNameSet length truncated from %d to %d", len, SA_MAX_UNEXTENDED_NAME_LENGTH);
			wasNameTruncated = true;
		}
		oldName->length = len;
		memcpy(oldName->value, value, len);
		oldName->value[len] = NULL;
		TRACE_INFO("saNameSet oldName %u [%s]", oldName->length, oldName->value);
#ifdef SA_EXTENDED_NAME_SOURCE
	}
	else {
#ifndef UNIT_TEST
		if (dlsym(RTLD_DEFAULT, "saAisNameLend") != NULL)
#endif
		{
			TRACE_INFO("saNameSet saAisNameLend %u [%s]", len, value);
			SaConstStringT tmpVal = NULL;
			if (len < SA_MAX_UNEXTENDED_NAME_LENGTH) {
				tmpVal = value;
			}
			else {
				tmpVal = strdup(value);
			}
			if (tmpVal != NULL) {
				saAisNameLend(tmpVal, name);
			}
			else {
				TRACE_ERROR("saNameSet tmpVal == NULL");
			}
		}
	}
#endif
	LEAVE();
	return wasNameTruncated;
}

/**
 * Get the name string from the name type
 *
 * @param[in]	name - the name type
 * @return 		The name string
 */
SaConstStringT saNameGet(const SaNameT* name)
{
	ENTER();
	SaConstStringT value = NULL;
#ifdef SA_EXTENDED_NAME_SOURCE
	if (!bExtendedNameEnabled) {
#endif
		OldSaNameT* oldName = (OldSaNameT*) name;
		if (name != NULL) {
			value = (char*) oldName->value;
		}
		else {
			value = "";
		}
#ifdef SA_EXTENDED_NAME_SOURCE
	}
	else {
#ifndef UNIT_TEST
		if (dlsym(RTLD_DEFAULT, "saAisNameBorrow") != NULL)
#endif
		{
			value = saAisNameBorrow(name);
			TRACE_INFO("saNameGet saAisNameBorrow");
		}
	}
	LEAVE();
#endif
	TRACE_INFO("saNameGet %d [%s]", (int) strlen(value), value);
	return value;
}

/**
 * Delete the name string from the name type
 *
 * @param[in]	name - the name type
 * @param[in]	deleteName - true, if the SaNameT struct is to be deleted
 * @return 		No return value.
 */
void saNameDelete(SaNameT* name, bool deleteName)
{
	ENTER();
	SaConstStringT value = saNameGet(name);
	if (value != NULL) {
		int len = strlen(value);
		TRACE_INFO("saNameDelete %d [%s]", len, value);
		if (bExtendedNameEnabled) {
			if (len >= SA_MAX_UNEXTENDED_NAME_LENGTH) {
				free((void*)value);
				value = NULL;
			}
		}
	}
	else {
		TRACE_ERROR("saNameDelete value == NULL");
	}
	if (deleteName && (name != NULL)) {
		free((void*)name);
		name = NULL;
	}
	LEAVE();
}

/**
 * Get the length of the name type
 *
 * @param[in]	name - the name type
 * @return 		Length of the name
 */
unsigned saNameLen(const SaNameT* name)
{
	ENTER();
	unsigned length = 0;
	if (!bExtendedNameEnabled) {
		OldSaNameT* oldName = (OldSaNameT*) name;
		length = oldName->length;
	}
	else {
		length = strlen(saNameGet(name));
	}
	LEAVE();
	TRACE_INFO("saNameLen %u  [%s]", length, saNameGet(name));
	return length;
}

/**
 * Get the maximum length of the name
 *
 * @return 		Maximum length of the name
 */
unsigned saNameMaxLen()
{
	ENTER();
	unsigned maxLen = 0;
	if (!bExtendedNameEnabled) {
		maxLen = SA_MAX_UNEXTENDED_NAME_LENGTH;
	}
	else {
		maxLen = MAX_DN_LENGTH;
	}
	TRACE_INFO("saNameMaxLen %u", maxLen);
	LEAVE();
	return maxLen;
}

/**
 * Get the maximum length of the NTF name
 *
 * @return 		Maximum length of the NTF name
 */
unsigned saNameMaxLenNtf()
{
	ENTER();
	unsigned maxLen = 0;
	if (!bExtendedNameEnabled) {
		maxLen = SA_MAX_UNEXTENDED_NAME_LENGTH+1;
	}
	else {
		maxLen = MAX_DN_LENGTH;
	}
	TRACE_INFO("saNameMaxLenNtf %u", maxLen);
	LEAVE();
	return maxLen;
}

/**
 * Convert a SaNameT to a char*
 * Note: the char* is allocated by new and must be deleted
 *
 * @param[in]	name - the name type
 * @return 		pointer to the name string
 */
char* makeCString(const SaNameT* saName) {
	ENTER();
	unsigned len = saNameLen(saName);
	char* tmpStr = new char[len + 1];
	if (tmpStr != NULL) {
		memcpy(tmpStr, saNameGet(saName), len);
		tmpStr[len] = 0; // make a c-string!!
		TRACE_INFO("makeCString %u [%s]", len, tmpStr);
	}
	else {
		TRACE_ERROR("makeCString tmpStr == NULL");
	}
	LEAVE();
	return tmpStr;
}

/**
 * Convert a char* to an SaNameT
 * Note: the SaNameT* is allocated by new and must be deleted
 *
 * @param[in]	cstr - the name string
 * @return 		pointer to the name type
 */
SaNameT* makeSaNameT(const char* cstr) {
	ENTER();
	unsigned len = strlen(cstr);
	TRACE_INFO("makeSaNameT %u [%s]", len, cstr);
	SaNameT* saname = new SaNameT;
	if (saname != NULL) {
		saNameSet(cstr, saname);
	}
	else {
		TRACE_ERROR("makeSaNameT saname == NULL");
	}
	LEAVE();
	return saname;
}

/**
 * Check if the required functionality is supported by comparing the IMM version
 *
 * @param[in]	currentVersion - loaded version of IMM
 * @param[in]	reqReleaseCode - required release code
 * @param[in]	reqMajorVersion - required major version
 * @param[in]	reqMinorVersion - required minor version
 * @return 		true, if [reqReleaseCode.reqMajorVersion.reqMinorVersion] > currentVersion
 */
bool isFunctionalitySupported(const SaVersionT currentVersion, const SaUint8T reqReleaseCode, const SaUint8T reqMajorVersion, SaUint8T reqMinorVersion)
{
	return (currentVersion.releaseCode > reqReleaseCode ||
			currentVersion.majorVersion > reqMajorVersion ||
			(currentVersion.majorVersion == reqMajorVersion && currentVersion.minorVersion >= reqMinorVersion));
}
