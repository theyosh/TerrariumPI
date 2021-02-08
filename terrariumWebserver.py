# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import gettext
import threading
import json
import os
import datetime
import hashlib
import functools
import re

from uuid import uuid4
from pathlib import Path
from hashlib import md5

from bottle import BaseRequest, Bottle, default_app, request, abort, redirect, static_file, jinja2_template, url, error, response, auth_basic, HTTPError, RouteBuildError
#Increase bottle memory to max 5MB to process images in WYSIWYG editor
BaseRequest.MEMFILE_MAX = 5 * 1024 * 1024

from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from queue import Queue
from gevent import sleep

from terrariumUtils import terrariumUtils
from terrariumAPI import terrariumAPI

class terrariumWebserver(object):

  def __init__(self, terrariumEngine):
    # Define caching timeouts per url/path
    self.__caching_timeouts = [
      {'path' : re.compile(r'^/webcam/.*\.m3u8$',re.I), 'timeout':                 1}, # 1 Second
      {'path' : re.compile(r'^/webcam/.*\.ts$',re.I),   'timeout':                10}, # 10 Seconds
      {'path' : re.compile(r'^/webcam/.*\.jpg$',re.I),  'timeout':                30}, # 30 Seconds
      {'path' : re.compile(r'^/static/assets/',re.I),   'timeout': 30 * 24 * 60 * 60}, # 1 Month
      {'path' : re.compile(r'^/api/',re.I),             'timeout':                60}, # 1 Minute
#      {'path' : re.compile(r'^.html$',re.I),            'timeout':           60 * 60}, # 1 Hour
    ]

    # This secret will change every reboot. So cookies will not work anymore after a reboot.
    self.cookie_secret = uuid4().bytes
    self.bottle        = default_app() # This is needed to get the APISpec BottlePlugin to work
    self.engine        = terrariumEngine
    self.websocket     = terrariumWebsocket(self)
    self.api           = terrariumAPI(self)

    # Load language
    gettext.translation('terrariumpi', 'locales/', languages=[self.engine.settings['language']]).install(True)

    # Load the routes
    self.__routes()

  # Custom HTTP authentication routine. This way there is an option to optional secure the hole web interface
  def __auth_basic(self, check, required, realm="private", text="Access denied"):
    """ Callback decorator to require HTTP auth (basic).
        TODO: Add route(check_auth=...) parameter. """

    def decorator(func):

      @functools.wraps(func)
      def wrapper(*a, **ka):
        if required or terrariumUtils.is_true(self.engine.settings['always_authenticate']):
          user, password = request.auth or (None, None)
          ip = request.remote_addr if request.get_header('X-Real-Ip') is None else request.get_header('X-Real-Ip')
          if user is None or not check(user, password):
            err = HTTPError(401, text)
            err.add_header('WWW-Authenticate', f'Basic realm="{realm}"')
            if user is not None or password is not None:
              self.engine.notification.message('authentication_warning',{'ip' : ip, 'username' : user, 'password' : password},[])
              logger.warning(f'Incorrect login detected using username \'{user}\' and password \'{password}\' from ip {ip}')
            return err

        if 'get' == request.method.lower() and request.url.lower().endswith('.html'):
          user, password = request.get_cookie('auth', secret=self.cookie_secret) or (None, None)
          if check(user, password):
            # Update the cookie timeout so that we are staying logged in as long as we are working on the interface
            response.set_cookie('auth', request.get_cookie('auth', secret=self.cookie_secret), secret=self.cookie_secret, **{ 'max_age' : 3600, 'path' : '/'})

          self.__add_caching_heders(response,request.fullpath)

        return func(*a, **ka)

      return wrapper

    return decorator

  def __clear_authentication(self, user, password):
    return True

  def __add_caching_heders(self, response, fullpath):
    if 200 == response.status_code:
      # Add the caching headers
      for caching in self.__caching_timeouts:
        if caching['path'].search(request.fullpath):
          response.expires = datetime.datetime.utcnow().timestamp() + caching['timeout']
          response.set_header('Cache-Control', f'public, max-age={caching["timeout"]}')

        elif re.search(r'\.html$',request.fullpath,re.I):
          response.set_header('Cache-Control', 'no-cache')
          response.set_header('Etag', md5(response.body.encode()).hexdigest())

  def __template_variables(self, template):
    def unit_variables():
      units = {}
      for unit in self.engine.units:
        units[unit] = {
          'name': _(unit),
          'value' : self.engine.units[unit]
        }

      return units

    def authenticated_cookie(cookie_data):
      if cookie_data is None:
        return False

      if len(cookie_data) != 2:
        return False

      return self.engine.authenticate(cookie_data[0],cookie_data[1])

    # Variables
    variables = {
      'authenticated' : authenticated_cookie(request.get_cookie('auth', secret=self.cookie_secret)),
      'lang'          : self.engine.settings['language'],
      'title'         : self.engine.settings['title'],
      'version'       : self.engine.settings['version'],
#                  'page_title'    : _(template.replace('_',' ').replace('.html','').capitalize()),
      'template'      : template,
      'device'        : self.engine.settings['device'],
      'username'      : self.engine.settings['username'],
      'profile_image' : self.engine.settings['profile_image'],

      'languages'     : self.engine.settings['languages'],
      'units'         : unit_variables(),

#                  'translations': self.__translations,
#                  'notifications' : self.engine.notification,
#                  'horizontal_graph_legend' : 1 if self.engine.get_horizontal_graph_legend() else 0,

      'show_gauge_overview'      : self.engine.settings['all_gauges_on_single_page'],
      'show_environment'         : not self.engine.settings['hide_environment_dashboard'],
      'graph_smooth_value'       : self.engine.settings['graph_smooth_value'],
      'graph_show_min_max_gauge' : 1 if self.engine.settings['show_min_max_gauge'] else 0
    }

    # Template functions
    variables['url_for'] = self.url_for
    variables['_']  = _

    return variables

  def render_page(self, page = 'index'):
    page_name = None
    if page.endswith('_sensors'):
      page_name = page
      page = 'sensors'

    page = Path(f'views/{page}.html')
    if not page.is_file():
      return HTTPError(404, 'Page does not exist.')

    if page_name is None:
      page_name = page.name

    variables = self.__template_variables(page_name)
    variables['ajax'] = request.is_ajax

    return jinja2_template(f'{page}',**variables)

  def __static_file(self, filename, root = 'static'):
    # TODO: This javascript file should not be templated parsed..... not correct
    if filename == 'js/terrariumpi.js':
      response.headers['Content-Type'] = 'application/javascript; charset=UTF-8'
      response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(days=self.__caching_days)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      return template(filename,template_lookup=[root])

    # Load the static file
    staticfile = static_file(filename, root=root)
    if isinstance(staticfile,HTTPError):
      # File does not exists, so just return the error
      return staticfile

    self.__add_caching_heders(staticfile,f'{root}/{filename}')

    return staticfile

  def __file_upload(self, root = 'media'):
    try:
      upload_file = request.files.get('file',None)
      if upload_file is not None:
        upload_file.save(root, overwrite=True)
        return {'file' : f'{root.strip("/")}/{upload_file.filename}'}

      raise Exception('No valid file upload')

    except Exception as ex:
      raise HTTPError(status=500, body=f'Error uploading file. {ex}')

  def __routes(self):
    # Add a 404 page...
    @self.bottle.error(400)
    @self.bottle.error(404)
    @self.bottle.error(500)
    def handle_error(error):
      if request.is_ajax:
        response.status = error.status
        response.content_type = 'application/json'
        return json.dumps({'message' : error.body})

      variables = self.__template_variables(f'{error.status}')
      variables['page_title'] = f'{error.status} Error'
      return jinja2_template('views/error.html',variables)

    # Add API including all the CRUD urls
    self.api.routes(self.bottle)

    # Websocket connection
    self.bottle.route('/live/', callback=self.websocket.connect, apply=websocket, name='websocket_connect')

    # Login url
    self.bottle.route('/login/', method='GET', callback=self.__login, apply=self.authenticate(True), name='login')

    # Logout url
    self.bottle.route('/logout/', method='POST', callback=self.__logout, apply=auth_basic(self.__clear_authentication,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes')), name='logout')

    # Index page
    self.bottle.route('/', method='GET', callback=self.render_page, apply=self.authenticate(), name='home')

    # Template pages
    self.bottle.route('/<page:re:[^/]+>.html', method='GET', callback=self.render_page, apply=self.authenticate(), name='page')

    # Special case: robots.txt
    self.bottle.route('/<filename:re:robots\.txt>', method='GET', callback=self.__static_file)

    # Static files
    self.bottle.route('/<root:re:(static|webcam|media|log)>/<filename:path>', method='GET', callback=self.__static_file, apply=self.authenticate())
    self.bottle.route('/<root:re:(media)>/upload/', method='POST', callback=self.__file_upload, apply=self.authenticate(), name='file_upload')





    # self.bottle.route('/api/<path:re:config.*>',
    #                  method=['GET'],
    #                  callback=self.__get_api_call,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/<path:path>',
    #                  method=['GET'],
    #                  callback=self.__get_api_call,
    #                  apply=self.authenticate())

    # self.bottle.route('/api/reboot',
    #                  method=['POST'],
    #                  callback=self.__reboot,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/shutdown',
    #                  method=['POST'],
    #                  callback=self.__shutdown,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/switch/toggle/<switchid:path>',
    #                  method=['POST'],
    #                  callback=self.__toggle_switch,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/switch/manual_mode/<switchid:path>',
    #                  method=['POST'],
    #                  callback=self.__manual_mode_switch,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/switch/state/<switchid:path>/<value:int>',
    #                  method=['POST'],
    #                  callback=self.__state_switch,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/config/switches/hardware',
    #                  method=['PUT'],
    #                  callback=self.__replace_switch_hardware,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/config/<path:re:(system|weather|switches|sensors|webcams|doors|audio|environment|profile|notifications)>',
    #                  method=['PUT','POST','DELETE'],
    #                  callback=self.__update_api_call,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/audio/player/<action:re:(start|stop|volumeup|volumedown|mute|unmute)>',
    #                  method=['POST'],
    #                  callback=self.__player_commands,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/audio/file',
    #                  method=['POST'],
    #                  callback=self.__upload_audio_file,
    #                  apply=self.authenticate(True)
    #                 )

    # self.bottle.route('/api/audio/file/<audiofileid:path>',
    #                  method=['DELETE'],
    #                  callback=self.__delete_audio_file,
    #                  apply=self.authenticate(True)
    #                 )



  def url_for(self, name, **kargs):
    # First check the webserver for named routes
    try:
      url = self.bottle.get_url(name, **kargs)
    except RouteBuildError:
      url = '#'
    # Then check if there is a view with the n
    #print(f'Url for {name} with {kargs} -> {url}')
    return url

  def authenticate(self, required = False):
    return self.__auth_basic(self.engine.authenticate,required,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))

  def __player_commands(self,action):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Player command could ot be executed!')}

    if 'start' == action:
      self.engine.audio_player_start()
    elif 'stop' == action:
      self.engine.audio_player_stop()
    elif 'volumeup' == action:
      self.engine.audio_player_volume_up()
      result = {'ok' : True, 'title' : _('OK!'), 'message' : _('Player command executed!')}
    elif 'volumedown' == action:
      self.engine.audio_player_volume_down()
      result = {'ok' : True, 'title' : _('OK!'), 'message' : _('Player command executed!')}
    elif 'mute' == action:
      pass
    elif 'unmute' == action:
      pass

    return result

  def __upload_audio_file(self):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('File is not uploaded!')}
    upload = request.files.get('file')
    try:
      upload.save(terrariumAudioPlayer.AUDIO_FOLDER)
      self.engine.reload_audio_files()
      result = {'ok' : True, 'title' : _('Success!'), 'message' : _('File \'%s\' is uploaded') % (upload.filename,)}
    except IOError as message:
      result['message'] = _('Duplicate file \'%s\'') % (upload.filename,)

    return result

  def __delete_audio_file(self,audiofileid):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Action could not be satisfied')}

    if self.engine.delete_audio_file(audiofileid):
      result = {'ok' : True, 'title' : _('Success!'), 'message' : _('Audio file is deleted')}

    return result

  # def __update_api_call(self,path):
  #   result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Data could not be saved')}
  #   postdata = {}

  #   if request.json is not None:
  #     postdata = request.json

  #   result['ok'] = self.engine.set_config(path,postdata,request.files)
  #   if result['ok']:
  #     result['title'] = _('Data saved')
  #     result['message'] = _('Your changes are saved')

  #     # Reload language if needed
  #     if 'language' in postdata:
  #       gettext.translation('terrariumpi', 'locales/', languages=[self.engine.config.get_language()]).install(True)
  #       self.__translations.reload()

  #   return result

  def __replace_switch_hardware(self):
    postdata = None
    if request.json is not None:
      postdata = request.json

    self.engine.replace_hardware_calender_event(postdata['switch']['id'],
                                                           postdata['switch']['device'],
                                                           postdata['switch']['reminder_amount'],
                                                           postdata['switch']['reminder_period'])
    result = {'ok' : True,
              'title' : _('Hardware is replaced'),
              'message' : _('Hardware replacement is logged in the calendar')}

    if '' != postdata['switch']['reminder_amount']:
      result['message'] += '<br />' + _('A new replacement reminder is created')

    return result

  # def __get_api_call(self,path):
  #   response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(seconds=10)).strftime('%a, %d %b %Y %H:%M:%S GMT')
  #   response.headers['Access-Control-Allow-Origin'] = '*'

  #   result = {}
  #   parameters = path.strip('/').split('/')

  #   action = parameters[0]
  #   del(parameters[0])

  #   if 'switches' == action:
  #     result = self.engine.get_switches(parameters)

  #   elif 'doors' == action:
  #     if len(parameters) > 0 and parameters[0] == 'status':
  #        result = {'status' : self.engine.get_doors_status()}
  #     else:
  #       result = self.engine.get_doors()

  #   elif 'profile' == action:
  #     result = self.engine.get_profile()

  #   elif 'calendar' == action:
  #     if 'ical' in parameters:
  #       response.headers['Content-Type'] = 'text/calendar'
  #       response.headers['Content-Disposition'] = 'attachment; filename=terrariumpi.ical.ics'

  #     response.headers['Content-Type'] = 'application/json'
  #     result = json.dumps(self.engine.get_calendar(parameters,**{'start':request.query.get('start'),'end':request.query.get('end')}))

  #   elif 'sensors' == action:
  #     result = self.engine.get_sensors(parameters)

  #   elif 'webcams' == action:
  #     result = self.engine.get_webcams(parameters)

  #   elif 'audio' == action:
  #     if len(parameters) > 0 and parameters[0] == 'files':
  #       del(parameters[0])
  #       result = self.engine.get_audio_files(parameters)
  #     elif len(parameters) > 0 and parameters[0] == 'playing':
  #       del(parameters[0])
  #       result = self.engine.get_audio_playing()
  #     elif len(parameters) > 0 and parameters[0] == 'hardware':
  #       del(parameters[0])
  #       result = {'audiohardware' : terrariumAudioPlayer.get_sound_cards()}
  #     else:
  #       result = self.engine.get_audio_playlists(parameters)

  #   elif 'environment' == action:
  #     result = self.engine.get_environment(parameters)

  #   elif 'weather' == action:
  #     result = self.engine.get_weather(parameters)

  #   elif 'uptime' == action:
  #     result = self.engine.get_uptime()

  #   elif 'power_usage' == action:
  #     result = self.engine.get_power_usage_water_flow()['power']

  #   elif 'water_usage' == action:
  #     result = self.engine.get_power_usage_water_flow()['water']

  #   elif 'system' == action:
  #     result = self.engine.get_system_stats()

  #   elif 'config' == action:
  #     # TODO: New way of data processing.... fix other config options
  #     result = self.engine.get_config(parameters[0] if len(parameters) == 1 else None)

  #   elif 'history' == action or 'export' == action:
  #     response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
  #     if 'export' == action:
  #       parameters.append('all')
  #     result = self.engine.get_history(parameters)

  #     if 'export' == action:
  #       csv = ''
  #       export_name = 'error'
  #       for datatype in result:
  #         for dataid in result[datatype]:
  #           export_name = datatype + '_' + dataid + '.csv'
  #           # Header
  #           fields = list(result[datatype][dataid].keys())
  #           if 'totals' in fields:
  #             fields.remove('totals')
  #           csv = '"' + '","'.join(['timestamp'] + fields) + "\"\n"

  #           for counter in range(0,len(result[datatype][dataid][fields[0]])):
  #             # Timestamp
  #             row = [datetime.datetime.fromtimestamp(int(str(int(result[datatype][dataid][fields[0]][counter][0]/1000)))).strftime('%Y-%m-%d %H:%M:%S')]
  #             for field in fields:
  #               # Row values
  #               row.append(str(result[datatype][dataid][field][counter][1]))

  #             csv += '"' + '","'.join(row) + "\"\n"

  #       response.headers['Content-Type'] = 'application/csv'
  #       response.headers['Content-Disposition'] = 'attachment; filename=' + export_name
  #       return csv

  #   return result

  # def __toggle_switch(self,switchid):
  #   if switchid in self.engine.power_switches:
  #     self.engine.power_switches[switchid].toggle()
  #     return {'ok' : True}

  #   return {'ok' : False}

  # def __manual_mode_switch(self,switchid):
  #   if switchid in self.engine.power_switches:
  #     self.engine.power_switches[switchid].set_manual_mode(not self.engine.power_switches[switchid].in_manual_mode())
  #     self.engine.config.save_power_switch(self.engine.power_switches[switchid].get_data())
  #     return {'ok' : True}

  #   return {'ok' : False}

  # def __state_switch(self,switchid,value):
  #   if switchid in self.engine.power_switches:
  #     if value == 1:
  #       self.engine.power_switches[switchid].set_state(True)
  #       return {'ok' : True}
  #     elif value == 0:
  #       self.engine.power_switches[switchid].set_state(False)
  #       return {'ok' : True}
  #     else:
  #       self.engine.power_switches[switchid].set_state(value)
  #       return {'ok' : True}

  #   return {'ok' : False}

  # -= NEW =-
  def __login(self):
    # TODO: Better cookie support
    response.set_cookie('auth', request.auth, secret=self.cookie_secret, **{ 'max_age' : 3600, 'path' : '/'})
    redirect(self.url_for('home'))

  # -= NEW =-
  def __logout(self):
    response.set_cookie('auth', '', secret=self.cookie_secret, **{ 'max_age' : 3600, 'path' : '/'})
    if request.is_ajax:
      return {'location' : self.url_for('home'), 'message' : 'User logged out.'}

    redirect(self.url_for('home'))

  # -= NEW =-
  def websocket_message(self, message_type, message_data):
    self.websocket.send_message({ 'type' : message_type, 'data' : message_data})

  # -= NEW =-
  def start(self):
    # Start the webserver
    logger.info(f'Running webserver at {self.engine.settings["host"]}:{self.engine.settings["port"]}')
    print(f'{datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S,000")} - INFO    - terrariumWebserver   - Running webserver at {self.engine.settings["host"]}:{self.engine.settings["port"]}')

    self.bottle.run(host=self.engine.settings['host'],
                    port=self.engine.settings['port'],
                    server=GeventWebSocketServer,
                    debug=True,
                    reloader=False,
                    quiet=True)

# -= NEW =-
class terrariumWebsocket(object):
  def __init__(self, terrariumWebserver):
    self.webserver = terrariumWebserver
    self.clients = []

  def connect(self,socket):
      messages = Queue()

      def listen_for_messages(messages,socket):
        self.clients.append(messages)
        logger.debug(f'Got a new websocket connecton from {socket}')

        while True:
          message = messages.get()
          try:
            socket.send(json.dumps(message))
            messages.task_done()
          except Exception as ex:
            # Socket connection is lost/closed, stop looping....
            logger.warning(f'Disconnected {socket}. Stop listening and remove queue... {ex}')
            try:
              self.clients.remove(messages)
            except Exception as ex:
              pass

            break

      while True:
        try:
          message = socket.receive()
        except Exception as ex:
          # Closed websocket connection.
          logger.warning(f'Websocket error receiving messages: {ex}')
          try:
            self.clients.remove(messages)
          except Exception as ex:
            pass

          break

        if message is not None:
          message = json.loads(message)

          if 'client_init' == message['type']:
            threading.Thread(target=listen_for_messages, args=(messages,socket)).start()
            # Load the running sensor types for adding new menu items below sensors
            self.send_message({'type' : 'sensortypes', 'data' : self.webserver.engine.sensor_types_loaded}, messages)
            self.send_message({'type' : 'systemstats', 'data' : self.webserver.engine.system_stats()}, messages)
            self.send_message({'type' : 'power_usage_water_flow', 'data' : self.webserver.engine.get_power_usage_water_flow}, messages)

          elif 'load_dashboard' == message['type']:
            self.send_message({'type' : 'systemstats', 'data' : self.webserver.engine.system_stats()}, messages)
            self.send_message({'type' : 'power_usage_water_flow', 'data' : self.webserver.engine.get_power_usage_water_flow}, messages)

            for sensor_type, avg_data in self.webserver.engine.sensor_averages.items():
              self.send_message({'type' : 'gauge_update', 'data' : { 'id' : f'avg_{sensor_type}', 'value' : avg_data['value']}}, messages)

          else:
            pass
            #self.send_message({'type':'echo_replay', 'data':message})

          # terrariumWebserver.app.terrarium.get_doors_status(socket=True)
          # terrariumWebserver.app.terrarium.get_environment(socket=True)

  def send_message(self, message, queue = None):
    # Get all the connected websockets (get a copy of the list, as we could delete entries and change the list length during the loop)
    clients = self.clients
    # Loop over all the clients
    for client in clients:
      if queue is None or queue == client:
        client.put(message)
      # If more then 50 messages in queue, looks like connection is gone and remove the queue from the list
      if client.qsize() > 50:
        logger.warning(f'Lost connection.... should not happen anymore. {len(self.clients)} - {client.qsize()} - {client}')
        try:
          self.clients.remove(client)
        except Exception as ex:
          pass

    logger.debug(f'Websocket message {message} is send to {len(self.clients)} clients')