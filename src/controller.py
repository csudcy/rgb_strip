#!/usr/bin/python
# -*- coding: utf8 -*-
import math


class RGBStripController(object):
    """
    A simple interface for an APA102 RGB LED strip
    """

    def __init__(
            self,
            width,
            height=1
        ):
        self.WIDTH = width
        self.HEIGHT = height
        self.LED_COUNT = width * height

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

    def _get_offset(self, index):
        return self.BYTES_START + index * 4

    def _get_index(self, x, y):
        return (y * self.WIDTH) + (x if y % 2 == 0 else self.WIDTH - x - 1)

    def set_leds(self, r=0, g=0, b=0, a=0):
        for offset in xrange(self.BYTES_START, self.BYTES_START + self.BYTES_LED, 4):
            self._set_led(
                offset,
                r,
                g,
                b,
                a
            )

    def set_led(self, index, r=0, g=0, b=0, a=0):
        offset = self._get_offset(index)
        self._set_led(
            self._get_offset(index),
            r,
            g,
            b,
            a
        )

    def set_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        index = self._get_index(x, y)
        self.set_led(index, r, g, b, a)

    def add_led(self, index, r=0, g=0, b=0, a=0):
        offset = self._get_offset(index)
        self._set_led(
            self._get_offset(index),
            self.BYTES[offset + 3] + r,
            self.BYTES[offset + 2] + g,
            self.BYTES[offset + 1] + b,
            self.BYTES[offset + 0] + a
        )

    def add_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        index = self._get_index(x, y)
        self.add_led(index, r, g, b, a)

    def _set_led(self, offset, r, g, b, a):
        # Brightness max is 31; or with 224 to add the padding 1s
        self.BYTES[offset + 0] = (int(a) & 31) | 224
        # R, G, B are max 255
        self.BYTES[offset + 1] = int(b) & 255
        self.BYTES[offset + 2] = int(g) & 255
        self.BYTES[offset + 3] = int(r) & 255
