#!/usr/bin/python
# -*- coding: utf8 -*-
import random

from RGBStrip.renderers.gravity import GravityRenderer


class GravityShotRenderer(GravityRenderer):

    def _add_new_shot(self):
        # Add a new shot
        self.SHOTS.append({
            'colour': random.choice(self.PALETTE),
            'speed': random.uniform(self.MIN_SPEED, self.MAX_SPEED),
            'position': 0.0
        })
