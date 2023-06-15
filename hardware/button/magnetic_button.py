# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from . import terrariumButton


class terrariumMagneticButton(terrariumButton):
    HARDWARE = "magnetic"
    NAME = "Magnetic (door) button"

    def _load_hardware(self):
        # Here we invert the values. Because when PRESSED, triggers will happen. But for a door, this is the normal case.
        self.RELEASED = 1
        self.PRESSED = 0

    @property
    def is_open(self):
        return self.pressed

    @property
    def is_closed(self):
        return not self.is_open
