#!/bin/sh

# The script measure alarms in COM.
# $ alarm_test.sh <raise_cease_50_alarms|raise_100_alarms|raise_1000_alarms|raise_100_alerts|raise_cease_10_alarms_per_second|measure_time>

for x in $(seq 1 500000) ; do 
   date
   ntfsend -T 0x4000 -c 18568,2,2 
   ntfsend -T 0x4000 -c 18568,2,2 -s0
done
