#!/usr/bin/python
# -*- coding: utf8 -*-
from typing import List

from RGBStrip.controllers.base import BaseController

BOARD_WIDTH = 32
BOARD_HEIGHT = 8
BOARD_LED_COUNT = BOARD_WIDTH * BOARD_HEIGHT


class BoardsController(BaseController):
  """An interface to control a strip of RGB LEDs arranged in a rectangle.
  """

  def __init__(self, boards_wide: int, boards_high: int, a=10):
    self.boards_wide = boards_wide
    self.boards_high = boards_high
    self._mapping = self._make_mapping()
    config = {
        'a': a,
        'boards_wide': boards_wide,
        'boards_high': boards_high,
        'type': 'boards',
    }
    BaseController.__init__(self, config, boards_wide * boards_high * BOARD_LED_COUNT, a)

  def _get_index(self, x, y):
    return self._mapping[y * self.boards_wide * BOARD_WIDTH + x]

  def add_led(self, x, y, colour):
    index = self._get_index(x, y)
    BaseController.add_led(self, index, colour)

  def set_led(self, x, y, colour):
    index = self._get_index(x, y)
    BaseController.set_led(self, index, colour)

  def _make_mapping(self) -> List[int]:
    mapping = []

    for board_row in range(0, self.boards_high):
      for row in range(0, BOARD_HEIGHT):
        for board_col in range(0, self.boards_wide):
          board_number = (board_row * self.boards_wide) + board_col
          board_offset = board_number * BOARD_LED_COUNT
          for col in range(0, BOARD_WIDTH):
            if col % 2 == 0: # Even
              offset = (BOARD_HEIGHT * col) + row
            else: # Odd
              offset = (BOARD_HEIGHT * (col + 1)) - (1 + row)

            mapping.append(board_offset + offset)

    return mapping
