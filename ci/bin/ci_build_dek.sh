#! /bin/tcsh -ex
# This is to start the CI-Build
# It will build and store the build in /home/comsaci/releases
cd $STARTDIR
if ($#argv < 2) then
  echo "You need two parameter to run this script"
  echo "Parameter 1 is branch you want to build on: ex comsa_dev"
  echo "Second parameter is type of build, SN=Snapshot SH=Shipment CP=CorrectionPackage"
  exit 1
endif

if (! -d comsa-source) then
  echo "current folder needs to be positioned so that on a 'ls' I see the repository folder named comsa-source"
  exit 1
endif

if (! -d comsa-verification) then
  echo "current folder needs to be positioned so that on a 'ls' I see the repository folder named comsa-verification"
  exit 1
endif

set last_build_folder="/home/comsaci/last_build/"

set COMSA_BRANCH="$1"
if ( $2 == "SN" ) then
  set BUILDCMD="all"
else if ( $2 == "SH" ) then
  set BUILDCMD="shipment"
else if ( $2 == "CP" ) then
  set BUILDCMD="correctionpackage"
else
  echo "Wrong buildtype, exiting"
  exit 1
endif
set BUILD_TYPE=$2

echo "Building on branch $COMSA_BRANCH and build command is: $BUILDCMD"

echo "Updating verification code"
cd comsa-source
git checkout master
git fetch
git rebase
cd ..

echo "Updating source code"
cd comsa-source
git checkout abs/tmp_version
git checkout $COMSA_BRANCH
git fetch
git rebase

if ( $status != 0 ) then
  echo "Something went wrong during git rebase, this need to be fixed manually"
  exit 1
endif

echo "Git branch checkout and rebase seem to work"

set MAJOR_VERSION=`cat ${last_build_folder}/${COMSA_BRANCH}`
if ( $status != 0 ) then
  echo "error in file ${last_build_folder}/${COMSA_BRANCH}"
  exit 1
endif

# Snapshots
if ( $BUILD_TYPE == "SN" ) then
  echo "Building a snapshot"
  set last_shipment=`cat ${last_build_folder}/${COMSA_BRANCH}_SH`
  set RELEASE_VERSION=`expr ${last_shipment} + 1`
  if ( $status != 0 ) then
    echo "error in file ${last_build_folder}/${COMSA_BRANCH}_SH"
    exit 1
  endif
  set P_REV=`cat ${last_build_folder}/${COMSA_BRANCH}_P_REV`
  if ( $status != 0 ) then
    echo "error in file ${last_build}/${COMSA_BRANCH}_P_REV"
    exit 1
  endif
  echo $P_REV > abs/tmp_version
  cd ..
  ci_build_build_dek.sh $BUILDCMD
  if ( $status != 0 ) then
    echo "failed to build COM SA"
    exit 1
  endif
  sleep 10
  cat "comsa-source/abs/tmp_version" > "${last_build_folder}/${COMSA_BRANCH}_P_REV"
  set BUILD_TIME=`date --date now +%Y%m%d.%H%M%S`

  ci_build_copy_dek.sh ${COMSA_BRANCH}-${MAJOR_VERSION}_SH${RELEASE_VERSION}-${BUILD_TYPE}${BUILD_TIME}


# Shipments
else if ( $BUILD_TYPE == "SH" ) then
  echo "Building a shipment"
  set last_shipment=`cat ${last_build_folder}/${COMSA_BRANCH}_${BUILD_TYPE}`
  set RELEASE_VERSION=`expr ${last_shipment} + 1`
  if ( $status != 0 ) then
    echo "error in file ${last_build_folder}/${COMSA_BRANCH}_${BUILD_TYPE}"
    exit 1
  endif

  git checkout -b comsa${MAJOR_VERSION}_sh${RELEASE_VERSION} origin/master
  git merge origin/comsa_dev
  cd ..

  ci_build_build_dek.sh $BUILDCMD
  if ( $status != 0 ) then
    echo "failed to build COM SA"
    exit 1
  endif
  sleep 10

  ci_build_copy_dek.sh ${COMSA_BRANCH}-${MAJOR_VERSION}_${BUILD_TYPE}${RELEASE_VERSION}

  echo "storing build version in ${last_build_folder}/${COMSA_BRANCH}_SH"
  echo "${RELEASE_VERSION}" > "${last_build_folder}/${COMSA_BRANCH}_SH"

  echo "Now whats needs to be done is to set the tags and commit the changed files"

# Correctionpackage
else if ( $BUILD_TYPE == "CP" ) then
  echo "Building a correctionpackage"
  set last_correctionpackage=`cat ${last_build_folder}/${COMSA_BRANCH}_${BUILD_TYPE}`
  set RELEASE_VERSION=`expr ${last_correctionpackage} + 1`
  if ( $status != 0 ) then
    echo "error in file ${last_build_folder}/${COMSA_BRANCH}_${BUILD_TYPE}"
    exit 1
  endif
  cd ..

  ci_build_build_dek.sh $BUILDCMD
  if ( $status != 0 ) then
    echo "failed to build COM SA"
    exit 1
  endif
  sleep 10
  ci_build_copy_dek.sh ${COMSA_BRANCH}-${MAJOR_VERSION}_${BUILD_TYPE}${RELEASE_VERSION}

  echo "storing build version in ${last_build_folder}/${COMSA_BRANCH}_${BUILD_TYPE}"
  echo "${RELEASE_VERSION}" > "${last_build_folder}/${COMSA_BRANCH}_${BUILD_TYPE}"

  echo "Now whats needs to be done is to set the tags and commit the changed files"

# Default (Error)
else
  echo "Wrong buildtype, this should not be reached"
  exit 1
endif

echo "DONE"
