# -*- coding: utf-8 -*-

import ConfigParser
from datetime import datetime

class terrariumConfig:
  def __init__(self):
    self.__config_file_name = 'terrariumSettings.cfg'
    self.__config = ConfigParser.SafeConfigParser()
    self.__config.read(self.__config_file_name)
    self.__starttime = datetime.now()
    
    self.__debug = True

  def getOWSPortnumber(self):
    value = 4304
    try:
      value = self.__config.getint('server','1Wireport')

    except ValueError:
      message = 'OWS port number is not a numeric value. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', '1Wireport', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'OWS port number is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', '1Wireport', str(value))

      if self.__debug:
        print message

    return value

  def getLogLevel(self):
    value = 5
    try:
      value = self.__config.getint('server','loglevel')

    except ValueError:
      message = 'Debug level is not a numeric value. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', 'loglevel', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Debug level is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', 'loglevel', str(value))

      if self.__debug:
        print message

    return value


  def getRunningTime(self):
    return (datetime.now() - self.__starttime).total_seconds()

  def getPiWattage(self):
    value = 5
    try:
      value = self.__config.getint('environment','pi_wattage')

    except ValueError:
      message = 'Pi wattage not a numeric value. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    except ConfigParser.NoSectionError:
      message = 'Environment section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('environment')
      self.__config.set('environment', 'pi_wattage', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Pi wattage is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('environment', 'pi_wattage', str(value))

      if self.__debug:
        print message

    return value

  def getServerIP(self):
    value = '0.0.0.0'
    try:
      value = self.__config.get('server','hostname')

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', 'hostname', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Server hostname is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', 'hostname', str(value))

      if self.__debug:
        print message

    return value

  def getServerPort(self):
    value = 8282
    try:
      value = self.__config.getint('server','port')

    except ValueError:
      message = 'Server port number is not a numeric value. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', 'port', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Server port number is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', 'port', str(value))

      if self.__debug:
        print message

    return value

  def getDoorGPIOPin(self):
    value = 21
    try:
      value = self.__config.getint('environment','door_gpi_pin')

    except ValueError:
      message = 'Door GPIO pin is not a numeric value. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    except ConfigParser.NoSectionError:
      message = 'Environment section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('environment')
      self.__config.set('environment', 'door_gpi_pin', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Door GPIO number is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('environment', 'door_gpi_pin', str(value))

      if self.__debug:
        print message

    return value

  def getServerAdmin(self):
    value = 'admin'
    try:
      value = self.__config.get('server','admin')

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', 'admin', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Server admin is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', 'admin', str(value))

      if self.__debug:
        print message

    return value

  def getServerPassword(self):
    value = 'admin'
    try:
      value = self.__config.get('server','password')

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', 'password', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Server password is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', 'password', str(value))

      if self.__debug:
        print message
    return value

  def setServerUsername(self,name):
    if not name:
      return False

    try:
      value = self.__config.set('server','admin',str(name))

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', 'admin', str(name))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Server admin is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', 'admin', str(name))

      if self.__debug:
        print message

    self.__saveConfig()
    return True

  def setServerPassword(self,password):
    if not password:
      return False

    try:
      value = self.__config.set('server','password',str(password))

    except ConfigParser.NoSectionError:
      message = 'Server section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('server')
      self.__config.set('server', 'password', str(password))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Server admin is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('server', 'password', str(password))

      if self.__debug:
        print message

    self.__saveConfig()
    return True

  def __getDeviceSettings(self,deviceid):
    valueList = {}
    if self.__config.has_section(deviceid):
      for key,value in self.__config.items(deviceid):
        valueList[key] = value

    return valueList

  def getSensorSettings(self,sensorid):
    return self.__getDeviceSettings('sensor_' + sensorid);

  def getSwitchSettings(self,switchid):
    return self.__getDeviceSettings('switch_' + switchid);

  def saveSensorSettings(self,sensorid,name,maxlimit,minlimit,timeout,alarm,logging,indicator):
    section_name = 'sensor_' + sensorid
    if not self.__config.has_section(section_name):
      self.__config.add_section(section_name)

    if name:
      self.__config.set(section_name, 'name', str(name))
    if maxlimit:
      self.__config.set(section_name, 'maxlimit', str(maxlimit))
    if minlimit:
      self.__config.set(section_name, 'minlimit', str(minlimit))
    if timeout:
      self.__config.set(section_name, 'timeout', str(timeout))
    if alarm:
      self.__config.set(section_name, 'alarm', str(alarm))
    #if logging != '':
    self.__config.set(section_name, 'logging', str(logging))
    if indicator:
      if '%' == indicator:
        indicator += '%'
      self.__config.set(section_name, 'indicator', str(indicator))

    self.__saveConfig()
    return True

  def saveSwitchSettings(self,switchid,name,timeout,logging,wattage,waterflow):
    section_name = 'switch_' + switchid
    if not self.__config.has_section(section_name):
      self.__config.add_section(section_name)

    if name:
      self.__config.set(section_name, 'name', str(name))
    if timeout:
      self.__config.set(section_name, 'timeout', str(timeout))
    if logging:
      self.__config.set(section_name, 'logging', str(logging))
    if wattage:
      self.__config.set(section_name, 'wattage', str(wattage))
    if waterflow:
      self.__config.set(section_name, 'waterflow', str(waterflow))

    self.__saveConfig()
    return True

  def getWebcamsList(self):
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
    return True

  def getWeatherURL(self):
    value = 'http://www.yr.no/place/Netherlands/Groningen/Groningen/forecast_hour_by_hour.xml'
    try:
      value = self.__config.get('weather','location')

    except ConfigParser.NoSectionError:
      message = 'Weather section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('weather')
      self.__config.set('weather', 'location', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'The weather XML url is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('weather', 'location', str(value))

      if self.__debug:
        print message

    return value

  def getWeatherLoggerEnabled(self):
    value = True
    try:
      value = self.__config.getboolean('weather','logger')

    except ConfigParser.NoOptionError:
      message = 'The weather XML url is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('weather', 'logger', str(value))

      if self.__debug:
        print message

    return value

  def getWeatherAlarmEnabled(self):
    value = True
    try:
      value = self.__config.getboolean('weather','alarm')

    except ConfigParser.NoOptionError:
      message = 'The weather XML url is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('weather', 'alarm', str(value))

      if self.__debug:
        print message

    return value

  def getWeatherMaxLimit(self):
    value = 35
    try:
      value = self.__config.get('weather','maxlimit')

    except ConfigParser.NoOptionError:
      message = 'The weather XML url is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('weather', 'maxlimit', str(value))

      if self.__debug:
        print message

    return value

  def getWeatherMinLimit(self):
    value = -10
    try:
      value = self.__config.get('weather','minlimit')

    except ConfigParser.NoOptionError:
      message = 'The weather XML url is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('weather', 'minlimit', str(value))

      if self.__debug:
        print message

    return value

  def saveWeatherSettings(self,url,max,min,logger,alarm):
    if not self.__config.has_section('weather'):
      self.__config.add_section('weather')

    if url:
      self.__config.set('weather', 'location', str(url))

    if max:
      self.__config.set('weather', 'maxlimit', str(max))

    if min:
      self.__config.set('weather', 'minlimit', str(min))

    if logger:
      self.__config.set('weather', 'logger', str(logger))

    if alarm:
      self.__config.set('weather', 'alarm', str(alarm))

    self.__saveConfig()
    return True

  def getEnvironmentConfig(self):
    valueList = { 'light_enabled' : False,
                  'light_on' : 'sunrise',
                  'light_off' : 'sunset',
                  'light_switch' : '',
                  'light_sensor' : '',
                  'light_duration_max_hours' : 16,
                  'light_duration_min_hours' : 10,
                  'light_duration_time_shift' : 0,
                  'heater_enabled' : False,
                  'heater_on' : '22:00',
                  'heater_off' : '6:00',
                  'heater_switch' : '',
                  'heater_sensor' : '',
                  'heater_modus' : 'time',
                  'heater_active_during_day' : False,
                  'humidity_enabled' : False,
                  'humidity_sensor' : '',
                  'humidity_switch' : '',
                  'humidity_switch_duration' : 15,
                  'humidity_switch_timeout' : 60,
                  'humidity_active_during_night' : False
                }
    try:
      for key,value in self.__config.items('environment'):
        valueList[key] = value

    except ConfigParser.NoSectionError:
      message = 'Environment section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('environment')
      for key in valueList:
        self.__config.set('environment', key, str(valueList[key]))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Something not set. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    return valueList

  def setEnvironmentLightConfig(self,enabled = False,on = 'sunrise',off = 'sunset',switches = '',sensors = '',min = 10,max = 10 ,shift = 0):
    self.__config.set('environment', 'light_enabled', str(enabled))
    self.__config.set('environment', 'light_on', str(on))
    self.__config.set('environment', 'light_off', str(off))
    self.__config.set('environment', 'light_switch', str(switches))
    self.__config.set('environment', 'light_sensor', str(sensors))
    self.__config.set('environment', 'light_duration_max_hours', str(max))
    self.__config.set('environment', 'light_duration_min_hours', str(min))
    self.__config.set('environment', 'light_duration_time_shift', str(shift))
    self.saveConfig()
    return True

  def setEnvironmentHeaterConfig(self, enabled = False, switches = '', sensors = '', modus = 'time', on = 0, off = 0, dayactive = False):
    self.__config.set('environment', 'heater_enabled', str(enabled))
    self.__config.set('environment', 'heater_on', str(on))
    self.__config.set('environment', 'heater_off', str(off))
    self.__config.set('environment', 'heater_switch', str(switches))
    self.__config.set('environment', 'heater_sensor', str(sensors))
    self.__config.set('environment', 'heater_modus', str(modus))
    self.__config.set('environment', 'heater_active_during_day', str(dayactive))
    self.saveConfig()
    return True

  def setEnvironmentHumidityConfig(self,enabled = False,switches = '',sensors = '',timeout = 60,duration = 15 ,nightactive = False):
    self.__config.set('environment', 'humidity_enabled', str(enabled))
    self.__config.set('environment', 'humidity_switch', str(switches))
    self.__config.set('environment', 'humidity_sensor', str(sensors))
    self.__config.set('environment', 'humidity_switch_timeout', str(timeout))
    self.__config.set('environment', 'humidity_switch_duration', str(duration))
    self.__config.set('environment', 'humidity_active_during_night', str(nightactive))
    self.saveConfig()
    return True

  def getTwitterEnabled(self):
    value = False
    try:
      value = self.__config.getboolean('twitter','enabled')

    except ValueError:
      message = 'Twitter Boolean value. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    except ConfigParser.NoSectionError:
      message = 'Twitter section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('twitter')
      self.__config.set('twitter', 'enabled', str(value))

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Twitter setting is not set. Please update the configuration file: ' + self.__config_file_name
      self.__config.set('twitter', 'enabled', str(value))

      if self.__debug:
        print message

    return value

  def getTwitterConfig(self):
    valueList = {}
    try:
      for key,value in self.__config.items('twitter'):
        valueList[key] = value

    except ConfigParser.NoSectionError:
      message = 'Twitter section is not available in the configuration file: ' + self.__config_file_name
      self.__config.add_section('twitter')

      if self.__debug:
        print message

    except ConfigParser.NoOptionError:
      message = 'Something not set. Please update the configuration file: ' + self.__config_file_name
      if self.__debug:
        print message

    return valueList

  def saveConfig(self):
    self.__saveConfig()

  def __saveConfig(self):
    with open(self.__config_file_name, 'wb') as configfile:
      self.__config.write(configfile)
