#!/usr/bin/python
# -*- coding: utf8 -*-
from typing import List, Optional

from luma.core.device import device as LumaDevice
from luma.emulator.device import asciiblock
from luma.led_matrix.device import ws2812
from PIL import Image

import led_mapping


class ImageDevice:

  def __init__(
      self,
      width: int,
      height: int,
      alpha: int,
      rotate: int = 0,
      flip_x: bool = False,
      flip_y: bool = False,
  ):
    self.width = width
    self.height = height
    self.alpha = alpha
    self.rotate = rotate
    self.flip_x = flip_x
    self.flip_y = flip_y
    self.device = self._get_device()

  def _get_device(self) -> Optional[LumaDevice]:
    return None

  def display(self, image: Image.Image) -> None:
    if self.device:
      self.device.display(image)


class ImageDeviceLumaBase(ImageDevice):

  LUMA_CLASS = None

  def _get_device(self, **kwargs) -> LumaDevice:
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


class ImageDeviceTerminal(ImageDeviceLumaBase):

  LUMA_CLASS = asciiblock


class ImageDeviceWS2812(ImageDeviceLumaBase):

  LUMA_CLASS = ws2812

  def _get_device(self) -> LumaDevice:
    mapping = led_mapping.make_snake(self.width, self.height, self.flip_x,
                                     self.flip_y)
    return super()._get_device(mapping=mapping)


class ImageDeviceWS2812Boards(ImageDeviceLumaBase):

  LUMA_CLASS = ws2812
  BOARD_WIDTH = 32
  BOARD_HEIGHT = 8
  BOARD_LED_COUNT = BOARD_WIDTH * BOARD_HEIGHT

  def _get_device(self) -> LumaDevice:
    if self.flip_x or self.flip_y:
      raise Exception('TODO: Implement flip with WS2812 boards!')
    if self.width % self.BOARD_WIDTH != 0:
      raise Exception(f'Width ({self.width}) must be a multiple of board width'
                      f' ({self.BOARD_WIDTH})!')
    if self.height % self.BOARD_HEIGHT != 0:
      raise Exception(
          f'Height ({self.height}) must be a multiple of board height'
          f' ({self.BOARD_HEIGHT})!')

    boards_wide = int(self.width / self.BOARD_WIDTH)
    boards_high = int(self.height / self.BOARD_HEIGHT)

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
            if col % 2 == 0:  # Even
              offset = (self.BOARD_HEIGHT * col) + row
            else:  # Odd
              offset = (self.BOARD_HEIGHT * (col + 1)) - (1 + row)

            mapping.append(board_offset + offset)

    return mapping
