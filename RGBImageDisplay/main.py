#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
import traceback

import click
import rgb_image_display
import server

DISPLAYS = {
    'none': rgb_image_display.ImageDisplayNone,
    'terminal': rgb_image_display.ImageDisplayTerminal,
    'ws2812': rgb_image_display.ImageDisplayWS2812,
}

ROTATE_MAP = {
    '0': 0,
    '90': 1,
    '180': 2,
    '270': 3,
}


@click.group()
def main() -> None:
  """Display moving images on neopixels!"""


@main.command()
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.argument('directory')
@click.option('--rotate',
              help='How many degrees to rotate the display by',
              type=click.Choice(ROTATE_MAP.keys()),
              default='0')
@click.option('--alpha',
              help='How bright to show the pixels (0-255)',
              type=int,
              default=40)
@click.option('--delay',
              help='How many ms to delay between frames',
              type=int,
              default=0)
@click.option('--display',
              help='The display to use for output',
              type=click.Choice(DISPLAYS.keys()),
              default='terminal')
@click.option('--debug',
              help='Enable debug output',
              type=bool,
              default=False,
              is_flag=True)
def run(
    width: int,
    height: int,
    directory: str,
    rotate: int,
    alpha: int,
    delay: int,
    display: str,
    debug: bool,
):
  if debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  ImageDisplayClass = DISPLAYS[display]
  display_thread = ImageDisplayClass(width, height, ROTATE_MAP[rotate], alpha,
                                     delay, directory)
  display_thread.daemon = True
  display_thread.start()

  # Block on the server
  server.run(display_thread)


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
