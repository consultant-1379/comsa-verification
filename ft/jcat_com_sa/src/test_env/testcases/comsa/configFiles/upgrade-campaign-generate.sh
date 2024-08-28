#!/bin/bash
#
# A script to generate COMSA upgrade campaign from ETF.xml file from the COMSA CXP Bundle
# and ImmConfig.xml using the DX AMF CGS tool
#
# The script expects the ETF.xml file from the COMSA CXP bundle to be in the current directory
# and all the other files to be included in the campaign SDP (excluding campaign*.xml) to be
# in a sub-directory 'upgrade_campaign'
#
################################################################################################



#
# get the R_STATE from the ETF
#
COMSA_NEW_R_STATE=`grep 'ERIC-ComSa-CXP9017697_' ETF.xml | awk 'NR==1 {print $2}' | sed 's/"//g' | awk -F'-' '{print $NF}'`
COMSA_VER=`grep 'ERIC-ComSa-CXP9017697_' ETF.xml | awk 'NR==1 {print $2}' | awk -F'-' '{print $(NF-1)}' | cut -d'_' -f2`
if grep 'safCompType=ERIC-ComSa-sshd' ETF.xml > /dev/null; then
    echo "COMSA already support SSHD"
    COMSA_OLD_R_STATE=`grep 'swRemove bundleDN' campaign.template.xml | awk '{print $2}' | sed 's/bundleDN="safSmfBundle=ERIC-ComSa-CXP9017697_${COMSA_VER}-/ /' | awk '{print $1}' | sed 's/"/ /' | awk '{print $1}'`
else
    COMSA_OLD_R_STATE=`grep 'swRemove bundleDN' campaign.xml | awk '{print $2}' | sed 's/bundleDN="safSmfBundle=ERIC-ComSa-CXP9017697_3-/ /' | awk '{print $1}' | sed 's/"/ /' | awk '{print $1}'`
fi
#
# Determine the number of SC in the cluster
#
#NUM_SC=`grep node /cluster/etc/cluster.conf | grep control | wc -l`
NUM_SC=`grep node /cluster/etc/cluster.conf | grep control | grep -v \# | wc -l`

#
#Export ImmConfig.xml
#
cmw-immconfig-export IMMConfig.xml
sed -i '/SA_NO_DANGLING/d' ./IMMConfig.xml

#
#Generate Upgrade campaign with input ETF.xml and IMMConfig.xml
#
amf-cgs --command upgradecampaign --input ./IMMConfig.xml ./ETF.xml "ERIC-ComSa-upgrade"


#
# Add the following <procInitAction> steps to upgradeProcedure
#
amf-cgs --command addprocinitaction --input safSmfProc=RollingUpgrade "cmw-partial-backup-unregister ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_OLD_R_STATE} backup_comsa" "/bin/false " SC-1 --file Upgrade_Campaign.uc

if [ $COMSA_VER < 4 ] ; then
    amf-cgs --command addprocinitaction --input safSmfProc=RollingUpgrade "\$OSAFCAMPAIGNROOT/updateME delete" "/bin/false " SC-1 --file Upgrade_Campaign.ucfi
amf-cgs --command addprocinitaction --input safSmfProc=RollingUpgrade "\$OSAFCAMPAIGNROOT/model_update ComImm ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_NEW_R_STATE} ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_OLD_R_STATE}" "/bin/false " SC-1 --file Upgrade_Campaign.uc

if [ $COMSA_VER < 4 ] ; then
    amf-cgs --command addprocinitaction --input safSmfProc=RollingUpgrade "\$OSAFCAMPAIGNROOT/updateME deleteObj" "/bin/false " SC-1 --file Upgrade_Campaign.uc
    amf-cgs --command addprocinitaction --input safSmfProc=RollingUpgrade "\$OSAFCAMPAIGNROOT/updateME add" "/bin/false " SC-1 --file Upgrade_Campaign.uc
fi
amf-cgs --command addprocinitaction --input safSmfProc=RollingUpgrade "\$OSAFCAMPAIGNROOT/model_update comsaupdate ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_NEW_R_STATE} ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_OLD_R_STATE}" "/bin/false " SC-1 --file Upgrade_Campaign.uc
amf-cgs --command addcampaignaction --input 2 "\$OSAFCAMPAIGNROOT/model_update cmwbackup ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_NEW_R_STATE} " "/bin/false" SC-1 --file Upgrade_Campaign.uc
amf-cgs --command addcampaignaction --input 2 "\$OSAFCAMPAIGNROOT/model_update remove ERIC-ComSa-CXP9017697_${COMSA_VER}-${COMSA_OLD_R_STATE}" "/bin/false" SC-1 --file Upgrade_Campaign.uc

if [[ 'grep 'safCompType=ERIC-ComSa-sshd' ETF.xml' ]]; then
    sed -i '/type\//d' ./Upgrade_Campaign.xml
    cp Upgrade_Campaign.xml upgrade_campaign/campaign.template.xml
else
    cp Upgrade_Campaign.xml upgrade_campaign/campaign.xml
fi

#tar upgrade_camapign
ls -l upgrade_campaign
cd upgrade_campaign
tar zcfv comsa_upgrade.sdp *
