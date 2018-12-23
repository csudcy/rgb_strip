#!/usr/bin/python
# -*- coding: utf8 -*-

from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class ConeSpinFullRenderer(BaseRenderer):

    def __init__(
            self,
            section,
            palette,
            active=True
        ):
        super(ConeSpinFullRenderer, self).__init__(section, palette, active=active)
        self.COLOUR_INDEX = 0
        self.PALETTE_LENGTH = len(self.PALETTE)

    def do_render(self):
        for level_index, level_count in enumerate(self.SECTION.LEVELS):
            level_angle = 360.0 / float(level_count)
            colour_step = self.PALETTE_LENGTH / float(level_count)
            for level_led in xrange(level_count):
                colour_index = int(self.COLOUR_INDEX + level_led * colour_step)
                colour = self.PALETTE[colour_index % self.PALETTE_LENGTH]
                self.SECTION.set_led(level_led * level_angle, level_index, *colour)

        # Move to the next angle/colour
        self.COLOUR_INDEX = (self.COLOUR_INDEX + 1) % self.PALETTE_LENGTH
