#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <saAis.h>
#include <unistd.h>
#include <pthread.h>
#include <ComMgmtSpiCommon.h>
#include <ComMgmtSpiComponent_1.h>
#include <ComOamSpiEvent_1.h>
#include <ComOamSpiNotificationFm_1.h>
#include <ComOamSpiServiceIdentities_1.h>
#include <SelectTimer.h>
#include <saNtf.h>
#include <ComSA.h>
#include <ComSANtf.h>

static ComOamSpiEventRouter_1T fake_router;
static ComOamSpiEventProducer_1T *pIf;
static pthread_mutex_t list_lock = PTHREAD_MUTEX_INITIALIZER;

#define COMSANTF_ADD_TEXT "Additional text ComSA NTF TEST"
#define COMSANTF_NO "3GPPsafApp=ComSaTest,safSi=NoRed5"
#define COMSANTF_DN "safApp=ComSaTest,safSi=NoRed5"

static const uint32_t outMajorType = 193;
static const uint32_t outMinorType = 0x000E0004;

static const uint32_t inVType = 193;
static const uint16_t inMaType = 14; /*(0xE)*/
static const uint16_t inMiType = 4;
static int expected = 16;
static int okReceived = 0;
static char *addtxt;

static const char *sa_severity_list[] = {
	"SA_NTF_SEVERITY_CLEARED",
	"SA_NTF_SEVERITY_INDETERMINATE",
	"SA_NTF_SEVERITY_WARNING",
	"SA_NTF_SEVERITY_MINOR",
	"SA_NTF_SEVERITY_MAJOR",
	"SA_NTF_SEVERITY_CRITICAL",
};

static void print_severity(SaNtfSeverityT input)
{
	if(!(input >= SA_NTF_SEVERITY_CLEARED)||!(input <= SA_NTF_SEVERITY_CRITICAL))
		ERR("wrong severity"); 
	DEBUG("severity = %s\n", (char *)sa_severity_list[input]);
}

ComReturnT notify(ComOamSpiEventProducerHandleT producerId,
                         ComOamSpiEventConsumerHandleT consumerId,
                         const char * eventType,
                         ComNameValuePairT **filter,
                         void * value)
{
	if (pthread_mutex_lock(&list_lock) != 0) abort();		
	ComReturnT com_rc = ComOk;
	ComOamSpiNotificationFmStructT *comNot = (ComOamSpiNotificationFmStructT*)value;
	DEBUG("------ ComAlarm --------\n"); 
	print_severity(comNot->severity);
	DEBUG("dn: \"%s\"\n", comNot->dn);
	DEBUG("addtxt: %s\n", comNot->additionalText);
	DEBUG("majorType %#x\n", comNot->majorType);
	DEBUG("minorType %#x\n", comNot->minorType);
	DEBUG("------------------------\n");
	if (comNot->majorType == outMajorType && comNot->minorType == outMinorType && 
		 strcmp(comNot->dn, COMSANTF_DN)== 0 &&
		 strcmp(comNot->additionalText, addtxt)==0) {
		okReceived++;
	}
	pIf->doneWithValue(NULL, (void*)comNot);
	if (pthread_mutex_unlock(&list_lock) != 0) abort();		
	return com_rc;	
}

ComReturnT registerProducer(ComOamSpiEventProducer_1T * interface, ComOamSpiEventProducerHandleT * handle)
{
	pIf = interface;
	return ComOk;
}

ComReturnT addProducerEvent(ComOamSpiEventProducerHandleT handle, const char * eventType)
{
	return ComOk;
}

static ComReturnT getIf( ComMgmtSpiInterface_1T interfaceId, ComMgmtSpiInterface_1T **result)
{
	*result = (ComMgmtSpiInterface_1T *)&fake_router;
	return ComOk; 
}

ComReturnT removeProducerEvent(ComOamSpiEventProducerHandleT handle, const char * eventType)
{
	return ComOk; 	
}

ComReturnT unregisterProducer(ComOamSpiEventProducerHandleT handle, ComOamSpiEventProducer_1T * interface)
{
	return ComOk;
}


int main(int argc, char *argv[])
{
	int rv;
	long int rnum = 0;
	char buf[2048], sbuf[2048];
	 
	ComReturnT com_rv; 
	ComMgmtSpiInterfacePortal_1T fake_portal;
	ComNameValuePairT *filter = NULL; 
	fake_portal.getInterface = &getIf;

	fake_router.registerProducer = &registerProducer;
	fake_router.addProducerEvent = &addProducerEvent;
	fake_router.removeProducerEvent = &removeProducerEvent;
	fake_router.unregisterProducer = &unregisterProducer;
	fake_router.notify = notify;
	srandom(getpid());
	rnum = random();
	 /* SelectTimer init; */
	addtxt = malloc(sizeof(COMSANTF_ADD_TEXT)+ 256);
	snprintf(addtxt, sizeof(COMSANTF_ADD_TEXT)+ 256, "%s:%ld", COMSANTF_ADD_TEXT, rnum);
	comSASThandle = timerCreateHandle_r();
	poll_maxfd(comSASThandle, 16);
	printf("START ComSA notification test\n");
	DEBUG("Send 4 Al  and 4 sec Al before subscribe\n");
	snprintf(buf, 2048, "ntfsend -r 4 -c %u,%hu,%hu -n \"%s\" -a \"%s:%ld\"",
		inVType, inMaType, inMiType, COMSANTF_NO, COMSANTF_ADD_TEXT,rnum);
	DEBUG(buf);
	snprintf(sbuf, 2048, "ntfsend -r 4 -T0x5000 -c %u,%hu,%hu -n \"%s\" -a \"%s:%ld\"",
		inVType, inMaType, inMiType, COMSANTF_NO, COMSANTF_ADD_TEXT,rnum);
	DEBUG(sbuf);
	rv = system(buf);
	if (rv != 0) 
		err_quit("ntfsend Al failed\n"); 
	rv = system(sbuf);
	if (rv != 0) 
		err_quit("ntfsend sec Al failed\n");   
	DEBUG("Open NTF service IF\n");  	
	com_rv = ComNtfServiceOpen(&fake_portal);
	assert(ComOk == com_rv);
	DEBUG("addFilter ComSA notifications\n");
	assert(ComOk == pIf->addFilter(44, NULL, &filter));
	DEBUG("Send 4 Al and 4 sec Al after subscribe\n");
	rv = system(buf);
	if (rv != 0) 
		err_quit("ntfsend Al failed\n"); 
	rv = system(sbuf);
	if (rv != 0) 
		err_quit("ntfsend sec Al failed\n"); 
	poll_execute(comSASThandle);
	DEBUG("Drop out of control-loop\n");  	
	DEBUG("removeFilter ComSA notifications\n");
	pIf->removeFilter(44, NULL, &filter); 
	assert(ComOk == ComNtfServiceClose(&fake_portal));
	if (okReceived == expected) {
		printf("ComSA notification test: test ok\n"); 
		exit(EXIT_SUCCESS);
	} else {
		printf("ComSA notification test: test failed received %d of %d\n",
			okReceived, expected); 
		exit(EXIT_FAILURE);
	}
}

