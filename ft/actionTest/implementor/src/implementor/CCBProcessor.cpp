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
 * Author: qjalars
 * Reviewed: -
 *
 */

#include <sstream>
#include <string>
#include <stdio.h>
#include <saAis.h>
#include <saImmOm.h>
#include <saImmOi.h>
#include "CCBProcessor.h"
#include "constants.h"
#include "trace.h"
#include "dump.h"
#include "immutil.h"
#include "saname_utils.h"

using namespace std;

SaImmOiHandleT oiHandle;

void DebugDumpOperationParams( const SaImmAdminOperationParamsT_2 * const ctp)
{
	TRACE_INFO("Parameters:");
	TRACE_INFO("Name = %s", ctp->paramName);

	switch (ctp->paramType)
	{
	case SA_IMM_ATTR_SAINT32T:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SAINT32T");
			SaInt32T *tmpI = (SaInt32T *) ctp->paramBuffer;
			TRACE_INFO("Value = %d", *tmpI);

			DUMP ("%s SA_IMM_ATTR_SAINT32T %d",ctp->paramName, *tmpI);
		}
		break;
	case SA_IMM_ATTR_SAUINT32T:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SAUINT32T");
			SaUint32T *tmpUi = (SaUint32T *) ctp->paramBuffer;
			TRACE_INFO("Value = %d", *tmpUi);

			DUMP ("%s SA_IMM_ATTR_SAUINT32T %d",ctp->paramName,*tmpUi);
		}
		break;
	case SA_IMM_ATTR_SAINT64T:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SAINT64T");
			SaInt64T *tmpI64 = (SaInt64T *) ctp->paramBuffer;
			TRACE_INFO("Value = %lld", *tmpI64);

			DUMP ("%s SA_IMM_ATTR_SAINT64T %lld",ctp->paramName,*tmpI64);
		}
		break;

	case SA_IMM_ATTR_SAUINT64T:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SAUINT64T");
			SaUint64T *tmpU64 = (SaUint64T *) ctp->paramBuffer;
			TRACE_INFO("Value = %llu", *tmpU64);

			DUMP ("%s SA_IMM_ATTR_SAINT64T %llu",ctp->paramName,*tmpU64);
		}
		break;

	case SA_IMM_ATTR_SASTRINGT:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SASTRINGT");
			SaStringT* tmpStringPtr = (SaStringT *) ctp->paramBuffer;
			SaStringT tmpString = *tmpStringPtr;
			TRACE_INFO("Value = %s", tmpString);

			DUMP ("%s SA_IMM_ATTR_SASTRINGT %s", ctp->paramName, tmpString);
		}
		break;
	case SA_IMM_ATTR_SATIMET:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SATIMET");
			SaTimeT *tmpTime = (SaTimeT *) ctp->paramBuffer;           // int64
			TRACE_INFO("Value = %lld", *tmpTime);

			DUMP ("%s SA_IMM_ATTR_SATIMET %lld",ctp->paramName,*tmpTime);
		}
		break;
	case SA_IMM_ATTR_SANAMET:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SANAMET");
			SaNameT* tmpName = (SaNameT*) ctp->paramBuffer;          // struct
			stringstream sstr;
			sstr << "{length =" << saNameLen(tmpName);
			sstr << ", value = ";
			const char* pValue = saNameGet(tmpName);
			for (unsigned int i = 0; i < saNameLen(tmpName); i++) {
				sstr << pValue[i];
				if (i < saNameLen(tmpName)-1 ) {
					sstr << ",";
				}
			}
			sstr << "}";
			if (saNameLen(tmpName) > 0) {
				sstr << " " << saNameGet(tmpName);
			}
			string str = sstr.str();
			TRACE_INFO("Value = %s ", str.c_str());

			DUMP ("%s SA_IMM_ATTR_SANAMET %s", ctp->paramName,str.c_str());
		}
		break;
	case SA_IMM_ATTR_SAFLOATT:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SAFLOATT");
			SaFloatT *tmpFloat = (SaFloatT *) ctp->paramBuffer;           // float
			TRACE_INFO("Value = %f", *tmpFloat);

			DUMP ("%s SA_IMM_ATTR_SAFLOATT %f", ctp->paramName,*tmpFloat);
		}
		break;
	case SA_IMM_ATTR_SADOUBLET:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SADOUBLET");
			SaDoubleT *tmpDouble = (SaDoubleT *) ctp->paramBuffer;         // double
			TRACE_INFO("Value = %f", *tmpDouble);

			DUMP ("%s SA_IMM_ATTR_SADOUBLET %f", ctp->paramName,*tmpDouble);
		}
		break;
	case SA_IMM_ATTR_SAANYT:
		{
			TRACE_INFO("Type = SA_IMM_ATTR_SAANYT");
			SaAnyT* tmpAny = (SaAnyT*) ctp->paramBuffer;                 // struct
			stringstream sstr;
			sstr << "{bufferSize =" << tmpAny->bufferSize;
			sstr << "value = ";
			for (int i = 0; i < (int) tmpAny->bufferSize; i++) {
				sstr << tmpAny->bufferAddr[i];
				if (i < (int) tmpAny->bufferSize-1 ) {
					sstr << ",";
				}
			}
			sstr << "}";
			string str = sstr.str();
			TRACE_INFO("Value = %s ", str.c_str());

			DUMP ("%s SA_IMM_ATTR_SAANYT %s",ctp->paramName, str.c_str());
		}
		break;

	default :
		TRACE_ERROR("Type = <UNKNOWN>");

	}

}

/**
 * Handles administrative operations.
 */
#define RETURN_PARAMS_NUM 10000 // The number of returned parameters (limited in IMM to 127)

void handleAdminOperation(SaImmOiHandleT immOiHandle, SaInvocationT invocation, const SaNameT *objectName,
				SaImmAdminOperationIdT operationId, const SaImmAdminOperationParamsT_2 **params)
{
	SaAisErrorT rc = SA_AIS_OK;
	TRACE_INFO("ActionAppl SaImmOiAdminOperationCallbackT_2 ");
	TRACE_INFO("operationId=%llu", operationId);
	SaImmAdminOperationParamsT_2** returnParams = new SaImmAdminOperationParamsT_2*[RETURN_PARAMS_NUM];
	for (int i = 0; i < RETURN_PARAMS_NUM; i++)
	{
		returnParams[i] = NULL;
	}

	if (NULL == params) {
		TRACE_INFO("No parameters");
		DUMP ("NO PARAMETERS");
		return;
	}

	if (params[0] != NULL) {
		for (int i = 0; params[i] != NULL; i++)
		{
			DebugDumpOperationParams(params[i]);

			if (operationId == 999 && i==0 && params[i]->paramBuffer != NULL) {
				rc = *((SaAisErrorT *) params[i]->paramBuffer);
			}

			if (operationId == 1000 && i==0 && params[0]->paramBuffer != NULL) {
				if (params[0]->paramType == SA_IMM_ATTR_SASTRINGT) {
					// Set filename
					SaStringT* tmpStringPtr = (SaStringT *) params[0]->paramBuffer;
					SaStringT tmpString = *tmpStringPtr;
					string fileName ((char*) tmpString);
					Dump::setFileName(fileName);
				}
			}
			//sdp875: testErrorString
			if (operationId == 31) {
				char errStr[] = "errorString";
				//const char errorText[] ="@CoMNbi@forced ERROR: This is for test purpose";
				char** pError = (char **) (params[0]->paramBuffer);
				char* pErrorText = *pError;
				char* errorText = new char[strlen(pErrorText) + 1];
				strcpy(errorText, pErrorText);
				TRACE_INFO("ErrorText is: %s", errorText);
				returnParams[0] = new SaImmAdminOperationParamsT_2;
				returnParams[0]->paramName = errStr;
				returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
				returnParams[0]->paramBuffer = &errorText;
				returnParams[1] = NULL;
				rc = SA_AIS_ERR_NO_OP;
			}
			//sdp872: UC1 return the input param simple type single value EcimInt32
			if (operationId == 40) {
//			if (operationId == 44) {
				char nameStr[] = "EcimInt32";
				TRACE_INFO("SDP872 UC1: return the input single EcimInt32 %d", *((int*) params[0]->paramBuffer));
				returnParams[0] = new SaImmAdminOperationParamsT_2;
				returnParams[0]->paramName = nameStr;
				returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
				returnParams[0]->paramBuffer = params[0]->paramBuffer;
				returnParams[1] = NULL;
				rc = SA_AIS_OK;
			}
			//sdp872: UC1 return the input param simple type single value EcimString
			if (operationId == 41) {
				char errStr[] = "EcimString";
				char** pError = (char **) (params[0]->paramBuffer);
				char* pErrorText = *pError;
				char* errorText = new char[strlen(pErrorText) + 1];
				strcpy(errorText, pErrorText);
				TRACE_INFO("SDP872: UC1 return the input param simple type single value EcimString: %s", errorText);
				returnParams[0] = new SaImmAdminOperationParamsT_2;
				returnParams[0]->paramName = errStr;
				returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
				returnParams[0]->paramBuffer = &errorText;
				returnParams[1] = NULL;
				rc = SA_AIS_OK;
			}
			//sdp872: UC1 return the input single value param of simple type BOOL
			if (operationId == 46) {
				char nameStr[] = "EcimBool";
				TRACE_INFO("SDP872 UC1: return the input single BOOL %d", *((int*) params[0]->paramBuffer));
				returnParams[0] = new SaImmAdminOperationParamsT_2;
				returnParams[0]->paramName = nameStr;
				returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
				returnParams[0]->paramBuffer = params[0]->paramBuffer;
				returnParams[1] = NULL;
				rc = SA_AIS_OK;
			}

			//sdp872: UC1 return variable number of hardcoded values EcimInt32.
			// the number of values to be returned is determined by the input parameter
			if (operationId == 48) {
				char nameStr[] = "EcimInt32_";
				char seqNum[RETURN_PARAMS_NUM][32];
				int values[RETURN_PARAMS_NUM];
				int *countPtr = (int *) params[0]->paramBuffer;
				int count = *countPtr;

				TRACE_INFO("SDP872 UC1: returning %d of hardcoded EcimInt32 values", count);
				int k;

				// to prevent writing beyond the array boundary
				if (count >= RETURN_PARAMS_NUM)
				{
					count = RETURN_PARAMS_NUM - 1;
				}

				for (k = 0; k < count; k++)
				{
					sprintf(seqNum[k], "%s%u", nameStr, k + 1);
					values[k] = k;
					returnParams[k] = new SaImmAdminOperationParamsT_2;
					returnParams[k]->paramName = seqNum[k];
					returnParams[k]->paramType = SA_IMM_ATTR_SAINT32T;
					returnParams[k]->paramBuffer = &values[k];
				}

				returnParams[k] = NULL; // terminator
				rc = SA_AIS_OK;
			}

			//sdp872: UC1 ( no output)
			if (operationId == 49) {
				TRACE_INFO("SDP872 UC1: returning nothing");
			}

			// the (operationId == 50) is in the 'else' section below
			if (operationId == 71)     // negative TC returning struct with invalid names
			{
				/* this is causing "Invalid struct member name. Expected 8". Detected error, but not doing the right thing! Need to add some extra error checking for number after the first number.
				   char nameStr1[] = "TestStruct01_1_7_stringMemb";
				   char nameStr2[] = "TestStruct01_1_8_intMember";
				*/
		        // get the test case number
				int *testCaseNum = (int *) params[0]->paramBuffer;
				std::string name1;
				std::string name2;
				switch (*testCaseNum)
				{
					case 1:
						TRACE_INFO("SDP872 UC1: Negative TC I1: invalid paramNames");
						name1 = "1_TestStruct01_1_stringMemb";
						name2 = "1_TestStruct01_2_intMember";
						break;

					case 2:
						TRACE_INFO("SDP872 UC1: Negative TC I2: invalid paramNames");
						name1 = "1TestStruct01_1_stringMemb";
						name2 = "12TestStruct01_2_intMember";
						break;

					case 3:
						TRACE_INFO("SDP872 UC1: Negative TC I3: invalid paramNames");
						name1 = "TestStruct01_1stringMemb";
						name2 = "TestStruct01_2intMember";
						break;

					case 4:
						TRACE_INFO("SDP872 UC1: Negative TC I4: invalid paramNames");
						name1 = "TestStruct01_1_3";
						name2 = "TestStruct01_2_4";
						break;

					case 5:
						TRACE_INFO("SDP872 UC1: Negative TC I5: invalid paramNames");
						name1 = "TestStruct01_stringMemb_1_2";
						name2 = "TestStruct01_intMember_3_4";
						break;

					case 6:
						TRACE_INFO("SDP872 UC1: Negative TC I6: invalid paramNames");
						name1 = "TestStruct01_1_stringMemb_1_2";
						name2 = "TestStruct01_2_intMember_3_4";
						break;

					case 7:
						TRACE_INFO("SDP872 UC1: Negative TC I7: invalid paramNames");
						name1 = "TestStruct01_1_stringMemb_hel";
						name2 = "TestStruct01_2_intMember_hel";
						break;

					case 8:
						TRACE_INFO("SDP872 UC1: Negative TC I8: invalid paramNames");
						name1 = "_TestStruct01_stringMemb";
						name2 = "_TestStruct01_intMember";
						break;

					case 9:
						TRACE_INFO("SDP872 UC1: Negative TC I9: invalid paramNames");
						name1 = "TestStruct01_stringMemb_";
						name2 = "TestStruct01_intMember_";
						break;

					case 10:
						TRACE_INFO("SDP872 UC1: Negative TC I10: invalid paramNames");
						name1 = "TestStruct01__stringMemb";
						name2 = "TestStruct01__intMember";
						break;

					case 11:
						TRACE_INFO("SDP872 UC1: Negative TC I11: invalid paramNames");
						name1 = "TestStruct01_stringMemb__1";
						name2 = "TestStruct01_intMember__1";
						break;

					case 12:
						TRACE_INFO("SDP872 UC1: Negative TC I12: invalid paramNames");
						name1 = "TestStruct01__1_stringMemb";
						name2 = "TestStruct01__2_intMember";
						break;

					case 13:
						TRACE_INFO("SDP872 UC1: Negative TC I13: invalid paramNames");
						name1 = "TestStruct01_1__stringMemb";
						name2 = "TestStruct01_2__intMember";
						break;

					case 14:
						TRACE_INFO("SDP872 UC1: Negative TC I14: invalid paramNames");
						name1 = "TestStruct01_stringMemb__";
						name2 = "TestStruct01_intMember__";
						break;

					case 15:
						TRACE_INFO("SDP872 UC1: Negative TC I15: invalid paramNames");
						name1 = "TestStruct01_1_stringMemb__1";
						name2 = "TestStruct01_2_intMember__2";
						break;
					default:
						TRACE_ERROR("SDP872 UC1: ERROR: Negative TC: Invalid test case number: %d ", *testCaseNum);
						break;
				}

				char *nameStr1 = new char[name1.length() + 1];
				char *nameStr2 = new char[name2.length() + 1];
				strcpy(nameStr1, name1.c_str());
				strcpy(nameStr2, name2.c_str());

				int value1 = 987;
				char strMember1[] = "You are not supposed to see this text !!!!";
				char* strParam = new char[strlen(strMember1) + 1];
				strcpy(strParam, strMember1);

				TRACE_INFO("SDP872 UC1: Negative TC: returning hardcoded struct with invalid paramNames (of string and EcimInt32 value): %s, %d", strMember1, value1);
				returnParams[0] = new SaImmAdminOperationParamsT_2;
				returnParams[0]->paramName = nameStr1;
				returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
				returnParams[0]->paramBuffer = &strParam;

				returnParams[1] = new SaImmAdminOperationParamsT_2;
				returnParams[1]->paramName = nameStr2;
				returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
				returnParams[1]->paramBuffer = &value1;

				returnParams[2] = NULL; // terminator
				rc = SA_AIS_OK;
			}
		}
	}
	else  // allow actions with no input parameters to return result params
	{
		//sdp872: UC1 return a struct with 2 members: string and int
		if ((operationId == 42) ||
			(operationId == 69))     // negative TC expecting 2 struct elements, returning 1.
		{
			char nameStr1[] = "TestStruct01_stringMemb";
			char nameStr2[] = "TestStruct01_intMember";
			int value1 = 5678;
			char strMember1[] = "The returned test string using new DX model";
			char* strParam = new char[strlen(strMember1) + 1];
			strcpy(strParam, strMember1);

			TRACE_INFO("SDP872 UC1: returning hardcoded struct of string and EcimInt32 value: %s, %d", strMember1, value1);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[0]->paramBuffer = &strParam;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &value1;

			returnParams[2] = NULL; // terminator
			rc = SA_AIS_OK;
		}
		//sdp872: UC1 return a struct with 2 members: array of strings with 2 values and array of int with 2 values
		if (operationId == 43) {
			char nameStr1[] = "TestStruct02_stringArrayMember_1";
			char nameStr2[] = "TestStruct02_stringArrayMember_2";
			char nameStr3[] = "TestStruct02_intArrayMember_1";
			char nameStr4[] = "TestStruct02_intArrayMember_2";
			int value1 = 3333;
			int value2 = 4444;
			char strMember1[] = "The FIRST returned test string";
			char strMember2[] = "The SECOND returned test string";
			char* strParam1 = new char[strlen(strMember1) + 1];
			strcpy(strParam1, strMember1);
			char* strParam2 = new char[strlen(strMember2) + 1];
			strcpy(strParam2, strMember2);

			TRACE_INFO("SDP872 UC1: struct of array of 2 strings and array of 2 EcimInt32 values:\n\t%s, \n\t%s, \n\t%d, \n\t%d",
					   strMember1, strMember2, value1, value2);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[0]->paramBuffer = &strParam1;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[1]->paramBuffer = &strParam2;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr3;
			returnParams[2]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[2]->paramBuffer = &value1;

			returnParams[3] = new SaImmAdminOperationParamsT_2;
			returnParams[3]->paramName = nameStr4;
			returnParams[3]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[3]->paramBuffer = &value2;

			returnParams[4] = NULL; // terminator
			rc = SA_AIS_OK;
		}

		//sdp872: UC1 return two hardcoded values EcimInt32
		if (operationId == 44) {
			char nameStr1[] = "EcimInt32_1";
			char nameStr2[] = "EcimInt32_2";
			int value1 = 1111;
			int value2 = 2222;
			TRACE_INFO("SDP872 UC1: returning two hardcoded EcimInt32 values %d %d ", value1, value2);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &value1;
			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &value2;
			returnParams[2] = NULL; // terminator
			rc = SA_AIS_OK;
		}

		//sdp872: UC1 return a struct with  members: one of all types
		if (operationId == 45) {
			char nameStr1[]  = "TestStructAllTypes_memberBool";
			char nameStr2[]  = "TestStructAllTypes_memberInt8";
			char nameStr3[]  = "TestStructAllTypes_memberInt16";
			char nameStr4[]  = "TestStructAllTypes_memberInt32";
			char nameStr5[]  = "TestStructAllTypes_memberInt64";
			char nameStr6[]  = "TestStructAllTypes_memberUint8";
			char nameStr7[]  = "TestStructAllTypes_memberUint16";
			char nameStr8[]  = "TestStructAllTypes_memberUint32";
			char nameStr9[]  = "TestStructAllTypes_memberUint64";
			char nameStr10[] = "TestStructAllTypes_memberString";
			char nameStr11[] = "TestStructAllTypes_memberDerivedInt";
			char nameStr12[] = "TestStructAllTypes_memberDerivedString";
			char nameStr13[] = "TestStructAllTypes_memberEnum";
			char nameStr14[] = "TestStructAllTypes_memberReference";

			int       valueBool   = 0;
			int       valueInt8   = -88;            // char
			int       valueInt16  = -1616;          // short
			int       valueInt32  = -32323232;      // int
			long long valueInt64  = -646464646464;

			unsigned int       valueUint8  = 88;
			unsigned int       valueUint16 = 1616;
			unsigned int       valueUint32 = 32323232;
			unsigned long long valueUint64 = 646464646464;

			char strMember1[] = "Another returned test string";
			char* strParam1 = new char[strlen(strMember1) + 1];
			strcpy(strParam1, strMember1);

			int valueDerivedInt = 7777;

			char strMember2[] = "Returned DERIVED test string";
			char* strParam2 = new char[strlen(strMember2) + 1];
			strcpy(strParam2, strMember2);

			int valueEnum = 2; // the ENUM range in the model is [1..2]
#ifdef TEST_FOR_LONG_DN
			char strMember3[] = "actionTestId=1,sdp617ActiontestRootId=This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_This_is_very_long_string_1";              // must be IMM style
#else
			char strMember3[] = "actionTestId=1,sdp617ActiontestRootId=1";              // must be IMM style
#endif
			char* strParam3 = new char[strlen(strMember3) + 1];
			strcpy(strParam3, strMember3);

			TRACE_INFO("SDP872 UC1: struct of all types, one each:\
\n\t%s, \n\t%s, \n\t%s, \n\t%d, \n\t%d, \n\t%d, \n\t%d, \n\t%lld, \n\t%u, \n\t%u, \n\t%u, \n\t%llu, \n\t%d, \n\t%d",
					   strMember1, strMember2, strMember3, valueBool,
					   valueInt8,  valueInt16,  valueInt32,  valueInt64,
					   valueUint8, valueUint16, valueUint32, valueUint64,
					   valueDerivedInt, valueEnum);

			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;             // bool
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &valueBool;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &valueInt8;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr3;
			returnParams[2]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[2]->paramBuffer = &valueInt16;

			returnParams[3] = new SaImmAdminOperationParamsT_2;
			returnParams[3]->paramName = nameStr4;
			returnParams[3]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[3]->paramBuffer = &valueInt32;

			returnParams[4] = new SaImmAdminOperationParamsT_2;
			returnParams[4]->paramName = nameStr5;
			returnParams[4]->paramType = SA_IMM_ATTR_SAINT64T;
			returnParams[4]->paramBuffer = &valueInt64;

			returnParams[5] = new SaImmAdminOperationParamsT_2;
			returnParams[5]->paramName = nameStr6;
			returnParams[5]->paramType = SA_IMM_ATTR_SAUINT32T;
			returnParams[5]->paramBuffer = &valueUint8;

			returnParams[6] = new SaImmAdminOperationParamsT_2;
			returnParams[6]->paramName = nameStr7;
			returnParams[6]->paramType = SA_IMM_ATTR_SAUINT32T;
			returnParams[6]->paramBuffer = &valueUint16;

			returnParams[7] = new SaImmAdminOperationParamsT_2;
			returnParams[7]->paramName = nameStr8;
			returnParams[7]->paramType = SA_IMM_ATTR_SAUINT32T;
			returnParams[7]->paramBuffer = &valueUint32;

			returnParams[8] = new SaImmAdminOperationParamsT_2;
			returnParams[8]->paramName = nameStr9;
			returnParams[8]->paramType = SA_IMM_ATTR_SAUINT64T;
			returnParams[8]->paramBuffer = &valueUint64;

			returnParams[9] = new SaImmAdminOperationParamsT_2;
			returnParams[9]->paramName = nameStr10;            // string
			returnParams[9]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[9]->paramBuffer = &strParam1;

			returnParams[10] = new SaImmAdminOperationParamsT_2;
			returnParams[10]->paramName = nameStr11;            // derived int
			returnParams[10]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[10]->paramBuffer = &valueDerivedInt;

			returnParams[11] = new SaImmAdminOperationParamsT_2;
			returnParams[11]->paramName = nameStr12;            // derived string
			returnParams[11]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[11]->paramBuffer = &strParam2;

			returnParams[12] = new SaImmAdminOperationParamsT_2;
			returnParams[12]->paramName = nameStr13;            // enum
			returnParams[12]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[12]->paramBuffer = &valueEnum;

			returnParams[13] = new SaImmAdminOperationParamsT_2;
			returnParams[13]->paramName = nameStr14;            // reference
			returnParams[13]->paramType = SA_IMM_ATTR_SANAMET;
			SaNameT* refData = new SaNameT;
			saNameSet(strParam3, refData);
			returnParams[13]->paramBuffer = refData;

			returnParams[14] = NULL; // terminator

			rc = SA_AIS_OK;
		}
		//sdp872: UC1 return the two input values of simple type BOOL
		if (operationId == 47) {
			char nameStr1[] = "EcimBool_1";
			char nameStr2[] = "EcimBool_2";

			int valueBool1 = 0;    // False
//			int valueBool2 = 777;  // True
			int valueBool2 = -77;  // True

			TRACE_INFO("SDP872 UC1: return two hardcoded values of type BOOL");
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &valueBool1;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &valueBool2;

			returnParams[2] = NULL;
			rc = SA_AIS_OK;
		}


		//sdp872: UC1 return one hardcoded value EcimInt32 (no input)
		if (operationId == 50) {
			char nameStr1[] = "EcimInt32_1";
			int value1 = 1234;
			TRACE_INFO("SDP872 UC1: returning a hardcoded EcimInt32 value of %d", value1);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &value1;
			returnParams[1] = NULL; // terminator
			rc = SA_AIS_OK;
		}
		//sdp872: UC1 return two instances of struct with 2 members: string and int
		if ((operationId == 51) ||
			(operationId == 65))  // negative test case - expecting single struct, but getting many
		{
			char nameStr1[] = "TestStruct01_1_stringMemb";
			char nameStr2[] = "TestStruct01_1_intMember";
			char nameStr3[] = "TestStruct01_2_stringMemb";
			char nameStr4[] = "TestStruct01_2_intMember";
			int value1 = 1111;
			int value2 = 2222;
			char strMember1[] = "The returned FIRST test string";
			char strMember2[] = "The returned SECOND test string";
			char* strParam1 = new char[strlen(strMember1) + 1];
			strcpy(strParam1, strMember1);
			char* strParam2 = new char[strlen(strMember2) + 1];
			strcpy(strParam2, strMember2);

			TRACE_INFO("SDP872 UC1: returning two hardcoded struct instances of struct type string and EcimInt32: %s, %d",
					   strMember1, value1, strMember2, value2);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[0]->paramBuffer = &strParam1;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &value1;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr3;
			returnParams[2]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[2]->paramBuffer = &strParam2;

			returnParams[3] = new SaImmAdminOperationParamsT_2;
			returnParams[3]->paramName = nameStr4;
			returnParams[3]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[3]->paramBuffer = &value2;

			returnParams[4] = NULL; // terminator
			rc = SA_AIS_OK;
		}

		//sdp872: UC1 return two instances of struct with 2 members: array of strings with 2 values and array of int with 2 and 3 values
		if (operationId == 52)
		{
			char nameStr1[] = "TestStruct02_1_stringArrayMember_1";
			char nameStr2[] = "TestStruct02_1_stringArrayMember_2";
			char nameStr3[] = "TestStruct02_1_intArrayMember_1";
			char nameStr4[] = "TestStruct02_1_intArrayMember_2";
			char nameStr5[] = "TestStruct02_2_stringArrayMember_1";
			char nameStr6[] = "TestStruct02_2_stringArrayMember_2";
			char nameStr7[] = "TestStruct02_2_intArrayMember_1";
			char nameStr8[] = "TestStruct02_2_intArrayMember_2";
			char nameStr9[] = "TestStruct02_2_intArrayMember_3";

			int value1 = 1111;
			int value2 = 2222;
			int value3 = 3333;
			int value4 = 4444;
			int value5 = 5555;

			char strMember1[] = "The FIRST returned test string in the FIRST struct";
			char strMember2[] = "The SECOND returned test string in the FIRST struct";
			char strMember3[] = "The FIRST returned test string in the SECOND struct";
			char strMember4[] = "The SECOND returned test string in the SECOND struct";

			char* strParam1 = new char[strlen(strMember1) + 1];
			strcpy(strParam1, strMember1);
			char* strParam2 = new char[strlen(strMember2) + 1];
			strcpy(strParam2, strMember2);
			char* strParam3 = new char[strlen(strMember3) + 1];
			strcpy(strParam3, strMember3);
			char* strParam4 = new char[strlen(strMember4) + 1];
			strcpy(strParam4, strMember4);

			TRACE_INFO("SDP872 UC1: two structs of array of 2 strings and array of 2 and 3 EcimInt32 values:\n\t%s, \n\t%s, \n\t%d, \n\t%d,\
 \n\t%s, \n\t%s, \n\t%d, \n\t%d, \n\t%d",
					   strMember1, strMember2, value1, value2, strMember3, strMember4, value3, value4, value5);

			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[0]->paramBuffer = &strParam1;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[1]->paramBuffer = &strParam2;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr3;
			returnParams[2]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[2]->paramBuffer = &value1;

			returnParams[3] = new SaImmAdminOperationParamsT_2;
			returnParams[3]->paramName = nameStr4;
			returnParams[3]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[3]->paramBuffer = &value2;

			returnParams[4] = new SaImmAdminOperationParamsT_2;
			returnParams[4]->paramName = nameStr5;
			returnParams[4]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[4]->paramBuffer = &strParam3;

			returnParams[5] = new SaImmAdminOperationParamsT_2;
			returnParams[5]->paramName = nameStr6;
			returnParams[5]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[5]->paramBuffer = &strParam4;

			returnParams[6] = new SaImmAdminOperationParamsT_2;
			returnParams[6]->paramName = nameStr7;
			returnParams[6]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[6]->paramBuffer = &value3;

			returnParams[7] = new SaImmAdminOperationParamsT_2;
			returnParams[7]->paramName = nameStr8;
			returnParams[7]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[7]->paramBuffer = &value4;

			returnParams[8] = new SaImmAdminOperationParamsT_2;
			returnParams[8]->paramName = nameStr9;
			returnParams[8]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[8]->paramBuffer = &value5;

			returnParams[9] = NULL; // terminator
			rc = SA_AIS_OK;
		}

		//sdp872: UC1 return three hardcoded values EcimInt32 in mixed order
		if (operationId == 53) {
			char nameStr1[] = "EcimInt32_1";
			char nameStr2[] = "EcimInt32_2";
			char nameStr3[] = "EcimInt32_3";
			int value1 = 1111;
			int value2 = 2222;
			int value3 = 3333;
			TRACE_INFO("SDP872 UC1: returning three hardcoded EcimInt32 values %d %d %d", value1, value2, value3);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &value1;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr2;
			returnParams[2]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[2]->paramBuffer = &value2;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr3;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &value3;

			returnParams[3] = NULL; // terminator
			rc = SA_AIS_OK;
		}
		//sdp872: UC1 test for optional struct member (some data member is not provided, but the struct is still returned to COM)
		if (operationId == 54)
		{
			char nameStr1[] = "TestStruct02_1_stringArrayMember_1";
			char nameStr2[] = "TestStruct02_1_stringArrayMember_2";
			char nameStr3[] = "TestStruct02_1_intArrayMember_1";
			char nameStr4[] = "TestStruct02_1_intArrayMember_2";
			char nameStr7[] = "TestStruct02_2_intArrayMember_1";
			char nameStr8[] = "TestStruct02_2_intArrayMember_2";
			char nameStr9[] = "TestStruct02_2_intArrayMember_3";

			int value1 = 111;
			int value2 = 222;
			int value3 = 333;
			int value4 = 444;
			int value5 = 555;

			char strMember1[] = "The FIRST returned test string in the FIRST struct";
			char strMember2[] = "The SECOND returned test string in the FIRST struct";

			char* strParam1 = new char[strlen(strMember1) + 1];
			strcpy(strParam1, strMember1);
			char* strParam2 = new char[strlen(strMember2) + 1];
			strcpy(strParam2, strMember2);

			TRACE_INFO("SDP872 UC1: test for optional struct member (the second struct element does not have the array of strings at all):\n\t%s, \n\t%s, \n\t%d, \n\t%d,\
 \n\t%d, \n\t%d, \n\t%d",
					   strMember1, strMember2, value1, value2, value3, value4, value5);

			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[0]->paramBuffer = &strParam1;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[1]->paramBuffer = &strParam2;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr3;
			returnParams[2]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[2]->paramBuffer = &value1;

			returnParams[3] = new SaImmAdminOperationParamsT_2;
			returnParams[3]->paramName = nameStr4;
			returnParams[3]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[3]->paramBuffer = &value2;

			returnParams[4] = new SaImmAdminOperationParamsT_2;
			returnParams[4]->paramName = nameStr7;
			returnParams[4]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[4]->paramBuffer = &value3;

			returnParams[5] = new SaImmAdminOperationParamsT_2;
			returnParams[5]->paramName = nameStr8;
			returnParams[5]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[5]->paramBuffer = &value4;

			returnParams[6] = new SaImmAdminOperationParamsT_2;
			returnParams[6]->paramName = nameStr9;
			returnParams[6]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[6]->paramBuffer = &value5;

			returnParams[7] = NULL; // terminator
			rc = SA_AIS_OK;
		}


		//sdp872: UC1 negative test cases - expected INT, we return string
		if ((operationId == 60) ||   // expected int
			(operationId == 66))     // expected bool
		{
			char nameStr[] = "EcimString";
			char strMember1[] = "The returned UNEXPECTED test string";
			char* strParam1 = new char[strlen(strMember1) + 1];
			strcpy(strParam1, strMember1);
			TRACE_INFO("SDP872: UC1 return a string: %s", strParam1);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr;
			returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[0]->paramBuffer = &strParam1;
			returnParams[1] = NULL;
			rc = SA_AIS_OK;
		}
		//sdp872: UC1 Negative test cases - return int when something else is expected
		if ((operationId == 61) || // expected string
			(operationId == 62) || // expected reference
			(operationId == 63) || // expected struct
			(operationId == 67) || // expeted enum
			(operationId == 68)) // expected 2 ints, but getting a single one
		{
			char nameStr1[] = "EcimInt32_";
			int value1 = 999;
			TRACE_INFO("SDP872 UC1: returning EcimInt32 value %d", value1);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &value1;

			returnParams[1] = NULL; // terminator
			rc = SA_AIS_OK;
		}
		//sdp872: UC1 Negative test cases
		if (operationId == 64) { // expected single int, getting three
			char nameStr1[] = "EcimInt32_1";
			char nameStr2[] = "EcimInt32_2";
			char nameStr3[] = "EcimInt32_3";
			int value1 = 11;
			int value2 = 22;
			int value3 = 33;
			TRACE_INFO("SDP872 UC1: returning three hardcoded EcimInt32 values %d %d %d", value1, value2, value3);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &value1;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr2;
			returnParams[2]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[2]->paramBuffer = &value2;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr3;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &value3;

			returnParams[3] = NULL; // terminator
			rc = SA_AIS_OK;
		}
		//sdp872: UC1 Negative test cases
		if (operationId == 70) { // use invalid param name
			char nameStr1[] = "7_EcimInt";
			char nameStr2[] = "8_EcimInt";
			char nameStr3[] = "9_EcimInt";
			int value1 = 11;
			int value2 = 22;
			int value3 = 33;
			TRACE_INFO("SDP872 UC1: returning three hardcoded EcimInt32 values %d %d %d, but using invalid names", value1, value2, value3);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[0]->paramBuffer = &value1;

			returnParams[2] = new SaImmAdminOperationParamsT_2;
			returnParams[2]->paramName = nameStr2;
			returnParams[2]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[2]->paramBuffer = &value2;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr3;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &value3;

			returnParams[3] = NULL; // terminator
			rc = SA_AIS_OK;
		}
#if 0
		// moved in the 'then' section of the 'if' to take input params
		if (operationId == 71)     // negative TC returning struct with invalid names
		{
			/* this is causing "Invalid struct member name. Expected 8". Detected error, but not doing the right thing! Need to add some extra error checking for number after the first number.
			char nameStr1[] = "TestStruct01_1_7_stringMemb";
			char nameStr2[] = "TestStruct01_1_8_intMember";
			*/

			char nameStr1[] = "TestStruct01_1_7_stringMemb";
			char nameStr2[] = "TestStruct01_1_8_intMember";
			int value1 = 987;
			char strMember1[] = "You are not supposed to see this text !!!!";
			char* strParam = new char[strlen(strMember1) + 1];
			strcpy(strParam, strMember1);

			TRACE_INFO("SDP872 UC1: returning hardcoded struct of string and EcimInt32 value: %s, %d", strMember1, value1);
			returnParams[0] = new SaImmAdminOperationParamsT_2;
			returnParams[0]->paramName = nameStr1;
			returnParams[0]->paramType = SA_IMM_ATTR_SASTRINGT;
			returnParams[0]->paramBuffer = &strParam;

			returnParams[1] = new SaImmAdminOperationParamsT_2;
			returnParams[1]->paramName = nameStr2;
			returnParams[1]->paramType = SA_IMM_ATTR_SAINT32T;
			returnParams[1]->paramBuffer = &value1;

			returnParams[2] = NULL; // terminator
			rc = SA_AIS_OK;
		}
#endif
	}

	if (returnParams != NULL)
	{
		for (int i = 0; returnParams[i] != NULL; i++)
		{
			DebugDumpOperationParams(returnParams[i]);
		}
	}

	TRACE_INFO("ReturnParam=%d", rc);

	rc = saImmOiAdminOperationResult_o2(immOiHandle, invocation, rc, (const SaImmAdminOperationParamsT_2**) returnParams);

	TRACE_INFO("After calling saImmOiAdminOperationResult_o2()");

	if (SA_AIS_OK != rc)
	{
		TRACE_ERROR("saImmOiAdminOperationResult_o2 FAILED %u", rc);
	}
}


/**
 * Creates a callback structure with all registered function pointers for handling call-backs from IMM
 */
SaImmOiCallbacksT_2 cbFunctions = {
	//holder will all the registered functions
	handleAdminOperation,
	0,
	0,
	0,
	0,
	0,
	0,
	0
};

SaImmOiCallbacksT_2 createCallbackStruct()
{
	return cbFunctions;
}
