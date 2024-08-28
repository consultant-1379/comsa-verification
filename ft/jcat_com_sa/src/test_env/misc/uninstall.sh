#!/bin/sh

die() {
    #logger -s -t CMW -p user.err "$prg: ERROR: $@"
    echo "Error: $1. Exiting!"
    exit 1
}

remove_rpms () {
    local sdpdir=$1
    local nodeid=$2
    local host=`cmwea hostname-get 1,1,${nodeid}`
    echo "Entering for host $nodeid = $host"
    
    local rpmname

    for file in `ls ${sdpdir}/rpms/*.rpm 2>/dev/null`
      do
      rpmfile=`basename $file`
      test -n "$debug" || echo "rpmfile: $rpmfile"
      rpmname=`grep ^${rpmfile}: ${sdpdir}/rpms/rpm.list | sed "s/^${rpmfile}://"`
      test -n "$debug" || echo "rpmname: $rpmname"
      test -n "${rpmname}" || continue
      cmwea rpm-config-delete $rpmname $host || die "Failed to remove $rpmname on $host"
      test -n "$debug" || echo "Successful delete of $rpmname on $host"
    done
    if [ $nodeid -le 2 ]
	then
	for file in `ls ${sdpdir}/rpms/control/*.rpm 2>/dev/null`
	  do
	  rpmfile=`basename $file`
	  test -n "$debug" || echo "rpmfile: $rpmfile"
	  rpmname=`grep ^${rpmfile}: ${sdpdir}/rpms/rpm.list | sed "s/^${rpmfile}://"`
	  test -n "$debug" || echo "rpmname: $rpmname"
	  test -n "${rpmname}" || continue
	  cmwea rpm-config-delete $rpmname $host || die "Failed to remove $rpmname on $host"
	  test -n "$debug" || echo "Successful delete of $rpmname on $host"
	done
    else
	for file in `ls ${sdpdir}/rpms/payload/*.rpm 2>/dev/null`
	  do
	  rpmfile=`basename $file`
	  test -n "$debug" || echo "rpmfile: $rpmfile"
      	  rpmname=`grep ^${rpmfile}: ${sdpdir}/rpms/rpm.list | sed "s/^${rpmfile}://"`
	  test -n "${rpmname}" || continue
	  test -n "$debug" || echo "rpmname: $rpmname"
	  cmwea rpm-config-delete $rpmname $host || die "Failed to remove $rpmname on $host"
	  test -n "$debug" || echo "Successful delete of $rpmname on $host"
	done
    fi
    

}   

debug=""
if [ "-v" = "$1" ] ; then
    debug="true"
fi

MAX_NODE_ID=`cmwea tipcaddress-get --max | sed 's/.*,.*,//'`
CMW_HOME_DIR="`cmwea software-location-get`/coremw"

for (( i=$MAX_NODE_ID; i >= 1; i-- )) ; do
    host=`cmwea hostname-get 1,1,${i}`
    cmwea initscript-execute $host opensafd stop
    for sdp in `ls ${CMW_HOME_DIR}/repository/`
      do
      remove_rpms ${CMW_HOME_DIR}/repository/${sdp} $i
    done
    cmwea rpm-config-activate $host 
    ssh $host \rm -Rf /etc/opensaf /usr/share/opensaf /opt/coremw
done

for d in `cmwea software-location-get`/coremw `cmwea clear-location-get`/coremw `cmwea config-location-get`/coremw `cmwea no-backup-location-get`/coremw `cmwea storage-location-get`/coremw `cmwea storage-location-get`/coremw_appdata; do
    if [ -d $d ] ; then
	\rm -rf $d
    fi
done

