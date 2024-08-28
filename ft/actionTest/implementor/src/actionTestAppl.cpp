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
#include <unistd.h>
#include <syslog.h>
#include <stdlib.h>
#include <string.h>

#include "trace.h"
#include "dump.h"
#include "implementor/Implementor.h"

/*
 * Controllable functions.
 */
int manageStart();
int manageStop();
int manageTerminate();

int main(int argc, char **argv)
{
	Trace::init();	//In order to able to use trace functionality
	Dump::init();   //In order to able to use dump functionality

	syslog(LOG_INFO, "actionTestAppl started");
	openlog(NULL, LOG_PERROR, LOG_USER);

	TRACE_INFO("actionTestAppl started");

	manageStart();

	while (1)
		/* Keep waiting forever */
		sleep(-1);

	return 0;
}

/**
 * Manages start of this component and all subsystems.
 */
int manageStart()
{
	implementor_init();
	return 0;
}

/**
 * Manages stop of this component and all subsystems.
 */
int manageStop()
{
	implementor_stop();
	return 0;
}

/**
 * Manages terminate of this component and all subsystems.
 */
int manageTerminate()
{
	return 0;
}
