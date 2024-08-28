/*
 * Copyright (C) 2010 by Ericsson AB
 * S - 125 26  STOCKHOLM
 * SWEDEN, tel int + 46 10 719 0000
 *
 * The copyright to the computer program herein is the property of
 * Ericsson AB. The program may be used and/or copied only with the
 * written permission from Ericsson AB, or in accordance with the terms
 * and conditions stipulated in the agreement/contract under which the
 * program has been supplied.
 *
 * All rights reserved.
 *
 * Author: qjalars
 * Reviewed: -
 * Modified: eozasaf 2011-07-22 add handleCcbAbort(), handleCcbApply(),	handleCcbComplete(),
 * 								handleCcbCreateObject(), handleCcbDeleteObject(), handleCcbModification(),
 * 								handleRtAttrUpdate() IMM callback functions
 *
 */

#include <stdio.h>
#include <saAis.h>
#include <saImmOm.h>
#include <saImmOi.h>
#include "CCBProcessor.h"
#include "constants.h"
#include "trace.h"
#include "immutil.h"

SaImmOiHandleT oiHandle;


static void DebugDumpOperationParams( const SaImmAdminOperationParamsT_2 * const ctp)
{
	TRACE_INFO("Parameters:");
	TRACE_INFO("Name = %s", ctp->paramName);

	switch (ctp->paramType)
	{
	case SA_IMM_ATTR_SAINT32T:
		{
		TRACE_INFO("Type = SA_IMM_ATTR_SAINT32T");
		int *tmpI;
		tmpI = (int *)ctp->paramBuffer;
		TRACE_INFO("Value = %d", *tmpI);
		break;
		}
	case SA_IMM_ATTR_SAUINT32T:
		{
		TRACE_INFO("Type = SA_IMM_ATTR_SAUINT32T");
		unsigned int *tmpUi;
		tmpUi = (unsigned int *)ctp->paramBuffer;
		TRACE_INFO("Value = %d", *tmpUi);
		break;
		}
	case SA_IMM_ATTR_SAINT64T:
		TRACE_INFO("Type = SA_IMM_ATTR_SAINT64T");
		break;
	case SA_IMM_ATTR_SAUINT64T:
		TRACE_INFO("Type = SA_IMM_ATTR_SAUINT64T");
		break;
	case SA_IMM_ATTR_SASTRINGT:
		TRACE_INFO("Type = SA_IMM_ATTR_SASTRINGT");
		break;
	case SA_IMM_ATTR_SATIMET:
		TRACE_INFO("Type = SA_IMM_ATTR_SATIMET");
		break;
	case SA_IMM_ATTR_SANAMET:
		TRACE_INFO("Type = SA_IMM_ATTR_SANAMET");
		break;
	case SA_IMM_ATTR_SAFLOATT:
		TRACE_INFO("Type = SA_IMM_ATTR_SAFLOATT");
		break;
	case SA_IMM_ATTR_SADOUBLET:
		TRACE_INFO("Type = SA_IMM_ATTR_SADOUBLET");
		break;
	case SA_IMM_ATTR_SAANYT:
		TRACE_INFO("Type = SA_IMM_ATTR_SAANYT");
		break;
	}

}

/*
* Sets the Oi handle
* @param objectImplementorHandle the handle set by IMM Agent.
*/
void setProcessorOiHandle(SaImmOiHandleT objectImplementorHandle)
{
	oiHandle = objectImplementorHandle;
}

/**
 * Checks correctness of ioHandle from IMM callback invoker.
 */
int checkOiHandle(SaImmOiHandleT ioHandleCandidate)
{
  if (ioHandleCandidate != oiHandle) {
    TRACE_ERROR ("checkOiHandle failed");
    return -1;
  }

  return 0;
}


/**
 * Handles administrative operations.
 */
void handleAdminOperation(SaImmOiHandleT immOiHandle, SaInvocationT invocation, const SaNameT *objectName,
				SaImmAdminOperationIdT operationId, const SaImmAdminOperationParamsT_2 **params)
{
	SaAisErrorT rc = SA_AIS_OK;
	TRACE_INFO("ErrorStringTestOIAppl SaImmOiAdminOperationCallbackT_2 ");
	TRACE_INFO("operationId=%llu", operationId);

	if (params != NULL) {
		for (int i = 0; params[i] != NULL; i++)
		{
			DebugDumpOperationParams(params[i]);

			if (operationId == 999 && i==0 && params[i]->paramBuffer != NULL) {
				rc = *((SaAisErrorT *) params[i]->paramBuffer);
			}
		}
	} else {
		TRACE_INFO("No parameters");
	}

	TRACE_INFO("ReturnParam=%d", rc);

	rc = saImmOiAdminOperationResult(immOiHandle, invocation, rc);

	if (SA_AIS_OK != rc)
	{
		TRACE_ERROR("saImmOiAdminOperationResult FAILED %u", rc);
	}
}

/**
 * All ccb changes are completed and ready for validation.
 * Returning OK indicates that the proposed changed are ok to apply.
 */
SaAisErrorT handleCcbComplete(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId)
{
	TRACE_INFO("handleCcbComplete() entered");

#ifdef ErrorStringTest
	TRACE_INFO("CCB Id: %u",ccbId);
	TRACE_INFO("Calling saImmOiCcbSetErrorString() in handleCcbComplete()");
	SaStringT errorText=(char*)"@CoMNbi@forced ERROR: handleCcbComplete()";
	SaAisErrorT errorCode=saImmOiCcbSetErrorString(immOiHandle,ccbId, errorText);
	TRACE_INFO("Error code returned by saImmOiCcbSetErrorString(): %d",errorCode);
	return SA_AIS_ERR_NO_OP;
#endif

	int ret = checkOiHandle(immOiHandle);
	if(ret!=0)
	{
		TRACE_ERROR ("handleCcbComplete, checkOiHandle returned %d", ret);
		return SA_AIS_ERR_INVALID_PARAM;
	}

	SaAisErrorT rc = SA_AIS_OK;
	struct CcbUtilCcbData *ccbUtilCcbData;
	struct CcbUtilOperationData *ccbUtilOperationData;
	const SaImmAttrModificationT_2 *attrMod;
	if ((ccbUtilCcbData = ccbutil_findCcbData(ccbId)) == NULL) {
		TRACE_ERROR("Failed to find CCB object for %llu", ccbId);
		rc = SA_AIS_ERR_BAD_OPERATION;
		goto done;
	}

	/*
	 ** "check that the sequence of change requests contained in the CCB is
	 ** valid and that no errors will be generated when these changes
	 ** are applied."
	 */
	ccbUtilOperationData = ccbUtilCcbData->operationListHead;
	for(int i=0; ccbUtilOperationData != NULL; ccbUtilOperationData = ccbUtilOperationData->next)
	{
	   if(ccbUtilOperationData->param.modify.attrMods!=NULL) //create or modify
	   {
		   if(ccbUtilOperationData->param.create.attrValues!=NULL)
			   TRACE_INFO("Create %s", ccbUtilOperationData->param.create.className);
		   else TRACE_INFO("Change %s", ccbUtilOperationData->param.modify.objectName->value);

		   attrMod = ccbUtilOperationData->param.modify.attrMods[i++];

		   for (;attrMod != NULL; attrMod = ccbUtilOperationData->param.modify.attrMods[i++])
		   {
			   const SaImmAttrValuesT_2 *attribute = &attrMod->modAttr;
			   TRACE_INFO("attribute %s", attribute->attrName);

			   if (attribute->attrValuesNumber == 0) {
				   rc = SA_AIS_ERR_BAD_OPERATION;
				   goto done;
			   }
		   }
	   }
	   else TRACE_INFO("Delete %s",ccbUtilOperationData->param.deleteOp.objectName->value);
	}

	done:
	TRACE_INFO("handleCcbComplete() exited with return code: %d",rc);
	return rc;
}
/**
 * Commits the actual CCB changes by invoking the environment adapter.
 */
void handleCcbApply(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId)
{
	TRACE_INFO("handleCcbApply() entered");

#ifdef ErrorStringTest
	TRACE_INFO("CCB Id: %u",ccbId);
	TRACE_INFO("Calling saImmOiCcbSetErrorString() in handleCcbApply()");
	SaStringT errorText=(char*)"@CoMNbi@forced ERROR: handleCcbApply()";
	SaAisErrorT errorCode=saImmOiCcbSetErrorString(immOiHandle,ccbId, errorText);
	TRACE_INFO("Error code returned by saImmOiCcbSetErrorString(): %d",errorCode);
#endif

	//dispose the ccb identifier
	if (checkOiHandle(immOiHandle) == 0)
	{
		/* Return CCB container memory */
		CcbUtilCcbData_t *ccb_util_ccb_data = ccbutil_findCcbData(ccbId);
		ccbutil_deleteCcbData(ccb_util_ccb_data);
	}
	else
	{
		TRACE_INFO("handleCcbApply() - checkOiHandle failed");
	}
	TRACE_INFO("handleCcbApply() exited");
}

/**
 * The proposed changes are not accepted. Remove the allocated holder object.
 * @param immOiHandle the oihandle
 * @param ccbId ccb identifier
 */
void handleCcbAbort(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId)
{
	TRACE_INFO("handleCcbAbort() entered");
	//dispose the ccb identifier
	if (checkOiHandle(immOiHandle) == 0)
	{
		CcbUtilCcbData_t *ccb_util_ccb_data;

		/* Return CCB container memory */
		ccb_util_ccb_data = ccbutil_findCcbData(ccbId);
		//assert(ccb_util_ccb_data);
		ccbutil_deleteCcbData(ccb_util_ccb_data);
	} else {
		TRACE_INFO("handleCcbAbort() - checkOiHandle failed");
	}
	TRACE_INFO("handleCcbAbort() exited");
}

/**
 * Handles create call-backs.
 * @param immOiHandle the handle of this processor
 * @param ccbId the configuration change bundle identifier.
 */
SaAisErrorT handleCcbCreateObject(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId, const SaImmClassNameT className, const SaNameT *parentName, const SaImmAttrValuesT_2 **attr)
{
  SaAisErrorT rc = SA_AIS_OK;
  TRACE_INFO("handleCcbCreateObject() entered");
#ifdef ErrorStringTest
  TRACE_INFO("CCB Id: %u",ccbId);
  TRACE_INFO("Calling saImmOiCcbSetErrorString() in handleCcbCreateObject()");
  SaStringT errorText=(char*)"@CoMNbi@forced ERROR: handleCcbCreateObject()";
  SaAisErrorT errorCode=saImmOiCcbSetErrorString(immOiHandle,ccbId, errorText);
  TRACE_INFO("Error code returned by saImmOiCcbSetErrorString(): %d",errorCode);
  return SA_AIS_ERR_NO_OP;
#endif

  CcbUtilCcbData_t *ccb_util_ccb_data;
  CcbUtilOperationData_t *operation;
  int i = 0;
  const SaImmAttrValuesT_2 *attrValue;

	if ((ccb_util_ccb_data = ccbutil_getCcbData(ccbId)) == NULL) {
	  TRACE_ERROR ("handleCcbCreateObject SA_AIS_ERR_NO_MEMORY");
		rc = SA_AIS_ERR_NO_MEMORY;
		goto done;
	}

	//add operation to the CCB change
	operation = ccbutil_ccbAddCreateOperation(ccb_util_ccb_data, className, parentName, attr);

	if (operation == NULL) {
		TRACE_ERROR ("handleCcbCreateObject operation null, SA_AIS_ERR_NO_MEMORY");
		rc = SA_AIS_ERR_NO_MEMORY;
		goto done;
	}

	/* Find the RDN attribute and store the object DN */
	while ((attrValue = attr[i++]) != NULL && attrValue->attrValues != NULL) {
		if (attrValue->attrValueType == SA_IMM_ATTR_SASTRINGT) {
			SaStringT rdnVal = *((SaStringT *)attrValue->attrValues[0]);
			if ((parentName != NULL) && (parentName->length > 0)) {
				operation->objectName.length = sprintf((char *)operation->objectName.value,
						"%s,%s", rdnVal, parentName->value);
			} else {
				operation->objectName.length = sprintf((char *)operation->objectName.value,
						"%s", rdnVal);
			}
		} else {
			SaNameT *rdnVal = ((SaNameT *)attrValue->attrValues[0]);
			operation->objectName.length = sprintf((char *)operation->objectName.value,
				"%s,%s", rdnVal->value, parentName->value);
		}
	}

done:
	TRACE_INFO("handleCcbCreateObject() exited with return code: %d",rc);
	return rc;

}

SaAisErrorT handleCcbDeleteObject(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId, const SaNameT *objectName)
{
	SaAisErrorT rc = SA_AIS_OK;
	TRACE_INFO("handleCcbDeleteObject() entered");
#ifdef ErrorStringTest
  TRACE_INFO("CCB Id: %u",ccbId);
  TRACE_INFO("Calling saImmOiCcbSetErrorString() in handleCcbDeleteObject()");
  SaStringT errorText=(char*)"@CoMNbi@forced ERROR: handleCcbDeleteObject()";
  SaAisErrorT errorCode=saImmOiCcbSetErrorString(immOiHandle,ccbId, errorText);
  TRACE_INFO("Error code returned by saImmOiCcbSetErrorString(): %d",errorCode);
  return SA_AIS_ERR_NO_OP;
#endif

	struct CcbUtilCcbData *ccb_util_ccb_data;

	if ((ccb_util_ccb_data = ccbutil_getCcbData(ccbId)) != NULL) {
		/* "memorize the request" */
		ccbutil_ccbAddDeleteOperation(ccb_util_ccb_data, objectName);
	} else {
		rc = SA_AIS_ERR_NO_MEMORY;
	}
    TRACE_INFO("handleCcbDeleteObject() exited with return code: %d",rc);
    return rc;
}

SaAisErrorT handleCcbModification(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId, const SaNameT *objectName, const SaImmAttrModificationT_2 **attrMods)
{
	SaAisErrorT rc = SA_AIS_OK;
	TRACE_INFO("handleCcbModification() entered");
#ifdef ErrorStringTest
  TRACE_INFO("CCB Id: %u",ccbId);
  TRACE_INFO("Calling saImmOiCcbSetErrorString() in handleCcbModification()");
  SaStringT errorText=(char*)"@CoMLog@forced ERROR: handleCcbModification()";
  SaAisErrorT errorCode=saImmOiCcbSetErrorString(immOiHandle,ccbId, errorText);
  TRACE_INFO("Error code returned by saImmOiCcbSetErrorString(): %d",errorCode);
  return SA_AIS_ERR_NO_OP;
#endif

  if (checkOiHandle(immOiHandle) == 0)
  {
	  struct CcbUtilCcbData *ccb_util_ccb_data;

	  if ((ccb_util_ccb_data = ccbutil_getCcbData(ccbId)) != NULL) {
		  /* "memorize the request" */
		  if (ccbutil_ccbAddModifyOperation(ccb_util_ccb_data, objectName, attrMods) != 0) {
			  rc = SA_AIS_ERR_BAD_OPERATION;
		  }
	  } else {
		  rc = SA_AIS_ERR_NO_MEMORY;
	  }
	  TRACE_INFO("handleCcbModification() exited with return code: %d",rc);
	  return rc;

  }
  TRACE_INFO("handleCcbModification() exited with return code: 20 SA_AIS_ERR_BAD_OPERATION");
  return SA_AIS_ERR_BAD_OPERATION;
}

/**
 * Not used and not implemented.
 **/
SaAisErrorT handleRtAttrUpdate(SaImmOiHandleT immOiHandle, const SaNameT *objectName, const SaImmAttrNameT *attributeNames)
{
	return SA_AIS_OK;
}

/**
 * Creates a callback structure with all registered function pointers for handling call-backs from IMM
 */
SaImmOiCallbacksT_2 cbFunctions = {
	//holder will all the registered functions
	handleAdminOperation,
	handleCcbAbort,
	handleCcbApply,
	handleCcbComplete,
	handleCcbCreateObject,
	handleCcbDeleteObject,
	handleCcbModification,
	handleRtAttrUpdate
};

SaImmOiCallbacksT_2 createCallbackStruct()
{
	return cbFunctions;
}
