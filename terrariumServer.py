# -*- coding: utf-8 -*-

from bottle import Bottle, static_file, response, request, auth_basic
from datetime import datetime, timedelta
from subprocess import PIPE, Popen
import psutil
import re
import copy
import operator
import os

# Needed for adding new webcams
from terrariumWebcam import terrariumWebcam

import logging
terrarium_log = logging.getLogger('root')

class terrariumServer:

  def __init__(self,host,port,admin,password,weatherObj,sensorList,powerswitchList,webcamList,environment,collector,engine,twitter,door,confObj):
    self.__startTime = datetime.now()

    self.__host = host
    self.__port = port
    self.__debug = False
    self.__webroot = 'webroot'

    self.__weather = weatherObj
    self.__sensors = sensorList
    self.__powerswitches = powerswitchList
    self.__webcams = webcamList
    self.__environment = environment
    self.__collector = collector
    self.__engine = engine
    self.__twitter = twitter
    self.__door = door
    self.__config = confObj

    self.__admin = admin
    self.__password = password

    self.__app = Bottle()
    self.__route()

    self.start()

  def start(self):
    self.__app.run(host=self.__host, port=self.__port, debug=self.__debug, server='cherrypy')

  def __route(self):
    response.set_header("Cache-Control", "public, max-age=" + str(60))

    self.__app.route('/', method="GET", callback=self.__staticfile)
    self.__app.route('/index.html', method="GET", callback=self.__staticfile)
    self.__app.route('/<filename:re:.*\.(png|jpg|gif|js|css|ico|svg|html|rrd)>', method="GET", callback=self.__staticfile)

    self.__app.route('/rrd/<rrdid>/<action:re:(get)>/<period:re:(day|week|month|year)>', method="GET", callback=self.__statsinfo)

    # Weahter information links
    # Read only urls
    self.__app.route('/weather/<action:re:(all|sunrise|sunset|city|country|temperature|lastupdate|credits|day|night)>', method="GET", callback=self.__weatherinfo)
    # Edit urls (needs authentication)
    self.__app.route('/weather/<action:re:(save)>', method="POST", callback=self.__weatherinfo,apply=auth_basic(self.__check))

    # Sensor urls
    # Read only urls
    self.__app.route('/sensor/list', method="GET", callback=self.__sensorinfo)
    self.__app.route('/sensor/list/<id:re:(temperature|humidity|light)>', method="GET", callback=self.__sensorinfo)
    self.__app.route('/sensor/<id>/<action:re:(get)>', method="GET", callback=self.__sensorinfo)
    # Edit urls (needs authentication)
    #self.__app.route('/sensor/<id>/<action:re:(toggle|on|off)>', method="GET", callback=self.__sensorinfo, apply=auth_basic(self.__check))
    self.__app.route('/sensor/<id>/<action:re:(set)>', method="POST", callback=self.__sensorinfo, apply=auth_basic(self.__check))

    # Switches urls
    # Read only urls
    self.__app.route('/switch/list', method="GET", callback=self.__switchinfo)
    self.__app.route('/switch/<id>/<action:re:(get)>', method="GET", callback=self.__switchinfo)
    # Edit urls (needs authentication)
    self.__app.route('/switch/<id>/<action:re:(toggle|on|off)>', method="GET", callback=self.__switchinfo, apply=auth_basic(self.__check))
    self.__app.route('/switch/<id>/<action:re:(set)>', method="POST", callback=self.__switchinfo, apply=auth_basic(self.__check))

    # Webcam urls
    # Read only urls
    self.__app.route('/webcam/list', method="GET", callback=self.__webcaminfo)
    self.__app.route('/webcam/<id>/<action:re:(get|max_zoom)>', method="GET", callback=self.__webcaminfo)
    # Edit urls (needs authentication)
    self.__app.route('/webcam/<action:re:(add)>', method="POST", apply=auth_basic(self.__check), callback=self.__webcaminfo)
    self.__app.route('/webcam/<id>/<action:re:(set)>', method="POST", apply=auth_basic(self.__check), callback=self.__webcaminfo)

    # Environment actions
    # Read only urls
    self.__app.route('/environment/<id:re:(lights|humidity|heater|door|all)>/<action:re:(status|online)>', callback=self.__environmentinfo)
    # Edit urls (needs authentication)
    self.__app.route('/environment/<id:re:(lights|humidity|heater|door)>/<action:re:(settings)>', callback=self.__environmentinfo,apply=auth_basic(self.__check))
    self.__app.route('/environment/<id:re:(lights|humidity|heater|door)>/<action:re:(toggle)>/<part:re:(engine|trigger|current)>', callback=self.__environmentinfo,apply=auth_basic(self.__check))


    self.__app.route('/environment/<id:re:(lights|humidity|heater|door)>/<action:re:(settings)>/<part:re:(save)>',method="POST", callback=self.__environmentinfo,apply=auth_basic(self.__check))

    # System actions
    # Read only urls
    self.__app.route('/system/<id:re:(all|engine|environment|collector|webserver|twitter|sms|loglevel|cpuload|cputemp|cpuspeed|uptime|memory|wattage|waterflow)>/<action:re:(status|online|graph)>', callback=self.__systeminfo)
    # Edit urls (needs authentication)
    # self.__app.route('/system/<id:re:(engine|environment|collector|logger)>/<action:re:(toggle)>/<part:re:(engine|trigger|current)>', callback=self.__environmentinfo,apply=auth_basic(self.__check))

    # Authentication check url. Does only check the HTTP auth header. No session data
    self.__app.route('/auth/<action:re:(login|update)>', method="POST", callback=self.__authenticate, apply=auth_basic(self.__check))


    # List of available urls
    self.__app.route('/methods', method="GET", callback=self.__methods)

    @self.__app.hook('after_request')
    def enable_cors():
      response.headers['Access-Control-Allow-Origin'] = '*'

  def __check(self,user, passwd):
    passwds = { self.__admin : self.__password,}
    if passwd and passwds.get(user) == passwd:
      return True
    return False

  def __authenticate(self,action):
    value = False
    if 'update' == action:
      new_username = request.forms.get('username')
      new_password1 = request.forms.get('password1')
      new_password2 = request.forms.get('password2')
      if new_password1 == new_password2:
        self.__admin = new_username
        self.__password = new_password1
        self.__config.setServerUsername(self.__admin)
        self.__config.setServerPassword(self.__password)
        value = True

    elif 'login' == action:
      value = True

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__authenticate', 'value' : value}

  def __statsinfo(self,rrdid,action='get',period = 'day'):
    value = []
    if 'environment_' in rrdid:
       data = {}
       if 'environment_humidity' == rrdid:
         data = self.__environment.getHumidityStatus()
       elif 'environment_heater' == rrdid or 'environment_light' == rrdid:
         pass

       for type in ['sensors']:
         amount = float(len(data[type]))
         firstrun = True

         for rrdid in data[type]:
           if 'sensors' == type:
             rrdid = 'sensor_' + rrdid['id']
           elif 'switches' == type:
             rrdid = 'switch_' + rrdid['id']

           rrdlist = self.__collector.getRRDDatabase(rrdid,period)
           for i, rrddata in enumerate(rrdlist):
             if firstrun == True:
               value.append(copy.deepcopy(rrddata))

             for key in rrddata:
               if 'timestamp' == key:
                 continue

               if firstrun == True:
                 value[i][key] = 0

               value[i][key] = str(float(value[i][key]) + (float(rrddata[key]) / amount))

           firstrun = False
         
         del value[-1]

    else:
      value = self.__collector.getRRDDatabase(rrdid,period)

    response.set_header("Cache-Control", "public, max-age=" + str(60))
    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__statsinfo', 'value' : value}

  def __systeminfo(self,id, action = 'online'):
    global startTime
    value = -1
    if 'all' == id:
      value = {}
      if 'online' == action:
        value['engine'] = self.__engine.online()
        value['environment'] = self.__environment.online()
        value['collector'] = self.__collector.online()
        value['webserver'] = True

        value['twitter'] = self.__twitter.online()['online']
        value['loglevel'] = True #self.__logger.getLogLevel() > 0

        value['uptime'] = (datetime.now()-self.__startTime).total_seconds()
        value['memory'] = self.__getMemory()
        value['cpuload'] = self.__getCPULoad()
        value['cputemp'] = self.__getCPUTemp()
        value['cpuspeed'] = self.__getCPUSpeed()

        value['wattage'] = self.__getWattage()
        value['waterflow'] = self.__getWaterflow()

    elif 'engine' == id:
      if 'online' == action:
        value = self.__engine.online()

    elif 'environment' == id:
      if 'online' == action:
        value = self.__environment.online()

    elif 'collector' == id:
      if 'online' == action:
        value = self.__collector.online()

    elif 'webserver' == id:
      if 'online' == action:
        value = True

    elif 'twitter' == id:
      if 'status' == action or 'online' == action:
        value = self.__twitter.online()

    elif 'loglevel' == id:
      if 'status' == action:
        value = 1 #self.__logger.getLogLevel()

    elif 'uptime' == id:
      if 'status' == action or 'online' == action:
        value = (datetime.now() - self.__startTime).total_seconds()

    elif 'memory' == id:
      if 'status' == action or 'online' == action:
        value = self.__getMemory();

    elif 'cpuload' == id:
      if 'status' == action or 'online' == action:
        value = self.__getCPULoad()

    elif 'cputemp' == id:
      if 'status' == action or 'online' == action:
        value = self.__getCPUTemp()

    elif 'cpuspeed' == id:
      if 'status' == action or 'online' == action:
        value = self.__getCPUspeed()

    elif 'wattage' == id:
      if 'status' == action or 'online' == action:
        value = self.__getWattage()
      elif 'graph' == action:
        value = self.__getWattageHistory()

    elif 'waterflow' == id:
      if 'status' == action or 'online' == action:
        value = self.__getWaterflow()

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__system:' + action, 'value' : value, 'part' : id}

  def __getMemory(self):
    try:
      mem = psutil.virtual_memory()
    except Exception, err:
      mem = psutil.phymem_usage()

    return (float(mem.used) / float(mem.total)) * 100

  def __getCPULoad(self):
    return psutil.cpu_percent(interval=None)

  def __getCPUTemp(self):
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

  def __getCPUSpeed(self):
    process = Popen(['vcgencmd', 'measure_clock arm'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:])

  def __environmentinfoAll(self):
    value = {}
    value['lights'] = self.__environmentinfo('lights')
    value['heater'] = self.__environmentinfo('heater')
    value['humidity'] = self.__environmentinfo('humidity')
    value['door'] = self.__environmentinfo('door')
    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__environment:' + 'status', 'value' : value, 'part' : 'all'}

  def __getWattage(self):
    current = self.__config.getPiWattage()
    max = self.__config.getPiWattage()
    for switchid,switch in self.__powerswitches.iteritems():
      max += switch.getWattage()
      current += switch.getCurrentWattage()

    return {'current': current, 'max': max}

  def __getWattageHistory(self,period = 'day'):
    interval = 5 * 60 # 300 seconds or 5 minutes
    total_wattage = {}
    switches = []

    for switchid,switch in self.__powerswitches.iteritems():
      switches.append('s' + switch.getID())
      for timestamp,wattage_data in (switch.get_wattage_usage()).iteritems():
        # Shift to every 5 minutes
        timestamp = int(timestamp)
        timestamp -= timestamp % interval
        timestamp = str(timestamp)

        if timestamp not in total_wattage:
          total_wattage[timestamp] = {}
          total_wattage[timestamp]['timestamp'] = int(timestamp) * 1000
          total_wattage[timestamp]['sRPI'] = self.__config.getPiWattage()

        total_wattage[timestamp]['s' + switch.getID()] = wattage_data

    # Start looping hole day to fill the gaps
    now = datetime.now()
    loopstamp = int(datetime(now.year,now.month,now.day,0,0,0).strftime('%s'))
    data = {'timestamp':0 , 'sRPI' : self.__config.getPiWattage()}
    for switchid in switches:
        data[switchid] = 0

    while loopstamp < int(now.strftime('%s')):
      if loopstamp not in total_wattage:
        total_wattage[loopstamp] = dict(data)
        total_wattage[loopstamp]['timestamp'] = loopstamp * 1000

      loopstamp += interval

    returndata = []
    laststamp = 0
    firststamp = 0

    # sorting on timestamp field
    for timestamp in sorted(total_wattage.iterkeys()):
      data = total_wattage[timestamp]
      
      if firststamp == 0:
        firststamp = int(timestamp)
      laststamp = int(timestamp)
      for switchid in switches:
        if switchid not in data:
          data[switchid] = 0

      returndata.append(data)

    return returndata

  def __getWaterflow(self):
    current = 0
    max = 0
    for switchid,switch in self.__powerswitches.iteritems():
      max += switch.getWaterflow()
      current += switch.getCurrentWaterflow()

    return {'current': current, 'max': max}

  def __environmentinfo(self,id, action = 'status', part = 'current'):
    if 'all' == id and 'status' == action:
      return self.__environmentinfoAll()

    value = -1
    if 'lights' == id:
      if 'status' == action:
        value = self.__environment.getLightsStatus()
      elif 'settings' == action:
        if 'save' == part:
          value = self.__environment.setEnvironmentLightConfig(
              request.forms.get('enabed'),
              request.forms.get('on'),
              request.forms.get('off'),
              request.forms.get('switch'),
              '',
              request.forms.get('minhours'),
              request.forms.get('maxhours'),
              request.forms.get('shifthours'),
            )
        else:
          value = self.__environment.getLightSettings()

      elif 'toggle' == action:
        if 'engine' == part:
          self.__environment.toggleLightsEngine()
          value = self.__environment.getLightsStatus()
        elif 'trigger' == part:
          value = self.__environment.toggleLightsTrigger()
        elif 'current' == part:
          value = self.__environment.toggleLights()

    elif 'humidity' == id:
      if 'status' == action:
        value = self.__environment.getHumidityStatus()
      elif 'settings' == action:
        if 'save' == part:
          value = self.__environment.setEnvironmentHumidityConfig(
              request.forms.get('enabed'),
              request.forms.get('switch'),
              request.forms.get('sensor'),
              request.forms.get('timeout'),
              request.forms.get('duration'),
              request.forms.get('night_enabled'),
            )
        else:
          value = self.__environment.getHumiditySettings()

      elif 'toggle' == action:
        if 'engine' == part:
          self.__environment.toggleHumidityEngine()
          value = self.__environment.getHumidityStatus()
        elif 'trigger' == part:
          value = self.__environment.toggleHumidityTrigger()
        elif 'current' == part:
          value = self.__environment.toggleHumidity()

    elif 'heater' == id:
      if 'status' == action:
        value = self.__environment.getHeaterStatus()
      elif 'settings' == action:
        if 'save' == part:
          value = self.__environment.setEnvironmentHeaterConfig(
              request.forms.get('enabed'),
              request.forms.get('switch'),
              request.forms.get('sensor'),
              request.forms.get('modus'),
              request.forms.get('on'),
              request.forms.get('off'),
              request.forms.get('dayactive')
            )
        else:
          value = self.__environment.getHeaterSettings()

      elif 'toggle' == action:
        if 'engine' == part:
          self.__environment.toggleHeaterEngine()
          value = self.__environment.getHeaterStatus()
        elif 'trigger' == part:
          value = self.__environment.toggleHeaterTrigger()
        elif 'current' == part:
          value = self.__environment.toggleHeater()

    elif 'door' == id:
      if 'status' == action:
        value = 'open' if self.__door.open() else 'closed'

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__environment:' + action, 'value' : value, 'part' : id}

  def __staticfile(self,filename = 'index.html'):
    extension = filename.split(".")[-1]
    cache_timeout = 60 * 60 * 24 * 7 # default cache timeout is 1 week
    if 'webcam/' in filename:
      cache_timeout = 30 # Web cam tiles short caching
      if not os.path.isfile(self.__webroot + '/' + filename):
        cache_timeout = 60 * 60 * 24 * 7
        filename = 'webcam/black.jpg'

    response = static_file(filename, root=self.__webroot)
    response.set_header("Cache-Control", "public, max-age=" + str(cache_timeout))
    return response

  def __webcaminfo(self,action = 'list', id = 'all'):
    value = -1
    if 'list' == action:
      value = []
      for webcamid,webcam in self.__webcams.iteritems():
        value.append({'id' : webcam.getID(),
                      'name' : webcam.getName(),
                      'url' : webcam.getUrl(),
                      'archive' : webcam.getArchive(),
                      'rotation' : webcam.getRotation(),
                      'height' : webcam.getHeight(),
                      'width' :webcam.getWidth(),
                      'max_zoom' : webcam.getMaxZoom(),
                      'lastupdate' : int(webcam.getLastUpdateTimeStamp().strftime('%s'))
                    })

    elif 'get' == action:
      if id in self.__webcams:
        value = { 'id' : self.__webcams[id].getID(),
                  'name' : self.__webcams[id].getName(),
                  'url' : self.__webcams[id].getUrl(),
                  'archive' : self.__webcams[id].getArchive(),
                  'rotation' : self.__webcams[id].getRotation(),
                  'height' : self.__webcams[id].getHeight(),
                  'width' :self.__webcams[id].getWidth(),
                  'max_zoom' : self__webcams[id].getMaxZoom(),
                  'lastupdate' : int(self.__webcams[id].getLastUpdateTimeStamp().strftime('%s'))
                }
    elif 'set' == action:
      if id in self.__webcams:
        if request.forms.get('name'):
          self.__webcams[id].setName(request.forms.get('name'))
        if request.forms.get('url'):
          self.__webcams[id].setUrl(request.forms.get('url'))

        value = True

    elif 'add' == action:
      webCam = terrariumWebcam(request.forms.get('name'), request.forms.get('url'), request.forms.get('archiving'), request.forms.get('rotation'),self.__config)
      webCam.saveConfig();
      self.__webcams[webCam.getID()] = webCam

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__webcaminfo:' + action, 'value' : value}

  def __switchinfo(self,action = 'list', id = 'all'):
    value = -1
    if 'list' == action:
      value = []
      for switchid,switch in self.__powerswitches.iteritems():
        value.append({'id' : switch.getID(),
                      'name' : switch.getName(),
                      'nr' : int(switch.getNr()),
                      'current' :switch.getState(),
                      'wattage' :switch.getWattage(),
                      'waterflow' :switch.getWaterflow(),
                      'lastupdate' : int(switch.getLastUpdateTimeStamp().strftime('%s'))
                    })

    elif 'get' == action:
      if id in self.__powerswitches:
        value = { 'id' : self.__powerswitches[id].getID(),
                  'name' : self.__powerswitches[id].getName(),
                  'nr' : int(self.__powerswitches[id].getNr()),
                  'current' :self.__powerswitches[id].getState(),
                  'wattage' :switch.getWattage(),
                  'waterflow' :switch.getWaterflow(),
                  'lastupdate' : int(self.__powerswitches[id].getLastUpdateTimeStamp().strftime('%s'))
                }

    elif 'set' == action:
      if id in self.__powerswitches:
        if request.forms.get('name'):
          self.__powerswitches[id].setName(request.forms.get('name'))
        if request.forms.get('wattage'):
          self.__powerswitches[id].setWattage(request.forms.get('wattage'))
        if request.forms.get('waterflow'):
          self.__powerswitches[id].setWaterflow(request.forms.get('waterflow'))

        value = True

    elif 'toggle' == action:
      if id in self.__powerswitches:
        value = self.__powerswitches[id].toggle() == True

    elif 'on' == action:
      if id in self.__powerswitches:
        value = self.__powerswitches[id].on()

    elif 'off' == action:
      if id in self.__powerswitches:
        value = self.__powerswitches[id].off()

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__switchinfo:' + action, 'value' : value}

  def __sensorinfo(self,action = 'list', id = 'all'):
    value = -1
    if 'list' == action:
      value = []
      for sensorid,sensor in self.__sensors.iteritems():
        if 'all' == id or sensor.getType() == id:
          settings = sensor.getSettings()
          settings['lastupdate'] = int(sensor.getLastUpdateTimeStamp().strftime('%s'))
          value.append(settings)

    elif 'get' == action:
      if id in self.__sensors:
        value = self.__sensors[id].getSettings()
        value['lastupdate'] = int(sensor.getLastUpdateTimeStamp().strftime('%s'))

    elif 'set' == action:
      if id in self.__sensors:
        if request.forms.get('name'):
          self.__sensors[id].setName(request.forms.get('name'))
        if request.forms.get('limit_min'):
          self.__sensors[id].setMinLimit(request.forms.get('limit_min'))
        if request.forms.get('limit_max'):
          self.__sensors[id].setMaxLimit(request.forms.get('limit_max'))
        if request.forms.get('alarm_enabled'):
          self.__sensors[id].setAlarm(request.forms.get('alarm_enabled'))
        if request.forms.get('logging_enabled'):
          self.__sensors[id].setLogging(request.forms.get('logging_enabled'))
        if request.forms.get('indicator'):
          self.__sensors[id].setIndicator(request.forms.get('indicator'))

        value = True

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__sensorinfo:' + action, 'value' : value}

  def __weatherinfo(self,action = ''):
    value = -1
    if 'all' == action:
      value = { 'xmlsource'   : self.__weather.getXMLUrl(),
                'sunrise'     : int(self.__weather.getSunRiseTime().strftime('%s')),
                'sunset'      : int(self.__weather.getSunSetTime().strftime('%s')),
                'city'        : self.__weather.getCity(),
                'country'     : self.__weather.getCountry(),
                'location'    : self.__weather.getLocation(),
                'locationtime': int(self.__weather.getLocationTime().strftime('%s')),
                'lastupdate'  : int(self.__weather.getLastUpdateTimeStamp().strftime('%s')),
                'credits'     : self.__weather.getCredits(),
                'day'         : self.__weather.isDaytime(),
                'temperature' : { 'current' : self.__weather.getCurrentTemperature(),
                                  'max' : self.__weather.getMaximumTemperature(),
                                  'min' : self.__weather.getMinimumTemperature(),
                                  'maxlimit'    : self.__weather.getMaximumTemperatureLimit(),
                                  'minlimit'    : self.__weather.getMinimumTemperatureLimit(),
                                  'alarm'    : self.__weather.getAlarm(),
                                  'alarm_enabled'    : self.__weather.isAlarmActive(),
                                  'logging_enabled'    : self.__weather.isLoggingEnabled(),
                                  'indicator'    : self.__weather.getIndicator()
                                  }
              }
    elif'set' == action:
      if request.forms.get('xmlsource'):
        self.__weather.setXMLUrl(request.forms.get('xmlsource'))
      if request.forms.get('limit_max'):
        self.__weather.setMaximumTemperatureLimit(request.forms.get('limit_max'))
      if request.forms.get('limit_min'):
        self.__weather.setMinimumTemperatureLimit(request.forms.get('limit_min'))

      value = True
    elif 'sunrise' == action:
      value = int(self.__weather.getSunRiseTime().strftime('%s'))
    elif 'sunset' == action:
      value = int(self.__weather.getSunSetTime().strftime('%s'))
    elif 'city' == action:
      value = self.__weather.getCity()
    elif 'country' == action:
      value = self.__weather.getCountry()
    elif 'location' == action:
      value = self.__weather.getLocation()
    elif 'lastupdate' == action:
      value = int(self.__weather.getLastUpdateTimeStamp().strftime('%s'))
    elif 'credits' == action:
      value = self.__weather.getCredits()

    elif 'day' == action:
      value = self.__weather.isDaytime()
    elif 'night' == action:
      value = not self.__weather.isDaytime()

    elif 'temperature' == action:
      value = { 'current' : self.__weather.getCurrentTemperature(),
                'max' : self.__weather.getMaximumTemperature(),
                'min' : self.__weather.getMinimumTemperature(),
                'maxlimit'    : self.__weather.getMaximumTemperatureLimit(),
                'minlimit'    : self.__weather.getMinimumTemperatureLimit(),
                'alarm'    : self.__weather.getAlarm(),
                'alarm_enabled'    : self.__weather.isAlarmActive(),
                'logging_enabled'    : self.__weather.isLoggingEnabled(),
                'indicator'    : self.__weather.getIndicator()
              }

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__weatherinfo:' + action, 'value' : value}

  def __methods(self):
    returnValue = []
    for route in self.__app.routes:
      returnValue.append({'url' : route.rule})

    return {'time': int((datetime.now()).strftime('%s')),'cmd' : '__methods', 'value' : returnValue}
