#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class RainbowRenderer(BaseRenderer):
    def __init__(
            self,
            section,
            palette,
            active=True,
            initial_x=0,
            initial_y=0
        ):
        super(RainbowRenderer, self).__init__(section, palette, active=active)

        self.X = initial_x
        self.Y = initial_y

    def do_render(self):
        # Output the colours
        x, y = self.X, self.Y
        for i, colour in enumerate(self.PALETTE):
            x, y = self.SECTION.increment_xy(x, y)
            self.SECTION.add_led(x, y, *colour, a=1)

        # Move the train along
        self.X, self.Y = self.SECTION.increment_xy(self.X, self.Y)
