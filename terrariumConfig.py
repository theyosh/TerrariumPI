# -*- coding: utf-8 -*-
import ConfigParser

class terrariumConfig:
  '''Class for loading the configuration for terrariumPI software.
     The configuration is based on two configuration files.
     - default.cfg holds system defaults for first run
     - settigs.cfg holds the user defined config files

     So the default.cfg file is read first, and overwritten by the settings
     from the settings.cfg file.

     Changes will always be written to settings.cfg.'''

  def __init__(self):
    '''Load terrariumPI config object'''
    self.__defaults_file = 'defaults.cfg'
    self.__config_file = 'settings.cfg'

    self.__config = ConfigParser.SafeConfigParser()
    self.__config.readfp(open(self.__defaults_file))
    self.__config.read(self.__config_file)

  # Private functions
  def __save_config(self):
    '''Write terrariumPI config to settings.cfg file'''
    with open(self.__config_file, 'wb') as configfile:
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

      self.__config.set(section, str(setting), str(data[setting]))

    return self.__save_config()

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
    return self.__get_config('terrariumpi')

  def set_system(self,data):
    '''Set terrariumPI configuration section 'terrariumpi'

    Make sure that the fields cur_password and new_password are never stored
    '''
    del(data['cur_password'])
    del(data['new_password'])
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
    config = self.get_system()
    return config['available_languages'].split(',')

  def get_active_language(self):
    '''Get terrariumPI active language'''
    config = self.get_system()
    if 'active_language' not in config:
      config['active_language'] = self.get_available_languages()[0]

    return config['active_language']

  def get_power_price(self):
    '''Get terrariumPI power price. Price is entered as euro/kWh'''
    config = self.get_system()
    return float(config['power_price'])

  def get_water_price(self):
    '''Get terrariumPI water price. Price is entered as euro/m3'''
    config = self.get_system()
    return float(config['water_price'])

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
    data = {'light' : {}, 'sprayer' : {}, 'heater' : {} }
    for key in config:
      config_keys = key.split('_')
      part = config_keys[0]
      del(config_keys[0])
      data[part]['_'.join(config_keys)] = config[key]

    return data

  def get_environment_light(self):
    data = self.get_environment()
    return data['light'] if 'light' in data else None
  # End Environment functions


  # Weather config functions
  def save_weather(self,data):
    return self.__update_config('weather',data)

  def get_weather(self):
    return self.__get_config('weather')

  def get_weather_location(self):
    data = self.get_weather()
    return data['location'] if 'location' in data else None

  def get_weather_windspeed(self):
    data = self.get_weather()
    return data['windspeed'] if 'windspeed' in data else None

  def get_weather_temperature(self):
    data = self.get_weather()
    return data['temperature'] if 'temperature' in data else None
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

    return self.__update_config('switch' + str(data['id']),data)

  def save_power_switches(self,data):
    update_ok = True
    for power_switch_id in self.get_power_switches():
      self.__config.remove_section('swicth' + power_switch_id)

    for power_switch_id in data:
      update_ok = update_ok and self.save_power_switch(data[power_switch_id].get_data())

    if len(data) == 0:
      update_ok = update_ok and self.__save_config()

    return update_ok

  def get_power_switches(self):
    data = {}
    for section in self.__config.sections():
      if section[:6] == 'switch':
        switch_data = self.__get_config(section)
        data[section[6:]] = switch_data

    return data
  # End switches config functions


  # Webcam config functions
  def get_webcams(self):
    data = {}
    for section in self.__config.sections():
      if section[:6] == 'webcam':
        sensor_data = self.__get_config(section)
        data[section[6:]] = sensor_data

    return data

  def save_webcam(self,data):
    del(data['state'])
    del(data['image'])
    del(data['max_zoom'])
    del(data['last_update'])
    del(data['resolution'])
    del(data['preview'])
    return self.__update_config('webcam' + str(data['id']),data)
  # End webcam config functions

  # Door config functions
  def get_doors(self):
    data = {}
    for section in self.__config.sections():
      if section[:4] == 'door':
        sensor_data = self.__get_config(section)
        data[section[6:]] = sensor_data

    return data

  def save_door(self,data):
    del(data['state'])
    return self.__update_config('door' + str(data['id']),data)
  # End door config functions
