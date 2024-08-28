/*
 * testConfig.cpp
 *
 *  Created on: 26 feb 2012
 *      Author: eaparob
 */

#include <string>

#include "ComMgmtSpiCommon.h"
#include "ComOamSpiModelRepository_1.h"
#include "MafMgmtSpiCommon.h"
#include "MafOamSpiModelRepository_1.h"

#include "testConfig.h"

Test_Config::Test_Config()
{
	pRegStorage = new Registration_Storage();
	pActionStorage = new Action_Storage();
	pAttributeStorage = new Attribute_Storage();
	//xmlParser = new Xml_Parser();
}

void Test_Config::addRegistration(std::string a, std::string b)
{
	pRegStorage->add(a,b);
}

void Test_Config::deleteRegistration(std::string a)
{
	pRegStorage->delete_(a);
}

ComReturnT Test_Config::getRegistration(ComMgmtSpiThreadContext_2T* a, const char* b, const char* c, const char* d)
{
	return (ComReturnT) pRegStorage->get(a,b,c,d);
}

//SDP1694 - support MAF SPI 
ComReturnT Test_Config::maf_getRegistration(MafMgmtSpiThreadContext_2T* a, const char* b, const char* c, const char* d)
{
	return (ComReturnT) pRegStorage->maf_get(a,b,c,d);
}

void Test_Config::setReturnValues(functionReturnValues a)
{
	pRegStorage->set_ReturnValues(a);
}

ComReturnT Test_Config::getReturnValue(std::string a)
{
	return pRegStorage->get_ReturnValue(a);
}

void Test_Config::addAction(std::string a, ComOamSpiMoAttributeType_3T b)
{
	pActionStorage->add(a,b);
}

ComOamSpiMoAttributeType_3T Test_Config::getAction(const char* a, const char* b)
{
	return pActionStorage->get(a,b);
}

void Test_Config::addAttribute(std::string a, Attribute b)
{
	pAttributeStorage->add(a,b);
}

Attribute Test_Config::getAttribute(const char* a, const char* b)
{
	return pAttributeStorage->get(a,b);
}

void Test_Config::printAll()
{
	pRegStorage->print();
	pActionStorage->print();
	pAttributeStorage->print();
}


