#!/usr/bin/python
# -*- coding: utf8 -*-
from .base import BaseRenderer


class PatchRenderer(BaseRenderer):
    def __init__(self, controllers, rgb_colours=((255, 0, 0), ), a=1):
        super(PatchRenderer, self).__init__(controllers)

        self.RGB_COLOURS = rgb_colours
        self.A = a
        self.INDEX = 0

    def render(self):
        rgb_colour = self.RGB_COLOURS[self.INDEX]
        for controller in self.CONTROLLERS:
            for x in xrange(self.WIDTH):
                for y in xrange(self.HEIGHT):
                    controller.add_led_xy(x, y, *rgb_colour, a=self.A)
        self.INDEX = (self.INDEX + 1) % len(self.RGB_COLOURS)
