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

  def log_summary_sensor_data(self, type, averagedata):
    self.__log_data(type,None,'summary',averagedata)

  def log_power_usage_water_flow(self,data):
    self.__log_data('switches',None,'summary',data)

  def log_system_data(self, data):
    for item in data:
      self.__log_data('system',item,'rawdata',data[item])

  #def get_history(self, type, subtype = None, id = None, starttime = None, stoptime = None):
  def get_history(self, parameters = [], starttime = None, stoptime = None):
    # Default return object
    history = {}
    # Every Xth minute will be returned
    modulo = 1

    history_type = parameters[0]
    del(parameters[0])

    # Define start time
    if starttime is None:
      starttime = int(time.time())
      if 'switches' != history_type:
        starttime -= starttime % (1 * 60)

    # Define stop time
    if stoptime is None:
      stoptime = starttime - (24 * 60 * 60)

    if starttime - stoptime > (8 * 60):
      modulo = 5

    if history_type == 'weather':
      field = 'rawdata'
      history_fields = { 'wind_speed' : [], 'temperature' : [], 'pressure' : [] , 'wind_direction' : [], 'rain' : [],
                        'weather' : [], 'icon' : []}
      datatypes = [history_type]

    elif history_type == 'system':
      field = 'rawdata'
      history_fields = {'load' : {'load1' : [], 'load5' : [], 'load15' : []},
                        'uptime' : [],
                        'temperature' : [],
                        'memory' : {'total' : [], 'used' : [], 'free' : []} }
      datatypes = [history_type]

    elif history_type == 'switches':
      field = 'rawdata'
      history_fields = { 'power_wattage' : [], 'water_flow' : [] , 'state' : []}
      datatypes = [history_type]

      if 'summary' in parameters:
        field = 'summary'
        del(parameters[parameters.index('summary')])
        del(history_fields['state'])
        history_fields['total_power'] = []
        history_fields['total_water'] = []

    elif history_type == 'sensors':
      field = 'rawdata'
      history_fields = { 'current' : [], 'alarm_min' : [], 'alarm_max' : [] , 'min' : [], 'max' : []}
      datatypes = ['temperature','humidity']

      if 'average' in parameters:
        field = 'summary'
        del(parameters[parameters.index('average')])

      if len(parameters) >= 1 and parameters[0] is not None and parameters[0] in ['temperature','humidity']:
        datatypes = [parameters[0]]
        del(parameters[0])

    '''elif history_type == 'environment':
      field = 'summary'
      history_fields = { 'current' : [], 'alarm_min' : [], 'alarm_max' : [] , 'min' : [], 'max' : []}
      datatypes = ['temperature','humidity']'''

    history = {}
    for datatype in datatypes:
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
            dbdata = { datatype : dbdatatmp }
            datatype = history_type
          else:
            dbdata = dbdatatmp

          if datatype not in history:
            history[datatype] = {}

          for dataid in dbdata:
            if len(parameters) > 0 and parameters[0] != dataid:
              continue

            if dataid not in history[datatype]:
              if dataid in history_fields and type(history_fields[dataid]) is dict:
                history[datatype][dataid] = copy.deepcopy(history_fields[dataid])
              elif dataid in history_fields:
                history[datatype][dataid] = []
              else:
                history[datatype][dataid] = copy.deepcopy(history_fields)

            timestamps = sorted(dbdata[dataid].keys())

            for timestamp in timestamps:
              if starttime > int(timestamp) > stoptime:
                timedata = dbdata[dataid][str(timestamp)]

                loopfields = history_fields
                if dataid in history_fields and type(history_fields[dataid]) is dict:
                  loopfields = history_fields[dataid]
                elif dataid in history_fields:
                  loopfields = { dataid : [] }
                  timedata = {dataid:timedata}

                for history_field in loopfields:
                  if history_field in timedata:
                    if history_field in history[datatype][dataid]:
                      history[datatype][dataid][history_field].append([int(timestamp) * 1000, timedata[history_field]])
                    else:
                      history[datatype][dataid].append([int(timestamp) * 1000, timedata[history_field]])

    return history
