# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from operator import itemgetter
import copy
import datetime

import statistics
import threading
import random

# http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
# https://onion.io/2bt-pid-control-python/
# https://github.com/m-lundberg/simple-pid
from simple_pid import PID
from gevent import sleep

from pony import orm
from terrariumAudio import terrariumAudioPlayer
from terrariumDatabase import Sensor, Playlist, Relay
from terrariumUtils import terrariumUtils, classproperty

class terrariumAreaException(TypeError):
  '''There is a problem with loading a hardware sensor.'''
  pass

class terrariumArea(object):

  __TYPES = {
    'lights' : {
      'name'    : _('Lighting'),
      'sensors' : [],
      'class' : lambda: terrariumAreaLights
    },

    'heating' : {
      'name'    : _('Heating'),
      'sensors' : ['temperature'],
      'class' : lambda: terrariumAreaHeater
    },

    'cooling' : {
      'name'    : _('Cooling'),
      'sensors' : ['temperature'],
      'class' : lambda: terrariumAreaCooler
    },

    'humidity' : {
      'name'    : _('Humidity'),
      'sensors' : ['humidity','moisture'],
      'class' : lambda: terrariumAreaHumidity
    },

    'watertank' : {
      'name'    : _('Water tank'),
      'sensors' : ['distance'],
      'class' : lambda: terrariumAreaWatertank
    },

    'audio' : {
      'name'    : _('Audio'),
      'sensors' : [],
      'class' : lambda: terrariumAreaAudio
    },

    'co2' : {
      'name'    : _('CO2'),
      'sensors' : ['co2']
    },

    'conductivity' : {
      'name'    : _('Conductivity'),
      'sensors' : ['conductivity']
    },

    'moisture' : {
      'name'    : _('Moisture'),
      'sensors' : ['moisture','humidity'],
      'class' : lambda: terrariumAreaMoisture
    },

    'ph' : {
      'name'    : _('PH'),
      'sensors' : ['ph']
    },
  }

  PERIODS = ['low','high']

  @classproperty
  def available_areas(__cls__):
    data = []
    for (type, area) in terrariumArea.__TYPES.items():
      data.append({'type' : type, 'name' : _(area['name']), 'sensors' : area['sensors']})

    return sorted(data, key=itemgetter('name'))

  # Return polymorph area....
  def __new__(cls, id, enclosure, type, name = '', mode = None, setup = None):
    known_areas = terrariumArea.available_areas

    if type not in [area['type'] for area in known_areas]:
      raise terrariumAreaException(f'Area of type {type} is unknown.')

    return super(terrariumArea, cls).__new__(terrariumArea.__TYPES[type]['class']())

  def __init__(self, id, enclosure, type, name, mode, setup):
    if id is None:
      id = terrariumUtils.generate_uuid()

    self.id   = id
    self.type = type
    self.name = name
    self.mode = mode

    self.enclosure = enclosure

    self.state = {}
    self.load_setup(setup)

  def __repr__(self):
    return f'{terrariumArea.__TYPES[self.type]["name"]} named {self.name}'


  @property
  def _powered(self):
    powered = None
    for period in self.PERIODS:
      if period not in self.state or len(self.setup[period]['relays']) == 0:
        continue

      powered = powered or self.state[period]['powered']

    return powered

  def _time_table(self):

    def make_time_table(begin, end, on_period = 0, off_period = 0):
      periods = []
      duration = 0

      now = datetime.datetime.now()
      begin = now.replace(hour=begin.hour, minute=begin.minute, second=begin.second)
      end   = now.replace(hour=end.hour,   minute=end.minute,   second=end.second)

      if begin == end:
        end += datetime.timedelta(hours=24)

      if begin > end:
        end += datetime.timedelta(hours=24)

      if now > end:
        begin += datetime.timedelta(hours=24)
        end   += datetime.timedelta(hours=24)

      if 0 == on_period and 0 == off_period:
        periods.append((int(begin.timestamp()), int(end.timestamp())))
        duration += periods[-1][1] - periods[-1][0]

      else:
        while begin < end:
          # The 'on' period is to big for the rest of the total timer time. So reduce it to the max left time
          if (begin + datetime.timedelta(seconds=on_period)) > end:
            on_period = (end - begin).total_seconds()

          # Add new entry int he time table
          periods.append((int(begin.timestamp()), int((begin + datetime.timedelta(seconds=on_period)).timestamp())))
          duration += periods[-1][1] - periods[-1][0]

          # Increate the start time with the on and off duration for the next round
          begin += datetime.timedelta(seconds=on_period + off_period)

      data = {
        'periods'  : periods,
        'duration' : duration
      }
      return data

    timetable = {}
    if 'main_lights' == self.mode:
      main_lights = self.enclosure.main_lights
      if main_lights is not None:
        for period in self.PERIODS:
          if period not in self.setup:
            continue

          self.setup[period]['timetable'] = copy.deepcopy(main_lights.setup['day' if 'low' == period else 'night']['timetable'])

          self.state[period]['begin']    = main_lights.state['day' if 'low' == period else 'night']['begin']
          self.state[period]['end']      = main_lights.state['day' if 'low' == period else 'night']['end']
          self.state[period]['duration'] = main_lights.state['day' if 'low' == period else 'night']['duration']

      return True

    if 'weather' == self.mode or 'weather_inverse' == self.mode:
      sunrise = copy.copy(self.enclosure.weather.sunrise if 'weather' == self.mode else self.enclosure.weather.sunset - datetime.timedelta(hours=24))
      sunset  = copy.copy(self.enclosure.weather.sunset  if 'weather' == self.mode else self.enclosure.weather.sunrise)

      max_hours = self.setup.get('max_day_hours',0.0)
      if max_hours != 0 and (sunset - sunrise) > datetime.timedelta(hours=max_hours):
        # On period to long, so reduce the on period by shifting the sunrise and sunset times closer to each other
        seconds_difference = ((sunset - sunrise) - datetime.timedelta(hours=max_hours)) / 2
        sunrise += seconds_difference
        sunset  -= seconds_difference

      min_hours = self.setup.get('min_day_hours',0.0)
      if min_hours != 0 and (sunset - sunrise) < datetime.timedelta(hours=min_hours):
        # On period to short, so extend the on period by shifting the sunrise and sunset times away from to each other
        seconds_difference = (datetime.timedelta(hours=min_hours) - (sunset - sunrise)) / 2
        sunrise -= seconds_difference
        sunset  += seconds_difference

      shift_hours = self.setup.get('shift_day_hours',0.0)
      if shift_hours != 0:
        # Shift the times back or forth...
        sunrise += datetime.timedelta(hours=shift_hours)
        sunset  += datetime.timedelta(hours=shift_hours)

      timetable['day']   = make_time_table(sunrise, sunset)
      timetable['night'] = make_time_table(sunset, sunrise)

    elif 'timer' == self.mode:
      for period in self.PERIODS:
        if period not in self.setup:
          continue

        begin      = datetime.time.fromisoformat(self.setup[period]['begin'])
        end        = datetime.time.fromisoformat(self.setup[period]['end'])
        on_period  = max(0.0,float(self.setup[period]['on_duration']))  * 60.0
        off_period = max(0.0,float(self.setup[period]['off_duration'])) * 60.0

        timetable[period] = make_time_table(begin, end, on_period, off_period)

    for period in timetable:
      if period not in self.setup:
        continue

      self.setup[period]['timetable'] = copy.deepcopy(timetable[period]['periods'])

      self.state[period]['begin']    = self.setup[period]['timetable'][0][0]
      self.state[period]['end']      = self.setup[period]['timetable'][-1][1]
      self.state[period]['duration'] = timetable[period]['duration']

    return True

  def load_setup(self, data):
    self.setup = copy.deepcopy(data)
    if self.state.get('last_update', None) is None:
      self.state = {
        'is_day'      : self.setup.get('is_day', None),
        'last_update' : int(datetime.datetime(1970,1,1).timestamp()),
        'powered'     : None
      }

    # Clean up parts that do not have relays configured)
    for period in self.PERIODS:

      if period in self.setup and len(self.setup[period]['relays']) == 0:
        del(self.setup[period])
        continue

      self.setup[period]['settle_time']   = self.setup[period].get('settle_time',0)
      self.setup[period]['power_on_time'] = self.setup[period].get('power_on_time',0)
      self.setup[period]['tweaks']        = {}

      if period not in self.state:
        self.state[period] = {}
        self.state[period]['last_powered_on'] = datetime.datetime(1970,1,1).timestamp()

      self.state[period]['powered'] = self.relays_state(period)

    if 'sensors' != self.mode:
      self._time_table()

    self.state['powered'] = self._powered

  def _is_timer_time(self, period):
    if 'main_lights' == self.mode:
      main_lights = self.enclosure.main_lights
      if main_lights is None:
        return None

      return main_lights._is_timer_time(period)

    now = int(datetime.datetime.now().timestamp())
    for time_schedule in self.setup[period]['timetable']:
      if now < time_schedule[0]:
        return False

      elif time_schedule[0] <= now < time_schedule[1]:
        return True

   # print('Timers are done')
   # print(self)
   # print(self.setup[period]['timetable'])
   # print(f'Day last timer: {datetime.datetime.fromtimestamp(self.setup[period]["timetable"][-1][1]).day} vs {datetime.datetime.now().day}')
    if 'weather' == self.mode and datetime.datetime.fromtimestamp(self.setup[period]['timetable'][-1][1]).day == datetime.datetime.now().day:
      # The day is not over yet, so return False. Else a new timetable for tomorrow will be calculated, and give wrong effect... This will delay it
      return False

    return None

  @property
  def is_day(self):
    if 'weather' == self.setup.get('day_night_source', None) and self.enclosure.weather is not None:
      return self.enclosure.weather.is_day

    return self.enclosure.lights_on

  def update(self):
    if 'disabled' == self.mode:
      return self.state

    light_state = ('on'     if self.enclosure.lights_on   else 'off')
    door_state  = ('closed' if self.enclosure.door_closed else 'open')

    old_is_day = self.state['is_day']
    self.state['is_day'] = self.is_day

    if 'sensors' in self.setup:
      # Change the sensor limits when changing from day to night and vs.
      if old_is_day != self.state['is_day'] and self.setup.get('day_night_difference', 0) != 0:
        difference = float(self.setup['day_night_difference']) * (-1.0 if self.state['is_day'] else 1.0)
        logger.info(f'Adjusting the sensors based on day/night difference. Changing by {difference} going from {("day" if old_is_day else "night")} to {("day" if self.state["is_day"] else "night")}')

        with orm.db_session():
          for sensor in Sensor.select(lambda s: s.id in self.setup['sensors']):
            sensor.alarm_min += difference
            sensor.alarm_max += difference

      # If there are sensors in use, calculate the current values
      self.state['sensors'] = self.current_value(self.setup['sensors'])
      # And set the alarm values
      self.state['sensors']['alarm_low']  = self.state['sensors']['current'] < self.state['sensors']['alarm_min']
      self.state['sensors']['alarm_high'] = self.state['sensors']['current'] > self.state['sensors']['alarm_max']

    for period in self.PERIODS:
      if period not in self.setup:
        continue

      # Set the lights state. Default True
      light_state_ok = True
      if 'light_status' in self.setup[period] and 'ignore' != self.setup[period]['light_status']:
        # Change the lights state based on the current state and requested state. False when not equal
        light_state_ok = self.setup[period]['light_status'] == light_state

      # Set the doors state. Default True
      door_state_ok = True
      if 'door_status' in self.setup[period] and 'ignore' != self.setup[period]['door_status']:
        # Change the doors state based on the current state and requested state. False when not equal
        door_state_ok = self.setup[period]['door_status'] == door_state

      # First check: Shutdown power when power is on and either the lights or doors are in wrong state. Despide 'mode'
      if self.state[period]['powered'] and not (light_state_ok and door_state_ok):
        # Power is on, but either the lights or doors are in wrong state. Power down now.
        logger.info(f'Forcing down the {period} power for area {self} because either the lights({"OK" if light_state_ok else "ERROR"}) or doors({"OK" if door_state_ok else "ERROR"}) are in an invalid state.')
        self.relays_toggle(period,False)
        # And ignore the rest....
        continue


      if 'sensors' != self.mode:
        # Weather(inverse) and timer mode
        toggle_relay = self._is_timer_time(period)

        if toggle_relay is None:
          print(f'Recalc time table for {self}')
          self._time_table()
          toggle_relay = False

        if toggle_relay is True and 'sensors' in self.setup:
          # We are in timer mode. But when there are sensors configured, they act as a second check
          # If there is NOT an alarm with the period name, then skip the toggle action.
          if self.state['sensors'][f'alarm_{period}'] is not True:
            logger.info(f'Relays for area {self} at period {period} are not switched because the additional sensors are at value: {self.state["sensors"]["current"]:.2f}{self.enclosure.engine.units[self.state["sensors"]["unit"]]}.')
            continue
      else:
        # Sensor mode only toggle ON when alarms are triggered (True).
        toggle_relay = self.state['sensors'][f'alarm_{period}']
        #print(f'Toggle on/off {period} based on sensors -> {toggle_relay}')
        if toggle_relay is False:
          other_alarm = self.state['sensors'][f'alarm_{("low" if period == "high" else "high")}']
          #print(f'Inverse alarm: {other_alarm}')
          toggle_relay = False if other_alarm else None
          #print(f'Final toggle state for relay based on sensors: {toggle_relay}')

      if toggle_relay is True and not self.state[period]['powered']:

        if not light_state_ok:
          logger.debug(f'Relays for {self} are not switched because the ligts are {light_state} while {self.setup[period]["light_status"]} is requested.')
          #print(f'Relays for {self} are not switched because the ligts are {light_state} while {self.setup[period]["light_status"]} is requested.')
          continue

        if not door_state_ok:
          logger.debug(f'Relays for {self} are not switched because the door is {door_state} while {self.setup[period]["door_status"]} is requested.')
          continue

        time_elapsed = int(datetime.datetime.now().timestamp()) - self.state[period]['last_powered_on']
        if time_elapsed <= self.setup[period]['settle_time']:
          logger.info(f'Relays for {self} are not switched because we have to wait for {self.setup[period]["settle_time"]-time_elapsed} more seconds of the total settle time of {self.setup[period]["settle_time"]} seconds.')
          continue

        self.relays_toggle(period,True)
        self.state[period]['last_powered_on'] = int(datetime.datetime.now().timestamp())
        if self.setup[period]['power_on_time'] > 0.0:
          self.state[period]['timer_on'] = True
          threading.Timer(self.setup[period]['power_on_time'], self.relays_toggle, [period, False]).start()


      elif toggle_relay is False and self.state[period]['powered'] and not self.state[period].get('timer_on',False):
        logger.info(f'Toggle off the relays for area {self}.')
        self.relays_toggle(period,False)

    self.state['powered'] = self._powered
    self.state['last_update'] = int(datetime.datetime.now().timestamp())
    return self.state

  def current_value(self, sensors):
    sensor_values = {
      'current'   : [],
      'alarm_max' : [],
      'alarm_min' : [],
      'unit' : ''
    }

    with orm.db_session():
      for sensor in Sensor.select(lambda s: s.id in sensors):
        if sensor.value is None:
          # Broken sensor, so ignore it
          continue

        sensor_values['current'].append(sensor.value)
        sensor_values['alarm_max'].append(sensor.alarm_max)
        sensor_values['alarm_min'].append(sensor.alarm_min)
        sensor_values['unit'] = sensor.type

    for key in sensor_values:
      if 'unit' == key:
        continue

      if len(sensor_values[key]) == 0:
        sensor_values[key] = 0
      else:
        sensor_values[key] = statistics.mean(sensor_values[key])

    sensor_values['alarm'] = not sensor_values['alarm_min'] <= sensor_values['current'] <= sensor_values['alarm_max']

    return sensor_values

  def relays_state(self, part):
    for relay in self.setup[part]['relays']:
      if self.enclosure.relays[relay].is_off():
        return False

    return True

  def relays_toggle(self, part, on):
    logger.info(f'Toggle the relays for area {self} to state {("on" if on else "off")}.')

    with orm.db_session():
      relays = orm.select(r.id for r in Relay if r.id in self.setup[part]['relays'] and not r.manual_mode)

#    print(relays)
#      relays = [relay.to_dict(only='id') for relay in Relay.select(lambda r: r.id in self.setup[part]['relays'] and not r.manual_mode)]

      # for db_relay in Relay.select(lambda r: r.id in self.setup[part]['relays'] and not r.manual_mode):
      #   if db_relay.manual_mode:
      #     continue

    for relay in relays:
      print(f'Toggle relay: {relay}')
      relay = self.enclosure.relays[relay]
      self._relay_action(part, relay, on)

      if on:
        self.state[part]['last_powered_on'] = int(datetime.datetime.now().timestamp())
      else:
        self.state[part]['timer_on'] = False

    self.state[part]['powered'] = on
    self.state['powered'] = self._powered

  def _relay_action(self, part, relay, action):
    if relay.id in self.enclosure.relays:
      logger.info(f'Set the relay {relay.name} to {relay.ON if on else relay.OFF}')
      self.enclosure.relays[relay.id].on(relay.ON if action else relay.OFF)


  # def _time_schema(self):
  #   return {
  #     'low'   : None,
  #     'hight' : None,
  #   }



  def stop(self):
    logger.info(f'Stopped Area {self}')


class terrariumAreaLights(terrariumArea):

  PERIODS = ['day','night']

  def load_setup(self, data):
    super().load_setup(data)

    #print('Load terrariumAreaLights setup')

    # Load extra tweaks
    for period in self.PERIODS:
     # print(f'Test period: {period}')
      if period not in self.setup:
      #  print(f'Period not found {period}')
        continue

      #print('Going over the relays')
      for relay_id in self.setup[period]['relays']:
        relay = self.enclosure.relays[relay_id]
       # print(f'Load relay {relay}')

        extra_tweaks = self.setup[period].get(('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'on_' + relay.id, None)
        if extra_tweaks is None:
          continue

        self.setup[period]['tweaks'][relay.id] = {
          'on' : {
            'delay'    : 0,
            'duration' : 0
          },
          'off' : {
            'delay'    : 0,
            'duration' : 0
          }
        }

        if relay.is_dimmer:
          values = self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'on_' + relay.id].split(',')
        #  print(f'Value data from period = {period}, : {values}')
          if len(values) == 1:
            values = [0,values[0]]

          self.setup[period]['tweaks'][relay.id]['on']['delay']    = float(values[0]) * 60.0
          self.setup[period]['tweaks'][relay.id]['on']['duration'] = float(values[1]) * 60.0

          values = self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'off_' + relay.id].split(',')
          if len(values) == 1:
            values = [0,values[0]]

          self.setup[period]['tweaks'][relay.id]['off']['delay']    = float(values[0]) * 60.0
          self.setup[period]['tweaks'][relay.id]['off']['duration'] = float(values[1]) * 60.0
        else:
          value = self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'on_' + relay.id]
          self.setup[period]['tweaks'][relay.id]['on']['delay']  = float(value) * 60.0
          value = self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'off_' + relay.id]
          self.setup[period]['tweaks'][relay.id]['off']['delay'] = float(value) * 60.0

    # Reset the powerd on state if the dimmers are not at max value. So the dimmer will continue where it left off
    for period in self.PERIODS:
      if period not in self.setup:
        continue

      if self.state[period]['powered']:
        max_states = []
        if self._is_timer_time(period):
          for relay in self.setup[period]['relays']:
            relay = self.enclosure.relays[relay]
            if relay.is_dimmer:
              max_states.append(relay.state == relay.ON)

        self.state[period]['powered'] = all(max_states)

    self.state['powered'] = self._powered

  def _relay_action(self, part, relay, action):
    if relay.id not in self.enclosure.relays:
      return

    tweaks = {
      'duration' : 0,
      'delay'    : 0
    }
    try:
      tweaks = self.setup[part]['tweaks'][f'{relay.id}']['on' if action else 'off']
    except Exception as ex:
      print(f'Could not find the tweaks: {relay.id}, state {"on" if action else "off"}')
      print(ex)

    # If the relay is a dimmer, recalc the on/off duration based on current state
    #print('Tweaks in relay action')
    #print(tweaks)

    if relay.is_dimmer:
      #print(f'Duration: {tweaks["duration"]}, on = {relay.ON}, off = {relay.OFF}, on-off = {relay.ON - relay.OFF}')
      step_size = tweaks['duration'] / (relay.ON - relay.OFF)
      #print(f'Duration step size: {step_size}')
      tweaks['duration'] = step_size * abs((relay.ON if action else relay.OFF) - relay.state)

      # If the relay is already powered and should be power up, ignore the delay time. Force to zero delay
      # Same for going out. When the lights should be off, and they are not at full power, no delay.
      if (action and relay.state != relay.OFF) or (not action and relay.state != relay.ON):
        tweaks['delay'] = 0

      if action:
        logger.info(f'Start the dimmer {relay.name} from {relay.state}% to {relay.ON}% in {tweaks["duration"]} seconds with a delay of {tweaks["delay"]/60} minutes')
      else:
        logger.info(f'Stopping the dimmer {relay.name} from {relay.state}% to {relay.OFF}% in {tweaks["duration"]} seconds with a delay of {tweaks["delay"]/60} minutes')

      self.enclosure.relays[relay.id].on(relay.ON if action else relay.OFF, duration=tweaks["duration"], delay=tweaks["delay"])

    else:
      logger.info(f'Set the relay {relay.name} to {relay.ON if action else relay.OFF} with a delay of {tweaks["delay"]/60} minutes')
      self.enclosure.relays[relay.id].on(relay.ON if action else relay.OFF, delay=tweaks["delay"])

class terrariumAreaHeater(terrariumArea):

  def __init__(self, id, enclosure, type, name, mode, setup):
    self.__dimmers = {}
    super().__init__(id, enclosure, type, name, mode, setup)

  def load_setup(self, data):
    super().load_setup(data)

    # Restore running dimmers with PID if running in sensor mode
    if 'sensors' == self.mode:
      for period in self.PERIODS:
        if period not in self.setup or not self.state[period]['powered']:
          continue

        for relay in self.setup[period]['relays']:
          relay = self.enclosure.relays[relay]
          if relay.is_dimmer:
            self._relay_action(period,relay,True)

    self.state['powered'] = self._powered

  def update(self):
    super().update()
    if 'disabled' != self.mode and len(self.__dimmers) > 0:
      sensor_values  = self.current_value(self.setup['sensors'])
      sensor_average = float(sensor_values['alarm_min'] + sensor_values['alarm_max']) / 2.0

      for period in self.PERIODS:
        if period not in self.setup:
          continue

        for relay in self.setup[period]['relays']:
          relay = self.enclosure.relays[relay]
          if relay.id in self.__dimmers:

            self.__dimmers[relay.id].setpoint = sensor_average
            self.__dimmers[relay.id].output_limits = (relay.OFF,relay.ON)

            dimmer_value = round(self.__dimmers[relay.id](sensor_values['current']))
            logger.info(f'Updating the dimmer {relay} to value {dimmer_value}%. Current value {sensor_values["current"]}{self.enclosure.engine.units[sensor_values["unit"]]}, target of {sensor_average}{self.enclosure.engine.units[sensor_values["unit"]]}')
            self.enclosure.relays[relay.id].on(dimmer_value)

    self.state['powered'] = self._powered
    return self.state

  def _relay_action(self, part, relay, action):
    if relay.id in self.enclosure.relays:

      if action:
        if relay.id in self.__dimmers:
          return

        if relay.is_dimmer and 'sensors' == self.mode:
          sensor_values      = self.current_value(self.setup['sensors'])
          sensor_average     = float(sensor_values['alarm_min'] + sensor_values['alarm_max']) / 2.0
          settle_time        = max(1,self.setup[part]['settle_time'])
          heating_or_cooling = 1.0 if 'low' == part else -1.0

          logger.info(f'Start the dimmer {relay} in PID modus to go to average value {sensor_average}{self.enclosure.engine.units[sensor_values["unit"]]} with a settile timeout of {settle_time} seconds.')
          self.__dimmers[relay.id] = PID(heating_or_cooling * 1, heating_or_cooling * 0.1, heating_or_cooling * 0.05,
                                        setpoint=sensor_average,
                                        sample_time=settle_time,
                                        output_limits=(relay.OFF,relay.ON))

          if relay.state > 0:
            dimmer_value = relay.state
            logger.info(f'Restoring old dimmer value {dimmer_value}% for relay {relay}')
            self.__dimmers[relay.id].set_auto_mode(True, last_output=dimmer_value)
          else:
            dimmer_value = round(self.__dimmers[relay.id](sensor_values['current']))
            logger.info(f'Setting the dimmer {relay} to value {dimmer_value}%. Current value {sensor_values["current"]}{self.enclosure.engine.units[sensor_values["unit"]]}, target of {sensor_average}{self.enclosure.engine.units[sensor_values["unit"]]}')

          self.enclosure.relays[relay.id].on(dimmer_value)
        else:
          logger.info(f'Set the relay {relay} to {relay.ON} with 0 seconds delay')
          self.enclosure.relays[relay.id].on(relay.ON)

      else:
        logger.info(f'Set the relay {relay} to {relay.OFF} with 0 seconds delay')
        self.enclosure.relays[relay.id].on(relay.OFF)
        self.state[part]['timer_on'] = False
        if relay.id in self.__dimmers:
          del(self.__dimmers[relay.id])

class terrariumAreaCooler(terrariumAreaHeater):
  pass

class terrariumAreaHumidity(terrariumArea):
  pass

class terrariumAreaMoisture(terrariumAreaHumidity):
  pass

class terrariumAreaWatertank(terrariumArea):
  def current_value(self, sensors):
    # TODO: Check if use of gall and inch does influence this...
    volume_per_distance = self.setup['watertank_volume'] / (self.setup['watertank_height'] - self.setup['watertank_offset'])

    sensor_values = {
      'current'   : [],
      'alarm_max' : [],
      'alarm_min' : [],
      'unit' : 'watertank'
    }
    for sensor in Sensor.select(lambda s: s.id in sensors):
      if sensor.value is None:
        # Broken sensor, so ignore it
        continue

      sensor_values['current'].append(self.setup['watertank_volume']   - (sensor.value     - self.setup['watertank_offset']) * volume_per_distance)
      sensor_values['alarm_max'].append(self.setup['watertank_volume'] - (sensor.alarm_min - self.setup['watertank_offset']) * volume_per_distance)
      sensor_values['alarm_min'].append(self.setup['watertank_volume'] - (sensor.alarm_max - self.setup['watertank_offset']) * volume_per_distance)

    for key in sensor_values:
      if 'unit' == key:
        continue

      sensor_values[key] = statistics.mean(sensor_values[key])

    sensor_values['alarm'] = not sensor_values['alarm_min'] <= sensor_values['current'] <= sensor_values['alarm_max']

    return sensor_values

class terrariumAreaAudio(terrariumArea):
  PERIODS = ['day','night']

  def load_setup(self, data):
    data = copy.deepcopy(data)

    # Rename the playlists variables back to relays so the rest of the code will work...
    data['day']['relays']   = copy.copy(data['day']['playlists'])
    data['night']['relays'] = copy.copy(data['night']['playlists'])

    del(data['day']['playlists'])
    del(data['night']['playlists'])

    super().load_setup(data)

    for period in self.PERIODS:
      if period not in self.setup:
        continue

      playlists = [playlist for playlist in self.setup[period]['relays']]
      with orm.db_session():
        playlists = [playlist.to_dict(with_collections=True,related_objects=True) for playlist in Playlist.select(lambda pl: pl.id in playlists)]
        for playlist in playlists:
          playlist['files'] = [audiofile.to_dict(only='filename')['filename'] for audiofile in playlist['files']]

      self.setup[period]['player'] = terrariumAudioPlayer(self.setup['soundcard'], playlists)

  def relays_state(self, period):
    # We do not check if the player is actual running. This will cause an unwanted repeat functionality
    return period in self.state and self.state[period].get('powered',False)

  def relays_toggle(self, period, on):
    if period not in self.setup:
      return False

    logger.info(f'Toggle the player for area {self} period {period} to state {("on" if on else "off")}.')

    if on:
      other_period = copy.copy(self.PERIODS)
      logger.info(f'Other periods: {other_period}')
      other_period.remove(period)
      other_period = other_period[0]
      logger.info(f'Other periods clean: {other_period}')

      if other_period in self.setup:
        logger.info(f'Stopping other ({other_period}) running player')
        self.setup[other_period]['player'].stop()

      logger.info(f'Starting audio player for {period}')
      self.setup[period]['player'].play()

    else:
      logger.info(f'Stopping audio player for {period}')
      self.setup[period]['player'].stop()

    self.state[period]['powered'] = on
    self.state['powered'] = self._powered

  def stop(self):
    for period in self.PERIODS:
      if period not in self.setup:
        continue

      self.setup[period]['player'].stop()