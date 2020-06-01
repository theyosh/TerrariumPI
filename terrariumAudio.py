# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

try:
  import thread as _thread
except ImportError as ex:
  import _thread
import time
import psutil
import os
import json
import alsaaudio

from hashlib import md5
from gevent import sleep
try:
  from MediaInfoDLL import MediaInfo, Stream
except ImportError as ex:
  from MediaInfoDLL3 import MediaInfo, Stream

from terrariumUtils import terrariumUtils

class terrariumAudioPlayer(object):

  AUDIO_FOLDER = 'audio'
  VALID_EXTENSION = ['mp3','m4a','ogg']
  LOOP_TIMEOUT = 30
  VOLUME_STEP = 5

  def __init__(self,playlistdata,cardid,pwmdimmer,callback=None):
    self.__audio_player = None
    self.__audio_mixer = None

    self.__load_audio_files()
    self.__load_playlists(playlistdata)
    hwcards = terrariumAudioPlayer.get_sound_cards()
    if cardid in hwcards:
      self.__hwid = hwcards[cardid]['hwid']
      self.__callback = callback

      if pwmdimmer and cardid.startswith('bcm2835'):
        logger.warning('Disabled audio playing due to hardware conflict with PWM dimmers and onboard soundcard')
      else:
        self.__load_audio_mixer()
        logger.info('Player loaded with %s audio files and %s playlists. Starting engine.' % (len(self.__audio_files),len(self.__playlists)))
        _thread.start_new_thread(self.__engine_loop, ())

  def __load_audio_files(self):
    self.__audio_files = {}
    for audiofilename in os.listdir(terrariumAudioPlayer.AUDIO_FOLDER):
      if os.path.splitext(audiofilename)[1][1:].lower() in terrariumAudioPlayer.VALID_EXTENSION:
        audiofile = terrariumAudioFile(os.path.join(terrariumAudioPlayer.AUDIO_FOLDER,audiofilename))
        if audiofile.get_id() is not None:
          self.__audio_files[audiofile.get_id()] = audiofile

  def __load_playlists(self,data):
    self.__playlists = {}
    for audio_playlist in data:
      audio_files = {}

      for fileid in audio_playlist['files']:
        if fileid in self.__audio_files:
          audio_files[fileid] = self.__audio_files[fileid]

      playlist = terrariumAudioPlaylist(audio_playlist['id'],
                                        audio_playlist['name'],
                                        audio_playlist['start'],
                                        audio_playlist['stop'],
                                        audio_playlist['volume'],
                                        audio_playlist['repeat'],
                                        audio_playlist['shuffle'],
                                        audio_files)

      self.__playlists[playlist.get_id()] = playlist

  def __load_audio_mixer(self):
    try:
      self.__audio_mixer = alsaaudio.Mixer(control='PCM',cardindex=self.__hwid)
    except alsaaudio.ALSAAudioError as ex:
      self.__audio_mixer = alsaaudio.Mixer(control='Headphone',cardindex=self.__hwid)

    self.mute()

  def __engine_loop(self):
    self.__current_playlist = None
    while True and self.__audio_mixer is not None:
      starttime = time.time()
      for audio_playlist_id in self.__playlists:
        playlist = self.__playlists[audio_playlist_id]
        if not self.is_running() and playlist.is_time() and playlist.has_files():
          # Current playlist needs to be running
          files = [self.__audio_files[audiofile_id].get_full_path() for audiofile_id in playlist.get_files()]
          logger.info('Starting playlist %s for period start %s and end %s with %s/%s amount of files at volume %s' %
                        (playlist.get_name(),
                        playlist.get_start(),
                        playlist.get_stop(),
                        len(playlist.get_files()),
                        len(files),
                        playlist.get_volume())
                      )

          audio_player_command = ['cvlc','-q','--no-interact','--play-and-exit','--aout=alsa','--alsa-audio-device=hw:' + str(self.__hwid)]
          #audio_player_command += ['--norm-buff-size','1000','--norm-max-level','5.0']

          if playlist.get_shuffle():
            audio_player_command += ['-Z']

          if playlist.get_repeat():
            audio_player_command += ['-L']

          audio_player_command += files

          self.__audio_player = psutil.Popen(audio_player_command)
          playlist.set_started()
          self.__active_playlist = playlist
          self.mute(False)
          self.set_volume(playlist.get_volume())
          if self.__callback is not None:
            self.__callback(socket=True)

        elif self.is_running() and self.__active_playlist.get_id() == playlist.get_id() and not playlist.is_time() :
          logger.info('Stopping playlist %s' % (playlist.get_name(),))
          self.__audio_player.terminate()
          self.__active_playlist = None
          self.__audio_player = None
          self.mute()

          if self.__callback is not None:
            self.__callback(socket=True)

        else:
          logger.debug('No player action needed')

      duration = time.time() - starttime
      if duration < terrariumAudioPlayer.LOOP_TIMEOUT:
        logger.info('Update done in %.5f seconds. Waiting for %.5f seconds for next update' % (duration,terrariumAudioPlayer.LOOP_TIMEOUT - duration))
        sleep(terrariumAudioPlayer.LOOP_TIMEOUT - duration)
      else:
        logger.warning('Updating took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumAudioPlayer.LOOP_TIMEOUT,terrariumEngine.LOOP_TIMEOUT))

  @staticmethod
  def get_sound_cards():
    soundcards = {}
    for i in alsaaudio.card_indexes():
      try:
        (name, longname) = alsaaudio.card_name(i)
        soundcards[name] = {'hwid' : int(i), 'name' : longname}

      except Exception as ex:
        # Just ignore error, and skip it
        pass

    return soundcards

  def get_volume(self):
    return (int(self.__audio_mixer.getvolume()[0]) if self.__audio_mixer is not None else -1)

  def set_volume(self,value):
    if self.__audio_mixer is not None:
      try:
        value = int(value)
      except Exception as ex:
        value = -1

      if 0 <= value <= 100:
        oldvalue = self.get_volume()
        self.__audio_mixer.setvolume(value,alsaaudio.MIXER_CHANNEL_ALL)
        logger.info('Changed volume from %s to %s' % (oldvalue,self.get_volume()))

  def volume_up(self):
    if self.__audio_mixer is not None:
      volume = self.get_volume() + terrariumAudioPlayer.VOLUME_STEP
      if volume > 100:
        volume = 100

      self.set_volume(volume)

  def volume_down(self):
    if self.__audio_mixer is not None:
      volume = self.get_volume() - terrariumAudioPlayer.VOLUME_STEP
      if volume < 0:
        volume = 0

      self.set_volume(volume)

  def mute(self,mute = True):
    if self.__audio_mixer is not None:
      self.__audio_mixer.setmute(1 if mute else 0, alsaaudio.MIXER_CHANNEL_ALL)

  def reload_audio_files(self):
    self.__load_audio_files()

  def reload_playlists(self,data):
    self.__load_playlists(data)

  def get_audio_files(self):
    return self.__audio_files

  def get_playlists(self):
    return self.__playlists

  def get_current_state(self):
    if self.__audio_mixer is None or len(self.get_audio_files()) == 0 and len(self.get_playlists()) == 0:
      return {'running' : 'disabled'}

    data = {'running' : self.is_running()}

    if data['running'] and self.__active_playlist is not None:
      data.update(self.get_active_playlist().get_data())

    data['volume'] = self.get_volume()

    return data

  def is_running(self):
    running = False
    if self.__audio_mixer is not None:
      try:
        running = self.__audio_player.status() in ['running','sleeping','disk-sleep']
      except Exception as ex:
        pass

    return running

  def get_active_playlist(self):
    return self.__active_playlist

class terrariumAudioPlaylist(object):

  def __init__(self, id, name = None, start = None, stop = None, volume = None, repeat = False, shuffle = False, files = None):
    self.__id = id
    self.__name = None
    self.__start = None
    self.__stop = None
    self.__volume = None
    self.__repeat = False
    self.__shuffle = False
    self.__files = []
    self.__is_started_at = None
    self.__timer_time_table = []

    self.set_name(name)
    self.set_start(start)
    self.set_stop(stop)
    self.set_volume(volume)
    self.set_repeat(repeat)
    self.set_shuffle(shuffle)
    self.set_files(files)

  def __calculate_time_table(self):
    self.__timer_time_table = []
    if self.get_start() is None or self.get_stop() is None:
      return

    logger.info('Calculating autioplaylist \'%s\' with timer data: start = %s, stop = %s',
      self.get_name(),
      self.get_start(),
      self.get_stop())

    duration_on = None
    if not self.get_repeat():
      duration_on = int(self.get_songs_duration()/60)

    self.__timer_time_table = terrariumUtils.calculate_time_table(self.get_start(),
                                                                  self.get_stop(),
                                                                  duration_on)
    logger.info('Timer time table loaded for autioplaylist \'%s\' with %s entries.', self.get_name(),len(self.__timer_time_table))

  def get_id(self):
    return self.__id

  def set_name(self,value):
    self.__name = value

  def get_name(self):
    return self.__name

  def set_start(self,value):
    self.__start = terrariumUtils.parse_time(value)
    self.__calculate_time_table()

  def get_start(self):
    return self.__start

  def set_stop(self,value):
    self.__stop = terrariumUtils.parse_time(value)
    self.__calculate_time_table()

  def get_stop(self):
    return self.__stop

  def set_volume(self,value):
    self.__volume = value

  def get_volume(self):
    return self.__volume

  def set_files(self,value):
    self.__files = value

  def get_files(self):
    return self.__files

  def set_repeat(self,repeat = True):
    self.__repeat = terrariumUtils.is_true(repeat)

  def get_repeat(self):
    return self.__repeat == True

  def set_shuffle(self,shuffle = True):
    self.__shuffle = terrariumUtils.is_true(shuffle)

  def get_shuffle(self):
    return self.__shuffle == True

  def set_started(self):
    self.__is_started_at = int(time.time())

  def is_time(self):
    logger.debug('Checking timer time table for switch %s with %s entries.', self.get_name(),len(self.__timer_time_table))
    is_time = terrariumUtils.is_time(self.__timer_time_table)

    if is_time is None:
      self.__calculate_time_table()
      is_time = False

    logger.debug('Timer action is done for switch %s. Is it time to play?: %s.', self.get_name(),('Yes' if is_time else 'Nope'))
    return is_time

  def get_duration(self):
    return terrariumUtils.duration(self.__timer_time_table)

  def get_songs_duration(self):
    return 0.0 + sum(self.__files[fileid].get_track_duration() for fileid in self.__files)

  def has_files(self):
    return len(self.__files) > 0

  def get_data(self):
    data = {'id'      : self.get_id(),
            'name'    : self.get_name(),
            'start'   : self.get_start(),
            'stop'    : self.get_stop(),
            'volume'  : self.get_volume(),
            'files'   : list(self.get_files().keys()),
            'repeat'  : self.get_repeat(),
            'shuffle' : self.get_shuffle(),
            'is_time' : self.is_time(),
            'duration': self.get_duration(),
            'songs_duration': self.get_songs_duration()
            }

    return data

class terrariumAudioFile(object):

  META_FIELDS = ['Format','Duration','Overall bit rate mode','Overall bit rate','Album','Track name','Format profile','Channel(s)','Sampling rate']
  VALID_EXTENSION = terrariumAudioPlayer.VALID_EXTENSION

  def __init__(self,filename):
    self.id = None
    self.full_filename = None
    self.name = None
    self.extension = None
    self.file_size = 0
    self.upload_date = None
    self.meta_data = {}

    if os.path.isfile(filename):
      self.full_filename = filename
      self.name = os.path.basename(self.get_full_path())
      self.extension = os.path.splitext(self.get_full_path())[1][1:].lower()
      self.file_size = os.path.getsize(self.get_full_path())
      self.upload_date = os.path.getmtime(self.get_full_path())

      self.id = md5(b'' + self.get_full_path()).hexdigest()
      self.__load_meta_data()

  def __load_meta_data(self):
    meta_data_cache_file = self.full_filename + '.meta'

    if not os.path.isfile(meta_data_cache_file):
      media_info = MediaInfo()
      media_info.Open(self.get_full_path())
      data = media_info.Inform().split("\n")

      for line in data:
        line = line.strip().split(':')
        if line[0].strip() in terrariumAudioFile.META_FIELDS:
          field = line[0].strip().replace(' ','').replace('(s)','s').lower()
          value = line[1].strip()
          if 'duration' == field:
            value = media_info.Get(Stream.Audio, 0, "Duration")

          self.meta_data[field] = value

      media_info.Close()

      if len(self.meta_data) > 0:
        with open(meta_data_cache_file, 'wb') as datafile:
          json.dump(self.meta_data, datafile)

    else:
      with open(meta_data_cache_file) as datafile:
        self.meta_data = json.load(datafile)

  def delete(self):
    if os.path.isfile(self.get_full_path() + '.meta'):
      os.unlink(self.get_full_path() + '.meta')

    if os.path.isfile(self.get_full_path()):
      os.unlink(self.get_full_path())
      return True

    return False

  def get_id(self):
    return self.id

  def get_full_path(self):
    return self.full_filename

  def get_name(self):
    return self.name

  def get_extension(self):
    return self.extension

  def get_file_size(self):
    return self.file_size

  def get_upload_date(self):
    return self.upload_date

  def get_track_name(self):
    return self.meta_data['trackname'] if 'trackname' in self.meta_data else None

  def get_track_album(self):
    return self.meta_data['album'] if 'album' in self.meta_data else None

  def get_track_duration(self):
    return int(self.meta_data['duration'])/1000 if 'duration' in self.meta_data else 0

  def get_track_bitrate(self):
    return self.meta_data['overallbitrate'] if 'overallbitrate' in self.meta_data else None

  def get_track_bitrate_type(self):
    return self.meta_data['overallbitratemode'] if 'overallbitratemode' in self.meta_data else None

  def get_track_channels(self):
    return self.meta_data['channels'] if 'channels' in self.meta_data else None

  def get_track_frequency(self):
    return self.meta_data['samplingrate'] if 'samplingrate' in self.meta_data else None

  def get_data(self):
    data = {'id' : self.get_id(),
            'name' : self.get_name(),
            'extension' : self.get_extension(),
            'path' : self.get_full_path(),
            'size' : self.get_file_size(),
            'uploaddate' : self.get_upload_date(),
            'trackname' : self.get_track_name(),
            'trackalbum' : self.get_track_album(),
            'trackduration' : self.get_track_duration(),
            'trackbitrate' : self.get_track_bitrate(),
            'trackbitratetype' : self.get_track_bitrate_type(),
            'trackchannels' : self.get_track_channels(),
            'trackfrequency' : self.get_track_frequency(),
          }

    return data
