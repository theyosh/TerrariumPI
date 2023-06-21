# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from .usb_webcam import terrariumUSBWebcam

# pip install opencv-python-headless
import cv2


class terrariumRTSPWebcam(terrariumUSBWebcam):
    HARDWARE = "rtsp"
    NAME = "RTSP camera"
    VALID_SOURCE = r"^rtsp?://.*(?<!\.m3u8)$"
    INFO_SOURCE = "rtsp://server.com/stream"

    def _load_hardware(self):
        camera = cv2.VideoCapture(self.device)
        if camera is not None:
            return self.address

        return None
