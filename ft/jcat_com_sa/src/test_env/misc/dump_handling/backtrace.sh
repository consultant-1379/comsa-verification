#! /bin/bash

CMDFILE=`dirname $0`/gdbcmd

echo bt >  $CMDFILE
echo "set print pretty on" >> $CMDFILE
echo "bt full" >> $CMDFILE
echo q  >> $CMDFILE

if [ ! -r "$1" ]; then
  echo "No core dump!"
  exit 1
fi

DUMP=$1

FILE=`echo $DUMP | sed 's/.*\///' | sed 's/\.[0-9]*\.[^.]*\.core//'`
EXEC=""

if `which $FILE > /dev/null 2>&1`; then
  EXEC=`which $FILE 2>/dev/null`
elif [ "$FILE" = "com" ]; then
  EXEC='/opt/com/bin/com'
else
  res=$(echo $FILE | grep "ta_")
  if [ $? -eq 0 ]; then
    for EXEC in `find /opt/ -name $FILE`; do
      if [ -x $EXEC ]; then
        break
      fi
    done
  else
    for EXEC in `find /usr/ -name $FILE`; do
      if [ -x $EXEC ]; then
        break
      fi
    done
  fi
fi

if [ "x$EXEC" = "x" ]; then
  echo "No exec found for $DUMP"
  exit 1
fi

echo "$DUMP ($EXEC)"
#gdb $EXEC $DUMP --command=$CMDFILE 2> /dev/null | sed -n '/#[0-9]/ p' 2> /dev/null
# get full information of backtrace
gdb $EXEC $DUMP --command=$CMDFILE 2> /dev/null
