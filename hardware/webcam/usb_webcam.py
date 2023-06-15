# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWebcam

# pip install opencv-python-headless
import cv2

from PIL import Image
from pathlib import Path
from io import BytesIO

from gevent import sleep


class terrariumUSBWebcam(terrariumWebcam):
    HARDWARE = "usbcam"
    NAME = "USB camera"
    VALID_SOURCE = r"^/dev/video\d+"
    INFO_SOURCE = "/dev/video[NR]"

    def _load_hardware(self):
        if not Path(self.address).exists():
            return None

        return int(self.address[10:])

    def _get_raw_data(self):
        stream = BytesIO()
        camera = cv2.VideoCapture(self.device)
        camera.set(3, float(self.width))
        camera.set(4, float(self.height))
        sleep(self._WARM_UP)
        readok, image = camera.read()

        if readok:
            jpeg = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            jpeg.save(stream, "JPEG")

        camera.release()

        if readok:
            return stream

        return False
