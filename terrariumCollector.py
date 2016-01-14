# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from time import sleep, time
from threading import Thread
import thread
import os

import subprocess
import rrdtool

import logging
terrarium_log = logging.getLogger('root')

class terrariumCollector(Thread):

  def __init__(self,weatherObj,sensorList,powerswitchList,webcamList,environment,logtimeout = 60):
    Thread.__init__(self)
    self.__log_location = 'webroot/rrd'

    self.__weather = weatherObj
    self.__sensors = sensorList
    self.__powerswitches = powerswitchList
    self.__webcams = webcamList
    self.__environment = environment

    self.__runTimeout = timedelta(seconds=int(logtimeout))
    self.__lastRun = datetime.fromtimestamp(0)

    self.__write_log = True

    self.__cache_data = {}
    self.start()

  def run(self):
    start_delay_time = int(self.__runTimeout.total_seconds() - (int(int(time()) % int(self.__runTimeout.total_seconds()))))
    if start_delay_time > 0:
      terrarium_log.debug('Delaying collector startup with %d seconds', start_delay_time)
      sleep(start_delay_time)

    terrarium_log.info('Starting collector')
    while True:
      self.__lastRun = datetime.now()
      terrarium_log.debug('Updating collector data ...')

      terrarium_log.debug('Running weather data')
      self.updateWeatherData()
      terrarium_log.debug('Running switch data')
      self.updateSwitchesData()
      terrarium_log.debug('Running sensor data')
      self.updateSensorsData()

      duration = datetime.now() - self.__lastRun
      terrarium_log.debug('Updating collector took %d seconds', duration.total_seconds())
      if duration < self.__runTimeout:
        terrarium_log.debug('Next collector update in %d seconds', (self.__runTimeout - duration).total_seconds())
        sleep(int((self.__runTimeout - duration).total_seconds()))

  def updateWeatherData(self):
    if self.__write_log:
      if self.__weather.isLoggingEnabled():
        self.__createWeatherDatabase('groningen')
        rrdtool.update(self.__log_location + '/weather_groningen.rrd',
                       'N:%s:%s:%s' %( self.__weather.getCurrentTemperature(),
                                       self.__weather.getMinimumTemperature(),
                                       self.__weather.getMaximumTemperature()))

  def updateSensorsData(self):
    if self.__write_log:
      for sensorid,sensor in self.__sensors.iteritems():
        if sensor.isLoggingEnabled():
          self.__createSensorDatabase(sensorid)
          rrdtool.update(self.__log_location + '/sensor_' + sensorid + '.rrd',
                          'N:%s:%s:%s:%s:%s' %( sensor.getCurrent(),
                                                sensor.getMin(),
                                                sensor.getMax(),
                                                sensor.getMinLimit(),
                                                sensor.getMaxLimit()))

  def updateSwitchesData(self):
    if self.__write_log:
      for switchid,switch in self.__powerswitches.iteritems():
        if switch.isLoggingEnabled():
          self.__createSwitchDatabase(switchid)
          rrdtool.update(self.__log_location + '/switch_' + switchid + '.rrd',
                          'N:%s:%s' %( 1 if switch.getState() == 1 else 0,
                                       0 if switch.getState() == 1 else 1))

  def getRRDDatabase(self,databaseid,period = 'day',format = 'json'):
    cache_key = databaseid + '' + period
    if cache_key in self.__cache_data and (datetime.now() - self.__cache_data[cache_key]['time']).total_seconds() <= 60:
      terrarium_log.debug('Getting cached RDD data')
      return self.__cache_data[cache_key]['data']

    terrarium_log.debug('Getting/generating fresh RDD data')
    periodStart = '-1d'
    if 'week' == period:
      periodStart = '-1w'
    elif 'month' == period:
      periodStart = '-1m'
    elif 'year' == period:
      periodStart = '-1y'

    if 'weather_' in databaseid:
      p = subprocess.Popen('/usr/bin/rrdtool xport --start ' + periodStart + ' \
                            DEF:current='+ self.__log_location + '/' + databaseid + '.rrd:current:AVERAGE \
                            DEF:low='+ self.__log_location + '/' + databaseid + '.rrd:low:AVERAGE \
                            DEF:high='+ self.__log_location + '/' + databaseid + '.rrd:high:AVERAGE \
                            XPORT:current:"Current" \
                            XPORT:low:"Lowest" \
                            XPORT:high:"Highest"', stdout=subprocess.PIPE, shell=True)
    elif 'switch_' in databaseid:
      p = subprocess.Popen('/usr/bin/rrdtool xport --start ' + periodStart + ' \
                            DEF:on='+ self.__log_location + '/' + databaseid + '.rrd:on:AVERAGE \
                            DEF:off='+ self.__log_location + '/' + databaseid + '.rrd:off:AVERAGE \
                            XPORT:on:"On" \
                            XPORT:off:"Off"', stdout=subprocess.PIPE, shell=True)
    elif 'sensor_' in databaseid:
      p = subprocess.Popen('/usr/bin/rrdtool xport --start ' + periodStart + ' \
                            DEF:current='+ self.__log_location + '/' + databaseid + '.rrd:current:AVERAGE \
                            DEF:low='+ self.__log_location + '/' + databaseid + '.rrd:low:AVERAGE \
                            DEF:high='+ self.__log_location + '/' + databaseid + '.rrd:high:AVERAGE \
                            DEF:limitlow='+ self.__log_location + '/' + databaseid + '.rrd:limitlow:AVERAGE \
                            DEF:limithigh='+ self.__log_location + '/' + databaseid + '.rrd:limithigh:AVERAGE \
                            XPORT:current:"Current" \
                            XPORT:low:"Lowest" \
                            XPORT:high:"Highest" \
                            XPORT:limitlow:"Limit low" \
                            XPORT:limithigh:"Limit high"', stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    maxvalue = 0
    minvalue = 0
    returndata = []
    skip = True
    for data in ET.fromstring(output).findall('./data/row'):
      if not skip:
        timestamp = int(data.find('t').text) * 1000
        datarow = {'timestamp' : timestamp, 'current': 0, 'low':0,'high':0,'limitlow':0 , 'limithigh': 0}
        valueCounter = 0
        for value in data.findall('v'):
          value = ('%.3f' % float(value.text))
          if 0 == valueCounter:
            datarow['current'] = value
          elif 1 == valueCounter:
            datarow['low'] = value
          elif 2 == valueCounter:
            datarow['high'] = value
          elif 3 == valueCounter:
            datarow['limitlow'] = value
          elif 4 == valueCounter:
            datarow['limithigh'] = value

          if value > maxvalue:
            maxvalue = value
          if value < minvalue:
            minvalue = value

          valueCounter = valueCounter + 1

        if 'nan' != datarow['current']:
          returndata.append(datarow)

      skip = False

    self.__cache_data[cache_key] = {'time': datetime.now(), 'min': minvalue, 'max' : maxvalue,'data': returndata}
    return returndata

  def __checkLogFolder(self):
    if not os.path.isdir(self.__log_location):
        terrarium_log.info('Creating RDD log folders at location %s',self.__log_location)
        os.makedirs(self.__log_location)

  def __createSensorDatabase(self,id):
    self.__checkLogFolder()
    if not os.path.isfile(self.__log_location + '/sensor_' + id + '.rrd'):
      terrarium_log.info('Creating new RDD database for sensor with ID %s',id)
      rrdtool.create(self.__log_location + '/sensor_' + id + '.rrd', '--step',str(self.__runTimeout.total_seconds()),
        'DS:current:GAUGE:' + str(int(2 * self.__runTimeout.total_seconds())) + ':-50:100',
        'DS:low:GAUGE:' + str(int(2 * self.__runTimeout.total_seconds())) + ':-50:100',
        'DS:high:GAUGE:' + str(int(2 * self.__runTimeout.total_seconds())) + ':-50:100',
        'DS:limitlow:GAUGE:' + str(int(2 * self.__runTimeout.total_seconds())) + ':-50:100',
        'DS:limithigh:GAUGE:' + str(int(2 * self.__runTimeout.total_seconds())) + ':-50:100',
      	'RRA:AVERAGE:0.5:1:60',
      	'RRA:AVERAGE:0.5:1:1440',
      	'RRA:AVERAGE:0.5:5:12',
      	'RRA:AVERAGE:0.5:5:288',
      	'RRA:AVERAGE:0.5:30:12',
      	'RRA:AVERAGE:0.5:30:288',
      	'RRA:AVERAGE:0.5:60:168',
      	'RRA:AVERAGE:0.5:60:720',
        'RRA:AVERAGE:0.5:1800:730',
      	'RRA:AVERAGE:0.5:3600:365',
      	'RRA:MIN:0.5:1:60',
      	'RRA:MIN:0.5:1:1440',
      	'RRA:MIN:0.5:5:12',
      	'RRA:MIN:0.5:5:288',
      	'RRA:MIN:0.5:30:12',
      	'RRA:MIN:0.5:30:288',
      	'RRA:MIN:0.5:60:168',
      	'RRA:MIN:0.5:60:720',
        'RRA:MIN:0.5:1800:730',
      	'RRA:MIN:0.5:3600:365',
      	'RRA:MAX:0.5:1:60',
      	'RRA:MAX:0.5:1:1440',
      	'RRA:MAX:0.5:5:12',
      	'RRA:MAX:0.5:5:288',
      	'RRA:MAX:0.5:30:12',
      	'RRA:MAX:0.5:30:288',
      	'RRA:MAX:0.5:60:168',
      	'RRA:MAX:0.5:60:720',
        'RRA:MAX:0.5:1800:730',
      	'RRA:MAX:0.5:3600:365')

  def __createWeatherDatabase(self,id):
    self.__checkLogFolder()
    if not os.path.isfile(self.__log_location + '/weather_' + id + '.rrd'):
      terrarium_log.info('Creating new RDD database for weather with ID %s',id)
      rrdtool.create(self.__log_location + '/weather_' + id + '.rrd', '--step',str(self.__runTimeout.total_seconds()),
        'DS:current:GAUGE:120:-50:50',
        'DS:low:GAUGE:120:-50:50',
        'DS:high:GAUGE:120:-50:50',
        'RRA:AVERAGE:0.5:1:1440',
        'RRA:MIN:0.5:1:1440',
        'RRA:MAX:0.5:1:1440',
        'RRA:AVERAGE:0.5:30:1440',
        'RRA:MIN:0.5:30:1440',
        'RRA:MAX:0.5:30:1440')

  def __createSwitchDatabase(self,id):
    self.__checkLogFolder()
    if not os.path.isfile(self.__log_location + '/switch_' + id + '.rrd'):
      terrarium_log.info('Creating new RDD database for switch with ID %s',id)
      rrdtool.create(self.__log_location + '/switch_' + id + '.rrd', '--step',str(self.__runTimeout.total_seconds()),
        'DS:on:GAUGE:120:0:1',
        'DS:off:GAUGE:120:0:1',
        'RRA:AVERAGE:0.5:1:1440',
        'RRA:MIN:0.5:1:1440',
        'RRA:MAX:0.5:1:1440',
        'RRA:AVERAGE:0.5:30:1440',
        'RRA:MIN:0.5:30:1440',
        'RRA:MAX:0.5:30:1440')

  def online(self):
    return datetime.now() - self.__lastRun < 3 * self.__runTimeout
