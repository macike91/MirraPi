#!/bin/bash
# play_file.sh

#  $1 - param - filename of record
#  $2 - path for sounds
#  $3 - enviroment paths2

FILENAME=$1
SOUNDS_PATH=$2

export PATHS=$3

SOUND_FILENAME=$SOUNDS_PATH$FILENAME
cvlc --quiet --play-and-exit $SOUND_FILENAME
