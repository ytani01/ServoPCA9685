#!/bin/sh -u
#
# (c) 2020 Yoichi Tanibayashi
#

##############################################################################
MYNAME=`basename $0`
MYDIR=`dirname $0`
echo "MYDIR=$MYDIR"
cd $MYDIR
echo "===" `pwd`


##############################################################################
if [ -z "$VIRTUAL_ENV" ]; then
    echo "$MYNAME: Please activate venv"
    exit 1
fi
VENVNAME=`basename $VIRTUAL_ENV`
echo "VENVNAME=$VENVNAME"

##############################################################################
# update pip
echo "=== update pip command"
set -e
pip install -U pip
hash -r
pip -V
set +e

##############################################################################
# install python packages
echo "=== install python packages"
set -e
pip install -r requirements.txt
set +e

##############################################################################
