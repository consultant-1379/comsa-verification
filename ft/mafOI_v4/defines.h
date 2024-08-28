/*
 * Important:
 *
 * This is an example configuration file for the test component
 * It is possible to configure the test component using this file(defines.h which is clearcase element)
 * But it is recommended to create a new (not clearcase element) file with the name "defines2.h"
 * then the Makefile will automatically build with "defines2.h"
 *
 *   Modified: xnikvap 2012-08-30  support for COM MO SPI Ver.3 (Ver.1 is not supported any more)
 *
 */

/* The component will be registered under this name.
 * That makes possible to run more then 1 instance of the test component
 * Syslog will be prefixed with this name also
 * If COMPONENT_NAME not defined then the default component name ("MAFOiComponent") will be used
 */
#define COMPONENT_NAME "testComp1120"

// To be able to use the test component as event producer you need to define this
#define ALARMS

/* Preconfiguration of the return values of the following functions are possible:
 *        createMo, deleteMo, setMo, getMo, action, join, prepare, commit, finish, abort
 *
 *        Note: it doesn't mean that these function will automatically return the preconfigured value, they can fail because of other reasons.
 *
 *        The reason to set these:
 *
 *                    -to reject unwanted callbacks
 *                    -test negative cases where some(or all) of the return values especially set other then MafOk.
 *
 */
#define returnValueConfig returnValues.createMo = MafOk; returnValues.deleteMo = MafOk; returnValues.setMo = MafFailure; returnValues.getMo = MafFailure; returnValues.action = MafOk; returnValues.join = MafOk; returnValues.prepare = MafOk; returnValues.commit = MafOk; returnValues.finish = MafOk; returnValues.abort = MafOk;


//Class registration:
#define REG1 "/ManagedElement/ObjImpEmptyClass"
#define REG1_PERMISSION "YES"

#define REG2 "/ManagedElement/ObjImpEmptyClass/TestClassOne"
#define REG2_PERMISSION "YES"

#define REG3 "/ManagedElement/ObjImpEmptyClass/TestClassOne/TestClassTwo"
#define REG3_PERMISSION "YES"

#define REG4 "/ManagedElement/ObjImpEmptyClass.MAID/TestClassOne.MAIID/TestClassTwo.MAIIID"
#define REG4_PERMISSION "YES"

//Object registration:
#define REG5 "ManagedElement=1,SystemFunctions=1,Fm=1"
#define REG5_PERMISSION "YES"

#define REG6 "ManagedElement=1,ObjImpTestClass=1,ActionTest=1"
#define REG6_PERMISSION "YES"

#define REG7 "ManagedElement=1,ObjImpEmptyClass.MAID=1,TestClassOne.MAIID=1"
#define REG7_PERMISSION "YES"

//Attribute data for Runtime Non-cached attributes:

#define ATTR1 "ManagedElement=1,ObjImpTestClass=1,testRuntimeInt8"
#define ATTR1_TYPE MafOamSpiMoAttributeType_3_INT8
#define ATTR1_VALUE "111"

#define ATTR2 "ManagedElement=1,ObjImpTestClass=1,testRuntimeInt16"
#define ATTR2_TYPE MafOamSpiMoAttributeType_3_INT16
#define ATTR2_VALUE "222"

#define ATTR3 "ManagedElement=1,ObjImpTestClass=1,testRuntimeInt32"
#define ATTR3_TYPE MafOamSpiMoAttributeType_3_INT32
#define ATTR3_VALUE "333"

#define ATTR4 "ManagedElement=1,ObjImpTestClass=1,testRuntimeInt64"
#define ATTR4_TYPE MafOamSpiMoAttributeType_3_INT64
#define ATTR4_VALUE "444"

#define ATTR5 "ManagedElement=1,ObjImpTestClass=1,testRuntimeUint8"
#define ATTR5_TYPE MafOamSpiMoAttributeType_3_UINT8
#define ATTR5_VALUE "555"

#define ATTR6 "ManagedElement=1,ObjImpTestClass=1,testRuntimeUint16"
#define ATTR6_TYPE MafOamSpiMoAttributeType_3_UINT16
#define ATTR6_VALUE "666"

#define ATTR7 "ManagedElement=1,ObjImpTestClass=1,testRuntimeUint32"
#define ATTR7_TYPE MafOamSpiMoAttributeType_3_UINT32
#define ATTR7_VALUE "777"

#define ATTR8 "ManagedElement=1,ObjImpTestClass=1,testRuntimeUint64"
#define ATTR8_TYPE MafOamSpiMoAttributeType_3_UINT64
#define ATTR8_VALUE "888"

#define ATTR9 "ManagedElement=1,ObjImpTestClass=1,testRuntimeString"
#define ATTR9_TYPE MafOamSpiMoAttributeType_3_STRING
#define ATTR9_VALUE "Runtime String is NEVER RELAXING"

#define ATTR10 "ManagedElement=1,ObjImpTestClass=1,testRuntimeBool"
#define ATTR10_TYPE MafOamSpiMoAttributeType_3_BOOL
#define ATTR10_VALUE "1"

// For testing complex data types it is possible to define multi-value structs. See example below
// Be aware that the syntax won't be checked (just space-filtered)
#define ATTR11 "ManagedElement=1,ObjImpTestClass=1,testRuntimeStruct"
#define ATTR11_TYPE MafOamSpiMoAttributeType_3_STRUCT
#define ATTR11_VALUE "{testRuntimeInt8(INT8) = 50, testRuntimeUint32(UINT32) =99, testRuntimeUint64(UINT64) = 3333},{testRuntimeInt8(INT32) = 20, testRuntimeUint32(UINT16) =13}"

// For HS37161
// Runtime attribute with type struct, support multi-type, multi-value attribute members.
#define ATTR12 "ManagedElement=1,ObjImpTestClass=1,testRuntimeStruct"
#define ATTR12_TYPE MafOamSpiMoAttributeType_3_STRUCT
#define ATTR12_VALUE "{testRuntimeInt8(INT8) = 50;51, testRuntimeUint32(UINT32) =99, testRuntimeUint64(UINT64) = 3333},{testRuntimeInt8(INT32) = 20, testRuntimeUint32(UINT16) =13;14;15}"

#define ACTION1 "ManagedElement=1,ObjImpTestClass=1,ActionTest=1,control"
#define ACTION1_TYPE MafOamSpiMoAttributeType_3_STRING

/* SDP1694 -support MAF SPI */
#define maf_returnValueConfig returnValues.createMo = MafOk; returnValues.deleteMo = MafOk; returnValues.setMo = MafFailure; returnValues.getMo = MafFailure; returnValues.action = MafOk; returnValues.join = MafOk; returnValues.prepare = MafOk; returnValues.commit = MafOk; returnValues.finish = MafOk; returnValues.abort = MafOk;

#define MAF_ATTR1_TYPE MafOamSpiMoAttributeType_3_INT8
#define MAF_ATTR2_TYPE MafOamSpiMoAttributeType_3_INT16
#define MAF_ATTR3_TYPE MafOamSpiMoAttributeType_3_INT32
#define MAF_ATTR4_TYPE MafOamSpiMoAttributeType_3_INT64
#define MAF_ATTR5_TYPE MafOamSpiMoAttributeType_3_UINT8
#define MAF_ATTR6_TYPE MafOamSpiMoAttributeType_3_UINT16
#define MAF_ATTR7_TYPE MafOamSpiMoAttributeType_3_UINT32
#define MAF_ATTR8_TYPE MafOamSpiMoAttributeType_3_UINT64
#define MAF_ATTR9_TYPE MafOamSpiMoAttributeType_3_STRING
#define MAF_ATTR10_TYPE MafOamSpiMoAttributeType_3_BOOL
#define MAF_ATTR11_TYPE MafOamSpiMoAttributeType_3_STRUCT
#define MAF_ACTION1_TYPE MafOamSpiMoAttributeType_3_STRING
