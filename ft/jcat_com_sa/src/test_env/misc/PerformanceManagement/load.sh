#!/bin/sh

if [ 2 -ne $# ] ; then
  echo "$0 pre|post numberOfSeconds"
  exit 1
fi
 
while [ ! -e /home/test/pm/startpmloadcheck ] ; do
   sleep 1
done
  
 
mpstat 1 $2 > /home/test/pm/$1.pmLoad.`hostname`
 
\rm -f /home/test/pm/startpmloadcheck

exit 0