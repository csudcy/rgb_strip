#!/usr/bin/python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO

from .. import utils

# Prepare lookup table
BITS_8 = utils.generate_binary_array_lookup(8)

class RPiManualDisplay(object):
    """
    A display module for RGBStrip to output to Raspberry Pi via any 2 GPIO pins.
    """

    def __init__(
            self,
            rgb_strip,
            pin_data,
            pin_clock,
        ):
        self.RGB_STRIP = rgb_strip
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

    def display(self, bytes):
        for byte in bytes:
            bits = BITS_8[byte]
            for bit in bits:
                # Set the data pin
                GPIO.output(self.PIN_DATA, bit)

                # Cycle the clock
                GPIO.output(self.PIN_CLOCK, True)
                GPIO.output(self.PIN_CLOCK, False)
