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
#include <signal.h>
#include <stdarg.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <syslog.h>

#include "trace.h"

class Trace_Impl : public Trace
{
public:
	Trace_Impl(); //register callback
	~Trace_Impl(){}
	static void signalHandlerUsr2(int sig);
	static Trace_Impl * s_instance;
	bool m_traceOn;
};
Trace_Impl * Trace_Impl::s_instance = 0;
// ====================== Trace implementation =========================
//static
void Trace::init()
{
	if (!Trace_Impl::s_instance)
	{
		Trace_Impl::s_instance = new Trace_Impl();
	}
}

void Trace::enable()
{
	if (Trace_Impl::s_instance)
	{
		Trace_Impl::s_instance->m_traceOn = true;
	}
}

void Trace::disable()
{
	if (Trace_Impl::s_instance)
	{
		Trace_Impl::s_instance->m_traceOn = false;
	}
}


void Trace::logTrace(const char *format, ...)
//void _logtrace_trace(const char *file, unsigned int line, const char *format, ...)
{
	if(Trace_Impl::s_instance->m_traceOn)
	{
		va_list ap;
		char buf[1024];

		va_start(ap, format);
		int length = vsnprintf(buf, sizeof(buf), format, ap);

		/* Add line feed if not there already */
		if (buf[length - 1] != '\n')
		{
			buf[length] = '\n';
			buf[length + 1] = '\0';
		}

		syslog(LOG_INFO, buf); //LOG_INFO is printed to stdout as well
		va_end(ap);
	}

}

// ====================== Trace_Impl implementation ======================
Trace_Impl::Trace_Impl()
{
	m_traceOn = false;
	signal(SIGUSR2,signalHandlerUsr2); //register callback
}

void Trace_Impl::signalHandlerUsr2(int sig)
{
	if(Trace_Impl::s_instance->m_traceOn == false)
	{
		Trace_Impl::s_instance->m_traceOn = true;
		syslog(LOG_INFO, "Trace is ON");
	}
	else
	{
		Trace_Impl::s_instance->m_traceOn = false;
		syslog(LOG_INFO, "Trace is OFF");
	}

}
