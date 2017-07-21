# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import untangle
from datetime import datetime, timedelta
import dateutil.parser
import thread
import time
import copy
import urllib2
import json
import re

from gevent import monkey, sleep
monkey.patch_all()

class terrariumWeatherYRno():

  update_timeout = 30 * 60
  forecast_hours = '{location}/forecast_hour_by_hour.xml'
  forecast_week = '{location}/forecast.xml'

  def __init__(self,url):
    # We 'accept' that the url is valid... :(
    self.source = url

    self.city = None
    self.country = None
    self.geo = None
    self.sunrise = None
    self.sunset = None
    self.forecast = []
    self.copyright = {'text' : '', 'url' : ''}

    self.last_update = None

  def __update(self):
    now = int(time.time())
    if self.last_update is None or now - self.last_update > terrariumWeatherYRno.update_timeout:
      logger.info('Update YR.no data from ONLINE refreshing cache.')
      self.__process_forecast_data('hour')
      self.__process_forecast_data('week')
      self.last_update = now

  def __load_defaults(self,xmldata):
    self.city = xmldata.weatherdata.location.name.cdata
    self.country = xmldata.weatherdata.location.country.cdata
    self.geo = {'lat'  : float(xmldata.weatherdata.location.location['latitude']),
                'long' : float(xmldata.weatherdata.location.location['longitude'])}

    self.copyright['text'] = xmldata.weatherdata.credit.link['text']
    self.copyright['url']  = xmldata.weatherdata.credit.link['url']

    self.sunrise = time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['rise']).timetuple())
    self.sunset  = time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['set']).timetuple())

  def __process_forecast_data(self,period = 'hour'):
    if period == 'hour':
      xmldata = untangle.parse(terrariumWeatherYRno.forecast_hours.replace('{location}',self.source))
    elif period == 'week':
      xmldata = untangle.parse(terrariumWeatherYRno.forecast_week.replace('{location}',self.source))

    self.__load_defaults(xmldata)

    data = []
    for forecast in xmldata.weatherdata.forecast.tabular.time:
      data.append({'from' : time.mktime(dateutil.parser.parse(forecast['from']).timetuple()),
                   'to' : time.mktime(dateutil.parser.parse(forecast['to']).timetuple()),
                   'weather' : forecast.symbol['name'],
                   'rain' : float(forecast.precipitation['value']),
                   'wind_direction' : forecast.windDirection['name'],
                   'wind_speed' : float(forecast.windSpeed['mps']),
                   'temperature' : float(forecast.temperature['value']),
                   'pressure' : float(forecast.pressure['value'])
                  })

    if period == 'hour':
      self.hour_forecast = copy.deepcopy(data)
    elif period == 'week':
      self.week_forecast = copy.deepcopy(data)

  #def __set_sunrise(self,data):
  #  now = datetime.now()
  #  self.sunrise = now.replace(hour=int(data['hour']), minute=int(data['minute']), second=0)

  #def __set_sunset(self,data):
  #  now = datetime.now()
  #  self.sunset = now.replace(hour=int(data['hour']), minute=int(data['minute']), second=0)
  #  if now > self.sunset:
  #    self.sunrise += timedelta(days=1)
  #    self.sunset += timedelta(days=1)

  def get_city(self):
    self.__update()
    return self.city

  def get_country(self):
    self.__update()
    return self.country

  def get_geo(self):
    self.__update()
    return self.geo

  def get_copyright(self):
    self.__update()
    return self.copyright

  def get_sunrise(self):
    self.__update()
    return self.sunrise

  def get_sunset(self):
    self.__update()
    return self.sunset

  def get_forecast(self,period = 'day'):
    self.__update()
    if period == 'day':
      return self.hour_forecast
    else:
      return self.week_forecast

class terrariumWeatherWunderground():

  update_timeout = 30 * 60

  def __init__(self,url):
    # We 'accept' that the url is valid... :(
    self.source = url

    self.city = None
    self.country = None
    self.geo = None
    self.sunrise = None
    self.sunset = None
    self.forecast = []
    self.copyright = {'text' : 'Wunderground weather data', 'url' : ''}

    self.last_update = None

  def __update(self):
    now = int(time.time())
    if self.last_update is None or now - self.last_update > terrariumWeatherWunderground.update_timeout:
      logger.info('Update Wunderground data from ONLINE refreshing cache.')
      json_data = urllib2.urlopen(self.source)
      parsed_json = json.loads(json_data.read())

      self.city = parsed_json['location']['city']
      self.country = parsed_json['location']['country_name']
      self.geo = {'lat' : float(parsed_json['location']['lat']), 'long' : float(parsed_json['location']['lon'])}
      self.copyright['url'] = parsed_json['location']['wuiurl']

      self.__set_sunrise(parsed_json['sun_phase']['sunrise'])
      self.__set_sunset(parsed_json['sun_phase']['sunset'])
      self.__process_forecast_data(parsed_json['hourly_forecast'])

      self.last_update = now

  def __set_sunrise(self,data):
    now = datetime.now()
    self.sunrise = now.replace(hour=int(data['hour']), minute=int(data['minute']), second=0)

  def __set_sunset(self,data):
    now = datetime.now()
    self.sunset = now.replace(hour=int(data['hour']), minute=int(data['minute']), second=0)

  def __process_forecast_data(self,data):
    self.forecast = []
    for forecast in data:
      self.forecast.append({'from' : int(forecast['FCTTIME']['epoch']),
                            'to' : int(forecast['FCTTIME']['epoch']) + (60 * 60),
                            'weather' : forecast['condition'],
                            'rain' : 0, # Figure out the data
                            'wind_direction' : forecast['wdir']['dir'],
                            'wind_speed' : float(forecast['wspd']['metric']) / 3.6,
                            'temperature' : float(forecast['temp']['metric']),
                            'pressure' : float(forecast['mslp']['metric'])
                          })

  def get_city(self):
    self.__update()
    return self.city

  def get_country(self):
    self.__update()
    return self.country

  def get_geo(self):
    self.__update()
    return self.geo

  def get_copyright(self):
    self.__update()
    return self.copyright

  def get_sunrise(self):
    self.__update()
    return time.mktime(self.sunrise.timetuple())

  def get_sunset(self):
    self.__update()
    return time.mktime(self.sunset.timetuple())

  def get_forecast(self,period = 'day'):
    self.__update()
    data = []
    datelimit = int(time.time()) + (1 * 24 * 60 * 60 if period == 'day' else 99 * 24 * 60 * 60)
    for forecast in self.forecast:
      if forecast['to'] < datelimit:
        data.append(forecast)

    return copy.deepcopy(data)

class terrariumWeather():
  # Weather data expects temperature in celcius degrees and windspeed in meters per second
  weather_update_timeout = 4 * 60 * 60 # In seconds (4 hours)

  valid_temperature_indicators = ['c','f']
  valid_windspeed_indicators = ['kmh','ms']

  valid_sources = {'yr.no'       : re.compile(r'^https?://(www.)?yr.no/place/(?P<country>[^/]+)/(?P<provance>[^/]+)/(?P<city>[^/]+/?)?', re.IGNORECASE),
                   'weather.com' : re.compile(r'^https?://api\.wunderground\.com/api/[^/]+/(?P<p1>[^/]+)/(?P<p2>[^/]+)/(?P<p3>[^/]+)/q/(?P<country>[^/]+)/(?P<city>[^/]+)\.json$', re.IGNORECASE)}

  def __init__(self, source,  windspeed  = 'kmh', temperature = 'C', callback = None):
    logger.info('Initializing weather object')
    self.source   = None
    self.next_update = 0
    self.location = {'city' : '', 'country' : '', 'geo' : {'lat' : 0, 'long' : 0}}
    self.credits  = {'text' : '', 'url' : ''}
    self.sun      = {'rise' : 0, 'set' : 0}
    self.hour_forecast = []
    self.week_forecast = []

    self.set_windspeed_indicator(windspeed)
    self.set_temperature_indicator(temperature)

    self.callback = callback

    if self.__set_source(source):
      self.refresh()

  def __set_source(self,source):
    for source_type in terrariumWeather.valid_sources:
      data = terrariumWeather.valid_sources[source_type].match(source)
      if data and self.source != source:
        self.source = source
        self.type = source_type

        if self.get_type() == 'yr.no':
          self.weater_source = terrariumWeatherYRno(self.source)
        elif self.get_type() == 'weather.com':
          self.weater_source = terrariumWeatherWunderground(self.source)

        logger.info('Set weather to type \'%s\' based on source to \'%s\'' % (self.get_type(),
                                                                              self.get_source()))
        return True

    logger.error('Setting weather source failed! The url \'%s\' is invalid' % source)
    return False

  def __update_weather_icons(self):
    for forecast in self.hour_forecast:
      forecast['icon'] = self.__get_weather_icon(forecast['weather'])

    for forecast in self.week_forecast:
      forecast['icon'] = self.__get_weather_icon(forecast['weather'])

  def __get_weather_icon(self,weathertype):
    weathertype = weathertype.lower().replace(' ','',10)

    icons = {'clearsky' : 'clear_' + ('day' if self.is_day() else 'night'),
             'fair' : 'clear_' + ('day' if self.is_day() else 'night'),
             'clear' : 'clear_' + ('day' if self.is_day() else 'night'),

             'partlycloudy' : 'partly_cloudy_' + ('day' if self.is_day() else 'night'),
             'mostlycloudy' : 'partly_cloudy_' + ('day' if self.is_day() else 'night'),
             'cloudy' : 'cloudy',
             'overcast' : 'cloudy',

             'lightrainshowers' : 'rain',
             'lightrain' : 'rain',
             'rain' : 'rain',
             'chanceofrain' : 'rain',

             'rainshowers' : 'sleet',
             'heavyrainshowers' : 'sleet',
             'heavyrain' : 'sleet',
             'chanceofathunderstorm' : 'sleet',
             'thunderstorm' : 'sleet',

             'fog' : 'fog',

             'lightsnowshowers' : 'snow'
           }

    if weathertype in icons:
      return icons[weathertype]

    return None

  def refresh(self):
    starttime = time.time()
    logger.info('Refreshing \'%s\' weather data from source \'%s\'' % (self.get_type(),
                                                                   self.get_source()))

    self.sun['rise'] = self.weater_source.get_sunrise()
    self.sun['set'] = self.weater_source.get_sunset()
    self.location['city'] = self.weater_source.get_city()
    self.location['country'] = self.weater_source.get_country()
    self.location['geo'] = self.weater_source.get_geo()
    self.credits = self.weater_source.get_copyright()
    self.hour_forecast = self.weater_source.get_forecast('day')
    self.week_forecast = self.weater_source.get_forecast('all')
    self.__update_weather_icons()

    self.next_update = int(starttime) + terrariumWeather.weather_update_timeout
    logger.info('Done refreshing weather data in %.5f seconds. Next refresh after: %s' % (time.time() - starttime,
                                                                                         datetime.fromtimestamp(self.next_update),))

  def update(self, socket = False):
    send_message = False
    now = int(time.time())

    # Refresh the data
    if len(self.hour_forecast) == 0 or now > self.next_update:
      self.refresh()
      send_message = True

    # Update hourly forecast for today
    if now > self.hour_forecast[0]['to']:
      del self.hour_forecast[0]
      logger.info('Shift hourly forecast to: %s' % (self.hour_forecast[0]['to'],))
      send_message = True

    # Update week forecast
    if now > self.week_forecast[0]['to']:
      del self.week_forecast[0]
      logger.info('Shift weekly forecast to: %s' % (self.hour_forecast[0]['to'],))
      send_message = True

    # Send message when there where changes
    if send_message:
      self.callback(socket=True)

  def get_data(self):
    data = copy.deepcopy({'city' : self.location,
                          'sun' : self.sun,
                          'day' : self.is_day(),
                          'windspeed' : self.get_windspeed_indicator(),
                          'temperature' : self.get_temperature_indicator(),
                          'hour_forecast' : self.hour_forecast,
                          'week_forecast' : self.week_forecast,
                          'credits': self.credits})

    for item in data['hour_forecast']:
      item['wind_speed'] *= (3.6 if self.get_windspeed_indicator() == 'kmh' else 1.0)
      item['temperature'] = item['temperature'] if self.get_temperature_indicator() == 'C' else 9.0 / 5.0 * item['temperature'] + 32.0

    for item in data['week_forecast']:
      item['wind_speed'] *= (3.6 if self.get_windspeed_indicator() == 'kmh' else 1.0)
      item['temperature'] = item['temperature'] if self.get_temperature_indicator() == 'C' else 9.0 / 5.0 * item['temperature'] + 32.0

    return data

  def get_config(self):
    return {'location'    : self.get_source(),
            'windspeed'   : self.get_windspeed_indicator(),
            'temperature' : self.get_temperature_indicator(),
            'type'        : self.get_type()}

  def get_type(self):
    return self.type

  def get_source(self):
    return self.source

  def set_soure(self,url):
    if self.__set_source(url):
      self.refresh()

  def get_windspeed_indicator(self):
    return self.windspeed

  def set_windspeed_indicator(self,indicator):
    if indicator.lower() in terrariumWeather.valid_windspeed_indicators:
      self.windspeed = indicator.lower()

  def get_temperature_indicator(self):
    return self.temperature.upper()

  def set_temperature_indicator(self,indicator):
    if indicator.lower() in terrariumWeather.valid_temperature_indicators:
      self.temperature = indicator.lower()

  def is_day(self):
    return self.sun['rise'] < int(time.time()) < self.sun['set']
