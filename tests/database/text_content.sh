#!/bin/sh

ROOT_DIR=database
SIG=0

# Always pet the $PWD to the root level of the repository
SCRIPTPATH="$(cd "$(dirname "$0")"; pwd -P)"
cd "$SCRIPTPATH"
cd ../../

# All ellipses in content should be represented as a unicode symbol …
triple_dots_within_text() {
    grep '\.\.\.' -r $ROOT_DIR
    return $?
}

# Chorus is bad
chorus_within_text() {
    grep 'Chorus' -r $ROOT_DIR
    return $?
}

TESTNAME='triple_dots_within_text'
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

TESTNAME='chorus_within_text'
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
