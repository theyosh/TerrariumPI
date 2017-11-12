# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import gettext
gettext.install('terrariumpi', 'locales/', unicode=True)

from bottle import BaseRequest, Bottle, request, abort, static_file, template, error, response, auth_basic, HTTPError
#Increase bottle memory to max 5MB to process images in WYSIWYG editor
BaseRequest.MEMFILE_MAX = 5 * 1024 * 1024

from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from Queue import Queue

from terrariumTranslations import terrariumTranslations
from terrariumAudio import terrariumAudioPlayer

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
    gettext.translation('terrariumpi', 'locales/', languages=[self.__terrariumEngine.config.get_language()]).install(True)
    self.__translations = terrariumTranslations()

    self.__routes()

  def __authenticate(self, user, password):
    return self.__terrariumEngine.authenticate(user,password)

  def __logout_authenticate(self, user, password):
    return True

  def __routes(self):
    self.__app.route('/', method="GET", callback=self.__render_page)
    self.__app.route('/<template_name:re:[^/]+\.html$>', method="GET", callback=self.__render_page)

    self.__app.route('/<filename:re:robots\.txt>', method="GET", callback=self.__static_file)
    self.__app.route('/<root:re:(static|gentelella|webcam)>/<filename:path>', method="GET", callback=self.__static_file)

    self.__app.route('/api/<path:path>', method=['GET'], callback=self.__get_api_call)

    self.__app.route('/api/switch/toggle/<switchid:path>',
                     method=['POST'],
                     callback=self.__toggle_switch,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/api/switch/state/<switchid:path>/<value:int>',
                     method=['POST'],
                     callback=self.__state_switch,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/api/config/<path:re:(system|weather|switches|sensors|webcams|doors|audio|environment|profile)>',
                     method=['PUT','POST','DELETE'],
                     callback=self.__update_api_call,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/api/audio/player/<action:re:(start|stop|volumeup|volumedown|mute|unmute)>',
                     method=['POST'],
                     callback=self.__player_commands,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/api/audio/file',
                     method=['POST'],
                     callback=self.__upload_audio_file,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/api/audio/file/<audiofileid:path>',
                     method=['DELETE'],
                     callback=self.__delete_audio_file,
                     apply=auth_basic(self.__authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

    self.__app.route('/logout',
                     method=['GET'],
                     callback=self.__logout_url,
                     apply=auth_basic(self.__logout_authenticate,_('TerrariumPI') + ' ' + _('Authentication'),_('Authenticate to make any changes'))
                    )

  def __template_variables(self, template):
    variables = { 'lang' : self.__terrariumEngine.config.get_language(),
                  'title' : self.__config['title'],
                  'version' : self.__config['version'],
                  'page_title' : _(template.replace('_',' ').capitalize()),
                  'temperature_indicator' : self.__terrariumEngine.get_temperature_indicator(),
                  'translations': self.__translations }

    if 'index' == template or 'profile' == template:
      variables['person_name'] = self.__terrariumEngine.get_profile_name()
      variables['person_image'] = self.__terrariumEngine.get_profile_image()

    elif 'webcam' == template or 'webcam_settings' == template:
      variables['amount_of_webcams'] = self.__terrariumEngine.get_amount_of_webcams()

    elif 'door_status' == template:
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
      response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(days=self.__caching_days)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      return template(filename,template_lookup=[root])

    staticfile = static_file(filename, root=root)
    if isinstance(staticfile,HTTPError):
      return staticfile

    if 'webcam' == root:
      staticfile.add_header('Expires',datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    else:
      staticfile.add_header('Expires',(datetime.datetime.utcnow() + datetime.timedelta(days=self.__caching_days)).strftime('%a, %d %b %Y %H:%M:%S GMT'))

    if staticfile.get_header('Last-Modified') is not None:
      staticfile.add_header('Etag',hashlib.md5(staticfile.get_header('Last-Modified')).hexdigest())

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
      result = {'ok' : True, 'title' : _('Success!'), 'message' : _('File \'%s\' is uploaded' % (upload.filename,))}
    except IOError, message:
      result['message'] = _('Duplicate file \'%s\'' % (upload.filename,))

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

  def __get_api_call(self,path):
    response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')

    result = {}
    parameters = path.strip('/').split('/')

    action = parameters[0]
    del(parameters[0])

    if 'switches' == action:
      result = self.__terrariumEngine.get_switches(parameters)

    elif 'profile' == action:
      result = self.__terrariumEngine.get_profile()

    elif 'doors' == action:
      if len(parameters) > 0 and parameters[0] == 'status':
         result = {'doors' : self.__terrariumEngine.door_status()}
      else:
        result = self.__terrariumEngine.get_doors()

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

    elif 'history' == action:
      response.headers['Expires'] = (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      result = self.__terrariumEngine.get_history(parameters)

    elif 'config' == action:
      result = self.__terrariumEngine.get_config(parameters[0] if len(parameters) == 1 else None)

    return result

  def __toggle_switch(self,switchid):
    if switchid in self.__terrariumEngine.power_switches:
      self.__terrariumEngine.power_switches[switchid].toggle()
      return {'ok' : True}

    return {'ok' : False}

  def __state_switch(self,switchid,value):
    if switchid in self.__terrariumEngine.power_switches:
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
        except Exception, err:
          # Socket connection is lost, stop looping....
          #print 'listen_for_messages error:'
          #print err
          break

        messages.task_done()

    while True:
      try:
        message = socket.receive()
      except Exception, err:
        #print 'handle_websocket error:'
        #print err
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
