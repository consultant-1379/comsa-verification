/*
 * actionStorage.h
 *
 *  Created on: Feb 27, 2012
 *      Author: eaparob
 *
 *   Modified: xnikvap 2012-08-30  support for COM MO SPI Ver.3 (Ver.1 is not supported any more)
 */

#ifndef ACTIONSTORAGE_H_
#define ACTIONSTORAGE_H_

#include <map>
#include <string>
using namespace std;
#include "ComOamSpiManagedObject_3.h"

/********************************************************************************
 *
 * class Action_Storage
 *
 * Description:
 *
 * Functionality:
 *
 ********************************************************************************/
class Action_Storage
{
	// Define a actionTest_MapType
	typedef std::map<std::string, ComOamSpiMoAttributeType_3T> actionTest_MapType;
	actionTest_MapType actionTest_Map;
	Action_Storage(){};
	void add(std::string, ComOamSpiMoAttributeType_3T);
	ComOamSpiMoAttributeType_3T get(const char*, const char*);
	void print();
public:
	friend class Test_Config;
};

#endif /* ACTIONSTORAGE_H_ */
