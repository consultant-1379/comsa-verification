#!/bin/sh

totalAlarms=`expr $1 + 1`
alarmNum=1
while [ $alarmNum -lt $totalAlarms ]
do
  #echo "Clearing another alarm  ---->>>> $alarmNum"
  ntfsend -T 0x4000 -e 16384 -c 193,12960,1 -n "fmAlarmTypeId=ComSaCLMClusterNodeUnavailable,fmAlarmModelId=CW,fmId=$alarmNum" -s 0 -a "Linux Time:1426922375" > /dev/null
  alarmNum=`expr $alarmNum + 1`
  #date
  #usleep 500
done
