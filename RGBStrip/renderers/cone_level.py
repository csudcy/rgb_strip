#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseSingleTimedRenderer


class ConeLevelRenderer(BaseSingleTimedRenderer):

    def __init__(
            self,
            loader,
            interval_seconds=0.1,
            section=None,
            palette=None,
            active=True
        ):
        super().__init__(
            loader, interval_seconds=interval_seconds, section=section, palette=palette, active=active)
        self.COLOUR_INDEX = 0

    def do_render_display(self):
        for level_index, level_count in enumerate(self.SECTION.LEVELS):
            colour_index = (self.COLOUR_INDEX + level_index) % len(self.PALETTE)
            colour = self.PALETTE[colour_index]
            for index in range(level_count):
                self.SECTION.set_led_by_level_index(index, level_index, colour)

    def do_render_step(self):
        # Move to the next angle/colour
        self.COLOUR_INDEX = (self.COLOUR_INDEX + 1) % len(self.PALETTE)
