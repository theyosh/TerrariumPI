# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

from datetime import datetime, timezone, timedelta
from pony import orm
from bottle import request, response, static_file, HTTPError
from json import dumps
from pathlib import Path
from ffprobe import FFProbe
from hashlib import md5
from uuid import uuid4
from ansi2html import Ansi2HTMLConverter

from terrariumArea         import terrariumArea
from terrariumAudio        import terrariumAudio
from terrariumDatabase     import Area, Audiofile, Button, Enclosure, Playlist, NotificationMessage, NotificationService, Relay, Sensor, SensorHistory, Setting, Webcam
from terrariumEnclosure    import terrariumEnclosure
from terrariumNotification import terrariumNotification, terrariumNotificationService

from hardware.button    import terrariumButton
from hardware.display   import terrariumDisplay
from hardware.relay     import terrariumRelay
from hardware.sensor    import terrariumSensor
from hardware.webcam    import terrariumWebcam

from terrariumUtils import terrariumUtils

# Set to false in production, else every API call that uses DB will produce a logline
DEBUG = False

class terrariumAPI(object):

  def __init__(self, webserver):
    self.webserver = webserver

  # Always (force = True) enable authentication on the API
  def authentication(self, force = True):
    return self.webserver.authenticate(force)

  def routes(self,bottle_app):

    # Area API
    bottle_app.route('/api/areas/types/',       'GET',    self.area_types,  apply=self.authentication(False), name='api:area_types')
    bottle_app.route('/api/areas/<area:path>/history/', 'GET',    self.area_detail_history, apply=self.authentication(False), name='api:area_history')

    bottle_app.route('/api/areas/<area:path>/', 'GET',    self.area_detail, apply=self.authentication(False), name='api:area_detail')


    bottle_app.route('/api/areas/<area:path>/', 'PUT',    self.area_update, apply=self.authentication(),      name='api:area_update')
    bottle_app.route('/api/areas/<area:path>/', 'DELETE', self.area_delete, apply=self.authentication(),      name='api:area_delete')
    bottle_app.route('/api/areas/',             'GET',    self.area_list,   apply=self.authentication(False), name='api:area_list')
    bottle_app.route('/api/areas/',             'POST',   self.area_add,    apply=self.authentication(),      name='api:area_add')


    # Audio API
    bottle_app.route('/api/audio/files/<audiofile:path>/', 'GET',    self.audiofile_detail, apply=self.authentication(False), name='api:audiofile_detail')
    bottle_app.route('/api/audio/files/<audiofile:path>/', 'DELETE', self.audiofile_delete, apply=self.authentication(),      name='api:audiofile_delete')
    bottle_app.route('/api/audio/files/',                  'GET',    self.audiofile_list,   apply=self.authentication(False), name='api:audiofile_list')
    bottle_app.route('/api/audio/files/',                  'POST',   self.audiofile_add,    apply=self.authentication(),      name='api:audiofile_add')
    bottle_app.route('/api/audio/hardware/',               'GET',    self.audio_hardware,   apply=self.authentication(False), name='api:audio_hardware')


    # Buttons API
    bottle_app.route('/api/buttons/<button:path>/history/<period:re:(day|week|month|year)>/', 'GET', self.button_history, apply=self.authentication(False), name='api:button_history_period')
    bottle_app.route('/api/buttons/<button:path>/history/', 'GET',    self.button_history,  apply=self.authentication(False), name='api:button_history')
    bottle_app.route('/api/buttons/hardware/',              'GET',    self.button_hardware, apply=self.authentication(),      name='api:button_hardware')
    bottle_app.route('/api/buttons/<button:path>/',         'GET',    self.button_detail,   apply=self.authentication(False), name='api:button_detail')
    bottle_app.route('/api/buttons/<button:path>/',         'PUT',    self.button_update,   apply=self.authentication(),      name='api:button_update')
    bottle_app.route('/api/buttons/<button:path>/',         'DELETE', self.button_delete,   apply=self.authentication(),      name='api:button_delete')
    bottle_app.route('/api/buttons/',                       'GET',    self.button_list,     apply=self.authentication(False), name='api:button_list')
    bottle_app.route('/api/buttons/',                       'POST',   self.button_add,      apply=self.authentication(),      name='api:button_add')


    # Calendar API
    bottle_app.route('/api/calendar/<calendar:path>/', 'GET',    self.calendar_detail,   apply=self.authentication(False), name='api:calendar_detail')
    bottle_app.route('/api/calendar/<calendar:path>/', 'PUT',    self.calendar_update,   apply=self.authentication(),      name='api:calendar_update')
    bottle_app.route('/api/calendar/<calendar:path>/', 'DELETE', self.calendar_delete,   apply=self.authentication(),      name='api:calendar_delete')
    bottle_app.route('/api/calendar/download/',        'GET',    self.calendar_download, apply=self.authentication(),      name='api:calendar_download')
    bottle_app.route('/api/calendar/',                 'GET',    self.calendar_list,     apply=self.authentication(False), name='api:calendar_list')
    bottle_app.route('/api/calendar/',                 'POST',   self.calendar_add,      apply=self.authentication(),      name='api:calendar_add')


    bottle_app.route('/api/displays/hardware/',        'GET',    self.display_hardware, apply=self.authentication(),      name='api:display_hardware')


    # Enclosure API
    bottle_app.route('/api/enclosures/<enclosure:path>/', 'GET',    self.enclosure_detail, apply=self.authentication(False), name='api:enclosure_detail')
    bottle_app.route('/api/enclosures/<enclosure:path>/', 'PUT',    self.enclosure_update, apply=self.authentication(),      name='api:enclosure_update')
    bottle_app.route('/api/enclosures/<enclosure:path>/', 'DELETE', self.enclosure_delete, apply=self.authentication(),      name='api:enclosure_delete')
    bottle_app.route('/api/enclosures/',                  'GET',    self.enclosure_list,   apply=self.authentication(False), name='api:enclosure_list')
    bottle_app.route('/api/enclosures/',                  'POST',   self.enclosure_add,    apply=self.authentication(),      name='api:enclosure_add')


    # Logfile API
    bottle_app.route('/api/logfile/download/', 'GET', self.logfile_download, apply=self.authentication(), name='api:logfile_download')


    # Notification API
    bottle_app.route('/api/notification/messages/types/',          'GET',    self.notification_message_types,  apply=self.authentication(), name='api:notification_message_types')
    bottle_app.route('/api/notification/messages/<message:path>/', 'GET',    self.notification_message_detail, apply=self.authentication(), name='api:notification_message_detail')
    bottle_app.route('/api/notification/messages/<message:path>/', 'PUT',    self.notification_message_update, apply=self.authentication(), name='api:notification_message_update')
    bottle_app.route('/api/notification/messages/<message:path>/', 'DELETE', self.notification_message_delete, apply=self.authentication(), name='api:notification_message_delete')
    bottle_app.route('/api/notification/messages/',                'GET',    self.notification_message_list,   apply=self.authentication(), name='api:notification_message_list')
    bottle_app.route('/api/notification/messages/',                'POST',   self.notification_message_add,    apply=self.authentication(), name='api:notification_message_add')
    bottle_app.route('/api/notification/services/types/',          'GET',    self.notification_service_types,  apply=self.authentication(), name='api:notification_service_types')
    bottle_app.route('/api/notification/services/<service:path>/', 'GET',    self.notification_service_detail, apply=self.authentication(), name='api:notification_service_detail')
    bottle_app.route('/api/notification/services/<service:path>/', 'PUT',    self.notification_service_update, apply=self.authentication(), name='api:notification_service_update')
    bottle_app.route('/api/notification/services/<service:path>/', 'DELETE', self.notification_service_delete, apply=self.authentication(), name='api:notification_service_delete')
    bottle_app.route('/api/notification/services/',                'GET',    self.notification_service_list,   apply=self.authentication(), name='api:notification_service_list')
    bottle_app.route('/api/notification/services/',                'POST',   self.notification_service_add,    apply=self.authentication(), name='api:notification_service_add')


    # Playlist API
    bottle_app.route('/api/playlists/<playlist:path>/', 'GET',    self.playlist_detail, apply=self.authentication(False), name='api:playlist_detail')
    bottle_app.route('/api/playlists/<playlist:path>/', 'PUT',    self.playlist_update, apply=self.authentication(),      name='api:playlist_update')
    bottle_app.route('/api/playlists/<playlist:path>/', 'DELETE', self.playlist_delete, apply=self.authentication(),      name='api:playlist_delete')
    bottle_app.route('/api/playlists/',                 'GET',    self.playlist_list,   apply=self.authentication(False), name='api:playlist_list')
    bottle_app.route('/api/playlists/',                 'POST',   self.playlist_add,    apply=self.authentication(),      name='api:playlist_add')


    # Reboot/start API
    bottle_app.route('/api/<action:re:(restart|reboot|shutdown)>/',   'POST', self.server_action, apply=self.authentication(), name='api:server_action')


    # Relays API
    bottle_app.route('/api/relays/<relay:path>/<action:re:(history)>/<period:re:(day|week|month|year|replaced)>/', 'GET', self.relay_history, apply=self.authentication(False), name='api:relay_history_period')
    bottle_app.route('/api/relays/<relay:path>/<action:re:(history)>/', 'GET',    self.relay_history,  apply=self.authentication(False), name='api:relay_history')

    bottle_app.route('/api/relays/<relay:path>/<action:re:(export)>/<period:re:(day|week|month|year|replaced)>/',  'GET', self.relay_history, apply=self.authentication(),      name='api:relay_export_period')
    bottle_app.route('/api/relays/<relay:path>/<action:re:(export)>/',  'GET',    self.relay_history,  apply=self.authentication(),      name='api:relay_export')

    bottle_app.route('/api/relays/<relay:path>/<action:re:(toggle|on|off|\d+)>/', 'POST',    self.relay_action,  apply=self.authentication(), name='api:relay_action')
    bottle_app.route('/api/relays/<relay:path>/manual/',   'POST',   self.relay_manual,           apply=self.authentication(), name='api:relay_manual')
    bottle_app.route('/api/relays/<relay:path>/replaced/', 'POST',   self.relay_replace_hardware, apply=self.authentication(), name='api:relay_replace_hardware')

    bottle_app.route('/api/relays/hardware/',              'GET',    self.relay_hardware, apply=self.authentication(),      name='api:relay_hardware')

    bottle_app.route('/api/relays/scan/',              'POST',    self.relay_scan, apply=self.authentication(),      name='api:relay_scan')

    bottle_app.route('/api/relays/<relay:path>/',          'GET',    self.relay_detail,   apply=self.authentication(False), name='api:relay_detail')
    bottle_app.route('/api/relays/<relay:path>/',          'PUT',    self.relay_update,   apply=self.authentication(),      name='api:relay_update')
    bottle_app.route('/api/relays/<relay:path>/',          'DELETE', self.relay_delete,   apply=self.authentication(),      name='api:relay_delete')
    bottle_app.route('/api/relays/',                       'GET',    self.relay_list,     apply=self.authentication(False), name='api:relay_list')
    bottle_app.route('/api/relays/',                       'POST',   self.relay_add,      apply=self.authentication(),      name='api:relay_add')


    # Sensors API
    all_sensor_types = '|'.join(terrariumSensor.sensor_types)
    bottle_app.route(f'/api/sensors/<filter:re:({all_sensor_types})>/<action:re:(history)>/<period:re:(day|week|month|year)>/', 'GET', self.sensor_history, apply=self.authentication(False), name='api:sensor_type_history_period')
    bottle_app.route(f'/api/sensors/<filter:re:({all_sensor_types})>/<action:re:(export)>/<period:re:(day|week|month|year)>/',  'GET', self.sensor_history, apply=self.authentication(),      name='api:sensor_type_export_period')
    bottle_app.route(f'/api/sensors/<filter:re:({all_sensor_types})>/<action:re:(history)>/', 'GET', self.sensor_history, apply=self.authentication(False), name='api:sensor_type_history')
    bottle_app.route(f'/api/sensors/<filter:re:({all_sensor_types})>/<action:re:(export)>/',  'GET', self.sensor_history, apply=self.authentication(),      name='api:sensor_type_export')
    bottle_app.route(f'/api/sensors/<filter:re:({all_sensor_types})>/',                       'GET', self.sensor_list,    apply=self.authentication(False), name='api:sensor_list_filtered')
    bottle_app.route('/api/sensors/<filter:path>/<action:re:(history)>/<period:re:(day|week|month|year)>/', 'GET', self.sensor_history, apply=self.authentication(False), name='api:sensor_history_period')
    bottle_app.route('/api/sensors/<filter:path>/<action:re:(export)>/<period:re:(day|week|month|year)>/',  'GET', self.sensor_history, apply=self.authentication(),      name='api:sensor_export_period')
    bottle_app.route('/api/sensors/<filter:path>/<action:re:(history)>/', 'GET',    self.sensor_history,  apply=self.authentication(False), name='api:sensor_history')
    bottle_app.route('/api/sensors/<filter:path>/<action:re:(export)>/',  'GET',    self.sensor_history,  apply=self.authentication(),      name='api:sensor_export')
    bottle_app.route('/api/sensors/hardware/',      'GET',    self.sensor_hardware, apply=self.authentication(),      name='api:sensor_hardware')
    bottle_app.route('/api/sensors/scan/',          'POST',    self.sensor_scan,    apply=self.authentication(),      name='api:sensor_scan')
    bottle_app.route('/api/sensors/<sensor:path>/', 'GET',    self.sensor_detail,   apply=self.authentication(False), name='api:sensor_detail')
    bottle_app.route('/api/sensors/<sensor:path>/', 'PUT',    self.sensor_update,   apply=self.authentication(),      name='api:sensor_update')
    bottle_app.route('/api/sensors/<sensor:path>/', 'DELETE', self.sensor_delete,   apply=self.authentication(),      name='api:sensor_delete')
    bottle_app.route('/api/sensors/',               'GET',    self.sensor_list,     apply=self.authentication(False), name='api:sensor_list')
    bottle_app.route('/api/sensors/',               'POST',   self.sensor_add,      apply=self.authentication(),      name='api:sensor_add')


    # Settings API
    bottle_app.route('/api/settings/<setting:path>/',       'GET',    self.setting_detail,                apply=self.authentication(), name='api:setting_detail')
    bottle_app.route('/api/settings/<setting:path>/',       'PUT',    self.setting_update,                apply=self.authentication(), name='api:setting_update')
    bottle_app.route('/api/settings/<setting:path>/',       'DELETE', self.setting_delete,                apply=self.authentication(), name='api:setting_delete')
#    bottle_app.route('/api/settings/profile_image/upload/', 'POST',   self.setting_upload_profile_image,  apply=self.authentication(), name='api:setting_upload_profile_image')
    bottle_app.route('/api/settings/',                      'PUT',    self.setting_update_multi,          apply=self.authentication(), name='api:setting_update_multi')
    bottle_app.route('/api/settings/',                      'GET',    self.setting_list,                  apply=self.authentication(), name='api:setting_list')
    bottle_app.route('/api/settings/',                      'POST',   self.setting_add,                   apply=self.authentication(), name='api:setting_add')


    # Status API
    bottle_app.route('/api/system_status/', 'GET', self.system_status, apply=self.authentication(False), name='api:system_status')


    # Weather API
    bottle_app.route('/api/weather/',          'GET', self.weather_detail,   apply=self.authentication(False), name='api:weather')
    bottle_app.route('/api/weather/forecast/', 'GET', self.weather_forecast, apply=self.authentication(False), name='api:weather_forecast')


    # Webcam API
    bottle_app.route('/api/webcams/<webcam:path>/archive/<period:path>',      'GET',    self.webcam_archive, apply=self.authentication(False),      name='api:webcam_archive')
    bottle_app.route('/api/webcams/hardware/',      'GET',    self.webcam_hardware, apply=self.authentication(),      name='api:webcam_hardware')
    bottle_app.route('/api/webcams/<webcam:path>/', 'GET',    self.webcam_detail,   apply=self.authentication(False), name='api:webcam_detail')
    bottle_app.route('/api/webcams/<webcam:path>/', 'PUT',    self.webcam_update,   apply=self.authentication(),      name='api:webcam_update')
    bottle_app.route('/api/webcams/<webcam:path>/', 'DELETE', self.webcam_delete,   apply=self.authentication(),      name='api:webcam_delete')
    bottle_app.route('/api/webcams/',               'GET',    self.webcam_list,     apply=self.authentication(False), name='api:webcam_list')
    bottle_app.route('/api/webcams/',               'POST',   self.webcam_add,      apply=self.authentication(),      name='api:webcam_add')


    # API DOC
    bottle_app.route('/<page:re:(api/redoc|api/swagger)>/', 'GET', self.webserver.render_page,   apply=self.authentication(False), name='api:documentation')

  # Areas
  def area_types(self):
    return { 'data' : terrariumArea.available_areas }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def area_list(self):
    data = []
    for area in Area.select(lambda r: not r.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.area_detail(area.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def area_detail(self, area):
    try:
      area = Area[area]
      area_data = area.to_dict(exclude='enclosure')
      area_data['enclosure'] = area.enclosure.id
      return area_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Area with id {area} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting area {area} detail. {ex}')

  def area_detail_history(self, area):
    area = self.area_detail(area)
    return self.sensor_history(list(area['setup']['sensors']))

  def __area_relay_check(self, api_data):
    update_ids = []
    if api_data.get('id') is not None:
      update_ids.append(api_data['id'])

    new_relays = []
    used_relays = []
    for part in ['day','night','low','high']:
      # Store relays from the post form data
      if part in api_data['setup'] and 'relays' in api_data['setup'][part] and len(api_data['setup'][part]['relays']) > 0:
        new_relays += api_data['setup'][part]['relays']

      # Get all the used relays in other areas
      for relay_data in orm.select(area.setup[part]['relays'] for area in Area if area.id not in update_ids and area.setup[part]['relays'] is not None and len(area.setup[part]['relays']) > 0):
        used_relays += relay_data

    duplicate = any(item in new_relays for item in used_relays)
    if duplicate:
      raise Exception('Duplicate relay usage. One or more relays are already used in other areas.')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def area_add(self):
    try:
      # Make sure the enclosure does exists
      _ = Enclosure[request.json['enclosure']]

      self.__area_relay_check(request.json)

      new_area = self.webserver.engine.add(terrariumArea(None, self.webserver.engine.enclosures[request.json['enclosure']], request.json['type'], request.json['name'], request.json['mode'], request.json['setup']))
      request.json['id'] = new_area.id

      area = Area(**request.json)

      return self.area_detail(area.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Enclosure with id {request.json["enclosure"]} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Area could not be added. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def area_update(self, area):
    try:
      area = Area[area]

      self.__area_relay_check(request.json)

      area.set(**request.json)
      orm.commit()

      self.webserver.engine.update(terrariumArea,**request.json)

      return self.area_detail(area.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Area with id {area} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating area {area}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def area_delete(self, area):
    try:
      area = Area[area]
      message = f'Area {area} is deleted.'

      area_id = area.id
      enclosure_id = area.enclosure.id
      area.delete()
      orm.commit()

      self.webserver.engine.delete(terrariumArea, area_id, enclosure_id)
      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Area with id {area} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting area {area}. {ex}')


  # Audiofiles
  def audio_hardware(self):
    return { 'data' : terrariumAudio.available_soundcards }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def audiofile_list(self):
    data = []
    for audiofile in Audiofile.select():
      data.append(audiofile.to_dict())

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def audiofile_detail(self, audiofile):
    try:
      audiofile = Audiofile[audiofile]
      audiofile_data = audiofile.to_dict()
      return audiofile_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Audio file with id {audiofile} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting audiofile {audiofile} detail. {ex}')

  def audiofile_add(self):
    __UPLOAD_PATH = 'media/'
    data = []
    try:
      for upload in request.files.getlist('audiofiles'):
        upload.save(__UPLOAD_PATH, overwrite=True)
        audio_file = Path(f'{__UPLOAD_PATH}{upload.filename}')
        meta_data = FFProbe(str(audio_file.resolve()))

        item = {
          'id'       : md5(f'{upload.filename}'.encode()).hexdigest(),
          'name'     : f'{meta_data.metadata.get("title",None)} - {meta_data.metadata.get("artist",None)}',
          'filename' : f'{audio_file.resolve()}',
          'duration' : meta_data.streams[0].duration,
          'filesize' : audio_file.stat().st_size
        }

        try:
          with orm.db_session:
            audiofile = Audiofile(**item)
        except orm.core.TransactionIntegrityError as e:
          if 'UNIQUE constraint failed' in str(e):
            with orm.db_session:
              audiofile = Audiofile[item['id']]
              audiofile.set(**item)

        data.append(item)

      return {'data' : data}
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting audio file {audiofile} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def audiofile_delete(self, audiofile):
    try:
      audiofile = Audiofile[audiofile]
      message = f'Audio file {audiofile.filename} is deleted.'
      audiofile.delete()
      orm.commit()
      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Audio file with id {audiofile} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting audiofile {audiofile}. {ex}')


  # Buttons
  def button_hardware(self):
    return { 'data' : terrariumButton.available_buttons }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def button_history(self, button, action = 'history', period = 'day'):
    try:
      button = Button[button]

      data = []

      if 'day' == period:
        period = 1
      elif 'week' == period:
        period = 7
      elif 'month' == period:
        period = 31
      elif 'year' == period:
        period = 365
      else:
        period = 1

      for item in button.history.filter(lambda h: h.timestamp >= datetime.now() - timedelta(days=period)):
        data.append({
          'timestamp' : item.timestamp.timestamp(),
          'value'     : item.value,
        })

      if 'export' == action:
        response.headers['Content-Type'] = 'application/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={button.name}_{period}.csv'

        # CSV Headers
        csv_data = ';'.join(data[0].keys()) + '\n'
        # Data
        for data_point in data:
          data_point['timestamp'] = datetime.fromtimestamp(data_point['timestamp'])
          csv_data += ';'.join([str(value) for value in data_point.values()]) + '\n'

        return csv_data

      return { 'data' : data }

    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Button with id {button} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting history for button {button}: {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def button_list(self):
    data = []
    for button in Button.select(lambda r: not r.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.button_detail(button.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def button_detail(self, button):
    try:
      button = Button[button]
      button_data = button.to_dict(exclude='enclosure')
      button_data['value']  = button.value
      return button_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Button with id {button} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting button {button}: {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def button_add(self):
    try:
      new_button = self.webserver.engine.add(terrariumButton(None, request.json['hardware'], request.json['address'], request.json['name']))
      request.json['id']      = new_button.id
      request.json['address'] = new_button.address

      button = Button(**request.json)
      new_value = new_button.update()
      button.update(new_value)

      return self.button_detail(button.id)
    except Exception as ex:
      raise HTTPError(status=500, body=f'Button could not be added: {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def button_update(self, button):
    try:
      button = Button[button]
      button.set(**request.json)
      orm.commit()
      self.webserver.engine.update(terrariumButton,**request.json)
      return self.button_detail(button.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Button with id {button} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating button {button}: {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def button_delete(self, button):
    try:
      message = f'Button {Button[button]} is deleted.'
      Button[button].delete()
      orm.commit()
      self.webserver.engine.delete(terrariumButton,button)
      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Button with id {button} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting button {button}: {ex}')


  # Calendar
  def calendar_detail(self,calendar):
    try:
      data = self.webserver.engine.calendar.get_event(calendar)
      if not data:
        # TODO: Make raising a CalendarNotFound exception
        raise HTTPError(status=404, body=f'Calender with id {calendar} does not exists.')

      # Convert uid to id field
      data['id'] = data['uid']
      del(data['uid'])
      return data
    except Exception as ex:
      raise HTTPError(status=500, body=f'Calender detail error. {ex}')

  def calendar_delete(self, calendar):
    data = self.calendar_detail(calendar)
    if not self.webserver.engine.calendar.delete_event(data['id']):
      raise HTTPError(status=500, body=f'Calender event {data["summary"]} could not be removed.')

    return {'message' : f'Calender event {data["summary"]} is deleted.'}

  def calendar_update(self, calendar):
    data = self.calendar_detail(calendar)
    for field in request.json:

      if field in ['dtstart','dtend'] and request.json[field]:
        data[field] = datetime.fromtimestamp(int(request.json[field])).replace(tzinfo=timezone.utc)
      else:
        data[field] = request.json[field]

    event = self.webserver.engine.calendar.create_event(
      data['id'],
      data['summary'],
      data['description'],
      data.get('location'),
      data['dtstart'],
      data.get('dtend'),

      data.get('freq'),
      data.get('interval')
    )

    return self.calendar_detail(event['uid'])

  def calendar_list(self):
    start = request.query.get('start', None)
    if start:
      start = datetime.fromisoformat(start)

    end = request.query.get('end', None)
    if end:
      end = datetime.fromisoformat(end)

    output = []
    for event in self.webserver.engine.calendar.get_events(start,end):
      output.append({
        'id'          : event['uid'],
        'title'       : event['summary'],
        'description' : event['description'],
        'start'       : datetime.fromtimestamp(event['dtstart'],timezone.utc).strftime('%Y-%m-%d'),
        'end'         : datetime.fromtimestamp(event['dtend'],timezone.utc).strftime('%Y-%m-%d'),
      })

    # https://stackoverflow.com/a/12294213
    response.content_type = 'application/json'
    return dumps(output)

  def calendar_add(self):
    event = self.webserver.engine.calendar.create_event(
      None,
      request.json['summary'],
      request.json['description'],
      request.json.get('location'),
      datetime.fromtimestamp(int(request.json['dtstart'])).replace(tzinfo=timezone.utc),
      None if request.json['dtend'] is None else datetime.fromtimestamp(int(request.json['dtend'])).replace(tzinfo=timezone.utc),
      request.json.get('freq'),
      request.json.get('interval'),
      request.json.get('repeatend')
    )

    return self.calendar_detail(event['uid'])

  def calendar_download(self):
    icalfile = self.webserver.engine.calendar.get_file().relative_to(Path(__file__).parent)
    return static_file(icalfile.name, root=icalfile.parent, download=icalfile.name)
  # End Calendar


  def display_hardware(self):
    return {'data' : terrariumDisplay.available_displays}


  # Enclosure
  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def enclosure_list(self):
    data = []
    for enclosure in Enclosure.select(lambda e: not e.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.enclosure_detail(enclosure.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def enclosure_detail(self, enclosure):
    try:
      enclosure = Enclosure[enclosure]
      enclosure_data = enclosure.to_dict(with_collections=True, related_objects=True)

      for area in list(enclosure_data['areas']):
        enclosure_data['areas'].remove(area)
        enclosure_data['areas'].append(area.to_dict(exclude='enclosure'))

      for door in list(enclosure_data['doors']):
        enclosure_data['doors'].remove(door)

        door_data = door.to_dict(exclude='enclosure')
        door_data['value'] = door.value

        enclosure_data['doors'].append(door_data)


      for webcam in list(enclosure_data['webcams']):
        enclosure_data['webcams'].remove(webcam)
        enclosure_data['webcams'].append(webcam.to_dict(exclude='enclosure'))

      return enclosure_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Enclosure with id {enclosure} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting enclosure {enclosure} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def enclosure_add(self):
    try:
      del(request.json['delete_image'])

      doors   = Button.select(lambda b: b.id in request.json['doors'])
      webcams = Webcam.select(lambda w: w.id in request.json['webcams'])

      # TODO: Swap logic! First try to create the enclosure in database, before loading it into the engine...
      new_enclosure = self.webserver.engine.add(terrariumEnclosure(None, request.json['name'], self.webserver.engine, request.json['doors']))

      request.json['id']      = new_enclosure.id
      request.json['doors']   = doors
      request.json['webcams'] = webcams
      enclosure = Enclosure(**request.json)

      return self.enclosure_detail(enclosure.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Door with id {request.json["doors"]} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Enclosure could not be added. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def enclosure_update(self, enclosure):
    try:
      enclosure = Enclosure[enclosure]
      doors     = Button.select(lambda b: b.id in request.json['doors'])
      webcams   = Webcam.select(lambda w: w.id in request.json['webcams'])

      # Check if we need to delete the image
      if request.json['delete_image']:
        enclosure.delete_image()
        request.json['image'] = ''

      del(request.json['delete_image'])

      # TODO: Will this work... not sure....
      self.webserver.engine.update(terrariumEnclosure,**request.json)

      request.json['doors'] = doors
      request.json['webcams'] = webcams

      enclosure.set(**request.json)
      orm.commit()

      return self.enclosure_detail(enclosure.id)
    # TODO: Make a better exception here. As it could be an enclosure, door or webcam exception
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Enclosure with id {enclosure} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating enclosure {enclosure}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def enclosure_delete(self, enclosure):
    try:
      message = f'Enclosure {Enclosure[enclosure]} is deleted.'
      Enclosure[enclosure].delete()
      orm.commit()
 #     self.webserver.engine.delete(terrariumEnclosure,enclosure)
      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Enclosure with id {enclosure} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting enclosure {enclosure}. {ex}')


  # Logfile
  def logfile_download(self):
    # https://stackoverflow.com/a/26017181
    logfile = Path(terrariumLogging.logging.getLogger().handlers[1].baseFilename)
    return static_file(logfile.name, root='log', mimetype='text/text', download=logfile.name)


  # Notifications
  def notification_message_types(self):
    return { 'data' : terrariumNotification.available_messages }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_message_detail(self, message):
    try:
      message = NotificationMessage[message]
      message_data = message.to_dict(with_collections=True)
      message_data['services'] = [self.notification_service_detail(service) for service in message_data['services']]
      return message_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Notification message with id {message} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting notification message with id {message} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_message_update(self, message):
    try:
      message = NotificationMessage[message]

      services = request.json['services'].split(',')
      request.json['services'] = NotificationService.select(lambda ns: ns.id in services)

      message.set(**request.json)
      orm.commit()

      return self.notification_message_detail(message.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Notification message with id {message} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating notification message with id {message}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_message_delete(self, message):
    try:
      title = f'Notification message {message} is deleted.'
      NotificationMessage[message].delete()
      orm.commit()

      return {'message' : title}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Notification message with id {message} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting notification message with id {message}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_message_list(self):
    data = []
    for message in NotificationMessage.select(lambda ns: not ns.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.notification_message_detail(message.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_message_add(self):
    try:
      request.json['services'] = NotificationService.select(lambda ns: ns.id in request.json['services'].split(','))
      request.json['id'] = str(uuid4())
      message = NotificationMessage(**request.json)

      return self.notification_message_detail(message.id)
    except Exception as ex:
      raise HTTPError(status=500, body=f'Notification message could not be added. {ex}')

  def notification_service_types(self):
    return { 'data' : terrariumNotificationService.available_services }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_service_detail(self, service):
    try:
      service = NotificationService[service]
      service_data = service.to_dict()

      return service_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Notification service with id {service} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting notification service with id {service} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_service_update(self, service):
    try:
      service = NotificationService[service]
      service.set(**request.json)
      orm.commit()

      self.webserver.engine.notification.reload_service(service.id,{**request.json})

      return self.notification_service_detail(service.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Notification service with id {service} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating notification service with id {service}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_service_delete(self, service):
    try:
      service = NotificationService[service]
      self.webserver.engine.notification.delete_service(service.id)
      message = f'Notification service {service} is deleted.'
      service.delete()
      orm.commit()

      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Notification service with id {service} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting notification service with id {service}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_service_list(self):
    data = []
    for service in NotificationService.select(lambda ns: not ns.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.notification_service_detail(service.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def notification_service_add(self):
    try:
      service = NotificationService(**request.json)
      orm.commit()

      self.webserver.engine.notification.load_services()

      return self.notification_service_detail(service.id)
    except Exception as ex:
      raise HTTPError(status=500, body=f'Notification service could not be added. {ex}')


  # Playlist
  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def playlist_list(self):
    data = []
    for playlist in Playlist.select(lambda p: not p.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.playlist_detail(playlist.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def playlist_detail(self, playlist):
    try:
      playlist = Playlist[playlist]
      playlist_data = playlist.to_dict(with_collections=True)
      playlist_data['length']   = playlist.length
      playlist_data['duration'] = playlist.duration

      return playlist_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Playlist with id {playlist} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting playlist {playlist} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def playlist_add(self):
    try:
      request.json['files'] = Audiofile.select(lambda af: af.id in request.json['files'])
      playlist = Playlist(**request.json)

      return self.playlist_detail(playlist.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Enclosure with id {request.json["enclosure"]} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Playlist could not be added. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def playlist_update(self, playlist):
    try:
      playlist = Playlist[playlist]
      request.json['files'] = Audiofile.select(lambda af: af.id in request.json['files'])
      playlist.set(**request.json)
      orm.commit()
      return self.playlist_detail(playlist.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Playlist with id {playlist} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating playlist {playlist}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def playlist_delete(self, playlist):
    try:
      message = f'Playlist {Playlist[playlist]} is deleted.'
      Playlist[playlist].delete()
      orm.commit()

      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Playlist with id {playlist} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting playlist {playlist}. {ex}')


  # Reboot/start API
  def server_action(self, action):
    if 'restart' == action:
      self.webserver.engine.restart()
      return { 'message' : f'TerrariumPI {self.webserver.engine.settings["version"]} is being restarted!' }
    elif 'reboot' == action:
      self.webserver.engine.reboot()
      return { 'message' : f'TerrariumPI {self.webserver.engine.settings["version"]} is being rebooted!' }
    elif 'shutdown' == action:
      self.webserver.engine.shutdown()
      return { 'message' : f'TerrariumPI {self.webserver.engine.settings["version"]} is being shutdown!' }


  # Relays
  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_action(self, relay, action = 'toggle'):
    try:
      relay = Relay[relay]
      self.webserver.engine.toggle_relay(relay,action)
      # Force to store the change, before sending the results back (which are cached due to orm.db_session)
      orm.commit()

      return self.relay_detail(relay.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Relay with id {relay} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting relay {relay} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_manual(self, relay):
    try:
      relay = Relay[relay]
      relay.manual_mode = not relay.manual_mode
      orm.commit()

      return self.relay_detail(relay.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Relay with id {relay} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating manual mode on relay {relay} detail. {ex}')


  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_replace_hardware(self, relay):
    try:
      relay = Relay[relay]
      relay.replacement = datetime.now()
      orm.commit()

      return self.relay_detail(relay.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Relay with id {relay} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating manual mode on relay {relay} detail. {ex}')


  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_history(self, relay, action = 'history', period = 'day'):
    try:
      relay = Relay[relay]

      data = []

      if 'day' == period:
        period = 1
      elif 'week' == period:
        period = 7
      elif 'month' == period:
        period = 31
      elif 'year' == period:
        period = 365
      elif 'replaced' == period:
        # We need to calculate back to days...
        period = (datetime.now() - relay.replacement).total_seconds() / (24.0 * 3600.0)
      else:
        period = 1

      for item in relay.history.filter(lambda h: h.timestamp >= datetime.now() - timedelta(days=period)):
        data.append({
          'timestamp' : item.timestamp.timestamp(),
          'value'     : item.value,
          'wattage'   : item.wattage,
          'flow'      : item.flow
        })

      if 'export' == action:
        response.headers['Content-Type'] = 'application/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={relay.name}_{period}.csv'

        # CSV Headers
        csv_data = ';'.join(data[0].keys()) + '\n'
        # Data
        for data_point in data:
          data_point['timestamp'] = datetime.fromtimestamp(data_point['timestamp'])
          csv_data += ';'.join([str(value) for value in data_point.values()]) + '\n'

        return csv_data

      return { 'data' : data }

    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Relay with id {relay} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'{ex}')

  def relay_hardware(self):
    return { 'data' : terrariumRelay.available_relays }

  def relay_scan(self):
    current_amount = len(self.webserver.engine.relays)
    self.webserver.engine.scan_new_relays()
    new = len(self.webserver.engine.relays) - current_amount
    return { 'message' : f'Found {new} new relays' }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_list(self):
    data = []
    for relay in Relay.select(lambda r: not r.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.relay_detail(relay.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_detail(self, relay):
    try:
      relay = Relay[relay]
      return relay.to_dict(exclude='webcam')
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Relay with id {relay} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting relay {relay} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_add(self):
    try:
      new_relay = self.webserver.engine.add(terrariumRelay(None, request.json['hardware'], request.json['address'], request.json['name']))
      if new_relay.is_dimmer:
        new_relay.calibrate(request.json['calibration'])

      request.json['id']      = new_relay.id
      request.json['address'] = new_relay.address

      relay = Relay(**request.json)
      new_value = new_relay.update()
      relay.update(new_value)

      return self.relay_detail(relay.id)
    except Exception as ex:
      raise HTTPError(status=500, body=f'Relay could not be added. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_update(self, relay):
    try:
      relay = Relay[relay]
      relay.set(**request.json)
      orm.commit()

      self.webserver.engine.update(terrariumRelay,**request.json)

      return self.relay_detail(relay.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Relay with id {relay} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating relay {relay}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def relay_delete(self, relay):
    try:
      message = f'Relay {Relay[relay]} is deleted.'
      Relay[relay].delete()
      orm.commit()

      self.webserver.engine.delete(terrariumRelay,relay)

      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Relay with id {relay} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting relay {relay}. {ex}')


  # Sensors
  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def sensor_history(self, filter = None, action = 'history', period = 'day'):
    data = []

    if 'day' == period:
      period = 1
    elif 'week' == period:
      period = 7
    elif 'month' == period:
      period = 31
    elif 'year' == period:
      period = 365
    else:
      period = 1

    if isinstance(filter, list):
      # Get history based on selected sensor IDs
      query = orm.select((sh.timestamp,
                          orm.avg(sh.value),
                          orm.avg(sh.alarm_min),
                          orm.avg(sh.alarm_max)) for sh in SensorHistory if  sh.sensor.id in filter
                                                                         and sh.exclude_avg == False
                                                                         and sh.timestamp >= datetime.now() - timedelta(days=period))

    elif filter in terrariumSensor.sensor_types:
      query = orm.select((sh.timestamp,
                          orm.avg(sh.value),
                          orm.avg(sh.alarm_min),
                          orm.avg(sh.alarm_max)) for sh in SensorHistory if  sh.sensor.type == filter
                                                                         and sh.exclude_avg == False
                                                                         and sh.timestamp >= datetime.now() - timedelta(days=period))

    else:
      query = orm.select((sh.timestamp,
                          sh.value,
                          sh.alarm_min,
                          sh.alarm_max,
                          sh.limit_min,
                          sh.limit_max) for sh in SensorHistory if  sh.sensor.id == filter
                                                                and sh.timestamp >= datetime.now() - timedelta(days=period))

    for item in query:
      data_point = {
        'timestamp' : item[0].timestamp(),
        'value'     : item[1],
        'alarm_min' : item[2],
        'alarm_max' : item[3]
      }
      if 'export' == action:
        data_point['limit_min'] = item[4]
        data_point['limit_max'] = item[5]
        data_point['alarm'] = not data_point['alarm_min'] <= data_point['value'] <= data_point['alarm_max']

      data.append(data_point)

    if 'export' == action:
      sensor = Sensor[filter]
      response.headers['Content-Type'] = 'application/csv'
      response.headers['Content-Disposition'] = f'attachment; filename={sensor.name}_{period}.csv'

      # CSV Headers
      csv_data = ';'.join(data[0].keys()) + '\n'
      # Data
      for data_point in data:
        data_point['timestamp'] = datetime.fromtimestamp(data_point['timestamp'])
        csv_data += ';'.join([str(value) for value in data_point.values()]) + '\n'

      return csv_data

    else:
      return { 'data' : data }

  def sensor_hardware(self):
    return { 'data' : terrariumSensor.available_sensors }

  def sensor_scan(self):
    current_amount = len(self.webserver.engine.sensors)
    self.webserver.engine.scan_new_sensors()
    new = len(self.webserver.engine.sensors) - current_amount
    return { 'message' : f'Found {new} new sensors' }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def sensor_list(self, filter = None):
    data = []
    for sensor in Sensor.select(lambda s: not s.id in self.webserver.engine.settings['exclude_ids']):
      if filter is None or filter == sensor.type:
        data.append(self.sensor_detail(sensor.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def sensor_detail(self, sensor):
    try:
      sensor = Sensor[sensor]
      return sensor.to_dict()
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Sensor with id {sensor} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting sensor {sensor} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def sensor_add(self):
    try:
      # Try to add a new sensor to the system
      new_sensor = self.webserver.engine.add(terrariumSensor(None, request.json['hardware'], request.json['type'], request.json['address'], request.json['name']))
      if 'chirp' == new_sensor.hardware.lower():
        # We need some moisture calibration for a Chirp sensor
        new_sensor.calibrate(request.json['calibration'])

      # The sensor will create a unique ID and can update the address
      request.json['id']      = new_sensor.id
      request.json['address'] = new_sensor.address

      sensor = Sensor(**request.json)
      new_value = new_sensor.update()
      sensor.update(new_value)

      return self.sensor_detail(sensor.id)
    except Exception as ex:
      raise HTTPError(status=500, body=f'Sensor could not be added. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def sensor_update(self, sensor):
    try:
      sensor = Sensor[sensor]
      sensor.set(**request.json)
      orm.commit()

      self.webserver.engine.update(terrariumSensor,**request.json)
      if 'chirp' == sensor.hardware.lower():
        # We need some moisture calibration for a Chirp sensor
        # TODO: This is a bad hack.....
        self.webserver.engine.sensors[sensor.id].calibrate(request.json['calibration'])

      return self.sensor_detail(sensor.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Sensor with id {sensor} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating sensor {sensor}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def sensor_delete(self, sensor):
    try:
      message = f'Sensor {Sensor[sensor]} is deleted.'
      Sensor[sensor].delete()
      orm.commit()
      self.webserver.engine.delete(terrariumSensor,sensor)
      return {'message' : message}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Sensor with id {sensor} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting sensor {sensor}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def setting_list(self):
    settings = []
    for setting in Setting.select():
      # Never give out this value in a list
      if setting.id in ['password','encryption_salt']:
        continue

      settings.append(self.setting_detail(setting.id))

    return { 'data' : settings }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def setting_detail(self, setting):
    if 'languages' == setting:
      return { 'languages' : self.webserver.engine.available_languages}

    try:
      data = Setting[setting].to_dict()
      if data['id'] in ['meross_cloud_username','meross_cloud_password']:
        data['value'] = terrariumUtils.decrypt(data['value'])
      elif 'exclude_ids' == data['id']:
        ids = data['value'].split(',')
        data['value'] = []

        for part in [Area, Enclosure, Button, Relay, Sensor, Webcam]:
          for item in part.select(lambda a: a.id in ids):
            data['value'].append({
              'id' : item.id,
              'name' : item.name
            })

      return data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Setting with id {setting} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error processing setting {setting}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def setting_add(self):
    try:
      if 'password' == request.json['id']:
        request.json['value'] = terrariumUtils.generate_password(request.json['value'])

      setting = Setting(**request.json)
      self.webserver.engine.load_settings()
      return setting.to_dict()
    except Exception as ex:
      raise HTTPError(status=400, body=f'Error adding new setting. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def setting_update(self, setting):
    try:
      data = Setting[setting]
      if 'exclude_ids' == data.id:
        tmp = data.value.strip(', ').split(',')
        if request.json['value'] in tmp:
          tmp.remove(request.json['value'])
        else:
          tmp.append(request.json['value'])

        request.json['value'] = ','.join(sorted(list(set(tmp)))).strip(', ')
      elif 'password' == data.id:
        request.json['value'] = terrariumUtils.generate_password(request.json['value'])

      data.set(**request.json)
      orm.commit()

      self.webserver.engine.load_settings()
      return data.to_dict()
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Setting with id {setting} does not exists.')
    except Exception as ex:
      raise HTTPError(status=400, body=f'Error updating new setting {setting}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def setting_update_multi(self):
    # First check if new password is set and is entered twice:
    if '' != request.json['password'] and request.json['password'] != request.json['password2']:
      raise HTTPError(status=400, body='Password fields do not match.')

    if terrariumUtils.is_true(request.json['delete_profile_image']):
      setting = Setting['profile_image']
      profile_image = Path(setting.value)
      if profile_image.exists() and profile_image.is_file():
        profile_image.unlink()

      request.json['profile_image'] = ''

    del(request.json['delete_profile_image'])

    # Delete the confirmation password
    del(request.json['password2'])
    # Delete normal password when empty so we keep the old one. Do not allow empty passwords
    if request.json['password'] == '':
      del(request.json['password'])

    for key in request.json.keys():
      try:
        setting = Setting[key]
        if 'password' == key:
          setting.value = terrariumUtils.generate_password(request.json[key])
        else:
          setting.value = request.json[key]

        orm.commit()

      except orm.core.ObjectNotFound:
        # Non existing setting can be ignored
        logger.debug(f'Database setting {key} does not exists.')

    self.webserver.engine.load_settings()
    return {'status' : True}

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def setting_delete(self, setting):
    try:
      Setting[setting].delete()
      orm.commit()
      return {'message' : f'Setting id {setting} is deleted.'}
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Setting with id {setting} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Setting {setting} could not be removed. {ex}')


  # System
  def system_status(self):
    data = self.webserver.engine.system_stats()
    conv = Ansi2HTMLConverter()
    motd_text = Path('motd.sh').read_text().split('\n')
    motd_text = motd_text[1:-1]
    data['summary'] = conv.convert("\n".join(motd_text).replace('echo "','').replace('\`','`'), full=True)
    return data


  # Weather
  def weather_detail(self):
    weather = {}

    if self.webserver.engine.weather:
      weather = {
        'location'   : self.webserver.engine.weather.location,
        'sun'        : {'rise' : self.webserver.engine.weather.sunrise.timestamp(),
                        'set'  : self.webserver.engine.weather.sunset.timestamp()},
        'is_day'     : self.webserver.engine.weather.is_day,
        'indicators' : {'wind' : self.webserver.engine.units['windspeed'],
                        'temperature' : self.webserver.engine.units['temperature']},
        'credits'    : self.webserver.engine.weather.credits,
        'forecast'   : self.webserver.engine.weather.short_forecast
      }

    return weather

  def weather_forecast(self):
    forecast_data = []

    if self.webserver.engine.weather:
      for forecast in self.webserver.engine.weather.forecast:
        forecast_data.append({
          'value'       : forecast['temperature'],
          'temperature' : forecast['temperature'],
          'humidity'    : forecast['humidity'],
          'timestamp'   : forecast['timestamp']
        })

    return {'data' : forecast_data}


  # Webcams
  def webcam_hardware(self):
    return { 'data' : terrariumWebcam.available_webcams }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def webcam_archive(self, webcam, period = None):
    try:
      webcam = Webcam[webcam]
      webcam_data = self.webcam_detail(webcam.id)

      if period is None:
        period = datetime.now().strftime('%Y/%m/%d')

      archive_path = Path(webcam.archive_path) / period
      webcam_data['archive_images'] = [f'/{archive_file}' for archive_file in sorted(archive_path.glob('*.jpg'), reverse=True)]

      return webcam_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Webcam with id {webcam} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting webcam {webcam} archive images. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def webcam_list(self):
    data = []
    for webcam in Webcam.select(lambda w: not w.id in self.webserver.engine.settings['exclude_ids']):
      data.append(self.webcam_detail(webcam.id))

    return { 'data' : data }

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def webcam_detail(self, webcam):
    try:
      webcam = Webcam[webcam]
      webcam_data = webcam.to_dict(exclude='enclosure',with_collections=True)
      webcam_data['is_live'] = webcam.is_live
      return webcam_data
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Webcam with id {webcam} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error getting webcam {webcam} detail. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def webcam_add(self):
    try:
      new_webcam = self.webserver.engine.add(terrariumWebcam(None,
                                                             request.json['address'],
                                                             request.json['name'],
                                                             request.json['width'],
                                                             request.json['height'],
                                                             request.json['rotation'],
                                                             request.json['awb']))

      request.json['id']       = new_webcam.id
      request.json['hardware'] = new_webcam.HARDWARE
      request.json['address']  = new_webcam.address
      # After loading some remote webcams, we could have a different resolution then entered
      request.json['width']    = new_webcam.width
      request.json['height']   = new_webcam.height

      request.json['flash']    = Relay.select(lambda r: r.id in request.json['flash'])

      webcam = Webcam(**request.json)

      # TODO: Fix updating or not. For now, disabled, as it can take up to 12 sec for RPICam
      return self.webcam_detail(webcam.id)
    except Exception as ex:
      raise HTTPError(status=500, body=f'Webcam could not be added. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def webcam_update(self, webcam):
    try:
      webcam = Webcam[webcam]
      request.json['flash'] = Relay.select(lambda r: r.id in request.json['flash'])
      webcam.set(**request.json)
      orm.commit()

      self.webserver.engine.update(terrariumWebcam,**request.json)

      return self.webcam_detail(webcam.id)
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Webcam with id {webcam} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error updating webcam {webcam}. {ex}')

  @orm.db_session(sql_debug=DEBUG,show_values=DEBUG)
  def webcam_delete(self, webcam):
    try:
      message = f'Webcam {Webcam[webcam]} is deleted.'
      Webcam[webcam].delete()
      orm.commit()
      self.webserver.engine.delete(terrariumWebcam,webcam)
      return message
    except orm.core.ObjectNotFound:
      raise HTTPError(status=404, body=f'Webcam with id {webcam} does not exists.')
    except Exception as ex:
      raise HTTPError(status=500, body=f'Error deleting webcam {webcam}. {ex}')
