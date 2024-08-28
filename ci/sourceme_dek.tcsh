#!/usr/bin/tcsh

setenv COMSA_VERIFICATION "`git rev-parse --git-dir`/.."
setenv COMSA_VERIFICATION_COMMIT_ID "`git --git-dir $COMSA_VERIFICATION/.git rev-parse --short HEAD`"
setenv COMSA_REPO_PATH $COMSA_VERIFICATION/../comsa-source/
setenv COMSA_REPO_PATH_COMMIT_ID "`git --git-dir $COMSA_REPO_PATH/.git rev-parse --short HEAD`"

setenv MY_WORKSPACE $COMSA_VERIFICATION/ft
setenv MY_REPOSITORY $MY_WORKSPACE/jcat_com_sa/src

setenv JCAT_OMP_EXTENSIONS $MY_WORKSPACE/JCAT_OMP_extensions
setenv JCAT_OMP_CORE_MW $MY_WORKSPACE/JCAT_OMP_core_mw

cd $COMSA_REPO_PATH/abs/
source $COMSA_REPO_PATH/abs/make_dek.cfg
cd -

# Overwrite the inherited compiler settings
setenv CMW_TOOLS $STARTDIR/../coremw-tools
setenv CC $CMW_TOOLS/LSB_BUILD_ENV/lsb/bin/x86_64-lsbcc
setenv CXX $CMW_TOOLS/LSB_BUILD_ENV/lsb/bin/x86_64-lsbc++

setenv DX_SYSROOT_X86_64 $CMW_TOOLS/lotc4.0_api
setenv CFLAGS "-I$DX_SYSROOT_X86_64/include -I$DX_SYSROOT_X86_64/include/libxml2"
setenv LDFLAGS -L$DX_SYSROOT_X86_64/lib


setenv JCAT_FW $CMW_TOOLS/JCAT/3PP/LM_JCATFW-JCatFw
setenv JCAT_EXTENSIONS $CMW_TOOLS/JCAT/3PP/LM_JCAT_Extensions

setenv CLASSPATH $JCAT_FW/jar/JCatFw.jar:$JCAT_FW/scripts/:$JCAT_EXTENSIONS/jar/JCatExtensions.jar:$JCAT_EXTENSIONS/lib/:$JCAT_OMP_CORE_MW/target/main/jar/JCAT_OMP_core_mw.jar:$JCAT_OMP_CORE_MW/target/main/python/coremw/:$JCAT_OMP_EXTENSIONS/target/main/jar/JCAT_OMP_extensions.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/junit-4.10.jar:$JCAT_OMP_EXTENSIONS/target/main/python/omp/:$MY_REPOSITORY/test_env/lib/config:$MY_REPOSITORY/test_env/config:$JCAT_OMP_EXTENSIONS/target/main/classs:$JCAT_OMP_EXTENSIONS/target/main/lib/library-broker-1.0.5.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/commons-io-2.4.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/commons-beanutils-1.7.0.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/commons-collections-3.2.1.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/remote-cli-1.3.0.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/snmp4j-1.11.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/jfreechart-1.0.13.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/schema_netconf.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/commons-lang-2.4.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/commons-configuration-1.6.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/xbean.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/commons-logging-1.1.1.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/jcommon-1.0.16.jar:$JCAT_FW/lib/commons-beanutils-1.7.0.jar:$JCAT_FW/lib/commons-logging-1.1.1.jar:$JCAT_FW/lib/saxon-9.jar:$JCAT_FW/lib/commons-beanutils-core-1.8.0.jar:$JCAT_FW/lib/jcat-fw-ignoreList-1.0.jar:$JCAT_FW/lib/saxon-dom-9.jar:$JCAT_FW/lib/commons-collections-3.2.1.jar:$JCAT_FW/lib/junit-3.8.2.jar:$JCAT_FW/lib/stax-api-1.0.1.jar:$JCAT_FW/lib/commons-configuration-1.6.jar:$JCAT_FW/lib/jython.jar:$JCAT_FW/lib/xmlbeans-2.4.0.jar:$JCAT_FW/lib/commons-digester-1.8.jar:$JCAT_FW/lib/log4j-1.2.16.jar:$JCAT_FW/lib/xmlbeans-xpath-2.4.0.jar:$JCAT_FW/lib/commons-lang-2.4.jar:$JCAT_FW/lib/mysql-connector-java-5.1.13.jar:$JCAT_EXTENSIONS/lib/snmp4j-1.9.3c.jar:$JCAT_EXTENSIONS/lib/trilead-ssh2-build213-svnkit-1.3-patch.jar
if ( -f /etc/SuSE-release ) then

    # TODO what about the opensaf/tools, used? then put it back /vobs/coremw/dev/opensaf/coremw-tools/
    setenv PATH $MY_REPOSITORY/test_env/bin:$COMSA_VERIFICATION/ci/bin:/home/tspsaf/public_html/test_env/targetconf/bin:/home/tspsaf/tools/Jython/bin:/home/tspsaf/bin:$PATH
    setenv JYTHONPATH ${MY_REPOSITORY}:${COMSA_REPO_PATH}/coremw-tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/jython:$JCAT_OMP_EXTENSIONS/target/main/python/:$JCAT_OMP_CORE_MW/target/main/python:$JCAT_OMP_EXTENSIONS/target/main/classes:/home/tspsaf/public_html/test_env/targetconf/lib:/home/tspsaf/tools/Jython/Lib
    setenv PYTHONPATH /home/tspsaf/public_html/test_env/targetconf/lib
    setenv JAVA_HOME /usr/lib64/jvm/java-1.7.0-openjdk
else
    setenv JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
    if ( -z $JAVA_HOME ) then
        setenv JAVA_HOME $(readlink -f /usr/bin/java | sed "s:bin/java::")
    endif
    setenv JYTHONPATH ${MY_REPOSITORY}:$JCAT_FW/scripts/jython:$JCAT_OMP_EXTENSIONS/target/main/python/:$JCAT_OMP_CORE_MW/target/main/python:$JCAT_OMP_EXTENSIONS/target/main/classes:../../coremw-tools/targetconf/lib
    setenv PATH $MY_REPOSITORY/test_env/bin:$COMSA_VERIFICATION/ci/bin:/home/tspsaf/public_html/test_env/targetconf/bin:/home/tspsaf/tools/Jython/bin:/home/tspsaf/bin:$PATH
    setenv JYTHONPATH ${MY_REPOSITORY}:$JCAT_FW/scripts/jython:$JCAT_OMP_EXTENSIONS/target/main/python/:$JCAT_OMP_CORE_MW/target/main/python:$JCAT_OMP_EXTENSIONS/target/main/classes:/home/tspsaf/public_html/test_env/targetconf/lib:/home/tspsaf/tools/Jython/Lib
    setenv PYTHONPATH /home/tspsaf/public_html/test_env/targetconf/lib
endif

alias eclipse /proj/rdav/tools/eclipse/eclipse/eclipse
chmod 600 $COMSA_VERIFICATION/ft/jcat_com_sa/src/test_env/misc/dump_handling/cluster_key*

mkdir -p /home/$USER/buildTokens
