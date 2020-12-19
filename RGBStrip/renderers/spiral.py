#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from RGBStrip.renderers.base import BaseSingleTimedRenderer



@dataclass
class SpiralConfig:
  first_dy: int
  next_dx: int
  next_dy: int


CONFIG = {
    '/': SpiralConfig(+1, -1, +1),
    '\\': SpiralConfig(-1, +1, +1),
}


class SpiralRenderer(BaseSingleTimedRenderer):

  IS_FINISHABLE = False

  def __init__(
      self,
      loader,
      name=None,
      interval_seconds=0.2,
      section=None,
      palette=None,
      active=True,
      # Custom
      direction='/',  # /, \
      reverse=False,
  ):
    super().__init__(loader,
                     name=name,
                     interval_seconds=interval_seconds,
                     section=section,
                     palette=palette,
                     active=active)
    self.Y = 0

    config = CONFIG[direction]
    if reverse:
      self.first_dy = -config.first_dy
      self.next_dx = -config.next_dx
      self.next_dy = -config.next_dy
    else:
      self.first_dy = config.first_dy
      self.next_dx = config.next_dx
      self.next_dy = config.next_dy

    self.LINE_COUNT = max(self.SECTION.WIDTH, self.SECTION.HEIGHT)
    self.PIXELS = [None] * self.LINE_COUNT
    self._fill_pixels()

  def do_render_display(self):
    for x, y, colour in self.PIXELS:
      self.SECTION.add_led(x, y, colour)

  def do_render_step(self):
    self.Y += self.first_dy
    self._fill_pixels()

  def _fill_pixels(self):
    x = 0
    y = self.Y
    for i in range(self.LINE_COUNT):
      self.PIXELS[i] = (x, y, self.PALETTE[i % len(self.PALETTE)])
      x += self.next_dx
      y += self.next_dy
