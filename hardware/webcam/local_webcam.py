from . import terrariumWebcam, terrariumWebcamException
from terrariumUtils import terrariumUtils

from pathlib import Path
from io import BytesIO
import re

class terrariumLocalWebcam(terrariumWebcam):
  HARDWARE     = 'local'
  NAME         = 'Local file webcam'
  VALID_SOURCE = r'^local://(.*)$'
  INFO_SOURCE  = 'local:///path/to/folder/with/image/file'

  def _load_hardware(self):
    self._device['device'] = Path(re.search(self.VALID_SOURCE, self.address, re.IGNORECASE).group(1))

  def _get_raw_data(self):
    if not self._device['device'].exists():
      return False

    return BytesIO(self._device['device'].read_bytes())