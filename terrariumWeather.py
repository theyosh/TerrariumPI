# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import untangle
from datetime import datetime, timedelta
import dateutil.parser
import thread
import time
import copy

from gevent import monkey, sleep
monkey.patch_all()

class terrariumWeather():

  # We only supprt yr.no for now
  forecast_hours = '{location}/forecast_hour_by_hour.xml'
  forecast_week = '{location}/forecast.xml'

  def __init__(self, location,  windspeed  = 'kmh', temperature = 'C', callback = None):
    self.settings = {'type':'yr.no', 'location': location.strip('/')}
    self.location = {'city' : '', 'country' : '', 'geo' : {'lat' : 0, 'long' : 0}}
    self.credits =  {'text' : '', 'url' : ''}
    self.updates =  {'lastupdate' : 0 , 'nextupdate' : 0}
    self.sun =      {'rise' : 0, 'set' : 0}
    self.hour_forecast = []
    self.week_forecast = []
    self.callback = callback
    self.next_update = 0
    self.windspeed = windspeed
    self.temperature = temperature
    self.__refresh()

  def __get_weather_icon(self,weathertype):
    weathertype = weathertype.lower()

    icons = {'clear sky' : 'clear_' + ('day' if self.is_day() else 'night'),
           'fair' : 'clear_' + ('day' if self.is_day() else 'night'),
           'partly cloudy' : 'partly_cloudy_' + ('day' if self.is_day() else 'night'),
           'cloudy' : 'cloudy',
           'light rain showers' : 'rain',
           'light rain' : 'rain',
           'rain' : 'rain',
           'rain showers' : 'sleet',
           'heavy rain showers' : 'sleet',
           'heavy rain' : 'sleet',
           'fog' : 'fog'
           }

    if weathertype in icons:
      return icons[weathertype]

    return None

  def __refresh(self):
    logger.info('Refreshing weather data')
    self.__load_hours_forecast()
    self.__load_week_forecast()

    self.next_update = int(time.time()) + 3600
    logger.info('Done refreshing weather data. Next update after: %s' % (self.next_update,))

  def update(self, socket = False):
    send_message = False
    now = int(time.time())

    # Refresh the data
    if len(self.hour_forecast) == 0 or now > self.next_update:
      self.__refresh()
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
    data = copy.deepcopy({'city' :self.location,
                          'sun' : self.sun,
                          'day' : self.is_day(),
                          'windspeed' : self.windspeed,
                          'temperature' : self.temperature,
                          'hour_forecast' : self.hour_forecast,
                          'week_forecast' : self.week_forecast,
                          'credits': self.credits})

    for item in data['hour_forecast']:
      item['icon'] = self.__get_weather_icon(item['weather'])
      item['wind_speed'] *= (3.6 if self.windspeed == 'kmh' else 1.0)
      item['temperature'] = item['temperature'] if self.temperature == 'C' else 9.0 / 5.0 * item['temperature'] + 32.0

    for item in data['week_forecast']:
      item['icon'] = self.__get_weather_icon(item['weather'])
      item['wind_speed'] *= (3.6 if self.windspeed == 'kmh' else 1.0)
      item['temperature'] = item['temperature'] if self.temperature == 'C' else 9.0 / 5.0 * item['temperature'] + 32.0

    return data

  def __load_defaults(self,xmldata):
    self.location['city'] = xmldata.weatherdata.location.name.cdata
    self.location['country'] = xmldata.weatherdata.location.country.cdata
    self.location['geo'] = {'lat': float(xmldata.weatherdata.location.location['latitude']),
                            'long' : float(xmldata.weatherdata.location.location['longitude'])}

    self.credits['text'] = xmldata.weatherdata.credit.link['text']
    self.credits['url'] = xmldata.weatherdata.credit.link['url']

    self.sun['rise'] = time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['rise']).timetuple())
    self.sun['set'] = time.mktime(dateutil.parser.parse(xmldata.weatherdata.sun['set']).timetuple())

    logger.debug('Loaded weather defaults for location %s, sun %s, credits %s' % (self.location,self.sun,self.credits))

  def __load_hours_forecast(self):
    logger.debug('Loading hours forcecast data from location: %s' % (terrariumWeather.forecast_hours.replace('{location}',self.settings['location']),))
    xmldata = untangle.parse(terrariumWeather.forecast_hours.replace('{location}',self.settings['location']))
    self.__load_defaults(xmldata);
    self.hour_forecast = []
    for forecast in xmldata.weatherdata.forecast.tabular.time:
      self.hour_forecast.append({'from' : time.mktime(dateutil.parser.parse(forecast['from']).timetuple()),
                            'to' : time.mktime(dateutil.parser.parse(forecast['to']).timetuple()),
                            'weather' : forecast.symbol['name'],
                            'rain' : float(forecast.precipitation['value']),
                            'wind_direction' : forecast.windDirection['name'],
                            'wind_speed' : float(forecast.windSpeed['mps']),
                            'temperature' : float(forecast.temperature['value']),
                            'pressure' : float(forecast.pressure['value']),
                            'icon' : self.__get_weather_icon(forecast.symbol['name'])
                           })
      logger.debug('Added hour forecast for timeslot %s to %s' % (datetime.fromtimestamp(self.hour_forecast[len(self.hour_forecast)-1]['from']),
                                                                  datetime.fromtimestamp(self.hour_forecast[len(self.hour_forecast)-1]['to'])))

  def __load_week_forecast(self):
    logger.debug('Loading week forcecast data from location: %s' % (terrariumWeather.forecast_week.replace('{location}',self.settings['location']),))
    xmldata = untangle.parse(terrariumWeather.forecast_week.replace('{location}',self.settings['location']))
    self.__load_defaults(xmldata);
    self.week_forecast = []
    for forecast in xmldata.weatherdata.forecast.tabular.time:
      self.week_forecast.append({'from' : time.mktime(dateutil.parser.parse(forecast['from']).timetuple()),
                              'to' : time.mktime(dateutil.parser.parse(forecast['to']).timetuple()),
                              'weather' : forecast.symbol['name'],
                              'rain' : float(forecast.precipitation['value']),
                              'wind_direction' : forecast.windDirection['name'],
                              'wind_speed' : float(forecast.windSpeed['mps']),
                              'temperature' : float(forecast.temperature['value']),
                              'pressure' : float(forecast.pressure['value']),
                              'icon' : self.__get_weather_icon(forecast.symbol['name'])
                             })
      logger.debug('Added week forecast for timeslot %s to %s' % (datetime.fromtimestamp(self.week_forecast[len(self.week_forecast)-1]['from']),
                                                                  datetime.fromtimestamp(self.week_forecast[len(self.week_forecast)-1]['to'])))

  def get_config(self):
    return {'location' : self.settings['location'],
            'windspeed' : self.windspeed,
            'temperature' : self.temperature,
            'type': self.settings['type']}

  def set_location(self,location):
    location = location.strip('/')
    refresh = location != self.settings['location'].strip('/')
    self.settings['location'] = location
    if refresh:
      # Start refresh in a thread, so it will not lockup the web interface / API call
      thread.start_new_thread(self.__refresh, (True))

  def set_windspeed_indicator(self,indicator):
    if indicator in ['kmh','ms']:
      self.windspeed = indicator

  def set_temperature_indicator(self,indicator):
    if indicator.upper() in ['C','F']:
      self.temperature = indicator.upper()

  def is_day(self):
    return self.sun['rise'] < int(time.time()) < self.sun['set']
