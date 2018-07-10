import os, md5

class MiraSound:

  def __init__(self, conf):
    self.conf = conf
    self.downloadVoiceCmd = './downloadVoice.sh {0} {1} {2} {3} {4} {5} {6}'
    self.playFileCmd = './play_file.sh {0} {1} {2}'

  def playFileBg(self, filename):
    cmd = (self.playFileCmd + ' &').format(filename, self.conf['SOUNDS_BUILDIN_PATH'], self.conf['PATHS'])
    os.system(cmd)

  def playFileFg(self, filename):
    cmd = self.playFileCmd.format(filename, self.conf['SOUNDS_BUILDIN_PATH'], self.conf['PATHS'])
    os.system(cmd)

  def playVoiceBg(self, text):
    cmd = (self.playFileCmd + ' &').format(self.getFilenameFromString(text), self.conf['SOUNDS_CACHE_PATH'], self.conf['PATHS'])
    os.system(cmd)

  def playVoiceFg(self, text):
    cmd = self.playFileCmd.format(self.getFilenameFromString(text), self.conf['SOUNDS_CACHE_PATH'], self.conf['PATHS'])
    os.system(cmd)

  def voiceExists(self, text):
    return os.path.exists(self.conf['SOUNDS_CACHE_PATH'] + self.getFilenameFromString(text))

  def downloadVoice(self, text):
    cmd = self.downloadVoiceCmd.format(self.conf['SPEECH_API_USER'], self.conf['SPEECH_API_PASS'], self.conf['SPEECH_API_URL'], 
      text, self.getFilenameFromString(text), self.conf['SOUNDS_CACHE_PATH'], self.conf['PATHS'])
    os.system(cmd)
  
  # If voice doesn't exist, download it and play, when it exists, just play. It stops all currently running voices.
  def downloadStopPlay(self, text):
    if not self.voiceExists(text):
      self.downloadVoice(text)
    self.stopAll()
    self.playVoiceFg(text)

  def getFilenameFromString(self, say_str):
    m = md5.new()
    m.update(say_str)
    return m.hexdigest() + '.wav'

  def stopAll(self):
    os.system("pids=$(ps aux | grep /usr/bin/vlc | grep -v grep | awk '{print $2}') ; if [ $pids ] ; then kill -15 $pids ; fi")
