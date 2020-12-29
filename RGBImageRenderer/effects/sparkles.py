import collections
import random
from dataclasses import dataclass
from typing import Deque, Generator, Iterable, List, Optional

from PIL import Image, ImageDraw

from . import base
import colours


@dataclass
class Sparkle:
  width: int
  height: int
  palette: List[colours.ColourType]
  fade_steps: Iterable[int]
  on_steps: Iterable[int]
  off_steps: Iterable[int]

  # Not set at init
  x: int = 0
  y: int = 0
  stage_steps: Deque[List[float]] = collections.deque()
  first_run: bool = True

  def randomise(self) -> None:
    self.x = random.randint(0, self.width)
    self.y = random.randint(0, self.height)
    colour_fade = colours.fade_in_out(
        random.choice(self.palette),
        random.randint(*self.fade_steps),
        random.randint(*self.fade_steps),
        random.randint(*self.on_steps),
        random.randint(*self.off_steps),
    )
    if self.first_run:
      # This is the first run; randomise the current stage in fade
      self.first_run = False
      start_at = random.randint(0, int(len(colour_fade) / 2))
      colour_fade = colour_fade[start_at:]
    self.stage_steps = collections.deque(reversed(colour_fade))

  def draw(self, canvas: ImageDraw.Draw) -> None:
    try:
      colour = self.stage_steps.pop()
    except IndexError:
      # No more steps; start again
      self.randomise()
      colour = self.stage_steps.pop()
    canvas.point((self.x, self.y), colour)


class SparklesEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: List[colours.ColourType],
      # Custom
      coverage: int = 20,  # Percentage of lights which should be sparkling
      fade_steps: List[int] = (5, 20),  # Range of steps to fade for
      on_steps: List[int] = (3, 10),  # Range of steps to stay on
      off_steps: List[int] = (1, 3),  # Range of steps to stay off
  ):
    super().__init__(width, height, name, palette)
    self.coverage = coverage
    self.fade_steps = fade_steps
    self.on_steps = on_steps
    self.off_steps = off_steps

  def iter_images(self) -> Generator[Image.Image, None, None]:
    leds_total = self.width * self.height
    leds_on = int(self.coverage * leds_total / 100)
    sparkles = [
        Sparkle(
            self.width,
            self.height,
            palette=self.palette,
            fade_steps=self.fade_steps,
            on_steps=self.on_steps,
            off_steps=self.off_steps,
        ) for _ in range(leds_on)
    ]

    for i in range(1000):
      image, canvas = self.get_blank_image()
      for sparkle in sparkles:
        sparkle.draw(canvas)
      yield image
