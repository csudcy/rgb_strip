import logging
import os
from typing import Any, Dict, Generator, Tuple

from PIL import Image, ImageDraw

LOGGER = logging.getLogger(__name__)


class BaseEffect():

  def __init__(self, width: int, height: int, name: str, palette: str):
    self.width = width
    self.height = height
    self.name = name
    self.palette = palette

  def render(self, directory: str) -> None:
    # Save the images
    LOGGER.debug(f'{self.name}: Generating images...')
    images = list(self.iter_images())
    LOGGER.debug(f'{self.name}: Saving {len(images)} images to png...')
    filename = os.path.join(directory, f'{self.name}.png')
    images[0].save(filename, save_all=True, append_images=images[1:])
    LOGGER.debug(f'{self.name}: Saved!')

  def get_blank_image(self) -> Tuple[Image.Image, ImageDraw.Draw]:
    image = Image.new('RGB', (self.width, self.height))
    canvas = ImageDraw.Draw(image)
    return image, canvas

  def iter_images(self) -> Generator[Image.Image, None, None]:
    # image = self.get_blank_image()
    raise Exception('Child classes must implement iter_images!')
