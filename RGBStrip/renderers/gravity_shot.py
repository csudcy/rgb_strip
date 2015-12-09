#!/usr/bin/python
# -*- coding: utf8 -*-
import random

from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class GravityShotRenderer(BaseRenderer):
    def __init__(self, controllers, max_shots=5):
        super(GravityShotRenderer, self).__init__(controllers)

        self.MAX_SHOTS = max_shots

        self.COLOURS = utils.get_rgb_rainbow(10)
        self.SHOTS = []
        self.MIN_SPEED = 0.5
        self.MAX_SPEED = 1.0
        self.G_SPEED = self.MAX_SPEED / (self.WIDTH * 2)

    def render(self):
        # Simulate existing shots
        for shot in self.SHOTS:
            # Update position
            shot['position'] += shot['speed']
            # Update speed
            shot['speed'] -= self.G_SPEED

        # Remove old shots
        self.SHOTS = [
            shot
            for shot in self.SHOTS
            if shot['position'] > 0
        ]

        # Add a new shot?
        if len(self.SHOTS) < self.MAX_SHOTS and random.random() < 0.07:
            self.SHOTS.append({
                'colour': random.choice(self.COLOURS),
                'speed': random.uniform(self.MIN_SPEED, self.MAX_SPEED),
                'position': 0.0
            })

        # Show all the shots
        for controller in self.CONTROLLERS:
            for shot in self.SHOTS:
                controller.add_led_xy(
                    int(shot['position']),
                    1,
                    *shot['colour'],
                    a=1
                )
