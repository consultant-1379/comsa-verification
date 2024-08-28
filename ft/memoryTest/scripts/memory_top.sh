#!/bin/sh

# The script measure alarms in COM.
# $ alarm_test.sh <raise_cease_50_alarms|raise_100_alarms|raise_1000_alarms|raise_100_alerts|raise_cease_10_alarms_per_second|measure_time>

LOG_PATH_FILE="/home/efaiami/mem_top.log"
PID_FILE=/opt/com/run/com.pid
PID_TMP=`cat $PID_FILE`
COM_PROCESS=`ps -p "${PID_TMP}" | grep com`
proc_path="/proc/$PID_TMP"
echo $proc_path

for x in $(seq 1 10000) ; do 
   #starttimewhole=`date +%s%N`
   cat $proc_path/smaps > /home/efaiami/temp.txt 
   date >> $LOG_PATH_FILE
   cat /home/efaiami/temp.txt | head -49 | tail -4 >> $LOG_PATH_FILE
#   top -b -n1 | grep memoryCheck >> $LOG_PATH_FILE
   sleep 5
done
