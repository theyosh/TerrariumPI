from . import terrariumSensor
from terrariumUtils import terrariumUtils

# pip install pyownet
from pyownet import protocol

class terrariumOWFSSensor(terrariumSensor):
  HARDWARE = 'owfs'
  TYPES    = ['temperature','humidity']
  NAME     = 'One-Wire File System'

  __HOST = 'localhost'
  __PORT = 4304

  def _load_hardware(self):
    # For now, we use/depend on the OWFS defaults
    device = protocol.proxy(self.__HOST, self.__PORT)
    return device

  def _get_data(self):
    data = {}

    try:
      data['temperature'] = float(self.device.read('/{}/temperature'.format(self.address.strip('/'))))
    except protocol.OwnetError:
       pass

    try:
      data['humidity'] = float(self.device.read('/{}/humidity'.format(self.address.strip('/'))))
    except protocol.OwnetError:
       pass

    return data

  @staticmethod
  def _scan_sensors(unit_value_callback = None, trigger_callback = None):
    try:
      proxy = protocol.proxy(terrariumOWFSSensor.__HOST, terrariumOWFSSensor.__PORT)
      for sensor in proxy.dir(slash=False, bus=False):
        stype = proxy.read(sensor + '/type').decode()
        address = proxy.read(sensor + '/address').decode()
        try:
          temp = float(proxy.read(sensor + '/temperature'))
          yield terrariumOWFSSensor(None,
                                    'temperature',
                                     address,
                                    '{} measuring {}'.format(terrariumOWFSSensor.NAME, 'temperature'),
                                    unit_value_callback = unit_value_callback,
                                    trigger_callback    = trigger_callback)

        except protocol.OwnetError:
          pass

        try:
          humidity = float(proxy.read(sensor + '/humidity'))
          yield terrariumOWFSSensor(None,
                                    'humidity',
                                    address,
                                    '{} measuring {}'.format(terrariumOWFSSensor.NAME, 'humidity'),
                                    unit_value_callback = unit_value_callback,
                                    trigger_callback    = trigger_callback)

        except protocol.OwnetError:
          pass

    except Exception as ex:
      pass
      #logger.warning('OWFS file system is not actve / installed on this device! If this is not correct, try \'i2cdetect -y 1\' to see if device is connected.')