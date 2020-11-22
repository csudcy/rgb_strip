#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseSingleRenderer


class ConeSpinFullRenderer(BaseSingleRenderer):

  def __init__(self, loader,name=None, section=None, palette=None, active=True):
    super().__init__(
        loader, name=name, section=section, palette=palette, active=active)
    self.COLOUR_INDEX = 0
    self.PALETTE_LENGTH = len(self.PALETTE)

  def do_render(self):
    for level_index, level_count in enumerate(self.SECTION.LEVELS):
      colour_step = self.PALETTE_LENGTH / float(level_count)
      for level_led in range(level_count):
        colour_index = int(self.COLOUR_INDEX + level_led * colour_step)
        colour = self.PALETTE[colour_index % self.PALETTE_LENGTH]
        self.SECTION.set_led_by_level_index(level_led, level_index, colour)

    # Move to the next angle/colour
    self.COLOUR_INDEX = (self.COLOUR_INDEX + 1) % self.PALETTE_LENGTH
