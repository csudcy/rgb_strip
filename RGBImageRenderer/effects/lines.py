from typing import Generator, List

from PIL import Image

import colours
from effects import base


class LinesEffect(base.BaseEffect):

  def __init__(
      self,
      width: int,
      height: int,
      name: str,
      palette: colours.Palette,
      # Custom
      reverse: bool = False,
      line_gap: int = 4,
  ):
    super().__init__(width, height, name, palette)
    self.reverse = reverse
    self.line_gap = line_gap

  def iter_images(self) -> Generator[Image.Image, None, None]:
    # Intro/outro take self.height frames each
    on_screen_frames = self.FRAMES - 2 * self.height

    if self.reverse:
      line_offsets = list(
          range(self.height, self.height + on_screen_frames, self.line_gap))
      move_by = -1
    else:
      line_offsets = list(range(0, -on_screen_frames, -self.line_gap))
      move_by = 1

    for i in range(self.FRAMES):
      image, canvas = self.get_blank_image()
      move_by_total = move_by * i
      # Draw the lines
      for index, offset in enumerate(line_offsets):
        y = offset + move_by_total
        colour = self.palette[index % len(self.palette)]
        canvas.line((0, y, image.width, y), fill=colour)
      yield image
