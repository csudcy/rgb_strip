#!/usr/bin/python
# -*- coding: utf8 -*-
from .base import BaseRenderer
from RGBStrip import utils


class PatchRenderer(BaseRenderer):
    def __init__(self, controllers, colours=((255, 0, 0), ), a=1, rainbow_steps=None, delay=1, start_index=0):
        super(PatchRenderer, self).__init__(controllers)

        if rainbow_steps:
            self.COLOURS = utils.get_rgb_rainbow(rainbow_steps)
        else:
            self.COLOURS = colours
        self.A = a
        self.INDEX = start_index % len(self.COLOURS)
        self.STEP_DELAYED = 0
        self.STEP_DELAY = delay

    def render(self):
        rgb_colour = self.COLOURS[self.INDEX]
        for controller in self.CONTROLLERS:
            for x in xrange(self.WIDTH):
                for y in xrange(self.HEIGHT):
                    controller.add_led_xy(x, y, *rgb_colour, a=self.A)
        self.STEP_DELAYED += 1
        if self.STEP_DELAYED >= self.STEP_DELAY:
            # We have stayed on this step for STEP_DELAY frames; move to the next step
            self.STEP_DELAYED = 0
            self.INDEX = (self.INDEX + 1) % len(self.COLOURS)
