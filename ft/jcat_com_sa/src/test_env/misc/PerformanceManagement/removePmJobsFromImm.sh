#!/bin/sh

for i in `immfind | grep "^pmJobId="` ; do
    immcfg -a requestedJobState=2 $i 2>/dev/null
done

for i in `immfind | grep "^safJob="` ; do
    immadm -o 2 $i 2>/dev/null
done


for j in pmJobId pmThresholdMonitoringId measurementReaderId measurementTypeId pmGroupId safThresHold safJobMT safMT safMeasObjClass safJob ; do
    echo $j
    for i in `immfind | grep "^$j="` ; do
        immcfg -d "$i"
    done
done

exit 0
