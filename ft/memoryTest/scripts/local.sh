#!/bin/sh

# The script measure alarms in COM.
# $ alarm_test.sh <raise_cease_50_alarms|raise_100_alarms|raise_1000_alarms|raise_100_alerts|raise_cease_10_alarms_per_second|measure_time>

LOG_PATH_FILE="/home/ejomnin/cli_output.log"

for x in $(seq 1 1000) ; do
   echo date

#   ./cliss < ./change_to_55.txt >> $LOG_PATH_FILE
#   ./cliss < ./change_to_60.txt >> $LOG_PATH_FILE
#   ./cliss < ./change_to_55.txt
#   ./cliss < ./change_to_60.txt
   ./cliss < ./small_test_struct.txt
done
