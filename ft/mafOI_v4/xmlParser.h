/*
 * xmlParser.h
 *
 *  Created on: Nov 15, 2012
 *      Author: eaparob
 */

#ifndef TESTCOMPXMLPARSER_H_
#define TESTCOMPXMLPARSER_H_

#include <syslog.h>
#include <libxml2/libxml/parser.h>
#include <libxml2/libxml/xmlmemory.h>
//#include <libxml2/libxml/tree.h>
//#include <libxml/parser.h>
//#include <libxml/xmlmemory.h>

extern const char * log_prefix;

#define xml_file "/home/testcomp.xml"
#define xml_root "testcomponent_config"

#define xml_config "config"

#define xml_component_name "component_name"
#define xml_alarm_service_enabled "alarm_service_enabled"
#define xml_log_service_enabled "log_service_enabled"
#define xml_startup_logwrite "startup_logwrite"
#define xml_startup_logwrite_delay "startup_logwrite_delay"
#define xml_skip_error "skip_error"
#define xml_unregister_all "unregister_all"
#define xml_return_value_config "return_value_config"

#define _createMo "createMo"
#define _deleteMo "deleteMo"
#define _setMo "setMo"
#define _getMo "getMo"
#define _action "action"
#define _join "join"
#define _prepare "prepare"
#define _commit "commit"
#define _finish "finish"
#define _abort "abort"

#define xml_reg "registrations"
#define _REG "REG"

#define xml_attr "attributes"
#define _ATTR "ATTR"

#define xml_act "actions"
#define _ACTION "ACTION"

#define _DN_or_MOC "DN_or_MOC"
#define _PERMISSION "PERMISSION"
#define _TYPE "TYPE"
#define _VALUE "VALUE"

/********************************************************************************
 *
 * class Xml_Parser
 *
 * Description: loads the testconfig xml file and parses it
 *
 ********************************************************************************/

class Xml_Parser
{
	Xml_Parser();
	std::string parseNode(xmlDocPtr doc, xmlNodePtr cur, const char * str);
	xmlNodePtr getXmlConfigNodes(xmlNodePtr current, const char * xmlConfig);
	xmlNodePtr getXmlroot(xmlDocPtr doc, xmlNodePtr cur, const char * xmlRoot);
	void setupTestConfig(xmlDocPtr doc, xmlNodePtr cur, std::string name);
	void parseReturnValues(xmlDocPtr doc, xmlNodePtr configNode, const char * node_name);
	void loadReturnValues(xmlDocPtr doc, xmlNodePtr configNode);
	void loadConfig(xmlDocPtr doc, xmlNodePtr configNode, std::string name);
	void loadXmlConfig();

public:
	friend class Test_Config;
};

#endif /* TESTCOMPXMLPARSER_H_ */
