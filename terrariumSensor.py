# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hashlib import md5
import ow

import logging
terrarium_log = logging.getLogger('root')

class terrariumSensor:
  valid_sensor_types = ['temperature','humidity']


  def __init__(self,sensor,type,configObj):
    self.__sensor = sensor
    self.__sensor.useCache(False)
    self.__type = type
    self.__config = configObj
    self.__id = md5(b'' + self.__sensor.address + self.__type).hexdigest()

    sensorConfig = self.__config.getSensorSettings(self.getID())

    self.__name             = str(sensorConfig['name'] if 'name' in sensorConfig and sensorConfig['name'] else '{unknown}')
    self.__maxLimit         = float(sensorConfig['maxlimit'] if 'maxlimit' in sensorConfig and sensorConfig['maxlimit'] else 0)
    self.__minLimit         = float(sensorConfig['minlimit'] if 'minlimit' in sensorConfig and sensorConfig['minlimit'] else 0)
    self.__alarmActive      = bool(sensorConfig['alarm'] if 'alarm' in sensorConfig and sensorConfig['alarm'] else True)
    self.__loggingActive    = bool(sensorConfig['logging'] if 'logging' in sensorConfig and sensorConfig['logging'] else True)
    self.__indicator        = str(sensorConfig['indicator'] if 'indicator' in sensorConfig and sensorConfig['indicator'] else '°C')

    self.__current      = float(0)
    self.__max          = float(-9999)
    self.__min          = float(9999)
    self.__lastUpdate   = datetime.fromtimestamp(0)
    self.__lastReset    = datetime.fromtimestamp(0)
    self.__lastResetTimeout = timedelta(seconds=float(30 * 60))

    if 'humidity' == self.__type:
      self.__cacheTimeOut     = timedelta(seconds=float(sensorConfig['timeout'] if 'timeout' in sensorConfig and sensorConfig['timeout'] else 15))
    else:
      self.__cacheTimeOut     = timedelta(seconds=float(sensorConfig['timeout'] if 'timeout' in sensorConfig and sensorConfig['timeout'] else 30))

    self.update()

  @staticmethod
  def scan(port):
    sensors = []
    try:
      ow.init(str(port));
      sensorsList = ow.Sensor('/').sensorList()
      for sensor in sensorsList:
        if 'temperature' in sensor.entryList():
          sensors.append({'type' : 'temperature',
                          'sensor' : sensor })

        if 'humidity' in sensor.entryList():
          sensors.append({'type' : 'humidity',
                          'sensor' : sensor })

    except ow.exNoController:
      message = '1 Wire file system is not actve / installed on this device!'
      print message

    return sensors

  def getID(self):
    return self.__id

  def setType(self,type):
    if type in terrariumSensor.valid_sensor_types:
      self.__type = str(type)
      self.__saveSensorConfig()
    else:
      terrarium_log.error('Unknown sensor type %s', type)

  def getType(self):
    return self.__type

  def setName(self,name):
    self.__name = str(name)
    self.__saveSensorConfig()

  def getName(self):
    return self.__name

  def setIndicator(self,indicator):
    self.__indicator = str(indicator)
    self.__saveSensorConfig()

  def getIndicator(self):
    return self.__indicator

  def getAddress(self):
    if '' == self.__address:
      try:
        self.__address = self.__sensor.address
      except Exception, err:
        terrarium_log.error('Error getting sensor address for %s(%s): %s',self.getName(), self.getID(),err)

    return self.__address

  def getCacheTimeOut(self):
    return self.__cacheTimeOut

  def setCacheTimeout(self,timeout):
    self.__cacheTimeOut = timedelta(seconds=int(timeout))
    self.__saveSensorConfig()

  def getMaxLimit(self):
    return self.__maxLimit

  def setMaxLimit(self,limit):
    self.__maxLimit = float(limit)
    self.__saveSensorConfig()

  def getMinLimit(self):
    return self.__minLimit

  def setMinLimit(self,limit):
    self.__minLimit = float(limit)
    self.__saveSensorConfig()

  def getCurrent(self):
    return self.__current

  def getMax(self):
    return self.__max

  def getMin(self):
    return self.__min

  def getLastUpdateTimeStamp(self):
    return self.__lastUpdate

  def resetMinMax(self):
    self.__max = self.__min = self.getCurrent()
    return True

  def update(self):
    now = datetime.now()
    if self.getAlarm() or now - self.__lastUpdate >= self.getCacheTimeOut():
      terrarium_log.debug('Updating sensor %s(%s) of type %s',self.getName(),self.getID(),self.getType())
      try:
        if 'temperature' == self.__type:
          self.__current = float(self.__sensor.temperature)
        elif 'humidity' == self.__type:
          self.__current = float(self.__sensor.humidity)
        self.__lastUpdate = now
      except Exception, err:
        # error.... don't update
        terrarium_log.error('Error updating sensor %s(%s): %s',self.getName(),self.getID(),err)

      if self.getCurrent() > self.getMax():
        self.__max = self.getCurrent()
        terrarium_log.debug('Updated the maximum measured value of sensor %s(%s) of type %s to value %f%s',self.getName(),self.getID(),self.getType(),self.getCurrent(),self.getIndicator())

      if self.getCurrent() < self.getMin():
        self.__min = self.getCurrent()
        terrarium_log.debug('Updated the minimum measured value of sensor %s(%s) of type %s to value %f%s',self.getName(),self.getID(),self.getType(),self.getCurrent(),self.getIndicator())

    if now - self.__lastReset >= self.__lastResetTimeout:
      self.resetMinMax()
      self.__lastReset = now
      terrarium_log.info('Resetting the minimum an maximum measured value for sensor %s(%s)',self.getName(),self.getID())

  def setAlarm(self,on):
    self.__alarmActive = on in ['1','True','true','on', True]

  def enableAlarm(self):
    self.__alarmActive = True

  def disableAlarm(self):
    self.__alarmActive = False

  def isAlarmActive(self):
    return True == self.__alarmActive

  def setLogging(self,on):
    self.__loggingActive = on in ['1','True','true','on', True]

  def enableLogging(self):
    self.__loggingActive = True

  def disableLogging(self):
    self.__loggingActive = False

  def isLoggingEnabled(self):
    return True == self.__loggingActive

  def getAlarmMax(self):
    if not self.isAlarmActive():
      return -1
    return self.getCurrent() > self.getMaxLimit()

  def getAlarmMin(self):
    if not self.isAlarmActive():
      return -1
    return self.getCurrent() < self.getMinLimit()

  def getAlarm(self):
    if not self.isAlarmActive():
      return -1
    return self.getAlarmMax() or self.getAlarmMin()

  def getSettings(self,format = 'json'):
    if 'json' == format:
      data = {}
      data['id'] = self.getID()
      data['type'] = self.getType()
      data['name'] = self.getName()
      data['current'] = self.getCurrent()
      data['max'] = self.getMax()
      data['min'] = self.getMin()
      data['maxlimit'] = self.getMaxLimit()
      data['minlimit'] = self.getMinLimit()
      data['alarm'] = self.getAlarm()
      data['alarm_enabled'] = self.isAlarmActive()
      data['logging_enabled'] = self.isLoggingEnabled()
      data['indicator'] = self.getIndicator()
      data['timeout'] = self.getCacheTimeOut().total_seconds()
      return data

    else:
      return self

  def __saveSensorConfig(self):
    self.__config.saveSensorSettings( self.getID(),
                                      self.getName(),
                                      self.getMaxLimit(),
                                      self.getMinLimit(),
                                      self.getCacheTimeOut().total_seconds(),
                                      self.isAlarmActive(),
                                      self.isLoggingEnabled(),
                                      self.getIndicator())
