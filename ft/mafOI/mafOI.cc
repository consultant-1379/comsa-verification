/**
 *   Copyright (C) 2010 by Ericsson AB
 *   S - 125 26  STOCKHOLM
 *   SWEDEN, tel int + 46 10 719 0000
 *
 *   The copyright to the computer program herein is the property of
 *   Ericsson AB. The program may be used and/or copied only with the
 *   written permission from Ericsson AB, or in accordance with the terms
 *   and conditions stipulated in the agreement/contract under which the
 *   program has been supplied.
 *
 *   All rights reserved.
 *
 *
 *   File:   mafOI.cc
 *
 *   Author: eozasaf
 *
 *   Date:   2011-08-29
 *
 *   A test COM (CCF) OI component. Initial version having the skeleton COM component structure along with the retrieval of
 *   ComOamSpiRegisterObjectImplementer_1, ComMgmtSpiThreadContext_2, ComOamSpiTransaction_2 interfaces from the COM SPI Interface portal
 *
 *	 Modified: eozasaf 2011-09-02 Implemented the ComOamSpiManagedObject_1T and ComOamSpiTransactionalResource_2T interfaces as mocks
 *
 *	 Modified: eaparob 2011-10-31 Implemented the functions for checking permissions for the transactions: -"CheckPermissionForObjAndClass", -"CheckPermission"
 *	 								Other implemented function: -"createMocPathfrom3gppDN"
 *									The permissions are configured in defines.h and loaded to "permission_Map" in registration time.
 *									New function-calls added: -"registerParticipant" is called in "join" function.
 *																-"addMessage" is called in function "CheckPermissionForObjAndClass" in case of "permissionNO" and "permissionNotAvailable"
 *
 *	 Modified: eaparob 2011-11-17 Implemented the functions for looking up runtime non-cached attributes for the function "getMoAttribute": -"getMoAttributeFromtestOiDB"
 *	 								The attribute data is configured in defines.h and loaded to "attribute_Map" in "start" function.
 *	 								Other implemented parts: -"attribute_Map" created
 *	 															-"getMoAttribute" function is able to handle runtime non-cached attributes
 *	 															-"setMoAttribute" function is able to handle writable config (cached) attributes
 *
 *	 Modified: eaparob 2011-12-12 Modified parts:          -"actionTest_Map" created
 *	 															-functionality of "getMoAttribute" function is extended
 *	 															-functionality of "setMoAttribute" function is extended
 *	 															-"action" function is corrected and extended
 *	 															-the way of loading config from defines.h changed
 *
 *	 Modified: eaparob 2012-02-16 Modified parts:          -functions added to handle complex data types for getMoAttribute call
 *	 														-functions added to handle complex data types for setMoAttribute call
 *	 														-prefix parameter added to all syslog
 *
 *	 Modified: eaparob 2012-02-28 Modified parts:       Split out some functions and added into new source and header files:
 *																				-testConfig.cpp
 *	 																				-registrationStorage.cpp
 *	 																				-actionStorage.cpp
 *	 																				-attributeStorage.cpp
 *
 *	 																				-testConfig.h
 *	 																				-registrationStorage.h
 *	 																				-actionStorage.h
 *	 																				-attributeStorage.h
 *
 *	 Modified: eaparob 2012-03-24 Modified parts:       -DN and MOC registration config changed to REG (from now there is no need to set the regtype)
 *                                                      -new functionality added to filter out unwanted callbacks from outside ("testConfig->getRegistration")
 *
 *	 Modified: eaparob 2012-04-10 Modified parts:       -testComponentControl function created to control the testOI by an action
 *
 *	 Modified: eaparob 2012-07-10 Modified parts:       -startupLogWriteThread function created. This can be enabled in defines.h
 *
 *	 Modified: xnikvap 2012-07-28 Modified parts:       converted to MO SPI Ver.3
 *
 *	 Modified: xjonbuc 2012-09-06 Modified parts:      Created mafLCMinit() and modified existing parts to use MAF SPI to align with product code
 *
 *	 Modified: eaparob 2012-11-06 Memory leaks fixed:   -new function created: saveToDeleteList(), freeDeleteList(), freeContainer()
 *															-saveToDeleteList() added to getMoAttribute() and to maf_getMoAttribute()
 *															-freeDeleteList() added to finish() function
 *															-memory freeing added to doneWithValue() function
 *
 *	 Modified: eaparob 2012-11-22 Modified parts:       -createMO/maf_createMO: keyAttributeName added as an input of the getRegistration/maf_getRegistration call to handle the exclusive key attributes.
 *
 *   Modified: eaparob 2013-02-19 Modified parts:       -test consumer functionality implemented for CM events (FT1724)
 *
 *   Modified: xjonbuc 2013-05-16  Implemented support for any return type from action()
 *
 *   Modified: eaparob 2014-03-31:                      -LOG and TRACE service overloading functions implemented (main methods: "startupLogSpamThread", "startupTraceSpamThread")
 *   Modified: xadaleg 2014-01-09  MR-29443 - align to ECIM FM 4.0
 *                                 MR-29443: Update mafOI.cc to handle alarms from V4
 *   Modified: xdonngu 2014-04-18  Re-implement freeContainer to release the allocated memory.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <sstream>

#include "ComMgmtSpiCommon.h"
#include "ComMgmtSpiComponent_1.h"
#include "ComMgmtSpiInterface_1.h"
#include "ComMgmtSpiInterfacePortal_1.h"
#include "MafMgmtSpiInterfacePortal_1.h"
#include "ComMgmtSpiInterfacePortalAccessor.h"
#include "ComOamSpiServiceIdentities_1.h"
#include "ComMgmtSpiServiceIdentities_1.h"
#include "ComOamSpiRegisterObjectImplementer_1.h"
#include "ComOamSpiTransaction_2.h"
#include "ComOamSpiTransactionalResource_2.h"
#include "ComOamSpiManagedObject_3.h"
#include "ComMgmtSpiThreadContext_2.h"
//#include "ComOamSpiEvent_1.h"
#include "MafOamSpiEvent_1.h"
//#include "ComOamSpiNotificationFm_2.h"
#include "MafOamSpiNotificationFm_1.h"
#include "MafOamSpiNotificationFm_2.h"
#include "MafOamSpiNotificationFm_3.h"
#ifdef ALARMS4
#include "MafOamSpiNotificationFm_4.h"
#endif
#include "MafOamSpiServiceIdentities_1.h"
#include "ComMwSpiServiceIdentities_1.h"
#include "ComMwSpiLog_1.h"
#include "ComMwSpiTrace_1.h"

#include "MafMgmtSpiCommon.h"
#include "MafMgmtSpiComponent_1.h"
#include "MafMgmtSpiInterface_1.h"
#include "MafMgmtSpiInterfacePortal_1.h"
#include "MafMgmtSpiInterfacePortalAccessor.h"
#include "MafOamSpiServiceIdentities_1.h"
#include "MafMgmtSpiServiceIdentities_1.h"
#include "MafOamSpiRegisterObjectImplementer_1.h"
#include "MafOamSpiTransaction_2.h"
#include "MafOamSpiTransactionalResource_2.h"
#include "MafOamSpiManagedObject_3.h"
#include "MafMgmtSpiThreadContext_2.h"
#include "MafMwSpiServiceIdentities_1.h"
#include "MafMwSpiLog_1.h"
#include "MafOamSpiCmEvent_1.h"
#include "saNtf.h"
#include <map>
#include <string>
#include <assert.h>
#include <cstring>
#include <vector>
#include <list>
#include <syslog.h>
#include <pthread.h>
#include <time.h>
#include "testConfig.h"

using namespace std;

#ifdef __GNUC__
#  define UNUSED(x) UNUSED_ ## x __attribute__((__unused__))
#else
#  define UNUSED(x) UNUSED_ ## x
#endif

#ifdef __GNUC__
#  define UNUSED_FUNCTION(x) __attribute__((__unused__)) UNUSED_ ## x
#else
#  define UNUSED_FUNCTION(x) UNUSED_ ## x
#endif

ComMgmtSpiInterfacePortal_1T* _portal;
MafMgmtSpiInterfacePortal_1T* _portal_MAF;
ComMgmtSpiComponent_1T component;
ComMgmtSpiInterface_1T* interfaceArray[3];
ComMgmtSpiInterface_1T* dependencyArray[2];
ComOamSpiManagedObject_3T managedObjectIf;
ComOamSpiTransactionalResource_2T transactionalResourceIf;
ComMgmtSpiThreadContext_2T* _threadContextIf;
ComOamSpiRegisterObjectImplementer_1T* _registerObjectImplementerIf;
ComOamSpiTransaction_2T * _transactionIf;
ComOamSpiTransactionalResource_2T * _txResourceIf;
MafOamSpiEventRouter_1T* _eventRouter;
ComMwSpiLog_1T* _logServiceIf;
ComMwSpiTrace_1T* _traceServiceIf;
MafNameValuePairT ** filter_from_addFilter;


/* SDP1694 - support MAF SPI */
MafMgmtSpiThreadContext_2T* _maf_threadContextIf;
MafMgmtSpiInterface_1T* maf_interfaceArray[3];
MafMgmtSpiInterface_1T* maf_dependencyArray[2];
MafMwSpiLog_1T* maf_logServiceIf;
MafMgmtSpiComponent_1T maf_component;
#ifndef ALARMS4
MafOamSpiNotificationFmStruct_2T *notificationStruct;
#else
MafOamSpiNotificationFmStruct_4T *notificationStruct;
#endif



Test_Config * testConfig;

// if component name defined, then use it
#ifdef COMPONENT_NAME
std::string log_prefix_str = COMPONENT_NAME;
#else
// default component name
std::string log_prefix_str = "MAFOiComponent";
#endif

const char * component_name = strdup((log_prefix_str).c_str());
const char * log_prefix = strdup((log_prefix_str + ':').c_str());

typedef struct StructType {
	std::string type;
	std::string name;
	std::vector<std::string> values;
} StructType;

typedef std::vector<StructType> StructVectorType;
typedef std::vector<std::string> configListT;

enum OIaction {
	REGISTER_DN_INSTANCE,
	REGISTER_DN_AND_ITS_SUBTREE,
	REGISTER_CLASS,
	UNREGISTER_DN,
	UNREGISTER_CLASS
};

bool startupLogWriteEnabled = false;
bool startupLogSpamEnabled = false;
bool startupTraceSpamEnabled = false;
//mr20275
bool flag_mr20275 = false;
bool validate_mr20275 = true;

//hs99358 fix - must abort ccb if prepare fails
ComOamSpiTransactionHandleT hs99358_current_txhandle_id = 0;
bool hs99358_bad_ccb_has_been_aborted = false;

unsigned int nrOfLogSpams = 5;
long long unsigned int nrOfTraceSpams = 5;
int startupLogWriteDelay = 10;
int startupTraceWriteDelay = 10;

ComReturnT registerAsOIToOamSA(std::string, OIaction, std::string);

static MafOamSpiEventProducerHandleT producer_handle = 0;
static MafOamSpiEventProducerHandleT consumer_handle = 0;

#if defined (ALARMS) || defined (ALARMS4)
	static MafReturnT addFilter(MafOamSpiEventConsumerHandleT consumerHandle, const char * eventType, MafNameValuePairT ** filter);
	static MafReturnT removeFilter(MafOamSpiEventConsumerHandleT consumerHandle, const char * eventType, MafNameValuePairT ** filter);
	static MafReturnT clearAll(void);
	static MafReturnT doneWithValue(const char *eventType, void * value);
#endif
typedef struct {
	MafOamSpiEventConsumerHandleT consumerHandle;
	const char *eventType;
	MafNameValuePairT ** filter;
	SaNtfSubscriptionIdT subscriptionId;
} MafFilterT;

#if defined (ALARMS) || defined (ALARMS4)
	static MafOamSpiEventProducer_1T producer_if = {
		addFilter,
		removeFilter,
		clearAll,
		doneWithValue
	};
#endif

typedef std::pair<ComOamSpiTransactionHandleT, ComMoAttributeValueContainer_3T *> deletePairType;
typedef std::map<ComOamSpiTransactionHandleT, ComMoAttributeValueContainer_3T *> deleteMapType;
typedef deleteMapType::iterator deleteMapIteratorType;
deleteMapType deleteMap;

static pthread_t OpenThreadId = 0;
int PthreadResult = 0;

#if defined (CM_EVENT_CONSUMER)
	static MafOamSpiEventConsumerHandleT consumer_handle;
#endif
//static MafNameValuePairT *cmNotificationFilter[1] = { NULL };
MafNameValuePairT **cmNotificationFilter;
#if defined (CM_EVENT_CONSUMER)
	static MafReturnT cmEventNotify(MafOamSpiEventConsumerHandleT handle, const char * eventType, MafNameValuePairT **filter, void * value);
	static MafOamSpiEventConsumer_1T consumer_if = { cmEventNotify };
#endif

// convert the MafOamSpiCmEvent_EventType_1T enum types to strings
std::string eventTypeToString(MafOamSpiCmEvent_EventType_1T eventType)
{
	switch(eventType)
	{
	case MafOamSpiCmEvent_MoCreated_1:
		return "MoCreated";
	case MafOamSpiCmEvent_MoDeleted_1:
		return "MoDeleted";
	case MafOamSpiCmEvent_AttributeValueChange_1:
		return "AttributeValueChange";
	case MafOamSpiCmEvent_Overflow_1:
		return "Overflow";
	default:
		syslog(LOG_INFO, "%s eventTypeToString(): invalid eventType",log_prefix);
		return "";
	}
}

// convert the MafOamSpiCmEvent_SourceIndicator_1T enum types to strings
std::string sourceIndicatorToString(MafOamSpiCmEvent_SourceIndicator_1T sourceIndicator)
{
	switch(sourceIndicator)
	{
	case MafOamSpiCmEvent_ResourceOperation_1:
		return "ResourceOperation";
	case MafOamSpiCmEvent_ManagementOperation_1:
		return "ManagementOperation";
	case MafOamSpiCmEvent_SonOperation_1:
		return "SonOperation";
	case MafOamSpiCmEvent_Unknown_1:
		return "Unknown";
	default:
		syslog(LOG_INFO, "%s eventTypeToString(): invalid sourceIndicator",log_prefix);
		return "";
	}
}

std::string attrValueContainerToString(MafMoAttributeValueContainer_3T &avc)
{
	std::string avcStr;
	char b[100];
	switch(avc.type)
	{
	case MafOamSpiMoAttributeType_3_INT8:
		avcStr = " attrType: INT8";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%d", avc.values[i].value.i8);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_INT16:
		avcStr = " attrType: INT16";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%d", avc.values[i].value.i16);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_INT32:
		avcStr = " attrType: INT32";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%d", avc.values[i].value.i32);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_INT64:
		avcStr = " attrType: INT64";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%ld", avc.values[i].value.i64);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_UINT8:
		avcStr = " attrType: UINT8";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%u", avc.values[i].value.u8);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_UINT16:
		avcStr = " attrType: UINT16";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%u", avc.values[i].value.u16);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_UINT32:
		avcStr = " attrType: UINT32";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%u", avc.values[i].value.u32);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_UINT64:
		avcStr = " attrType: UINT64";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%lu", avc.values[i].value.u64);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_STRING:
		avcStr = " attrType: STRING";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			avcStr += " " + std::string(avc.values[i].value.theString);
		}
		break;
	case MafOamSpiMoAttributeType_3_BOOL:
		avcStr = " attrType: BOOL";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%d", avc.values[i].value.theBool);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_REFERENCE:
		syslog(LOG_INFO, "%s attrValueContainerToString(): not supported type",log_prefix);
		avcStr = " attrType: REFERENCE";
		break;
	case MafOamSpiMoAttributeType_3_ENUM:
		avcStr = " attrType: ENUM";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%ld", avc.values[i].value.theEnum);
			avcStr += " " + std::string(buf);
		}
		break;
	case MafOamSpiMoAttributeType_3_STRUCT:
		avcStr = " attrType: STRUCT";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b);
		for(unsigned int i = 0; i != avc.nrOfValues; i++)
		{
			//syslog(LOG_INFO, "%s attrValueContainerToString(): struct element %d:",log_prefix,i);
			MafMoAttributeValueStructMember_3 *SM = avc.values[i].value.structMember;
			while(SM != NULL)
			{
				//syslog(LOG_INFO, "%s attrValueContainerToString():    while enter SM != NULL",log_prefix);
				if(SM->memberName != NULL)
				{
					//syslog(LOG_INFO, "%s attrValueContainerToString():       SM->memberName != NULL",log_prefix);
					avcStr += " memberName: " + std::string(SM->memberName);
					if(SM->memberValue != NULL)
					{
						std::string memberValue = attrValueContainerToString(*(SM->memberValue));
						//syslog(LOG_INFO, "%s attrValueContainerToString():          memberValue: (%s)",log_prefix,memberValue.c_str());
						avcStr += " memberValue:" + memberValue;
					}
				}
				SM = SM->next;
			}
		}
		break;
	case MafOamSpiMoAttributeType_3_DECIMAL64:
		avcStr = " attrType: DECIMAL64";
		sprintf(b,"%u", avc.nrOfValues);
		avcStr += " nrOfValues: " + std::string(b) + " values:";
		for(unsigned int i = 0; i < avc.nrOfValues; i++)
		{
			char buf[100];
			sprintf(buf,"%f", avc.values[i].value.decimal64);
			avcStr += " " + std::string(buf);
		}
		break;
	default:
		syslog(LOG_INFO, "%s attrValueContainerToString(): invalid type",log_prefix);
		avcStr = "";
		break;
	}
	return avcStr;
}

#if defined (CM_EVENT_CONSUMER)
// CM event consumer callback
static MafReturnT cmEventNotify(MafOamSpiEventConsumerHandleT handle, const char * eventType, MafNameValuePairT **filter, void * value)
{
	//syslog(LOG_INFO, "%s cmEventNotify(): handle(%lu) eventType(%s), filter(%p) eventStruct(%p)",log_prefix,handle,eventType,filter,value);
	// Checking input values first
	if(eventType == NULL)
	{
		syslog(LOG_INFO, "%s cmEventNotify(): eventType = NULL, returning MafFailure",log_prefix);
		return MafFailure;
	}
	if(strcmp(eventType,MafOamSpiCmEvent_Notification_1))
	{
		syslog(LOG_INFO, "%s cmEventNotify(): eventType != %s, returning MafFailure",log_prefix, MafOamSpiCmEvent_Notification_1);
		return MafFailure;
	}
	if(filter == NULL)
	{
		syslog(LOG_INFO, "%s cmEventNotify(): filter = NULL, returning MafFailure",log_prefix);
		return MafFailure;
	}
	if(value == NULL)
	{
		syslog(LOG_INFO, "%s cmEventNotify(): CM_eventStructure = NULL, returning MafFailure",log_prefix);
		return MafFailure;
	}
	MafOamSpiCmEvent_Notification_1T* ES = (MafOamSpiCmEvent_Notification_1T*)value;
	std::string sourceIndicatorStr = sourceIndicatorToString(ES->sourceIndicator);
	MafOamSpiCmEvent_1T **events = ES->events;

	std::string eventsStr;
	for(int i = 0; events[i] != NULL; i++)
	{
		eventsStr += " dn: ";
		eventsStr += events[i]->dn;
		eventsStr += " eventType: ";
		eventsStr += eventTypeToString(events[i]->eventType);
		if(events[i]->attributes != NULL)
		{
			MafMoNamedAttributeValueContainer_3T **attrs = events[i]->attributes;
			eventsStr += " attributes:";
			std::string attrStr = "";
			for(int j = 0; attrs[j] != NULL; j++)
			{
				std::string nameStr = attrs[j]->name;
				std::string attrValueContStr = attrValueContainerToString(attrs[j]->value);

				attrStr += " name: " + nameStr + attrValueContStr;
			}
			eventsStr += attrStr;
		}
		else
		{
			eventsStr += " attributes: NULL";
		}
	}
	syslog(LOG_INFO, "%s cmEventNotify(): txHandle: %lu sourceIndicator: %s%s eventTime: %llu", log_prefix,ES->txHandle, sourceIndicatorStr.c_str(), eventsStr.c_str(), ES->eventTime);
	return MafOk;
}
#endif

void comsa_sleep( time_t seconds, long nsecs )
{
	struct timespec sleepPeriod = { seconds, nsecs };
	struct timespec unusedPeriod;
	while(nanosleep(&sleepPeriod, &unusedPeriod) != 0);
}

/* Save txHandle and the pointer of the container(which need to be freed later) into a map
 *
 * return true : if it is possible to insert txHandle to the map(it wasn't in the map before)
 * return false: if it is not possible to insert txHandle to the map(it was in the map before)
 */
bool saveToDeleteList(ComOamSpiTransactionHandleT txHandle, ComMoAttributeValueContainer_3T * pContainer)
{
	bool ret = true;
	syslog(LOG_INFO, "%s saveToDeleteList(%p) txHandle(%lu)",log_prefix,pContainer,txHandle);
	std::pair<deleteMapIteratorType, bool> insertRet = deleteMap.insert(deletePairType(txHandle, pContainer));
	// if txHandle already exists in the map then it is a negative case
	if(!insertRet.second)
	{
		syslog(LOG_INFO, "%s saveToDeleteList() error: txHandle(%lu) is already in the map",log_prefix,txHandle);
		ret = false;
	}
	return ret;
}

void freeContainer(ComMoAttributeValueContainer_3T * cnt)
{
	syslog(LOG_INFO, "%s freeContainer(%p)",log_prefix,cnt);
	//	check input parameters
	if(!cnt) {
		syslog(LOG_INFO, "%s MO::freeContainer() left.",log_prefix);
		return;
	}

	//	Check if the attribute cnt is type of STRUCT
	if(cnt->type != ComOamSpiMoAttributeType_3_STRUCT)
	{
		//	Free allocated memory
		if(cnt->values)
		{
			if(cnt->type == ComOamSpiMoAttributeType_3_STRING)
			{
				for(unsigned int i=0; i<cnt->nrOfValues; i++)
				{
					if(cnt->values[i].value.theString)
					{
						free((void*)cnt->values[i].value.theString);
					}
				}
			}
			else if(cnt->type == ComOamSpiMoAttributeType_3_REFERENCE)
			{
				for(unsigned int i=0; i<cnt->nrOfValues; i++)
				{
					if(cnt->values[i].value.moRef)
					{
						free((void*)cnt->values[i].value.moRef);
					}
				}
			}
			if(cnt->nrOfValues >= 1)
			{
				delete []cnt->values;
			}
		}
		delete cnt;
		syslog(LOG_INFO, "%s MO::freeContainer() left.",log_prefix);
		return;
	}

	//	Free allocated memory
	if(cnt->values)
	{
		ComMoAttributeValueStructMember_3T *member;
		ComMoAttributeValueContainer_3T *value;

		for(unsigned int i=0; i<cnt->nrOfValues; i++)
		{
			member = cnt->values[i].value.structMember;
			while(member != NULL)
			{
				value = member->memberValue;
				freeContainer(value);
				if(member->memberName)
				{
					delete []member->memberName;
				}
				ComMoAttributeValueStructMember_3T *tmp_member = member->next;
				delete member;
				member = tmp_member;
			}
		}
		if(cnt->nrOfValues >= 1)
		{
			delete []cnt->values;
		}
	}
	delete cnt;
	syslog(LOG_INFO, "%s MO::freeContainer() left.",log_prefix);
	return;
}

/*
 * Input: txHandle
 *
 * Description:
 *
 *     If txHandle is in deleteMap:
 *           Free the memory of the container which allocated during the transaction with txHandle
 *           Remove the txHandle entry from the deleteMap
 *
 *     Else: write a syslog
 */
void freeDeleteList(ComOamSpiTransactionHandleT txHandle)
{
	deleteMapIteratorType it = deleteMap.find(txHandle);
	if(it != deleteMap.end())
	{
		syslog(LOG_INFO, "%s freeDeleteList(): release memory of container with txHandle: %lu",log_prefix, txHandle);
		freeContainer(it->second);
		deleteMap.erase(txHandle);
	}
	else
	{
		syslog(LOG_INFO, "%s freeDeleteList(): txHandle(%lu) is not in the map",log_prefix, txHandle);
	}
}

std::string linuxCmd(std::string command)
{
	FILE *fpipe;
	int resCode,fd;
	std::string strBuf = "";
	syslog(LOG_INFO, "%s linuxCmd(): sending command: (%s)",log_prefix,command.c_str());
	if ( !(fpipe = (FILE*)popen(command.c_str(), "r")) )
	{
		syslog(LOG_ERR, "%s linuxCmd(): Could not create pipe",log_prefix);

		return "";
	}
	fd = fileno(fpipe);
	syslog(LOG_INFO, "%s linuxCmd(): Open file desc = %d",log_prefix,fd);
	char buf[500];
	while(!feof(fpipe) )
	{
		if( fgets( buf, 128, fpipe ) != NULL )
		{
			break;
		}
	}
	syslog(LOG_INFO, "%s linuxCmd(): output of the command: (%s)",log_prefix,buf);
	strBuf = buf;
	if ((resCode = pclose(fpipe)) == -1)
	{
		syslog(LOG_ERR, "%s linuxCmd(): Could not close spawned process (%d)",log_prefix,resCode);
	}
	syslog(LOG_INFO, "%s linuxCmd(): Could not close spawned process",log_prefix);
	//printf ("Closed file desc = %d\n", fd);
	return strBuf;
}

configListT readConfigFile(const char *configFile)
{
	configListT filterList;
	FILE* cfg_fp = NULL;

	syslog(LOG_INFO, "%s readConfigFile(): Opening config file \"%s\"",log_prefix, configFile);
	if ((cfg_fp = fopen(configFile,"r")) != NULL)
	{
		char buf[2000];
		for (;;)
		{
			if (fgets(buf,sizeof(buf),cfg_fp) == NULL)
			{
				break;
			}
			// put the lines to the filter list
			filterList.push_back(buf);

		}
		syslog(LOG_INFO, "%s readConfigFile(): Closing config file \"%s\"",log_prefix, configFile);
		fclose(cfg_fp);
		syslog(LOG_INFO, "%s readConfigFile(): File successfully closed",log_prefix);
	}
	else
	{
		syslog(LOG_INFO, "%s readConfigFile(): Failed to open filter config file \"%s\"",log_prefix, configFile);
	}
	return filterList;
}

// This function fills out the CM event filter array with the filter names and expressions
//
// Steps:
//    First it will filter out the useless lines and chars from the cmFilterList
//    Then fills in the filter array from cmFilterList
void setCmEventFilterArray(configListT cmFilterList, MafNameValuePairT **filter)
{
	// remove the useless elements from the list
	for(size_t i = 0; i < cmFilterList.size(); i++)
	{
		// if there is '\n' char at the end of the lines then remove it
		if(cmFilterList.at(i)[cmFilterList.at(i).length()-1] == '\n')
		{
			cmFilterList.at(i) = cmFilterList.at(i).substr(0,cmFilterList.at(i).length()-1);
		}

		// remove the lines from the list:
		//     -which line's size is zero. E.g.: ""
		//     -or which line only containes one or more ' ' chars. E.g.: " " or e.g.: "   "
		//
		// note: this is not a white space filtering of the line, since regexp can contain white spaces.
		// This will only skip the non-regexp lines, which contains only spaces or contains nothing
		bool allSpaceOrEmpty = true;
		for(size_t j = 0; j < cmFilterList.at(i).length(); j++)
		{
			if(cmFilterList.at(i)[j] != ' ')
			{
				// found a char which is not " ", so this line is not an empty or a full space line. Keeping it.
				allSpaceOrEmpty = false;
				break;
			}
		}
		if(allSpaceOrEmpty)
		{
			//printf("empty or allSpace element found: (%s)\n",cmFilterList.at(i).c_str());
			cmFilterList.erase(cmFilterList.begin()+i);
			i--;
		}
	}
	// print the list content to syslog just for debugging
	for(size_t i = 0; i < cmFilterList.size(); i++)
	{
		syslog(LOG_INFO, "%s setCmEventFilterArray(): List element: (%s)\n",log_prefix, cmFilterList.at(i).c_str());
	}
	// allocate memory for the filters
	for(size_t i = 0; i < cmFilterList.size(); i++)
	{
		filter[i] = new MafNameValuePairT;
		// fill in the data
		filter[i]->name = strdup(MafOamSpiCmEvent_FilterTypeRegExp_1);
		filter[i]->value = strdup(cmFilterList.at(i).c_str());
	}
	filter[cmFilterList.size()] = NULL;
}

void freeCmEventFilterArray()
{
	syslog(LOG_INFO, "%s freeCmEventFilterArray(): freeing CM Event filter",log_prefix);
	if(cmNotificationFilter != NULL)
	{
		for(unsigned int i = 0; cmNotificationFilter[i] != NULL; i++)
		{
			syslog(LOG_INFO, "%s freeCmEventFilterArray():    freeing filter[%u] name (%s) value (%s)",log_prefix,i,cmNotificationFilter[i]->name,cmNotificationFilter[i]->value);
			delete[] cmNotificationFilter[i]->name;
			delete[] cmNotificationFilter[i]->value;
			delete cmNotificationFilter[i];
		}

		delete cmNotificationFilter;
	}
	syslog(LOG_INFO, "%s freeCmEventFilterArray(): done",log_prefix);
}

std::string replaceChar(std::string text,char oldValue, char newValue)
{
	while(text.find(oldValue) != string::npos)
	{
		text[text.find(oldValue)] = newValue;
	}
	return text;
}

static void* startupLogWriteThread(void * arg)
{
	syslog(LOG_INFO, "%s startupLogWriteThread(): ENTER",log_prefix);
	ComReturnT ret;
	std::string alarmLogText;
	std::string alertLogText;
	std::string cmdOutput;
	std::string unixTimeCmd= "date +%s";
	std::string timeStampCmd= "date \"+%Y-%m-%dT%TZ\"";
	// wait 10 sec for COM to start
	comsa_sleep((time_t)startupLogWriteDelay,0);

	syslog(LOG_INFO, "%s startupLogWriteThread(): logWrite an Alarm",log_prefix);
	alarmLogText += "   <Alarm>0;";
	cmdOutput = linuxCmd(timeStampCmd);
	alarmLogText += replaceChar(cmdOutput,'\n',';');
	cmdOutput = linuxCmd(unixTimeCmd);
	alarmLogText += replaceChar(cmdOutput,'\n',';');
	alarmLogText += "testComp556: Alarm test log;";
	alarmLogText += "</Alarm>";
	syslog(LOG_INFO, "%s alarmLogText is: (%s)",log_prefix,alarmLogText.c_str());
	ret = _logServiceIf->logWrite(300, MW_SA_LOG_SEV_INFO, 100, alarmLogText.c_str());
	if(ret != ComOk)
	{
		syslog(LOG_ERR, "%s startupLogWriteThread(): logWrite Alarm failed: (%d)",log_prefix,ret);
	}

	syslog(LOG_INFO, "%s startupLogWriteThread(): logWrite an Alert",log_prefix);
	alertLogText += "   <Alert>0;";
	cmdOutput = linuxCmd(timeStampCmd);
	alertLogText += replaceChar(cmdOutput,'\n',';');
	cmdOutput = linuxCmd(unixTimeCmd);
	alertLogText += replaceChar(cmdOutput,'\n',';');
	alertLogText += "testComp556: Alert test log;";
	alertLogText += "</Alert>";
	syslog(LOG_INFO, "%s alertLogText is: (%s)",log_prefix,alertLogText.c_str());
	ret = _logServiceIf->logWrite(301, MW_SA_LOG_SEV_INFO, 101, alertLogText.c_str());
	if(ret != ComOk)
	{
		syslog(LOG_ERR, "%s startupLogWriteThread(): logWrite Alert failed: (%d)",log_prefix,ret);
	}

	syslog(LOG_INFO, "%s startupLogWriteThread(): LEAVE",log_prefix);
	pthread_exit(NULL);
	return NULL;
}

static void* startupLogSpamThread(void * arg)
{
	syslog(LOG_INFO, "%s startupLogSpamThread(): ENTER",log_prefix);
	//ComReturnT ret;
    std::string alarmLogText;

    // wait X sec for COM to start
    syslog(LOG_INFO, "%s startupLogSpamThread(): wait %d sec for startup of Log service",log_prefix,startupLogWriteDelay);
    comsa_sleep((time_t)startupLogWriteDelay,0);

    syslog(LOG_INFO, "%s startupLogSpamThread(): logWrite %d Alarms",log_prefix, nrOfLogSpams);
    const char * logText = "testCompLogSpam: spamming LOG service with logs";
    for(unsigned int i = 0; i < nrOfLogSpams; i++)
    {
    	_logServiceIf->logWrite(300, MW_SA_LOG_SEV_INFO, 100, logText);
    	/*alarmLogText = "testCompLogSpam: spamming LOG service with logs, log number: ";
    	stringstream ss;
    	ss << i;
    	alarmLogText += ss.str();*/
    	//syslog(LOG_INFO, "%s startupLogSpamThread(): spam nr %u with text: \"%s\"",log_prefix, i, alarmLogText.c_str());
    	/*ret = _logServiceIf->logWrite(300, MW_SA_LOG_SEV_INFO, 100, alarmLogText.c_str());
    	if(ret != ComOk)
    	{
    		syslog(LOG_ERR, "%s startupLogSpamThread(): logWrite failed: (%d)",log_prefix,ret);
    	}
    	else
    	{
    		syslog(LOG_ERR, "%s startupLogSpamThread(): logWrite returned ComOk",log_prefix);
    	}
    	comsa_sleep((time_t)1,0);*/
    }

    syslog(LOG_INFO, "%s startupLogSpamThread(): LEAVE",log_prefix);
    pthread_exit(NULL);
    return NULL;
}

static void* startupTraceSpamThread(void * arg)
{
	syslog(LOG_INFO, "%s startupTraceSpamThread(): ENTER",log_prefix);

	// wait X sec for COM to start
    syslog(LOG_INFO, "%s startupTraceSpamThread():    wait %d sec for startup of Trace service",log_prefix,startupTraceWriteDelay);
    comsa_sleep((time_t)startupTraceWriteDelay,0);

    syslog(LOG_INFO, "%s startupTraceSpamThread():    traceWrite %llu traces",log_prefix, nrOfTraceSpams);
    unsigned int group = 0;
    //const char * traceText = "testCompTraceSpam: spamming TRACE service ";

    std::string traceTextStr = "testCompTraceSpam: spamming TRACE service ";
    for(long long unsigned int i = 0; i < 10; i++)
    {
    	traceTextStr += " - Some test text ";
    	stringstream ss;
    	ss << i;
    	traceTextStr += ss.str();
    }
    const char * traceText = strdup(traceTextStr.c_str());

    for(long long unsigned int i = 0; i < nrOfTraceSpams; i++)
    {
    	_traceServiceIf->traceWrite(group, traceText);
    }
    syslog(LOG_INFO, "%s startupLogSpamThread(): RETURN",log_prefix);
    pthread_exit(NULL);
    return NULL;
}

#if defined (ALARMS) || defined (ALARMS4)
static MafReturnT addFilter(MafOamSpiEventConsumerHandleT consumerHandle, const char * eventType, MafNameValuePairT ** filter)
{
	syslog(LOG_INFO, "%s addFilter(): ENTER",log_prefix);
	syslog(LOG_INFO, "%s addFilter(): consumerHandle(%lu)",log_prefix, consumerHandle);
	syslog(LOG_INFO, "%s addFilter(): filter (%p)",log_prefix, filter);
	// This pointer is needed for "notify" call, so saving it
	filter_from_addFilter = filter;
	consumer_handle = consumerHandle;
	syslog(LOG_INFO, "%s addFilter(): filter_from_addFilter (%p)",log_prefix, filter_from_addFilter);
	if(eventType == NULL)
	{
		syslog(LOG_INFO, "%s addFilter(): eventType is NULL",log_prefix);
	}
	else
	{
		syslog(LOG_INFO, "%s addFilter(): eventType(%s)",log_prefix, eventType);
	}

	// filter debug printouts
	if(filter != NULL)
	{
		if(filter[0] != NULL)
		{
			syslog(LOG_INFO, "%s addFilter(): *filter exists",log_prefix);
		}
		else
		{
			syslog(LOG_INFO, "%s addFilter(): *filter is NULL",log_prefix);
		}
	}
	else
	{
		syslog(LOG_INFO, "%s addFilter(): filter is NULL",log_prefix);
	}

	syslog(LOG_INFO, "%s addFilter(): LEAVE: returning ComOk",log_prefix);
	return MafOk;
}

static MafReturnT removeFilter(MafOamSpiEventConsumerHandleT consumerHandle, const char * eventType, MafNameValuePairT ** filter)
{
	syslog(LOG_INFO, "%s removeFilter(): ENTER",log_prefix);
	syslog(LOG_INFO, "%s removeFilter(): LEAVE: returning ComOk",log_prefix);
	return MafOk;
}

static MafReturnT clearAll(void)
{
	syslog(LOG_INFO, "%s clearAll(): ENTER",log_prefix);
	syslog(LOG_INFO, "%s clearAll(): LEAVE: returning ComOk",log_prefix);
	return MafOk;
}

static MafReturnT doneWithValue(const char *eventType, void * value)
{
	syslog(LOG_INFO, "%s doneWithValue(): ENTER",log_prefix);
	if (notificationStruct != NULL)
	{
		syslog(LOG_INFO, "%s doneWithValue(): freeing notificationStruct(%p)",log_prefix, notificationStruct);
		if(notificationStruct->dn != NULL)
		{
			delete[] notificationStruct->dn;
		}
		if(notificationStruct->dn != NULL)
		{
			delete[] notificationStruct->additionalText;
		}
#if defined (ALARMS4)
		if ((notificationStruct->additionalInfo.additionalInfoArr != NULL) && (notificationStruct->additionalInfo.size > 0))
		{
			unsigned int iAddInfo = 0;
			for (iAddInfo = 0; iAddInfo < notificationStruct->additionalInfo.size; iAddInfo++)
			{
				free(notificationStruct->additionalInfo.additionalInfoArr[iAddInfo].name);
				free(notificationStruct->additionalInfo.additionalInfoArr[iAddInfo].value);
			}
			delete[] notificationStruct->additionalInfo.additionalInfoArr;
		}
#endif

		delete notificationStruct;
	}
	syslog(LOG_INFO, "%s doneWithValue(): LEAVE: returning ComOk",log_prefix);
	return MafOk;
}
#endif

std::string removeKeyAttributes(std::string str)
{
	std::string out1, out2;

	// continue processing the string if it contains "."
	while(str.find(".") != std::string::npos)
	{
		// save the first part of the string before the first "."
		out1 =str.substr(0,str.find("."));
		// save the second part of the string from the first "."
		out2 = str.substr(str.find("."));

		// if the second part contains "/" then remove everything before "/"
		// else return the first part
		if(out2.find("/") != std::string::npos)
		{
			str = out1 + out2.substr(out2.find("/"));
		}
		else
		{
			str = out1;
		}
	}
	return str;
}

std::string findTypeForSetMO(ComMoAttributeValueStructMember_3 * struct_Member)
{
	//syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ENTER",log_prefix);
	std::string Type_And_Value = "";

	switch (struct_Member->memberValue->type)
	{
	case ComOamSpiMoAttributeType_3_INT8:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_INT8 type entered",log_prefix);
		Type_And_Value = "INT8 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%i", struct_Member->memberValue->values[i].value.i8);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}

		}
		break;
	case ComOamSpiMoAttributeType_3_INT16:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_INT16 type entered",log_prefix);
		Type_And_Value = "INT16 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%i", struct_Member->memberValue->values[i].value.i16);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_INT32:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_INT32 type entered",log_prefix);
		Type_And_Value = "INT32 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%i", struct_Member->memberValue->values[i].value.i32);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_INT64:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_INT64 type entered",log_prefix);
		Type_And_Value = "INT64 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%li", struct_Member->memberValue->values[i].value.i64);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_UINT8:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_UINT8 type entered",log_prefix);
		Type_And_Value = "UINT8 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%u", struct_Member->memberValue->values[i].value.u8);
			//Mr20275
			if ((flag_mr20275) and (struct_Member->memberValue->values[i].value.u8 == 13))
			{
				validate_mr20275 = false;
				syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: validate_mr20275 is FALSE",log_prefix);
				std::string errorText = "@ComNbi@Error: MR-20275 test: Validate failed. Invalid UINT8 parameter: 13";
				_maf_threadContextIf->addMessage(ThreadContextMsgNbi_2, errorText.c_str());

			}
			syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: validate_mr20275 = %d",log_prefix,validate_mr20275);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_UINT16:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_UINT16 type entered",log_prefix);
		Type_And_Value = "UINT16 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%u", struct_Member->memberValue->values[i].value.u16);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_UINT32:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_UINT32 type entered",log_prefix);
		Type_And_Value = "UINT32 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%u", struct_Member->memberValue->values[i].value.u32);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_UINT64:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_UINT64 type entered",log_prefix);
		Type_And_Value = "UINT64 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%lu", struct_Member->memberValue->values[i].value.u64);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_DECIMAL64:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_DECIMAL64 type entered",log_prefix);
		Type_And_Value = "DECIMAL64 = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%f", struct_Member->memberValue->values[i].value.decimal64);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_STRING:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_STRING type entered",log_prefix);
		Type_And_Value = "STRING = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%s", struct_Member->memberValue->values[i].value.theString);
			//MR20275
			if ((flag_mr20275) and (struct_Member->memberValue->values[i].value.theString == std::string("bad")))
			{
				validate_mr20275 = false;
				std::string errorText = "@ComNbi@Error: MR-20275 test: Validate failed. Invalid STRING parameter: 'bad'";
				_maf_threadContextIf->addMessage(ThreadContextMsgNbi_2, errorText.c_str());
			}
			syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO.STRING: validate_mr20275 = %d", log_prefix, validate_mr20275);

			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_BOOL:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_BOOL type entered",log_prefix);
		Type_And_Value = "BOOL = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%i", struct_Member->memberValue->values[i].value.theBool);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;
	case ComOamSpiMoAttributeType_3_ENUM:
		syslog(LOG_INFO, "%s MO::setMoAttribute(): findTypeForSetMO: ComOamSpiMoAttributeType_3_ENUM type entered",log_prefix);
		Type_And_Value = "ENUM = ";
		for(unsigned int i = 0; i < struct_Member->memberValue->nrOfValues; i++)
		{
			char charBuffer[1000];
			sprintf(charBuffer,"%ld", struct_Member->memberValue->values[i].value.theEnum);
			Type_And_Value += charBuffer;
			if(i != (struct_Member->memberValue->nrOfValues - 1)) {Type_And_Value += ", ";}
		}
		break;

	default:
		// This is a fault, a type we do not support is received
		syslog(LOG_INFO, "%s MO::setMoAttribute() findTypeForSetMO: UNKNOW TYPE IN STRUCT",log_prefix);
		return "Error";
		break;
	}
	return Type_And_Value;
}

std::string getAttrsFromStructForSetMO(ComMoAttributeValueStructMember_3 * StructMember)
{
	//syslog(LOG_INFO, "%s ENTER readStructForSetMO",log_prefix);
	std::string TypeAndValue = "";
	TypeAndValue += "{";
	bool notfirst = false;

	// Be positive. Asume all parameters are valid. If any parameter is found later not to be valid this will become 'false'.
	validate_mr20275 = true;

	// Process the elements of the linked list. (list ends with NULL)
	while(StructMember != NULL)
	{
		//syslog(LOG_INFO, "%s MO::setMoAttribute() StructMember->memberName: (%s)",log_prefix,StructMember->memberName);
		// Yes, there is a reason to do this instead of do-while
		if(notfirst)
		{
			TypeAndValue += ", ";
		}
		notfirst = true;
		TypeAndValue += StructMember->memberName;
		TypeAndValue += " ";
		TypeAndValue += findTypeForSetMO(StructMember);
		StructMember = StructMember->next;
	}
	TypeAndValue += "}";
	//syslog(LOG_INFO, "%s LEAVE readStructForSetMO",log_prefix);
	return TypeAndValue;
}

void getSingleStructVector(std::string theString, std::vector<StructType>& retVector)
{
    //syslog(LOG_INFO, "%s getStructFromString() theString: %s",log_prefix, theString.c_str());
    //printf("%s getStructFromString() theString: %s\n",theString.c_str());
    // Do space filtering on the string
    while (theString.find(' ') != std::string::npos)
    {
        theString.erase(theString.find(' '), 1);
    }

    StructType theStruct;
    int pos = 0;
    std::string tempString = "";
    do
    {
        // Name parsing
        pos++;
        do
        {
            tempString += theString[pos];
            pos++;
        } while (theString[pos] != '(');
        theStruct.name = tempString;
        tempString = "";
        pos++;

        // Type parsing
        do
        {
            tempString += theString[pos];
            pos++;
        } while ((theString[pos] != ')') && (theString[pos + 1] != '='));
        theStruct.type = tempString;
        tempString = "";
        pos++;
        if (theString[pos] == '}') { break; }
        pos++;

        if (theString[pos] == '[')
        {
            pos++;
        }
        // Value parsing
        theStruct.values.clear();
        bool forMoRef = false;
        do
        {
            if(theString[pos] == '\'')
            {
                if (forMoRef == false)
                {
                    forMoRef = true;
                }
                else
                {
                    forMoRef = false;
                    theStruct.values.push_back(tempString);
                    tempString = "";
                }
                pos++;
            }
            else if(forMoRef)
            {
                tempString += theString[pos];
                pos++;
            }
            else if (theString[pos] == ';')
            {
                theStruct.values.push_back(tempString);
                tempString = "";
                pos++;
            }
            else if (theString[pos] == ']')
            {
                theStruct.values.push_back(tempString);
                tempString = "";
                pos++;
                goto OUT;
            }
            else
            {
                tempString += theString[pos];
                pos++;
            }
            if (theString[pos] == '}')
            {
                break;
            }
            if ((theString[pos] == ',') && (forMoRef == false))
            {
                break;
            }
        } while (1);
        if (tempString != "")
        {
            theStruct.values.push_back(tempString);
            tempString = "";
        }
OUT:
        //syslog(LOG_INFO, "%s getStructFromString() theStruct.name: %s theStruct.type: %s theStruct.value: %s",log_prefix, theStruct.name.c_str(), theStruct.type.c_str(), theStruct.value.c_str());
        //printf("%s getStructFromString() theStruct.name: %s theStruct.type: %s theStruct.value: %s\n",theStruct.name.c_str(), theStruct.type.c_str(), theStruct.value.c_str());
        // Push back the struct to the vector
        retVector.push_back(theStruct);
    } while (theString[pos] != '}');
    // Returning here
}

void getMultiStructVector(std::string stringOfMultiStruct, std::vector<StructVectorType> & MultiStructVector)
{
	//syslog(LOG_INFO, "%s getMultiStruct: ENTER",log_prefix);
	std::string stringOfSingleStruct = "";
	std::string tempString = stringOfMultiStruct;
	std::string::size_type endOfStruct;

	while(true)
	{
		endOfStruct = tempString.find('}');
		// Get the first "{...}" set from the whole "{...},{...}, ... {...}"
		stringOfSingleStruct = tempString.substr(0, endOfStruct + 1);

		StructVectorType SingleStructVector;
		// Process the single struct "{...}"
		getSingleStructVector(stringOfSingleStruct, SingleStructVector);
		// Push back the pointer of the SingleStructVector to the MultiStructVector
		MultiStructVector.push_back(SingleStructVector);
		/*for(int i = 0; i < (*SingleStructVector).size(); i++)
		{
			syslog(LOG_INFO, "%s getMultiStruct: name: %s type: %s value: %s",log_prefix, (*SingleStructVector)[i].name.c_str(), (*SingleStructVector)[i].type.c_str(), (*SingleStructVector)[i].value.c_str());
		}*/

		// If end of the whole string then break
		if( (endOfStruct + 1) == tempString.length() )
		{
			break;
		}
		// Take the next "{...}" set
		tempString = tempString.substr(endOfStruct + 2);
	}
	//syslog(LOG_INFO, "%s getMultiStruct: LEAVE",log_prefix);
	// Return here
}

// Space filtering on the input string
void spaceFilter(std::string &str)
{
	while(str.find(' ') != std::string::npos)
	{
		str.erase(str.find(' '),1);
	}
}

void prepareContainer(ComOamSpiMoAttributeType_3T attrType, int numOfValues, ComMoAttributeValueContainer_3T ** result)
{
	*result = new ComMoAttributeValueContainer_3T;
	syslog(LOG_INFO, "%s prepareContainer(%p)",log_prefix,*result);
	(*result)->nrOfValues = numOfValues;
	(*result)->type = attrType;
	(*result)->values = new ComMoAttributeValue_3T[numOfValues];
}

/*
 * Input: string
 * Return: vector<string>
 *
 * This function parses the input string to a vector as follows:
 * e.g. input string: "123, 444, 21"
 *      output vector [0]: "123", [1]: "444", [2]: "21"
 */
std::vector<std::string> multiValueStringToVector(std::string theString)
{
	std::vector<std::string> retVector;
	int pos = 0;
	// Do space filtering on the string
	while(theString.find(' ') != std::string::npos)
	{
		theString.erase(theString.find(' '),1);
	}
	// Push back the string parts separated by "," to the vector
	while(theString.length() != 0)
	{
		// Set pos to the first ","
		if(theString.find(',') != std::string::npos)
		{
			pos = theString.find(',');
		}
		// Set pos to the end of the string
		else
		{
			pos = theString.length();
		}
		// Push back the string until "," or until end of the string
		retVector.push_back(theString.substr(0, pos));
		// Erase the last part (which is pushed back to the vector by the last step)
		theString.erase(0, pos+1);
	}
	return retVector;
}

ComOamSpiMoAttributeType_3T findTypeForStructAttr(std::string type)
{
	ComOamSpiMoAttributeType_3T ret;
	if     (type == "INT8")  {ret = ComOamSpiMoAttributeType_3_INT8;}
	else if(type == "INT16") {ret = ComOamSpiMoAttributeType_3_INT16;}
	else if(type == "INT32") {ret = ComOamSpiMoAttributeType_3_INT32;}
	else if(type == "INT64") {ret = ComOamSpiMoAttributeType_3_INT64;}
	else if(type == "UINT8") {ret = ComOamSpiMoAttributeType_3_UINT8;}
	else if(type == "UINT16"){ret = ComOamSpiMoAttributeType_3_UINT16;}
	else if(type == "UINT32"){ret = ComOamSpiMoAttributeType_3_UINT32;}
	else if(type == "UINT64"){ret = ComOamSpiMoAttributeType_3_UINT64;}
	else if(type == "DECIMAL64"){ret = ComOamSpiMoAttributeType_3_DECIMAL64;}
	else if(type == "STRING"){ret = ComOamSpiMoAttributeType_3_STRING;}
	else if(type == "BOOL")  {ret = ComOamSpiMoAttributeType_3_BOOL;}
	else if(type == "ENUM")  {ret = ComOamSpiMoAttributeType_3_ENUM;}
	else if(type == "MOREF") {ret = ComOamSpiMoAttributeType_3_REFERENCE;}
	else
	{
		syslog(LOG_INFO, "%s findTypeForStructAttr(): ERROR: wrong type setting for struct attribute",log_prefix);
	}
	return ret;
}

void fillContainerWithStructAttrValues(ComOamSpiMoAttributeType_3T attrType, std::string attrValue, ComMoAttributeValue_3 *containerValue)
{
	switch(attrType)
	{
	case ComOamSpiMoAttributeType_3_INT8:
		containerValue->value.i8 = atoi(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_INT16:
		containerValue->value.i16 = atoi(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_INT32:
		containerValue->value.i32 = atoi(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_INT64:
		containerValue->value.i64 = atoll(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_UINT8:
		containerValue->value.u8 = atoi(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_UINT16:
		containerValue->value.u16 = atoi(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_UINT32:
		containerValue->value.u32 = strtoul(attrValue.c_str(), NULL, 10);
		break;
	case ComOamSpiMoAttributeType_3_UINT64:
		containerValue->value.u64 = strtoull(attrValue.c_str(), NULL, 10);
		break;
	case ComOamSpiMoAttributeType_3_DECIMAL64:
		containerValue->value.decimal64 = strtod(attrValue.c_str(), NULL);
		break;
	case ComOamSpiMoAttributeType_3_STRING:
		containerValue->value.theString = strdup(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_BOOL:
		containerValue->value.theBool = atoi(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_ENUM:
		containerValue->value.theEnum = atoi(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_REFERENCE:
		containerValue->value.moRef = strdup(attrValue.c_str());
		break;
	case ComOamSpiMoAttributeType_3_STRUCT:
		break;
	}
}

/*std::string generateTimeValue()
{

#define NANOS_PER_SEC 1000000000L
typedef unsigned long long uint64_t;

//date +%s
//g++ -o my_time_gen my_time_gen.cpp -lrt

	struct timespec ts;
	std::string _currentDateTime;
	//int c = clock_gettime(CLOCK_REALTIME, &ts);
	clock_gettime(CLOCK_REALTIME, &ts);
	//if (c != 0) {THROW_EXCEPTION("Failed to get system time");}

	std::stringstream ss;
	uint64_t eventTime = ((uint64_t)ts.tv_nsec) + ((uint64_t)ts.tv_sec) * NANOS_PER_SEC;
	ss << eventTime;
	_currentDateTime = ss.str();
	return _currentDateTime;
}*/

MafReturnT notify(std::string dn,
				unsigned long int majorType,
				unsigned long int minorType,
				std::string additionalText,
				std::string severity_string,
				unsigned long long eventTime,
				std::string additionalInfo)
{
	syslog(LOG_INFO, "%s notify(): ENTER",log_prefix);
	MafFilterT nFilter;
	MafOamSpiNotificationFmSeverityT severity;
#if defined (ALARMS)
	syslog(LOG_INFO, "%s notify(): notificationStruct = new MafOamSpiNotificationFmStruct_2T",log_prefix);
	notificationStruct = new MafOamSpiNotificationFmStruct_2T;
#endif
#if defined (ALARMS4)
	syslog(LOG_INFO, "%s notify(): notificationStruct = new MafOamSpiNotificationFmStruct_4T",log_prefix);
	notificationStruct = new MafOamSpiNotificationFmStruct_4T;
#endif
	if(!notificationStruct)
	{
		syslog(LOG_INFO, "%s notify(): memory allocation failed, returning MafFailure",log_prefix);
		return MafFailure;
	}

	notificationStruct->dn = strdup(dn.c_str());
	notificationStruct->majorType = majorType;
	notificationStruct->minorType = minorType;
	//notificationStruct->eventTime = time(NULL);
	notificationStruct->eventTime = eventTime;
	notificationStruct->additionalText = strdup(additionalText.c_str());
#if defined (ALARMS4)
	int nAdditionalInfo = 0, iAddInfo = 0;
	int nEnd = 0;
	if (additionalInfo.size() > 0)
	{
		nAdditionalInfo = std::count(additionalInfo.begin(), additionalInfo.end(), ';') + 1;
		syslog(LOG_INFO, "%s notify(): additionalInfo num=%d value=%s", log_prefix, nAdditionalInfo, additionalInfo.c_str());
		notificationStruct->additionalInfo.additionalInfoArr = new MafOamSpiNotificationFmAdditionalInfoT[nAdditionalInfo];
		std::string addInfo;
		for (iAddInfo = 0; iAddInfo < nAdditionalInfo; iAddInfo++)
		{
			nEnd = additionalInfo.find(";");
			addInfo = additionalInfo.substr(0, nEnd);
			additionalInfo.erase(0, nEnd+1);
			syslog(LOG_INFO, "%s notify(): iAddInfo=%d nEnd=%d addInfo=%s additionalInfo=%s", log_prefix, iAddInfo, nEnd, addInfo.c_str(), additionalInfo.c_str());
			notificationStruct->additionalInfo.additionalInfoArr[iAddInfo].name = strdup("");
			notificationStruct->additionalInfo.additionalInfoArr[iAddInfo].value = strdup(addInfo.c_str());
			syslog(LOG_INFO, "%s notify(): additionalInfo num=%d value=%s", log_prefix, iAddInfo,
					notificationStruct->additionalInfo.additionalInfoArr[iAddInfo].name,
					notificationStruct->additionalInfo.additionalInfoArr[iAddInfo].value);
		}
	}
	notificationStruct->additionalInfo.size = nAdditionalInfo;
#endif

	if (severity_string == "cleared") {severity = MafOamSpiNotificationFmSeverityCleared;}
	else if (severity_string == "indeterminate") {severity = MafOamSpiNotificationFmSeverityIndeterminate;}
	else if (severity_string == "warning") {severity = MafOamSpiNotificationFmSeverityWarning;}
	else if (severity_string == "minor") {severity = MafOamSpiNotificationFmSeverityMinor;}
	else if (severity_string == "major") {severity = MafOamSpiNotificationFmSeverityMajor;}
	else if (severity_string == "critical") {severity = MafOamSpiNotificationFmSeverityCritical;}
	else
	{
		syslog(LOG_INFO, "%s notify(): Bad alarm type: (%s), returning MafFailure",log_prefix, severity_string.c_str());
		return MafFailure;
	}
	notificationStruct->severity = severity;
	nFilter.consumerHandle = consumer_handle;
#if defined (ALARMS)
	syslog(LOG_INFO, "%s notify(): nFilter.eventType = MafOamSpiNotificationFmEventComponent_3",log_prefix);
	nFilter.eventType = MafOamSpiNotificationFmEventComponent_3;
#endif
#if defined (ALARMS4)
	syslog(LOG_INFO, "%s notify(): nFilter.eventType = MafOamSpiNotificationFmEventComponent_4",log_prefix);
	nFilter.eventType = MafOamSpiNotificationFmEventComponent_4;
#endif

	syslog(LOG_INFO, "%s notify(): filter_from_addFilter (%p)",log_prefix, filter_from_addFilter);
	syslog(LOG_INFO, "%s notify(): Param 1: producer_handle (%d)",log_prefix, producer_handle);
	syslog(LOG_INFO, "%s notify(): Param 2: consumerHandle (%d)",log_prefix, nFilter.consumerHandle);
	syslog(LOG_INFO, "%s notify(): Param 3: nFilter.eventType(%s)",log_prefix, nFilter.eventType);
//	syslog(LOG_INFO, "%s notify(): Param 4: filter:",log_prefix);
//	syslog(LOG_INFO, "%s notify(): nFilter.filter[0]->name (%s)",log_prefix, nFilter.filter[0]->name);
//	syslog(LOG_INFO, "%s notify(): nFilter.filter[0]->value (%s)",log_prefix, nFilter.filter[0]->value);
	syslog(LOG_INFO, "%s notify(): Param 5: notificationStruct:",log_prefix);
	syslog(LOG_INFO, "%s notify(): notificationStruct(%p)",log_prefix, notificationStruct);
	syslog(LOG_INFO, "%s notify(): notificationStruct->dn (%s)",log_prefix, notificationStruct->dn);
	syslog(LOG_INFO, "%s notify(): notificationStruct->majorType (%lu)",log_prefix, notificationStruct->majorType);
	syslog(LOG_INFO, "%s notify(): notificationStruct->minorType (%lu) (0x%x)",log_prefix, notificationStruct->minorType, notificationStruct->minorType);
	syslog(LOG_INFO, "%s notify(): notificationStruct->eventTime (%lu)",log_prefix, notificationStruct->eventTime);
	syslog(LOG_INFO, "%s notify(): notificationStruct->additionalText (%s)",log_prefix, notificationStruct->additionalText);
	syslog(LOG_INFO, "%s notify(): notificationStruct->severity (%d)",log_prefix, notificationStruct->severity);
#if defined (ALARMS4)
	syslog(LOG_INFO, "%s notify(): notificationStruct->additionalInfo.size (%d)",log_prefix, notificationStruct->additionalInfo.size);
	for (iAddInfo = 0; iAddInfo < nAdditionalInfo; iAddInfo++)
	{
		syslog(LOG_INFO, "%s notify(): notificationStruct->additionalInfo.additionalInfoArr (%d) (%s)", log_prefix, iAddInfo,
						notificationStruct->additionalInfo.additionalInfoArr[iAddInfo].value);
	}
#endif

	syslog(LOG_INFO, "%s notify(): eventRouter->notify",log_prefix);
	MafReturnT ret = _eventRouter->notify(producer_handle, nFilter.consumerHandle, nFilter.eventType, filter_from_addFilter, notificationStruct);
	syslog(LOG_INFO, "%s notify(): returning with (%d)",log_prefix, ret);
	return ret;
}

/*ComReturnT logWrite()
{
	ComReturnT ret = _logServiceIf->logWrite(123, 1, 100,"Log from testComponent556");
	return ret;
}*/

ComReturnT testComponentControl(std::string command)
{
	syslog(LOG_INFO, "%s testComponentControl(): enter with (%s)",log_prefix, command.c_str());
	OIaction regType;
	ComReturnT ret = ComOk;
	bool alarmsDefined = false;
	bool logServiceDefined = false;
	#if defined(ALARMS) || defined(ALARMS4)
	{
		syslog(LOG_INFO, "%s testComponentControl(): alarmsDefined = true",log_prefix);
		alarmsDefined = true;
	}
	#endif
	#if defined(LOGSERVICE)
	{
		logServiceDefined = true;
	}
	#endif
	// remove possible quote from the beginning of the string
	if(command[0] == '\"')
	{
		command.erase(0,1);
	}
	// If show test config requested
	if(command.substr(0,8) == "show all")
	{
		testConfig->printAll();
		syslog(LOG_INFO, "%s testComponentControl(): returning (%i)",log_prefix, ret);
		return ret;
	}
	// If unregistration requested
	else if(command.substr(0,5) == "UNREG")
	{
		spaceFilter(command);
		// Erase the first part of the string (UNREG)
		command.erase(0,5);
		// Erase the last character of the string if that is a quote (")
		if(command[command.length()-1] == '\"')
		{
			command.erase(command.length()-1, 1);
		}
		if (command[0] == '/')
		{
			regType = UNREGISTER_CLASS;
			syslog(LOG_INFO, "%s testComponentControl(): Unregister MOC: %s",log_prefix, command.c_str());
		}
		else
		{
			regType = UNREGISTER_DN;
			syslog(LOG_INFO, "%s testComponentControl(): Unregister DN: %s",log_prefix, command.c_str());
		}
		ret = registerAsOIToOamSA(command, regType, "YES");
		testConfig->printAll();
	}
	// If registration requested
	else if(command.substr(0,3) == "REG")
	{
		spaceFilter(command);
		// Erase the first part of the string (REG)
		command.erase(0,3);
		// Erase the last character of the string if that is a quote (")
		if(command[command.length()-1] == '\"')
		{
			command.erase(command.length()-1, 1);
		}
		if (command[0] == '/')
		{
			regType = REGISTER_CLASS;
			syslog(LOG_INFO, "%s testComponentControl(): Register MOC: %s",log_prefix, command.c_str());
		}
		else
		{
			regType = REGISTER_DN_INSTANCE;
			syslog(LOG_INFO, "%s testComponentControl(): Register DN: %s",log_prefix, command.c_str());
		}
		ret = registerAsOIToOamSA(command, regType, "YES");
		testConfig->printAll();
	}
	// If alarm function requested
	else if(command.substr(0,5) == "ALARM")
	{
		if(!alarmsDefined)
		{
			syslog(LOG_INFO, "%s ERROR: controlling alarms without alarm configuration, returning ComFailure",log_prefix);
			return ComFailure;
		}
		spaceFilter(command);
		// Erase the first part of the string (ALARM)
		command.erase(0,5);
		// Erase the last character of the string if that is a quote (")
		if(command[command.length()-1] == '\"')
		{
			command.erase(command.length()-1, 1);
		}
		syslog(LOG_INFO, "%s testComponentControl(): ALARM raise: %s",log_prefix, command.c_str());

		std::string dn;
		unsigned long int majorType;
		unsigned long int minorType;
		std::string additionalText, severity_string, additionalInfo;
		unsigned long long eventTime;

		// 1. param: DN
		command.erase(0,command.find('\'') + 1);
		dn = command.substr(0,command.find('\''));
		command.erase(0,command.find('\'') + 1);
		command.erase(0,command.find(',') + 1);

		// 2. param: majorType
		majorType = atoi(command.substr(0,command.find(',')).c_str());
		command.erase(0,command.find(',') + 1);

		// 3. param: minorType
		minorType = atoi(command.substr(0,command.find(',')).c_str());
		command.erase(0,command.find(',') + 1);

		// 4. param: additionalText
		command.erase(0,command.find('\'') + 1);
		additionalText = command.substr(0,command.find('\''));
		command.erase(0,command.find('\'') + 1);
		command.erase(0,command.find(',') + 1);

		// 5. param: severity_string
		command.erase(0,command.find('\'') + 1);
		severity_string = command.substr(0,command.find('\''));
		command.erase(0,command.find('\'') + 1);
		command.erase(0,command.find(',') + 1);

		// 6. param: eventTime
		eventTime = strtoul(command.substr(0,command.find(',')).c_str(), NULL, 0);
		command.erase(0,command.find(',') + 1);

		// 7. param: additionalInfo
		additionalInfo = command.substr(0,command.find('\''));
		command.erase(0,command.find(',') + 1);

		syslog(LOG_INFO, "%s testComponentControl(): ALARM raise: (%s)",log_prefix, command.c_str());
		syslog(LOG_INFO, "%s testComponentControl(): ALARM dn: (%s) majorType: (%lu) minorType: (%lu) additionalText: (%s) severity_string: (%s) eventTime: (%llu) additionalInfo: (%s)",
			log_prefix, dn.c_str(), majorType, minorType, additionalText.c_str(), severity_string.c_str(), eventTime, additionalInfo.c_str());

		MafReturnT mafReturnValue = notify(dn, majorType, minorType, additionalText, severity_string, eventTime, additionalInfo);
		syslog(LOG_INFO, "%s testComponentControl(): notify returned with: (%d)",log_prefix, mafReturnValue);
		if (mafReturnValue == MafOk)
		{
			ret = ComOk;
		}
		else
		{
			ret = ComFailure;
		}
	}
	else if(command.substr(0,3) == "LOG")
		{
			if(!logServiceDefined)
			{
				syslog(LOG_INFO, "%s ERROR: controlling log service functions without log service configuration, returning ComFailure",log_prefix);
				return ComFailure;
			}
			unsigned long int eventId;
			MwSpiSeverityT severity;
			MwSpiFacilityT facility;
			std::string severity_string,databuffer;

			spaceFilter(command);
			// Erase the first part of the string (LOG)
			command.erase(0,3);
			// Erase the last character of the string if that is a quote (")
			if(command[command.length()-1] == '\"')
			{
				command.erase(command.length()-1, 1);
			}
			syslog(LOG_INFO, "%s testComponentControl(): log write: %s",log_prefix, command.c_str());

			// 1. param: eventId
			eventId = atoi(command.substr(0,command.find(',')).c_str());
			command.erase(0,command.find(',') + 1);

			// 2. param: severity
			command.erase(0,command.find('\'') + 1);
			severity_string = command.substr(0,command.find('\''));
			command.erase(0,command.find('\'') + 1);
			command.erase(0,command.find(',') + 1);

			// 3. param: facility
			facility = atoi(command.substr(0,command.find(',')).c_str());
			command.erase(0,command.find(',') + 1);

			// 4. param: databuffer
			command.erase(0,command.find('\'') + 1);
			databuffer = command.substr(0,command.find('\''));

			if (severity_string == "EMERGENCY") {severity = MW_SA_LOG_SEV_EMERGENCY;}
			else if (severity_string == "ALERT") {severity = MW_SA_LOG_SEV_ALERT;}
			else if (severity_string == "CRITICAL") {severity = MW_SA_LOG_SEV_CRITICAL;}
			else if (severity_string == "ERROR") {severity = MW_SA_LOG_SEV_ERROR;}
			else if (severity_string == "WARNING") {severity = MW_SA_LOG_SEV_WARNING;}
			else if (severity_string == "NOTICE") {severity = MW_SA_LOG_SEV_NOTICE;}
			else if (severity_string == "INFO") {severity = MW_SA_LOG_SEV_INFO;}
			else
			{
				syslog(LOG_INFO, "%s logWrite(): Bad severity type: (%s), returning ComFailure",log_prefix, severity_string.c_str());
				return ComFailure;
			}
			syslog(LOG_INFO, "%s logWrite(): calling logWrite with eventId (%lu) severity (%d) facility (%d) databuffer (%s)",log_prefix, eventId, severity, facility, databuffer.c_str());
			ret = _logServiceIf->logWrite(eventId, severity, facility, databuffer.c_str());
			//ret = logWrite();
		}
	syslog(LOG_INFO, "%s testComponentControl(): returning (%i)",log_prefix, ret);
	return ret;
}

void setAllReturnValuesToFail()
{
// if SKIP_ERROR is not defined in "defines.h" than it is an error case
// where we set all the return values to fail,
// so all functions that called from outside will return ComFailure
#if !defined(SKIP_ERROR)
	{
		// Create a structure of return values
		functionReturnValues returnValues;
		returnValues.createMo = ComFailure;
		returnValues.deleteMo = ComFailure;
		returnValues.setMo    = ComFailure;
		returnValues.getMo    = ComFailure;
		returnValues.action   = ComFailure;
		returnValues.join     = ComFailure;
		returnValues.prepare  = ComFailure;
		returnValues.commit   = ComFailure;
		returnValues.finish   = ComFailure;
		returnValues.abort    = ComFailure;
		returnValues.validate = ComFailure;

		syslog(LOG_INFO, "%s setAllReturnValuesToFail(): ERROR case: setting ComFailure for return values",log_prefix);
		syslog(LOG_INFO, "%s setAllReturnValuesToFail(): preconfigured return values: createMo: (%i) deleteMo: (%i) setMo: (%i) getMo: (%i) action: (%i) join: (%i) prepare: (%i) commit: (%i) finish: (%i) abort: (%i)",log_prefix, returnValues.createMo, returnValues.deleteMo, returnValues.setMo, returnValues.getMo, returnValues.action, returnValues.join, returnValues.prepare, returnValues.commit, returnValues.finish, returnValues.abort);
		testConfig->setReturnValues(returnValues);
	}
#endif
}

/****************************************************************************************************************
 ***************************************************************************************************************
 ***************************************************************************************************************
 *
 *  ComOamSpiManagedObject_3T interface functions
 *
 ***************************************************************************************************************
 ***************************************************************************************************************
 ***************************************************************************************************************/
ComReturnT setMoAttribute(ComOamSpiTransactionHandleT txHandle,
		const char * dn,
		const char * attributeName,
		const ComMoAttributeValueContainer_3T * attributeValueContainer)
{
	syslog(LOG_INFO, "%s MO::setMoAttribute() entered",log_prefix);
	std::string structAttrValuesAndTypes = "";
	//MR20275
	std::string DN_MR20275 = "ManagedElement=1,ObjectMr20275=1";
	if (dn == DN_MR20275)
	{
		flag_mr20275 = true;
		syslog(LOG_INFO, "%s MO::setMoAttribute flag_mr20275 is TRUE",log_prefix);
	}
	else flag_mr20275 = false;

	if (attributeValueContainer!=NULL) {
		switch (attributeValueContainer->type) {

		case ComOamSpiMoAttributeType_3_STRUCT:
			syslog(LOG_INFO, "%s MO::setMoAttribute(): ComOamSpiMoAttributeType_3_STRUCT ENTERED",log_prefix);
			syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s txHandle %lu",log_prefix,dn,attributeName,txHandle);
			syslog(LOG_INFO, "%s MO::setMoAttribute(): ComOamSpiMoAttributeType_3_STRUCT nrOfValues: %u",log_prefix, attributeValueContainer->nrOfValues);
			if(attributeValueContainer->values->value.structMember == NULL)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): ComOamSpiMoAttributeType_3_STRUCT is NULL",log_prefix);
				return ComFailure;
			}
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				structAttrValuesAndTypes = getAttrsFromStructForSetMO((attributeValueContainer->values)[i].value.structMember);
				syslog(LOG_INFO, "%s MO::setMoAttribute(): attributeName: %s Struct[%d]: %s",log_prefix, attributeName, i, structAttrValuesAndTypes.c_str());
			}
			break;

		case ComOamSpiMoAttributeType_3_INT8:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i8,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_INT16:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i16,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_INT32:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i32,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_INT64:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %ld txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i64,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT8:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %u txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u8,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT16:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %u txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u16,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT32:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %u txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u32,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT64:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %lu txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u64,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_DECIMAL64:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %f txHandle %f",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.decimal64,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_STRING:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %s txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.theString,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_BOOL:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.theBool,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_ENUM:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.theEnum,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_REFERENCE:
			syslog(LOG_INFO, "%s MO::setMoAttribute(): ComOamSpiMoAttributeType_3_REFERENCE ENTERED",log_prefix);
			break;

/*  // DERIVED and VOID not supported in MO SPI Ver.3
		case ComOamSpiMoAttributeType_DERIVED:
			syslog(LOG_INFO, "%s MO::setMoAttribute(): ComOamSpiMoAttributeType_DERIVED ENTERED",log_prefix);
			break;
		case ComOamSpiMoAttributeType_VOID:
			syslog(LOG_INFO, "%s MO::setMoAttribute(): ComOamSpiMoAttributeType_VOID ENTERED",log_prefix);
			break;
*/
		default:
			// This is a fault, a type we do not support is received
			syslog(LOG_INFO, "%s MO::setMoAttribute() AttributeValue : UNKNOW TYPE RECEIVED",log_prefix);
			return ComFailure;
			break;
		}
	}else {
		syslog(LOG_INFO, "%s MO::setMoAttribute() attributeValueContainer equal to NULL ",log_prefix);
	}

	ComReturnT permissionReturnValue = testConfig->getRegistration(_threadContextIf, dn);

	if(permissionReturnValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::setMoAttribute() Permission denied, returning %i",log_prefix,permissionReturnValue);
		return permissionReturnValue;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT retValue;
	retValue = testConfig->getReturnValue("set");
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::setMoAttribute() returning (%i)",log_prefix, retValue);
	}
	return retValue;
}


static void dummyReleaseOne(ComMoAttributeValueContainer_3T *container)
{
	syslog(LOG_INFO, "%s MO::dummyReleaseOne() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::dummyReleaseOne() left.",log_prefix);
	return;
}


static void UNUSED_FUNCTION(dummyReleaseMany)(ComMoAttributeValueContainer_3T **containers)
{
	syslog(LOG_INFO, "%s MO::dummyReleaseMany() entered",log_prefix);
}


ComReturnT getMoAttribute(ComOamSpiTransactionHandleT txHandle,
		const char * dn,
		const char * attributeName,
		ComMoAttributeValueResult_3T * result)
{
	syslog(LOG_INFO, "%s MO::getMoAttribute() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::getMoAttribute(): dn %s attributeName %s txHandle %lu",log_prefix,dn,attributeName,txHandle);

	// changes for MO SPI Ver.3
	ComMoAttributeValueContainer_3T** cont_result = &(result->container);
	result->release = &(dummyReleaseOne);

	ComReturnT permissionReturnValue = testConfig->getRegistration(_threadContextIf, dn);

	if(permissionReturnValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::getMoAttribute() Permission denied, returning %i",log_prefix,permissionReturnValue);
		return permissionReturnValue;
	}

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT retValue;
	retValue = testConfig->getReturnValue("get");
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::getMoAttribute() returning (%i)",log_prefix, retValue);
		return retValue;
	}

	Attribute theAttribute;
	theAttribute = testConfig->getAttribute(dn, attributeName);
	std::vector<std::string> multiValueVector;
	vector<StructVectorType> MultiStructVector;

	switch (theAttribute.attrType) {

	case ComOamSpiMoAttributeType_3_STRUCT:
		syslog(LOG_INFO, "%s MO::getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT type ENTER",log_prefix);

		// Parse the testconfig and create a MultiStructVector (vector of vectors of attributes)
		getMultiStructVector(theAttribute.attrValue, MultiStructVector);
		// Allocate memory for the container and for the values
		prepareContainer(theAttribute.attrType, MultiStructVector.size(), cont_result);
		syslog(LOG_INFO, "%s MO::getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT nrOfValues: %i",log_prefix, MultiStructVector.size());

		// For all the structs fill in the container
		for(unsigned int m = 0; m < MultiStructVector.size(); m++)
		{
			ComMoAttributeValueStructMember_3T * tempStruct;
			// allocate memory for the struct
			(*cont_result)->values[m].value.structMember = NULL; // new ComMoAttributeValueStructMember_3T;
			// using tempStruct for operations on the linked list
			// so keeping the original "(*cont_result)->values[m].value.structMember" as a head of the linked list
//			tempStruct = (*cont_result)->values[m].value.structMember;

			ComMoAttributeValueStructMember_3T * temp;
			for(unsigned int s = 0; s < MultiStructVector[m].size(); s++)
			{
				temp = new ComMoAttributeValueStructMember_3T;
				memset(temp, 0, sizeof(ComMoAttributeValueStructMember_3T));
				temp->next = NULL;

				if((*cont_result)->values[m].value.structMember == NULL) {
					(*cont_result)->values[m].value.structMember = temp;
					tempStruct = temp;
				} else {
					tempStruct->next = temp;
					tempStruct = temp;
				}

				// Set member name
				tempStruct->memberName = strdup(MultiStructVector[m][s].name.c_str());
				// Allocate memory for container
				tempStruct->memberValue = new ComMoAttributeValueContainer_3T;
				// Set the type
				tempStruct->memberValue->type = findTypeForStructAttr(MultiStructVector[m][s].type.c_str());
				// Set the number of values
				tempStruct->memberValue->nrOfValues =  MultiStructVector[m][s].values.size();
				// Allocate memory for values
				tempStruct->memberValue->values = new ComMoAttributeValue_3T[tempStruct->memberValue->nrOfValues];

				for(unsigned int i = 0; i < tempStruct->memberValue->nrOfValues; i++)
				{
					syslog(LOG_INFO, "%s MO::getMoAttribute(): Struct %d,%d name: %s type: %s value[%u]: %s",log_prefix, m, s,
							MultiStructVector[m][s].name.c_str(), MultiStructVector[m][s].type.c_str(), i, MultiStructVector[m][s].values[i].c_str() );
					// Set the values
					fillContainerWithStructAttrValues(tempStruct->memberValue->type, MultiStructVector[m][s].values[i], tempStruct->memberValue->values + i);
				}
				// Set next member (if last, then after for loop set null)
//				tempStruct->next = new ComMoAttributeValueStructMember_3T;
//				tempStruct = tempStruct->next;
			}
//			tempStruct->next = NULL;
		}
		//syslog(LOG_INFO, "%s MO::getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT container nrOfValues: (%i)",log_prefix,(*cont_result)->nrOfValues);

		//syslog(LOG_INFO, "%s MO::getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT container 2nd struct type: (%i)",log_prefix,
		//		(*cont_result)->values[0].value.structMember->next->memberValue->type);
		//syslog(LOG_INFO, "%s MO::getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT container 2nd struct value: (%s)",log_prefix,
		//(*cont_result)->values[0].value.structMember->next->memberValue->values->value.theString);

		//syslog(LOG_INFO, "%s MO::getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT type LEAVE",log_prefix);
		break;

	case ComOamSpiMoAttributeType_3_INT8:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i8 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_INT16:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i16 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_INT32:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i32 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_INT64:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i64 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT8:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u8 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT16:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u16 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT32:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u32 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT64:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u64 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_DECIMAL64:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.decimal64 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_STRING:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		/*multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.theString = (char*)(multiValueVector[i].c_str());
		}*/
		*cont_result = new ComMoAttributeValueContainer_3T;
		(*cont_result)->nrOfValues = 1;
		(*cont_result)->type = theAttribute.attrType;
		(*cont_result)->values = new ComMoAttributeValue_3T[1];
		(*cont_result)->values[0].value.theString = strdup(theAttribute.attrValue.c_str());
		break;

	case ComOamSpiMoAttributeType_3_BOOL:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.theBool = atoi(multiValueVector[i].c_str());
		}
		break;
	case ComOamSpiMoAttributeType_3_ENUM:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.theEnum = atoi(multiValueVector[i].c_str());
		}
		break;

	default:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type not found, returning ComFailure",log_prefix);
		std::string nbi_message = "ComNbi Error: Unexpected attribute type in getMO callback in ";
		nbi_message += component_name;

		_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());

		return ComFailure;
	}

	// saving the pointer of the container for freeing it later
	if(!saveToDeleteList(txHandle, *cont_result))
	{
		std::string nbi_message = "ComNbi Error: Duplicated call for the same txHandle";
		nbi_message += component_name;
		_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());
		return ComFailure;
	}
	syslog(LOG_INFO, "%s MO::getMoAttribute() return ComOk",log_prefix);
	return ComOk;
}


ComReturnT getMoAttributes(ComOamSpiTransactionHandleT txHandle,
							const char * dn,
							const char ** attributeNames,
							ComMoAttributeValuesResult_3T * result)
{
	syslog(LOG_INFO, "%s MO::getMoAttributes() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}


ComReturnT newMoIterator(ComOamSpiTransactionHandleT txHandle,
		const  char * dn,
		const  char * className,
		ComOamSpiMoIteratorHandle_3T *result)
{
	syslog(LOG_INFO, "%s MO::newMoIterator() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::newMoIterator(): txHandle %lu dn %s className %s",log_prefix,txHandle,dn,className);
	//TODO dump result

	return ComOk;
}

ComReturnT nextMo(ComOamSpiMoIteratorHandle_3T itHandle, char **result)
{
	syslog(LOG_INFO, "%s MO::nextMo() entered",log_prefix);
	//TODO dump result

	return ComOk;
}

ComReturnT createMo(ComOamSpiTransactionHandleT txHandle,
					const char * parentDn,
					const char * className,
					const char * keyAttributeName,
					const char * keyAttributeValue,
					ComMoNamedAttributeValueContainer_3T ** initialAttributes)
{
	syslog(LOG_INFO, "%s MO::createMo() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::createMo(): parentDn %s className %s keyAttributeName %s keyAttributeValue %s txHandle %lu",log_prefix,parentDn,className,keyAttributeName,keyAttributeValue,txHandle);

	ComReturnT retValue;
	// Check the DN's or MOC's permission in testConfig

	retValue = testConfig->getRegistration(_threadContextIf, parentDn, className, keyAttributeName);

	// If retValue not ComOk then return
	if(retValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::createMo() returning (%i)",log_prefix, retValue);
		return retValue;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	retValue = testConfig->getReturnValue("create");
	// If retValue not ComOk then write return value to syslog
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::createMo() returning (%i)",log_prefix, retValue);
	}
	return retValue;
}

ComReturnT deleteMo(ComOamSpiTransactionHandleT txHandle, const char * dn)
{
	syslog(LOG_INFO, "%s MO::deleteMo() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::deleteMo(): dn %s txHandle %lu",log_prefix,dn,txHandle);

	ComReturnT retValue;
	// Check the DN's or MOC's permission in testConfig
	retValue = testConfig->getRegistration(_threadContextIf, dn);

	// If retValue not ComOk then return
	if(retValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::deleteMo() returning (%i)",log_prefix, retValue);
		return retValue;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	retValue = testConfig->getReturnValue("delete");
	// If retValue not ComOk then write return value to syslog
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::deleteMo() returning (%i)",log_prefix, retValue);
	}
	return retValue;
}


ComReturnT action(ComOamSpiTransactionHandleT txHandle,
					const char * dn,
					const char * name,
					ComMoNamedAttributeValueContainer_3T **parameters,
					ComMoAttributeValueResult_3T * result)
{
	syslog(LOG_INFO, "%s MO::action() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::action(): dn %s name %s txHandle %lu",log_prefix, dn, name, txHandle);

	// ---- begin MO SPI Ver.3 changes ----
	// for the new COM SPI Ver. 3.0 need to convert from
	// ComMoNamedAttributeValueContainer_3T** to ComMoAttributeValueContainer_3T**
	ComMoAttributeValueContainer_3T **cont_parameters;
	ComMoNamedAttributeValueContainer_3T **pP = parameters;
	int i = 0;

	while (*pP) {
		pP++;
		i++;
	}

	cont_parameters = new ComMoAttributeValueContainer_3T*[i+1];

	int j = 0;
	pP = parameters;

	for (j = 0; j < i; j++)
	{
		cont_parameters[j] = &((*pP)->value);
		pP++;
	}

	cont_parameters[j] = NULL;
	result->release   = &(freeContainer);
	result->container = NULL; // since it is not used must be set to NULL
	// ---- end MO SPI Ver.3 changes ----

	ComReturnT permissionReturnValue = testConfig->getRegistration(_threadContextIf, dn);
	if(permissionReturnValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::action() Permission denied, returning %i",log_prefix,permissionReturnValue);
		delete []cont_parameters;
		return permissionReturnValue;
	}

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT retValue;
	retValue = testConfig->getReturnValue("action");
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::action() returning (%i)",log_prefix, retValue);
		delete []cont_parameters;
		return retValue;
	}

	ComOamSpiMoAttributeType_3T actionParamType;
	actionParamType = testConfig->getAction(dn,name);

	std::string paramList = "";
	switch (actionParamType) {

	case ComOamSpiMoAttributeType_3_STRING:
		if(cont_parameters[0]!= NULL)
		{
			std::string paramText = "";
			paramText = cont_parameters[0]->values->value.theString;
			syslog(LOG_INFO, "%s MO::action(): paramText: %s",log_prefix, paramText.c_str());
			if(paramText.length() >= 9)
			{
				if(paramText.substr(0,4) == "\"REG" || paramText.substr(0,6) == "\"UNREG" || paramText.substr(0,9) == "\"show all" || paramText.substr(0,6) == "\"ALARM" || paramText.substr(0,4) == "\"LOG")
				{
					syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i",log_prefix,dn, name, actionParamType);
					syslog(LOG_INFO, "%s MO::action(): Control commands entered: %s",log_prefix, paramText.c_str());
					retValue = testComponentControl(paramText);
					syslog(LOG_INFO, "%s MO::action() returning %i",log_prefix, retValue);
					delete []cont_parameters;
					return retValue;
				}
			}
		}

		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			paramList += cont_parameters[i]->values->value.theString;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());

		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT8:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.i8);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT16:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.i16);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT32:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.i32);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT64:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%li", cont_parameters[i]->values->value.i64);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT8:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.u8);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT16:

		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.u16);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT32:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.u32);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT64:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%li", cont_parameters[i]->values->value.u64);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_DECIMAL64:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%f", cont_parameters[i]->values->value.decimal64);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_BOOL:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.theBool);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;
	case ComOamSpiMoAttributeType_3_ENUM:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%ld", cont_parameters[i]->values->value.theEnum);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	default:
		syslog(LOG_INFO, "%s MO::action() type not found, returning ComFailure",log_prefix);
		std::string nbi_message = "ComNbi Error: Unexpected action method callback received by ";
		nbi_message += component_name;

		_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());

		delete []cont_parameters;
		return ComFailure;
	}
}


ComReturnT finalizeMoIterator(ComOamSpiMoIteratorHandle_3T itHandle)
{
	syslog(LOG_INFO, "%s MO::finalizeMoIterator() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}


ComReturnT existsMo(ComOamSpiTransactionHandleT txHandle,
					const char * dn,
					bool * result)
{
	syslog(LOG_INFO, "%s MO::existsMo() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}


ComReturnT countMoChildren(ComOamSpiTransactionHandleT txHandle,
							const char * dn,
							const char * className,
							uint64_t * result)
{
	syslog(LOG_INFO, "%s MO::countMoChildren() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}

/*SDP1694 - support MAF SPI */

/****************************************************************************************************************
 ***************************************************************************************************************
 ***************************************************************************************************************
 *
 *  ComOamSpiManagedObject_3T interface functions
 *
 ***************************************************************************************************************
 ***************************************************************************************************************
 ***************************************************************************************************************/
ComReturnT maf_setMoAttribute(ComOamSpiTransactionHandleT txHandle,
		const char * dn,
		const char * attributeName,
		const ComMoAttributeValueContainer_3T * attributeValueContainer)
{
	syslog(LOG_INFO, "%s MO::maf_setMoAttribute() entered",log_prefix);
	std::string structAttrValuesAndTypes = "";
	//Mr20275
	std::string DN_MR20275 = "ManagedElement=1,ObjectMr20275=1";
	if (dn == DN_MR20275)
	{
		flag_mr20275 = true;
		syslog(LOG_INFO, "%s MO::maf_setMoAttribute() flag_mr20275 is TRUE",log_prefix);
	}
	else flag_mr20275 = false;

	if (attributeValueContainer!=NULL) {
		switch (attributeValueContainer->type) {

		case ComOamSpiMoAttributeType_3_STRUCT:
			syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): ComOamSpiMoAttributeType_3_STRUCT ENTERED",log_prefix);
			syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s txHandle %lu",log_prefix,dn,attributeName,txHandle);
			syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): ComOamSpiMoAttributeType_3_STRUCT nrOfValues: %u",log_prefix, attributeValueContainer->nrOfValues);
			if(attributeValueContainer->values->value.structMember == NULL)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): ComOamSpiMoAttributeType_3_STRUCT is NULL",log_prefix);
				return ComFailure;
			}
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				structAttrValuesAndTypes = getAttrsFromStructForSetMO((attributeValueContainer->values)[i].value.structMember);
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): attributeName: %s Struct[%d]: %s",log_prefix, attributeName, i, structAttrValuesAndTypes.c_str());
			}
			break;

		case ComOamSpiMoAttributeType_3_INT8:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i8,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_INT16:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i16,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_INT32:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i32,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_INT64:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %ld txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.i64,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT8:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %u txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u8,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT16:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %u txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u16,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT32:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %u txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u32,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_UINT64:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %lu txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u64,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_DECIMAL64:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %f txHandle %f",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.u64,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_STRING:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %s txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.theString,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_BOOL:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.theBool,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_ENUM:
			for(unsigned int i = 0; i < attributeValueContainer->nrOfValues; i++)
			{
				syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): dn %s attributeName %s attributeValue %d txHandle %lu",log_prefix,dn,attributeName,attributeValueContainer->values[i].value.theEnum,txHandle);
			}
			break;
		case ComOamSpiMoAttributeType_3_REFERENCE:
			syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): ComOamSpiMoAttributeType_3_REFERENCE ENTERED",log_prefix);
			break;

/*  // DERIVED and VOID not supported in MO SPI Ver.3
		case ComOamSpiMoAttributeType_DERIVED:
			syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): ComOamSpiMoAttributeType_DERIVED ENTERED",log_prefix);
			break;
		case ComOamSpiMoAttributeType_VOID:
			syslog(LOG_INFO, "%s MO::maf_setMoAttribute(): ComOamSpiMoAttributeType_VOID ENTERED",log_prefix);
			break;
*/
		default:
			// This is a fault, a type we do not support is received
			syslog(LOG_INFO, "%s MO::maf_setMoAttribute() AttributeValue : UNKNOW TYPE RECEIVED",log_prefix);
			return ComFailure;
			break;
		}
	}else {
		syslog(LOG_INFO, "%s MO::maf_setMoAttribute() attributeValueContainer equal to NULL ",log_prefix);
	}

	ComReturnT permissionReturnValue = testConfig->maf_getRegistration(_maf_threadContextIf, dn);
	if(permissionReturnValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::maf_setMoAttribute() Permission denied, returning %i",log_prefix,permissionReturnValue);
		return permissionReturnValue;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT retValue;
	retValue = testConfig->getReturnValue("set");
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::maf_setMoAttribute() returning (%i)",log_prefix, retValue);
	}
	return retValue;
}



ComReturnT maf_getMoAttribute(ComOamSpiTransactionHandleT txHandle,
		const char * dn,
		const char * attributeName,
		ComMoAttributeValueResult_3T * result)
{
	syslog(LOG_INFO, "%s MO::maf_getMoAttribute() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::maf_getMoAttribute(): dn %s attributeName %s txHandle %lu",log_prefix,dn,attributeName,txHandle);

	// changes for MO SPI Ver.3
	ComMoAttributeValueContainer_3T** cont_result = &(result->container);
	result->release = &(dummyReleaseOne);

	ComReturnT permissionReturnValue = testConfig->maf_getRegistration(_maf_threadContextIf, dn);
	if(permissionReturnValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() Permission denied, returning %i",log_prefix,permissionReturnValue);
		return permissionReturnValue;
	}

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT retValue;
	retValue = testConfig->getReturnValue("get");
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() returning (%i)",log_prefix, retValue);
		return retValue;
	}

	Attribute theAttribute;
	theAttribute = testConfig->getAttribute(dn, attributeName);
	std::vector<std::string> multiValueVector;
	vector<StructVectorType>  MultiStructVector;

	switch (theAttribute.attrType) {

	case ComOamSpiMoAttributeType_3_STRUCT:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT type ENTER",log_prefix);

		// Parse the testconfig and create a MultiStructVector (vector of vectors of attributes)
		getMultiStructVector(theAttribute.attrValue, MultiStructVector);
		// Allocate memory for the container and for the values
		prepareContainer(theAttribute.attrType, MultiStructVector.size(), cont_result);
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT nrOfValues: %i",log_prefix, MultiStructVector.size());

		// For all the structs fill in the container
		for(unsigned int m = 0; m < MultiStructVector.size(); m++)
		{
			ComMoAttributeValueStructMember_3T * tempStruct;
			// allocate memory for the struct
			(*cont_result)->values[m].value.structMember = NULL; // new ComMoAttributeValueStructMember_3T;
			// using tempStruct for operations on the linked list
			// so keeping the original "(*cont_result)->values[m].value.structMember" as a head of the linked list
//			tempStruct = (*cont_result)->values[m].value.structMember;

			ComMoAttributeValueStructMember_3T * temp;
			for(unsigned int s = 0; s < MultiStructVector[m].size(); s++)
			{
				temp = new ComMoAttributeValueStructMember_3T;
				memset(temp, 0, sizeof(ComMoAttributeValueStructMember_3T));
				temp->next = NULL;

				if((*cont_result)->values[m].value.structMember == NULL) {
					(*cont_result)->values[m].value.structMember = temp;
					tempStruct = temp;
				} else {
					tempStruct->next = temp;
					tempStruct = temp;
				}

				// Set member name
				tempStruct->memberName = strdup(MultiStructVector[m][s].name.c_str());
				// Allocate memory for container
				tempStruct->memberValue = new ComMoAttributeValueContainer_3T;
				// Set the type
				tempStruct->memberValue->type = findTypeForStructAttr(MultiStructVector[m][s].type.c_str());
				// Set the number of values
				tempStruct->memberValue->nrOfValues =  MultiStructVector[m][s].values.size();
				// Allocate memory for values
				tempStruct->memberValue->values = new ComMoAttributeValue_3T[tempStruct->memberValue->nrOfValues];

				for(unsigned int i = 0; i < tempStruct->memberValue->nrOfValues; i++)
				{
					syslog(LOG_INFO, "%s MO::maf_getMoAttribute(): Struct %d,%d name: %s type: %s value[%u]: %s",log_prefix, m, s,
							MultiStructVector[m][s].name.c_str(), MultiStructVector[m][s].type.c_str(), i, MultiStructVector[m][s].values[i].c_str() );
					// Set the values
					fillContainerWithStructAttrValues(tempStruct->memberValue->type, MultiStructVector[m][s].values[i], tempStruct->memberValue->values + i);
				}

				// Set next member (if last, then after for loop set null)
//				tempStruct->next = new ComMoAttributeValueStructMember_3T;
//				tempStruct = tempStruct->next;
			}
//			tempStruct->next = NULL;
		}
//		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT container nrOfValues: (%i)",log_prefix,(*cont_result)->nrOfValues);
//
//		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT container 2nd struct type: (%i)",log_prefix,
//				(*cont_result)->values[0].value.structMember->next->memberValue->type);
//		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT container 2nd struct value: (%s)",log_prefix,
//		(*cont_result)->values[0].value.structMember->next->memberValue->values->value.theString);
//
//		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() ComOamSpiMoAttributeType_3_STRUCT type LEAVE",log_prefix);
		break;

	case ComOamSpiMoAttributeType_3_INT8:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i8 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_INT16:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i16 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_INT32:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i32 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_INT64:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.i64 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT8:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u8 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT16:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u16 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT32:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u32 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_UINT64:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.u64 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_DECIMAL64:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.decimal64 = atoi(multiValueVector[i].c_str());
		}
		break;

	case ComOamSpiMoAttributeType_3_STRING:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		/*multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.theString = (char*)(multiValueVector[i].c_str());
		}*/
		*cont_result = new ComMoAttributeValueContainer_3T;
		syslog(LOG_INFO, "%s maf_getMoAttribute(): string type: container(%p)",log_prefix,*cont_result);
		(*cont_result)->nrOfValues = 1;
		(*cont_result)->type = theAttribute.attrType;
		(*cont_result)->values = new ComMoAttributeValue_3T[1];
		(*cont_result)->values[0].value.theString = strdup(theAttribute.attrValue.c_str());
		break;

	case ComOamSpiMoAttributeType_3_BOOL:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.theBool = atoi(multiValueVector[i].c_str());
		}
		break;
	case ComOamSpiMoAttributeType_3_ENUM:
		syslog(LOG_INFO, "%s MO::getMoAttribute() type %i entered",log_prefix, theAttribute.attrType);
		multiValueVector = multiValueStringToVector(theAttribute.attrValue);
		prepareContainer(theAttribute.attrType, multiValueVector.size(), cont_result);
		for(unsigned int i = 0; i < multiValueVector.size(); i++)
		{
			//syslog(LOG_INFO, "%s MO::getMoAttribute(): multivalue element %i: %s",log_prefix,i,multiValueVector[i].c_str());
			(*cont_result)->values[i].value.theEnum = atoi(multiValueVector[i].c_str());
		}
		break;

	default:
		syslog(LOG_INFO, "%s MO::maf_getMoAttribute() type not found, returning ComFailure",log_prefix);
		std::string nbi_message = "ComNbi Error: Unexpected attribute type in getMO callback in ";
		nbi_message += component_name;
		_maf_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());
		return ComFailure;
	}

	// saving the pointer of the container for freeing it later
	if(!saveToDeleteList(txHandle, *cont_result))
	{
		std::string nbi_message = "ComNbi Error: Duplicated call for the same txHandle";
		nbi_message += component_name;
		_maf_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());
		return ComFailure;
	}
	syslog(LOG_INFO, "%s MO::getMoAttribute() return ComOk",log_prefix);
	return ComOk;
}


ComReturnT maf_getMoAttributes(ComOamSpiTransactionHandleT txHandle,
							const char * dn,
							const char ** attributeNames,
							ComMoAttributeValuesResult_3T * result)
{
	syslog(LOG_INFO, "%s MO::maf_getMoAttributes() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}


ComReturnT maf_newMoIterator(ComOamSpiTransactionHandleT txHandle,
		const  char * dn,
		const  char * className,
		ComOamSpiMoIteratorHandle_3T *result)
{
	syslog(LOG_INFO, "%s MO::maf_newMoIterator() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::maf_newMoIterator(): txHandle %lu dn %s className %s",log_prefix,txHandle,dn,className);
	//TODO dump result

	return ComOk;
}

ComReturnT maf_nextMo(ComOamSpiMoIteratorHandle_3T itHandle, char **result)
{
	syslog(LOG_INFO, "%s MO::maf_nextMo() entered",log_prefix);
	//TODO dump result

	return ComOk;
}

ComReturnT maf_createMo(ComOamSpiTransactionHandleT txHandle,
					const char * parentDn,
					const char * className,
					const char * keyAttributeName,
					const char * keyAttributeValue,
					ComMoNamedAttributeValueContainer_3T ** initialAttributes)
{
	syslog(LOG_INFO, "%s MO::maf_createMo() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::maf_createMo(): parentDn %s className %s keyAttributeName %s keyAttributeValue %s txHandle %lu",log_prefix,parentDn,className,keyAttributeName,keyAttributeValue,txHandle);

	ComReturnT retValue;
	// Check the DN's or MOC's permission in testConfig
	retValue = testConfig->maf_getRegistration(_maf_threadContextIf, parentDn, className, keyAttributeName);

	// If retValue not ComOk then return
	if(retValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::createMo() returning (%i)",log_prefix, retValue);
		return retValue;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	retValue = testConfig->getReturnValue("create");
	// If retValue not ComOk then write return value to syslog
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::createMo() returning (%i)",log_prefix, retValue);
	}
	return retValue;
}

ComReturnT maf_deleteMo(ComOamSpiTransactionHandleT txHandle, const char * dn)
{
	syslog(LOG_INFO, "%s MO::maf_deleteMo() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::maf_deleteMo(): dn %s txHandle %lu",log_prefix,dn,txHandle);

	ComReturnT retValue;
	// Check the DN's or MOC's permission in testConfig
	retValue = testConfig->maf_getRegistration(_maf_threadContextIf, dn);

	// If retValue not ComOk then return
	if(retValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::maf_deleteMo() returning (%i)",log_prefix, retValue);
		return retValue;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	retValue = testConfig->getReturnValue("delete");
	// If retValue not ComOk then write return value to syslog
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::maf_deleteMo() returning (%i)",log_prefix, retValue);
	}
	return retValue;
}


ComReturnT maf_action(ComOamSpiTransactionHandleT txHandle,
					const char * dn,
					const char * name,
					ComMoNamedAttributeValueContainer_3T **parameters,
					ComMoAttributeValueResult_3T * result)
{
	syslog(LOG_INFO, "%s MO::maf_action() entered",log_prefix);
	syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s txHandle %lu",log_prefix, dn, name, txHandle);

	// ---- begin MO SPI Ver.3 changes ----
	// for the new COM SPI Ver. 3.0 need to convert from
	// ComMoNamedAttributeValueContainer_3T** to ComMoAttributeValueContainer_3T**
	ComMoAttributeValueContainer_3T **cont_parameters;
	ComMoNamedAttributeValueContainer_3T **pP = parameters;
	//SDP872 changes
	ComMoAttributeValueContainer_3T *sdp872_parameters;
	//mr24146 changes
	ComMoAttributeValueContainer_3T *mr24146_parameters;
	std::string actionName (name);

	int i = 0;

	while (*pP) {
		pP++;
		i++;
	}

	cont_parameters = new ComMoAttributeValueContainer_3T*[i+1];

	int j = 0;
	pP = parameters;

	for (j = 0; j < i; j++)
	{
		cont_parameters[j] = &((*pP)->value);
		pP++;
	}

	cont_parameters[j] = NULL;
	result->release   = &(freeContainer);
	result->container = NULL; // since it is not used must be set to NULL
	// ---- end MO SPI Ver.3 changes ----


	//BEGIN SDP872 UC2 changes - return values to COM
	syslog(LOG_INFO, "%s MO::maf_action() actionName: %s", log_prefix, actionName.c_str());


	if(actionName == "testReturnMultiBool") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[4];
			if (sdp872_parameters->values != NULL)
			{

				sdp872_parameters->type = ComOamSpiMoAttributeType_3_BOOL;
				sdp872_parameters->nrOfValues = 4;
				sdp872_parameters->values[0].value.theBool = false;
				sdp872_parameters->values[1].value.theBool = false;
				sdp872_parameters->values[2].value.theBool = true;
				sdp872_parameters->values[3].value.theBool = false;


				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if((actionName == "testReturnNothing") || (actionName == "noReturn")) {
		delete []cont_parameters;
		return ComOk;
	}
	else if(actionName == "testReturnNoInput") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (sdp872_parameters->values != NULL)
			{
				sdp872_parameters->type = ComOamSpiMoAttributeType_3_INT32;
				sdp872_parameters->nrOfValues = 1;
				sdp872_parameters->values[0].value.i32 = 64646464;

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if(actionName == "testReturnMultiInt") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[3];
			if (sdp872_parameters->values != NULL)
			{
				sdp872_parameters->type = ComOamSpiMoAttributeType_3_INT32;
				sdp872_parameters->nrOfValues = 3;
				sdp872_parameters->values[0].value.i32 = 64646464;
				sdp872_parameters->values[1].value.i32 = 46464646;
				sdp872_parameters->values[2].value.i32 = 55667788;

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if(actionName == "testReturnSingleBool") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (sdp872_parameters->values != NULL)
			{

				sdp872_parameters->type = ComOamSpiMoAttributeType_3_BOOL;
				sdp872_parameters->nrOfValues = 1;
				sdp872_parameters->values[0].value.theBool = false;

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if(actionName == "testReturnSingleInt") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (sdp872_parameters->values != NULL)
			{

				sdp872_parameters->type = ComOamSpiMoAttributeType_3_INT32;
				sdp872_parameters->nrOfValues = 1;
				sdp872_parameters->values[0].value.i32 = 32323232;

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if(actionName == "testReturnSingleString") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (sdp872_parameters->values != NULL)
			{

				sdp872_parameters->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->nrOfValues = 1;

				std::string testString = "@SDP872 testReturnSingleString UC2: Test String";
				sdp872_parameters->values[0].value.theString = (char *)malloc(testString.length());
				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.theString), testString.c_str() );

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if (actionName == "testReturnStruct") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (sdp872_parameters->values != NULL)
			{
				sdp872_parameters->type = ComOamSpiMoAttributeType_3_STRUCT;
				sdp872_parameters->nrOfValues = 1;

					sdp872_parameters->values[0].value.structMember = new ComMoAttributeValueStructMember_3T;
					memset(sdp872_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[0].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[0].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue->nrOfValues = 1;
				sdp872_parameters->values[0].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->values[0].value.structMember->memberValue->values = new ComMoAttributeValue_3T[1];

				if( sdp872_parameters->values[0].value.structMember->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}
				std::string ParamText = "@SDP872 testReturnStruct UC2: Struct String member";
				sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString = (char *)malloc(ParamText.length());
				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString), ParamText.c_str() );
				//sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString[ParamText.length()]='\0';

				sdp872_parameters->values[0].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if( sdp872_parameters->values[0].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->nrOfValues = 1;
				sdp872_parameters->values[0].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_INT32;

				sdp872_parameters->values[0].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[1];

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->values[0].value.i32 = 12345678;
				sdp872_parameters->values[0].value.structMember->next->next = NULL;

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if (actionName == "testReturnStruct02") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (sdp872_parameters->values != NULL)
			{
				sdp872_parameters->type = ComOamSpiMoAttributeType_3_STRUCT;
				sdp872_parameters->nrOfValues = 1;

				sdp872_parameters->values[0].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[0].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[0].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue->nrOfValues = 3;
				sdp872_parameters->values[0].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->values[0].value.structMember->memberValue->values = new ComMoAttributeValue_3[3];

				if( sdp872_parameters->values[0].value.structMember->memberValue->values == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				std::string ParamText1 = "@SDP872 testReturnStruct02 UC2: Struct String member 1";
				std::string ParamText2 = "@SDP872 testReturnStruct02 UC2: Struct String member 2";
				std::string ParamText3 = "@SDP872 testReturnStruct02 UC2: Struct String member 3";

				sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString = (char*) calloc(ParamText1.length()+1,sizeof(char));
				sdp872_parameters->values[0].value.structMember->memberValue->values[1].value.theString = (char*) calloc(ParamText2.length()+1,sizeof(char));
				sdp872_parameters->values[0].value.structMember->memberValue->values[2].value.theString = (char*) calloc(ParamText3.length()+1,sizeof(char));

				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString), ParamText1.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[1].value.theString), ParamText2.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[2].value.theString), ParamText3.c_str() );

				sdp872_parameters->values[0].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));
				if( sdp872_parameters->values[0].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->nrOfValues = 4;
				sdp872_parameters->values[0].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_INT32;

				sdp872_parameters->values[0].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[4];

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->values[0].value.i32 =  (int) 12345678;
				sdp872_parameters->values[0].value.structMember->next->memberValue->values[1].value.i32 =  (int) 23456789;
				sdp872_parameters->values[0].value.structMember->next->memberValue->values[2].value.i32 =  (int) 34567890;
				sdp872_parameters->values[0].value.structMember->next->memberValue->values[3].value.i32 =  (int) 45678901;

				sdp872_parameters->values[0].value.structMember->next->next = NULL;
				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if (actionName == "testReturnStructAllTypes") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (sdp872_parameters->values != NULL)
			{
				ComMoAttributeValueStructMember_3T *StructMemberPtr;

				sdp872_parameters->type = ComOamSpiMoAttributeType_3_STRUCT;
				sdp872_parameters->nrOfValues = 1;

				sdp872_parameters->values[0].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[0].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[0].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue->nrOfValues = 1;
				sdp872_parameters->values[0].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_BOOL;
				sdp872_parameters->values[0].value.structMember->memberValue->values = new ComMoAttributeValue_3T[1];

				if( sdp872_parameters->values[0].value.structMember->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theBool = true;

				//Create new member in structure
				StructMemberPtr = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr, 0, sizeof(ComMoAttributeValueStructMember_3T));
				sdp872_parameters->values[0].value.structMember->next = StructMemberPtr;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create INT16 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_INT16;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.i16 = 23456;


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create INT32 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_INT32;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.i32 = 1234567;


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create INT64 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_INT64;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.i64 = 123456789;



				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create INT8 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_INT8;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.i8 = 123;


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create STRING value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				std::string ParamText = "@SDP872 testReturnStructAllTypes UC2: Struct String member";
				StructMemberPtr->memberValue->values[0].value.theString = (char*) calloc(ParamText.length()+1,sizeof(char));
				strcpy(const_cast<char *>(StructMemberPtr->memberValue->values[0].value.theString), ParamText.c_str() );


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create UINT16 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_UINT16;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.u16 = 34567;


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create UINT32 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_UINT32;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.u32 = 2345678;


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create UINT64 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_UINT64;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.u64 = 234567890;


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create UINT8 value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_UINT8;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.u8 = 234;

				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create Derived Int value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_INT16;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.i16 = 34567;

				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create Derived String value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}


				std::string DerivedText = "@SDP872 testReturnStructAllTypes UC2: Struct Derived String member";
				StructMemberPtr->memberValue->values[0].value.theString = (char*) calloc(DerivedText.length()+1,sizeof(char));
				strncpy(const_cast<char *>(StructMemberPtr->memberValue->values[0].value.theString), DerivedText.c_str(),DerivedText.length());


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
				StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create ENUM value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_ENUM;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

				StructMemberPtr->memberValue->values[0].value.theEnum = 2;


				//Create new member in structure
				StructMemberPtr->next = new ComMoAttributeValueStructMember_3T;
				memset(StructMemberPtr->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				StructMemberPtr = StructMemberPtr->next;

				if( StructMemberPtr == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}
					StructMemberPtr->memberValue = new ComMoAttributeValueContainer_3;

				if( StructMemberPtr->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				// Create REFERENCE value
				StructMemberPtr->memberValue->nrOfValues = 1;
				StructMemberPtr->memberValue->type = ComOamSpiMoAttributeType_3_REFERENCE;
				StructMemberPtr->memberValue->values = new ComMoAttributeValue_3T[1];

				if( StructMemberPtr->memberValue->values== NULL){
					delete []cont_parameters;
					return ComFailure;
				}

#ifdef TEST_FOR_LONG_DN
				std::string RefText = "ManagedElement=1,Sdp617ActiontestRoot=This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_1";
#else
				std::string RefText = "ManagedElement=1,Sdp617ActiontestRoot=1";
#endif
				StructMemberPtr->memberValue->values[0].value.moRef = (char*) calloc(RefText.length()+1,sizeof(char));
				strcpy(const_cast<char *>(StructMemberPtr->memberValue->values[0].value.moRef), RefText.c_str() );


				StructMemberPtr->next = NULL;

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if (actionName == "testReturnMultiStruct") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[2];
			if (sdp872_parameters->values != NULL)
			{
				sdp872_parameters->type = ComOamSpiMoAttributeType_3_STRUCT;
				sdp872_parameters->nrOfValues = 2;
				//Populate structure A
				sdp872_parameters->values[0].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[0].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[0].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue->nrOfValues = 1;
				sdp872_parameters->values[0].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->values[0].value.structMember->memberValue->values = new ComMoAttributeValue_3T[1];

				if( sdp872_parameters->values[0].value.structMember->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}
				std::string ParamTextA = "@SDP872 testReturnMultiStruct UC2: Struct A String member";
				sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString = (char *)malloc(ParamTextA.length());
				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString), ParamTextA.c_str() );
				//sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString[ParamText.length()]='\0';

				sdp872_parameters->values[0].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if( sdp872_parameters->values[0].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->nrOfValues = 1;
				sdp872_parameters->values[0].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_INT32;

				sdp872_parameters->values[0].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[1];

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->values[0].value.i32 = 12345678;
				sdp872_parameters->values[0].value.structMember->next->next = NULL;

				//Populate structure B
				sdp872_parameters->values[1].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[1].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[1].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[1].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->memberValue->nrOfValues = 1;
				sdp872_parameters->values[1].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->values[1].value.structMember->memberValue->values = new ComMoAttributeValue_3T[1];

				if( sdp872_parameters->values[1].value.structMember->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}
				std::string ParamTextB = "@SDP872 testReturnMultiStruct UC2: Struct B String member";
				sdp872_parameters->values[1].value.structMember->memberValue->values[0].value.theString = (char *)malloc(ParamTextB.length());
				strcpy(const_cast<char *>(sdp872_parameters->values[1].value.structMember->memberValue->values[0].value.theString), ParamTextB.c_str() );

				sdp872_parameters->values[1].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[1].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if( sdp872_parameters->values[1].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( sdp872_parameters->values[1].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->next->memberValue->nrOfValues = 1;
				sdp872_parameters->values[1].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_INT32;

				sdp872_parameters->values[1].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[1];

				if( sdp872_parameters->values[1].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->next->memberValue->values[0].value.i32 = 87654321;
				sdp872_parameters->values[1].value.structMember->next->next = NULL;

				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if (actionName == "testReturnMultiStruct02") {

		sdp872_parameters = new ComMoAttributeValueContainer_3T;

		if (sdp872_parameters != NULL)
		{
			sdp872_parameters->values 				= new ComMoAttributeValue_3T[3];
			if (sdp872_parameters->values != NULL)
			{

				sdp872_parameters->type = ComOamSpiMoAttributeType_3_STRUCT;
				sdp872_parameters->nrOfValues = 3;

				// Populate structure A
				sdp872_parameters->values[0].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[0].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[0].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->memberValue->nrOfValues = 3;
				sdp872_parameters->values[0].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->values[0].value.structMember->memberValue->values = new ComMoAttributeValue_3[3];

				if( sdp872_parameters->values[0].value.structMember->memberValue->values == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				std::string ParamText1 = "@SDP872 testReturnMultiStruct02 UC2: Struct A String member 1";
				std::string ParamText2 = "@SDP872 testReturnMultiStruct02 UC2: Struct A String member 2";
				std::string ParamText3 = "@SDP872 testReturnMultiStruct02 UC2: Struct A String member 3";

				sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString = (char*) calloc(ParamText1.length()+1,sizeof(char));
				sdp872_parameters->values[0].value.structMember->memberValue->values[1].value.theString = (char*) calloc(ParamText2.length()+1,sizeof(char));
				sdp872_parameters->values[0].value.structMember->memberValue->values[2].value.theString = (char*) calloc(ParamText3.length()+1,sizeof(char));

				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[0].value.theString), ParamText1.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[1].value.theString), ParamText2.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[0].value.structMember->memberValue->values[2].value.theString), ParamText3.c_str() );

				sdp872_parameters->values[0].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[0].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				if( sdp872_parameters->values[0].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->nrOfValues = 4;
				sdp872_parameters->values[0].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_INT32;

				sdp872_parameters->values[0].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[4];

				if( sdp872_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[0].value.structMember->next->memberValue->values[0].value.i32 =  (int) 12345678;
				sdp872_parameters->values[0].value.structMember->next->memberValue->values[1].value.i32 =  (int) 23456789;
				sdp872_parameters->values[0].value.structMember->next->memberValue->values[2].value.i32 =  (int) 34567890;
				sdp872_parameters->values[0].value.structMember->next->memberValue->values[3].value.i32 =  (int) 45678901;

				sdp872_parameters->values[0].value.structMember->next->next = NULL;

				// Populate structure B
				sdp872_parameters->values[1].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[1].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[1].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[1].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->memberValue->nrOfValues = 3;
				sdp872_parameters->values[1].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->values[1].value.structMember->memberValue->values = new ComMoAttributeValue_3[3];

				if( sdp872_parameters->values[1].value.structMember->memberValue->values == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				std::string ParamTextB1 = "@SDP872 testReturnMultiStruct02 UC2: Struct B String member 1";
				std::string ParamTextB2 = "@SDP872 testReturnMultiStruct02 UC2: Struct B String member 2";
				std::string ParamTextB3 = "@SDP872 testReturnMultiStruct02 UC2: Struct B String member 3";

				sdp872_parameters->values[1].value.structMember->memberValue->values[0].value.theString = (char*) calloc(ParamTextB1.length()+1,sizeof(char));
				sdp872_parameters->values[1].value.structMember->memberValue->values[1].value.theString = (char*) calloc(ParamTextB2.length()+1,sizeof(char));
				sdp872_parameters->values[1].value.structMember->memberValue->values[2].value.theString = (char*) calloc(ParamTextB3.length()+1,sizeof(char));

				strcpy(const_cast<char *>(sdp872_parameters->values[1].value.structMember->memberValue->values[0].value.theString), ParamTextB1.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[1].value.structMember->memberValue->values[1].value.theString), ParamTextB2.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[1].value.structMember->memberValue->values[2].value.theString), ParamTextB3.c_str() );

				sdp872_parameters->values[1].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[1].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				if( sdp872_parameters->values[1].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( sdp872_parameters->values[1].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->next->memberValue->nrOfValues = 4;
				sdp872_parameters->values[1].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_INT32;

				sdp872_parameters->values[1].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[4];

				if( sdp872_parameters->values[1].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[1].value.structMember->next->memberValue->values[0].value.i32 =  (int) 13579;
				sdp872_parameters->values[1].value.structMember->next->memberValue->values[1].value.i32 =  (int) 24680;
				sdp872_parameters->values[1].value.structMember->next->memberValue->values[2].value.i32 =  (int) 35791;
				sdp872_parameters->values[1].value.structMember->next->memberValue->values[3].value.i32 =  (int) 46802;

				sdp872_parameters->values[1].value.structMember->next->next = NULL;

				// Populate structure C
				sdp872_parameters->values[2].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[2].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (sdp872_parameters->values[2].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[2].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (sdp872_parameters->values[2].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[2].value.structMember->memberValue->nrOfValues = 3;
				sdp872_parameters->values[2].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				sdp872_parameters->values[2].value.structMember->memberValue->values = new ComMoAttributeValue_3[3];

				if( sdp872_parameters->values[2].value.structMember->memberValue->values == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				std::string ParamTextC1 = "@SDP872 testReturnMultiStruct02 UC2: Struct C String member 1";
				std::string ParamTextC2 = "@SDP872 testReturnMultiStruct02 UC2: Struct C String member 2";
				std::string ParamTextC3 = "@SDP872 testReturnMultiStruct02 UC2: Struct C String member 3";

				sdp872_parameters->values[2].value.structMember->memberValue->values[0].value.theString = (char*) calloc(ParamTextC1.length()+1,sizeof(char));
				sdp872_parameters->values[2].value.structMember->memberValue->values[1].value.theString = (char*) calloc(ParamTextC2.length()+1,sizeof(char));
				sdp872_parameters->values[2].value.structMember->memberValue->values[2].value.theString = (char*) calloc(ParamTextC3.length()+1,sizeof(char));

				strcpy(const_cast<char *>(sdp872_parameters->values[2].value.structMember->memberValue->values[0].value.theString), ParamTextC1.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[2].value.structMember->memberValue->values[1].value.theString), ParamTextC2.c_str() );
				strcpy(const_cast<char *>(sdp872_parameters->values[2].value.structMember->memberValue->values[2].value.theString), ParamTextC3.c_str() );

				sdp872_parameters->values[2].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(sdp872_parameters->values[2].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));
				if( sdp872_parameters->values[2].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[2].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( sdp872_parameters->values[2].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[2].value.structMember->next->memberValue->nrOfValues = 4;
				sdp872_parameters->values[2].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_INT32;

				sdp872_parameters->values[2].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[4];

				if( sdp872_parameters->values[2].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				sdp872_parameters->values[2].value.structMember->next->memberValue->values[0].value.i32 =  (int) 97351;
				sdp872_parameters->values[2].value.structMember->next->memberValue->values[1].value.i32 =  (int) 86420;
				sdp872_parameters->values[2].value.structMember->next->memberValue->values[2].value.i32 =  (int) 75319;
				sdp872_parameters->values[2].value.structMember->next->memberValue->values[3].value.i32 =  (int) 64208;

				sdp872_parameters->values[2].value.structMember->next->next = NULL;


				result->container = sdp872_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}



//-----END SDP872 UC2 changes -------------------

//BEGIN MR24146 UC2 changes - return values to COM


	else if(actionName == "testReturnSingleFloat") {

		mr24146_parameters = new ComMoAttributeValueContainer_3T;

		if (mr24146_parameters != NULL)
		{
			mr24146_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (mr24146_parameters->values != NULL)
			{

				mr24146_parameters->type = ComOamSpiMoAttributeType_3_DECIMAL64;
				mr24146_parameters->nrOfValues = 1;
				mr24146_parameters->values[0].value.decimal64 = 3.14159 ;

				result->container = mr24146_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if(actionName == "testArrayFloat") {

		mr24146_parameters = new ComMoAttributeValueContainer_3T;

		if (mr24146_parameters != NULL)
		{
			mr24146_parameters->values 				= new ComMoAttributeValue_3T[3];
			if (mr24146_parameters->values != NULL)
			{
				mr24146_parameters->type = ComOamSpiMoAttributeType_3_DECIMAL64;
				mr24146_parameters->nrOfValues = 3;
				mr24146_parameters->values[0].value.decimal64 = 1.111;
				mr24146_parameters->values[1].value.decimal64 = 2.222;
				mr24146_parameters->values[2].value.decimal64 = 3.333;

				result->container = mr24146_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if(actionName == "testReturnFloat") {

		mr24146_parameters = new ComMoAttributeValueContainer_3T;

		if (mr24146_parameters != NULL)
		{
			mr24146_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (mr24146_parameters->values != NULL)
			{
				mr24146_parameters->type = ComOamSpiMoAttributeType_3_DECIMAL64;
				mr24146_parameters->nrOfValues = 1;
				mr24146_parameters->values[0].value.decimal64 = 4.444;

				result->container = mr24146_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if (actionName == "testReturnStructFloat") {

		mr24146_parameters = new ComMoAttributeValueContainer_3T;

		if (mr24146_parameters != NULL)
		{
			mr24146_parameters->values 				= new ComMoAttributeValue_3T[1];
			if (mr24146_parameters->values != NULL)
			{
				mr24146_parameters->type = ComOamSpiMoAttributeType_3_STRUCT;
				mr24146_parameters->nrOfValues = 1;

				mr24146_parameters->values[0].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(mr24146_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (mr24146_parameters->values[0].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (mr24146_parameters->values[0].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->memberValue->nrOfValues = 1;
				mr24146_parameters->values[0].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				mr24146_parameters->values[0].value.structMember->memberValue->values = new ComMoAttributeValue_3T[1];

				if( mr24146_parameters->values[0].value.structMember->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}
				std::string ParamText = "@mr24146 testReturnStruct UC2: Struct String member";
				mr24146_parameters->values[0].value.structMember->memberValue->values[0].value.theString = (char *)malloc(ParamText.length());
				strcpy(const_cast<char *>(mr24146_parameters->values[0].value.structMember->memberValue->values[0].value.theString), ParamText.c_str() );

				mr24146_parameters->values[0].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(mr24146_parameters->values[0].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if( mr24146_parameters->values[0].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( mr24146_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->next->memberValue->nrOfValues = 1;
				mr24146_parameters->values[0].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_DECIMAL64;

				mr24146_parameters->values[0].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[1];

				if( mr24146_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->next->memberValue->values[0].value.decimal64 = 5.555;
				mr24146_parameters->values[0].value.structMember->next->next = NULL;

				result->container = mr24146_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}
	else if (actionName == "tetsReturnArrayFloat") {

		mr24146_parameters = new ComMoAttributeValueContainer_3T;

		if (mr24146_parameters != NULL)
		{
			mr24146_parameters->values 				= new ComMoAttributeValue_3T[2];
			if (mr24146_parameters->values != NULL)
			{
				mr24146_parameters->type = ComOamSpiMoAttributeType_3_STRUCT;
				mr24146_parameters->nrOfValues = 2;
				//Populate structure A
				mr24146_parameters->values[0].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(mr24146_parameters->values[0].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (mr24146_parameters->values[0].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (mr24146_parameters->values[0].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->memberValue->nrOfValues = 1;
				mr24146_parameters->values[0].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				mr24146_parameters->values[0].value.structMember->memberValue->values = new ComMoAttributeValue_3T[1];

				if( mr24146_parameters->values[0].value.structMember->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}
				std::string ParamTextA = "@mr24146 tetsReturnArrayFloat UC2: Struct A String member";
				mr24146_parameters->values[0].value.structMember->memberValue->values[0].value.theString = (char *)malloc(ParamTextA.length());
				strcpy(const_cast<char *>(mr24146_parameters->values[0].value.structMember->memberValue->values[0].value.theString), ParamTextA.c_str() );

				mr24146_parameters->values[0].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(mr24146_parameters->values[0].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if( mr24146_parameters->values[0].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( mr24146_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->next->memberValue->nrOfValues = 1;
				mr24146_parameters->values[0].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_DECIMAL64;

				mr24146_parameters->values[0].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[1];

				if( mr24146_parameters->values[0].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[0].value.structMember->next->memberValue->values[0].value.decimal64 = 1.2345 ;
				mr24146_parameters->values[0].value.structMember->next->next = NULL;

				//Populate structure B
				mr24146_parameters->values[1].value.structMember = new ComMoAttributeValueStructMember_3T;
				memset(mr24146_parameters->values[1].value.structMember, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if (mr24146_parameters->values[1].value.structMember == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[1].value.structMember->memberValue = new ComMoAttributeValueContainer_3;

				if (mr24146_parameters->values[1].value.structMember->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[1].value.structMember->memberValue->nrOfValues = 1;
				mr24146_parameters->values[1].value.structMember->memberValue->type = ComOamSpiMoAttributeType_3_STRING;
				mr24146_parameters->values[1].value.structMember->memberValue->values = new ComMoAttributeValue_3T[1];

				if( mr24146_parameters->values[1].value.structMember->memberValue->values == NULL){
					delete []cont_parameters;
					return ComFailure;
				}
				std::string ParamTextB = "@mr24146 tetsReturnArrayFloat UC2: Struct B String member";
				mr24146_parameters->values[1].value.structMember->memberValue->values[0].value.theString = (char *)malloc(ParamTextB.length());
				strcpy(const_cast<char *>(mr24146_parameters->values[1].value.structMember->memberValue->values[0].value.theString), ParamTextB.c_str() );

				mr24146_parameters->values[1].value.structMember->next = new ComMoAttributeValueStructMember_3T;
				memset(mr24146_parameters->values[1].value.structMember->next, 0, sizeof(ComMoAttributeValueStructMember_3T));

				if( mr24146_parameters->values[1].value.structMember->next == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[1].value.structMember->next->memberValue = new ComMoAttributeValueContainer_3;

				if( mr24146_parameters->values[1].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[1].value.structMember->next->memberValue->nrOfValues = 1;
				mr24146_parameters->values[1].value.structMember->next->memberValue->type = ComOamSpiMoAttributeType_3_DECIMAL64;

				mr24146_parameters->values[1].value.structMember->next->memberValue->values = new ComMoAttributeValue_3T[1];

				if( mr24146_parameters->values[1].value.structMember->next->memberValue == NULL) {
					delete []cont_parameters;
					return ComFailure;
				}

				mr24146_parameters->values[1].value.structMember->next->memberValue->values[0].value.decimal64 = 5.4321;
				mr24146_parameters->values[1].value.structMember->next->next = NULL;

				result->container = mr24146_parameters;
				delete []cont_parameters;
				return ComOk;
			}
		}
	}


//----END MR24146 UC2  changes -------------------




	ComReturnT permissionReturnValue = testConfig->maf_getRegistration(_maf_threadContextIf, dn);
	if(permissionReturnValue != ComOk)
	{
		syslog(LOG_INFO, "%s MO::maf_action() Permission denied, returning %i",log_prefix,permissionReturnValue);
		delete []cont_parameters;
		return permissionReturnValue;
	}

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *					-an unexpected callback
	 *					-or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT retValue;
	retValue = testConfig->getReturnValue("action");
	if(retValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s MO::maf_action() returning (%i)",log_prefix, retValue);
		std::string errorText = "@ComNbi@Error: action() return failed. SDP875 UC2 test 2";
		_maf_threadContextIf->addMessage(ThreadContextMsgNbi_2, errorText.c_str());
		delete []cont_parameters;
		return retValue;
	}

	ComOamSpiMoAttributeType_3T actionParamType;
	actionParamType = testConfig->getAction(dn,name);

	std::string paramList = "";
	switch (actionParamType) {

	case ComOamSpiMoAttributeType_3_STRING:
		if(cont_parameters[0]!= NULL)
		{
			std::string paramText = "";
			paramText = cont_parameters[0]->values->value.theString;
			syslog(LOG_INFO, "%s MO::maf_action(): paramText: %s",log_prefix, paramText.c_str());
			if(paramText.length() >= 9)
			{
				if(paramText.substr(0,4) == "\"REG" || paramText.substr(0,6) == "\"UNREG" || paramText.substr(0,9) == "\"show all" || paramText.substr(0,6) == "\"ALARM" || paramText.substr(0,4) == "\"LOG" ||
					paramText.substr(0,3) == "REG" || paramText.substr(0,5) == "UNREG" || paramText.substr(0,8) == "show all" || paramText.substr(0,5) == "ALARM" || paramText.substr(0,3) == "LOG")
				{
					syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i",log_prefix,dn, name, actionParamType);
					syslog(LOG_INFO, "%s MO::maf_action(): Control commands entered: %s",log_prefix, paramText.c_str());
					retValue = testComponentControl(paramText);
					syslog(LOG_INFO, "%s MO::maf_action() returning %i",log_prefix, retValue);
					delete []cont_parameters;
					return retValue;
				}
			}
		}

		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			paramList += cont_parameters[i]->values->value.theString;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());

		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT8:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.i8);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT16:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.i16);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT32:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.i32);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_INT64:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%li", cont_parameters[i]->values->value.i64);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT8:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.u8);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT16:

		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.u16);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT32:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.u32);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_UINT64:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%li", cont_parameters[i]->values->value.u64);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_DECIMAL64:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%f", cont_parameters[i]->values->value.decimal64 );
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	case ComOamSpiMoAttributeType_3_BOOL:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%i", cont_parameters[i]->values->value.theBool);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;
	case ComOamSpiMoAttributeType_3_ENUM:
		for (int i=0; cont_parameters[i]!= NULL; i++)
		{
			char charBuffer[500];
			sprintf(charBuffer,"%ld", cont_parameters[i]->values->value.theEnum);
			paramList += charBuffer;
			paramList += " ";
		}
		syslog(LOG_INFO, "%s MO::maf_action(): dn %s name %s type %i input values: %s",log_prefix,dn, name, actionParamType,paramList.c_str());
		delete []cont_parameters;
		return ComOk;

	default:
		syslog(LOG_INFO, "%s MO::maf_action() type not found, returning ComFailure",log_prefix);
		std::string nbi_message = "@ComNbi@ Error: Unexpected action method callback received by ";
		nbi_message += component_name;

		_maf_threadContextIf->addMessage(ThreadContextMsgNbi_2, nbi_message.c_str());

		delete []cont_parameters;
		return ComFailure;
	}
}


ComReturnT maf_finalizeMoIterator(ComOamSpiMoIteratorHandle_3T itHandle)
{
	syslog(LOG_INFO, "%s MO::maf_finalizeMoIterator() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}


ComReturnT maf_existsMo(ComOamSpiTransactionHandleT txHandle,
					const char * dn,
					bool * result)
{
	syslog(LOG_INFO, "%s MO::maf_existsMo() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}


ComReturnT maf_countMoChildren(ComOamSpiTransactionHandleT txHandle,
							const char * dn,
							const char * className,
							uint64_t * result)
{
	syslog(LOG_INFO, "%s MO::maf_countMoChildren() entered", log_prefix);
	// TODO: a place holder only. to be implemented
	return ComOk;
}



/****************************************************************************************************************
 ***************************************************************************************************************
 ***************************************************************************************************************
 *
 *  ComOamSpiTransactionalResource_2T interface functions
 *
 ***************************************************************************************************************
 ***************************************************************************************************************
 ***************************************************************************************************************/

ComReturnT join (ComOamSpiTransactionHandleT txHandle)
{
	syslog(LOG_INFO, "%s TR::join() entered",log_prefix);
	syslog(LOG_INFO, "%s TR::join(): txHandle %lu",log_prefix,txHandle);
	syslog(LOG_INFO, "%s TR::registerParticipant(): txHandle %lu",log_prefix,txHandle);

	ComReturnT returnValue = _transactionIf->registerParticipant(txHandle, &transactionalResourceIf);

	// If retValue not ComOk then return
	if(returnValue != ComOk)
	{
		syslog(LOG_INFO, "%s TR::join(): returning (%i)",log_prefix, returnValue);
		return returnValue;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	returnValue = testConfig->getReturnValue("join");
	// If retValue not ComOk then write return value to syslog
	if(returnValue != ComOk)
	{
		// test for HS99358 fix
		// if returnValue of join() is not ComOk, this will give same condition as saImmOmCcbObjectCreate() returning != SA_AIS_OK
		// and to confirm this ccb is aborted afterwards, check for hs99358_ccb_has_been_aborted flag_mr20275
		// If it has been overridden, return ComOk
		hs99358_current_txhandle_id = txHandle;
		if (hs99358_bad_ccb_has_been_aborted != true)
		{
			setAllReturnValuesToFail();
			syslog(LOG_INFO, "%s TR::join(): returning (%i)",log_prefix, returnValue);
		}
		else return ComOk;
	}
	return returnValue;
}

ComReturnT prepare (ComOamSpiTransactionHandleT txHandle)
{
	syslog(LOG_INFO, "%s TR::prepare() entered",log_prefix);
	syslog(LOG_INFO, "%s TR::prepare(): txHandle %lu",log_prefix,txHandle);

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT returnValue = testConfig->getReturnValue("prepare");
	// If retValue not ComOk then write return value to syslog
	if(returnValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s TR::prepare(): returning (%i)",log_prefix, returnValue);
	}
	return returnValue;
}

ComReturnT commit (ComOamSpiTransactionHandleT txHandle)
{
	syslog(LOG_INFO, "%s TR::commit() entered",log_prefix);
	syslog(LOG_INFO, "%s TR::commit(): txHandle %lu",log_prefix,txHandle);
	///MR20275,
	syslog(LOG_INFO, "%s TR::commit() %d",log_prefix,validate_mr20275);
	if (!validate_mr20275)
	{
		syslog(LOG_INFO, "%s TR::commit(): returning ComFailure",log_prefix);
		std::string errorText = "@ComNbi@Error: commit failed. MR-20275 Validate failed";
		_maf_threadContextIf->addMessage(ThreadContextMsgNbi_2, errorText.c_str());
		return ComFailure;
	}
	else
	{
		syslog(LOG_INFO, "%s TR::commit(): returning ComOk",log_prefix);
		return ComOk;
	}
	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT returnValue = testConfig->getReturnValue("commit");
	// If retValue not ComOk then write return value to syslog
	if(returnValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s TR::commit(): returning (%i)",log_prefix, returnValue);
	}
	return returnValue;
}

ComReturnT abort (ComOamSpiTransactionHandleT txHandle)
{
	syslog(LOG_INFO, "%s TR::abort() entered",log_prefix);
	syslog(LOG_INFO, "%s TR::abort(): txHandle %lu",log_prefix,txHandle);

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	 // HS99358 fix - detect when a bad CCB has been aborted
	 if (hs99358_current_txhandle_id != 0) {
		if(hs99358_current_txhandle_id == txHandle) {
			hs99358_bad_ccb_has_been_aborted = true;
		}
	}
	ComReturnT returnValue = testConfig->getReturnValue("abort");
	// If retValue not ComOk then write return value to syslog
	if(returnValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s TR::abort(): returning (%i)",log_prefix, returnValue);
	}
	return returnValue;
}

ComReturnT finish (ComOamSpiTransactionHandleT txHandle)
{
	syslog(LOG_INFO, "%s TR::finish() entered",log_prefix);
	syslog(LOG_INFO, "%s TR::finish(): txHandle %lu",log_prefix,txHandle);

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT returnValue = testConfig->getReturnValue("finish");

	if(returnValue != ComOk)
	{
		setAllReturnValuesToFail();
		syslog(LOG_INFO, "%s TR::finish(): returning (%i)",log_prefix, returnValue);
	}
	else
	{
		// release all memory allocated for containers by test component during the specific transaction (txHandle)
		freeDeleteList(txHandle);
		syslog(LOG_INFO, "%s TR::finish(): returning ComOk",log_prefix);
	}
	return returnValue;
}

ComReturnT validate(ComOamSpiTransactionHandleT txHandle, bool *result)
{
	syslog(LOG_INFO, "%s TR::validate() entered",log_prefix);
	syslog(LOG_INFO, "%s TR::validate(): txHandle %lu",log_prefix,txHandle);
	//Mr20275
	syslog(LOG_INFO, "%s TR::validate() %d",log_prefix,validate_mr20275);
	if (!validate_mr20275)
        {
                syslog(LOG_INFO, "%s TR::validate(): returning ComFailure",log_prefix);
                return ComFailure;
        }
        else
        {
                syslog(LOG_INFO, "%s TR::validate(): returning ComOk",log_prefix);
                return ComOk;
        }

	/* If a preconfigured return value is already set, then return that value instead of ComOk.
	 * That means it is:
	 *                    -an unexpected callback
	 *                    -or a negative testcase where we especially set the return value other then ComOk
	 */
	ComReturnT returnValue = testConfig->getReturnValue("validate");

	if(returnValue != ComOk)
	{
		setAllReturnValuesToFail();
		*result=false;
		syslog(LOG_INFO, "%s TR::validate(): returning (%i)",log_prefix, returnValue);
	}
	else
	{
		// release all memory allocated for containers by test component during the specific transaction (txHandle)
		freeDeleteList(txHandle);
		*result=true;
		syslog(LOG_INFO, "%s TR::validate(): returning ComOk",log_prefix);
	}
	return returnValue;
}


ComReturnT registerAsOIToOamSA(std::string DN_or_MOC, OIaction registration, std::string permission)
{
	syslog(LOG_INFO, "%s ENTER function registerAsOIToOamSA",log_prefix);
	ComReturnT ret;
	std::string cleaned_DN_or_MOC;
	switch(registration)
	{
	case REGISTER_DN_INSTANCE:
		syslog(LOG_INFO, "%s ENTER REGISTER_DN_INSTANCE in function registerAsOIToOamSA",log_prefix);
		ret = _registerObjectImplementerIf->registerDn( (ComMgmtSpiInterface_1T&) managedObjectIf,
				(ComMgmtSpiInterface_1T&) transactionalResourceIf,
				DN_or_MOC.c_str(), COM_OAM_REGISTER_OI_INSTANCE);

//		syslog(LOG_INFO, "%s in registerAsOIToOamSA _registerObjectImplementerIf->registerDn, string = %s returns %d", log_prefix, DN_or_MOC.c_str(), ret);

		if(ret == ComOk)
		{
			// Adding the current DN and permission to testConfig
			testConfig->addRegistration(DN_or_MOC, permission);
		}
		return ret;

	case REGISTER_CLASS:
		syslog(LOG_INFO, "%s ENTER REGISTER_CLASS in function registerAsOIToOamSA",log_prefix);
		// class registration needs special action: remove exclusive key attributes from MOC
		cleaned_DN_or_MOC = removeKeyAttributes(DN_or_MOC);
		ret = _registerObjectImplementerIf->registerClass( (ComMgmtSpiInterface_1T&) managedObjectIf,
				(ComMgmtSpiInterface_1T&) transactionalResourceIf,
				cleaned_DN_or_MOC.c_str());
		if(ret == ComOk)
		{
			// Adding the current MOC and permission to testConfig
			testConfig->addRegistration(DN_or_MOC, permission);
		}
		return ret;

	case UNREGISTER_DN:
		syslog(LOG_INFO, "%s ENTER UNREGISTER_DN in function registerAsOIToOamSA",log_prefix);
		ret = _registerObjectImplementerIf->unregisterDn( (ComMgmtSpiInterface_1T&) managedObjectIf,
				(ComMgmtSpiInterface_1T&) transactionalResourceIf,
				DN_or_MOC.c_str());
		if(ret == ComOk)
		{
			// Delete the current DN from testConfig
			testConfig->deleteRegistration(DN_or_MOC);
		}
		return ret;

	case UNREGISTER_CLASS:
		syslog(LOG_INFO, "%s ENTER UNREGISTER_CLASS in function registerAsOIToOamSA",log_prefix);
		// class registration needs special action: remove exclusive key attributes from MOC
		cleaned_DN_or_MOC = removeKeyAttributes(DN_or_MOC);
		ret = _registerObjectImplementerIf->unregisterClass( (ComMgmtSpiInterface_1T&) managedObjectIf,
				(ComMgmtSpiInterface_1T&) transactionalResourceIf,
				cleaned_DN_or_MOC.c_str());
		if(ret == ComOk)
		{
			// Delete the current MOC from testConfig
			testConfig->deleteRegistration(DN_or_MOC);
		}
		return ret;

	default:
		syslog(LOG_INFO, "%s ENTER default case ComInvalidArgument in function registerAsOIToOamSA",log_prefix);
		return ComInvalidArgument;
	}
}

ComReturnT loadMocOrDnConfig(std::string DN_or_MOC, std::string DN_PERMISSION)
{
	OIaction regType;
	// If registration text starts with "/" than it is a CLASS registration, otherwise it is a DN registration
	if(DN_or_MOC[0] == '/')
		{
			regType = REGISTER_CLASS;
		}
		else
		{
			regType = REGISTER_DN_INSTANCE;
		}

	#if defined(UNREGISTER_ALL)
	{
		if(regType == REGISTER_DN_INSTANCE)
		{
			regType = UNREGISTER_DN;
		}
		else if(regType == REGISTER_CLASS)
		{
			regType = UNREGISTER_CLASS;
		}
	}
	#else
	{
		if(regType == REGISTER_DN_INSTANCE)
		{
			syslog(LOG_INFO, "%s loadMocOrDnConfig(): registerAsOIToOamSA: DN: %s Permission: %s",log_prefix, DN_or_MOC.c_str(), DN_PERMISSION.c_str());
		}
		else if(regType == REGISTER_CLASS)
		{
			syslog(LOG_INFO, "%s loadMocOrDnConfig(): registerAsOIToOamSA: MOC: %s Permission: %s",log_prefix, DN_or_MOC.c_str(), DN_PERMISSION.c_str());
		}
	}
	#endif
	return registerAsOIToOamSA(DN_or_MOC, regType, DN_PERMISSION);
}

void loadAttributeConfig(std::string ATTR, ComOamSpiMoAttributeType_3T ATTR_TYPE, std::string ATTR_VALUE)
{
	syslog(LOG_INFO, "%s loadAttributeConfig(): attribute: %s type: %i, value: %s",log_prefix, ATTR.c_str(), ATTR_TYPE, ATTR_VALUE.c_str());
	// Fill out the AttributeStruct with attribute type and attribute value which comes from "defines.h"
	Attribute AttributeStruct;
	AttributeStruct.attrType = ATTR_TYPE;
	AttributeStruct.attrValue = ATTR_VALUE;
	// Adding key-value pair to "attribute_Map":
	//       -key: the DN of the attribute
	//       -value: AttributeStruct (type and value of attribute)
	testConfig->addAttribute(ATTR, AttributeStruct);
}

void loadActionTestConfig(std::string ACTION, ComOamSpiMoAttributeType_3T ACTION_TYPE)
{
	syslog(LOG_INFO, "%s loadActionTestConfig(): Action: %s type: %i",log_prefix, ACTION.c_str(), ACTION_TYPE);
	// Adding the current Action's DN and type (read out from "defines.h") to testConfig
	testConfig->addAction(ACTION, ACTION_TYPE);
}

/*
 * The component starts providing service.
 */
extern "C" ComReturnT start(ComStateChangeReasonT reason)
{
	syslog(LOG_INFO, "%s start(): Starting to provide service.. ",log_prefix);
	ComReturnT ret;
	// Get RegisterOI interface
	ret = _portal->getInterface(ComOamSpiRegisterObjectImplementer_2Id, (ComMgmtSpiInterface_1T**) &_registerObjectImplementerIf);
	if (ret != ComOk)
	{
		syslog(LOG_ERR,"%s start(): failed(%i) to get '%s' interface",log_prefix, ret, ComOamSpiRegisterObjectImplementer_2Id.interfaceName);
		return ret;
	}
	else if (!_registerObjectImplementerIf)
	{
		syslog(LOG_ERR,"%s start(): failed to get '%s' interface, NULL returned",log_prefix, ComOamSpiRegisterObjectImplementer_2Id.interfaceName);
		return ComFailure;
	}

	// Get Thread Context interface
	ret = _portal->getInterface(ComMgmtSpiThreadContext_2Id, (ComMgmtSpiInterface_1T**) &_threadContextIf);
	if (ComOk != ret)
	{
		syslog(LOG_ERR,"%s start(): failed(%i) to get '%s' interface",log_prefix,ret, ComMgmtSpiThreadContext_2Id.interfaceName);
		return ret;
	}
	else if (!_threadContextIf)
	{
		syslog(LOG_ERR,"%s start(): failed to get '%s' interface, NULL returned",log_prefix, ComMgmtSpiThreadContext_2Id.interfaceName);
		return ComFailure;
	}

	// Get Transactional interface
	ret = _portal->getInterface(ComOamSpiTransaction_2Id, (ComMgmtSpiInterface_1T**) &_transactionIf);
	if (ret != ComOk)
	{
		syslog(LOG_ERR,"%s start(): failed(%i) to get ComOamSpiTransaction_2T interface",log_prefix,ret);
		return ret;
	}
	else if (!_transactionIf)
	{
		syslog(LOG_ERR,"%s start(): failed to get '%s' interface, NULL returned",log_prefix, ComOamSpiTransaction_2Id.interfaceName);
		return ComFailure;
	}

	// Get Event Router interface
#if defined (ALARMS) || defined (ALARMS4)
	{
		// Get interface
		syslog(LOG_INFO, "%s start(): Get Event Router Interface",log_prefix);
		MafReturnT ret_MAF = _portal_MAF->getInterface(MafOamSpiEventService_1Id, (MafMgmtSpiInterface_1T**) &_eventRouter);
		if (ret_MAF != MafOk)
		{
			syslog(LOG_ERR,"%s start(): failed(%i) to get ComOamSpiEventService_1T interface",log_prefix,ret_MAF);
			return ComFailure;
		}
		else if (!_eventRouter)
		{
			syslog(LOG_ERR,"%s start(): failed to get '%s' interface, NULL returned",log_prefix, ComOamSpiEventService_1Id.interfaceName);
			return ComFailure;
		}
	}
#endif

#if defined (LOGSERVICE)
	{
		// Get interface
		ComReturnT ret;
		ret = _portal->getInterface(ComMwSpiLog_1Id, (ComMgmtSpiInterface_1T**) &_logServiceIf);

		if (ret != ComOk)
		{
			syslog(LOG_ERR,"%s start(): failed(%i) to get %s interface",log_prefix,ret,ComMwSpiLog_1Id.interfaceName);
			return ret;
		}
		else if (!_logServiceIf)
		{
			syslog(LOG_ERR,"%s start(): failed to get '%s' interface, NULL returned",log_prefix, ComMwSpiLog_1Id.interfaceName);
			return ComFailure;
		}
	}
#endif
#if defined (TRACESERVICE)
	{
		// Get interface
		ComReturnT ret;
		ret = _portal->getInterface(ComMwSpiTrace_1Id, (ComMgmtSpiInterface_1T**) &_traceServiceIf);

		if (ret != ComOk)
		{
			syslog(LOG_ERR,"%s start(): failed(%i) to get %s interface",log_prefix,ret,ComMwSpiTrace_1Id.interfaceName);
			return ret;
		}
		else if (!_traceServiceIf)
		{
			syslog(LOG_ERR,"%s start(): failed to get '%s' interface, NULL returned",log_prefix, ComMwSpiTrace_1Id.interfaceName);
			return ComFailure;
		}
	}
#endif
	syslog(LOG_INFO, "%s start(): Interfaces gathered from the portal successfully",log_prefix);

#if defined (ALARMS) || defined (ALARMS4)
	// Register producer
	syslog(LOG_INFO, "%s start(): registerProducer",log_prefix);
	MafReturnT ret_MAF = _eventRouter->registerProducer(&producer_if, &producer_handle);
	if (ret_MAF != MafOk)
	{
		syslog(LOG_ERR,"%s start(): failed to registerProducer (%d)",log_prefix, ret_MAF);
		return ComFailure;
	}
	syslog(LOG_INFO, "%s start(): producer_handle: (%lu)",log_prefix, producer_handle);
#endif
#if defined (ALARMS)
	// Register event type
	syslog(LOG_INFO, "%s start(): addProducerEvent",log_prefix);
	ret_MAF = _eventRouter->addProducerEvent(producer_handle, MafOamSpiNotificationFmEventComponent_3);
	if (ret_MAF != MafOk)
	{
		syslog(LOG_ERR,"%s start(): failed to addProducerEvent (%d)",log_prefix, ret_MAF);
		return ComFailure;
	}
#endif
#if defined (ALARMS4)
	// Register event type
	syslog(LOG_INFO, "%s start4(): addProducerEvent",log_prefix);
	ret_MAF = _eventRouter->addProducerEvent(producer_handle, MafOamSpiNotificationFmEventComponent_4);
	if (ret_MAF != MafOk)
	{
		syslog(LOG_ERR,"%s start4(): failed to addProducerEvent (%d)",log_prefix, ret_MAF);
		return ComFailure;
	}
#endif
	/*
	 *  At this point we allocate memory for "testConfig"
	 *  this pointer points to the object which handles all the test configurations of the test component
	 */
	testConfig = new Test_Config();

	// Preconfigure return values
#if defined (returnValueConfig)
	{
		// Create a structure of return values
		functionReturnValues returnValues;
		// By default all preconfigured return values are ComOk
		// Note that it does not mean that the functions will return ComOk by default.
		returnValues.createMo = ComOk;
		returnValues.deleteMo = ComOk;
		returnValues.setMo    = ComOk;
		returnValues.getMo    = ComOk;
		returnValues.action   = ComOk;
		returnValues.join     = ComOk;
		returnValues.prepare  = ComOk;
		returnValues.commit   = ComOk;
		returnValues.finish   = ComOk;
		returnValues.abort    = ComOk;
		returnValues.validate = ComOk;
		// Some of the preconfigured return values can be overwritten here. It depends on what is configured in "defines.h"
		returnValueConfig;
		syslog(LOG_INFO, "%s start(): preconfigured return values: createMo: (%i) deleteMo: (%i) setMo: (%i) getMo: (%i) action: (%i) join: (%i) prepare: (%i) commit: (%i) finish: (%i) abort: (%i)",log_prefix, returnValues.createMo, returnValues.deleteMo, returnValues.setMo, returnValues.getMo, returnValues.action, returnValues.join, returnValues.prepare, returnValues.commit, returnValues.finish, returnValues.abort);
		testConfig->setReturnValues(returnValues);
	}
#endif
	// testOI Registration to ComSA
#if defined(REG1) & defined(REG1_PERMISSION)
	{
		ret = loadMocOrDnConfig(REG1, REG1_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s start(): failed(%i) to loadMocOrDnConfig(REG1, REG1_PERMISSION)",log_prefix,ret);
			return ret;
		}
	}
#endif
#if defined(REG2) & defined(REG2_PERMISSION)
	{
		ret = loadMocOrDnConfig(REG2, REG2_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s start(): failed(%i) to loadMocOrDnConfig(REG2, REG2_PERMISSION)",log_prefix,ret);
			return ret;
		}
	}
#endif
#if defined(REG3) & defined(REG3_PERMISSION)
	{
		ret = loadMocOrDnConfig(REG3, REG3_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s start(): failed(%i) to loadMocOrDnConfig(REG3, REG3_PERMISSION)",log_prefix,ret);
			return ret;
		}
	}
#endif
#if defined(REG4) & defined(REG4_PERMISSION)
	{
		ret = loadMocOrDnConfig(REG4, REG4_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s start(): failed(%i) to loadMocOrDnConfig(REG4, REG4_PERMISSION)",log_prefix,ret);
			return ret;
		}
	}
#endif
#if defined(REG5) & defined(REG5_PERMISSION)
	{
		ret = loadMocOrDnConfig(REG5, REG5_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s start(): failed(%i) to loadMocOrDnConfig(REG5, REG5_PERMISSION)",log_prefix,ret);
			return ret;
		}
	}
#endif

#if defined(ACTION1) & defined(ACTION1_TYPE)
	{
		loadActionTestConfig(ACTION1, ACTION1_TYPE);
	}
#endif
	/*#if defined(DN1_UNREGISTER) & defined(DN1_UNREGISTER_VALUE)
		{
			syslog(LOG_INFO, "%s start(): registerAsOIToOamSA: You can unregister: %s by calling action-method %s",DN1_UNREGISTER,DN1_UNREGISTER_VALUE);
			unregisterParams.methodDN = DN1_UNREGISTER;
			unregisterParams.unregDN = DN1_UNREGISTER;
		}
	#endif*/
#if defined(ATTR1) & defined(ATTR1_TYPE) & defined(ATTR1_VALUE)
	{
		loadAttributeConfig(ATTR1, ATTR1_TYPE, ATTR1_VALUE);
	}
#endif
#if defined(ATTR2) & defined(ATTR2_TYPE) & defined(ATTR2_VALUE)
	{
		loadAttributeConfig(ATTR2, ATTR2_TYPE, ATTR2_VALUE);
	}
#endif
#if defined(ATTR3) & defined(ATTR3_TYPE) & defined(ATTR3_VALUE)
	{
		loadAttributeConfig(ATTR3, ATTR3_TYPE, ATTR3_VALUE);
	}
#endif
#if defined(ATTR4) & defined(ATTR4_TYPE) & defined(ATTR4_VALUE)
	{
		loadAttributeConfig(ATTR4, ATTR4_TYPE, ATTR4_VALUE);
	}
#endif
#if defined(ATTR5) & defined(ATTR5_TYPE) & defined(ATTR5_VALUE)
	{
		loadAttributeConfig(ATTR5, ATTR5_TYPE, ATTR5_VALUE);
	}
#endif
#if defined(ATTR6) & defined(ATTR6_TYPE) & defined(ATTR6_VALUE)
	{
		loadAttributeConfig(ATTR6, ATTR6_TYPE, ATTR6_VALUE);
	}
#endif
#if defined(ATTR7) & defined(ATTR7_TYPE) & defined(ATTR7_VALUE)
	{
		loadAttributeConfig(ATTR7, ATTR7_TYPE, ATTR7_VALUE);
	}
#endif
#if defined(ATTR8) & defined(ATTR8_TYPE) & defined(ATTR8_VALUE)
	{
		loadAttributeConfig(ATTR8, ATTR8_TYPE, ATTR8_VALUE);
	}
#endif
#if defined(ATTR9) & defined(ATTR9_TYPE) & defined(ATTR9_VALUE)
	{
		loadAttributeConfig(ATTR9, ATTR9_TYPE, ATTR9_VALUE);
	}
#endif
#if defined(ATTR10) & defined(ATTR10_TYPE) & defined(ATTR10_VALUE)
	{
		loadAttributeConfig(ATTR10, ATTR10_TYPE, ATTR10_VALUE);
	}
#endif
#if defined(ATTR11) & defined(ATTR11_TYPE) & defined(ATTR11_VALUE)
	{
		loadAttributeConfig(ATTR11, ATTR11_TYPE, ATTR11_VALUE);
	}
#endif
#if defined(ATTR12) & defined(ATTR12_TYPE) & defined(ATTR12_VALUE)
	{
		loadAttributeConfig(ATTR12, ATTR12_TYPE, ATTR12_VALUE);
	}
#endif
#if defined(STARTUP_LOGWRITE)
	{
		startupLogWriteEnabled = true;
	}
#endif
#if defined(STARTUP_LOGSPAM)
	{
		startupLogSpamEnabled = true;
	}
#endif
#if defined(STARTUP_TRACESPAM)
	{
		startupTraceSpamEnabled = true;
	}
#endif
#if defined(NR_OF_LOGSPAMS)
	{
		nrOfLogSpams = NR_OF_LOGSPAMS;
	}
#endif
#if defined(NR_OF_TRACESPAMS)
	{
		nrOfTraceSpams = NR_OF_TRACESPAMS;
	}
#endif
#if defined(STARTUP_LOGWRITE_DELAY)
	{
		startupLogWriteDelay = STARTUP_LOGWRITE_DELAY;
	}
#endif
#if defined(STARTUP_TRACEWRITE_DELAY)
	{
		startupTraceWriteDelay = STARTUP_TRACEWRITE_DELAY;
	}
#endif
	/*
	 * Print all internal data to syslog that stored by the testOi (testConfig)
	 */
	testConfig->printAll();

	// Starting startup-logWrite thread
	if(startupLogWriteEnabled)
	{
		if ((PthreadResult = pthread_create(&OpenThreadId,NULL, &startupLogWriteThread, NULL)) != 0)
		{
			syslog(LOG_INFO, "%s start(): pthread_create failed PthreadResult (%d)",log_prefix,PthreadResult);
		}
		else if (pthread_detach(OpenThreadId) != 0)
		{
			syslog(LOG_INFO, "%s start(): failed to detach thread",log_prefix);
		}
	}
	// Starting startup-logspam thread
	if(startupLogSpamEnabled)
	{
		if ((PthreadResult = pthread_create(&OpenThreadId,NULL, &startupLogSpamThread, NULL)) != 0)
		{
			syslog(LOG_INFO, "%s start(): pthread_create failed PthreadResult (%d)",log_prefix,PthreadResult);
		}
		else if (pthread_detach(OpenThreadId) != 0)
		{
			syslog(LOG_INFO, "%s start(): failed to detach thread",log_prefix);
		}
	}
	// Starting startup-traceSpam thread
	if(startupTraceSpamEnabled)
	{
		if ((PthreadResult = pthread_create(&OpenThreadId,NULL, &startupTraceSpamThread, NULL)) != 0)
		{
			syslog(LOG_INFO, "%s start(): pthread_create failed PthreadResult (%d)",log_prefix,PthreadResult);
		}
		else if (pthread_detach(OpenThreadId) != 0)
		{
			syslog(LOG_INFO, "%s start(): failed to detach thread",log_prefix);
		}
	}
	syslog(LOG_INFO, "%s start(): returning ComOk",log_prefix);
	return ComOk;
}

/*
 * The component stops providing service.
 */
extern "C" ComReturnT stop(ComStateChangeReasonT reason)
{
	syslog(LOG_INFO, "%s stop() called (%i), returning ComOk",log_prefix, reason);
	return ComOk;
}

/*
 * All the necessary values are set by the component.
 * This example component have no interfaces or
 * dependencies. The arrays are set to empty.
 */
void initComponent()
{
	syslog(LOG_INFO, "%s initComponent()",log_prefix);
	component.base.componentName = component_name;
	component.base.interfaceName = "ComMgmtSpiComponent";
	component.base.interfaceVersion = "1";

	dependencyArray[0] = 0;

	managedObjectIf.base.componentName    = component.base.componentName;
	managedObjectIf.base.interfaceName    = ComOamSpiManagedObject_3Id.interfaceName;
	managedObjectIf.base.interfaceVersion = ComOamSpiManagedObject_3Id.interfaceVersion;

	managedObjectIf.setMoAttribute     = setMoAttribute;
	managedObjectIf.getMoAttribute     = getMoAttribute;
	managedObjectIf.getMoAttributes    = getMoAttributes;
	managedObjectIf.newMoIterator      = newMoIterator;
	managedObjectIf.nextMo             = nextMo;
	managedObjectIf.createMo           = createMo;
	managedObjectIf.deleteMo           = deleteMo;
	managedObjectIf.action             = action;
	managedObjectIf.finalizeMoIterator = finalizeMoIterator;
	managedObjectIf.existsMo           = existsMo;
	managedObjectIf.countMoChildren    = countMoChildren;

	transactionalResourceIf.base.componentName = component.base.componentName;
	transactionalResourceIf.base.interfaceName = ComOamSpiTransactionalResource_1Id.interfaceName;
	transactionalResourceIf.base.interfaceVersion = ComOamSpiTransactionalResource_1Id.interfaceVersion;

	transactionalResourceIf.join    = join;
	transactionalResourceIf.prepare = prepare;
	transactionalResourceIf.commit  = commit;
	transactionalResourceIf.abort   = abort;
	transactionalResourceIf.finish  = finish;
	transactionalResourceIf.validate  = validate;

	interfaceArray[0] = (ComMgmtSpiInterface_1T*)&managedObjectIf;
	interfaceArray[0]->componentName = component.base.componentName;
	interfaceArray[1] = (ComMgmtSpiInterface_1T*)&transactionalResourceIf;
	interfaceArray[1]->componentName = component.base.componentName;
	interfaceArray[2] = 0;

	component.interfaceArray  = interfaceArray;
	component.dependencyArray = dependencyArray;

	component.start = &start;
	component.stop  = &stop;
}



/* The init method must register components. It must
 * be implemented in init because the start of the
 * components is done in two steps. In step one, init,
 * all the components register. In step two, all the
 * components are started in the start order that COM
 * has figured out based on the dependencies that the
 * component has specified. When started, a component
 * can expect all the needed services to be started,
 * and the component can use the interfaces it
 * fetches.
 */
extern "C" ComReturnT comLCMinit(ComMgmtSpiInterfacePortalAccessorT* accessor, const char* config)
{
	syslog(LOG_INFO, "%s comLCMinit(): Component started",log_prefix);
	ComReturnT ret = ComFailure;

	initComponent();

	syslog(LOG_INFO, "%s comLCMinit(): initComponent() finished",log_prefix);

	_portal = (ComMgmtSpiInterfacePortal_1T*)accessor-> getPortal("1");
	assert(_portal);
	_portal_MAF = (MafMgmtSpiInterfacePortal_1T*)accessor-> getPortal("1");
	assert(_portal_MAF);

	ret = _portal->registerComponent(&component);
	if (ret != ComOk) {
		syslog(LOG_ERR,"%s comLCMinit(): failed(%d) to register component",log_prefix,ret);
		return ret;
	}

	syslog(LOG_INFO, "%s comLCMinit(): Component registered, returning ComOk",log_prefix);

	return ComOk;
}

/*
 * The component unregisters itself.
 */
extern "C" void comLCMterminate()
{
	syslog(LOG_INFO, "%s comLCMterminate(): Unregistering component..",log_prefix);
	_portal->unregisterComponent(&component);
}


/*
** SDP1694  - support MAF SPI
*/

extern "C" MafReturnT maf_start(MafStateChangeReasonT reason)
{
	syslog(LOG_INFO, "%s maf_start(): Starting to provide service.. ",log_prefix);
	ComReturnT ret;
	MafReturnT maf_return;
	// Get RegisterOI interface
	ret = _portal->getInterface(ComOamSpiRegisterObjectImplementer_2Id, (ComMgmtSpiInterface_1T**) &_registerObjectImplementerIf);
	if (ret != ComOk)
	{
		syslog(LOG_ERR,"%s maf_start(): failed(%i) to get '%s' interface",log_prefix, ret, ComOamSpiRegisterObjectImplementer_2Id.interfaceName);
		return (MafReturnT)ret;
	}
	else if (!_registerObjectImplementerIf)
	{
		syslog(LOG_ERR,"%s maf_start(): failed to get '%s' interface, NULL returned",log_prefix, ComOamSpiRegisterObjectImplementer_2Id.interfaceName);
		return MafFailure;
	}

	// Get Thread Context interface
	maf_return = _portal_MAF->getInterface(MafMgmtSpiThreadContext_2Id, (MafMgmtSpiInterface_1T**) &_maf_threadContextIf);
	if (MafOk != maf_return)
	{
		syslog(LOG_ERR,"%s maf_start(): failed(%i) to get '%s' interface",log_prefix,ret,  MafMgmtSpiThreadContext_2Id.interfaceName);
		return maf_return;
	}
	else if (!_maf_threadContextIf)
	{
		syslog(LOG_ERR,"%s maf_start(): failed to get '%s' interface, NULL returned",log_prefix, MafMgmtSpiThreadContext_2Id.interfaceName);
		return MafFailure;
	}

	// Get Transactional interface
	ret = _portal->getInterface(ComOamSpiTransaction_2Id, (ComMgmtSpiInterface_1T**) &_transactionIf);
	if (ret != ComOk)
	{
		syslog(LOG_ERR,"%s maf_start(): failed(%i) to get ComOamSpiTransaction_2T interface",log_prefix,ret);
		return(MafReturnT) ret;
	}
	else if (!_transactionIf)
	{
		syslog(LOG_ERR,"%s maf_start(): failed to get '%s' interface, NULL returned",log_prefix, ComOamSpiTransaction_2Id.interfaceName);
		return MafFailure;
	}

	// Get Event Router interface
#if defined (ALARMS) || defined (CM_EVENT_CONSUMER) || defined (ALARMS4)
	{
		// Get interface
		syslog(LOG_INFO,"%s maf_start(): Get Event Router interface",log_prefix);
		MafReturnT ret_MAF = _portal_MAF->getInterface(MafOamSpiEventService_1Id, (MafMgmtSpiInterface_1T**) &_eventRouter);
		if (ret_MAF != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to get MafOamSpiEventService_1T interface",log_prefix,ret_MAF);
			return MafFailure;
		}
		else if (!_eventRouter)
		{
			syslog(LOG_ERR,"%s maf_start(): failed to get '%s' interface, NULL returned",log_prefix, MafOamSpiEventService_1Id.interfaceName);
			return MafFailure;
		}
	}
#endif

#if defined (LOGSERVICE)
	{
		// Get interface
		MafReturnT ret;
		ret = _portal_MAF->getInterface(MafMwSpiLog_1Id, (MafMgmtSpiInterface_1T**) &_logServiceIf);

		if (ret != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to get %s interface",log_prefix,ret,MafMwSpiLog_1Id.interfaceName);
			return ret;
		}
		else if (!_logServiceIf)
		{
			syslog(LOG_ERR,"%s maf_start(): failed to get '%s' interface, NULL returned",log_prefix, MafMwSpiLog_1Id.interfaceName);
			return MafFailure;
		}
	}
#endif

#if defined (TRACESERVICE)
	{
		// Get interface
		MafReturnT ret;
		ret = _portal_MAF->getInterface(MafMwSpiTrace_1Id, (MafMgmtSpiInterface_1T**) &_traceServiceIf);

		if (ret != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to get %s interface",log_prefix,ret,MafMwSpiTrace_1Id.interfaceName);
			return ret;
		}
		else if (!_traceServiceIf)
		{
			syslog(LOG_ERR,"%s maf_start(): failed to get '%s' interface, NULL returned",log_prefix, MafMwSpiTrace_1Id.interfaceName);
			return MafFailure;
		}
	}
#endif
	syslog(LOG_INFO, "%s maf_start(): Interfaces gathered from the portal successfully",log_prefix);

#if defined (ALARMS) || defined (ALARMS4)
		// Register producer
		syslog(LOG_INFO, "%s maf_start(): registerProducer",log_prefix);
		MafReturnT ret_MAF = _eventRouter->registerProducer(&producer_if, &producer_handle);
		if (ret_MAF != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start(): failed to registerProducer (%d)",log_prefix, ret_MAF);
			return MafFailure;
		}
		syslog(LOG_INFO, "%s maf_start(): producer_handle: (%lu)",log_prefix, producer_handle);
#endif
#if defined (ALARMS)
		// Register event type
		syslog(LOG_INFO, "%s maf_start(): addProducerEvent",log_prefix);
		ret_MAF = _eventRouter->addProducerEvent(producer_handle, MafOamSpiNotificationFmEventComponent_3);
		if (ret_MAF != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start(): failed to addProducerEvent (%d)",log_prefix, ret_MAF);
			return MafFailure;
		}
#endif
#if defined (ALARMS4)
		// Register event type
		syslog(LOG_INFO, "%s maf_start4(): addProducerEvent",log_prefix);
		ret_MAF = _eventRouter->addProducerEvent(producer_handle, MafOamSpiNotificationFmEventComponent_4);
		if (ret_MAF != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start4(): failed to addProducerEvent (%d)",log_prefix, ret_MAF);
			return MafFailure;
		}
#endif

#if defined (CM_EVENT_CONSUMER)
	{
		// Register producer
		MafReturnT ret_MAF;
		syslog(LOG_INFO, "%s maf_start(): registerProducer",log_prefix);
		ret_MAF = _eventRouter->registerConsumer((MafOamSpiEventConsumer_1T *)&consumer_if,	(MafOamSpiEventConsumerHandleT *)&consumer_handle);
		if (ret_MAF != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start(): failed to registerConsumer (%d)",log_prefix, ret_MAF);
			return MafFailure;
		}
		syslog(LOG_INFO, "%s maf_start(): consumer_handle: (%lu)",log_prefix, consumer_handle);

		// Load the filter expressions from the config file
		std::string configFile =  component_name;
		configFile = "/home/" + configFile;
		configFile += ".cfg";
		configListT cmEventFilterList = readConfigFile(configFile.c_str());

		// Fill in the cmNotificationFilter with the filter expressions
		cmNotificationFilter = new MafNameValuePairT*[cmEventFilterList.size()+1];
		setCmEventFilterArray(cmEventFilterList, cmNotificationFilter);

		// only syslog the contents of the cmNotificationFilter array before sending
		if(cmNotificationFilter != NULL)
		{
			int i = 0;
			for(; cmNotificationFilter[i] != NULL; i++)
			{
				syslog(LOG_ERR,"%s maf_start(): cmNotificationFilter[%d] name(%s) value(%s)",log_prefix, i, cmNotificationFilter[i]->name, cmNotificationFilter[i]->value);
			}
			if(cmNotificationFilter[i] == NULL)
			{
				syslog(LOG_ERR,"%s maf_start(): cmNotificationFilter[%d] = NULL",log_prefix, i);
			}
		}
		else
		{
			syslog(LOG_ERR,"%s maf_start(): cmNotificationFilter = NULL",log_prefix);
		}

		// Add subscription
		syslog(LOG_INFO, "%s maf_start(): addSubscription for CM events with filter(%p)",log_prefix,cmNotificationFilter);
		ret_MAF = _eventRouter->addSubscription((MafOamSpiEventConsumerHandleT)consumer_handle, MafOamSpiCmEvent_Notification_1, (MafNameValuePairT **)cmNotificationFilter);
		if (ret_MAF != MafOk)
		{
			syslog(LOG_ERR,"%s maf_start(): failed to addSubscription (%d)",log_prefix, ret_MAF);
			return MafFailure;
		}
	}
#endif

	/*
	 *  At this point we allocate memory for "testConfig"
	 *  this pointer points to the object which handles all the test configurations of the test component
	 */
	testConfig = new Test_Config();

	// Preconfigure return values
#if defined (returnValueConfig)
	{
		// Create a structure of return values
		functionReturnValues returnValues;
		// By default all preconfigured return values are MafOk
		// Note that it does not mean that the functions will return MafOk by default.
		returnValues.createMo = ComOk;
		returnValues.deleteMo = ComOk;
		returnValues.setMo    = ComOk;
		returnValues.getMo    = ComOk;
		returnValues.action   = ComOk;
		returnValues.join     = ComOk;
		returnValues.prepare  = ComOk;
		returnValues.commit   = ComOk;
		returnValues.finish   = ComOk;
		returnValues.abort    = ComOk;
		returnValues.validate = ComOk;
		// Some of the preconfigured return values can be overwritten here. It depends on what is configured in "defines.h"
		returnValueConfig;
		syslog(LOG_INFO, "%s maf_start(): preconfigured return values: createMo: (%i) deleteMo: (%i) setMo: (%i) getMo: (%i) action: (%i) join: (%i) prepare: (%i) commit: (%i) finish: (%i) abort: (%i)",log_prefix, returnValues.createMo, returnValues.deleteMo, returnValues.setMo, returnValues.getMo, returnValues.action, returnValues.join, returnValues.prepare, returnValues.commit, returnValues.finish, returnValues.abort);
		testConfig->setReturnValues(returnValues);
	}
#endif
	// testOI Registration to ComSA
#if defined(REG1) & defined(REG1_PERMISSION)
	{
		ret = loadMocOrDnConfig(REG1, REG1_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to loadMocOrDnConfig(REG1, REG1_PERMISSION)",log_prefix,ret);
			return (MafReturnT)ret;
		}
	}
#endif
#if defined(REG2) & defined(REG2_PERMISSION)
	{
		ret =  loadMocOrDnConfig(REG2, REG2_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to loadMocOrDnConfig(REG2, REG2_PERMISSION)",log_prefix,ret);
			return (MafReturnT)ret;
		}
	}
#endif
#if defined(REG3) & defined(REG3_PERMISSION)
	{
		ret =  loadMocOrDnConfig(REG3, REG3_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to loadMocOrDnConfig(REG3, REG3_PERMISSION)",log_prefix,ret);
			return (MafReturnT)ret;
		}
	}
#endif
#if defined(REG4) & defined(REG4_PERMISSION)
	{
		ret =  loadMocOrDnConfig(REG4, REG4_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to loadMocOrDnConfig(REG4, REG4_PERMISSION)",log_prefix,ret);
			return (MafReturnT)ret;
		}
	}
#endif
#if defined(REG5) & defined(REG5_PERMISSION)
	{
		ret =  loadMocOrDnConfig(REG5, REG5_PERMISSION);
		if (ret != ComOk) {
			syslog(LOG_ERR,"%s maf_start(): failed(%i) to loadMocOrDnConfig(REG5, REG5_PERMISSION)",log_prefix,ret);
			return (MafReturnT)ret;
		}
	}
#endif

// SDP1694. Only use the MAF_xxxx_TYPE below when the transactional resource SPI has been converted to MAF.
// Do not use for current implementation, it uses COM SPI for transactions.

#if defined(ACTION1) & defined(ACTION1_TYPE)
	{
		loadActionTestConfig(ACTION1, ACTION1_TYPE);
	}
#endif
	/*#if defined(DN1_UNREGISTER) & defined(DN1_UNREGISTER_VALUE)
		{
			syslog(LOG_INFO, "%s maf_start(): registerAsOIToOamSA: You can unregister: %s by calling action-method %s",DN1_UNREGISTER,DN1_UNREGISTER_VALUE);
			unregisterParams.methodDN = DN1_UNREGISTER;
			unregisterParams.unregDN = DN1_UNREGISTER;
		}
	#endif*/
#if defined(ATTR1) & defined(ATTR1_TYPE) & defined(ATTR1_VALUE)
	{
		loadAttributeConfig(ATTR1, ATTR1_TYPE, ATTR1_VALUE);
	}
#endif
#if defined(ATTR2) & defined(ATTR2_TYPE) & defined(ATTR2_VALUE)
	{
		loadAttributeConfig(ATTR2, ATTR2_TYPE, ATTR2_VALUE);
	}
#endif
#if defined(ATTR3) & defined(ATTR3_TYPE) & defined(ATTR3_VALUE)
	{
		loadAttributeConfig(ATTR3, ATTR3_TYPE, ATTR3_VALUE);
	}
#endif
#if defined(ATTR4) & defined(ATTR4_TYPE) & defined(ATTR4_VALUE)
	{
		loadAttributeConfig(ATTR4, ATTR4_TYPE, ATTR4_VALUE);
	}
#endif
#if defined(ATTR5) & defined(ATTR5_TYPE) & defined(ATTR5_VALUE)
	{
		loadAttributeConfig(ATTR5, ATTR5_TYPE, ATTR5_VALUE);
	}
#endif
#if defined(ATTR6) & defined(ATTR6_TYPE) & defined(ATTR6_VALUE)
	{
		loadAttributeConfig(ATTR6, ATTR6_TYPE, ATTR6_VALUE);
	}
#endif
#if defined(ATTR7) & defined(ATTR7_TYPE) & defined(ATTR7_VALUE)
	{
		loadAttributeConfig(ATTR7, ATTR7_TYPE, ATTR7_VALUE);
	}
#endif
#if defined(ATTR8) & defined(ATTR8_TYPE) & defined(ATTR8_VALUE)
	{
		loadAttributeConfig(ATTR8, ATTR8_TYPE, ATTR8_VALUE);
	}
#endif
#if defined(ATTR9) & defined(ATTR9_TYPE) & defined(ATTR9_VALUE)
	{
		loadAttributeConfig(ATTR9, ATTR9_TYPE, ATTR9_VALUE);
	}
#endif
#if defined(ATTR10) & defined(ATTR10_TYPE) & defined(ATTR10_VALUE)
	{
		loadAttributeConfig(ATTR10, ATTR10_TYPE, ATTR10_VALUE);
	}
#endif
#if defined(ATTR11) & defined(ATTR11_TYPE) & defined(ATTR11_VALUE)
	{
		loadAttributeConfig(ATTR11, ATTR11_TYPE, ATTR11_VALUE);
	}
#endif
#if defined(ATTR12) & defined(ATTR12_TYPE) & defined(ATTR12_VALUE)
	{
		loadAttributeConfig(ATTR12, ATTR12_TYPE, ATTR12_VALUE);
	}
#endif
#if defined(STARTUP_LOGWRITE)
	{
		startupLogWriteEnabled = true;
	}
#endif
#if defined(STARTUP_LOGSPAM)
	{
		startupLogSpamEnabled = true;
	}
#endif
#if defined(STARTUP_TRACESPAM)
	{
		startupTraceSpamEnabled = true;
	}
#endif
#if defined(NR_OF_LOGSPAMS)
	{
		nrOfLogSpams = NR_OF_LOGSPAMS;
	}
#endif
#if defined(NR_OF_TRACESPAMS)
	{
		nrOfTraceSpams = NR_OF_TRACESPAMS;
	}
#endif
#if defined(STARTUP_LOGWRITE_DELAY)
	{
		startupLogWriteDelay = STARTUP_LOGWRITE_DELAY;
	}
#endif
#if defined(STARTUP_TRACEWRITE_DELAY)
	{
		startupTraceWriteDelay = STARTUP_TRACEWRITE_DELAY;
	}
#endif
	/*
	 * Print all internal data to syslog that stored by the testOi (testConfig)
	 */
	testConfig->printAll();

	// Starting startup-logWrite thread
	if(startupLogWriteEnabled)
	{
		if ((PthreadResult = pthread_create(&OpenThreadId,NULL, &startupLogWriteThread, NULL)) != 0)
		{
			syslog(LOG_INFO, "%s maf_start(): pthread_create failed PthreadResult (%d)",log_prefix,PthreadResult);
		}
		else if (pthread_detach(OpenThreadId) != 0)
		{
			syslog(LOG_INFO, "%s maf_start(): failed to detach thread",log_prefix);
		}
	}
	// Starting startup-logSpam thread
	if(startupLogSpamEnabled)
	{
		if ((PthreadResult = pthread_create(&OpenThreadId,NULL, &startupLogSpamThread, NULL)) != 0)
		{
			syslog(LOG_INFO, "%s maf_start(): pthread_create failed PthreadResult (%d)",log_prefix,PthreadResult);
		}
		else if (pthread_detach(OpenThreadId) != 0)
		{
			syslog(LOG_INFO, "%s maf_start(): failed to detach thread",log_prefix);
		}
	}
	// Starting startup-traceSpam thread
	if(startupTraceSpamEnabled)
	{
		if ((PthreadResult = pthread_create(&OpenThreadId,NULL, &startupTraceSpamThread, NULL)) != 0)
		{
			syslog(LOG_INFO, "%s maf_start(): pthread_create failed PthreadResult (%d)",log_prefix,PthreadResult);
		}
		else if (pthread_detach(OpenThreadId) != 0)
		{
			syslog(LOG_INFO, "%s maf_start(): failed to detach thread",log_prefix);
		}
	}
	syslog(LOG_INFO, "%s maf_start(): returning MafOk",log_prefix);
	return MafOk;
}

/*
 * The component stops providing service.
 */
extern "C" MafReturnT maf_stop(MafStateChangeReasonT reason)
{
	syslog(LOG_INFO, "%s maf_stop() called (%i)",log_prefix, reason);
	MafReturnT ret_MAF = MafOk;

#if defined (CM_EVENT_CONSUMER)
	syslog(LOG_INFO, "%s maf_stop() removeSubscription for CM Event consumer (%lu)",log_prefix,consumer_handle);
	ret_MAF = _eventRouter->removeSubscription((MafOamSpiEventConsumerHandleT)consumer_handle, MafOamSpiCmEvent_Notification_1, (MafNameValuePairT **)cmNotificationFilter);
	if (ret_MAF != MafOk)
	{
		syslog(LOG_ERR,"%s maf_stop(): failed to removeSubscription (%d) for CM Event consumer",log_prefix, ret_MAF);
		return MafFailure;
	}
	freeCmEventFilterArray();
#endif
	syslog(LOG_INFO, "%s maf_stop() returns (%d)",log_prefix, ret_MAF);
	return ret_MAF;
}

/*
 * All the necessary values are set by the component.
 * This example component have no interfaces or
 * dependencies. The arrays are set to empty.
 */



void maf_initComponent()
{
	syslog(LOG_INFO, "%s maf_initComponent()",log_prefix);
	maf_component.base.componentName = component_name;
	maf_component.base.interfaceName = "MafMgmtSpiComponent";
	maf_component.base.interfaceVersion = "1";

	dependencyArray[0] = 0;

	managedObjectIf.base.componentName    = maf_component.base.componentName;
	managedObjectIf.base.interfaceName    = ComOamSpiManagedObject_3Id.interfaceName;
	managedObjectIf.base.interfaceVersion = ComOamSpiManagedObject_3Id.interfaceVersion;

	managedObjectIf.setMoAttribute     = maf_setMoAttribute;
	managedObjectIf.getMoAttribute     =maf_getMoAttribute;
	managedObjectIf.getMoAttributes    = maf_getMoAttributes;
	managedObjectIf.newMoIterator      = maf_newMoIterator;
	managedObjectIf.nextMo             = maf_nextMo;
	managedObjectIf.createMo           = maf_createMo;
	managedObjectIf.deleteMo           = maf_deleteMo;
	managedObjectIf.action             = maf_action;
	managedObjectIf.finalizeMoIterator = maf_finalizeMoIterator;
	managedObjectIf.existsMo           = maf_existsMo;
	managedObjectIf.countMoChildren    = maf_countMoChildren;

	transactionalResourceIf.base.componentName = maf_component.base.componentName;
	transactionalResourceIf.base.interfaceName = ComOamSpiTransactionalResource_2Id.interfaceName;
	transactionalResourceIf.base.interfaceVersion = ComOamSpiTransactionalResource_2Id.interfaceVersion;

	transactionalResourceIf.join    = join;
	transactionalResourceIf.prepare = prepare;
	transactionalResourceIf.commit  = commit;
	transactionalResourceIf.abort   = abort;
	transactionalResourceIf.finish  = finish;
	transactionalResourceIf.validate  = validate;

	interfaceArray[0] = (ComMgmtSpiInterface_1T*)&managedObjectIf;
	interfaceArray[0]->componentName = maf_component.base.componentName;
	interfaceArray[1] = (ComMgmtSpiInterface_1T*)&transactionalResourceIf;
	interfaceArray[1]->componentName = maf_component.base.componentName;
	interfaceArray[2] = 0;

	maf_component.interfaceArray  = (MafMgmtSpiInterface_1T **)interfaceArray;
	maf_component.dependencyArray = (MafMgmtSpiInterface_1T **)dependencyArray;

	maf_component.start = &maf_start;
	maf_component.stop  = &maf_stop;
}



extern "C" MafReturnT mafLCMinit(MafMgmtSpiInterfacePortalAccessorT* accessor, const char* config)
{
	syslog(LOG_INFO, "%s mafLCMinit(): Component started",log_prefix);
	MafReturnT ret = MafFailure;

	maf_initComponent();
	syslog(LOG_INFO, "%s mafLCMinit(): maf_initComponent() finished",log_prefix);

	_portal = (ComMgmtSpiInterfacePortal_1T*)accessor-> getPortal("1");
	assert(_portal);
	_portal_MAF = (MafMgmtSpiInterfacePortal_1T*)accessor-> getPortal("1");
	assert(_portal_MAF);

	ret = (MafReturnT) _portal_MAF->registerComponent(&maf_component);
	if (ret != MafOk) {
		syslog(LOG_ERR,"%s mafLCMinit(): failed(%d) to register component",log_prefix,ret);
		return ret;
	}

	syslog(LOG_INFO, "%s mafLCMinit(): Component registered, returning MafOk",log_prefix);
	return MafOk;
}

/*
 * The component unregisters itself.
 */
extern "C" void mafLCMterminate()
{
	syslog(LOG_INFO, "%s mafLCMterminate(): Unregistering component..",log_prefix);
	_portal->unregisterComponent(&component);
}
