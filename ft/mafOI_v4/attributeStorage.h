/*
 * attributeStorage.h
 *
 *  Created on: Feb 27, 2012
 *      Author: eaparob
 *
 *   Modified: xnikvap 2012-08-30  support for COM MO SPI Ver.3 (Ver.1 is not supported any more)
 */

#ifndef ATTRIBUTESTORAGE_H_
#define ATTRIBUTESTORAGE_H_

#include "MafOamSpiManagedObject_3.h"
typedef struct Attribute {
		MafOamSpiMoAttributeType_3T attrType;
		std::string attrValue;
	} Attribute;

/********************************************************************************
 *
 * class Attribute_Storage
 *
 * Description:
 *
 * Functionality:
 *
 ********************************************************************************/
class Attribute_Storage
{
	// Define a attribute_MapType
	typedef std::map<std::string, Attribute> attribute_MapType;
	attribute_MapType attribute_Map;
	Attribute_Storage(){};
	void add(std::string, Attribute);
	Attribute get(const char*, const char*);
	void print();
public:
	friend class Test_Config;
};

#endif /* ATTRIBUTESTORAGE_H_ */
