#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import annotations

import collections
import math
import random
from dataclasses import dataclass
from typing import Deque, List, Optional

from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleTimedRenderer
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
  colour: Optional[List[float]] = None
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

  def update_colour(self):
    try:
      self.colour = self.stage_steps.pop()
    except IndexError:
      # No more steps; start again
      self.randomise()
      self.colour = self.stage_steps.pop()

  def do_render(self):
    self.section.set_led(self.x, self.y, self.colour)


class SparklesRenderer(BaseSingleTimedRenderer):

  def __init__(
      self,
      loader,
      name=None,
      interval_seconds=0.1,
      section=None,
      palette=None,
      active=True,
      # Custom
      coverage: int = 20,  # Percentage of lights which should be sparkling
      fade_steps: List[int] = (5, 20),  # Range of steps to fade for
      on_steps: List[int] = (3, 10),  # Range of steps to stay on
      off_steps: List[int] = (1, 3),  # Range of steps to stay off
  ):
    super().__init__(loader,
                     name=name,
                     interval_seconds=interval_seconds,
                     section=section,
                     palette=palette,
                     active=active)

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
    # Setup the first colours of the sparkles
    self.do_render_step()

  def do_render_display(self):
    for sparkle in self.SPARKLES:
      sparkle.do_render()

  def do_render_step(self):
    for sparkle in self.SPARKLES:
      sparkle.update_colour()
