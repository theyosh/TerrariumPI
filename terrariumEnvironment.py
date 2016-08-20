# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from time import sleep
from copy import copy

import thread

import logging
terrarium_log = logging.getLogger('root')

class terrariumEnvironment:

  def __init__(self,weatherObj,sensorList,powerswitchList,configObj,twitterObj,doorObj,configObj2):
    terrarium_log.info('Loading environment settings')
    self.__weather = weatherObj
    self.__config = configObj2
    self.__twitter = twitterObj
    self.__door = doorObj

    self.__powerswitches = powerswitchList
    self.__sensors = sensorList

    self.__runTimeout = timedelta(seconds=15)
    self.__lastRun = datetime.fromtimestamp(0)

    #Lights object
    self.__lights = { 'enabled'       : configObj['light_enabled'] in ['1','True','true','on', True],
                      'active'        : True,
                      'switches'      : [],
                      'sensors'       : [],
                      'trigger_on'    : configObj['light_on'],
                      'trigger_off'   : configObj['light_off'],
                      'current_on'    : False,
                      'current_off'   : False,
                      'current_state' : 'unknown',
                      'last_change'   : datetime.fromtimestamp(0),
                      'max_duration'  : timedelta(seconds=int(configObj['light_duration_max_hours'])*3600),
                      'min_duration'  : timedelta(seconds=int(configObj['light_duration_min_hours'])*3600),
                      'time_shift'    : timedelta(seconds=int(float(configObj['light_duration_time_shift']) * 3600)),
                    }

    switches = configObj['light_switch'].split(',')
    for switch in switches:
      if switch in self.__powerswitches:
        self.__lights['switches'].append(self.__powerswitches[switch])

    sensors = configObj['light_sensor'].split(',')
    for sensor in sensors:
      if sensor in self.__sensors:
        self.__lights['sensors'].append(self.__sensors[sensor])

    #Heater object
    self.__heater = { 'enabled'       : configObj['heater_enabled'] in ['1','True','true','on', True],
                      'active'        : True,
                      'switches'      : [],
                      'sensors'       : [],
                      'trigger_on'    : configObj['heater_on'],
                      'trigger_off'   : configObj['heater_off'],
                      'current_on'    : False,
                      'current_off'   : False,
                      'current_state' : 'off',
                      'avg_val'       : -1,
                      'avg_min'       : -1,
                      'avg_max'       : -1,
                      'last_change'   : datetime.fromtimestamp(0),
                      'modus'         : configObj['heater_modus'],
                      'day_active'    : configObj['heater_active_during_day'] in ['1','True','true','on', True],
                      'alarm'         : False,
                      'direction'     : 'down'
                    }

    switches = configObj['heater_switch'].split(',')
    for switch in switches:
      if switch in self.__powerswitches:
        self.__heater['switches'].append(self.__powerswitches[switch])

    sensors = configObj['heater_sensor'].split(',')
    for sensor in sensors:
      if sensor in self.__sensors:
        self.__heater['sensors'].append(self.__sensors[sensor])


    # Humidity object
    self.__humidity = { 'enabled'         : configObj['humidity_enabled'] in ['1','True','true','on', True],
                        'active'          : True,
                        'switches'        : [],
                        'sensors'         : [],
                        'current_on'      : False,
                        'current_off'     : False,
                        'current_state'   : 'unknown',
                        'avg_val'         : -1,
                        'avg_min'         : -1,
                        'avg_max'         : -1,
                        'last_change'     : datetime.fromtimestamp(0),
                        'switch_timeout'  : timedelta(seconds=int(configObj['humidity_switch_timeout'])),
                        'duration'        : timedelta(seconds=int(configObj['humidity_switch_duration'])),
                        'night_active'    : configObj['humidity_active_during_night'] in ['1','True','true','on'],
                        'alarm'           : False
                      }

    switches = configObj['humidity_switch'].split(',')
    for switch in switches:
      if switch in self.__powerswitches:
        self.__humidity['switches'].append(self.__powerswitches[switch])

    sensors = configObj['humidity_sensor'].split(',')
    for sensor in sensors:
      if sensor in self.__sensors:
        self.__humidity['sensors'].append(self.__sensors[sensor])

    thread.start_new_thread(self.__checker, ())

  def __checker(self):
    while True:
      terrarium_log.debug('Checking environment ...')
      self.__lastRun = datetime.now()

      terrarium_log.debug('Checking lights status and settings')
      self.__checkLights()
      terrarium_log.debug('Checking temperature status and settings')
      self.__checkHeater()
      terrarium_log.debug('Checking humidity status and settings')
      self.__checkHumidity()

      duration = datetime.now() - self.__lastRun
      terrarium_log.debug('Updating environment took %d seconds', duration.total_seconds())
      if duration < self.__runTimeout:
        terrarium_log.debug('Next environment update in %d seconds', (self.__runTimeout - duration).total_seconds())
        sleep(int((self.__runTimeout - duration).total_seconds()))

  def __checkLights(self):
    if not self.__lights['enabled']:
      self.__lights['current_state'] = 'disabled'
      terrarium_log.warn('Lights are disabled')
    else:
      terrarium_log.debug('Getting lights switch on and off time')
      if 'sunrise' == self.__lights['trigger_on']:
        self.__lights['current_on'] = self.__weather.getSunRiseTime()

      else:
        self.__lights['current_on'] = self.__lights['trigger_on'].split(':')
        self.__lights['current_on'] = datetime(int((datetime.now()).strftime('%Y')),
                                               int((datetime.now()).strftime('%m')),
                                               int((datetime.now()).strftime('%d')),
                                               int(self.__lights['current_on'][0]),
                                               int(self.__lights['current_on'][1]))

      terrarium_log.debug('Trigger for lights switch on is based on %s which is at %s', ('sunrise' if 'sunrise' == self.__lights['trigger_on'] else 'static time'), 
                                                                                        self.__lights['current_on'].strftime('%d-%m-%Y %H:%M:%S'))

      if 'sunset' == self.__lights['trigger_off']:
        self.__lights['current_off'] = self.__weather.getSunSetTime()

      else:
        self.__lights['current_off'] = self.__lights['trigger_off'].split(':')
        self.__lights['current_off'] = datetime(int((datetime.now()).strftime('%Y')),
                                                int((datetime.now()).strftime('%m')),
                                                int((datetime.now()).strftime('%d')),
                                                int(self.__lights['current_off'][0]),
                                                int(self.__lights['current_off'][1]))

      terrarium_log.debug('Trigger for lights switch off is based on %s which is at %s', ('sunset' if 'sunset' == self.__lights['trigger_off'] else 'static time'), 
                                                                                        self.__lights['current_off'].strftime('%d-%m-%Y %H:%M:%S'))

      current_duration = self.__lights['current_off'] - self.__lights['current_on']
      terrarium_log.debug('Total durating of lights on is %d seconds', current_duration.total_seconds())
      if not self.__lights['min_duration'] < current_duration < self.__lights['max_duration']:
        terrarium_log.debug('Total lights on duration is not within specified boundaries')
        if current_duration < self.__lights['min_duration']:
          delta = (self.__lights['min_duration'] - current_duration)/2
          terrarium_log.debug('Increasing lights on duration with %d seconds',delta.total_seconds()*2)
        else:
          delta = (current_duration-self.__lights['max_duration'])/-2
          terrarium_log.debug('Decreasing lights on duration with %d seconds',delta.total_seconds()*2)

        terrarium_log.debug('Old lights on duration was on at %s and off at %s which gave %d seconds of light', self.__lights['current_on'].strftime('%d-%m-%Y %H:%M:%S'),
                                                                                                                self.__lights['current_off'].strftime('%d-%m-%Y %H:%M:%S'),
                                                                                                                current_duration.total_seconds())
        self.__lights['current_on'] -= delta
        self.__lights['current_off'] += delta

        terrarium_log.debug('New lights on duration is on at %s and off at %s which give %d seconds of light', self.__lights['current_on'].strftime('%d-%m-%Y %H:%M:%S'), 
                                                                                                                self.__lights['current_off'].strftime('%d-%m-%Y %H:%M:%S'), 
                                                                                                                (self.__lights['current_off']-self.__lights['current_on']).total_seconds())

      if self.__lights['time_shift'].total_seconds() != 0:
        self.__lights['current_on'] += self.__lights['time_shift']
        self.__lights['current_off'] += self.__lights['time_shift']
        terrarium_log.debug('Shifting lights on and off with %s seconds to new starttime %s and endtime %s' , self.__lights['time_shift'], self.__lights['current_on'].strftime('%d-%m-%Y %H:%M:%S'),
                                                                                                                self.__lights['current_off'].strftime('%d-%m-%Y %H:%M:%S'))

      if not self.__lights['active']:
        terrarium_log.warn('Light system is manually disabled')

      else:
        if self.__lights['current_on'] < datetime.now() < self.__lights['current_off']:
          # Turn the lights on!
          if 'off' == self.__lights['current_state']:
            # Old state was off, so this is the actual switch!
            self.__lights['last_change'] = datetime.now()
            tweet = {'media' : 'webroot/images/weather_icons/sunrise.png'}
            if self.__lights['last_change'].isoweekday() > 5:
              # Weekend
              tweet['message'] = 'It is weekend. Let us sleep out some more time!: ' + self.__lights['current_on'].strftime('%d-%m-%Y %H:%M:%S')
            else:
              tweet['message'] = 'A brand new day started at: ' + self.__lights['current_on'].strftime('%d-%m-%Y %H:%M:%S')
            self.__twitter.post(tweet)

          self.__lights['current_state'] = 'on'
          for switch in self.__lights['switches']:
            if switch.getState() == 0:
              terrarium_log.debug('Switching light on at switch %s(%s)', switch.getName(),switch.getID())
              switch.on()

        else:
          if 'on' == self.__lights['current_state']:
            # Old state was on, so this is the actual switch!
            self.__lights['last_change'] = datetime.now()
            tweet = {'media' : 'webroot/images/twitter/GekkoSleep1.png',
                     'message' : 'Good night: ' + self.__lights['current_off'].strftime('%d-%m-%Y %H:%M:%S')}
            self.__twitter.post(tweet)

          self.__lights['current_state'] = 'off'
          for switch in self.__lights['switches']:
            if switch.getState() == 1:
              terrarium_log.debug('Switching light off at switch %s(%s)', switch.getName(),switch.getID())
              switch.off()

      terrarium_log.info('The lights are turned on at %s and off at %s. The lights are current in state %s', self.__lights['current_on'].strftime('%d-%m-%Y %H:%M:%S'),
                                                                                                             self.__lights['current_off'].strftime('%d-%m-%Y %H:%M:%S'),
                                                                                                             self.__lights['current_state'])

  def __checkHeater(self):
    should_be_on = False
    if not self.__heater['enabled']:
      terrarium_log.warn('Heating is disabled')
      self.__heater['current_state'] = 'disabled'
    else:
      min_val = 0
      max_val = 0
      current_val = 0
      for sensor in self.__heater['sensors']:
        current_val += sensor.getCurrent()
        min_val += sensor.getMinLimit()
        max_val += sensor.getMaxLimit()

      self.__heater['avg_val'] = current_val / len(self.__heater['sensors'])
      self.__heater['avg_max'] = max_val / len(self.__heater['sensors'])
      self.__heater['avg_min'] = min_val / len(self.__heater['sensors'])
      self.__heater['alarm'] = not (self.__heater['avg_min'] < self.__heater['avg_val'] < self.__heater['avg_max'])

      terrarium_log.debug('Getting heater switch on and off time')
      if self.__heater['modus'] in ['weather','timer']:
        terrarium_log.debug('Getting heater on and off time')
        #self.__heater['alarm'] = self.__heater['avg_val'] > self.__heater['avg_max']
        if 'weather' == self.__heater['modus']:
          self.__heater['current_on'] = self.__weather.getSunSetTime()
          self.__lights['current_off'] = self.__weather.getSunRiseTime()
        elif 'timer' == self.__heater['modus']:
          self.__heater['current_on'] = self.__heater['trigger_on'].split(':')
          self.__heater['current_on'] = datetime( int((datetime.now()).strftime('%Y')),
                                                  int((datetime.now()).strftime('%m')),
                                                  int((datetime.now()).strftime('%d')),
                                                  int(self.__heater['current_on'][0]),
                                                  int(self.__heater['current_on'][1]))

          self.__heater['current_off'] = self.__heater['trigger_off'].split(':')
          self.__heater['current_off'] = datetime( int((datetime.now()).strftime('%Y')),
                                                  int((datetime.now()).strftime('%m')),
                                                  int((datetime.now()).strftime('%d')),
                                                  int(self.__heater['current_off'][0]),
                                                  int(self.__heater['current_off'][1]))

        #If stop time is earlier then the start time, the end time should be one day ahead
        if self.__heater['current_off'] < self.__heater['current_on']:
          self.__heater['current_off'] += timedelta(days=1)

        # If the end time is more than a day away, we have to shift one day back...
        if (self.__heater['current_off'] - datetime.now()).days >= 1:
          self.__heater['current_on'] -= timedelta(days=1)
          self.__heater['current_off'] -= timedelta(days=1)

        terrarium_log.debug('Heater system is based on %s. Heater should be running between %s and %s',('weater' if 'weather' == self.__heater['modus'] else 'static time'), 
                                                                                                       self.__heater['current_on'].strftime('%d-%m-%Y %H:%M:%S'), 
                                                                                                       self.__heater['current_off'].strftime('%d-%m-%Y %H:%M:%S'))

        should_be_on = self.__heater['current_on'] < datetime.now() < self.__heater['current_off'] and \
                       ( ('up' == self.__heater['direction'] and self.__heater['avg_max'] > self.__heater['avg_val']) \
                         or ('down' == self.__heater['direction'] and self.__heater['avg_min'] > self.__heater['avg_val']) \
                         or ('null' == self.__heater['direction']) )

        self.__heater['alarm'] = self.__heater['alarm'] if should_be_on else False

        terrarium_log.debug('Heater running state should be %s', ('running' if should_be_on else 'off'))

      elif 'sensor' == self.__heater['modus']:
        should_be_on = self.__heater['alarm'] and self.__heater['avg_min'] > self.__heater['avg_val']
        terrarium_log.debug('Heater system is based on temperature sensor and should be %s',('running' if should_be_on else 'off'))


      if not self.__heater['day_active'] and self.__weather.isDaytime():
        terrarium_log.warn('Heater system is disabled during day time')
        should_be_on = False

      if not self.__heater['active']:
        terrarium_log.warn('Heater system is manually disabled')
      else:

        if should_be_on:
          # Turn the heater on!
          if 'off' == self.__heater['current_state']:
          # Old state was off, so this is the actual switch!
            self.__heater['last_change'] = datetime.now()
            tweet = {'message' : 'Damm it is getting cold! Lucky we have a heater turning on: ' + (datetime.now()).strftime('%d-%m-%Y %H:%M:%S')}
            tweet['media'] = '/home/pi/terrarium/twitter_images/heater_on1.gif'

            self.__twitter.post(tweet)
          self.__heater['current_state'] = 'on'
          self.__heater['direction'] = 'up'
          for switch in self.__heater['switches']:
            if switch.getState() == 0:
              terrarium_log.info('Switching heater on at switch %s(%s)', switch.getName(),switch.getID())
              switch.on()

        else:
          if 'on' == self.__heater['current_state']:
          # Old state was on, so this is the actual switch!
            self.__heater['last_change'] = datetime.now()
            tweet = {'message' : 'It is like a sauna over here... Turning the heater off: ' + (datetime.now()).strftime('%d-%m-%Y %H:%M:%S')}
            self.__twitter.post(tweet)
          self.__heater['current_state'] = 'off'
          self.__heater['direction'] = 'down'
          for switch in self.__heater['switches']:
            if switch.getState() == 1:
              terrarium_log.info('Switching heater off at switch %s(%s)', switch.getName(),switch.getID())
              switch.off()

        terrarium_log.info('The heater is turned on at %s and off at %s. The heater current in state %s', self.__heater['current_on'].strftime('%d-%m-%Y %H:%M:%S'),
                                                                                                             self.__heater['current_off'].strftime('%d-%m-%Y %H:%M:%S'),
                                                                                                             self.__heater['current_state'])


  def __checkHumidity(self):
    # Some weard issues with the power switch.... make sure that the humidity system will be shutdown...
#    for switch in self.__humidity['switches']:
#      switch.off()

    if not self.__humidity['enabled']:
      self.__humidity['current_state'] = 'disabled'
      terrarium_log.warn('Humidity is disabled')
    else:
      terrarium_log.debug('Getting humidity switch on value')
      min_val = 0
      max_val = 0
      current_val = 0
      for sensor in self.__humidity['sensors']:
        logLine = 'Sensor ' + sensor.getName()
        current_val += sensor.getCurrent()
        min_val += sensor.getMinLimit()
        max_val += sensor.getMaxLimit()

      self.__humidity['avg_val'] = current_val / len(self.__humidity['sensors'])
      self.__humidity['avg_max'] = max_val / len(self.__humidity['sensors'])
      self.__humidity['avg_min'] = min_val / len(self.__humidity['sensors'])

      self.__humidity['alarm'] = self.__humidity['avg_min'] > self.__humidity['avg_val']
      if not self.__humidity['active']:
         terrarium_log.info('Humidity system is manually disabled')

      elif 'off' == self.__lights['current_state'] and not self.__humidity['night_active']:
        self.__humidity['current_state'] = 'inactive'
        self.__humidity['alarm'] = False
        terrarium_log.info('Lights are off and therefore the humidity check is inactive')

      elif 'on' == self.__lights['current_state'] or self.__humidity['night_active']:
        if self.__humidity['alarm'] and datetime.now() - self.__humidity['last_change'] > self.__humidity['switch_timeout']:
          terrarium_log.info('Trigger humidity system') 
          self.__humidity['current_state'] = 'on'
          for switch in self.__humidity['switches']:
            if switch.getState() == 0:
              terrarium_log.info('Trigger on switch %s(%s) for humidity',switch.getName(),switch.getID())
              if not self.__door.open():
                switch.on()
              else:
                terrarium_log.warn('Door is open, therefore the humidity will not be triggered')
            else:
              terrarium_log.warn('Humidity siwtch %s(%s) was already triggered!',switch.getName(),switch.getID())

          sleep(float(self.__humidity['duration'].total_seconds()))
          self.__humidity['current_state'] = 'off'
          for switch in self.__humidity['switches']:
            if switch.getState() == 1:
              terrarium_log.info('Trigger off switch %s(%s) for humidity',switch.getName(),switch.getID())
              switch.off()

          self.__humidity['last_change'] = datetime.now()

        elif self.__humidity['alarm']:
          terrarium_log.warn('Humidity is not ok, but the timeout of %d seconds has not been expired yet. Last action was %d seconds ago', self.__humidity['switch_timeout'].total_seconds(),
                                                                                                                                           (datetime.now() - self.__humidity['last_change']).total_seconds())

        else:
          terrarium_log.info('Humidity is all ok')
          self.__humidity['current_state'] = 'off'
          for switch in self.__humidity['switches']:
            if switch.getState() == 1:
              terrarium_log.info('Trigger off switch %s(%s) for humidity',switch.getName(),switch.getID())
              switch.off()

        terrarium_log.info('Humidity is in %s state', self.__humidity['current_state'])

  def _getJsonStatus(self,items):
    data = {}
    for key,value in items:
      if key in ['switches','sensors']:
        data[key] = []
        for item in value:
          data[key].append(item.getSettings())

      else:
        if type(value) == datetime:
          value = int(value.strftime('%s'))
        elif type(value) == timedelta:
          value = int(value.total_seconds())

        data[key] = value

    return data

# Environment Methods
# Power usage

  def getPowerStatus(self,format = 'json'):
    data = {'switches' : [{'id':'pi'}]}
    for switch in (self.__lights['switches'] + self.__humidity['switches'] + self.__heater['switches']):
      data['switches'].append({ 'id' : switch.getID()})

    return data
    

# Lights
  def getLightsStatus(self,format = 'json'):
    if 'json' == format:
      return self._getJsonStatus(self.__lights.iteritems())

    else:
      return self.__lights

  def getLightSettings(self):
    return self.getLightsStatus('json')

  def toggleLightsEngine(self):
    self.__lights['enabled'] = not self.__lights['enabled']
    return self.__lights['enabled']

  def toggleLightsTrigger(self):
    self.__lights['active'] = not self.__lights['active']
    return self.__lights['active']

  def toggleLights(self):
    for switch in self.__lights['switches']:
      if 'on' == self.__lights['current_state'] and switch.getState() == 1:
        switch.off()
      elif 'off' == self.__lights['current_state'] and switch.getState() == 0:
        switch.on()

    # Toggle the lights state
    self.__lights['current_state'] = 'off' if 'on' == self.__lights['current_state'] else 'on'
    return {'current' : self.__lights['current_state']}

#Heater
  def getHeaterStatus(self,format = 'json'):
    if 'json' == format:
      return self._getJsonStatus(self.__heater.iteritems())

    else:
      return self.__heater

  def getHeaterSettings(self):
    return self.getHeaterStatus('json')

  def toggleHeaterEngine(self):
    self.__heater['enabled'] = not self.__heater['enabled']
    return self.__heater['enabled']

  def toggleHeaterTrigger(self):
    self.__heater['active'] = not self.__heater['active']
    return self.__heater['active']

  def toggleHeater(self):
    for switch in self.__heater['switches']:
      if 'on' == self.__heater['current_state'] and switch.getState() == 1:
        switch.off()
      elif 'off' == self.__heater['current_state'] and switch.getState() == 0:
        switch.on()

    # Toggle the lights state
    self.__heater['current_state'] = 'off' if 'on' == self.__heater['current_state'] else 'on'
    return {'current' : self.__heater['current_state']}

#Humidity
  def getHumidityStatus(self,format = 'json'):
    if 'json' == format:
      return self._getJsonStatus(self.__humidity.iteritems())

    else:
      return self.__humidity

  def getHumiditySettings(self):
    return self.getHumidityStatus('json')

  def toggleHumidityEngine(self):
    self.__humidity['enabled'] = not self.__humidity['enabled']
    return self.__humidity['enabled']

  def toggleHumidityTrigger(self):
    self.__humidity['active'] = not self.__humidity['active']
    return self.__humidity['active']

  def toggleHumidity(self):
    for switch in self.__humidity['switches']:
      if 'on' == self.__humidity['current_state'] and switch.getState() == 1:
        switch.off()
      elif 'off' == self.__humidity['current_state'] and switch.getState() == 0:
        switch.on()

    # Toggle the lights state
    self.__humidity['current_state'] = 'off' if 'on' == self.__humidity['current_state'] else 'on'
    return {'current' : self.__humidity['current_state']}


  def getHeaterActive(self):
    return self.__heater['active']

  def getHeaterDayActive(self):
    return self.__heater['dayactive'] or not int(self.__heater['triggeron'].strftime('%s')) < int(time()) < int(self.__heater['triggeroff'].strftime('%s'))

  def getLightsActive(self):
    return self.__lights['active']

  def getHumidityActive(self):
    return self.__humidity['active']

  def getHumidityNightActive(self):
    return self.__humidity['nightactive'] or self.__light_on < int(time()) < self.__light_off

  def setEnvironmentLightConfig(self,enabled = False,on = 'sunrise',off = 'sunset',switches = '',sensors = '',min = 10,max = 10 ,shift = 0):
    self.__config.setEnvironmentLightConfig(enabled,on,off,switches,sensors,min,max,shift)

    switches = switches.split(',')
    self.__lights['switches'] = []
    for switch in switches:
      if switch in self.__powerswitches:
        self.__lights['switches'].append(self.__powerswitches[switch])

    sensors = sensors.split(',')
    self.__lights['sensors'] = []
    for sensor in sensors:
      if sensor in self.__sensors:
        self.__lights['sensors'].append(self.__sensors[sensor])

    self.__lights['enabled']      = enabled in ['1','True','true','on', True]
    self.__lights['trigger_on']   = on
    self.__lights['trigger_off']  = off
    self.__lights['max_duration'] = timedelta(seconds=int(max)*3600)
    self.__lights['min_duration'] = timedelta(seconds=int(min)*3600)
    self.__lights['time_shift']   = timedelta(seconds=int(float(shift)*3600))
    self.__checkLights()

    return True

  def setEnvironmentHeaterConfig(self, enabled = False, switches = '', sensors = '', modus = 'time', on = 0, off = 0, dayactive = False):
    self.__config.setEnvironmentHeaterConfig(enabled,switches,sensors,modus,on,off,dayactive)

    switches = switches.split(',')
    self.__heater['switches'] = []
    for switch in switches:
      if switch in self.__powerswitches:
        self.__heater['switches'].append(self.__powerswitches[switch])

    sensors = sensors.split(',')
    self.__heater['sensors'] = []
    for sensor in sensors:
      if sensor in self.__sensors:
        self.__heater['sensors'].append(self.__sensors[sensor])

    self.__heater['enabled']      = enabled in ['1','True','true','on', True]
    self.__heater['trigger_on']   = on
    self.__heater['trigger_off']  = off
    self.__heater['modus']        = modus
    self.__heater['day_active']   = dayactive in ['1','True','true','on', True]
    self.__checkHeater()
    return True

  def setEnvironmentHumidityConfig(self,enabled = False,switches = '',sensors = '',timeout = 60,duration = 15 ,nightactive = False):
    self.__config.setEnvironmentHumidityConfig(enabled,switches,sensors,timeout,duration,nightactive)

    switches = switches.split(',')
    self.__humidity['switches'] = []
    for switch in switches:
      if switch in self.__powerswitches:
        self.__humidity['switches'].append(self.__powerswitches[switch])

    sensors = sensors.split(',')
    self.__humidity['sensors'] = []
    for sensor in sensors:
      if sensor in self.__sensors:
        self.__humidity['sensors'].append(self.__sensors[sensor])

    self.__humidity['enabled']        = enabled in ['1','True','true','on', True]
    self.__humidity['switch_timeout'] = timedelta(seconds=int(timeout))
    self.__humidity['duration']       = timedelta(seconds=int(duration))
    self.__humidity['night_active']   = nightactive in ['1','True','true','on', True]

    self.__checkHumidity()
    return True

  def online(self):
    return datetime.now() - self.__lastRun < 3 * self.__runTimeout
