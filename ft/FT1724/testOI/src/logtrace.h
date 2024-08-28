/*******************************************************************************
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
*
* Author: 
*
* Date:   2011-06-14
*
* Reviewed: 
* 
*******************************************************************************/

#ifndef LOGTRACE_H
#define LOGTRACE_H

#include <syslog.h>

#ifdef  __cplusplus
extern "C" {
#endif

extern void trace_on();
extern void trace_off();
extern void trace_init(const char* name);

/* internal functions, do not use directly */
extern void __logtrace_log(const char *file, unsigned int line, int priority,
			  const char *format, ...) __attribute__ ((format(printf, 4, 5)));

extern void __logtrace_trace(const char *file, unsigned int line, const char *format, ...) 
	__attribute__ ((format(printf, 3, 4)));

/* LOG API. */
#define LOG_ER(format, args...) __logtrace_log(__FILE__, __LINE__, LOG_ERR, (format), ##args)
#define LOG_NO(format, args...) __logtrace_log(__FILE__, __LINE__, LOG_NOTICE, (format), ##args)
#define LOG_IN(format, args...) __logtrace_log(__FILE__, __LINE__, LOG_INFO, (format), ##args)

/* TRACE API. */
#define TRACE(format, args...)  __logtrace_trace(__FILE__, __LINE__, (format), ##args)

#ifdef  __cplusplus
}
#endif

#endif

