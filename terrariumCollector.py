# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from time import sleep, time
from threading import Thread
import thread
import os
import math
import copy

import subprocess
import rrdtool

import logging
terrarium_log = logging.getLogger('root')

class terrariumCollector(Thread):
  TYPES = {'sensor'   : { 'rddtype' : 'GAUGE', 'lines' : ['low','high','limitlow','limithigh'], 'min' : -20, 'max' : 110 },
           'weather'  : { 'rddtype' : 'GAUGE', 'lines' : ['low','high'], 'min' : -20, 'max' : 60 },
           'switch'   : { 'rddtype' : 'DERIVE', 'lines' : [], 'min' : 0, 'max' : 'U' }
          }


#DERIVE
#  rrd_types = {'sensor':'GAUGE', 'weather' : 'GAUGE', 'switch' : 'GAUGE'}
#  rrd_lines = {'sensor': ['low','high','limitlow','limithigh'],
#                 'weather': ['low','high'],
#                'switch' : []}
#
#    rrd_min_values = {'sensor': -20, 'weather' : -20, 'switch' : 0}
#    rrd_max_values = {'sensor': 110, 'weather' : 110 , 'switch': 'U'}


  def __init__(self,config,weatherObj,sensorList,powerswitchList,webcamList,environment,logtimeout = 60):
    Thread.__init__(self)
    self.__log_location = 'webroot/rrd'

    self.__config = config
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
      terrarium_log.debug('Running PI data')
      self.updatePIData()

      duration = datetime.now() - self.__lastRun
      terrarium_log.debug('Updating collector took %d seconds', duration.total_seconds())
      if duration < self.__runTimeout:
        terrarium_log.debug('Next collector update in %d seconds', (self.__runTimeout - duration).total_seconds())
        sleep((self.__runTimeout - duration).total_seconds())

  def updatePIData(self):
    if self.__write_log:
      self.__createPIDatabase()
      usage = (float(self.__config.getPiWattage()) / 3600.0) * float(self.__config.getRunningTime())
#      print(str(datetime.now()) + ': RRD Tool update switch PI data: %.5f' % usage )
      rrdtool.update(self.__log_location + '/switch_pi.rrd','N:%s' %( int(round( usage * 60000 ))))

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
          usage = switch.getPowerUsage()
#          print( str(datetime.now()) + ': RRD Tool update switch %s data: %.5f' %( switch.getName(), usage ))
          rrdtool.update(self.__log_location + '/switch_' + switchid + '.rrd',
                          'N:%s' %( int(round( usage * 60000) )))

  def getRRDDatabase(self,databaseid,period = 'day',format = 'json'):
    cache_key = databaseid + '' + period
    if cache_key in self.__cache_data and (datetime.now() - self.__cache_data[cache_key]['time']).total_seconds() <= 60:
      terrarium_log.debug('Getting cached RDD data')
      return self.__cache_data[cache_key]['data']

    terrarium_log.debug('Getting/generating fresh RDD data: %s, period: %s', databaseid, period)
    periodStart = '-1d'
    if 'week' == period:
      periodStart = '-1w'
    elif 'month' == period:
      periodStart = '-1m'
    elif 'year' == period:
      periodStart = '-1y'

    type = 'weather'
    if 'switch_' in databaseid:
      type = 'switch'
    elif 'sensor_' in databaseid:
      type = 'sensor'

    rrdcmd = '/usr/bin/rrdtool xport --step ' + str(int(self.__runTimeout.total_seconds())) + ' --end -1 --start ' + periodStart + ' '

    lines = ['current'] + terrariumCollector.TYPES[type]['lines']
    for line in lines:
      if type == 'switch':
        rrdcmd += 'DEF:tmp' + line + '=' + self.__log_location + '/' + databaseid + '.rrd:' + line + ':AVERAGE '
        rrdcmd += 'CDEF:' + line + '=tmp' + line + ',0.001,* '
      else:
        rrdcmd += 'DEF:' + line + '=' + self.__log_location + '/' + databaseid + '.rrd:' + line + ':AVERAGE '

      rrdcmd += 'XPORT:' + line + ':"' + line + '" '

    #print('Run data graph command:\n' + rrdcmd)
    p = subprocess.Popen(rrdcmd,stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    # Get the right labels... saves some time...
    legend = []
    datarow_data = {'timestamp': 0}
    for data in ET.fromstring(output).findall('./meta/legend/entry'):
      legend.append(data.text)
      datarow_data[data.text] = 0

    maxvalue = -9999
    minvalue = 9999
    returndata = []

    for data in ET.fromstring(output).findall('./data/row'):
      datarow = copy.deepcopy(datarow_data)
      datarow['timestamp'] = int(data.find('t').text) * 1000

      valueCounter = 0
      invalidRow = False
      for value in data.findall('v'):
        value = float(value.text)
        if 'nan' == str(value):
          # If we have no data yet, this is to 'early' data. Just skip the row
          if len(returndata) == 0:
            invalidRow = True
            break
          else:
            # Get the previous value to continue the line....
            value = returndata[len(returndata)-1][legend[valueCounter]]
          
        datarow[legend[valueCounter]] = value
        valueCounter += 1

        if value > maxvalue:
          maxvalue = value
        if value < minvalue:
          minvalue = value

      if not invalidRow:
        returndata.append(datarow)

    self.__cache_data[cache_key] = {'time': datetime.now(), 'min': minvalue, 'max' : maxvalue,'data': returndata}
    return returndata

  def __checkLogFolder(self):
    if not os.path.isdir(self.__log_location):
      terrarium_log.info('Creating RDD log folders at location %s',self.__log_location)
      os.makedirs(self.__log_location)

  def __createRRD(self,id,type):
    self.__checkLogFolder()
    rrdfile = self.__log_location + '/' + type + '_' + id + '.rrd'
    
    # some defaults
 #   rrd_min_values = {'sensor': -20, 'weather' : -20, 'switch' : 0}
 #   rrd_max_values = {'sensor': 110, 'weather' : 110 , 'switch': 'U'}
 #   rrd_types = {'sensor':'GAUGE', 'weather' : 'GAUGE', 'switch' : 'DERIVE'}
 #   rrd_lines = {'sensor': ['low','high','limitlow','limithigh'],
 #                'weather': ['low','high'],
 #     		'switch' : []}

    if not os.path.isfile(rrdfile):
      terrarium_log.info('Creating new RDD database for %s with ID %s',type,id)
      rrdcmd = [rrdfile, '--step',str(int(self.__runTimeout.total_seconds()))]
      # Always append line current
      lines = ['current'] + terrariumCollector.TYPES[type]['lines']
      for line in lines:

#      rrd_lines[type] = ['current'] + rrd_lines[type]

#      for line in rrd_lines[type]:
        rrdcmd.append('DS:' + line + ':' + terrariumCollector.TYPES[type]['rddtype'] \
                      + ':' + str(int(2 * self.__runTimeout.total_seconds())) + ':' + str(terrariumCollector.TYPES[type]['min']) \
                      + ':' + str(terrariumCollector.TYPES[type]['max']))

#rrd_min_values[type]) + ':' + str(rrd_max_values[type]))

      # Average for 400 times 1 day (86400) every minute or self.__runTimeout.total_seconds() time
      rrdcmd.append('RRA:AVERAGE:0.5:1:' + str(int(( 1 * 86400) / self.__runTimeout.total_seconds())))

      # Average for 1 week (604800) every 30 minutes (1800)  measurement
      rrdcmd.append('RRA:AVERAGE:0.5:' + str(int(1800 / self.__runTimeout.total_seconds())) + ':' + str(int(604800 / (1800 / self.__runTimeout.total_seconds()) ) ))
      # Average for 1 month (2629744) every 2 hours (7200) measurement
      rrdcmd.append('RRA:AVERAGE:0.5:' + str(int(7200 / self.__runTimeout.total_seconds())) + ':' + str(int(2629744 / (7200 / self.__runTimeout.total_seconds()) ) ))
      # Average for 1 year every (31556926) every 6 hours (21600) measurement
      rrdcmd.append('RRA:AVERAGE:0.5:' + str(int(21600 / self.__runTimeout.total_seconds())) + ':' + str(int(31556926 / (21600 / self.__runTimeout.total_seconds()) )) )

      rrdtool.create(rrdcmd)

  def __createSensorDatabase(self,id):
    self.__createRRD(id,'sensor')

  def __createWeatherDatabase(self,id):
    self.__createRRD(id,'weather')

  def __createSwitchDatabase(self,id):
    self.__createRRD(id,'switch')

  def __createPIDatabase(self):
    self.__createRRD('pi','switch')

  def online(self):
    return datetime.now() - self.__lastRun < 1 * self.__runTimeout
