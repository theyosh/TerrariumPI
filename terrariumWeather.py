# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import untangle
from datetime import datetime, timedelta
import dateutil.parser
import thread
import time
import copy
import urllib2
import json
import re

from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumWeatherSource():

  update_timeout = 30 * 60 # Default update timeout of 30 minutes

  def __init__(self,url):
    self.source_url = url

    self.type = None
    self.city = None
    self.country = None
    self.geo = {'lat'  : None, 'long' : None}
    self.sunrise = None
    self.sunset = None
    self.hour_forecast = []
    self.week_forecast = []
    self.copyright = {'text' : '', 'url' : ''}

    self.last_update = None

  def update(self):
    now = time.time()
    if self.last_update is None or int(now) - self.last_update > terrariumWeatherSource.update_timeout:
      self.load_data()
      logger.info('Done loading data in %s seconds. Hour forcecast items: %s, week forecast items: %s.' % (time.time()-now,
                                                                                                           len(self.get_forecast('day')),
                                                                                                           len(self.get_forecast('all'))
                  ))
      self.last_update = int(now)

  def load_data(self):
    # Here custom code per type should be created
    pass

  def get_type(self):
    return self.type

  def get_city(self):
    return self.city

  def get_country(self):
    return self.country

  def get_geo(self):
    return self.geo

  def get_copyright(self):
    return self.copyright

  def get_sunrise(self):
    return self.sunrise

  def get_sunset(self):
    return self.sunset

  def get_forecast(self,period = 'day'):
    if period == 'day':
      return self.hour_forecast
    else:
      return self.week_forecast

class terrariumWeatherYRno(terrariumWeatherSource):

  def load_data(self):
    starttime = time.time()
    logger.info('Update YR.no data from ONLINE refreshing cache.')
    self.type = 'yr.no'

    try:
      # Parse hour forecast
      xmldata = untangle.parse(self.source_url.strip('/') + '/forecast_hour_by_hour.xml')
      # Parse general data information
      self.city = xmldata.weatherdata.location.name.cdata
      self.country = xmldata.weatherdata.location.country.cdata
      self.geo['lat']  = float(xmldata.weatherdata.location.location['latitude'])
      self.geo['long'] = float(xmldata.weatherdata.location.location['longitude'])
      self.copyright['text'] = xmldata.weatherdata.credit.link['text']
      self.copyright['url']  = xmldata.weatherdata.credit.link['url']
      self.sunrise = time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['rise']).timetuple())
      self.sunset  = time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['set']).timetuple())

      self.hour_forecast = []
      for forecast in xmldata.weatherdata.forecast.tabular.time:
        self.hour_forecast.append({ 'from' : time.mktime(dateutil.parser.parse(forecast['from']).timetuple()),
                                    'to' : time.mktime(dateutil.parser.parse(forecast['to']).timetuple()),
                                    'weather' : forecast.symbol['name'],
                                    'rain' : float(forecast.precipitation['value']),
                                    'humidity' : 0,
                                    'wind_direction' : forecast.windDirection['name'],
                                    'wind_speed' : float(forecast.windSpeed['mps']),
                                    'temperature' : float(forecast.temperature['value']),
                                    'pressure' : float(forecast.pressure['value'])
                                  })

      # Parse week forecast
      self.week_forecast = []
      xmldata = untangle.parse(self.source_url.strip('/') + '/forecast.xml')
      for forecast in xmldata.weatherdata.forecast.tabular.time:
        self.week_forecast.append({ 'from' : time.mktime(dateutil.parser.parse(forecast['from']).timetuple()),
                                    'to' : time.mktime(dateutil.parser.parse(forecast['to']).timetuple()),
                                    'weather' : forecast.symbol['name'],
                                    'rain' : float(forecast.precipitation['value']),
                                    'humidity' : 0,
                                    'wind_direction' : forecast.windDirection['name'],
                                    'wind_speed' : float(forecast.windSpeed['mps']),
                                    'temperature' : float(forecast.temperature['value']),
                                    'pressure' : float(forecast.pressure['value'])
                                  })
    except Exception:
      logger.exception('Error getting online data from yr.no')
      return False

    return True

class terrariumWeatherWunderground(terrariumWeatherSource):

  def load_data(self):
    logger.info('Update Wunderground data from ONLINE refreshing cache.')
    self.type = 'weather.com'
    self.copyright = {'text' : 'Wunderground weather data', 'url' : ''}

    try:
      json_data = urllib2.urlopen(self.source_url)
      parsed_json = json.loads(json_data.read())

      # Parse general data information
      self.city = parsed_json['location']['city']
      self.country = parsed_json['location']['country_name']
      self.geo['lat'] = float(parsed_json['location']['lat'])
      self.geo['long'] = float(parsed_json['location']['lon'])
      self.copyright['url'] = parsed_json['location']['wuiurl']

      now = datetime.now()
      self.sunrise = time.mktime(now.replace(hour=int(parsed_json['sun_phase']['sunrise']['hour']),
                                             minute=int(parsed_json['sun_phase']['sunrise']['minute']),
                                             second=0).timetuple())

      now = datetime.now() # Not sure if needed. But this will never fail!
      self.sunset = time.mktime(now.replace(hour=int(parsed_json['sun_phase']['sunset']['hour']),
                                            minute=int(parsed_json['sun_phase']['sunset']['minute']),
                                            second=0).timetuple())

      # Parse hourly and week forecast
      self.hour_forecast = []
      self.week_forecast = []
      datelimit = int(time.time()) + (2 * 24 * 60 * 60) # Hourly forecast limit of 2 days
      for forecast in parsed_json['hourly_forecast']:
        forecast_hour = { 'from' : int(forecast['FCTTIME']['epoch']),
                          'to' : int(forecast['FCTTIME']['epoch']) + (60 * 60), # Data is provided per 1 hour
                          'weather' : forecast['condition'],
                          'rain' : 0, # Figure out the data
                          'humidity' : float(forecast['humidity']),
                          'wind_direction' : forecast['wdir']['dir'],
                          'wind_speed' : float(forecast['wspd']['metric']) / 3.6,
                          'temperature' : float(forecast['temp']['metric']),
                          'pressure' : float(forecast['mslp']['metric'])
                        }
        self.week_forecast.append(copy.deepcopy(forecast_hour))
        if forecast_hour['to'] <= datelimit:
          self.hour_forecast.append(copy.deepcopy(forecast_hour))

    except Exception:
      logger.exception('Error getting online data from weather.com')
      return False

    return True

class terrariumWeatherOpenWeathermap(terrariumWeatherSource):

  def load_data(self):
    logger.info('Update OpenWeatherMap data from ONLINE refreshing cache.')
    self.type = 'openweathermap.org'
    self.copyright = {'text' : 'OpenWeatherMap data', 'url' : 'https://openweathermap.org/city/'}

    try:
      json_data = urllib2.urlopen(self.source_url)
      parsed_json = json.loads(json_data.read())

      # Parse general data information
      self.city = parsed_json['name']
      self.country = parsed_json['sys']['country']
      self.geo['lat'] = float(parsed_json['coord']['lat'])
      self.geo['long'] = float(parsed_json['coord']['lon'])
      self.copyright['url'] = 'https://openweathermap.org/city/' +  str(parsed_json['id'])
      self.sunrise = parsed_json['sys']['sunrise']
      self.sunset = parsed_json['sys']['sunset']

      # Parse hourly and week forecast
      json_data = urllib2.urlopen(self.source_url.replace('/weather?q','/forecast?q'))
      parsed_json = json.loads(json_data.read())

      self.hour_forecast = []
      self.week_forecast = []
      datelimit = int(time.time()) + (2 * 24 * 60 * 60) # Hourly forecast limit of 2 days
      for forecast in parsed_json['list']:
        forecast_hour = { 'from' : forecast['dt'],
                          'to' : forecast['dt'] + (3 * 60 * 60),  # Data is provided per 3 hours
                          'weather' : forecast['weather'][0]['description'],
                          'rain' : (float(forecast['rain']['3h']) / 3.0) if '3h' in forecast['rain'] else 0,  # Guess in mm
                          'humidity' : float(forecast['main']['humidity']),
                          'wind_direction' : forecast['wind']['deg'],
                          'wind_speed' : float(forecast['wind']['speed']) / 3.6,
                          'temperature' : float(forecast['main']['temp']),
                          'pressure' : float(forecast['main']['pressure'])
                        }
        self.week_forecast.append(copy.deepcopy(forecast_hour))
        if forecast_hour['to'] <= datelimit:
          self.hour_forecast.append(copy.deepcopy(forecast_hour))

    except Exception:
      logger.exception('Error getting online data from openweathermap.org')
      return False

    return True

class terrariumWeather():
  # Weather data expects temperature in celcius degrees and windspeed in meters per second
  weather_update_timeout = 4 * 60 * 60 # In seconds (4 hours)

  valid_temperature_indicators = ['C','F']
  valid_windspeed_indicators = ['kmh','ms']

  valid_sources = {'yr.no'       : re.compile(r'^https?://(www.)?yr.no/place/(?P<country>[^/]+)/(?P<provance>[^/]+)/(?P<city>[^/]+/?)?', re.IGNORECASE),
                   'weather.com' : re.compile(r'^https?://api\.wunderground\.com/api/[^/]+/(?P<p1>[^/]+)/(?P<p2>[^/]+)/(?P<p3>[^/]+)/q/(?P<country>[^/]+)/(?P<city>[^/]+)\.json$', re.IGNORECASE),
                   'openweathermap.org' : re.compile('https?://api\.openweathermap\.org/data/2\.5/weather\?q=(?P<city>[^,&]+),(?P<country>[^,&]+)&units=metric&appid=[a-z0-9]{32}$')
                   }

  def __init__(self, source,  windspeed  = 'kmh', temperature_indicator = None, callback = None):
    logger.info('Initializing weather object')
    self.source   = None
    self.next_update = 0
    self.location = {'city' : '', 'country' : '', 'geo' : {'lat' : 0, 'long' : 0}}
    self.credits  = {'text' : '', 'url' : ''}
    self.sun      = {'rise' : 0, 'set' : 0}
    self.hour_forecast = []
    self.week_forecast = []

    self.set_windspeed_indicator(windspeed)
    self.set_temperature_indicator(temperature_indicator)

    self.callback = callback

    if self.__set_source(source):
      self.refresh()

  def __set_source(self,source):
    for source_type in terrariumWeather.valid_sources:
      data = terrariumWeather.valid_sources[source_type].match(source)
      if data:
        self.source = source
        self.type = source_type

        if self.get_type() == 'yr.no':
          self.weater_source = terrariumWeatherYRno(self.source)
        elif self.get_type() == 'weather.com':
          self.weater_source = terrariumWeatherWunderground(self.source)
        elif self.get_type() == 'openweathermap.org':
          self.weater_source = terrariumWeatherOpenWeathermap(self.source)

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

             'rainshowers' : 'sleet',
             'heavyrainshowers' : 'sleet',
             'heavyrain' : 'sleet',
             'chanceofathunderstorm' : 'sleet',
             'thunderstorm' : 'sleet',
             'lightsleet' : 'sleet',


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

    self.weater_source.update()
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
    if len(self.hour_forecast) > 0 and now > self.hour_forecast[0]['to']:
      del self.hour_forecast[0]
      logger.info('Shift hourly forecast to: %s' % (self.hour_forecast[0]['to'],))
      send_message = True

    # Update week forecast
    if len(self.hour_forecast) > 0 and now > self.week_forecast[0]['to']:
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
                          'temperature_indicator' : self.get_temperature_indicator(),
                          'hour_forecast' : self.hour_forecast,
                          'week_forecast' : self.week_forecast,
                          'credits': self.credits})

    for item in data['hour_forecast']:
      item['wind_speed'] *= (3.6 if self.get_windspeed_indicator() == 'kmh' else 1.0)
      item['temperature'] = item['temperature'] if self.get_temperature_indicator() == 'C' else terrariumUtils.to_fahrenheit(item['temperature'])

    for item in data['week_forecast']:
      item['wind_speed'] *= (3.6 if self.get_windspeed_indicator() == 'kmh' else 1.0)
      item['temperature'] = item['temperature'] if self.get_temperature_indicator() == 'C' else terrariumUtils.to_fahrenheit(item['temperature'])

    return data

  def get_config(self):
    return {'location'    : self.get_source(),
            'windspeed'   : self.get_windspeed_indicator(),
            'type'        : self.get_type()}

  def get_type(self):
    return self.type

  def get_source(self):
    return self.source

  def set_source(self,url):
    if self.__set_source(url):
      self.refresh()

  def get_windspeed_indicator(self):
    return self.windspeed

  def set_windspeed_indicator(self,indicator):
    if indicator.lower() in terrariumWeather.valid_windspeed_indicators:
      self.windspeed = indicator.lower()

  def get_temperature_indicator(self):
    # 'Realtime' callback to terrariumEngine for right indicator
    return self.temperature_indicator().upper()

  def set_temperature_indicator(self,indicator):
    if indicator().upper() in terrariumWeather.valid_temperature_indicators:
      self.temperature_indicator = indicator

  def is_day(self):
    return self.sun['rise'] < int(time.time()) < self.sun['set']

  def is_night(self):
    return not self.is_day()
