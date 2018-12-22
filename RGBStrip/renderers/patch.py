#!/usr/bin/python
# -*- coding: utf8 -*-
from .base import BaseRenderer
from RGBStrip import utils


class PatchRenderer(BaseRenderer):
    def __init__(
            self,
            sections,
            palette,
            active=True,
            a=1,
            # TODO: remove delay?
            delay=1,
            start_index=0):
        super(PatchRenderer, self).__init__(sections, palette, active=active)

        self.A = a
        self.INDEX = start_index % len(self.PALETTE)
        self.STEP_DELAYED = 0
        self.STEP_DELAY = delay

    def do_render(self):
        rgb_colour = self.PALETTE[self.INDEX]
        for section in self.SECTIONS:
            for x in xrange(self.WIDTH):
                for y in xrange(self.HEIGHT):
                    section.add_led(x, y, *rgb_colour, a=self.A)
        self.STEP_DELAYED += 1
        if self.STEP_DELAYED >= self.STEP_DELAY:
            # We have stayed on this step for STEP_DELAY frames; move to the next step
            self.STEP_DELAYED = 0
            self.INDEX = (self.INDEX + 1) % len(self.PALETTE)
