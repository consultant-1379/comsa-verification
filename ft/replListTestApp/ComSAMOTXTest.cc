/*
 *   Include files   Copyright (C) 2010 by Ericsson AB
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
 *   File:   OamSAManagedObjects.cc
 * 
 *   Author: efaiami & egorped
 * 
 *   Date:   2010-06-02
 *
 *   Function test for MOTX
 *
 *   Modified: xnikvap 2012-08-30  support for COM MO SPI Ver.3 (Ver.1 is not supported any more)
 */

#include "OamSAManagedObjects.h"
#include "ComOamSpiTransaction_1.h"
#include "OamSATransactionalResource.h"
#include "ComOamSpiModelRepository_1.h"
#include "ComMgmtSpiInterfacePortal_1.h"
#include <stdio.h>
#include "trace.h"

// To avoid linking problem
ComMgmtSpiInterfacePortal_1T* portal = NULL;

ComReturnT registerParticipant(ComOamSpiTransactionHandleT txHandle, 
			        ComOamSpiTransactionalResource_1T * resp)
{
	return ComOk;
}

ComReturnT setContext(ComOamSpiTransactionHandleT txHandle, 
			ComOamSpiTransactionalResource_1T *resource, void *context)
{
	return ComOk;
}

ComReturnT getContext(ComOamSpiTransactionHandleT txHandle, 
			ComOamSpiTransactionalResource_1T *resource, void **context)
{
		return ComOk;
}

ComReturnT getLockPolicy(ComOamSpiTransactionHandleT txHandle, ComLockPolicyT *result)
{
		return ComOk;
}

ComOamSpiTransaction_1T  type = { {"","",""}, registerParticipant, setContext, getContext, getLockPolicy};

ComOamSpiTransaction_1*	ComOamSpiTransactionStruct_p = &type;



/**
 * MO
 */
ComReturnT testRetrievesAttr(ComOamSpiTransactionHandleT theHandle, const char *dn, const char *attributeName);
ComReturnT testCreateAttr(ComOamSpiTransactionHandleT theHandle, const char *parentDn,
			   const char *className, const char *keyAttributeName,
				const char *keyAttributevalue);
ComReturnT testDeleteAttr(ComOamSpiTransactionHandleT theHandle, const char *dn);
ComReturnT testsetMoAttribute(ComOamSpiTransactionHandleT theHandle, const char *dn, 
				const char *attributeName, const ComMoAttributeValueContainerT *attributeValue);
/**
 * TX
 */
ComReturnT testJoin(ComOamSpiTransactionHandleT theHandle);
ComReturnT testPrepare(ComOamSpiTransactionHandleT theHandle);
ComReturnT testCommit(ComOamSpiTransactionHandleT theHandle);
ComReturnT testAbort(ComOamSpiTransactionHandleT theHandle);
ComReturnT testFinish(ComOamSpiTransactionHandleT theHandle);

int main(int argc, char* argv[])
{
	ComMoAttributeValueContainerT*  ValueContainer = new ComMoAttributeValueContainerT;
	ComReturnT retVal = ComOk;
	struct log_state_t log;
	int theTxHandle;
	int input=0;
	log.level = LOG_LEVEL_DEBUG;
	log.tags = TRACE_TAG_LOG | TRACE_TAG_ENTER | TRACE_TAG_LEAVE;
	log.mode = LOG_MODE_FILE | LOG_MODE_FILELINE | LOG_MODE_TIMESTAMP;
	log_control( &log, 0 );
	log_to_file("logfilemotx.txt");
	log_init("ComSAMOTXTest");

	LOG_PRINTF(LOG_LEVEL_DEBUG,"ComSAMOTXTest starting........\n");

  	do
	{
		printf("1 = join, 2 = prepare, 3 = commit, 4 = abort, 5 = finish, 6 = createMo, 7 = deleteMo, 8 = setMo, 9 = getMo, 0 = exit\n");
		scanf("%d",&input);
		switch (input)
		{
			case 1:
				printf("txHandle = ");
				scanf("%d",&theTxHandle);
				retVal = testJoin(theTxHandle);
				if(retVal == ComOk){
					printf("Call to join OK\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to join OK\n");
				}
				else {
					printf("Call to join failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to join failed\n");
				}
				break;
			case 2:
				retVal = testPrepare(theTxHandle);
				if(retVal == ComOk){
					printf("Call to prepare OK\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to prepare OK\n");
				}
				else {
					printf("Call to prepare failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to prepare failed\n");
				}
				break;
			case 3:
				retVal = testCommit(theTxHandle);
				if(retVal == ComOk){	
					printf("Call to commit OK\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to commit OK\n");
				}
				else {
					printf("Call to commit failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to commit failed\n");
				}
				break;
			case 4:
				retVal = testAbort(theTxHandle);
				if(retVal == ComOk){	
					printf("Call to abrot OK\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to abrot OK\n");
				}
				else {
					printf("Call to abrot failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to abrot failed\n");
				}
				break;
			case 5:
				retVal = testFinish(theTxHandle);
				if(retVal == ComOk){
					printf("Call to finish OK\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to finish OK\n");
				}
				else {
					printf("Call to finish failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to finish failed\n");
				}
				break;
			case 6:
				retVal = testCreateAttr(theTxHandle, "", "Splortf", "TransportId","CPND5");
				if(retVal == ComOk){
					printf("Call to createMo ok\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to createMo ok\n");
				}
				else {
					printf("Call to createMo failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to createMo failed\n");
				}
				break;
			case 7:
				retVal = testDeleteAttr(theTxHandle,"Splortf.CPND5");
				if(retVal == ComOk){
					printf("Call to delete OK\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to delete OK\n");
				}
				else {
					printf("Call to delete failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Call to delete failed\n");
				}
				break;
			case 8:
				ValueContainer->type = ComOamSpiMoAttributeType_STRING;
				ValueContainer->nrOfValues = 1 ;
				ValueContainer->values = new ComMoAttributeValue;
				ValueContainer->values->value.theString = "something else";
				retVal = testsetMoAttribute(theTxHandle,"Splort.CPND4", "userLabel", ValueContainer);
				if(retVal == ComOk){
					printf("Test case for set an attribute OK\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Test case for set an attribute OK\n");
				}
				else {
					printf("Test case for set an attribute failed\n");
					LOG_PRINTF(LOG_LEVEL_DEBUG,"Test case for set an attribute failed\n");
				}
				break;
			case 9:
				printf("9 = getMo\n");
				break;
			default:
				printf("default set input = 0\n");
				input = 0;
				break;
		}
	}while(input!=0);

	delete ValueContainer;

	return 0;
}


/**
 * TX
 */

ComReturnT testJoin(ComOamSpiTransactionHandleT theHandle)
{
	ComOamSpiTransactionalResource_1T* theRI = ExportOamSATransactionalResourceInterface();
	return  theRI->join(theHandle); 
}

ComReturnT testPrepare(ComOamSpiTransactionHandleT theHandle)
{
	ComOamSpiTransactionalResource_1T* theRI = ExportOamSATransactionalResourceInterface();
	return theRI->prepare(theHandle);
}

ComReturnT testCommit(ComOamSpiTransactionHandleT theHandle)
{
	ComOamSpiTransactionalResource_1T* theRI = ExportOamSATransactionalResourceInterface();
	return theRI->commit(theHandle);
			
}

ComReturnT testAbort(ComOamSpiTransactionHandleT theHandle)
{
	ComOamSpiTransactionalResource_1T* theRI = ExportOamSATransactionalResourceInterface();
	return theRI->abort(theHandle);
			
}

ComReturnT testFinish(ComOamSpiTransactionHandleT theHandle)
{
	ComOamSpiTransactionalResource_1T* theRI = ExportOamSATransactionalResourceInterface();
	return theRI->finish(theHandle);
}

/**
 * MO
 */

ComReturnT testCreateAttr(ComOamSpiTransactionHandleT theHandle, const char *parentDn,
			   const char *className, const char *keyAttributeName,
				const char *keyAttributevalue)
{
	ComOamSpiManagedObject_3T* theMO = ExportOamManagedObjectInterface();
	return theMO->createMo(theHandle, parentDn, className, keyAttributeName, keyAttributevalue);
}


		
ComReturnT testsetMoAttribute(ComOamSpiTransactionHandleT theHandle, const char *dn, 
				const char *attributeName, const ComMoAttributeValueContainerT *attributeValue)
{
		
	ComOamSpiManagedObject_3T* theMO = ExportOamManagedObjectInterface();
	return theMO->setMoAttribute(theHandle, dn, attributeName, attributeValue);
}

ComReturnT testDeleteAttr(ComOamSpiTransactionHandleT theHandle, const char *dn)
{
		
	ComOamSpiManagedObject_3T* theMO = ExportOamManagedObjectInterface();
	return theMO->deleteMo(theHandle, dn);
}
