# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import thread
import datetime
import time
import psutil
import os
import json
import alsaaudio

from hashlib import md5
from MediaInfoDLL import MediaInfo, Stream

from gevent import monkey, sleep
monkey.patch_all()

class terrariumAudioPlayer():

  AUDIO_FOLDER = 'audio'
  VALID_EXTENSION = ['mp3','m4a','ogg']
  LOOP_TIMEOUT = 30

  def __init__(self,config,callback=None):
    self.__config = config
    self.__callback = callback
    self.__audio_player = None
    self.__audio_mixer = None
    self.__load_audio_files()
    self.__load_playlists()
    self.__load_audio_mixer()
    logger.info('Player loaded with %s audio files and %s playlists. Starting engine.' % (len(self.__audio_files),len(self.__playlists)))
    thread.start_new_thread(self.__engine_loop, ())

  def __load_audio_files(self):
    self.__audio_files = {}
    for audiofilename in os.listdir(terrariumAudioPlayer.AUDIO_FOLDER):
      if os.path.splitext(audiofilename)[1][1:].lower() in terrariumAudioPlayer.VALID_EXTENSION:
        audiofile = terrariumAudioFile(os.path.join(terrariumAudioPlayer.AUDIO_FOLDER,audiofilename))
        if audiofile.get_id() is not None:
          self.__audio_files[audiofile.get_id()] = audiofile

  def __load_playlists(self):
    self.__playlists = {}
    data = self.__config.get_audio_playlists()
    for audio_playlist_id in data:
      playlist = terrariumAudioPlaylist(data[audio_playlist_id]['id'],
                                        data[audio_playlist_id]['name'],
                                        data[audio_playlist_id]['start'],
                                        data[audio_playlist_id]['stop'],
                                        data[audio_playlist_id]['volume'],
                                        data[audio_playlist_id]['files'])

      self.__playlists[playlist.get_id()] = playlist

  def __load_audio_mixer(self):
    self.__audio_mixer = alsaaudio.Mixer('PCM')
    self.mute()

  def __engine_loop(self):
    self.__current_playlist = None
    while True:
      starttime = time.time()
      for audio_playlist_id in self.__playlists:
        playlist = self.__playlists[audio_playlist_id]
        if playlist.is_time() and playlist.has_files() and not self.is_running():
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

          self.__audio_player = psutil.Popen(['cvlc','-q','--no-interact', '-L','--norm-buff-size=','1000','--norm-max-level','5.0'] + files)
          self.__active_playlist = playlist
          self.mute(False)
          self.set_volume(playlist.get_volume())
          if self.__callback is not None:
            self.__callback(socket=True)

        elif self.is_running() and self.__active_playlist.get_id() == playlist.get_id() and not playlist.is_time() :
          logger.info('Stopping playlist %s' % (playlist.get_name(),))
          self.__audio_player.terminate()
          self.__active_playlist = None
          self.mute()
          if self.__callback is not None:
            self.__callback(socket=True)

        else:
          logger.debug('No player action needed')

      duration = time.time() - starttime
      if duration < terrariumAudioPlayer.LOOP_TIMEOUT:
        logger.info('Engine loop done in %.5f seconds. Waiting for %.5f seconds for next round' % (duration,terrariumAudioPlayer.LOOP_TIMEOUT - duration))
        sleep(terrariumAudioPlayer.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        logger.warning('Engine took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumAudioPlayer.LOOP_TIMEOUT,terrariumEngine.LOOP_TIMEOUT))

  def get_volume(self):
    return int(self.__audio_mixer.getvolume()[0])

  def set_volume(self,value):
    try:
      value = int(value)
    except Exception, ex:
      pass

    if 0 <= value <= 100:
      self.__audio_mixer.setvolume(value,alsaaudio.MIXER_CHANNEL_ALL)

  def mute(self,mute = True):
    self.__audio_mixer.setmute(1 if mute else 0, alsaaudio.MIXER_CHANNEL_ALL)

  def reload_audio_files(self):
    self.__load_audio_files()

  def reload_playlists(self):
    self.__load_playlists()

  def get_audio_files(self):
    return self.__audio_files

  def get_playlists(self):
    return self.__playlists

  def get_current_state(self):
    data = {'running' : self.is_running()}

    if data['running'] and self.__active_playlist is not None:
      data.update(self.get_active_playlist().get_data())

    return data

  def is_running(self):
    if self.__audio_player is not None:
      print self.__audio_player.status()

    return self.__audio_player is not None and self.__audio_player.status() in ['running','sleeping']

  def get_active_playlist(self):
    return self.__active_playlist

class terrariumAudioPlaylist():

  def __init__(self,id,name = None,start = None,stop = None,volume = None,files = None):
    self.__id = id
    self.__name = None
    self.__start = None
    self.__stop = None
    self.__volume = None
    self.__files = None

    self.set_name(name)
    self.set_start(start)
    self.set_stop(stop)
    self.set_volume(volume)
    self.set_files(files)

  def __calculate_start_stop_times(self):
    now = datetime.datetime.now()
    on = None
    off = None

    if self.__start is not None:
      on = datetime.datetime.fromtimestamp(self.__start).replace(year=int(now.strftime('%Y')),
                                                                 month=int(now.strftime('%m')),
                                                                 day=int(now.strftime('%d')))

    if self.__stop is not None:
      off = datetime.datetime.fromtimestamp(self.__stop).replace(year=int(now.strftime('%Y')),
                                                                 month=int(now.strftime('%m')),
                                                                 day=int(now.strftime('%d')))
    if on is not None and off is not None and on > off:
      if now > off:
        off += datetime.timedelta(hours=24)
      else:
        on -= datetime.timedelta(hours=24)

    return {'on':on,'off':off}

  def get_id(self):
    return self.__id

  def set_name(self,value):
    self.__name = value

  def get_name(self):
    return self.__name

  def set_start(self,value):
    self.__start = value

  def get_start(self):
    return self.__calculate_start_stop_times()['on']

  def set_stop(self,value):
    self.__stop = value

  def get_stop(self):
    return self.__calculate_start_stop_times()['off']

  def set_volume(self,value):
    self.__volume = value

  def get_volume(self):
    return self.__volume

  def set_files(self,value):
    if not isinstance(value,list):
      value = value.split(',')

    self.__files = value

  def get_files(self):
    return self.__files

  def is_time(self):
    return self.get_start() < datetime.datetime.now() < self.get_stop()

  def get_duration(self):
    return (self.get_stop() - self.get_start()).total_seconds()

  def has_files(self):
    return len(self.__files) > 0

  def get_data(self):
    data = {'id'      : self.get_id(),
            'name'    : self.get_name(),
            'start'   : time.mktime(self.get_start().timetuple()),
            'stop'    : time.mktime(self.get_stop().timetuple()),
            'volume'  : self.get_volume(),
            'files'   : self.get_files(),
            'is_time' : self.is_time()
            }

    return data

class terrariumAudioFile():

  META_FIELDS = ['Format','Duration','Overall bit rate mode','Overall bit rate','Album','Track name','Format profile','Channel(s)','Sampling rate']
  VALID_EXTENSION = ['mp3','m4a','ogg']

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
