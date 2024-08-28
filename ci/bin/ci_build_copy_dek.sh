#! /bin/csh -x
#
if ($#argv == 0) then
  echo "You need a parameter to run this script"
  echo "Parameter 1 is branch you build on"
  exit 1
endif

set COMSA_RELEASE_DIR="/home/comsaci/releases"
set COMSA_SOURCE_REPO="comsa-source"
set COMSA_TEST_REPO="comsa-verification"
set COMSA_TARGET_DIR="${COMSA_RELEASE_DIR}/$1"
echo "Copying"
echo "Creating dir $COMSA_TARGET_DIR"
mkdir -p $COMSA_TARGET_DIR
\cp $COMSA_SOURCE_REPO/release/cxp_archive/* $COMSA_TARGET_DIR/
sleep 2
cd $COMSA_SOURCE_REPO
set sha1source=`git rev-parse --verify HEAD`
cd ..
echo $sha1source > $COMSA_TARGET_DIR/$COMSA_SOURCE_REPO.txt
cd $COMSA_TEST_REPO
git pull
set sha1source=`git rev-parse --verify HEAD`
cd ..
echo $sha1source > $COMSA_TARGET_DIR/$COMSA_TEST_REPO.txt
chmod -R 0777 $COMSA_TARGET_DIR
