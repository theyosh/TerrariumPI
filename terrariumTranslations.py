# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from terrariumWeather import terrariumWeather
from terrariumSensor import terrariumSensor
from terrariumSwitch import terrariumPowerSwitch
from terrariumDoor import terrariumDoor
from terrariumWebcam import terrariumWebcam

class terrariumTranslations(object):

  def __init__(self):
    logger.info('Initialize TerariumPI translations')
    self.translations = {}
    self.__load()

  def __load(self):
    logger.debug('Loading TerariumPI translations')
    # Weather
    weather_sources = terrariumWeather.valid_sources()
    self.translations['weather_field_location'] = _('Holds the external source URL. Supported sources are: %s.') % ('<strong>' + '</strong>, <strong>'.join(list(weather_sources.keys())) + '</strong>')

    weather_sources_list = ''
    for weather_source in weather_sources:
      weather_sources_list += '<li><strong>{}</strong>: {}</li>'.format(weather_source,weather_sources[weather_source])

    self.translations['weather_field_location_long'] = self.translations['weather_field_location'] + '<ul>' + weather_sources_list + '</ul>'
    self.translations['weather_field_wind_speed'] = _('Choose the wind speed indicator. The software will recalculate to the chosen indicator.')
    # End weather

    # Calendar
    self.translations['calendar_title'] = _('Holds the title of the calendar event.')
    self.translations['calendar_description'] = _('Holds the body of the calendar event. You can include images.')
    # End Calendar

    # Sensors
    self.translations['sensor_field_hardware'] = _('Holds the sensor hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSensor.valid_hardware_types()) + '</strong>')
    self.translations['sensor_field_address'] = _('Holds the sensor address. Depending on hardware type, it is either a read only hex number, a GPIO pin, a GPIO pin combination of %s or a full HTTP(S) address. Full url specification can be found on the %s wiki page. For GPIO use <strong>physical</strong> GPIO pin numbering.') % ('<a href="https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi" target="_blank">\'<i>TRIG,ECHO</i>\'</a>','<a href="https://github.com/theyosh/TerrariumPI/wiki/Remote-data#temperature-and-humidity-sensors" target="_blank">\'<i>' + _('Remote data') + '</i>\'</a>')
    self.translations['sensor_field_type'] = _('Holds the sensor type. Supported sensor types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumSensor.valid_sensor_types()) + '</strong>')
    self.translations['sensor_field_name'] = _('Holds the name of the sensor.')
    self.translations['sensor_field_alarm_min'] = _('Holds the sensor lower alarm value of the sensor. When below this value, alarms can be triggered.')
    self.translations['sensor_field_alarm_max'] = _('Holds the sensor maximum alarm value of the sensor. When above this value, alarms can be triggered.')
    self.translations['sensor_field_limit_min'] = _('Holds the sensor lowest value that should be used in the graphs.')
    self.translations['sensor_field_limit_max'] = _('Holds the sensor maximum value that should be used in the graphs.')
    self.translations['sensor_field_current'] = _('Shows the sensor current value in temperature or humidity (read only).')
    self.translations['sensor_field_min_moist'] = _('Holds the sensor lowest moisture value measured in dry air. %s') % ('<a href="https://github.com/ageir/chirp-rpi#calibration" target="_blank" title="' + _('More calibration information') + '"><i>' + _('More calibration information') + '</i></a>')
    self.translations['sensor_field_max_moist'] = _('Holds the sensor highest moisture value measured in full water. %s') % ('<a href="https://github.com/ageir/chirp-rpi#calibration" target="_blank" title="' + _('More calibration information') + '"><i>' + _('More calibration information') + '</i></a>')
    self.translations['sensor_field_temperature_offset'] = _('Holds the temperature offset value.')
    self.translations['sensor_field_max_diff'] = _('Holds the maximum number that a sensor may change in value up or down.')
    # End sensors

    # Switches
    self.translations['switch_field_hardware'] = _('Holds the switch hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumPowerSwitch.valid_hardware_types()) + '</strong>')
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
    self.translations['switch_new_device'] = _('Enter the name of the hardware device that has been replace. Will be used for title in the reminder.')
    self.translations['switch_reminder_amount'] = _('Enter the amount of days/weeks/months/years to reminder.')
    self.translations['switch_reminder_period'] = _('Enter the period type.')
    # End switches

    # Doors
    self.translations['door_field_hardware'] = _('Holds the door hardware type. Supported hardware types are: %s.') % ('<strong>' + '</strong>, <strong>'.join(terrariumDoor.VALID_HARDWARE_TYPES) + '</strong>')
    self.translations['door_field_address'] = _('Holds the door address. When using GPIO use <strong>physical</strong> GPIO pin numbering as address.')
    self.translations['door_field_name'] = _('Holds the door name.')
    # End doors

    # Webcam
    self.translations['webcam_field_location'] = _('Holds the webcam location source. Supported sources are: %s') % ('<strong>RPICam</strong>, <strong>V4L device</strong>, <strong>Remote URL</strong>, <strong>Local URL</strong>')
    self.translations['webcam_field_name'] = _('Holds the webcam name.')
    self.translations['webcam_field_resolution'] = _('Holds the webcam resolution.')
    self.translations['webcam_field_resolution_width'] = _('Holds the webcam resolution width in pixels.')
    self.translations['webcam_field_resolution_height'] = _('Holds the webcam resolution height in pixels.')
    self.translations['webcam_field_rotation'] = _('Holds the webcam rotation of the image.')
    self.translations['webcam_field_awb'] = _('Select the white balance type. Only for Raspberry PI camera\'s.')
    self.translations['webcam_field_preview'] = _('Shows the webcam preview image.')
    self.translations['webcam_field_archive'] = _('Enabled or disable image archiving based on motion detection.')
    self.translations['webcam_field_archive_light'] = _('Select the environment light state when enabling archiving.')
    self.translations['webcam_field_archive_door'] = _('Select the environment door state when enabling archiving.')
    self.translations['webcam_field_motion_boxes'] = _('Enable or disable motion boxes for Motion archiving.')
    self.translations['webcam_field_motion_delta_threshold'] = _('Minimum difference between frames to be identified as motion. Higher value means that the image must be more different for motion to be detected.')
    self.translations['webcam_field_motion_min_area'] = _('Minimum area of an image in pixels for a region to be considered motion. Larger values mean that only larger areas will be detected as motion.')
    self.translations['webcam_field_motion_compare_frame'] = _('Last frame means that only consecutive frames will be compared for motion. Last archived frame means that the current frame will be compared to the last archived frame. Setting to last frame will ignore motion when it is very gradual.')
    self.translations['webcam_realtime_sensors_list'] = _('Select the sensors to show at the marker place on the webcam.')
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
    self.translations['environment_field_mode'] = _('Select the mode on which this environment part be put on and off. Select \'%s\' to use the sun rise and sun set at your location. This will make the amount of lighting variable to the actual amount of daylight. When selecting \'%s\', the light will put on and off at selected times.') % (_('Weather'),_('Timer'))
    self.translations['environment_field_sensors'] = _('Select the sensors that are used to control this environment part. When selecting multiple sensors, the average is calculated to determine the final values.')
    self.translations['environment_field_day_night_difference'] = _('Holds the value in degrees which the sensors are changing when it become night. Use positive numbers to increase the values and negative numbers to lower the values.')
    self.translations['environment_field_day_night_source'] = _('Holds the source that is used to determing when it is day or night.')
    self.translations['environment_field_start'] = _('Enter the time when this environment part should be put on. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_stop'] = _('Enter the time when this environment part should be put off. Only available when running in \'%s\' mode.') % _('Timer')
    self.translations['environment_field_on_duration'] = _('Holds the period in minutes that this environment part is powered on withing the total timer window.')
    self.translations['environment_field_off_duration'] = _('Holds the period in minutes that this environment part is powered off withing the total timer window.')
    self.translations['environment_field_delay'] = _('How much time must there be between two actions and after start up. Enter the amount of seconds in which this environment part can settle.')
    self.translations['environment_field_power_on_duration'] = _('Holds the amount of seconds that this environment part is powered on when the value is out of range.')
    self.translations['environment_field_lights_max_hours'] = _('Enter the maximum amount of time in hours. When the time between on and off is more then this maximum, the on and off time will be shifted more to each other.')
    self.translations['environment_field_lights_min_hours'] = _('Enter the minimum amount of time in hours. When the time between on and off is less then this amount of hours, the on and off time will be widened until the minimum amount of hours entered here.')
    self.translations['environment_field_lights_hour_shift'] = _('Enter the amount of hours that the power on and off times should shift. Is only needed when running in the \'%s\' mode. Enter a positive number for adding hours to the start time. Use negative numbers for subtracting from the start time.') % _('Weather')
    self.translations['environment_field_power_switches'] = _('Select the power switches that should be used when the alarms or timers are hit. Select all needed switches below.')
    self.translations['environment_field_watertank_volume'] = _('Holds the water volume in liters.')
    self.translations['environment_field_watertank_height'] = _('Holds the water tank height in cm or inches.')
    self.translations['environment_field_watertank_offset'] = _('Holds the distance between top of the liquid when full and the sensor in cm or inches.')
    self.translations['environment_field_light_state'] = _('Select when the power switches can toggle. When lights are on, off or just always')
    self.translations['environment_field_door_state'] = _('Select when the power switches can toggle. When the door is open, cosed or just always')
    # End environment

    # Notifications
    self.translations['notification_email_receiver'] = _('Holds the email address on which you would like to receive messages.')
    self.translations['notification_email_server'] = _('Holds the mail server hostname or IP.')
    self.translations['notification_email_serverport'] = _('Holds the mail server portnumber. SSL and TLS will be autodetected.')
    self.translations['notification_email_email_username'] = _('Holds the username for authentication with the mailserver if needed.')
    self.translations['notification_email_email_password'] = _('Holds the password for authentication with the mailserver if needed.')

    self.translations['notification_display_hardwaretype'] = _('Holds the display chip that is used.')
    self.translations['notification_display_address'] = _('Holds the I2C address of the LCD screen. Use the value found with i2cdetect. Add ,[NR] to change the I2C bus.')
    self.translations['notification_display_title'] = _('Reserve first LCD line for static title.')

    self.translations['notification_twitter_consumer_key'] = _('Holds your Twitter consumer key. More information %shere%s') % ('<a href=\'https://apps.twitter.com/\' target=\'_blank\'>','</a>')
    self.translations['notification_twitter_consumer_secret'] = _('Holds your Twitter consumer secret. More information %shere%s') % ('<a href=\'https://apps.twitter.com/\' target=\'_blank\'>','</a>')
    self.translations['notification_twitter_access_token'] = _('Holds your Twitter access token. More information %shere%s') % ('<a href=\'https://apps.twitter.com/\' target=\'_blank\'>','</a>')
    self.translations['notification_twitter_access_token_secret'] = _('Holds your Twitter access token secret. More information %shere%s') % ('<a href=\'https://apps.twitter.com/\' target=\'_blank\'>','</a>')

    self.translations['notification_pushover_api_token'] = _('Holds the PushOver API token. More information %shere%s') % ('<a href=\'https://pushover.net/api\' target=\'_blank\'>','</a>')
    self.translations['notification_pushover_user_key'] =  _('Holds the PushOver API user key. More information %shere%s') % ('<a href=\'https://pushover.net/api\' target=\'_blank\'>','</a>')

    self.translations['notification_telegram_bot_token'] =  _('Holds the Telegram Bot token. More information %shere%s') % ('<a href=\'https://core.telegram.org/bots#6-botfather\' target=\'_blank\'>','</a>')
    self.translations['notification_telegram_username'] =  _('Holds the Telegram username that is allowed for receiving messages. Can be multiple usernames seperated by a comma. More information %shere%s') % ('<a href=\'https://core.telegram.org/bots#6-botfather\' target=\'_blank\'>','</a>')
    self.translations['notification_telegram_proxy'] =  _('Holds the proxy address in form of [schema]://[user]:[password]@[server.com]:[port]. Can either be socks5 or http(s) for schema.')

    self.translations['notification_webhook_address'] =  _('Holds the url to post notification data to. You can use %name% variables in the post url')

    # End notifications

    # System
    self.translations['system_field_language'] = _('Choose your interface language.')
    self.translations['system_field_distance_indicator'] = _('Holds the distance type used by distance sensors.')
    self.translations['system_field_admin'] = _('Holds the username which can make changes (Administrator).')
    self.translations['system_field_admin'] = _('Holds the username which can make changes (Administrator).')
    self.translations['system_field_new_password'] = _('Enter the new password for the administration user. Leaving empty will not change the password!')
    self.translations['system_field_current_password'] = _('Enter the current password in order to change the password.')
    self.translations['system_field_always_authentication'] = _('Toggle on or off full authentication. When on, you need to authenticate at all times.')
    self.translations['system_field_external_calendar_url'] = _('Holds the external calendar url.')
    self.translations['system_field_horizontal_graph_legend'] = _('Toggle on or off horizontal graph legends. Reload the web interface after changing the setting.')
    self.translations['system_field_hide_environment_on_dashboard'] = _('Toggle on or off the environment summary on the dashboard. Reload the web interface after changing the setting.')
    self.translations['system_field_soundcard'] = _('Holds the soundcard that is used for playing audio.')
    self.translations['system_field_pi_power'] = _('Holds the amount of power in Wattage that the Raspberry PI uses including all USB equipment.')
    self.translations['system_field_power_price'] = _('Holds the amount of euro/dollar per 1 kW/h (1 Kilowatt per hour).')
    self.translations['system_field_water_price'] = _('Holds the amount of euro/dollar per 1000 liters water.')
    self.translations['system_field_temperature_indicator'] = _('Choose the temperature indicator. The software will recalculate to the chosen indicator.')
    self.translations['system_field_windspeed_indicator'] = _('Choose the windspeed indicator. The software will recalculate to the chosen indicator.')
    self.translations['system_field_volume_indicator'] = _('Choose the volume (liquid) indicator. The software will recalculate to the chosen indicator.')
    self.translations['system_field_hostname'] = _('Holds the host name or IP address on which the software will listen for connections. Enter :: for all addresses to bind.')
    self.translations['system_field_port_number'] = _('Holds the port number on which the software is listening for connections.')
    self.translations['system_field_meross_username'] = _('Enter the e-mail address that is used for your Meross devices.')
    self.translations['system_field_meross_password'] = _('Enter the password that is used for your Meross devices. Password is stored in plain text!')
    self.translations['system_field_graph_smooth_value'] = _('Holds the amount of data points (each 30 sec) to use for smoothing. The higher the value, the smoother the graph. Enter 0 to disable. Reload the web interface after changing the setting.')
    self.translations['system_field_all_sensors_gauges_page'] = _('Select true or false to show an extra sensor page which holds all the sensors with there gauges. Reload the web interface after changing the setting.')
    self.translations['system_field_graph_show_min_max_gauge'] = _('Toggle on or off the min and max measured value in the gauge graphs.')
    # End system


    self.translations['profile_name'] = _('Holds the name of the animal.')
    self.translations['profile_type'] = _('Holds the type of the animal')
    self.translations['profile_gender'] = _('Holds the gender of the animal.')
    self.translations['profile_age'] = _('Holds the day of birth of the animal.')
    self.translations['profile_species'] = _('Holds the species name of the animal.')
    self.translations['profile_latin_name'] = _('Holds the latin name of the animal.')
    self.translations['profile_description'] = _('Holds a small description about the animal.')
    self.translations['profile_more_information'] = _('Holds a link to more information.')

    logger.info('Loaded TerrariumPI with %s translations' % (len(self.translations),))

  def get_translation(self,translation):
    if translation in self.translations:
      return self.translations[translation]

    logger.warning('No translation available for \'%s\'' % (translation,))
    return 'No translation available for \'%s\'' % (translation,)

  def reload(self):
    logger.info('Reloading TerrariumPI translations')
    self.__load()
