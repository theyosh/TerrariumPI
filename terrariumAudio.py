# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from gevent import sleep
import psutil
from subprocess import PIPE
import threading
import copy

import alsaaudio
import tempfile
import random

from terrariumUtils import terrariumUtils, classproperty

class terrariumAudio(object):

  @classproperty
  def available_soundcards(__cls__):
    soundcards = []
    for i in alsaaudio.card_indexes():
      try:
        (name, longname) = alsaaudio.card_name(i)
        soundcards.append({'index' : int(i), 'name' : longname})

      except Exception as ex:
        # Just ignore error, and skip it
        pass

    return soundcards

  @classmethod
  def volume(__cls__, hw, value = None):
    mixer = alsaaudio.Mixer(control='PCM',cardindex=hw)

    if value is None:
      # We get stereo volume but asume that left and right channel are at the same volume.
      return mixer.getvolume()[0]

    else:
      value = max(0,min(100,value))
      mixer.setvolume(value)

class terrariumAudioPlayer(object):

  CMD = '/usr/bin/ffmpeg'

  def __init__(self, hw, playlists = [], shuffle = False, repeat = False):
    self.__hw = hw
    self.__stop = False
    self.__player = {
      'ffmpeg' : None,
      'thread' : None,
      'exit_status' : None
    }

    self.playlists = playlists
    self.shuffle   = shuffle
    self.repeat    = repeat

  def __run(self):
    for playlist in self.playlists:
      if self.__stop:
        break

      files = copy.copy(playlist['files'])

      if playlist.get('shuffle'):
        random.shuffle(files)

      repeat = playlist.get('repeat',False)
      first_start = True
      while not self.__stop and (repeat or first_start):
        first_start = False

        playlist = [ f'file \'{audiofile}\'' for audiofile in files]

        with tempfile.NamedTemporaryFile() as fp:
          fp.write('\n'.join(playlist).encode())
          fp.flush()

          cmd = f'{self.CMD} -hide_banner -v 0 -f concat -safe 0 -i {fp.name} -f alsa hw:{self.__hw}'.split(' ')
          self.__player['ffmpeg'] = psutil.Popen(cmd, stdout=PIPE)
          self.__player['exit_status'] = self.__player['ffmpeg'].poll()
          while self.__player['exit_status'] is None:
            self.__player['exit_status'] = self.__player['ffmpeg'].poll()
            sleep(1)

    self.__player['ffmpeg'] = None

  def play(self):
    if self.running:
      self.stop()

    if len(self.playlists) > 0:
      self.__stop = False
      self.__player['thread'] = threading.Thread(target=self.__run)
      self.__player['thread'].start()

  def stop(self):
    self.__stop = True
    if self.running:
      self.__player['ffmpeg'].terminate()
      self.__player['thread'].join()

  @property
  def playlists(self):
    return self.__playlists

  @playlists.setter
  def playlists(self, playlists):
    self.__playlists = copy.copy(playlists)

  @property
  def running(self):
    return self.__player['ffmpeg'] is not None and self.__player['ffmpeg'].poll() is None


# if __name__  == "__main__":
#   t = terrariumAudioPlayer(1,['/home/pi/TerrariumPI/media/01-Eric-Prydz-vs.-Floyd-Proper-education.mp3','/home/pi/TerrariumPI/media/03-Jekyll-Hyde-Frozen-flame.mp3'])
#   t.play()

#   time.sleep(30)

#   t.stop()




# class terrariumAudioPlayer(object):

#   AUDIO_FOLDER = 'audio'
#   VALID_EXTENSION = ['mp3','m4a','ogg']
#   LOOP_TIMEOUT = 30
#   VOLUME_STEP = 5

#   def __init__(self,playlistdata,cardid,pwmdimmer,callback=None):
#     self.__audio_player = None
#     self.__audio_mixer = None

#     self.__load_audio_files()
#     self.__load_playlists(playlistdata)
#     hwcards = terrariumAudioPlayer.get_sound_cards()
#     if cardid in hwcards:
#       self.__hwid = hwcards[cardid]['hwid']
#       self.__callback = callback

#       if pwmdimmer and cardid.startswith('bcm2835'):
#         logger.warning('Disabled audio playing due to hardware conflict with PWM dimmers and onboard soundcard')
#       else:
#         self.__load_audio_mixer()
#         logger.info('Player loaded with %s audio files and %s playlists. Starting engine.' % (len(self.__audio_files),len(self.__playlists)))
#         _thread.start_new_thread(self.__engine_loop, ())

#   def __load_audio_files(self):
#     self.__audio_files = {}
#     for audiofilename in os.listdir(terrariumAudioPlayer.AUDIO_FOLDER):
#       if os.path.splitext(audiofilename)[1][1:].lower() in terrariumAudioPlayer.VALID_EXTENSION:
#         audiofile = terrariumAudioFile(os.path.join(terrariumAudioPlayer.AUDIO_FOLDER,audiofilename))
#         if audiofile.get_id() is not None:
#           self.__audio_files[audiofile.get_id()] = audiofile

#   def __load_playlists(self,data):
#     self.__playlists = {}
#     for audio_playlist in data:
#       audio_files = {}

#       for fileid in audio_playlist['files']:
#         if fileid in self.__audio_files:
#           audio_files[fileid] = self.__audio_files[fileid]

#       playlist = terrariumAudioPlaylist(audio_playlist['id'],
#                                         audio_playlist['name'],
#                                         audio_playlist['start'],
#                                         audio_playlist['stop'],
#                                         audio_playlist['volume'],
#                                         audio_playlist['repeat'],
#                                         audio_playlist['shuffle'],
#                                         audio_files)

#       self.__playlists[playlist.get_id()] = playlist

#   def __load_audio_mixer(self):
#     try:
#       self.__audio_mixer = alsaaudio.Mixer(control='PCM',cardindex=self.__hwid)
#     except alsaaudio.ALSAAudioError as ex:
#       self.__audio_mixer = alsaaudio.Mixer(control='Headphone',cardindex=self.__hwid)

#     self.mute()

#   def __engine_loop(self):
#     self.__current_playlist = None
#     while True and self.__audio_mixer is not None:
#       starttime = time.time()
#       for audio_playlist_id in self.__playlists:
#         playlist = self.__playlists[audio_playlist_id]
#         if not self.is_running() and playlist.is_time() and playlist.has_files():
#           # Current playlist needs to be running
#           files = [self.__audio_files[audiofile_id].get_full_path() for audiofile_id in playlist.get_files()]
#           logger.info('Starting playlist %s for period start %s and end %s with %s/%s amount of files at volume %s' %
#                         (playlist.get_name(),
#                         playlist.get_start(),
#                         playlist.get_stop(),
#                         len(playlist.get_files()),
#                         len(files),
#                         playlist.get_volume())
#                       )

#           audio_player_command = ['cvlc','-q','--no-interact','--play-and-exit','--aout=alsa','--alsa-audio-device=hw:' + str(self.__hwid)]
#           #audio_player_command += ['--norm-buff-size','1000','--norm-max-level','5.0']

#           if playlist.get_shuffle():
#             audio_player_command += ['-Z']

#           if playlist.get_repeat():
#             audio_player_command += ['-L']

#           audio_player_command += files

#           self.__audio_player = psutil.Popen(audio_player_command)
#           playlist.set_started()
#           self.__active_playlist = playlist
#           self.mute(False)
#           self.set_volume(playlist.get_volume())
#           if self.__callback is not None:
#             self.__callback(socket=True)

#         elif self.is_running() and self.__active_playlist.get_id() == playlist.get_id() and not playlist.is_time() :
#           logger.info('Stopping playlist %s' % (playlist.get_name(),))
#           self.__audio_player.terminate()
#           self.__active_playlist = None
#           self.__audio_player = None
#           self.mute()

#           if self.__callback is not None:
#             self.__callback(socket=True)

#         else:
#           logger.debug('No player action needed')

#       duration = time.time() - starttime
#       if duration < terrariumAudioPlayer.LOOP_TIMEOUT:
#         logger.info('Update done in %.5f seconds. Waiting for %.5f seconds for next update' % (duration,terrariumAudioPlayer.LOOP_TIMEOUT - duration))
#         sleep(terrariumAudioPlayer.LOOP_TIMEOUT - duration)
#       else:
#         logger.warning('Updating took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumAudioPlayer.LOOP_TIMEOUT,terrariumEngine.LOOP_TIMEOUT))

#   @staticmethod
#   def get_sound_cards():
#     soundcards = {}
#     for i in alsaaudio.card_indexes():
#       try:
#         (name, longname) = alsaaudio.card_name(i)
#         soundcards[name] = {'hwid' : int(i), 'name' : longname}

#       except Exception as ex:
#         # Just ignore error, and skip it
#         pass

#     return soundcards

#   def get_volume(self):
#     return (int(self.__audio_mixer.getvolume()[0]) if self.__audio_mixer is not None else -1)

#   def set_volume(self,value):
#     if self.__audio_mixer is not None:
#       try:
#         value = int(value)
#       except Exception as ex:
#         value = -1

#       if 0 <= value <= 100:
#         oldvalue = self.get_volume()
#         self.__audio_mixer.setvolume(value,alsaaudio.MIXER_CHANNEL_ALL)
#         logger.info('Changed volume from %s to %s' % (oldvalue,self.get_volume()))

#   def volume_up(self):
#     if self.__audio_mixer is not None:
#       volume = self.get_volume() + terrariumAudioPlayer.VOLUME_STEP
#       if volume > 100:
#         volume = 100

#       self.set_volume(volume)

#   def volume_down(self):
#     if self.__audio_mixer is not None:
#       volume = self.get_volume() - terrariumAudioPlayer.VOLUME_STEP
#       if volume < 0:
#         volume = 0

#       self.set_volume(volume)

#   def mute(self,mute = True):
#     if self.__audio_mixer is not None:
#       self.__audio_mixer.setmute(1 if mute else 0, alsaaudio.MIXER_CHANNEL_ALL)

#   def reload_audio_files(self):
#     self.__load_audio_files()

#   def reload_playlists(self,data):
#     self.__load_playlists(data)

#   def get_audio_files(self):
#     return self.__audio_files

#   def get_playlists(self):
#     return self.__playlists

#   def get_current_state(self):
#     if self.__audio_mixer is None or len(self.get_audio_files()) == 0 and len(self.get_playlists()) == 0:
#       return {'running' : 'disabled'}

#     data = {'running' : self.is_running()}

#     if data['running'] and self.__active_playlist is not None:
#       data.update(self.get_active_playlist().get_data())

#     data['volume'] = self.get_volume()

#     return data

#   def is_running(self):
#     running = False
#     if self.__audio_mixer is not None:
#       try:
#         running = self.__audio_player.status() in ['running','sleeping','disk-sleep']
#       except Exception as ex:
#         pass

#     return running

#   def get_active_playlist(self):
#     return self.__active_playlist
