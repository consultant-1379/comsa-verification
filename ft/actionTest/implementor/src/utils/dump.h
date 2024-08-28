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
#ifndef ACTIONTEST_DUMP_HH_
#define ACTIONTEST_DUMP_HH_

#include <string>

#define DUMP(__fmt,__arg...) Dump::log(__fmt , ## __arg)
#define DUMP_DIR "/tmp/actiontest_"

class Dump
{
protected:
	Dump(){}
public:
	/*
	 * Must be executed before trace is used. Example in main function.
	 **/
	static void init();
	static void setFileName(const std::string &fileName);
	virtual ~Dump(){}

	/*
	 * Only use the Macro above to access the method.
	 **/
	static void log(const char *format, ...);
};

#endif /* ACTIONTEST_DUMP_HH_ */
