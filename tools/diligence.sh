#!/bin/sh

BASEDIR=$(dirname "$0")

find $BASEDIR/../database | grep -i 'Edition' --color
