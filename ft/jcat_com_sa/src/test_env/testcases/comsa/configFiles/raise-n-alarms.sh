#!/bin/sh

#
# Register $1 unique alarms by calling ntfsend in a loop with some delay between the iterations.
# The alarm rate is controlled by a delay in microseconds
# $2 is set to '1' if running on Virtual Box to set the delay to 0
# On Virtual Box target the delay is set to 0 which gives rate of about 30 alarms per second (at DEK)
#

totalAlarms=`expr $1 + 1`

alarmNum=1

# delays in microseconds
#my_delay=500000 #   2 alarms per second
#my_delay=150000 #   7 alarms per second
#my_delay=100000 #  10 alarms per second
#my_delay=50000  # < 20 alarms per second
my_delay=20000  #  < 50 alarms per second
#my_delay=10000  # < 100 alarms per second

if [ $2 -eq 1 ]; then
	my_delay=0  #  For Virtual Box target at DEK
fi

#echo Start raising alarms time: `date`
#while [ $alarmNum -lt 2001 ]
while [ $alarmNum -lt $totalAlarms ]
do
  #echo "Sending another alarm  ---->>>> $alarmNum"
  ntfsend -T 0x4000 -e 16384 -c 193,12960,1 -n "fmAlarmTypeId=ComSaCLMClusterNodeUnavailable,fmAlarmModelId=CW,fmId=$alarmNum" -s 5 -a "Linux Time:1426922375" > /dev/null
  alarmNum=`expr $alarmNum + 1`
  #date
  usleep $my_delay
done

# Return the timestamp number of seconds since 1-Jan-1970
echo `date +%s`
