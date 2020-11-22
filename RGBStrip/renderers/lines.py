#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

from RGBStrip import utils
from RGBStrip.renderers.base import BaseSingleTimedRenderer
from RGBStrip.sections.rectangular import RectangularSection


@dataclass
class Line:
  section: RectangularSection
  color: List[float]
  max_gap: int
  max_position: int
  line_count: int
  reverse: bool
  # fill: bool
  prev_line: Optional[Line]

  # Not set at init
  position: float = 0
  gap: int = 0

  # stuck: bool = False

  def __post_init__(self):
    self.gap = self.max_gap
    if self.prev_line is None:
      # I'm the first line; work out an absolute position
      if self.reverse:
        self.position = self.max_position  + (self.line_count - 1) * self.max_gap - 1
      else:
        self.position = 0
    else:
      # Set position based on previous line
      self.update_position()

  def do_render(self):
    if self.is_on_screen:
      self.draw()

  def update_position(self):
    if self.prev_line is None:
      # I'm the first line; do a relative move
      if self.reverse:
        self.position -= 1
      else:
        self.position += 1
    else:
      self.position = self.prev_line.position - self.gap

  @property
  def is_on_screen(self):
    return 0 <= self.position and self.position < self.max_position

  def draw(self):
    raise Exception('Children must override draw!')


class HorizontalLine(Line):

  def draw(self):
    self.section.add_line_horizontal(self.position, self.color)


class VerticalLine(Line):

  def draw(self):
    self.section.add_line_vertical(self.position, self.color)


class LineRenderer(BaseSingleTimedRenderer):

  IS_FINISHABLE = True

  def __init__(
      self,
      loader,
      name=None,
      interval_seconds=0.2,
      section=None,
      palette=None,
      active=True,
      # Custom
      direction='DOWN',  # Up, Down, Left, Right
      line_gap=4,  # Number of lines between lines
      line_count=100,  # Number of lines to use
      # style='FILL',  # NO_FILL, FILL
  ):
    super().__init__(
        loader, name=name, interval_seconds=interval_seconds, section=section,
        palette=palette, active=active)
    self.FINISHED = False
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
    for i in range(line_count):
      self.LINES.append(
          LineClass(
              section=self.SECTION,
              color=self.PALETTE[i % len(self.PALETTE)],
              max_gap=line_gap,
              max_position=max_position,
              line_count=line_count,
              reverse=reverse,
              # fill=(style == 'FILL'),
              prev_line=prev_line,
          ))
      prev_line = self.LINES[-1]

  def do_render_display(self):
    for line in self.LINES:
      line.do_render()

  def do_render_step(self):
    # If all lines are on the screen, we're full - reverse them all
    # If all lines are off the screen, we're empty - reverse them all
    all_on_screen = all(line.is_on_screen for line in self.LINES)
    all_off_screen = all(not line.is_on_screen for line in self.LINES)
    self.FINISHED = (all_on_screen or all_off_screen)

    for line in self.LINES:
      if self.FINISHED:
        line.reverse = not line.reverse
      line.update_position()

  def is_finished(self):
    """Check if this display is in a "finished" state.
    """
    return self.FINISHED
