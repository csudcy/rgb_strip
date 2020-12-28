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
from luma.emulator.device import asciiblock, emulator
from luma.led_matrix.device import ws2812
from PIL import Image

LOGGER = logging.getLogger(__name__)

NamedImageType = Tuple[str, Image.Image]


class ImageDisplayBase(Thread):

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
    self.rotate = rotate
    self.alpha = alpha
    self.delay_seconds = delay / 1000.0
    self.device = self._get_device()
    self.images = self._get_images(directory)

  def _make_mapping(self):
    """
    Given LEDs arranged like this:
      0  7  8
      1  6  9
      2  5  10
      3  4  11

    Map them to positions expected like this:
      0  1  2
      3  4  5
      6  7  8
      9  10 11

    Return an array like this:
      [0, 7, 8, 1, 6, 9, 2, 5, 10, 3, 4, 11]
    """
    # TODO: Take self.rotate into account
    mapping = []
    for y in range(self.height):
      for x in range(self.width):
        if x % 2 == 0:
          index = x * self.height + y
        else:
          index = x * self.height + (self.height - y - 1)
        mapping.append(index)
    return mapping

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

      for frame_index in range(image.n_frames):
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


class ImageDisplayLumaBase(ImageDisplayBase):

  LUMA_CLASS = None

  def _get_device(self, **kwargs):
    if self.rotate in (1, 3):
      # Display is rotated; switch width & height
      width, height = self.height, self.width
    else:
      width, height = self.width, self.height
    device = self.LUMA_CLASS(width=width,
                             height=height,
                             rotate=self.rotate,
                             **kwargs)
    device.contrast(self.alpha)
    return device


class ImageDisplayTerminal(ImageDisplayLumaBase):

  LUMA_CLASS = asciiblock


class ImageDisplayWS2812(ImageDisplayLumaBase):

  LUMA_CLASS = ws2812

  def _get_device(self):
    mapping = self._make_mapping()
    return super()._get_device(mapping=mapping)


class ImageDisplayNone(ImageDisplayBase):

  def _get_device(self):
    return None
