#!/usr/bin/python
# -*- coding: utf8 -*-
import random

from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class GravityRenderer(BaseRenderer):
    def __init__(
            self,
            sections,
            palettes,
            palette=None,
            active=True,
            max_shots=5,
            shot_add_chance=0.07,
            min_speed=0.5,
            max_speed=1.0,
            g_speed=None
        ):
        super(GravityRenderer, self).__init__(sections, palettes, active=active)

        self.MAX_SHOTS = max_shots
        self.SHOT_ADD_CHANCE = shot_add_chance
        self.MIN_SPEED = min_speed
        self.MAX_SPEED = max_speed
        if g_speed is None:
            g_speed = self.MAX_SPEED / (self.WIDTH * 2)
        self.G_SPEED = g_speed

        if palette is None:
            self.PALETTE = utils.get_rgb_rainbow(10)
        else:
            self.PALETTE = palettes[palette]
        self.SHOTS = []

    def _simulate_shots(self):
        # Simulate existing shots
        for shot in self.SHOTS:
            # Update position
            shot['position'] += shot['speed']
            # Update speed
            shot['speed'] -= self.G_SPEED

    def _remove_old_shots(self):
        # Remove old shots
        self.SHOTS = [
            shot
            for shot in self.SHOTS
            if shot['position'] > 0
        ]

    def _add_new_shot(self):
        # Add a new shot
        raise Exception('_add_new_shot must be implemented!')

    def _render_shots(self):
        # Show all the shots
        for section in self.SECTIONS:
            for shot in self.SHOTS:
                section.add_led_xy(
                    int(shot['position']),
                    1,
                    *shot['colour'],
                    a=1
                )

    def do_render(self):
        self._simulate_shots()
        self._remove_old_shots()
        if len(self.SHOTS) < self.MAX_SHOTS and random.random() < self.SHOT_ADD_CHANCE:
            self._add_new_shot()
        self._render_shots()
