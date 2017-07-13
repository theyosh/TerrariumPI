# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import gettext
gettext.install('terrariumpi', 'locales/', unicode=True)

from bottle import Bottle, request, abort, static_file, template, error, response, auth_basic, HTTPError
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from Queue import Queue

from terrariumTranslations import terrariumTranslations

import thread
import json
import os
import datetime
import hashlib

from gevent import monkey, sleep
monkey.patch_all()

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
        response.headers['Etag'] = hashlib.md5(response.headers['Last-Modified']).hexdigest()

      return fn(*args, **kwargs)

    return webserver_headers

class terrariumWebserver():

  app = Bottle()
  app.install(terrariumWebserverHeaders())

  def __init__(self, terrariumEngine):
    self.__terrariumEngine = terrariumEngine
    self.__app = terrariumWebserver.app
    self.__config = self.__terrariumEngine.get_config('system')
    self.__caching_days = 30

    terrariumWebserver.app.terrarium = self.__terrariumEngine
    # Load language
    gettext.translation('terrariumpi', 'locales/', languages=[self.__terrariumEngine.config.get_active_language()]).install(True)
    self.__translations = terrariumTranslations()

    self.__routes()

  def __authenticate(self, user, password):
    return self.__terrariumEngine.authenticate(user,password)

  def __routes(self):
    self.__app.route('/', method="GET", callback=self.__render_page)
    self.__app.route('/<template_name:re:[^/]+\.html$>', method="GET", callback=self.__render_page)

    self.__app.route('/<root:re:(static|gentelella|webcam)>/<filename:path>', method="GET", callback=self.__static_file)

    self.__app.route('/api/switch/toggle/<switchid:path>',
                     method=['GET'],
                     callback=self.__toggle_switch,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/api/config/<path:re:(system|weather|switches|sensors|webcams|doors|environment)>',
                     method=['PUT','POST','DELETE'],
                     callback=self.__update_api_call,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/api/<path:path>', method=['GET'], callback=self.__get_api_call)

  def __template_variables(self, template):
    variables = { 'lang' : self.__terrariumEngine.config.get_active_language(),
                  'title' : self.__config['title'],
                  'page_title' : _(template.replace('_',' ').capitalize()),
                  'translations': self.__translations }

    if 'index' == template:
      variables['person_name'] = self.__config['person']
      variables['person_image'] = self.__config['image']

    elif 'webcam' == template or 'webcam_settings' == template:
      variables['amount_of_webcams'] = self.__terrariumEngine.get_amount_of_webcams()

    elif 'door_status' == template or 'door_settings' == template:
      variables['amount_of_doors'] = self.__terrariumEngine.get_amount_of_doors()

    elif 'switch_status' == template:
      variables['amount_of_switches'] = self.__terrariumEngine.get_amount_of_switches()

    elif 'sensor_temperature' == template:
      variables['amount_of_sensors'] = self.__terrariumEngine.get_amount_of_sensors('temperature')

    elif 'sensor_humidity' == template:
      variables['amount_of_sensors'] = self.__terrariumEngine.get_amount_of_sensors('humidity')

    return variables

  def __render_page(self,template_name = 'index.html'):
    template_name = template_name[:-5]

    if not os.path.isfile('views/' + template_name + '.tpl'):
      template_name = '404'

    return template(template_name,**self.__template_variables(template_name))

  def __static_file(self,filename, root = 'static'):
    if filename == 'js/terrariumpi.js':
      response.headers['Content-Type'] = 'application/javascript; charset=UTF-8'
      return template(filename,template_lookup=[root])

    staticfile = static_file(filename, root=root)
    if isinstance(staticfile,HTTPError):
      return staticfile

    if 'webcam' == root:
      staticfile.add_header('Expires',datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    else:
      staticfile.add_header('Expires',(datetime.datetime.now() + datetime.timedelta(days=self.__caching_days)).strftime('%a, %d %b %Y %H:%M:%S GMT'))

    if staticfile.get_header('Last-Modified') is not None:
      staticfile.add_header('Etag',hashlib.md5(staticfile.get_header('Last-Modified')).hexdigest())

    return staticfile

  def __update_api_call(self,path):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Data could not be saved')}
    postdata = json.loads(request.body.getvalue())
    result['ok'] = self.__terrariumEngine.set_config(path,postdata)
    if result['ok']:
      result['title'] = _('Data saved')
      result['message'] = _('Your changes are saved')

      # Reload language if needed
      if 'active_language' in postdata:
        gettext.translation('terrariumpi', 'locales/', languages=[self.__terrariumEngine.config.get_active_language()]).install(True)
        self.__translations.reload()

    return result

  def __get_api_call(self,path):
    result = {}
    parameters = path.strip('/').split('/')

    action = parameters[0]
    del(parameters[0])

    if 'switches' == action:
      result = self.__terrariumEngine.get_switches(parameters)

    if 'doors' == action:
      if len(parameters) > 0 and parameters[0] == 'status':
         result = {'doors' : self.__terrariumEngine.door_status()}
      else:
        result = self.__terrariumEngine.get_doors()

    elif 'sensors' == action:
      result = self.__terrariumEngine.get_sensors(parameters)

    elif 'webcams' == action:
      result = self.__terrariumEngine.get_webcams(parameters)

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

    elif 'history' == action:
      result = self.__terrariumEngine.get_history(parameters)

    elif 'config' == action:
      result = self.__terrariumEngine.get_config(parameters[0] if len(parameters) == 1 else None)

    return result

  def __toggle_switch(self,switchid):
    if switchid in self.__terrariumEngine.power_switches:
      self.__terrariumEngine.power_switches[switchid].toggle()
      return {'ok' : True}

    return {'ok' : False}

  @app.error(404)
  def error404(error):
    config = terrariumWebserver.app.terrarium.get_config('system')
    variables = { 'lang' : terrariumWebserver.app.terrarium.config.get_active_language(),
                  'title' : config['title'],
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
        except Exception, e:
          # Socket connection is lost, stop looping....
          break

        messages.task_done()

    while True:
      try:
        message = socket.receive()
      except Exception, e:
        break

      if message is not None:
        message = json.loads(message)

        if message['type'] == 'client_init':
          thread.start_new_thread(listen_for_messages, (messages,socket))
          terrariumWebserver.app.terrarium.subscribe(messages)

        terrariumWebserver.app.terrarium.door_status(socket=True)
        terrariumWebserver.app.terrarium.get_uptime(socket=True)
        terrariumWebserver.app.terrarium.get_environment(socket=True)
        terrariumWebserver.app.terrarium.get_sensors(['average'],socket=True)
        terrariumWebserver.app.terrarium.get_power_usage_water_flow(socket=True)

  def start(self):
    # Start the webserver
    logger.info('Running webserver at %s:%s' % (self.__config['host'],self.__config['port']))
    print '%s - INFO - terrariumWebserver - Running webserver at %s:%s' % (datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S,000'),
                                             self.__config['host'],
                                             self.__config['port'])
    self.__app.run(host=self.__config['host'],
                   port=self.__config['port'],
                   server=GeventWebSocketServer,
                   debug=True,
                   reloader=False,
                   quiet=True)
