#!/bin/sh

BASEDIR=$(dirname "$0")

grep -r '&#x' $BASEDIR/../database --color
