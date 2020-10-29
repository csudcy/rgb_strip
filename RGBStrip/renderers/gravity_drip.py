#!/usr/bin/python
# -*- coding: utf8 -*-
import random

from RGBStrip.renderers.gravity import GravityRenderer


class GravityDripRenderer(GravityRenderer):

  def _add_new_shot(self):
    # Add a new shot
    self.SHOTS.append({
        'colour': random.choice(self.PALETTE),
        'speed': -random.uniform(0, self.MIN_SPEED),
        'position': self.SECTION.WIDTH - 1
    })
