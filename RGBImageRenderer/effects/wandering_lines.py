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
class WanderingLine(utils.Line):

  speed_range: Tuple[float, float] = (-1.0, 1.0)
  speed_d_range: Tuple[float, float] = (-1.0, 1.0)
  angle_d_range: Tuple[float, float] = (-1.0, 1.0)

  # Not set at init
  speed: float = 0
  speed_d: float = 0
  angle_d: float = 0

  def __post_init__(self):
    super().__post_init__()
    self.angle = utils.uniform_negatable(self.angle_range)
    self.speed = utils.uniform_negatable(self.speed_range)
    self.randomise()

  def randomise(self) -> None:
    self.speed_d = utils.uniform_negatable(self.speed_d_range)
    self.angle_d = utils.uniform_negatable(self.angle_d_range)

  def draw(self, canvas: ImageDraw.ImageDraw) -> None:
    super().draw(canvas)

    # Update position/speed/etc.
    self.angle = utils.clamp_negatable(self.angle + self.angle_d,
                                       *self.angle_range)
    self.speed = utils.clamp_negatable(self.speed + self.speed_d,
                                       *self.speed_range)
    self.x = utils.clamp(self.x + math.cos(self.angle) * self.speed, 0,
                         self.width)
    self.y = utils.clamp(self.y + math.sin(self.angle) * self.speed, 0,
                         self.height)

    # Sometimes, change speed_d/angle_d
    if random.random() < 0.1:
      self.randomise()


class WanderingLinesEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: List[colours.ColourType],
      # Custom
      line_count_range: Tuple[int, int] = (3, 5),
      line_repeat_range: Tuple[int, int] = (2, 5),
      speed_range: Tuple[float, float] = (0.5, 2.0),
      speed_d_range: Tuple[float, float] = (0.2, 0.5),
      angle_range: Tuple[float, float] = (15.0, 75.0),
      angle_d_range: Tuple[float, float] = (0.5, 2.0),
  ):
    super().__init__(width, height, name, palette)
    self.line_count_range = line_count_range
    self.line_repeat_range = line_repeat_range
    self.speed_range = speed_range
    self.speed_d_range = speed_d_range
    self.angle_range = angle_range
    self.angle_d_range = angle_d_range

  def iter_images(self) -> Generator[Image.Image, None, None]:
    lines = [
        WanderingLine(
            width=self.width,
            height=self.height,
            palette=self.palette,
            line_repeat=random.randint(*self.line_repeat_range),
            speed_range=self.speed_range,
            speed_d_range=self.speed_d_range,
            angle_range=self.angle_range,
            angle_d_range=self.angle_d_range,
        ) for i in range(random.randint(*self.line_count_range))
    ]

    for i in range(self.FRAMES):
      image, canvas = self.get_blank_image()
      for line in lines:
        line.draw(canvas)
      yield image
