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
from PIL import Image

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
    ]

    # This secret will change every reboot. So cookies will not work anymore after a reboot.
    self.cookie_secret = uuid4().bytes
    self.bottle        = default_app() # This is needed to get the APISpec BottlePlugin to work
    self.engine        = terrariumEngine
    self.websocket     = terrariumWebsocket(self)
    self.api           = terrariumAPI(self)

    # Load language
    gettext.translation('terrariumpi', 'locales/', languages=[self.engine.settings['language']]).install()

    # Load the routes
    self.__routes()

  # Custom HTTP authentication routine. This way there is an option to optional secure the hole web interface
  def __auth_basic(self, check, required, realm="private", text="Access denied"):
    """ Callback decorator to require HTTP auth (basic).
        TODO: Add route(check_auth=...) parameter. """

    def decorator(func):

      @functools.wraps(func)
      def wrapper(*a, **ka):
        if int(self.engine.settings['always_authenticate']) != -1 and (required or terrariumUtils.is_true(self.engine.settings['always_authenticate'])):
          user, password = request.auth or (None, None)
          ip = request.remote_addr if request.get_header('X-Real-Ip') is None else request.get_header('X-Real-Ip')
          if user is None or not check(user, password):
            err = HTTPError(401, text)
            err.add_header('WWW-Authenticate', f'Basic realm="{realm}"')
            if user is not None or password is not None:
              self.engine.notification.message('authentication_error',{'ip' : ip, 'username' : user, 'password' : password},[])
              logger.warning(f'Incorrect login detected using username \'{user}\' and password \'{password}\' from ip {ip}')
            return err

        if request.method.lower() in ['get','head']:
          self.__add_caching_headers(response,request.fullpath)

          if request.url.lower().endswith('.html') or '/' == request.fullpath:
            user, password = request.get_cookie('auth', secret=self.cookie_secret) or (None, None)
            if check(user, password):
              # Update the cookie timeout so that we are staying logged in as long as we are working on the interface
              response.set_cookie('auth', request.get_cookie('auth', secret=self.cookie_secret), secret=self.cookie_secret, **{ 'max_age' : 3600, 'path' : '/'})

        elif request.method.lower() in ['post','put','delete']:
          response.set_cookie('no-cache','1', secret=None, **{ 'max_age' : 90, 'path' : '/'})
          response.set_header('Cache-Control', 'no-cache')


        return func(*a, **ka)

      return wrapper

    return decorator

  def __clear_authentication(self, user, password):
    return True

  def __add_caching_headers(self, response, fullpath):
    if 200 == response.status_code:
      # Add the caching headers
      for caching in self.__caching_timeouts:
        if caching['path'].search(request.fullpath):
          response.expires = datetime.datetime.utcnow().timestamp() + caching['timeout']
          response.set_header('Cache-Control', f'public, max-age={caching["timeout"]}')

        elif '/' == request.fullpath or re.search(r'\.html$',request.fullpath,re.I):
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

    authenticated = False
    try:
      cookie_data = request.get_cookie('auth', secret=self.cookie_secret)
      if cookie_data is not None:
        authenticated = self.engine.authenticate(cookie_data[0],cookie_data[1])
    except Exception:
      # Some strange cookie error when cleared... we can ignore that
      pass

    # Variables
    variables = {
      'authenticated' : int(self.engine.settings['always_authenticate']) == -1 or authenticated,
      'lang'          : self.engine.settings['language'],
      'title'         : self.engine.settings['title'],
      'version'       : self.engine.settings['version'],
      'template'      : template,
      'device'        : self.engine.settings['device'],
      'username'      : self.engine.settings['username'],
      'profile_image' : self.engine.settings['profile_image'],
      'favicon'       : self.engine.settings['favicon'],

      'languages'     : self.engine.settings['languages'],
      'units'         : unit_variables(),

      'show_gauge_overview'      : self.engine.settings['all_gauges_on_single_page'],
      'show_environment'         : not self.engine.settings['hide_environment_dashboard'],
      'graph_smooth_value'       : self.engine.settings['graph_smooth_value'],
      'graph_show_min_max_gauge' : 1 if self.engine.settings['show_min_max_gauge'] else 0,
      'auto_dark_mode'           : 1 if self.engine.settings['auto_dark_mode'] else 0,
      'is_night'                 : 0 if self.engine.weather is None or self.engine.weather.is_day else 1
    }

    # Template functions
    variables['url_for'] = self.url_for
    variables['_']  = _

    return variables

  def authenticate(self, required = False):
    return self.__auth_basic(self.engine.authenticate,required,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))

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

  def _static_file(self, filename, root = 'static'):
    # TODO: This javascript file should not be templated parsed..... not correct
    if filename == 'js/terrariumpi.js':
      response.headers['Content-Type'] = 'application/javascript; charset=UTF-8'
      response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(days=self.__caching_days)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      return template(filename,template_lookup=[root])

    # Load the static file
    if request.headers.get('Accept-Encoding') and 'gzip' in request.headers.get('Accept-Encoding'):
      staticfile = static_file(filename + '.gz', root=root)
      if not isinstance(staticfile, HTTPError):
        self.__add_caching_headers(staticfile,f'{root}/{filename}')
        return staticfile

    staticfile = static_file(filename, root=root)
    if isinstance(staticfile,HTTPError):
      # File does not exists, so just return the error
      return staticfile

    self.__add_caching_headers(staticfile,f'{root}/{filename}')

    return staticfile

  def __file_upload(self, root = 'media'):
    try:
      upload_file = request.files.get('file',None)
      if upload_file is not None:
        upload_file.save(root, overwrite=True)
        if 'profile_image.' in upload_file.filename:
          img = Image.open(f'{root.strip("/")}/{upload_file.filename}')
          img.save(f'{root.strip("/")}/favicon.ico')

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
    self.bottle.route('/<page:re:[^/]+>.html',        method='GET', callback=self.render_page, apply=self.authenticate(), name='page')
    self.bottle.route('/<page:re:modals/[^/]+>.html', method='GET', callback=self.render_page, apply=self.authenticate(), name='modal')

    # Special case: robots.txt and favicon.ico
    self.bottle.route('/<filename:re:(robots\.txt|favicon\.ico)>', method='GET', callback=self._static_file)

    # Static files
    self.bottle.route('/<root:re:(static|webcam|media|log)>/<filename:path>', method='GET', callback=self._static_file, apply=self.authenticate())
    self.bottle.route('/<root:re:(media)>/upload/', method='POST', callback=self.__file_upload, apply=self.authenticate(), name='file_upload')

  def url_for(self, name, **kwargs):
    # First check the webserver for named routes
    try:
      url = self.bottle.get_url(name, **kwargs)
    except RouteBuildError:
      url = '#'

    return url

  def __login(self):
    response.set_cookie('auth', request.auth, secret=self.cookie_secret, **{ 'max_age' : 3600, 'path' : '/'})
    redirect(self.url_for('home'))

  def __logout(self):
    response.set_cookie('auth', None, secret=self.cookie_secret, **{ 'max_age' : 3600, 'path' : '/'})
    if request.is_ajax:
      return {'location' : self.url_for('home'), 'message' : 'User logged out.'}

    redirect(self.url_for('home'))

  def websocket_message(self, message_type, message_data):
    self.websocket.send_message({ 'type' : message_type, 'data' : message_data})

  def start(self):
    # Start the webserver
    logger.info(f'Running webserver at {self.engine.settings["host"]}:{self.engine.settings["port"]}')
    print(f'{datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S,000")} - INFO    - terrariumWebserver    - Running webserver at {self.engine.settings["host"]}:{self.engine.settings["port"]}')

    self.bottle.run(host=self.engine.settings['host'],
                    port=self.engine.settings['port'],
                    server=GeventWebSocketServer,
                    debug=True,
                    reloader=False,
                    quiet=True)

class terrariumWebsocket(object):
  def __init__(self, terrariumWebserver):
    self.webserver = terrariumWebserver
    self.clients = []

  def connect(self,socket):
      messages = Queue()

      def listen_for_messages(messages, socket):
        self.clients.append(messages)
        logger.debug(f'Got a new websocket connection from {socket}')

        while True:
          message = messages.get()
          try:
            socket.send(json.dumps(message))
            messages.task_done()
          except Exception as ex:
            # Socket connection is lost/closed, stop looping....
            logger.debug(f'Disconnected {socket}. Stop listening and remove queue... {ex}')
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
          logger.debug(f'Websocket error receiving messages: {ex}')
          try:
            self.clients.remove(messages)
          except Exception as ex:
            pass

          break

        if message is not None:
          message = json.loads(message)

          if 'client_init' == message['type']:
            messages.authenticated = False
            try:
              cookie_data = request.get_cookie('auth', secret=self.webserver.cookie_secret)
              if cookie_data is not None:
                messages.authenticated = self.webserver.engine.authenticate(cookie_data[0],cookie_data[1])
            except Exception:
              # Some strange cookie error when cleared... we can ignore that
              pass

            logger.debug(f'Starting authenticated socket? {messages.authenticated}')
            threading.Thread(target=listen_for_messages, args=(messages, socket)).start()
            # Load the running sensor types for adding new menu items below sensors
            self.send_message({'type' : 'sensortypes', 'data' : self.webserver.engine.sensor_types_loaded}, messages)
            self.send_message({'type' : 'systemstats', 'data' : self.webserver.engine.system_stats()}, messages)
            self.send_message({'type' : 'power_usage_water_flow', 'data' : self.webserver.engine.get_power_usage_water_flow}, messages)

            if self.webserver.engine.update_available:
              self.send_message({'type' : 'softwareupdate', 'data' : {'title':_('Software Update'), 'message' : '<a href="https://github.com/theyosh/TerrariumPI/releases" target="_blank" rel="noopener">' + _('A new version ({version}) is available!').format(version=self.webserver.engine.latest_version) + '</a>'}}, messages)

          elif 'load_dashboard' == message['type']:
            self.send_message({'type' : 'systemstats', 'data' : self.webserver.engine.system_stats()}, messages)
            self.send_message({'type' : 'power_usage_water_flow', 'data' : self.webserver.engine.get_power_usage_water_flow}, messages)

            for sensor_type, avg_data in self.webserver.engine.sensor_averages.items():
              self.send_message({'type' : 'gauge_update', 'data' : { 'id' : f'avg_{sensor_type}', 'value' : avg_data['value']}}, messages)

          else:
            pass

  def send_message(self, message, queue = None):
    # Get all the connected websockets (get a copy of the list, as we could delete entries and change the list length during the loop)
    clients = self.clients
    # Loop over all the clients
    for client in clients:
      if queue is None or queue == client:

        if 'logfile_update' == message['type'] and not client.authenticated:
          # Clean the logline message. Keep date and type for web indicators
          message['data'] = message['data'][0:36].strip()

        client.put(message)
      # If more then 50 messages in queue, looks like connection is gone and remove the queue from the list
      if client.qsize() > 50:
        logger.debug(f'Lost connection.... should not happen anymore. {len(self.clients)} - {client.qsize()} - {client}')
        try:
          self.clients.remove(client)
        except Exception as ex:
          pass

    logger.debug(f'Websocket message {message} is send to {len(self.clients)} clients')
