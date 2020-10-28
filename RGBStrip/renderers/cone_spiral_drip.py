#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseSingleTimedRenderer


class ConeSpiralDripRenderer(BaseSingleTimedRenderer):

    def __init__(
            self,
            loader,
            interval_seconds=0.1,
            section=None,
            palette=None,
            active=True,
            # Custom
            segment_length=3,
            segment_gap=5,
            reverse_colour=False
        ):
        super().__init__(
            loader, interval_seconds=interval_seconds, section=section, palette=palette, active=active)
        self.REVERSE_COLOUR = reverse_colour
        self.SEGMENT_LENGTH = segment_length
        self.SEGMENT_TOTAL = segment_gap + segment_length
        self.INDEX = 0

        self.LEVEL_SUM = sum(self.SECTION.LEVELS)

    def do_render_display(self):
        start_index = self.INDEX - self.SEGMENT_TOTAL
        for segment_index in range(start_index, self.LEVEL_SUM, self.SEGMENT_TOTAL):
            # Work out the colour
            colour_index = segment_index
            if self.REVERSE_COLOUR:
                colour_index = self.LEVEL_SUM - colour_index - 1
            colour = self.PALETTE[colour_index % len(self.PALETTE)]

            for length_index in range(self.SEGMENT_LENGTH):
                actual_index = segment_index + length_index

                if 0 <= actual_index and actual_index < self.LEVEL_SUM:
                    # Always using level 0 allows us to directly index pixels
                    self.SECTION.set_led_by_level_index(actual_index, 0, colour)

    def do_render_step(self):
        # Move to the next index
        self.INDEX = (self.INDEX + 1) % self.SEGMENT_TOTAL
