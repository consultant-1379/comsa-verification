#!/bin/bash
#
# A script to generate COMSA installation campaign from ETF.xml file from the COMSA CXP Bundle
# using the DX AMF CGS tool
#
# The script expects the ETF.xml file from the COMSA CXP bundle to be in the current directory
# and all the other files to be included in the campaign SDP (excluding campaign*.xml) to be
# in a sub-directory 'install_campaign'
#
################################################################################################

#
# get the R_STATE from the ETF
#
COMSA_R_STATE=`grep 'ERIC-ComSa-CXP9017697_' ETF.xml | awk 'NR==1 {print $2}' | sed 's/"//g' | awk -F'-' '{print $NF}'`
COMSA_VER=`grep 'ERIC-ComSa-CXP9017697_' ETF.xml | awk 'NR==1 {print $2}' | awk -F'-' '{print $(NF-1)}' | cut -d'_' -f2`

#
# Determine the number of SC in the cluster
#
NUM_SC=`grep node /cluster/etc/cluster.conf | grep control | wc -l`
# NUM_PL=`grep node /cluster/etc/cluster.conf | grep payload | wc -l`

#
# Create UI file. Define SGs, SI Template, CSI Templates.
#
# amf-cgs -command createui -file ETF.xml --input 2 2 # 2+2 cluster
# amf-cgs --command createui -file ETF.xml --input 1 0 # Single node cluster
# amf-cgs --command createui -file ETF.xml --input $NUM_SC $NUM_PL
if [ ${NUM_SC} == 2 ]
then
    amf-cgs --command createui -file ETF.xml --input 2 0
else
    amf-cgs --command createui -file ETF.xml --input 1 0
fi
#
#
#
if [ ${NUM_SC} == 2 ]
then
    amf-cgs --command addservicegroup --input ERIC-ComSa-2N SA_AMF_2N_REDUNDANCY_MODEL AllNodes 1 1 0 --file ./ETF.ui
else
    amf-cgs --command addservicegroup --input ERIC-ComSa-2N SA_AMF_2N_REDUNDANCY_MODEL AllNodes 1 0 0 --file ./ETF.ui
fi
amf-cgs --command addsitemplate --input ERIC-ComSa-2N ERIC-ComSa-2N safSvcType=ERIC-ComSa-2N 1 0 1 --file ETF.ui
amf-cgs --command addcsitemplates --input ERIC-ComSa-2N ERIC-ComSa-2N  ERIC-ComSa-2N safCSType=ERIC-ComSa-2N 1 --file ETF.ui

#
# Generate AC (AMF Config) file from UI file.
#
amf-cgs --command generate --file ETF.ui
#cp null/configuration0.ac .

#
# Generate Install campaign from AC file.
#
amf-cgs --command generate --file configuration0.ac --input "ERIC-ComSaInstall"
#cp null/Installation_Campaign.* .

#
# Add the following <procInitAction> steps to upgradeProcedure
#

amf-cgs --command addprocinitaction --input safSmfProc=SingleStepProc1 "\$OSAFCAMPAIGNROOT/comsa_pso ComImm ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_R_STATE}" "/bin/false " SC-1 --file Installation_Campaign.uc
# COM SA MR42277 Remove old interfaces exposed to COM & CoreMW - Don't need to add following actions to campaign
if [ $COMSA_VER -lt 4 ]
then
    amf-cgs --command addprocinitaction --input safSmfProc=SingleStepProc1 "\$OSAFCAMPAIGNROOT/comsa_pso CmwFm ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_R_STATE}" "/bin/false " SC-1 --file Installation_Campaign.uc
    amf-cgs --command addprocinitaction --input safSmfProc=SingleStepProc1 "\$OSAFCAMPAIGNROOT/comsa_pso CmwCom ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_R_STATE}" "/bin/false " SC-1 --file Installation_Campaign.uc
    amf-cgs --command addprocinitaction --input safSmfProc=SingleStepProc1 "\$OSAFCAMPAIGNROOT/comsa-mim-tool commit" "/bin/false " SC-1 --file Installation_Campaign.uc
fi
amf-cgs --command addprocinitaction --input safSmfProc=SingleStepProc1 "/opt/com/bin/com_mim_tool --modelHandler=MW_OAM --managedObjectVersion=3 --transactionalResourceVersion=1" "/bin/false " SC-1 --file Installation_Campaign.uc
amf-cgs --command addprocinitaction --input safSmfProc=SingleStepProc1 "\$OSAFCAMPAIGNROOT/comsa_pso install" "/bin/false " SC-1 --file Installation_Campaign.uc

# mkdir install_campaign
cp Installation_Campaign.xml install_campaign/campaign.xml
ls -l install_campaign
cd install_campaign

if [ ${NUM_SC} == 2 ]
then
    tar zcfv ComSa_install.sdp *
else
    tar zcfv ComSa_install_Single.sdp *
fi
