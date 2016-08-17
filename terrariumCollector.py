# -*- coding: utf-8 -*-
import sqlite3
import time
import json
import copy

class terrariumCollector():
  database = 'history.db'

  def __init__(self):
    self.db = sqlite3.connect(terrariumCollector.database)
    self.db.row_factory = sqlite3.Row
    self.__create_database_structure()

  def __create_database_structure(self):
    with self.db:
      cur = self.db.cursor()
      cur.execute('CREATE TABLE IF NOT EXISTS data (day DATE, type VARCHAR(15), summary TEXT, rawdata TEXT)')
      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS historykey ON data(day,type)')
      self.db.commit()

  def __log_data(self,type,id,datatype,newdata):
    now = int(time.time())
    if 'switches' != type:
      now -= (now % 60)

    data = {'rawdata' : {}, 'summary' : {}}
    with self.db:
      cur = self.db.cursor()
      cur.execute("SELECT rawdata, summary FROM data WHERE day = date(?,'unixepoch') and type=?", (now, type,))
      rows = cur.fetchall()
      if len(rows) == 1:
        if rows[0]['rawdata'] != '':
          data['rawdata'] = json.loads(rows[0]['rawdata'])

        if rows[0]['summary'] != '':
          data['summary'] = json.loads(rows[0]['summary'])

    if type == 'weather' or datatype == 'summary':
      data[datatype][now] = newdata
    else:
      if id not in data[datatype]:
        data[datatype][id] = {}

      data[datatype][id][now] = newdata

    with self.db:
      cur = self.db.cursor()
      cur.execute("REPLACE INTO data (day, type, rawdata, summary) VALUES (date(?,'unixepoch'),?,?,?)",
                  (now, type,json.dumps(data['rawdata']),json.dumps(data['summary'])))
      self.db.commit()

  def log_switch_data(self,switch):
    switch_id = switch['id']
    del(switch['id'])
    del(switch['name'])
    del(switch['nr'])
    self.__log_data('switches',switch_id,'rawdata',switch)

  def log_weather_data(self,weather):
    del(weather['from'])
    del(weather['to'])
    self.__log_data('weather',None,'rawdata',weather)

  def log_sensor_data(self,sensor):
    sensor_data  = sensor.get_data()
    del(sensor_data['id'])
    del(sensor_data['address'])
    del(sensor_data['type'])
    del(sensor_data['name'])
    self.__log_data(sensor.get_type(),sensor.get_id(),'rawdata',sensor_data)

  def log_environment_data(self, type, averagedata):
    self.__log_data(type,None,'summary',averagedata)

  def log_power_usage_water_flow(self,data):
    self.__log_data('switches',None,'summary',data)

  def log_system_data(self, data):
    for item in data:
      self.__log_data('system',item,'rawdata',data[item])

  def get_history(self, type, subtype = None, id = None, starttime = None, stoptime = None):
    #print 'get history: ' + str(type) + ' - ' + str(subtype) + ' - ' + str(id)
    # Default return object
    history = {}
    # Every Xth minute will be returned
    modulo = 1

    # Define start time
    if starttime is None:
      starttime = int(time.time())
      if 'switches' != type:
        starttime -= starttime % (1 * 60)

    # Define stop time
    if stoptime is None:
      stoptime = starttime - (24 * 60 * 60)

    if starttime - stoptime > (8 * 60):
      modulo = 5

    if type == 'weather':
      field = 'rawdata'
      history_fields = { 'wind_speed' : [], 'temperature' : [], 'pressure' : [] , 'wind_direction' : [], 'rain' : [],
                        'weather' : [], 'icon' : []}
      datatypes = [subtype]

    elif type == 'system':
      field = 'rawdata'
      history_fields = { 'load1' : [], 'load5' : [], 'load15' : [], 'uptime' : [] }
      datatypes = [type]

    elif type == 'switches':
      field = 'rawdata'
      history_fields = { 'power_wattage' : [], 'water_flow' : [] , 'state' : []}
      datatypes = [type]

      if subtype == 'summary':
        field = 'summary'
        history_fields = { 'total_power' : [], 'total_water' : []}

    elif type == 'sensors' and subtype in ['temperature','humidity','summary']:
      field = 'rawdata'
      history_fields = { 'current' : [], 'alarm_min' : [], 'alarm_max' : [] , 'min' : [], 'max' : []}
      datatypes = [subtype]

      if subtype == 'summary':
        field = 'summary'
        datatypes = ['temperature','humidity']
      elif id == 'summary':
        field = 'summary'

    history = {}
    for datatype in datatypes:
      history[datatype] = {}
      with self.db:
        cur = self.db.cursor()
        cur.execute('''SELECT day, ''' + field + ''' FROM data
                    WHERE day >= date(?,"unixepoch") and day <= date(?,"unixepoch") and type=?
                    ORDER BY day ASC''', (stoptime,starttime,datatype,))
        rows = cur.fetchall()

        for row in rows:
          if row[field] is None or row[field] == '':
            continue

          dbdatatmp = json.loads(row[field])

          if field == 'summary':
            dbdata = { 'summary' : dbdatatmp }
          elif id is None:
            dbdata = dbdatatmp
          else:
            dbdata = { id : dbdatatmp[id] }

          for dataid in dbdata:
            if dataid not in history[datatype]:
              history[datatype][dataid] = copy.deepcopy(history_fields)

            timestamps = sorted(dbdata[dataid].keys())

            for timestamp in timestamps:
              if starttime > int(timestamp) > stoptime:
                timedata = dbdata[dataid][str(timestamp)]

                #if type == 'sensors' and int(timestamp) % (modulo * 60) == 0:
                for history_field in history_fields:
                  if history_field in timedata:
                    history[datatype][dataid][history_field].append([int(timestamp) * 1000, timedata[history_field]])

    return history
