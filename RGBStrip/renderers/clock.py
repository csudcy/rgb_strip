#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime

from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleRenderer


class ClockRenderer(BaseSingleRenderer):

  DEFAULT_PALETTE = utils.get_rgb_rainbow(3)

  def do_render(self):
    now = datetime.now()
    self.SECTION.add_led(now.hour, 0, self.PALETTE[0])
    self.SECTION.add_led(now.minute, 0, self.PALETTE[1])
    self.SECTION.add_led(now.second, 0, self.PALETTE[2])
