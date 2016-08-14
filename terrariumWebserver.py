# -*- coding: utf-8 -*-

from bottle import Bottle, request, abort, static_file, template, error, response
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

from Queue import Queue

import thread
#import time

import uptime
import json
import os
import datetime
import hashlib
#import random

from gevent import monkey, sleep
monkey.patch_all()

class terrariumWebserverHeaders(object):
  name = 'webserver_headers'
  api = 2

  def apply(self, fn, context):
    def _webserver_headers(*args, **kwargs):
      template_file = 'views' + request.fullpath[:-5] + '.tpl'
      if os.path.isfile(template_file):
        t = os.path.getmtime(template_file)
        response.headers['Last-Modified'] = datetime.datetime.fromtimestamp(t).strftime( '%a, %d %b %Y %H:%M:%S GMT')
        response.headers['Etag'] = hashlib.md5(response.headers['Last-Modified']).hexdigest()

      return fn(*args, **kwargs)

    return _webserver_headers

class terrariumWebserver():

  app = Bottle()
  #app.install(terrariumWebserverHeaders())

  def __init__(self, terrariumEngine):
    self.__terrariumEngine = terrariumEngine
    self.__app = terrariumWebserver.app
    self.__config = terrariumEngine.get_config('system')
    terrariumWebserver.app.terrarium = self.__terrariumEngine

    self.__routes()

  def __routes(self):
    self.__app.route('/', method="GET", callback=self.__render_page)
    self.__app.route('/<template_name:re:[^/]+\.html$>', method="GET", callback=self.__render_page, apply=[terrariumWebserverHeaders()])

    self.__app.route('/static/<filename:path>', method="GET", callback=self.__static_file)
    self.__app.route('/gentelella/<filename:path>', method="GET", callback=self.__static_file_gentelella)

    self.__app.route('/api/config/<path:re:(system|weather|switches|sensors|environment)>', method=['PUT','POST'], callback=self.__update_api_call)
    self.__app.route('/api/<path:path>', method=['GET'], callback=self.__get_api_call)


  #def __get_caching_header(self,file):


  def __template_variables(self, template):
    variables = { 'title' : self.__config['title'],
                  'page_title' : template.replace('_',' ').title()}

    if 'index' == template:
      variables['person_name'] = self.__config['person']
      variables['person_image'] = self.__config['image']
    elif 'sensor_settings' == template:
      variables['amount_of_sensors'] = self.__terrariumEngine.get_amount_of_sensors()
    elif 'switch_settings' == template:
      variables['max_swithes'] = self.__terrariumEngine.get_switches_config()['max_switches']
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

  def __static_file(self,filename):
    return static_file(filename, root='./static/')

  def __static_file_gentelella(self,filename):
    return static_file(filename, root='./gentelella-1.3.0/')

  def __update_api_call(self,path):
    result = {'ok' : False}
    postdata = json.loads(request.body.getvalue())
    result['ok'] = self.__terrariumEngine.set_config(path,postdata)
    return result

  def __get_api_call(self,path):
    result = {}
    path = path.strip('/').split('/')

    what = path[0]
    subwhat = None
    if len(path) > 1:
      subwhat = path[1]

    if 'switches' == what:
      result = self.__terrariumEngine.get_switches(subwhat)

    elif 'sensors' == what:
      result = self.__terrariumEngine.get_sensors(subwhat)

    elif 'environment' == what:
      result = self.__terrariumEngine.get_environment(subwhat)

    elif 'weather' == what:
      if subwhat is None:
        result = self.__terrariumEngine.get_weather()

    elif 'uptime' == what:
      result = self.__terrariumEngine.get_uptime()

    elif 'power_usage' == what:
      result = self.__terrariumEngine.get_power_usage_water_flow()['power']

    elif 'water_usage' == what:
      result = self.__terrariumEngine.get_power_usage_water_flow()['water']

    elif 'total_usage' == what:
      result = self.__terrariumEngine.get_total_power_usage_water_flow()
      result['power_wattage'] /= 1000.0
      result['total_power'] /= 1000.0

    elif 'history' == what:
      if subwhat is None:
        pass

      elif 'sensors' == subwhat or 'environment' == subwhat or 'switches' == subwhat:
        type = None
        id = None

        if len(path) >= 3:
          type = path[2]

        if len(path) >= 4:
          id = path[3]

        if 'environment' == subwhat:
          subwhat = 'sensors'
          type = 'summary'

        result = self.__terrariumEngine.get_history(subwhat,type,id)

    elif 'config' == what:
      result = self.__terrariumEngine.get_config(subwhat)

    return result

  @app.error(404)
  def error404(error):
    config = terrariumWebserver.app.terrarium.get_config('system')
    variables = { 'title' : config['title'],
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
        except:
          pass
        messages.task_done()

    while True:
      message = socket.receive()
      if message is not None:
        message = json.loads(message)
        print message

        if message['type'] == 'client_init':
          thread.start_new_thread(listen_for_messages, (messages,socket))
          terrariumWebserver.app.terrarium.subscribe(messages)

          # Load/Update actual data after reconnect
          if message['reconnect']:
            terrariumWebserver.app.terrarium.get_weather(True)
            terrariumWebserver.app.terrarium.get_switches(True)
            terrariumWebserver.app.terrarium.get_power_usage_water_flow(True)
            terrariumWebserver.app.terrarium.get_total_power_usage_water_flow(True)

        elif message['type'] == 'toggle_switch':
          if message['data']['state']:
            terrariumWebserver.app.terrarium.switch_board.switches[int(message['data']['nr'])-1].on()
          else:
            terrariumWebserver.app.terrarium.switch_board.switches[int(message['data']['nr'])-1].off()
      else:
        break

  def start(self):
      self.__app.run(host=self.__config['host'], port=self.__config['port'], server=GeventWebSocketServer, debug=False, reloader=False)
