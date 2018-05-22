# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import ConfigParser
from glob import glob
import datetime

from terrariumUtils import terrariumUtils

class terrariumConfig(object):
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

        elif version == 330:
          logger.info('Updating configuration file to version: %s' % (version,))
          for section in self.__config.sections():
            if section[:8] == 'playlist':
              playlist_data = self.__get_config(section)
              self.__config.set(section, 'start', str(datetime.datetime.fromtimestamp(float(playlist_data['start'])).strftime('%H:%M')))
              self.__config.set(section, 'stop',  str(datetime.datetime.fromtimestamp(float(playlist_data['stop'])).strftime('%H:%M')))

            if section == 'environment':
              environment_data = self.__get_config(section)
              self.__config.set(section, 'light_on',  str(datetime.datetime.fromtimestamp(float(environment_data['light_on'])).strftime('%H:%M')))
              self.__config.set(section, 'light_off', str(datetime.datetime.fromtimestamp(float(environment_data['light_off'])).strftime('%H:%M')))
              self.__config.set(section, 'heater_on',  str(datetime.datetime.fromtimestamp(float(environment_data['heater_on'])).strftime('%H:%M')))
              self.__config.set(section, 'heater_off', str(datetime.datetime.fromtimestamp(float(environment_data['heater_off'])).strftime('%H:%M')))
              self.__config.set(section, 'cooler_on',  str(datetime.datetime.fromtimestamp(float(environment_data['cooler_on'])).strftime('%H:%M')))
              self.__config.set(section, 'cooler_off', str(datetime.datetime.fromtimestamp(float(environment_data['cooler_off'])).strftime('%H:%M')))

        elif version == 351:
          logger.info('Updating configuration file to version: %s' % (version,))
          for section in self.__config.sections():
            if section[:6] == 'webcam':
              data = self.__get_config(section)
              if 'archive' in data:
                self.__config.set(section, 'archive', 'motion' if terrariumUtils.is_true(data['archive']) else 'disabled')

        elif version == 360:
          logger.info('Updating configuration file to version: %s' % (version,))
          for section in self.__config.sections():
            if section == 'environment':
              data = self.__get_config(section)
              newdata = {}

              if 'temperature_mode' not in newdata:
                newdata['temperature_mode'] = 'weatherinverse' if data['cooler_mode'] == 'weather' else data['cooler_mode']
                if 'cooler_night_difference' in data:
                  newdata['temperature_day_night_difference'] = data['cooler_night_difference']
                if 'cooler_night_source' in data:
                  newdata['temperature_day_night_source'] = data['cooler_night_source']
                if 'cooler_sensors' in data:
                  newdata['temperature_sensors'] = data['cooler_sensors']

              if 'cooler_night_enabled' in data:
                newdata['temperature_alarm_max_light_state'] = 'always' if terrariumUtils.is_true(data['cooler_night_enabled']) else 'off'

              if 'cooler_power_switches' in data:
                newdata['temperature_alarm_max_powerswitches'] = data['cooler_power_switches']

              if 'cooler_settle_timeout' in data:
                newdata['temperature_alarm_max_settle'] = data['cooler_settle_timeout']

              if 'cooler_off_duration' in data:
                newdata['temperature_alarm_max_timer_off'] = data['cooler_off_duration']

              if 'cooler_on_duration' in data:
                newdata['temperature_alarm_max_timer_on'] = data['cooler_on_duration']

              if 'cooler_on' in data:
                newdata['temperature_alarm_max_timer_start'] = data['cooler_on']

              if 'cooler_off' in data:
                newdata['temperature_alarm_max_timer_stop'] = data['cooler_off']

              if 'temperature_mode' not in newdata:
                newdata['temperature_mode'] = 'weatherinverse' if data['heater_mode'] == 'weather' else data['heater_mode']

              if 'temperature_day_night_difference' in newdata and newdata['temperature_day_night_difference'] != '':
                newdata['temperature_day_night_difference'] = (float(newdata['temperature_day_night_difference']) + float(data['heater_night_difference'])) / 2.0
              else:
                newdata['temperature_day_night_difference'] = data['heater_night_difference']

              if 'temperature_day_night_source' not in newdata or newdata['temperature_day_night_source'] == '':
                newdata['temperature_day_night_source'] = data['heater_night_source']

              if 'temperature_sensors' in newdata and newdata['temperature_sensors'] != '':
                newdata['temperature_sensors'] += ',' + data['heater_sensors']
              else:
                newdata['temperature_sensors'] = data['heater_sensors']

              if 'heater_day_enabled' in data:
                newdata['temperature_alarm_min_light_state'] = 'always' if terrariumUtils.is_true(data['heater_day_enabled']) else 'off'

              if 'heater_power_switches' in data:
                newdata['temperature_alarm_min_powerswitches'] = data['heater_power_switches']

              if 'heater_settle_timeout' in data:
                newdata['temperature_alarm_min_settle'] = data['heater_settle_timeout']

              if 'heater_off_duration' in data:
                newdata['temperature_alarm_min_timer_off'] = data['heater_off_duration']

              if 'heater_on_duration' in data:
                newdata['temperature_alarm_min_timer_on'] = data['heater_on_duration']

              if 'heater_on' in data:
                newdata['temperature_alarm_min_timer_start'] = data['heater_on']

              if 'heater_off' in data:
                newdata['temperature_alarm_min_timer_stop'] = data['heater_off']

              newdata['light_mode'] = data['light_mode']
              newdata['light_min_hours'] = data['light_min_hours']
              newdata['light_max_hours'] = data['light_max_hours']
              newdata['light_hours_shift'] = data['light_hours_shift']

              newdata['light_alarm_min_powerswitches'] = data['light_power_switches']

              newdata['light_alarm_min_timer_start'] = data['light_on']
              newdata['light_alarm_min_timer_stop'] = data['light_off']
              newdata['light_alarm_min_timer_on'] = data['light_on_duration']
              newdata['light_alarm_min_timer_off'] = data['light_off_duration']

              newdata['moisture_mode'] = data['moisture_mode']
              newdata['moisture_sensors'] = data['moisture_sensors']

              newdata['moisture_alarm_min_powerswitches'] = data['moisture_power_switches']
              newdata['moisture_alarm_min_timer_start'] = data['moisture_on']
              newdata['moisture_alarm_min_timer_stop'] = data['moisture_off']
              newdata['moisture_alarm_min_timer_on'] = data['moisture_on_duration']
              newdata['moisture_alarm_min_timer_off'] = data['moisture_off_duration']

              newdata['moisture_alarm_min_duration_on'] = data['moisture_spray_duration']
              newdata['moisture_alarm_min_settle'] = data['moisture_spray_timeout']

              newdata['moisture_alarm_min_light_state'] = 'always' if terrariumUtils.is_true(data['moisture_night_enabled']) else 'off'

              newdata['ph_mode'] = data['ph_mode']
              newdata['ph_sensors'] = data['ph_sensors']

              newdata['ph_alarm_min_powerswitches'] = data['ph_power_switches']
              newdata['ph_alarm_min_timer_start'] = data['ph_on']
              newdata['ph_alarm_min_timer_stop'] = data['ph_off']
              newdata['ph_alarm_min_timer_on'] = data['ph_on_duration']
              newdata['ph_alarm_min_timer_off'] = data['ph_off_duration']

              newdata['ph_alarm_min_settle'] = data['ph_settle_timeout']

              newdata['ph_alarm_min_light_state'] = 'always' if terrariumUtils.is_true(data['ph_day_enabled']) else 'off'

              newdata['humidity_mode'] = data['sprayer_mode']
              newdata['humidity_sensors'] = data['sprayer_sensors']

              newdata['humidity_alarm_min_powerswitches'] = data['sprayer_power_switches']
              newdata['humidity_alarm_min_timer_start'] = data['sprayer_on']
              newdata['humidity_alarm_min_timer_stop'] = data['sprayer_off']
              newdata['humidity_alarm_min_timer_on'] = data['sprayer_on_duration']
              newdata['humidity_alarm_min_timer_off'] = data['sprayer_off_duration']

              newdata['humidity_alarm_min_duration_on'] = data['sprayer_spray_duration']
              newdata['humidity_alarm_min_settle'] = data['sprayer_spray_timeout']

              newdata['humidity_alarm_min_light_state'] = 'always' if terrariumUtils.is_true(data['sprayer_night_enabled']) else 'off'

              newdata['watertank_mode'] = data['watertank_mode']
              newdata['watertank_sensors'] = data['watertank_sensors']
              newdata['watertank_height'] = data['watertank_height']
              newdata['watertank_volume'] = data['watertank_volume']

              newdata['watertank_alarm_min_powerswitches'] = data['watertank_power_switches']
              newdata['watertank_alarm_min_timer_start'] = data['watertank_on']
              newdata['watertank_alarm_min_timer_stop'] = data['watertank_off']
              newdata['watertank_alarm_min_timer_on'] = data['watertank_on_duration']
              newdata['watertank_alarm_min_timer_off'] = data['watertank_off_duration']

              newdata['watertank_alarm_min_duration_on'] = data['watertank_pump_duration']

              self.save_environment(newdata)
              break

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

  def __update_config(self,section,data,exclude = []):
    '''Update terrariumPI config with new values

    Keyword arguments:
    section -- section in configuration. If not exists it will be created
    data -- data to save in dict form'''

    if not self.__config.has_section(section):
      self.__config.add_section(section)

    keys = data.keys()
    keys.sort()
    for setting in keys:
      if setting in exclude:
        continue

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

  def __get_all_config(self,part):
    data = []
    for section in self.__config.sections():
      if section[:len(part)] == part:
        data.append(self.__get_config(section))

    return data

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
    return self.__update_config('terrariumpi',data,['cur_password','new_password','available_languages','location','windspeed'])

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

  def get_weather_location(self):
    data = self.get_weather()
    return data['location'] if 'location' in data else None

  def get_weather_windspeed(self):
    data = self.get_weather()
    return data['windspeed'] if 'windspeed' in data else None

  def get_temperature_indicator(self):
    config = self.get_system()
    return config['temperature_indicator']

  def get_distance_indicator(self):
    config = self.get_system()
    return config['distance_indicator']

  def get_admin(self):
    '''Get terrariumPI admin name'''
    config = self.get_system()
    return config['admin']

  def get_password(self):
    '''Get terrariumPI admin password'''
    config = self.get_system()
    return config['password']

  def get_active_soundcard(self):
    config = self.get_system()
    return config['soundcard']

  def get_external_calender_url(self):
    config = self.get_system()
    if 'external_calendar_url' in config and config['external_calendar_url'] != '':
      return config['external_calendar_url']

    return ''

  def get_pi_power_wattage(self):
    '''Get terrariumPI power usage'''
    config = self.get_system()
    return float(config['power_usage'])

  def get_power_price(self):
    '''Get terrariumPI power price. Price is entered as euro/kWh'''
    config = self.get_system()
    return float(config['power_price'])

  def get_water_price(self):
    '''Get terrariumPI water price. Price is entered as euro/m3'''
    config = self.get_system()
    return float(config['water_price'])

  def get_hostname(self):
    config = self.get_system()
    return config['host']

  def get_port_number(self):
    config = self.get_system()
    return config['port']

  # Environment functions

  def save_environment(self,data):
    '''Save the terrariumPI environment config

    '''
    config = {}
    for key, value in terrariumUtils.flatten_dict(data).iteritems():
      config[key] = value

    self.__config.remove_section('environment')
    return self.__update_config('environment',config,[])

  def get_environment(self):
    config = {}
    for key, value in self.__get_config('environment').iteritems():
      config_keys = key.split('_')
      part = config_keys[0]
      del(config_keys[0])

      if part not in config:
        config[part] = {}

      config[part]['_'.join(config_keys)] = value

    return config
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
    return self.__update_config('weather',data,['type'])

  def get_weather(self):
    return self.__get_config('weather')


  # End weather config functions


  # Sensor config functions
  def get_owfs_port(self):
    return int(self.get_system()['owfs_port'])

  def save_sensor(self,data):
    return self.__update_config('sensor' + data['id'],data,['current','indicator'])

  def save_sensors(self,data):
    update_ok = True
    for sensor in self.get_sensors():
      self.__config.remove_section('sensor' + sensor['id'])

    for sensorid in data:
      update_ok = update_ok and self.save_sensor(data[sensorid].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_sensors(self):
    return self.__get_all_config('sensor')
  # End sensor config functions


  # Switches config functions
  def save_power_switch(self,data):
    clearfields = ['state','current_power_wattage','current_water_flow']
    if data['hardwaretype'] != 'pwm-dimmer':
      clearfields += ['dimmer_duration','dimmer_off_duration','dimmer_off_percentage','dimmer_on_duration','dimmer_on_percentage']

    return self.__update_config('switch' + data['id'],data,clearfields)

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
    return self.__get_all_config('switch')
  # End switches config functions

  # Door config functions
  def save_door(self,data):
    return self.__update_config('door' + data['id'],data,['state'])

  def save_doors(self,data):
    update_ok = True
    for door in self.get_doors():
      self.__config.remove_section('door' + door['id'])

    for door_id in data:
      update_ok = update_ok and self.save_door(data[door_id].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_doors(self):
    return self.__get_all_config('door')
  # End door config functions


  # Webcam config functions
  def save_webcam(self,data):
    if 'resolution' in data:
      data['resolution_width'] = data['resolution']['width']
      data['resolution_height'] = data['resolution']['height']
      del(data['resolution'])

    return self.__update_config('webcam' + data['id'],data,['state','image','max_zoom','last_update','preview','archive_images'])

  def save_webcams(self,data):
    update_ok = True
    for webcam in self.get_webcams():
      self.__config.remove_section('webcam' + webcam['id'])

    for webcam_id in data:
      update_ok = update_ok and self.save_webcam(data[webcam_id].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_webcams(self):
    return self.__get_all_config('webcam')
  # End webcam config functions

  # Audio playlist config functions
  def save_audio_playlist(self,data):
    return self.__update_config('playlist' + data['id'],data,['running','songs_duration','duration'])

  def save_audio_playlists(self,data):
    update_ok = True
    for audio_playlist in self.get_audio_playlists():
      self.__config.remove_section('playlist' + audio_playlist['id'])

    for audio_playlist_id in data:
      update_ok = update_ok and self.save_audio_playlist(data[audio_playlist_id].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_audio_playlists(self):
    data = self.__get_all_config('playlist')
    for playlist in data:
      playlist['files'] = playlist['files'].split(',')

    return data
  # End audio playlist config functions
