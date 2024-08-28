/*
 * xmlParser.cpp
 *
 *  Created on: Nov 15, 2012
 *      Author: eaparob
 */

#include <stdio.h>
#include <string.h>
#include <sstream>
#include "xmlParser.h"

extern MafReturnT loadMocOrDnConfig(std::string DN_or_MOC, std::string DN_PERMISSION);

Xml_Parser::Xml_Parser()
{
	//syslog(LOG_INFO, "%s Xml_Parser::Xml_Parser(): ENTER",log_prefix);
	Xml_Parser::loadXmlConfig();
	//syslog(LOG_INFO, "%s Xml_Parser::Xml_Parser(): LEAVE",log_prefix);
}

// This function returns the value of the input node
// if e.g.: <component_name>testcomp</component_name>
//        input is: "component_name"
//        return value is: "testcomp"
std::string Xml_Parser::parseNode(xmlDocPtr doc, xmlNodePtr cur, const char * str)
{
	xmlChar *key;
	while (cur != NULL)
	{
		if ((!xmlStrcmp(cur->name, (const xmlChar *)str)))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			//printf("keyword: %s\n", key);
			std::string ret = (const char *)key;
			//xmlFree(key);
			return ret;
		}
		cur = cur->next;
	}
	return "";
}

xmlNodePtr Xml_Parser::getXmlConfigNodes(xmlNodePtr current, const char * xmlConfig)
{
	xmlNodePtr cur = current->xmlChildrenNode;
	while (cur != NULL)
	{
		if ((!xmlStrcmp(cur->name, (const xmlChar *)xmlConfig)))
		{
			//printf("xml node found: %s\n", xmlConfig);
			return cur;
		}
		cur = cur->next;
	}
	return NULL;
}

xmlNodePtr Xml_Parser::getXmlroot(xmlDocPtr doc, xmlNodePtr cur, const char * xmlRoot)
{
	//syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): ENTER with xmlRoot=(%s)",log_prefix,xmlRoot);
	if(xmlRoot == NULL)
	{
		syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): error: no xml root input",log_prefix);
		xmlFreeDoc(doc);
		return NULL;
	}

	// open XML file to parse
	syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): open XML file to parse: xml_file=\"%s\"",log_prefix,xml_file);
	doc = xmlParseFile(xml_file);
	//syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): check if XML file exists",log_prefix);
	if (doc == NULL )
	{
		syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): error reading xml",log_prefix);
		xmlFreeDoc(doc);
		return NULL;
	}

	// get root element
	//syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): get root element",log_prefix);
	cur = xmlDocGetRootElement(doc);
	if (cur == NULL)
	{
		syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): error empty xml",log_prefix);
		xmlFreeDoc(doc);
		return NULL;
	}

	// check if it the correct root element
	// if correct: return the pointer
	// else: return NULL
	if (xmlStrcmp(cur->name, (const xmlChar *)xmlRoot))
	{
		syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): error: xml_root not found",log_prefix);
		return NULL;
	}
	else
	{
		syslog(LOG_INFO, "%s Xml_Parser::getXmlroot(): xml_root found: %s",log_prefix, xmlRoot);
		return cur;
	}
}

void Xml_Parser::setupTestConfig(xmlDocPtr doc, xmlNodePtr cur, std::string name)
{
	xmlNodePtr configNode1, configNode2, configNode3;
	std::string input1, input2, input3, key1, key2, key3;
	bool attrCase = false;
	if(name == _REG)
	{
		input1 = _DN_or_MOC;
		input2 = _PERMISSION;
	}
	else if(name == _ATTR)
	{
		attrCase = true;
		input1 = _DN_or_MOC;
		input2 = _TYPE;
		input3 = _VALUE;
	}
	else if(name == _ACTION)
	{
		input1 = _DN_or_MOC;
		input2 = _TYPE;
	}
	configNode1 = getXmlConfigNodes(cur, input1.c_str());
	configNode2 = getXmlConfigNodes(cur, input2.c_str());
	if(attrCase)
	{
		configNode3 = getXmlConfigNodes(cur, input3.c_str());
	}
	// check only the first 2 (configNode1 and configNode2)
	if(configNode1 != NULL && configNode2 != NULL)
	{
		key1 = parseNode(doc, configNode1, input1.c_str());
		key2 = parseNode(doc, configNode2, input2.c_str());
		if(attrCase && configNode3 != NULL)
		{
			key3 = parseNode(doc, configNode3, input3.c_str());
		}
		//printf("%s\n", key1.c_str());
		//printf("%s\n", key2.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::setupTestConfig(): (%s)",log_prefix, key1.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::setupTestConfig(): (%s)",log_prefix, key2.c_str());
		if(attrCase)
		{
			//printf("%s\n\n", key3.c_str());
			syslog(LOG_INFO, "%s Xml_Parser::setupTestConfig(): (%s)",log_prefix, key3.c_str());
		}
		if(name == _REG)
		{
			syslog(LOG_INFO, "%s Xml_Parser::setupTestConfig(): call loadMocOrDnConfig() with (%s) (%s)",log_prefix, key1.c_str(), key2.c_str());
			loadMocOrDnConfig(key1, key2);
			syslog(LOG_INFO, "%s Xml_Parser::setupTestConfig(): after calling loadMocOrDnConfig()",log_prefix);
		}
	}
}

void Xml_Parser::parseReturnValues(xmlDocPtr doc, xmlNodePtr configNode, const char * node_name)
{
	xmlNodePtr node;
	node  = getXmlConfigNodes(configNode, node_name);
	std::string key;
	if(node != NULL)
	{
		key = parseNode(doc, node, node_name);
		//printf("\n%s = (%s)\n",node_name,key.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::parseReturnValues(): %s = (%s)",log_prefix, node_name, key.c_str());
	}
}

void Xml_Parser::loadReturnValues(xmlDocPtr doc, xmlNodePtr configNode)
{
	parseReturnValues(doc, configNode, _createMo);
	parseReturnValues(doc, configNode, _deleteMo);
}

void Xml_Parser::loadConfig(xmlDocPtr doc, xmlNodePtr configNode, std::string name)
{
	for(int i = 1; i < 1000; i++)
	{
		xmlNodePtr node;
		std::stringstream num;
		num << i;
		std::string str  = name + num.str();
		node  = getXmlConfigNodes(configNode, str.c_str());
		if(node != NULL)
		{
			setupTestConfig(doc, node, name);
		}
	}
}

void Xml_Parser::loadXmlConfig()
{
	syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): ENTER",log_prefix);
	xmlDocPtr doc;
	xmlNodePtr cur, configNode, globalConfigNode;
	std::string globalConfig = "";
	cur = getXmlroot(doc, cur, xml_root);
	if(cur != NULL)
	{
		// load "config" from xml file
		configNode = getXmlConfigNodes(cur, xml_config);

		// load global configs from xml file
		globalConfigNode = getXmlConfigNodes(configNode, xml_component_name);
		globalConfig = parseNode(doc, globalConfigNode, xml_component_name);
		//printf("%s = (%s)\n", xml_component_name, globalConfig.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): %s = (%s)",log_prefix, xml_component_name, globalConfig.c_str());

		globalConfigNode = getXmlConfigNodes(configNode, xml_alarm_service_enabled);
		globalConfig = parseNode(doc, globalConfigNode, xml_alarm_service_enabled);
		//printf("%s = (%s)\n", xml_alarm_service_enabled, globalConfig.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): %s = (%s)",log_prefix, xml_alarm_service_enabled, globalConfig.c_str());

		globalConfigNode = getXmlConfigNodes(configNode, xml_log_service_enabled);
		globalConfig = parseNode(doc, globalConfigNode, xml_log_service_enabled);
		//printf("%s = (%s)\n", xml_log_service_enabled, globalConfig.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): %s = (%s)",log_prefix, xml_log_service_enabled, globalConfig.c_str());

		globalConfigNode = getXmlConfigNodes(configNode, xml_startup_logwrite);
		globalConfig = parseNode(doc, globalConfigNode, xml_startup_logwrite);
		//printf("%s = (%s)\n", xml_startup_logwrite, globalConfig.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): %s = (%s)",log_prefix, xml_startup_logwrite, globalConfig.c_str());

		globalConfigNode = getXmlConfigNodes(configNode, xml_startup_logwrite_delay);
		globalConfig = parseNode(doc, globalConfigNode, xml_startup_logwrite_delay);
		//printf("%s = (%s)\n", xml_startup_logwrite_delay, globalConfig.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): %s = (%s)",log_prefix, xml_startup_logwrite_delay, globalConfig.c_str());

		globalConfigNode = getXmlConfigNodes(configNode, xml_skip_error);
		globalConfig = parseNode(doc, globalConfigNode, xml_skip_error);
		//printf("%s = (%s)\n", xml_skip_error, globalConfig.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): %s = (%s)",log_prefix, xml_skip_error, globalConfig.c_str());

		globalConfigNode = getXmlConfigNodes(configNode, xml_unregister_all);
		globalConfig = parseNode(doc, globalConfigNode, xml_unregister_all);
		//printf("%s = (%s)\n", xml_unregister_all, globalConfig.c_str());
		syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): %s = (%s)",log_prefix, xml_unregister_all, globalConfig.c_str());

		//printf("\nLoad %s config\n\n", xml_return_value_config);
		globalConfigNode = getXmlConfigNodes(configNode, xml_return_value_config);
		loadReturnValues(doc, globalConfigNode);

		// load registration configs from xml file
		//printf("\nLoad %s config\n\n", xml_reg);
		configNode = getXmlConfigNodes(cur, xml_reg);
		loadConfig(doc, configNode, _REG);

		// load attribute configs from xml file
		//printf("\nLoad %s config\n\n", xml_attr);
		configNode = getXmlConfigNodes(cur, xml_attr);
		loadConfig(doc, configNode, _ATTR);

		// load action configs from xml file
		//printf("\nLoad %s config\n\n", xml_act);
		configNode = getXmlConfigNodes(cur, xml_act);
		loadConfig(doc, configNode, _ACTION);
	}

	//xmlFreeDoc(doc);
	syslog(LOG_INFO, "%s Xml_Parser::loadXmlConfig(): LEAVE",log_prefix);
	return;
}
