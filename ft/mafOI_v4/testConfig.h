/*
 * testConfig.h
 *
 *  Created on: 27 feb 2012
 *      Author: eaparob
 *
 *   Modified: xnikvap 2012-08-30  support for COM MO SPI Ver.3 (Ver.1 is not supported any more)
 */

#ifndef TESTCONFIG_H_
#define TESTCONFIG_H_

#include <syslog.h>
#include <string>
#include "registrationStorage.h"
#include "actionStorage.h"
#include "attributeStorage.h"
#include "xmlParser.h"

/********************************************************************************
 *
 * class Test_Config
 *
 * Description:
 *
 * Functionality:
 *
 ********************************************************************************/
class Test_Config
{
	Registration_Storage * pRegStorage;
	Action_Storage * pActionStorage;
	Attribute_Storage * pAttributeStorage;
	Xml_Parser * xmlParser;
public:
	Test_Config();

	// Registration config (DN/class registrations and their permissions)
	void addRegistration(std::string, std::string);

	MafReturnT getRegistration(MafMgmtSpiThreadContext_2T*, const char*, const char* = 0, const char* = 0);
//SDP1694 - support MAF SPI
	MafReturnT maf_getRegistration(MafMgmtSpiThreadContext_2T*, const char*, const char* = 0, const char* = 0);
	void deleteRegistration(std::string);

	// Preconfigure the return values for all callbacks
	void setReturnValues(functionReturnValues);
	MafReturnT getReturnValue(std::string);


	// Action test configurations
	void addAction(std::string, MafOamSpiMoAttributeType_3T);
	MafOamSpiMoAttributeType_3T getAction(const char*, const char*);

	// Attribute configurations
	void addAttribute(std::string, Attribute);
	Attribute getAttribute(const char*, const char*);

	// Print all test configuration
	void printAll();
};

// ******************************************************************************

#endif /* TESTCONFIG_H_ */
