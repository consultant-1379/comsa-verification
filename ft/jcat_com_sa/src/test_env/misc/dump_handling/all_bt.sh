#!/bin/bash

BT=`dirname $0`/backtrace.sh

if [ "x$1" = "x" ]; then
  echo "No directory with core dumps!"
  exit 1
fi

if [ ! -d $1 ]; then
  echo "$1 does not exist!"
fi

for i in $1/*; do
  DUMP="$i"
  
  SUM=`$BT $DUMP | sed 's/([^)]*)/(...)/' | sed 's/0x[0-9a-fA-F]*/0x????????/' | grep "#[0-9]*" | md5sum`
  echo $DUMP $SUM
done
