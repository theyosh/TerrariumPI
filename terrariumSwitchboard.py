# -*- coding: utf-8 -*-
from pylibftdi import Driver, BitBangDevice, SerialDevice, Device
from hashlib import md5

class terrariumSwitchboard():
  bitbang_addresses = {
    "1":"2",
    "2":"8",
    "3":"20",
    "4":"80",
    "all":"FF"
  }

  OFF = False
  ON = True

  def __init__(self, config, callback = None):
    switch_config = config.get_system()
    self.max_number_of_switches = int(switch_config['max_switches'])
    # Reload config
    switch_config = config.get_switches()['switches']
    self.active_number_of_switches = self.max_number_of_switches if len(switch_config) == 0 else len(switch_config)

    switch_numbers = [None] * self.active_number_of_switches
    for switchid in switch_config:
      switch_numbers[int(switch_config[switchid]['nr'])-1] = switchid

    self.id = None
    self.device = None
    self.device_type = None
    self.switches = {}

    for device in Driver().list_devices():
      vendor, product, self.device = map(lambda x: x.decode('latin1'), device)
      self.device_type = 'Serial' if product.endswith('UART') else 'BitBang'
      break # For now, we only support 1 switch board!

    for nr in range(0,self.active_number_of_switches):
      power_switch_config = {}
      if switch_numbers[nr] is not None:
        power_switch_config = switch_config[switch_numbers[nr]]

      power_switch = terrariumSwitch(self.device,
                                        self.device_type,
                                        power_switch_config['nr'] if 'nr' in power_switch_config else nr+1,
                                        power_switch_config['name'] if 'name' in power_switch_config else '',
                                        power_switch_config['power_wattage'] if 'power_wattage' in power_switch_config else 0.0,
                                        power_switch_config['water_flow'] if 'water_flow' in power_switch_config else 0.0,
                                        callback)

      self.switches[power_switch.get_id()] = power_switch

    self.id = md5(b'' + self.device + self.device_type).hexdigest()

  def get_id(self):
    return self.id

  def get_device(self):
    return self.device

  def get_type(self):
    return self.device_type

  def get_config(self):
    config = self.get_switches()
    config['max_switches'] = self.max_number_of_switches
    return config

  def reload(self,config):
    switch_config = config.get_switches()

    for switch in self.switches:
      switch.set_name(switch_config['switches'][switch.get_nr()-1]['name'])
      switch.set_power_wattage(switch_config['switches'][switch.get_nr()-1]['power_wattage'])
      switch.set_water_flow(switch_config['switches'][switch.get_nr()-1]['water_flow'])

  def get_switches(self):
    data = {'switchboard_id':self.get_id(),
            'switchboard_device':self.get_device(),
            'switchboard_type':self.get_type(),
            'switches' : []}

    for switch in self.switches:
      data['switches'].append({'id': switch.get_id(),
                                 'nr' : switch.get_nr(),
                                 'name': switch.get_name(),
                                 'state': switch.get_state(),
                                 'power_wattage': switch.get_power_wattage(),
                                 'water_flow': switch.get_water_flow()})

    return data


class terrariumSwitch():

  def __init__(self,device,device_type,nr,name = '', power_wattage = 0, water_flow = 0, callback = None):
    self.nr = int(nr)
    self.device = device
    self.device_type = device_type
    self.bitbang_address = terrariumSwitchboard.bitbang_addresses if 'BitBang' == self.device_type else None
    self.callback = callback

    self.id = md5(b'' + self.device + self.device_type + str(self.nr)).hexdigest()

    self.set_name(name)
    self.set_power_wattage(power_wattage)
    self.set_water_flow(water_flow)

    # Force to off state!
    self.state = None
    self.set_state(False,True)

  def set_state(self, state, force = False):
    if self.get_state() is not state or force:
      try:
        if 'BitBang' == self.device_type:
          with BitBangDevice(self.device) as device:
            device.baudrate = 9600
            if state is terrariumSwitchboard.ON:
              device.port |= int(self.bitbang_address[str(self.nr)], 16)
            else:
              device.port &= ~int(self.bitbang_address[str(self.nr)], 16)
            device.close()

        elif 'Serial' == self.device_type:
          with SerialDevice(self.device) as device:
            device.baudrate = 9600
            cmd = chr(0xff) + chr(0x0 + self.nr) + chr(0x0 + (1 if state is terrariumSwitchboard.ON else 0))
            device.write(cmd)
            device.close()

#        terrarium_log.info('Switched switch %s(%s) from %s',self.getName(),self.getID(),('off to on' if 'on' == state else 'on to off'))
        self.state = state
        self.callback(self.get_data())
      except Exception, err:
        # Ignore for now
        pass

      finally:
        pass

#    else:
#        return false
#      terrarium_log.warn('No action made. State of switch %s(%s) is already in the requested state: %s', self.getName(),self.getID(),('on' if self.getState() else 'off'))

    return self.get_state() == state

  def get_state(self,force = False):
    if force:
      try:
        old_state = self.get_state()
        if 'BitBang' == self.device_type:
          with BitBangDevice(self.device) as device:
            device.baudrate = 9600
            self.state = self.__get_relay_state( device.port )
            device.close()
        elif 'Serial' == self.device_type:
          # Not posible to question device...
          self.state = self.state

        if old_state != self.get_state():
          #terrarium.debug('Changed status of switch %s(%s) from %s to %s',self.getName(), self.getID(), ('on' if old_state else 'off'),('on' if self.getState() else 'off'))
          self.callback(self.get_data())

      except Exception, err:
        pass
        #terrarium_log.error('Error updating switch %s(%s). Got error: %s',self.getName(),self.getID(),err)
      finally:
        pass

    return self.state

  def get_data(self):
    return {'id': self.get_id(),
            'nr' : self.get_nr(),
            'name' : self.get_name(),
            'power_wattage' : self.get_power_wattage(),
            'water_flow' : self.get_water_flow(),
            'state' : self.get_state()}

  def get_id(self):
    return self.id

  def get_nr(self):
    return self.nr

  def get_name(self):
    return self.name if self.name is not '' else 'Switch ' + str(self.nr)

  def set_name(self,name):
    self.name = name

  def get_power_wattage(self):
    return self.power_wattage

  def set_power_wattage(self,value):
    self.power_wattage = float(value)

  def get_water_flow(self):
    return self.water_flow

  def set_water_flow(self,value):
    self.water_flow = float(value)

  def toggle(self):
    if self.get_state() is not None:
      old_state = self.get_state()
      self.set_state(not old_state)
      return self.get_state() is not old_state

    return None

  def is_on(self):
    return self.get_state() is terrariumSwitchboard.ON

  def is_off(self):
    return self.get_state() is terrariumSwitchboard.OFF

  def on(self):
    if self.get_state() is None or self.is_off():
      self.set_state(terrariumSwitchboard.ON)
      return self.is_on()

  def off(self):
    if self.get_state() is None or self.is_on():
      self.set_state(terrariumSwitchboard.OFF)
      return self.is_off()
