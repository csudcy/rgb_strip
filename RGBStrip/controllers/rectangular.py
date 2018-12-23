#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.controllers.base import BaseController


class RectangularController(BaseController):
    """
    An interface to control a strip of RGB LEDs arranged in a rectangle.
    """

    def __init__(
            self,
            width,
            height=1,
            reverse_x=False,
            reverse_y=False,
            a=0.2
        ):
        self.WIDTH = width
        self.HEIGHT = height
        self.REVERSE_X = reverse_x
        self.REVERSE_Y = reverse_y
        config = {
            'a': a,
            'height': height,
            'reverse_x': reverse_x,
            'reverse_y': reverse_y,
            'type': 'rectangle',
            'width': width,
        }
        BaseController.__init__(self, config, width*height, a)

    def _get_index(self, x, y):
        if self.REVERSE_X:
            x = self.WIDTH - x - 1
        if self.REVERSE_Y:
            y = self.HEIGHT - y - 1
        return (y * self.WIDTH) + (x if y % 2 == 0 else self.WIDTH - x - 1)

    def add_led(self, x, y, *args, **kwargs):
        index = self._get_index(x, y)
        BaseController.add_led(self, index, *args, **kwargs)

    def set_led(self, x, y, *args, **kwargs):
        index = self._get_index(x, y)
        BaseController.set_led(self, index, *args, **kwargs)

    def get_rgba(self, x, y):
        index = self._get_index(x, y)
        return BaseController.get_rgba(self, index)
