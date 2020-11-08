#!/usr/bin/python
# -*- coding: utf8 -*-

from typing import Tuple


class RectangularSection(object):
  """Allow a rectangular section of an RGBStrip to be controlled.
  """

  def __init__(self,
               controller,
               x: int,
               y: int,
               width: int,
               height: int,
               active: bool = True,
               reverse_x: bool = False,
               reverse_y: bool = False):
    self.CONTROLLER = controller
    self.X: int = x
    self.Y: int = y
    self.WIDTH: int = width
    self.HEIGHT: int = height
    self.ACTIVE: bool = active
    self.REVERSE_X: bool = reverse_x
    self.REVERSE_Y: bool = reverse_y

  def add_led(self, x: int, y: int, colour):
    if self.ACTIVE:
      ax, ay = self._get_absolute_xy(x, y)
      self.CONTROLLER.add_led(ax, ay, colour)

  def set_led(self, x: int, y: int, colour):
    if self.ACTIVE:
      ax, ay = self._get_absolute_xy(x, y)
      self.CONTROLLER.set_led(ax, ay, colour)

  def add_line_horizontal(self, y: int, colour):
    if self.ACTIVE:
      for x in range(self.WIDTH):
        ax, ay = self._get_absolute_xy(x, y)
        self.CONTROLLER.add_led(ax, ay, colour)

  def add_line_vertical(self, x: int, colour):
    if self.ACTIVE:
      for y in range(self.HEIGHT):
        ax, ay = self._get_absolute_xy(x, y)
        self.CONTROLLER.add_led(ax, ay, colour)

  def increment_xy(self, x: int, y: int) -> Tuple[int, int]:
    # Move to the next column
    x += 1
    if x >= self.WIDTH:
      # Move to the next row
      x = 0
      y += 1
      if y >= self.HEIGHT:
        y = 0
    return x, y

  def _get_absolute_xy(self, x: int, y: int) -> Tuple[int, int]:
    x = x % self.WIDTH
    y = y % self.HEIGHT
    if self.REVERSE_X:
      x = self.WIDTH - x - 1
    if self.REVERSE_Y:
      y = self.HEIGHT - y - 1
    return self.X + x, self.Y + y
