/*
 * actionStorage.cpp
 *
 *  Created on: Feb 27, 2012
 *      Author: eaparob
 *
 *   Modified: xnikvap 2012-08-30  support for COM MO SPI Ver.3 (Ver.1 is not supported any more)
 */

#include <syslog.h>
#include "actionStorage.h"

extern const char * log_prefix;
extern const char * component_name;

void Action_Storage::add(std::string ACTION, MafOamSpiMoAttributeType_3T ACTION_TYPE)
{
	actionTest_Map.insert(std::pair<std::string, MafOamSpiMoAttributeType_3T>(ACTION, ACTION_TYPE));
}

/*
 * This function gets the given attribute from testOI database
 *
 * Input: parent_Dn, class_Name
 *
 * Returns: AttributeValue (type: string)
 *
 */
MafOamSpiMoAttributeType_3T Action_Storage::get(const char* ActionTestDN, const char* methodName)
{
	//syslog(LOG_INFO, "%s ENTER function getActionParamType",log_prefix);
	std::string actionTestMethodPath = ActionTestDN;
	MafOamSpiMoAttributeType_3T returnActionParamType;

	actionTestMethodPath = actionTestMethodPath + "," + methodName;
	syslog(LOG_INFO, "%s function getActionParamType ActionTest method full path: %s",log_prefix, actionTestMethodPath.c_str());

	// Iterate the map and look for the ActionTest method
	actionTest_MapType::iterator iter = actionTest_Map.find(actionTestMethodPath);

	if (iter != actionTest_Map.end() )
	{
		returnActionParamType = iter->second;
		syslog(LOG_INFO, "%s function getActionParamType: actionTest method configured in %s: %s type: %i",log_prefix,component_name,actionTestMethodPath.c_str(), returnActionParamType);
	}
	else
	{
	    returnActionParamType = MafOamSpiMoAttributeType_3_INT8;  // used to be _VOID, but this is not supported in MO SPI Ver.3
		syslog(LOG_INFO, "%s function getActionParamType: actionTest method NOT configured in %s: %s",log_prefix,component_name,actionTestMethodPath.c_str());
	}

	//syslog(LOG_INFO, "%s LEAVE function getActionParamType",log_prefix);
	return returnActionParamType;
}

void Action_Storage::print()
{
	actionTest_MapType::iterator iter = actionTest_Map.begin();
	while(iter != actionTest_Map.end())
	{
		syslog(LOG_INFO, "%s *** Internal config: Action: %s type: %i",log_prefix, iter->first.c_str(), iter->second);
		iter++;
	}
}
