#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import random
import time
from threading import Thread
from typing import List, Tuple

import PIL
from luma.core.device import device as LumaDevice
from PIL import Image

NamedImageType = Tuple[str, Image.Image]


class GifDisplayBase(Thread):

  def __init__(
      self,
      width: int,
      height: int,
      alpha: int,
      delay: int,
      directory: str,
  ):
    super().__init__()
    self.width = width
    self.height = height
    self.device = self._get_device(width, height)
    self.device.contrast(alpha)

    self.delay_seconds = delay / 1000.0
    self.images = self._get_images(directory)

  def _get_device(self, width: int, height: int):
    raise Exception('Must be overridden!')

  def _get_images(self, directory: str) -> List[NamedImageType]:
    images: List[NamedImageType] = []
    for filename in os.listdir(directory):
      filepath = os.path.join(directory, filename)

      # Check it's an image
      print(f'Checking {filename}...')
      try:
        image = Image.open(filepath)
      except PIL.UnidentifiedImageError:
        print('  Skipped: Not an image')
        continue

      if not hasattr(image, 'n_frames'):
        print('  Skipped: Must be multiple frames')
        continue

      print('  Good!')
      images.append((filename, image))

    if not images:
      raise Exception('No files found!')

    return images

  def run(self):
    while True:
      name, image = random.choice(self.images)

      for frame_index in range(image.n_frames):
        image.seek(frame_index)
        resized = image.resize((self.width, self.height))
        converted = resized.convert('RGB')
        self.device.display(converted)
        print(f'{name} : {frame_index} / {image.n_frames}...')
        time.sleep(self.delay_seconds)


class GifDisplayEmulator(GifDisplayBase):

  def _get_device(self, width: int, height: int):
    from luma.emulator.device import asciiblock
    return asciiblock(width=width, height=height)


class GifDisplayLeds(GifDisplayBase):

  def _get_device(self, width: int, height: int):
    from luma.led_matrix.device import ws2812
    return ws2812(width=width, height=height)
