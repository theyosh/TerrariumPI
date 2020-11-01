# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

try:
  import thread as _thread
except ImportError as ex:
  import _thread
import datetime
import time

from gevent import sleep

from threading import Timer
from terrariumUtils import terrariumUtils

class terrariumEnvironmentPart(object):

  env_type = None

  def __init__(self,mode,sensors,day_night_difference,day_night_source):
    self.config = {'mode' : mode,
                   'sensors' : sensors if isinstance(sensors, list) else sensors.split(','),
                   'day_night_difference': float(day_night_difference),
                   'day_night_source' : day_night_source}

    self.sensor_data = {'current': 0, 'alarm_min' : 0, 'alarm_max' : 0, 'limit_min' : 0, 'limit_max' : 0}
    self.night_mode = False
    self.sensors_error = False
    self.timer_min_data = {'lastaction' : 0, 'power_state' : None}
    self.timer_max_data = {'lastaction' : 0, 'power_state' : None}

    self.last_update = 0
    self.active_timer = None

  def __get_power_state(self,powerswitchlist):
    self.timer_min_data['max_power'] = False
    self.timer_min_data['min_power'] = True

    self.timer_max_data['max_power'] = False
    self.timer_max_data['min_power'] = True

    if len(self.config['alarm_min']['powerswitches']) > 0 or True:
      self.timer_min_data['max_power'] = all([powerswitchlist[switchid].is_at_max_power() for switchid in self.config['alarm_min']['powerswitches'] if switchid in powerswitchlist])

      self.timer_min_data['min_power'] = all([powerswitchlist[switchid].is_at_min_power() for switchid in self.config['alarm_min']['powerswitches'] if switchid in powerswitchlist])

    if len(self.config['alarm_max']['powerswitches']) > 0 or True:
      self.timer_max_data['max_power'] = all([powerswitchlist[switchid].is_at_max_power() for switchid in self.config['alarm_max']['powerswitches'] if switchid in powerswitchlist])

      self.timer_max_data['min_power'] = all([powerswitchlist[switchid].is_at_min_power() for switchid in self.config['alarm_max']['powerswitches'] if switchid in powerswitchlist])

    self.timer_min_data['power_state'] = not self.timer_min_data['min_power']
    self.timer_max_data['power_state'] = not self.timer_max_data['min_power']

  def __toggle_powerswitches(self,powerswitches,action = None):
    for switchid in powerswitches:
      if powerswitches[switchid].in_manual_mode():
        logger.warning('Power switch \'{}\' is in manual mode and will not change state.'.format(powerswitches[switchid].get_name()))
        continue

      if 'on' == action:
        powerswitches[switchid].go_up()

      elif 'off' == action:
        powerswitches[switchid].go_down()

    self.__get_power_state(powerswitches)

  def __toggle_alarm(self,part,action,powerswitchlist,timer = False):
    now = int(time.time())
    switches = {}
    lastaction = 0
    settletime = 0
    onduration = 0
    timerdata = {}

    if 'min' == part:
      powerswitches = self.config['alarm_min']['powerswitches']
      settletime = self.config['alarm_min']['settle']
      onduration = self.config['alarm_min']['duration_on']
      timerdata = self.timer_min_data
      lastaction = timerdata['lastaction']
    elif 'max' == part:
      powerswitches = self.config['alarm_max']['powerswitches']
      settletime = self.config['alarm_max']['settle']
      onduration = self.config['alarm_max']['duration_on']
      timerdata = self.timer_max_data
      lastaction = timerdata['lastaction']

    if len(powerswitches) == 0:
      return

    if now - lastaction > settletime or timer:
      for powerswitch in powerswitches:
        switches[powerswitch] = powerswitchlist[powerswitch]

      self.__toggle_powerswitches(switches,action)

      timerdata['lastaction'] = now
      if self.active_timer != None:
        self.active_timer.cancel()
        self.active_timer = None
      if 'on' == action and onduration > 0:
        self.active_timer = Timer(onduration, self.toggle_off_alarm_min if 'min' == part else self.toggle_off_alarm_max, (powerswitchlist,True))
        self.active_timer.start()

  def set_alarm_min(self,start,stop,timer_on,timer_off,light_state,door_state,duration_on,settle,powerswitches):
    self.config['alarm_min'] = {'timer_start':start,
                           'timer_stop':stop,
                           'timer_on': None if not terrariumUtils.is_float(timer_on) else float(timer_on),
                           'timer_off':None if not terrariumUtils.is_float(timer_off) else float(timer_off),
                           'light_state' : light_state,
                           'door_state' : door_state,
                           'duration_on':None if not terrariumUtils.is_float(duration_on) else float(duration_on),
                           'settle':None if not terrariumUtils.is_float(settle) else float(settle),
                           'powerswitches': powerswitches if isinstance(powerswitches, list) else powerswitches.split(',')
                           }
    self.timer_min_data['lastaction'] = 0
    self.timer_min_data['power_state'] = False

  def set_alarm_max(self,start,stop,timer_on,timer_off,light_state,door_state,duration_on,settle,powerswitches):
    self.config['alarm_max'] = {'timer_start':start,
                           'timer_stop':stop,
                           'timer_on':None if not terrariumUtils.is_float(timer_on) else float(timer_on),
                           'timer_off':None if not terrariumUtils.is_float(timer_off) else float(timer_off),
                           'light_state' : light_state,
                           'door_state' : door_state,
                           'duration_on':None if not terrariumUtils.is_float(duration_on) else float(duration_on),
                           'settle':None if not terrariumUtils.is_float(settle) else float(settle),
                           'powerswitches': powerswitches if isinstance(powerswitches, list) else powerswitches.split(','),
                           }
    self.timer_max_data['lastaction'] = 0
    self.timer_max_data['power_state'] = False

  def update(self,sensorlist,powerswitchlist,weather,light):
    self.update_timer_data(weather)
    self.update_day_night_data(sensorlist,weather,light)
    self.update_average_data(sensorlist)
    self.update_powerswitches_data(powerswitchlist)
    self.last_update = int(time.time())

  def update_timer_data(self,weather):
    logger.debug('Updating timer data for %s running in mode: %s' % (self.get_type(),self.get_mode()))
    if self.in_weather_mode() or self.in_weather_inverse_mode():

      # Upate times based on weather
      if self.in_weather_inverse_mode():
        self.config['alarm_min']['timer_start']  = datetime.datetime.fromtimestamp(weather.get_sun_set())
        self.config['alarm_min']['timer_stop']   = datetime.datetime.fromtimestamp(weather.get_sun_rise())

      else:
        self.config['alarm_min']['timer_start']  = datetime.datetime.fromtimestamp(weather.get_sun_rise())
        self.config['alarm_min']['timer_stop']   = datetime.datetime.fromtimestamp(weather.get_sun_set())

      self.config['alarm_min']['timer_on'] = None
      self.config['alarm_min']['timer_off'] = None
      self.config['alarm_max']['timer_on'] = None
      self.config['alarm_max']['timer_off'] = None

      if self.get_type() == 'light':
        # Duration check
        duration = self.config['alarm_min']['timer_stop'] - self.config['alarm_min']['timer_start']
        # Reduce the amount of hours if to much
        if self.config['max_hours'] > 0 and duration > datetime.timedelta(hours=self.config['max_hours']):
          duration -= datetime.timedelta(hours=self.config['max_hours'])
          self.config['alarm_min']['timer_start'] += datetime.timedelta(seconds=duration.total_seconds()/2)
          self.config['alarm_min']['timer_stop'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
        # Increase the amount of hours if to little
        elif self.config['min_hours'] > 0 and duration < datetime.timedelta(hours=self.config['min_hours']):
          duration = datetime.timedelta(hours=self.config['min_hours']) - duration
          self.config['alarm_min']['timer_start'] -= datetime.timedelta(seconds=duration.total_seconds()/2)
          self.config['alarm_min']['timer_stop'] += datetime.timedelta(seconds=duration.total_seconds()/2)

        # Shift hours
        self.config['alarm_min']['timer_start'] += datetime.timedelta(hours=self.config['hours_shift'])
        self.config['alarm_min']['timer_stop'] += datetime.timedelta(hours=self.config['hours_shift'])


      self.config['alarm_min']['timer_start'] = self.config['alarm_min']['timer_start'].strftime('%H:%M')
      self.config['alarm_min']['timer_stop'] = self.config['alarm_min']['timer_stop'].strftime('%H:%M')

      # Swap weather times..... for night period
      self.config['alarm_max']['timer_start'] = self.config['alarm_min']['timer_stop'] if self.get_type() == 'light' else self.config['alarm_min']['timer_start']
      self.config['alarm_max']['timer_stop'] = self.config['alarm_min']['timer_start'] if self.get_type() == 'light' else self.config['alarm_min']['timer_stop']

    if not self.in_sensor_mode() and len(list(self.config['alarm_min'].keys())) > 0:
      self.timer_min_data['time_table'] = terrariumUtils.calculate_time_table(self.config['alarm_min']['timer_start'],
                                                                              self.config['alarm_min']['timer_stop'],
                                                                              self.config['alarm_min']['timer_on'],
                                                                              self.config['alarm_min']['timer_off'])

      self.timer_min_data['duration'] = terrariumUtils.duration(self.timer_min_data['time_table'])

    if not self.in_sensor_mode() and len(list(self.config['alarm_max'].keys())) > 0:
      self.timer_max_data['time_table'] = terrariumUtils.calculate_time_table(self.config['alarm_max']['timer_start'],
                                                                              self.config['alarm_max']['timer_stop'],
                                                                              self.config['alarm_max']['timer_on'],
                                                                              self.config['alarm_max']['timer_off'])

      self.timer_max_data['duration'] = terrariumUtils.duration(self.timer_max_data['time_table'])

  def update_day_night_data(self,sensorlist,weather,light):
    if self.get_day_night_difference() != 0.0:
      is_night = ('weather' == self.get_day_night_source() and weather.is_night()) or ('lights' == self.get_day_night_source() and light.is_night())

      if self.is_in_night_mode() != is_night:
        logger.info('Changing environment %s to %s modus. Changing the min and max alarm %s by %s degrees.' % (
              self.get_type(),
              ('night' if is_night else 'day'),
              ('up' if is_night else 'down'),
              self.get_day_night_difference()))
        # Change temperatures when switching from day to night and vise versa
        for sensor in self.get_sensors(sensorlist):
          sensor.set_alarm_min(sensor.get_alarm_min() + (self.get_day_night_difference() * (1 if is_night else -1)))
          sensor.set_alarm_max(sensor.get_alarm_max() + (self.get_day_night_difference() * (1 if is_night else -1)))

        self.night_mode = is_night

  def update_average_data(self,sensorlist):
    self.sensor_data = {'current':0.0, 'alarm_min' : 0.0, 'alarm_max' : 0.0, 'limit_min' : 0.0, 'limit_max' : 0.0}
    amount_of_sensors = 0

    for sensor in self.get_sensors(sensorlist):
      if not sensor.is_active():
        # Skip sensor in error state...
        continue

      self.sensor_data['current']   += sensor.get_current()
      self.sensor_data['alarm_min'] += sensor.get_alarm_min()
      self.sensor_data['alarm_max'] += sensor.get_alarm_max()
      self.sensor_data['limit_min'] += sensor.get_limit_min()
      self.sensor_data['limit_max'] += sensor.get_limit_max()
      amount_of_sensors += 1

    if amount_of_sensors > 0:
      for part in self.sensor_data:
        self.sensor_data[part] /= float(amount_of_sensors)

    self.sensors_error = amount_of_sensors == 0 and len(self.get_sensors()) > 0

  def update_powerswitches_data(self,powerswitchList):
    self.__get_power_state(powerswitchList)

  def get_type(self):
    return None

  def get_sensors(self,filterList = None):
    if filterList is None:
      return self.config['sensors']

    data = []
    for sensor in self.get_sensors():
      if sensor not in filterList:
        continue
      else:
        data.append(filterList[sensor])

    return data

  def has_sensors(self):
    return len(self.get_sensors()) > 0

  def sensors_in_error(self):
    return self.sensors_error

  def is_enabled(self):
    return self.get_mode() != 'disabled'

  def is_alarm_min(self):
    alarm = None
    # This offset will make powerswitches go off at either:
    # 1. The max value when NO max limit power switches configured
    # 2. Halfway between min and max value when max limit power switches ARE configured
    alarm_false_offset = 0 if len(self.config['alarm_max']['powerswitches']) == 0 else (self.sensor_data['alarm_max'] - self.sensor_data['alarm_min']) / 2
    if self.sensor_data['current'] < self.sensor_data['alarm_min']:
      alarm = True
    elif self.sensor_data['current'] > (self.sensor_data['alarm_max'] - alarm_false_offset):
      alarm = False

    return alarm

  def is_alarm_max(self):
    alarm = None
    # This offset will make powerswitches go off at either:
    # 1. The max value when NO max limit power switches configured
    # 2. Halfway between min and max value when max limit power switches ARE configured
    alarm_false_offset = 0 if len(self.config['alarm_min']['powerswitches']) == 0 else (self.sensor_data['alarm_max'] - self.sensor_data['alarm_min']) / 2

    if self.sensor_data['current'] > self.sensor_data['alarm_max']:
      alarm = True
    elif self.sensor_data['current'] < self.sensor_data['alarm_min'] + alarm_false_offset:
      alarm = False

    return alarm

  def is_time_min(self):
    return terrariumUtils.is_true(terrariumUtils.is_time(self.timer_min_data['time_table']))

  def is_time_max(self):
    return terrariumUtils.is_true(terrariumUtils.is_time(self.timer_max_data['time_table']))

  def get_mode(self):
    return self.config['mode']

  def in_sensor_mode(self):
    return self.get_mode() == 'sensor'

  def in_timer_mode(self):
    return self.get_mode() == 'timer'

  def in_weather_mode(self):
    return self.get_mode() == 'weather'

  def in_weather_inverse_mode(self):
    return self.get_mode() == 'weatherinverse'

  def get_day_night_difference(self):
    return self.config['day_night_difference']

  def get_day_night_source(self):
    return self.config['day_night_source']

  def is_in_night_mode(self):
    return self.night_mode == True

  def get_alarm_min_light_state(self):
    return self.config['alarm_min']['light_state']

  def get_alarm_max_light_state(self):
    return self.config['alarm_max']['light_state']

  def get_alarm_min_door_state(self):
    return self.config['alarm_min']['door_state']

  def get_alarm_max_door_state(self):
    return self.config['alarm_max']['door_state']

  def is_alarm_min_on(self):
    return self.timer_min_data['power_state'] == True

  def is_alarm_min_off(self):
    return not self.is_alarm_min_on()

  def is_alarm_max_on(self):
    return self.timer_max_data['power_state'] == True

  def is_alarm_max_off(self):
    return not self.is_alarm_max_on()

  def has_settled_alarm_min(self):
    return int(time.time()) - self.timer_min_data['lastaction'] > self.config['alarm_min']['settle']

  def has_settled_alarm_max(self):
    return int(time.time()) - self.timer_max_data['lastaction'] > self.config['alarm_max']['settle']

  def toggle_on_alarm_min(self,powerswitches,timer = False):
    self.__toggle_alarm('min','on',powerswitches,timer)

  def toggle_off_alarm_min(self,powerswitches,timer = False):
    self.__toggle_alarm('min','off',powerswitches,timer)

  def toggle_on_alarm_max(self,powerswitches,timer = False):
    self.__toggle_alarm('max','on',powerswitches,timer)

  def toggle_off_alarm_max(self,powerswitches,timer = False):
    self.__toggle_alarm('max','off',powerswitches,timer)

  def has_alarm_min_powerswitches(self):
    return len(self.config['alarm_min']['powerswitches']) > 0

  def has_alarm_max_powerswitches(self):
    return len(self.config['alarm_max']['powerswitches']) > 0

  def is_alarm_min_at_min_power(self):
    return self.timer_min_data['min_power'] == True

  def is_alarm_min_at_max_power(self):
    return self.timer_min_data['max_power'] == True

  def is_alarm_max_at_min_power(self):
    return self.timer_max_data['min_power'] == True

  def is_alarm_max_at_max_power(self):
    return self.timer_max_data['max_power'] == True

  def get_config(self):
    return self.config

  def get_data(self, alarm_part = None):
    data = {'enabled'     : self.is_enabled(),
            'state'       : self.timer_min_data['power_state'] or self.timer_max_data['power_state'],
            'alarm'       : self.is_alarm_min() == True or self.is_alarm_max() == True,
            'error'       : self.sensors_in_error(),
            'is_night'    : self.is_in_night_mode(),
            'last_update' : self.last_update}

    data = dict(data, **{'config' : dict(self.config)})

    if alarm_part is not None:
      del(data['config']['alarm_min' if alarm_part == 'max' else 'alarm_max'])
      data['config'] = dict(data['config'], **dict(data['config']['alarm_min' if alarm_part == 'min' else 'alarm_max']))
      del(data['config']['alarm_min' if alarm_part == 'min' else 'alarm_max'])

    data = dict(data, **dict(self.sensor_data))

    if alarm_part is None or alarm_part == 'min':
      data = dict(data, **{'timer_min' : dict(self.timer_min_data)})
    if alarm_part is None or alarm_part == 'max':
      data = dict(data, **{'timer_max' : dict(self.timer_max_data)})

    return data

class terrariumEnvironmentLight(terrariumEnvironmentPart):

  env_type = 'light'

  def get_type(self):
    return terrariumEnvironmentLight.env_type

  def set_alarm_min(self,start,stop,timer_on,timer_off,light_state,door_state,duration_on,settle,powerswitches):
    super(terrariumEnvironmentLight, self).set_alarm_min(start,stop,timer_on,timer_off,'ignore',door_state,0,0,powerswitches)

  def set_alarm_max(self,start,stop,timer_on,timer_off,light_state,door_state,duration_on,settle,powerswitches):
    super(terrariumEnvironmentLight, self).set_alarm_max(start,stop,timer_on,timer_off,'ignore',door_state,0,0,powerswitches)

  def set_hours_limits(self,max_hours,min_hours,hours_shift):
    self.config['max_hours']   = float(max_hours)
    self.config['min_hours']   = float(min_hours)
    self.config['hours_shift'] = float(hours_shift)

  def is_day(self):
    now = int(time.time())
    start_time = self.timer_min_data['time_table'][0][0]
    # Small flaw... end time can be earlier then stop time... due to the period trigger timing
    end_time = self.timer_min_data['time_table'][len(self.timer_min_data['time_table'])-1][1]

    logger.debug ('Day period is from: %s to %s. Current %s' % (datetime.datetime.fromtimestamp(start_time),
                                                                datetime.datetime.fromtimestamp(end_time),
                                                                datetime.datetime.fromtimestamp(now)))
    return start_time < now <= end_time

  def is_night(self):
    return not self.is_day()

class terrariumEnvironmentTemperature(terrariumEnvironmentPart):

  env_type = 'temperature'

  def get_type(self):
    return terrariumEnvironmentTemperature.env_type

class terrariumEnvironmentHumidity(terrariumEnvironmentPart):

  env_type = 'humidity'

  def get_type(self):
    return terrariumEnvironmentHumidity.env_type

class terrariumEnvironmentMoisture(terrariumEnvironmentPart):

  env_type = 'moisture'

  def get_type(self):
    return terrariumEnvironmentMoisture.env_type

class terrariumEnvironmentPH(terrariumEnvironmentPart):

  env_type = 'ph'

  def get_type(self):
    return terrariumEnvironmentPH.env_type

class terrariumEnvironmentConductivity(terrariumEnvironmentPart):

  env_type = 'conductivity'

  def get_type(self):
    return terrariumEnvironmentConductivity.env_type

class terrariumEnvironmentDistance(terrariumEnvironmentPart):

  env_type = 'distance'

  def get_type(self):
    return terrariumEnvironmentDistance.env_type

class terrariumEnvironmentFertility(terrariumEnvironmentPart):

  env_type = 'fertility'

  def get_type(self):
    return terrariumEnvironmentFertility.env_type

class terrariumEnvironmentCO2(terrariumEnvironmentPart):

  env_type = 'co2'

  def get_type(self):
    return terrariumEnvironmentCO2.env_type

class terrariumEnvironmentVolume(terrariumEnvironmentPart):

  env_type = 'volume'

  def get_type(self):
    return terrariumEnvironmentVolume.env_type

# Factory class
class terrariumEnvironmentWatertank(object):

  env_type = 'watertank'

  def __new__(self,mode,sensors,day_night_difference,day_night_source,tank_type):
    if 'distance' == tank_type:
      return terrariumEnvironmentWatertankDistance(mode,sensors,day_night_difference,day_night_source)
    elif 'volume' == tank_type:
      return terrariumEnvironmentWatertankVolume(mode,sensors,day_night_difference,day_night_source)

    raise Exception()

class terrariumEnvironmentWatertankVolume(terrariumEnvironmentVolume):

  env_type = 'watertank'

  def get_type(self):
    return terrariumEnvironmentWatertank.env_type

  def set_volume(self,volume,height,offset):
    self.config['volume'] = float(volume)
    self.config['height'] = float(height)
    self.config['offset'] = float(offset)

class terrariumEnvironmentWatertankDistance(terrariumEnvironmentDistance):

  env_type = 'watertank'

  def get_type(self):
    return terrariumEnvironmentWatertank.env_type

  def set_volume(self,volume,height,offset):
    self.config['volume'] = float(volume)
    self.config['height'] = float(height)
    self.config['offset'] = float(offset)

  # Overrule the sensor data here...
  def update_average_data(self,sensorlist):
    super(terrariumEnvironmentWatertankDistance, self).update_average_data(sensorlist)

    # The current value is the distance between sensor and water surface
    # To get the amount of volume:
    # 1. Reduce the current distance with the offset
    # 2. Reduce the tank height with the new distance
    # 3. Multiplay the new tank height with the liter per cm value
    # 4. Swap min and max values

    # Get liter per cm
    factor = self.config['volume'] / (self.config['height'] - self.config['offset'])

    self.sensor_data['current']   = ((self.config['height'] - self.config['offset']) - (self.sensor_data['current'] - self.config['offset'])) * factor
    __tmp = ((self.config['height'] - self.config['offset']) - (self.sensor_data['alarm_max'] - self.config['offset'])) * factor
    self.sensor_data['alarm_max'] = ((self.config['height'] - self.config['offset']) - (self.sensor_data['alarm_min'] - self.config['offset'])) * factor
    self.sensor_data['alarm_min'] = __tmp

class terrariumEnvironment(object):
  LOOP_TIMEOUT = 15
  VALID_ENVIRONMENT_TYPES = []

  # Append environment parts
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentLight.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentTemperature.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentHumidity.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentMoisture.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentPH.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentConductivity.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentDistance.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentWatertank.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentFertility.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentCO2.env_type)
  VALID_ENVIRONMENT_TYPES.append(terrariumEnvironmentVolume.env_type)

  def __init__(self, sensors, powerswitches, weather, door_status, config, notification):
    logger.debug('Init terrariumPI environment')
    self.__environment_parts = {}
    for env_part in terrariumEnvironment.VALID_ENVIRONMENT_TYPES:
      self.__environment_parts[env_part] = None

    # Config callback
    self.config = config
    # Door status callback
    self.__is_door_open = door_status

    self.notification = notification

    self.sensors = sensors
    self.powerswitches = powerswitches

    self.weather = weather

    self.load_environment()
    _thread.start_new_thread(self.__engine_loop, ())

  def __engine_loop(self):
    logger.info('Starting engine')
    self.__running = True
    while self.__running:
      logger.debug('Start updating')
      starttime = time.time()
      self.update()

      duration = time.time() - starttime
      if duration < terrariumEnvironment.LOOP_TIMEOUT:
        logger.info('Update done in %.5f seconds. Waiting for %.5f seconds for next update' % (duration,terrariumEnvironment.LOOP_TIMEOUT - duration))
        sleep(terrariumEnvironment.LOOP_TIMEOUT - duration) # TODO: Config setting
      else:
        logger.warning('Update took to much time. Needed %.5f seconds which is %.5f more then the limit %s' % (duration,duration-terrariumEnvironment.LOOP_TIMEOUT,terrariumEnvironment.LOOP_TIMEOUT))

  # End private functions

  # System functions
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

    for env_part in terrariumEnvironment.VALID_ENVIRONMENT_TYPES:
      if env_part not in config_data:
        continue

      env_conf = config_data[env_part]

      self.__environment_parts[env_part] = None
      if env_part == terrariumEnvironmentLight.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentLight(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                               'weather'   if 'day_night_source' not in env_conf else env_conf['day_night_source'])

        self.__environment_parts[env_part].set_hours_limits(0.0 if 'max_hours'   not in env_conf else env_conf['max_hours'],
                                                            0.0 if 'min_hours'   not in env_conf else env_conf['min_hours'],
                                                            0.0 if 'hours_shift' not in env_conf else env_conf['hours_shift'])

      if env_part == terrariumEnvironmentTemperature.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentTemperature(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                               'weather'   if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentHumidity.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentHumidity(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentMoisture.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentMoisture(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentPH.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentPH(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentConductivity.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentConductivity(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentFertility.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentFertility(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentCO2.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentCO2(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentVolume.env_type:
        self.__environment_parts[env_part] = terrariumEnvironmentVolume(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'])

      elif env_part == terrariumEnvironmentWatertank.env_type:
        all_sensors = [] if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else (env_conf['sensors'] if isinstance(env_conf['sensors'], list) else env_conf['sensors'].split(','))
        tank_type = 'distance' if all([self.sensors[sensor].get_sensor_type() == 'distance' for sensor in all_sensors]) else 'volume'
        self.__environment_parts[env_part] = terrariumEnvironmentWatertank(
                                                'disabled' if 'mode' not in env_conf else env_conf['mode'],
                                                []         if ('sensors' not in env_conf or env_conf['sensors'] in ['',None]) else env_conf['sensors'],
                                                0.0        if 'day_night_difference' not in env_conf else env_conf['day_night_difference'],
                                                'weather'  if 'day_night_source' not in env_conf else env_conf['day_night_source'],
                                                tank_type)

        self.__environment_parts[env_part].set_volume(10.0 if 'volume'   not in env_conf else env_conf['volume'],
                                                      20.0 if 'height'   not in env_conf else env_conf['height'],
                                                       0.0 if 'offset'   not in env_conf else env_conf['offset'])

      self.__environment_parts[env_part].set_alarm_min(
                                      '00:00'  if 'alarm_min_timer_start' not in env_conf else env_conf['alarm_min_timer_start'],
                                      '00:00'  if 'alarm_min_timer_stop' not in env_conf else env_conf['alarm_min_timer_stop'],
                                      1.0      if 'alarm_min_timer_on' not in env_conf else env_conf['alarm_min_timer_on'],
                                      59.0     if 'alarm_min_timer_off' not in env_conf else env_conf['alarm_min_timer_off'],
                                      'ignore' if 'alarm_min_light_state' not in env_conf else env_conf['alarm_min_light_state'],
                                      'ignore' if 'alarm_min_door_state' not in env_conf else env_conf['alarm_min_door_state'],
                                      0.0      if 'alarm_min_duration_on' not in env_conf else env_conf['alarm_min_duration_on'],
                                      120.0    if 'alarm_min_settle' not in env_conf else env_conf['alarm_min_settle'],
                                      []       if ('alarm_min_powerswitches' not in env_conf or env_conf['alarm_min_powerswitches'] in ['',None]) else env_conf['alarm_min_powerswitches'])

      self.__environment_parts[env_part].set_alarm_max(
                                      '00:00'  if 'alarm_max_timer_start' not in env_conf else env_conf['alarm_max_timer_start'],
                                      '00:00'  if 'alarm_max_timer_stop' not in env_conf else env_conf['alarm_max_timer_stop'],
                                      1.0      if 'alarm_max_timer_on' not in env_conf else env_conf['alarm_max_timer_on'],
                                      59.0     if 'alarm_max_timer_off' not in env_conf else env_conf['alarm_max_timer_off'],
                                      'ignore' if 'alarm_max_light_state' not in env_conf else env_conf['alarm_max_light_state'],
                                      'ignore' if 'alarm_max_door_state' not in env_conf else env_conf['alarm_max_door_state'],
                                      0.0      if 'alarm_max_duration_on' not in env_conf else env_conf['alarm_max_duration_on'],
                                      120.0    if 'alarm_max_settle' not in env_conf else env_conf['alarm_max_settle'],
                                      []       if ('alarm_max_powerswitches' not in env_conf or env_conf['alarm_max_powerswitches'] in ['',None]) else env_conf['alarm_max_powerswitches'])

    logger.info('Done %s terrariumPI Environment %.3f seconds' % ('reloading' if reloading else 'loading',
                                                                                      time.time()-starttime))
    if reloading:
      self.update()

  def update(self, trigger = True):
    starttime = time.time()
    # Make sure that the light environment part is run first in order to determen 'day' or 'night' state
    environment_parts = list(self.__environment_parts.keys())
    environment_parts.remove('light')
    environment_parts = ['light'] + environment_parts

    for environment_part in environment_parts:
      if self.__environment_parts[environment_part] is None:
        logger.debug('Environment part %s is not setup' % (environment_part,))
        continue
      else:
        environment_part = self.__environment_parts[environment_part]

      logger.debug('Checking environment part %s: enabled: %s' % (environment_part.get_type(),
                                                                  environment_part.is_enabled()))
      if environment_part.is_enabled():
        logger.debug('Environment %s is enabled and based on: %s.' % (environment_part.get_type(),
                                                                      environment_part.get_mode()))
        environment_part.update(self.sensors,self.powerswitches,self.weather,self.__environment_parts['light'])
        if not trigger:
          continue

        toggle_on_alarm_min = None
        toggle_on_alarm_max = None

        if environment_part.in_sensor_mode():
          logger.debug('Environment %s sensors ok? %s' % (environment_part.get_type(),
                                                          environment_part.sensors_in_error()))
          if environment_part.sensors_in_error():
            logger.error('Environment %s sensors are not up to date. Check your sensors on the sensor page. So force the power down to be sure!' % (environment_part.get_type(),))
            toggle_on_alarm_min = False
            toggle_on_alarm_max = False
          else:
            toggle_on_alarm_min = environment_part.is_alarm_min()
            toggle_on_alarm_max = environment_part.is_alarm_max()

        elif environment_part.in_timer_mode() or environment_part.in_weather_mode() or environment_part.in_weather_inverse_mode():
          toggle_on_alarm_min = environment_part.is_time_min()
          toggle_on_alarm_max = environment_part.is_time_max()

          if toggle_on_alarm_min and environment_part.has_sensors() and not environment_part.sensors_in_error():
            # Use the extra added sensors for finetuning the trigger action
            toggle_on_alarm_min = environment_part.is_alarm_min()

          if toggle_on_alarm_max and environment_part.has_sensors() and not environment_part.sensors_in_error():
            # Use the extra added sensors for finetuning the trigger action
            toggle_on_alarm_max = environment_part.is_alarm_max()

        # There is an extra lights check. Only allow power on when the lights are in the same state as the environment light status, else force to off
        if 'ignore' != environment_part.get_alarm_min_light_state() and toggle_on_alarm_min is not False:
          # Check if the switch should be off
          if environment_part.get_alarm_min_light_state() != ('on' if self.light_on() else 'off'):
            # Switch should be set to off... so force to False to make sure the power will be shutdown if there is still power running...
            logger.debug('Forcing alarm low to off due to lights off')
            toggle_on_alarm_min = False

        # There is an extra lights check. Only allow power on when the lights are in the same state as the environment light status, else force to off
        if 'ignore' != environment_part.get_alarm_max_light_state() and toggle_on_alarm_max is not False:
          # Check if the switch should be off
          if environment_part.get_alarm_max_light_state() != ('on' if self.light_on() else 'off'):
            # Switch should be set to off... so force to False to make sure the power will be shutdown if there is still power running...
            logger.debug('Forcing alarm high to off due to lights off')
            toggle_on_alarm_max = False

        logger.debug('Environment %s is has alarm_min: %s, alarm_max: %s, trigger?: %s' % (environment_part.get_type(),toggle_on_alarm_min,toggle_on_alarm_max,trigger))

        if toggle_on_alarm_min is not None and not environment_part.has_alarm_min_powerswitches():
          logger.debug('Environment %s alarm min is triggered to state %s, but has no powerswitches configured' % (environment_part.get_type(),toggle_on_alarm_min))
        elif toggle_on_alarm_min is not None:
          settle_check = (environment_part.in_sensor_mode() or environment_part.has_sensors()) and not (environment_part.is_alarm_min_on() and not toggle_on_alarm_min)

          if settle_check and not environment_part.has_settled_alarm_min():
            logger.info('Environment %s alarm min is triggered to state %s, but the settle time has not passed: %s seconds.' % (environment_part.get_type(),toggle_on_alarm_min,environment_part.get_config()['alarm_min']['settle']))

          else:
            if toggle_on_alarm_min:

              if not environment_part.is_alarm_min_at_max_power():
                light_check_ok = 'ignore' == environment_part.get_alarm_min_light_state() or \
                                 (environment_part.get_alarm_min_light_state() == ('on' if self.light_on() else 'off'))
                door_check_ok  = 'ignore' == environment_part.get_alarm_min_door_state() or \
                                 (environment_part.get_alarm_min_door_state() == ('open' if self.is_door_open() else 'closed'))

                if light_check_ok and door_check_ok:
                  logger.info('Environment %s is turning on the alarm min powerswitches based on %s' % (environment_part.get_type(),environment_part.get_mode()))
                  environment_part.toggle_on_alarm_min(self.powerswitches)
                  self.notification.message('environment_' + environment_part.get_type() + '_alarm_low_on',environment_part.get_data('min'))
                else:
                  if not light_check_ok:
                    logger.info('Environment %s has blocked the alarm min powerswitches due to light state %s' % (environment_part.get_type(),environment_part.get_alarm_min_light_state()))
                  if not door_check_ok:
                    logger.warning('Environment %s has blocked the alarm min powerswitches due to door state %s' % (environment_part.get_type(),environment_part.get_alarm_min_door_state()))

              else:
                logger.debug('Environment %s alarm low is already at max power.' % environment_part.get_type())

            elif not toggle_on_alarm_min and not environment_part.is_alarm_min_at_min_power():
              logger.info('Environment %s is turning off the alarm min powerswitches based on %s' % (environment_part.get_type(),environment_part.get_mode()))
              environment_part.toggle_off_alarm_min(self.powerswitches)
              self.notification.message('environment_' + environment_part.get_type() + '_alarm_low_off',environment_part.get_data('min'))


        if toggle_on_alarm_max is not None and not environment_part.has_alarm_max_powerswitches():
          logger.debug('Environment %s alarm max is triggered to state %s, but has no powerswitches configured' % (environment_part.get_type(),toggle_on_alarm_max))
        elif toggle_on_alarm_max is not None:
          settle_check = (environment_part.in_sensor_mode() or environment_part.has_sensors()) and not (environment_part.is_alarm_max_on() and not toggle_on_alarm_max)

          if settle_check and not environment_part.has_settled_alarm_max():
            logger.info('Environment %s alarm max is triggered to state %s, but the settle time has not passed: %s seconds.' % (environment_part.get_type(),toggle_on_alarm_max,environment_part.get_config()['alarm_max']['settle']))

          else:
            if toggle_on_alarm_max:

              if not environment_part.is_alarm_max_at_max_power():
                light_check_ok = 'ignore' == environment_part.get_alarm_max_light_state() or \
                                 (environment_part.get_alarm_max_light_state() == ('on' if self.light_on() else 'off'))
                door_check_ok  = 'ignore' == environment_part.get_alarm_max_door_state() or \
                                 (environment_part.get_alarm_max_door_state() == ('open' if self.is_door_open() else 'closed'))

                if light_check_ok and door_check_ok:
                  logger.info('Environment %s is turning on the alarm max powerswitches based on %s' % (environment_part.get_type(),environment_part.get_mode()))
                  environment_part.toggle_on_alarm_max(self.powerswitches)
                  self.notification.message('environment_' + environment_part.get_type() + '_alarm_high_on',environment_part.get_data('max'))
                else:
                  if not light_check_ok:
                    logger.info('Environment %s has blocked the alarm max powerswitches due to light state %s' % (environment_part.get_type(),environment_part.get_alarm_max_light_state()))
                  if not door_check_ok:
                    logger.warning('Environment %s has blocked the alarm max powerswitches due to door state %s' % (environment_part.get_type(),environment_part.get_alarm_max_door_state()))

              else:
                logger.debug('Environment %s alarm high is already at max power.' % environment_part.get_type())

            elif not toggle_on_alarm_max and not environment_part.is_alarm_max_at_min_power():
              logger.info('Environment %s is turning off the alarm max powerswitches based on %s' % (environment_part.get_type(),environment_part.get_mode()))
              environment_part.toggle_off_alarm_max(self.powerswitches)
              self.notification.message('environment_' + environment_part.get_type() + '_alarm_high_off',environment_part.get_data('max'))


  def light_on(self):
    # Default is on, works better when no lights are configured
    on = True
    if isinstance(self.__environment_parts['light'],terrariumEnvironmentLight):
      on = self.__environment_parts['light'].is_alarm_min_on()

    return on

  def set_sensors(self,sensorlist):
    self.sensors = sensorlist
    self.update()

  def set_power_switches(self,powerswitchlist):
    self.powerswitches = powerswitchlist
    self.update()

  def stop(self):
    self.__running = False
    logger.info('Shutdown environment')

  def get_config(self):
    data = {}
    for env_part in self.__environment_parts:
      if self.__environment_parts[env_part] is not None:
        data[env_part] = self.__environment_parts[env_part].get_config()

    return data

  def get_data(self):
    data = {}
    for env_part in self.__environment_parts:
      if self.__environment_parts[env_part] is not None:
        data[env_part] = self.__environment_parts[env_part].get_data()

    return data

  def is_day(self):
    return self.weather.is_day()

  def is_night(self):
    return not self.is_day()

  def is_door_open(self):
    return self.__is_door_open()

  def is_door_closed(self):
    return not self.is_door_open()
  # End system functions
