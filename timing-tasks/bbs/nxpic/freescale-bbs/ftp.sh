#!/bin/sh
LCD=$1
CD=$2
FILE=$3
HOST=$4
USER=$5
PASSWD=$6
ftp -n<<!
open $HOST
user $USER $PASSWD
binary
cd $CD
lcd $LCD
prompt
mput $FILE
close
bye
!
