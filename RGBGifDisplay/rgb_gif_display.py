#!/usr/bin/python
# -*- coding: utf8 -*-
import io
import logging
import os
import random
import time
from threading import Thread
from typing import List, Tuple

import PIL
from luma.core.device import device as LumaDevice
from luma.emulator.device import emulator
from luma.emulator.device import asciiblock
from luma.led_matrix.device import ws2812
from PIL import Image

LOGGER = logging.getLogger(__name__)

NamedImageType = Tuple[str, Image.Image]


class GifDisplayBase(Thread):

  def __init__(
      self,
      width: int,
      height: int,
      rotate: int,
      alpha: int,
      delay: int,
      directory: str,
  ):
    super().__init__()
    self.width = width
    self.height = height
    if rotate in (1, 3):
      # Display is rotated; switch width & height
      width, height = height, width
    self.device = self._get_device(width, height, rotate, alpha)

    self.delay_seconds = delay / 1000.0
    self.images = self._get_images(directory)

  def _get_device(self, width: int, height: int, rotate: int, alpha: int):
    raise Exception('Must be overridden!')

  def _get_images(self, directory: str) -> List[NamedImageType]:
    images: List[NamedImageType] = []
    for filename in os.listdir(directory):
      filepath = os.path.join(directory, filename)

      # Check it's an image
      LOGGER.info(f'Checking {filename}...')
      try:
        image = Image.open(filepath)
      except PIL.UnidentifiedImageError:
        LOGGER.info('  Skipped: Not an image')
        continue

      if not hasattr(image, 'n_frames'):
        LOGGER.info('  Skipped: Must be multiple frames')
        continue

      LOGGER.info('  Good!')
      images.append((filename, image))

    if not images:
      raise Exception('No files found!')

    return images

  def run(self):
    while True:
      name, image = random.choice(self.images)
      LOGGER.info(f'{name} ({image.n_frames} frames)')

      if random.choice((True, False)):
        frame_range = range(image.n_frames)
      else:
        frame_range = range(image.n_frames - 1, 0, -1)

      for frame_index in frame_range:
        LOGGER.debug(f'Seeking frame {frame_index}...')
        image.seek(frame_index)

        current_image = image
        if image.size != (self.width, self.height):
          LOGGER.debug('Resizing...')
          current_image = current_image.resize((self.width, self.height))
        if image.mode != 'RGB':
          LOGGER.debug('Converting...')
          current_image = current_image.convert('RGB')

        # Dump a PNG of the image
        LOGGER.debug('Dumping...')
        buffer = io.BytesIO()
        current_image.save(buffer, format='png')
        self.image_bytes = buffer.getvalue()

        if self.device:
          LOGGER.debug('Displaying...')
          self.device.display(current_image)
        LOGGER.debug('Waiting...')
        time.sleep(self.delay_seconds)


class GifDisplayTerminal(GifDisplayBase):

  def _get_device(self, width: int, height: int, rotate: int, alpha: int):
    device = asciiblock(width=width, height=height, rotate=rotate)
    device.contrast(alpha)
    return device


class GifDisplayWS2812(GifDisplayBase):

  def _get_device(self, width: int, height: int, rotate: int, alpha: int):
    device = ws2812(width=width, height=height, rotate=rotate)
    device.contrast(alpha)
    return device


class GifDisplayNone(GifDisplayBase):

  def _get_device(self, width: int, height: int, rotate: int, alpha: int):
    return None
