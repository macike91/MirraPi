#!/bin/bash
# play_sound.sh

#  $1 - text-to-speech username
#  $2 - text-to-speech password
#  $3 - text-to-speech URL
#  $4 - param - text for synthetisation
#  $5 - param - filename of record
#  $6 - path for sounds
#  $7 - enviroment paths

USERNAME=$1
PASSWORD=$2
URL=$3
TEXT=$4
FILENAME=$5
SOUNDS_PATH=$6

export PATHS=$7
SOUND_FILENAME=$SOUNDS_PATH$FILENAME

curl --silent -X POST -u $USERNAME:$PASSWORD --header "Content-Type: application/json" --header "Accept: audio/wav" --data "{\"text\":\"$TEXT\"}" --output $SOUND_FILENAME $URL
