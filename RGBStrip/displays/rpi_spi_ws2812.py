from typing import List

from .rpi_spi import RPiSPIDisplay


class RPiSPIDisplayWS2812(RPiSPIDisplay):
  """A display module for RGBStrip to output to Raspberry Pi via the SPI chip.
  For WS2812b LEDs.
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def make_bytes(byte: int) -> List[int]:
      """Convert a value into the value to send using the WS2812b protocol.

      For each byte in the given value, convert it using:
        0 => 100
        1 => 110
      """
      binary = bin(byte)[2:].rjust(8, '0')
      converted_binary = ''.join(
          '100' if bit == '0' else '110' for bit in binary)
      return [
          int(converted_binary[:8], 2),
          int(converted_binary[8:16], 2),
          int(converted_binary[16:], 2),
      ]

    self.BYTE_LOOKUP = {byte: make_bytes(byte) for byte in range(256)}

  def display(self):
    bytes_ = []
    for byte in self.CONTROLLER.BYTES:
      bytes_.extend(self.BYTE_LOOKUP[byte])
    self.SPI.writebytes2(bytes_)
