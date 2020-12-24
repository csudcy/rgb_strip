#!/usr/bin/python
# -*- coding: utf8 -*-
import traceback

import click

import rgb_gif_display

DISPLAYS = {
    'none': rgb_gif_display.GifDisplayNone,
    'terminal': rgb_gif_display.GifDisplayTerminal,
    'ws2812': rgb_gif_display.GifDisplayWS2812,
}


@click.group()
def main() -> None:
  """Display GIFs on neopixels!"""


@main.command()
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.argument('directory')
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
def run(
    width: int,
    height: int,
    directory: str,
    alpha: int,
    delay: int,
    display: str,
):
  GifDisplayClass = DISPLAYS[display]
  display_thread = GifDisplayClass(width, height, alpha, delay, directory)
  display_thread.daemon = True
  display_thread.start()
  display_thread.join()


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
