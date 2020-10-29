#!/usr/bin/python
# -*- coding: utf8 -*-
from threading import Thread

from Tkinter import BOTH, Canvas, Frame, Tk

from .base import BaseDisplay
"""
TODO:
    Close nicely if the window is closed
"""


def int_to_2_hex(i):
  return ('00' + hex(i)[2:])[-2:]


HEX_LOOKUP = [int_to_2_hex(i) for i in range(256)]


def rgba_to_hex(r, g, b, a):
  if (a & 31) == 0:
    return 'grey'
  return '#' + HEX_LOOKUP[r] + HEX_LOOKUP[g] + HEX_LOOKUP[b]


class TkDisplay(BaseDisplay):
  """A display module for RGBStrip to output to a TkInter GUI.
  """

  def __init__(self, controller):
    super().__init__(controller)
    self.root = None
    self.frame = None

  def display(self):
    self.frame.update()

  def setup(self):
    BaseDisplay.setup(self)
    # Setup the window
    self.root = ThreadedTk()
    self.frame = TkFrame(self.root, self.CONTROLLER)
    self.root.start()

  def teardown(self):
    # Destroy the window
    self.root.destroy()


class ThreadedTk(Tk, Thread):

  def __init__(self):
    Tk.__init__(self)
    Thread.__init__(self)

    self.title('RGBStrip')

  def run(self):
    self.mainloop()


class TkFrame(Frame):
  BORDER = 5
  LED_SIZE = 20

  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    self.CONTROLLER = controller

    # Setup the layout method
    self.pack(fill=BOTH, expand=1)

    # Add a canvas
    self.canvas = Canvas(self)
    self.canvas.pack(fill=BOTH, expand=1)

    # Setup the correct geometry
    total_width = 2 * self.BORDER + self.CONTROLLER.WIDTH * self.LED_SIZE
    total_height = 2 * self.BORDER + self.CONTROLLER.HEIGHT * self.LED_SIZE
    parent.geometry(f'{total_width}x{total_height}+300+300')

    # Add all the LEDs
    def make_led(x, y):
      y_top = self.BORDER + y * self.LED_SIZE
      x_left = self.BORDER + x * self.LED_SIZE
      return self.canvas.create_oval(x_left,
                                     y_top,
                                     x_left + self.LED_SIZE,
                                     y_top + self.LED_SIZE,
                                     outline='white',
                                     fill='white',
                                     width=1)

    self.LEDS = [[make_led(x, y)
                  for y in range(self.CONTROLLER.HEIGHT)]
                 for x in range(self.CONTROLLER.WIDTH)]

  def update(self):
    # Update all the LEDs
    for y in range(self.CONTROLLER.HEIGHT):
      for x in range(self.CONTROLLER.WIDTH):
        colour = self.CONTROLLER.get_rgba(x, y)
        self.canvas.itemconfig(
            self.LEDS[x][y],
            fill=rgba_to_hex(*colour),
        )
