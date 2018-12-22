#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.controllers.base import BaseController


class RectangularController(BaseController):
    """
    An interface to control a rectangular strip of RGB LEDs.
    """

    def __init__(
            self,
            width,
            height=1,
            reverse_x=False,
            reverse_y=False
        ):
        self.WIDTH = width
        self.HEIGHT = height
        self.REVERSE_X = reverse_x
        self.REVERSE_Y = reverse_y
        BaseController.__init__(self, width*height)

    def _get_index(self, x, y):
        if self.REVERSE_X:
            x = self.WIDTH - x - 1
        if self.REVERSE_Y:
            y = self.HEIGHT - y - 1
        return (y * self.WIDTH) + (x if y % 2 == 0 else self.WIDTH - x - 1)

    def add_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        index = self._get_index(x, y)
        self.add_led(index, r, g, b, a)

    def set_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        index = self._get_index(x, y)
        self.set_led(index, r, g, b, a)

    def get_rgba_xy(self, x, y):
        index = self._get_index(x, y)
        return self.get_rgba(index)
