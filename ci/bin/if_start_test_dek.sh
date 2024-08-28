#! /bin/tcsh -ex
# Start testsuites in the ci

if ($#argv < 6) then
  echo "You need atleast six parameters"
  echo "<COMSA branch> <RUN_TEST_DIR> <COM_VERSION> <COREMW_VERSION> <NOTE_TYPE> <TEST_SUITES> [ -f <build_folder>]"
  echo "example: comsa_dev my_test_folder_2n 4.0/latest 3.4/latest 1 regTestSuite.xml,regTestSuite2.xml"
  echo "-f=fore another dir than latest snapshow than latest"
  echo "-a=additional paramter, can not be used together with -f"
  echo "NOTE!!! NOTE_TYPE 1=2NODE, 2=1NODE"
  exit 1
endif
set COMSA_BRANCH="$1"
set RUN_TEST_DIR="$2"
set COM_VERSION="$3"
set COREMW_VERSION="$4"
set NODE_TYPE="$5"

set TEST_SUITES = `echo $6:q | sed 's/,/ /g'`

set COMSA_SOURCE_REPO="comsa-source"
set COMSA_TEST_REPO="comsa-verification"
set ADDITIONAL_CMD=""
set ADDITIONAL_PARAM=""

if ( "$7" == '-f' ) then
  echo "Untested force was used, lets try to start the test on the date in the following argument <$8>"
  set COMSA_TARGET_DIR=$8
  if ( "$9" == '-a' ) then
    echo "additional paramter [$10] [$11] will be passed to the build"
    set ADDITIONAL_CMD=$10
    set ADDITIONAL_PARAM=$11
  endif
else
  set COMSA_TARGET_DIR=`findBuild_dek.sh ${COMSA_BRANCH} SN`
endif
if ( "$7" == '-a' ) then
  echo "additional paramter [$8] [$9] will be passed to the build"
  set ADDITIONAL_CMD=$8
  set ADDITIONAL_PARAM=$9
endif


echo "Trying to find directory: ${COMSA_TARGET_DIR}"
if ( -d ${COMSA_TARGET_DIR} ) then
  echo "It appeards that we have something to test today"
  echo "Todays run will be on whats in ${COMSA_TARGET_DIR}"
else
  echo "Nothing in todays directory, resting for today"
  exit 0
endif

PrepareTestDirectory.tcsh ${RUN_TEST_DIR} ${COM_VERSION} ${COREMW_VERSION} ${COMSA_TARGET_DIR} ${NODE_TYPE}
if ( ${status} != 0 ) then
  echo "Something went wrong when setting up test envirement"
  exit 1
endif

echo "Prepare the source-git repo"
cd ${COMSA_SOURCE_REPO}
git fetch
set sourceSHA1=`cat ${COMSA_TARGET_DIR}/${COMSA_SOURCE_REPO}.txt`
git checkout src/com_specific/unittest/Makefile
git checkout ${sourceSHA1}
if ( ${status} != 0 ) then
  echo "Something went wrong when checking out latest source sha1 commit"
  exit 1
endif
cd ..

echo "prepare the test repo"
cd ${COMSA_TEST_REPO}
git fetch
set testSHA1=`cat ${COMSA_TARGET_DIR}/${COMSA_TEST_REPO}.txt`
git checkout ${testSHA1}
if ( ${status} != 0 ) then
  echo "Something went wrong when checking out latest test sha1 commit"
  exit 1
endif
cd ${STARTDIR}
sed -i 's/COM_SA_DEV)\/coremw-tools/STARTDIR)\/..\/coremw-tools/g' comsa-source/src/com_specific/unittest/Makefile
cd ${COMSA_TEST_REPO}
cd ft
./compiledeps_dek.sh
cd ..
cd ..
echo "GIT setup complete"

setenv COMSA_VERIFICATION_COMMIT_ID `echo ${testSHA1} | cut -c 1-7`
setenv COMSA_REPO_PATH_COMMIT_ID `echo ${sourceSHA1} | cut -c 1-7`

foreach TEST_SUITE ($TEST_SUITES:q)
  echo "RUN_TEST_DIR:${RUN_TEST_DIR}"
  echo "COMSA_TARGET_DIR: $COMSA_TARGET_DIR"
  echo $TEST_SUITE:q
  echo "ADDITIONAL_CMD:${ADDITIONAL_CMD}"
  echo "ADDITIONAL_PARAM:${ADDITIONAL_PARAM}"
  ciTest_dek.sh ${RUN_TEST_DIR} ${COMSA_TARGET_DIR} $TEST_SUITE:q ${ADDITIONAL_CMD} ${ADDITIONAL_PARAM}
  if ( $status != 0 ) then
    echo "There were fatal errors during the testrun"
    exit 1
  endif
end

echo "done with all suites"
