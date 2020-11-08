from .rpi_spi import RPiSPIDisplay


class RPiSPIDisplayWS2812(RPiSPIDisplay):
  """A display module for RGBStrip to output to Raspberry Pi via the SPI chip.
  For WS2812b LEDs.
  """

  def __init__(self, controller, speed_mhz=2.22):
    super().__init__(controller, speed_mhz=speed_mhz)

  def display(self):
    output_bytes = self.CONTROLLER.iter_bytes_ws2812()
    self.SPI.writebytes(output_bytes)
