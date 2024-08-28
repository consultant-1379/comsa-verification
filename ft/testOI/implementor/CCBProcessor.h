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
 * Author: epkadsz
 * Reviewed: erannjn
*/

#ifndef CCBPROCESSOR_H_
#define CCBPROCESSOR_H_

#include <saAis.h>
#include <saImmOm.h>
#include <saImmOi.h>

/*
* Sets the Oi handle
* @param objectImplementorHandle the handle set by IMM Agent.
*/
void setProcessorOiHandle(SaImmOiHandleT objectImplementorHandle);

/**
 * Checks correctness of ioHandle from IMM call-back invoker.
 */
int checkOiHandle(SaImmOiHandleT ioHandleCandidate);

/**
 * Process the attributes initially retreived from IMM.
 * @param attributes all attributes for the object.
 **/
void processAttributes(SaImmAttrValuesT_2 **attributes, const SaNameT *objectName);

/** Commits any pending changes. */
void commit();

/**
 * Forward declaration of IMM callback functions.
 */
void handleAdminOperation(SaImmOiHandleT immOiHandle, SaInvocationT invocation, const SaNameT *objectName, SaImmAdminOperationIdT operationId, const SaImmAdminOperationParamsT_2 **params);

SaAisErrorT handleCcbModification(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId, const SaNameT *objectName, const SaImmAttrModificationT_2 **attrMods);

SaAisErrorT handleRtAttrUpdate(SaImmOiHandleT immOiHandle, const SaNameT *objectName, const SaImmAttrNameT *attributeNames);

SaAisErrorT handleCcbDeleteObject(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId, const SaNameT *objectName);

SaAisErrorT handleCcbCreateObject(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId, const SaImmClassNameT className, const SaNameT *parentName, const SaImmAttrValuesT_2 **attr);

SaAisErrorT handleCcbComplete(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId);
void handleCcbApply(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId);
void handleCcbAbort(SaImmOiHandleT immOiHandle, SaImmOiCcbIdT ccbId);

/**
 * Creates a call-back structure with all registered function pointers for handling callback from IMM
 */
SaImmOiCallbacksT_2 createCallbackStruct();


#endif /* CCBPROCESSOR_H_ */
