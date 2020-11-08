#!/usr/bin/python
# -*- coding: utf8 -*-
import math
from typing import List


def _clockless_bytes(byte: int, alpha: int) -> List[int]:
  """Convert a value into the value to send using the WS2812b protocol.

  For each bit in the given byte, convert it using:
    0 => 100
    1 => 110
  """
  alpha_byte = int(byte * alpha / 32)
  binary = bin(alpha_byte)[2:].rjust(8, '0')
  converted_binary = ''.join('100' if bit == '0' else '110' for bit in binary)
  return [
      int(converted_binary[:8], 2),
      int(converted_binary[8:16], 2),
      int(converted_binary[16:], 2),
  ]


CLOCKLESS_BYTE_LOOKUP = {(alpha, byte): _clockless_bytes(byte, alpha)
                         for byte in range(256) for alpha in range(32)}


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

  def iter_bytes_apa102(self):
    """Convert pixels into APA102 bytes.

    APA102 uses AGBR (with a clock).
    """
    # Send reset bytes
    yield from [0x00, 0x00, 0x00, 0x00]

    # Yield all the pixel data
    for r, g, b in self.PIXELS:
      # Brightness max is 31; or with 224 to add the padding 1s
      yield self.ALPHA | 224
      # R, G, B are max 255
      yield max(min(int(b), 255), 0)
      yield max(min(int(g), 255), 0)
      yield max(min(int(r), 255), 0)

    # Add end bytes (to push all the data through properly)
    end_byte_count = int(math.ceil(self.LED_COUNT / 2 / 8))
    yield from [0xFF] * end_byte_count

  def iter_bytes_ws2812(self):
    """Convert pixels into WS2812B bytes.

    WS2812B uses BRG (without a clock).
    """
    # Yield all the pixel data
    for r, g, b in self.PIXELS:
      yield from CLOCKLESS_BYTE_LOOKUP[(self.ALPHA, b)]
      yield from CLOCKLESS_BYTE_LOOKUP[(self.ALPHA, r)]
      yield from CLOCKLESS_BYTE_LOOKUP[(self.ALPHA, g)]

    # Yield the latch time
    yield from [0x00, 0x00]
