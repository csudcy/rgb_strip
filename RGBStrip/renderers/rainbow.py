#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class RainbowRenderer(BaseRenderer):
    def __init__(
            self,
            sections,
            palettes,
            palette,
            active=True,
            initial_x=0,
            initial_y=0
        ):
        super(RainbowRenderer, self).__init__(sections, palettes, active=active)

        self.PALETTE = utils.resolve_palette(palettes, palette)
        self.X = initial_x
        self.Y = initial_y

    def do_render(self):
        for section in self.SECTIONS:
            # Output the colours
            x, y = self.X, self.Y
            for i, colour in enumerate(self.PALETTE):
                x, y = utils.xy_inc(x, y, self.WIDTH, self.HEIGHT)
                section.add_led_xy(x, y, *colour, a=1)

        # Move the train along
        self.X, self.Y = utils.xy_inc(self.X, self.Y, self.WIDTH, self.HEIGHT)
