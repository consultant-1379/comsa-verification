#! /bin/tcsh 
# 
if ($#argv == 0) then
  echo "You need a parameter to run this script"
  echo "Parameter 1 is the command to send to comsabuild script, it can be all, shipment or correctionpackage"
  exit 1
endif


echo "Building"
cd comsa-source/abs/
./comsabuild clean
sleep 5
./comsabuild $1 > ../../buildoutput.txt
sleep 15
cd ../../
set errors=`cat buildoutput.txt | grep -c -i "error"`
set warnings=`cat buildoutput.txt | grep -c -i "warning"`
if ( $errors != 0 ) then
  echo "Errors during the build, this need manual checking"
  exit 1
endif
if ( $warnings != 0 ) then
  echo "Warnings during the build, this need manual checking"
  exit 1
endif
rm buildoutput.txt

