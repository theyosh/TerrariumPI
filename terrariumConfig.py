# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import datetime
try:
  import configparser
except ImportError as ex:
  import ConfigParser as configparser

from glob import glob
from hashlib import md5

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

    self.__config = configparser.ConfigParser(interpolation=None)
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
      for version in range(current_version+1,new_version+1):
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
                newdata['temperature_alarm_max_light_state'] = 'ignore' if terrariumUtils.is_true(data['cooler_night_enabled']) else 'on'

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


              if 'temperature_mode' not in newdata or 'disabled' == newdata['temperature_mode']:
                newdata['temperature_mode'] = 'weatherinverse' if data['heater_mode'] == 'weather' else data['heater_mode']

              if 'heater_night_difference' in data:
                if 'temperature_day_night_difference' in newdata and terrariumUtils.is_float(newdata['temperature_day_night_difference']):
                  newdata['temperature_day_night_difference'] = (float(newdata['temperature_day_night_difference']) + float(data['heater_night_difference'])) / 2.0
                else:
                  newdata['temperature_day_night_difference'] = data['heater_night_difference']

              if 'heater_night_source' in data and ('temperature_day_night_source' not in newdata or newdata['temperature_day_night_source'] == ''):
                newdata['temperature_day_night_source'] = data['heater_night_source']

              if 'heater_sensors' in data:
                if 'temperature_sensors' in newdata and newdata['temperature_sensors'] != '':
                  newdata['temperature_sensors'] += ',' + data['heater_sensors']
                else:
                  newdata['temperature_sensors'] = data['heater_sensors']

              if 'heater_day_enabled' in data:
                newdata['temperature_alarm_min_light_state'] = 'ignore' if terrariumUtils.is_true(data['heater_day_enabled']) else 'off'

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


              if 'light_mode' in data:
                newdata['light_mode'] = data['light_mode']

              if 'light_min_hours' in data:
                newdata['light_min_hours'] = data['light_min_hours']

              if 'light_max_hours' in data:
                newdata['light_max_hours'] = data['light_max_hours']

              if 'light_hours_shift' in data:
                newdata['light_hours_shift'] = data['light_hours_shift']

              if 'light_power_switches' in data:
                newdata['light_alarm_min_powerswitches'] = data['light_power_switches']

              if 'light_on' in data:
                newdata['light_alarm_min_timer_start'] = data['light_on']

              if 'light_off' in data:
                newdata['light_alarm_min_timer_stop'] = data['light_off']

              if 'light_on_duration' in data:
                newdata['light_alarm_min_timer_on'] = data['light_on_duration']

              if 'light_off_duration' in data:
                newdata['light_alarm_min_timer_off'] = data['light_off_duration']

              newdata['light_alarm_min_settle'] = 10
              newdata['light_alarm_max_settle'] = 10


              if 'moisture_mode' in data:
                newdata['moisture_mode'] = data['moisture_mode']

              if 'moisture_sensors' in data:
                newdata['moisture_sensors'] = data['moisture_sensors']

              if 'moisture_power_switches' in data:
                newdata['moisture_alarm_min_powerswitches'] = data['moisture_power_switches']

              if 'moisture_on' in data:
                newdata['moisture_alarm_min_timer_start'] = data['moisture_on']

              if 'moisture_off' in data:
                newdata['moisture_alarm_min_timer_stop'] = data['moisture_off']

              if 'moisture_on_duration' in data:
                newdata['moisture_alarm_min_timer_on'] = data['moisture_on_duration']

              if 'moisture_off_duration' in data:
                newdata['moisture_alarm_min_timer_off'] = data['moisture_off_duration']

              if 'moisture_spray_duration' in data:
                newdata['moisture_alarm_min_duration_on'] = data['moisture_spray_duration']

              if 'moisture_spray_timeout' in data:
                newdata['moisture_alarm_min_settle'] = data['moisture_spray_timeout']

              if 'moisture_night_enabled' in data:
                newdata['moisture_alarm_min_light_state'] = 'ignore' if terrariumUtils.is_true(data['moisture_night_enabled']) else 'on'


              if 'ph_mode' in data:
                newdata['ph_mode'] = data['ph_mode']

              if 'ph_sensors' in data:
                newdata['ph_sensors'] = data['ph_sensors']

              if 'ph_power_switches' in data:
                newdata['ph_alarm_min_powerswitches'] = data['ph_power_switches']

              if 'ph_on' in data:
                newdata['ph_alarm_min_timer_start'] = data['ph_on']

              if 'ph_off' in data:
                newdata['ph_alarm_min_timer_stop'] = data['ph_off']

              if 'ph_on_duration' in data:
                newdata['ph_alarm_min_timer_on'] = data['ph_on_duration']

              if 'ph_off_duration' in data:
                newdata['ph_alarm_min_timer_off'] = data['ph_off_duration']

              if 'ph_settle_timeout' in data:
                newdata['ph_alarm_min_settle'] = data['ph_settle_timeout']

              if 'ph_day_enabled' in data:
                newdata['ph_alarm_min_light_state'] = 'ignore' if terrariumUtils.is_true(data['ph_day_enabled']) else 'on'


              if 'sprayer_mode' in data:
                newdata['humidity_mode'] = data['sprayer_mode']

              if 'sprayer_sensors' in data:
                newdata['humidity_sensors'] = data['sprayer_sensors']

              if 'sprayer_power_switches' in data:
                newdata['humidity_alarm_min_powerswitches'] = data['sprayer_power_switches']

              if 'sprayer_on' in data:
                newdata['humidity_alarm_min_timer_start'] = data['sprayer_on']

              if 'sprayer_off' in data:
                newdata['humidity_alarm_min_timer_stop'] = data['sprayer_off']

              if 'sprayer_on_duration' in data:
                newdata['humidity_alarm_min_timer_on'] = data['sprayer_on_duration']

              if 'sprayer_off_duration' in data:
                newdata['humidity_alarm_min_timer_off'] = data['sprayer_off_duration']

              if 'sprayer_spray_duration' in data:
                newdata['humidity_alarm_min_duration_on'] = data['sprayer_spray_duration']

              if 'sprayer_spray_timeout' in data:
                newdata['humidity_alarm_min_settle'] = data['sprayer_spray_timeout']

              if 'sprayer_night_enabled' in data:
                newdata['humidity_alarm_min_light_state'] = 'ignore' if terrariumUtils.is_true(data['sprayer_night_enabled']) else 'on'

              newdata['humidity_alarm_min_door_state'] = 'closed'


              if 'watertank_mode' in data:
                newdata['watertank_mode'] = data['watertank_mode']

              if 'watertank_sensors' in data:
                newdata['watertank_sensors'] = data['watertank_sensors']

              if 'watertank_height' in data:
                newdata['watertank_height'] = data['watertank_height']

              if 'watertank_volume' in data:
                newdata['watertank_volume'] = data['watertank_volume']

              if 'watertank_power_switches' in data:
                newdata['watertank_alarm_min_powerswitches'] = data['watertank_power_switches']

              if 'watertank_on' in data:
                newdata['watertank_alarm_min_timer_start'] = data['watertank_on']

              if 'watertank_off' in data:
                newdata['watertank_alarm_min_timer_stop'] = data['watertank_off']

              if 'watertank_on_duration' in data:
                newdata['watertank_alarm_min_timer_on'] = data['watertank_on_duration']

              if 'watertank_off_duration' in data:
                newdata['watertank_alarm_min_timer_off'] = data['watertank_off_duration']

              if 'watertank_pump_duration' in data:
                newdata['watertank_alarm_min_duration_on'] = data['watertank_pump_duration']

              self.save_environment(newdata)
              break

        elif version == 385:
          logger.info('Updating configuration file to version: %s' % (version,))

          windspeed_indicator = self.__get_config('weather').get('windspeed')
          if windspeed_indicator is None:
            windspeed_indicator = self.__get_config('terrariumpi').get('windspeed_indicator')
            if windspeed_indicator is None:
                windspeed_indicator = 'kmh'

          self.__config.set('terrariumpi', 'windspeed_indicator',  windspeed_indicator)
          self.__config.remove_option('weather','windspeed')

        elif version == 393:
          logger.info('Updating configuration file to version: %s' % (version,))
          # Only change IDs of sensors that can be scanned
          collector_update_sql = ''
          sensor_rename_list = {}
          for section in self.__config.sections():
            if section[:6] == 'sensor':
              data = self.__get_config(section)
              if data['hardwaretype'] in ['w1','owfs','miflora']:
                old_id = data['id']
                new_id = md5((data['hardwaretype'] + data['address'] + data['type']).encode()).hexdigest()

                if old_id != new_id:
                  if old_id not in sensor_rename_list:
                    sensor_rename_list[old_id] = new_id

                  data['id'] = new_id
                  new_section = 'sensor' + new_id
                  if not self.__config.has_section(new_section):
                    self.__config.add_section(new_section)

                  keys = list(data.keys())
                  keys.sort()
                  for setting in keys:
                    if setting in ['firmware','battery']:
                      continue

                    self.__config.set(new_section, str(setting), str(data[setting]))

                  # Clear any existing new data (should not happen)
                  collector_update_sql += 'DELETE FROM sensor_data WHERE id = \'{}\';\n'.format(new_id)
                  # Rename the sensor ID in the database
                  collector_update_sql += 'UPDATE sensor_data SET id = \'{}\' WHERE id = \'{}\';\n'.format(new_id,old_id)

                  self.__config.remove_section(section)

          # Update environment sensor settings
          environment = self.__get_config('environment')
          keys = list(environment.keys())
          for setting in keys:
            if '_sensors' in setting:
              for old_id in sensor_rename_list:
                environment[setting] = environment[setting].replace(old_id,sensor_rename_list[old_id])

              self.__config.set('environment', str(setting), str(environment[setting]))

          if '' != collector_update_sql:
            config_ok = self.__save_config()
            if config_ok:
              self.__reload_config()

              with open('.collector.update.{}.sql'.format(version),'w') as sql_file:
                sql_file.write(collector_update_sql.strip())


        elif version == 399:
          title = self.__get_config('terrariumpi').get('title').replace('3.9.9','').strip()
          self.__config.set('terrariumpi', 'title', str(title))

      # Update version number
      self.__config.set('terrariumpi', 'version', str(to_version))
      self.__save_config()
      self.__config.read(terrariumConfig.CUSTOM_CONFIG)
      logger.info('Updated configuration. Set version to: %s' % (to_version,))

  def __reload_config(self):
    self.__config.read(terrariumConfig.CUSTOM_CONFIG)

  def __save_config(self):
    '''Write terrariumPI config to settings.cfg file'''
    with open(terrariumConfig.CUSTOM_CONFIG, 'w') as configfile:
      self.__config.write(configfile)

    return True

  def __update_config(self,section,data,exclude = []):
    '''Update terrariumPI config with new values

    Keyword arguments:
    section -- section in configuration. If not exists it will be created
    data -- data to save in dict form'''

    if not self.__config.has_section(section):
      self.__config.add_section(section)

    keys = list(data.keys())
    keys.sort()
    for setting in keys:
      if setting in exclude:
        continue

      if type(data[setting]) is list:
        data[setting] = ','.join(data[setting])

      if isinstance(data[setting], str):
        try:
          data[setting] = data[setting].encode('utf-8').decode()
        except Exception as ex:
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
      self.__cache_available_languages = ['en'] + [language.replace('locales/','').replace('/','') for language in glob("locales/*/")]

    return self.__cache_available_languages

  def get_language(self):
    '''Get terrariumPI language'''
    config = self.get_system()
    if 'language' not in config:
      config['language'] = self.get_available_languages()[0]

    return config['language']

  def get_weather_location(self):
    config = self.get_weather()
    return config['location'] if 'location' in config else None

  '''def get_weather_windspeed(self):
    config = self.get_system()
    return config['windspeed_indicator'] if 'windspeed_indicator' in config else None'''

  def get_windspeed_indicator(self):
    config = self.get_system()
    return config['windspeed_indicator'] if 'windspeed_indicator' in config else None

  def get_volume_indicator(self):
    config = self.get_system()
    return config['volume_indicator'] if 'volume_indicator' in config else None

  def get_temperature_indicator(self):
    config = self.get_system()
    return config['temperature_indicator'] if 'temperature_indicator' in config else None

  def get_distance_indicator(self):
    config = self.get_system()
    return config['distance_indicator'] if 'distance_indicator' in config else None

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
  # End system functions

  def get_meross_cloud(self):
    return self.__get_config('meross_cloud')

  def set_meross_cloud(self,data):
    data = {'meross_username' : data['meross_username'],
            'meross_password' : data['meross_password']}

    return self.__update_config('meross_cloud',data)
  # End system functions

  # Environment functions

  def save_environment(self,data):
    '''Save the terrariumPI environment config

    '''
    config = {}
    for key, value in terrariumUtils.flatten_dict(data).items():
      config[key] = value

    self.__config.remove_section('environment')
    return self.__update_config('environment',config,[])

  def get_environment(self):
    config = {}
    for key, value in self.__get_config('environment').items():
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
    return self.__update_config('weather',data,['type','windspeed_indicator','windspeed'])

  def get_weather(self):
    return self.__get_config('weather')
  # End weather config functions


  # Sensor config functions
  def save_sensor(self,data):
    return self.__update_config('sensor' + data['id'],data,['current','indicator','firmware','battery'])

  def save_sensors(self,data):
    update_ok = True
    for sensor in self.get_sensors():
      if 'exclude' not in sensor or not terrariumUtils.is_true(sensor['exclude']):
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
    if 'dimmer' not in data['hardwaretype'] and 'brightpi' != data['hardwaretype']:
      clearfields += ['dimmer_duration','dimmer_off_duration','dimmer_off_percentage','dimmer_on_duration','dimmer_on_percentage']

    return self.__update_config('switch' + data['id'],data,clearfields)

  def save_power_switches(self,data):
    update_ok = True
    for power_switch in self.get_power_switches():
      if 'exclude' not in power_switch or not terrariumUtils.is_true(power_switch['exclude']):
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
