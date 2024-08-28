/*
 * attributeStorage.cpp
 *
 *  Created on: Feb 27, 2012
 *      Author: eaparob
 */

#include <syslog.h>
#include <string>
#include <map>
#include "attributeStorage.h"

extern const char * log_prefix;
extern const char * component_name;

void Attribute_Storage::add(std::string ATTR, Attribute AttributeStruct)
{
	attribute_Map.insert(std::pair<std::string, Attribute>(ATTR, AttributeStruct));
}

/*
 * This function gets the given attribute from testOI database
 *
 * Input: parent_Dn, class_Name
 *
 * Returns: AttributeValue (type: string)
 *
 */
Attribute Attribute_Storage::get (const char* parent_Dn, const char* class_Name = 0)
{
	std::string attrPath = parent_Dn;
	Attribute returnAttribute;
	returnAttribute.attrValue = "";

	if(class_Name != 0)
	{
		attrPath = attrPath + "," + class_Name;
	}

	syslog(LOG_INFO, "%s function getMoAttributeFromTestOiInternalConfig Attribute full DN: %s",log_prefix, attrPath.c_str());
	// Iterate the map and look for the attribute
	attribute_MapType::iterator iter = attribute_Map.find(attrPath);

	if (iter != attribute_Map.end() )
	{
		returnAttribute = iter->second;
		syslog(LOG_INFO, "%s function getMoAttributeFromTestOiInternalConfig: attribute exists in %s database: %s type: %i value: %s",log_prefix,component_name,attrPath.c_str(), returnAttribute.attrType, returnAttribute.attrValue.c_str());
	}
	else
	{
		returnAttribute.attrValue = "ATTR NOT EXISTS";
		syslog(LOG_INFO, "%s function getMoAttributeFromTestOiInternalConfig: attribute NOT exists in %s database",log_prefix,component_name);
	}
	return returnAttribute;
}

void Attribute_Storage::print()
{
	attribute_MapType::iterator iter = attribute_Map.begin();
	while(iter != attribute_Map.end())
	{
		syslog(LOG_INFO, "%s *** Internal config: Attribute name: %s type: %i value: %s",log_prefix, iter->first.c_str(), iter->second.attrType, iter->second.attrValue.c_str());
		iter++;
	}
}
