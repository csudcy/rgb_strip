#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import annotations

import collections
import math
import random
from dataclasses import dataclass
from enum import Enum
from typing import Deque, List

from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleRenderer
from RGBStrip.sections.rectangular import RectangularSection


@dataclass
class Sparkle:
  section: RectangularSection
  palette: List[List[float]]
  fade_steps: List[int]
  on_steps: List[int]
  off_steps: List[int]

  # Not set at init
  x: int = 0
  y: int = 0
  stage_steps: Deque[List[float]] = collections.deque()

  def randomise(self):
    self.x = random.randint(0, self.section.WIDTH)
    self.y = random.randint(0, self.section.HEIGHT)
    self.stage_steps = collections.deque(
        utils.fade_in_out(
            [random.choice(self.palette)],
            random.randint(*self.fade_steps),
            random.randint(*self.fade_steps),
            random.randint(*self.on_steps),
            random.randint(*self.off_steps),
        ))

  def do_render(self):
    try:
      colour = self.stage_steps.pop()
    except IndexError:
      # No more steps; start again
      self.randomise()
      colour = self.stage_steps.pop()

    self.section.set_led(self.x, self.y, colour)


class SparklesRenderer(BaseSingleRenderer):

  def __init__(
      self,
      loader,
      section=None,
      palette=None,
      active=True,
      # Custom
      coverage: int = 20,  # Percentage of lights which should be sparkling
      fade_steps: List[int] = (50, 200),  # Range of steps to fade for
      on_steps: List[int] = (30, 100),  # Range of steps to stay on
      off_steps: List[int] = (5, 25),  # Range of steps to stay off
  ):
    super().__init__(loader, section=section, palette=palette, active=active)

    # Create all the sparkles
    leds_total = self.SECTION.WIDTH * self.SECTION.HEIGHT
    leds_on = int(coverage * leds_total / 100)
    self.SPARKLES = [
        Sparkle(
            section=self.SECTION,
            palette=self.PALETTE,
            fade_steps=fade_steps,
            on_steps=on_steps,
            off_steps=off_steps,
        ) for _ in range(leds_on)
    ]

  def do_render(self):
    for sparkle in self.SPARKLES:
      sparkle.do_render()
