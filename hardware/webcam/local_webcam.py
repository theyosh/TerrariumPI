# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWebcam

from pathlib import Path
from io import BytesIO
import re
from PIL import Image


class terrariumLocalWebcam(terrariumWebcam):
    HARDWARE = "local"
    NAME = "Local file webcam"
    VALID_SOURCE = r"^local://(.*)$"
    INFO_SOURCE = "local:///path/to/folder/with/image/file"

    def _load_hardware(self):
        return Path(re.search(self.VALID_SOURCE, self.address, re.IGNORECASE).group(1))

    def _get_raw_data(self):
        if not self._device["device"].exists():
            return False

        image = BytesIO(self._device["device"].read_bytes())

        try:
            with Image.open(image) as img:
                img.load()
            return image
        except OSError as e:
            logger.error(f"Webcam image for {self} is not ready yet: {e}")
        except Exception as e:
            logger.error(f"Webcam image for {self} is not ready yet: {e}")
