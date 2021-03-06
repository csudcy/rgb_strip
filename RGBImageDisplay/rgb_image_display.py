#!/usr/bin/python
# -*- coding: utf8 -*-
from dataclasses import dataclass
import io
import itertools
import logging
import os
import random
from threading import Thread
import time
from typing import Any, Dict, List, Tuple

from luma.core.device import device as LumaDevice
from luma.emulator.device import asciiblock
from luma.emulator.device import emulator
from luma.led_matrix.device import ws2812
import PIL
from PIL import Image

import led_mapping

LOGGER = logging.getLogger(__name__)

NamedImageType = Tuple[str, Image.Image]


@dataclass
class ImageInfo:
  name: str
  image: Image.Image

  # Not set at init
  prefix: str = ''

  def __post_init__(self):
    self.prefix = self.name.split('_')[0]


@dataclass
class ImageGroup:
  name: str
  images: List[ImageInfo]

  def get_random(self) -> ImageInfo:
    return random.choice(self.images)


class ImageDisplayBase(Thread):

  width: int
  height: int
  rotate: int
  flip_x: bool
  flip_y: bool
  alpha: int
  delay_seconds: int
  device: Any
  image_groups: List[ImageGroup]
  image_bytes: bytes
  frame_info: Dict[str, str]
  move_next: bool

  def __init__(
      self,
      *,
      width: int,
      height: int,
      rotate: int,
      flip_x: bool,
      flip_y: bool,
      alpha: int,
      delay: int,
      directory: str,
  ):
    super().__init__()
    self.width = width
    self.height = height
    self.rotate = rotate
    self.flip_x = flip_x
    self.flip_y = flip_y
    self.alpha = alpha
    self.delay_seconds = delay / 1000.0
    self.device = self._get_device()
    image_infos = self._get_image_infos(directory)
    self.image_groups = self._group_images(image_infos)

  def _get_device(self):
    raise Exception('Must be overridden!')

  def _get_image_infos(self, directory: str) -> List[ImageInfo]:
    image_infos: List[ImageInfo] = []
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
      image_infos.append(ImageInfo(filename.split('.')[0], image))

    if not image_infos:
      raise Exception('No files found!')

    return image_infos

  def _group_images(self, image_infos: List[ImageInfo]) -> List[ImageGroup]:
    image_infos.sort(key=lambda ii: ii.name)
    groups: List[ImageGroup] = []
    for key, group in itertools.groupby(image_infos, lambda ii: ii.prefix):
      groups.append(ImageGroup(key, list(group)))
    return groups

  def run(self):
    while True:
      image_group = random.choice(self.image_groups)
      image_info = image_group.get_random()
      LOGGER.info(f'{image_info.name} ({image_info.image.n_frames} frames)')

      try:
        self.show_image(image_info)
      except Exception as ex:
        LOGGER.exception('Error while showing image! Continuing...')

  def show_image(self, image_info: ImageInfo):
    self.move_next = False
    for frame_index in range(image_info.image.n_frames):
      if self.move_next:
        LOGGER.debug(f'Moving to next image...')
        break
      LOGGER.debug(f'Seeking frame {frame_index}...')
      image_info.image.seek(frame_index)
      current_image = image_info.image

      if current_image.size != (self.width, self.height):
        LOGGER.debug('Resizing...')
        current_image = current_image.resize((self.width, self.height))
      if current_image.mode != 'RGB':
        LOGGER.debug('Converting...')
        current_image = current_image.convert('RGB')

      # Dump a PNG of the image & current frame info
      LOGGER.debug('Dumping...')
      buffer = io.BytesIO()
      current_image.save(buffer, format='png')
      self.image_bytes = buffer.getvalue()
      self.frame_info = {
          'name': image_info.name,
          'frames': image_info.image.n_frames,
          'frame_index': frame_index,
      }

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
    mapping = led_mapping.make_snake(self.width, self.height, self.flip_x,
                                     self.flip_y)
    return super()._get_device(mapping=mapping)


class ImageDisplayNone(ImageDisplayBase):

  def _get_device(self):
    return None
