/*
 * registrationStorage.h
 *
 *  Created on: Feb 27, 2012
 *      Author: eaparob
 */

#ifndef REGISTRATIONSTORAGE_H_
#define REGISTRATIONSTORAGE_H_

#include <string>
#include <map>
#include <syslog.h>
#include <ComMgmtSpiCommon.h>
#include "ComMgmtSpiThreadContext_2.h"
#include <MafMgmtSpiCommon.h>
#include "MafMgmtSpiThreadContext_2.h"
extern const char * log_prefix;

// Struct for the preconfigured return values
struct functionReturnValues {
	ComReturnT createMo;
	ComReturnT deleteMo;
	ComReturnT setMo;
	ComReturnT getMo;
	ComReturnT action;
	ComReturnT join;
	ComReturnT prepare;
	ComReturnT commit;
	ComReturnT finish;
	ComReturnT abort;
	ComReturnT validate;
};


/********************************************************************************
 *
 * class Registration_Storage
 *
 * Description:
 *
 * Functionality:
 *
 ********************************************************************************/

class Registration_Storage
{
	// Define registration types
	typedef enum {
		ObjectRegistration = 0,
		ClassRegistration = 1,
		UnknownRegistration = 2
	} registrationType;

	// Define permission types
	typedef enum {
		permissionNO = 0,
		permissionYES = 1,
		permissionNotAvailable = 2
	} permissionType;

	// Define a permission_MapType type
	typedef std::map<std::string, std::string> permission_MapType;

	// Create a permissionMap instance for storing the registration config
	permission_MapType permissionMap;

	// The preconfigured return values stored here	
	functionReturnValues returnValues;
	

	Registration_Storage();
	std::string createMocPathfrom3gppDN(std::string);
	void add(std::string, std::string);

	ComReturnT get(ComMgmtSpiThreadContext_2T*, const char*, const char*, const char*);
// SDP1694 - support MAF SPI 
	ComReturnT maf_get(MafMgmtSpiThreadContext_2T*, const char*, const char*, const char*);
	void delete_(std::string);

	void set_ReturnValues(functionReturnValues);
	ComReturnT get_ReturnValue(std::string);
	permissionType FindPermission (const char*, const char*, const char*, registrationType);
	void print();
	std::string stringToLower(std::string str);
	bool exclusiveKeyAttr(std::string className, std::string keyAttrName);
public:
	friend class Test_Config;
};

#endif /* REGISTRATIONSTORAGE_H_ */
