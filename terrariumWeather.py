# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urllib2 import urlopen
from datetime import datetime, timedelta
from time import sleep

import logging
terrarium_log = logging.getLogger('root')

class terrariumWeather:

  def __init__(self,config):
    self.__config = config

    self.__location = self.__config.getWeatherURL()
    self.__weatherMaxTempLimit = self.__config.getWeatherMaxLimit()
    self.__weatherMinTempLimit = self.__config.getWeatherMinLimit()

    self.__loggingActive = self.__config.getWeatherLoggerEnabled();
    self.__alarmActive   = self.__config.getWeatherAlarmEnabled();

    self.__weatherXML = ''
    self.__weatherTimezone = ''
    self.__weatherTimezoneOffset = 0
    self.__weatherCityName = ''
    self.__weatherCountryName = ''
    self.__weatherLatLong = ''
    self.__weatherSunrise = ''
    self.__weatherSunset = ''
    self.__weatherMaxTemp = float(-999)
    self.__weatherMinTemp = float(999)
    self.__weatherIndicator = '°C'
    self.__weatherCreditsText = ''
    self.__weatherCreditsLink = ''
    self.__weahterForecast = []

    self.__lastUpdate = datetime.fromtimestamp(0)
    self.__cacheTimeOut = timedelta(seconds=3600)

    self.update()

  def update(self,force = False):
    now = datetime.now()
    if force or self.__lastUpdate == 0 or now - self.__lastUpdate > self.__cacheTimeOut:
      self.__lastUpdate = now
      terrarium_log.debug('Refreshing weather data from source %s', self.getXMLUrl())

      for nr in range(10):
        try:
          self.__weatherXML = ET.fromstring(urlopen(self.__location).read())
          break
        except Exception, err:
          terrarium_log.warn('Error getting new weather data from source %s. Error: %s', self.getXMLUrl(), err)
          sleep(5)

      terrarium_log.debug('Updating weather location data')
      self.__parseLocationData()
      terrarium_log.debug('Updating weather sunrise and sunset')
      self.__parseSunRiseSunSet()
      terrarium_log.debug('Updating weather forecast')
      self.__parseForcast()

      terrarium_log.info('Updated weather data from source %s took %d seconds', self.getXMLUrl(), (datetime.now()-now).total_seconds())

  def __parseLocationData(self):
    data = self.__weatherXML.find('./location')
    self.__weatherCityName = data.find('name').text
    self.__weatherCountryName = data.find('country').text
    self.__weatherTimezone = data.find('timezone').get('id')
    self.__weatherTimezoneOffset = int(data.find('timezone').get('utcoffsetMinutes'))
    self.__weatherLatLong = {'lat' : data.find('location').get('latitude'), 'long' : data.find('location').get('longitude')}
    data = self.__weatherXML.find('./credit')
    self.__weatherCreditsText = data.find('link').get('text')
    self.__weatherCreditsLink = data.find('link').get('url')

  def __parseSunRiseSunSet(self):
    data = self.__weatherXML.find('./sun')
    if data is not None:
      self.__weatherSunrise = datetime.strptime(data.get('rise'),'%Y-%m-%dT%H:%M:%S')
      self.__weatherSunset  = datetime.strptime(data.get('set'),'%Y-%m-%dT%H:%M:%S')
    else:
      self.__weatherSunrise = datetime.strptime(datetime.now().strftime('%Y-%m-%dT') + '08:00:00','%Y-%m-%dT%H:%M:%S')
      self.__weatherSunset  = datetime.strptime(datetime.now().strftime('%Y-%m-%dT') + '20:00:00','%Y-%m-%dT%H:%M:%S')

  def __parseForcast(self):
     self.__weahterForecast = []
     indicator = False
     for data in self.__weatherXML.findall('./forecast/tabular/time'):
       forecastStartTime = datetime.strptime(data.get('from'),'%Y-%m-%dT%H:%M:%S')
       forecastEndTime = datetime.strptime(data.get('to'),'%Y-%m-%dT%H:%M:%S')

       forecastWeather = data.find('symbol').get('name')

       forecastRain = float(data.find('precipitation').get('value'))
       forecastWindDirection = float(data.find('windDirection').get('deg'))
       forecastWindSpeed = float(data.find('windSpeed').get('mps'))
       forecastTemperature = float(data.find('temperature').get('value'))
       forecastPressure = float(data.find('pressure').get('value'))

       if not indicator:
         indicator = str(data.find('temperature').get('unit'))
         if 'celsius' == indicator:
           self.__weatherIndicator = '°C'
         else:
          self.__weatherIndicator = '°F'

       if forecastTemperature > self.__weatherMaxTemp:
         self.__weatherMaxTemp = forecastTemperature

       if forecastTemperature < self.__weatherMinTemp:
         self.__weatherMinTemp = forecastTemperature

       self.__weahterForecast.append({'start' : forecastStartTime,
                                      'end' : forecastEndTime,
                                      'weather' : forecastWeather,
                                      'rain' : forecastRain,
                                      'wind_direction' : forecastWindDirection,
                                      'windspeed' : forecastWindSpeed,
                                      'temperature' : forecastTemperature,
                                      'pressure' : forecastPressure })

  def getXMLUrl(self):
    return self.__location

  def setXMLUrl(self,location):
    self.__location = location
    self.__saveWeatherConfig()
    self.update(True)

  def setMaximumTemperatureLimit(self,limit):
    self.__weatherMaxTempLimit = limit
    self.__saveWeatherConfig()

  def setMinimumTemperatureLimit(self,limit):
    self.__weatherMinTempLimit = limit
    self.__saveWeatherConfig()

  def getMaximumTemperatureLimit(self):
    return self.__weatherMaxTempLimit

  def getMinimumTemperatureLimit(self):
    return self.__weatherMinTempLimit

  def getSunRiseTime(self):
    return self.__weatherSunrise

  def getSunSetTime(self):
    return self.__weatherSunset

  def getCity(self):
    return self.__weatherCityName

  def getCountry(self):
    return self.__weatherCountryName

  def getLocation(self):
    return self.__weatherLatLong

  def getLocationTime(self):
    return datetime.utcnow() + timedelta(minutes=self.__weatherTimezoneOffset)

  def getMaximumTemperature(self):
    return self.__weatherMaxTemp

  def getMinimumTemperature(self):
    return self.__weatherMinTemp

  def getCurrentTemperature(self):
    return self.getCurrentWeatherInfo()['temperature']

  def getIndicator(self):
    return self.__weatherIndicator

  def isDaytime(self):
    return self.getSunRiseTime() < self.getLocationTime() < self.getSunSetTime()

  def getCurrentWeatherInfo(self,hours = 0):
    now = datetime.now() + timedelta(hours=hours)
    returnlist = []

    for weatherForecast in self.__weahterForecast:
      if (now < weatherForecast['start']) or (now > weatherForecast['start'] and now < weatherForecast['end']) or (now > weatherForecast['end']):
        returnlist.append(weatherForecast)
        if hours == 0:
          break

    if len(returnlist) == 1:
      return returnlist[0]
    return returnlist

  def getLastUpdateTimeStamp(self):
    return self.__lastUpdate

  def getCredits(self):
    return {'text' : self.__weatherCreditsText, 'link' : self.__weatherCreditsLink}

  def setAlarm(self,on):
    self.__alarmActive = bool(on)

  def enableAlarm(self):
    self.__alarmActive = True

  def disableAlarm(self):
    self.__alarmActive = False

  def isAlarmActive(self):
    return True == self.__alarmActive

  def setLogging(self,on):
    self.__loggingActive = bool(on)

  def enableLogging(self):
    self.__loggingActive = True

  def disableLogging(self):
    self.__loggingActive = False

  def isLoggingEnabled(self):
    return True == self.__loggingActive

  def getAlarmMax(self):
    if not self.isAlarmActive():
      return -1
    return self.getCurrent() > self.getMaximumTemperatureLimit()

  def getAlarmMin(self):
    if not self.isAlarmActive():
      return -1
    return self.getCurrentTemperature() < self.getMinimumTemperatureLimit()

  def getAlarm(self):
    if not self.isAlarmActive():
      return -1
    return self.getCurrentTemperature() or self.getAlarmMin()

  def __saveWeatherConfig(self):
    self.__config.saveWeatherSettings(self.getXMLUrl(),self.__weatherMaxTempLimit,self.__weatherMinTempLimit,self.__loggingActive,self.__alarmActive)
