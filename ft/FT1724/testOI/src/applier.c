#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <getopt.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <sys/un.h>
#include <sys/time.h>
#include <fcntl.h>
#include <ctype.h>
#include <libgen.h>
#include <assert.h>

#include <saAis.h>
#include <saImmOm.h>
#include <immutil.h>
#include <poll.h>
#include "saf_error.h"

#define CREATE 1
#define MODIFY 2
#define DELETE 3

#define ATTR_TYPE_INT32 0
#define ATTR_TYPE_STRING 1

#define DEFAULT_SLEEP_TIME 5
#define STRUCT_PATTERN "id="
#define EMPTY_STRUCT_PATTERN "EMPTY_STRUCT"

typedef struct {
  const char* attrName;
  SaImmValueTypeT attrType;
  void** attrValues;
} TestAttributeValue;

int DEBUG_ENABLED = 0;

//const static SaImmOiImplementerNameT const implementerName = "Runtime_implementer";
char *implementerName = "Runtime_implementer";
static SaImmOiHandleT immOiHnd = 0;
const SaImmClassNameT runtimeClassName = "cmNtfRtTest";
int attrValueType = 0;

SaImmHandleT immOmHandle;
/* SaImmCallbacksT immOmCallbacks = {NULL}; */
SaVersionT immVersion = {'A', 0x02, 0x0c}; 

void DEBUG(const char* text)
{
	if(DEBUG_ENABLED)
	{
		if(text != NULL)
		{
			printf("DEBUG: %s\n",text);
		}
	}
}

void DEBUG_STR(const char* text, const char* value)
{
	if(DEBUG_ENABLED)
	{
		if(text != NULL)
		{
			if(value == NULL)
				DEBUG(text);
			else
				printf("DEBUG: %s: (%s)\n",text,value);
		}
	}
}

void debugAttrModArray(const SaImmAttrValuesT_2 ** attr)
{
	if(DEBUG_ENABLED)
	{
		if(attr == NULL)
		{
			printf("debugAttrModArray(): attr = NULL\n");
			return;
		}
		unsigned int i;
		for(i = 0; attr[i] != NULL; i++)
		{
			printf("\nDEBUG: attr[%u]->attrName: (%s)\n",i, attr[i]->attrName);

			printf("DEBUG: attr[%u]->attrValueType: (%d)\n",i, attr[i]->attrValueType);

			printf("DEBUG: attr[%u]->attrValuesNumber: (%u)\n",i, attr[i]->attrValuesNumber);

			if(attr[i]->attrValues == NULL)
			{
				printf("DEBUG: attr[%u]->attrValues = NULL\n",i);
			}
			else
			{
				// print the rdn
				if(i == 0)
				{
					printf("DEBUG:    rdn[%u]->attrValues[0](STRING): (%s)\n", i, *(char**)(attr[i]->attrValues[0]) );
				}
				// print the attribute value (we have only 1)
				else
				{
					switch(attrValueType)
					{
					case ATTR_TYPE_INT32:
						printf("DEBUG:    attr[%u]->attrValues[0](INT32): (%d)\n", i, *((int*)(attr[i]->attrValues[0])) );
						break;
					case ATTR_TYPE_STRING:
						printf("DEBUG:    attr[%u]->attrValues(STRING)\n",i);
						break;
					default:
						printf("DEBUG:    attr[%u]->attrValues(other type) received\n",i);
						break;
					}
				}
			}
		}
	}
}

static void usage(const char *progname)
{
  printf("\nNAME\n");
  printf("\t%s - an IMM Runtime Object tester\n", progname);

  printf("\nSYNOPSIS\n");
  printf("\t%s [options]\n", progname);

  printf("\nDESCRIPTION\n\n");
  printf("\t%s is a test Object Implementer for testing Runtime cached objects and attributes\n", progname);
  printf("\tIt will do 1 of the 3 operations at a time: -C/--create -M/--modify -D/--delete (It is a must to give only one of them)\n");

  printf("\n\tNote 1: class definitions must be defined in IMM before running this program\n");
  printf("\n\tNote 2: if the testOI exited then the objects still remain in IMM but their values are locked, so it is not possible to read them.\n");
  printf("\t\tFor preventing a fast exit -s/--sleepTime with a parameter can be used to give time for checking the values in IMM\n");

  printf("\n\tLimitations: only 1 attribute is supported under an object.\n");
  printf("\t\tIt can be INT32, STRING or SA_NAME_T (don't need to provide the type, it is set automatically)\n");

  printf("\nOPTIONS\n");
  printf("\t-h, --help\n");
  printf("\t\tthis help\n");

  printf("\t-d, --debug\n");
  printf("\t\tEnable debug printouts to console\n");

  printf("\t-C, --create\n");
  printf("\t\tSelecting \"create object\" mode\n");

  printf("\t-M, --modify\n");
  printf("\t\tSelecting \"modify attribute\" mode\n");

  printf("\t-D, --delete\n");
  printf("\t\tSelecting \"delete object\" mode\n");

  printf("\t-c, --class\n");
  printf("\t\tSet class name\n");

  printf("\t-k, --keyAttr\n");
  printf("\t\tSet key attribute\n");

  printf("\t-r, --rdn\n");
  printf("\t\tSet rdn\n");

  printf("\t-p, --parentObject\n");
  printf("\t\tSet parent object rdn\n");

  printf("\t-a, --attrName\n");
  printf("\t\tSet attribute name\n");

  printf("\t-v, --attrValue\n");
  printf("\t\tSet attribute value\n");

  printf("\t-s, --sleepTime\n");
  printf("\t\tSet sleep time - using this is useful if something needs to read the runtime values from IMM. After exiting from this program it is not possible!\n");

  printf("\t-n, --testOiName\n");
  printf("\t\tSet testOI name\n");

  printf("\nEXAMPLE\n");

  printf("\n\tCreate struct\n");
  printf("\n\t\t./imm-applier -d -C -c ObjImpComplexClassSv -k objImpComplexClassSvId -r objImpComplexClassSvId=1 -a TestStructAttrSv -v id=TestStructAttrSv_0,objImpComplexClassSvId=1 -s 1 -n FT1724testOI\n");
  printf("\n\t\t./imm-applier -d -C -c TestStructSv -k id -r id=TestStructAttrSv_0 -p objImpComplexClassSvId=1 -a testRuntimeAttrInt32 -v 4 -s 100 -n FT1724testOI\n");

  printf("\n\tModify struct\n");
  printf("\n\t\t./imm-applier -d -M -k id -r id=TestStructAttrSv_0,objImpComplexClassSvId=1 -a testRuntimeAttrInt32 -v 6 -s 100 -n FT1724testOI\n");

  printf("\n\tModify struct reference to empty value\n");
  printf("\n\t\t./imm-applier -d -M -k objImpComplexClassSvId -r objImpComplexClassSvId=1 -a TestStructAttrSv -v EMPTY_STRUCT -s 10000 -n FT1724testOI\n");

  printf("\n\tDelete struct\n");
  printf("\n\t\t./imm-applier -d -D -r objImpComplexClassSvId=1 -s 1 -n FT1724testOI\n");

}

/**
 * Create a runtime object in IMM.
 */
static void create_rt_test_object(const char* className, const char* parentObject, const SaImmAttrValuesT_2 *attribute1, const SaImmAttrValuesT_2 *attribute2)
{
	DEBUG("create_rt_test_object(): ENTER");
	SaAisErrorT rc;
	SaNameT *parent = NULL;
	const SaImmAttrValuesT_2 * attrVal[] = {attribute1,	attribute2,	NULL};
	debugAttrModArray(attrVal);

	if(parentObject != NULL)
	{
		parent = (SaNameT*)calloc(1, sizeof(SaNameT));
		strcpy((char*) parent->value, parentObject);
		parent->length = strlen(parentObject) + 1;
		if(DEBUG_ENABLED)
			printf("DEBUG: create_rt_test_object(): calling saImmOiRtObjectCreate_2() with immOiHnd: (%llu) className: (%s) parent: (%s)\n",immOiHnd,(SaImmClassNameT)className, parent->value);
	}
	else
	{
		if(DEBUG_ENABLED)
			printf("DEBUG: create_rt_test_object(): calling saImmOiRtObjectCreate_2() with immOiHnd: (%llu) className: (%s) parent: no parent given\n",immOiHnd,(SaImmClassNameT)className);
	}

	rc = saImmOiRtObjectCreate_2(immOiHnd, (SaImmClassNameT)className, parent, attrVal);
	if (rc == SA_AIS_OK)
	{
		if(DEBUG_ENABLED)
		printf("DEBUG: create_rt_test_object(): object created successfully\n");
	}
	else
	{
		fprintf(stderr, "create_rt_test_object: saImmOiRtObjectCreate_2 failed - %s\n",saf_error(rc));
		exit(rc);
	}
}

/**
 * Modify a runtime object.
 */
static void modify_rt_test_object(const char* dn, const SaImmAttrValuesT_2 *attr1, const SaImmAttrValuesT_2 *attr2)
{
	DEBUG("modify_rt_test_object(): ENTER");
	DEBUG_STR("modify_rt_test_object(): dn",dn);
	SaAisErrorT rc;
	SaInt32T modType = 3;
	SaNameT objName;

	strcpy((char*)objName.value, dn);
	objName.length = strlen(dn);
	DEBUG_STR("modify_rt_test_object(): objName",(const char*)objName.value);

	SaImmAttrModificationT_2 attrMod1 = {modType, *attr2};
	const SaImmAttrModificationT_2 * attrVal[] = {&attrMod1, NULL};

	DEBUG("modify_rt_test_object(): calling saImmOiRtObjectUpdate_2()");
	rc = saImmOiRtObjectUpdate_2(immOiHnd, &objName, (const SaImmAttrModificationT_2 **)attrVal);
	if (rc == SA_AIS_OK)
	{
		DEBUG("modify_rt_test_object(): successfully modified");
	}
	else
	{
		fprintf(stderr, "modify_rt_test_object: saImmOiRtObjectUpdate_2 failed - %s\n", saf_error(rc));
		exit(rc);
	}
}

/**
 * Delete runtime object in IMM.
 */
static void delete_rt_test_object(const char* dn)
{
	DEBUG("delete_rt_test_object(): ENTER");
	if(dn == NULL)
	{
		DEBUG("delete_rt_test_object(): dn = NULL");
	}
	else
	{
		DEBUG_STR("delete_rt_test_object(): dn",dn);
	}
	SaAisErrorT rc;
	SaNameT objName;

	strcpy((char*)objName.value, dn);
	objName.length = strlen(dn);

	DEBUG_STR("delete_rt_test_object(): calling saImmOiRtObjectDelete()",dn);
	DEBUG("delete_rt_test_object(): before calling saImmOiRtObjectDelete()");
	rc = saImmOiRtObjectDelete(immOiHnd, &objName);
	if (rc == SA_AIS_OK)
	{
		DEBUG_STR("delete_rt_test_object(): object successfully deleted",dn);
	}
	else
	{
		fprintf(stderr, "delete_rt_test_object: saImmOiRtObjectDelete failed - %s\n", saf_error(rc));
		exit(rc);
	}
	DEBUG("delete_rt_test_object(): returning SA_AIS_OK");
}

int main(int argc, char *argv[])
{
	SaAisErrorT rc;
	int operationMode = 0;
	unsigned int sleepTime = DEFAULT_SLEEP_TIME;

	/* create the runtime object */
	//char *dn = NULL;// = "cmNtfRtTest=1";
	char *attrName = NULL;
	char *className = NULL;
	char *keyAttrName = NULL;
	char *rdn = NULL;
	char *parentObject = NULL;
	char * attrValue = NULL;
	SaInt32T attrValue_INT32 = 0;

	int c;
	struct option long_options[] = {
			{"help", no_argument, 0, 'h'},
			{"debug", no_argument, 0, 'd'},
			{"create", no_argument, 0, 'C'},
			{"modify", no_argument, 0, 'M'},
			{"delete", no_argument, 0, 'D'},
			{"class", required_argument, 0, 'c'},
			{"keyAttr", required_argument, 0, 'k'},
			{"rdn", required_argument, 0, 'r'},
			{"parentObject", required_argument, 0, 'p'},
			{"attrName", required_argument, 0, 'a'},
			{"attrValue", required_argument, 0, 'v'},
			{"sleepTime", required_argument, 0, 's'},
			{"testOiName", required_argument, 0, 'n'},
			{0, 0, 0, 0}
	};

	while (1) {
		c = getopt_long(argc, argv, "hdCMDc:k:r:p:a:v:s:n:", long_options, NULL);

		if (c == -1)	/* have all command-line options have been parsed? */
			break;
		switch (c) {
		case 'h':
			DEBUG("help called");
			usage(basename(argv[0]));
			exit(EXIT_SUCCESS);
		case 'd':
			DEBUG_ENABLED = 1;
			DEBUG("debug enabled");
			break;
		case 'C':
			DEBUG("Operation mode: create object");
			operationMode = CREATE;
			break;
		case 'M':
			DEBUG("Operation mode: modify attribute");
			operationMode = MODIFY;
			break;
		case 'D':
			DEBUG("Operation mode: delete object");
			operationMode = DELETE;
			break;
		case 'c':
			className = strdup(optarg);
			if ((errno == EINVAL) || (errno == ERANGE)) {
				fprintf(stderr, "Error at reading '-c' / '--class' option\n");
				exit(EXIT_FAILURE);
			}
			DEBUG_STR("class name",className);
			break;
		case 'k':
			keyAttrName = strdup(optarg);
			if ((errno == EINVAL) || (errno == ERANGE))
			{
				fprintf(stderr, "Error at reading '-k' / '--keyAttr' option\n");
				exit(EXIT_FAILURE);
			}
			DEBUG_STR("key attribute name",keyAttrName);
			break;
		case 'r':
			rdn = strdup(optarg);
			if ((errno == EINVAL) || (errno == ERANGE))
			{
				fprintf(stderr, "Error at reading '-r' / '--rdn' option\n");
				exit(EXIT_FAILURE);
			}
			DEBUG_STR("rdn",rdn);
			break;
		case 'p':
			parentObject = strdup(optarg);
			if ((errno == EINVAL) || (errno == ERANGE))
			{
				fprintf(stderr, "Error at reading '-p' / '--parentObject' option\n");
				exit(EXIT_FAILURE);
			}
			DEBUG_STR("parentObject",parentObject);
			break;
		case 'a':
			attrName = strdup(optarg);
			if ((errno == EINVAL) || (errno == ERANGE))
			{
				fprintf(stderr, "Error at reading '-a' / '--attrName' option\n");
				exit(EXIT_FAILURE);
			}
			DEBUG_STR("attrName",attrName);
			break;
		case 'v':
			attrValue = strdup(optarg);
			if ((errno == EINVAL) || (errno == ERANGE))
			{
				fprintf(stderr, "Error at reading '-v' / '--attrValue' option\n");
				exit(EXIT_FAILURE);
			}
			DEBUG_STR("attrValue",attrValue);
			attrValue_INT32 = atoi(attrValue);
			if(attrValue_INT32 == 0)
			{
				attrValueType = ATTR_TYPE_STRING;
			}
			else
			{
				attrValueType = ATTR_TYPE_INT32;
			}
			break;
		case 's':
			sleepTime = atoi(optarg);
			if ((errno == EINVAL) || (errno == ERANGE))
			{
				fprintf(stderr, "Error at reading '-s' / '--sleepTime' option\n");
				exit(EXIT_FAILURE);
			}
			if(sleepTime == 0)
			{
				sleepTime = DEFAULT_SLEEP_TIME;
				fprintf(stderr, "Invalid sleepTime given, setting to default: %u sec\n",sleepTime);
			}
			break;
		case 'n':
			implementerName = strdup(optarg);
			if ((errno == EINVAL) || (errno == ERANGE))
			{
				fprintf(stderr, "Error at reading '-n' / '--testOiName' option\n");
				exit(EXIT_FAILURE);
			}
			DEBUG_STR("implementerName",implementerName);
			break;
		default:
			fprintf(stderr, "%c(%d) was given\n", c, c);
			fprintf(stderr, "Try '%s --help' for more information\n", argv[0]);
			exit(EXIT_FAILURE);
		}
	}

	// One of the 3 options must be given: "-c", "-m", "-d")
	if(operationMode < 1 || operationMode > 3)
	{
		fprintf(stderr, "Error: one of the 3 options must be given: \"-c\", \"-m\", \"-d\"");
		exit(EXIT_FAILURE);
	}

	//printf("sleepTime: (%u)\n", sleepTime);

	void* attr1[] = {&rdn};
	const SaImmAttrValuesT_2 attr_rdn = {
			.attrName = keyAttrName,
			.attrValueType = SA_IMM_ATTR_SASTRINGT,
			.attrValuesNumber = 1,
			.attrValues = attr1
	};

	SaImmValueTypeT attrImmType = SA_IMM_ATTR_SAINT32T;
	void *pAttrVal = NULL;
	int empty_value_case = 0;

	switch(attrValueType)
	{
	case ATTR_TYPE_INT32:
		if(DEBUG_ENABLED)
			printf("DEBUG: attrValue(INT32) is: (%d)\n", attrValue_INT32);
		attrImmType = SA_IMM_ATTR_SAINT32T;
		pAttrVal = (void*)&attrValue_INT32;
		break;
	case ATTR_TYPE_STRING:
		if(!strncmp(STRUCT_PATTERN, attrValue, 3))
		{
			DEBUG_STR("attrValue(SA_NAME_T)",attrValue);
			attrImmType = SA_IMM_ATTR_SANAMET;
			SaNameT *attrSA_NAME_T = (SaNameT*)calloc(1, sizeof(SaNameT));
			strcpy((char*) attrSA_NAME_T->value, attrValue);
			attrSA_NAME_T->length = strlen(attrValue) + 1;
			pAttrVal = (void*)attrSA_NAME_T;
		}
		else if(!strncmp(EMPTY_STRUCT_PATTERN, attrValue, 7))
		{
			DEBUG_STR("attrValue(SA_NAME_T)",attrValue);
			empty_value_case = 1;
			attrImmType = SA_IMM_ATTR_SANAMET;
			SaNameT *attrSA_NAME_T = (SaNameT*)calloc(1, sizeof(SaNameT));
			strcpy((char*) attrSA_NAME_T->value, attrValue);
			attrSA_NAME_T->length = strlen(attrValue) + 1;
			pAttrVal = (void*)attrSA_NAME_T;
		}
		else
		{
			DEBUG_STR("attrValue(STRING)", attrValue);
			attrImmType = SA_IMM_ATTR_SASTRINGT;
			pAttrVal = (void*)&attrValue;
		}
		break;
	default:
		fprintf(stderr, "Wrong attribute type was given\n");
		exit(EXIT_FAILURE);
	}

	void* attr2[] = {pAttrVal};

	// For number of values 0
	const SaImmAttrValuesT_2 attr_testAttr_empty = {
			.attrName = attrName,
			.attrValueType = attrImmType,
			.attrValuesNumber = 0,
			.attrValues = attr2
	};
	// For number of values 1
	const SaImmAttrValuesT_2 attr_testAttr = {
			.attrName = attrName,
			.attrValueType = attrImmType,
			.attrValuesNumber = 1,
			.attrValues = attr2
	};
	//************************************************************************
	if(DEBUG_ENABLED)
		printf("DEBUG: calling saImmOiInitialize_2() with IMM version{ma=%d,mi=%d,re=%d}\n",((SaVersionT*)&immVersion)->majorVersion,((SaVersionT*)&immVersion)->minorVersion,((SaVersionT*)&immVersion)->releaseCode);
	rc = saImmOiInitialize_2(&immOiHnd, NULL, (SaVersionT*)&immVersion);
	if (rc == SA_AIS_OK)
	{
		DEBUG("saImmOiInitialize_2(): OK");
		if(DEBUG_ENABLED)
			printf("DEBUG: calling saImmOiImplementerSet() with immOiHnd: (%llu) implementerName: (%s)\n",immOiHnd,implementerName);
		rc = saImmOiImplementerSet(immOiHnd, (const SaImmOiImplementerNameT)implementerName);
		if (rc == SA_AIS_OK)
		{
			DEBUG("saImmOiImplementerSet(): OK");
		}
		else
		{
			fprintf(stderr, "main: saImmOiImplementerSet failed - %s\n",saf_error(rc));
			exit(rc);
		}
	}
	else
	{
		fprintf(stderr, "main: saImmOiInitialize_2 failed - %s\n", saf_error(rc));
		exit(rc);
	}
	//************************************************************************
	switch(operationMode)
	{
	case CREATE:
		create_rt_test_object((const char*)className, parentObject, &attr_rdn, &attr_testAttr);
		break;
	case MODIFY:
		if(empty_value_case)
		{
			modify_rt_test_object((const char*)rdn, &attr_rdn, &attr_testAttr_empty);
		}
		else
		{
			modify_rt_test_object((const char*)rdn, &attr_rdn, &attr_testAttr);
		}
		break;
	case DELETE:
		delete_rt_test_object((const char*)rdn);
		break;
	default:
		fprintf(stderr, "Wrong operation mode (%d) was given\n",operationMode);
		exit(EXIT_FAILURE);
	}
	//************************************************************************

	DEBUG("wait few secs for COM SA to read IMM data while processing the NTF callback");
	/* This sleep is mandatory here
	 * Waiting few seconds for COM SA to read IMM (when processing the NTF callback)
	 * After waiting few secs "saImmOiFinalize" or exit process can be called.
	 * Note: calling finalize or exiting from process will make IMM to lock the runtime object params(see IMM doc).
	 */
	sleep(sleepTime);
	/*rc = saImmOiFinalize(immOiHnd);
	if (rc != SA_AIS_OK)
	{
		fprintf(stderr, "saImmOiFinalize failed - %s\n", saf_error(rc));
	}*/
	exit(0);
}
