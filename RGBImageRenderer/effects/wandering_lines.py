from dataclasses import dataclass
import math
import random
from typing import Generator, List, Tuple

from PIL import Image
from PIL import ImageDraw

import colours
from effects import base


def clamp(value: float, v_min: float, v_max: float) -> float:
  return min(max(value, v_min), v_max)


def clamp_negatable(value: float, v_min: float, v_max: float) -> float:
  if value < 0:
    return min(max(value, -v_max), -v_min)
  else:
    return min(max(value, v_min), v_max)


def uniform_negatable(range: Tuple[float, float]):
  value = random.uniform(*range)
  if random.choice([False, True]):
    return value
  else:
    return -value


@dataclass
class WanderingLine:

  width: int
  height: int
  palette: List[colours.ColourType]
  line_repeat: int
  speed_range: Tuple[float, float]
  speed_d_range: Tuple[float, float]
  angle_range: Tuple[float, float]
  angle_d_range: Tuple[float, float]

  # Not set at init
  x: float = 0
  y: float = 0
  colour_index: int = 0
  colour_d: float = 0
  speed: float = 0
  speed_d: float = 0
  angle: float = 0
  angle_d: float = 0
  line_length: int = 0

  def __post_init__(self):
    self.x = random.uniform(0, self.width)
    self.y = random.uniform(0, self.height)
    self.colour_index = random.randint(0, len(self.palette) - 1)
    self.line_length = max(self.width, self.height) * 20
    self.speed = uniform_negatable(self.speed_range)
    self.angle = uniform_negatable(self.angle_range)
    self.randomise()

  def randomise(self) -> None:
    self.colour_d = random.randint(-2, 2)
    self.speed_d = uniform_negatable(self.speed_d_range)
    self.angle_d = uniform_negatable(self.angle_d_range)

  def draw(self, canvas: ImageDraw.Draw) -> None:
    # Draw my lines
    angle = math.radians(self.angle)
    x1 = self.x + math.cos(angle) * self.line_length
    y1 = self.y + math.sin(angle) * self.line_length
    x2 = self.x + math.cos(angle + math.pi) * self.line_length
    y2 = self.y + math.sin(angle + math.pi) * self.line_length

    colour = self.palette[self.colour_index]
    for i in range(-self.line_repeat, self.line_repeat + 1):
      canvas.line(
          (
              (int(x1 + i * self.width), int(y1)),
              (int(x2 + i * self.width), int(y2)),
          ),
          fill=colour,
      )

    # Update position/speed/etc.
    self.colour_index = (self.colour_index + self.colour_d) % len(self.palette)
    self.angle = clamp_negatable(self.angle + self.angle_d, *self.angle_range)
    self.speed = clamp_negatable(self.speed + self.speed_d, *self.speed_range)
    self.x = clamp(self.x + math.cos(self.angle) * self.speed, 0, self.width)
    self.y = clamp(self.y + math.sin(self.angle) * self.speed, 0, self.height)

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
