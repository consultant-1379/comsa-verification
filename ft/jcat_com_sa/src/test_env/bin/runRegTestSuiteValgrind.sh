#! /bin/sh
outputFile=`date +%s%N`
outputFile="$outputFile.txt"
touch $outputFile
tail -f $outputFile &
executive.py --suite regTestSuiteValgrind.xml $@ > $outputFile
executive.py --suite regTestSuite2Valgrind.xml $@ > $outputFile
kill $(jobs -pr)
\rm $outputFile
trap 'kill $(jobs -pr)' SIGINT SIGTERM EXIT

