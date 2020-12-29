import math
from typing import Generator, List

from PIL import Image

import colours
from . import base


class SpiralEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: List[colours.ColourType],
      # Custom
      direction: str = 'forward',
      reverse: bool = False,
      line_gap: int = 4,
  ):
    super().__init__(width, height, name, palette)
    self.direction = direction
    self.reverse = reverse
    self.line_gap = line_gap
    self.frames = 1000

  def iter_images(self) -> Generator[Image.Image, None, None]:
    if self.direction == 'forward':
      # /
      first_x = self.width - 1
      next_dx = -1
    else:
      # \
      first_x = 0
      next_dx = +1

    if self.reverse:
      first_dy = -1
    else:
      first_dy = +1

    line_count = max(self.width, self.height)
    current_y = 0
    for i in range(self.frames):
      image, canvas = self.get_blank_image()

      for i in range(line_count):
        x = first_x + i * next_dx
        y = current_y + i
        canvas.point((x % self.width, y % self.height),
                     self.palette[i % len(self.palette)])

      current_y += first_dy

      yield image
