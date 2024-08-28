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
  * Author: elidmar
  * Reviewed:
 */

#include "dump.h"
#include "trace.h"
#include <stdarg.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

class Dump_Impl : public Dump
{
public:
	Dump_Impl();
	~Dump_Impl() {}
	static Dump_Impl * s_instance;
	bool m_traceOn;
	string m_fileName;
};

Dump_Impl * Dump_Impl::s_instance = 0;

// ====================== Dump implementation =========================

void Dump::init()
{
	if (!Dump_Impl::s_instance)
	{
		Dump_Impl::s_instance = new Dump_Impl();
	}
}


void Dump::log(const char *format, ...)
{
	if(Dump_Impl::s_instance->m_traceOn)
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

		TRACE_INFO ("Dump to file %s", Dump_Impl::s_instance->m_fileName.c_str());

		ofstream outfile;
		outfile.open (Dump_Impl::s_instance->m_fileName.c_str(), ios::app);
		if (!outfile.fail()) {
			outfile << buf;
		} else {
			TRACE_ERROR ("Cannot open file %s", Dump_Impl::s_instance->m_fileName.c_str());
		}
		outfile.close();
		va_end(ap);
	}

}

void Dump::setFileName(const string& fileName)
{
	Dump_Impl::s_instance->m_fileName = DUMP_DIR + fileName;
	Dump_Impl::s_instance->m_traceOn = true;
	TRACE_INFO ("setFileName to file %s", Dump_Impl::s_instance->m_fileName.c_str());
}

// ====================== Dump_Impl implementation ======================

Dump_Impl::Dump_Impl()
{
	m_traceOn = false;
}

