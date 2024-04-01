#!/usr/bin/python
# -*- coding: utf8 -*-
from dataclasses import dataclass
import logging
import pathlib
import random
from threading import Thread
import time
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

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
  parent: str
  name: str
  image: Image.Image
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


class ImageDisplayBase(Thread):

  width: int
  height: int
  rotate: int
  flip_x: bool
  flip_y: bool
  alpha: int
  delay_seconds: float
  device: Any
  image_groups: Dict[str, ImageGroup]
  image_bytes: bytes
  frame_info: Dict[str, Union[int, str]]
  _move_next: bool = False
  _next_image_info: Optional[ImageInfo] = None

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
      directory: pathlib.Path,
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
    self.image_groups = self._get_image_groups(directory)

  def _get_device(self):
    raise Exception('Must be overridden!')

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
          image=image,
          n_frames=getattr(image, 'n_frames'),
      )

    if not image_infos:
      raise Exception(f'No files found in {directory}!')

    return image_infos

  def run(self):
    while True:
      if self._next_image_info:
        image_info = self._next_image_info
        self._next_image_info = None
      else:
        image_group = random_dict_choice(self.image_groups)
        image_info = random_dict_choice(image_group.images)

      LOGGER.info(f'{image_info.name} ({image_info.n_frames} frames)')

      try:
        self.show_image(image_info)
      except Exception as ex:
        LOGGER.exception('Error while showing image! Continuing...')

  def show_image(self, image_info: ImageInfo):
    self._move_next = False
    for frame_index in range(image_info.n_frames):
      if self._move_next:
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
      self.frame_info = FrameInfo(
          image_info=image_info,
          frame_index=frame_index,
          image=current_image,
      )

      if self.device:
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


class ImageDisplayWS2812Boards(ImageDisplayLumaBase):

  LUMA_CLASS = ws2812
  BOARD_WIDTH = 32
  BOARD_HEIGHT = 8
  BOARD_LED_COUNT = BOARD_WIDTH * BOARD_HEIGHT

  def _get_device(self):
    if self.flip_x or self.flip_y:
      raise Exception('TODO: Implement flip with WS2812 boards!')
    if self.width % self.BOARD_WIDTH != 0:
      raise Exception(f'Width ({self.width}) must be a multiple of board width'
                      f' ({self.BOARD_WIDTH})!')
    if self.height % self.BOARD_HEIGHT != 0:
      raise Exception(f'Height ({self.height}) must be a multiple of board height'
                      f' ({self.BOARD_HEIGHT})!')

    boards_wide = self.width / self.BOARD_WIDTH
    boards_high = self.height / self.BOARD_HEIGHT

    mapping = self._make_mapping(boards_wide, boards_high)
    return super()._get_device(mapping=mapping)

  def _make_mapping(self, boards_wide: int, boards_high: int) -> List[int]:
    mapping = []

    for board_row in range(0, boards_high):
      for row in range(0, self.BOARD_HEIGHT):
        for board_col in range(0, boards_wide):
          board_number = (board_row * boards_wide) + board_col
          board_offset = board_number * self.BOARD_LED_COUNT
          for col in range(0, self.BOARD_WIDTH):
            if col % 2 == 0: # Even
              offset = (self.BOARD_HEIGHT * col) + row
            else: # Odd
              offset = (self.BOARD_HEIGHT * (col + 1)) - (1 + row)

            mapping.append(board_offset + offset)

    return mapping


class ImageDisplayNone(ImageDisplayBase):

  def _get_device(self):
    return None
