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
* Modified: eozasaf 2011-07-25 Parameterized MO class name(s)
*/
#include <unistd.h>
#include <syslog.h>
#include <stdlib.h>
#include <string.h>

#include "trace.h"
#include "implementor/Implementor.h"

/*
 * Controllable functions.
 */
int manageStart(char**,int);
int manageStop();
int manageTerminate();

int main(int argc, char **argv)
{
	Trace::init();	//In order to able to use trace functionality
	syslog(LOG_INFO, "testOI started");
	openlog(NULL, LOG_PERROR, LOG_USER);

	TRACE_INFO("testOI started");

	syslog(LOG_INFO,"%d class(es)",(argc-1));
	char** class_names=new char* [argc-1];
	for(int i=0;i<argc-1;i++)
		class_names[i]=argv[i+1];

	manageStart(class_names,argc-1);

	while (1)
		/* Keep waiting forever */
		sleep(-1);

	return 0;
}

/**
 * Manages start of this component and all subsystems.
 */
int manageStart(char ** class_names,int count)
{
	implementor_init(class_names,count);
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
