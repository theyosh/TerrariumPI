# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import thread
import datetime
import time

from threading import Timer
from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumEnvironment(object):
  LOOP_TIMEOUT = 15

  def __init__(self, sensors, power_switches, weather, door_status, config):
    logger.debug('Init terrariumPI environment')

    # Config callback
    self.config = config
    # Door status callback
    self.is_door_open = door_status

    self.sensors = sensors
    self.power_switches = power_switches
    self.weather = weather

    self.load_environment()

    self.__running = True
    thread.start_new_thread(self.__engine_loop, ())

  def load_environment(self, data = None):
    # Load Sensors, with ID as index
    starttime = time.time()
    reloading = data is not None

    logger.info('%s terrariumPI Environment system' % ('Reloading' if reloading else 'Loading',))

    data = (self.config() if not reloading else data)
    # Cleanup of empty fields.....
    config_data = {}
    for part in data:
      if part not in config_data:
        config_data[part] = {}

      for field in data[part]:
        if not (data[part][field] == '' or data[part][field] is None):
          config_data[part][field] = data[part][field]

    if len(config_data['light'].keys()) == 0 or not reloading:
      self.light = {}

    self.light['mode']           = 'disabled' if 'mode' not in config_data['light'] else config_data['light']['mode']
    self.light['on']             = '00:00'    if 'on' not in config_data['light'] else config_data['light']['on']
    self.light['off']            = '00:00'    if 'off' not in config_data['light'] else config_data['light']['off']
    self.light['on_duration']    = 60.0       if 'on_duration' not in config_data['light'] else float(config_data['light']['on_duration'])
    self.light['off_duration']   = 60.0       if 'off_duration' not in config_data['light'] else float(config_data['light']['off_duration'])
    self.light['hours_shift']    = 0.0        if 'hours_shift' not in config_data['light'] else float(config_data['light']['hours_shift'])
    self.light['min_hours']      = 0.0        if 'min_hours' not in config_data['light'] else float(config_data['light']['min_hours'])
    self.light['max_hours']      = 0.0        if 'max_hours' not in config_data['light'] else float(config_data['light']['max_hours'])
    self.light['power_switches'] = []         if ('power_switches' not in config_data['light'] or config_data['light']['power_switches'] in ['',None]) else config_data['light']['power_switches']

    if not isinstance(self.light['power_switches'], list):
      self.light['power_switches'] = self.light['power_switches'].split(',')

    self.light['enabled']        =  'disabled' != self.light['mode']


    if len(config_data['sprayer'].keys()) == 0 or not reloading:
      self.sprayer = {}

    self.sprayer['mode']           = 'disabled' if 'mode' not in config_data['sprayer'] else config_data['sprayer']['mode']
    self.sprayer['on']             = '00:00'    if 'on' not in config_data['sprayer'] else config_data['sprayer']['on']
    self.sprayer['off']            = '00:00'    if 'off' not in config_data['sprayer'] else config_data['sprayer']['off']
    self.sprayer['on_duration']    =  1.0       if 'on_duration' not in config_data['sprayer'] else float(config_data['sprayer']['on_duration'])
    self.sprayer['off_duration']   = 59.0       if 'off_duration' not in config_data['sprayer'] else float(config_data['sprayer']['off_duration'])
    self.sprayer['night_enabled']  = False      if 'night_enabled' not in config_data['sprayer'] else terrariumUtils.is_true(config_data['sprayer']['night_enabled'])
    self.sprayer['spray_duration'] = 0.0        if 'spray_duration' not in config_data['sprayer'] else float(config_data['sprayer']['spray_duration'])
    self.sprayer['spray_timeout']  = 120.0      if 'spray_timeout' not in config_data['sprayer'] else float(config_data['sprayer']['spray_timeout'])
    self.sprayer['power_switches'] = []         if ('power_switches' not in config_data['sprayer'] or config_data['sprayer']['power_switches'] in ['',None]) else config_data['sprayer']['power_switches']
    self.sprayer['sensors']        = []         if ('sensors' not in config_data['sprayer'] or config_data['sprayer']['sensors'] in ['',None]) else config_data['sprayer']['sensors']

    if not isinstance(self.sprayer['power_switches'], list):
      self.sprayer['power_switches'] = self.sprayer['power_switches'].split(',')
    if not isinstance(self.sprayer['sensors'], list):
      self.sprayer['sensors'] = self.sprayer['sensors'].split(',')

    self.sprayer['enabled']        =  'disabled' != self.sprayer['mode']
    self.sprayer['lastaction']     = int(time.time())


    if len(config_data['watertank'].keys()) == 0 or not reloading:
      self.watertank = {}

    self.watertank['mode']           = 'disabled' if 'mode' not in config_data['watertank'] else config_data['watertank']['mode']
    self.watertank['on']             = '00:00'    if 'on' not in config_data['watertank'] else config_data['watertank']['on']
    self.watertank['off']            = '00:00'    if 'off' not in config_data['watertank'] else config_data['watertank']['off']
    self.watertank['on_duration']    =  1.0       if 'on_duration' not in config_data['watertank'] else float(config_data['watertank']['on_duration'])
    self.watertank['off_duration']   = 59.0       if 'off_duration' not in config_data['watertank'] else float(config_data['watertank']['off_duration'])
    self.watertank['pump_duration']  = 0.0        if 'pump_duration' not in config_data['watertank'] else float(config_data['watertank']['pump_duration'])
    self.watertank['volume']         = 1.0        if 'volume' not in config_data['watertank'] else float(config_data['watertank']['volume'])
    self.watertank['height']         = 1.0        if 'height' not in config_data['watertank'] else float(config_data['watertank']['height'])
    self.watertank['power_switches'] = []         if ('power_switches' not in config_data['watertank'] or config_data['watertank']['power_switches'] in ['',None]) else config_data['watertank']['power_switches']
    self.watertank['sensors']        = []         if ('sensors' not in config_data['watertank'] or config_data['watertank']['sensors'] in ['',None]) else config_data['watertank']['sensors']

    if not isinstance(self.watertank['power_switches'], list):
      self.watertank['power_switches'] = self.watertank['power_switches'].split(',')
    if not isinstance(self.watertank['sensors'], list):
      self.watertank['sensors'] = self.watertank['sensors'].split(',')

    self.watertank['enabled']        =  'disabled' != self.watertank['mode']
    self.watertank['lastaction']     = int(time.time())


    if len(config_data['heater'].keys()) == 0 or not reloading:
      self.heater = {}

    self.heater['mode']             = 'disabled' if 'mode' not in config_data['heater'] else config_data['heater']['mode']
    self.heater['on']               = '00:00'    if 'on' not in config_data['heater'] else config_data['heater']['on']
    self.heater['off']              = '00:00'    if 'off' not in config_data['heater'] else config_data['heater']['off']
    self.heater['on_duration']      = 60.0       if 'on_duration' not in config_data['heater'] else float(config_data['heater']['on_duration'])
    self.heater['off_duration']     = 60.0       if 'off_duration' not in config_data['heater'] else float(config_data['heater']['off_duration'])
    self.heater['day_enabled']      = False      if 'day_enabled' not in config_data['heater'] else terrariumUtils.is_true(config_data['heater']['day_enabled'])
    self.heater['settle_timeout']   = 120.0      if 'settle_timeout' not in config_data['heater'] else float(config_data['heater']['settle_timeout'])
    self.heater['night_difference'] = 0.0      if 'night_difference' not in config_data['heater'] else float(config_data['heater']['night_difference'])
    self.heater['night_source']     = 'weather'     if 'night_source' not in config_data['heater'] else config_data['heater']['night_source']
    self.heater['power_switches']   = []         if ('power_switches' not in config_data['heater'] or config_data['heater']['power_switches'] in ['',None]) else config_data['heater']['power_switches']
    self.heater['sensors']          = []         if ('sensors' not in config_data['heater'] or config_data['heater']['sensors'] in ['',None]) else config_data['heater']['sensors']

    if not isinstance(self.heater['power_switches'], list):
      self.heater['power_switches'] = self.heater['power_switches'].split(',')
    if not isinstance(self.heater['sensors'], list):
      self.heater['sensors'] = self.heater['sensors'].split(',')

    self.heater['enabled']        =  'disabled' != self.heater['mode']
    self.heater['night_modus']    = False
    self.heater['lastaction']     = int(time.time())


    if len(config_data['cooler'].keys()) == 0 or not reloading:
      self.cooler = {}

    self.cooler['mode']           = 'disabled' if 'mode' not in config_data['cooler'] else config_data['cooler']['mode']
    self.cooler['on']             = '00:00'    if 'on' not in config_data['cooler'] else config_data['cooler']['on']
    self.cooler['off']            = '00:00'    if 'off' not in config_data['cooler'] else config_data['cooler']['off']
    self.cooler['on_duration']    = 60.0       if 'on_duration' not in config_data['cooler'] else float(config_data['cooler']['on_duration'])
    self.cooler['off_duration']   = 60.0       if 'off_duration' not in config_data['cooler'] else float(config_data['cooler']['off_duration'])
    self.cooler['night_enabled']  = False      if 'night_enabled' not in config_data['cooler'] else terrariumUtils.is_true(config_data['cooler']['night_enabled'])
    self.cooler['power_switches'] = []         if ('power_switches' not in config_data['cooler'] or config_data['cooler']['power_switches'] in ['',None]) else config_data['cooler']['power_switches']
    self.cooler['sensors']        = []         if ('sensors' not in config_data['cooler'] or config_data['cooler']['sensors'] in ['',None]) else config_data['cooler']['sensors']

    if not isinstance(self.cooler['power_switches'], list):
      self.cooler['power_switches'] = self.cooler['power_switches'].split(',')
    if not isinstance(self.cooler['sensors'], list):
      self.cooler['sensors'] = self.cooler['sensors'].split(',')

    self.cooler['enabled']        =  'disabled' != self.cooler['mode']

    self.__check_available_power_switches()
    self.__check_available_sensors()
    self.__update_timing()

    logger.info('Done %s terrariumPI Environment %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                                      time.time()-starttime))

  def __check_available_power_switches(self):
    # Filter out the non existing powerswiches
    self.light['power_switches']     = [switchid for switchid in self.light['power_switches'] if switchid in self.power_switches]
    self.sprayer['power_switches']   = [switchid for switchid in self.sprayer['power_switches'] if switchid in self.power_switches]
    self.heater['power_switches']    = [switchid for switchid in self.heater['power_switches'] if switchid in self.power_switches]
    self.cooler['power_switches']    = [switchid for switchid in self.cooler['power_switches'] if switchid in self.power_switches]
    self.watertank['power_switches'] = [switchid for switchid in self.watertank['power_switches'] if switchid in self.power_switches]

  def __check_available_sensors(self):
    # Filter out the non existing sensors
    self.sprayer['sensors']   = [sensorid for sensorid in self.sprayer['sensors'] if sensorid in self.sensors]
    self.heater['sensors']    = [sensorid for sensorid in self.heater['sensors'] if sensorid in self.sensors]
    self.cooler['sensors']    = [sensorid for sensorid in self.cooler['sensors'] if sensorid in self.sensors]
    self.watertank['sensors'] = [sensorid for sensorid in self.watertank['sensors'] if sensorid in self.sensors]

  def __check_active_sensors(self,part):
    sensorlist = self.sprayer['sensors']

    if 'heater' == part:
      sensorlist = self.heater['sensors']
    elif 'cooler' == part:
      sensorlist = self.cooler['sensors']
    elif 'watertank' == part:
      sensorlist = self.watertank['sensors']
    elif 'moisture' == part:
      sensorlist = self.moisture['sensors']
    elif 'ph' == part:
      sensorlist = self.ph['sensors']

    return len(sensorlist) == 0 or any(self.sensors[sensor].is_active() for sensor in sensorlist)

  def __update_timing(self,part = None):
    if part is None or part == 'light':
      if self.light['mode'] == 'weather':
        # Upate times based on weather
        self.light['on']  = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['rise'])
        self.light['off'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['set'])

        # Duration check
        duration = self.light['off'] - self.light['on']
        # Reduce the amount of hours if to much
        if self.light['max_hours'] > 0 and duration > datetime.timedelta(hours=self.light['max_hours']):
          duration -= datetime.timedelta(hours=self.light['max_hours'])
          self.light['on'] += datetime.timedelta(seconds=duration.total_seconds()/2)
          self.light['off'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
        # Increase the amount of hours if to little
        elif self.light['min_hours'] > 0 and duration < datetime.timedelta(hours=self.light['min_hours']):
          duration = datetime.timedelta(hours=self.light['min_hours']) - duration
          self.light['on'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
          self.light['off'] += datetime.timedelta(seconds=duration.total_seconds()/2)

        # Shift hours
        self.light['on'] += datetime.timedelta(hours=self.light['hours_shift'])
        self.light['off'] += datetime.timedelta(hours=self.light['hours_shift'])

        self.light['on'] = self.light['on'].strftime('%H:%M')
        self.light['off'] = self.light['off'].strftime('%H:%M')

      self.light['time_table']   = terrariumUtils.calculate_time_table(self.light['on'],self.light['off'],
                                                                       None if self.light['mode'] == 'weather' else self.light['on_duration'],
                                                                       None if self.light['mode'] == 'weather' else self.light['off_duration'])

      self.light['duration'] = terrariumUtils.duration(self.light['time_table'])

    if part is None or part == 'sprayer':
      self.sprayer['time_table'] = terrariumUtils.calculate_time_table(self.sprayer['on'],self.sprayer['off'],
                                                                       self.sprayer['on_duration'],self.sprayer['off_duration'])

      self.sprayer['duration'] = terrariumUtils.duration(self.sprayer['time_table'])

    if part is None or part == 'watertank':
      self.watertank['time_table'] = terrariumUtils.calculate_time_table(self.watertank['on'],self.watertank['off'],
                                                                       self.watertank['on_duration'],self.watertank['off_duration'])

      self.watertank['duration'] = terrariumUtils.duration(self.watertank['time_table'])

    if part is None or part == 'heater':
      if self.heater['mode'] == 'weather':
        self.heater['on']  = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['set']).strftime('%H:%M')
        self.heater['off'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['rise']).strftime('%H:%M')


      self.heater['time_table']  = terrariumUtils.calculate_time_table(self.heater['on'],self.heater['off'],
                                                                       None if self.heater['mode'] == 'weather' else self.heater['on_duration'],
                                                                       None if self.heater['mode'] == 'weather' else self.heater['off_duration'])

      self.heater['duration'] = terrariumUtils.duration(self.heater['time_table'])

    if part is None or part == 'cooler':
      if self.cooler['mode'] == 'weather':
        self.cooler['on']  = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['rise']).strftime('%H:%M')
        self.cooler['off'] = datetime.datetime.fromtimestamp(self.weather.get_data()['sun']['set']).strftime('%H:%M')

      self.cooler['time_table']  = terrariumUtils.calculate_time_table(self.cooler['on'],self.cooler['off'],
                                                                       None if self.cooler['mode'] == 'weather' else self.cooler['on_duration'],
                                                                       None if self.cooler['mode'] == 'weather' else self.cooler['off_duration'])

      self.cooler['duration'] = terrariumUtils.duration(self.cooler['time_table'])

  def update_timing(self):
    self.__update_timing()

  def __update_environment_state(self):
    self.sprayer['humidity']   = self.get_average_humidity(self.sprayer['sensors'])
    self.heater['temperature'] = self.get_average_temperature(self.heater['sensors'])
    self.cooler['temperature'] = self.get_average_temperature(self.cooler['sensors'])
    self.watertank['distance'] = self.get_average_distance(self.watertank['sensors'])

  def __engine_loop(self):
    logger.info('Starting engine')
    while self.__running:
      logger.debug('Environment starts new checks')
      starttime = time.time()

      self.__update_environment_state()

      # Light checks and actions
      if self.light['enabled']:
        logger.debug('Environment lighting is enabled in mode %s' % self.light['mode'])
        toggle_on = terrariumUtils.is_time(self.light['time_table'])

        if toggle_on is None:
          self.__update_timing('light')

        if toggle_on:
          if not self.is_light_on():
            logger.info('Environment is turning on the lights based on %s' % self.light['mode'])
          self.light_on()
        else:
          if self.is_light_on():
            logger.info('Environment is turning off the lights based on %s' % self.light['mode'])
          self.light_off()

      #else:
      #  logger.debug('Make sure that the lights are off when not enabled at all.')
      #  if self.is_light_on():
      #    logger.info('Environment is turning off the lights due to disabling it')
      #  self.light_off()


      # Sprayer checks and actions
      if self.sprayer['enabled']:
        toggle_on = False
        extra_logging_message = ''
        logger.debug('Environment spraying is enabled.')
        logger.debug('Environment spraying is based on: %s' % self.sprayer['mode'])
        if 'sensor' == self.sprayer['mode']:
          if not self.__check_active_sensors('sprayer'):
            logger.error('Environment spraying sensors are not up to date. Check you sensors on the sensor page So force the power down to be sure!')
            toggle_on = False
          else:
            # Only spray when the lights are on. Or when explicit enabled during the nights.
            if self.sprayer['night_enabled'] or self.is_light_on():
              # Spray based on the average humidity values of the used sensors
              toggle_on = self.sprayer['humidity']['current'] < self.sprayer['humidity']['alarm_min']
              if toggle_on:
                extra_logging_message = 'Sprayer humdity value %f%% is lower then alarm %f%%.' % (self.sprayer['humidity']['current'],
                                                                                          self.sprayer['humidity']['alarm_min'])
        else:
          # Spray based on time table
          toggle_on = terrariumUtils.is_time(self.sprayer['time_table'])
          if toggle_on is None:
            self.__update_timing('sprayer')

          if toggle_on and len(self.sprayer['sensors']) > 0:
            # Use the extra added sensors for finetuning the trigger action
            toggle_on = self.sprayer['humidity']['current'] < self.sprayer['humidity']['alarm_min']
            if toggle_on:
              extra_logging_message = 'Sprayer humdity value %f%% is lower then alarm %f%%.' % (self.sprayer['humidity']['current'],
                                                                                        self.sprayer['humidity']['alarm_min'])

        if toggle_on:
          if self.is_door_open():
            logger.warning('Environment could not spray for %f seconds based on %s mode because of an open door.%s' % (self.sprayer['spray_duration'],
                                                                                                                       self.sprayer['mode'],
                                                                                                                       extra_logging_message))
          else:
            if not self.is_sprayer_on():
              logger.info('Environment is turning on the sprayer for %f seconds based on %s mode.%s' % (self.sprayer['spray_duration'],
                                                                                                      self.sprayer['mode'],
                                                                                                      extra_logging_message))
            self.sprayer_on()
        else:
          if self.is_sprayer_on():
            logger.info('Environment is turning off the sprayer based on %s mode.' % (self.sprayer['mode'],))

          self.sprayer_off()

      #else:
      #  logger.debug('Make sure that the spayer is off when not enabled at all.')
      #  if self.is_sprayer_on():
      #    logger.info('Environment is turning off the sprayer due to disabling it')
      #  self.sprayer_off()


      # Watertank checks and actions
      if self.watertank['enabled']:
        toggle_on = False
        extra_logging_message = ''
        logger.debug('Environment watertank is enabled.')
        logger.debug('Environment watertank is based on: %s' % self.watertank['mode'])
        if 'sensor' == self.watertank['mode']:
          if not self.__check_active_sensors('watertank'):
            logger.error('Environment watertank sensors are not up to date. Check you sensors on the sensor page So force the power down to be sure!')
            toggle_on = False
          else:
            # Spray based on the average humidity values of the used sensors
            toggle_on = self.watertank['height'] - self.watertank['distance']['current'] < self.watertank['distance']['alarm_min']
            if toggle_on:
              extra_logging_message = 'Water tank level value %f%% is lower then alarm %f%%.' % (self.watertank['height'] - self.watertank['distance']['current'],
                                                                                          self.watertank['distance']['alarm_min'])
        else:
          # Spray based on time table
          toggle_on = terrariumUtils.is_time(self.watertank['time_table'])
          if toggle_on is None:
            self.__update_timing('watertank')

          if toggle_on and len(self.watertank['sensors']) > 0:
            # Use the extra added sensors for finetuning the trigger action
            toggle_on = self.watertank['height'] - self.watertank['distance']['current'] < self.watertank['distance']['alarm_min']
            if toggle_on:
              extra_logging_message = 'Water tank level value %f%% is lower then alarm %f%%.' % (self.watertank['height'] - self.watertank['distance']['current'],
                                                                                        self.watertank['distance']['alarm_min'])

        if toggle_on:
          if not self.is_watertank_on():
            logger.info('Environment is turning on the water punt for %f seconds based on %s mode.%s' % (self.watertank['pump_duration'],
                                                                                                      self.watertank['mode'],
                                                                                                      extra_logging_message))
            self.watertank_on()
        else:
          if self.is_watertank_on():
            logger.info('Environment is turning off the water pump based on %s mode.' % (self.watertank['mode'],))

          self.watertank_off()

      #else:
      #  logger.debug('Make sure that the water pump is off when not enabled at all.')
      #  if self.is_watertank_on():
      #    logger.info('Environment is turning off the water pump due to disabling it')
      #  self.watertank_off()


      # Heater checks and actions
      if self.heater['enabled']:
        toggle_on = None
        extra_logging_message = ''
        logger.debug('Environment heater is enabled.')
        logger.debug('Environment heater is based on: %s.' % self.heater['mode'])

        if self.heater['night_difference'] != 0.0:
          is_night = False
          if self.heater['night_source'] == 'weather':
            is_night = self.is_night()
          elif self.heater['night_source'] == 'lights':
            is_night = not self.is_light_on()

          if self.heater['night_modus'] != is_night:
            logger.info('Changing heater to %s modus. Changing the min and max alarm %s by %s degrees.' % (
                  ('night' if is_night else 'day'),
                  ('up' if is_night else 'down'),
                  self.heater['night_difference']))
            # Change temperatures when switching from day to night and vise versa
            for sensorid in self.heater['sensors']:
              if is_night:
                self.sensors[sensorid].set_alarm_min(self.sensors[sensorid].get_alarm_min() + self.heater['night_difference'])
                self.sensors[sensorid].set_alarm_max(self.sensors[sensorid].get_alarm_max() + self.heater['night_difference'])
              else:
                self.sensors[sensorid].set_alarm_min(self.sensors[sensorid].get_alarm_min() - self.heater['night_difference'])
                self.sensors[sensorid].set_alarm_max(self.sensors[sensorid].get_alarm_max() - self.heater['night_difference'])

              self.heater['night_modus'] = is_night

        if 'sensor' == self.heater['mode']:
          if not self.__check_active_sensors('heater'):
            logger.error('Environment heater sensors are not up to date. Check you sensors on the sensor page So force the power down to be sure!')
            toggle_on = False
          else:
            # Only heat when the lights are off. Or when explicit enabled during the day.
            if self.heater['day_enabled'] or self.is_light_off():
              # Heat based on the average temperature values of the used sensors
              if self.heater['temperature']['current'] < self.heater['temperature']['alarm_min']:
                toggle_on = True
                extra_logging_message = 'Heater temperature value %f%% is lower then alarm %f%%.' % (self.heater['temperature']['current'],
                                                                                              self.heater['temperature']['alarm_min'])
              elif self.heater['temperature']['current'] > self.heater['temperature']['alarm_max']:
                toggle_on = False
                extra_logging_message = 'Heater temperature value %f%% is higher then alarm %f%%.' % (self.heater['temperature']['current'],
                                                                                               self.heater['temperature']['alarm_max'])
            else:
              # Force off when lights are on!
              if self.is_heater_on():
                logger.info('Environment is turning off the heater due to lights on based on %s mode.' % (self.heater['mode'],))

              toggle_on = False

        else:
          # Heat based on time table
          toggle_on = terrariumUtils.is_time(self.heater['time_table'])
          if toggle_on is None:
            self.__update_timing('heater')

          if toggle_on and len(self.heater['sensors']) > 0:
            # Reset toggle based on the extra available sensors
            toggle_on = None
            # Use the extra added sensors for finetuning the trigger action
            if self.heater['temperature']['current'] < self.heater['temperature']['alarm_min']:
              toggle_on = True
              extra_logging_message = 'Heater temperature value %f%% is lower then alarm %f%%.' % (self.heater['temperature']['current'],
                                                                                            self.heater['temperature']['alarm_min'])
            elif self.heater['temperature']['current'] > self.heater['temperature']['alarm_max']:
              toggle_on = False
              extra_logging_message = 'Heater temperature value %f%% is higher then alarm %f%%.' % (self.heater['temperature']['current'],
                                                                                             self.heater['temperature']['alarm_max'])

        if toggle_on is True:
          if not self.is_heater_on():
            logger.info('Environment is turning on the heater based on %s mode. %s' % (self.heater['mode'],
                                                                                      extra_logging_message))
          self.heater_on()

        elif toggle_on is False:
          if self.is_heater_on():
            logger.info('Environment is turning off the heater based on %s mode. %s' % (self.heater['mode'],
                                                                                       extra_logging_message))
          self.heater_off()

      #else:
      #  logger.debug('Make sure that the heating is off when not enabled at all.')
      #  if self.is_heater_on():
      #    logger.info('Environment is turning off the heater due to disabling it')
      #  self.heater_off()



     # Cooler checks and actions
      if self.cooler['enabled']:
        toggle_on = None
        extra_logging_message = ''
        logger.debug('Environment cooler is enabled.')
        logger.debug('Environment cooler is based on: %s' % self.cooler['mode'])
        if 'sensor' == self.cooler['mode']:
          if not self.__check_active_sensors('cooler'):
            logger.error('Environment cooler sensors are not up to date. Check you sensors on the sensor page So force the power down to be sure!')
            toggle_on = False
          else:

            # Only cool when the lights are on. Or when explicit enabled during the night.
            if self.cooler['night_enabled'] or self.is_light_on():
              # Cooler based on the average temperature values of the used sensors
              if self.cooler['temperature']['current'] < self.cooler['temperature']['alarm_min']:
                toggle_on = False
                extra_logging_message = 'Cooler temperature value %f%% is lower then alarm %f%%.' % (self.cooler['temperature']['current'],
                                                                                              self.cooler['temperature']['alarm_min'])
              elif self.cooler['temperature']['current'] > self.cooler['temperature']['alarm_max']:
                toggle_on = True
                extra_logging_message = 'Cooler temperature value %f%% is higher then alarm %f%%.' % (self.cooler['temperature']['current'],
                                                                                               self.cooler['temperature']['alarm_max'])
            else:
              # Force off when lights are on!
              if self.is_cooler_on():
                logger.info('Environment is turning off the cooler due to lights on based on %s mode.' % (self.cooler['mode'],))

              toggle_on = False


        else:
          # Cooler based on time table
          toggle_on = terrariumUtils.is_time(self.cooler['time_table'])
          if toggle_on is None:
            self.__update_timing('cooler')

          if toggle_on and len(self.cooler['sensors']) > 0:
            # Reset toggle based on the extra available sensors
            toggle_on = None
            # Use the extra added sensors for finetuning the trigger action
            if self.cooler['temperature']['current'] < self.cooler['temperature']['alarm_min']:
              toggle_on = False
              extra_logging_message = 'Cooler temperature value %f%% is lower then alarm %f%%.' % (self.cooler['temperature']['current'],
                                                                                            self.cooler['temperature']['alarm_min'])
            elif self.cooler['temperature']['current'] > self.cooler['temperature']['alarm_max']:
              toggle_on = True
              extra_logging_message = 'Cooler temperature value %f%% is higher then alarm %f%%.' % (self.cooler['temperature']['current'],
                                                                                             self.cooler['temperature']['alarm_max'])

        if toggle_on is True:
          if not self.is_cooler_on():
            logger.info('Environment is turning on the cooler based on %s mode.%s' % (self.cooler['mode'],
                                                                                      extra_logging_message))
          self.cooler_on()

        elif toggle_on is False:
          if self.is_cooler_on():
            logger.info('Environment is turning off the cooler based on %s mode.%s' % (self.cooler['mode'],
                                                                                       extra_logging_message))
          self.cooler_off()

      #else:
      #  logger.debug('Make sure that the cooler is off when not enabled at all.')
      #  if self.is_cooler_on():
      #    logger.info('Environment is turning off the cooler due to disabling it')
      #  self.cooler_off()

      duration = time.time() - starttime
      if duration < terrariumEnvironment.LOOP_TIMEOUT:
        logger.info('Update done in %.5f seconds. Waiting for %.5f seconds for next round' % (duration,terrariumEnvironment.LOOP_TIMEOUT - duration))
        sleep(terrariumEnvironment.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        logger.warning('Update took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumEnvironment.LOOP_TIMEOUT,terrariumEnvironment.LOOP_TIMEOUT))

  def __on_off(self,part, state = None):
    power_switches = []
    if 'light' == part:
      power_switches = self.light['power_switches']
    elif 'sprayer' == part:
      power_switches = self.sprayer['power_switches']
    elif 'heater' == part:
      power_switches = self.heater['power_switches']
    elif 'cooler' == part:
      power_switches = self.cooler['power_switches']
    elif 'watertank' == part:
      power_switches = self.watertank['power_switches']

    is_on = len(power_switches) > 0
    for switch_id in power_switches:
      if switch_id not in self.power_switches:
        is_on = False
      elif state is None:
        is_on = is_on and self.power_switches[switch_id].is_on()
      else:
        if state:
          if part in ['heater','cooler'] and self.power_switches[switch_id].get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
            self.power_switches[switch_id].go_up()
          else:
            self.power_switches[switch_id].on()
        else:
          if part in ['heater','cooler'] and self.power_switches[switch_id].get_hardware_type() in ['pwm-dimmer','remote-dimmer']:
            self.power_switches[switch_id].go_down()
          else:
            self.power_switches[switch_id].off()

        is_on = state

    return is_on

  def __switch_on(self,part):
    return True == self.__on_off(part,True)

  def __switch_off(self,part):
    return False == self.__on_off(part,False)

  def __is_on(self,part):
    return self.__on_off(part) == True

  def __is_off(self,part):
    return not self.__is_on(part)

  def __get_state(self,part,exclude_fields = []):
    return_data = {}
    state_data = {}
    average = {}
    state = False

    if part == 'light':
      state_data = self.light
      state = self.is_light_on()
    elif part == 'sprayer':
      state_data = self.sprayer
      average = self.get_average_humidity(self.sprayer['sensors'])
      state = self.is_sprayer_on()
    elif part == 'watertank':
      state_data = self.watertank
      average = self.get_average_distance(self.watertank['sensors'])
      state = self.is_watertank_on()

      # Update to Liters based on the distanes
      factor = float(self.watertank['volume']) / float(self.watertank['height'])
      average['current'] = (float(self.watertank['height']) - average['current']) * factor
      average['alarm_max'] *= factor
      average['alarm_min'] *= factor
      average['limit_max'] *= factor
      average['limit_min'] *= factor

    elif part == 'heater':
      state_data = self.heater
      average = self.get_average_temperature(self.heater['sensors'])
      state = self.is_heater_on()
    elif part == 'cooler':
      state_data = self.cooler
      average = self.get_average_temperature(self.cooler['sensors'])
      state = self.is_cooler_on()

    for key in state_data:
      if key not in exclude_fields:
        return_data[key] = state_data[key]

    return_data.update(average)

    # Reset alarm for to high mudity and sprayer, to hot and heater, or to cool and cooling
    if part != 'light':
      return_data['error'] = not self.__check_active_sensors(part)
      if 'alarm' not in return_data or \
          return_data['mode'] == 'disabled' or \
         (part in ['sprayer','heater','watertank'] and return_data['current'] >= return_data['alarm_max']) or \
         (part == 'cooler'  and return_data['current'] <= return_data['alarm_max']):
        return_data['alarm'] = False

    return_data['state'] = 'on' if state else 'off'
    return return_data
  # End private functions

  # System functions
  def stop(self):
    self.__running = False
    logger.info('Shutdown environment')

  def set_power_switches(self,data):
    self.power_switches = data
    self.__check_available_power_switches()

  def set_sensors(self,data):
    self.sensors = data
    self.__check_available_sensors()

  def get_config(self):
    data = {'light'     : self.get_light_config(),
            'sprayer'   : self.get_sprayer_config() ,
            'heater'    : self.get_heater_config(),
            'cooler'    : self.get_cooler_config(),
            'watertank' : self.get_watertank_config()}

    return data

  def get_average_temperature(self,sensors = []):
    data = self.get_average(sensors)
    if 'temperature' in data:
      return data['temperature']

    return {'current'   : 0.0,
            'alarm_min' : 0.0,
            'alarm_max' : 0.0,
            'limit_min' : 0.0,
            'limit_max' : 0.0,
            'amount'    : 0.0,
            'alarm'     : False}


  def get_average_humidity(self,sensors = []):
    data = self.get_average(sensors)
    if 'humidity' in data:
      return data['humidity']

    return {'current'   : 0.0,
            'alarm_min' : 0.0,
            'alarm_max' : 0.0,
            'limit_min' : 0.0,
            'limit_max' : 0.0,
            'amount'    : 0.0,
            'alarm'     : False}

  def get_average_distance(self,sensors = []):
    data = self.get_average(sensors)
    if 'distance' in data:
      return data['distance']

    return {'current'   : 0.0,
            'alarm_min' : 0.0,
            'alarm_max' : 0.0,
            'limit_min' : 0.0,
            'limit_max' : 0.0,
            'amount'    : 0.0,
            'alarm'     : False}

  def get_average(self,sensors_filter = []):
    average = {}
    # Make a set, in order to get a list of unique sensorids. In other words, set will remove duplicate sensorids
    for sensorid in set(self.sprayer['sensors'] + self.heater['sensors'] + self.cooler['sensors'] + self.watertank['sensors']):
      if len(sensors_filter) > 0 and sensorid not in sensors_filter:
        # If we want to filter, we only count the ones that are giving as parameter
        continue

      if sensorid not in self.sensors:
        part = ''
        if sensorid in self.sprayer['sensors']:
          part += 'sprayer,'
        if sensorid in self.heater['sensors']:
          part += 'heater,'
        if sensorid in self.cooler['sensors']:
          part += 'cooler,'
        if sensorid in self.watertank['sensors']:
          part += 'watertank,'

        part = part[:-1]

        logger.error('Error getting average data from sensor with id %s. Sensor is specified in \'%s\' part, but the sensor is not known anymore in confg' % (sensorid,part))
        continue

      sensor = self.sensors[sensorid]
      sensor_type = sensor.get_type()

      if sensor_type not in average:
        average[sensor_type] = {'current'   : 0.0,
                                'alarm_min' : 0.0,
                                'alarm_max' : 0.0,
                                'limit_min' : 0.0,
                                'limit_max' : 0.0,
                                'amount'    : 0.0,
                                'alarm'     : False}

      average[sensor_type]['current'] += sensor.get_current()
      average[sensor_type]['alarm_min'] += sensor.get_alarm_min()
      average[sensor_type]['alarm_max'] += sensor.get_alarm_max()
      average[sensor_type]['limit_min'] += sensor.get_limit_min()
      average[sensor_type]['limit_max'] += sensor.get_limit_max()
      average[sensor_type]['amount'] += 1

    for averagetype in average:
      amount = average[averagetype]['amount']
      del(average[averagetype]['amount'])
      for field in average[averagetype]:
        average[averagetype][field] /= amount

      average[averagetype]['alarm'] = not (average[averagetype]['alarm_min'] <= average[averagetype]['current'] <= average[averagetype]['alarm_max'])
      average[averagetype]['type'] = averagetype
      #average[averagetype]['indicator'] = self.__unit_type(averagetype)

    return average

  def is_day(self):
    return (self.light['enabled'] and self.is_light_on()) or self.weather.is_day()

  def is_night(self):
    return not self.is_day()
  # End system functions


  # Light functions
  def get_light_config(self):
    return self.__get_state('light',['time_table','enabled','state','duration'])

  def set_light_config(self,data):
    self.__set_config('light',data)

  def get_light_state(self):
    cleanup_fields = []

    if 'weather' == self.light['mode']:
      cleanup_fields = ['on_duration','off_duration','time_table']

    elif 'timer' == self.light['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift']

    return self.__get_state('light',cleanup_fields)

  def light_on(self):
    return self.__switch_on('light')

  def light_off(self):
    return self.__switch_off('light')

  def is_light_on(self):
    return self.__is_on('light')

  def is_light_off(self):
    return self.__is_off('light')
  # End light functions


  # Sprayer functions
  def get_sprayer_config(self):
    return self.__get_state('sprayer',['time_table','enabled','state','lastaction','duration'])

  def set_sprayer_config(self,data):
    self.__set_config('sprayer',data)

  def get_sprayer_state(self):
    cleanup_fields = []

    if 'weather' == self.sprayer['mode']:
      cleanup_fields = ['on_duration','off_duration','time_table']

    elif 'timer' == self.sprayer['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift']

    elif 'sensor' == self.sprayer['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift','time_table']

    return self.__get_state('sprayer',cleanup_fields)

  def sprayer_on(self):
    if int(time.time()) - self.sprayer['lastaction'] > self.sprayer['spray_timeout']:
      self.__switch_on('sprayer')
      (Timer(self.sprayer['spray_duration'], self.sprayer_off)).start()
      self.sprayer['lastaction'] = int(time.time())

  def sprayer_off(self):
    self.__switch_off('sprayer')

  def is_sprayer_on(self):
    return self.__is_on('sprayer')

  def is_sprayer_off(self):
    return self.__is_off('sprayer')
  # End sprayer functions

  # Watertank functions
  def get_watertank_config(self):
    return self.__get_state('watertank',['time_table','enabled','state','lastaction','duration'])

  def set_watertank_config(self,data):
    self.__set_config('watertank',data)

  def get_watertank_state(self):
    cleanup_fields = []

    if 'weather' == self.watertank['mode']:
      cleanup_fields = ['on_duration','off_duration','time_table']

    elif 'timer' == self.watertank['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift']

    elif 'sensor' == self.watertank['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift','time_table']

    return self.__get_state('watertank',cleanup_fields)

  def watertank_on(self):
#    if int(time.time()) - self.watertank['lastaction'] > self.watertank['spray_timeout']:
    self.__switch_on('watertank')
    (Timer(self.watertank['pump_duration'], self.watertank_off)).start()
    self.watertank['lastaction'] = int(time.time())

  def watertank_off(self):
    self.__switch_off('watertank')

  def is_watertank_on(self):
    return self.__is_on('watertank')

  def is_watertank_off(self):
    return self.__is_off('watertank')
  # End watertank functions

  # Heater functions
  def get_heater_config(self):
    return self.__get_state('heater',['time_table','enabled','state','duration'])

  def set_heater_config(self,data):
    self.__set_config('heater',data)

  def get_heater_state(self):
    cleanup_fields = []

    if 'weather' == self.heater['mode']:
      cleanup_fields = ['on_duration','off_duration','time_table']

    elif 'timer' == self.heater['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift']

    elif 'sensor' == self.heater['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift','time_table']

    return self.__get_state('heater',cleanup_fields)

  def heater_on(self):
    if int(time.time()) - self.heater['lastaction'] > self.heater['settle_timeout']:
      self.__switch_on('heater')
      self.heater['lastaction'] = int(time.time())

  def heater_off(self):
    self.__switch_off('heater')

  def is_heater_on(self):
    return self.__is_on('heater')

  def is_heater_off(self):
    return self.__is_off('heater')
  # End heater functions


  # Cooler functions
  def get_cooler_config(self):
    return self.__get_state('cooler',['time_table','enabled','state','duration'])

  def set_cooler_config(self,data):
    self.__set_config('cooler',data)

  def get_cooler_state(self):
    cleanup_fields = []

    if 'weather' == self.cooler['mode']:
      cleanup_fields = ['on_duration','off_duration','time_table']

    elif 'timer' == self.cooler['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift']

    elif 'sensor' == self.cooler['mode']:
      cleanup_fields = ['min_hours','max_hours','hours_shift','time_table']

    return self.__get_state('cooler',cleanup_fields)

  def cooler_on(self):
    self.__switch_on('cooler')

  def cooler_off(self):
    self.__switch_off('cooler')

  def is_cooler_on(self):
    return self.__is_on('cooler')

  def is_cooler_off(self):
    return self.__is_off('cooler')
  # End cooler functions
