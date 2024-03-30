from typing import Generator, List

from PIL import Image
from PIL import ImageFont

import colours
from effects import base


class TextEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: colours.Palette,
      # Custom
      text: str = 'MERRY.CHRISTMAS...',
      speed: float = 1.0,
      font_name: str = 'MonumentValley12-X55o.otf',
      font_size: int = 100,
  ):
    super().__init__(width, height, name, palette)
    self.text = text
    self.speed = speed
    self.font = ImageFont.truetype(font_name, font_size)

    self.x = width
    self.colour_index = 0

    # No attribute 'getsize' on PIL.ImageFont.FreeTypeFont
    text_w, _ = self.font.getsize(self.text)  # pytype: disable=attribute-error
    self.min_x = -text_w

  def iter_images(self) -> Generator[Image.Image, None, None]:

    for i in range(self.FRAMES):
      image, canvas = self.get_blank_image()

      canvas.text(
          (self.x, 0),
          text=self.text,
          fill=self.palette[self.colour_index],
          font=self.font,
      )

      self.x -= self.speed
      # Restart when the text is off the screen
      if self.x <= self.min_x:
        self.x = self.width
      self.colour_index = (self.colour_index + 1) % len(self.palette)

      yield image
