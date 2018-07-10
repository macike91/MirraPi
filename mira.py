import os, time as t
import random
import urllib, json
import RPi.GPIO as GPIO
import sys
from subprocess import Popen, PIPE
import pprint as pp

from utils.sound import MiraSound


CURRENT_DIR='/home/pi/mira/'

os.chdir(CURRENT_DIR)
CONFIG_FILENAME='config.json'


# load JSON configuration file
conf = {}
with open(CONFIG_FILENAME) as data_file:    
    conf = json.load(data_file)

miraSound = MiraSound(conf)

# configuration for button
BUTTON_PIN = conf['BUTTON_PIN']
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN ,GPIO.IN)

isTest = 0

DEBUG = conf['DEBUG']
if len(sys.argv) == 1:
  print 'mode: normal'
else:
  print 'mode: self_triggered'

# current state variables
age = 0
sex = ''
temp = 0
weather = ''
time = 0
faces = 0
toodark = 0

# load actions and rules into memmory
actions = [line.rstrip('\n') for line in open(conf['ACTIONS_DATA'])]
rules = [line.rstrip('\n') for line in open(conf['RULES_DATA'])]

def getMillis():
  return int(t.time() * 1000.0)

def setDefaultFace():
  global faces
  global age
  global sex
  global toodark
  age = 0
  sex = ''
  faces = 0
  toodark = 0

def doAction(action_type, action_data):
  if action_type == 'say':
    if conf['DEBUG']:
      print 'Say: ' + action_data
      print '------------------\nPARAMETERS:'
      print '* Age: ' + str(age)
      print '* Sex: ' + sex
      print '* Temp: ' + str(temp)
      print '* Weather: ' + weather
      print '* Time: ' + str(time)
      print '* Faces: ' + str(faces)
      print '* Toodark: ' + str(toodark)
    miraSound.downloadStopPlay(action_data)

def chooseAction():
  global faces
  global age
  global sex
  global temp
  global weather
  global time
  selected_actions = []
  parseFaceRecog()
  if faces > 0:
    if conf['SAY_INFO'] == 1:
      miraSound.downloadStopPlay(sex)
      #t.sleep(0.1)
      miraSound.downloadStopPlay(str(age))
      #t.sleep(0.1)
  else:
    setDefaultFace()
  try:
    parseWheather()
  except:
    weather = 'sunny'
    print "Weather parsing error! default value 'sunny'"
  idx = 0
  nonTautology = []
  for condition in rules:
    if eval(condition):
      if condition.strip() != '1':
        nonTautology.append(actions[idx])
      selected_actions.append(actions[idx])
    idx += 1
  if faces > 0:
    if len(nonTautology) > 0:
      selected_actions = nonTautology
  action = selected_actions[random.randint(0, len(selected_actions) - 1)]
  splited_a = action.split(';')
  doAction(splited_a[0].strip(), splited_a[1].strip())

def parseFaceRecog():
  global faces
  global age
  global sex
  #face_recog_cmd = CURRENT_DIR + 'face-recog.sh {0} {1} {2} {4} {5} {6} {7} {8} {9}'.format(conf['FACE_RECOG_API_KEY'], conf['FACE_RECOG_URL'], conf['TMP_IMG_PATH'], conf['IMG_W'], conf['IMG_H'], conf['IMG_Q'], conf['IMG_ROT'], conf['DEBUG'], conf['BACKUP_PATH'], conf['PATHS'])
  (stdout_json, stderr) = Popen(['./face-recog.sh', conf['FACE_RECOG_API_KEY'], conf['FACE_RECOG_URL'], conf['TMP_IMG_PATH'], str(conf['IMG_W']), str(conf['IMG_H']), str(conf['IMG_Q']), str(conf['IMG_ROT']), str(conf['DEBUG']), conf['BACKUP_PATH'], conf['PATHS'], str(isTest)], stdout=PIPE).communicate()
  try:
    json_obj = json.loads(stdout_json)
  except ValueError:
    print 'err: probably problem with camera'
    setDefaultFace()
    return
  if DEBUG == 1:
    pp.pprint(json_obj)
  faces = len(json_obj['images'][0]['faces'])
  if faces > 0:
    age_min = json_obj['images'][0]['faces'][0]['age']['min']
    age_max = json_obj['images'][0]['faces'][0]['age']['max']
    # print range of age in debug mode
    if DEBUG == 1:
      print 'age-min: ' + str(age_min)
      print 'age-max: ' + str(age_max)
    age = int((age_min + age_max) / 2.0) - random.randint(0, 5)
    sex = json_obj['images'][0]['faces'][0]['gender']['gender'].lower()


def parseWheather():
  global temp
  global weather
  global temp
  global time
  w_data = urllib.urlopen(conf['WEATHER_URL']).read()
  output = json.loads(w_data)
  print 'wheater begin:'
  pp.pprint(output)
  print 'wheater end.'
  temp = output['list'][1]['main']['temp']
  weather_orig = output['list'][1]['weather'][0]['description']
  if weather_orig == 'clear sky' or 'few clouds':
    weather = 'sunny'
  elif weather_tmp == 'snow':
    weather = 'snow'
  elif weather_tmp == 'thunderstorm' or weather_tmp == 'rain' or weather_tmp == 'shower rain':
    weather = 'rain'
  else :
    weather = 'other'
  time = int(t.strftime("%H"))

def btnLongPress():
  print 'long press...'

def btnShortPress():
  print 'short press...'
  miraSound.playFileBg('shutter_hmm.wav')
  chooseAction()
  print 'info: mirra is done'

lastState = bool(GPIO.input(BUTTON_PIN))
press_t = 0
release_t = 0

miraSound.downloadStopPlay('Hello!')

# infinite loop is triggering button routines
if len(sys.argv) > 1 and sys.argv[1] == 'test':
  isTest = 1
  while True:
    c = raw_input("Press\n\'ENTER\' for short press\n\'l\' for long press\n\'q\' for quit\n")
    if c == 'q':
      break
    elif c == 'l':
      btnLongPress()
    else:
      btnShortPress()
else:
  while True:
    t.sleep(conf['BTN_REFRESH_DELAY'])
    if (bool(GPIO.input(BUTTON_PIN)) is not lastState):
      if (lastState == True):
        press_t = getMillis()
      else:
        release_t = getMillis()
        if release_t - press_t > conf['LONG_PRESS_DELAY']:
          btnLongPress()
        else:
          btnShortPress()
      lastState = not lastState
     
