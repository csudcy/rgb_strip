#!/usr/bin/python
# -*- coding: utf8 -*-
try:
  import spidev
except ImportError:
  # spidev is not installed
  spidev = None

from .base import BaseDisplay


class RPiSPIDisplay(BaseDisplay):
  """A display module for RGBStrip to output to Raspberry Pi via the SPI chip.
  """

  def __init__(self, controller, pixel_type, bus=0, device=0, speed_mhz=16):
    if spidev is None:
      raise Exception(
          'To use RaspberryPi SPI output, you must pip install spidev!')

    super().__init__(controller, pixel_type)

    # Init the SPI bus
    self.SPI = spidev.SpiDev()
    self.SPI.open(bus, device)
    self.SPI.max_speed_hz = int(speed_mhz * 1000 * 1000)

  def display(self):
    output_bytes = self.iter_bytes()
    self.SPI.writebytes(output_bytes)
