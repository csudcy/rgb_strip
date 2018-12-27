#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseSingleTimedRenderer


class ConeSpiralDripRenderer(BaseSingleTimedRenderer):

    def __init__(
            self,
            loader,
            interval_seconds=1,
            section=None,
            palette=None,
            active=True,
            # Custom
            led_interval=3,
            reverse_colour=False
        ):
        super(ConeSpiralDripRenderer, self).__init__(
            loader, interval_seconds=interval_seconds, section=section, palette=palette, active=active)
        self.REVERSE_COLOUR = reverse_colour
        self.LED_INTERVAL = led_interval
        self.INDEX = 0

        self.LEVEL_SUM = sum(self.SECTION.LEVELS)

    def do_render_display(self):
        for index in xrange(self.INDEX, self.LEVEL_SUM, self.LED_INTERVAL):
            # Work out the colour
            colour_index = index
            if self.REVERSE_COLOUR:
                colour_index = self.LEVEL_SUM - colour_index - 1
            colour = self.PALETTE[colour_index % len(self.PALETTE)]

            # Always using level 0 allows us to directly index pixels
            self.SECTION.set_led_by_level_index(index, 0, colour)

    def do_render_step(self):
        # Move to the next index
        self.INDEX = (self.INDEX + 1) % self.LED_INTERVAL
