#!/bin/bash -x
# Compiles JCAP dependencies
echo $PWD
#Prints errors and exists
# $@ Error message
_error()
{
   echo "Error: $@"
   exit 1
}

# Checks environment variables are set in order to make sucessfull build of dependencies
_check_env()
{
    local readonly __sourcescript="sourceme.sh"
    local readonly __variables=`cat ${__sourcescript} | sed -rn 's/.*export (.*)=.*/\1/p'`

    for var in ${__variables}; do
       [[ -z ${!var} ]] && _error "$var is not set. Did you sourced ${__sourcescript}?"
    done
}

#Build the OMP extension dependencies
_build_deps()
{
   cd $JCAT_OMP_CORE_MW
   ant clean
   cd $JCAT_OMP_EXTENSIONS
   ant clean
   ant clean
   ant
   cd $JCAT_OMP_CORE_MW
   ant

}

_check_env
_build_deps
