#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleTimedRenderer


class PatchRenderer(BaseSingleTimedRenderer):

  def __init__(
      self,
      loader,
      name=None,
      section=None,
      palette=None,
      active=True,
  ):
    super().__init__(loader,
                     name=name,
                     section=section,
                     palette=palette,
                     active=active)
    self.INDEX = 0

  def do_render_display(self):
    rgb_colour = self.PALETTE[self.INDEX]
    for x in range(self.SECTION.WIDTH):
      for y in range(self.SECTION.HEIGHT):
        self.SECTION.add_led(x, y, rgb_colour)

  def do_render_step(self):
      self.INDEX = (self.INDEX + 1) % len(self.PALETTE)
