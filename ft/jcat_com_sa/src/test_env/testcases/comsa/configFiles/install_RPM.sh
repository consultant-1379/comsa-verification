#!/bin/bash
rpm -ivh --nodeps $1
rpm_test=`rpm -qa | grep -e ComSa -e comsa | awk '{print $1}'`
if [[ $rpm_test ]] ; then
   echo "The RPM of COM SA installed SUCCESS "
   exit 0
else
   echo "The RPM of COM SA installed FAILED"
   exit 1
fi
