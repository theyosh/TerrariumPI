# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

class terrariumTranslations():

  def __init__(self):
    logger.info('Initialize translations')
    self.translations = {}
    self.__load()

  def __load(self):
    logger.debug('Loading translations')
    # Weather
    self.translations['weather_field_location'] = _('Enter the full url to the weather data source. For now only YR.no is supported')
    self.translations['weather_field_wind_speed'] = _('Choose the windspeed indicator. The software will recalculate to the chosen indicator')
    self.translations['weather_field_temperature'] = _('Choose the temperature indicator. The software will recalulate to the chosen indicator')
    # End weather

    # Sensors
    self.translations['sensor_field_address'] = _('Shows the 1-wire address of the sensor. (readonly)')
    self.translations['sensor_field_name'] = _('Holds the name of the sensor.')
    self.translations['sensor_field_alarm_min'] = _('Holds the lower limit of the sensor. When below this value, alarms will trigger. Like humidity gets to low, it will trigger the spraying system.')
    self.translations['sensor_field_alarm_max'] = _('Holds the maximum limit of the sensor. When above this value, it will show alarms to indicate but no triggers.')
    self.translations['sensor_field_limit_min'] = _('Holds the lowest value that should be used in the graphs.')
    self.translations['sensor_field_limit_max'] = _('Holds the maximum value that should be used in the graphs.')
    self.translations['sensor_field_current'] = _('Shows the current value in temperature or humidity.')
    # End sensors

    # Switches
    self.translations['switch_field_id'] = _('Shows the switch ID. (readonly)')
    self.translations['switch_field_name'] = _('Holds the name of the switch.')
    self.translations['switch_field_power_usage'] = _('Holds the amount of watt of the power comsupmtion when switched on.')
    self.translations['switch_field_water_flow'] = _('Holds the amount of water in liter per minute that is flowing through when switched on.')
    # End switches

    # Doors
    self.translations['door_field_id'] = _('Shows the door ID. (readonly)')
    self.translations['door_field_name'] = _('Holds the name of the door.')
    self.translations['door_field_gpio_pin'] = _('Holds the pin number on which the door sensor is connected.')
    # End doors

    # Webcam
    self.translations['webcam_field_id'] = _('Shows the webcam ID. (readonly)')
    self.translations['webcam_field_name'] = _('Holds the name of the webcam.')
    self.translations['webcam_field_location'] = _('Holds the location of the source. For Raspberry PI cam use \'%s\'. For V4L use \'%s\'. And for a remote HTTP webcam use a full url like \'%s\'.')
    self.translations['webcam_field_rotation'] = _('Holds the rotation value of the webcam.')
    # End webcam

    logger.info('Translations loaded')

  def get_translation(self,translation):
    if translation in self.translations:
      return self.translations[translation]

    logger.warning('No translation available for \'%s\'' % (translation,))
    return 'No translation available for \'%s\'' % (translation,)

  def reload(self):
    logger.info('Reloading translations')
    self.__load()
