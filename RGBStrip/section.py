#!/usr/bin/python
# -*- coding: utf8 -*-
from collections import namedtuple
from datetime import datetime
import math
import random
import time

import RPi.GPIO as GPIO

from gpio_22 import GPIO22
from lcd import LCD


StripSection = namedtuple('StripSection', ('ID', 'RGB_STRIP', 'X', 'Y'))

class StripSection(object):
    """
    Allow a section of and RGBStrip to be controlled
    """
    def __init__(self, controller, x, y, width, height):
        self.controller = controller
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        ax, ay = self._get_absolute_xy(x, y)
        self.set_led_xy(ax, ay, r=r, g=g, b=b, a=a)

    def add_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        ax, ay = self._get_absolute_xy(x, y)
        self.add_led_xy(ax, ay, r=r, g=g, b=b, a=a)

    def _get_absolute_xy(self, x, y):
        x = x % self.width
        y = y % self.width
        return self.x + x, self.y + y
