/**
 * Include files   Copyright (C) 2010 by Ericsson AB
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
 *   File:   TestComponent.c
 *
 *   Author: uablrek & egorped
 *
 *   Date:   2010-09-30
 *
 *
 *   Reviewed: efaiami 2010-10-01
 *
 */

#include <assert.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <ComSA.h>
#include <saNtf.h>
#include <ComSANtf.h>
#include <SelectTimer.h>
#include <ComMwSpiServiceIdentities_1.h>
#include <MafMwSpiServiceIdentities_1.h>
#include <ComMwSpiReplicatedList_1.h>
#include <MafMwSpiReplicatedList_1.h>
#include <ComMwSpiTrace_1.h>
#include <MafMwSpiTrace_1.h>
#include <ComMwSpiLog_1.h>
#include <MafMwSpiLog_1.h>
#include <ComMgmtSpiCommon.h>
#include <MafMgmtSpiCommon.h>
#include <ComMgmtSpiComponent_1.h>
#include <MafMgmtSpiComponent_1.h>
#include <ComOamSpiEvent_1.h>
#include <MafOamSpiEvent_1.h>
#include <ComOamSpiNotificationFm_1.h>
#include <MafOamSpiNotificationFm_1.h>
#include <ComOamSpiServiceIdentities_1.h>
#include <MafOamSpiServiceIdentities_1.h>
#include "trace.h"
#include <stdlib.h>
#include <ComSALogService.h>

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

/* Forward declarations; */
static ComReturnT comSATestComponentStart(ComStateChangeReasonT reason);
static ComReturnT comSATestComponentStop(ComStateChangeReasonT reason);
static int comSATest_execute(void* userRef);

/* Data */

#define MIN_TRACE_GROUP 1
#define MAX_TRACE_GROUP 32

#define TEST_COMPONENT_NAME "MW_TEST"
static char const* const test_component_name = TEST_COMPONENT_NAME;


/* Test things relating to NTF and alarms */

static ComOamSpiEventRouter_1T fake_router;
static ComOamSpiEventProducer_1T *pIf;
static pthread_mutex_t list_lock = PTHREAD_MUTEX_INITIALIZER;

#define COMSANTF_ADD_TEXT "Additional text ComSA NTF TEST"
#define COMSANTF_NO "3GPPsafApp=ComSaTest,safSi=NoRed5"
#define COMSANTF_DN "safApp=ComSaTest,safSi=NoRed5"

static const uint32_t outMajorType = 193;
static const uint32_t outMinorType = 0x000E0004;

static const uint32_t inVType = 193;
static const uint16_t inMaType = 14; /*(0xE)*/
static const uint16_t inMiType = 4;
static int expected = 16;
static int okReceived = 0;
static char *addtxt;

static const char *sa_severity_list[] = {
	"SA_NTF_SEVERITY_CLEARED",
	"SA_NTF_SEVERITY_INDETERMINATE",
	"SA_NTF_SEVERITY_WARNING",
	"SA_NTF_SEVERITY_MINOR",
	"SA_NTF_SEVERITY_MAJOR",
	"SA_NTF_SEVERITY_CRITICAL",
};




static ComMgmtSpiInterface_1T* ifarray[] = { NULL };
static ComMgmtSpiInterface_1T rlist_interface = ComMwSpiReplicatedList_1Id;
static ComMgmtSpiInterface_1T trace_interface = ComMwSpiTrace_1Id;
static ComMgmtSpiInterface_1T log_interface   = ComMwSpiLog_1Id;
static ComMgmtSpiInterface_1T* deparray[] =  {
	&rlist_interface,
	&trace_interface,
	&log_interface,
	NULL
};
static ComMgmtSpiComponent_1T mw_test = {
	.base = {TEST_COMPONENT_NAME, "ComMgmtSpiComponent", "1"},
	.interfaceArray = ifarray,
	.dependencyArray = deparray,
	.start = comSATestComponentStart,
	.stop = comSATestComponentStop
};
static ComMwSpiReplicatedList_1T* rlist;
static ComMgmtSpiInterfacePortal_1T* portal;
static ComMwSpiTrace_1T*	trace;
static ComMwSpiLog_1T*		logger;


/* SDP1694 - support MAF SPI */
static MafReturnT maf_comSATestComponentStart(MafStateChangeReasonT reason);
static MafReturnT maf_comSATestComponentStop(MafStateChangeReasonT reason);
static int maf_comSATest_execute(void* userRef);


/* Test things relating to NTF and alarms */

static MafOamSpiEventRouter_1T maf_fake_router;
static MafOamSpiEventProducer_1T *maf_pIf;


static MafMgmtSpiInterface_1T* maf_ifarray[] = { NULL };
static MafMgmtSpiInterface_1T maf_rlist_interface = MafMwSpiReplicatedList_1Id;
static MafMgmtSpiInterface_1T maf_trace_interface = MafMwSpiTrace_1Id;
static MafMgmtSpiInterface_1T maf_log_interface   = MafMwSpiLog_1Id;
static MafMgmtSpiInterface_1T* maf_deparray[] =  {
	&maf_rlist_interface,
	&maf_trace_interface,
	&maf_log_interface,
	NULL
};
static MafMgmtSpiComponent_1T maf_mw_test = {
	.base = {TEST_COMPONENT_NAME, "MafMgmtSpiComponent", "1"},
	.interfaceArray = maf_ifarray,
	.dependencyArray = maf_deparray,
	.start = maf_comSATestComponentStart,
	.stop = maf_comSATestComponentStop
};
static MafMwSpiReplicatedList_1T* maf_rlist;
static MafMgmtSpiInterfacePortal_1T* maf_portal;
static MafMwSpiTrace_1T*	maf_trace;
static MafMwSpiLog_1T*		maf_logger;


/* ----------------------------------------------------------------------
 * Component control functions;
 */

static ComReturnT comSATestComponentStart(ComStateChangeReasonT reason)
{
        ENTER();
	DEBUG("comSATestComponentStart called...");
	if (portal->getInterface(
		    rlist_interface, (ComMgmtSpiInterface_1T**)&rlist)!=ComOk){
		ERR("Failed to get ComMwSpiReplicatedList");
		return ComFailure;
	}
	DEBUG("comSATestComponentStart 1");
	if (portal->getInterface(
		   trace_interface, (ComMgmtSpiInterface_1T**)&trace)!=ComOk){
		ERR("Failed to get ComMwSpiTrace");
		return ComFailure;
	}
	if (portal->getInterface(
		   log_interface, (ComMgmtSpiInterface_1T**)&logger)!=ComOk){
		ERR("Failed to get ComMwSpiLog");
		return ComFailure;
	}
        DEBUG("comSATestComponentStart 2");
	timerStart_r(comSASThandle, 3000, comSATest_execute, NULL);
	DEBUG("comSATestComponentStart 3");
	LEAVE();
	return ComOk;
}

static ComReturnT comSATestComponentStop(ComStateChangeReasonT reason)
{
	ENTER();
	DEBUG("comSATestComponentStop called...");
	LEAVE();
	return ComOk;
}

/* ----------------------------------------------------------------------
 * Functions called from the library control (in ComSAAc.c)
 */
ComReturnT comSATestComponentInitialize(
	ComMgmtSpiInterfacePortal_1T* _portal,
	xmlDocPtr config)
{
        ENTER();
        DEBUG("Calling registerComponent mw_test");
        LOG("comSATestComponentInitialize called...");
        portal = _portal;
        ComReturnT com_rc = portal->registerComponent(&mw_test);
	LEAVE();
	return com_rc;
}

void comSATestComponentFinalize(
	ComMgmtSpiInterfacePortal_1T* portal)
{
        ENTER();
	LOG("comSATestComponentFinalize called...");
	LEAVE();
}

/* ----------------------------------------------------------------------
 * TEST FUNCTIONS;
 */

#define ITEM_SIZE 1024

static void mkname(char const* name, ComMwSpiListNameT* buf)
{
        ENTER();
       	buf->length = strlen(name);
	assert(buf->length < MW_SPI_MAX_NAME_LENGTH);
	strcpy((char*)buf->value, name);
	LEAVE();
}

static ComReturnT comSATest_checkItem(
	char pattern,
	ComMwSpiListItemNameT* listItemName,
	char* data, unsigned datasize)
{
        ENTER();
       	unsigned i;
	if (listItemName->length != 1
	    || listItemName->value[0] != pattern) {
		WARN("Unexpected item-name {%u,%c} (%c)",
		     listItemName->length, listItemName->value[0], pattern);

		return ComFailure;
	}

	for (i = 0; i < datasize; i++) {
		if (data[i] != pattern) {
			WARN("Invalid data[%u] = '%c' (%c)",
			     i, data[i], pattern);
			return ComFailure;
		}
	}
	LEAVE();
	return ComOk;
}

static ComReturnT comSATest_addtolist(
	ComMwSpiListNameT* name, char const* pattern, unsigned long datasize)
{
	ENTER();
        ComReturnT com_rc;
	char* data = malloc(datasize);
	assert(data != 0);

	for (com_rc = ComOk; *pattern != 0; pattern++) {
		ComMwSpiListItemNameT listItemName;
		listItemName.length = 0;
		listItemName.value[0] = 0;
		memset(data, *pattern, datasize);
		com_rc = rlist->listPushBack(name, &listItemName, data);
		if (com_rc != ComOk) break;
		if (listItemName.length != 1
		    || listItemName.value[0] != *pattern) {
			com_rc = ComFailure;
			WARN("Pattern mismatch '%c' != '%c'",
			     listItemName.value[0], *pattern);
			break;
		}
	}

	free(data);
	LEAVE();
	return com_rc;
}

static ComReturnT comSATest_checklist(
	ComMwSpiListNameT* name, char const* pattern, unsigned long datasize)
{
	ENTER();
        ComReturnT com_rc = ComOk;
	char* data = malloc(datasize);
	ComMwSpiListItemRefT listInstanceRef = NULL;
	ComMwSpiListItemNameT listItemName;
	uint32_t listSize;
	bool isEmpty;
	char str[256];
	assert(data != 0);

	com_rc = rlist->listGetSize(name, &listSize);
	if (com_rc != ComOk) goto out;
	if (strlen(pattern) != listSize) {
	  DEBUG("Invalid size %u, expected %u", listSize,
		(unsigned)strlen(pattern));
	  com_rc = ComFailure;
	  DEBUG("comSATest_checklist error1");
	  goto out;
	}

	com_rc = rlist->listIsEmpty(name, &isEmpty);
	if (com_rc != ComOk)
	  {
	    DEBUG("comSATest_checklist error2");
	    goto out;
	  }
	if ((listSize > 0 && isEmpty) || (listSize == 0 && !isEmpty)) {
		DEBUG("listSize = %u, isEmpty = %d", listSize, (int)isEmpty);
		com_rc = ComFailure;
		DEBUG("comSATest_checklist error3");
		goto out;

	}
	DEBUG("comSATest_checklist listSize = %u, isEmpty = %d", listSize, (int)isEmpty);
	com_rc = rlist->listGetFrontRef(name, &listInstanceRef);
	if (com_rc != ComOk){
	  DEBUG("comSATest_checklist error4");
	  goto out;
	}
        memset (str,0,256);
        strncpy(str, (char*) name->value, name->length < 256? name->length:255);
	DEBUG("comSATest_checklist name=%s  ",str);
        if (listInstanceRef != NULL) {
  	    com_rc = rlist->listGetNextItemFront(
		name, &listInstanceRef, &listItemName, data);
	   if (com_rc != ComOk){
	     DEBUG("comSATest_checklist error5, rc=%d", com_rc);
	     goto out;
	   }
	}
	else DEBUG("comSATest_checklist listInstanceRef = NULL");

      	while (listInstanceRef != NULL) {
	  DEBUG("comSATest_checklist *pattern '%c'", *pattern);
	       if (*pattern == 0) {
			WARN("List too long");
			com_rc = ComFailure;
			goto out;
		}
	       DEBUG("comSATest_checklist while1");
		com_rc = comSATest_checkItem(
			*pattern, &listItemName, data, datasize);
		if (com_rc != ComOk){
		  DEBUG("comSATest_checklist error6");
		  goto out;
		}
		DEBUG("comSATest_checklist while2 ");
		com_rc = rlist->listGetNextItemFront(
			name, &listInstanceRef, &listItemName, data);
		if (com_rc != ComOk){
		  DEBUG("comSATest_checklist error7");
		  goto out;
		}
		pattern++;
	}
        if (listInstanceRef != NULL) {
	  com_rc = rlist->listGetFinalize(name, listInstanceRef);
	  if (com_rc != ComOk)
	    {
	      DEBUG("comSATest_checklist error8");
	      goto out;
	    }
	}


 out:
	free(data);
	LEAVE();
	return com_rc;
}

/*
 * Create and delete list. Operations on an empty list.
 */
static ComReturnT comSATest_basic(void)
{
	ENTER();
        ComReturnT com_rc;
	ComMwSpiListNameT name;
	uint32_t listSize;
	bool isEmpty;
	ComMwSpiListItemNameT listItemName = {1, "A"};
	char data[ITEM_SIZE];

	LOG("BASIC TEST ...");

	mkname("MyTestList", &name);
	com_rc = rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != ComOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_basic 1");
	com_rc = rlist->listIsEmpty(&name, &isEmpty);
	if (com_rc != ComOk || isEmpty == 0) {
		LOG("listIsEmpty, com_rc=%d, isEmpty=%d",
		    (int)com_rc, (int)isEmpty);
		return ComFailure;
	}
	DEBUG("comSATest_basic 2");
	com_rc = rlist->listGetSize(&name, &listSize);
	if (com_rc != ComOk || listSize > 0) {
		LOG("listGetSize, com_rc=%d, size=%u", (int)com_rc, listSize);
		return ComFailure;
	}
	DEBUG("comSATest_basic listGetSize, com_rc=%d, size=%u", (int)com_rc, listSize);
	DEBUG("comSATest_basic 3");
	com_rc = rlist->listClear(&name);
	if (com_rc != ComOk) {
		LOG("rlist->listClear, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_basic 4");
	com_rc = rlist->listGetSize(&name, &listSize);
	DEBUG("comSATest_basic listGetSize, com_rc=%d, size=%u", (int)com_rc, listSize);
	com_rc = comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != ComOk) return ComFailure;
	DEBUG("comSATest_basic 5");
	com_rc = rlist->listPopBack(&name);
	if (com_rc != ComOk) {
		LOG("rlist->listPopBack, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_basic 6");
	com_rc = rlist->listFindItem(&name, &listItemName, data);
	if (com_rc != ComNotExist) {
		LOG("rlist->listFindItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_basic 7");
	com_rc = rlist->listReplaceItem(&name, &listItemName, data);
	if (com_rc != ComNotExist) {
		LOG("rlist->listReplaceItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_basic 8");
	com_rc = rlist->listDelete(&name);
	if (com_rc != ComOk) {
		LOG("rlist->listDelete, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_basic 9");
	LOG("======== BASIC TEST PASSED ===========");
	LEAVE();
	return ComOk;

}

static ComReturnT comSATest_itemdata(void)
{
	ENTER();
        ComReturnT com_rc;
	ComMwSpiListNameT name;
	ComMwSpiListItemNameT listItemName = {1, " "};
	char data[ITEM_SIZE];
	LOG("ITEM DATA TEST ...");

	mkname("MyItemDataList", &name);
	com_rc = rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != ComOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 1");
	/*
	 * Create some items, find/replace items and clear the list.
	 */

	com_rc = comSATest_addtolist(&name, "123456", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemdata 2");
	com_rc = comSATest_checklist(&name, "123456", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemdata 3");
	DEBUG("Test; listFindItem");
	listItemName.value[0] = '1';
	com_rc = rlist->listFindItem(&name, &listItemName, data);
	DEBUG("comSATest_itemdata 4");
	if (com_rc != ComOk) {
		LOG("rlist->listFindItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 5");
	com_rc = comSATest_checkItem('1', &listItemName, data, ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemdata 6");
	listItemName.value[0] = '6';
	com_rc = rlist->listFindItem(&name, &listItemName, data);
	DEBUG("comSATest_itemdata 7");
	if (com_rc != ComOk) {
		LOG("rlist->listFindItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 8");
	com_rc = comSATest_checkItem('6', &listItemName, data, ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemdata 9");
	listItemName.value[0] = '7';
	com_rc = rlist->listFindItem(&name, &listItemName, data);
	if (com_rc != ComNotExist) {
		LOG("rlist->listFindItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 10");
	DEBUG("---------------- listReplaceItem");
	memset(data, 'X', ITEM_SIZE);
	listItemName.value[0] = '4';
	com_rc = rlist->listReplaceItem(&name, &listItemName, data);
	if (com_rc != ComOk) {
		LOG("rlist->listReplaceItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 11");
	com_rc = rlist->listFindItem(&name, &listItemName, data);
	if (com_rc != ComOk) {
		LOG("rlist->listFindItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 12");
	listItemName.value[0] = 'X';
	com_rc = comSATest_checkItem('X', &listItemName, data, ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemdata 13");
	memset(data, '4', ITEM_SIZE);
	listItemName.value[0] = '4';
	com_rc = rlist->listReplaceItem(&name, &listItemName, data);
	if (com_rc != ComOk) {
		LOG("rlist->listReplaceItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 14");
	com_rc = comSATest_checklist(&name, "123456", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemdata 15");

	com_rc = rlist->listClear(&name);
	if (com_rc != ComOk) {
		LOG("rlist->listClear, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 16");
	com_rc = comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemdata 17");
	com_rc = rlist->listDelete(&name);
	if (com_rc != ComOk) {
		LOG("rlist->listDelete, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemdata 18");
	LOG("======== ITEM DATA TEST PASSED ===========");
	LEAVE();
	return ComOk;
}

static ComReturnT comSATest_itemaddrem(void)
{
        ENTER();
	ComReturnT com_rc;
	ComMwSpiListNameT name;
	ComMwSpiListItemNameT itemName = {1, " "};

	LOG("ITEM ADD/REMOVE TEST ...");

	mkname("MyItemDataList", &name);
	com_rc = rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != ComOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 1");
	com_rc = comSATest_addtolist(&name, "12345", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 2");
	com_rc = comSATest_checklist(&name, "12345", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 3");

	com_rc = rlist->listPopBack(&name);
	if (com_rc != ComOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 4");
	com_rc = comSATest_checklist(&name, "1234", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 5");

	com_rc = rlist->listPopBack(&name);
	if (com_rc != ComOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 6");
	com_rc = comSATest_checklist(&name, "123", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 7");

	com_rc = rlist->listPopBack(&name);
	if (com_rc != ComOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 8");
	com_rc = comSATest_checklist(&name, "12", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 9");

	com_rc = rlist->listPopBack(&name);
	if (com_rc != ComOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 10");
	com_rc = comSATest_checklist(&name, "1", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 11");

	com_rc = rlist->listPopBack(&name);
	if (com_rc != ComOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 12");
	com_rc = comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 13");

	com_rc = rlist->listPopBack(&name);
	if (com_rc != ComOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 14");
	com_rc = comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 15");

	com_rc = rlist->listDelete(&name);
	if (com_rc != ComOk) {
		LOG("rlist->listDelete, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 16");

	/* -- new list -- */

	com_rc = rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != ComOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 17");

	com_rc = comSATest_addtolist(&name, "123456", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 18a");
	com_rc = comSATest_checklist(&name, "123456", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 18");

	itemName.value[0] = '3';
	com_rc = rlist->listEraseItem(&name, &itemName);
	if (com_rc != ComOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 19");
	com_rc = comSATest_checklist(&name, "12456", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 20");

	itemName.value[0] = '1';
	com_rc = rlist->listEraseItem(&name, &itemName);
	if (com_rc != ComOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 21");
	com_rc = comSATest_checklist(&name, "2456", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 22");

	itemName.value[0] = '6';
	com_rc = rlist->listEraseItem(&name, &itemName);
	if (com_rc != ComOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 23");
	com_rc = comSATest_checklist(&name, "245", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 24");

	itemName.value[0] = '4';
	com_rc = rlist->listEraseItem(&name, &itemName);
	if (com_rc != ComOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 25");
	com_rc = comSATest_checklist(&name, "25", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 26");

	itemName.value[0] = '5';
	com_rc = rlist->listEraseItem(&name, &itemName);
	if (com_rc != ComOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 27");
	com_rc = comSATest_checklist(&name, "2", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 28");

	itemName.value[0] = '5';
	com_rc = rlist->listEraseItem(&name, &itemName);
	if (com_rc != ComNotExist) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 29");
	com_rc = comSATest_checklist(&name, "2", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 30");

	itemName.value[0] = '2';
	com_rc = rlist->listEraseItem(&name, &itemName);
	if (com_rc != ComOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 31");
	com_rc = comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != ComOk) return com_rc;
	DEBUG("comSATest_itemaddrem 32");

	com_rc = rlist->listDelete(&name);
	if (com_rc != ComOk) {
		LOG("rlist->listDelete, com_rc=%d", (int)com_rc);
		return ComFailure;
	}
	DEBUG("comSATest_itemaddrem 33");

	LOG("======== ITEM ADD/REMOVE PASSED ===========");
	LEAVE();
	return ComOk;
}

static int comSATest_traceWrite(void)
{
        ENTER();
       	uint32_t	u;
	char		Message[256];
	for (u = MIN_TRACE_GROUP; u <= MAX_TRACE_GROUP; u++)
	{
		sprintf(Message,"Tracing group no %d",u);
		trace->traceWrite(u,Message);
	}
	LEAVE();
	return ComOk;
}

static int comSATest_traceEnter(void)
{
        ENTER();
       	uint32_t	u;
	char		Message[256];
	for (u = MIN_TRACE_GROUP; u <= MAX_TRACE_GROUP; u++)
	{
		sprintf(Message,"Tracing group no %d",u);
		trace->traceWriteEnter(u,"comSATest_traceEnter()",Message);
	}
	LEAVE();
	return ComOk;
}

static int comSATest_traceExit(void)
{
        ENTER();
       	uint32_t	u;
	char		Message[256];
	for (u = MIN_TRACE_GROUP; u <= MAX_TRACE_GROUP; u++)
	{
		sprintf(Message,"Tracing group no %d",u);
		trace->traceWriteExit(u,"comSATest_traceExit()",u,Message);
	}
	LEAVE();
	return ComOk;
}

static int comSATest_log(void)
{
        ENTER();
       	int failures = 0;
	int facility;
	int severity;
	char databuffer[256];

       	for(severity = 0;  severity <= 6; severity++)
	{
		for(facility = 0; facility <= 22 ; facility++)
		{
			sprintf(databuffer," Test component logging severity = %d, facility = %d\n", severity,facility);
			ComReturnT ReturnValue = logger->logWrite( 1 , severity, facility , databuffer);
			if (ReturnValue != ComOk)
			failures++;
		}
	}
	LEAVE();
	return failures;
}

/* Test NTF and Alarms */

static void comSATest_print_severity(SaNtfSeverityT input)
{
        ENTER();
	if(!(input >= SA_NTF_SEVERITY_CLEARED)||!(input <= SA_NTF_SEVERITY_CRITICAL))
		ERR("wrong severity");
	DEBUG("severity = %s\n", (char *)sa_severity_list[input]);
	LEAVE();
}

static ComReturnT comSATest_notify(ComOamSpiEventProducerHandleT producerId,
                         ComOamSpiEventConsumerHandleT consumerId,
                         const char * eventType,
                         ComNameValuePairT **filter,
                         void * value)
{
        ENTER();
	if (pthread_mutex_lock(&list_lock) != 0) abort();
	ComReturnT com_rc = ComOk;
	ComOamSpiNotificationFmStructT *comNot = (ComOamSpiNotificationFmStructT*)value;
	DEBUG("------ ComAlarm --------\n");
	comSATest_print_severity(comNot->severity);
	DEBUG("dn: \"%s\"\n", comNot->dn);
	DEBUG("addtxt: %s\n", comNot->additionalText);
	DEBUG("majorType %#x\n", comNot->majorType);
	DEBUG("minorType %#x\n", comNot->minorType);
	DEBUG("------------------------\n");
	if (comNot->majorType == outMajorType && comNot->minorType == outMinorType &&
		 strcmp(comNot->dn, COMSANTF_DN)== 0 &&
		 strcmp(comNot->additionalText, addtxt)==0) {
		okReceived++;
	}
	pIf->doneWithValue(NULL, (void*)comNot);
	if (pthread_mutex_unlock(&list_lock) != 0) abort();
	LEAVE();
	return com_rc;
}

static ComReturnT comSATest_registerProducer(ComOamSpiEventProducer_1T * interface, ComOamSpiEventProducerHandleT * handle)
{
        ENTER();
	pIf = interface;
	LEAVE();
	return ComOk;
}

static ComReturnT comSATest_addProducerEvent(ComOamSpiEventProducerHandleT handle, const char * eventType)
{
	 ENTER();
	 LEAVE();
	 return ComOk;
}

static ComReturnT comSATest_getIf( ComMgmtSpiInterface_1T interfaceId, ComMgmtSpiInterface_1T **result)
{
        ENTER();
	*result = (ComMgmtSpiInterface_1T *)&fake_router;
	LEAVE();
	return ComOk;
}

static ComReturnT comSATest_removeProducerEvent(ComOamSpiEventProducerHandleT handle, const char * eventType)
{
	 ENTER();
	 LEAVE();
	 return ComOk;
}

static ComReturnT comSATest_unregisterProducer(ComOamSpiEventProducerHandleT handle, ComOamSpiEventProducer_1T * interface)
{
	 ENTER();
	 LEAVE();
	 return ComOk;
}

static ComReturnT UNUSED_FUNCTION(comSATest_testNotifications)()
{
	ENTER();
	int rv;
	long int rnum = 0;
	char buf[2048], sbuf[2048];
	DEBUG("comSATest_testNotifications");
	ComReturnT com_rv = ComOk;
	ComMgmtSpiInterfacePortal_1T fake_portal;
	ComNameValuePairT *filter = NULL;
	fake_portal.getInterface = &comSATest_getIf;

	fake_router.registerProducer = &comSATest_registerProducer;
	fake_router.addProducerEvent = &comSATest_addProducerEvent;
	fake_router.removeProducerEvent = &comSATest_removeProducerEvent;
	fake_router.unregisterProducer = &comSATest_unregisterProducer;
	fake_router.notify = comSATest_notify;
	srandom(getpid());
	rnum = random();
	 /* SelectTimer init; */
	addtxt = malloc(sizeof(COMSANTF_ADD_TEXT)+ 256);
	snprintf(addtxt, sizeof(COMSANTF_ADD_TEXT)+ 256, "%s:%ld", COMSANTF_ADD_TEXT, rnum);
	comSASThandle = timerCreateHandle_r();
	poll_maxfd(comSASThandle, 16);
	printf("START ComSA notification test\n");
	DEBUG("Send 4 Al  and 4 sec Al before subscribe\n");
	snprintf(buf, 2048, "ntfsend -r 4 -c %u,%hu,%hu -n \"%s\" -a \"%s:%ld\"",
		inVType, inMaType, inMiType, COMSANTF_NO, COMSANTF_ADD_TEXT,rnum);
	DEBUG(buf);
	snprintf(sbuf, 2048, "ntfsend -r 4 -T0x5000 -c %u,%hu,%hu -n \"%s\" -a \"%s:%ld\"",
		inVType, inMaType, inMiType, COMSANTF_NO, COMSANTF_ADD_TEXT,rnum);
	DEBUG(sbuf);
	rv = system(buf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend Al failed\n");
		com_rv = ComFailure;
		goto end_exit;
	}
	rv = system(sbuf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend sec Al failed\n");
		com_rv = ComFailure;
		goto end_exit;
	}
	DEBUG("Open NTF service IF\n");
	com_rv = ComNtfServiceOpen(&fake_portal);
	if (com_rv != ComOk)
	{
		LOG("COM SA TEST  ComNtfServiceOpen FAILED error = %d\n", com_rv);
		goto end_exit;
	}

	DEBUG("addFilter ComSA notifications\n");
	com_rv = pIf->addFilter(44, NULL, &filter);
	if (com_rv != ComOk)
	{
		LOG("COM SA TEST  addFilter FAILED error = %d\n", com_rv);
		goto end_close_exit;
	}
	DEBUG("Send 4 Al and 4 sec Al after subscribe\n");
	rv = system(buf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend Al failed after subscribtion \n");
		goto end_close_exit;
	}
	rv = system(sbuf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend sec Al failed after subscribtion \n");
		goto end_close_exit;
	}
	poll_execute(comSASThandle);
	DEBUG("Drop out of control-loop\n");
	DEBUG("removeFilter ComSA notifications\n");
	pIf->removeFilter(44, NULL, &filter);
	if (okReceived == expected) {
		LOG("ComSA notification test: test ok\n");
	} else {
		LOG("ComSA notification test: test failed received %d of %d\n",
			okReceived, expected);
		com_rv = ComFailure;
	}
end_close_exit:
	ComNtfServiceClose(&fake_portal);
end_exit:
	LEAVE();
	return com_rv;
}

static int comSATest_execute(void* userRef)
{
	ENTER();
	int failed_testcases;
	LOG("comSATest_execute called...");


	if (comSATest_basic() != ComOk)
	{
		LOG("=== REPLICATED LISTS BASIC FAILED ====");
	}
	if (comSATest_itemdata() != ComOk){
	  DEBUG("comSATest_execute error1");
	  return 0;
	}
	if (comSATest_itemaddrem() != ComOk) {
	  DEBUG("comSATest_execute error2");
	  return 0;
	}


		LOG("=== REPLICATED LISTS TESTS PASSED====");

	if (comSATest_traceWrite() != ComOk) {
	  DEBUG("comSATest_execute error3");
	  return 0;
	}
	if (comSATest_traceEnter() != ComOk) {
	  DEBUG("comSATest_execute error4");
	  return 0;
	}
	if (comSATest_traceExit() != ComOk){
	  DEBUG("comSATest_execute error5");
	  return 0;
	}
	LOG("=== TRACE TESTS PASSED ==============");

	if ((failed_testcases = comSATest_log()) == 0)
	{
		LOG("=== LOG TESTS PASSED ===============");
	}
	else
	{
		LOG("=== LOG TESTS FAILED WITH %d FAILURES==", failed_testcases);
		return 0;
	}
/*
	if (comSATest_testNotifications() != ComOk)
	{
		LOG("=== NOTIFICATION/ALARM TESTS FAILED ===");
		return 0;
	}
*/
	LOG("======== ALL TESTS PASSED ===========");
	LEAVE();
	return 0;
}


/* SDP1694 - support MAF SPI */
/* ----------------------------------------------------------------------
 * Component control functions;
 */

static MafReturnT maf_comSATestComponentStart(MafStateChangeReasonT reason)
{
        ENTER();
	DEBUG("comSATestComponentStart called...");
	if (maf_portal->getInterface(
		    maf_rlist_interface, (MafMgmtSpiInterface_1T**)&maf_rlist)!=MafOk){
		ERR("Failed to get MafMwSpiReplicatedList");
		return MafFailure;
	}
	DEBUG("comSATestComponentStart 1");
	if (maf_portal->getInterface(
		   maf_trace_interface, (MafMgmtSpiInterface_1T**)&maf_trace)!=MafOk){
		ERR("Failed to get MafMwSpiTrace");
		return MafFailure;
	}
	if (maf_portal->getInterface(
		   maf_log_interface, (MafMgmtSpiInterface_1T**)&maf_logger)!=MafOk){
		ERR("Failed to get MafMwSpiLog");
		return MafFailure;
	}
        DEBUG("comSATestComponentStart 2");
	timerStart_r(comSASThandle, 3000, maf_comSATest_execute, NULL);
	DEBUG("comSATestComponentStart 3");
	LEAVE();
	return MafOk;
}

static MafReturnT maf_comSATestComponentStop(MafStateChangeReasonT reason)
{
	ENTER();
	DEBUG("comSATestComponentStop called...");
	LEAVE();
	return MafOk;
}

/* ----------------------------------------------------------------------
 * Functions called from the library control (in ComSAAc.c)
 */
MafReturnT maf_comSATestComponentInitialize(
	MafMgmtSpiInterfacePortal_1T* _portal,
	xmlDocPtr config)
{
        ENTER();
        DEBUG("Calling registerComponent mw_test");
        LOG("maf_comSATestComponentInitialize called...");
        maf_portal = _portal;
        MafReturnT com_rc = maf_portal->registerComponent(&maf_mw_test);
	LEAVE();
	return com_rc;
}

void maf_comSATestComponentFinalize(
	MafMgmtSpiInterfacePortal_1T* maf_portal)
{
        ENTER();
	LOG("maf_comSATestComponentFinalize called...");
	LEAVE();
}

/* ----------------------------------------------------------------------
 * TEST FUNCTIONS;
 */

#define ITEM_SIZE 1024

static void maf_mkname(char const* name, MafMwSpiListNameT* buf)
{
        ENTER();
       	buf->length = strlen(name);
	assert(buf->length < MW_SPI_MAX_NAME_LENGTH);
	strcpy((char*)buf->value, name);
	LEAVE();
}

static MafReturnT maf_comSATest_checkItem(
	char pattern,
	MafMwSpiListItemNameT* listItemName,
	char* data, unsigned datasize)
{
        ENTER();
       	unsigned i;
	if (listItemName->length != 1
	    || listItemName->value[0] != pattern) {
		WARN("Unexpected item-name {%u,%c} (%c)",
		     listItemName->length, listItemName->value[0], pattern);

		return MafFailure;
	}

	for (i = 0; i < datasize; i++) {
		if (data[i] != pattern) {
			WARN("Invalid data[%u] = '%c' (%c)",
			     i, data[i], pattern);
			return MafFailure;
		}
	}
	LEAVE();
	return MafOk;
}

static MafReturnT maf_comSATest_addtolist(
	MafMwSpiListNameT* name, char const* pattern, unsigned long datasize)
{
	ENTER();
        MafReturnT com_rc;
	char* data = malloc(datasize);
	assert(data != 0);

	for (com_rc = MafOk; *pattern != 0; pattern++) {
		MafMwSpiListItemNameT listItemName;
		listItemName.length = 0;
		listItemName.value[0] = 0;
		memset(data, *pattern, datasize);
		com_rc = maf_rlist->listPushBack(name, &listItemName, data);
		if (com_rc != MafOk) break;
		if (listItemName.length != 1
		    || listItemName.value[0] != *pattern) {
			com_rc = MafFailure;
			WARN("Pattern mismatch '%c' != '%c'",
			     listItemName.value[0], *pattern);
			break;
		}
	}

	free(data);
	LEAVE();
	return com_rc;
}

static MafReturnT maf_comSATest_checklist(
	MafMwSpiListNameT* name, char const* pattern, unsigned long datasize)
{
	ENTER();
        MafReturnT com_rc = MafOk;
	char* data = malloc(datasize);
	MafMwSpiListItemRefT listInstanceRef = NULL;
	MafMwSpiListItemNameT listItemName;
	uint32_t listSize;
	bool isEmpty;
	char str[256];
	assert(data != 0);

	com_rc = maf_rlist->listGetSize(name, &listSize);
	if (com_rc != MafOk) goto out;
	if (strlen(pattern) != listSize) {
	  DEBUG("Invalid size %u, expected %u", listSize,
		(unsigned)strlen(pattern));
	  com_rc = MafFailure;
	  DEBUG("maf_comSATest_checklist error1");
	  goto out;
	}

	com_rc = maf_rlist->listIsEmpty(name, &isEmpty);
	if (com_rc != MafOk)
	  {
	    DEBUG("maf_comSATest_checklist error2");
	    goto out;
	  }
	if ((listSize > 0 && isEmpty) || (listSize == 0 && !isEmpty)) {
		DEBUG("listSize = %u, isEmpty = %d", listSize, (int)isEmpty);
		com_rc = MafFailure;
		DEBUG("maf_comSATest_checklist error3");
		goto out;

	}
	DEBUG("maf_comSATest_checklist listSize = %u, isEmpty = %d", listSize, (int)isEmpty);
	com_rc = maf_rlist->listGetFrontRef(name, &listInstanceRef);
	if (com_rc != MafOk){
	  DEBUG("maf_comSATest_checklist error4");
	  goto out;
	}
        memset (str,0,256);
        strncpy(str, (char*) name->value, name->length < 256? name->length:255);
	DEBUG("maf_comSATest_checklist name=%s  ",str);
        if (listInstanceRef != NULL) {
  	    com_rc = maf_rlist->listGetNextItemFront(
		name, &listInstanceRef, &listItemName, data);
	   if (com_rc != MafOk){
	     DEBUG("maf_comSATest_checklist error5, rc=%d", com_rc);
	     goto out;
	   }
	}
	else DEBUG("maf_comSATest_checklist listInstanceRef = NULL");

      	while (listInstanceRef != NULL) {
	  DEBUG("maf_comSATest_checklist *pattern '%c'", *pattern);
	       if (*pattern == 0) {
			WARN("List too long");
			com_rc = MafFailure;
			goto out;
		}
	       DEBUG("maf_comSATest_checklist while1");
		com_rc = maf_comSATest_checkItem(
			*pattern, &listItemName, data, datasize);
		if (com_rc != MafOk){
		  DEBUG("maf_comSATest_checklist error6");
		  goto out;
		}
		DEBUG("maf_comSATest_checklist while2 ");
		com_rc = maf_rlist->listGetNextItemFront(
			name, &listInstanceRef, &listItemName, data);
		if (com_rc != MafOk){
		  DEBUG("maf_comSATest_checklist error7");
		  goto out;
		}
		pattern++;
	}
        if (listInstanceRef != NULL) {
	  com_rc = maf_rlist->listGetFinalize(name, listInstanceRef);
	  if (com_rc != MafOk)
	    {
	      DEBUG("maf_comSATest_checklist error8");
	      goto out;
	    }
	}


 out:
	free(data);
	LEAVE();
	return com_rc;
}

/*
 * Create and delete list. Operations on an empty list.
 */
static MafReturnT maf_comSATest_basic(void)
{
	ENTER();
        MafReturnT com_rc;
	MafMwSpiListNameT name;
	uint32_t listSize;
	bool isEmpty;
	MafMwSpiListItemNameT listItemName = {1, "A"};
	char data[ITEM_SIZE];

	LOG("BASIC TEST ...");

	maf_mkname("MyTestList", &name);
	com_rc = maf_rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != MafOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic 1");
	com_rc = maf_rlist->listIsEmpty(&name, &isEmpty);
	if (com_rc != MafOk || isEmpty == 0) {
		LOG("listIsEmpty, com_rc=%d, isEmpty=%d",
		    (int)com_rc, (int)isEmpty);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic 2");
	com_rc = maf_rlist->listGetSize(&name, &listSize);
	if (com_rc != MafOk || listSize > 0) {
		LOG("listGetSize, com_rc=%d, size=%u", (int)com_rc, listSize);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic listGetSize, com_rc=%d, size=%u", (int)com_rc, listSize);
	DEBUG("maf_comSATest_basic 3");
	com_rc = maf_rlist->listClear(&name);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listClear, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic 4");
	com_rc = maf_rlist->listGetSize(&name, &listSize);
	DEBUG("maf_comSATest_basic listGetSize, com_rc=%d, size=%u", (int)com_rc, listSize);
	com_rc = maf_comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != MafOk) return MafFailure;
	DEBUG("maf_comSATest_basic 5");
	com_rc = maf_rlist->listPopBack(&name);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listPopBack, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic 6");
	com_rc = maf_rlist->listFindItem(&name, &listItemName, data);
	if (com_rc != MafNotExist) {
		LOG("maf_rlist->listFindItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic 7");
	com_rc = maf_rlist->listReplaceItem(&name, &listItemName, data);
	if (com_rc != MafNotExist) {
		LOG("maf_rlist->listReplaceItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic 8");
	com_rc = maf_rlist->listDelete(&name);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listDelete, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_basic 9");
	LOG("======== BASIC TEST PASSED ===========");
	LEAVE();
	return MafOk;

}

static MafReturnT maf_comSATest_itemdata(void)
{
	ENTER();
        MafReturnT com_rc;
	MafMwSpiListNameT name;
	MafMwSpiListItemNameT listItemName = {1, " "};
	char data[ITEM_SIZE];
	LOG("ITEM DATA TEST ...");

	maf_mkname("MyItemDataList", &name);
	com_rc = maf_rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != MafOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 1");
	/*
	 * Create some items, find/replace items and clear the list.
	 */

	com_rc = maf_comSATest_addtolist(&name, "123456", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemdata 2");
	com_rc = maf_comSATest_checklist(&name, "123456", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemdata 3");
	DEBUG("Test; listFindItem");
	listItemName.value[0] = '1';
	com_rc = maf_rlist->listFindItem(&name, &listItemName, data);
	DEBUG("maf_comSATest_itemdata 4");
	if (com_rc != MafOk) {
		LOG("maf_rlist->listFindItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 5");
	com_rc = maf_comSATest_checkItem('1', &listItemName, data, ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemdata 6");
	listItemName.value[0] = '6';
	com_rc = maf_rlist->listFindItem(&name, &listItemName, data);
	DEBUG("maf_comSATest_itemdata 7");
	if (com_rc != MafOk) {
		LOG("maf_rlist->listFindItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 8");
	com_rc = maf_comSATest_checkItem('6', &listItemName, data, ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemdata 9");
	listItemName.value[0] = '7';
	com_rc = maf_rlist->listFindItem(&name, &listItemName, data);
	if (com_rc != MafNotExist) {
		LOG("maf_rlist->listFindItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 10");
	DEBUG("---------------- listReplaceItem");
	memset(data, 'X', ITEM_SIZE);
	listItemName.value[0] = '4';
	com_rc = maf_rlist->listReplaceItem(&name, &listItemName, data);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listReplaceItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 11");
	com_rc = maf_rlist->listFindItem(&name, &listItemName, data);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listFindItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 12");
	listItemName.value[0] = 'X';
	com_rc = maf_comSATest_checkItem('X', &listItemName, data, ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemdata 13");
	memset(data, '4', ITEM_SIZE);
	listItemName.value[0] = '4';
	com_rc = maf_rlist->listReplaceItem(&name, &listItemName, data);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listReplaceItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 14");
	com_rc = maf_comSATest_checklist(&name, "123456", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemdata 15");

	com_rc = maf_rlist->listClear(&name);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listClear, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 16");
	com_rc = maf_comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemdata 17");
	com_rc = maf_rlist->listDelete(&name);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listDelete, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemdata 18");
	LOG("======== ITEM DATA TEST PASSED ===========");
	LEAVE();
	return MafOk;
}

static MafReturnT maf_comSATest_itemaddrem(void)
{
        ENTER();
	MafReturnT com_rc;
	MafMwSpiListNameT name;
	MafMwSpiListItemNameT itemName = {1, " "};

	LOG("ITEM ADD/REMOVE TEST ...");

	maf_mkname("MyItemDataList", &name);
	com_rc = maf_rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != MafOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 1");
	com_rc = maf_comSATest_addtolist(&name, "12345", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 2");
	com_rc = maf_comSATest_checklist(&name, "12345", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 3");

	com_rc = maf_rlist->listPopBack(&name);
	if (com_rc != MafOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 4");
	com_rc = maf_comSATest_checklist(&name, "1234", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 5");

	com_rc = maf_rlist->listPopBack(&name);
	if (com_rc != MafOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 6");
	com_rc = maf_comSATest_checklist(&name, "123", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 7");

	com_rc = maf_rlist->listPopBack(&name);
	if (com_rc != MafOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 8");
	com_rc = maf_comSATest_checklist(&name, "12", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 9");

	com_rc = maf_rlist->listPopBack(&name);
	if (com_rc != MafOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 10");
	com_rc = maf_comSATest_checklist(&name, "1", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 11");

	com_rc = maf_rlist->listPopBack(&name);
	if (com_rc != MafOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 12");
	com_rc = maf_comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 13");

	com_rc = maf_rlist->listPopBack(&name);
	if (com_rc != MafOk) {
		LOG("listPopBack, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 14");
	com_rc = maf_comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 15");

	com_rc = maf_rlist->listDelete(&name);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listDelete, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 16");

	/* -- new list -- */

	com_rc = maf_rlist->listCreate(&name, ITEM_SIZE);
	if (com_rc != MafOk) {
		LOG("listCreate, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 17");

	com_rc = maf_comSATest_addtolist(&name, "123456", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 18a");
	com_rc = maf_comSATest_checklist(&name, "123456", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 18");

	itemName.value[0] = '3';
	com_rc = maf_rlist->listEraseItem(&name, &itemName);
	if (com_rc != MafOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 19");
	com_rc = maf_comSATest_checklist(&name, "12456", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 20");

	itemName.value[0] = '1';
	com_rc = maf_rlist->listEraseItem(&name, &itemName);
	if (com_rc != MafOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 21");
	com_rc = maf_comSATest_checklist(&name, "2456", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 22");

	itemName.value[0] = '6';
	com_rc = maf_rlist->listEraseItem(&name, &itemName);
	if (com_rc != MafOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 23");
	com_rc = maf_comSATest_checklist(&name, "245", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 24");

	itemName.value[0] = '4';
	com_rc = maf_rlist->listEraseItem(&name, &itemName);
	if (com_rc != MafOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 25");
	com_rc = maf_comSATest_checklist(&name, "25", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 26");

	itemName.value[0] = '5';
	com_rc = maf_rlist->listEraseItem(&name, &itemName);
	if (com_rc != MafOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 27");
	com_rc = maf_comSATest_checklist(&name, "2", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 28");

	itemName.value[0] = '5';
	com_rc = maf_rlist->listEraseItem(&name, &itemName);
	if (com_rc != MafNotExist) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 29");
	com_rc = maf_comSATest_checklist(&name, "2", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 30");

	itemName.value[0] = '2';
	com_rc = maf_rlist->listEraseItem(&name, &itemName);
	if (com_rc != MafOk) {
		LOG("listEraseItem, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 31");
	com_rc = maf_comSATest_checklist(&name, "", ITEM_SIZE);
	if (com_rc != MafOk) return com_rc;
	DEBUG("maf_comSATest_itemaddrem 32");

	com_rc = maf_rlist->listDelete(&name);
	if (com_rc != MafOk) {
		LOG("maf_rlist->listDelete, com_rc=%d", (int)com_rc);
		return MafFailure;
	}
	DEBUG("maf_comSATest_itemaddrem 33");

	LOG("======== ITEM ADD/REMOVE PASSED ===========");
	LEAVE();
	return MafOk;
}

static int maf_comSATest_traceWrite(void)
{
        ENTER();
       	uint32_t	u;
	char		Message[256];
	for (u = MIN_TRACE_GROUP; u <= MAX_TRACE_GROUP; u++)
	{
		sprintf(Message,"Tracing group no %d",u);
		maf_trace->traceWrite(u,Message);
	}
	LEAVE();
	return MafOk;
}

static int maf_comSATest_traceEnter(void)
{
        ENTER();
       	uint32_t	u;
	char		Message[256];
	for (u = MIN_TRACE_GROUP; u <= MAX_TRACE_GROUP; u++)
	{
		sprintf(Message,"Tracing group no %d",u);
		maf_trace->traceWriteEnter(u,"maf_comSATest_traceEnter()",Message);
	}
	LEAVE();
	return MafOk;
}

static int maf_comSATest_traceExit(void)
{
        ENTER();
       	uint32_t	u;
	char		Message[256];
	for (u = MIN_TRACE_GROUP; u <= MAX_TRACE_GROUP; u++)
	{
		sprintf(Message,"Tracing group no %d",u);
		maf_trace->traceWriteExit(u,"maf_comSATest_traceExit()",u,Message);
	}
	LEAVE();
	return MafOk;
}

static int maf_comSATest_log(void)
{
        ENTER();
       	int failures = 0;
	int facility;
	int severity;
	char databuffer[256];

       	for(severity = 0;  severity <= 6; severity++)
	{
		for(facility = 0; facility <= 22 ; facility++)
		{
			sprintf(databuffer," Test component logging severity = %d, facility = %d\n", severity,facility);
			MafReturnT ReturnValue = maf_logger->logWrite( 1 , severity, facility , databuffer);
			if (ReturnValue != MafOk)
			failures++;
		}
	}
	LEAVE();
	return failures;
}

/* Test NTF and Alarms */

static void maf_comSATest_print_severity(SaNtfSeverityT input)
{
        ENTER();
	if(!(input >= SA_NTF_SEVERITY_CLEARED)||!(input <= SA_NTF_SEVERITY_CRITICAL))
		ERR("wrong severity");
	DEBUG("severity = %s\n", (char *)sa_severity_list[input]);
	LEAVE();
}

static MafReturnT maf_comSATest_notify(MafOamSpiEventProducerHandleT producerId,
                         MafOamSpiEventConsumerHandleT consumerId,
                         const char * eventType,
                         MafNameValuePairT **filter,
                         void * value)
{
        ENTER();
	if (pthread_mutex_lock(&list_lock) != 0) abort();
	MafReturnT com_rc = MafOk;
	MafOamSpiNotificationFmStructT *comNot = (MafOamSpiNotificationFmStructT*)value;
	DEBUG("------ ComAlarm --------\n");
	maf_comSATest_print_severity(comNot->severity);
	DEBUG("dn: \"%s\"\n", comNot->dn);
	DEBUG("addtxt: %s\n", comNot->additionalText);
	DEBUG("majorType %#x\n", comNot->majorType);
	DEBUG("minorType %#x\n", comNot->minorType);
	DEBUG("------------------------\n");
	if (comNot->majorType == outMajorType && comNot->minorType == outMinorType &&
		 strcmp(comNot->dn, COMSANTF_DN)== 0 &&
		 strcmp(comNot->additionalText, addtxt)==0) {
		okReceived++;
	}
	maf_pIf->doneWithValue(NULL, (void*)comNot);
	if (pthread_mutex_unlock(&list_lock) != 0) abort();
	LEAVE();
	return com_rc;
}

static MafReturnT maf_comSATest_registerProducer(MafOamSpiEventProducer_1T * interface, MafOamSpiEventProducerHandleT * handle)
{
        ENTER();
	maf_pIf = interface;
	LEAVE();
	return MafOk;
}

static MafReturnT maf_comSATest_addProducerEvent(MafOamSpiEventProducerHandleT handle, const char * eventType)
{
	 ENTER();
	 LEAVE();
	 return MafOk;
}

static MafReturnT maf_comSATest_getIf( MafMgmtSpiInterface_1T interfaceId, MafMgmtSpiInterface_1T **result)
{
        ENTER();
	*result = (MafMgmtSpiInterface_1T *)&maf_fake_router;
	LEAVE();
	return MafOk;
}

static MafReturnT maf_comSATest_removeProducerEvent(MafOamSpiEventProducerHandleT handle, const char * eventType)
{
	 ENTER();
	 LEAVE();
	 return MafOk;
}

static MafReturnT maf_comSATest_unregisterProducer(MafOamSpiEventProducerHandleT handle, MafOamSpiEventProducer_1T * interface)
{
	 ENTER();
	 LEAVE();
	 return MafOk;
}

static MafReturnT UNUSED_FUNCTION(maf_comSATest_testNotifications)()
{
	ENTER();
	int rv;
	long int rnum = 0;
	char buf[2048], sbuf[2048];
	DEBUG("comSATest_testNotifications");
	MafReturnT com_rv = MafOk;
	ComMgmtSpiInterfacePortal_1T fake_portal_com;
	MafMgmtSpiInterfacePortal_1T fake_portal;
	MafNameValuePairT *filter = NULL;
	fake_portal.getInterface = &maf_comSATest_getIf;

	maf_fake_router.registerProducer = &maf_comSATest_registerProducer;
	maf_fake_router.addProducerEvent = &maf_comSATest_addProducerEvent;
	maf_fake_router.removeProducerEvent = &maf_comSATest_removeProducerEvent;
	maf_fake_router.unregisterProducer = &maf_comSATest_unregisterProducer;
	maf_fake_router.notify = maf_comSATest_notify;
	srandom(getpid());
	rnum = random();
	 /* SelectTimer init; */
	addtxt = malloc(sizeof(COMSANTF_ADD_TEXT)+ 256);
	snprintf(addtxt, sizeof(COMSANTF_ADD_TEXT)+ 256, "%s:%ld", COMSANTF_ADD_TEXT, rnum);
	comSASThandle = timerCreateHandle_r();
	poll_maxfd(comSASThandle, 16);
	printf("START ComA notification test\n");
	DEBUG("Send 4 Al  and 4 sec Al before subscribe\n");
	snprintf(buf, 2048, "ntfsend -r 4 -c %u,%hu,%hu -n \"%s\" -a \"%s:%ld\"",
		inVType, inMaType, inMiType, COMSANTF_NO, COMSANTF_ADD_TEXT,rnum);
	DEBUG(buf);
	snprintf(sbuf, 2048, "ntfsend -r 4 -T0x5000 -c %u,%hu,%hu -n \"%s\" -a \"%s:%ld\"",
		inVType, inMaType, inMiType, COMSANTF_NO, COMSANTF_ADD_TEXT,rnum);
	DEBUG(sbuf);
	rv = system(buf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend Al failed\n");
		com_rv = MafFailure;
		goto end_exit;
	}
	rv = system(sbuf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend sec Al failed\n");
		com_rv = MafFailure;
		goto end_exit;
	}
	DEBUG("Open NTF service IF\n");
	com_rv = maf_ComNtfServiceOpen(&fake_portal_com, &fake_portal);
	if (com_rv != MafOk)
	{
		LOG("COM SA TEST  ComNtfServiceOpen FAILED error = %d\n", com_rv);
		goto end_exit;
	}

	DEBUG("addFilter ComSA notifications\n");
	com_rv = maf_pIf->addFilter(44, NULL, &filter);
	if (com_rv != MafOk)
	{
		LOG("COM SA TEST  addFilter FAILED error = %d\n", com_rv);
		goto end_close_exit;
	}
	DEBUG("Send 4 Al and 4 sec Al after subscribe\n");
	rv = system(buf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend Al failed after subscribtion \n");
		goto end_close_exit;
	}
	rv = system(sbuf);
	if (rv != 0)
	{
		LOG("COM SA TEST ntfsend sec Al failed after subscribtion \n");
		goto end_close_exit;
	}
	poll_execute(comSASThandle);
	DEBUG("Drop out of control-loop\n");
	DEBUG("removeFilter ComSA notifications\n");
	maf_pIf->removeFilter(44, NULL, &filter);
	if (okReceived == expected) {
		LOG("ComSA notification test: test ok\n");
	} else {
		LOG("ComSA notification test: test failed received %d of %d\n",
			okReceived, expected);
		com_rv = MafFailure;
	}
end_close_exit:
	maf_ComNtfServiceClose(&fake_portal_com);
end_exit:
	LEAVE();
	return com_rv;
}

static int maf_comSATest_execute(void* userRef)
{
	ENTER();
	int failed_testcases;
	LOG("comSATest_execute called...");


	if (maf_comSATest_basic() != MafOk)
	{
		LOG("=== REPLICATED LISTS BASIC FAILED ====");
	}
	if (maf_comSATest_itemdata() != MafOk){
	  DEBUG("comSATest_execute error1");
	  return 0;
	}
	if (maf_comSATest_itemaddrem() != MafOk) {
	  DEBUG("comSATest_execute error2");
	  return 0;
	}


		LOG("=== REPLICATED LISTS TESTS PASSED====");

	if (maf_comSATest_traceWrite() != MafOk) {
	  DEBUG("comSATest_execute error3");
	  return 0;
	}
	if (maf_comSATest_traceEnter() != MafOk) {
	  DEBUG("comSATest_execute error4");
	  return 0;
	}
	if (maf_comSATest_traceExit() != MafOk){
	  DEBUG("comSATest_execute error5");
	  return 0;
	}
	LOG("=== TRACE TESTS PASSED ==============");

	if ((failed_testcases = maf_comSATest_log()) == 0)
	{
		LOG("=== LOG TESTS PASSED ===============");
	}
	else
	{
		LOG("=== LOG TESTS FAILED WITH %d FAILURES==", failed_testcases);
		return 0;
	}
/*
	if (comSATest_testNotifications() != MafOk)
	{
		LOG("=== NOTIFICATION/ALARM TESTS FAILED ===");
		return 0;
	}
*/
	LOG("======== ALL TESTS PASSED ===========");
	LEAVE();
	return 0;
}

