#!/usr/bin/python
# -*- coding: utf8 -*-
import spidev

from .base import BaseDisplay


class RPiSPIDisplay(BaseDisplay):
    """
    A display module for RGBStrip to output to Raspberry Pi via the SPI chip.
    """

    def __init__(self, controller, bus=0, device=0, speed_mhz=16):
        BaseDisplay.__init__(self, controller)

        # Init the SPI bus
        self.SPI = spidev.SpiDev()
        self.SPI.open(
            bus,
            device
        )
        self.SPI.max_speed_hz = speed_mhz * 1000 * 1000

    def display(self):
        self.SPI.writebytes(self.CONTROLLER.BYTES)
