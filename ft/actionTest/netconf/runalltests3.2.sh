#!/bin/bash

if [ "$1" = "" ]
then
  echo "Target address not specified "
  echo "Usage: runalltest.sh <target address>"
  exit 1
fi
SC_ADDR=$1
COMSA3_2_BWD=$2
run () {
	./runtest.sh $SC_ADDR $COMSA3_2_BWD $1 $2 $3

	ret=$?
	if [[ $ret -ne 0 ]]
	then
	  echo "TEST FAILED, exit ..."
	  exit 1;
	fi
}

# Create key
./pwdfree_ssh.py $SC_ADDR -k ~/.ssh/id_rsa

run netconf_returntype_simple.xml er_returntype_simple.xml
run netconf_returntype_void.xml   er_returntype_void.xml
run netconf_returntype_int.xml   er_returntype_int_3.2.xml
run netconf_returntype_error.xml   er_returntype_error.xml

run netconf_parameters_bool.xml er_parameters_bool.xml er_dump_bool.txt
run netconf_parameters_enum.xml er_parameters_enum.xml er_dump_enum.txt
run netconf_parameters_eventtype.xml er_parameters_eventtype.xml er_dump_eventtype.txt
run netconf_parameters_int.xml er_parameters_int.xml er_dump_int.txt
run netconf_parameters_order.xml er_parameters_order.xml er_dump_order.txt
run netconf_parameters_classref.xml er_parameters_classref.xml er_dump_classref.txt

echo ""
echo "--- RESULT: All Test PASSED ---"
