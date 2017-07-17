# -*- coding: utf-8 -*-
import sqlite3
import time
import json
import copy
import os

import logging
logger = logging.getLogger(__name__)

class terrariumCollector():
  database = 'history.db'

  def __init__(self):
    logger.info('Setting up collector database %s' % (terrariumCollector.database,))
    self.__recovery = False
    self.__connect()
    # Store data every Xth minute. Except switches.
    self.modulo = 5 * 60
    self.__create_database_structure()
    logger.info('TerrariumPI Collecter is ready')

  def __connect(self):
    self.db = sqlite3.connect(terrariumCollector.database)
    self.db.row_factory = sqlite3.Row
    logger.info('Database connection created to database %s' % (terrariumCollector.database,))

  def __create_database_structure(self):
    with self.db:
      cur = self.db.cursor()
      cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                      (id VARCHAR(50),
                       type VARCHAR(15),
                       timestamp INTEGER(4),
                       current FLOAT(4),
                       limit_min FLOAT(4),
                       limit_max FLOAT(4),
                       alarm_min FLOAT(4),
                       alarm_max FLOAT(4),
                       alarm INTEGER(1) )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS sensor_data_unique ON sensor_data(id,type,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_timestamp ON sensor_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_type ON sensor_data(type)')
      cur.execute('CREATE INDEX IF NOT EXISTS sensor_data_id ON sensor_data(id)')

      cur.execute('''CREATE TABLE IF NOT EXISTS switch_data
                      (id VARCHAR(50),
                       timestamp INTEGER(4),
                       state INTERGER(1),
                       power_wattage FLOAT(2),
                       water_flow FLOAT(2)
                        )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS switch_data_unique ON switch_data(id,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS switch_data_timestamp ON switch_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS switch_data_id ON switch_data(id)')

      cur.execute('''CREATE TABLE IF NOT EXISTS door_data
                      (id INTEGER(4),
                       timestamp INTEGER(4),
                       state TEXT CHECK( state IN ('open','closed') ) NOT NULL DEFAULT 'closed'
                       )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS door_data_unique ON door_data(id,timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS door_data_timestamp ON door_data(timestamp ASC)')
      cur.execute('CREATE INDEX IF NOT EXISTS door_data_id ON door_data(id)')

      cur.execute('''CREATE TABLE IF NOT EXISTS weather_data
                      (timestamp INTEGER(4),
                       wind_speed FLOAT(4),
                       temperature FLOAT(4),
                       pressure FLOAT(4),
                       wind_direction VARCHAR(50),
                       weather VARCHAR(50),
                       icon VARCHAR(50)
                        )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS weather_data_unique ON weather_data(timestamp ASC)')


      cur.execute('''CREATE TABLE IF NOT EXISTS system_data
                       (timestamp INTEGER(4),
                       load_load1 FLOAT(4),
                       load_load5 FLOAT(4),
                       load_load15 FLOAT(4),
                       uptime INTEGER(4),
                       temperature FLOAT(4),
                       cores VARCHAR(25),
                       memory_total INTEGER(6),
                       memory_used INTEGER(6),
                       memory_free INTEGER(6)
                        )''')

      cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS system_data_unique ON system_data(timestamp ASC)')

    self.db.commit()

  def __log_data(self,type,id,newdata):
    if self.__recovery:
      logger.warn('TerrariumPI Collecter is in recovery mode. Cannot store new logging data!')
      return

    now = int(time.time())
    rows = []
    if 'switches' != type and 'door' != type:
      now -= (now % 60)

    try:
      with self.db:
        cur = self.db.cursor()

        if type in ['humidity','temperature']:
          cur.execute('REPLACE INTO sensor_data (id, type, timestamp, current, limit_min, limit_max, alarm_min, alarm_max, alarm) VALUES (?,?,?,?,?,?,?,?,?)',
                      (id, type, now, newdata['current'], newdata['limit_min'], newdata['limit_max'], newdata['alarm_min'], newdata['alarm_max'], newdata['alarm']))

        if type in ['switches']:
          cur.execute('REPLACE INTO switch_data (id, timestamp, state, power_wattage, water_flow) VALUES (?,?,?,?,?)',
                      (id, now, newdata['state'], newdata['power_wattage'], newdata['water_flow']))

        if type in ['door']:
          cur.execute('REPLACE INTO door_data (id, timestamp, state) VALUES (?,?,?)',
                      (id, now, newdata))

        if type in ['weather']:
          cur.execute('REPLACE INTO weather_data (timestamp, wind_speed, temperature, pressure, wind_direction, weather, icon) VALUES (?,?,?,?,?,?,?)',
                      (now, newdata['wind_speed'], newdata['temperature'], newdata['pressure'], newdata['wind_direction'], newdata['weather'], newdata['icon']))

        if type in ['system']:
          cur.execute('REPLACE INTO system_data (timestamp, load_load1, load_load5, load_load15, uptime, temperature, cores, memory_total, memory_used, memory_free) VALUES (?,?,?,?,?,?,?,?,?,?)',
                      (now, newdata['load']['load1'], newdata['load']['load5'], newdata['load']['load15'], newdata['uptime'], newdata['temperature'], newdata['cores'], newdata['memory']['total'], newdata['memory']['used'], newdata['memory']['free']))

        self.db.commit()
    except sqlite3.DatabaseError as ex:
      logger.error('TerrariumPI Collecter exception! %s', (ex,))
      if 'database disk image is malformed' == str(ex):
        self.__recover()

  def __recover(self):
    # Based on: http://www.dosomethinghere.com/2013/02/20/fixing-the-sqlite-error-the-database-disk-image-is-malformed/
    # Enable recovery status
    self.__recovery = True
    logger.warn('TTerrariumPI Collecter recovery mode is starting! %s', (self.__recovery,))

    # Create empty sql dump variable
    sqldump = ''
    lines = 0
    with open('.recovery.sql', 'w') as f:
      # Dump SQL data line for line
      for line in self.db.iterdump():
        lines += 1
        sqldump += line + "\n"
        f.write('%s\n' % line)

    logger.warn('TerrariumPI Collecter recovery mode created SQL dump of %s lines and %s bytes!', (lines,strlen(sqldump),))

    # Delete broken db
    os.remove(terrariumCollector.database)
    logger.warn('TerrariumPI Collecter recovery mode deleted faulty database from disk %s', (terrariumCollector.database,))

    # Reconnect will recreate the db
    logger.warn('TerrariumPI Collecter recovery mode starts reconnecting database to create a new clean database at %s', (terrariumCollector.database,))
    self.__connect()
    cur = self.db.cursor()
    # Load the SQL data back to db
    cur.executescript(sqldump)
    logger.warn('TerrariumPI Collecter recovery mode restored the old data in a new database. %s', (terrariumCollector.database,))

    # Return to normal mode
    self.__recovery = False
    logger.warn('TerrariumPI Collecter recovery mode is finished! %s', (self.__recovery,))

  def log_switch_data(self,switch):
    switch_id = switch['id']
    del(switch['id'])
    del(switch['hardwaretype'])
    del(switch['address'])
    del(switch['name'])
    self.__log_data('switches',switch_id,switch)

  def log_door_data(self,door):
    self.__log_data('door',door['id'], door['state'])

  def log_weather_data(self,weather):
    del(weather['from'])
    del(weather['to'])
    self.__log_data('weather',None,weather)

  def log_sensor_data(self,sensor):
    sensor_data  = sensor.get_data()
    del(sensor_data['id'])
    del(sensor_data['hardwaretype'])
    del(sensor_data['address'])
    del(sensor_data['type'])
    del(sensor_data['name'])
    self.__log_data(sensor.get_type(),sensor.get_id(),sensor_data)

  def log_system_data(self, data):
    self.__log_data('system',None,data)

  def log_total_power_and_water_usage(self,pi_wattage):
    if self.__recovery:
      logger.warn('TerrariumPI Collecter is in recovery mode. Cannot store new power and water total usage!')
      return

    today = int(time.time())
    time_past = today % 86400
    today -= time_past
    data = {'day' : today, 'on': 0, 'power' : time_past * pi_wattage, 'water' : 0}

    sql = '''SELECT
              switch_data_duration.id,
              switch_data_duration.timestamp AS aan,
              switch_data.timestamp AS uit,
              switch_data.power_wattage,
              switch_data.water_flow ,
              switch_data.timestamp - max(switch_data_duration.timestamp) AS duration
            FROM switch_data left JOIN switch_data as switch_data_duration
              ON switch_data.id = switch_data_duration.id
              AND switch_data.timestamp > switch_data_duration.timestamp
              AND switch_data_duration.id <> 'total'
            WHERE switch_data_duration.id NOT null
              AND switch_data.id <> 'total'
              AND switch_data.timestamp >= ?
              AND switch_data_duration.timestamp < ?
            GROUP BY switch_data.id, switch_data.timestamp
            HAVING switch_data_duration.state = 1
              AND switch_data.timestamp >= ?
              AND switch_data_duration.timestamp < ?
            ORDER BY aan ASC'''

    filters = (today,today+86400,today,today+86400,)
    rows = []
    try:
      with self.db:
        cur = self.db.cursor()
        cur.execute(sql, filters)
        rows = cur.fetchall()
    except sqlite3.DatabaseError as ex:
      logger.error('TerrariumPI Collecter exception! %s', (ex,))
      if 'database disk image is malformed' == str(ex):
        self.__recover()

    for row_tmp in rows:
      row = {'aan': row_tmp['aan'],
             'uit':row_tmp['uit'],
             'duration' : row_tmp['duration'],
             'power_wattage' : row_tmp['power_wattage'],
             'water_flow' : row_tmp['water_flow']}

      if row['aan'] < today:
        row['duration'] -= today - row['aan']
        row['aan'] = today

      if row['uit'] > today+86400:
        row['duration'] -= row['uit'] - (today+86400)
        row['uit'] = today+86400

      data['on'] += row['duration']
      data['power'] += row['duration'] * row['power_wattage']
      data['water'] += row['duration'] * row['water_flow']

    # Power is in Wh (Watt/hour) so devide by 3600 seconds
    data['power'] /= 3600
    # Water is in Liters
    data['water'] /= 60

    try:
      with self.db:
        cur = self.db.cursor()
        cur.execute('REPLACE INTO switch_data (id, timestamp, state, power_wattage, water_flow) VALUES (?,?,?,?,?)',
                    ('total', today, data['on'], data['power'], data['water']))
        self.db.commit()
    except sqlite3.DatabaseError as ex:
      logger.error('TerrariumPI Collecter exception! %s', (ex,))
      if 'database disk image is malformed' == str(ex):
        self.__recover()

  def get_history(self, parameters = [], starttime = None, stoptime = None):
    # Default return object
    history = {}
    periods = {'day' : 1 * 24,
               'week' : 7 * 24,
               'month' : 30 * 24,
               'year' : 365 * 24}
    modulo = self.modulo

    logtype = parameters[0]
    del(parameters[0])

    # Define start time
    if starttime is None:
      starttime = int(time.time())

    # Define stop time
    if stoptime is None:
      stoptime = starttime - (24 * 60 * 60)

    if len(parameters) > 0 and parameters[-1] in periods.keys():
      stoptime = starttime - periods[parameters[-1]] * 60 * 60
      modulo = (periods[parameters[-1]] / 24) * self.modulo
      del(parameters[-1])

    sql = ''
    filters = (stoptime,starttime,)
    if logtype == 'sensors':
      fields = { 'current' : [], 'alarm_min' : [], 'alarm_max' : [] , 'limit_min' : [], 'limit_max' : []}
      sql = 'SELECT id, type, timestamp,' + ', '.join(fields.keys()) + ' FROM sensor_data WHERE timestamp >= ? and timestamp <= ? AND timestamp % ' + str(modulo) + ' = 0'

      if len(parameters) > 0 and parameters[0] == 'average':
        sql = 'SELECT "average" as id, type, timestamp'
        for field in fields:
          sql = sql + ', AVG(' + field + ') as ' + field
        sql = sql + ' FROM sensor_data WHERE timestamp >= ? and timestamp <= ? AND timestamp % ' + str(modulo) + ' = 0'

        if len(parameters) == 2:
          sql = sql + ' and type = ?'
          filters = (stoptime,starttime,parameters[1],)

        sql = sql + ' GROUP BY type, timestamp'

      elif len(parameters) == 2 and parameters[0] in ['temperature','humidity']:
        sql = sql + ' and type = ? and id = ?'
        filters = (stoptime,starttime,parameters[0],parameters[1],)
      elif len(parameters) == 1 and parameters[0] in ['temperature','humidity']:
        sql = sql + ' and type = ?'
        filters = (stoptime,starttime,parameters[0],)

      elif len(parameters) == 1:
        sql = sql + ' and id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'switches':
      fields = { 'power_wattage' : [], 'water_flow' : [] , 'state' : []}
      sql = 'SELECT id, "switches" as type, timestamp, ' + ', '.join(fields.keys()) + ' FROM switch_data WHERE timestamp >= ? and timestamp <= ? '
      if len(parameters) > 0 and parameters[0] == 'summary':
        fields = ['total_power', 'total_water', 'duration']
        filters = ('total',)
        # Temporary overrule.... :P
        sql = '''
          SELECT ''' + str(stoptime) + ''' as timestamp,
                  IFNULL(MAX(timestamp) - MIN(timestamp),0) as duration,
                  IFNULL(SUM(power_wattage),0) as total_power,
                  IFNULL(SUM(water_flow),0) as total_water
            FROM switch_data
            WHERE id = ? '''

      elif len(parameters) > 0 and parameters[0] is not None:
        sql = sql + ' and id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'doors':
      fields = { 'state' : []}
      sql = 'SELECT id, "door" as type, timestamp, ' + ', '.join(fields.keys()) + ' FROM door_data WHERE timestamp >= ? and timestamp <= ? '

      if len(parameters) > 0 and parameters[0] is not None:
        sql = sql + ' and id = ?'
        filters = (stoptime,starttime,parameters[0],)

    elif logtype == 'weather':
      fields = { 'wind_speed' : [], 'temperature' : [], 'pressure' : [] , 'wind_direction' : [], 'rain' : [],
                 'weather' : [], 'icon' : []}
      sql = 'SELECT "city" as id, "weather" as type, timestamp, ' + ', '.join(fields.keys()) + ' FROM weather_data WHERE timestamp >= ? and timestamp <= ? AND timestamp % ' + str(modulo) + ' = 0'

    elif logtype == 'system':
      fields = ['load_load1', 'load_load5','load_load15','uptime', 'temperature','cores', 'memory_total', 'memory_used' , 'memory_free']

      if len(parameters) > 0 and parameters[0] == 'load':
        fields = ['load_load1', 'load_load5','load_load15']
      elif len(parameters) > 0 and parameters[0] == 'cores':
        fields = ['cores']
      elif len(parameters) > 0 and parameters[0] == 'uptime':
        fields = ['uptime']
      elif len(parameters) > 0 and parameters[0] == 'temperature':
        fields = ['temperature']
      elif len(parameters) > 0 and parameters[0] == 'memory':
        fields = ['memory_total', 'memory_used' , 'memory_free']

      sql = 'SELECT "system" as type, timestamp, ' + ', '.join(fields) + ' FROM system_data WHERE timestamp >= ? and timestamp <= ? AND timestamp % ' + str(modulo) + ' = 0'

    sql = sql + ' ORDER BY timestamp ASC'

    rows = []
    if not self.__recovery:
      try:
        with self.db:
          cur = self.db.cursor()
          cur.execute(sql, filters)
          rows = cur.fetchall()
      except sqlite3.DatabaseError as ex:
        logger.error('TerrariumPI Collecter exception! %s', (ex,))
        if 'database disk image is malformed' == str(ex):
          self.__recover()

    for row in rows:
      if logtype == 'switches' and len(row) == len(fields)+1:
        for field in fields:
          history[field] = row[field]

        return history

      if row['type'] not in history:
        history[row['type']] = {}

      if logtype == 'system':
        for field in fields:
          system_parts = field.split('_')
          if system_parts[0] not in history[row['type']]:
            history[row['type']][system_parts[0]] = {} if len(system_parts) == 2 else []

          if len(system_parts) == 2:
            if system_parts[1] not in history[row['type']][system_parts[0]]:
              history[row['type']][system_parts[0]][system_parts[1]] = []

            history[row['type']][system_parts[0]][system_parts[1]].append([row['timestamp'] * 1000,row[field]])
          else:
            history[row['type']][system_parts[0]].append([row['timestamp'] * 1000,row[field]])

      else:
        if row['id'] not in history[row['type']]:
          history[row['type']][row['id']] = copy.deepcopy(fields)

        for field in fields:
          history[row['type']][row['id']][field].append([row['timestamp'] * 1000,row[field]])

    return history
