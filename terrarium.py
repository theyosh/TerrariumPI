#!/usr/bin/python

# -*- coding: utf-8 -*-

VERSION = 0.9

import logging.config
import logging
logging.config.fileConfig('terrarium_logging.conf')
terrarium_log = logging.getLogger('root')
LOG_DATE_FORMAT = '%d-%m-%Y %H:%M:%S'


from terrariumConfig import terrariumConfig
from terrariumSensor import terrariumSensor
from terrariumSwitch import terrariumSwitch
from terrariumWebcam import terrariumWebcam
from terrariumWeather import terrariumWeather
from terrariumDoor import terrariumDoor

from terrariumEngine import terrariumEngine
from terrariumCollector import terrariumCollector
#from terrariumLog import terrariumLog
from terrariumEnvironment import terrariumEnvironment
from terrariumTwitter import terrariumTwitter

from terrariumServer import terrariumServer

from datetime import datetime

class terrarium:
  #Start program
  startTime = datetime.now()
  terrarium_log.info('Starting terrarium server %.1f at %s',VERSION,startTime.strftime(LOG_DATE_FORMAT))

  #Create log object
  #log = terrariumLog(terrariumLog.INFO)

  #Read config
  terrarium_log.debug('Loading configuration')
  config = terrariumConfig()
 # log.setLogLevel(config.getLogLevel())

  # Create Door object
  terrarium_log.debug('Loading door sensor')
  door = terrariumDoor(config.getDoorGPIOPin())

  #Create Twitter object
  twitter = terrariumTwitter(config.getTwitterEnabled(),config)

  #Create Weather object
  terrarium_log.debug('Loading weahter data')
  weather = terrariumWeather(config)

  #Loading the switches
  terrarium_log.debug('Scanning for connected power switches')
  powerSwitchesFound = terrariumSwitch.scan()
  powerSwitches = {}
  for powerSwitch in powerSwitchesFound:
    switch = terrariumSwitch(powerSwitch['nr'],powerSwitch['device'],powerSwitch['type'],config)
    powerSwitches[switch.getID()] = switch
    terrarium_log.debug('Loaded switch: %s',switch.getName())

  terrarium_log.info('Loaded %d switches',len(powerSwitches))

  #Loading the sensors
  terrarium_log.debug('Scanning for connected 1-wire sensors')
  terrarium_log.debug('Using OWS port number %d', config.getOWSPortnumber())

  sensorsFound = terrariumSensor.scan(config.getOWSPortnumber())
#  log.logLine(terrariumLog.MOREINFO,'Found ' + str(len(sensorsFound)) + ' sensors...')
  sensors = {}
  for sensor in sensorsFound:
    sensor = terrariumSensor(sensor['sensor'],sensor['type'],config)
    sensors[sensor.getID()] = sensor
    terrarium_log.debug('Loaded sensor type %s with name %s',sensor.getType(),sensor.getName())

  terrarium_log.info('Loaded %d sensors',len(sensors))

  #Loading the webcams
  terrarium_log.debug('Scanning for online webcams')
  webcamConfigList = config.getWebcamsList()
  webCams = {}
  for webcamConfig in webcamConfigList:
    webCam = terrariumWebcam(webcamConfig['name'],webcamConfig['location'],webcamConfig['archive'],webcamConfig['rotation'],config)
    webCams[webCam.getID()] = webCam
    terrarium_log.debug('Found webcam %s at location %s', webCam.getName(), webCam.getUrl())

  terrarium_log.info('Loaded %d webcams',len(webCams))


  environment = terrariumEnvironment(weather,sensors,powerSwitches,config.getEnvironmentConfig(),twitter,door,config)
  terrarium_log.info('Started the terrarium environment')

  collector = terrariumCollector(config,weather,sensors,powerSwitches,config.getEnvironmentConfig(),environment)
  terrarium_log.info('Started the terrarium collector')

  engine = terrariumEngine(weather,sensors,powerSwitches,webCams)
  terrarium_log.info('Started the terrarium engine')

  config.saveConfig()
  terrarium_log.info('Saving configuration after startup')

  terrarium_log.info('Sarted the terrarium REST API server on location: http://%s:%d',config.getServerIP(),config.getServerPort())
  server = terrariumServer(config.getServerIP(),config.getServerPort(),config.getServerAdmin(),config.getServerPassword(),weather,sensors,powerSwitches,webCams,environment,collector,engine,twitter,door,config)

if __name__ == "__main__":
  terrarium()
