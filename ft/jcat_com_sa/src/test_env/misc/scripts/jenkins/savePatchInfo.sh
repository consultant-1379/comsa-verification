#!/bin/bash

myStream=$1
changeset=$(which_changeset | head -n 1)
recBaseLine=$(cleartool desc stream:$myStream@/vobs/coremw/pvob | grep -A1 "recommended baselines" | tail -n 1)
echo "$changeset. $recBaseLine."
