#!/usr/bin/python
# -*- coding: utf8 -*-
import curses

from .base import BaseDisplay
from RGBStrip import utils


class CursesDisplay(BaseDisplay):
  """A display module for RGBStrip to output to console.
  Note: On windows, you will need to install a wheel from http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
  """

  def display(self):
    # Construct the output
    for y in range(self.CONTROLLER.HEIGHT):
      for x in range(self.CONTROLLER.WIDTH):
        char = utils.classify_colour(*self.CONTROLLER.get_rgba(x, y))
        self.STDSCR.addch(y + 1, x + 1, ord(char))

    self._move_cursor()

    # Check if we should stop
    self.STDSCR.nodelay(1)
    if self.STDSCR.getch() != -1:
      raise KeyboardInterrupt()

  def _move_cursor(self):
    self.STDSCR.move(self.CONTROLLER.HEIGHT + 5, 0)

  def setup(self):
    BaseDisplay.setup(self)

    # Setup the window
    self.STDSCR = curses.initscr()
    curses.cbreak()

    # Draw the borders
    self.STDSCR.addstr(0, 0, '/' + '-' * self.CONTROLLER.WIDTH + '\\')
    for y in range(self.CONTROLLER.HEIGHT):
      self.STDSCR.addstr(y + 1, 0, '|' + ' ' * self.CONTROLLER.WIDTH + '|')
    self.STDSCR.addstr(self.CONTROLLER.HEIGHT + 1, 0,
                       '\\' + '-' * self.CONTROLLER.WIDTH + '/')

    self.STDSCR.addstr(self.CONTROLLER.HEIGHT + 3, 0, 'Press any key to exit')
    self._move_cursor()

  def teardown(self):
    # Destroy the window
    curses.nocbreak()
    curses.endwin()
