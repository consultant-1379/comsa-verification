#
# Makefile for CoreMW-COM_SA Function Test
#
# The CoreMW-COM_SA is a simple program from a build point-of-view.
# One Makefile is considered to be enough. If some make-guru feels an
# urge to complicate things, please feel free to do so after I have
# left.
#  /Lars Ekman
#

# Build-tools. Usually the DX cross-compiler
ARCHITECTURE := i686
#BUILD_TOOLS ?= /vobs/tsp_saf/tools/safade/compilers
# Put back what Lars Ekman removed. I agree it should not be here but
# we have a need to make it work quickly. Fix later.
CC := gcc
CXX := g++

LD := $(CXX)

# CoreMW-COM_SA dirs. Default is the com_sa vob.
COM_SA_DEV ?= /vobs/com_sa/dev
COM_SA_DEP ?= $(COM_SA_DEV)/dependencies
COM_SA_RESULT ?= /tmp/COM_SA_RESULT-$(USER)
OPENSAFD ?= /local/scratch/$(USER)/work/opensaf-staging
COM_SA_OPENSAF ?= $(OPENSAFD)/tools/cluster_sim_uml/rootfs/usr/local/lib/opensaf
COM_SA_OPENSAFLOG ?= $(OPENSAFD)/tools/cluster_sim_uml/rootfs/usr/local/lib
COM_SA_OPENSAFEXE ?= $(OPENSAFD)/tools/cluster_sim_uml

# Includes, Libs and flags
SAF_INCL ?= -I$(COM_SA_DEP)/core_mw_api/inc
SAF_LIB ?= -L$(COM_SA_DEP)/core_mw_api/lib/$(ARCHITECTURE)-suse-linux
SAF_OPSLIB ?= -L$(COM_SA_OPENSAF)
SAF_LIBLOG ?= -L$(COM_SA_OPENSAFLOG)
COM_INCL ?= -I$(COM_SA_DEP)/com_spi
MAF_INCL ?= -I$(COM_SA_DEP)/maf_spi
COM_MOTXINC ?= -I$(COM_SA_DEV)/src/motransaction
ACCMGM_INCL ?= -I$(COM_SA_DEV)/src/accessmgm -I$(COM_SA_DEV)/src/accessmgm/implementor -I$(COM_SA_DEV)/src/accessmgm/utils 
CPPFLAGS := -I$(COM_SA_DEV)/src/incl $(SAF_INCL) $(COM_INCL) $(MAF_INCL) $(COM_MOTXINC) $(ACCMGM_INCL)
CFLAGS := -Wall -fPIC -g
CXXFLAGS := $(CFLAGS)
LDFLAGS := $(SAF_LIBLOG) -lSaLog -lSaAmf -lSaCkpt -lSaImmOm -lSaNtf -lxml2 $(SAF_LIB) -lopensaf_core

# The COM_SA library to be loaded by COM
COM_SA_LOGEXE := $(COM_SA_OPENSAFEXE)/ComSALogTest
COM_SA_MOTXEXE := $(COM_SA_OPENSAFEXE)/ComSAMOTXTest
COM_SA_NTFEXE := $(COM_SA_OPENSAFEXE)/ComSANtfTest
COM_SA_ACCMGMEXE := $(COM_SA_OPENSAFEXE)/ComSAAccessMgmTest

# SDP and RUNTIME stuff
#COMSA_ID := CXP9017697_2

# Add your source-dirs here!
VPATH = \
	$(COM_SA_DEV)/src/ac \
	$(COM_SA_DEV)/src/log \
	$(COM_SA_DEV)/src/rlist \
	$(COM_SA_DEV)/src/trace \
	$(COM_SA_DEV)/src/accessmgm \
	$(COM_SA_DEV)/src/accessmgm/utils \
	$(COM_SA_DEV)/src/motransaction \
	$(COM_SA_DEV)/src/ntf \
	$(COM_SA_DEV)/src/test

# Add your objs here!
OBJS := \
	$(COM_SA_RESULT)/ComSAAc.o \
	$(COM_SA_RESULT)/ComSALogService.o \
	$(COM_SA_RESULT)/SelectTimer.o \
	$(COM_SA_RESULT)/ComSARlist.o \
	$(COM_SA_RESULT)/ComSATraceService.o \
	$(COM_SA_RESULT)/ComSAAccessMgm.o \
	$(COM_SA_RESULT)/ImmCmd.o \
	$(COM_SA_RESULT)/OamSACache.o \
	$(COM_SA_RESULT)/OamSADataClasses.o \
	$(COM_SA_RESULT)/OamSAImmBridge.o \
	$(COM_SA_RESULT)/OamSAManagedObjects.o \
	$(COM_SA_RESULT)/OamSATransactionalResource.o \
	$(COM_SA_RESULT)/OamSATransactionRepository.o \
	$(COM_SA_RESULT)/OamSATranslator.o \
	$(COM_SA_RESULT)/ComSANtf.o \
	$(COM_SA_RESULT)/TxContext.o \
	$(COM_SA_RESULT)/trace.o  


TESTOBJSALOG := $(COM_SA_RESULT)/ComSALogTest.o
TESTOBJSANTF := $(COM_SA_RESULT)/ComSANtfTest.o
TESTOBJSAMOTX := $(COM_SA_RESULT)/ComSAMOTXTest.o \
		$(COM_SA_RESULT)/OamSpiModelRepositoryDummy.o
TESTOBJSAACCMGM := $(COM_SA_RESULT)/ComSAAccessMgmTest.o \
		$(COM_SA_RESULT)/RoleClientHandler.o \
		$(COM_SA_RESULT)/ProcessUtil.o

MOTRANSACTION_SRC := $(COM_SA_DEV)/src/motransaction

DEPS = $(shell mkdir -p $(COM_SA_RESULT)) $(OBJS:.o=.d)

# Unit test variables
CMWDEP := ../../dependencies/core_mw_api/inc
COMDEP := ../../dependencies/com_spi
MO_DIR := ../motransaction
UTEST_INCLUDE := -I../incl -I$(CMWDEP) -I$(COMDEP) -I. -I$(MO_DIR) 

UTEST_SRCS := OamSAImmBridge_unittest.cc \
	$(MO_DIR)/OamSAImmBridge.cc \
	$(MO_DIR)/OamSATranslator.cc \
	$(MO_DIR)/OamSACache.cc \
	$(MO_DIR)/TxContext.cc \
	$(MO_DIR)/OamSADataClasses.cc \
	$(MO_DIR)/OamSATransactionRepository.cc \
	$(MO_DIR)/trace.c

UTEST_EXE := ut
UTEST_OBJS := $(UTEST_SRCS:%.cc=%.o)
UTEST_OBJS := $(UTEST_OBJS:%.c=%.o)
CXXFLAGS = -g -O0 -fno-inline -I/vobs/coremw/tools/gtest/include

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

.PHONY: clean comsatest


$(COM_SA_RESULT):
	mkdir -p $(COM_SA_RESULT)

comsalogtest: $(TESTOBJSALOG) $(OBJS) 
	   $(LD) -o $(COM_SA_LOGEXE) $(TESTOBJSALOG) $(OBJS) $(LDFLAGS)

comsamotxtest: $(TESTOBJSAMOTX) $(OBJS) 
	   $(LD) -o $(COM_SA_MOTXEXE) $(TESTOBJSAMOTX) $(OBJS) $(LDFLAGS)

comsantftest: $(TESTOBJSANTF) $(OBJS) 
	   $(LD) -o $(COM_SA_NTFEXE) $(TESTOBJSANTF) $(OBJS) $(LDFLAGS)

comsaaccmgmtest: $(TESTOBJSAACCMGM)
	$(LD) -o $(COM_SA_ACCMGMEXE) $(TESTOBJSAACCMGM) $(ACCMGM_INCL)

$(UTEST_EXE): $(UTEST_OBJS)
	$(CXX) -g -O0 -fno-inline $(UTEST_INCLUDE) -I/vobs/coremw/tools/gtest/include -o $(UTEST_EXE) $(UTEST_OBJS) -L/vobs/coremw/tools/gtest/lib -L./lib -lgtest_main_32 -lpthread


clean:
	rm -rf $(COM_SA_RESULT) $(UTEST_EXE) $(MO_DIR)/*.o *.o

ifneq ($(MAKECMDGOALS),clean)
 -include $(DEPS)
endif

