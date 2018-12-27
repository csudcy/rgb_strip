#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseSingleTimedRenderer


class ConeSpiralFillRenderer(BaseSingleTimedRenderer):

    def __init__(
            self,
            loader,
            interval_seconds=0.2,
            section=None,
            palette=None,
            active=True,
            # Custom
            reverse=False,
            reverse_colour=False
        ):
        super(ConeSpiralFillRenderer, self).__init__(
            loader, interval_seconds=interval_seconds, section=section, palette=palette, active=active)
        self.REVERSE = reverse
        self.REVERSE_COLOUR = reverse_colour
        self.INDEX = 0

        self.LEVEL_SUM = sum(self.SECTION.LEVELS)

    def do_render_display(self):
        for index in xrange(int(self.INDEX) + 1):
            # Work out the colour
            colour_index = index
            if self.REVERSE_COLOUR:
                colour_index = self.LEVEL_SUM - colour_index - 1
            colour = self.PALETTE[colour_index % len(self.PALETTE)]

            # Work out the LED index
            if self.REVERSE:
                index = self.LEVEL_SUM - index - 1

            # Always using level 0 allows us to directly index pixels
            self.SECTION.set_led_by_level_index(index, 0, colour)

    def do_render_step(self):
        # Move to the next index
        self.INDEX = (self.INDEX + 1) % self.LEVEL_SUM
