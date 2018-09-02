#!/bin/sh

ROOT_DIR=database
SIG=0

# Always pet the $PWD to the root level of the repository
SCRIPTPATH="$(cd "$(dirname "$0")"; pwd -P)"
cd "$SCRIPTPATH"
cd ../../

filename_extensions() {
    find $ROOT_DIR -type f -name "*.txt" -ls | egrep '.*'
    return $?
}

TESTNAME='filename_extensions'
if $TESTNAME
then
    SIG=1
    tput setaf 1
    echo "[ ERROR ]:" $TESTNAME
    tput sgr0
else
    tput setaf 2
    echo "[ OK ]: no" $TESTNAME
    tput sgr0
fi
echo -n $SEPARATOR

exit $SIG
