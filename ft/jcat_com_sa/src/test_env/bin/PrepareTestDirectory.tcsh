#! /bin/tcsh
#
if ( $#argv < 4 || $#argv > 6 ) then
 echo "Usage: <targetDir> <COM_version> <CoewMW_version> <COMSA_Builddate> [node_type] [distro_type]"
 echo "Example: my_signum_dir '3.4/sh12' '3.4/sh6' 'release_folder or absolute path to folder'"
 echo "NOTE! nodetype 1 = two nodes, nodetype 2 = One node"
 echo "Distro Type: sles or rhel. Default: sles"
 exit 1
endif
if ( ${%6} != 0) then
  if ( $6[:1] == "/" ) then
    set COMSA_DIR="$6"
  else
    set COMSA_DIR="/home/comsaci/releases/$6"
  endif
endif

set TARGETDIR="/home/jenkinuser/release/install/$1"
echo "TARGETDIR:$TARGETDIR"
set COM_DIR="$2"
echo "COM_DIR:$COM_DIR"
set COREMW_DIR="$3"
echo "COREMW_DIR:$COREMW_DIR"
if ( -d $4 ) then
  set COMSA_DIR="$4"
else
  set COMSA_DIR="/home/comsaci/releases/$4"
endif
echo "COMSA_DIR:$COMSA_DIR"
if ($# == 4) then
  set NODE_TYPE="1"
  set DISTRO_TYPE="sles"
else
  set NODE_TYPE="$5"
endif
echo "NODE_TYPE:$NODE_TYPE"

if ($# == 5) then
  set DISTRO_TYPE="sles"
else
  set DISTRO_TYPE="$6"
endif
echo "DISTRO_TYPE:$DISTRO_TYPE"

echo "Preparing the environment"
echo "Creating the test base directory"
mkdir -p $TARGETDIR
\rm -fR $TARGETDIR/*
mkdir $TARGETDIR/com
mkdir $TARGETDIR/comsa
mkdir $TARGETDIR/coremw

echo "Copying CoreMW from /home/comsaci/neighbors/coremw/$COREMW_DIR"
\cp /home/comsaci/neighbors/coremw/$COREMW_DIR/*CXP9020355*.tar $TARGETDIR/coremw/
ls $TARGETDIR/coremw/

echo "Copy COM from /home/comsaci/neighbors/com/$COM_DIR"
if ($DISTRO_TYPE == "sles") then
  tar xf /home/comsaci/neighbors/com/$COM_DIR/*CXP9017585*.tar -C $TARGETDIR/com/
  mkdir $TARGETDIR/com/tmp
  tar -zxf /home/comsaci/neighbors/com/$COM_DIR/*CXP9017586*.tar.gz -C $TARGETDIR/com/tmp/
  \mv -f $TARGETDIR/com/tmp/ERIC-COM-I${NODE_TYPE}-TEMPLATE-CXP9017585*/*.sdp $TARGETDIR/com/
  \rm -fR $TARGETDIR/com/tmp
  ls $TARGETDIR/com/
else
  # rhel
  tar xf /home/comsaci/neighbors/com/$COM_DIR/*CXP9026454*.tar -C $TARGETDIR/com/
  mkdir $TARGETDIR/com/tmp
  tar -zxf /home/comsaci/neighbors/com/$COM_DIR/*CXP9026455*.tar.gz -C $TARGETDIR/com/tmp/
  \mv -f $TARGETDIR/com/tmp/ERIC-COM-I${NODE_TYPE}-TEMPLATE-CXP9026454*/*.sdp $TARGETDIR/com/
  \rm -fR $TARGETDIR/com/tmp
  ls $TARGETDIR/com/
endif

echo "Copy COM SA from $COMSA_DIR"
if ($DISTRO_TYPE == "sles") then
  tar xf $COMSA_DIR/*CXP9018914*.tar -C $TARGETDIR/comsa/
  mkdir $TARGETDIR/comsa/tmp
  tar -zxf $COMSA_DIR/*CXP9017695*.tar.gz -C $TARGETDIR/comsa/tmp/
  \mv -f $TARGETDIR/comsa/tmp/COM_SA_I${NODE_TYPE}_TEMPLATE-CXP9018914*/*.sdp $TARGETDIR/comsa/
  \mv -f $TARGETDIR/comsa/tmp/COM_SA_R${NODE_TYPE}_TEMPLATE-CXP9018914*/*.sdp $TARGETDIR/comsa/
  \cp $COMSA_DIR/*CXP9017695*.tar.gz $TARGETDIR/comsa/
  \cp $COMSA_DIR/*CXP9018914*.tar $TARGETDIR/comsa/
  \rm -fR $TARGETDIR/comsa/tmp
  ls $TARGETDIR/comsa/
else
  # rhel
  tar xf $COMSA_DIR/*CXP9028074*.tar -C $TARGETDIR/comsa/
  mkdir $TARGETDIR/comsa/tmp
  tar -zxf $COMSA_DIR/*CXP9028075*.tar.gz -C $TARGETDIR/comsa/tmp/
  \mv -f $TARGETDIR/comsa/tmp/COM_SA_I${NODE_TYPE}_TEMPLATE-CXP9028074*/*.sdp $TARGETDIR/comsa/
  \mv -f $TARGETDIR/comsa/tmp/COM_SA_R${NODE_TYPE}_TEMPLATE-CXP9028074*/*.sdp $TARGETDIR/comsa/
  \cp $COMSA_DIR/*CXP9028075*.tar.gz $TARGETDIR/comsa/
  \cp $COMSA_DIR/*CXP9028074*.tar $TARGETDIR/comsa/
  \rm -fR $TARGETDIR/comsa/tmp
  ls $TARGETDIR/comsa/
endif

echo "Test environment setup complete"
