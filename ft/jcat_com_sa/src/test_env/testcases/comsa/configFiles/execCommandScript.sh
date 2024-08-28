#!/bin/sh
file1=$1
file2=$2
file3=$3
ipAdress=$4
file4=$5
cat $file1 $file2 $file3 | ssh root@$ipAdress -s -t -t netconf > $file4
cat $file4 