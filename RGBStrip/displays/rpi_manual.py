#!/usr/bin/python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO

from .. import utils
from .base import BaseDisplay

# Prepare lookup table
BITS_8 = utils.generate_binary_array_lookup(8)


class RPiManualDisplay(BaseDisplay):
  """A display module for RGBStrip to output to Raspberry Pi via any 2 GPIO pins.
  """

  def __init__(
      self,
      controller,
      pixel_type,
      pin_data,
      pin_clock,
  ):
    super().__init__(controller, pixel_type)
    self.PIN_DATA = pin_data
    self.PIN_CLOCK = pin_clock

    # Setup GPIO
    GPIO.setup(
        self.PIN_DATA,
        GPIO.OUT,
    )
    GPIO.setup(
        self.PIN_CLOCK,
        GPIO.OUT,
    )

  def display(self):
    output_bytes = self.iter_bytes()
    for byte in output_bytes:
      bits = BITS_8[byte]
      for bit in bits:
        # Set the data pin
        GPIO.output(self.PIN_DATA, bit)

        # Cycle the clock
        GPIO.output(self.PIN_CLOCK, True)
        GPIO.output(self.PIN_CLOCK, False)
