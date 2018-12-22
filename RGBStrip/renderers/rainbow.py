#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class RainbowRenderer(BaseRenderer):
    def __init__(
            self,
            sections,
            palette,
            active=True,
            initial_x=0,
            initial_y=0
        ):
        super(RainbowRenderer, self).__init__(sections, palette, active=active)

        self.X = initial_x
        self.Y = initial_y

    def do_render(self):
        for section in self.SECTIONS:
            # Output the colours
            x, y = self.X, self.Y
            for i, colour in enumerate(self.PALETTE):
                x, y = section.increment_xy(x, y)
                section.add_led(x, y, *colour, a=1)

        # Move the train along
        self.X, self.Y = self.SECTIONS[0].increment_xy(self.X, self.Y)
