#!/usr/bin/python
# -*- coding: utf8 -*-
import traceback
import os
import random
import time
from typing import List, Tuple

import click
from PIL import Image
from luma.core.device import device as LumaDevice
import PIL


@click.group()
def main() -> None:
  """Display GIFs on neopixels!"""


@main.command()
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.argument('directory')
@click.option('--alpha', help='How bright to show the pixels (0-255)', type=int, default=40)
@click.option('--delay', help='How many ms to delay between frames', type=int, default=0)
@click.option('--emulate', help='Emulate the display in terminal', type=bool, default=False, is_flag=True)
def run(
    width: int,
    height: int,
    directory: str,
    alpha: int,
    delay: int,
    emulate: bool,
):
  images = get_images(width, height, directory)
  if not images:
    raise Exception('No files found!')

  device = get_device(width, height, emulate)
  device.contrast(alpha)

  delay_seconds = delay / 1000.0

  while True:
    name, image = random.choice(images)

    for frame_index in range(image.n_frames):
      image.seek(frame_index)
      resized = image.resize((width, height))
      converted = resized.convert('RGB')
      device.display(converted)
      print(f'{name} : {frame_index} / {image.n_frames}...')
      time.sleep(delay_seconds)


def get_device(width: int, height: int, emulate: bool) -> LumaDevice:
  if emulate:
    from luma.emulator.device import asciiblock
    return asciiblock(width=width, height=height)
  else:
    from luma.led_matrix.device import ws2812
    return ws2812(width=width, height=height)


def get_images(width: int, height: int, directory: str) -> List[Tuple[str, Image.Image]]:
  images: List[Tuple[str, Image.Image]] = []
  for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)

    # Check it's an image
    print(f'Checking {filename}...')
    try:
      image = Image.open(filepath)
    except PIL.UnidentifiedImageError:
      print('  Skipped: Not an image')
      continue

    # Check some things about the image
    checks = [
        # (image.mode == 'RGB', 'Must be RGB'),
        (hasattr(image, 'n_frames'), 'Must be multiple frames'),
        # (image.width == width, f'Width must be {width} pixels'),
        # (image.height == height, f'Height must be {height} pixels'),
    ]
    failed_checks = [
        message
        for passed, message in checks
        if not passed
    ]
    if failed_checks:
      print(f'  Skipped: {failed_checks}')
    else:
      print('  Good!')
      images.append((filename, image))

  return images


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
