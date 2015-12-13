#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class RainbowRenderer(BaseRenderer):
    def __init__(
            self,
            controllers,
            active=True,
            train_length=10,
            max_rgb=127,
            initial_x=0,
            initial_y=0
        ):
        super(RainbowRenderer, self).__init__(controllers, active=active)

        self.COLOURS = utils.get_rgb_rainbow(train_length, max_rgb=max_rgb)
        self.X = initial_x
        self.Y = initial_y

    def do_render(self):
        for controller in self.CONTROLLERS:
            # Output the colours
            x, y = self.X, self.Y
            for i, colour in enumerate(self.COLOURS):
                x, y = utils.xy_inc(x, y, self.WIDTH, self.HEIGHT)
                controller.add_led_xy(x, y, *colour, a=1)

        # Move the train along
        self.X, self.Y = utils.xy_inc(self.X, self.Y, self.WIDTH, self.HEIGHT)
