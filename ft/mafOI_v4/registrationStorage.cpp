/*
 * registrationStorage.cpp
 *
 *  Created on: Feb 27, 2012
 *      Author: eaparob
 */

#include "registrationStorage.h"
#include <syslog.h>

extern const char * component_name;

Registration_Storage::Registration_Storage()
{
	returnValues.createMo = MafOk;
	returnValues.deleteMo = MafOk;
	returnValues.setMo    = MafOk;
	returnValues.getMo    = MafOk;
	returnValues.action   = MafOk;
	returnValues.join     = MafOk;
	returnValues.prepare  = MafOk;
	returnValues.commit   = MafOk;
	returnValues.finish   = MafOk;
	returnValues.abort    = MafOk;
	returnValues.validate = MafOk;
}

void Registration_Storage::add(std::string DN, std::string DN_PERMISSION)
{
	permissionMap.insert(std::pair<std::string, std::string>(DN, DN_PERMISSION));
}

void Registration_Storage::delete_(std::string DN_or_MOC)
{
	permission_MapType::iterator iter = permissionMap.find(DN_or_MOC);
		if (iter != permissionMap.end())
		{
			permissionMap.erase(iter);
		}
}

/*
 * This function calls the "FindPermission" function with "ObjectRegistration" and "ClassRegistration".
 * From these outputs: It generates the corresponding: -MafReturnT, -syslogs, -addMessage (if necessary)
 *
 * Input: parent_Dn, class_Name
 *
 * Returns: permissionRet (type: MafReturnT)
 *
 * 			Possible Return values:
 * 									-MafOk
 * 									-MafNotExist
 * 									-MafFailure
 *
 */

MafReturnT Registration_Storage::get(MafMgmtSpiThreadContext_2T* _threadContextIf, const char* parent_Dn, const char* class_Name = 0, const char* key_Attr = 0)
{
	//syslog(LOG_INFO, "%s ENTER function CheckPermission",log_prefix);
	permissionType permission = permissionNotAvailable;
	MafReturnT permissionRet = MafFailure;

	permission = Registration_Storage::FindPermission(parent_Dn, class_Name, key_Attr, ObjectRegistration);
	if(permission == permissionNotAvailable)
	{
		permission = Registration_Storage::FindPermission(parent_Dn, class_Name, key_Attr, ClassRegistration);
	}
	std::string nbi_message;

	switch(permission)
	{
	case permissionYES:
		syslog(LOG_INFO, "%s function CheckPermission: Permission: YES",log_prefix);
		permissionRet = MafOk;
		break;
	case permissionNO:
		syslog(LOG_INFO, "%s function CheckPermission: Permission: NO",log_prefix);
		syslog(LOG_INFO, "%s function CheckPermission: sending addMessage",log_prefix);
		nbi_message = "@ComNbi@Error: Permission denied by ";
		nbi_message += component_name;
		_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());
		syslog(LOG_INFO, "%s function CheckPermission: sending MafNotExist",log_prefix);
		permissionRet = MafNotExist;
		break;
	case permissionNotAvailable:
		syslog(LOG_INFO, "%s function CheckPermission: Permission: N/A",log_prefix);
		syslog(LOG_INFO, "%s function CheckPermission: sending addMessage",log_prefix);
		nbi_message = "@ComNbi@Error: Unexpected callback or Expected callback with wrong parameters in ";
		nbi_message += component_name;
		_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());
		syslog(LOG_INFO, "%s function CheckPermission: sending MafFailure",log_prefix);
		permissionRet = MafFailure;
		break;
	}
	//syslog(LOG_INFO, "%s LEAVE function CheckPermission",log_prefix);
	return permissionRet;
}

/* SDP1694 - support MAF SPI */
MafReturnT Registration_Storage::maf_get(MafMgmtSpiThreadContext_2T* _threadContextIf, const char* parent_Dn, const char* class_Name = 0, const char* key_Attr = 0)
{
	//syslog(LOG_INFO, "%s ENTER function CheckPermission",log_prefix);
	permissionType permission = permissionNotAvailable;
	MafReturnT permissionRet = MafFailure;

	permission = Registration_Storage::FindPermission(parent_Dn, class_Name, key_Attr, ObjectRegistration);
	if(permission == permissionNotAvailable)
	{
		permission = Registration_Storage::FindPermission(parent_Dn, class_Name, key_Attr, ClassRegistration);
	}
	std::string nbi_message;

	switch(permission)
	{
	case permissionYES:
		syslog(LOG_INFO, "%s function CheckPermission: Permission: YES",log_prefix);
		permissionRet = MafOk;
		break;
	case permissionNO:
		syslog(LOG_INFO, "%s function CheckPermission: Permission: NO",log_prefix);
		syslog(LOG_INFO, "%s function CheckPermission: sending addMessage",log_prefix);
		nbi_message = "@ComNbi@Error: Permission denied by ";
		nbi_message += component_name;
		_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());
		syslog(LOG_INFO, "%s function CheckPermission: sending MafNotExist",log_prefix);
		permissionRet = MafNotExist;
		break;
	case permissionNotAvailable:
		syslog(LOG_INFO, "%s function CheckPermission: Permission: N/A",log_prefix);
		syslog(LOG_INFO, "%s function CheckPermission: sending addMessage",log_prefix);
		nbi_message = "@ComNbi@Error: Unexpected callback or Expected callback with wrong parameters in ";
		nbi_message += component_name;
		_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());
		syslog(LOG_INFO, "%s function CheckPermission: sending MafFailure",log_prefix);
		permissionRet = MafFailure;
		break;
	}
	//syslog(LOG_INFO, "%s LEAVE function CheckPermission",log_prefix);
	return permissionRet;
}

void Registration_Storage::set_ReturnValues(functionReturnValues retValues)
{
	returnValues.createMo = retValues.createMo;
	returnValues.deleteMo = retValues.deleteMo;
	returnValues.setMo    = retValues.setMo;
	returnValues.getMo    = retValues.getMo;
	returnValues.action   = retValues.action;
	returnValues.join     = retValues.join;
	returnValues.prepare  = retValues.prepare;
	returnValues.commit   = retValues.commit;
	returnValues.finish   = retValues.finish;
	returnValues.abort    = retValues.abort;
	returnValues.validate = retValues.validate;
}


MafReturnT Registration_Storage::get_ReturnValue(std::string functionName)
{
	     if(functionName == "create") {return returnValues.createMo;}
	else if(functionName == "delete") {return returnValues.deleteMo;}
	else if(functionName == "set")    {return returnValues.setMo;}
	else if(functionName == "get")    {return returnValues.getMo;}
	else if(functionName == "action") {return returnValues.action;}
	else if(functionName == "join")   {return returnValues.join;}
	else if(functionName == "prepare"){return returnValues.prepare;}
	else if(functionName == "commit") {return returnValues.commit;}
	else if(functionName == "finish") {return returnValues.finish;}
	else if(functionName == "abort")  {return returnValues.abort;}
	else if(functionName == "validate")  {return returnValues.validate;}
	else {return MafFailure;}
}

/*
 * This function checks the permission of the given DN in "permissionMap".
 * "permissionMap" is configured in "defines.h" and loaded registration-time.
 *
 * It returns "permissionYES" if "YES" found as the value of DN's key in "permissionMap".
 * It returns "permissionNO"  if "NO"  found as the value of DN's key in "permissionMap".
 * It returns "permissionNotAvailable" if no DN key found in "permissionMap".
 *
 * Input: parent_Dn, class_Name, registration_type
 *
 * Returns: permission (type: permissionType)
 *
 * 			Possible Return values:
 * 									-permissionYES
 * 									-permissionNO
 * 									-permissionNotAvailable
 *
 */
Registration_Storage::permissionType Registration_Storage::FindPermission (const char* parent_Dn, const char* class_Name = 0, const char* key_Attr = 0, registrationType registration_type = UnknownRegistration)
{
	//syslog(LOG_INFO, "%s ENTER function CheckPermission",log_prefix);
	permissionType permission = permissionNotAvailable;
	std::string mocPath = parent_Dn;
	std::string registrationStr = "";

	if(class_Name != 0)
	{
		mocPath = mocPath + "," + class_Name;
	}

	if(registration_type == ObjectRegistration)
	{
		registrationStr = "Object";
	}
	else if(registration_type == ClassRegistration)
	{
		mocPath = createMocPathfrom3gppDN(mocPath);
		if(key_Attr != 0)
		{
			// if it is an exclusive key attribute, then append it to the moc path
			if(Registration_Storage::exclusiveKeyAttr(class_Name, key_Attr))
			{
				mocPath = mocPath + "." + key_Attr;
			}
		}
		registrationStr = "Class";
	}
	syslog(LOG_INFO, "%s function CheckPermission mocPath: %s",log_prefix, mocPath.c_str());
	// Iterate the map and look for DN name
	permission_MapType::iterator iter = permissionMap.find(mocPath);

	if (iter != permissionMap.end() )
	{
		if (iter->second == "YES")
		{
			syslog(LOG_INFO, "%s permission setting found by function CheckPermission: YES for DN: %s for %s registration",log_prefix, mocPath.c_str(), registrationStr.c_str());
			permission = permissionYES;
		}
		else if (iter->second == "NO")
		{
			syslog(LOG_INFO, "%s permission setting found by function CheckPermission: NO for DN: %s for %s registration",log_prefix, mocPath.c_str(), registrationStr.c_str());
			permission = permissionNO;
		}
	}
	else
	{
		syslog(LOG_INFO, "%s NO permission setting found by function CheckPermission for DN: %s for %s registration",log_prefix, mocPath.c_str(), registrationStr.c_str());
		permission = permissionNotAvailable;
	}

	//syslog(LOG_INFO, "%s LEAVE function CheckPermission",log_prefix);
	return permission;
}

/*
 * This function creates MocPath in IMM-format from 3gpp DN.
 *
 * Input: DN
 *
 * Returns: mocPath
 *
 */
std::string Registration_Storage::createMocPathfrom3gppDN(std::string DN)
{
	//syslog(LOG_INFO, "%s ENTER function createMocPathfrom3gppDN with DN: %s",log_prefix,DN.c_str());
	std::string mocPath;
	size_t eq_index;
	size_t digit_index;

	while((eq_index=DN.find("="))!=std::string::npos) //while there exists a "=" in the string
	{
		digit_index = eq_index + 1;

		while (isdigit(DN[digit_index])) //count the digits after "="
		{
			digit_index++;
		}

		DN.erase(eq_index, digit_index - eq_index); //remove "=" and the following (previously counted) digits
	}

	while((eq_index=DN.find(","))!=std::string::npos) //while there exists a "," in the string
	{
		DN.replace(eq_index,1,"/"); //replace "," char (eq_index in the string) with "/"
	}

	mocPath = "/" + DN;

	//syslog(LOG_INFO, "%s LEAVE function createMocPathfrom3gppDN with mocPath: %s",log_prefix,mocPath.c_str());
	return mocPath;
}

void Registration_Storage::print()
{
	permission_MapType::iterator iter = permissionMap.begin();
	while(iter != permissionMap.end())
	{
		syslog(LOG_INFO, "%s *** Internal config: Registration: %s permission: %s",log_prefix, iter->first.c_str(), iter->second.c_str());
		iter++;
	}
}

std::string Registration_Storage::stringToLower(std::string str)
{
	const int length = str.length();
	for(int i = 0; i < length; i++)
	{
		str[i] = std::tolower(str[i]);
	}
	return str;
}

bool Registration_Storage::exclusiveKeyAttr(std::string className, std::string keyAttrName)
{
	if(strcmp(stringToLower(className + "id").c_str(), stringToLower(keyAttrName).c_str()) == 0)
		{
			return false;
		}
		else
		{
			return true;
		}
}
