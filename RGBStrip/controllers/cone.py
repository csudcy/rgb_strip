#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.controllers.base import BaseController


class ConeController(BaseController):
    """
    An interface to control a strip of RGB LEDs arranged in a cone.
    """

    def __init__(
            self,
            levels,
            reverse=False
        ):
        if not levels:
            raise Exception('ConeController must be given levels!')
        self.LEVELS = levels
        self.REVERSE = reverse
        level_offset = 0
        self.LEVEL_OFFSETS = [
            sum(levels[:level_index])
            for level_index in xrange(len(levels))
        ]
        config = {
            'levels': levels,
            'reverse': reverse
        }
        BaseController.__init__(self, config, sum(levels))

    def _get_index(self, angle, level):
        index = self.LEVEL_OFFSETS[level] + angle/360.0 * self.LEVELS[level]
        if self.reverse:
            index = self.LED_COUNT - index
        return index

    def add_led(self, angle, level, **colour):
        index = self._get_index(angle, level)
        self.add_led(index, **colour)

    def set_led(self, angle, level, **colour):
        index = self._get_index(angle, level)
        self.set_led(index, **colour)

    def get_rgba(self, angle, level):
        index = self._get_index(angle, level)
        return self.get_rgba(index)
