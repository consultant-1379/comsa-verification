#!/bin/bash

# echo "Params: " $1 $2 $3 $4 $5
# $2 support for test on COM SA 3.2 backward.

print_usage () {
  echo "Usage: runtest.sh <target address> <add option: True/False> <netconf file> <expected reply> [er_dumpfile] "
  exit 1
}

if [ "$1" = "" ]
then
  echo "Target address not specified "
  print_usage
fi

if [ "$3" = "" ]
then
  echo "netconf file not specified "
  print_usage
fi

if [ "$4" = "" ]
then
  echo "expected netconf reply file not specified "
  print_usage
fi

#Address to SC-1
SC_ADDR=$1
COMSA3_2_BWD=$2
NETCONF_FILE=$3
ER_REPLY_FILE=$4


SSH_SC="ssh root@$SC_ADDR"
SCP_SC="scp "

CURTIME=`date +%d%m%y_%H%M%S`

#
# Check if tmp folder is exist
#
if [[ ! -d "/tmp/$USER" ]]; then
	mkdir -p /tmp/$USER
fi

#
# Check if expected dump file is specified
#
DUMPFILE=
ER_DUMPFILE=
if [ "$5" != "" ]
then
	DUMPFILE=dump_$CURTIME.txt
	ER_DUMPFILE=$5
	echo "Set result filename on cluster " $ER_DUMPFILE
fi

#
# Execute netconf, set file name for dump on cluster
#
if [ "$DUMPFILE" != "" ]
then
	# replace _FILENAME_ with dump file name
	NETCONF_SETFILENAME=/tmp/$USER/netconf_$CURTIME.xml
	NETCONF_SETFILENAM_REPLY=/tmp/$USER/netconf_$CURTIME_reply.xml

	sed "s/_FILENAME_/$DUMPFILE/g" netconf_setfilename.xml > $NETCONF_SETFILENAME

	echo "Execute netconf set dump filename " $NETCONF_SETFILENAME
	if [ "$COMSA3_2_BWD" = "True" ]; then
		cat $NETCONF_SETFILENAME | $SSH_SC -s -t -t netconf > $NETCONF_SETFILENAM_REPLY 2> /dev/null &
	else
		cat $NETCONF_SETFILENAME | $SSH_SC -s -t netconf > $NETCONF_SETFILENAM_REPLY 2> /dev/null &
	fi
	sleep 5
	kill -TERM $! 2> /dev/null
fi

#
# Execute netconf
#
OUTFILE=/tmp/$USER/out_parameters_$CURTIME.txt
echo "Execute netconf " $NETCONF_FILE
#echo "cat $NETCONF_FILE | $SSH_SC -s -t -t netconf > $OUTFILE & "
if [ "$COMSA3_2_BWD" = "True" ]; then
	cat $NETCONF_FILE | $SSH_SC -s -t -t netconf > $OUTFILE 2> /dev/null &
else
	cat $NETCONF_FILE | $SSH_SC -s -t netconf > $OUTFILE 2> /dev/null &
fi
sleep 5
kill -TERM $! 2> /dev/null

TMPFILE=/tmp/$USER/tmp_action_$CURTIME.txt

#
# Check reply
#
echo "Check returned result..."
cat $OUTFILE | sed -n '/^<rpc-reply/,/^<\/rpc-reply/p' > $TMPFILE
diff -q -w -B $TMPFILE $ER_REPLY_FILE
ret=$?
if [[ $ret -ne 0 ]]
then
  echo "FAILED: Return values not as expected"
  exit 1;
fi

#
# Check dump file
#
if [ "$DUMPFILE" != "" ]
then
	echo "Check result on cluster..."
	$SCP_SC  root@$SC_ADDR:/tmp/actiontest_$DUMPFILE /tmp/$USER/actiontest_$DUMPFILE
	ret=$?
	if [[ $ret -ne 0 ]]
	then
	  echo "Cannot copy /tmp/actiontest_$DUMPFILE from SC, exit"
	  exit 1;
	fi
	diff -q -w -B /tmp/$USER/actiontest_$DUMPFILE  $ER_DUMPFILE
	ret=$?
	if [[ $ret -ne 0 ]]
	then
	  echo "FAILED: Parameter values not as expected"
	  exit 1;
	fi
fi

echo "*** TEST PASSED "
exit 0;
