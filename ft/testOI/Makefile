#
# Copyright (C) 2010 by Ericsson AB
# S - 125 26  STOCKHOLM
# SWEDEN, tel int + 46 10 719 0000
# 
# The copyright to the computer program herein is the property of
# Ericsson AB. The program may be used and/or copied only with the
# written permission from Ericsson AB, or in accordance with the terms
# and conditions stipulated in the agreement/contract under which the
# program has been supplied.
# 
# All rights reserved.
# 
# File: Makefile for the test Object Implementer (OI)
#
#  
# Author: eozasaf
# 
# Date:   2011-07-25
# 
# IMPORTANT:
# It is mandatory to source the .../ft/sourceme.tcsh file before building the test component

export DX_SYSROOT_X86_64=$(CMW_TOOLS)/lotc4.0_api

PROG = testOI

SRCS = testAppl.cpp implementor/CCBProcessor.cpp implementor/Implementor.cpp utils/immutil.cpp utils/trace.cpp
OBJS=$(SRCS:.c=.o)

ARCHITECTURE := x86_64
COM_SA_DEP ?= $(COMSA_REPO_PATH)/dependencies
SAF_INCL ?= -I$(COM_SA_DEP)/core_mw_api/inc
#SAF_LIB ?= -L$(COM_SA_DEP)/core_mw_api/lib/$(ARCHITECTURE)-suse-linux
SAF_LIB ?= -L$(LSB_SHAREDLIBPATH)
CC =$(CMW_TOOLS)/LSB_BUILD_ENV/compilers/bin/x86_64-dx-linux-gnu-g++
CFLAGS = -g -O2 -Wall -fPIC
INCLUDES = -I. -Iimplementor -Iutils $(SAF_INCL)
LIBDIR= $(SAF_LIB)
LDFLAGS = -lrt -lSaImmOi -lSaImmOm -Wl,--allow-shlib-undefined -Wl,$(SAF_LIB)
errstrtest: CFLAGS += -DErrorStringTest

all: $(PROG)

errstrtest: $(PROG)

$(PROG): $(OBJS)
	@echo "--- Compiling $@"
	${CC} ${CFLAGS} ${INCLUDES} -o $@ ${SRCS} ${LIBDIR} ${LDFLAGS}

.c.o:
	${CC} ${CFLAGS} ${INCLUDES} -c $<

depend:
	makedepend ${INCLUDES} ${SRCS}

clean:
	rm -f *.o core *~ $(PROG) *.tgz
