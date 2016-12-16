# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from bottle import Bottle, request, abort, static_file, template, error, response, auth_basic
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from Queue import Queue

import gettext
gettext.install('terrariumpi', 'locales/', unicode=True)

#gettext.translation('terrariumpi', 'locales/', languages=['nl_NL']).install(True)

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
    self.__config = terrariumEngine.get_config('system')
    # Load language
    gettext.translation('terrariumpi', 'locales/', languages=[self.__terrariumEngine.config.get_active_language()]).install(True)

    terrariumWebserver.app.terrarium = self.__terrariumEngine

    self.__routes()

  def __authenticate(self, user, password):
    return self.__terrariumEngine.authenticate(user,password)

  def __routes(self):
    self.__app.route('/', method="GET", callback=self.__render_page)
    self.__app.route('/<template_name:re:[^/]+\.html$>', method="GET", callback=self.__render_page, apply=[terrariumWebserverHeaders()])

    self.__app.route('/static/<filename:path>', method="GET", callback=self.__static_file)
    self.__app.route('/gentelella/<filename:path>', method="GET", callback=self.__static_file_gentelella)

    self.__app.route('/api/switch/toggle/<switchid:path>',
                     method=['GET'],
                     callback=self.__toggle_switch,
                     apply=auth_basic(self.__authenticate,'TerrarumPI Authentication','Authenticate to make any changes')
                    )

    self.__app.route('/api/config/<path:re:(system|weather|switches|sensors|webcams|environment)>',
                     method=['PUT','POST','DELETE'],
                     callback=self.__update_api_call,
                     apply=auth_basic(self.__authenticate,'TerrarumPI Authentication','Authenticate to make any changes')
                    )

    self.__app.route('/api/<path:path>', method=['GET'], callback=self.__get_api_call)

  def __template_variables(self, template):
    variables = { 'lang' : self.__terrariumEngine.config.get_active_language(),
                  'title' : self.__config['title'],
                  'page_title' : template.replace('_',' ').title()}

    if 'index' == template:
      variables['person_name'] = self.__config['person']
      variables['person_image'] = self.__config['image']

    elif 'webcam' == template or 'webcam_settings' == template:
      variables['amount_of_webcams'] = self.__terrariumEngine.get_amount_of_webcams()

    elif 'switch_settings' == template:
      variables['max_swithes'] = self.__terrariumEngine.get_max_switches_config()
    elif 'switch_status' == template:
      variables['amount_of_switches'] = self.__terrariumEngine.get_amount_of_switches()

    elif 'sensor_settings' == template:
      variables['amount_of_sensors'] = self.__terrariumEngine.get_amount_of_sensors()
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

  def __static_file(self,filename):
    if filename == 'js/terrariumpi.js':
      response.headers['Content-Type'] = 'application/javascript'
      return template(filename,template_lookup=['./static/'])

    return static_file(filename, root='./static/')

  def __static_file_gentelella(self,filename):
    return static_file(filename, root='./gentelella/')

  def __update_api_call(self,path):
    result = {'ok' : False, 'title' : _('Error!'), 'message' : _('Data could not be saved')}
    postdata = json.loads(request.body.getvalue())
    result['ok'] = self.__terrariumEngine.set_config(path,postdata)
    if result['ok']:
      result['title'] = _('Data saved')
      result['message'] = _('Your changes are saved')

      # Reload language
      gettext.translation('terrariumpi', 'locales/', languages=[self.__terrariumEngine.config.get_active_language()]).install(True)

    return result

  def __get_api_call(self,path):
    result = {}
    parameters = path.strip('/').split('/')

    action = parameters[0]
    del(parameters[0])

    if 'switches' == action:
      result = self.__terrariumEngine.get_switches(parameters)

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
    variables = { 'lang' : self.__terrariumEngine.config.get_active_language(),
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
        terrariumWebserver.app.terrarium.get_power_usage_water_flow(socket=True)
        terrariumWebserver.app.terrarium.get_environment(socket=True)
        terrariumWebserver.app.terrarium.get_sensors(['average'],socket=True)

  def start(self):
    # Start the webserver
    self.__app.run(host=self.__config['host'],
                   port=self.__config['port'],
                   server=GeventWebSocketServer,
                   debug=False,
                   reloader=False)
