from dataclasses import dataclass
import math
import random
from typing import List, Tuple

from PIL import ImageDraw

import colours


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
class Line:

  width: int
  height: int
  palette: List[colours.ColourType]
  line_repeat: int
  angle_range: Tuple[float, float]
  colour_d_range: Tuple[int, int] = (-2, 2)

  # Not set at init
  x: float = 0
  y: float = 0
  colour_index: int = 0
  colour_d: int = 0
  angle: float = 0
  line_length: int = 0

  def __post_init__(self):
    self.x = random.uniform(0, self.width)
    self.y = random.uniform(0, self.height)
    self.colour_index = random.randint(0, len(self.palette) - 1)
    self.line_length = max(self.width, self.height) * 20
    self.angle = random.uniform(*self.angle_range)
    self.colour_d = random.randint(*self.colour_d_range)

  def draw(self, canvas: ImageDraw.ImageDraw) -> None:
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

    # Update colour
    self.colour_index = (self.colour_index + self.colour_d) % len(self.palette)
