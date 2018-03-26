# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

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
    self.translations['sensor_field_hardware'] = _('Holds the sensor hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSensor.VALID_HARDWARE_TYPES) + '</strong>')
    self.translations['sensor_field_address'] = _('Holds the sensor address. Depending on hardware type, it is either a read only hex number, a GPIO pin, a GPIO pin combination of %s or a full HTTP(S) adress. Full url specification can be found on the %s wiki page. For GPIO use <strong>physical</strong> GPIO pin numbering.') % ('<a href="https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi" target="_blank">\'<i>TRIG,ECHO</i>\'</a>','<a href="https://github.com/theyosh/TerrariumPI/wiki/Remote-data#temperature-and-humidity-sensors" target="_blank">\'<i>' + _('Remote data') + '</i>\'</a>')
    self.translations['sensor_field_type'] = _('Holds the sensor type. Supported sensor types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSensor.VALID_SENSOR_TYPES) + '</strong>')
    self.translations['sensor_field_name'] = _('Holds the name of the sensor.')
    self.translations['sensor_field_alarm_min'] = _('Holds the sensor lower alarm value of the sensor. When below this value, alarms can be triggered.')
    self.translations['sensor_field_alarm_max'] = _('Holds the sensor maximum alarm value of the sensor. When above this value, alarms can be triggered.')
    self.translations['sensor_field_limit_min'] = _('Holds the sensor lowest value that should be used in the graphs.')
    self.translations['sensor_field_limit_max'] = _('Holds the sensor maximum value that should be used in the graphs.')
    self.translations['sensor_field_current'] = _('Shows the sensor current value in temperature or humidity (read only).')
    # End sensors

    # Switches
    self.translations['switch_field_hardware'] = _('Holds the switch hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSwitch.VALID_HARDWARE_TYPES) + '</strong>')
    self.translations['switch_field_address'] = _('Holds the switch address. Depending on hardware type, it is either a number or GPIO pin. For GPIO and PWM-Dimmer use <strong>physical</strong> GPIO pin numbering.')
    self.translations['switch_field_name'] = _('Holds the switch name.')
    self.translations['switch_field_power_wattage'] = _('Holds the switch power usage in Watt when switched on.')
    self.translations['switch_field_water_flow'] = _('Holds the switch water flow in liters per minute when switched on')
    self.translations['switch_field_timer_enabled'] = _('Enable or disable timer functionality. When enabled you can specify the timing below.')
    self.translations['switch_field_timer_start'] = _('Holds the timer start time. The timer will run after this start time.')
    self.translations['switch_field_timer_stop'] = _('Holds the timer stop time. The timer will stop after this start time.')
    self.translations['switch_field_timer_on_duration'] = _('Holds the period in minutes that the power switch is on withing the total timer window.')
    self.translations['switch_field_timer_off_duration'] = _('Holds the period in minutes that the power switch is off withing the total timer window.')
    self.translations['switch_field_dimmer_duration'] = _('Holds the amount of seconds for the duration in which the dimmer changes to the new value.')
    self.translations['switch_field_dimmer_step'] = _('Holds the amount in percentage to change the dimmer by the heater environment.')
    self.translations['switch_field_dimmer_on_duration'] = _('Holds the amount of seconds for the duration in which it increases the power.')
    self.translations['switch_field_dimmer_on_percentage'] = _('Holds the amount in percentage to go to when switched on.')
    self.translations['switch_field_dimmer_off_duration'] = _('Holds the amount of seconds for the duration in which it decresses the power.')
    self.translations['switch_field_dimmer_off_percentage'] = _('Holds the amount in percentage to go to when switched off.')
    # End switches

    # Doors
    self.translations['door_field_hardware'] = _('Holds the door hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumDoor.VALID_HARDWARE_TYPES) + '</strong>')
    self.translations['door_field_address'] = _('Holds the door address. When using GPIO use <strong>physical</strong> GPIO pin numbering as address.')
    self.translations['door_field_name'] = _('Holds the door name.')
    # End doors

    # Webcam
    self.translations['webcam_field_location'] = _('Holds the webcam location source. Supported sources are: %s') % ('<strong>RPICam</strong>, <strong>V4L device</strong>, <strong>Remote URL</strong>')
    self.translations['webcam_field_name'] = _('Holds the webcam name.')
    self.translations['webcam_field_resolution'] = _('Holds the webcam resolution.')
    self.translations['webcam_field_resolution_width'] = _('Holds the webcam resolution width in pixels.')
    self.translations['webcam_field_resolution_height'] = _('Holds the webcam resolution height in pixels.')
    self.translations['webcam_field_rotation'] = _('Holds the webcam rotation of the image.')
    self.translations['webcam_field_preview'] = _('Shows the webcam preview image.')
    # End webcam

    # Audio
    self.translations['audio_playlist_field_name'] = _('Holds the audio playlist name.')
    self.translations['audio_playlist_field_start'] = _('Holds the time when the playlist should be started.')
    self.translations['audio_playlist_field_stop'] = _('Holds the time when the playlist should be stopped.')
    self.translations['audio_playlist_field_volume'] = _('Holds the volume for this playlist.')
    self.translations['audio_playlist_field_repeat'] = _('Toggle on to enable repeating of the audio files.')
    self.translations['audio_playlist_field_shuffle'] = _('Toggle on to enable shuffeling of the audio files.')
    self.translations['audio_playlist_field_files'] = _('Select the audio files for this playlist. It is possible to select the same audio file in multiple playlists.')
    # End Audio

    # Environment
    self.translations['environment_field_lights_mode'] = _('Select the mode on which the lights will be put on and off. Select \'%s\' to use the sun rise and sun set at your location. This will make the amount of lighting variable to the actual amount of daylight. When selecting \'%s\', the light will put on and off at selected times.') % (_('Weather'),_('Timer'))
    self.translations['environment_field_lights_on'] = _('Enter the time when the light should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_lights_off'] = _('Enter the time when the lights should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_lights_on_duration'] = _('Holds the period in minutes that the lights are on withing the total timer window.')
    self.translations['environment_field_lights_off_duration'] = _('Holds the period in minutes that the lights are off withing the total timer window')
    self.translations['environment_field_lights_max_hours'] = _('Enter the maximum amount of lights time in hours. When the time between on and off is more then this maximum, the on and off time will be shifted more to each other.')
    self.translations['environment_field_lights_min_hours'] = _('Enter the minimum amount of lights time in hours. When the time between on and off is less then this amount of hours, the on and off time will be widened until the minimum amount of hours entered here.')
    self.translations['environment_field_lights_hour_shift'] = _('Enter the amount of hours that the lights should shift. Is only needed when running in the \'%s\' mode. Enter a positive number for adding hours to the start time. Use negative numbers for subtracting from the start time.') % _('Weather')
    self.translations['environment_field_lights_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the lights. Select all needed switches below.')


    self.translations['environment_field_sprayer_enable_during_night'] = _('Enable spraying when the lights are off. This can cause water flow when there is not enough heat to vaporize the water.')
    self.translations['environment_field_sprayer_mode'] = _('Select the operating mode.')

    self.translations['environment_field_sprayer_on_duration'] = _('Holds the period in minutes that the sprayer is on withing the total timer window.')
    self.translations['environment_field_sprayer_off_duration'] = _('Holds the period in minutes that the sprayer is off withing the total timer window')
    self.translations['environment_field_sprayer_delay'] = _('How much time must there be between two spray actions and after start up. Enter the amount of seconds in which the humidity can settle.')
    self.translations['environment_field_sprayer_duration'] = _('How long is the system spraying. Enter the amount of seconds that the system is on when the humidity is too low.')
    self.translations['environment_field_sprayer_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the sprayer. Select all needed switches below.')
    self.translations['environment_field_sprayer_humidity_sensors'] = _('Select the humidity sensors that are used to control the humidity. When selecting multiple sensors, the average is calculated to determine the final humidity.')


    self.translations['environment_field_watertank_mode'] = _('Select the operating mode. Use \'%s\' mode to select the time period in which the water pump is running. Select \'%s\' mode to use the sun rise and sun set as on and off times. Use \'%s\' mode to have the water pump running when the water level is to low.') % (_('Timer'),_('Weather'),_('Sensor'))
    self.translations['environment_field_watertank_on'] = _('Enter the time when the water pump should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_watertank_off'] = _('Enter the time when the water pump should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_watertank_on_duration'] = _('Holds the period in minutes that the watertank is on withing the total timer window.')
    self.translations['environment_field_watertank_off_duration'] = _('Holds the period in minutes that the watertank is off withing the total timer window')
    self.translations['environment_field_watertank_duration'] = _('How long is the system pumping water. Enter the amount of seconds that the system is on when the water level is too low.')
    self.translations['environment_field_watertank_volume'] = _('Holds the water volume in liters.')
    self.translations['environment_field_watertank_height'] = _('Holds the water tank height in cm or inches.')
    self.translations['environment_field_watertank_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the watertank. Select all needed switches below.')
    self.translations['environment_field_watertank_distance_sensors'] = _('Select the distance sensors that are used to control the level. When selecting multiple sensors, the average is calculated to determine the final distance.')


    self.translations['environment_field_heater_enable_during_day'] = _('Enable heating when the lights are on. This can cause overheating when the lights are on.')
    self.translations['environment_field_heater_mode'] = _('Select the operating mode. Use \'%s\' mode to select the time period in which the heating is running. Select \'%s\' mode to use the sun rise and sun set as on and off times. When the sun rises the heating system will stop. Use \'%s\' mode to have the heating running when the lights are off.') % (_('Timer'),_('Weather'),_('Sensor'))
    self.translations['environment_field_heater_on'] = _('Enter the time when the heater should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_heater_off'] = _('Enter the time when the heater should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_heater_on_duration'] = _('Holds the period in minutes that the heater is on withing the total timer window.')
    self.translations['environment_field_heater_off_duration'] = _('Holds the period in minutes that the heater is off withing the total timer window')
    self.translations['environment_field_heater_settle_timeout'] = _('Holds the period in seconds in which the heating will wait to settle the new temperature before changing again.')
    self.translations['environment_field_heater_night_difference'] = _('Holds the dirrence in degrees that the night temperature should change. Use positive and negative values.')
    self.translations['environment_field_heater_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the heater. Select all needed switches below.')
    self.translations['environment_field_heater_temperature_sensors'] = _('Select the temperature sensors that are used to control the temperature. When selecting multiple sensors, the average is calculated to determine the final temperature.')


    self.translations['environment_field_cooler_enable_during_night'] = _('Enable cooling when the lights are off. This can cause a very low temperature when the lights are off.')
    self.translations['environment_field_cooler_mode'] = _('Select the operating mode. Use \'%s\' mode to select the time period in which the heating is running. Select \'%s\' mode to use the sun rise and sun set as on and off times. When the sun rises the heating system will stop. Use \'%s\' mode to have the heating running when the lights are off.') % (_('Timer'),_('Weather'),_('Sensor'))
    self.translations['environment_field_cooler_on'] = _('Enter the time when the cooler should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_cooler_off'] = _('Enter the time when the cooler should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_cooler_on_duration'] = _('Holds the period in minutes that the cooler is on withing the total timer window.')
    self.translations['environment_field_cooler_off_duration'] = _('Holds the period in minutes that the cooler is off withing the total timer window')
    self.translations['environment_field_cooler_power_switches'] = _('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the cooler. Select all needed switches below.')
    self.translations['environment_field_cooler_temperature_sensors'] = _('Select the temperature sensors that are used to control the temperature. When selecting multiple sensors, the average is calculated to determine the final temperature.')
    # End environment

    # System
    self.translations['system_field_language'] = _('Choose your interface language.')
    self.translations['system_field_distance_indicator'] = _('Holds the distance type used by distance sensors.')
    self.translations['system_field_admin'] = _('Holds the username which can make changes (Administrator).')
    self.translations['system_field_admin'] = _('Holds the username which can make changes (Administrator).')
    self.translations['system_field_new_password'] = _('Enter the new password for the administration user. Leaving empty will not change the password!')
    self.translations['system_field_current_password'] = _('Enter the current password in order to change the password.')
    self.translations['system_field_always_authentication'] = _('Toggle on or off full authentication. When on, you need to authenticate at all times.')
    self.translations['system_field_external_calendar_url'] = _('Holds the external calendar url.')
    self.translations['system_field_soundcard'] = _('Holds the soundcard that is used for playing audio.')
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

    logger.info('Loaded TerrariumPI %s translations' % (len(self.translations),))

  def get_translation(self,translation):
    if translation in self.translations:
      return self.translations[translation]

    logger.warning('No translation available for \'%s\'' % (translation,))
    return 'No translation available for \'%s\'' % (translation,)

  def reload(self):
    logger.info('Reloading TerrariumPI translations')
    self.__load()
