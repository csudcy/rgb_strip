#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleRenderer
from RGBStrip.sections.rectangular import RectangularSection


@dataclass
class Line:
  section: RectangularSection
  color: List[float]
  move_steps: int
  max_gap: int
  max_position: int
  reverse: bool
  # fill: bool
  prev_line: Optional[Line]

  # Not set at init
  position: float = 0
  gap: int = 0
  steps_since_move: int = 0

  # stuck: bool = False

  def __post_init__(self):
    self.gap = self.max_gap
    if self.prev_line is None:
      # I'm the first line; work out an absolute position
      if self.reverse:
        self.position = (self.max_position - 1) * (self.max_gap + 1)
      else:
        self.position = 0
    else:
      # Set position based on previous line
      self.update_position()

  def do_render(self):
    self.update_position()
    if self.is_on_screen:
      self.draw()

  def update_position(self):
    mult = -1 if self.reverse else 1

    if self.prev_line is None:
      # I'm the first line; do a relative move
      self.steps_since_move += 1
      if self.steps_since_move >= self.move_steps:
        # Move now
        self.steps_since_move = 0
        self.position += mult
    else:
      self.position = self.prev_line.position - self.gap

  @property
  def is_on_screen(self):
    return 0 <= self.position and self.position < self.max_position

  def draw(self):
    raise Exception('Children must override draw!')


class HorizontalLine(Line):

  def draw(self):
    self.section.add_line_horizontal(round(self.position), self.color)


class VerticalLine(Line):

  def draw(self):
    self.section.add_line_vertical(round(self.position), self.color)


class LineRenderer(BaseSingleRenderer):

  def __init__(
      self,
      loader,
      section=None,
      palette=None,
      active=True,
      # Custom
      direction='DOWN',  # Up, Down, Left, Right
      move_steps=5,  # Steps between moving lines
      line_gap=4,  # Number of lines between lines
      # style='FILL',  # NO_FILL, FILL
  ):
    super().__init__(loader, section=section, palette=palette, active=active)
    direction = direction.upper()

    if direction in ('DOWN', 'UP'):
      LineClass = HorizontalLine
      max_position = self.SECTION.HEIGHT
      reverse = (direction == 'UP')
    elif direction in ('RIGHT', 'LEFT'):
      LineClass = VerticalLine
      max_position = self.SECTION.WIDTH
      reverse = (direction == 'LEFT')
    else:
      raise Exception(f'Unknown direction: {self.DIRECTION}')

    # self.STYLE = style

    # Create all the lines
    self.LINES = []
    prev_line = None
    for i in range(max_position):
      self.LINES.append(
          LineClass(
              section=self.SECTION,
              color=self.PALETTE[i % len(self.PALETTE)],
              move_steps=move_steps,
              max_gap=line_gap,
              max_position=max_position,
              reverse=reverse,
              # fill=(style == 'FILL'),
              prev_line=prev_line,
          ))
      prev_line = self.LINES[-1]

  def do_render(self):
    # If all lines are on the screen, we're full - reverse them all
    # If all lines are off the screen, we're empty - reverse them all
    all_on_screen = all(line.is_on_screen for line in self.LINES)
    all_off_screen = all(not line.is_on_screen for line in self.LINES)
    if all_on_screen or all_off_screen:
      for line in self.LINES:
        line.reverse = not line.reverse
        line.update_position()

    for line in self.LINES:
      line.do_render()
