#!/usr/bin/python
# -*- coding: utf8 -*-

from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class ConeSpinRenderer(BaseRenderer):

    def __init__(
            self,
            section,
            palette,
            active=True,
            degrees_per_step=2
        ):
        super(ConeSpinRenderer, self).__init__(section, palette, active=active)
        self.DEGREES_PER_STEP = degrees_per_step
        self.CURRENT_ANGLE = 0
        self.COLOUR_INDEX = 0

    def do_render(self):
        colour = self.PALETTE[self.COLOUR_INDEX]
        for level_index in xrange(len(self.SECTION.LEVELS)):
            self.SECTION.set_led(self.CURRENT_ANGLE, level_index, *colour)

        # Move to the next angle/colour
        self.CURRENT_ANGLE = (360 + self.CURRENT_ANGLE + self.DEGREES_PER_STEP) % 360
        self.COLOUR_INDEX = (self.COLOUR_INDEX + 1) % len(self.PALETTE)
