#!/bin/bash
collect_cov_results_into_final_location()
{
    path_of_cov_files=`ls $userhome | grep cov_comsa`
    mkdir -p $final_cov_path
    #Copy ft coverage result to final path
    for ix in $path_of_cov_files
    do
        echo Getting path at $ix
        #Pick up cov info and copy to final destination
        cp ${userhome}/${ix}/${cov_ft_filename} ${final_cov_path}/${ix}_${cov_ft_filename}
    done
    #Copy ut cov result to final path
    cp ${unittest_repo}/${cov_ut_filename} ${final_cov_path}
}

combine_into_one_cov_file()
{
    cov_path_array=( `ls $final_cov_path | grep cov_comsa` )
    ${COMSA_REPO_PATH}/${lcov_tool_path}lcov --add-tracefile  ${final_cov_path}/${cov_path_array[0]} --add-tracefile ${final_cov_path}/${cov_path_array[1]}\
    --add-tracefile  ${final_cov_path}/${cov_path_array[2]} --add-tracefile ${final_cov_path}/${cov_path_array[3]} --add-tracefile /${final_cov_path}/${cov_ut_filename}\
    --output-file ${final_cov_path}/${final_combined_cov_init_file}

    echo "Removing pattern of tracefile"
    ${COMSA_REPO_PATH}/${lcov_tool_path}lcov --remove ${final_cov_path}/${final_combined_cov_init_file} $ut_pattern --output-file ${final_cov_path}/${final_combined_cov_file}
}

generate_cov_file_to_html_format()
{
    ${COMSA_REPO_PATH}/${lcov_tool_path}genhtml ${final_cov_path}/$1 --output-directory ${final_cov_path}/$2
}

remove_old_data()
{
    #Remove obsolete folders and files
    echo "Removing old files"
    rm -rf $final_cov_path
    rm -rf $userhome/cov_comsa*
}

read_option()
{
    echo -n "Enter your choice (timeout 30s): "
    read -t 30 choice
    if [ "$choice" == "1" ]; then
        return 0
    elif [ "$choice" == "2" ]; then
        return 1
    elif [ "$choice" == "3" ]; then
        return 2
    else
        return 0
    fi
}

usage_help()
{
    echo "Usage:"
    echo "./run4CovRegTestSuites --config [x] --sc [x] --pl [x] --productSettings [x] --swDirNumber [x] --installSw [x] --loglevel [x] --checkCompilerWarn [x]"
    echo "Or"
    echo "./run4CovRegTestSuites --config [x] [x] [x] [x] --sc [x] --pl [x] --productSettings [x] --swDirNumber [x] --installSw [x] --loglevel [x] --checkCompilerWarn [x]"
    exit 1
}

run_cov_in_sequence()
{
    echo "Running coverage suite in sequence"
    build_and_copy_cov_comsa_sdp_to_swdir $5 $2
    executive.py --suite regTestSuite1CovInSequence.xml --config $1 --sc $2 --pl $3 --productSettings $4 --swDirNumber $5 --installSw $6 --build False --loglevel $8 --checkCompilerWarn False
    executive.py --suite regTestSuite2CovInSequence.xml --config $1 --sc $2 --pl $3 --productSettings $4 --swDirNumber $5 --installSw $6 --build False --loglevel $8 --checkCompilerWarn False
    executive.py --suite regTestSuite3CovInSequence.xml --config $1 --sc $2 --pl $3 --productSettings $4 --swDirNumber $5 --installSw $6 --build False --loglevel $8 --checkCompilerWarn False
    executive.py --suite regTestSuite4CovInSequence.xml --config $1 --sc $2 --pl $3 --productSettings $4 --swDirNumber $5 --installSw $6 --build False --loglevel $8 --checkCompilerWarn False
}

build_and_copy_cov_comsa_sdp_to_swdir()
{
    echo "Building coverage comsa:"
    comsa_src=$COMSA_REPO_PATH/src
    jenkinuser_install=/home/jenkinuser/release/install/
    build_release=$COMSA_REPO_PATH/release/
    comsa_sdp_sles="ComSa-CXP9017697_*.sdp"
    comsa_sdp_rhel="ComSa-CXP9028073_1.sdp"
    comsa_dual_install_campaign="ComSa_install.sdp"
    comsa_dual_remove_campaign="ComSa_remove.sdp"
    comsa_single_install_campaign="ComSa_install_Single.sdp"
    comsa_single_remove_campaign="ComSa_remove_Single.sdp"
    pushd $comsa_src
    make clean
    make coverage
    popd
    rm -f ${jenkinuser_install}/$1/comsa/*.sdp
    if ls ${build_release}/${comsa_sdp_sles} 1> /dev/null 2>&1; then
        cp ${build_release}/${comsa_sdp_sles} ${jenkinuser_install}/$1/comsa/
    fi
    if ls ${build_release}/${comsa_sdp_rhel} 1> /dev/null 2>&1; then
        cp ${build_release}/${comsa_sdp_rhel} ${jenkinuser_install}/$1/comsa/
    fi
    if [ "$2" == "2" ]; then
        cp  ${build_release}/${comsa_dual_install_campaign} ${jenkinuser_install}/$1/comsa/
        cp  ${build_release}/${comsa_dual_remove_campaign} ${jenkinuser_install}/$1/comsa/
    elif [ "$2" == "1" ]; then
        cp  ${build_release}/${comsa_single_install_campaign} ${jenkinuser_install}/$1/comsa/
        cp  ${build_release}/${comsa_single_remove_campaign} ${jenkinuser_install}/$1/comsa/
    fi
}

run_cov_in_paralel()
{
    tmp_log_1=/home/$USER/log_1.txt
    tmp_log_2=/home/$USER/log_2.txt
    tmp_log_3=/home/$USER/log_3.txt
    tmp_log_4=/home/$USER/log_4.txt
    if [ $# -ne 11 ]; then
        return 1
    else
        echo "Running coverage suite in parallel"
        echo "Please check output stream from /home/$USER/log_1.txt to log_4.txt"
        build_and_copy_cov_comsa_sdp_to_swdir $8 $5
        screen -d -m /bin/bash -c "executive.py --suite regTestSuite1CovInParalel.xml --config $1 --sc $5 --pl $6 --productSettings $7 --swDirNumber $8 --installSw $9 --build False --loglevel ${10}\
        --checkCompilerWarn False > $tmp_log_1 2>&1"
        screen -d -m /bin/bash -c "executive.py --suite regTestSuite2CovInParalel.xml --config $2 --sc $5 --pl $6 --productSettings $7 --swDirNumber $8 --installSw $9 --build False --loglevel ${10}\
        --checkCompilerWarn False > $tmp_log_2 2>&1"
        screen -d -m /bin/bash -c "executive.py --suite regTestSuite3CovInParalel.xml --config $3 --sc $5 --pl $6 --productSettings $7 --swDirNumber $8 --installSw $9 --build False --loglevel ${10}\
        --checkCompilerWarn False > $tmp_log_3 2>&1"
        screen -d -m /bin/bash -c "executive.py --suite regTestSuite4CovInParalel.xml --config $4 --sc $5 --pl $6 --productSettings $7 --swDirNumber $8 --installSw $9 --build False --loglevel ${10}\
        --checkCompilerWarn False > $tmp_log_4 2>&1"
        sleep 10
    fi
    return 0
}

wait_for_all_cov_suites_done()
{
    while [ 1 ];
    do
        running_status=`ps aux | grep executive | awk '{print $13}' | grep $USER`
        echo "Waiting for 4 suites completed"
        if [ ! -z "$running_status" ]; then
            echo "Sleep for 15 minutes ................."
            sleep 15m
            continue
        else
            break
        fi
    done
}

create_and_send_automatic_mail()
{
    if [ ! -e ${final_cov_path}/${html_output_dir_name}/index.html ]; then
       echo "Coverage testing has not done. Exit"
       exit 1
    fi
    log_dir=${cmw_scratch_log_path}/$(date +%d%m%Y%H%M%S)
    mkdir $log_dir
    cp -r ${final_cov_path}/${html_output_dir_name} $log_dir
    cp -r ${unittest_repo}/${html_output_ut_dir_name} $log_dir
    mail_list=( `cat $COMSA_VERIFICATION/ft/jcat_com_sa/src/test_env/testcases/comsa/configFiles/emailList.txt` )
    hostname=`hostname`
    if [ -n `hostname | grep cbaserv` ]; then
        logfile_link_1="file://${hostname}.dek-tpc.internal/${log_dir}/${html_output_dir_name}/index.html"
        ut_logfile_link="file://${hostname}.dek-tpc.internal/${log_dir}/${html_output_ut_dir_name}/index.html"
    else
        logfile_link_1="https://cc-userarea.rnd.ki.sw.ericsson.se/${log_dir}/${html_output_dir_name}/index.html"
        ut_logfile_link="https://cc-userarea.rnd.ki.sw.ericsson.se/${log_dir}/${html_output_ut_dir_name}/index.html"
    fi
    logfile_link_2="file://${log_dir}/${html_output_dir_name}/index.html"
    if [ $sc_num == "2" ]; then
        target_name="$cluster_config_1 $cluster_config_2 $cluster_config_3 $cluster_config_4 - Dual Node"
    else
        target_name="$cluster_config_1 $cluster_config_2 $cluster_config_3 $cluster_config_4 - Single Node"
    fi
    for mail_address in ${mail_list[@]}
    do
        mail_subject="Final coverage result by ($USER) FINISHED"
        cat <<EOF | mail -s "$mail_subject" "$mail_address"

This is an automatic mail generated by an automated test run.
You received this mail, because your are in the following email list:
Host name is: $hostname
Target name: $target_name

Link of the final coverage result:
$logfile_link_1
$ut_logfile_link

$logfile_link_2
EOF
    done
}

lcov_tool_path=tools/lcov/1.10-5.4/usr/bin/
gcov_tool=coremw-tools/LSB_BUILD_ENV/compilers/x86_64-dx/bin/x86_64-dx-linux-gnu-gcov

final_combined_cov_init_file=final_combined_ft_cov_init.info
final_combined_cov_file=final_combined_ft_cov.info
cov_ft_filename=comsa_ft_new_cov.info
cov_ut_filename=comsa_ut_cov.info
html_output_dir_name=final_ft_combined_html
html_output_ut_dir_name=html_ut

userhome=/home/$USER
final_cov_path=/home/$USER/final_cov/
cov_file_location=/home/$USER/COV_COMSA/
unittest_repo=$COMSA_REPO_PATH/src/com_specific/unittest/
cmw_scratch_log_path=/proj/coremw_scratch/$USER/

ut_pattern='*4.8.1/* *unittest/* *dependencies/*'
cluster_config_1=""
cluster_config_2=""
cluster_config_3=""
cluster_config_4=""
sc_num=""
pl_num=""
product_settings="comsa"
sw_directory=""
sw_install="False"
sw_build="False"
log_level="INFO"
check_compilerWarn="True"
######################################################################################
# To run script with parameters as example below
#./run4CovRegTestSuites --config qemu_target_01 --sc [x] --pl [x] --productSettings comsa --swDirNumber [x] --installSw True --build False --loglevel DEBUG
#
######################################################################################

for i in ${1+"$@"}
do
    if [ "$i" == "--config" ]; then
        cluster_config_1="Set"
        cluster_config_2="Set"
        cluster_config_3="Set"
        cluster_config_4="Set"
    elif [ "$i" == "--sc" ]; then
        sc_num="Set"
        if [ "$cluster_config_2" == "Set" ] || [ "$cluster_config_3" == "Set" ] || [ "$cluster_config_4" == "Set" ]; then
            cluster_config_2=""
            cluster_config_3=""
            cluster_config_4=""
        fi
    elif [ "$i" == "--pl" ]; then
        pl_num="Set"
    elif [ "$i" == "--productSettings" ]; then
        product_settings="Set"
    elif [ "$i" == "--swDirNumber" ]; then
        sw_directory="Set"
    elif [ "$i" == "--installSw" ]; then
        sw_install="Set"
    elif [ "$i" == "--build" ]; then
        sw_build="Set"
    elif [ "$i" == "--loglevel" ]; then
        log_level="Set"
    elif [ "$i" == "--checkCompilerWarn" ]; then
        check_compilerWarn="Set"
    elif [ "$cluster_config_1" == "Set" ]; then
        cluster_config_1=$i
    elif [ "$cluster_config_2" == "Set" ]; then
        cluster_config_2=$i
    elif [ "$cluster_config_3" == "Set" ]; then
        cluster_config_3=$i
    elif [ "$cluster_config_4" == "Set" ]; then
        cluster_config_4=$i
    elif [ "$sc_num" == "Set" ]; then
        sc_num=$i
    elif [ "$pl_num" == "Set" ]; then
        pl_num=$i
    elif [ "$product_settings" == "Set" ]; then
        product_settings=$i
    elif [ "$sw_directory" == "Set" ]; then
        sw_directory=$i
    elif [ "$sw_install" == "Set" ]; then
        sw_install=$i
    elif [ "$sw_build" == "Set" ]; then
        sw_build=$i
    elif [ "$log_level" == "Set" ]; then
        log_level=$i
    elif [ "$check_compilerWarn" == "Set" ]; then
        check_compilerWarn=$i
    else
        usage_help
        exit 1
    fi
done

echo "1 - Running coverage on one cluster in sequence (default option)"
echo "2 - Running coverage on 4 clusters in parallel"
echo "3 - Exit"

while [ 1 ];
do
    read_option
    choice=$?
    if [ "$choice" == "0" ] || [ "$choice" == "1" ]; then
        break
    elif [ "$choice" == "2" ]; then
        exit 1
    else
        echo "Wrong choice"
        continue
    fi
done

if [ -z ${sw_directory} ]; then
    echo "Missing parameter"
    echo "You have to specify swDirNumber"
    exit 1
fi

remove_old_data
case $choice in
0)
    run_cov_in_sequence $cluster_config_1 $sc_num $pl_num $product_settings $sw_directory $sw_install $sw_build $log_level $check_compilerWarn;;
1)
    run_cov_in_paralel $cluster_config_1 $cluster_config_2 $cluster_config_3 $cluster_config_4 $sc_num $pl_num $product_settings $sw_directory $sw_install $log_level $check_compilerWarn;
    case $? in
    0)
        wait_for_all_cov_suites_done;;
    1)
        echo "Your configuration is not enough for running in paralel"; exit 1;;
    *)
        echo "Unknown error";
        exit 1;;
    esac;;
*)
    echo "Don't know option";
    exit 1;;
esac

#Hope everything is going smootly and now to collect coverage data
collect_cov_results_into_final_location
combine_into_one_cov_file
generate_cov_file_to_html_format $final_combined_cov_file $html_output_dir_name

#Send final result automatically to users
create_and_send_automatic_mail
