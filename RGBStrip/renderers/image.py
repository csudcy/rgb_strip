#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import annotations

import random

from PIL import Image

from RGBStrip.renderers.base import BaseSingleTimedRenderer


class ImageRenderer(BaseSingleTimedRenderer):

  FINISHABLE = True
  # TODO: Make renderers work without specifying a palette
  DEFAULT_PALETTE = 'red'

  def __init__(
      self,
      loader,
      name=None,
      interval_seconds=0.1,
      section=None,
      palette=None,
      active=True,
      # Custom
      image: str = None,  # Image to load & show
  ):
    super().__init__(loader,
                     name=name,
                     interval_seconds=interval_seconds,
                     section=section,
                     palette=palette,
                     active=active)

    if not image:
      raise Exception('No image provided!')

    # Load the image
    self.image = Image.open(image)
    self.frame_index = 0
    self.FINISHED = False

  def is_finished(self):
    """Check if this display is in a "finished" state.
    """
    return self.FINISHED

  def do_render_display(self):
    self.image.seek(self.frame_index)
    resized = self.image.resize((self.SECTION.WIDTH, self.SECTION.HEIGHT))
    converted = resized.convert('RGB')
    for x in range(self.SECTION.WIDTH):
      for y in range(self.SECTION.HEIGHT):
        pixel = converted.getpixel((x, y))
        self.SECTION.set_led(x, y, pixel)

  def do_render_step(self):
    self.frame_index += 1
    if self.frame_index >= self.image.n_frames:
      self.frame_index = 0
      self.FINISHED = True
