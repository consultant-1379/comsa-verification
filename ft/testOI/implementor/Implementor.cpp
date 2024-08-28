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
* Reviewed: ? 2010-?-?
* Modified: eozasaf 2011-07-25 Parameterized MO class name(s) and IMM OM related things
*
*/

#include <stdlib.h>
#include <errno.h>
#include <poll.h>
#include <pthread.h>

#include <saAis.h>
#include <saImmOm.h>
#include <saImmOi.h>
#include <time.h>

#include "CCBProcessor.h"
#include "constants.h"
#include "immutil.h"

#include "Implementor.h"
#include "trace.h"

extern struct ImmutilWrapperProfile immutilWrapperProfile;

/** Handle for immOi part */
SaImmOiHandleT objectImplementorHandle;
SaSelectionObjectT selectionObject;

/** Thread reference. */
pthread_t thread;

/* global variables */
bool volatile implementor_exit_thread = false;
/* This global variable makes it possible for the thread to terminate itself.*/

char** class_names=NULL;
int noOfClasses=0;
/**
 * Initialize the implementor.
 */
SaAisErrorT init_imm()
{
	TRACE_INFO("init_imm\n");

	SaAisErrorT error = SA_AIS_OK;

	const SaImmOiCallbacksT_2 callBackStructem = createCallbackStruct();
	const SaImmOiCallbacksT_2 *callBackStruct = &callBackStructem;

	SaVersionT ver = { 'A', 2, 11 };

	if ((error = immutil_saImmOiInitialize_2(&objectImplementorHandle, callBackStruct, &ver)) != SA_AIS_OK) {
		TRACE_ERROR("saImmOiInitialize failed %u", error);
		goto done;
	}

	setProcessorOiHandle(objectImplementorHandle);

	if ((error = immutil_saImmOiSelectionObjectGet(objectImplementorHandle, &selectionObject)) != SA_AIS_OK) {
		TRACE_ERROR("saImmOiSelectionObjectGet failed %u", error);
		goto done;
	}

	//associate the implementer name with the oihandle
	error = immutil_saImmOiImplementerSet(objectImplementorHandle, (char*)IMPLEMENTOR_NAME);
	if (error != SA_AIS_OK) {
		TRACE_ERROR("error - saImmOiImplementerSet FAILED: %s\n", saf_error(error));
		exit(EXIT_FAILURE);
	}

	for(int i=0;i<noOfClasses;i+=1)
	{
		syslog(LOG_INFO,"Class %d: %s",i+1,class_names[i]);
		error = immutil_saImmOiClassImplementerSet(objectImplementorHandle, class_names[i]);
		if (error != SA_AIS_OK) {
			TRACE_ERROR("error - saImmOiClassImplementerSet FAILED for class %s: %s\n", class_names[i], saf_error(error));
			exit(EXIT_FAILURE);
		}
	}

	TRACE_INFO("Successfully initialized IMM\n");

done:
	return error;
}

/**
 * Dispatches the calls from IMM.
 */
void dispatch()
{
	SaAisErrorT rc;
	struct pollfd fds[1];
	fds[0].fd = selectionObject;
	fds[0].events = POLLIN;

	/*
	 * This is the dispatcher loop, it should exit only when the implementor is stopped
	 */
	while (!implementor_exit_thread)
	{
		int res = poll(fds, 1, 20); /* return 0 if timed out */

		if (res == -1)
		{
			if (errno == EINTR)
				continue;
			else
			{
				syslog(LOG_ERR, "poll FAILED - %s", strerror(errno));
				exit(1);
			}
		}

		if (fds[0].revents & POLLIN)
		{
			/* There is an Implementor callback waiting to be be processed. Process it */
			TRACE_INFO("Dispatching from IMM.");
			rc = saImmOiDispatch(objectImplementorHandle, SA_DISPATCH_ONE);
			if (SA_AIS_OK != rc)
			{
				TRACE_ERROR("saImmOiDispatch FAILED %u", rc);
				exit(1);
				break;
			}
		}
	}

	TRACE_INFO("Stopping dispatching\n");
	implementor_terminate();
	pthread_exit(NULL);
}

/**
 * Detaches from IMM agent by finalizing the different handles and removing the implementor.
 **/
void finalize()
{
	SaAisErrorT error;
    	//immutil_saImmOiImplementerClear, considered as not needed to clear the implementor name
    	TRACE_INFO("saImmOiClassImplementerRelease\n");
    	for(int i=0;i<noOfClasses;i+=1)
    	{
    		syslog(LOG_INFO,"Class %d: %s",i+1,class_names[i]);
    		error = immutil_saImmOiClassImplementerRelease(objectImplementorHandle, class_names[i]);
    		if (error != SA_AIS_OK) {
    			TRACE_ERROR("error - saImmOiClassImplementerRelease FAILED for class %s: %s\n",class_names[i], saf_error(error));
    			exit(EXIT_FAILURE);
    		} else {
    			TRACE_INFO("saImmOiClassImplementerRelease\n");
    		}
    	}

	TRACE_INFO("saImmOiFinalize\n");
	error = immutil_saImmOiFinalize(objectImplementorHandle);

	if (error != SA_AIS_OK) {
		TRACE_ERROR("error - saImmOiFinalize FAILED: %s\n", saf_error(error));
		exit(EXIT_FAILURE);
	}
}

/**
 * Thread starting for implementor.
 */
static void *cmp_thread_start (void* dummy)
{
	init_imm();

	dispatch();

	return NULL;
}

int implementor_init(char** classes,int count)
{
	TRACE_INFO("starting thread implementor thread");

	class_names=classes;
	noOfClasses=count;

	int rc;

	implementor_exit_thread = false;

	/* Create handle command interface task */
	rc = pthread_create(&thread, NULL, cmp_thread_start, NULL);
	if (rc != 0)
		syslog(LOG_ERR, "pthread_create FAILED - %s", strerror(errno));

	return rc;
}

/* called from AMF thread */
int implementor_stop(void)
{
	TRACE_INFO("if started - implementor thread will be stopped");

	//Signal to currently running thread
	implementor_exit_thread = true;

	if (thread)
		pthread_join (thread, NULL);

	return 0;
}

int implementor_terminate()
{
	TRACE_INFO("Cleaning up implementor thread before exiting");

	finalize();
	return 0;
}
