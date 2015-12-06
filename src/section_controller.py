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
