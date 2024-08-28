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
* Author: qjalars
* Reviewed: -
*/
#include <string>
#include <unistd.h>
#include <syslog.h>
#include <stdlib.h>
#include <string.h>

#include "trace.h"
#include <saImmOi.h>
#include <saImmOm.h>

SaNameT * toSaNameT(const char *dnIn)
{
    // temp SaNameTs are deleted in destructor
    SaNameT * dn = NULL;
    if (strlen (dnIn) > 0) {
        dn = new SaNameT();
        dn->length = strlen (dnIn);
        snprintf((char*)(dn->value), SA_MAX_NAME_LENGTH,"%s", dnIn);
    }
    return dn;
}

void start()
{
  SaImmHandleT immHandle;
  SaAisErrorT err = SA_AIS_OK;
  SaVersionT version = { 'A', 2, 1 };

  //
  // Om Initialize
  //   
  syslog(LOG_INFO, "saImmOmInitialize");
  err = saImmOmInitialize(&immHandle/*out*/, 
                          NULL, 
                          &version);

  if (err != SA_AIS_OK) {
    syslog(LOG_INFO, "saImmOmInitialize returned error %d", err);
    return;
  }

  //
  // Admin Owner Initialize
  //   
  syslog(LOG_INFO, "saImmOmAdminOwnerInitialize");
  SaImmAdminOwnerHandleT mAdminOwnerHandle;
  err = saImmOmAdminOwnerInitialize(immHandle, 
                                    (char*) "KalleAnka",
                                    SA_TRUE, 
                                    &mAdminOwnerHandle/*out*/);

  if (err != SA_AIS_OK) {
    syslog(LOG_INFO, "saImmOmAdminOwnerInitialize returned error %d", err);
    return;
  }

  //
  // Admin Owner Set
  //   
  SaNameT *objectName = toSaNameT ("actionApplId=1,authenticationId=1");
  const SaNameT* dnsList[] = {objectName, 0};
  syslog(LOG_INFO, "saImmOmAdminOwnerSet");
  err = saImmOmAdminOwnerSet(mAdminOwnerHandle,
                             dnsList, 
                             SA_IMM_ONE);  // SA_IMM_ONE, SA_IMM_SUBLEVEL, SA_IMM_SUBTREE


  syslog(LOG_INFO, "1");
  //
  // Admin Operation Invoke
  //   
  SaImmAdminOperationIdT operationId = 2;
  SaAisErrorT operationReturnValue;
  SaImmAdminOperationParamsT_2 *opParam = new SaImmAdminOperationParamsT_2[2];
  SaImmAdminOperationParamsT_2** opPP = new SaImmAdminOperationParamsT_2*[3];

  unsigned int par0 = 1;	
  char parName0[9];
  strcpy(parName0, "opParam");

  syslog(LOG_INFO, "2");
  opParam[0].paramName = parName0;
  opParam[0].paramType = SA_IMM_ATTR_SAUINT32T;  
  opParam[0].paramBuffer = (void*)&par0;
  opPP[1] = &opParam[0];

  char parName1[9];
  strcpy(parName1, "returnParam");
 
  syslog(LOG_INFO, "3");
  unsigned int par1 = 2;	
  opParam[1].paramName = parName1;
  opParam[1].paramType = SA_IMM_ATTR_SAUINT32T; 
  opParam[1].paramBuffer = (void*)&par1;
  opPP[0] = &opParam[1];

  opPP[2] = NULL;
 
  syslog(LOG_INFO, "calling saImmOmAdminOperationInvoke_2");
  err = saImmOmAdminOperationInvoke_2(mAdminOwnerHandle, 
                                      objectName, 
                                      0,  /* continuationId */
                                      operationId, 
                                      (const SaImmAdminOperationParamsT_2 **)opPP,
                                      &operationReturnValue, 
                                      SA_TIME_MAX  /* timeout */ );
 
  if (err != SA_AIS_OK) {
    syslog(LOG_INFO, "saImmOmAdminOperationInvoke_2 returned error %d", err);
    return;
  }
   
  syslog(LOG_INFO, "saImmOmAdminOperationInvoke_2 return value = %d", operationReturnValue);

}

int main(int argc, char **argv)
{
	Trace::init();	//In order to able to use trace functionality
	syslog(LOG_INFO, "admintest started");
	openlog(NULL, LOG_PERROR, LOG_USER);

	syslog(LOG_INFO, "admintest started");

	start();

//	while (1)
		/* Keep waiting forever */
//		sleep(-1);

	return 0;    
}

