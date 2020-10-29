#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleRenderer


class PatchRenderer(BaseSingleRenderer):

  def __init__(
      self,
      loader,
      section=None,
      palette=None,
      active=True,
      # TODO: remove delay?
      delay=1,
      start_index=0):
    super().__init__(loader, section=section, palette=palette, active=active)

    self.INDEX = start_index % len(self.PALETTE)
    self.STEP_DELAYED = 0
    self.STEP_DELAY = delay

  def do_render(self):
    rgb_colour = self.PALETTE[self.INDEX]
    for x in range(self.SECTION.WIDTH):
      for y in range(self.SECTION.HEIGHT):
        self.SECTION.add_led(x, y, rgb_colour)
    self.STEP_DELAYED += 1
    if self.STEP_DELAYED >= self.STEP_DELAY:
      # We have stayed on this step for STEP_DELAY frames; move to the next step
      self.STEP_DELAYED = 0
      self.INDEX = (self.INDEX + 1) % len(self.PALETTE)
