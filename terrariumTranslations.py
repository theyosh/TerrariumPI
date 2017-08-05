# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from terrariumWeather import terrariumWeather
from terrariumSensor import terrariumSensor
from terrariumSwitch import terrariumSwitch
from terrariumDoor import terrariumDoor
from terrariumWebcam import terrariumWebcam

class terrariumTranslations():

  def __init__(self):
    logger.info('Initialize TerariumPI translations')
    self.translations = {}
    self.__load()

  def __load(self):
    logger.debug('Loading TerariumPI translations')
    # Weather
    self.translations['weather_field_location'] = _('Holds the external source URL. Supported sources are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumWeather.valid_sources.keys()) + '</strong>')
    self.translations['weather_field_wind_speed'] = _('Choose the wind speed indicator. The software will recalculate to the chosen indicator.')
    # End weather

    # Sensors
    self.translations['sensor_field_hardware'] = _('Holds the sensor hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSensor.valid_hardware_types) + '</strong>')
    self.translations['sensor_field_address'] = _('Holds the sensor address. Depending on hardware type, it is either a read only hex number or GPIO pin. When using DHT11, DHT22 or AM2303 use <strong>Broadcom</strong> pin numbering (BCM)')
    self.translations['sensor_field_type'] = _('Holds the sensor type. Supported sensor types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSensor.valid_sensor_types) + '</strong>')
    self.translations['sensor_field_name'] = _('Holds the name of the sensor.')
    self.translations['sensor_field_alarm_min'] = _('Holds the sensor lower alarm value of the sensor. When below this value, alarms can be triggered.')
    self.translations['sensor_field_alarm_max'] = _('Holds the sensor maximum alarm value of the sensor. When above this value, alarms can be triggered.')
    self.translations['sensor_field_limit_min'] = _('Holds the sensor lowest value that should be used in the graphs.')
    self.translations['sensor_field_limit_max'] = _('Holds the sensor maximum value that should be used in the graphs.')
    self.translations['sensor_field_current'] = _('Shows the sensor current value in temperature or humidity (read only).')
    # End sensors

    # Switches
    self.translations['switch_field_hardware'] = _('Holds the switch hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSwitch.valid_hardware_types) + '</strong>')
    self.translations['switch_field_address'] = _('Holds the switch address. Depending on hardware type, it is either a number or GPIO pin. For GPIO use <strong>normal</strong> GPIO numbering.')
    self.translations['switch_field_name'] = _('Holds the switch name.')
    self.translations['switch_field_power_wattage'] = _('Holds the switch power usage in Watt when switched on.')
    self.translations['switch_field_water_flow'] = _('Holds the switch water flow in liters per minute when switched on')
    # End switches

    # Doors
    self.translations['door_field_hardware'] = _('Holds the door hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumDoor.valid_hardware_types) + '</strong>')
    self.translations['door_field_address'] = _('Holds the door address. When using GPIO use <strong>normal</strong> GPIO pin numbering as address.')
    self.translations['door_field_name'] = _('Holds the door name.')
    # End doors

    # Webcam
    self.translations['webcam_field_location'] = _('Holds the webcam location source. Supported sources are: %s') % ('<strong>RPICam</strong>, <strong>V4L device</strong>, <strong>Remote URL</strong>')
    self.translations['webcam_field_name'] = _('Holds the webcam name.')
    self.translations['webcam_field_rotation'] = _('Holds the webcam rotation of the image.')
    self.translations['webcam_field_preview'] = _('Shows the webcam preview image.')
    # End webcam

    # System
    self.translations['environment_field_lights_enable'] = _('Enable or disable the light system. When enabled, you can make changes below. By disabling it will not loose the current settings. It will temporary stop the lighting system.')
    self.translations['environment_field_lights_mode'] = _('Select the mode on which the lights will be put on and off. Select \'%s\' to use the sun rise and sun set at your location. This will make the amount of lighting variable to the actual amount of daylight. When selecting \'%s\', the light will put on and off at selected times.') % (_('Weather'),_('Timer'))
    self.translations['environment_field_lights_on'] = _('Enter the time when the light should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_lights_off'] = _('Enter the time when the lights should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_lights_max_hours'] = _('Enter the maximum amount of lights time in hours. When the time between on and off is more then this maximum, the on and off time will be shifted more to each other.')
    self.translations['environment_field_lights_min_hours'] = _('Enter the minimum amount of lights time in hours. When the time between on and off is less then this amount of hours, the on and off time will be widened until the minimum amount of hours entered here.')
    self.translations['environment_field_lights_hour_shift'] = _('Enter the amount of hours that the lights should shift. Is only needed when running in the \'%s\' mode. Enter a positive number for adding hours to the start time. Use negative numbers for subtracting from the start time.') % _('Weather')
    self.translations['environment_field_lights_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the lights. Select all needed switches below.')


    self.translations['environment_field_sprayer_enable'] = _('Enable or disable the sprayer system. When enabled, you can make changes below. By disabling it will not loose the current settings. It will temporary stop the sprayer system.')
    self.translations['environment_field_sprayer_enable_during_night'] = _('Enable spraying when the lights are off. This can cause water flow when there is not enough heat to vaporize the water.')
    self.translations['environment_field_sprayer_mode'] = _('Select the operating mode. For now only sensor mode is available.')
    self.translations['environment_field_sprayer_delay'] = _('How much time must there be between two spray actions and after start up. Enter the amount of seconds in which the humidity can settle.')
    self.translations['environment_field_sprayer_duration'] = _('How long is the system spraying. Enter the amount of seconds that the system is on when the humidity is to low.')
    self.translations['environment_field_sprayer_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the sprayer. Select all needed switches below.')
    self.translations['environment_field_sprayer_humidity_sensors'] = _('Select the humidity sensors that are used to control the humidity. When selecting multiple sensors, the average is calculated to determine the final humidity.')


    self.translations['environment_field_heater_enable'] = _('Enable or disable the heater system. When enabled, you can make changes below. By disabling it will not loose the current settings. It will temporary stop the heater system.')
    self.translations['environment_field_heater_enable_during_day'] = _('Enable heating when the lights are on. This can cause overheating when the lights are on.')
    self.translations['environment_field_heater_mode'] = _('Select the operating mode. Use \'%s\' mode to select the time period in which the heating is running. Select \'%s\' mode to use the sun rise and sun set as on and off times. When the sun rises the heating system will stop. Use \'%s\' mode to have the heating running when the lights are off.') % (_('Timer'),_('Weather'),_('Sensor'))
    self.translations['environment_field_heater_on'] = _('Enter the time when the heater should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_heater_off'] = _('Enter the time when the heater should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_heater_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the heater. Select all needed switches below.')
    self.translations['environment_field_heater_temperature_sensors'] = _('Select the temperature sensors that are used to control the temperature. When selecting multiple sensors, the average is calculated to determine the final temperature.')


    self.translations['environment_field_cooler_enable'] = _('Enable or disable the cooler system. When enabled, you can make changes below. By disabling it will not loose the current settings. It will temporary stop the cooler system.')
    self.translations['environment_field_cooler_enable_during_night'] = _('Enable cooling when the lights are off. This can cause a very low temperature when the lights are off.')
    self.translations['environment_field_cooler_mode'] = _('Select the operating mode. Use \'%s\' mode to select the time period in which the heating is running. Select \'%s\' mode to use the sun rise and sun set as on and off times. When the sun rises the heating system will stop. Use \'%s\' mode to have the heating running when the lights are off.') % (_('Timer'),_('Weather'),_('Sensor'))
    self.translations['environment_field_cooler_on'] = _('Enter the time when the cooler should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_cooler_off'] = _('Enter the time when the cooler should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_cooler_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the cooler. Select all needed switches below.')
    self.translations['environment_field_cooler_temperature_sensors'] = _('Select the temperature sensors that are used to control the temperature. When selecting multiple sensors, the average is calculated to determine the final temperature.')


    self.translations['system_field_language'] = _('Choose your interface language.')
    self.translations['system_field_admin'] = _('Holds the username which can make changes (Administrator).')
    self.translations['system_field_new_password'] = _('Enter the new password for the administration user. Leaving empty will not change the password!')
    self.translations['system_field_current_password'] = _('Enter the current password in order to change the password.')
    self.translations['system_field_pi_power'] = _('Holds the amount of power in Wattage that the Raspberry PI uses including all USB equipment.')
    self.translations['system_field_power_price'] = _('Holds the amount of euro/dollar per 1 kW/h (1 Kilowatt per hour).')
    self.translations['system_field_water_price'] = _('Holds the amount of euro/dollar per 1000 liters water.')
    self.translations['system_field_temperature_indicator'] = _('Choose the temperature indicator. The software will recalculate to the chosen indicator.')
    self.translations['system_field_hostname'] = _('Holds the host name or IP address on which the software will listen for connections. Enter :: for all addresses to bind.')
    self.translations['system_field_port_number'] = _('Holds the port number on which the software is listening for connections.')
    self.translations['system_field_owfs_port'] = _('Holds the port number on which the OWFS software is running. Leave empty to disable OWFS support.')
    # End system


    self.translations['profile_name'] = _('Holds the name of the animal.')
    self.translations['profile_type'] = _('Holds the type of the animal')
    self.translations['profile_gender'] = _('Holds the gender of the animal.')
    self.translations['profile_age'] = _('Holds the day of birth of the animal.')
    self.translations['profile_species'] = _('Holds the species name of the animal.')
    self.translations['profile_latin_name'] = _('Holds the latin name of the animal.')
    self.translations['profile_description'] = _('Holds a small description about the animal.')
    self.translations['profile_more_information'] = _('Holds a link to more information.')

    logger.info('Loaded TerrariumPI translations')

  def get_translation(self,translation):
    if translation in self.translations:
      return self.translations[translation]

    logger.warning('No translation available for \'%s\'' % (translation,))
    return 'No translation available for \'%s\'' % (translation,)

  def reload(self):
    logger.info('Reloading TerrariumPI translations')
    self.__load()
