#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime

from .base import BaseRenderer


class ClockRenderer(BaseRenderer):
    def render(self):
        now = datetime.now()
        for controller in self.CONTROLLERS:
            controller.add_led_xy(now.hour, 0, r=255, a=1)
            controller.add_led_xy(now.minute, 0, g=255, a=1)
            controller.add_led_xy(now.second, 0, b=255, a=1)
