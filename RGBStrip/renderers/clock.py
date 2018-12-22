#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime

from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class ClockRenderer(BaseRenderer):

    DEFAULT_PALETTE = utils.get_rgb_rainbow(3)

    def do_render(self):
        now = datetime.now()
        for section in self.SECTIONS:
            section.add_led(now.hour, 0, *self.PALETTE[0])
            section.add_led(now.minute, 0, *self.PALETTE[1])
            section.add_led(now.second, 0, *self.PALETTE[2])
