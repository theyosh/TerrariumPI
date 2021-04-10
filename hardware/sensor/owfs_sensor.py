from . import terrariumSensor

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
          yield terrariumSensor(None,
                                terrariumOWFSSensor.HARDWARE,
                                'temperature',
                                address,
                                f'{terrariumOWFSSensor.NAME} measuring temperature',
                                unit_value_callback = unit_value_callback,
                                trigger_callback    = trigger_callback)

        except protocol.OwnetError as ex:
          pass

        try:
          humidity = float(proxy.read(sensor + '/humidity'))
          yield terrariumSensor(None,
                                terrariumOWFSSensor.HARDWARE,
                                'humidity',
                                address,
                                f'{terrariumOWFSSensor.NAME} measuring humidity',
                                unit_value_callback = unit_value_callback,
                                trigger_callback    = trigger_callback)

        except protocol.OwnetError:
          pass

    except Exception as ex:
      pass