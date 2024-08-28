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
  * Author: erannjn
  * Reviewed: erafodz
 */
#ifndef AASERVICE_TRACE_HH_
#define AASERVICE_TRACE_HH_

#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <syslog.h>
#include <stdio.h>
#include <getopt.h>

/*
 * TRACE_INFO could be turned on/off using USR2 signal to process in terminal.
 * Exampel "killall -USR2 aaservice". The output will be written in syslog and
 * to stdout as well.
 **/
#define TRACE_INFO(__fmt,__arg...) Trace::logTrace("%s(%d) %s: [TRACE] "__fmt, __FILE__, __LINE__, __FUNCTION__ , ## __arg)
/*
 * TRACE_ERROR will always write to syslog and cannot be turned off. Should be used carefully
 * in order not to spam the syslog.
 **/
#define TRACE_ERROR(__fmt,__arg...) syslog(LOG_ERR, "%s(%d) %s: "__fmt , __FILE__, __LINE__, __FUNCTION__ , ## __arg)

/*
 * printf is redefined and is the same as TRACE_INFO
 **/
#define printf(__fmt,__arg...) Trace::logTrace("%s(%d) %s: "__fmt, __FILE__, __LINE__, __FUNCTION__ , ## __arg)

class Trace
{
protected:
	Trace(){}
public:
	/*
	 * Must be executed before trace is used. Example in main function.
	 **/
	static void init();
	static void enable();
	static void disable();
	virtual ~Trace(){}
	/*
	 * Only use the Macro above to access the method.
	 **/
	static void logTrace(const char *format, ...);
};

#endif /* AASERVICE_TRACE_HH_ */
