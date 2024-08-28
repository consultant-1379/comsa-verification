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
source $COMSA_REPO_PATH/abs/make.cfg
cd -

# Overwrite the inherited compiler settings
setenv CMW_TOOLS $COMSA_REPO_PATH/coremw-tools
setenv CC $CMW_TOOLS/LSB_BUILD_ENV/lsb/bin/x86_64-lsbcc
setenv CXX $CMW_TOOLS/LSB_BUILD_ENV/lsb/bin/x86_64-lsbc++

setenv DX_SYSROOT_X86_64 $CMW_TOOLS/lotc4.0_api
setenv CFLAGS "-I$DX_SYSROOT_X86_64/include -I$DX_SYSROOT_X86_64/include/libxml2"
setenv LDFLAGS -L$DX_SYSROOT_X86_64/lib


setenv JCAT_FW $CMW_TOOLS/JCAT/3PP/LM_JCATFW-JCatFw
setenv JCAT_EXTENSIONS $CMW_TOOLS/JCAT/3PP/LM_JCAT_Extensions

setenv CLASSPATH $CMW_TOOLS/JCAT/3PP/LM_JCATFW-JCatFw/jar/JCatFw.jar:$CMW_TOOLS/JCAT/3PP/LM_JCATFW-JCatFw/lib/junit-3.8.2.jar:$CMW_TOOLS/JCAT/3PP/LM_JCATFW-JCatFw/lib/*:$CMW_TOOLS/JCAT/3PP/LM_JCATFW-JCatFw/scripts/:$CMW_TOOLS/JCAT/3PP/LM_JCAT_Extensions/jar/JCatExtensions.jar:$CMW_TOOLS/JCAT/3PP/LM_JCAT_Extensions/lib/*:$JCAT_OMP_CORE_MW/target/main/jar/*:$JCAT_OMP_CORE_MW/target/main/python/coremw/:$JCAT_OMP_EXTENSIONS/target/main/jar/JCAT_OMP_extensions.jar:$JCAT_OMP_EXTENSIONS/target/main/lib/*:$JCAT_OMP_EXTENSIONS/target/main/python/omp/:$MY_REPOSITORY/test_env/lib/config:$MY_REPOSITORY/test_env/config:$JCAT_OMP_EXTENSIONS/target/main/classes                                               
if ( -f /etc/SuSE-release ) then
    # modernize
    eval `/app/modules/0/bin/modulecmd tcsh add j2sdk`
    eval `/app/modules/0/bin/modulecmd tcsh add ant`
    eval `/app/modules/0/bin/modulecmd tcsh add git`
    eval `/app/modules/0/bin/modulecmd tcsh add python`
    eval `/app/modules/0/bin/modulecmd tcsh add autoconf`
    eval `/app/modules/0/bin/modulecmd tcsh add make`
    # TODO what about the opensaf/tools, used? then put it back /vobs/coremw/dev/opensaf/coremw-tools/
    setenv PATH $MY_REPOSITORY/test_env/bin:/home/tspsaf/public_html/test_env/targetconf/bin:/home/tspsaf/tools/Jython/bin:/home/tspsaf/bin:$PATH
    setenv JYTHONPATH ${MY_REPOSITORY}:${COMSA_REPO_PATH}/coremw-tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/jython:$JCAT_OMP_EXTENSIONS/target/main/python/:$JCAT_OMP_CORE_MW/target/main/python:$JCAT_OMP_EXTENSIONS/target/main/classes:/home/tspsaf/public_html/test_env/targetconf/lib:/home/tspsaf/tools/Jython/Lib:/proj/rdav/tools/eclipse/eclipse-helios-201204/plugins/org.python.pydev.debug_2.1.0.2011052613/pysrc
    setenv PYTHONPATH /home/tspsaf/public_html/test_env/targetconf/lib
else
    if ( -z $JAVA_HOME ) then
        setenv JAVA_HOME $(readlink -f /usr/bin/java | sed "s:bin/java::")
    endif         
    setenv JYTHONPATH ${MY_REPOSITORY}:$COMSA_REPO_PATH/coremw-tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/jython:$JCAT_OMP_EXTENSIONS/target/main/python/:$JCAT_OMP_CORE_MW/target/main/python:$JCAT_OMP_EXTENSIONS/target/main/classes:../../coremw-tools/targetconf/lib
    setenv PATH $MY_REPOSITORY/test_env/bin:$PATH
    setenv JYTHONPATH ${MY_REPOSITORY}:$COMSA_REPO_PATH/coremw-tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/jython:$JCAT_OMP_EXTENSIONS/target/main/python/:$JCAT_OMP_CORE_MW/target/main/python:$JCAT_OMP_EXTENSIONS/target/main/classes:../../coremw-tools/targetconf/lib:/proj/rdav/tools/eclipse/eclipse-helios-201204/plugins/org.python.pydev.debug_2.1.0.2011052613/pysrc
endif

alias eclipse /proj/rdav/tools/eclipse/eclipse/eclipse
chmod 600 $COMSA_VERIFICATION/ft/jcat_com_sa/src/test_env/misc/dump_handling/cluster_key*

mkdir -p /home/$USER/buildTokens


