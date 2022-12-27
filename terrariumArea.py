# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from operator import itemgetter
import copy
import datetime
import time

import statistics
import threading

# http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
# https://onion.io/2bt-pid-control-python/
# https://github.com/m-lundberg/simple-pid
from simple_pid import PID

from pony import orm
from terrariumAudio import terrariumAudioPlayer
from terrariumDatabase import Sensor, Playlist, Relay
from terrariumUtils import terrariumCache, terrariumUtils, classproperty

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
      'sensors' : ['co2'],
      'class' : lambda: terrariumAreaCO2
    },

    'conductivity' : {
      'name'    : _('Conductivity'),
      'sensors' : ['conductivity'],
      'class' : lambda: terrariumAreaConductivity
    },

    'fertility' : {
      'name'    : _('Fertility'),
      'sensors' : ['fertility'],
      'class' : lambda: terrariumAreaFertility
    },

    'moisture' : {
      'name'    : _('Moisture'),
      'sensors' : ['moisture','humidity'],
      'class' : lambda: terrariumAreaMoisture
    },

    'ph' : {
      'name'    : _('pH'),
      'sensors' : ['ph'],
      'class' : lambda: terrariumAreaPH
    },
  }

  PERIODS = ['low','high']

  @classproperty
  def available_areas(__cls__):
    data = []
    for (area_type, area) in terrariumArea.__TYPES.items():
      data.append({'type' : area_type, 'name' : area['name'], 'sensors' : area['sensors']})

    return sorted(data, key=itemgetter('name'))

  # Return polymorph area....
  def __new__(cls, area_id, enclosure, area_type, name = '', mode = None, setup = None):
    known_areas = terrariumArea.available_areas

    if area_type not in [area['type'] for area in known_areas]:
      raise terrariumAreaException(f'Area of type {area_type} is unknown.')

    return super(terrariumArea, cls).__new__(terrariumArea.__TYPES[area_type]['class']())

  def __init__(self, area_id, enclosure, type, name, mode, setup):
    if area_id is None:
      area_id = terrariumUtils.generate_uuid()

    self.id   = area_id
    self.type = type
    self.name = name
    self.mode = mode

    self.depends_on = []

    self.enclosure = enclosure

    self.state = {}
    self.load_setup(setup)

  def __repr__(self):
    """
    Show the area in a nice way

    Returns:
        string: Area with area type
    """
    return f'{terrariumArea.__TYPES[self.type]["name"]} named {self.name}'


  @property
  def _powered(self):
    powered = None
    for period in self.PERIODS:
      if period not in self.state or self.setup.get(period) is None or len(self.setup[period]['relays']) == 0:
        continue

      powered = powered or self.state[period]['powered']

    logger.debug(f'Area {self} is powered: {powered}')
    return powered

  def _time_table(self):

    def make_time_table(begin, end, on_period = 0, off_period = 0):
      logger.debug(f'Make new time table for {self}. Begin: {begin}, End: {end}, On: {on_period}, Off: {off_period}')
      periods = []
      duration = 0

      now = datetime.datetime.now()

      if not isinstance(begin, datetime.datetime):
        begin = now.replace(hour=begin.hour, minute=begin.minute, second=begin.second)

      if not isinstance(end, datetime.datetime):
        end   = now.replace(hour=end.hour,   minute=end.minute,   second=end.second)

      if begin >= end:
        logger.debug(f'Begin time is bigger then end time (swap). Add 24 hours to end time (next day) {self}')
        end += datetime.timedelta(hours=24)

      if now < end - datetime.timedelta(hours=24):
        logger.debug(f'Current time should be running previous day. Period is upcoming. Use previous day by subtracting 24 hours {self}')
        begin -= datetime.timedelta(hours=24)
        end   -= datetime.timedelta(hours=24)
      elif now > end:
        logger.debug(f'Current time past end. Period is pasted. Use next day by adding 24 hours {self}')
        begin += datetime.timedelta(hours=24)
        end   += datetime.timedelta(hours=24)

      if 0 == on_period and 0 == off_period:
        logger.debug(f'Area {self} is full period usage')
        periods.append((int(begin.timestamp()), int(end.timestamp())))
        duration += periods[-1][1] - periods[-1][0]

      else:
        logger.debug(f'Area {self} has different periods')
        while begin < end:
          # The 'on' period is to big for the rest of the total timer time. So reduce it to the max left time
          if (begin + datetime.timedelta(seconds=on_period)) > end:
            on_period = (end - begin).total_seconds()

          # Add new entry int he time table
          periods.append((int(begin.timestamp()), int((begin + datetime.timedelta(seconds=on_period)).timestamp())))
          duration += periods[-1][1] - periods[-1][0]

          # Increase the start time with the on and off duration for the next round
          begin += datetime.timedelta(seconds=on_period + off_period)

      data = {
        'periods'  : periods,
        'duration' : duration
      }
      logger.debug(f'New time table for {self}')
      logger.debug(data)

      return data

    timetable = {}
    if 'main_lights' == self.mode:
      # We copy the timetable from the area with the toggle 'main lights' on. We follow that area its timetable
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

      sunrise = self.enclosure.weather.sunrise if 'weather' == self.mode else self.enclosure.weather.sunset - datetime.timedelta(hours=24)
      sunset  = self.enclosure.weather.sunset  if 'weather' == self.mode else self.enclosure.weather.sunrise

      next_sunrise = self.enclosure.weather.next_sunrise if 'weather' == self.mode else self.enclosure.weather.next_sunset - datetime.timedelta(hours=24)
      next_sunset  = self.enclosure.weather.next_sunset  if 'weather' == self.mode else self.enclosure.weather.next_sunrise

      max_hours = self.setup['max_day_hours']
      if max_hours != 0 and (sunset - sunrise) > datetime.timedelta(hours=max_hours):
        # On period to long, so reduce the on period by shifting the sunrise and sunset times closer to each other
        seconds_difference = ((sunset - sunrise) - datetime.timedelta(hours=max_hours)) / 2
        sunrise += seconds_difference
        sunset  -= seconds_difference

      if max_hours != 0 and (next_sunset - next_sunrise) > datetime.timedelta(hours=max_hours):
        # On period to long, so reduce the on period by shifting the sunrise and sunset times closer to each other
        seconds_difference = ((next_sunset - next_sunrise) - datetime.timedelta(hours=max_hours)) / 2
        next_sunrise += seconds_difference
        next_sunset  -= seconds_difference

      min_hours = self.setup['min_day_hours']
      if min_hours != 0 and (sunset - sunrise) < datetime.timedelta(hours=min_hours):
        # On period to short, so extend the on period by shifting the sunrise and sunset times away from to each other
        seconds_difference = (datetime.timedelta(hours=min_hours) - (sunset - sunrise)) / 2
        sunrise -= seconds_difference
        sunset  += seconds_difference

      if min_hours != 0 and (next_sunset - next_sunrise) < datetime.timedelta(hours=min_hours):
        # On period to short, so extend the on period by shifting the sunrise and sunset times away from to each other
        seconds_difference = (datetime.timedelta(hours=min_hours) - (next_sunset - next_sunrise)) / 2
        next_sunrise -= seconds_difference
        next_sunset  += seconds_difference

      shift_hours = self.setup['shift_day_hours']
      if shift_hours != 0:
        # Shift the times back or forth...
        sunrise += datetime.timedelta(hours=shift_hours)
        sunset  += datetime.timedelta(hours=shift_hours)

        next_sunrise += datetime.timedelta(hours=shift_hours)
        next_sunset  += datetime.timedelta(hours=shift_hours)

      # Default day and night schedule:
      timetable['day']   = make_time_table(sunrise, sunset)
      timetable['night'] = make_time_table(sunset, next_sunrise)

      # Pick the next day
      if datetime.datetime.now() > sunset:
        timetable['day'] = make_time_table(next_sunrise, next_sunset)

      # Night is still active till sunrise
      if datetime.datetime.now() < sunrise:
        timetable['night'] = make_time_table(sunset - datetime.timedelta(hours=24), sunrise)

    elif 'timer' == self.mode:
      for period in self.PERIODS:
        if period not in self.setup:
          continue

        begin      = datetime.time.fromisoformat(self.setup[period]['begin'])
        end        = datetime.time.fromisoformat(self.setup[period]['end'])
        on_period  = max(0.0,self.setup[period]['on_duration'])  * 60.0
        off_period = max(0.0,self.setup[period]['off_duration']) * 60.0

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

    self.depends_on = self.setup.get('depends_on',[])
    self.ignore_low_alarm  = False
    self.ignore_high_alarm = False

    try:
      self.ignore_low_alarm = bool(self.setup['low']['ignore_low'])
    except Exception:
      self.ignore_low_alarm  = False

    try:
      self.ignore_high_alarm = bool(self.setup['high']['ignore_high'])
    except Exception:
      self.ignore_high_alarm = False

    self.low_deviation  = self.setup.get('deviation_low_alarm',  0.0)
    self.low_deviation  = 0.0 if not terrariumUtils.is_float(self.low_deviation)  else float(self.low_deviation)
    self.high_deviation = self.setup.get('deviation_high_alarm', 0.0)
    self.high_deviation = 0.0 if not terrariumUtils.is_float(self.high_deviation) else float(self.high_deviation)

    float_values = ['max_day_hours','min_day_hours','shift_day_hours']
    for float_value in float_values:
      self.setup[float_value] = self.setup.get(float_value, 0.0)
      self.setup[float_value] = 0.0 if not terrariumUtils.is_float(self.setup[float_value]) else float(self.setup[float_value])

    for period in self.PERIODS:

      # Clean up parts that do not have relays configured)
      if period in self.setup and len(self.setup[period]['relays']) == 0:
        del(self.setup[period])
        continue

      # With version 4.6.0 we get also empty string fields back. So we have to make sure that the fields in the list below are all float values
      float_values = ['on_duration','off_duration','settle_time','power_on_time','alarm_threshold']
      for float_value in float_values:
        self.setup[period][float_value] = self.setup[period].get(float_value, 0.0)
        self.setup[period][float_value] = 0.0 if not terrariumUtils.is_float(self.setup[period][float_value]) else float(self.setup[period][float_value])

      self.setup[period]['tweaks'] = {}

      if period not in self.state:
        self.state[period] = {}
        self.state[period]['last_powered_on'] = datetime.datetime(1970,1,1).timestamp()

      self.state[period]['powered'] = self.relays_state(period)
      self.state[period]['alarm_count'] = 0

    if 'sensors' != self.mode:
      self._time_table()

    # Setup variation data
    if self.setup.get('variation'):
      self._setup_variation_data()

    self.state['powered'] = self._powered

  def _setup_variation_data(self):
    self.state['variation'] = {
        'active'   : len(self.setup['sensors']) > 0,
        'dynamic'  : False,
        'external' : False,
        'script'   : False,
        'weather'  : False,
        'offset'   : float(0),
        'source'   : None,
        'periods'  : []
      }

    variation_data = copy.deepcopy(self.setup.get('variation',[]))
    if len(variation_data) == 0:
      return

    if variation_data[0]['when'] in ['script','external','weather']:
      try:
        self.state['variation']['offset'] = float(variation_data[0]['offset'])
      except Exception as ex:
        # Not a valid float, so use default 0
        logger.debug(f'Invalid variation offset value {variation_data[0]["offset"]}: {ex}')

      self.state['variation'][variation_data[0]['when']] = True
      if 'weather' != variation_data[0]['when']:
        self.state['variation']['source'] = variation_data[0]['source']

      if 'external' == variation_data[0]['when']:
        self.__external_cache = terrariumCache()

      variation_data = []

    for variation in variation_data:
      periods = len(self.state['variation']['periods'])

      if 'at' == variation.get('when'):
        # Format datetime object to a time object

        # TODO: Need to check if this will interfere with utc timestamps from history...
        period_timestamp = datetime.datetime.fromtimestamp(int(variation.get('period'))).strftime('%H:%M')

      elif 'after' == variation.get('when'):
        # !! UNTESTED !!
        if periods == 0:
          # We need main lights on starting time....
          self.state['variation']['dynamic'] = True

        else:
          # We need the previous period start time and adding the 'after' period duration
          period_timestamp = datetime.time.fromisoformat(self.state['variation']['periods'][periods-1]['start'])
          period_timestamp = datetime.datetime.now().replace(hour=period_timestamp.hour, minute=period_timestamp.minute) + datetime.timeldeta(minute=int(variation.get('period')))
          period_timestamp = period_timestamp.strftime('%H:%M')

      if periods > 0:
        # We have at least 1 item so we need to update the previous entry with the new end time and value
        self.state['variation']['periods'][periods-1]['end']       = period_timestamp
        self.state['variation']['periods'][periods-1]['end_value'] = str(variation.get('value'))

      self.state['variation']['periods'].append({
        'start'       : period_timestamp,
        'end'         : '23:59',    # By default, we stop at the end of the day
        'start_value' : str(variation.get('value')),
        'end_value'   : str(variation.get('value')), # This will be overwritten by the next value to get a nice change during the period
      })

  def _is_timer_time(self, period):
    if period not in self.setup or 'timetable' not in self.setup[period]:
      logger.debug(f'Area {self} does not have a timer table')
      return False

    now = int(datetime.datetime.now().timestamp())
    for time_schedule in self.setup[period]['timetable']:
      if now < time_schedule[0]:
        logger.debug(f'Area {self} is not time yet. Period has to start first.')
        return False

      elif time_schedule[0] <= now < time_schedule[1]:
        logger.debug(f'Area {self} is in period, so toggle on: {time_schedule[0]} <= {now} <= {time_schedule[1]}')
        return True

    logger.debug(f'Area {self} does not know if it is time.... Should update new timetable for next day?')
    return None

  def _update_variation(self):
    # !! This variation updates will interfere with the 'day/night difference' setting !!
    if ('variation' not in self.state) or (not self.state['variation']['active']):
      return

    # Get the current time in minutes
    now = datetime.datetime.now().time()
    # Loop over the periods to find the current period
    period = None
    if self.state['variation']['script'] or self.state['variation']['external']:
      value = None

      if self.state['variation']['script']:
        value = float(terrariumUtils.get_script_data(self.state['variation']['source'])) + self.state['variation']['offset']

      elif self.state['variation']['external']:
        # Here we get data from an external source. We cache this data for 10 minutes
        cache_key = f'{self.id}_external'
        value = self.__external_cache.get_data(cache_key)
        if value is None:
          start = time.time()
          value = float(terrariumUtils.get_remote_data(self.state['variation']['source'])) + self.state['variation']['offset']
          if value is not None:
            unit = self.enclosure.engine.units[self.state["sensors"]["unit"]]
            self.__external_cache.set_data(cache_key, value, 10 * 60)
            logger.info(f'Updated external source variation data with value: {value}{unit} in {time.time() - start:.2f} seconds')
          else:
            logger.error('Could not load data from external source! Please check your settings.')

      if value is not None:
        period = {
          'start'       : (datetime.datetime.now() - datetime.timedelta(minutes=2)).time(),
          'end'         : (datetime.datetime.now() + datetime.timedelta(minutes=2)).time(),   # By default, we stop at the end of the day
          'start_value' : str(value),
          'end_value'   : str(value), # This will be overwritten by the next value to get a nice change during the period
        }

    elif self.state['variation']['weather']:

      weather_current_source = None
      if self.type in ['heating','cooling']:
        weather_current_source = 'temperature'
      elif self.type in ['humidity']:
        weather_current_source = 'humidity'

      if weather_current_source is None:
        return

      current_timestamp = int( (datetime.datetime.now()-datetime.timedelta(hours=24)).timestamp() )
      for counter, history in enumerate(self.enclosure.engine.weather.history):
        if current_timestamp <= history["timestamp"] + time.timezone:
          period = {
            'start'       : datetime.datetime.fromtimestamp(int(self.enclosure.engine.weather.history[counter-1]["timestamp"] + time.timezone)),
            'end'         : datetime.datetime.fromtimestamp(int(history["timestamp"] + time.timezone)),
            'start_value' : str(self.enclosure.engine.weather.history[counter-1][weather_current_source]),
            'end_value'   : str(history[weather_current_source]),
          }
          break

    else:
      for item in self.state['variation']['periods']:
        if now >= datetime.time.fromisoformat(item['start']) and now < datetime.time.fromisoformat(item['end']):
          # Fond the right period, so save and stop looping
          period = copy.copy(item)
          period['start'] = datetime.time.fromisoformat(item['start'])
          period['end']   = datetime.time.fromisoformat(item['end'])
          break

    if period is None:
      # No valid period found, so we are done!
      return

    # Get the current 'wanted' average value based on the alarm min and max values
    current_average_value = (self.state['sensors']['alarm_min'] + self.state['sensors']['alarm_max']) / 2.0

    # Convert relative sensor values to absolute values based on the current state.
    # This is done only once when the period starts. Once converted, we keep the absolute values
    # !! UNTESTED !!
    if period['start_value'].startswith('+'):
      period['start_value'] = current_average_value + int(period['start_value'][1:])

    elif period['start_value'].startswith('-'):
      period['start_value'] = current_average_value - int(period['start_value'][1:])

    if period['end_value'].startswith('+'):
      period['end_value'] = current_average_value + int(period['end_value'][1:])

    elif period['end_value'].startswith('-'):
      period['end_value'] = current_average_value+ - int(period['end_value'][1:])


    # Start calculation
    # Get the total duration of the period in seconds
    period_duration   = round((datetime.datetime.now().replace(hour=period['end'].hour, minute=period['end'].minute) - datetime.datetime.now().replace(hour=period['start'].hour, minute=period['start'].minute) ).total_seconds())
    # Get the total difference that needs to change during the period
    period_difference = float(period['end_value']) - float(period['start_value'])
    # How far are we in this period in seconds
    period_duration_done = round((datetime.datetime.now().replace(hour=now.hour, minute=now.minute) - datetime.datetime.now().replace(hour=period['start'].hour, minute=period['start'].minute)).total_seconds())
    # Calculate the wanted average based on the start period value and the time elapsed * sensor difference/second
    wanted_average_value = float(period['start_value']) + (float(period_duration_done) * float(period_difference / period_duration))
    # Get the difference between the actual current average and the wanted average rounded at .1
    sensor_diff = round(wanted_average_value - current_average_value,1)

    if sensor_diff != 0.0:
      # Change every sensor its min max alarm values with `sensor_diff` change
      with orm.db_session():
        for sensor in Sensor.select(lambda s: s.id in self.setup['sensors']):
          sensor.alarm_min += sensor_diff
          sensor.alarm_max += sensor_diff
          unit = self.enclosure.engine.units[self.state["sensors"]["unit"]]
          logger.info(f'Variation change {sensor.type} sensor \'{sensor.name}\' for area \'{self.name}\'. New values min: {sensor.alarm_min:.2f}{unit}, max:{sensor.alarm_max:.2f}{unit}. New average is: {wanted_average_value:.2f}{unit}.')

    # Reload the current sensor values after changing them
    self.state['sensors'] = self.current_value(self.setup['sensors'])

  @property
  def is_day(self):
    light_mode = self.setup.get('day_night_source', '')

    # Base day time on weather information
    if 'weather' == light_mode and self.enclosure.weather is not None:
      return self.enclosure.weather.is_day

    # Else we have to see if we are between the begin and end time of the 'main lights' light area
    if 'lights' == light_mode and self.enclosure.main_lights is not None and self.enclosure.main_lights.mode != 'disabled':
      is_day_time = self.enclosure.main_lights.state['day']['begin'] < int(datetime.datetime.now().timestamp()) < self.enclosure.main_lights.state['day']['end']
      return is_day_time

    # Default day period is from 07:00 till 19:00
    return 700 < int(time.strftime('%H%M')) < 1900

  def update(self, read_only = False):
    if self.mode == 'disabled':
      # Make it readonly, so sensors and relay changes are still shown
      read_only = True

    start = time.time()

    light_state = ('on'     if self.enclosure.lights_on   else 'off')
    door_state  = ('closed' if self.enclosure.door_closed else 'open')

    old_is_day = self.state['is_day']
    self.state['is_day'] = self.is_day

    if 'variation' in self.state and self.state['variation']['dynamic']:
      if old_is_day != self.state['is_day'] or int(datetime.datetime.now().strftime("%H%M")) % 400 == 0:
        # logger.info('Updating variation data based on day/night change or modulo 400')
        self._setup_variation_data()

    if 'sensors' in self.setup and len(self.setup['sensors']) > 0:
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

      # If there are variations on the alarm values, update them here
      if not read_only:
        self._update_variation()

      # Deviation calculation is done in current_value() function
      if self.ignore_low_alarm:
        # Use the max alarm value to changing the relays
        self.state['sensors']['alarm_low']  = self.state['sensors']['current'] < self.state['sensors']['alarm_max']
      else:
        # Normal state
        self.state['sensors']['alarm_low']  = self.state['sensors']['current'] < self.state['sensors']['alarm_min']

      if self.ignore_high_alarm:
        # Use the min alarm value to changing the relays
        self.state['sensors']['alarm_high'] = self.state['sensors']['current'] > self.state['sensors']['alarm_min']
      else:
        self.state['sensors']['alarm_high'] = self.state['sensors']['current'] > self.state['sensors']['alarm_max']

    # If the depending area is in alarm state, we cannot toggle this area and all the relays should be shutdown
    depends_on_alarm = False
    for area in self.depends_on:
      if area in self.enclosure.areas and self.enclosure.areas[area].state.get('sensors'):

        depends_on_alarm = depends_on_alarm or self.enclosure.areas[area].state['sensors']['alarm']
        if depends_on_alarm:
          unit_value = self.enclosure.engine.units[self.enclosure.areas[area].state['sensors']['unit']]
          logger.info(f'Depending area {self.enclosure.areas[area].name} is in alarm state for area {self}. Current: {self.enclosure.areas[area].state["sensors"]["current"]:.2f}{unit_value}')

          for period in self.PERIODS:
            if period in self.setup and self.relays_state(period):
              logger.info(f'Toggle down the power for period {period} due to depending area {self.enclosure.areas[area].name} alarm state.')
              self.relays_toggle(period,False)

          break

    for period in self.PERIODS:
      if period not in self.setup:
        continue

      if read_only:
        self.state[period]['powered'] = self.relays_state(period)
        continue

      # Set the lights state. Default True
      light_state_ok = True
      if 'light_status' in self.setup[period] and self.setup[period]['light_status'] not in ['ignore','']:
        # Change the lights state based on the current state and requested state. False when not equal
        light_state_ok = self.setup[period]['light_status'] == light_state

      # Set the doors state. Default True
      door_state_ok = True
      if 'door_status' in self.setup[period] and self.setup[period]['door_status'] not in ['ignore','']:
        # Change the doors state based on the current state and requested state. False when not equal
        door_state_ok = self.setup[period]['door_status'] == door_state

      # First check: Shutdown power when power is on and either the lights or doors are in wrong state. Despite 'mode'
      if not self.relays_state(period,False) and not (light_state_ok and door_state_ok and (not depends_on_alarm)):
        # Power is on, but either the lights or doors are in wrong state. Power down now.
        logger.info(f'Forcing down the {period} power for area {self} because either the lights({"OK" if light_state_ok else "ERROR"}), doors({"OK" if door_state_ok else "ERROR"}) or depending area ({"OK" if not depends_on_alarm else "ERROR"}) are in an invalid state.')
        self.relays_toggle(period,False)
        # And ignore the rest....
        continue

      if 'sensors' != self.mode:
        # Weather(inverse) and timer mode
        toggle_relay = self._is_timer_time(period)
        logger.debug(f'Need to toggle the relays for {self} period {period}? {toggle_relay}')

        if toggle_relay is None:
          logger.info(f'Refreshing timer table for {self} period: {period}')
          self._time_table()
          toggle_relay = False

        if toggle_relay is True and 'sensors' in self.setup and len(self.setup['sensors']) > 0:
          # We are in timer mode. But when there are sensors configured, they act as a second check
          # If there is NOT an alarm with the period name, then skip the toggle action.
          if self.state['sensors'][f'alarm_{period}'] is not True:
            logger.info(f'Relays for area {self} at period {period} are not switched because the additional sensors are at value: {self.state["sensors"]["current"]:.2f}{self.enclosure.engine.units[self.state["sensors"]["unit"]]}.')
            continue
      else:
        # Sensor mode only toggle ON when alarms are triggered (True).
        toggle_relay = self.state['sensors'][f'alarm_{period}']
        if toggle_relay is False:
          other_alarm = self.state['sensors'][f'alarm_{("low" if period == "high" else "high")}']
          toggle_relay = False if other_alarm else None

      if toggle_relay is True and not self.relays_state(period): #self.state[period]['powered']:

        if not light_state_ok:
          logger.info(f'Relays for {self} period {period} are not switched because the lights are {light_state} while {self.setup[period]["light_status"]} is requested.')
          continue

        if not door_state_ok:
          logger.info(f'Relays for {self} period {period} are not switched because the door is {door_state} while {self.setup[period]["door_status"]} is requested.')
          continue

        if depends_on_alarm:
          logger.info(f'Relays for {self} period {period} are not switched because one of the depending areas are in an alarm state.')
          continue

        time_elapsed = abs(int(datetime.datetime.now().timestamp()) - self.state[period]['last_powered_on'])
        if time_elapsed <= self.setup[period]['settle_time']:
          logger.info(f'Relays for {self} period {period} are not switched because we have to wait for {self.setup[period]["settle_time"]-time_elapsed} more seconds of the total settle time of {self.setup[period]["settle_time"]} seconds.')
          continue

        other_period = list(self.setup.keys())
        other_period.remove(period)
        if 1 == len(other_period):
          other_period = other_period[0]
          time_elapsed = abs(int(datetime.datetime.now().timestamp()) - self.state[other_period]['last_powered_on'])
          if time_elapsed <= self.setup[other_period]['settle_time']:
            logger.info(f'Relays for {self} period {period} are not switched because of the other period {other_period} settle time. We have to wait for {self.setup[other_period]["settle_time"]-time_elapsed} more seconds of the total settle time of {self.setup[other_period]["settle_time"]} seconds.')
            continue

        if self.state[period]['alarm_count'] < self.setup[period]['alarm_threshold']:
          logger.info(f'The alarm counter ({self.state[period]["alarm_count"]}) for area {self} for alarm {period} is lower than the threshold ({self.setup[period]["alarm_threshold"]}). Skip this round.')
          self.state[period]['alarm_count'] += 1
          continue

        self.relays_toggle(period,True)
        self.state[period]['alarm_count'] = 0
        self.state[period]['last_powered_on'] = int(datetime.datetime.now().timestamp())

        if self.setup[period]['power_on_time'] > 0.0:
          self.state[period]['timer_on'] = True
          threading.Timer(self.setup[period]['power_on_time'], self.relays_toggle, [period, False]).start()

      elif toggle_relay is False and not self.relays_state(period, False) and not self.state[period].get('timer_on',False):
        self.relays_toggle(period,False)

      # else:
      #   # Just update the current relay state
      #   print('No area action.. so NO update....')
      #   #self.state[period]['powered'] = self.relays_state(period)

    self.state['powered'] = self._powered
    self.state['last_update'] = int(datetime.datetime.now().timestamp())

    logger.info(f'Updated area {self} in {self.mode} mode at enclosure {self.enclosure.name} in {time.time()-start:.2f} seconds.')
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
        sensor_values['unit'] = sensor.type
        if sensor.value is None:
          # Broken sensor, so ignore it
          continue

        sensor_values['current'].append(sensor.value)
        sensor_values['alarm_max'].append(sensor.alarm_max)
        sensor_values['alarm_min'].append(sensor.alarm_min)

    for key in sensor_values:
      if 'unit' == key:
        continue

      if len(sensor_values[key]) == 0:
        sensor_values[key] = 0
      else:
        sensor_values[key] = statistics.mean(sensor_values[key])

    sensor_values['alarm_min'] += self.low_deviation
    sensor_values['alarm_max'] += self.high_deviation
    sensor_values['alarm'] = not sensor_values['alarm_min'] <= sensor_values['current'] <= sensor_values['alarm_max']

    return sensor_values

  def relays_state(self, part, state = True):

    relay_states = []
    for relay in self.setup[part]['relays']:

      if relay not in self.enclosure.relays:
        continue

      if state:
        relay_states.append(self.enclosure.relays[relay].is_on())
      else:
        relay_states.append(self.enclosure.relays[relay].is_off())

    return all(relay_states)

  def relays_toggle(self, part, on):
    logger.info(f'Toggle the relays for area {self} part {part} to state {("on" if on else "off")}.')

    relays = []
    with orm.db_session():
      relays = orm.select(r.id for r in Relay if r.id in self.setup[part]['relays'] and not r.manual_mode)[:]

    for relay in relays:
      if relay not in self.enclosure.relays:
        continue

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
      logger.info(f'Set the relay {relay.name} to {relay.ON if action else relay.OFF}')
      self.enclosure.relays[f'{relay.id}'].on(relay.ON if action else relay.OFF)

  def stop(self):
    logger.info(f'Stopped Area {self}')


class terrariumAreaLights(terrariumArea):

  PERIODS = ['day','night']

  def load_setup(self, data):
    super().load_setup(data)

    # Load extra tweaks
    for period in self.PERIODS:
      if period not in self.setup:
        continue

      if data[period].get('tweaks', None) in [None, {}]:
        # Legacy tweaks loading
        for relay_id in self.setup[period]['relays']:
          relay = self.enclosure.relays[relay_id]

          extra_tweaks = self.setup[period].get(('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'on_' + relay.id, None)
          if extra_tweaks is None:
            continue

          self.setup[period]['tweaks'][f'{relay.id}'] = {
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
            if len(values) == 1:
              values = [0,values[0]]

            self.setup[period]['tweaks'][f'{relay.id}']['on']['delay']    = float(values[0]) * 60.0
            self.setup[period]['tweaks'][f'{relay.id}']['on']['duration'] = float(values[1]) * 60.0

            values = self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'off_' + relay.id].split(',')
            if len(values) == 1:
              values = [0,values[0]]

            self.setup[period]['tweaks'][f'{relay.id}']['off']['delay']    = float(values[0]) * 60.0
            self.setup[period]['tweaks'][f'{relay.id}']['off']['duration'] = float(values[1]) * 60.0
          else:
            value = self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'on_' + relay.id]
            self.setup[period]['tweaks'][f'{relay.id}']['on']['delay']  = float(value) * 60.0
            value = self.setup[period][('dimmer_duration_' if relay.is_dimmer else 'relay_delay_') + 'off_' + relay.id]
            self.setup[period]['tweaks'][f'{relay.id}']['off']['delay'] = float(value) * 60.0
      else:
        # New tweaks loading
        tweaks = {}
        for relay in data[period]['tweaks']:
          # Input is either a number, or a string with two numbers and a comma separator
          # We cast value to a string, split it on ',' and convert the values back to integers
          # We have now an array with 1 or 2 integers
          value_on  = [int(value) for value in str(relay['on']).split(',')]
          value_off = [int(value) for value in str(relay['off']).split(',')]
          tweaks[f'{relay["id"]}'] = {
            'on' : {
              'delay'    : 0 if len(value_on) == 0 else float(value_on[0]) * 60.0,
              'duration' : 0 if len(value_on) == 1 else float(value_on[1]) * 60.0
            },
            'off' : {
              'delay'    : 0 if len(value_off) == 0 else float(value_off[0]) * 60.0,
              'duration' : 0 if len(value_off) == 1 else float(value_off[1]) * 60.0
            }
          }

        self.setup[period]['tweaks'] = tweaks

    # Reset the powered on state if the dimmers are not at max value. So the dimmer will continue where it left off
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

    duration = 0
    delay = 0

    try:
      tweaks = self.setup[part]['tweaks'][f'{relay.id}']['on' if action else 'off']
      duration = tweaks['duration']
      delay = tweaks['delay']
    except Exception as ex:
      logger.debug(f'Could not find the tweaks: {relay.id}, state {"on" if action else "off"}, error: {ex}')

    if (relay.ON if action else relay.OFF) != relay.state and self.state[part]['powered'] == action:
      delay = 0

    if relay.is_dimmer:
      step_size = duration / (relay.ON - relay.OFF)
      duration = step_size * abs((relay.ON if action else relay.OFF) - relay.state)
      old_state = relay.state
      action_ok = self.enclosure.relays[f'{relay.id}'].on(relay.ON if action else relay.OFF, duration=duration, delay=delay)

      if action_ok:
        if action:
          logger.info(f'Start the dimmer {relay.name} from {old_state}% to {relay.ON}% in {duration:.2f} seconds with a delay of {delay/60:.2f} minutes')
        else:
          logger.info(f'Stopping the dimmer {relay.name} from {old_state}% to {relay.OFF}% in {duration:.2f} seconds with a delay of {delay/60:.2f} minutes')

    else:
      action_ok = self.enclosure.relays[f'{relay.id}'].on(relay.ON if action else relay.OFF, delay=delay)

      if action_ok:
        logger.info(f'Set the relay {relay.name} to {relay.ON if action else relay.OFF} with a delay of {delay/60:.2f} minutes')

class terrariumAreaHeater(terrariumArea):

  def __init__(self, id, enclosure, type, name, mode, setup):
    self.__dimmers = {}
    super().__init__(id, enclosure, type, name, mode, setup)

  @property
  def _powered(self):
    powered = None
    for period in self.PERIODS:
      if period not in self.state or len(self.setup[period]['relays']) == 0:
        continue

      powered = powered or (not self.relays_state(period, False))

    return powered

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

  def update(self, read_only = False):
    super().update(read_only)

    if not read_only and self.mode != 'disabled' and len(self.__dimmers) > 0:
      sensor_values  = self.current_value(self.setup['sensors'])
      sensor_average = float(sensor_values['alarm_min'] + sensor_values['alarm_max']) / 2.0

      for period in self.PERIODS:
        if period not in self.setup:
          continue

        for relay in self.setup[period]['relays']:
          relay = self.enclosure.relays[relay]
          if relay.id in self.__dimmers:

            self.__dimmers[f'{relay.id}'].setpoint = sensor_average
            self.__dimmers[f'{relay.id}'].output_limits = (relay.OFF,relay.ON)

            dimmer_value = round(self.__dimmers[f'{relay.id}'](sensor_values['current']))
            logger.info(f'Updating {relay} to value {dimmer_value}%. Current: {sensor_values["current"]:.2f}{self.enclosure.engine.units[sensor_values["unit"]]}, target: {sensor_average:.2f}{self.enclosure.engine.units[sensor_values["unit"]]}')
            self.enclosure.relays[f'{relay.id}'].on(dimmer_value)

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
          unit               = self.enclosure.engine.units[sensor_values['unit']]

          logger.info(f'Start the dimmer {relay} in PID modus to go to average value {sensor_average}{unit} with a settle timeout of {settle_time} seconds.')
          self.__dimmers[f'{relay.id}'] = PID(heating_or_cooling * 1, heating_or_cooling * 0.1, heating_or_cooling * 0.05,
                                        setpoint=sensor_average,
                                        sample_time=settle_time,
                                        output_limits=(relay.OFF,relay.ON))

          if relay.state > 0:
            dimmer_value = relay.state
            logger.info(f'Restoring old dimmer value {dimmer_value}% for relay {relay}')
            self.__dimmers[f'{relay.id}'].set_auto_mode(True, last_output=dimmer_value)
          else:
            dimmer_value = round(self.__dimmers[f'{relay.id}'](sensor_values['current']))
            logger.info(f'Setting the dimmer {relay} to value {dimmer_value}%. Current value {sensor_values["current"]}{self.enclosure.engine.units[sensor_values["unit"]]}, target of {sensor_average}{self.enclosure.engine.units[sensor_values["unit"]]}')

          self.enclosure.relays[f'{relay.id}'].on(dimmer_value)
        else:
          logger.info(f'Set the relay {relay} to {relay.ON} with 0 seconds delay')
          self.enclosure.relays[f'{relay.id}'].on(relay.ON)

      else:
        logger.info(f'Set the relay {relay} to {relay.OFF} with 0 seconds delay')
        self.enclosure.relays[f'{relay.id}'].on(relay.OFF)
        self.state[part]['timer_on'] = False
        if relay.id in self.__dimmers:
          del(self.__dimmers[f'{relay.id}'])

class terrariumAreaCooler(terrariumAreaHeater):
  pass

class terrariumAreaHumidity(terrariumAreaHeater):
  pass

class terrariumAreaMoisture(terrariumAreaHeater):
  pass

class terrariumAreaCO2(terrariumAreaHeater):
  pass

class terrariumAreaConductivity(terrariumAreaHeater):
  pass

class terrariumAreaFertility(terrariumAreaHeater):
  pass

class terrariumAreaPH(terrariumAreaHeater):
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

      sensor_values[key] = 0 if len(sensor_values[key]) == 0 else statistics.mean(sensor_values[key])

    sensor_values['alarm_min'] += self.low_deviation
    sensor_values['alarm_max'] += self.high_deviation
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

  def relays_state(self, period, state = True):
    # We do not check if the player is actual running. This will cause an unwanted repeat functionality
    return period in self.state and self.state[period].get('powered',False)

  def relays_toggle(self, period, on):
    if period not in self.setup:
      return False

    if self.state[period]['powered'] != on:
      logger.info(f'Toggle the player for area {self} period {period} to state {("on" if on else "off")}.')

    if on:
      # As we can only have one player running, we have to make sure that there is not a player still running from the other period
      other_period = copy.copy(self.PERIODS)
      other_period.remove(period)
      other_period = other_period[0]

      if other_period in self.setup and self.state[other_period]['powered']:
        logger.info(f'Forcing to stop the player for area {self} period {other_period} due to period change.')
        self.setup[other_period]['player'].stop()
        self.state[other_period]['powered'] = False

      self.setup[period]['player'].play()

    else:
      self.setup[period]['player'].stop()

    self.state[period]['powered'] = on
    self.state['powered'] = self._powered

  def stop(self):
    for period in self.PERIODS:
      if period not in self.setup:
        continue

      self.setup[period]['player'].stop()
      self.state[period]['powered'] = False
