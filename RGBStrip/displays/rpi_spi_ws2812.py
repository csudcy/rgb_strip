from .rpi_spi import RPiSPIDisplay


class RPiSPIDisplayWS2812(RPiSPIDisplay):
  """A display module for RGBStrip to output to Raspberry Pi via the SPI chip.
  For WS2812b LEDs.
  """

  def __init__(self, controller, speed_mhz=4):
    # Not sure why 4MHz works; calculations said 2.22...
    super().__init__(controller, speed_mhz=speed_mhz)

  def display(self):
    output_bytes = self.CONTROLLER.get_bytes_ws2182()
    self.SPI.writebytes2(output_bytes)
