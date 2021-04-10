# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from abc import ABCMeta, abstractmethod
from pathlib import Path
import inspect
from importlib import import_module
import sys
from hashlib import md5

# pip install retry
from retry import retry

from time import time
from datetime import date, datetime, timedelta
import re

from terrariumUtils import terrariumUtils

class terrariumWeatherException(TypeError):
  '''There is a problem with loading a hardware switch. Invalid power switch action.'''

  def __init__(self, message, *args):
    self.message = message
    super().__init__(message, *args)

# https://www.bnmetrics.com/blog/factory-pattern-in-python3-simple-version
class terrariumWeatherAbstract(metaclass=ABCMeta):
  HARDWARE     = None
  NAME         = None
  VALID_SOURCE = None
  INFO_SOURCE  = None

  # Weather data expects temperature in celcius degrees and windspeed in meters per second
  __UPDATE_TIMEOUT = 4 * 60 * 60

  def __init__(self, address, name = '', unit_value_callback = None, trigger_callback = None):
    self._device = {'id'       : None,
                    'address'  : None,
                    'name'     : None,

                    'trigger_callback' : trigger_callback,
                    'unit_callback'    : unit_value_callback,
                    'last_update' : None}

    self._data = {'forecast' : {}}

#    self._device['trigger_callback'] = unit_value_callback
#    self._device['unit_callback'] = trigger_callback

    self.name = name
    self.address = address

  @retry(tries=3, delay=0.5, max_delay=2)
  def update(self):
    if self._device['last_update'] is None or (datetime.now() - self._device['last_update']).total_seconds() > self.__UPDATE_TIMEOUT:
      start = time()
      logger.debug(f'Loading online weather data from source: {self.address}')

      if self._load_data():
        self._device['last_update'] = datetime.now()
        logger.info(terrariumUtils.clean_log_line(f'Loaded new weather data in {time()-start:.3f} seconds.'))
      else:
        logger.error(terrariumUtils.clean_log_line(f'Error loading online weather data! Please check your source address: {self.address}.'))

  def __get_today_data(self):
    now = int(time())
    for timestamp in sorted(self._data['forecast'].keys()):
      if not now > self._data['forecast'][timestamp]['set']:
        return self._data['forecast'][timestamp]

    return None

  @property
  def address(self):
    return self._device['address']

  @property
  def _address(self):
    return [ part.strip() for part in self.address.split(',') ]

  @address.setter
  def address(self, value):
    if value is not None and '' != str(value).strip(', '):
      reload = self.address != str(value).strip(', ')
      self._device['address'] = str(value).strip(', ')
      if reload:
        logger.debug(f'Reloading weather data due to changing weather source to: {self.address}')
        self._device['last_update'] = None
        self.update()

  @property
  def name(self):
    return self._device['name']

  @name.setter
  def name(self, value):
    if value is not None and '' != str(value).strip():
      self._device['name'] = str(value).strip()

  @property
  def sunrise(self):
    data = self.__get_today_data()
    if data is not None:
      return datetime.fromtimestamp(data['rise'])

    return datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

  @property
  def sunset(self):
    data = self.__get_today_data()
    if data is not None:
      return datetime.fromtimestamp(data['set'])

    return datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)

  @property
  def is_day(self):
    return self.sunrise < datetime.now() < self.sunset

  @property
  def forecast(self):
    data = []
    timestamps = sorted(self._data['forecast'].keys())
    now = datetime.now().timestamp()
    for timestamp in timestamps:
      if int(timestamp) >= now:
        data.append({'value' : self._data['forecast'][timestamp]['temp'], 'timestamp' : datetime.fromtimestamp(int(timestamp))})

    return data

  @property
  def location(self):
    return {'city'    : self._data['city'],
            'country' : self._data['country'],
            'geo'     : self._data['geo']}

  @property
  def credits(self):
    return {'text' :  self._data['credits'] , 'url' : self._data['url']}

  @property
  def get_available_types(self):
    return terrariumWeather.get_available_types()

  @abstractmethod
  def _load_data(self):
    pass


# Factory class
class terrariumWeather(object):

  SOURCES = {}

  # Start dynamically loading switches (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
  for file in sorted(Path(__file__).parent.glob('*_weather.py')):
    imported_module = import_module( '.' + file.stem, package='{}'.format(__name__))

    for i in dir(imported_module):
      attribute = getattr(imported_module, i)

      if inspect.isclass(attribute) and attribute != terrariumWeatherAbstract and issubclass(attribute, terrariumWeatherAbstract):
        setattr(sys.modules[__name__], file.stem, attribute)
        SOURCES[attribute.HARDWARE] = attribute

  # Return polymorph sensor....
  def __new__(self, address, name = '', unit_value_callback = None, trigger_callback = None):
    for weather_source in terrariumWeather.SOURCES:
      if re.search(terrariumWeather.SOURCES[weather_source].VALID_SOURCE, address, re.IGNORECASE):
        return terrariumWeather.SOURCES[weather_source](address, name, unit_value_callback, trigger_callback)

    raise terrariumWeatherException('Weather url \'{}\' is not valid! Please check your source'.format(address))

  # Return a list with type and names of supported switches
  @staticmethod
  def get_available_types():
    data = []
    for (hardware_type,weather_source) in terrariumWeather.SOURCES.items():
      if weather_source.NAME is not None:
        data.append({'hardware' : hardware_type, 'name' : weather_source.NAME, 'url' : weather_source.INFO_SOURCE, 'validator' : weather_source.VALID_SOURCE})
    return data