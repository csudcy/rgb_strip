from dataclasses import dataclass
import random
from typing import Generator, List, Optional, Tuple

from PIL import Image
from PIL import ImageDraw

import colours
from effects import base


@dataclass
class Pixel:
  x: int
  y: int
  palette: colours.Palette
  # Not set at init
  palette_index: Optional[int] = None
  neighbours: List['Pixel'] = None

  def next_colour(self):
    # was = self.palette_index
    if self.palette_index is None:
      self.palette_index = 0
    elif self.palette_index < len(self.palette) - 1:
      self.palette_index += 1
    # else:
    #   self.palette_index = (self.palette_index + 1) % len(self.palette)
    # print(f'{self.x}, {self.y}: {was} -> {self.palette_index}')

  def draw(self, canvas: ImageDraw.ImageDraw) -> None:
    if self.palette_index is not None:
      canvas.point((self.x, self.y), self.palette[self.palette_index])
    
    neighbour = random.choice(self.neighbours)
    if neighbour.palette_index is not None:
      self.palette_index = max(self.palette_index or 0, neighbour.palette_index)
      # print(self.palette_index)


class SpreadEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: colours.Palette,
      # Custom
      # Left, Right, Top, Bottom
      edges_lrtb: Tuple[bool] = (True, True, True, True),
      initiate_chance: float = 0.3,
  ):
    super().__init__(width, height, name, palette)
    self.edges_lrtb = edges_lrtb
    self.initiate_chance = initiate_chance

  def iter_images(self) -> Generator[Image.Image, None, None]:
    pixel_dict = {
        (x, y): Pixel(x, y, self.palette)
        for x in range(self.width)
        for y in range(self.height)
    }
    for x in range(self.width):
      for y in range(self.height):
        pixel_dict[(x, y)].neighbours = [
            pixel_dict[(x + dx, y + dy)]
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (x + dx, y + dy) in pixel_dict
        ]
    
    initiators = (
        [pixel_dict[(x, 0)] for x in range(self.width)] + 
        [pixel_dict[(x, self.height - 1)] for x in range(self.width)] + 
        [pixel_dict[(0, y)] for y in range(self.height)] + 
        [pixel_dict[(self.width - 1, y)] for y in range(self.height)]
    )

    pixels = list(pixel_dict.values())

    for i in range(self.FRAMES):
      image, canvas = self.get_blank_image()

      if random.random() <= self.initiate_chance:
        initiator = random.choice(initiators)
        initiator.next_colour()

      for pixel in pixels:
        pixel.draw(canvas)

      yield image
