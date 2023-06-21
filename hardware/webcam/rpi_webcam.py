# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumWebcam
from io import BytesIO

from pathlib import Path
import subprocess


class terrariumRPIWebcam(terrariumWebcam):
    HARDWARE = "rpicam"
    NAME = "Raspberry PI camera"
    VALID_SOURCE = r"^rpicam$"
    INFO_SOURCE = "rpicam"

    def _load_hardware(self):
        # # New RPI Camera app
        # raspistill = Path('/usr/bin/libcamera-still')
        # if not raspistill.exists():

        # Old RPI Camera app (works better...)
        raspistill = Path("/usr/bin/raspistill")
        if not raspistill.exists():
            return None

        return [str(raspistill), "--quality", "95", "--timeout", str(self._WARM_UP * 1000), "--encoding", "jpg"]

    def _get_raw_data(self):
        if self._device["device"] is None:
            return False

        cmd = self._device["device"] + [
            "--width",
            str(self.width),
            "--height",
            str(self.height),
            "--awb",
            self.awb,
            "--output",
            "-",
        ]
        logger.debug(f"Starting rpicam: {cmd}")

        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False) as proc:
            out, _ = proc.communicate()
            return BytesIO(out)

        return False
