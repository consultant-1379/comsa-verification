#! /bin/bash 

if [ "x$1" = "x" ]; then
  echo "No directory!"
  exit 1
fi

if [ ! -d $1 ]; then
  echo "Bad directory: $1!"
  exit 1
fi

ALL=`dirname $0`/all_bt.sh
BT=`dirname $0`/backtrace.sh

$ALL $1 > all_dumps

sed 's/.*core //' < all_dumps | sort | uniq -c > frequency

for MD5 in `sed 's/ *[0-9]* *//' < frequency | sed 's/ -//'`; do
  DUMP=$(grep $MD5 all_dumps | sed 's/ .*$//' | tail -1)
  COUNT=$(grep $MD5 frequency | sed 's/[^0-9]*\([0-9]*\).*/\1/')

  echo ""
  echo "========== $COUNT =========="
  $BT $DUMP
done
