#!/bin/sh

# Ensure the script's $PWD is relative to its location within the filesystem
SCRIPTPATH="$(cd "$(dirname "$0")"; pwd -P)"
cd "$SCRIPTPATH"

export SEPARATOR='==========================================================\n'

echo -n $SEPARATOR

for f in database/*.sh; do
    sh "$f" -H
done

for f in translations/*.sh; do
    sh "$f" -H
done
