# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import untangle
import dateutil.parser
import time
import copy
import json
import re

from datetime import datetime, timedelta
from gevent import sleep

from terrariumUtils import terrariumUtils

class terrariumWeatherSource(object):
  TYPE = None
  # Weather data expects temperature in celcius degrees and windspeed in meters per second
  UPDATE_TIMEOUT = 4 * 60 * 60

  def __init__(self, source, temperature_indicator, windspeed_indicator, callback = None):
    logger.info('Initialising \'{}\' weather object'.format(self.get_type()))
    self.source   = None
    # Callback functions to engine settings
    self.temperature_indicator = temperature_indicator
    self.windspeed_indicator = windspeed_indicator
    self.callback = callback

    self.__last_update = 0
    self.__running = False

    self.location = {'city' : '', 'country' : '', 'geo' : {'lat' : 0, 'long' : 0}}
    self.credits  = {'text' : '', 'url' : ''}
    self.sun      = {'rise' : 0, 'set' : 0}
    self.hour_forecast = {}
    self.week_forecast = {}

    self.set_source(source,True)

  def __update_weather_icons(self):
    for forecast in self.hour_forecast:
      self.hour_forecast[forecast]['icon'] = self.__get_weather_icon(self.hour_forecast[forecast]['weather'])

    for forecast in self.week_forecast:
      self.week_forecast[forecast]['icon'] = self.__get_weather_icon(self.week_forecast[forecast]['weather'])

  def __get_weather_icon(self,weathertype):
    weathertype = weathertype.lower().replace(' ','',10)

    icons = {'clearsky' : 'clear_' + ('day' if self.is_day() else 'night'),
             'fair' : 'clear_' + ('day' if self.is_day() else 'night'),
             'clear' : 'clear_' + ('day' if self.is_day() else 'night'),

             'partlycloudy' : 'partly_cloudy_' + ('day' if self.is_day() else 'night'),
             'mostlycloudy' : 'partly_cloudy_' + ('day' if self.is_day() else 'night'),
             'brokenclouds' : 'partly_cloudy_' + ('day' if self.is_day() else 'night'),
             'fewclouds' : 'partly_cloudy_' + ('day' if self.is_day() else 'night'),

             'cloudy' : 'cloudy',
             'scatteredclouds' : 'cloudy',
             'overcast' : 'cloudy',
             'overcastclouds' : 'cloudy',

             'lightrainshowers' : 'rain',
             'lightrain' : 'rain',
             'rain' : 'rain',
             'chanceofrain' : 'rain',
             'moderaterain' : 'rain',
             'rainshowersandthunder' : 'rain',

             'sleet' : 'sleet',
             'sleetshowers' : 'sleet',
             'rainshowers' : 'sleet',
             'heavyrainshowers' : 'sleet',
             'heavyrain' : 'sleet',
             'chanceofathunderstorm' : 'sleet',
             'thunderstorm' : 'sleet',
             'lightsleet' : 'sleet',
             'lightsleetshowers' : 'sleet',
             'heavysleet' : 'sleet',

             'fog' : 'fog',

             'lightsnowshowers' : 'snow',
             'snowshowers' : 'snow',
             'lightsnow' : 'snow',
             'heavysnow' : 'snow',
             'snow' : 'snow'
           }

    if weathertype in icons:
      return icons[weathertype]
    else:
      logger.warn('Missing skycon %s' % weathertype,)

    return None

  def update(self,force = False):
    starttime = time.time()
    if force or not self.__running and ((int(starttime) - self.get_last_update()) >= terrariumWeatherSource.UPDATE_TIMEOUT):
      self.__running = True
      logger.debug('Start getting new {} weather data from location: \'{}\''.format(self.get_type(),self.get_source()))
      # Some default sun rise and sun set when there no valid weather data. This is the bear minimum to keep the software running
      self.sun['rise'] = int(datetime.now().replace(hour=8, minute=0, second=0).strftime('%s'))
      self.sun['set']  = self.sun['rise'] + (12 * 60 * 60)

      load_counter = 0
      while load_counter < 3 and not self.load_data():
        load_counter +=1
        sleep(1)

      self.__update_weather_icons()
      logger.info('Done loading {} weather data in {} seconds. Hour forcecast items: {}, week forecast items: {}.'.format(self.get_type(),
                                                                                                                          time.time()-starttime,
                                                                                                                          len(self.get_forecast('day')),
                                                                                                                          len(self.get_forecast('all'))))
      self.__running = False
      self.__last_update = int(starttime)

    # Update hourly forecast for today
    now = int(starttime)
    send_message = False
    for period in sorted(self.hour_forecast.keys(),key=int):
      if now > self.hour_forecast[period]['to']:
        del(self.hour_forecast[period])
        send_message = True
      elif now < self.hour_forecast[period]['to']:
        break

    # Update week forecast
    for period in sorted(self.week_forecast.keys(),key=int):
      if now > self.week_forecast[period]['to']:
        del(self.week_forecast[period])
        send_message = True
      elif now < self.week_forecast[period]['to']:
        break

    # Send message when there where changes
    if send_message:
      self.callback(socket=True)

  def load_data(self):
    # Here custom code per type should be created
    return True

  def get_data(self):
    data = {'city' : self.location,
            'sun' : self.sun,
            'day' : self.is_day(),
            'windspeed' : self.get_windspeed_indicator(),
            'temperature_indicator' : self.get_temperature_indicator(),
            'hour_forecast' : [],
            'week_forecast' : [],
            'credits': self.credits}

    for period in sorted(self.hour_forecast.keys(),key=int):
      item = copy.deepcopy(self.hour_forecast[period])
      item['wind_speed'] *= (3.6 if self.get_windspeed_indicator() == 'kmh' else 1.0)

      if self.get_temperature_indicator() == 'F':
        item['temperature'] = terrariumUtils.to_fahrenheit(item['temperature'])
      elif self.get_temperature_indicator() == 'K':
        item['temperature'] = terrariumUtils.to_kelvin(item['temperature'])

      data['hour_forecast'].append(item)

    for period in sorted(self.week_forecast.keys(),key=int):
      item = copy.deepcopy(self.week_forecast[period])
      item['wind_speed'] *= (3.6 if self.get_windspeed_indicator() == 'kmh' else 1.0)

      if self.get_temperature_indicator() == 'F':
        item['temperature'] = terrariumUtils.to_fahrenheit(item['temperature'])
      elif self.get_temperature_indicator() == 'K':
        item['temperature'] = terrariumUtils.to_kelvin(item['temperature'])

      data['week_forecast'].append(item)

    return data

  def get_config(self):
    return {'location' : self.get_source()}

  def get_type(self):
    return terrariumWeatherSource.TYPE

  def get_source(self):
    return self.source

  def set_source(self,url,refresh = False):
    self.source = url.replace('http://','https://')
    if refresh:
      self.update(refresh)

    return True

  def get_temperature_indicator(self):
    return self.temperature_indicator()

  def get_windspeed_indicator(self):
    return self.windspeed_indicator()

  def get_sun_rise(self):
    return self.sun['rise']

  def get_sun_set(self):
    return self.sun['set']

  def is_day(self):
    return self.get_sun_rise() < int(time.time()) < self.get_sun_set()

  def is_night(self):
    return not self.is_day()

  def get_city(self):
    return self.location['city']

  def get_country(self):
    return self.location['country']

  def get_geo(self):
    return self.location['geo']

  def get_copyright(self):
    return self.credits

  def get_last_update(self):
    return self.__last_update

  def get_forecast(self,period = 'day'):
    if period == 'day':
      return self.hour_forecast
    else:
      return self.week_forecast

class terrariumWeatherYRno(terrariumWeatherSource):
  TYPE = 'YR.no'
  VALID_SOURCE = '^https?://(www\.)?yr\.no/place/(?P<country>[^/]+)/(?P<provance>[^/]+)/(?P<city>[^/]+/?)?'
  INFO_SOURCE = 'https://www.yr.no/place/[COUNTRY]/[PROVANCE]/[CITY]'

  def load_data(self):
    starttime = time.time()
    logger.info('Update {} data from ONLINE refreshing cache.'.format(self.get_type()))

    xmldata = terrariumUtils.get_remote_data(self.source.strip('/') + '/forecast_hour_by_hour.xml')
    if xmldata is not None:
      try:
        xmldata = untangle.parse(xmldata)
      except Exception:
        logger.exception('Error getting online data from {}'.format(self.get_type()))
        return False

      # Parse hour forecast
      # Parse general data information
      self.location['city'] = xmldata.weatherdata.location.name.cdata
      self.location['country'] = xmldata.weatherdata.location.country.cdata
      self.location['geo']['lat'] = float(xmldata.weatherdata.location.location['latitude'])
      self.location['geo']['long'] = float(xmldata.weatherdata.location.location['longitude'])

      self.credits['text'] = xmldata.weatherdata.credit.link['text']
      self.credits['url'] = xmldata.weatherdata.credit.link['url']

      self.sun['rise'] = int(time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['rise']).timetuple()))
      self.sun['set'] = int(time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['set']).timetuple()))

      for forecast in xmldata.weatherdata.forecast.tabular.time:
        forecast_data = { 'from' : int(time.mktime(dateutil.parser.parse(forecast['from']).timetuple())),
                          'to' : int(time.mktime(dateutil.parser.parse(forecast['to']).timetuple())),
                          'weather' : forecast.symbol['name'],
                          'rain' : float(forecast.precipitation['value']),
                          'humidity' : 0.0,
                          'wind_direction' : forecast.windDirection['name'],
                          'wind_speed' : float(forecast.windSpeed['mps']),
                          'temperature' : float(forecast.temperature['value']),
                          'pressure' : float(forecast.pressure['value'])
                        }

        self.hour_forecast[forecast_data['from']] = forecast_data

      # Parse week forecast
      xmldata = terrariumUtils.get_remote_data(self.source.strip('/') + '/forecast.xml')
      if xmldata is not None:
        try:
          xmldata = untangle.parse(xmldata)
        except Exception:
          logger.exception('Error getting online data from {}'.format(self.get_type()))

        for forecast in xmldata.weatherdata.forecast.tabular.time:
          forecast_data = { 'from' : int(time.mktime(dateutil.parser.parse(forecast['from']).timetuple())),
                            'to' : int(time.mktime(dateutil.parser.parse(forecast['to']).timetuple())),
                            'weather' : forecast.symbol['name'],
                            'rain' : float(forecast.precipitation['value']),
                            'humidity' : 0.0,
                            'wind_direction' : forecast.windDirection['name'],
                            'wind_speed' : float(forecast.windSpeed['mps']),
                            'temperature' : float(forecast.temperature['value']),
                            'pressure' : float(forecast.pressure['value'])
                          }
          self.week_forecast[forecast_data['from']] = forecast_data

      else:
        logger.error('Error getting online data from {}'.format(self.get_type()))
    else:
      logger.error('Error getting online data from {}'.format(self.get_type()))
      return False

    return True

  def get_type(self):
    return terrariumWeatherYRno.TYPE

class terrariumWeatherWunderground(terrariumWeatherSource):
  TYPE = 'Wunderground.com'
  VALID_SOURCE = '^https?://api\.wunderground\.com/api/[a-z0-9]{16}/geolookup/astronomy/hourly10day/q/(?P<country>[^/]+)/(?P<city>[^/]+)\.json$'
  INFO_SOURCE = 'https://api.wunderground.com/api/[YOUR_API_KEY]/geolookup/astronomy/hourly10day/q/[COUNTRY]/[CITY].json'

  def load_data(self):
    logger.info('Update {} data from ONLINE refreshing cache.'.format(self.get_type()))
    self.credits['text'] = 'Wunderground weather data'

    parsed_json = terrariumUtils.get_remote_data(self.source)
    if parsed_json is not None:
      # Parse general data information
      self.location['city'] = parsed_json['location']['city']
      self.location['country'] = parsed_json['location']['country_name']
      self.location['geo']['lat'] = float(parsed_json['location']['lat'])
      self.location['geo']['long'] = float(parsed_json['location']['lon'])

      self.credits['url'] = parsed_json['location']['wuiurl']

      now = datetime.now()
      self.sun['rise'] = int(time.mktime(now.replace(hour=int(parsed_json['sun_phase']['sunrise']['hour']),
                                                  minute=int(parsed_json['sun_phase']['sunrise']['minute']),
                                                  second=0).timetuple()))
      now = datetime.now()
      self.sun['set'] = int(time.mktime(now.replace(hour=int(parsed_json['sun_phase']['sunset']['hour']),
                                            minute=int(parsed_json['sun_phase']['sunset']['minute']),
                                            second=0).timetuple()))

      # Parse hourly and week forecast
      datelimit = int(time.time()) + (2 * 24 * 60 * 60) # Hourly forecast limit of 2 days
      for forecast in parsed_json['hourly_forecast']:
        forecast_data = { 'from' : int(forecast['FCTTIME']['epoch']),
                          'to' : int(forecast['FCTTIME']['epoch']) + (60 * 60), # Data is provided per 1 hour
                          'weather' : forecast['condition'],
                          'rain' : 0.0, # Figure out the data
                          'humidity' : float(forecast['humidity']),
                          'wind_direction' : forecast['wdir']['dir'],
                          'wind_speed' : float(forecast['wspd']['metric']) / 3.6,
                          'temperature' : float(forecast['temp']['metric']),
                          'pressure' : float(forecast['mslp']['metric'])
                        }

        self.week_forecast[forecast_data['from']] = forecast_data
        if forecast_data['to'] <= datelimit:
          self.hour_forecast[forecast_data['from']] = forecast_data

    else:
      logger.error('Error getting online data from {}'.format(self.get_type()))
      return False

    return True

  def get_type(self):
    return terrariumWeatherWunderground.TYPE

class terrariumWeatherOpenWeathermap(terrariumWeatherSource):
  TYPE = 'Openweathermap.org'
  VALID_SOURCE = '^https?://api\.openweathermap\.org/data/2\.5/weather\?q=(?P<city>[^,&]+),(?P<country>[^,&]+)&units=metric&appid=[a-z0-9]{32}$'
  INFO_SOURCE = 'https://api.openweathermap.org/data/2.5/weather?q=[CITY],[COUNTRY_2LETTER]&units=metric&appid=[YOUR_API_KEY]'

  def load_data(self):
    logger.info('Update {} data from ONLINE refreshing cache.'.format(self.get_type()))
    self.credits['text'] = 'OpenWeatherMap weather data'

    parsed_json = terrariumUtils.get_remote_data(self.source)
    if parsed_json is not None:
      # Parse general data information
      self.location['city'] = parsed_json['name']
      self.location['country'] = parsed_json['sys']['country']
      self.location['geo']['lat'] = float(parsed_json['coord']['lat'])
      self.location['geo']['long'] = float(parsed_json['coord']['lon'])

      self.credits['url'] = 'https://openweathermap.org/city/{}'.format(parsed_json['id'])
      self.sun['rise'] = int(parsed_json['sys']['sunrise'])
      self.sun['set'] = int(parsed_json['sys']['sunset'])

      parsed_json = terrariumUtils.get_remote_data(self.source.replace('/weather?q','/forecast?q'))
      if parsed_json is not None:
        # Parse hourly and week forecast
        datelimit = int(time.time()) + (2 * 24 * 60 * 60) # Hourly forecast limit of 2 days
        for forecast in parsed_json['list']:
          forecast_data = { 'from' : int(forecast['dt']),
                            'to' : int(forecast['dt']) + (3 * 60 * 60),  # Data is provided per 3 hours
                            'weather' : forecast['weather'][0]['description'],
                            'rain' : (float(forecast['rain']['3h']) / 3.0) if 'rain' in forecast and '3h' in forecast['rain'] else 0,  # Guess in mm
                            'humidity' : float(forecast['main']['humidity']),
                            'wind_direction' : forecast['wind']['deg'],
                            'wind_speed' : float(forecast['wind']['speed']),
                            'temperature' : float(forecast['main']['temp']),
                            'pressure' : float(forecast['main']['pressure'])
                          }

          self.week_forecast[forecast_data['from']] = forecast_data
          if forecast_data['to'] <= datelimit:
            self.hour_forecast[forecast_data['from']] = forecast_data

    else:
      logger.error('Error getting online data from {}'.format(self.get_type()))
      return False

    return True

  def get_type(self):
    return terrariumWeatherOpenWeathermap.TYPE

class terrariumWeatherSourceException(Exception):
  '''The entered online weather source is not known or invalid'''

# Factory class
class terrariumWeather(object):
  SOURCES = [terrariumWeatherYRno,
             terrariumWeatherWunderground,
             terrariumWeatherOpenWeathermap]

  def __new__(self,source, temperature_indicator, windspeed_indicator, callback = None):
    for weather_source in terrariumWeather.SOURCES:
      if re.search(weather_source.VALID_SOURCE, source, re.IGNORECASE):
        return weather_source(source, temperature_indicator, windspeed_indicator, callback)

    raise terrariumWeatherSourceException()

  @staticmethod
  def valid_sources():
    data = {}
    for weather_source in terrariumWeather.SOURCES:
      data[weather_source.TYPE] = weather_source.INFO_SOURCE

    return data
