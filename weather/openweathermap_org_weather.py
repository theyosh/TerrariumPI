# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWeatherAbstract, terrariumWeatherException
from terrariumUtils import terrariumUtils

from datetime import datetime, date
import copy

class terrariumOpenweathermap(terrariumWeatherAbstract):
  HARDWARE     = 'Openweathermap.org'
  NAME         = 'OpenWeatherMap weather data'
  VALID_SOURCE = '^https?://api\.openweathermap\.org/data/2\.5/weather\?q=(?P<city>[^,&]+),(?P<country>[^,&]{2})&appid=[a-z0-9]{32}$'
  INFO_SOURCE  = 'https://api.openweathermap.org/data/2.5/weather?q=[CITY],[COUNTRY_2CHAR]&appid=[YOUR_API_KEY]'

  def __load_general_data(self):
    address = self.address + '&units=metric'
    logger.debug('Loading weather source {}'.format(address))
    data = terrariumUtils.get_remote_data(self.address)
    if data:
      self._data['city']    = data['name']
      self._data['country'] = data['sys']['country']
      self._data['geo']     = {'lat'  : float(data['coord']['lat']),
                               'long' : float(data['coord']['lon']) }
      self._data['url']     = 'https://openweathermap.org/city/{}'.format(data['id'])
      self._data['credits'] = 'OpenWeatherMap weather data'

      self._data['days'] = []

      return True

    logger.warning('Error loading online weather data from source {} !'.format(address))
    return False

  def __load_forecast_data(self):
    address = terrariumUtils.parse_url(self.address)
    data = terrariumUtils.get_remote_data('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=minutely&appid={}'.format(self._data['geo']['lat'],self._data['geo']['long'],address['query_params']['appid']))

    if data:
      # Get the sunrise and sunset from the current data
      sunrise = data['current']['sunrise']
      sunset = data['current']['sunset']

      # Loop over hourly and daily forecasts
      for day in data['hourly'] + data['daily']:
        #print(day)
        # Here we store the new sunrise and sunset. If there is no new update, use the old values.
        sunrise = day.get('sunrise',sunrise)
        sunset  = day.get('sunset',sunset)

        # As daily forecast has four time parts, we have to use a list.
        tempdata = []

        # Is the temp value a float (hourly forecast), then just process this single forecast
        if terrariumUtils.is_float(day['temp']):
          tempdata.append(day)

        else:
          # Else we have to create multiple forecasts with differnt timestamps and temperatures
          for part in day['temp']:
            tempday = copy.deepcopy(day)
            tempday['temp'] = day['temp'][part]

            if part == 'day':
              self._data['days'].append({
                'dt' : tempday['dt'],
                'rise'     : sunrise,
                'set'      : sunset,
                'temp'     : tempday['temp'],
                'humidity' : tempday['humidity'],
                'wind'     : {'speed'     : tempday['wind_speed'],    # Speed is in meter per second
                              'direction' : tempday['wind_deg']},
                'weather'  : tempday['weather'][0]['description']
              })

            elif part == 'night':
              continue

            # Modify the timestamp based on period of the day and the timestamp of the forecast
            # The forecast timestamp is always 12:00 UTC (middle of the day)
            if 'night' == part:
              tempday['dt'] = day['dt'] + 12 * 60 * 60

              sunrise += 24 * 60 * 60
              sunset += 24 * 60 * 60

            elif 'eve' == part:
              tempday['dt'] = day['dt'] + 6 * 60 * 60
            elif 'morn' == part:
              tempday['dt'] = day['dt'] - 6 * 60 * 60

            tempdata.append(tempday)

        # Put of the forecast data in one list indexed on the forecast timestamps

        for forecast  in tempdata:
          temperature = forecast['temp'] if terrariumUtils.is_float(forecast['temp']) else forecast['temp']['day']

          self._data['forecast'][str(forecast['dt'])] = {'rise'     : sunrise,
                                                    'set'      : sunset,
                                                    'temp'     : temperature,
                                                    'humidity' : forecast['humidity'],
                                                    'wind'     : {'speed'     : forecast['wind_speed'],    # Speed is in meter per second
                                                                  'direction' : forecast['wind_deg']},
                                                    'weather'  : forecast['weather'][0]['description']}

          # TODO: Make a sorting based on the timestamps??


      self._data['days'][0]['temp'] = data['current']['temp']
      self._data['days'][0]['weather'] = data['current']['weather'][0]['description']

#      print(self._data['forecast'])
      for timestamp in sorted(self._data['forecast'].keys()):
        for day in self._data['days']:
          if date.fromtimestamp(int(timestamp)) == date.fromtimestamp(int(day['dt'])):
            self._data['forecast'][timestamp]['rise'] = day['rise']
            self._data['forecast'][timestamp]['set'] = day['set']

#        print('{} -> {}, {}'.format(datetime.fromtimestamp(int(timestamp)), datetime.fromtimestamp(self._data['forecast'][timestamp]['rise']), datetime.fromtimestamp(self._data['forecast'][timestamp]['set'])))


      return True

    return False

  def _load_data(self):
    if self.__load_general_data():
      return self.__load_forecast_data()

    return False
