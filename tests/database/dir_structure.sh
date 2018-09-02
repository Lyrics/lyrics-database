#!/bin/sh

ROOT_DIR=database
SIG=0

# Always pet the $PWD to the root level of the repository
SCRIPTPATH="$(cd "$(dirname "$0")"; pwd -P)"
cd "$SCRIPTPATH"
cd ../../

# There should only be dirs until we reach the album level dirs
files_in_upper_level_dirs() {
    find $ROOT_DIR -maxdepth 3 -type f | egrep '.*'
    return $?
}

# There should be only files within album level dirs
directories_in_album_dirs() {
    find $ROOT_DIR -mindepth 4 -type d | egrep '.*'
    return $?
}

TESTNAME='files_in_upper_level_dirs'
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

TESTNAME='directories_in_album_dirs'
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
