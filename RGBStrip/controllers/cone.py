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
            extra_leds=0,
            reverse=False,
            a=10
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
            'a': a,
            'extra_leds': extra_leds,
            'levels': levels,
            'reverse': reverse,
            'type': 'cone',
        }
        BaseController.__init__(self, config, sum(levels)+extra_leds, a)

    def _get_index(self, angle, level):
        index = int(self.LEVEL_OFFSETS[level] + angle/360.0 * self.LEVELS[level])
        if self.REVERSE:
            index = self.LED_COUNT - index - 1
        return index

    def add_led(self, angle, level, colour):
        index = self._get_index(angle, level)
        BaseController.add_led(self, index, colour)

    def set_led(self, angle, level, colour):
        index = self._get_index(angle, level)
        BaseController.set_led(self, index, colour)

    def get_rgba(self, angle, level):
        index = self._get_index(angle, level)
        return BaseController.get_rgba(self, index)
