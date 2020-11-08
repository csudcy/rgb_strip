#!/usr/bin/python
# -*- coding: utf8 -*-


class BaseController(object):
  """An interface to control a strip of RGB LEDs.
  """

  def __init__(self, config, led_count, a):
    self.CONFIG = config
    self.LED_COUNT = led_count
    self.ALPHA = max(min(int(a), 31), 0)
    self.PIXELS = [(0, 0, 0)] * led_count

  def add_led(self, index, colour):
    current_colour = self.PIXELS[index]
    new_colour = (
        current_colour[0] + colour[0],
        current_colour[1] + colour[1],
        current_colour[2] + colour[2],
    )
    self._set_led(index, new_colour)

  def set_led(self, index, colour):
    self._set_led(index, colour)

  def set_leds(self, colour):
    for index in range(len(self.PIXELS)):
      self._set_led(index, colour)

  def _set_led(self, index, colour):
    r, g, b = colour
    self.PIXELS[index] = (
        max(min(int(r), 255), 0),
        max(min(int(g), 255), 0),
        max(min(int(b), 255), 0),
    )
