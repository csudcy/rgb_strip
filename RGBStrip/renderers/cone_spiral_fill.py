#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleRenderer


class ConeSpiralFillRenderer(BaseSingleRenderer):

    def __init__(
            self,
            loader,
            section=None,
            palette=None,
            active=True,
            advance_per_step=0.2,
            reverse=False
        ):
        super(ConeSpiralFillRenderer, self).__init__(loader, section=section, palette=palette, active=active)
        self.ADVANCE_PER_STEP = advance_per_step
        self.REVERSE = reverse
        self.INDEX = 0

        self.LEVEL_SUM = sum(self.SECTION.LEVELS)

    def do_render(self):
        for index in xrange(int(self.INDEX)):
            colour = self.PALETTE[index % len(self.PALETTE)]

            if self.REVERSE:
                index = self.LEVEL_SUM - index - 1

            # Always using level 0 allows us to directly index pixels
            self.SECTION.set_led_by_level_index(index, 0, colour)

        # Move to the next index
        self.INDEX = (self.INDEX + self.ADVANCE_PER_STEP) % self.LEVEL_SUM
