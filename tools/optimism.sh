#!/bin/sh

BASEDIR=$(dirname "$0")

set 's/\s*$//g' \
    's/&#xA0;/\x20/g' \
    's/&#xB4;/\x27/g' \
    's/&#xC4;/Ä/g' \
    's/&#xDC;/Ü/g' \
    's/&#xDF;/ß/g' \
    's/&#xE0;/à/g' \
    's/&#xE1;/á/g' \
    's/&#xE2;/â/g' \
    's/&#xE3;/ã/g' \
    's/&#xE4;/ä/g' \
    's/&#xE5;/å/g' \
    's/&#xE6;/æ/g' \
    's/&#xE7;/ç/g' \
    's/&#xE8;/è/g' \
    's/&#xE9;/é/g' \
    's/&#xEA;/ê/g' \
    's/&#xEB;/ë/g' \
    's/&#xEC;/ì/g' \
    's/&#xED;/í/g' \
    's/&#xEE;/î/g' \
    's/&#xEF;/ï/g' \
    's/&#xF1;/ñ/g' \
    's/&#xF3;/ó/g' \
    's/&#xF6;/ö/g' \
    's/&#xFC;/ü/g' \
    's/&#x2026/.../g' \
    's/&#x2019;/\x27/g'

for i do
        echo $i
        find $BASEDIR/../database -type f -exec sed -i -e $i {} \;
done

