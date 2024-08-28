#! /bin/tcsh -fx
#
set OUTPUTFILE="ci_output.txt"
set COMSA_TEST_REPO="comsa-verification"

if ($#argv < 3) then
  echo "You need atleast three parameters"
  echo "<COM-CoreMW-COMSA_Test_Dir> <test result output dir> <Testsuite.xml>"
  echo "example: ciTest my_testDir /home/comsaci/releases/comsa_dev_2014-05-08 regTestSuite.xml"
  exit 1
endif

echo "Running the tests"
echo "Asuming sourceme.tcsh has been sourced already"
echo "Asuming dependencies have been compiled"
cd ${COMSA_TEST_REPO}/ft/
rm -f ${OUTPUTFILE}

executive.py --config $VBOX_TARGET --productSettings comsa --suite $3 --swDirNumber $1 --installSw True --build False $4 $5 > $OUTPUTFILE

set TESTRESULTDIR=`grep "The log dir will be : " $OUTPUTFILE | cut -d ':' -f4`
echo "Copying the test results from $TESTRESULTDIR to $2/dek"
mkdir -p $2/dek
cp $TESTRESULTDIR/tpt.txt $2/dek/${1}-${3}.tpt
echo $TESTRESULTDIR > $2/dek/${1}-${3}.path
rm $OUTPUTFILE
if ($?WORKSPACE) then
  if ($?BUILD_NUMBER) then
    mkdir -p ${WORKSPACE}/${BUILD_NUMBER}
    cp $TESTRESULTDIR/dt.xml ${WORKSPACE}/${BUILD_NUMBER}/${1}-${3}.xml
  endif
endif
cd ../../

echo "Test done"