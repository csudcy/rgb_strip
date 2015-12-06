#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime

from .base import BaseRenderer


class ClockRenderer(BaseRenderer):
    def __init__(self):
        super(ClockRenderer, self).__init__(60, 1)

    def render(self):
        now = datetime.now()
        for output in self.OUTPUTS:
            output.RGB_STRIP.add_led_xy(output.X + now.hour, output.Y, r=255, a=1)
            output.RGB_STRIP.add_led_xy(output.X + now.minute, output.Y, g=255, a=1)
            output.RGB_STRIP.add_led_xy(output.X + now.second, output.Y, b=255, a=1)
