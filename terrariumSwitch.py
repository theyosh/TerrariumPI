# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import RPi.GPIO as GPIO
import pigpio
import math
import os
import sys
import subprocess
import re
import pywemo
import datetime
import brightpi
import pca9685_driver

try:
  import thread as _thread
except ImportError as ex:
  import _thread

# Dirty hack to include someone his code... to lazy to make it myself :)
# https://github.com/perryflynn/energenie-connect0r
sys.path.insert(0, './energenie-connect0r')
import energenieconnector

sys.path.insert(0, './relay8-rpi/python')
from relay8 import set as relay8SetV1
from relay8 import get as relay8GetV1

from lib8relay import set as relay8SetV3
from lib8relay import get as relay8GetV3

from hashlib import md5
from pylibftdi import Driver, BitBangDevice, SerialDevice, Device
from gpiozero import Energenie
from time import time
from gevent import sleep

try:
  from meross_iot.api import MerossHttpClient, UnauthorizedException
except ImportError as ex:
  # Python 2 does not support Meross XXX Power Switches
  pass

from terrariumUtils import terrariumUtils, terrariumTimer, terrariumCache

class terrariumPowerSwitchSource(object):
  TYPE = None

  def __init__(self, switchid, address, name = '', prev_state = None, callback = None):
    logger.info('Initialising \'{}\' power switch object'.format(self.get_type()))
    self.power_wattage = 0.0
    self.water_flow = 0.0
    self.manual_mode = False
    self.hardware_replacement = '2019-01-01'

    self.switchid = switchid
    self.set_name(name)
    self.set_address(address)

    self.callback = callback
    self.timer = terrariumTimer('00:00','00:00',0,0,False)

    self.load_hardware()

    self.state = None
    ignore_scanning = [terrariumPowerSwitchWeMo.TYPE, terrariumPowerSwitchMSS425E.TYPE]
    if sys.version_info >= (3, 7):
      ignore_scanning.append('tplinkkasa')

    if self.get_type() not in ignore_scanning:
      # Do not toggle off switches during scanning.....
      prev_state = prev_state if prev_state is not None else terrariumPowerSwitch.OFF
      self.set_state(prev_state,True)

    logger.info('Loaded power switch \'{}\' with values: power {}W and waterflow {}L/s'.format(self.get_name(),self.get_power_wattage(),self.get_water_flow()))

  def get_type(self):
    return self.TYPE

  def get_id(self):
    if self.switchid in [None,'None','']:
      self.switchid = md5(b'' + self.get_type() + self.get_address()).hexdigest()

    return self.switchid

  def set_name(self,name):
    self.name = name

  def get_name(self):
    return self.name

  def set_address(self,value):
    self.address = value

  def get_address(self):
    return self.address

  def set_power_wattage(self,value):
    if terrariumUtils.is_float(value):
      self.power_wattage = float(value)

  def get_power_wattage(self):
    return self.power_wattage

  def set_water_flow(self,value):
    if terrariumUtils.is_float(value):
      self.water_flow = float(value)

  def get_water_flow(self):
    return self.water_flow

  def on(self):
    return self.set_state(terrariumPowerSwitch.ON)

  def off(self):
    return self.set_state(terrariumPowerSwitch.OFF)

  def is_on(self):
    return self.get_state() == terrariumPowerSwitch.ON

  def is_off(self):
    return not self.is_on()

  def go_up(self):
    self.on()

  def go_down(self):
    self.off()

  def is_dimmer(self):
    return False

  def is_pwm_dimmer(self):
    return False

  def is_at_max_power(self):
    return self.is_on()

  def is_at_min_power(self):
    return self.is_off()

  def get_current_power_wattage(self):
    return (0.0 if self.is_off() else self.get_power_wattage())

  def get_current_water_flow(self):
    return (0.0 if self.is_off() else self.get_water_flow())

  def toggle(self):
    if self.is_on():
      self.off()
    else:
      self.on()

  def load_hardware(self):
    pass

  def set_hardware_state(self, value, force = False):
    pass

  def get_hardware_state(self):
    return None

  def set_last_hardware_replacement(self,replacement_date = None):
    if replacement_date is None:
      replacement_date = datetime.date.today().strftime('%Y-%m-%d')

    self.hardware_replacement = replacement_date

  def get_last_hardware_replacement(self):
    return self.hardware_replacement

  def set_state(self, state, force = False):
    changed = False
    logger.debug('Changing power switch \'{}\' of type \'{}\' at address \'{}\' from state \'{}\' to state \'{}\' (Forced:{})'.format(self.get_name(),
                                                                                                                              self.get_type(),
                                                                                                                              self.get_address(),
                                                                                                                              self.get_state(),
                                                                                                                              state,force))

    if self.get_state() is not state or terrariumUtils.is_true(force):
      old_state = self.get_state()

      try:
        self.set_hardware_state(state,force)
        self.state = state
        logger.info('Changed power switch \'{}\' of type \'{}\' at address \'{}\' from state \'{}\' to state \'{}\' (Forced:{})'.format(self.get_name(),
                                                                                                                                self.get_type(),
                                                                                                                                self.get_address(),
                                                                                                                                old_state,
                                                                                                                                state,
                                                                                                                                force))


      except Exception as ex:
        print(ex)
        logger.error('Failed changing power switch \'{}\' of type \'{}\' at address \'{}\' from state \'{}\' to state \'{}\' (Forced:{})'.format(self.get_name(),
                                                                                                                                         self.get_type(),
                                                                                                                                         self.get_address(),
                                                                                                                                         self.get_state(),
                                                                                                                                         state,force))

      if (old_state is not None) or (old_state is None and state == 0):
        # This is due to a bug that will graph 0 watt usage in the graph after rebooting.
        # Fix is to add power and water usage in constructor
        changed = old_state != self.get_state()

    if changed and self.callback is not None:
      self.callback(self.get_data())

    return changed

  def get_state(self):
    return self.state

  def stop(self):
    logger.debug('Stopping power switch {} at location {}'.format(self.get_name(), self.get_address()))

  def in_manual_mode(self):
    return terrariumUtils.is_true(self.manual_mode)

  def set_manual_mode(self,mode):
    self.manual_mode = terrariumUtils.is_true(mode)

  def update(self):
    starttime = time()
    old_state = self.get_state()

    self.timer_update()
    data = self.get_hardware_state()
    if data is not None:
      self.set_state(data)

    if self.get_state() != old_state:
      logger.info('Power switch changed from {} state to new {} state'.format(old_state,self.get_state()))

    logger.info('Updated {} power switch \'{}\' status in {:.5f} seconds'.format(self.get_type(),self.get_name(),time()-starttime))

  def timer_update(self):
    if not self.in_manual_mode() and self.timer.is_enabled():
      if self.timer.is_time():
        self.on()
      else:
        self.off()

  def set_timer(self,start,stop,on_duration,off_duration,enabled):
    self.timer = terrariumTimer(start,stop,on_duration,off_duration,enabled)
    self.timer_update()

  def get_data(self):
    data = {'id' : self.get_id(),
            'hardwaretype' : self.get_type(),
            'address' : self.get_address(),
            'name' : self.get_name(),
            'power_wattage' : self.get_power_wattage(),
            'current_power_wattage' : self.get_current_power_wattage(),
            'water_flow' : self.get_water_flow(),
            'current_water_flow' : self.get_current_water_flow(),
            'state' : self.get_state(),
            'manual_mode' : self.in_manual_mode(),
            'last_replacement_date' : self.get_last_hardware_replacement()}

    data.update(self.timer.get_data())

    return data

class terrariumPowerSwitchFTDI(terrariumPowerSwitchSource):
  TYPE = 'ftdi'

  BITBANG_ADDRESSES = {
    "1":"2",
    "2":"8",
    "3":"20",
    "4":"80",
    "5":"1",
    "6":"4",
    "7":"10",
    "8":"40",
    "all":"FF"
  }

  def __get_address(self):
    data = self.get_address().strip().split(',')
    if len(data) == 1:
      data.append(1)
    elif '' == data[1]:
      data[1] = 1

    data[0] = int(data[0])
    data[1] = int(data[1])

    return data

  def load_hardware(self):
    address = self.__get_address()

    self.__device_type = None
    counter = 1
    for device in Driver().list_devices():
      if counter != address[1]:
        counter += 1
        continue

      vendor, product, self.__device = [x for x in device]
      self.__device_type = 'Serial' if product.endswith('UART') else 'BitBang'
      logger.debug('Found switch board {}, {}, {}, of type {}'.format(vendor,product,self.__device,self.__device_type))
      break # For now, we only support 1 switch board!

  def set_hardware_state(self, state, force = False):
    address = self.__get_address()

    if 'BitBang' == self.__device_type:
      with BitBangDevice(self.__device) as device:
        device.baudrate = 9600
        if state is terrariumPowerSwitch.ON:
          device.port |= int(terrariumPowerSwitchFTDI.BITBANG_ADDRESSES[str(address[0])], 16)
        else:
          device.port &= ~int(terrariumPowerSwitchFTDI.BITBANG_ADDRESSES[str(address[0])], 16)

    elif 'Serial' == self.__device_type:
      with SerialDevice(self.__device) as device:
        device.baudrate = 9600
        cmd = chr(0xff) + chr(0x0 + int(address[0])) + chr(0x0 + (1 if state is terrariumPowerSwitch.ON else 0))
        device.write(cmd)

  def get_hardware_state(self):

    def get_relay_state(data, relay ):

      def testBit(int_type, offset):
        mask = 1 << offset
        return(int_type & mask)

      if relay == "1":
        return testBit(data, 1)
      if relay == "2":
        return testBit(data, 3)
      if relay == "3":
        return testBit(data, 5)
      if relay == "4":
        return testBit(data, 7)
      if relay == "5":
        return testBit(data, 2)
      if relay == "6":
        return testBit(data, 4)
      if relay == "7":
        return testBit(data, 6)
      if relay == "8":
        return testBit(data, 8)

    data = None
    address = self.__get_address()

    if 'BitBang' == self.__device_type:
      with BitBangDevice(self.__device) as device:
        device.baudrate = 9600
        data = get_relay_state( device.port, str(address[0]) )

    elif 'Serial' == self.__device_type:
      return None

    return terrariumPowerSwitch.OFF if data is None or data == 0 else terrariumPowerSwitch.ON

class terrariumPowerSwitchGPIO(terrariumPowerSwitchSource):
  TYPE = 'gpio'

  def load_hardware(self):
    GPIO.setup(terrariumUtils.to_BCM_port_number(self.get_address()), GPIO.OUT)

  def stop(self):
    GPIO.cleanup(terrariumUtils.to_BCM_port_number(self.get_address()))
    super(terrariumPowerSwitchGPIO,self).stop()

  def set_hardware_state(self, state, force = False):
    if self.get_type() == terrariumPowerSwitchGPIO.TYPE:
      GPIO.output(terrariumUtils.to_BCM_port_number(self.get_address()), ( GPIO.HIGH if state is terrariumPowerSwitch.ON else GPIO.LOW ))

    elif self.get_type() == terrariumPowerSwitchGPIOInverse.TYPE:
      GPIO.output(terrariumUtils.to_BCM_port_number(self.get_address()), ( GPIO.LOW if state is terrariumPowerSwitch.ON else GPIO.HIGH ))

class terrariumPowerSwitchGPIOInverse(terrariumPowerSwitchGPIO):
  TYPE = 'gpio-inverse'

class terrariumPowerSwitchRelay8Stack(terrariumPowerSwitchSource):
  TYPE = '8relay-stack_v1'

  def __get_addres(self):
    address = self.address.split(',')
    if 1 == len(address):
        address.append(address[0])
        address[0] = 0

    return address

  def set_hardware_state(self, state, force = False):
    address = self.__get_addres()
    if self.get_type() == terrariumPowerSwitchRelay8Stack.TYPE:
      relay8SetV1(address[0], address[1], 1 if state is terrariumPowerSwitch.ON else 0)
    elif self.get_type() == terrariumPowerSwitchRelay8StackV3.TYPE:
      relay8SetV3(address[0], address[1], 1 if state is terrariumPowerSwitch.ON else 0)

  def get_hardware_state(self):
    address = self.__get_addres()
    if self.get_type() == terrariumPowerSwitchRelay8Stack.TYPE:
      relay8GetV1(address[0], address[1])
    elif self.get_type() == terrariumPowerSwitchRelay8StackV3.TYPE:
      relay8GetV3(address[0], address[1])

class terrariumPowerSwitchRelay8StackV3(terrariumPowerSwitchRelay8Stack):
  TYPE = '8relay-stack_v3'

class terrariumPowerSwitchWeMo(terrariumPowerSwitchSource):
  TYPE = 'wemo'
  URL = 'http://{}:{}/setup.xml'

  def set_hardware_state(self, state, force = False):
    port = pywemo.ouimeaux_device.probe_wemo(self.get_address())
    device = pywemo.discovery.device_from_description(terrariumPowerSwitchWeMo.URL.format(self.get_address(), port), None)
    if state is terrariumPowerSwitch.ON:
      device.on()
    else:
      device.off()

  def get_hardware_state(self):
    data = None
    try:
      port = pywemo.ouimeaux_device.probe_wemo(self.get_address())
      if port is not None:
        device = pywemo.discovery.device_from_description(terrariumPowerSwitchWeMo.URL.format(self.get_address(), port), None)
        data = device.get_state()

    except Exception as err:
      # Ignore for now
      print(err)

    return terrariumPowerSwitch.ON if terrariumUtils.is_true(data) else terrariumPowerSwitch.OFF

  @staticmethod
  def scan_power_switches(callback=None, **kwargs):
    for device in pywemo.discover_devices():
      yield terrariumPowerSwitch(md5((terrariumPowerSwitchWeMo.TYPE + device.serialnumber).encode()).hexdigest(),
                                 terrariumPowerSwitchWeMo.TYPE,
                                 device.host,
                                 device.name,
                                 None,
                                 callback)

class terrariumPowerSwitchEnergenieUSB(terrariumPowerSwitchSource):
  TYPE = 'eg-pm-usb'
  CMD = '/usr/local/bin/sispmctl' if os.path.exists('/usr/local/bin/sispmctl') else '/usr/bin/sispmctl'

  def load_hardware(self):
    address = self.get_address().strip().split(',')
    self.__socket_nr = int(address[0].strip())
    # Default we use the device counter option
    self.__device_type = '-d'
    # Check if custom device number or serial is entered
    self.__device = 0 if len(address) == 1 else address[1].strip()
    # If the device is not a number, it should be a string with an identifier in it
    if not terrariumUtils.is_float(self.__device):
      # Use the device serial identification
      self.__device_type = '-D'
    else:
      # If the user has enterd a number, it is probaly 1 to high. A human will enter device number 1 and not zero....
      self.__device = int(self.__device) - 1

  def set_hardware_state(self, state, force = False):
    cmd = [self.CMD, self.__device_type, str(self.__device),('-o' if state is terrariumPowerSwitch.ON else '-f'),str(self.__socket_nr)]
    subprocess.check_output(cmd)

  def get_hardware_state(self):
    status_regex = r'Status of outlet ' + str(self.__socket_nr) + ':\s*(?P<status>[0,1])'

    cmd = [self.CMD, self.__device_type, str(self.__device),'-n','-g',str(self.__socket_nr)]
    data = subprocess.check_output(cmd).strip().decode('utf-8').split('\n')
    for line in data:
      line = re.match(status_regex,line)
      if line is not None:
        line = line.groupdict()
        return terrariumPowerSwitch.ON if int(line['status']) == 1 else terrariumPowerSwitch.OFF

    # Could not read out, so return nothing...
    return None

  @staticmethod
  def scan_power_switches(callback=None, **kwargs):
    switch_type = terrariumPowerSwitchEnergenieUSB.TYPE
    scan_regex = r'^(?P<option>[^:]+):\s*(?P<value>.*)$'

    cmd = [terrariumPowerSwitchEnergenieUSB.CMD,'-s']

    try:
      data = subprocess.check_output(cmd).strip().decode('utf-8').split('\n')
    except subprocess.CalledProcessError as ex:
      return False

    amount_sockets = None
    serial = None
    device_nr = 0

    for line in data:
      line = re.match(scan_regex,line)
      if line is not None:
        line = line.groupdict()
        if 'device type' == line['option']:
          # By default we have 4 sockets.... not sure..
          amount_sockets = 4
          amount_regex = r'(?P<amount>\d+)'
          value = re.match(scan_regex,line['value'])
          if value is not None:
            value = value.groupdict()
            amount_sockets = int(value['amount'])

        elif 'serial number' == line['option'] and amount_sockets is not None:
          serial = line['value']

          # New switches can be added....
          device_nr += 1
          for x in range(1,amount_sockets+1):
            yield terrariumPowerSwitch(md5((switch_type + str(x) + ',' + str(serial)).encode()).hexdigest(),
                                 switch_type,
                                 '{},{}'.format(x,serial),
                                 '{} device nr: {}, Socket: {}'.format(switch_type,device_nr,x),
                                 None,
                                 callback)

          amount_sockets = None



class terrariumPowerSwitchEnergenieLAN(terrariumPowerSwitchSource):
  TYPE = 'eg-pm-lan'
  VALID_SOURCE = '^http:\/\/((?P<passwd>[^@]+)@)?(?P<host>[^#\/]+)(\/)?#(?P<switch>[1-4])$'

 # def set_address(self,value):
 #   super(terrariumPowerSwitchEnergenieLAN, self).set_address(value)
 #   self.load_hardware()

  def load_hardware(self):
    self.__device = None
    # Input format should be either:
    # - http://[HOST]#[POWER_SWITCH_NR]
    # - http://[HOST]/#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]

    data = re.match(terrariumPowerSwitchEnergenieLAN.VALID_SOURCE,self.get_address())
    if data:
      data = data.groupdict()
      if 'passwd' not in data:
        data['passwd'] = ''

      try:
        # https://github.com/perryflynn/energenie-connect0r
        self.__device = energenieconnector.EnergenieConnector('http://' + data['host'],data['passwd'])
        status = self.__device.getstatus()

        if status['login'] == 1:
          if self.__device.login():
            logger.info('Connection to remote Energenie LAN \'%s\' is successfull at location %s' % (self.get_name(), self.get_address()))
            status = self.__device.getstatus()
            self.__device.logout()

        if status['login'] != 0:
          logger.error('Could not login to the Energenie LAN device %s at location %s. Error status %s(%s)' % (self.get_name(),self.get_address(),status['logintxt'],status['login']))
          self.__device = None

      except Exception as ex:
        logger.exception('Could not login to the Energenie LAN device %s at location %s. Error status %s' % (self.get_name(),self.get_address(),ex))

  def set_hardware_state(self, state, force = False):
    changed = True

    if self.__device is None:
      logger.error('Energenie LAN device is not connected. Cannot trigger power switch')
      changed = False
    else:
      data = re.match(terrariumPowerSwitchEnergenieLAN.VALID_SOURCE,self.get_address())
      if data:
        power_socket = int(data.group('switch')) % 4
        if power_socket == 0:
          power_socket = 4

      #try:
      webstatus = self.__device.getstatus()
      if webstatus['login'] == 1:
        logger.debug('Logged in at remote Energenie LAN power switch  %s' % (self.get_address(),))
        if self.__device.login():
          webstatus = self.__device.getstatus()

      if webstatus['login'] == 0:
        self.__device.changesocket(power_socket, ( 1 if state is terrariumPowerSwitch.ON else 0 ))
        self.__device.logout()
      else:

        # raise exception here...
        logger.error('Could not login to the Energenie LAN device %s at location %s. Error status %s(%s)' % (self.get_name(),self.get_address(),webstatus['logintxt'],webstatus['login']))

    return changed

  def stop(self):
    self.__device.logout()
    super(terrariumPowerSwitchEnergenieLAN,self).stop()

class terrariumPowerSwitchEnergenieRF(terrariumPowerSwitchSource):
  TYPE = 'eg-pm-rf'

  def load_hardware(self):
    self.__device = Energenie(int(self.get_address()))

  def set_hardware_state(self, state, force = False):
    if state:
      self.__device.on()
    else:
      self.__device.off()

  def stop(self):
    self.__device.close()
    super(terrariumPowerSwitchEnergenieRF,self).stop()

class terrariumPowerSwitchSonoff(terrariumPowerSwitchSource):
  TYPE = 'sonoff'
  VALID_SOURCE = '^http:\/\/((?P<user>[^:]+):(?P<passwd>[^@]+)@)?(?P<host>[^#\/]+)(\/)?(#(?P<nr>\d+))?$'

  def load_hardware(self):
    self.__firmware = None
    if not hasattr(self, '__retries'):
      self.__retries = 0

    # Input format should be either:
    # - http://[HOST]#[POWER_SWITCH_NR]
    # - http://[HOST]/#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]#[POWER_SWITCH_NR]
    # - http://[PASSWORD]@[HOST]/#[POWER_SWITCH_NR]

    data = re.match(self.VALID_SOURCE,self.get_address())
    if data:
      data = data.groupdict()
      if 'nr' not in data or data['nr'] == '' or data['nr'] is None:
        data['nr'] = 1

      try:
        # Try Tasmota

        # http://sonoff/cm?cmnd=Power%20TOGGLE
        # http://sonoff/cm?cmnd=Power%20On
        # http://sonoff/cm?cmnd=Power%20off
        # http://sonoff/cm?user=admin&password=joker&cmnd=Power%20Toggle

        url = 'http://{}/cm?'.format(data['host'])
        if 'user' in data and 'password' in data:
          url += 'user={}&password={}&'.format(data['user'],data['password'])

        url += 'cmnd=Power{}'.format(data['nr'])
      
        state = terrariumUtils.get_remote_data(url)
        if state is None:
          raise Exception('No data, jump to next test')

        self.__firmware = 'tasmota'
        self.__retries = 0
        self.url = url

      except Exception as ex:
        print('Tasmota exceptions')
        print(ex)


      if self.__firmware is None:
        try:
          # Try ESP Easy

          # url_switch_on  = 'http://192.168.1.42/control?cmd=event,T1'
          # url_switch_off  = 'http://192.168.1.42/control?cmd=event,T0'

          #print('Test ESP Easy')

          url = 'http://{}/json'.format(data['host'])
          # No information about using username and password:
          # https://www.letscontrolit.com/wiki/index.php?title=ESPEasy_Command_Reference
          # https://www.letscontrolit.com/wiki/index.php?title=ESP_Easy_web_interface#JSON_page_.28hidden_prior_to_version_2.0.2B.29

          #print(url)
          state = terrariumUtils.get_remote_data(url)
          #print('Result')
          #print(state)
          if state is None:
            raise Exception('No data, jump to next test')

          self.__firmware = 'espeasy'
          self.__retries = 0

        except Exception as ex:
          print('ESP Easy exceptions')
          print(ex)

      if self.__firmware is None:
        try:
          # Try ESPurna
          # https://github.com/xoseperez/espurna/wiki/RESTAPI

          # http://192.168.1.108/apis?apikey=C62ED7BE7593B658
          # http://192.168.1.108/api/relay/0?apikey=C62ED7BE7593B658&value=0 (off)
          # http://192.168.1.108/api/relay/0?apikey=C62ED7BE7593B658&value=1 (on)
          # http://192.168.1.108/api/relay/0?apikey=C62ED7BE7593B658&value=2 (toggle)


          #print('Test ESPurna')

          if 'password' not in data:
            # Just add dummy value...
            data['password'] = 'password'

          url = 'http://{}/apis?apikey={}'.format(data['host'],data['password'])

          #print(url)
          state = terrariumUtils.get_remote_data(url,json=True)
          #print('Result')
          #print(state)
          if state is None:
            raise Exception('No data, this was the last attempt...')

          self.__firmware = 'espurna'
          self.__retries = 0

        except Exception as ex:
          print('ESPurna exceptions')
          print(ex)

  def set_hardware_state(self, state, force = False):
    changed = True

    if self.__firmware is None:
      if self.__retries < 5:
        self.__retries += 1
        logger.warning('Sonoff device is not connected for trigger action. Reconnect attempt: {}'.format(self.__retries))
        self.load_hardware()
        return self.set_hardware_state(state,force)
      else:
        logger.error('Sonoff device is not connected. Cannot trigger power switch')
        return False

    data = re.match(self.VALID_SOURCE,self.get_address())
    if data:
      data = data.groupdict()
      url = None

      if 'tasmota' == self.__firmware:
        url = self.url + '%20{}'.format('1' if state else '0')

      elif 'espeasy' == self.__firmware:
        url = 'http://{}/control?cmd=event,T{}'.format(data['host'],('1' if state else '0'))

      elif 'espurna' == self.__firmware:
        url = 'http://{}/api/relay/0?apikey={}&value={}'.format(data['host'],data['password'],('1' if state else '0'))

      state = terrariumUtils.get_remote_data(url)
      if state is None:
        changed = False

    return changed

  def get_hardware_state(self):
    data = None

    if self.__firmware is None:
      if self.__retries < 5:
        self.__retries += 1
        logger.warning('Sonoff device is not connected while reading the state. Reconnect attempt: {}'.format(self.__retries))
        self.load_hardware()
        return self.get_hardware_state()
      else:
        logger.error('Sonoff device is not connected. Cannot read power switch state')
        return terrariumPowerSwitch.OFF

    data = re.match(self.VALID_SOURCE,self.get_address())
    if data:
      data = data.groupdict()
      url = None

      if 'tasmota' == self.__firmware:
        url = self.url

      elif 'espeasy' == self.__firmware:
        url = 'http://{}/json'.format(data['host'])

      elif 'espurna' == self.__firmware:
        if 'password' not in data:
          # Just add dummy value...
          data['password'] = 'password'

        url = 'http://{}/apis?apikey={}'.format(data['host'],data['password'])

      state = terrariumUtils.get_remote_data(url)
      if state is None:
        logger.warning('Error reading Sonoff \'{}\' power state. So returning last known state: {}'.format(self.get_name(),self.state))
        return self.state

      if 'tasmota' == self.__firmware:
        return terrariumPowerSwitch.ON if terrariumUtils.is_true(state['POWER']) else terrariumPowerSwitch.OFF
      elif 'espeasy' == self.__firmware:
        return terrariumPowerSwitch.ON if terrariumUtils.is_true(state['POWER']) else terrariumPowerSwitch.OFF
      elif 'espurna' == self.__firmware:
        return terrariumPowerSwitch.ON if terrariumUtils.is_true(state['POWER']) else terrariumPowerSwitch.OFF

    return terrariumPowerSwitch.OFF

class terrariumPowerSwitchDenkoviV2(terrariumPowerSwitchSource):
  TYPE = 'denkovi_v2'

  def __init__(self, switchid, address, name = '', prev_state = None, callback = None):
    self.__cache = terrariumCache()
    super(terrariumPowerSwitchDenkoviV2,self).__init__(switchid, address, name, prev_state, callback)

  def __get_cache_key(self):
    key = md5((self.get_type() + str(self.__device)).encode()).hexdigest()
    return key

  def _get_relay_count(self):
    return int(self.TYPE.split('_')[-1])

  def _get_board_type(self):
    return '{}{}'.format(self._get_relay_count(),self.__version)

  def load_hardware(self):
    serial_regex = r"^(?P<serial>[^ ]+)\W(\[[^\]]+\])\W\[id=\d\]$"
    self.__device = None
    self.__version = ''

    # We only support one board for now...
    cmd = ['/usr/bin/sudo','/usr/bin/java','-jar','DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar','list']
    logger.debug('Running load hardware command {}'.format(cmd))

    try:
      data = subprocess.check_output(cmd).strip().decode('utf-8')
      for line in data.split("\n"):
        match = re.match(r"^(?P<serial>[^ ]+)\W(?P<device>\[[^\]]+\])\W\[id=\d\]$",line,re.MULTILINE)
        if match:
          self.__device = str(match.group('serial'))
          self.__version = 'v2' if 'MCP2200' in match.group('device') else ''
          break

    except Exception as err:
      # Ignore for now
      logger.error('Error loading hardware for switch type {}, with error: {}'.format(self.get_type(),err))

  def get_hardware_state(self):
    #data = None
    #print('Get hardware state cache data')
    data = self.__cache.get_data(self.__get_cache_key())
    #print(data)
    #print('IS running: {}' .format(self.__cache.is_running(self.__get_cache_key())))

    if data is None and not self.__cache.is_running(self.__get_cache_key()):
      self.__cache.set_running(self.__get_cache_key())

      cmd = ['/usr/bin/sudo','/usr/bin/java','-jar','DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar',self.__device,self._get_board_type(),'all','status']
      logger.debug('Running get hardware state command {}'.format(cmd))
      #print('Running cmd: {}'.format(cmd))

      try:
        data = subprocess.check_output(cmd).strip().decode('utf-8')

        #print('Got data: *{}*'.format(data))
        self.__cache.set_data(self.__get_cache_key(),data)
      except Exception as err:
        # Ignore for now
        logger.error('Error getting hardware state for switch type {}, with error: {}'.format(self.get_type(),err))


      self.__cache.clear_running(self.__get_cache_key())

    if data is None:
      return terrariumPowerSwitch.OFF

    address = int(self.get_address()) % self._get_relay_count()
    if address == 0:
      address = self._get_relay_count()

    #print('Final state data at address{} : {}'.format(address,data[address-1:address]))

    return terrariumPowerSwitch.ON if terrariumUtils.is_true(data[address-1:address]) else terrariumPowerSwitch.OFF

  def set_hardware_state(self, state, force = False):
    address = int(self.get_address()) % self._get_relay_count()
    if address == 0:
      address = self._get_relay_count()

    cmd = ['/usr/bin/sudo','/usr/bin/java','-jar','DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar',self.__device,self._get_board_type(),str(address),str(1 if state is terrariumPowerSwitch.ON else 0)]
    logger.debug('Running set hardware state command {}'.format(cmd))
    #print('Running set hardware state cmd: {}'.format(cmd))

    try:
      subprocess.check_output(cmd)

      # After change, clear the cache so next run actual data is forced fetched
      #print('Clear caching')
      self.__cache.clear_data(self.__get_cache_key())
      #print('Clear caching DONE!')
      return True

    except Exception as err:
      # Ignore for now
      logger.error('Error setting hardware state for switch type {}, with error: {}'.format(self.get_type(),err))
      #print(err)

class terrariumPowerSwitchDenkoviV2_4(terrariumPowerSwitchDenkoviV2):
  TYPE = 'denkovi_v2_4'

class terrariumPowerSwitchDenkoviV2_8(terrariumPowerSwitchDenkoviV2):
  TYPE = 'denkovi_v2_8'

class terrariumPowerSwitchDenkoviV2_16(terrariumPowerSwitchDenkoviV2):
  TYPE = 'denkovi_v2_16'

class terrariumPowerSwitchScript(terrariumPowerSwitchSource):
  TYPE = 'script'

  def set_hardware_state(self, state, force = False):
    value = (100 if state else 0)

    try:
      logger.info('Running script: %s.' % (self.get_address()))
      data = subprocess.check_output('{} {}'.format(self.get_address(),value), shell=True)
      logger.info('Output was: %s.' % (data))
    except Exception as ex:
      logger.exception('Error parsing script data for script %s. Exception %s' % (self.get_address(), ex))

    return state

class terrariumPowerDimmerSource(terrariumPowerSwitchSource):
  TYPE = 'dimmer'

  # General Dimmer settings
  DIMMER_MIN_TIMEOUT = 0.1
  DIMMER_MIN_STEP    = 0.1

  def __init__(self, switchid, address, name = '', prev_state = None, callback = None):
    self.duration       = 0.0
    self.step           = 0.0
    self.on_duration    = 0.0
    self.off_duration   = 0.0
    self.on_percentage  = 100.0
    self.off_percentage = 0.0

    self._dimmer_state = 0.0
    self._dimmer_running = False
    super(terrariumPowerDimmerSource,self).__init__(switchid, address, name, prev_state, callback)

  def get_state(self):
    return self._dimmer_state

  def load_hardware(self):
    self.__device = None

  def is_dimmer(self):
    return True

  def is_pwm_dimmer(self):
    return True

  def get_current_power_wattage(self):
    return (float(self.get_state()) / 100) *  self.get_power_wattage()

  def get_current_water_flow(self):
    return (float(self.get_state()) / 100) *  self.get_water_flow()

  def is_at_max_power(self):
    return self.get_state() >= self.get_dimmer_on_percentage()

  def is_at_min_power(self):
    return self.get_state() <= self.get_dimmer_off_percentage()

  def is_on(self):
    return self.is_at_max_power()

  def __go_up_down(self,direction):
    if not self._dimmer_running:
      new_value = self.get_state() + (direction * self.get_dimmer_step())
      if new_value > self.get_dimmer_on_percentage():
        new_value = self.get_dimmer_on_percentage()

      if new_value < self.get_dimmer_off_percentage():
        new_value = self.get_dimmer_off_percentage()

      self.set_state(new_value)

  def go_up(self):
    self.__go_up_down(1)

  def go_down(self):
    self.__go_up_down(-1)

  def set_dimmer(self,duration,step,on_duration,off_duration,on_percentage,off_percentage):
    self.duration = float(duration)
    self.step = float(step)
    self.on_duration = float(on_duration)
    self.off_duration = float(off_duration)
    self.on_percentage = float(on_percentage)
    self.off_percentage = float(off_percentage)

  def get_dimmer_duration(self):
    return self.duration

  def get_dimmer_step(self):
    return self.step

  def get_dimmer_on_duration(self):
    return self.on_duration

  def get_dimmer_off_duration(self):
    return self.off_duration

  def get_dimmer_on_percentage(self):
    return self.on_percentage

  def get_dimmer_off_percentage(self):
    return self.off_percentage

  def set_hardware_state(self, value, force = False):
    if not self._dimmer_running:
      duration = self.get_dimmer_duration()
      # State 100 = full on which means 0 dim.
      # State is inverse of dim
      if value is terrariumPowerSwitch.ON:
        value = self.get_dimmer_on_percentage()
        duration = self.get_dimmer_on_duration()
      elif value is terrariumPowerSwitch.OFF or not (0.0 <= float(value) <= 100.0):
        value = self.get_dimmer_off_percentage()
        duration = self.get_dimmer_off_duration()

      if force:
        duration = 0

      _thread.start_new_thread(self._dim_switch, (value,duration))

    return True

  def _dim_switch(self,value,duration):
    if self._device is None:
      logger.error('Dimmer device {} is not loaded... cannot dimm'.format(self.get_name()))
      return

    # When the dimmer is working, ignore new state changes.
    prev_value = -1

    if not self._dimmer_running:
      self._dimmer_running = True

      self._dimmer_state = (0.0 if not terrariumUtils.is_float(self.get_state()) else float(self.get_state()))
      value    = (0.0 if not terrariumUtils.is_float(value) else float(value))
      duration = (0.0 if not terrariumUtils.is_float(duration) else float(duration))

      direction = (1.0 if self._dimmer_state <= value else -1.0)
      distance  = abs(self._dimmer_state - value)

      if int(duration) == 0 or int(distance) == 0:
        steps = 1.0
      else:
        steps = math.floor(min( (abs(duration) / terrariumPowerDimmerSource.DIMMER_MIN_TIMEOUT),
                                (distance / terrariumPowerDimmerSource.DIMMER_MIN_STEP)))
        distance /= steps
        duration /= steps

      logger.debug('Dimmer settings: Steps: %s, Distance per step: %s%%, Time per step: %s, Direction: %s',steps, distance, duration, direction)

      for counter in range(int(steps)):
        self._dimmer_state += (direction * distance)
        if self.get_type() == terrariumPowerDimmerPWM.TYPE:
          dim_value = terrariumPowerDimmerPWM.DIMMER_MAXDIM * ((100.0 - float(self._dimmer_state)) / 100.0)
          dim_freq = terrariumPowerDimmerPWM.DIMMER_FREQ
        elif self.get_type() == terrariumPowerDimmerDC.TYPE:
          dim_value = terrariumPowerDimmerDC.DIMMER_MAXDIM * (float(self._dimmer_state) / 100.0)
          dim_freq = terrariumPowerDimmerDC.DIMMER_FREQ

        elif self.get_type() == terrariumPowerDimmerBrightPi.TYPE:
          dim_value = int(50 * (float(self._dimmer_state) / 100.0))

        elif self.get_type() == terrariumPowerDimmerIRF520.TYPE:
          dim_value = self._dimmer_state
          dim_freq = terrariumPowerDimmerIRF520.DIMMER_FREQ

        skip_first = True
        for gpiopin in self.get_address().split(','):
          logger.debug('Dimmer animation: Step: %s, value %s%%, Dim value: %s, timeout %s',counter+1, self._dimmer_state, dim_value, duration)
          if self.get_type() in [terrariumPowerDimmerPWM.TYPE,terrariumPowerDimmerDC.TYPE, terrariumPowerDimmerPCA9685.TYPE, terrariumPowerDimmerIRF520.TYPE]:
            if terrariumUtils.to_BCM_port_number(gpiopin) is False:
              continue

            if self.get_type() == terrariumPowerDimmerPCA9685.TYPE:
              if skip_first:
                skip_first = False
                continue

              self._device.set_pwm(int(gpiopin), self._dimmer_state * (4095 / 100))

            elif self.get_type() == terrariumPowerDimmerIRF520.TYPE:
              self._device.hardware_PWM(terrariumUtils.to_BCM_port_number(gpiopin), dim_freq, int(dim_value) * 10000)

            else:
              self._device.hardware_PWM(terrariumUtils.to_BCM_port_number(gpiopin), dim_freq, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle

          elif self.get_type() == terrariumPowerDimmerBrightPi.TYPE:

            if dim_value != prev_value:
              leds = brightpi.LED_WHITE
              if self.get_address().split(',')[-1].lower() == 'ir':
                leds = brightpi.LED_IR

              self._device.set_led_dim(leds, dim_value)
              prev_value = dim_value

        if duration > 0.0:
          sleep(duration)

        # For impatient people... Put the dimmer at the current state value if it has changed during the animation (DISABLED FOR NOW)
        # dim_value = terrariumSwitch.PWM_DIMMER_MAXDIM * ((100.0 - self.get_state()) / 100.0)
        # self.__device.hardware_PWM(terrariumUtils.to_BCM_port_number(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle

      self._dimmer_state = value
      self._dimmer_running = False
      if self.callback is not None:
        self.callback(self.get_data())
      logger.info('Power switch \'{}\' at address \'{}\' is done at value {}% in {} seconds'.format(self.get_name(),
                                                                                                    self.get_address(),
                                                                                                    self.get_state(),
                                                                                                    duration*steps))
    #else:
    #  logger.warning('Dimmer %s is already working. Ignoring state change!. Will switch to latest state value when done', self.get_name())

  def get_data(self):
    data = super(terrariumPowerDimmerSource,self).get_data()

    data.update({
      'dimmer_duration'      : self.get_dimmer_duration(),
      'dimmer_step'          : self.get_dimmer_step(),
      'dimmer_on_duration'   : self.get_dimmer_on_duration(),
      'dimmer_on_percentage' : self.get_dimmer_on_percentage(),
      'dimmer_off_duration'  : self.get_dimmer_off_duration(),
      'dimmer_off_percentage': self.get_dimmer_off_percentage()
      })

    return data


class terrariumPowerDimmerPiGPIOSource(terrariumPowerDimmerSource):
  TYPE = 'pigpio-dimmer'

  def load_hardware(self):
    self._dimmer_running = False
    pigpio.exceptions = False
    self._device = pigpio.pi('localhost')
    if not self._device.connected:
      self._device = pigpio.pi()
      if not self._device.connected:
        logger.error('PiGPIOd process is not running')
        self._device = None

    if self._device is not None:
      pigpio.exceptions = True
      self._device.set_pull_up_down(terrariumUtils.to_BCM_port_number(self.get_address()), pigpio.PUD_OFF)


class terrariumPowerDimmerPWM(terrariumPowerDimmerPiGPIOSource):
  TYPE = 'pwm-dimmer'

  # PWM dimmer settings
  # According to http://www.esp8266-projects.com/2017/04/raspberry-pi-domoticz-ac-dimmer-part-1/
  # is 860 DIM value equal to 95% dimming -> 905 is 100% dimming
  DIMMER_MAXDIM = 870
  DIMMER_FREQ   = 5000

class terrariumPowerDimmerDC(terrariumPowerDimmerPiGPIOSource):
  TYPE = 'dc-dimmer'

  # DC dimmer settings
  DIMMER_MAXDIM = 1000 # https://github.com/theyosh/TerrariumPI/issues/178#issuecomment-412667010
  DIMMER_FREQ   = 15000 # https://github.com/theyosh/TerrariumPI/issues/178#issuecomment-413697246

class terrariumPowerDimmerIRF520(terrariumPowerDimmerPiGPIOSource):
  # https://opencircuit.nl/Product/IRF520-mosfet-module
  # https://github.com/DrLex0/MightyVariableFan/blob/master/pi_files/pwm_server.py#L97
  TYPE = 'irf520-dimmer'

  # Dimmer settings
  DIMMER_MAXDIM = 100
  DIMMER_FREQ   = 50 # Tested with a 24V PC fan.

class terrariumPowerDimmerBrightPi(terrariumPowerDimmerSource):
  TYPE = 'brightpi'

  def load_hardware(self):
    self._dimmer_running = False
    self._device = None
    try:
      self._device = brightpi.BrightPi()
      self._device.reset()
      self._device.set_gain(5)
      leds = brightpi.LED_WHITE
      if self.get_address().split(',')[-1].lower() == 'ir':
        leds = brightpi.LED_IR

      self._device.set_led_on_off(leds, brightpi.ON)
    except Exception as ex:
      print('load_hardware exception')
      print(ex)

class terrariumPowerDimmerPCA9685(terrariumPowerDimmerSource):
  TYPE = 'pca9685-dimmer'

  # Dimmer settings
  DIMMER_FREQ   = 1000

  def load_hardware(self):
    self._dimmer_running = False
    self._device = None
    try:
      gpio_pins = self.get_address().split(',')
      self._device = pca9685_driver.Device(int('0x' + gpio_pins[0],16))
      self._device.set_pwm_frequency(terrariumPowerDimmerPCA9685.DIMMER_FREQ)

    except Exception as ex:
      print('load_hardware exception')
      print(ex)

class terrariumPowerSwitchRemote(terrariumPowerSwitchSource):
  TYPE = 'remote'

  def set_hardware_state(self, state, force = False):
    pass

  def get_hardware_state(self):
    data = None
    url_data = terrariumUtils.parse_url(self.get_address())
    if url_data is False:
      logger.error('Remote url \'%s\' for switch \'%s\' is not a valid remote source url!' % (self.get_address(),self.get_name()))
    else:
      data = terrariumUtils.get_remote_data(self.get_address())

    return terrariumPowerSwitch.ON if terrariumUtils.is_true(data) else terrariumPowerSwitch.OFF

class terrariumPowerSwitchMSS425E(terrariumPowerSwitchSource):
  TYPE = 'mss425e'

  def __init__(self, switch_id, address, name = '', prev_state = None, callback = None):
    self.__device = address[0]
    super(terrariumPowerSwitchMSS425E,self).__init__(switch_id, address[1], name, prev_state, callback)

  def set_hardware_state(self, state, force = False):
    if state is terrariumPowerSwitch.ON:
      self.__device.turn_on_channel(int(self.get_address()))
    else:
      self.__device.turn_off_channel(int(self.get_address()))

  def get_hardware_state(self):
    data = None

    try:
      tmpdata = self.__device.get_sys_data()
      for channel_data in tmpdata['all']['digest']['togglex']:
        if int(self.get_address()) == int(channel_data['channel']):
          data = channel_data['onoff']
          break

    except Exception as ex:
      print('Get hardware ex')
      print(ex)

    return terrariumPowerSwitch.ON if terrariumUtils.is_true(data) else terrariumPowerSwitch.OFF

  @staticmethod
  def scan_power_switches(callback=None, **kwargs):
    if '' == kwargs['meross_username'] or '' == kwargs['meross_password']:
      logger.info('Meross cloud is not enabled.')
      return

    try:
      httpHandler = MerossHttpClient(email=kwargs['meross_username'], password=kwargs['meross_password'])
      logger.info('Logged into Meross cloud successfull.')

      devices = httpHandler.list_supported_devices()
      if len(devices) == 0:
        logger.warning('Unfortunaly your Meross device is not supported by this software. We found zero power switches.')
      for counter, device in enumerate(devices):
        data = device.get_sys_data()

        try:
          for channel_data in data['all']['digest']['togglex']:
            if int(channel_data['channel']) > 0:
              yield terrariumPowerSwitch(md5((terrariumPowerSwitchMSS425E.TYPE + data['all']['system']['hardware']['macAddress'] + str(channel_data['channel'])).encode()).hexdigest(),
                                         terrariumPowerSwitchMSS425E.TYPE,
                                         (device,int(channel_data['channel'])),
                                         'Channel {}'.format(channel_data['channel']),
                                         None,
                                         callback)

        except Exception as ex:
          print('Scan error in terrariumPowerSwitchMSS425E')
          print(ex)

    except UnauthorizedException as ex:
      logger.error('Authentication error with Merros cloud for \'{}\' type power switch. Please check username and password.'.format(terrariumPowerSwitchMSS425E.TYPE))

class terrariumPowerSwitchTypeException(TypeError):
  '''There is a problem with loading a hardware switch. Invalid hardware type.'''

  def __init__(self, message, *args):
    self.message = message
    super(terrariumPowerSwitchTypeException, self).__init__(message, *args)

# Factory class
class terrariumPowerSwitch(object):
  OFF = False
  ON = True

  POWER_SWITCHES = [terrariumPowerSwitchFTDI,
                    terrariumPowerSwitchGPIO,
                    terrariumPowerSwitchGPIOInverse,
                    terrariumPowerSwitchRelay8Stack,
                    terrariumPowerSwitchEnergenieUSB,
                    terrariumPowerSwitchEnergenieLAN,
                    terrariumPowerSwitchEnergenieRF,
                    terrariumPowerSwitchWeMo,
                    terrariumPowerSwitchRemote,
                    terrariumPowerDimmerPWM,
                    terrariumPowerDimmerDC,
                    terrariumPowerDimmerBrightPi,
                    terrariumPowerDimmerPCA9685,
                    terrariumPowerDimmerIRF520,
                    terrariumPowerSwitchDenkoviV2_4,
                    terrariumPowerSwitchDenkoviV2_8,
                    terrariumPowerSwitchDenkoviV2_16,
                    terrariumPowerSwitchSonoff,
                    terrariumPowerSwitchScript]

  if sys.version_info >= (3, 3):
    # Merros IoT library needs Python 3.3+
    POWER_SWITCHES.append(terrariumPowerSwitchMSS425E)

  if sys.version_info >= (3, 7):
    # Merros IoT library needs Python 3.3+
    from terrariumSwitchKasa import terrariumPowerSwitchTPLinkKasa
    POWER_SWITCHES.append(terrariumPowerSwitchTPLinkKasa)

  def __new__(self, switch_id, hardware_type, address, name = '', prev_state = None, callback = None):
    for powerswitch in terrariumPowerSwitch.POWER_SWITCHES:
      if hardware_type == powerswitch.TYPE:
        return powerswitch(switch_id, address, name, prev_state, callback)

    raise terrariumPowerSwitchTypeException('Power switch of type {} is unknown. We cannot controll this power switch.'.format(hardware_type))

  @staticmethod
  def valid_hardware_types():
    data = {}
    for powerswitch in terrariumPowerSwitch.POWER_SWITCHES:
      data[powerswitch.TYPE] = powerswitch.TYPE

    return data

  @staticmethod
  def scan_power_switches(callback=None, **kwargs):
    for power_switch_device in terrariumPowerSwitch.POWER_SWITCHES:
      try:
        for power_switch in power_switch_device.scan_power_switches(callback, **kwargs):
          yield power_switch
      except AttributeError as ex:
        logger.debug('Device \'{}\' does not support hardware scanning'.format(power_switch_device.TYPE))
