#!/usr/bin/python
# -*- coding: utf8 -*-
import spidev

class RPiSPIDisplay(object):
    """
    A display module for RGBStrip to output to Raspberry Pi via the SPI chip.
    """

    def __init__(self, bus=0, device=0, speed_mhz=16):
        # Init the SPI bus
        self.SPI = spidev.SpiDev()
        self.SPI.open(
            bus,
            device
        )
        self.SPI.max_speed_hz = speed_mhz * 1000 * 1000

    def display(self, bytes):
        self.SPI.writebytes(bytes)
