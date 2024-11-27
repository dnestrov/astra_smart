#!/bin/bash

if [ "$1" = "--help" ]
then
    echo " "
    echo "#command line arguments:"
    echo "# $1 full or relative path to astra_work/.exe/astrarc"
    echo "# $2 full or relative path to sophia/models/st40/bin"
    echo "# $3 (optional) variable name to assign a list of libraries for linking. Default value libSOPHIA."
    echo "#"
    echo "# variable name must actually exist already in astrarc. This script find that line and replaces it"
    echo "#"
    echo "# example: ./setenv_interface_so.sh ../../astra_work/.exe/astrarc ../models/st40/bin"
    echo " "
    exit 0
fi

varName=${3:-libSOPHIA}

lib_str="\"$2/tools.o $2/simulink_to_fortran.o $2/fortran_to_simulink.o\""
new_line="setenv libSOPHIA ${lib_str}"

sed -i "s|setenv \+$varName.*|$new_line|g" "$1"
