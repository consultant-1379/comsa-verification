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
# File: Makefile
#
# Author: eozasaf
# 
# Date:   2011-08-29
#
# This is a Makefile for the test MAF OI component 
#

# IMPORTANT:
# It is mandatory to source the .../ft/sourceme.tcsh file before building mafOi

LD := $(CXX)
COM_SA_DEP := $(COMSA_REPO_PATH)/dependencies
COM_INCL ?= -I$(COM_SA_DEP)/com_spi
MAF_INCL ?= -I$(COM_SA_DEP)/maf_spi
CMW_INCL ?= -I$(COM_SA_DEP)/core_mw_api/inc
COM_SA_RESULT ?= /tmp/COM_SA_RESULT-$(USER)
LSB_SHAREDLIBPATH := $(COM_SA_DEP)/core_mw_api/lib/$(ARCHITECTURE)-suse-linux
DEFINES_FILE ?= defines.h
DEFINES_FILE2 ?= defines2.h
TESTCONFIG_H ?= testConfig.h
REGSTORAGE_H ?= registrationStorage.h
ACTSTORAGE_H ?= actionStorage.h
ATTRSTORAGE_H ?= attributeStorage.h
XMLPARSER_H ?= xmlParser.h

ifeq (${shell ls ${DEFINES_FILE2}},$(DEFINES_FILE2))
        DEFINES_FILE = ${DEFINES_FILE2}
endif

CPPFLAGS := -I$(COM_SA_DEV_DIR)/src/incl $(COM_INCL) $(CMW_INCL) $(MAF_INCL)
CFLAGS := -Wall -fPIC -g -include $(DEFINES_FILE) -include $(TESTCONFIG_H) -include $(REGSTORAGE_H) -include $(ACTSTORAGE_H) -include $(ATTRSTORAGE_H) -include $(XMLPARSER_H)
CXXFLAGS := $(CFLAGS)
LDFLAGS := -lxml2

COM_COMP_SO := test-maf-oi.so

VPATH = $(COM_SA_DEV_DIR)/src/test/mafOI

# Add your objs here!
OBJS := \
	$(COM_SA_RESULT)/mafOI.o \
	$(COM_SA_RESULT)/testConfig.o \
	$(COM_SA_RESULT)/registrationStorage.o \
	$(COM_SA_RESULT)/actionStorage.o \
	$(COM_SA_RESULT)/attributeStorage.o \
	$(COM_SA_RESULT)/xmlParser.o
	
DEPS = $(shell mkdir -p $(COM_SA_RESULT)) $(OBJS:.o=.d)

# Implicit rules

$(COM_SA_RESULT)/%.o: %.c
	$(COMPILE.c) -o $@ $<

$(COM_SA_RESULT)/%.o: %.cc
	$(COMPILE.cc) -o $@ $<

$(COM_SA_RESULT)/%.o: %.cpp
	$(COMPILE.cpp) -o $@ $<

$(COM_SA_RESULT)/%.d: %.c
	@echo -n $(COM_SA_RESULT)/ > $@
	@$(COMPILE.c) -MM $< >> $@

$(COM_SA_RESULT)/%.d: %.cc
	@echo -n $(COM_SA_RESULT)/ > $@
	@$(COMPILE.cc) -MM $< >> $@

$(COM_SA_RESULT)/%.d: %.cpp
	@echo -n $(COM_SA_RESULT)/ > $@
	@$(COMPILE.cpp) -MM $< >> $@

# Main targets

.PHONY: clean lib

all: clean $(COM_SA_RESULT) lib 

lib: $(COM_COMP_SO) 

$(COM_COMP_SO): $(OBJS)
	$(LD) -o $@ -shared $(OBJS) $(LDFLAGS)
	
$(COM_SA_RESULT):
	mkdir -p $(COM_SA_RESULT)

clean:
	rm -rf $(COM_SA_RESULT)/mafOI.o $(COM_SA_RESULT)/testConfig.o $(COM_SA_RESULT)/registrationStorage.o $(COM_SA_RESULT)/actionStorage.o $(COM_SA_RESULT)/attributeStorage.o $(COM_SA_RESULT)/xmlParser.o $(COM_COMP_SO)

ifneq ($(MAKECMDGOALS),clean)
-include $(DEPS)
endif
