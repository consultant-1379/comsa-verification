#!/bin/bash                                                                                                                                                                                                                                


export COMSA_REPO_PATH=$(pwd)/../../../
export MY_WORKSPACE=$(pwd)           

export MY_REPOSITORY=$MY_WORKSPACE/jcat_com_sa/src

#xport CXP_ARCHIVE=$COMSA_REPO_PATH/output/TargetRoot/x86_64-lsb/Archives/

#xport RUNTIMES_ARCHIVE=$MY_WORKSPACE/runtimes

export JCAT_OMP_EXTENSIONS=$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions
export JCAT_OMP_CORE_MW=$COMSA_REPO_PATH/tools/st/JCAT_OMP_core_mw      

export JCAT_FW=$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCATFW-JCatFw
export JCAT_EXTENSIONS=$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCAT_Extensions

export CLASSPATH=$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCATFW-JCatFw/jar/JCatFw.jar:$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCATFW-JCatFw/lib/junit-3.8.2.jar:$COMSA_REPO_PATH/JCAT/3PP/LM_JCATFW-JCatFw/lib/*:$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/:$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCAT_Extensions/jar/JCatExtensions.jar:$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCAT_Extensions/lib/*:$COMSA_REPO_PATH/tools/st/JCAT_OMP_core_mw/target/main/jar/*:$COMSA_REPO_PATH/tools/st/JCAT_OMP_core_mw/target/main/python/coremw/:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/jar/../../tools/st/JCAT_OMP_extensions.jar:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/lib/*:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/python/omp/:$MY_REPOSITORY/test_env/lib/config:$MY_REPOSITORY/test_env/config:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/classes                                               

if [ ! -f /etc/SuSE-release ]
then                         
    if [[ -z $JAVA_HOME ]]
    then                     
        export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
    fi                                                                    
    export JYTHONPATH=$MY_REPOSITORY:$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/jython:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/python/:$COMSA_REPO_PATH/tools/st/JCAT_OMP_core_mw/target/main/python:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/classes:../../tools/targetconf/lib
    export PATH=$MY_REPOSITORY/test_env/bin:$PATH
    export JYTHONPATH=$MY_REPOSITORY:$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/jython:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/python/:$COMSA_REPO_PATH/tools/st/JCAT_OMP_core_mw/target/main/python:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/classes:../../tools/targetconf/lib

else
    # modernize
    eval `/app/modules/0/bin/modulecmd bash add j2sdk`
    eval `/app/modules/0/bin/modulecmd bash add ant`
    eval `/app/modules/0/bin/modulecmd bash add git`
    eval `/app/modules/0/bin/modulecmd bash add python`
    eval `/app/modules/0/bin/modulecmd bash add autoconf`
    eval `/app/modules/0/bin/modulecmd bash add make`
    # TODO what about the opensaf/tools, used? then put it back /vobs/coremw/dev/opensaf/tools/
    export PATH=$MY_REPOSITORY/test_env/bin:/home/tspsaf/public_html/test_env/targetconf/bin:/home/tspsaf/tools/Jython/bin:/home/tspsaf/bin:$PATH
    export JYTHONPATH=$MY_REPOSITORY:$COMSA_REPO_PATH/tools/JCAT/3PP/LM_JCATFW-JCatFw/scripts/jython:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/python/:$COMSA_REPO_PATH/tools/st/JCAT_OMP_core_mw/target/main/python:$COMSA_REPO_PATH/tools/st/JCAT_OMP_extensions/target/main/classes:/home/tspsaf/public_html/test_env/targetconf/lib:/home/tspsaf/tools/Jython/Lib
    export PYTHONPATH=/home/tspsaf/public_html/test_env/targetconf/lib

fi

