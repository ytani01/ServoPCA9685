#!/bin/sh -u
#
# (c) 2020 Yoichi Tanibayashi
#

##############################################################################
MYNAME=`basename $0`
MYDIR=`dirname $0`
echo "MYDIR=$MYDIR"
cd $MYDIR
echo "pwd:" `pwd`


##############################################################################
if [ -z "$VIRTUAL_ENV" ]; then
    echo "$MYNAME: Please activate python3 venv"
    exit 1
fi
VENVNAME=`basename $VIRTUAL_ENV`
echo "VENVNAME=$VENVNAME"

##############################################################################
# update pip
echo
echo "=== update pip command"
set -e
pip install -U pip
hash -r
pip -V
set +e

##############################################################################
# install python packages
echo
echo "=== install python packages"
set -e
pip install -r requirements.txt
set +e

##############################################################################
# check and modify crontab
echo
echo "=== check crontab"
TEMP_FILE=`tempfile`
crontab -l > $TEMP_FILE
if ! grep '^@reboot *sudo pigpiod' $TEMP_FILE; then
    cat $TEMP_FILE crontab-sample | crontab
    echo "* modified crontab"
    crontab -l | tail
fi
rm -f $TEMP_FILE
