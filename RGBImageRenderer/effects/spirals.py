from dataclasses import dataclass
import math
import random
from typing import Generator, List, Tuple

from PIL import Image
from PIL import ImageDraw

import colours
from effects import base
from effects import utils


@dataclass
class MovingLine(utils.Line):

  dy: float = 0  # Have to add a default as it's after other kwargs

  def draw(self, canvas: ImageDraw.ImageDraw) -> None:
    super().draw(canvas)

    # Update position
    self.y += self.dy


class SpiralsEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: colours.Palette,
      # Custom
      angle_speed_colour_d: List[Tuple[float, float, float]] = [
          (30, 0.7, 1),
          (150, -0.7, -1),
      ],
  ):
    super().__init__(width, height, name, palette)
    self.angle_speed_colour_d = angle_speed_colour_d

  def iter_images(self) -> Generator[Image.Image, None, None]:
    lines = [
        MovingLine(
            width=self.width,
            height=self.height,
            palette=self.palette,
            line_repeat=max(self.width, self.height),
            angle_range=(angle, angle),
            colour_d_range=(colour_d, colour_d),
            dy=speed,
        ) for angle, speed, colour_d in self.angle_speed_colour_d
    ]

    for i in range(self.FRAMES):
      image, canvas = self.get_blank_image()

      for line in lines:
        line.draw(canvas)

      yield image
