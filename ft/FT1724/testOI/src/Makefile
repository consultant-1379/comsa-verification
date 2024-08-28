#
# Plain and simple makefile to build in this folder
#

# If targetdir is empty, we put the result in the current folder.

ifeq ($(TARGETDIR),)
TARGETDIR = ./bin
$(info "Setting target-directory to $(TARGETDIR)")
endif

ifeq ($(COREMW_TEST_PREFIX),)
COREMW_TEST_PREFIX = $(COMSA_DIR)/comsa-verification/ft/FT1724/testOI/
$(info "Setting source-home to $(COREMW_TEST_PREFIX)")
endif

ifeq ($(COREMW_PREFIX),)
COREMW_PREFIX = $(COMSA_DEV_DIR)/dependencies/
$(info "Setting coremw-prefix to $(COREMW_TEST_PREFIX)")
endif

ifeq ($(OSAFINC),)
OSAFINC = $(COREMW_PREFIX)/core_mw_api/inc
#OSAFINC = $(COREMW_PREFIX)/opensaf_api/include
$(info "Using $(OSAFINC) as default include path")
endif

ifeq ($(OSAFLIB),)
OSAFLIB = $(COREMW_PREFIX)/core_mw_api/lib/x86_64-suse-linux
$(info "Using $(OSAFLIB) as default library path")
endif

ifeq ($(LOCAL_ARCHIVES_DIR),)
LOCAL_ARCHIVES_DIR = ./
$(info "Using $(LOCAL_ARCHIVES_DIR) as path to install packages")
endif

ifeq ($(NUMBER_OF_BLADES),)
NUMBER_OF_BLADES = 4
endif

ifeq ($(REV),)
REV = P1A01
$(info Setting REVISION to $(REV))
endif

ECHO  := $(shell if [ -x /bin/echo ]; then echo /bin/echo; else echo /usr/bin/echo; fi)
MKDIR := $(shell if [ -x /bin/mkdir ]; then $(ECHO) /bin/mkdir; else $(ECHO) /usr/bin/mkdir; fi)
RM    := $(shell if [ -x /bin/rm ]; then $(ECHO) /bin/rm; else $(ECHO) /usr/bin/rm; fi)
SED   := $(shell if [ -x /bin/sed ]; then $(ECHO) /bin/sed; else $(ECHO) /usr/bin/sed; fi)
TAR   := $(shell if [ -x /bin/tar ]; then $(ECHO) /bin/tar; else $(ECHO) /usr/bin/tar; fi)
CP    := $(shell if [ -x /bin/cp ]; then $(ECHO) /bin/cp; else $(ECHO) /usr/bin/cp; fi)

.PHONY: all clean install installpackage
oi: $(TARGETDIR)/imm-applier | $(TARGETDIR)
	@$(ECHO) Built $@

all: $(TARGETDIR)/ntfSubscribeApp $(TARGETDIR)/imm-applier $(TARGETDIR)/ntfSubscribeApp_init $(TARGETDIR)/rotate_log.sh | $(TARGETDIR)
	@$(ECHO) Built $@

clean:
	@rm -f $(TARGETDIR)/imm-applier; rm -f $(TARGETDIR)/*.d ; rm -f $(TARGETDIR)/*.o 

$(TARGETDIR) :
	@if [ ! -d $@ ]; then \
		$(MKDIR) -p $@ ; \
	fi

install: all
	@$(MKDIR) -p $(DESTDIR)/opt/NTFSUBSCRIBE-CXP9010000_1-$(REV)/bin
	@install -m 755 $(TARGETDIR)/ntfSubscribeApp $(DESTDIR)/opt/NTFSUBSCRIBE-CXP9010000_1-$(REV)/bin/ntfSubscribeApp
	@install -m 755 $(TARGETDIR)/imm-applier $(DESTDIR)/opt/NTFSUBSCRIBE-CXP9010000_1-$(REV)/bin/imm-applier
	@install -m 755 $(TARGETDIR)/ntfSubscribeApp_init $(DESTDIR)/opt/NTFSUBSCRIBE-CXP9010000_1-$(REV)/bin/ntfSubscribeApp_init
	@install -m 755 $(TARGETDIR)/rotate_log.sh $(DESTDIR)/opt/NTFSUBSCRIBE-CXP9010000_1-$(REV)/bin/rotate_log.sh
	@-chown -R root:root $(DESTDIR)/opt/NTFSUBSCRIBE-CXP9010000_1-$(REV)/bin
	@$(ECHO) Done $@

APPDIRNAME = ntfSubscribeApp
SRCDIR = $(COREMW_TEST_PREFIX)/src/
XTRAINC = $(COREMW_TEST_PREFIX)/apps/$(APPDIRNAME)/inc

INSTALL_SDP = ERIC-NtfSubscribeAppInstall.sdp
APP_SDP = ERIC-NTFSUBSCRIBE-CXP9010000_1.sdp
ETF_XML = etc/ETF.xml
CAMPAIGN_XML = etc/campaign.xml

LIBFILES = -lSaNtf -lSaAmf -lSaClm -lSaSmf -lSaImmOi -lSaImmOm -lopensaf_core -lpthread -lrt
LIBFLAGS = -Wl,--allow-shlib-undefined,-rpath

CFLAGS += -g -O2 -Wall -fPIC -pthread -I$(SRCDIR) -I$(XTRAINC) $(XML2_CFLAGS) -I$(OSAFINC)

APPSRC := $(SRCDIR)/ntfsubscribe.c $(SRCDIR)/appMain.c 
APPDEP := $(patsubst %.c,%.d, $(addprefix $(TARGETDIR)/, $(notdir $(APPSRC))))
APPOBJ := $(patsubst %.c,%.o, $(addprefix $(TARGETDIR)/, $(notdir $(APPSRC))))

IMMSRC := $(SRCDIR)/applier.c $(SRCDIR)/immutil.c $(SRCDIR)/saf_error.c
IMMDEP := $(patsubst %.c,%.d, $(addprefix $(TARGETDIR)/, $(notdir $(IMMSRC))))
IMMOBJ := $(patsubst %.c,%.o, $(addprefix $(TARGETDIR)/, $(notdir $(IMMSRC))))

$(APPDEP) : $(APPSRC) | $(TARGETDIR)
$(APPOBJ) : $(APPDEP) 

$(IMMDEP) : $(IMMSRC) | $(TARGETDIR)
$(IMMOBJ) : $(IMMDEP) 

# Tell that compiler where to find the source
VPATH = $(SRCDIR)

$(TARGETDIR)/imm-applier : $(IMMDEP) $(IMMOBJ)
	@$(ECHO) Linking $@
	@$(CC) -o $@ $(IMMOBJ) $(XML2_LIBS) -L$(OSAFLIB) $(LIBFILES) $(LIBFLAGS)

$(TARGETDIR)/ntfSubscribeApp : $(APPDEP) $(APPOBJ)
	@$(ECHO) Linking $@
	@$(CC) -o $@ $(APPOBJ) $(XML2_LIBS) -L$(OSAFLIB) $(LIBFILES) $(LIBFLAGS)

$(TARGETDIR)/%.o : %.c
	@$(ECHO) "Compiling $<"
	@$(CC) -c -o $@ $(CFLAGS) $<

$(TARGETDIR)/%.d : %.c
	@$(ECHO) "Generating dependencies for $<"
	@$(MKDIR) -p $(TARGETDIR)
	@set -e; $(RM) -f $@; \
	$(CC) -c $(CFLAGS) -M $< > $@.$$$$; \
	$(SED) 's,\($*\)\.o[ :]*,$(TARGETDIR)/\1.o $@ : ,g' < $@.$$$$ > $@; \
	$(RM) -f $@.$$$$

$(TARGETDIR)/ntfSubscribeApp_init : $(SRCDIR)/$(notdir $@) | $(TARGETDIR)
	@$(CP) -f $(SRCDIR)/$(notdir $@) $@

$(TARGETDIR)/rotate_log.sh : $(SRCDIR)/../utils/rotate_log.sh | $(TARGETDIR)
	@$(CP) -f $(SRCDIR)/../utils/rotate_log.sh $@

# Some ugly solutions, might be fixed later, but this is a test-app ...

T2DIR = $(TARGETDIR)/..

.PHONY: $(T2DIR)/campaign.xml $(T2DIR)/ETF.xml installpackage

$(T2DIR)/campaign.xml :
	@$(ECHO) Creating $@
	@$(SED) "s/APPVER/$(REV)/g" $(SRCDIR)/../etc/$(notdir $@) > $@

$(T2DIR)/ETF.xml : 
	@$(ECHO) Copying $@
	@$(CP) -f $(SRCDIR)/../etc/ETF.xml $@

$(LOCAL_ARCHIVES_DIR)/$(INSTALL_SDP) : $(T2DIR)/campaign.xml $(T2DIR)/ETF.xml
	@cd $(T2DIR); $(TAR) czf $@ ETF.xml campaign.xml; $(RM) -f ETF.xml campaign.xml

installpackage : $(LOCAL_ARCHIVES_DIR)/$(INSTALL_SDP)
	@$(ECHO) Done $@

ifneq ($(MAKECMDGOALS),clean)
-include $(APPDEP)
endif

