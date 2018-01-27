# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import ConfigParser
from glob import glob

from terrariumUtils import terrariumUtils

class terrariumConfig:
  DEFAULT_CONFIG = 'defaults.cfg'
  CUSTOM_CONFIG = 'settings.cfg'

  '''Class for loading the configuration for terrariumPI software.
     The configuration is based on two configuration files.
     - default.cfg holds system defaults for first run
     - settigs.cfg holds the user defined config files

     So the default.cfg file is read first, and overwritten by the settings
     from the settings.cfg file.

     Changes will always be written to settings.cfg.'''

  def __init__(self):
    '''Load terrariumPI config object'''
    logger.info('Setting up configuration')
    self.__cache_available_languages = None

    self.__config = ConfigParser.SafeConfigParser()
    # Read defaults config file
    self.__config.readfp(open(terrariumConfig.DEFAULT_CONFIG))
    logger.info('Loaded default settings from %s' % (terrariumConfig.DEFAULT_CONFIG,))

    # Read new version number
    version = self.get_system()['version']
    # Read custom config file
    self.__config.read(terrariumConfig.CUSTOM_CONFIG)
    logger.info('Loaded custom settings from %s' % (terrariumConfig.CUSTOM_CONFIG,))
    # Upgrade config and save new version number
    self.__upgrade_config(version)
    logger.info('TerrariumPI Config is ready')

  # Private functions
  def __upgrade_config(self,to_version):
    # Set minimal version to 3.0.0
    current_version = 300
    new_version = int(to_version.replace('.',''))
    if int(self.get_system()['version'].replace('.','')) >= current_version:
      current_version = int(self.get_system()['version'].replace('.',''))

    if not current_version < new_version:
      logger.info('Configuration is up to date')
    else:
      logger.info('Configuration is out of date. Running updates from %s to %s' % (current_version,new_version))
      for version in xrange(current_version+1,new_version+1):
        if version == 300:
          logger.info('Updating configuration file to version: %s' % (version,))
          # Upgrade: Move temperature indicator from weather to system
          temperature_indicator = self.__get_config('weather')
          if 'temperature' in temperature_indicator:
            self.__config.set('terrariumpi', 'temperature_indicator', str(temperature_indicator['temperature']))
            self.__config.remove_option('weather','temperature')

          # Upgrade: Change profile image path to new path and config location
          data = self.__get_config('terrariumpi')
          if 'image' in data and '/static/images/gecko.jpg' == data['image']:
            self.__config.set('profile', 'image', '/static/images/profile_image.jpg')
            self.__config.remove_option('terrariumpi','image')

          # Upgrade: Change profile name path to new config location
          data = self.__get_config('terrariumpi')
          if 'person' in data:
            self.__config.set('profile', 'name', data['person'])
            self.__config.remove_option('terrariumpi','person')

          # Upgrade: Remove default available languages variable
          data = self.__get_config('terrariumpi')
          if 'available_languages' in data:
            self.__config.remove_option('terrariumpi','available_languages')

        elif version == 310:
          logger.info('Updating configuration file to version: %s' % (version,))
          # Upgrade: Rename active_language to just language
          data = self.__get_config('terrariumpi')
          if 'active_language' in data:
            self.__config.set('terrariumpi', 'language', data['active_language'])
            self.__config.remove_option('terrariumpi','active_language')

          # Update the GPIO pinnumbering for PWM dimmers and DHT like sensors
          for section in self.__config.sections():
            if section[:6] == 'sensor':
              sensor_data = self.__get_config(section)
              if 'dht' in sensor_data['hardwaretype'] or 'am2302' == sensor_data['hardwaretype']:
                self.__config.set(section, 'address', str(terrariumUtils.to_BOARD_port_number(sensor_data['address'])))

            if section[:6] == 'switch':
              switch_data = self.__get_config(section)
              if 'pwm-dimmer' == switch_data['hardwaretype']:
                self.__config.set(section, 'address', str(terrariumUtils.to_BOARD_port_number(switch_data['address'])))

        elif version == 312:
          logger.info('Updating configuration file to version: %s' % (version,))
          data = self.__get_config('terrariumpi')
          if 'soundcard' in data and data['soundcard'] == '0':
            self.__config.set('terrariumpi', 'soundcard', 'bcm2835 ALSA')

      # Update version number
      self.__config.set('terrariumpi', 'version', str(to_version))
      self.__save_config()
      self.__config.read(terrariumConfig.CUSTOM_CONFIG)
      logger.info('Updated configuration. Set version to: %s' % (to_version,))

  def __reload_config(self):
    self.__config.read(terrariumConfig.CUSTOM_CONFIG)

  def __save_config(self):
    '''Write terrariumPI config to settings.cfg file'''
    with open(terrariumConfig.CUSTOM_CONFIG, 'wb') as configfile:
      self.__config.write(configfile)

    return True

  def __update_config(self,section,data):
    '''Update terrariumPI config with new values

    Keyword arguments:
    section -- section in configuration. If not exists it will be created
    data -- data to save in dict form'''

    if not self.__config.has_section(section):
      self.__config.add_section(section)

    keys = data.keys()
    keys.sort()
    for setting in keys:
      if type(data[setting]) is list:
        data[setting] = ','.join(data[setting])

      if isinstance(data[setting], basestring):
        try:
          data[setting] = data[setting].encode('utf-8')
        except Exception, ex:
          'Not sure what to do... but it seams already utf-8...??'
          pass

      self.__config.set(section, str(setting), str(data[setting]))

    config_ok = self.__save_config()
    if config_ok:
      self.__reload_config()

    return config_ok

  def __get_config(self,section):
    '''Get terrariumPI config based on section. Return empty dict when not exists
    Keyword arguments:
    section -- section to read from the config'''

    config = {}
    if not self.__config.has_section(section):
      return config

    for config_part in self.__config.items(section):
      config[config_part[0]] = config_part[1]

    return config
  # End private functions

  def get_system(self):
    '''Get terrariumPI configuration section 'terrariumpi'
    '''
    data = self.__get_config('terrariumpi')
    data['available_languages'] = self.get_available_languages()
    return data

  def set_system(self,data):
    '''Set terrariumPI configuration section 'terrariumpi'

    Make sure that the fields cur_password and new_password are never stored
    '''
    if 'cur_password' in data:
      del(data['cur_password'])
    if 'new_password' in data:
      del(data['new_password'])
    if 'available_languages' in data:
      del(data['available_languages'])
    return self.__update_config('terrariumpi',data)

  def get_pi_power_wattage(self):
    '''Get terrariumPI power usage'''
    config = self.get_system()
    return float(config['power_usage'])

  def get_admin(self):
    '''Get terrariumPI admin name'''
    config = self.get_system()
    return config['admin']

  def get_password(self):
    '''Get terrariumPI admin password'''
    config = self.get_system()
    return config['password']

  def get_available_languages(self):
    '''Get terrariumPI available languages'''
    if self.__cache_available_languages is None:
      self.__cache_available_languages = [language.replace('locales/','').replace('/','') for language in glob("locales/*/")]

    return self.__cache_available_languages

  def get_language(self):
    '''Get terrariumPI language'''
    config = self.get_system()
    if 'language' not in config:
      config['language'] = self.get_available_languages()[0]

    return config['language']

  def get_power_price(self):
    '''Get terrariumPI power price. Price is entered as euro/kWh'''
    config = self.get_system()
    return float(config['power_price'])

  def get_water_price(self):
    '''Get terrariumPI water price. Price is entered as euro/m3'''
    config = self.get_system()
    return float(config['water_price'])

  def get_temperature_indicator(self):
    config = self.get_system()
    return config['temperature_indicator'].upper()

  def get_active_soundcard(self):
    config = self.get_system()
    return config['soundcard']

  # Environment functions
  def save_environment(self,data):
    '''Save the terrariumPI environment config

    '''
    config = {}
    for environment_part in data:
      for part in data[environment_part]:
        if data[environment_part][part] is None:
          data[environment_part][part] = ''
        config[environment_part + '_' + part] = data[environment_part][part]

    return self.__update_config('environment',config)

  def get_environment(self):
    config = self.__get_config('environment')
    data = {'light' : {}, 'sprayer' : {}, 'heater' : {} , 'cooler' : {}}
    for key in config:
      config_keys = key.split('_')
      part = config_keys[0]
      del(config_keys[0])
      data[part]['_'.join(config_keys)] = config[key]

    return data
  # End Environment functions

  # Profile functions
  def get_profile(self):
    return self.__get_config('profile')

  def get_profile_image(self):
    config = self.get_profile()
    return config['image']

  def get_profile_name(self):
    config = self.get_profile()
    return config['name']

  def save_profile(self,data):
    return self.__update_config('profile',data)
  # End profile functions


  # Weather config functions
  def save_weather(self,data):
    if 'type' in data:
      del(data['type'])
    return self.__update_config('weather',data)

  def get_weather(self):
    return self.__get_config('weather')

  def get_weather_location(self):
    data = self.get_weather()
    return data['location'] if 'location' in data else None

  def get_weather_windspeed(self):
    data = self.get_weather()
    return data['windspeed'] if 'windspeed' in data else None
  # End weather config functions


  # Sensor config functions
  def get_owfs_port(self):
    return int(self.get_system()['owfs_port'])

  def save_sensor(self,data):
    # Upgrade step
    if 'min' in data:
      data['limit_min'] = data['min']
      del(data['min'])

    if 'max' in data:
      data['limit_max'] = data['max']
      del(data['max'])

    del(data['current'])
    return self.__update_config('sensor' + str(data['id']),data)

  def save_sensors(self,data):
    update_ok = True
    for sensorid in self.get_sensors():
      self.__config.remove_section('sensor' + sensorid)

    for sensorid in data:
      update_ok = update_ok and self.save_sensor(data[sensorid].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_sensors(self):
    data = {}
    for section in self.__config.sections():
      if section[:6] == 'sensor':
        sensor_data = self.__get_config(section)
        data[section[6:]] = sensor_data

    # Upgrade step
    if 'min' in data:
      data['limit_min'] = data['min']
      del(data['min'])

    if 'max' in data:
      data['limit_max'] = data['max']
      del(data['max'])

    return data
  # End sensor config functions


  # Switches config functions
  def save_power_switch(self,data):
    if 'state' in data:
      del(data['state'])

    if 'current_power_wattage' in data:
      del(data['current_power_wattage'])

    if 'current_water_flow' in data:
      del(data['current_water_flow'])

    if data['hardwaretype'] != 'pwm-dimmer':
      if 'dimmer_duration' in data:
        del(data['dimmer_duration'])

      if 'dimmer_off_duration' in data:
        del(data['dimmer_off_duration'])

      if 'dimmer_off_percentage' in data:
        del(data['dimmer_off_percentage'])

      if 'dimmer_on_duration' in data:
        del(data['dimmer_on_duration'])

      if 'dimmer_on_percentage' in data:
        del(data['dimmer_on_percentage'])

    return self.__update_config('switch' + str(data['id']),data)

  def save_power_switches(self,data):
    update_ok = True
    for power_switch in self.get_power_switches():
      self.__config.remove_section('switch' + power_switch['id'])

    for power_switch_id in data:
      update_ok = update_ok and self.save_power_switch(data[power_switch_id].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_power_switches(self):
    data = []
    for section in self.__config.sections():
      if section[:6] == 'switch':
        switch_data = self.__get_config(section)
        data.append(switch_data)

    return data
  # End switches config functions

  # Door config functions
  def save_door(self,data):
    if 'state' in data:
      del(data['state'])

    return self.__update_config('door' + str(data['id']),data)

  def save_doors(self,data):
    update_ok = True
    for door_id in self.get_doors():
      self.__config.remove_section('door' + door_id)

    for door_id in data:
      update_ok = update_ok and self.save_door(data[door_id].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_doors(self):
    data = {}
    for section in self.__config.sections():
      if section[:4] == 'door':
        door_data = self.__get_config(section)
        data[section[4:]] = door_data

    return data
  # End door config functions


  # Webcam config functions
  def save_webcam(self,data):
    del(data['state'])
    del(data['image'])
    del(data['max_zoom'])
    del(data['last_update'])
    del(data['resolution'])
    del(data['preview'])
    return self.__update_config('webcam' + str(data['id']),data)

  def save_webcams(self,data):
    update_ok = True
    for webcam_id in self.get_webcams():
      self.__config.remove_section('webcam' + webcam_id)

    for webcam_id in data:
      update_ok = update_ok and self.save_webcam(data[webcam_id].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_webcams(self):
    data = {}
    for section in self.__config.sections():
      if section[:6] == 'webcam':
        sensor_data = self.__get_config(section)
        data[section[6:]] = sensor_data

    return data
  # End webcam config functions

  # Audio playlist config functions
  def save_audio_playlist(self,data):
    if 'running' in data:
      del(data['running'])

    return self.__update_config('playlist' + str(data['id']),data)

  def save_audio_playlists(self,data):
    update_ok = True
    for audio_playlist_id in self.get_audio_playlists():
      self.__config.remove_section('playlist' + audio_playlist_id)

    for audio_playlist_id in data:
      update_ok = update_ok and self.save_audio_playlist(data[audio_playlist_id])

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_audio_playlists(self):
    data = {}
    for section in self.__config.sections():
      if section[:8] == 'playlist':
        audio_playlist_data = self.__get_config(section)
        audio_playlist_data['start'] = int(audio_playlist_data['start'])
        audio_playlist_data['stop'] = int(audio_playlist_data['stop'])
        audio_playlist_data['files'] = audio_playlist_data['files'].split(',') if audio_playlist_data['files'] is not None else []
        audio_playlist_data['volume'] = int(audio_playlist_data['volume'])
        audio_playlist_data['repeat'] = audio_playlist_data['repeat'] in [True,1,'True','true','1','on']
        audio_playlist_data['shuffle'] = audio_playlist_data['shuffle'] in [True,1,'True','true','1','on']
        data[section[8:]] = audio_playlist_data

    return data
  # End audio playlist config functions
