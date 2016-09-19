#!/bin/sh

BASEDIR=$(dirname "$0")

grep -r '&#' $BASEDIR/.. --color
