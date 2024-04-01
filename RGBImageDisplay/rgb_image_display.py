#!/usr/bin/python
# -*- coding: utf8 -*-
from dataclasses import dataclass
import logging
import pathlib
import random
from threading import Thread
import time
from typing import Any, Dict, Optional, TypeVar

import devices
import PIL
from PIL import Image

LOGGER = logging.getLogger(__name__)


@dataclass
class ImageInfo:
  parent: str
  name: str
  filepath: pathlib.Path
  n_frames: int


@dataclass
class ImageGroup:
  name: str
  images: Dict[str, ImageInfo]


@dataclass
class FrameInfo:
  image_info: ImageInfo
  frame_index: int
  image: Image.Image


T = TypeVar('T')


def random_dict_choice(d: Dict[Any, T]) -> T:
  return random.choice(list(d.values()))


class ImageDisplay(Thread):
  device: devices.ImageDevice
  delay_seconds: float
  image_groups: Dict[str, ImageGroup]
  image_bytes: bytes
  frame_info: FrameInfo
  _move_next: bool = False
  _next_image_info: Optional[ImageInfo] = None

  def __init__(
      self,
      *,
      device: devices.ImageDevice,
      delay: int,
      directory: pathlib.Path,
  ):
    super().__init__()
    self.device = device
    self.delay_seconds = delay / 1000.0
    self.image_groups = self._get_image_groups(directory)

  def _get_image_groups(self, directory: pathlib.Path) -> Dict[str, ImageGroup]:
    LOGGER.info(f'Loading groups {directory}...')
    image_groups: Dict[str, ImageGroup] = {}
    for group_directory in directory.iterdir():
      if not group_directory.is_dir():
        LOGGER.info(f'  Skipping non-directory {group_directory}')
        continue

      image_groups[group_directory.name] = ImageGroup(
          group_directory.name, self._get_image_infos(group_directory))

    if not image_groups:
      raise Exception(f'No groups found in {directory}!')

    return image_groups

  def _get_image_infos(self, directory: pathlib.Path) -> Dict[str, ImageInfo]:
    LOGGER.info(f'Loading images {directory}...')
    image_infos: Dict[str, ImageInfo] = {}
    for filename in directory.iterdir():
      filepath = directory.joinpath(filename)

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
      image_infos[filename.stem] = ImageInfo(
          parent=directory.name,
          name=filename.stem,
          filepath=filepath,
          n_frames=image.n_frames,
      )

    if not image_infos:
      raise Exception(f'No files found in {directory}!')

    return image_infos

  def run(self):
    while True:
      if self._next_image_info:
        LOGGER.info(f'Using next image_info...')
        image_info = self._next_image_info
        self._next_image_info = None
      else:
        LOGGER.info(f'Using random image_info...')
        image_group = random_dict_choice(self.image_groups)
        image_info = random_dict_choice(image_group.images)

      LOGGER.info(
          f'{image_info.parent}:{image_info.name} ({image_info.n_frames} frames)'
      )

      try:
        self.show_image(image_info)
      except Exception as ex:
        LOGGER.exception('Error while showing image! Continuing...')

  def show_image(self, image_info: ImageInfo):
    self._move_next = False
    image = Image.open(image_info.filepath)
    for frame_index in range(image_info.n_frames):
      if self._move_next:
        LOGGER.info(f'Moving to next image...')
        break
      LOGGER.debug(f'Seeking frame {frame_index}...')
      image.seek(frame_index)
      current_image = image.copy()

      if current_image.size != (self.device.width, self.device.height):
        LOGGER.debug('Resizing...')
        current_image = current_image.resize(
            (self.device.width, self.device.height))
      if current_image.mode != 'RGB':
        LOGGER.debug('Converting...')
        current_image = current_image.convert('RGB')

      # Dump a PNG of the image & current frame info
      LOGGER.debug('Dumping...')
      self.frame_info = FrameInfo(
          image_info=image_info,
          frame_index=frame_index,
          image=current_image,
      )

      LOGGER.debug('Displaying...')
      self.device.display(current_image)
      LOGGER.debug('Waiting...')
      time.sleep(self.delay_seconds)

  def next(self) -> None:
    self._move_next = True

  def play(self, group_name: str, image_name: str) -> None:
    image_group = self.image_groups[group_name]
    image_info = image_group.images[image_name]
    self._next_image_info = image_info
    self._move_next = True
