# -*- coding: utf-8 -*-

from pylibftdi import Driver, BitBangDevice, SerialDevice, Device
from hashlib import md5
from datetime import datetime, timedelta
from time import sleep
import thread

import logging
terrarium_log = logging.getLogger('root')

class terrariumSwitch:
  locked = False
  addresses = {
            "1":"2",
            "2":"8",
            "3":"20",
            "4":"80",
            "all":"FF"
            }

  def __init__(self,nr,device,type,configObj):
    self.__nr = nr
    self.__device = device
    self.__device_type = type
    self.__config = configObj

    self.__id = md5(b'' + device + str(self.getNr())).hexdigest()

    switchConfig          = self.__config.getSwitchSettings(self.getID())
    self.__name           = str(switchConfig['name'] if 'name' in switchConfig and switchConfig['name'] else '{unknown}')
    self.__loggingActive  = bool(switchConfig['logging'] if 'logging' in switchConfig and switchConfig['logging'] else True)
    self.__cacheTimeOut   = timedelta(seconds=float(switchConfig['timeout'] if 'timeout' in switchConfig and switchConfig['timeout'] else 24 * 60 * 60))
    self.__wattage        = float(switchConfig['wattage'] if 'wattage' in switchConfig and switchConfig['wattage'] else 0.0)
    self.__waterflow      = float(switchConfig['waterflow'] if 'waterflow' in switchConfig and switchConfig['waterflow'] else 0.0)

    self.__state          = -1
    self.__lastUpdate     = datetime.fromtimestamp(0)

    self.__running_time   = 0.0
    self.__r_time_update  = datetime.now()
    self.__r_lock         = False

    self.__lastUsageChange     = datetime.now()
    self.__usageUpdateTimeout = 300

    # Serial device does not have an status indicator
    # Force to 'out' state
    if 'Serial' == self.__device_type:
      print 'Force to be switched off'
      self.off()

    self.update()
    thread.start_new_thread(self.__usage_updater, ())

  def __testBit(self,int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

  def __get_relay_state(self, data):
    if 1 == self.__nr:
        return self.__testBit(data, 1)
    if 2 == self.__nr:
        return self.__testBit(data, 3)
    if 3 == self.__nr:
        return self.__testBit(data, 5)
    if 4 == self.__nr:
        return self.__testBit(data, 7)

  def __setState(self, state):
    action = False
    newstate = 0
    if 'on' == state:
      action = self.getState() == 0
    else:
      action = self.getState() == 1

    if action:
      if self.getDeviceLock():
        try:
          if 'BitBang' == self.__device_type:
            with BitBangDevice(self.__device) as device:
              device.baudrate = 9600
              if 'on' == state:
                device.port |= int(terrariumSwitch.addresses[str(self.__nr)], 16)
              else:
                device.port &= ~int(terrariumSwitch.addresses[str(self.__nr)], 16)
              device.close()
          elif 'Serial' == self.__device_type:
            with SerialDevice(self.__device) as device:
              device.baudrate = 9600
              cmd = chr(0xff) + chr(0x0 + self.__nr) + chr(0x0 + (1 if 'on' == state else 0))
              device.write(cmd)
              device.close()

          self.__lastUpdate = datetime.now()
          self.__power_usage_stats()
          self.__state = 1 if 'on' == state else 0
          terrarium_log.info('Switched switch %s(%s) from %s',self.getName(),self.getID(),('off to on' if 'on' == state else 'on to off')) 
          newstate = 1
        except Exception, err:
#          self.__log.logLine(self.__log.ERROR,'Error switching ' + ('on' if 'on' == state else 'off') + ' switch: ' + str(self.getName()) + ' (' + str(self.getID()) + ')!: ' + str(err))
          newstate = -1
        finally:
          self.releaseDeviceLock()
      else:
        terrarium_log.error('Error getting lock for switch %s(%s). Device is busy with another switch', self.getName(),self.getID())
    else:
      terrarium_log.warn('No action made. State of switch %s(%s) is already in the requested state: %s', self.getName(),self.getID(),('on' if self.getState() else 'off'))

    return newstate

  def __power_usage_stats(self):
    now = datetime.now()
    self.__running_time += (now - self.__r_time_update).total_seconds() if self.getState() == 1 else 0.0
    self.__r_time_update = now

  def __usage_updater(self):
    while True:
      terrarium_log.debug('Update wattage usage for switch %s ...', self.getName())
      self.__power_usage_stats()

      now = datetime.now()
      waittime = self.__usageUpdateTimeout - (int(now.strftime('%s')) % self.__usageUpdateTimeout)
      sleep(int(waittime))

  def __setLogging(self,on):
    self.__loggingActive = bool(on)

  def __saveSwitchConfig(self):
    self.__config.saveSwitchSettings(self.getID(),self.getName(), int(self.getCacheTimeOut().total_seconds()), self.isLoggingEnabled(),self.getWattage(),self.getWaterflow())

  @staticmethod
  def scan():
    switches = []
    for device in Driver().list_devices():
      vendor, product, id = map(lambda x: x.decode('latin1'), device)
      type =  'Serial' if product.endswith('UART') else 'BitBang'
      for nr in range(1,5):
        switches.append({ 'nr' : nr,
                          'type' : type,
                          'device' : id})

    return switches

  def getDeviceLock(self,timeout = 10):
    timer = 0;
    while timer < timeout:
      if False == terrariumSwitch.locked:
        terrariumSwitch.locked = self.getID()
 #       self.__log.logLine(self.__log.DEBUG,'Device(' + str(self.__device) + ') lock for switch ' + str(self.getName()) + '(' + str(self.getID()) +') acquired.')
        return True
      else:
        timer += 1
 #       self.__log.logLine(self.__log.DEBUG,'Waiting for device(' + str(self.__device) + ') lock for switch ' + str(self.getName()) + '(' + str(self.getID()) +'). Current lock by device id ' + str(terrariumSwitch.locked) + ', ' + str(timeout-timer) + ' second(s) left.')
        sleep(1)

 #   self.__log.logLine(self.__log.ERROR,'Error getting lock on device(' + str(self.__device) + ') for switch ' + str(self.getName()) + '(' + str(self.getID()) +') after ' + str(timeout) + ' seconds.')
    return False

  def releaseDeviceLock(self):
    terrariumSwitch.locked = False
 #   self.__log.logLine(self.__log.DEBUG,'Device(' + str(self.__device) + ') released lock for switch ' + str(self.getName()) + '(' + str(self.getID()) +').')

  def getID(self):
    return self.__id

  def getNr(self):
    return self.__nr

  def getLastUpdateTimeStamp(self):
    return self.__lastUpdate

  def getCacheTimeOut(self):
    return self.__cacheTimeOut

  def setName(self,name):
    self.__name = str(name)
    self.__saveSwitchConfig()

  def getName(self):
    return self.__name

  def update(self):
    now = datetime.now()
    if now - self.__lastUpdate >= self.__cacheTimeOut:
      if self.getDeviceLock():
        try:
          old_state = self.getState()
          if 'BitBang' == self.__device_type:
            with BitBangDevice(self.__device) as device:
              device.baudrate = 9600
              self.__state = self.__get_relay_state( device.port )
              device.close()
          elif 'Serial' == self.__device_type:
            self.__state = self.__state

          if old_state != self.getState():
            terrarium.debug('Changed status of switch %s(%s) from %s to %s',self.getName(), self.getID(), ('on' if old_state else 'off'),('on' if self.getState() else 'off'))

          self.__lastUpdate = now

        except Exception, err:
          terrarium_log.error('Error updating switch %s(%s). Got error: %s',self.getName(),self.getID(),err)
        finally:
          self.releaseDeviceLock()
      else:
        terrarium_log.warn('Switch lock error. Could not update to new state!')

  def getState(self):
    if 1 == self.__state:
      return 1
    else:
      return 0

  def on(self):
    self.__setState('on')
    return self.getState()

  def off(self):
    self.__setState('off')
    return self.getState()

  def toggle(self):
    if 1 == self.__state:
      return self.off()
    else:
      return self.on()

  def getPowerUsage(self):
    self.__power_usage_stats()
    usage = (float(self.__running_time) / 3600.0) * float(self.getWattage())
    return usage

  def getCurrentWattage(self):
    return (0 if self.getState() == 0 else self.getWattage())

  def getWattage(self):
    if self.__wattage >= 0:
      return self.__wattage
    else:
      return False

  def setWattage(self,wattage):
    if 0 <= int(wattage) <= 500:
      self.__wattage = int(wattage)
      self.__saveSwitchConfig()
      return self.getWattage()
    else:
      return False

  def getWaterUsage(self):
    self.__power_usage_stats()
    usage = (float(self.__running_time) / 60.0) * self.getWaterflow()
    return usage

  def getCurrentWaterflow(self):
    return (0 if self.getState() == 0 else self.getWaterflow())

  def getWaterflow(self):
    if self.__waterflow >= 0.0:
      return self.__waterflow
    else:
      return False

  def setWaterflow(self,waterflow):
    waterflow = float(waterflow)
    if 0.0 <= waterflow <= 500.0:
      self.__waterflow = waterflow
      self.__saveSwitchConfig()
      return self.getWaterflow()
    else:
      return False

  def enableLogging(self):
    self.__setLogging(True)

  def disableLogging(self):
    self.__setLogging(False)

  def isLoggingEnabled(self):
    return True == self.__loggingActive

  def getSettings(self,format = 'json'):
    if 'json' == format:
      data = {}
      data['id'] = self.getID()
      data['nr'] = self.getNr()
      data['name'] = self.getName()
      data['wattage'] = self.getWattage()
      data['waterflow'] = self.getWaterflow()
      data['logging'] = self.isLoggingEnabled()
      data['timeout'] = self.getCacheTimeOut().total_seconds()
      return data
    else:
      return self
