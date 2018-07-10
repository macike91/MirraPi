#!/bin/bash
SCRIPT_PATH=/home/pi/mira/mira.py

if [ $(ps aux | grep $SCRIPT_PATH | grep -v "grep" | wc -l) -eq "0" ] ; then
  /usr/bin/python $SCRIPT_PATH &
fi
