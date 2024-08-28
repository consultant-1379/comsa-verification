/*
*  For Function Test for Log Service
*/
#include <stdio.h>
#include <stdlib.h>
#include "ComSALogService.h"
#include "trace.h"
#include <SelectTimer.h>
#include <ComSA.h>

ComReturnT ComSALogTest(int eventId, int severity, int facility, const char* databuffer);

int main()
{
	int i, j, errcnt = 0;
	ComReturnT retValue = ComOk;

	struct log_state_t log;

	log.level = LOG_LEVEL_DEBUG;
	log.tags = TRACE_TAG_LOG | TRACE_TAG_ENTER | TRACE_TAG_LEAVE;
	log.mode = LOG_MODE_FILE | LOG_MODE_FILELINE | LOG_MODE_TIMESTAMP;
	log_control( &log, 0 );
	log_to_file("logfile.txt");
	log_init("ComSALogTest");

	printf("ComSALogTest Start.......................\n\n");
	comSASThandle = timerCreateHandle_r();
	poll_maxfd(comSASThandle, 16);
	/* (the log-callbacks are never handled. It ain't pretty but it works.) */

 	for(i = 0; i<=6; i++) {
		for(j = 0; j<= 22 ;j++) {
			printf("severity = %d, facility = %d\n", i,j);
			retValue = ComSALogTest(1, i, j, "ComSALog Function Test");
			if(retValue == ComOk)
				printf("ComSALogTest OK, severity = %d and facility = %d\n", i, j);
			else {
				LOG_PRINTF(LOG_LEVEL_ERROR,"ComSALogTest Error, severity = %d and facility = %d\n", i, j);
				errcnt++;
			}
			printf("Return value after ComSALogTest %d\n\n",retValue);
		}
	}

	if (errcnt == 0)
		printf("\n=== ALL TESTS PASSED\n");
	else
		printf("\n=== %d TESTS FAILED!\n", errcnt);

	return 0;
}

ComReturnT ComSALogTest(int eventId, int severity, int facility, const char* databuffer)
{
	ComReturnT	ReturnValue;
	ComMwSpiLog_1T* myLogPointer = ExportLogServiceInterface();

	ReturnValue = ComLogServiceOpen();
	if (ReturnValue != ComOk)
	{
		LOG_PRINTF(LOG_LEVEL_ERROR,"Error when opening logs, return value %d\n", ReturnValue);
		return ReturnValue;
	}
	else
	{
		printf("OK opening logs, return value %d\n", ReturnValue);
		ReturnValue = myLogPointer->logWrite(eventId , severity, facility , databuffer);
		if (ReturnValue != ComOk)
		{
			LOG_PRINTF(LOG_LEVEL_ERROR,"Error when opening logs, return value %d\n", ReturnValue);
			return ReturnValue;
		}
		else
		{
			printf("Return value after logWrite %d\n",ReturnValue);
			ReturnValue = ComLogServiceClose();
			if (ReturnValue != ComOk)
			{
				LOG_PRINTF(LOG_LEVEL_ERROR,"Error when close logs, return value %d\n", ReturnValue);
				return ReturnValue;
			}
			printf("Return value after close %d\n",ReturnValue);
			return ReturnValue;
		}
	}
}
