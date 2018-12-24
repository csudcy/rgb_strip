#!/usr/bin/python
# -*- coding: utf8 -*-
import math


class BaseController(object):
    """
    An interface to control a strip of RGB LEDs.
    """

    def __init__(self, config, led_count, a):
        self.CONFIG = config
        self.LED_COUNT = led_count
        self.A = a

        # Work out some byte counts
        self.BYTES_START = 4
        self.BYTES_LED = self.LED_COUNT * 4
        end_bit_count = self.LED_COUNT / 2.0
        self.BYTES_END = int(math.ceil(end_bit_count / 8.0))
        self.BYTES_TOTAL = self.BYTES_START + self.BYTES_LED + self.BYTES_END

        # Setup the byte array that we will output
        self.BYTES = [None] * self.BYTES_TOTAL

        # Setup the start & end frames
        self.BYTES[:self.BYTES_START] = [0x00] * self.BYTES_START
        self.BYTES[-self.BYTES_END:] = [0xFF] * self.BYTES_END

        # Setup the LED frames so the padding bits are set correctly
        self.set_leds()

    def add_led(self, index, r=0, g=0, b=0):
        offset = self._get_offset(index)
        self._set_led(
            self._get_offset(index),
            self.BYTES[offset + 3] + r,
            self.BYTES[offset + 2] + g,
            self.BYTES[offset + 1] + b
        )

    def set_led(self, index, r=0, g=0, b=0):
        self._set_led(
            self._get_offset(index),
            r,
            g,
            b
        )

    def set_leds(self, r=0, g=0, b=0):
        for offset in xrange(self.BYTES_START, self.BYTES_START + self.BYTES_LED, 4):
            self._set_led(
                offset,
                r,
                g,
                b
            )

    def _get_offset(self, index):
        return self.BYTES_START + index * 4

    def _set_led(self, offset, r, g, b):
        # Brightness max is 31; or with 224 to add the padding 1s
        self.BYTES[offset + 0] = max(min(int(self.A), 31), 0) | 224
        # R, G, B are max 255
        self.BYTES[offset + 1] = max(min(int(b), 255), 0)
        self.BYTES[offset + 2] = max(min(int(g), 255), 0)
        self.BYTES[offset + 3] = max(min(int(r), 255), 0)

    def get_rgba(self, index):
        offset = self._get_offset(index)
        return (
            self.BYTES[offset + 3],
            self.BYTES[offset + 2],
            self.BYTES[offset + 1],
            self.BYTES[offset + 0]
        )