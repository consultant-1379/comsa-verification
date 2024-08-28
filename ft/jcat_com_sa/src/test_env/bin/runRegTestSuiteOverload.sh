#! /bin/sh
outputFile=`date +%s%N`
outputFile="$outputFile.txt"
touch $outputFile
tail -f $outputFile &
executive.py --suite cliConfigurationTestSuite.xml --runStressTool True $@ > $outputFile
executive.py --suite netconfConfigurationTestSuite.xml --runStressTool True $@ > $outputFile
executive.py --suite ftSdp556.xml --runStressTool True $@ > $outputFile
executive.py --suite ftSdp665.xml --runStressTool True $@ > $outputFile
executive.py --suite ftSdp763.xml --runStressTool True $@ > $outputFile
executive.py --suite ftSdp1043_2.xml --runStressTool True $@ > $outputFile
executive.py --suite ftSdp1272.xml --runStressTool True $@ > $outputFile
executive.py --suite ftMr29333.xml --runStressTool True $@ > $outputFile
executive.py --suite TraceCCTestSuite.xml --runStressTool True $@ > $outputFile
executive.py --suite ftSdp1724.xml --runStressTool True $@ > $outputFile
executive.py --suite ftMr29443.xml --runStressTool True $@ > $outputFile
executive.py --suite ftMr35347.xml --runStressTool True $@ > $outputFile
executive.py --suite ftMr26712.xml --runStressTool True $@ > $outputFile
executive.py --suite pmtsaSuite.xml --runStressTool True $@ > $outputFile
executive.py --suite alarmsTestSuite.xml --runStressTool True $@ > $outputFile
executive.py --suite complexDataTypes.xml --runStressTool True $@ > $outputFile
executive.py --suite ftBfuTestSuite.xml --runStressTool True $@ > $outputFile
executive.py --suite bfuCL5TestSuite.xml --runStressTool True $@ > $outputFile
kill $(jobs -pr)
\rm $outputFile
trap 'kill $(jobs -pr)' SIGINT SIGTERM EXIT
