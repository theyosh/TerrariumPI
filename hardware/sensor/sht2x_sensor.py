from . import terrariumI2CSensor, terrariumI2CSensorMixin
from terrariumUtils import terrariumUtils

class terrariumSHT2XSensor(terrariumI2CSensor, terrariumI2CSensorMixin):
  HARDWARE = 'sht2x'
  TYPES    = ['temperature','humidity']
  NAME     = 'Sensirion SHT2X sensor'

  # SHT2XX - 3.3 Volt VCC
  # 黄 = Yellow = DATA
  # 蓝 = Blue   = CLK
  # 黑 = Black  = GND
  # 棕 = Brown  = VCC

  # datasheet (v4), page 9, table 7, thanks to Martin Milata
  # for suggesting the use of these better values
  # code copied from https://github.com/mmilata/growd
  # http://www.farnell.com/datasheets/1780639.pdf
  # https://cdn-shop.adafruit.com/datasheets/Sensirion_Humidity_SHT1x_Datasheet_V5.pdf
  TEMPERATURE_WAIT_TIME = 0.086 # (datasheet: typical=66, max=85 in ms)
  HUMIDITY_WAIT_TIME    = 0.030 # (datasheet: typical=22, max=29 in ms)
  SOFTRESET_TIMEOUT     = 0.016 # (datasheet: typical=??, max=15 in ms)