# -*- coding: utf-8 -*-
import ConfigParser

class terrariumConfig:
  def __init__(self,callback):
    self.__defaults_file = 'defaults.cfg'
    self.__config_file = 'settings.cfg'

    self.__config = ConfigParser.SafeConfigParser()
    self.__config.readfp(open(self.__defaults_file))
    self.__config.read(self.__config_file)

    self.callback = callback

  # Private functions
  def __save_config(self):
    with open(self.__config_file, 'wb') as configfile:
      self.__config.write(configfile)

    return True

  def __update_config(self,section,data):
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
    config = {}
    if not self.__config.has_section(section):
      return config

    for config_part in self.__config.items(section):
      config[config_part[0]] = config_part[1]

    return config

  def get_system(self):
    return self.__get_config('terrariumpi')

  def get_door_pin(self):
    config = self.get_system()
    return int(config['gpio_door_pin'])

  def get_pi_power_wattage(self):
    config = self.get_system()
    return float(config['power_usage'])

  # Environment functions
  def save_environment(self,data):
    config = {}
    for environment_part in data:
      for part in data[environment_part]:
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

  # Switches config functions
  def save_switch(self,data):
    return self.__update_config('switch' + str(data['nr']),data)

  def get_switches(self):
    config = self.__get_config('terrariumpi')
    data = {'max_switches' : config['max_switches'],
            'switches': []}
    for switchnr in range (1,int(config['max_switches'])+1):
      switch_config = self.__get_config('switch' + str(switchnr));
      if len(switch_config) > 0:
        data['switches'].append(switch_config)

    return data

  def get_1wire_port(self):
    return int(self.get_system()['1wire_port'])

  def save_sensor(self,data):
    del(data['address'])
    return self.__update_config('sensor' + str(data['id']),data)

  def get_sensors(self):
    data = {}
    for section in self.__config.sections():
      if section[:6] == 'sensor':
        sensor_data = self.__get_config(section)
        data[section[6:]] = sensor_data

    return data

  def get_full_config(self):
    print self


  '''def getWebcamsList(self):
    valuelist = []
    for configSection in self.__config.sections():
      if 'webcam_' in configSection:
        archive = 0
        try:
          archive = self.__config.get(configSection,'archive')
        except ConfigParser.NoOptionError:
          archive = 0

        rotate = 0
        try:
          rotate = self.__config.get(configSection,'rotation')
        except ConfigParser.NoOptionError:
          rotate = 0

        valuelist.append({'location':self.__config.get(configSection,'location'),
                          'name':self.__config.get(configSection,'name'),
                          'archive' : archive,
                          'rotation' : rotate})

    return valuelist

  def saveWebCamSettings(self,webcamid,name,url,archive,rotate):
    webcamid = 'webcam_' + webcamid
    if not self.__config.has_section(webcamid):
      self.__config.add_section(webcamid)

    if name:
      self.__config.set(webcamid, 'name', str(name))
    if url:
      self.__config.set(webcamid, 'location', str(url))
    if archive:
      self.__config.set(webcamid, 'archive', str(archive))
    if rotate:
      self.__config.set(webcamid, 'rotation', str(rotate))

    self.__saveConfig()
    return True'''
