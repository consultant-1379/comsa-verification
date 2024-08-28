#!/bin/bash
rpm_test=`rpm -qa | grep -e ComSa -e comsa | awk '{print $1}'`
if [[ $rpm_test ]] ; then
   echo "remove RPM"
   echo "$rpm_test"
   rpm -e $rpm_test
fi
