#!/bin/sh
startDate=`date`
for x in $(seq 1 600) ; do
   cd /opt/com/bin/
   ./cliss < $1 > /dev/null
   echo "Iterations done: $x"
done
echo "start date: $startDate"
date=`date`
echo "end date:   $date"
