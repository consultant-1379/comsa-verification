#! /bin/sh
##
## Copyright (c) Ericsson AB, 2012.
##
## All Rights Reserved. Reproduction in whole or in part is prohibited
## without the written consent of the copyright owner.
##
## ERICSSON MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
## SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
## BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. ERICSSON
## SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY LICENSEE AS A
## RESULT OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS
## DERIVATIVES.
##
##

# This script is executed when storing operation is performed on the node.
# This script is used to persist the data, transfer the data from the temporarily file (/tmp/char) to the persistent storage(home/tspsaf)

MEAS_HOME_DIR="/home/tspsaf/measPersis"
MEAS_HOME_FILE="${MEAS_HOME_DIR}/measData.dat"
MEAS_TMP_FILE="/tmp/char/measData.dat"


print_usage () {
    echo "Invalid command: $0 $*"
    echo $"Usage: $0 {create | store } $2 {CMW tag} $3 {HW} $4 {VIP} $5 {LOTC}"

}


createNew () {

    # Create the directory if it does not exist
    if [[ ! -f ${MEAS_HOME_FILE} ]]; then

	    # Add the heading
		echo "TC-tag;TC-name;value(unit);CMW-tag;LOTC-version;VIP-version;HW;NrOfNodes;Date" > ${MEAS_HOME_FILE}
		cat ${MEAS_TMP_FILE} | grep  $2 | grep $3 | grep $4 | grep $5 >>  ${MEAS_HOME_FILE}
		chmod 777 ${MEAS_HOME_FILE}
	else
	   echo "File ${MEAS_HOME_FILE} already exist"
       exit 1
    fi

}

storeData () {
    
	if [[ -f ${MEAS_HOME_FILE} ]]; then
	   cat ${MEAS_TMP_FILE} | grep $2 | grep $3 | grep $4 | grep $5 >>  ${MEAS_HOME_FILE}
	else
	   echo "File ${MEAS_HOME_FILE} not exist"
       exit 1
	fi
}



case "$1" in
    create)
        if [ "$#" = 5 ]; then

            createNew $@

        else
            print_usage
            exit 1
        fi
        ;;

    store)
        if [ "$#" = 5 ]; then
            storeData $@
        else
            print_usage
            exit 1
        fi
        ;;
    
    *)
        print_usage
        exit 1

esac

exit 0
