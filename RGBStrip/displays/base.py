import logging
import math
from typing import List


def _clockless_bytes(byte: int, alpha: int) -> List[int]:
  """Convert a value into the value to send using the WS2812b protocol.

  For each bit in the given byte, convert it using:
    0 => 100
    1 => 110
  """
  alpha_byte = int(byte * alpha / 32)
  binary = (bin(alpha_byte)[2:]).zfill(8)
  converted_binary = ''.join('100' if bit == '0' else '110' for bit in binary)
  return [
      int(converted_binary[:8], 2),
      int(converted_binary[8:16], 2),
      int(converted_binary[16:], 2),
  ]


CLOCKLESS_BYTE_LOOKUP = {(alpha, byte): _clockless_bytes(byte, alpha)
                         for byte in range(256) for alpha in range(32)}


class BaseDisplay(object):

  def __init__(self, controller, pixel_type=None):
    self.CONTROLLER = controller
    if pixel_type == 'apa102':
      self.iter_bytes = self.iter_bytes_apa102
    elif pixel_type == 'ws2812':
      self.iter_bytes = self.iter_bytes_ws2812
    elif pixel_type:
      raise Exception(f'Unknown pixel_type: ${pixel_type}')

  def display(self):
    raise Exception('Inheriting classes must override BaseDisplay.display!')

  def setup(self):
    """Put any context setup logic here.
    """
    self.SETUP_DONE = True

  def safe_teardown(self):
    if getattr(self, 'SETUP_DONE', False):
      try:
        self.teardown()
      except Exception as ex:
        logging.error('Exception during teardown: %s', str(ex))
      self.SETUP_DONE = False

  def teardown(self):
    """Put any context teardown logic here.
    """
    pass

  def __enter__(self):
    self.setup()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.teardown()

  def iter_bytes(self):
    raise Exception('To use iter_bytes, you must call init with a pixel_type!')

  def iter_bytes_apa102(self):
    """Convert pixels into APA102 bytes.

    APA102 uses AGBR (with a clock).
    """
    # Send reset bytes
    yield from [0x00, 0x00, 0x00, 0x00]

    # Yield all the pixel data
    for r, g, b in self.CONTROLLER.PIXELS:
      # Brightness max is 31; or with 224 to add the padding 1s
      yield self.CONTROLLER.ALPHA | 224
      # R, G, B are max 255
      yield max(min(int(b), 255), 0)
      yield max(min(int(g), 255), 0)
      yield max(min(int(r), 255), 0)

    # Add end bytes (to push all the data through properly)
    end_byte_count = int(math.ceil(self.CONTROLLER.LED_COUNT / 2 / 8))
    yield from [0xFF] * end_byte_count

  def iter_bytes_ws2812(self):
    """Convert pixels into WS2812B bytes.

    WS2812B uses GRB (without a clock).
    """
    # Yield all the pixel data
    for r, g, b in self.CONTROLLER.PIXELS:
      yield from CLOCKLESS_BYTE_LOOKUP[(self.CONTROLLER.ALPHA, g)]
      yield from CLOCKLESS_BYTE_LOOKUP[(self.CONTROLLER.ALPHA, r)]
      yield from CLOCKLESS_BYTE_LOOKUP[(self.CONTROLLER.ALPHA, b)]

    # Yield the latch time
    yield from [0x00, 0x00]
