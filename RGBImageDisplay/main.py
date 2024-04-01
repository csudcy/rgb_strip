#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime
import logging
import pathlib
import time
import traceback

import click
import devices
from luma.core.render import canvas
from PIL import ImageFont
import rgb_image_display
import server

DEVICES = {
    'none': devices.ImageDevice,
    'terminal': devices.ImageDeviceTerminal,
    'ws2812': devices.ImageDeviceWS2812,
    'ws2812_boards': devices.ImageDeviceWS2812Boards,
}

ROTATE_MAP = {
    '0': 0,
    '90': 1,
    '180': 2,
    '270': 3,
}

CURRENT_DIR = pathlib.Path(__file__).parent
FONT_FILE = CURRENT_DIR / 'pixelmix.ttf'

HSL_FORMAT = 'hsl({hue}, 100%, 50%)'


@click.group()
def main() -> None:
  """Display moving images on neopixels!"""


@main.command()
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.argument('directory', type=pathlib.Path)
@click.option('--rotate',
              help='How many degrees to rotate by (--display=terminal only)',
              type=click.Choice(ROTATE_MAP.keys()),
              default='0')
@click.option('--flip_x',
              help='Flip output around x axis (--display=ws2812 only)',
              type=bool,
              default=False,
              is_flag=True)
@click.option('--flip_y',
              help='Flip output around y axis (--display=ws2812 only)',
              type=bool,
              default=False,
              is_flag=True)
@click.option('--alpha',
              help='How bright to show the pixels (0-255)',
              type=int,
              default=40)
@click.option('--delay',
              help='How many ms to delay between frames',
              type=int,
              default=0)
@click.option('--device',
              help='The device to use for output',
              type=click.Choice(DEVICES.keys()),
              default='terminal')
@click.option('--debug',
              help='Enable debug output',
              type=bool,
              default=False,
              is_flag=True)
def run(
    width: int,
    height: int,
    directory: pathlib.Path,
    rotate: str,
    flip_x: bool,
    flip_y: bool,
    alpha: int,
    delay: int,
    device: str,
    debug: bool,
):
  if debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  DeviceClass = DEVICES[device]
  device = DeviceClass(
      width=width,
      height=height,
      alpha=alpha,
      rotate=ROTATE_MAP[rotate],
      flip_x=flip_x,
      flip_y=flip_y,
  )

  display_thread = rgb_image_display.ImageDisplay(
      device=device,
      delay=delay,
      directory=directory.resolve(),
  )
  display_thread.daemon = True
  display_thread.start()

  # Block on the server
  server.run(device, display_thread)


@main.command()
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.option('--alpha',
              help='How bright to show the pixels (0-255)',
              type=int,
              default=40)
@click.option('--rainbow-seconds',
              help='How many seconds to cycle through the rainbow over',
              type=int,
              default=60)
@click.option('--device',
              help='The device to use for output',
              type=click.Choice(DEVICES.keys()),
              default='terminal')
@click.option('--debug',
              help='Enable debug output',
              type=bool,
              default=False,
              is_flag=True)
def clock(
    width: int,
    height: int,
    alpha: int,
    rainbow_seconds: int,
    device: str,
    debug: bool,
):
  if debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  logging.info('Running clock...')

  DeviceClass = DEVICES[device]
  device = DeviceClass(
      width=width,
      height=height,
      alpha=alpha,
  )

  font = ImageFont.truetype(FONT_FILE.as_posix(), 8)
  seconds_multiplier = 360 / rainbow_seconds
  while True:
    now = datetime.now()
    text = now.strftime('%H : %M')
    seconds = now.timestamp() % rainbow_seconds
    hue = int(seconds * seconds_multiplier)

    with canvas(device.device) as draw:
      # Clear the canvas
      draw.rectangle(((0, 0), (device.device.width, device.device.height)),
                     fill='black')

      # Work out where to draw the text
      text_width = draw.textlength(text, font=font)
      offset = int(float(device.device.width - text_width) / 2.0)

      # Draw the text
      draw.text((offset, 0), text, font=font, fill=HSL_FORMAT.format(hue=hue))

    time.sleep(0.01)


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
