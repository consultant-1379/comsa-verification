#! /bin/tcsh -e
# This will find the latest build of the specified type in the release folder

if ($#argv < 2) then
  echo "Find the latest of todays build / latest shipment or CP"
  echo "You need a parameter to run this script"
  echo "Parameter 1 is branch you want to find latest build on: ex comsa_dev"
  echo "Parameter 2 is what build type you are looking for SN, SH or CP"
  echo "-f is optional, specify what day to look for, format +%Y%m%d"
  exit 1
endif

set COMSA_BRANCH="$1"

if ( $2 == "SN" ) then
else if ( $2 == "SH" ) then
else if ( $2 == "CP" ) then
else
  echo "Wrong buildtype, exiting"
  exit 1
endif
set BUILD_TYPE=$2

set last_build_folder="/home/comsaci/last_build/"
set RELEASE_FOLDER="/home/comsaci/releases/"

if ( "$3" == "-f" ) then
  set BUILD_DAY="$4"
else
  set BUILD_DAY="*"
endif

#set YESTERDAY=`date --date --yesterday +%Y%m%d`

set MAJOR_VERSION=`cat ${last_build_folder}/${COMSA_BRANCH}`
if ( $status != 0 ) then
  echo "error in file ${last_build_folder}/${COMSA_BRANCH}"
  exit 1
endif

if ( $BUILD_TYPE == "CP" ) then
  set RELEASE_VERSION=`cat ${last_build_folder}/${COMSA_BRANCH}_CP`
  set FOLDERS=`ls -d "${RELEASE_FOLDER}${COMSA_BRANCH}-${MAJOR_VERSION}_CP${RELEASE_VERSION}"`
else if ( $BUILD_TYPE == "SH" ) then
  set RELEASE_VERSION=`cat ${last_build_folder}/${COMSA_BRANCH}_SH`
  set FOLDERS=`ls -d "${RELEASE_FOLDER}${COMSA_BRANCH}-${MAJOR_VERSION}_SH${RELEASE_VERSION}"`
else if ( $BUILD_TYPE == "SN" ) then
  set last_shipment=`cat ${last_build_folder}/${COMSA_BRANCH}_SH`
  set RELEASE_VERSION=`expr ${last_shipment} + 1`
  set FOLDERS=`ls -d ${RELEASE_FOLDER}${COMSA_BRANCH}-${MAJOR_VERSION}_SH${RELEASE_VERSION}-${BUILD_TYPE}${BUILD_DAY}.*`
else
  echo "unsupported build type, exiting"
  exit 1
endif
if ( $status != 0 ) then
  echo "error finding release version"
  exit 1
endif

set FOLDERLIST=`echo $FOLDERS:q | sed 's/ / /g'`
foreach FOLDER (${FOLDERLIST:q})
  set LATEST="$FOLDER"
end


if ( -d ${LATEST} ) then
  echo "$FOLDER"
else
  echo "Something went wrong in finding folders, exiting"
  exit 1
endif
