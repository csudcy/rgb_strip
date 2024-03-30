import logging
import os
import pathlib
from typing import Generator, List, Tuple

from PIL import Image
from PIL import ImageDraw

import colours

LOGGER = logging.getLogger(__name__)


class BaseEffect():

  FRAMES = 1000

  def __init__(self, width: int, height: int, name: str,
               palette: colours.Palette):
    self.width = width
    self.height = height
    self.name = name
    self.palette = palette

  def get_filepath(self, directory: pathlib.Path) -> pathlib.Path:
    return directory.joinpath(f'{self.name}.png')

  def render(self, directory: pathlib.Path) -> None:
    # Save the images
    LOGGER.debug(f'{self.name}: Generating images...')
    images = list(self.iter_images())
    LOGGER.debug(f'{self.name}: Saving {len(images)} images to png...')
    filename = self.get_filepath(directory)
    images[0].save(filename, save_all=True, append_images=images[1:])
    LOGGER.debug(f'{self.name}: Saved!')
    loaded = Image.open(filename)
    LOGGER.info(f'{self.name}: Generated {loaded.n_frames} frames!')

  def get_blank_image(self) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new('RGB', (self.width, self.height))
    canvas = ImageDraw.Draw(image)
    return image, canvas

  def iter_images(self) -> Generator[Image.Image, None, None]:
    # image = self.get_blank_image()
    raise Exception('Child classes must implement iter_images!')
