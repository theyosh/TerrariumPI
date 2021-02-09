# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from operator import itemgetter
import copy
import datetime

import statistics
import threading
import uuid

# http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
# https://github.com/m-lundberg/simple-pid
from simple_pid import PID

from pony import orm
from terrariumDatabase import Sensor
from terrariumUtils import terrariumUtils, classproperty

class terrariumAreaException(TypeError):
  '''There is a problem with loading a hardware sensor.'''
  pass

class terrariumArea(object):

  __TYPES = {
    'lights' : {
      'name'    : _('Lights'),
      'sensors' : [],
      'class' : lambda: terrariumAreaLights
    },

    'temperature' : {
      'name'    : _('Heating / cooling'),
      'sensors' : ['temperature'],
      'class' : lambda: terrariumAreaTemperature
    },

    'humidity' : {
      'name'    : _('Humidity'),
      'sensors' : ['humidity','moisture'],
      'class' : lambda: terrariumAreaHumidity
    },

    'co2' : {
      'name'    : _('CO2'),
      'sensors' : ['co2']
    },

    'conductivity' : {
      'name'    : _('Conductivity'),
      'sensors' : ['conductivity']
    },

    'watertank' : {
      'name'    : _('Watertank'),
      'sensors' : ['distance'],
      'class' : lambda: terrariumAreaWatertank
    },

    'moisture' : {
      'name'    : _('Moisture'),
      'sensors' : ['moisture','humidity']
    },

    'ph' : {
      'name'    : _('PH'),
      'sensors' : ['ph']
    },
  }

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
      id = str(uuid.uuid4())

    self.id   = id
    self.type = type
    self.name = name
    self.mode = mode

    self.enclosure = enclosure

    self.load_setup(setup)


  def __repr__(self):
    return f'{terrariumArea.__TYPES[self.type]["name"]} area {self.name}'

  def _time_table(self):

    def make_time_table(begin, end, on_period = 0, off_period = 0):
      periods = []
      duration = 0

      now = datetime.datetime.now()
      begin = now.replace(hour=begin.hour, minute=begin.minute, second=begin.second)
      end   = now.replace(hour=end.hour,   minute=end.minute,   second=end.second)

      if begin == end:
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


    if 'weather' == self.mode or 'weather_inverse' == self.mode:
      sunrise = copy.copy(self.enclosure.weather.sunrise if 'weather' == self.mode else self.enclosure.weather.sunset - datetime.timedelta(hours=24))
      sunset  = copy.copy(self.enclosure.weather.sunset  if 'weather' == self.mode else self.enclosure.weather.sunrise)

      if datetime.datetime.now() > sunset:
        sunrise += datetime.timedelta(hours=24)
        sunset  += datetime.timedelta(hours=24)

      if self.setup['day']['max_hours'] != 0 and (sunset - sunrise) > datetime.timedelta(hours=self.setup['day']['max_hours']):
        # On period to long, so reduce the on period by shifting the sunrise and sunset times closer to each other
        seconds_difference = ((sunset - sunrise) - datetime.timedelta(hours=self.setup['day']['max_hours'])) / 2
        sunrise += seconds_difference
        sunset  -= seconds_difference

      if self.setup['day']['min_hours'] != 0 and (sunset - sunrise) < datetime.timedelta(hours=self.setup['day']['min_hours']):
        # On period to short, so extend the on period by shifting the sunrise and sunset times away from to each other
        seconds_difference = (datetime.timedelta(hours=self.setup['day']['min_hours']) - (sunset - sunrise)) / 2
        sunrise -= seconds_difference
        sunset  += seconds_difference

      if self.setup['day']['shift_hours'] != 0:
        # Shift the times back or forth...
        sunrise += datetime.timedelta(hours=self.setup['day']['shift_hours'])
        sunset  += datetime.timedelta(hours=self.setup['day']['shift_hours'])

      timetable['day'] = make_time_table(sunrise, sunset)

    elif 'timer' == self.mode:
      for period in ['day','night','low','high']:
        if period in self.setup:

          begin = datetime.time.fromisoformat(self.setup[period]['begin'])
          end   = datetime.time.fromisoformat(self.setup[period]['end'])
          on_period  = max(0.0,float(self.setup[period]['on_duration']))  * 60.0
          off_period = max(0.0,float(self.setup[period]['off_duration'])) * 60.0

          timetable[period] = make_time_table(begin, end, on_period, off_period)

    for period in ['day','night','low','high']:
      if period not in timetable:
        continue

      self.setup[period]['timetable'] = copy.deepcopy(timetable[period]['periods'])

      self.state[period]['begin']    = self.setup[period]['timetable'][0][0]
      self.state[period]['end']      = self.setup[period]['timetable'][-1][1]
      self.state[period]['duration'] = timetable[period]['duration']

    return True

  def load_setup(self, data):
    self.setup = copy.deepcopy(data)

    self.state = {
      'last_update' : int(datetime.datetime(1970,1,1).timestamp()),
      'powered' : None
    }

    # Clean up parts that do not have relays configured)
    for period in ['day','night','low','high']:

      if period in self.setup and len(self.setup[period]['relays']) == 0:
        del(self.setup[period])

    for period in ['day','night','low','high']:
      if period not in self.setup:
        continue

#      self.state['powered'] = False
      self.state['powered'] = self.relays_state(period)

      if period not in self.state:
        self.state[period] = {}

      self.state[period]['last_powered_on'] = datetime.datetime(1970,1,1).timestamp()
      self.setup[period]['settle_time']   = self.setup[period].get('settle_time',0)
      self.setup[period]['power_on_time'] = self.setup[period].get('power_on_time',0)

      if 'sensors' != self.mode:

        if period not in self.state:
          self.state[period] = {}

        self._time_table()


      ## Add the dimmer / relay extra tweaks...

      # print('TWEAKS')
      # print(self)
      # print(self.setup[period])

      self.setup[period]['tweaks'] = {}

      dimmer_found = False
      average_dimmer_durations = {'on' : [], 'off' : []}
      for relay_id in self.setup[period]['relays']:
        relay = self.enclosure.relays[relay_id]
        if not dimmer_found:
          dimmer_found = relay.is_dimmer

        field = ('dimmer_duration_' if relay.is_dimmer else 'relay_step_') + 'on_' + relay.id
        extra_tweaks = self.setup[period].get(field, False)

 #       print(f'Looking for field {field} -> {extra_tweaks}')

#        extra_tweaks = self.setup[period].get(field, False)


        if extra_tweaks != False:

          # Durations are in minutes for dimmers, in percentage for relays
          self.setup[period]['tweaks'][relay.id] = {
            'on'  : float(self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_step_') + 'on_' + relay.id]),
            'off' : float(self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_step_') + 'off_' + relay.id]),
          }

          # print('tweaks added')
          # print(self.setup[period]['tweaks'])

          if relay.is_dimmer:
            average_dimmer_durations['on'].append(self.setup[period]['tweaks'][relay.id]['on'])
            average_dimmer_durations['off'].append(self.setup[period]['tweaks'][relay.id]['off'])

      if not dimmer_found:
        # There was no dimmer in the relay list. So all normal on/off.
        self.setup[period]['tweaks'] = {}
      elif len(average_dimmer_durations['on']) > 0:
        # Add the average dimmer duration, so that the normal relays can use for their percentage delay toggle
        self.setup[period]['tweaks']['on']  = {'dimmer_duration' : statistics.mean(average_dimmer_durations['on'])}
        self.setup[period]['tweaks']['off'] = {'dimmer_duration' : statistics.mean(average_dimmer_durations['off'])}

      # print('Extra tweaks')
      # print(self.setup[period]['tweaks'])


  def _is_timer_time(self, period):
    now = int(datetime.datetime.now().timestamp())
    for time_schedule in self.setup[period]['timetable']:
      if time_schedule[0] <= now < time_schedule[1]:
        return True

      elif now < time_schedule[0]:
        return False

    return None

  def update(self):
    light_state = ('on'     if self.enclosure.lights_on   else 'off')
    door_state  = ('closed' if self.enclosure.door_closed else 'open')

    if 'sensors' in self.setup:
      # If there are sensors in use, calculate the current values
      self.state['sensors'] = self.current_value(self.setup['sensors'])
      # And set the alarm values
      self.state['sensors']['alarm_low']  = self.state['sensors']['current'] < self.state['sensors']['alarm_min']
      self.state['sensors']['alarm_high'] = self.state['sensors']['current'] > self.state['sensors']['alarm_max']

    for period in ['day','night','low','high']:
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
      if self.state['powered'] and not (light_state_ok and door_state_ok):
        # Power is on, but either the lights or doors are in wrong state. Power down now.
        logger.info(f'Forcing down the {period} power for area {self} because either the lights({"OK" if light_state_ok else "ERROR"}) or doors({"OK" if door_state_ok else "ERROR"}) are in an invalid state.')
        self.relays_toggle(period,False)
        # And ignore the rest....
        continue


      if 'sensors' != self.mode:
        # Weather(inverse) and timer mode
        toggle_relay = self._is_timer_time(period)

        if toggle_relay is True and 'sensors' in self.setup:
          # We are in timer mode. But when there are sensors configured, they act as a second check
          # If there is NOT an alarm with the period name, then skip the toggle action.
          if self.state['sensors'][f'alarm_{period}'] is not True:
            logger.info(f'Relays for area {self} at period {period} are not switched because the additional sensors are at value: {self.state["sensors"]["current"]:.2f}{self.enclosure.engine.units[self.state["sensors"]["unit"]]}.')
            continue
      else:
        # Sensor mode only toggle ON when alarms are triggered (True).
        toggle_relay = self.state['sensors'][f'alarm_{period}']
        print(f'Toggle on/off {period} based on sensors -> {toggle_relay}')
        if toggle_relay is False:
          other_alarm = self.state['sensors'][f'alarm_{("low" if period == "high" else "high")}']
          print(f'Inverse alarm: {other_alarm}')
          toggle_relay = False if other_alarm else None
          print(f'Final toggle state for relay based on sensors: {toggle_relay}')

      if toggle_relay is True and not self.state['powered']:

        if not light_state_ok:
          logger.debug(f'Relays for {self} are not switched because the ligts are {light_state} while {self.setup[period]["light_status"]} is requested.')
          print(f'Relays for {self} are not switched because the ligts are {light_state} while {self.setup[period]["light_status"]} is requested.')
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


      elif False == toggle_relay and self.state['powered'] and not self.state[period].get('timer_on',False):
        logger.info(f'Toggle off the relays for area {self}.')
        self.relays_toggle(period,False)

      elif 'sensors' != self.mode and toggle_relay is None:
        print(f'Recalc time table for {self}')
        self._time_table()

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

    for relay in self.setup[part]['relays']:
      relay = self.enclosure.relays[relay]

      if on:
        logger.info(f'Set the relay {relay.name} to ON')
        self.enclosure.relays[relay.id].on(relay.ON)

      else:
        logger.info(f'Set the relay {relay.name} to OFF')
        self.enclosure.relays[relay.id].on(relay.OFF)
        self.state[part]['timer_on'] = False

    self.state['powered'] = on


  def _time_schema(self):
    return {
      'low'   : None,
      'hight' : None,
    }


class terrariumAreaLights(terrariumArea):

  def relays_toggle(self, part, on):
    logger.info(f'Toggle the relays for area {self} to state {("on" if on else "off")}.')

    for relay in self.setup[part]['relays']:
      relay = self.enclosure.relays[relay]
      tweaks = self.setup[part]['tweaks']

      duration_or_delay_value = tweaks.get(str(relay.id), None)
      duration_or_delay_value = 0 if duration_or_delay_value is None else float(duration_or_delay_value['on' if on else 'off'])

      if relay.is_dimmer:
        duration_or_delay_value *= 60.0
      else:
        duration_or_delay_value = (float(duration_or_delay_value)/100) * (tweaks['on' if on else 'off']['dimmer_duration'] * 60.0)

      if on:

        if relay.is_dimmer:
          logger.info(f'Start the dimmer {relay.name} from 0 to {relay.ON}% in {duration_or_delay_value} seconds')
          # TODO: In the future we will also be able to set the ON value...
        else:
          logger.info(f'Set the relay {relay.name} to on with {duration_or_delay_value} seconds delay')

        self.enclosure.relays[relay.id].on(relay.ON,duration_or_delay_value)
        self.state[part]['last_powered_on'] = int(datetime.datetime.now().timestamp())

      else:

        if relay.is_dimmer:
          logger.info(f'Stopping the dimmer {relay.name} from {relay.OFF}% to 0 in {duration_or_delay_value} seconds')
          # TODO: In the future we will also be able to set the ON value...
        else:
          logger.info(f'Set the relay {relay.name} to off with {duration_or_delay_value} seconds delay')

        self.enclosure.relays[relay.id].on(relay.OFF,duration_or_delay_value)

        self.state[part]['timer_on'] = False

    self.state['powered'] = on

class terrariumAreaTemperature(terrariumArea):


  def __init__(self, id, enclosure, type, name, mode, setup):
    # https://onion.io/2bt-pid-control-python/
    self.__pid = None
    super().__init__(id, enclosure, type, name, mode, setup)

  def update(self):
    super().update()
#    print(f'Update terrariumAreaTemperature {self.__pid}')
    if self.__pid is not None:
      # Update the heater/cooler dimmer values

      current_values = self.current_value(self.setup['sensors'])

      self.__pid.setpoint = (current_values['alarm_min'] + current_values['alarm_max']) / 2.0
      self.__pid.sample_time = max(1,self.setup[period]["settle_time"])

      dimmer_value = round(self.__pid(current_values['current']))

      for period in ['day','night','low','high']:
        if period not in self.setup:
          continue

        for relay in self.setup[period]['relays']:
          relay = self.enclosure.relays[relay]
          if relay.is_dimmer:
            print(f'Put dimmer {self} to state: {dimmer_value}% based on temp: {current_values["current"]} -> goal: {self.__pid.setpoint}')
            self.enclosure.relays[relay.id].on(dimmer_value)

    return self.state

  def relays_toggle(self, part, on):
    print(f'Toggle the relays for area {self} to state {("on" if on else "off")}.')
    logger.info(f'Toggle the relays for area {self} to state {("on" if on else "off")}.')

    for relay in self.setup[part]['relays']:
      relay = self.enclosure.relays[relay]
      # print('Relay')
      # print(relay)

      if on:
        print('Set to on....')
        print(f'Is dimmer: {relay.is_dimmer}')
        print(f'Has sensors: {"sensors" in self.setup}')

        if relay.is_dimmer and 'sensors' in self.setup:
          current_values = self.current_value(self.setup['sensors'])
          pid_target = (current_values['alarm_min'] + current_values['alarm_max']) / 2.0

          logger.info(f'Start the dimmer {relay.name} in PID modus to go to average value {pid_target}')
          print(f'Start the dimmer {relay.name} in PID modus to go to average value {pid_target}')
          print(f'Min max values: (0,{relay.ON}), sample_time {self.setup[period]["settle_time"]}')
          if self.__pid is None:
            self.__pid = PID(1, 0.1, 0.05,
                              setpoint=pid_target,
                              sample_time=max(1,self.setup[period]["settle_time"]),
                              output_limits=(0,100))

            print(f'Starting dimmer {self} with PID setup. Target temp {self.__pid}')
            dimmer_value = round(self.__pid(current_values['current']))
            print(f'Put dimmer {self} to state: {dimmer_value}%')
            self.enclosure.relays[relay.id].on(dimmer_value)

        else:
          print(f'Set the relay {relay.name} to ON with 0 seconds delay')
          logger.info(f'Set the relay {relay.name} to ON with 0 seconds delay')
          self.enclosure.relays[relay.id].on(relay.ON)

        self.state[part]['last_powered_on'] = int(datetime.datetime.now().timestamp())

      else:
        print(f'Set the relay {relay.name} to OFF with 0 seconds delay')
        logger.info(f'Set the relay {relay.name} to OFF with 0 seconds delay')
        self.enclosure.relays[relay.id].on(relay.OFF)
        self.state[part]['timer_on'] = False
        if self.__pid is not None:
          print('CLEAR PID')
          self.__pid = None

    self.state['powered'] = on

class terrariumAreaHumidity(terrariumArea):
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

      sensor_values['current'].append(self.setup['watertank_volume']   - (sensor.value - self.setup['watertank_offset']) * volume_per_distance)
      sensor_values['alarm_max'].append(self.setup['watertank_volume'] - (sensor.alarm_min - self.setup['watertank_offset']) * volume_per_distance)
      sensor_values['alarm_min'].append(self.setup['watertank_volume'] - (sensor.alarm_max - self.setup['watertank_offset']) * volume_per_distance)

    for key in sensor_values:
      if 'unit' == key:
        continue

      sensor_values[key] = statistics.mean(sensor_values[key])

    sensor_values['alarm'] = not sensor_values['alarm_min'] <= sensor_values['current'] <= sensor_values['alarm_max']

    return sensor_values