#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseSingleTimedRenderer


class ConeSpinLineRenderer(BaseSingleTimedRenderer):

    def __init__(
            self,
            loader,
            interval_seconds=0.2,
            section=None,
            palette=None,
            active=True,
            # Custom
            start_degrees=0,
            degrees_per_step=10
        ):
        super(ConeSpinLineRenderer, self).__init__(
            loader, interval_seconds=interval_seconds, section=section, palette=palette, active=active)
        self.COLOUR_INDEX = 0
        self.CURRENT_ANGLE = start_degrees
        self.DEGREES_PER_STEP = degrees_per_step

    def do_render_display(self):
        colour = self.PALETTE[self.COLOUR_INDEX]
        for level_index in xrange(len(self.SECTION.LEVELS)):
            self.SECTION.set_led(self.CURRENT_ANGLE, level_index, colour)

        self.COLOUR_INDEX = (self.COLOUR_INDEX + 1) % len(self.PALETTE)

    def do_render_step(self):
        # Move to the next angle/colour
        self.CURRENT_ANGLE = (360 + self.CURRENT_ANGLE + self.DEGREES_PER_STEP) % 360
