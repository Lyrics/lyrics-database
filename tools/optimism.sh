#!/bin/sh

BASEDIR=$(dirname "$0")

set 's/&#xDF;/ß/g' \
    's/&#xFC;/ü/g' \
    's/&#xA0;/\x20/g' \
    's/&#xF6;/ö/g' \
    's/&#xE4;/ä/g' \
    's/&#xC4;/Ä/g' \
    's/&#xF3;/ó/g' \
    's/&#xED;/í/g' \
    's/&#xF1;/ñ/g' \
    's/&#xE9;/é/g' \
    's/&#xDC;/Ü/g' \
    's/&#x2026/.../g' \
    's/&#xB4;/\x27/g' \
    's/&#x2019;/\x27/g' \
    's/[ \t]*$//'

for i do
        echo $i
        find $BASEDIR/../database -type f -exec sed -i -e $i {} \;
done

