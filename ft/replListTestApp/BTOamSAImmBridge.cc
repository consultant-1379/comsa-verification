/**
* stubs and tests for OamSAImmBridge
*
*   Modify: xnikvap 2012-08-30  support for COM MO SPI Ver.3 (Ver.1 is not supported any more)
*/

#define IMM_A_02_01


#include <string>
#include <list>
#include <vector>
#include <map>
#include <ctype.h>

#include <assert.h>

#include "saAis.h"
#include "saImm.h"
#include "saImmOm.h"
#include "ComMgmtSpiCommon.h"
#include "ComMgmtSpiComponent_1.h"
#include "ComMgmtSpiInterfacePortal_1.h"
#include "ComOamSpiModelRepository_1.h"
#include "ComOamSpiManagedObject_3.h"
#include "OamSATransactionRepository.h"
#include "OamSACache.h"
#include "TxContext.h"
#include "ImmCmd.h"

// STUBS

void mydebug(char* str){
	printf(str);	
}


void ENTER(){};
void LEAVE(){};
#define DEBUG printf;

// TESTS
#include "OamSAImmBridge.h"


//////////////////////////////////////////////////////
// Utilities
//////////////////////////////////////////////////////
/**
 * Convert a SA_NAME to a char* 
 */
char* makeCString(const SaNameT* saName){
	char* tmp = new char[saName->length+1];
	memcpy(tmp,saName->value,saName->length);
	tmp[saName->length]=0; // make a c-string!!	
	return tmp;
}

/**
 * Convert a char* to an SaNameT
 */
SaNameT* makeSaNameT(const char* cstr){
	SaNameT* saname = new SaNameT;
	int len = strlen(cstr);
	if(len>SA_MAX_NAME_LENGTH){
		len = SA_MAX_NAME_LENGTH;
	}
	saname->length = len;
	memcpy(saname->value,cstr,len);
	return saname;
}

///////////////////////////
//STUB IMPL IMM
///////////////////////////'

/////// IMM tracks memory //////////
class ImmMemoryTracker {
public:
	std::vector<SaImmAttrDefinitionT_2**> attrDefs;
	std::vector<SaImmAttrValuesT_2**> attrVals;

	void reg(SaImmAttrDefinitionT_2** defArray){
			attrDefs.push_back(defArray);
	}
	
	void reg(SaImmAttrValuesT_2** valArray){
			attrVals.push_back(valArray);
	}


	void clear(SaImmAttrValuesT_2* v){
		SaImmAttrValuesT_2* res = v;
		for(int i=0;i<res->attrValuesNumber;i++){	
			switch(res->attrValueType){
				case SA_IMM_ATTR_SANAMET:
					delete (SaNameT*)res->attrValues[i];
				break;
				case SA_IMM_ATTR_SASTRINGT:
					delete [] (char*)(*(char**)res->attrValues[i]);
					delete (char**)res->attrValues[i];		
				break;
			}
		}
		delete [] res->attrName;
		delete [] res->attrValues;
		delete v;
	}

	void clear(SaImmAttrDefinitionT_2* d){
		//delete [] (char*)d->attrName;  // why invalid!?!?
		delete d;
	}


	void clear(SaImmAttrValuesT_2** vArray){
		int i=0;
		while(vArray[i] != NULL){
			clear(vArray[i]);
			i = i+1;
		}
		delete [] vArray;
	}
	
	void clear(SaImmAttrDefinitionT_2** dArray){
		int i=0;
		while(dArray[i] != NULL){
			clear(dArray[i]);
			i = i+1;
		}
		delete [] dArray;
	}
	
	void cleanup(){
		for(int i=0;i<attrDefs.size();i++){
			clear(attrDefs[i]);
		}
		for(int i=0;i<attrVals.size();i++){
			clear(attrVals[i]);
		}
	}
};

// Globale Memory tracker!
ImmMemoryTracker immMemoryTrackerG;




class ImmItem {
	// default constructor and we never copy
public:

	unsigned int type;
	std::vector<std::string> data;
	
	bool isEmpty(){
		return data.size() == 0;
	}
	
	std::string toString(){
		std::string outp;
		outp.append("ImmItem( type=");
		switch(type){
			case 0: outp.append("0"); break;
			case 1: outp.append("1");break;
			case 2: outp.append("2");break;
			case 3: outp.append("3");break;
			case 4: outp.append("4");break;
			case 5: outp.append("5");break;
			case 6: outp.append("6");break;
			case 7: outp.append("7");break;
			case 8: outp.append("8");break;
			case 9: outp.append("9");break;
			default:outp.append("n");break;
		}
		outp.append(", data=");
		for(int i=0;i<data.size();i++){
			outp.append(data[i]);
			outp.append(" ");
		}
		outp.append(")");
		return outp;
	}
};

class ImmAttrDef {
	public:
	unsigned int attrType;
	std::string attrName;
};

class ImmClassDef {
	public:
	std::vector<ImmAttrDef> attrDef;
};



class ImmStorage {

   // Storage backend for fake IMM impl
   std::map<std::string,ImmItem> immStorage;
   std::map<std::string,int> createLog;
   std::map<std::string,int> deleteLog;
   std::map<std::string, ImmClassDef> immClassStorage;

public:

  void reset(){
  	immStorage.clear();
  	createLog.clear();
  	deleteLog.clear();
  	immClassStorage.clear();
  }

  int getItemCount(){
  	return immStorage.size();
  }
  
  bool isEmpty(){
  	return immStorage.empty();
  }
  
/**
 * Add a class attribute definition, used by saImmOmClassDecriptionGet_2
 */
  void addImmClassAttributeDef(std::string className, std::string attrName, unsigned int attrType){
  	ImmAttrDef attr;
  	attr.attrType = attrType;
  	attr.attrName = attrName;
  	immClassStorage[className].attrDef.push_back(attr);
  }

  ImmClassDef getClassDef(std::string className){
  	return immClassStorage[className];
  }


  void addToImmStorage(const char* dn, const char* attr, unsigned int type, std::vector<std::string> values){
	std::string key = makeKey(dn,attr);
	ImmItem item;
	item.type = type;
	item.data = values;	
	immStorage[key] = item;
  }
  
  ImmItem readFromImmStorage(const char* dn, const char* attr){  	
	std::string key = makeKey(dn,attr);
	if(immStorage.find(key)==immStorage.end()){
		printf("Error: no such element, dn=%s attribute=%s\n",dn,attr);
		printf("Available elements:\n");
		for(std::map<std::string,ImmItem>::iterator it = immStorage.begin() ; it!= immStorage.end(); it++){
			printf("   [%s]=>%s\n",(*it).first.c_str(),(*it).second.toString().c_str());
		}
	}
	ImmItem item = immStorage[key];  // creates default value if not found.
  	return item;
  }
   
  ImmItem deleteFromImmStorage(const char* dn, const char* attr){  	
  	immStorage.erase(makeKey(dn,attr));
  } 
   
  void logCreate(const char* dn){
  	createLog[std::string(dn)] = 1;
  }
  
  void logDelete(const char* dn){
  	deleteLog[std::string(dn)] = 1;
  }
  
  private:
  
  std::string makeKey(const char* dn, const char* attr){
  	std::string key(dn);
  	key.append(",");
  	key.append(attr);
  	return key;  	
  }
  
};

// Global IMM storage!!
ImmStorage immStorageG;

//////////////////////////////////////////////////////
// Setup model repository
//////////////////////////////////////////////////////

// Cleaners
void cleanUp(struct ComOamSpiStructMember* m);
void cleanUp(struct ComOamSpiMom* mom);
void cleanUp(struct ComOamSpiMoc* moc);
void cleanUp(struct ComOamSpiContainment* cont);
void cleanUp(struct ComOamSpiMoAttribute* attr);
void cleanUp(struct ComOamSpiStruct* s);
void cleanUp(struct ComOamSpiStructMember* m);

/// Builders
 
struct ComOamSpiMom* makeMom(char* name, struct ComOamSpiMoc* rootMoc){
	struct ComOamSpiMom* mom = new struct ComOamSpiMom;
	mom->generalProperties.name = (char*) name;
	mom->next = NULL;
	mom->rootMoc = rootMoc;
	mom->version = "Unit testing 101";
	mom->release = "BETA";
	rootMoc->mom = mom;
	return mom;
}

void cleanUp(struct ComOamSpiMom* mom){
	delete mom->generalProperties.name;
	delete mom->version;
	delete mom->release;	
	delete mom;
}

struct ComOamSpiMoc* makeMoc(char* name, struct ComOamSpiMoAttribute* attrList){
	struct ComOamSpiMoc* moc = new struct ComOamSpiMoc;
	moc->generalProperties.name = (char*) name;
	moc->moAttribute = attrList;
	moc->parentContainment = NULL;
	moc->childContainment = NULL;
	return moc;	
}

void cleanUp(struct ComOamSpiMoc* moc){
	delete moc->generalProperties.name;
	delete moc;
}

struct ComOamSpiContainment* makeContainment(ComOamSpiMocT* parent, ComOamSpiMocT* child, ComOamSpiContainmentT* nextSameParent, ComOamSpiContainmentT* nextSameChild){
	struct ComOamSpiContainment* cont = new struct ComOamSpiContainment;
	cont->parentMoc = parent;
	cont->childMoc = child;
	cont->nextContainmentSameParentMoc = nextSameParent;
	cont->nextContainmentSameChildMoc = nextSameChild;
	return cont;
}

void cleanUp(struct ComOamSpiContainment* cont){
	delete cont;
}

struct ComOamSpiContainment*  makeContainment(struct ComOamSpiMoc* parent, struct ComOamSpiMoc* child){
	struct ComOamSpiContainment* cont = new struct ComOamSpiContainment;
	cont->parentMoc = parent;
	cont->childMoc = child;
	cont->nextContainmentSameParentMoc = NULL;
	cont->nextContainmentSameChildMoc = NULL;
	
	// update child and parent
	parent->childContainment = cont;
	child->parentContainment = cont;
	//parent->mom = mom;
	//child->mom = mom;
	return cont;
}


struct ComOamSpiMoAttribute* makeAttribute(char* name, ComOamSpiMoAttributeTypeT type, struct ComOamSpiMoAttribute* next){
	struct ComOamSpiMoAttribute* attr = new struct ComOamSpiMoAttribute;
	attr->generalProperties.name = (char*) name;
	attr->type = type;
	//attr->moc = moc;
	attr->next = next;
	return attr;
}

void cleanUp(struct ComOamSpiMoAttribute* attr){
	delete attr->generalProperties.name;
	delete attr->generalProperties.description;
	delete attr->generalProperties.specification;
	delete attr->generalProperties.hidden;
	delete attr;
}

struct ComOamSpiMoAttribute* makeAttribute(char* name, struct ComOamSpiStruct* structData, struct ComOamSpiMoAttribute* next){
	struct ComOamSpiMoAttribute* attr = new struct ComOamSpiMoAttribute;
	attr->generalProperties.name = (char*) name;
	attr->generalProperties.description = "This is an attribute in UnitTesting";
	attr->generalProperties.specification = "A specification";
	attr->generalProperties.status = ComOamSpiStatus_CURRENT;
	attr->generalProperties.hidden = "The hidden!!";
	
	attr->type = ComOamSpiMoAttributeType_STRUCT; // implicit
	attr->structDatatype = structData;
	//attr->moc = moc;
	attr->next = next;
	return attr;
}

struct ComOamSpiStruct* makeStruct(char* name, struct ComOamSpiStructMember* memberList){
	struct ComOamSpiStruct* s = new struct ComOamSpiStruct;
	s->generalProperties.name = name;
	s->members = memberList;
	return s;
}

void cleanUp(struct ComOamSpiStruct* s){
	delete s->generalProperties.name;
	delete s;
}

struct ComOamSpiStructMember* makeStructMember(char* name, ComOamSpiDatatype type, struct ComOamSpiStructMember* next){
	struct ComOamSpiStructMember* m = new struct ComOamSpiStructMember;	
	m->generalProperties.name = name;
	m->memberType.type = type;
	m->next = next;
	return m;
}

void cleanUp(struct ComOamSpiStructMember* m){
	delete m->generalProperties.name;
	delete m;
}

// Export the global MOM pointer
//
//
static struct ComOamSpiMom* theGlobalMom;

void setMom(struct ComOamSpiMom* theMom){
	theGlobalMom = theMom;
}

//
// Interface SPI
//
static ComReturnT getMoms(const ComOamSpiMomT ** result)
{
        *result = (ComOamSpiMomT*)theGlobalMom;
        return ComOk;
}

static ComReturnT getMoc(const char*            momName,
                                                 const char*            momVersion,
                                                 const char*            mocName,
                                                 ComOamSpiMocT**        result)

{
        return ComOk;
}

static ComOamSpiModelRepository_1T InterfaceStruct = {{"","","1"},getMoms,getMoc, NULL};
ComOamSpiModelRepository_1T*     theModelRepository_p = &InterfaceStruct;




//////////////////////////////////////////////////////
// LOG
//////////////////////////////////////////////////////
#ifdef  __cplusplus
extern "C" {
#endif

void coremw_log(int priority, const char* fmt, ...)
{
	//printf("LOG");
};
#ifdef  __cplusplus
}
#endif

//////////////////////////////////////////////////////
// SPI Interface portal exports
//////////////////////////////////////////////////////
ComMgmtSpiInterfacePortal_1T* portal = NULL;

ComReturnT registerParticipant(ComOamSpiTransactionHandleT txHandle,
                                ComOamSpiTransactionalResource_1T * resp)
{
        return ComOk;
}

ComReturnT setContext(ComOamSpiTransactionHandleT txHandle,
                        ComOamSpiTransactionalResource_1T *resource, void *context)
{
        return ComOk;
}

ComReturnT getContext(ComOamSpiTransactionHandleT txHandle,
                        ComOamSpiTransactionalResource_1T *resource, void **context)
{
                return ComOk;
}

ComReturnT getLockPolicy(ComOamSpiTransactionHandleT txHandle, ComLockPolicyT *result)
{
                return ComOk;
}

ComOamSpiTransaction_1T  type = { {"","",""}, registerParticipant, setContext, getContext, getLockPolicy};

ComOamSpiTransaction_1* ComOamSpiTransactionStruct_p = &type;




#ifdef  __cplusplus
extern "C" {
#endif
ComReturnT join(ComOamSpiTransactionHandleT txHandle)
{
	return ComOk;
}
ComReturnT prepare(ComOamSpiTransactionHandleT txHandle)
{
	return ComOk;
}
ComReturnT commit(ComOamSpiTransactionHandleT txHandle)
{
	return ComOk;
}
ComReturnT myabort(ComOamSpiTransactionHandleT txHandle)
{
	return ComOk;
}
ComReturnT finish(ComOamSpiTransactionHandleT txHandle)
{
	return ComOk;
}

ComOamSpiTransactionalResource_1T myTxRes = { {"","",""}, join, prepare, commit, myabort, finish};

ComOamSpiTransactionalResource_1T* 
ExportOamSATransactionalResourceInterface(void)
{
	return &myTxRes;
}
#ifdef  __cplusplus
}
#endif



//////////////////////////////////////////////////////
// IMM API
//////////////////////////////////////////////////////
SaAisErrorT
saImmOmSearchFinalize(SaImmSearchHandleT searchHandle)
{
	printf("----> saImmOmSearchFinalize \n");
	return SA_AIS_OK;
}

SaAisErrorT
saImmOmCcbFinalize(SaImmCcbHandleT ccbHandle)
{
	printf("----> saImmOmCcbFinalize \n");
	return SA_AIS_OK;
}
         
SaAisErrorT
saImmOmAdminOwnerFinalize(SaImmAdminOwnerHandleT ownerHandle)
{
	printf("----> saImmOmAdminOwnerFinalize \n");
	return SA_AIS_OK;
}


SaAisErrorT
saImmOmAccessorGet_2(SaImmAccessorHandleT accessorHandle,
                      const SaNameT *objectName,
                      const SaImmAttrNameT *attributeNames, SaImmAttrValuesT_2 ***attributes)
{
	// used directly by cache
	printf("----> saImmOmAccessorGet_2 \n");
	
	char* tmp = new char[objectName->length+1];
	memcpy(tmp,objectName->value,objectName->length);
	tmp[objectName->length] = 0;
	
	std::string dn(tmp);
	std::string attrName(attributeNames[0]);
	
	
	printf("saImmOmAccessorGet_2 dn=%s attrName=%s \n",dn.c_str(), attrName.c_str());
		
	CM::ImmCmdOmAccessorGet immGet(NULL,dn,attrName,attributes); // no need to run execute() on command, we stubbed this command!
	
		
	delete[] tmp;
	return SA_AIS_OK;
}

SaAisErrorT
saImmOmFinalize(SaImmHandleT immHandle)
{
	printf("----> saImmOmFinalize \n");
	return SA_AIS_OK;
}

SaAisErrorT
saImmOmInitialize(SaImmHandleT *immHandle, const SaImmCallbacksT *immCallbacks, SaVersionT *version)
{
	printf("----> saImmOmInitialize \n");
	(*immHandle) = (SaImmHandleT) 1; // set to value != 0 to inidcate success!
	return SA_AIS_OK;
}

SaAisErrorT
saImmOmAccessorInitialize(SaImmHandleT immHandle, SaImmAccessorHandleT *accessorHandle)
{
	printf("----> saImmOmAccessorInitialize \n");
	(*accessorHandle) = (SaImmAccessorHandleT) 1; // set to value != 0 to show success
	return SA_AIS_OK;
}

SaAisErrorT
saImmOmAccessorFinalize(SaImmAccessorHandleT accessorHandle)
{
	printf("----> saImmOmAccessorFinalize \n");
	return SA_AIS_OK;	
}


SaAisErrorT
saImmOmClassDescriptionGet_2(SaImmHandleT immHandle,
                              const SaImmClassNameT className,
                              SaImmClassCategoryT *classCategory, SaImmAttrDefinitionT_2 ***attrDefinitions)
{
	printf("----> saImmOmClassDescriptionGet_2 \n");

	ImmClassDef immDef = immStorageG.getClassDef(className);
	
	SaImmAttrDefinitionT_2** defArray = new SaImmAttrDefinitionT_2*[immDef.attrDef.size() + 1];

    for(int i=0; i<immDef.attrDef.size();i++){
    	
		SaImmAttrDefinitionT_2* def = new SaImmAttrDefinitionT_2;
		
		def->attrName = (char *) immDef.attrDef[i].attrName.c_str();
		def->attrValueType = (SaImmValueTypeT) immDef.attrDef[i].attrType;
		def->attrFlags = 0;
		def->attrDefaultValue = NULL;
		printf("   attrDef: name=%s type=%d\n",immDef.attrDef[i].attrName.c_str(), immDef.attrDef[i].attrType);
		defArray[i] = def;		
    }
	defArray[immDef.attrDef.size()] = NULL;
	
	(*attrDefinitions) = defArray;
	immMemoryTrackerG.reg(defArray);
	return SA_AIS_OK;
}


///////////////////////////////////
// ImmCommands
///////////////////////////////////


SaVersionT CM::ImmCmd::mVersion = { 'A', 02, 01 }; 

CM::ImmCmd::ImmCmd(TxContext * txContextIn, std::string cmd, int retries)
: mTxContextIn( txContextIn ), mCmd( cmd ), mRetries( retries )
{
	ENTER();
	LEAVE();
}

CM::ImmCmd::~ImmCmd()
{
//	ENTER();
//	int size = mTmpDns.size();
//	for (int i=0; i<size; i++)
//	{
//		delete mTmpDns.at(i);
//	}
//	LEAVE();
}

SaAisErrorT
CM::ImmCmd::execute()
{
    return SA_AIS_OK;
}

SaNameT * 
CM::ImmCmd::toSaNameT(std::string &dnIn)
{
	ENTER();
    // temp SaNameTs are deleted in destructor
 //   SaNameT * dn = NULL;
  //  if (dnIn.size()>0) {
   //     dn = new SaNameT();
    //    mTmpDns.push_back(dn);
        //from the root
  //      dn->length = dnIn.length();
  //      snprintf((char*)(dn->value), SA_MAX_NAME_LENGTH,"%s", dnIn.c_str());
  //  }
	//LEAVE();
    return NULL;
}

//------------------------ ImmCmdOmInit ----------------------------------------------------
CM::ImmCmdOmInit::ImmCmdOmInit(TxContext * txContextIn)
: ImmCmd(txContextIn, "saImmOmInitialize")
{
	ENTER();
	LEAVE();
}

SaAisErrorT
CM::ImmCmdOmInit::doExecute()
{
    return SA_AIS_OK;
}

//------------------------ ImmCmdOmAccessorInit ----------------------------------------------------

CM::ImmCmdOmAccessorInit::ImmCmdOmAccessorInit( TxContext * txContextIn)
: ImmCmd(txContextIn, "saImmOmAccessorInitialize")
{
	ENTER();
	LEAVE();
}

SaAisErrorT
CM::ImmCmdOmAccessorInit::doExecute()
{
	return SA_AIS_OK;
}


//------------------------ ImmCmdOmAdminOwnerInit ----------------------------------------------------
CM::ImmCmdOmAdminOwnerInit::ImmCmdOmAdminOwnerInit( TxContext * txContextIn, 
                                                char *immOwnerNameIn, 
                                                SaBoolT releaseOnFinalizeIn)
: ImmCmd(txContextIn,"saImmOmAdminOwnerInitialize"),
mImmOwnerNameIn( immOwnerNameIn ),
mReleaseOnFinalizeIn( releaseOnFinalizeIn )
{
}

SaAisErrorT
ImmCmdOmAdminOwnerInit::doExecute()
{
	return SA_AIS_OK;
}


//------------------------ ImmCmdOmAdminOwnerSet ----------------------------------------------------
CM::ImmCmdOmAdminOwnerSet::ImmCmdOmAdminOwnerSet(TxContext * txContextIn,
                          std::vector <std::string> *objectDns,
                          SaImmScopeT scope)
: ImmCmd(txContextIn, "saImmOmAdminOwnerSet"),
mObjectDns( objectDns ), mScope( scope )
{
}

SaAisErrorT 
CM::ImmCmdOmAdminOwnerSet::doExecute()
{
	return SA_AIS_OK;
}

//------------------------ ImmCmdOmAdminOwnerClear ----------------------------------------------------
CM::ImmCmdOmAdminOwnerClear::ImmCmdOmAdminOwnerClear(TxContext * txContextIn,
                          std::string dnIn,
                          SaImmScopeT scope)
: ImmCmd(txContextIn, "saImmOmAdminOwnerClear"),
mDnIn( dnIn ), mScope( scope )
{
}

SaAisErrorT 
CM::ImmCmdOmAdminOwnerClear::doExecute()
{
	return SA_AIS_OK;
}
 
 
//------------------------ ImmCmdOmAdminOwnerRelease ----------------------------------------------------
ImmCmdOmAdminOwnerRelease::ImmCmdOmAdminOwnerRelease(TxContext * txContextIn,
                          std::vector <std::string> *objectDns,
                          SaImmScopeT scope)
: ImmCmd(txContextIn, "saImmOmAdminOwnerRelease"),
mObjectDns( objectDns ), mScope( scope )
{
}

SaAisErrorT 
ImmCmdOmAdminOwnerRelease::doExecute()
{
     return SA_AIS_OK;
}
 
//------------------------ ImmCmdOmClassDescriptionGet ----------------------------------------------------
CM::ImmCmdOmClassDescriptionGet::ImmCmdOmClassDescriptionGet(TxContext * txContextIn/*in*/, 
                                SaImmClassNameT className/*in*/,
                                SaImmClassCategoryT *classCategory/*out*/, 
                                SaImmAttrDefinitionT_2 *** attrDef/*out*/)
: ImmCmd(txContextIn,"saImmOmClassDescription_2"), mAttrDef( attrDef ),
mClassCategory( classCategory ), mClassName( className )
{
}

SaAisErrorT 
CM::ImmCmdOmClassDescriptionGet::doExecute()
{
	return SA_AIS_OK;
}

//------------------------ ImmCmdOmKeySearchInit ----------------------------------------------------
CM::ImmCmdOmKeySearchInit::ImmCmdOmKeySearchInit(TxContext *txContextIn,
                                             std::string dnIn, 
                                             std::string classNameIn, 
                                             BridgeImmIterator* biter)
: ImmCmd(txContextIn, "saImmOmSearchInitialize_2"),
mDnIn( dnIn ), mClassNameIn( classNameIn )
{
	printf("-----> ImmCmdOmKeySearchInit: dn=%s classname=%s\n",dnIn.c_str(),classNameIn.c_str());
}

SaAisErrorT
CM::ImmCmdOmKeySearchInit::doExecute()
{
	return SA_AIS_OK;
}


// result string for CM::ImmCmdOmSearchNext::ImmCmdOmSearchNext
std::string GLOBAL_immCmdOmSearchNextDnOut;

//------------------------ ImmCmdOmKeySearchNext ----------------------------------------------------
CM::ImmCmdOmSearchNext::ImmCmdOmSearchNext(TxContext *txContextIn,
                                       std::string dnIn,
                                       BridgeImmIterator* biter, 
                                       std::string *dnOut/*out*/, 
                                       SaImmAttrValuesT_2*** attrValsOut/*out*/)
: ImmCmd(txContextIn, "saImmOmSearchNext_2"),
mDnIn( dnIn ), mDnOut( dnOut ), mAttrValsOut( attrValsOut )
{        
	printf("-----> ImmCmdOmSearchNext: dn=%s dnOut=%s\n",dnIn.c_str(),GLOBAL_immCmdOmSearchNextDnOut.c_str());
	// returnt the response
	// note that the ImmBridge does not seem to care about attrvalsOut at all, only the dnOut.
	(*dnOut) = GLOBAL_immCmdOmSearchNextDnOut;
	
}

SaAisErrorT
CM::ImmCmdOmSearchNext::doExecute()
{
	return SA_AIS_OK;
}

//------------------------ ImmCmAccessorGet ----------------------------------------------------


CM::ImmCmdOmAccessorGet::ImmCmdOmAccessorGet(TxContext *txContextIn,
                                         std::string  dnIn,
                                         std::string attrNameIn, 
                                         SaImmAttrValuesT_2*** attrValsOut /*out*/)
: ImmCmd(txContextIn,"saImmOmAccessorGet_2"),
mDnIn( dnIn ), mAttrNameIn( attrNameIn ), mAttrValsOut( attrValsOut )
{
	ImmItem item = immStorageG.readFromImmStorage(dnIn.c_str(), attrNameIn.c_str());
	SaImmAttrValuesT_2* res = new SaImmAttrValuesT_2;         // allocate value space
	SaImmAttrValuesT_2** resPtr = new SaImmAttrValuesT_2*[2]; // allocate pointer array
	resPtr[0] = res;  // add our attribute to the array
	resPtr[1] = NULL; // null terminate array of attributes (no counter!)
	
	res->attrName = new char[attrNameIn.size()];
	memcpy(res->attrName,attrNameIn.c_str(),attrNameIn.size());
	
	int nrofValues = item.data.size();
	res->attrValueType    = (SaImmValueTypeT)item.type;
	res->attrValuesNumber = nrofValues;
	if(nrofValues == 0){
		// exit if there are no values!
		res->attrValues = NULL;
		(*attrValsOut) = resPtr;
		return;
	}
	res->attrValues = new void*[nrofValues]; // allocate array of void*
	for(int i=0;i<nrofValues;i++){	
		
		switch(res->attrValueType){
			case SA_IMM_ATTR_SANAMET:
			{
				
				// make a SaNameT
				int size = item.data[i].size();
				if(size > SA_MAX_NAME_LENGTH){
					size = SA_MAX_NAME_LENGTH;
				}
				SaNameT* buf = new SaNameT;
				//char* buf = new char[size+1];
				//SaNameT** bufPtr = new SaNameT*; 
				//*bufPtr = buf;
				buf->length = size;
				memcpy(buf->value,item.data[i].c_str(),size);
				res->attrValues[i] = (void*) buf;
				break;
			}
			case SA_IMM_ATTR_SASTRINGT:
			{
				// make a char**
				int size = item.data[i].size();
				char* buf = new char[size+1];
				char** bufPtr = new char*; 
				*bufPtr = buf;
				strcpy(buf,item.data[i].c_str());
				res->attrValues[i] = (void*) bufPtr;
				break;
			}
			default:
			{
				printf("ERROR in CM::ImmCmdOmAccessorGet::ImmCmdOmAccessorGet, unsupported TYPE %d\n",res->attrValueType);
			}			
		}
	}	
	(*attrValsOut) = resPtr;
	immMemoryTrackerG.reg(resPtr);
}

SaAisErrorT
CM::ImmCmdOmAccessorGet::doExecute()
{
	return SA_AIS_OK;
}

//------------------------ ImmCmdOmCcbInitialize ----------------------------------------------------
CM::ImmCmdOmCcbInit::ImmCmdOmCcbInit(TxContext *txContextIn)
: ImmCmd(txContextIn, "saImmOmCcbInitialize")
{
}

SaAisErrorT
CM::ImmCmdOmCcbInit::doExecute()
{
	return SA_AIS_OK;
}


//------------------------ ImmCmdOmCcbFinalize ----------------------------------------------------
CM::ImmCmdOmCcbFinalize::ImmCmdOmCcbFinalize(TxContext *txContextIn)
: ImmCmd(txContextIn, "saImmOmCcbFinalize")
{
}

SaAisErrorT
CM::ImmCmdOmCcbFinalize::doExecute()
{
	return SA_AIS_OK;
}

//------------------------ ImmCmdOmCcbObjectModify ----------------------------------------------------
CM::ImmCmdOmCcbObjectModify::ImmCmdOmCcbObjectModify(TxContext *txContextIn,
                                                 SaNameT* dnIn, 
                                                 SaImmAttrModificationT_2 **attrModsIn)
: ImmCmd(txContextIn, "saImmOmCcbObjectModify_2"),
mDnIn( dnIn ), mAttrModsIn( attrModsIn )
{	
//	char* dn = new char[dnIn->length+1];
//	memcpy(dn,dnIn->value,dnIn->length);
//	dn[dnIn->length]=0; // make a c-string!!
	
	char* dn = makeCString(dnIn);
		
	SaImmAttrModificationT_2** modArray = attrModsIn;
	
	int i = 0;
	while(modArray[i] != NULL){
		SaImmAttrModificationT_2* mod = modArray[i];		
		switch(mod->modType){
			
			case SA_IMM_ATTR_VALUES_ADD:
			case SA_IMM_ATTR_VALUES_REPLACE:
			{
				std::vector<std::string> values;
			    for(int a=0;a<mod->modAttr.attrValuesNumber;a++){
			    	// assume string type!!
			    	switch(mod->modAttr.attrValueType){
			    		case SA_IMM_ATTR_SASTRINGT:
			    		{
					    	std::string strval(*((char**)mod->modAttr.attrValues[a]));
					    	values.push_back(strval);
							printf("ModifyImm: dn=%s modtype=%d attr=%s attrtype=%d attval=%s\n", dn, mod->modType, mod->modAttr.attrName, mod->modAttr.attrValueType, strval.c_str());			    	
			    			break;
			    		}
			    		case SA_IMM_ATTR_SANAMET:
			    		{
					    	std::string strval(((char*)mod->modAttr.attrValues[a]));
					    	values.push_back(strval);
							printf("ModifyImm: dn=%s modtype=%d attr=%s attrtype=%d attval=%s\n", dn, mod->modType, mod->modAttr.attrName, mod->modAttr.attrValueType, strval.c_str());			    	
			    			break;
			    		}
			    		default:
			    		{
			    			printf("ERROR: Unsupported datatype in CM::ImmCmdOmCcbObjectModify::ImmCmdOmCcbObjectModify, currently IMM stub backend only support SA_STRING and SA_NAME\n");
			    		}
			    		
			    	}
				}
				immStorageG.addToImmStorage(dn, mod->modAttr.attrName, mod->modAttr.attrValueType, values);
				break;
			}		
			case SA_IMM_ATTR_VALUES_DELETE:
			{
			    for(int a=0;a<mod->modAttr.attrValuesNumber;a++){
			    	immStorageG.deleteFromImmStorage(dn, mod->modAttr.attrName);
				}
				
				break;
			}	
					
		}// switch
		
		i=i+1;
	}// while
	delete[] dn;			// remove tmp
	
	
}

SaAisErrorT 
CM::ImmCmdOmCcbObjectModify::doExecute()
{
	return SA_AIS_OK;
}

//------------------------ ImmCmdOmCcbApply ----------------------------------------------------
CM::ImmCmdOmCcbApply::ImmCmdOmCcbApply(TxContext *txContextIn)
: ImmCmd(txContextIn, "saImmOmCcbApply")
{
}

SaAisErrorT
ImmCmdOmCcbApply::doExecute()
{
	return SA_AIS_OK;
}

/**
 * Helper to find the key attribute matching the classname!
 */
std::string findInstanceKey(char* className, SaImmAttrValuesT_2** attrValsIn ){
	
	std::string keyName(className);
	keyName[0] = tolower(keyName[0]);
	keyName.append("Id");
	
	int i = 0;
	while(attrValsIn[i] != NULL ) {
		if ( 0 == strcmp(attrValsIn[i]->attrName,keyName.c_str()) && attrValsIn[i]->attrValueType == 9){
			// found key now make instance key!
			std::string instance;
			char* attr = *((char**)attrValsIn[i]->attrValues[0]);
			instance.append(attr);
			return instance;
		}
		i=i+1;
	}
	return "";
}

//------------------------ ImmCmdOmCcbCreate ----------------------------------------------------
CM::ImmCmdOmCcbObjectCreate::ImmCmdOmCcbObjectCreate(TxContext* txContextIn,
                                                 SaNameT *parentIn,
                                                 SaImmClassNameT classNameIn, 
                                                 SaImmAttrValuesT_2** attrValsIn)
: ImmCmd(txContextIn, "saImmOmCcbObjectCreate_2"),
mParentIn( parentIn ), mClassNameIn( classNameIn ), mAttrValsIn( attrValsIn )
{
	char* parentDn = makeCString(parentIn);
	printf("ImmCmdOmCcbObjectCreate parent=%s class=%s\n",parentDn,classNameIn);
	
	// build complete path
	std::string instance = findInstanceKey((char*)classNameIn, attrValsIn);
	std::string dn(instance);
	dn.append(",");
	dn.append(parentDn);

	SaNameT* path = makeSaNameT(dn.c_str());
		
	SaImmAttrModificationT_2 mod;
	mod.modType = SA_IMM_ATTR_VALUES_REPLACE;
	mod.modAttr.attrValuesNumber = 1;
	
	SaImmAttrModificationT_2** modArray = new SaImmAttrModificationT_2*[2];	
	modArray[0] = &mod;
	modArray[1] = NULL;	
	int i = 0;
	while(attrValsIn[i] != NULL ) {
		mod.modAttr.attrValueType = attrValsIn[i]->attrValueType;
		mod.modAttr.attrName = attrValsIn[i]->attrName;
		mod.modAttr.attrValuesNumber = attrValsIn[i]->attrValuesNumber;
		mod.modAttr.attrValues = attrValsIn[i]->attrValues;		
		CM::ImmCmdOmCcbObjectModify::ImmCmdOmCcbObjectModify modCmd(txContextIn, path, modArray);
		i=i+1;
	}
	
	modArray[0] = NULL;
	delete[] modArray;
	delete path;
	delete[] parentDn;
	
}

SaAisErrorT
CM::ImmCmdOmCcbObjectCreate::doExecute()
{
	return SA_AIS_OK;
}

//------------------------ ImmCmdOmCcbDelete ----------------------------------------------------
CM::ImmCmdOmCcbObjectDelete::ImmCmdOmCcbObjectDelete(TxContext* txContextIn,
                                                 SaNameT* dnIn)
: ImmCmd(txContextIn, "saImmOmCcbObjectDelete"),
mDnIn( dnIn )
{
}

SaAisErrorT 
CM::ImmCmdOmCcbObjectDelete::doExecute()
{
	return SA_AIS_OK;
}



///////////////////////////////////
// Helpers
///////////////////////////////////
const char* STARS="******************************";
const char* runningTest;
void testStarted(const char* testName){
	runningTest=testName;
	printf(STARS);
	printf(" Starting: %s\n",runningTest);
}

void testPassed(){
	printf(STARS);
	printf(" Passed  : %s\n",runningTest);
	printf("\n");
}

void testAllPassed(){
	printf("\n All tests passed!\n");
}



///////////////////////////////////
// Cleanup methods
///////////////////////////////////
// forward declarations
void cleanUp(ComMoAttributeValueStructMemberT *m);
void cleanUp(ComMoAttributeValueContainerT *c);

//


void cleanUp(ComMoAttributeValueContainerT** c){
	int i=0;
	while(c[i] != NULL){
		cleanUp(c[i]);
		i = i+1;
	}
	delete c;
}

void cleanUp(ComMoAttributeValueContainerT *c){
	switch(c->type){
		case ComOamSpiMoAttributeType_STRING:
			for(int i=0;i<c->nrOfValues;i++){
				delete[] c->values[i].value.theString;
			}
		break;
		
		case ComOamSpiMoAttributeType_STRUCT:
			for(int i=0;i<c->nrOfValues;i++){
				
				cleanUp(c->values[i].value.structMember);
			}
		break;
		
		case ComOamSpiMoAttributeType_REFERENCE:
			for(int i=0;i<c->nrOfValues;i++){
				delete[] c->values[i].value.moRef;
			}
		break;
		
		default:
		break;
	}
	delete[] c->values;
	delete c;			
}

void cleanUp(ComMoAttributeValueStructMemberT *m){

	ComMoAttributeValueStructMemberT* member = m;
	while(member != NULL){
		delete[] member->memberName;
		cleanUp(member->memberValue);
		ComMoAttributeValueStructMemberT* next = member->next;
		delete member;
		member = next;
	}
}

/**
 * Allocate c-string on heap
 */
char* allocCstr(const char* str){
	unsigned int len = strlen(str);
	char* tmp = new char[len+1]; // the '\0' terminator
	strcpy(tmp,str);
	return tmp;
}

///////////////////////////////////
//  MAIN
///////////////////////////////////

int main(int argc, char* argv[])
{
	printf("running all tests\n");
	
	{
		testStarted("IMM Storage");
		
		std::vector<std::string> values;
		values.push_back(std::string("attrValue1"));
		values.push_back(std::string("attrValue2"));
		immStorageG.addToImmStorage("dn=1,path=2","attrName",9,values);
		
		ImmItem test = immStorageG.readFromImmStorage("dn=1,path=2","attrName");
		assert(test.type==9);
		assert(test.data[0]=="attrValue1");
		assert(test.data[1]=="attrValue2");
		
		testPassed();
		
	}


	{
		testStarted("getImmMoAttribute()");

		// setup ModelRepository
		struct ComOamSpiMoAttribute* attrs = makeAttribute("pets",ComOamSpiMoAttributeType_STRING,NULL);
		struct ComOamSpiMoc* meMoc = makeMoc("Me", NULL);
		struct ComOamSpiMoc* homeMoc = makeMoc("Home",attrs);
		struct ComOamSpiContainment* cont = makeContainment(meMoc, homeMoc);
		struct ComOamSpiMom* mom = makeMom("Me",meMoc);
		setMom(mom);

		
		// setup IMM storage
		immStorageG.reset();		
		std::vector<std::string> values;
		values.push_back(std::string("tiger"));
		values.push_back(std::string("lion"));
		immStorageG.addToImmStorage("homeId=2,meId=1","pets",9,values);
		
		// setup the call
		ComOamSpiTransactionHandleT txh=1;
		TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
		OamSAImmBridge testObj;		
		ComMoAttributeValueContainerT *result = NULL;
		ComReturnT ret = testObj.getImmMoAttribute(txh,"Me=1,Home=2","pets",&result);
		
		// verify the result
		assert(ret==ComOk);
		assert(result != NULL);
		assert(result->type==9);
		assert(result->nrOfValues==2);
		assert(std::string(result->values[0].value.theString) == std::string("tiger"));
		assert(std::string(result->values[1].value.theString) == std::string("lion"));		
		
		delete attrs;
		delete meMoc;
		delete homeMoc;
		delete cont;
		delete mom;
		delete txContextIn;
		//cleanUp(result);
		testPassed();
	}
	
	
/*	
	{
		testStarted("setImmMoAttribute()");
				
		// setup IMM storage
		immStorageG.reset();		
		std::vector<std::string> values;
		values.push_back(std::string("tiger"));
		values.push_back(std::string("lion"));
		immStorageG.addToImmStorage("homeId=2,meId=1","pets",9,values);
		
		
		// add the class name attribute
		{	
			std::vector<std::string> className;
			className.push_back("Home");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("homeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("Home"), std::string("pets"), IMM_STRING_TYPE);
		}
		// add the class name attribute
		{	
			std::vector<std::string> className;
			className.push_back("Me");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("homeId=2","SaImmAttrClassName",IMM_STRING_TYPE,className);
		}
				
		// perform the test
		ComOamSpiTransactionHandleT txh=1;
		TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
		OamSAImmBridge testObj;	


		// 1. Create new Mo of class Home
		ComReturnT retCre = testObj.createImmMo(txh,"Me=1","Home","dn","Home=1");
		assert(retCre==ComOk);
		
		// 2. Add string attribute	
		ComMoAttributeValueContainerT *value = new ComMoAttributeValueContainerT;
		value->type = ComOamSpiMoAttributeType_STRING;
		value->nrOfValues = 1;
		value->values = new ComMoAttributeValueT[1];
		value->values[0].value.theString = allocCstr("rabbit");								
		ComReturnT retSet = testObj.setImmMoAttribute(txh,"Me=1,Home=2","pets",value);
		ComReturnT retPrep = testObj.OamSAPrepare(txh);
		
		// 3. verify the result is ok
		assert(retSet==ComOk);
		assert(retPrep==ComOk);
		ImmItem item = immStorageG.readFromImmStorage("homeId=2,meId=1","pets");
		printf("item=%s\n",item.toString().c_str());
		assert(item.type==9);
		assert(item.data.size()==1);
		assert(item.data[0]==std::string("rabbit"));
				
		// cleanup
		cleanUp(value);
		delete txContextIn;		
		
		testPassed();
	}

*/	
	
	{
		
		testStarted("Read Struct from Imm");
		
		// Setup ModelRepository with Me base class and Sub class Employee containing a struct type PersonData

		//   Me<<EcimClass>,
		//     Employee<<EcimClass>>
		//           title:string
		//           person:PersonData
		//
		//  PersonData<<EcimStruct>>{
		//                firstname:string;
		//                lastname:string;     
		//          }  
		
		struct ComOamSpiStructMember* mLastname =  makeStructMember("lastname", ComOamSpiDatatype_STRING,NULL);
		struct ComOamSpiStructMember* mFirstname =  makeStructMember("firstname", ComOamSpiDatatype_STRING, mLastname);
		struct ComOamSpiStruct* personData = makeStruct("PersonData", mFirstname);
		struct ComOamSpiMoAttribute* attrPerson = makeAttribute("person",personData, NULL);
		struct ComOamSpiMoAttribute* employeeAttrs = makeAttribute("title",ComOamSpiMoAttributeType_STRING,attrPerson);
		struct ComOamSpiMoc* meMoc = makeMoc("Me", NULL);
		struct ComOamSpiMoc* employeeMoc = makeMoc("Employee",employeeAttrs);
		struct ComOamSpiContainment* cont =makeContainment(meMoc, employeeMoc);
		struct ComOamSpiMom* mom = makeMom("Me",meMoc);
		setMom(mom);


		// setup IMM storage
		immStorageG.reset();		
		{
			// add Employee instance 1 attribute: title
			std::vector<std::string> values;
			values.push_back(std::string("President"));
			immStorageG.addToImmStorage("employeeId=1,meId=1","title",9,values);
		}
		{
			// add Employee instance 1 attribute: person (a reference to the struct instance!)
			std::vector<std::string> values;
			values.push_back(std::string("Me=1,Employee=1,PersonData.id=person_1"));
			unsigned int IMM_SA_NAME=6;
			immStorageG.addToImmStorage("employeeId=1,meId=1","person",IMM_SA_NAME,values);
		}
		{
			// add personData instance person_1 attribute: firstname
			std::vector<std::string> values;
			values.push_back(std::string("Bob"));
			immStorageG.addToImmStorage("id=person_1,employeeId=1,meId=1","firstname",9,values);
		}
		{
			// add personData instance person_1 attribute: lastname
			std::vector<std::string> values;
			values.push_back(std::string("Dole"));
			immStorageG.addToImmStorage("id=person_1,employeeId=1,meId=1","lastname",9,values);
		}
		
		
		{	
			// add the class name attribute for Employee with two attributes "title" and "person"
			std::vector<std::string> className;
			className.push_back("Employee");
			unsigned int IMM_STRING_TYPE=9;
			unsigned int IMM_REF_TYPE = 6;
			immStorageG.addToImmStorage("employeeId=1,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("title"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("person"), IMM_REF_TYPE);
		}
		{	
			// add the class name attribute for PersonData with two attributes "firstname" and "lastname"
			std::vector<std::string> className;
			className.push_back("PersonData");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("id=person_1,employeeId=1,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("firstname"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("lastname"), IMM_STRING_TYPE);
		}
		// add the class name attribute for Me
		{	
			std::vector<std::string> className;
			className.push_back("Me");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
		}
				

		
		// read the Ecim struct value from "Me=1,Employee=1,person"
		
		ComOamSpiTransactionHandleT txh=1;
		TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
		OamSAImmBridge testObj;		
		ComMoAttributeValueContainerT *result = NULL;
		ComReturnT ret = testObj.getImmMoAttribute(txh,"Me=1,Employee=1","person",&result);
		
		// verify the result
		assert(ret==ComOk);
		assert(result != NULL);
		assert(result->type==14); // struct
		assert(result->nrOfValues==1);
		
		ComMoAttributeValueStructMember* member;
		// First struct member		
		member = result->values[0].value.structMember;
		assert(std::string(member->memberName) == std::string("firstname"));
		assert(member->memberValue->type == 9); // string
		assert(member->memberValue->nrOfValues == 1);
		assert(std::string(member->memberValue->values[0].value.theString) == std::string("Bob"));
		assert(member->next!=NULL);
		
		// Second struct member
		member = member->next;
		assert(std::string(member->memberName) == std::string("lastname"));
		assert(member->memberValue->type == 9); // string
		assert(member->memberValue->nrOfValues == 1);
		assert(std::string(member->memberValue->values[0].value.theString) == std::string("Dole"));
		assert(member->next==NULL);	// no more members
		
		delete mLastname;
		delete mFirstname;
		delete personData;
		delete attrPerson;
		delete employeeAttrs;
		delete meMoc;
		delete employeeMoc;
		delete cont;
		delete mom;
		
		delete txContextIn;
		//cleanUp(result);
		
		testPassed();
	}
	
	{		
		testStarted("Write Struct to Imm");

		// Setup ModelRepository with Me base class and Sub class Employee containing a struct type PersonData

		//   Me<<EcimClass>,
		//     Employee<<EcimClass>>
		//           title:string
		//           person:PersonData
		//
		//  PersonData<<EcimStruct>>{
		//                firstname:string;
		//                lastname:string;     
		//          }  
		struct ComOamSpiStructMember* mLastname =  makeStructMember("lastname", ComOamSpiDatatype_STRING,NULL);
		struct ComOamSpiStructMember* mFirstname =  makeStructMember("firstname", ComOamSpiDatatype_STRING, mLastname);
		struct ComOamSpiStruct* personData = makeStruct("PersonData", mFirstname);
		struct ComOamSpiMoAttribute* attrPerson = makeAttribute("person",personData, NULL);
		struct ComOamSpiMoAttribute* employeeAttrs = makeAttribute("title",ComOamSpiMoAttributeType_STRING,attrPerson);
		struct ComOamSpiMoc* meMoc = makeMoc("Me", NULL);
		struct ComOamSpiMoc* employeeMoc = makeMoc("Employee",employeeAttrs);
		struct ComOamSpiContainment* cont =makeContainment(meMoc, employeeMoc);
		struct ComOamSpiMom* mom = makeMom("Me",meMoc);
		setMom(mom);


		// setup IMM storage
		immStorageG.reset();		
		
		{	
			// add the class name attribute for Employee with two attributes "title" and "person"
			std::vector<std::string> className;
			className.push_back("Employee");
			unsigned int IMM_STRING_TYPE=9;
			unsigned int IMM_REF_TYPE = 6;
			immStorageG.addToImmStorage("employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("title"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("person"), IMM_REF_TYPE);
		}
		{	
			// add the class name attribute for PersonData with two attributes "firstname" and "lastname"
			std::vector<std::string> className;
			className.push_back("PersonData");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("id=person_0,employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("firstname"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("lastname"), IMM_STRING_TYPE);
		}
		// add the class name attribute for Me
		{	
			std::vector<std::string> className;
			className.push_back("Me");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
		}
				
		// create an new employee Richard Nixon, Vice President! :-)		
		
		ComOamSpiTransactionHandleT txh=1;
		TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
		OamSAImmBridge testObj;		
		ComMoAttributeValueContainerT *result = NULL;

		//1. Create the Employee class instance 2	
		ComReturnT retCre = testObj.createImmMo(txh,"Me=1","Employee","employeeId","2");		
		assert(retCre==ComOk);
		
		// 2. Add string attribute title
		ComMoAttributeValueContainerT *value = new ComMoAttributeValueContainerT;
		value->type = ComOamSpiMoAttributeType_STRING;
		value->nrOfValues = 1;
		value->values = new ComMoAttributeValueT[1];
		value->values[0].value.theString = allocCstr("Vice President");				
		ComReturnT retSet = testObj.setImmMoAttribute(txh,"Me=1,Employee=2","title",value);
		assert(retSet==ComOk);
		cleanUp(value);
		
		// 3. Add struct attribute person

		// lastname (LN)
		ComMoAttributeValueContainerT *valueLN = new ComMoAttributeValueContainerT;
		valueLN->type = ComOamSpiMoAttributeType_STRING;
		valueLN->nrOfValues = 1;
		valueLN->values = new ComMoAttributeValueT[1];
		valueLN->values[0].value.theString = allocCstr("Nixon");								
		ComMoAttributeValueStructMemberT *memberLN = new ComMoAttributeValueStructMemberT;
		memberLN->memberName = allocCstr("lastname");
		memberLN->memberValue = valueLN;
		memberLN->next=NULL; // last member


		// firstname (FN)
		ComMoAttributeValueContainerT *valueFN = new ComMoAttributeValueContainerT;
		valueFN->type = ComOamSpiMoAttributeType_STRING;
		valueFN->nrOfValues = 1;
		valueFN->values = new ComMoAttributeValueT[1];
		valueFN->values[0].value.theString = allocCstr("Richard");								
		ComMoAttributeValueStructMemberT *memberFN = new ComMoAttributeValueStructMemberT;
		memberFN->memberName = allocCstr("firstname");
		memberFN->memberValue = valueFN;
		memberFN->next=memberLN; // link to next member
		
		// Set struct attribute by linking in the members
		ComMoAttributeValueContainerT *valueStruct = new ComMoAttributeValueContainerT;
		valueStruct->type = ComOamSpiMoAttributeType_STRUCT;
		valueStruct->nrOfValues = 1;
		valueStruct->values = new ComMoAttributeValueT[1];
		valueStruct->values[0].value.structMember = memberFN;				

		// write the struct attribute person
		ComReturnT retSetStruct = testObj.setImmMoAttribute(txh,"Me=1,Employee=2","person",valueStruct);
		assert(retSetStruct==ComOk);
		cleanUp(valueStruct);
					

		// Flush changes towards IMM
		ComReturnT retPrep = testObj.OamSAPrepare(txh);
		assert(retPrep==ComOk);
		
		
		
		// verify the result by looking in the IM backend to see if we find the expected values
		// we want a new class instance personDataId=person_1 below employeeId=2
		// the class instance should have two attributes, firstname and lastname
		{
			// check attribute "title" in Employee
			ImmItem item = immStorageG.readFromImmStorage("employeeId=2,meId=1","title");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Vice President"));
		}

		{
			// check attribute "person" reference in Employee points to the PersonData instance person_0
			ImmItem item = immStorageG.readFromImmStorage("employeeId=2,meId=1","person");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==6); // SA_NAME
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Me=1,Employee=2,PersonData.id=person_0"));
		}

		{
			// check attribute "person.firstname" in Employee
			ImmItem item = immStorageG.readFromImmStorage("id=person_0,employeeId=2,meId=1","firstname");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Richard"));
		}

		{
			// check attribute "person.lastname" in Employee
			ImmItem item = immStorageG.readFromImmStorage("id=person_0,employeeId=2,meId=1","lastname");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Nixon"));
		}

		
		delete mLastname;
		delete mFirstname;
		delete personData;
		delete attrPerson;
		delete employeeAttrs;
		delete meMoc;
		delete employeeMoc;
		delete cont;
		delete mom;
		
		delete txContextIn;
		
		testPassed();
		
	}

	{
		testStarted("Read Struct array[2] from Imm");
		
		// Setup ModelRepository with Me base class and Sub class Employee containing a struct type PersonData

		//   Me<<EcimClass>,
		//     Employee<<EcimClass>>
		//           title:string
		//           person[2]:PersonData
		//
		//  PersonData<<EcimStruct>>{
		//                firstname:string;
		//                lastname:string;     
		//          }  

		struct ComOamSpiStructMember* mLastname =  makeStructMember("lastname", ComOamSpiDatatype_STRING,NULL);
		struct ComOamSpiStructMember* mFirstname =  makeStructMember("firstname", ComOamSpiDatatype_STRING, mLastname);
		struct ComOamSpiStruct* personData = makeStruct("PersonData", mFirstname);
		struct ComOamSpiMoAttribute* attrPerson = makeAttribute("person",personData, NULL);
		struct ComOamSpiMoAttribute* employeeAttrs = makeAttribute("title",ComOamSpiMoAttributeType_STRING,attrPerson);
		struct ComOamSpiMoc* meMoc = makeMoc("Me", NULL);
		struct ComOamSpiMoc* employeeMoc = makeMoc("Employee",employeeAttrs);
		struct ComOamSpiContainment* cont =makeContainment(meMoc, employeeMoc);
		struct ComOamSpiMom* mom = makeMom("Me",meMoc);
		setMom(mom);


		// setup IMM storage
		immStorageG.reset();		
		{
			// add Employee instance 1 attribute: title
			std::vector<std::string> values;
			values.push_back(std::string("President"));
			immStorageG.addToImmStorage("employeeId=1,meId=1","title",9,values);
		}

		// person[0]		
		{
			// add personData instance person_0 attribute: firstname
			std::vector<std::string> values;
			values.push_back(std::string("Bob"));
			immStorageG.addToImmStorage("id=person_0,employeeId=1,meId=1","firstname",9,values);
		}
		{
			// add personData instance person_0 attribute: lastname
			std::vector<std::string> values;
			values.push_back(std::string("Dole"));
			immStorageG.addToImmStorage("id=person_0,employeeId=1,meId=1","lastname",9,values);
		}

		// person[1]
		{
			// add personData instance person_1 attribute: firstname
			std::vector<std::string> values;
			values.push_back(std::string("Jimmy"));
			immStorageG.addToImmStorage("id=person_1,employeeId=1,meId=1","firstname",9,values);
		}
		{
			// add personData instance person_1 attribute: lastname
			std::vector<std::string> values;
			values.push_back(std::string("Carter"));
			immStorageG.addToImmStorage("id=person_1,employeeId=1,meId=1","lastname",9,values);
		}
		// add the person reference array to employee
		{
			// add Employee instance 1 attribute: person (a reference to the struct instance!)
			std::vector<std::string> values;
			values.push_back(std::string("Me=1,Employee=1,PersonData.id=person_0"));
			values.push_back(std::string("Me=1,Employee=1,PersonData.id=person_1"));
			unsigned int IMM_SA_NAME=6;
			immStorageG.addToImmStorage("employeeId=1,meId=1","person",IMM_SA_NAME,values);
		}
		
		
		
		{	
			// add the class name attribute for Employee with two attributes "title" and "person"
			std::vector<std::string> className;
			className.push_back("Employee");
			unsigned int IMM_STRING_TYPE=9;
			unsigned int IMM_REF_TYPE = 6;
			immStorageG.addToImmStorage("employeeId=1,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("title"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("person"), IMM_REF_TYPE);
		}
		{	
			// add the class name attribute for PersonData with two attributes "firstname" and "lastname"
			std::vector<std::string> className;
			className.push_back("PersonData");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("id=person_0,employeeId=1,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			immStorageG.addToImmStorage("id=person_1,employeeId=1,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("firstname"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("lastname"), IMM_STRING_TYPE);
		}
		// add the class name attribute for Me
		{	
			std::vector<std::string> className;
			className.push_back("Me");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
		}
				

		
		// read the Ecim struct value from "Me=1,Employee=1,person"
		
		ComOamSpiTransactionHandleT txh=1;
		TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
		OamSAImmBridge testObj;		
		ComMoAttributeValueContainerT *result = NULL;
		ComReturnT ret = testObj.getImmMoAttribute(txh,"Me=1,Employee=1","person",&result);
		
		// verify the result
		assert(ret==ComOk);
		assert(result != NULL);
		assert(result->type==14); // struct
		assert(result->nrOfValues==2);
		
		ComMoAttributeValueStructMember* member;
		// person[0] First struct member		
		member = result->values[0].value.structMember;
		assert(std::string(member->memberName) == std::string("firstname"));
		assert(member->memberValue->type == 9); // string
		assert(member->memberValue->nrOfValues == 1);
		assert(std::string(member->memberValue->values[0].value.theString) == std::string("Bob"));
		assert(member->next!=NULL);
		
		// person[0] Second struct member
		member = member->next;
		assert(std::string(member->memberName) == std::string("lastname"));
		assert(member->memberValue->type == 9); //string
		assert(member->memberValue->nrOfValues == 1);
		assert(std::string(member->memberValue->values[0].value.theString) == std::string("Dole"));
		assert(member->next==NULL);	// no more members


		// person[1] First struct member		
		member = result->values[1].value.structMember;
		assert(std::string(member->memberName) == std::string("firstname"));
		assert(member->memberValue->type == 9); //string
		assert(member->memberValue->nrOfValues == 1);
		assert(std::string(member->memberValue->values[0].value.theString) == std::string("Jimmy"));
		assert(member->next!=NULL);
		
		// person[1] Second struct member
		member = member->next;
		assert(std::string(member->memberName) == std::string("lastname"));
		assert(member->memberValue->type == 9); // string
		assert(member->memberValue->nrOfValues == 1);
		assert(std::string(member->memberValue->values[0].value.theString) == std::string("Carter"));
		assert(member->next==NULL);	// no more members
		
		//cleanUp(result);
		delete txContextIn;
		
		delete mLastname;
		delete mFirstname;
		delete personData;
		delete attrPerson;
		delete employeeAttrs;
		delete meMoc;
		delete employeeMoc;
		delete cont;
		delete mom;
		
		testPassed();
	}
		

	{		
		testStarted("Write struct array[2] to Imm");

		// Setup ModelRepository with Me base class and Sub class Employee containing a struct type PersonData

		//   Me<<EcimClass>,
		//     Employee<<EcimClass>>
		//           title:string
		//           person[2]:PersonData
		//
		//  PersonData<<EcimStruct>>{
		//                firstname:string;
		//                lastname:string;     
		//          }  

		struct ComOamSpiStructMember* mLastname =  makeStructMember("lastname", ComOamSpiDatatype_STRING,NULL);
		struct ComOamSpiStructMember* mFirstname =  makeStructMember("firstname", ComOamSpiDatatype_STRING, mLastname);
		struct ComOamSpiStruct* personData = makeStruct("PersonData", mFirstname);
		struct ComOamSpiMoAttribute* attrPerson = makeAttribute("person",personData, NULL);
		struct ComOamSpiMoAttribute* employeeAttrs = makeAttribute("title",ComOamSpiMoAttributeType_STRING,attrPerson);
		struct ComOamSpiMoc* meMoc = makeMoc("Me", NULL);
		struct ComOamSpiMoc* employeeMoc = makeMoc("Employee",employeeAttrs);
		struct ComOamSpiContainment* cont =makeContainment(meMoc, employeeMoc);
		struct ComOamSpiMom* mom = makeMom("Me",meMoc);
		setMom(mom);


		// setup IMM storage
		immStorageG.reset();		
		
		{	
			// add the class name attribute for Employee with two attributes "title" and "person"
			std::vector<std::string> className;
			className.push_back("Employee");
			unsigned int IMM_STRING_TYPE=9;
			unsigned int IMM_REF_TYPE = 6;
			immStorageG.addToImmStorage("employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("title"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("person"), IMM_REF_TYPE);
		}
		{	
			// add the class name attribute for PersonData with two attributes "firstname" and "lastname"
			std::vector<std::string> className;
			className.push_back("PersonData");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("id=person_0,employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			immStorageG.addToImmStorage("id=person_1,employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("firstname"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("lastname"), IMM_STRING_TYPE);
		}
		// add the class name attribute for Me
		{	
			std::vector<std::string> className;
			className.push_back("Me");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
		}
				
		// create an new employee Richard Nixon, Vice President! :-)		
		
		ComOamSpiTransactionHandleT txh=1;
		TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
		OamSAImmBridge testObj;		
		ComMoAttributeValueContainerT *result = NULL;

		//1. Create the Employee class instance 2	
		ComReturnT retCre = testObj.createImmMo(txh,"Me=1","Employee","dn","Employee=2");
		assert(retCre==ComOk);
		
		// 2. Add string attribute title
		ComMoAttributeValueContainerT *value = new ComMoAttributeValueContainerT;
		value->type = ComOamSpiMoAttributeType_STRING;
		value->nrOfValues = 1;
		value->values = new ComMoAttributeValueT[1];
		value->values[0].value.theString = allocCstr("Vice President");				
		ComReturnT retSet = testObj.setImmMoAttribute(txh,"Me=1,Employee=2","title",value);
		assert(retSet==ComOk);
		cleanUp(value);
		
		
		{
		// 3. Add struct attribute person[0] Richard Nixon
		
			// Build person[]
			ComMoAttributeValueContainerT *valueStruct = new ComMoAttributeValueContainerT;
			valueStruct->type = ComOamSpiMoAttributeType_STRUCT;
			valueStruct->nrOfValues = 2; // <<< two structs
			valueStruct->values = new ComMoAttributeValueT[2];
		
			{		
				// person[0] lastname (LN)
				ComMoAttributeValueContainerT *valueLN = new ComMoAttributeValueContainerT;
				valueLN->type = ComOamSpiMoAttributeType_STRING;
				valueLN->nrOfValues = 1;
				valueLN->values = new ComMoAttributeValueT[1];
				valueLN->values[0].value.theString = allocCstr("Nixon");								
				ComMoAttributeValueStructMemberT *memberLN = new ComMoAttributeValueStructMemberT;
				memberLN->memberName = allocCstr("lastname");
				memberLN->memberValue = valueLN;
				memberLN->next=NULL; // last member
		
		
				// person[0] firstname (FN)
				ComMoAttributeValueContainerT *valueFN = new ComMoAttributeValueContainerT;
				valueFN->type = ComOamSpiMoAttributeType_STRING;
				valueFN->nrOfValues = 1;
				valueFN->values = new ComMoAttributeValueT[1];
				valueFN->values[0].value.theString = allocCstr("Richard");								
				ComMoAttributeValueStructMemberT *memberFN = new ComMoAttributeValueStructMemberT;
				memberFN->memberName = allocCstr("firstname");
				memberFN->memberValue = valueFN;
				memberFN->next=memberLN; // link to next member
				
				// add person[0]
				valueStruct->values[0].value.structMember = memberFN;							
			}									
			
			{		
				// person[1] lastname (LN)
				ComMoAttributeValueContainerT *valueLN = new ComMoAttributeValueContainerT;
				valueLN->type = ComOamSpiMoAttributeType_STRING;
				valueLN->nrOfValues = 1;
				valueLN->values = new ComMoAttributeValueT[1];
				valueLN->values[0].value.theString = allocCstr("Obama");								
				ComMoAttributeValueStructMemberT *memberLN = new ComMoAttributeValueStructMemberT;
				memberLN->memberName = allocCstr("lastname");
				memberLN->memberValue = valueLN;
				memberLN->next=NULL; // last member
		
		
				// person[1] firstname (FN)
				ComMoAttributeValueContainerT *valueFN = new ComMoAttributeValueContainerT;
				valueFN->type = ComOamSpiMoAttributeType_STRING;
				valueFN->nrOfValues = 1;
				valueFN->values = new ComMoAttributeValueT[1];
				valueFN->values[0].value.theString = allocCstr("Barak");								
				ComMoAttributeValueStructMemberT *memberFN = new ComMoAttributeValueStructMemberT;
				memberFN->memberName = allocCstr("firstname");
				memberFN->memberValue = valueFN;
				memberFN->next=memberLN; // link to next member
				
				// add person[1]
				valueStruct->values[1].value.structMember = memberFN;							
			}									
			
	
			// write the struct attribute person
			ComReturnT retSetStruct = testObj.setImmMoAttribute(txh,"Me=1,Employee=2","person",valueStruct);
			assert(retSetStruct==ComOk);
			cleanUp(valueStruct);
		}			



		// Flush changes towards IMM
		ComReturnT retPrep = testObj.OamSAPrepare(txh);
		assert(retPrep==ComOk);
		
		
		// verify the result by looking in the IM backend to see if we find the expected values
		// we want a new class instance personDataId=person_1 below employeeId=2
		// the class instance should have two attributes, firstname and lastname
		{
			// check attribute "title" in Employee
			ImmItem item = immStorageG.readFromImmStorage("employeeId=2,meId=1","title");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Vice President"));
		}

		{
			// check attribute "person" reference in Employee points to the PersonData instance person_0
			ImmItem item = immStorageG.readFromImmStorage("employeeId=2,meId=1","person");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==6); //SA_NAME
			assert(item.data.size()==2);
			assert(item.data[0]==std::string("Me=1,Employee=2,PersonData.id=person_0"));
			assert(item.data[1]==std::string("Me=1,Employee=2,PersonData.id=person_1"));
		}

		{
			// check attribute "person[0].firstname" in Employee
			ImmItem item = immStorageG.readFromImmStorage("id=person_0,employeeId=2,meId=1","firstname");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Richard"));
		}

		{
			// check attribute "person[0].lastname" in Employee
			ImmItem item = immStorageG.readFromImmStorage("id=person_0,employeeId=2,meId=1","lastname");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Nixon"));
		}
		
		{
			// check attribute "person[1].firstname" in Employee
			ImmItem item = immStorageG.readFromImmStorage("id=person_1,employeeId=2,meId=1","firstname");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Barak"));
		}

		{
			// check attribute "person[1].lastname" in Employee
			ImmItem item = immStorageG.readFromImmStorage("id=person_1,employeeId=2,meId=1","lastname");
			printf("item=%s\n",item.toString().c_str());
			assert(item.type==9);
			assert(item.data.size()==1);
			assert(item.data[0]==std::string("Obama"));
		}

		///////////////////////////////////
		// Test the iterator filtering
		///////////////////////////////////
		
		// We expect the iterator to NOT return the struct classes that we KNOW has been created above due to the tests
		{
			// first a test that iterators work ok
			ComOamSpiMoIteratorHandleT ith;
			GLOBAL_immCmdOmSearchNextDnOut = "errorId=555";  // this value should NOT be returned cause of the cache!

			// perform a search that will succeed, 
			// we search for "Me=1" subinstances and should get "Employee=2" back
			ComReturnT retGet = testObj.getImmMoIterator(txh,"Me=1","Employee", &ith);	// COM always iterates using ClassName filter
			assert(retGet==ComOk);
			char* searchResult = NULL;
			ComReturnT retNext = testObj.getImmNextMo (ith, &searchResult);		
			assert(retNext==ComOk);
			assert(searchResult != NULL);
			printf("Search Result=%s\n",searchResult);
			assert(searchResult == std::string("2")); //NOTE, iterators only return the instance!!!!! not the classname!!!!						
		}
		{
			////////////////////////////////
			// Test iterator with filtering
			////////////////////////////////
			ComOamSpiMoIteratorHandleT ith;
			GLOBAL_immCmdOmSearchNextDnOut = "immTestId=555";  // this value will be returned because all struct instances are filtered out

			// perform a search that will NOT succeed due to filtering
			// we search for "Me=1,Employee=2" subinstances and should get nothing back since only struct classes are found
			ComReturnT retGet = testObj.getImmMoIterator(txh,"Me=1,Employee=2","Test", &ith);	// COM calls using class filters
			assert(retGet==ComOk);
			char* searchResult = NULL;
			ComReturnT retNext = testObj.getImmNextMo (ith, &searchResult);		
			assert(retNext==ComOk);
			assert(searchResult != NULL);
			printf("Search Result=%s\n",searchResult);
			assert(searchResult == std::string("555"));	// only instance!					
		}
		
		
		
		delete mLastname;
		delete mFirstname;
		delete personData;
		delete attrPerson;
		delete employeeAttrs;
		delete meMoc;
		delete employeeMoc;
		delete cont;
		delete mom;
		
		delete txContextIn;
		
		testPassed();
		
	}


	{
		testStarted("Imm Iterator ");

		// First we setup the test so that we can perform a write!

		// Setup ModelRepository with Me base class and Sub class Employee containing a struct type PersonData

		//   Me<<EcimClass>,
		//     Employee<<EcimClass>>
		//           title:string
		//           person:PersonData
		//
		//  PersonData<<EcimStruct>>{
		//                firstname:string;
		//                lastname:string;     
		//          }  
		
		// COM will read the model from the repository and then it will look for instances for each contained class
		// This means that COM will always iterate over a known class, and since struct classes in IMM are unknown to COM
		// COM will never iterate over them, they are infact invisible to COM without us doing anything!
		//
		
		struct ComOamSpiStructMember* mLastname =  makeStructMember("lastname", ComOamSpiDatatype_STRING,NULL);
		struct ComOamSpiStructMember* mFirstname =  makeStructMember("firstname", ComOamSpiDatatype_STRING, mLastname);
		struct ComOamSpiStruct* personData = makeStruct("PersonData", mFirstname);
		struct ComOamSpiMoAttribute* attrPerson = makeAttribute("person",personData, NULL);
		struct ComOamSpiMoAttribute* employeeAttrs = makeAttribute("title",ComOamSpiMoAttributeType_STRING,attrPerson);
		struct ComOamSpiMoc* meMoc = makeMoc("Me", NULL);
		struct ComOamSpiMoc* employeeMoc = makeMoc("Employee",employeeAttrs);
		struct ComOamSpiContainment* cont =makeContainment(meMoc, employeeMoc);
		struct ComOamSpiMom* mom = makeMom("Me",meMoc);
		setMom(mom);


		// setup IMM storage
		immStorageG.reset();		
		
		{	
			// add the class name attribute for Employee with two attributes "title" and "person"
			std::vector<std::string> className;
			className.push_back("Employee");
			unsigned int IMM_STRING_TYPE=9;
			unsigned int IMM_REF_TYPE = 6;
			immStorageG.addToImmStorage("employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("title"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("person"), IMM_REF_TYPE);
		}
		{	
			// add the class name attribute for PersonData with two attributes "firstname" and "lastname"
			std::vector<std::string> className;
			className.push_back("PersonData");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("personDataId=person_0,employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("firstname"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("lastname"), IMM_STRING_TYPE);
		}
		// add the class name attribute for Me
		{	
			std::vector<std::string> className;
			className.push_back("Me");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
		}
				
		


		
		// iterator across root, eg DN="" and classname "Me" (COM always uses classname!) (Search directly towards IMM, no cache)
		{		
			ComOamSpiTransactionHandleT txh=1;
			TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
			OamSAImmBridge testObj;		
			ComMoAttributeValueContainerT *result = NULL;
			ComOamSpiMoIteratorHandleT ith;		
	
	
			// perform a root search
			
			// setup the search result
			GLOBAL_immCmdOmSearchNextDnOut = "meId=1";
			// performt the search		
			ComReturnT retGet = testObj.getImmMoIterator(txh,"","Me", &ith);		
			assert(retGet==ComOk);
			char* searchResult = NULL;
			ComReturnT retNext = testObj.getImmNextMo (ith, &searchResult);		
			assert(retNext==ComOk);
			assert(searchResult != NULL);
			printf("Search Result=%s\n",searchResult);
			assert(searchResult == std::string("1")); // result should be a COM path!
			delete txContextIn;			
		}


		// iterator across root, eg DN="Me=1,Employee=1" and classname Test (Search directly towards IMM, no cache)
		{		
			ComOamSpiTransactionHandleT txh=1;
			TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
			OamSAImmBridge testObj;		
			ComMoAttributeValueContainerT *result = NULL;
			ComOamSpiMoIteratorHandleT ith;		
			
			// setup the search result
			GLOBAL_immCmdOmSearchNextDnOut = "testId=66";
			// performt the search		
			ComReturnT retGet = testObj.getImmMoIterator(txh,"Me=1,Employee=1","Test", &ith);		
			assert(retGet==ComOk);
			char* searchResult = NULL;
			ComReturnT retNext = testObj.getImmNextMo (ith, &searchResult);		
			assert(retNext==ComOk);
			assert(searchResult != NULL);
			printf("Search Result=%s\n",searchResult);
			assert(searchResult == std::string("66"));
			delete txContextIn;						
		}
		
		
		{
			// create an new employee=2 Richard Nixon, Vice President! :-)		
			// This will store the value in the cache and any search should look in the cache!!
			
			ComOamSpiTransactionHandleT txh=1;
			TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
			OamSAImmBridge testObj;		
	
			//Create an instance to prime the cache
			ComReturnT retCre = testObj.createImmMo(txh,"Me=1","Employee","Employee","2");
			assert(retCre==ComOk);
		
			// NOW we try to search and expect to get a cache hit
			ComOamSpiMoIteratorHandleT ith;
			GLOBAL_immCmdOmSearchNextDnOut = "errorId=555";  // this value should NOT be returned cause of the cache!

			// perform the search, we search for "Me=1" subinstances and should get "Employee=2" back
			ComReturnT retGet = testObj.getImmMoIterator(txh,"Me=1","Employee", &ith);	// COM only ever iterates over known classes!
			assert(retGet==ComOk);
			char* searchResult = NULL;
			ComReturnT retNext = testObj.getImmNextMo (ith, &searchResult);		
			assert(retNext==ComOk);
			assert(searchResult != NULL);
			printf("Search Result=%s\n",searchResult);
			assert(searchResult == std::string("2")); //Only the instance value, not the class...COM style!
			delete txContextIn;
		}
		
		delete mLastname;
		delete mFirstname;
		delete personData;
		delete attrPerson;
		delete employeeAttrs;
		delete meMoc;
		delete employeeMoc;
		delete cont;
		delete mom;
		
		testPassed();
	}




	{		
		testStarted("Write to cache and read from cache only, no IMM access");

		// Setup ModelRepository with Me base class and Sub class Employee containing a struct type PersonData

		//   Me<<EcimClass>,
		//     Employee<<EcimClass>>
		//           title:string
		//           person:PersonData
		//
		//  PersonData<<EcimStruct>>{
		//                firstname:string;
		//                lastname:string;     
		//          }  

		struct ComOamSpiStructMember* mLastname =  makeStructMember("lastname", ComOamSpiDatatype_STRING,NULL);
		struct ComOamSpiStructMember* mFirstname =  makeStructMember("firstname", ComOamSpiDatatype_STRING, mLastname);
		struct ComOamSpiStruct* personData = makeStruct("PersonData", mFirstname);
		struct ComOamSpiMoAttribute* attrPerson = makeAttribute("person",personData, NULL);
		struct ComOamSpiMoAttribute* employeeAttrs = makeAttribute("title",ComOamSpiMoAttributeType_STRING,attrPerson);
		struct ComOamSpiMoc* meMoc = makeMoc("Me", NULL);
		struct ComOamSpiMoc* employeeMoc = makeMoc("Employee",employeeAttrs);
		struct ComOamSpiContainment* cont =makeContainment(meMoc, employeeMoc);
		struct ComOamSpiMom* mom = makeMom("Me",meMoc);
		setMom(mom);


		// setup IMM storage
		immStorageG.reset();		
		
		{	
			// add the class name attribute for Employee with two attributes "title" and "person"
			std::vector<std::string> className;
			className.push_back("Employee");
			unsigned int IMM_STRING_TYPE=9;
			unsigned int IMM_REF_TYPE = 6;
			immStorageG.addToImmStorage("employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("title"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("Employee"), std::string("person"), IMM_REF_TYPE);
		}
		{	
			// add the class name attribute for PersonData with two attributes "firstname" and "lastname"
			std::vector<std::string> className;
			className.push_back("PersonData");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("id=person_0,employeeId=2,meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
			// add attribute defintions to class
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("firstname"), IMM_STRING_TYPE);
			immStorageG.addImmClassAttributeDef(std::string("PersonData"), std::string("lastname"), IMM_STRING_TYPE);
		}
		// add the class name attribute for Me
		{	
			std::vector<std::string> className;
			className.push_back("Me");
			unsigned int IMM_STRING_TYPE=9;
			immStorageG.addToImmStorage("meId=1","SaImmAttrClassName",IMM_STRING_TYPE,className);
		}

		// Count the items in IMM (so we can see that nothing new was added!)
		int itemsInImmBeforeTest = 	immStorageG.getItemCount();

				
		// create an new employee Richard Nixon, Vice President! :-)		
		
		ComOamSpiTransactionHandleT txh=1;
		TxContext* txContextIn = OamSATransactionRepository::getOamSATransactionRepository()->newTxContext(txh);		
		OamSAImmBridge testObj;		
		ComMoAttributeValueContainerT *result = NULL;

		//1. Create the Employee class instance 2	
		ComReturnT retCre = testObj.createImmMo(txh,"Me=1","Employee","dn","Employee=2");
		assert(retCre==ComOk);
		
		// 2. Add string attribute title
		ComMoAttributeValueContainerT *value = new ComMoAttributeValueContainerT;
		value->type = ComOamSpiMoAttributeType_STRING;
		value->nrOfValues = 1;
		value->values = new ComMoAttributeValueT[1];
		value->values[0].value.theString = allocCstr("Vice President");				
		ComReturnT retSet = testObj.setImmMoAttribute(txh,"Me=1,Employee=2","title",value);
		assert(retSet==ComOk);
		cleanUp(value);
		
		// 3. Add struct attribute person

		// lastname (LN)
		ComMoAttributeValueContainerT *valueLN = new ComMoAttributeValueContainerT;
		valueLN->type = ComOamSpiMoAttributeType_STRING;
		valueLN->nrOfValues = 1;
		valueLN->values = new ComMoAttributeValueT[1];
		valueLN->values[0].value.theString = allocCstr("Nixon");								
		ComMoAttributeValueStructMemberT *memberLN = new ComMoAttributeValueStructMemberT;
		memberLN->memberName = allocCstr("lastname");
		memberLN->memberValue = valueLN;
		memberLN->next=NULL; // last member


		// firstname (FN)
		ComMoAttributeValueContainerT *valueFN = new ComMoAttributeValueContainerT;
		valueFN->type = ComOamSpiMoAttributeType_STRING;
		valueFN->nrOfValues = 1;
		valueFN->values = new ComMoAttributeValueT[1];
		valueFN->values[0].value.theString = allocCstr("Richard");								
		ComMoAttributeValueStructMemberT *memberFN = new ComMoAttributeValueStructMemberT;
		memberFN->memberName = allocCstr("firstname");
		memberFN->memberValue = valueFN;
		memberFN->next=memberLN; // link to next member
		
		// Set struct attribute by linking in the members
		ComMoAttributeValueContainerT *valueStruct = new ComMoAttributeValueContainerT;
		valueStruct->type = ComOamSpiMoAttributeType_STRUCT;
		valueStruct->nrOfValues = 1;
		valueStruct->values = new ComMoAttributeValueT[1];
		valueStruct->values[0].value.structMember = memberFN;				

		// write the struct attribute person
		ComReturnT retSetStruct = testObj.setImmMoAttribute(txh,"Me=1,Employee=2","person",valueStruct);
		assert(retSetStruct==ComOk);
		cleanUp(valueStruct);					

		// Flush changes towards IMM
		//ComReturnT retPrep = testObj.OamSAPrepare(txh);
		//assert(retPrep==ComOk);
		
		
		
		// Read the values back from CACHE, not the IMM
		
		{	
			// Read struct
			ComMoAttributeValueContainerT *result = NULL;
			ComReturnT ret = testObj.getImmMoAttribute(txh,"Me=1,Employee=2","person",&result);
			
			// verify the result
			assert(ret==ComOk);
			assert(result != NULL);
			assert(result->type==14); // struct
			assert(result->nrOfValues==1);
			
			ComMoAttributeValueStructMember* member;
			// First struct member		
			member = result->values[0].value.structMember;
			assert(std::string(member->memberName) == std::string("firstname"));
			assert(member->memberValue->type == 9); // string
			assert(member->memberValue->nrOfValues == 1);
			assert(std::string(member->memberValue->values[0].value.theString) == std::string("Richard"));
			assert(member->next!=NULL);
			
			// Second struct member
			member = member->next;
			assert(std::string(member->memberName) == std::string("lastname"));
			assert(member->memberValue->type == 9); // string
			assert(member->memberValue->nrOfValues == 1);
			assert(std::string(member->memberValue->values[0].value.theString) == std::string("Nixon"));
			assert(member->next==NULL);	// no more members
			//cleanUp(result);		
		}	

		// Verify that we can read normal attr from cache		
		{	
			// Read title attribute
			ComMoAttributeValueContainerT *result = NULL;			
			ComReturnT ret = testObj.getImmMoAttribute(txh,"Me=1,Employee=2","title",&result);
			// verify the result
			assert(ret==ComOk);
			assert(result != NULL);
			assert(result->type==9); // string
			assert(result->nrOfValues==1);
			assert(result->values[0].value.theString == std::string("Vice President"));
			//cleanUp(result);
		}			
		
		//
		// Verify that the IMM was not modified		
		{
			assert(itemsInImmBeforeTest == immStorageG.getItemCount());
		}
		
		delete mLastname;
		delete mFirstname;
		delete personData;
		delete attrPerson;
		delete employeeAttrs;
		delete meMoc;
		delete employeeMoc;
		delete cont;
		delete mom;
		
		delete txContextIn;
		
		testPassed();
		
	}





	{
		// TODO: additional testing needed
		// 1. negative tests, what if transactions towards IMM fail when we are creating structs?
		// 2. memory leak tests!!!!! 
	}

	// Clean up all memory allocated by IMM functions to allow valgrind some peace-of-mind
	immMemoryTrackerG.cleanup();
	
	
	testAllPassed();
	
}
