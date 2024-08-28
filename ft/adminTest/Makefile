
PROG = adminTest

SRCS = adminTest.cpp utils/trace.cpp
OBJS=$(SRCS:.c=.o)

ARCHITECTURE := x86_64
COM_SA_DEV ?= /vobs/com_sa/dev
COM_SA_DEP ?= $(COM_SA_DEV)/dependencies
SAF_INCL ?= -I$(COM_SA_DEP)/core_mw_api/inc
SAF_LIB ?= -L$(COM_SA_DEP)/core_mw_api/lib/$(ARCHITECTURE)-suse-linux

CC = /vobs/coremw/tools/LSB_BUILD_ENV/compilers/bin/x86_64-dx-linux-gnu-g++
CFLAGS = -g -O2 -Wall -fPIC
INCLUDES = -I. -Iutils -I$(COM_SA_DEV)/src/incl -I/vobs/coremw/dev/opensaf_api/include $(SAF_INCL)
LIBDIR= $(SAF_LIB)
LDFLAGS = -lrt -lSaImmOi -lSaImmOm -Wl,--allow-shlib-undefined 

all: $(PROG)

$(PROG): $(OBJS)
	${CC} ${CFLAGS} ${INCLUDES} -o $@ ${SRCS} ${LIBDIR} ${LIBDIR}/opensaf ${LDFLAGS}


.c.o:
	${CC} ${CFLAGS} ${INCLUDES} -c $<

depend:
	makedepend ${INCLUDES} ${SRCS}

clean:
	rm -f *.o core *~ $(PROG) *.tgz
