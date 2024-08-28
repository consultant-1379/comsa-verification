#!/bin/sh

## This script analyzes all valgrind log files in the directory it is run from.
## In order to use it, simply copy it to the directory where the log files are stored and run it without arguments.
## The output is a set of files, as follows:
## - leak*.txt: all the unique blocks from the valgrind leak summary including the line containing
##   the number of bytes and blocks that are affected by the leak and the type of the leak (definitely lost or possibly lost etc.).
## - no_header_leak*.txt: all the unique blocks from the valgrind leak summary including the line containing
##   the type of the leak (definitely lost or possibly lost etc.), but without the number of bytes and blocks that are affected by the leak.
##   This is needed to be distinguished because some leaks point to the same location in the source code, but in different
##   log files these leaks can have different sizes
## - reportLongHeader.txt: the content of all leak*.txt files in one file
## - reportShortHeader.txt: the content of all no_header_leak*.txt files in one file

leakFileCounter=0
# leakFileCounter will be incremented every time the read line contains only "==PID==". Then we know we get to a new information block.
# Since there are two lines with only the PID between the blocks, there will be jumps of 2 in the counter between the leak files.

knownMd5Sums=()
# knownMd5Sums is an array that contains all the unique md5sums of the individual entries in the logs with long header.

knownMd5Sums_noHeader=()
# knownMd5Sums_noHeader is an array that contains all the unique md5sums of the individual entries in the logs with short header.

tmpRes=0
# Global used by elemInArray() function. It set to 1 in case of match, but reset to 0 when beginning the execution of the method.

elemInArray(){
# $1 is the element to be searched for.
# $2 is name of the array
    arrayName=$2
    tmpRes=0
    for elem in $(eval echo \${$arrayName[@]}); do
        if [[ "$1" == "$elem" ]]; then
            tmpRes=1
            return
        fi
    done
}

fileName=`echo $0 | cut -d/ -f2`

for file in `ls | grep -v $fileName`; do
    echo "Analysing $file"
    internalLineCounter=0
    latestLeakCounts=($internalLineCounter $internalLineCounter $internalLineCounter)
# latestLeakCounts is an array that holds the latest two values of leakFileCounter, updated after each line read
# if first two elements are equal and the third differs, we know that we have a new leak file and we can analyze the previous
    sed -n '/HEAP SUMMARY/,/LEAK SUMMARY/p' $file > tmpfile.txt
    noOfLines=`wc -l tmpfile.txt | awk '{print $1}'`
    if [[ "$noOfLines" == "0" ]]; then
        echo "WARNING: file $file did not contain any LEAK SUMMARY"
    fi
    pid=`head -1 tmpfile.txt | awk -F "==" '{print $2}'`

    while read line
    do
        if [[ "$line" == "==$pid==" ]]; then
            # line is equal to pid. We do not write to any file
            leakFileCounter=`expr "$leakFileCounter" + 1`
            internalLineCounter=`expr "$internalLineCounter" + 1`
        else
            if [ $internalLineCounter -gt 1 ]; then
                if [[ `echo "$line" | grep "0x"` == "" ]]; then
                    # This is the header of the block
                    echo "$line" | awk '{for (i=2; i<NF; i++) printf $i " "; print $NF }' | awk -F "in loss record" '{print $1}' >> leak$leakFileCounter.txt
                    echo "$line" | awk '{for (i=2; i<NF; i++) printf $i " "; print $NF }' | awk -F "in loss record" '{print $1}' | awk -F "blocks are" '{print $2}' >> no_header_leak$leakFileCounter.txt
                else
                    # This is the content of the block
                    echo "$line" | awk '{for (i=4; i<NF; i++) printf $i " "; print $NF }' >> leak$leakFileCounter.txt
                    echo "$line" | awk '{for (i=4; i<NF; i++) printf $i " "; print $NF }' >> no_header_leak$leakFileCounter.txt
                fi
            fi
        fi
        # shift elements
        # we will execute the md5sum command after we detect a new file, but the two lines before have to belong to the same (previous) file
        latestLeakCounts[0]=${latestLeakCounts[1]}
        latestLeakCounts[1]=${latestLeakCounts[2]}
        latestLeakCounts[2]=$internalLineCounter
        if [[ ${latestLeakCounts[0]} == ${latestLeakCounts[1]} ]]; then
            if [[ ${latestLeakCounts[1]} != ${latestLeakCounts[2]} ]]; then
                latestCompletedFileCounter=`expr "$leakFileCounter" - 1`
                if [ -f leak$latestCompletedFileCounter.txt ]; then
                    mdSum=`md5sum leak$latestCompletedFileCounter.txt | awk '{print $1}'`
                    elemInArray $mdSum knownMd5Sums
                    if [[ $tmpRes == 1 ]]; then
                        rm -f leak$latestCompletedFileCounter.txt
                    else
                        knownMd5Sums+=($mdSum)
                    fi
                fi
                if [ -f no_header_leak$latestCompletedFileCounter.txt ]; then
                    mdSum=`md5sum no_header_leak$latestCompletedFileCounter.txt | awk '{print $1}'`
                    elemInArray $mdSum knownMd5Sums_noHeader
                    if [[ $tmpRes == 1 ]]; then
                        rm -f no_header_leak$latestCompletedFileCounter.txt
                    else
                        knownMd5Sums_noHeader+=($mdSum)
                        cp no_header_leak$latestCompletedFileCounter.txt $mdSum
                    fi
                fi
            fi
        fi
    done<tmpfile.txt

    # Here we know we finished writing to the last leak file taken from tmpfile.txt
    latestCompletedFileCounter=`expr "$leakFileCounter"`
    if [ -f leak$latestCompletedFileCounter.txt ]; then
        mdSum=`md5sum leak$latestCompletedFileCounter.txt | awk '{print $1}'`
        elemInArray $mdSum knownMd5Sums
        if [[ $tmpRes == 1 ]]; then
            rm -f leak$latestCompletedFileCounter.txt
        else
            knownMd5Sums+=($mdSum)
        fi
    fi
    if [ -f no_header_leak$latestCompletedFileCounter.txt ]; then
        mdSum=`md5sum no_header_leak$latestCompletedFileCounter.txt | awk '{print $1}'`
        elemInArray $mdSum knownMd5Sums_noHeader
        if [[ $tmpRes == 1 ]]; then
            rm -f no_header_leak$latestCompletedFileCounter.txt
        else
            knownMd5Sums_noHeader+=($mdSum)
        fi
    fi
done

rm -f tmpfile.txt
for file in `find . -name "no_header*.txt"`; do echo ""; echo "$file"; echo ""; cat $file; done > reportShortHeader.txt
for file in `find . -name "leak*.txt"`; do echo ""; echo "$file"; echo ""; cat $file; done > reportLongHeader.txt
