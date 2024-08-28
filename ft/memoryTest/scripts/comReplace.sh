#! /bin/sh

logPath=$1 #path to where the logs will be stored
currentComFile=$2 #name of com.sh file with full path. Typically /opt/com/bin/com.sh

newComFile="$currentComFile.new"
oldComFile="$currentComFile.old"
rm -f $newComFile
#searchPattern='grep COM_CMD $currentComFile | grep COM_CONF | grep "2>&1"'
mkdir -p $logPath
replaceLine="/usr/bin/valgrind --malloc-fill=25 --free-fill=27 --leak-check=full --error-limit=no --fullpath-after= --show-possibly-lost=no --undef-value-errors=no --log-file=\"$logPath/valgrind_\$(date '+%y-%m-%d_%H%M%S').log\" \${COM_CMD} \${COM_CONF} >> \${STDOUT_FILE} 2>&1 &"

matchCounter=0
IFS='¨'
exec<$currentComFile
while read line
do
	if [[ `echo $line | grep COM_CMD | grep COM_CONF | grep "2>&1"` = "" ]]; then
		echo "$line" >> $newComFile
	else
		echo "    $replaceLine" >> $newComFile
#		echo "" >> $newComFile
		matchCounter=`expr $matchCounter + 1`
	fi
done


if [ $matchCounter -ne 1 ]; then
	echo "Number of matches for the search pattern is $matchCounter, which is not equal to the expected 1. New com.sh is corrupt and cannot be used."
	exit 1
fi
unset IFS

cp -f $currentComFile $oldComFile
cp -f $newComFile $currentComFile
