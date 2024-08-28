#!/bin/bash

# File: backup_rpms.sh
# This script is used to backup and/or restore the rpms on the cluster.
# Should be only used with cmw-partial-backup-* --no-hostdata commands.
# Usage:
# backup_rpms.sh <option> backup_name
# Options
# -c|--create        : Create backup
# -r|--restore       : Restore backup
# -p|--path <path>   : Absolute path for storing backup
#                      Default is: /home/backup_rpms

PREFIX="rpms_"
BACKUP_NAME=
BACKUP_PATH="/home/backup_rpms"
CREATE_BACKUP=

print_usage(){
    echo "
 Usage:
 backup_rpms.sh <options> backup_name
 Options
    -c|--create        : Create backup
    -r|--restore       : Restore backup
    -p|--path <path>   : Absolute path for storing backup
                         Default is: /home/backup_rpms
"
}

die(){
    echo "ERROR backup_rpms.sh: $@" >&2
    exit 1
}

if [[ -z $1 ]]; then
    print_usage
    exit 0
fi

while [ "$1" ]; do
    case $1 in
        -h|--help)
        print_usage
        exit 0
        ;;

        -c|--create)
        if [[ -z $CREATE_BACKUP ]]; then
            CREATE_BACKUP="1"
        else
            print_usage
            die "Unknown parameter \"$1\", see help."
        fi
        ;;

        -r|--restore)
        if [[ -z $CREATE_BACKUP ]]; then
            CREATE_BACKUP="0"
        else
            print_usage
            die "Unknown parameter \"$1\", see help."
        fi
        ;;
        
        -p|--path)
        BACKUP_PATH=$2
        shift
        ;;

        *)
        if [[ -z $BACKUP_NAME ]]; then
            BACKUP_NAME=$1
        else
            print_usage
            die "Unknown parameter \"$1\", see help."
        fi
        ;;

    esac
    shift
done

if [[ -z $CREATE_BACKUP ]]; then
    print_usage
    die "Please specify which action to perform: create or restore backup \"$1\", see help."
fi
if [[ -z $BACKUP_NAME ]]; then
    print_usage
    die "Please specify backup name \"$1\", see help."
fi
if [[ ! -d $BACKUP_PATH ]]; then
    mkdir -p $BACKUP_PATH
fi

create_backup(){
    BACKUP_FULL_NAME="${BACKUP_PATH}/${PREFIX}${BACKUP_NAME}.tar.gz"
    if [[ -e $BACKUP_FULL_NAME ]]; then
        rm -rf $BACKUP_FULL_NAME
    fi
    FILES="`find /cluster/rpms | grep "\.rpm" | grep -iv linux-` `find /cluster/nodes/*/etc/rpm.conf`"
    tar czfP $BACKUP_FULL_NAME $FILES || die "create_backup failed"
    echo "Backup $BACKUP_FULL_NAME created succesfully!"
}

restore_backup(){
    BACKUP_FULL_NAME="${BACKUP_PATH}/${PREFIX}${BACKUP_NAME}.tar.gz"
    if [[ ! -e $BACKUP_FULL_NAME ]]; then
        die "restore_backup failed. Can't find backup file!"
    fi
    rm -rf `find /cluster/rpms | grep "\.rpm" | grep -iv linux-`
    tar xvfP $BACKUP_FULL_NAME || die "restore_backup failed"
    echo "Backup $BACKUP_FULL_NAME restored succesfully!"
}

if [[ $CREATE_BACKUP == "1" ]]; then
    create_backup
else
    restore_backup
fi