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

from hashlib import md5
from pylibftdi import Driver, BitBangDevice, SerialDevice, Device
from gpiozero import Energenie

try:
  import thread as _thread
except ImportError as ex:
  import _thread

try:
  from meross_iot.api import MerossHttpClient, UnauthorizedException
except ImportError as ex:
  # Python 2 does not support Meross XXX Power Switches
  pass

from terrariumUtils import terrariumUtils, terrariumTimer

# Dirty hack to include someone his code... to lazy to make it myself :)
# https://github.com/perryflynn/energenie-connect0r
sys.path.insert(0, './energenie-connect0r')
import energenieconnector

from gevent import monkey, sleep
monkey.patch_all()

class terrariumPowerSwitchSource(object):
  TYPE = None

  def __init__(self, switchid, address, name = '', prev_state = None, callback = None):
    logger.info('Initialising \'{}\' power switch object'.format(self.get_type()))
    self.power_wattage = 0.0
    self.water_flow = 0.0
    self.manual_mode = False

    self.switchid = switchid
    self.set_name(name)
    self.set_address(address)

    self.callback = callback
    self.timer = terrariumTimer('00:00','00:00',0,0,False)

    self.load_hardware()

    self.state = None
    if self.get_type() not in [terrariumPowerSwitchWeMo.TYPE, terrariumPowerSwitchMSS425E.TYPE]:
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

  def set_state(self, state, force = False):
    changed = False
    logger.debug('Changing power switch \'{}\' of type \'{}\' at address \'{}\' from state \'{}\' to state \'{}\' (Forced:{})'.format(self.get_name(),
                                                                                                                              self.get_type(),
                                                                                                                              self.get_address(),
                                                                                                                              self.get_state(),
                                                                                                                              state,force))

    if self.get_state() is not state or terrariumUtils.is_true(force):
      try:
        old_state = self.get_state()
        self.set_hardware_state(state,force)
        self.state = state
        changed = True

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

    if changed and self.callback is not None:
      self.callback(self.get_data())

    return changed

  def get_state(self):
    return self.state

  def stop(self):
    pass

  def in_manual_mode(self):
    return terrariumUtils.is_true(self.manual_mode)

  def set_manual_mode(self,mode):
    self.manual_mode = terrariumUtils.is_true(mode)

  def update(self):
    self.timer_update()
    data = self.get_hardware_state()
    if data is not None:
      self.set_state(data)

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
            'manual_mode' : self.in_manual_mode()}

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

  def load_hardware(self):
    self.__device_type = None
    for device in Driver().list_devices():
      vendor, product, self.__device = [x.decode('latin1') for x in device]
      self.__device_type = 'Serial' if product.endswith('UART') else 'BitBang'
      logger.debug('Found switch board {}, {}, {}, of type {}'.format(vendor,product,self.__device,self.__device_type))
      break # For now, we only support 1 switch board!

  def set_address(self,value):
    if value in terrariumPowerSwitchFTDI.BITBANG_ADDRESSES:
      self.address = value

  def set_hardware_state(self, state, force = False):
    if 'BitBang' == self.__device_type:
      with BitBangDevice(self.__device) as device:
        device.baudrate = 9600
        if state is terrariumPowerSwitch.ON:
          device.port |= int(terrariumPowerSwitchFTDI.BITBANG_ADDRESSES[str(self.get_address())], 16)
        else:
          device.port &= ~int(terrariumPowerSwitchFTDI.BITBANG_ADDRESSES[str(self.get_address())], 16)
        device.close()

    elif 'Serial' == self.__device_type:
      with SerialDevice(self.__device) as device:
        device.baudrate = 9600
        cmd = chr(0xff) + chr(0x0 + int(self.get_address())) + chr(0x0 + (1 if state is terrariumPowerSwitch.ON else 0))
        device.write(cmd)
        device.close()

class terrariumPowerSwitchGPIO(terrariumPowerSwitchSource):
  TYPE = 'gpio'

  def load_hardware(self):
    GPIO.setup(terrariumUtils.to_BCM_port_number(self.get_address()), GPIO.OUT)

  def stop(self):
    GPIO.cleanup(terrariumUtils.to_BCM_port_number(self.get_address()))

  def set_hardware_state(self, state, force = False):
    if self.get_type() == terrariumPowerSwitchGPIO.TYPE:
      GPIO.output(terrariumUtils.to_BCM_port_number(self.get_address()), ( GPIO.HIGH if state is terrariumPowerSwitch.ON else GPIO.LOW ))

    elif self.get_type() == terrariumPowerSwitchGPIOInverse.TYPE:
      GPIO.output(terrariumUtils.to_BCM_port_number(self.get_address()), ( GPIO.LOW if state is terrariumPowerSwitch.ON else GPIO.HIGH ))

class terrariumPowerSwitchGPIOInverse(terrariumPowerSwitchGPIO):
  TYPE = 'gpio-inverse'

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

  def load_hardware(self):
    # We have per device 4 outlets.... so outlet 7 is device 1
    self.__device = (int(self.get_address())-1) / 4
    if self.__device < 0:
      self.__device = 0

  def set_hardware_state(self, state, force = False):
    address = int(self.get_address()) % 4
    if address == 0:
      address = 4

    if sys.version_info.major == 2:
      with open(os.devnull, 'w') as devnull:
        subprocess.call(['/usr/bin/sispmctl', '-d',str(self.__device),('-o' if state is terrariumPowerSwitch.ON else '-f'),str(address)],stdout=devnull, stderr=subprocess.STDOUT)
    elif sys.version_info.major == 3:
      subprocess.run(['/usr/bin/sispmctl', '-d',str(self.__device),('-o' if state is terrariumPowerSwitch.ON else '-f'),str(address)],capture_output=True)

class terrariumPowerSwitchEnergenieLAN(terrariumPowerSwitchSource):
  TYPE = 'eg-pm-lan'
  VALID_SOURCE = '^http:\/\/((?P<passwd>[^@]+)@)?(?P<host>[^#\/]+)(\/)?#(?P<switch>[1-4])$'

  def set_address(self,value):
    super(terrariumPowerSwitchEnergenieLAN, self).set_address(value)
    self.load_hardware()

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

      #except Exception as ex:
      #  logger.exception('Could not login to the Energenie LAN device %s at location %s. Error status %s' % (self.get_name(),self.get_address(),ex))
      #  changed = False

    return changed

  def stop(self):
    self.__device.logout()

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

class terrariumPowerSwitchDenkoviV2_4(terrariumPowerSwitchSource):
  TYPE = 'denkovi_v2_4'

  def _get_relay_count(self):
    return int(self.TYPE.split('_')[-1])

  def _get_board_type(self):
    return '{}v2'.format(self._get_relay_count())

  def load_hardware(self):
    serial_regex = r"^(?P<serial>[^ ]+)\W(\[[^\]]+\])\W\[id=\d\]$"

    # We only support one board for now...
    cmd = ['sudo','/usr/bin/java','-jar','DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar','list']

    print('Get power switch serial data:')
    print(cmd)

    try:
      data = subprocess.check_output(cmd).strip().decode('utf-8')
      print(data)

      data = data.split("\n")
      for line in data:
        print(line)
        match = re.match(r"^(?P<serial>[^ ]+)\W(\[[^\]]+\])\W\[id=\d\]$",line,re.MULTILINE)
        print(match)
        if match:
          self.__device = str(match.group('serial'))
          break

    except Exception as err:
      # Ignore for now
      print('Get serial error')
      print(err)


  def get_hardware_state(self):
    address = int(self.get_address()) % self._get_relay_count()
    if address == 0:
      address = self._get_relay_count()

    data = None
    cmd = ['sudo','/usr/bin/java','-jar','DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar',self.__device,self._get_board_type(),str(address),'status']
    print('Get power switch state cmd:')
    print(cmd)

    try:

      data = subprocess.check_output(cmd).strip().decode('utf-8')
      print(data)

    except Exception as err:
      # Ignore for now
      print('Get state error')
      print(err)

    return terrariumPowerSwitch.ON if terrariumUtils.is_true(data) else terrariumPowerSwitch.OFF

  def set_hardware_state(self, state, force = False):
    address = int(self.get_address()) % self._get_relay_count()
    if address == 0:
      address = self._get_relay_count()

    cmd = ['sudo','/usr/bin/java','-jar','DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar',self.__device,self._get_board_type(),str(address),str(1 if state is terrariumPowerSwitch.ON else 0)]

    print('Set power switch state cmd:')
    print(cmd)

    try:
      if sys.version_info.major == 2:
        with open(os.devnull, 'w') as devnull:
          subprocess.call(cmd,stdout=devnull, stderr=subprocess.STDOUT)
      elif sys.version_info.major == 3:
        subprocess.run(cmd,capture_output=True)
    except Exception as err:
      # Ignore for now
      print('Set state error')
      print(err)

    print('Set state done!')

class terrariumPowerSwitchDenkoviV2_8(terrariumPowerSwitchDenkoviV2_4):
  TYPE = 'denkovi_v2_8'

class terrariumPowerSwitchDenkoviV2_16(terrariumPowerSwitchDenkoviV2_4):
  TYPE = 'denkovi_v2_16'

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

    self.__dimmer_state = 0.0
    super(terrariumPowerDimmerSource,self).__init__(switchid, address, name, prev_state, callback)

  def get_state(self):
    return self.__dimmer_state

  def load_hardware(self):
    self.__dimmer_running = False
    pigpio.exceptions = False
    self.__pigpio = pigpio.pi('localhost')
    if not self.__pigpio.connected:
      self.__pigpio = pigpio.pi()
      if not self.__pigpio.connected:
        logger.error('PiGPIOd process is not running')
        self.__pigpio = False

    pigpio.exceptions = True
    self.__pigpio.set_pull_up_down(terrariumUtils.to_BCM_port_number(self.get_address()), pigpio.PUD_OFF)

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
    if not self.__dimmer_running:
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
    if not self.__dimmer_running:
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
      _thread.start_new_thread(self.__dim_switch, (value,duration))

    return True

  def __dim_switch(self,value,duration):
    # When the dimmer is working, ignore new state changes.
    if not self.__dimmer_running:
      self.__dimmer_running = True

      self.__dimmer_state = (0.0 if not terrariumUtils.is_float(self.get_state()) else float(self.get_state()))
      value    = (0.0 if not terrariumUtils.is_float(value) else float(value))
      duration = (0.0 if not terrariumUtils.is_float(duration) else float(duration))

      direction = (1.0 if self.__dimmer_state <= value else -1.0)
      distance  = abs(self.__dimmer_state - value)

      if int(duration) == 0 or int(distance) == 0:
        steps = 1.0
      else:
        steps = math.floor(min( (abs(duration) / terrariumPowerDimmerSource.DIMMER_MIN_TIMEOUT),
                                (distance / terrariumPowerDimmerSource.DIMMER_MIN_STEP)))
        distance /= steps
        duration /= steps

      logger.debug('Dimmer settings: Steps: %s, Distance per step: %s%%, Time per step: %s, Direction: %s',steps, distance, duration, direction)

      for counter in range(int(steps)):
        self.__dimmer_state += (direction * distance)
        if self.get_type() == terrariumPowerDimmerPWM.TYPE:
          dim_value = terrariumPowerDimmerPWM.DIMMER_MAXDIM * ((100.0 - float(self.__dimmer_state)) / 100.0)
          dim_freq = terrariumPowerDimmerPWM.DIMMER_FREQ
        elif self.get_type() == terrariumPowerDimmerDC.TYPE:
          dim_value = terrariumPowerDimmerDC.DIMMER_MAXDIM * (float(self.__dimmer_state) / 100.0)
          dim_freq = terrariumPowerDimmerDC.DIMMER_FREQ

        for gpiopin in self.get_address().split(','):
          if terrariumUtils.to_BCM_port_number(gpiopin) is False:
            continue
          logger.debug('Dimmer animation: Step: %s, value %s%%, Dim value: %s, timeout %s',counter+1, self.__dimmer_state, dim_value, duration)
          self.__pigpio.hardware_PWM(terrariumUtils.to_BCM_port_number(gpiopin), dim_freq, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle

        if duration > 0.0:
          sleep(duration)

        # For impatient people... Put the dimmer at the current state value if it has changed during the animation (DISABLED FOR NOW)
        # dim_value = terrariumSwitch.PWM_DIMMER_MAXDIM * ((100.0 - self.get_state()) / 100.0)
        # self.__pigpio.hardware_PWM(terrariumUtils.to_BCM_port_number(self.get_address()), 5000, int(dim_value) * 1000) # 5000Hz state*1000% dutycycle

      self.__dimmer_state = value
      self.__dimmer_running = False
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

class terrariumPowerDimmerPWM(terrariumPowerDimmerSource):
  TYPE = 'pwm-dimmer'

  # PWM dimmer settings
  # According to http://www.esp8266-projects.com/2017/04/raspberry-pi-domoticz-ac-dimmer-part-1/
  # is 860 DIM value equal to 95% dimming -> 905 is 100% dimming
  DIMMER_MAXDIM = 870
  DIMMER_FREQ   = 5000

class terrariumPowerDimmerDC(terrariumPowerDimmerSource):
  TYPE = 'dc-dimmer'

  # DC dimmer settings
  DIMMER_MAXDIM = 1000 # https://github.com/theyosh/TerrariumPI/issues/178#issuecomment-412667010
  DIMMER_FREQ   = 15000 # https://github.com/theyosh/TerrariumPI/issues/178#issuecomment-413697246

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
      if tmpdata['all']['system']['hardware']['type'] == terrariumPowerSwitchMSS425E.TYPE:
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
      return

    try:
      httpHandler = MerossHttpClient(email=kwargs['meross_username'], password=kwargs['meross_password'])

      devices = httpHandler.list_supported_devices()
      for counter, device in enumerate(devices):
        data = device.get_sys_data()

        try:
          if data['all']['system']['hardware']['type'] == terrariumPowerSwitchMSS425E.TYPE:
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
                    terrariumPowerSwitchEnergenieUSB,
                    terrariumPowerSwitchEnergenieLAN,
                    terrariumPowerSwitchEnergenieRF,
                    terrariumPowerSwitchWeMo,
                    terrariumPowerSwitchRemote,
                    terrariumPowerDimmerPWM,
                    terrariumPowerDimmerDC,
                    terrariumPowerSwitchDenkoviV2_4,
                    terrariumPowerSwitchDenkoviV2_8,
                    terrariumPowerSwitchDenkoviV2_16]

  if sys.version_info >= (3, 3):
    # Merros IoT library needs Python 3.3+
    POWER_SWITCHES.append(terrariumPowerSwitchMSS425E)

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
