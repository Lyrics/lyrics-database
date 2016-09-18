#!/bin/sh

BASEDIR=$(dirname "$0")

find $BASEDIR/.. | grep -i 'Edition' --color
