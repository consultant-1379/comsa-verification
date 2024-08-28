/* Stub file to be able to compile and link the OAM files */

 
/*
*
*/

/*
*/


/*
 * Include files
 */

#include <stdlib.h>
#include "OamSpiModelRepositoryDummy.h"
/*
 *  defines
 */
 
 /* Remove this definition to remove debugging printf's */
#define _DEBUG_PRINTF
#define _MAX_RETRY_COUNT	20

/*
 * typedefs
 */
 /* Here we will typedef things that in real life are constant structs */
typedef struct DummyComOamSpiMoc			DummyComOamSpiMocT; 
typedef struct DummyComOamSpiMom			DummyComOamSpiMomT; 
typedef struct DummyComOamSpiContainment	DummyComOamSpiContainmentT;
typedef struct DummyComOamSpiMoAttribute	DummyComOamSpiMoAttributeT;
 
typedef struct DummyComOamSpiContainment 
{
	ComOamSpiGeneralPropertiesT 	generalProperties; 
	DummyComOamSpiMomT* 			mom;
	DummyComOamSpiMocT* 			parentMoc;
	DummyComOamSpiMocT* 			childMoc;
	ComOamSpiMultiplicityRangeT 	cardinality; 
	bool 							isSystemCreated;
	DummyComOamSpiContainmentT* 	nextContainmentSameParentMoc;
	DummyComOamSpiContainmentT* 	nextContainmentSameChildMoc;
} DummyComOamSpiContainmentT; 
 
 
typedef struct DummyComOamSpiMoc 
{
	ComOamSpiGeneralPropertiesT 	generalProperties;
	DummyComOamSpiMomT* 			mom; 
	bool 							isReadOnly;
	bool 							isRoot;
	char* 							constraint;
	DummyComOamSpiMoAttributeT* 	moAttribute;
	DummyComOamSpiContainmentT* 	childContainment; 
	DummyComOamSpiContainmentT* 	parentContainment;
} DummyComOamSpiMocT;
 
typedef struct DummyComOamSpiMoAttribute 
{
    ComOamSpiGeneralPropertiesT generalProperties;
    DummyComOamSpiMocT* 		moc;
	ComOamSpiMoAttributeType 	type;
	ComOamSpiDerivedDatatypeT* 	derivedDatatype;
	ComOamSpiEnumT* 			enumDatatype;
	ComOamSpiStructT* 			structDatatype;
	DummyComOamSpiMocT * 		referencedMoc; 
	bool 						isKey;
	bool 						isMandatory;
	bool 						isPersistent;
	bool 						isReadOnly;
    ComOamSpiMultiplicityRangeT multiplicity;
	bool 						isOrdered;
	bool 						isUnique;
	char* 						defaultValue;
	char* 						unit; 
	ComOamSpiMoAttributeT* 		next;
} DummyComOamSpiMoAttributeT;

typedef struct DummyComOamSpiMom 
{ 
	ComOamSpiGeneralPropertiesT generalProperties; 
	char* 						version;
	char* 						release;
	char* 						namespaceURI;
	char* 						namespacePrefix;
	DummyComOamSpiMocT* 		rootMoc;
	char* 						docNo;
	char* 						revision;
	char* 						author;
	char* 						organization;
	DummyComOamSpiMomT*			next;
} DummyComOamSpiMomT;
/*
 * constants
 *
 */
 
 
/*
 *  Global variables
 * 
 */
 
// static SaSelectionObjectT 	theSelectionObject;

/* Forward declaration of functions 
 * 
 */

static ComReturnT getMoms(const ComOamSpiMomT ** result);

static ComReturnT getMoc(const char* 		momName, 
						 const char* 		momVersion, 
						 const char*	 	mocName,
						 ComOamSpiMocT**	result);
						 
/******* TO DO!!!!! Get the real string values in here **************************************/


static ComOamSpiModelRepository_1T InterfaceStruct = {{"OurComponentName","OurInterfaceName","1"},	
														  		  getMoms, 
														  		  getMoc}; 

ComOamSpiModelRepository_1T*     theModelRepository_p = &InterfaceStruct;

static DummyComOamSpiContainmentT ContainmentThree = {{"ContainmentThree","A containment", "A standard"}, NULL, NULL, NULL, {0,0}, false, NULL, NULL };														  		  
														  		  
static DummyComOamSpiMocT MocTThree = {{"safApp=safLogService", "Another moc to test with", "Another standard"},NULL , false, true, "" , NULL, NULL,&ContainmentThree };														  		  
														  		  
static DummyComOamSpiMomT MomTThree = { {"MomThreeElement", "A mom to test with", "A standard", ComOamSpiStatus_CURRENT , "Some hidden info" },
								   "1.0", "AZ1B2","","", &MocTThree, "DocOne", "1.1", "M.I. Sahlin", "Monsters Inc", NULL};														  		  
														  		  
static DummyComOamSpiContainmentT ContainmentTwo = {{"ContainmentTwo","A containment", "A standard"},NULL, &MocTThree, NULL, {0,0}, false, NULL, NULL };

static DummyComOamSpiMocT MocTTwo = {{"MeId=1", "Another moc to test with", "Another standard"},NULL , false, true, "" , NULL, NULL,&ContainmentTwo };
														  		
static DummyComOamSpiMomT MomTTwo = { {"MomTWOElement", "A mom to test with", "A standard", ComOamSpiStatus_CURRENT , "Some hidden info" },
								   "1.0", "AZ1B2","","", &MocTTwo, "DocOne", "1.1", "D.R. Jekyl", "Monsters Inc", &MomTThree};
								   
static DummyComOamSpiContainmentT ContainmentOne = {{"ContainmentOne","A containment", "A standard"},NULL, &MocTTwo, NULL, {0,0}, false, NULL, NULL };
														  		  
static DummyComOamSpiMocT MocTOne = {{"safApp=safImmService", "A moc to test with", "Another standard"},NULL , false, true, "" , NULL, NULL,&ContainmentOne };
														  		


static DummyComOamSpiMomT MomTOne = { {"MomOneElement", "A mom to test with", "A standard", ComOamSpiStatus_CURRENT , "Some hidden info" },
								   "1.0", "AZ1B2","","", &MocTOne, "DocOne", "1.1", "G.O. Dzilla", "Monsters Inc", &MomTTwo};
/*
*	Global i/f
*/

//ComOamSpiModelRepository_1T* ExportOamSpiModelRepository(void)
//{
//	return (ComOamSpiModelRepository_1T*)&InterfaceStruct;
//}


/*
 *  Routines called via the pointer interface
 *
 */
 
 /*
  *  getMoms
  */

static ComReturnT getMoms(const ComOamSpiMomT ** result)
{
static bool Initialized = false;

	if (!Initialized)
	{
		MocTOne.mom 	= &MomTOne;
		MocTTwo.mom 	= &MomTTwo;
		MocTThree.mom 	= &MomTThree;
		ContainmentOne.mom = &MomTOne;
		ContainmentTwo.mom = &MomTTwo;
		ContainmentThree.mom = &MomTThree;
		Initialized = true;
	}
	*result = (ComOamSpiMomT*)&MomTOne;
	ComReturnT	myRetVal = ComOk;
	return myRetVal;
}

static ComReturnT getMoc(const char* 		momName, 
						 const char* 		momVersion, 
						 const char*	 	mocName,
						 ComOamSpiMocT**	result)

{
	ComReturnT	myRetVal = ComOk;
	return myRetVal;
}
