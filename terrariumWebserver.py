# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import gettext
gettext.install('terrariumpi', 'locales/')

try:
  import thread as _thread
except ImportError as ex:
  import _thread
import json
import os
import datetime
import hashlib
import functools

from bottle import BaseRequest, Bottle, request, abort, static_file, template, error, response, auth_basic, HTTPError
#Increase bottle memory to max 5MB to process images in WYSIWYG editor
BaseRequest.MEMFILE_MAX = 5 * 1024 * 1024

from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from queue import Queue
from gevent import sleep

from terrariumTranslations import terrariumTranslations
from terrariumAudio import terrariumAudioPlayer
from terrariumUtils import terrariumUtils

class terrariumWebserverHeaders(object):
  name = 'webserver_headers'
  api = 2

  def apply(self, fn, context):
    def webserver_headers(*args, **kwargs):
      template_file = 'views' + request.fullpath[:-5] + '.tpl'
      if os.path.isfile(template_file):
        t = os.path.getmtime(template_file)
        #response.headers['Expires'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        response.headers['Last-Modified'] = datetime.datetime.fromtimestamp(t).strftime( '%a, %d %b %Y %H:%M:%S GMT')
        response.headers['Etag'] = hashlib.md5(response.headers['Last-Modified'].encode()).hexdigest()

      return fn(*args, **kwargs)

    return webserver_headers

class terrariumWebserver(object):

  app = Bottle()
  app.install(terrariumWebserverHeaders())

  def __init__(self, terrariumEngine):
    self.__terrariumEngine = terrariumEngine
    self.__app = terrariumWebserver.app
    self.__config = self.__terrariumEngine.get_config('system')
    self.__caching_days = 30
    terrariumWebserver.app.terrarium = self.__terrariumEngine
    # Load language
    gettext.translation('terrariumpi', 'locales/', languages=[self.__terrariumEngine.config.get_language()]).install(True)
    self.__translations = terrariumTranslations()

    self.__routes()

  # Custom HTTP authentication routine. This way there is an option to optional secure the hole web interface
  def __auth_basic2(self, check, required, realm="private", text="Access denied"):
    """ Callback decorator to require HTTP auth (basic).
        TODO: Add route(check_auth=...) parameter. """

    def decorator(func):

      @functools.wraps(func)
      def wrapper(*a, **ka):

        if required or terrariumUtils.is_true(self.__terrariumEngine.config.get_system()['always_authenticate']):
          user, password = request.auth or (None, None)
          ip = request.remote_addr if request.get_header('X-Real-Ip') is None else request.get_header('X-Real-Ip')
          if user is None or not check(user, password):
            err = HTTPError(401, text)
            err.add_header('WWW-Authenticate', 'Basic realm="%s"' % realm)
            if user is not None or password is not None:
              self.__terrariumEngine.notification.message('authentication_warning',{'ip' : ip, 'username' : user, 'password' : password},[])
              logger.warning('Incorrect login detected using username \'{}\' and password \'{}\' from ip {}'.format(user,password,ip))
            return err

        return func(*a, **ka)

      return wrapper

    return decorator

  def __authenticate(self, required):
    return self.__auth_basic2(self.__terrariumEngine.authenticate,required,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))

  def __logout_authenticate(self, user, password):
    return True

  def __routes(self):
    self.__app.route('/',
                     method="GET",
                     callback=self.__render_page,
                     apply=self.__authenticate(False))

    self.__app.route('/<template_name:re:[^/]+\.html$>',
                     method="GET",
                     callback=self.__render_page,
                     apply=self.__authenticate(False))

    self.__app.route('/<filename:re:robots\.txt>',
                     method="GET",
                     callback=self.__static_file)

    self.__app.route('/<root:re:static/extern>/<filename:path>',
                     method="GET",
                     callback=self.__static_file)

    self.__app.route('/<root:re:(static|gentelella|webcam|audio|log)>/<filename:path>',
                     method="GET",
                     callback=self.__static_file,
                     apply=self.__authenticate(False))

    self.__app.route('/api/<path:re:config.*>',
                     method=['GET'],
                     callback=self.__get_api_call,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/<path:path>',
                     method=['GET'],
                     callback=self.__get_api_call,
                     apply=self.__authenticate(False))

    self.__app.route('/api/calendar',
                     method=['POST'],
                     callback=self.__create_calender_event,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/reboot',
                     method=['POST'],
                     callback=self.__reboot,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/shutdown',
                     method=['POST'],
                     callback=self.__shutdown,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/switch/toggle/<switchid:path>',
                     method=['POST'],
                     callback=self.__toggle_switch,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/switch/manual_mode/<switchid:path>',
                     method=['POST'],
                     callback=self.__manual_mode_switch,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/switch/state/<switchid:path>/<value:int>',
                     method=['POST'],
                     callback=self.__state_switch,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/config/switches/hardware',
                     method=['PUT'],
                     callback=self.__replace_switch_hardware,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/config/<path:re:(system|weather|switches|sensors|webcams|doors|audio|environment|profile|notifications)>',
                     method=['PUT','POST','DELETE'],
                     callback=self.__update_api_call,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/audio/player/<action:re:(start|stop|volumeup|volumedown|mute|unmute)>',
                     method=['POST'],
                     callback=self.__player_commands,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/audio/file',
                     method=['POST'],
                     callback=self.__upload_audio_file,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/api/audio/file/<audiofileid:path>',
                     method=['DELETE'],
                     callback=self.__delete_audio_file,
                     apply=self.__authenticate(True)
                    )

    self.__app.route('/logout',
                     method=['GET'],
                     callback=self.__logout_url,
                     apply=auth_basic(self.__logout_authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

  def __reboot(self):
    terrariumUtils.get_script_data('sudo reboot')

  def __shutdown(self):
    terrariumUtils.get_script_data('sudo shutdown')

  def __template_variables(self, template):
    variables = { 'lang' : self.__terrariumEngine.config.get_language(),
                  'title' : self.__config['title'],
                  'version' : self.__config['version'],
                  'page_title' : _(template.replace('_',' ').capitalize()),
                  'temperature_indicator' : self.__terrariumEngine.get_temperature_indicator(),
                  'distance_indicator' : self.__terrariumEngine.get_distance_indicator(),
                  'volume_indicator' : self.__terrariumEngine.get_volume_indicator(),
                  'horizontal_graph_legend' : 1 if self.__terrariumEngine.get_horizontal_graph_legend() else 0,
                  'translations': self.__translations,
                  'device': self.__terrariumEngine.device,
                  'notifications' : self.__terrariumEngine.notification,
                  'show_gauge_overview' : 1 if self.__terrariumEngine.get_show_gauge_overview() else 0,
                  'hide_environment' : self.__terrariumEngine.get_hide_environment_on_dashboard(),
                  'graph_smooth_value' : self.__terrariumEngine.get_graph_smooth_value(),
                  'graph_show_min_max_gauge': 1 if self.__terrariumEngine.get_graph_show_min_max_gauge() else 0}

    if 'index' == template or 'profile' == template:
      variables['person_name'] = self.__terrariumEngine.get_profile_name()
      variables['person_image'] = self.__terrariumEngine.get_profile_image()

    return variables

  def __render_page(self,template_name = 'index.html'):
    template_name = template_name[:-5]

    if not os.path.isfile('views/' + template_name + '.tpl'):
      template_name = '404'

    return template(template_name,**self.__template_variables(template_name))

  def __static_file(self,filename, root = 'static'):
    if filename == 'js/terrariumpi.js':
      response.headers['Content-Type'] = 'application/javascript; charset=UTF-8'
      response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(days=self.__caching_days)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      return template(filename,template_lookup=[root])

    staticfile = static_file(filename, root=root)
    if isinstance(staticfile,HTTPError):
      return staticfile

    if 'webcam' == root or 'log' == root:
      staticfile.add_header('Expires',datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
      if 'log' == root:
        staticfile.add_header('Content-Type','text/text; charset=UTF-8')
        staticfile.add_header('Content-Disposition','Attachment;filename=' + filename)
    else:
      staticfile.add_header('Expires',(datetime.datetime.utcnow() + datetime.timedelta(days=self.__caching_days)).strftime('%a, %d %b %Y %H:%M:%S GMT'))

    if staticfile.get_header('Last-Modified') is not None:
      staticfile.add_header('Etag',hashlib.md5(staticfile.get_header('Last-Modified').encode()).hexdigest())

    return staticfile

  def __player_commands(self,action):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Player command could ot be executed!')}

    if 'start' == action:
      self.__terrariumEngine.audio_player_start()
    elif 'stop' == action:
      self.__terrariumEngine.audio_player_stop()
    elif 'volumeup' == action:
      self.__terrariumEngine.audio_player_volume_up()
      result = {'ok' : True, 'title' : _('OK!'), 'message' : _('Player command executed!')}
    elif 'volumedown' == action:
      self.__terrariumEngine.audio_player_volume_down()
      result = {'ok' : True, 'title' : _('OK!'), 'message' : _('Player command executed!')}
    elif 'mute' == action:
      pass
    elif 'unmute' == action:
      pass

    return result;

  def __upload_audio_file(self):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('File is not uploaded!')}
    upload = request.files.get('file')
    try:
      upload.save(terrariumAudioPlayer.AUDIO_FOLDER)
      self.__terrariumEngine.reload_audio_files()
      result = {'ok' : True, 'title' : _('Success!'), 'message' : _('File \'%s\' is uploaded') % (upload.filename,)}
    except IOError as message:
      result['message'] = _('Duplicate file \'%s\'') % (upload.filename,)

    return result

  def __delete_audio_file(self,audiofileid):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Action could not be satisfied')}

    if self.__terrariumEngine.delete_audio_file(audiofileid):
      result = {'ok' : True, 'title' : _('Success!'), 'message' : _('Audio file is deleted')}

    return result

  def __update_api_call(self,path):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Data could not be saved')}
    postdata = {}

    if request.json is not None:
      postdata = request.json

    result['ok'] = self.__terrariumEngine.set_config(path,postdata,request.files)
    if result['ok']:
      result['title'] = _('Data saved')
      result['message'] = _('Your changes are saved')

      # Reload language if needed
      if 'language' in postdata:
        gettext.translation('terrariumpi', 'locales/', languages=[self.__terrariumEngine.config.get_language()]).install(True)
        self.__translations.reload()

    return result

  def __replace_switch_hardware(self):
    postdata = None
    if request.json is not None:
      postdata = request.json

    self.__terrariumEngine.replace_hardware_calender_event(postdata['switch']['id'],
                                                           postdata['switch']['device'],
                                                           postdata['switch']['reminder_amount'],
                                                           postdata['switch']['reminder_period'])
    result = {'ok' : True,
              'title' : _('Hardware is replaced'),
              'message' : _('Hardware replacement is logged in the calendar')}

    if '' != postdata['switch']['reminder_amount']:
      result['message'] += '<br />' + _('A new replacement reminder is created')

    return result

  def __create_calender_event(self):
    postdata = None
    if request.json is not None:
      postdata = request.json

    if 'daterangepicker_start' not in postdata:
      postdata['daterangepicker_start'] = postdata['calendar_date']

    if 'daterangepicker_end' not in postdata:
      postdata['daterangepicker_end'] = postdata['calendar_date']

    self.__terrariumEngine.create_calendar_event(postdata['calendar_title'],
                                                 postdata['calendar_description'],
                                                 None,
                                                 postdata['daterangepicker_start'],
                                                 postdata['daterangepicker_end'],
                                                 None if 'calendar_id' not in postdata else postdata['calendar_id'])
    result = {'ok' : True,
              'title' : _('Calender event created'),
              'message' : _('The calender event is created')}

    return result

  def __get_api_call(self,path):
    response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(seconds=10)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    response.headers['Access-Control-Allow-Origin'] = '*'

    result = {}
    parameters = path.strip('/').split('/')

    action = parameters[0]
    del(parameters[0])

    if 'switches' == action:
      result = self.__terrariumEngine.get_switches(parameters)

    elif 'doors' == action:
      if len(parameters) > 0 and parameters[0] == 'status':
         result = {'status' : self.__terrariumEngine.get_doors_status()}
      else:
        result = self.__terrariumEngine.get_doors()

    elif 'profile' == action:
      result = self.__terrariumEngine.get_profile()

    elif 'calendar' == action:
      if 'ical' in parameters:
        response.headers['Content-Type'] = 'text/calendar'
        response.headers['Content-Disposition'] = 'attachment; filename=terrariumpi.ical.ics'

      response.headers['Content-Type'] = 'application/json'
      result = json.dumps(self.__terrariumEngine.get_calendar(parameters,**{'start':request.query.get('start'),'end':request.query.get('end')}))

    elif 'sensors' == action:
      result = self.__terrariumEngine.get_sensors(parameters)

    elif 'webcams' == action:
      result = self.__terrariumEngine.get_webcams(parameters)

    elif 'audio' == action:
      if len(parameters) > 0 and parameters[0] == 'files':
        del(parameters[0])
        result = self.__terrariumEngine.get_audio_files(parameters)
      elif len(parameters) > 0 and parameters[0] == 'playing':
        del(parameters[0])
        result = self.__terrariumEngine.get_audio_playing()
      elif len(parameters) > 0 and parameters[0] == 'hardware':
        del(parameters[0])
        result = {'audiohardware' : terrariumAudioPlayer.get_sound_cards()}
      else:
        result = self.__terrariumEngine.get_audio_playlists(parameters)

    elif 'environment' == action:
      result = self.__terrariumEngine.get_environment(parameters)

    elif 'weather' == action:
      result = self.__terrariumEngine.get_weather(parameters)

    elif 'uptime' == action:
      result = self.__terrariumEngine.get_uptime()

    elif 'power_usage' == action:
      result = self.__terrariumEngine.get_power_usage_water_flow()['power']

    elif 'water_usage' == action:
      result = self.__terrariumEngine.get_power_usage_water_flow()['water']

    elif 'system' == action:
      result = self.__terrariumEngine.get_system_stats()

    elif 'config' == action:
      # TODO: New way of data processing.... fix other config options
      result = self.__terrariumEngine.get_config(parameters[0] if len(parameters) == 1 else None)

    elif 'history' == action or 'export' == action:
      response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      if 'export' == action:
        parameters.append('all')
      result = self.__terrariumEngine.get_history(parameters)

      if 'export' == action:
        csv = ''
        export_name = 'error'
        for datatype in result:
          for dataid in result[datatype]:
            export_name = datatype + '_' + dataid + '.csv'
            # Header
            fields = list(result[datatype][dataid].keys())
            if 'totals' in fields:
              fields.remove('totals')
            csv = '"' + '","'.join(['timestamp'] + fields) + "\"\n"

            for counter in range(0,len(result[datatype][dataid][fields[0]])):
              # Timestamp
              row = [datetime.datetime.fromtimestamp(int(str(int(result[datatype][dataid][fields[0]][counter][0]/1000)))).strftime('%Y-%m-%d %H:%M:%S')]
              for field in fields:
                # Row values
                row.append(str(result[datatype][dataid][field][counter][1]))

              csv += '"' + '","'.join(row) + "\"\n"

        response.headers['Content-Type'] = 'application/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=' + export_name
        return csv

    return result

  def __toggle_switch(self,switchid):
    if switchid in self.__terrariumEngine.power_switches:
      self.__terrariumEngine.power_switches[switchid].toggle()
      return {'ok' : True}

    return {'ok' : False}

  def __manual_mode_switch(self,switchid):
    if switchid in self.__terrariumEngine.power_switches:
      self.__terrariumEngine.power_switches[switchid].set_manual_mode(not self.__terrariumEngine.power_switches[switchid].in_manual_mode())
      self.__terrariumEngine.config.save_power_switch(self.__terrariumEngine.power_switches[switchid].get_data())
      return {'ok' : True}

    return {'ok' : False}

  def __state_switch(self,switchid,value):
    if switchid in self.__terrariumEngine.power_switches:
      if value == 1:
        self.__terrariumEngine.power_switches[switchid].set_state(True)
        return {'ok' : True}
      elif value == 0:
        self.__terrariumEngine.power_switches[switchid].set_state(False)
        return {'ok' : True}
      else:
        self.__terrariumEngine.power_switches[switchid].set_state(value)
        return {'ok' : True}

    return {'ok' : False}

  def __logout_url(self):
    return {'ok'      : True,
            'title'   : _('Log out'),
            'message' : _('You are now logged out')
           }

  @app.error(404)
  def error404(error):
    config = terrariumWebserver.app.terrarium.get_config('system')
    variables = { 'lang' : terrariumWebserver.app.terrarium.config.get_language(),
                  'title' : config['title'],
                  'version' : config['version'],
                  'page_title' : config['title'] + ' | 404'
                }

    return template('404',**variables)

  @app.route('/live', apply=[websocket])
  def handle_websocket(socket):
    messages = Queue()

    def listen_for_messages(messages,socket):
      while True:
        message = messages.get()

        try:
          socket.send(json.dumps(message))
        except Exception as ex:
          # Socket connection is lost, stop looping....
          break

        messages.task_done()

    while True:
      try:

        message = socket.receive()
      except Exception as ex:
        break

      if message is not None:
        message = json.loads(message)

        if message['type'] == 'client_init':
          _thread.start_new_thread(listen_for_messages, (messages,socket))
          terrariumWebserver.app.terrarium.subscribe(messages)

        terrariumWebserver.app.terrarium.get_doors_status(socket=True)
        terrariumWebserver.app.terrarium.get_uptime(socket=True)
        terrariumWebserver.app.terrarium.get_environment(socket=True)
        terrariumWebserver.app.terrarium.get_power_usage_water_flow(socket=True)

  def start(self):
    # Start the webserver
    logger.info('Running webserver at %s:%s' % (self.__config['host'],self.__config['port']))
    print('%s - INFO    - terrariumWebserver   - Running webserver at %s:%s' % (datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S,000'),
                                             self.__config['host'],
                                             self.__config['port']))
    self.__app.run(host=self.__config['host'],
                   port=self.__config['port'],
                   server=GeventWebSocketServer,
                   debug=True,
                   reloader=False,
                   quiet=True)
