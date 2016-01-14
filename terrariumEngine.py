# -*- coding: utf-8 -*-

from datetime import datetime,timedelta
from time import sleep
from threading import Thread

import logging
terrarium_log = logging.getLogger('root')

class terrariumEngine(Thread):

  def __init__(self,weatherObj,sensorList,powerswitchList,webcamList):
    Thread.__init__(self)
    self.__weather = weatherObj
    self.__sensors = sensorList
    self.__powerswitches = powerswitchList
    self.__webcams = webcamList

    self.__runTimeout = timedelta(seconds=20)
    self.__lastRun = datetime.fromtimestamp(0)

    self.start()

  def run(self):
    terrarium_log.info('Starting engine')
    while True:
      self.__lastRun = datetime.now()
      terrarium_log.debug('Updating engine ...')

      terrarium_log.debug('Running weather data')
      self.__updateWeatherData()
      terrarium_log.debug('Running webcam data')
      self.__updateWebcamData()
      terrarium_log.debug('Running switch data')
      self.__updatePowerSwitchData()
      terrarium_log.debug('Running sensor data')
      self.__updateSensorData()

      duration = datetime.now() - self.__lastRun
      terrarium_log.debug('Updating engine took %d seconds', duration.total_seconds())
      if duration < self.__runTimeout:
        terrarium_log.debug('Next engine update in %d seconds', (self.__runTimeout - duration).total_seconds())
        sleep(int((self.__runTimeout - duration).total_seconds()))

  def __updateWeatherData(self):
    self.__weather.update()

  def __updateWebcamData(self):
    for webcamid,webcam in self.__webcams.iteritems():
      webcam.update()

  def __updatePowerSwitchData(self):
    for switchid,switch in self.__powerswitches.iteritems():
      switch.update()

  def __updateSensorData(self):
    for sensorid,sensor in self.__sensors.iteritems():
      sensor.update()

  def online(self):
    return datetime.now() - self.__lastRun < 3 * self.__runTimeout
