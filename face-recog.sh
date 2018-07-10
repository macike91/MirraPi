#!/bin/bash
# face-recog.sh

# params:
#  $1 - API_KEY for faces recognition
#  $2 - URL for faces recognition service
#  $3 - temporery image path
#  $4 - image width
#  $5 - image height
#  $6 - jpeg image quality (1 - 100)
#  $7 - image rotation
#  $8 - debug mode 1 / 0
#  $9 - images backup path
#  $10 - enviroment paths
#  $11 - is test '1' or '0'

API_KEY=$1
URL=$2
TMP_IMG=$3
IMG_W=$4
IMG_H=$5
IMG_Q=$6
IMG_ROT=$7
DEBUG=$8
BACKUP_PATH=$9
TMP_PATHS=${10}
TEST=${11}

LOG=/tmp/faces_recog.log

TEST_SUFFIX=""

if [ "$TEST" = "1" ] ; then
  echo "Last run: $(date)" > $LOG
  echo "API_KEY: $API_KEY" >> $LOG
  echo "URL: $URL" >> $LOG
  echo "TMP_IMG: $TMP_IMG" >> $LOG
  echo "IMG_W: $IMG_W" >> $LOG
  echo "IMG_H: $IMG_H" >> $LOG
  echo "IMG_Q: $IMG_Q" >> $LOG
  echo "IMG_ROT: $IMG_ROT" >> $LOG
  echo "DEBUG: $DEBUG" >> $LOG
  echo "BACKUP_PATH: $BACKUP_PATH" >> $LOG
  echo "TMP_PATHS: $TMP_PATHS" >> $LOG
  echo "TEST: $TEST" >> $LOG
  if [ ! -f $TMP_IMG ] ; then
    cp test/female.jpg $TMP_IMG
    echo "tmp_img copied!" >> $LOG
  fi
  TEST_SUFFIX="_test"
fi

# prepare enviroment (reason: this script is started from python enviroment)
export PATHS=$TMP_PATHS

if [[ $DEBUG -eq 1 && -f  $TMP_IMG ]] ; then
  cp $TMP_IMG $BACKUP_PATH$(date +%s)_img.jpg
fi

raspistill -rot $IMG_ROT -t 100 -w $IMG_W -h $IMG_H -q $IMG_Q -o $TMP_IMG$TEST_SUFFIX
echo $(curl -X POST -F "images_file=@$TMP_IMG" "$URL?api_key=$API_KEY&version=$(date +%Y-%m-%d)")
