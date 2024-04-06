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
from PIL import Image
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

HSL_FORMAT = 'hsl({hue}, 100%, 50%)'

CURRENT_DIRECTORY = pathlib.Path(__file__).parent
WEATHER_DIRECTORY = CURRENT_DIRECTORY / 'weather'
WEATHER_IMAGES = WEATHER_DIRECTORY.glob('*.png')


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
@click.option('--display',
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
@click.option('--alpha-min',
              help='Minimum brightness for pixels (0-255)',
              type=int,
              default=10)
@click.option('--alpha-max',
              help='Maximum brightness for pixels (0-255)',
              type=int,
              default=100)
@click.option('--rainbow-seconds',
              help='How many seconds to cycle through the rainbow over',
              type=int,
              default=60)
@click.option('--display',
              help='The device to use for output',
              type=click.Choice(DEVICES.keys()),
              default='terminal')
@click.option('--font',
              help='The font file to use',
              type=str,
              default='pixelmix.ttf')
@click.option('--format',
              help='The strftime format to use',
              type=str,
              default='%H : %M')
@click.option('--debug',
              help='Enable debug output',
              type=bool,
              default=False,
              is_flag=True)
def clock(
    width: int,
    height: int,
    alpha_min: int,
    alpha_max: int,
    rainbow_seconds: int,
    display: str,
    font: str,
    format: str,
    debug: bool,
):
  if debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  logging.info('Running clock...')

  DeviceClass = DEVICES[display]
  device = DeviceClass(
      width=width,
      height=height,
      alpha=alpha_min,
  )

  font_object = ImageFont.truetype(font, 8)

  # Work out alpha values to use per-minute
  alpha_ranges = (
      # (hour from, hour to, alpha from, alpha to)
      (0, 6, alpha_min, alpha_min),
      (6, 8, alpha_min, alpha_max),
      (8, 20, alpha_max, alpha_max),
      (20, 22, alpha_max, alpha_min),
      (22, 24, alpha_min, alpha_min),
  )
  alpha_lookup = []
  for hour_from, hour_to, alpha_from, alpha_to in alpha_ranges:
    length_minutes = (hour_to - hour_from) * 60
    alpha_diff = (alpha_to - alpha_from)
    for minute in range(length_minutes):
      alpha_lookup.append(alpha_from +
                          int(alpha_diff * minute / length_minutes))
  assert len(alpha_lookup) == 24 * 60, 'Alpha lookup length incorrect!'

  seconds_multiplier = 360 / rainbow_seconds
  while True:
    now = datetime.now()
    text = now.strftime(format)
    seconds = now.timestamp() % rainbow_seconds
    hue = int(seconds * seconds_multiplier)

    alpha = alpha_lookup[now.hour * 60 + now.minute]
    device.set_alpha(alpha)

    with canvas(device.device) as draw:
      # Clear the canvas
      draw.rectangle(((0, 0), (device.device.width, device.device.height)),
                     fill='black')

      # Work out where to draw the text
      text_width = draw.textlength(text, font=font_object)
      offset = int(float(device.device.width - text_width) / 2.0)

      # Draw the text
      draw.text((offset, 0),
                text,
                font=font_object,
                fill=HSL_FORMAT.format(hue=hue))

    time.sleep(0.01)


@main.command()
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.option('--display',
              help='The device to use for output',
              type=click.Choice(DEVICES.keys()),
              default='terminal')
@click.option('--font',
              help='The font file to use',
              type=str,
              default='pixelmix.ttf')
@click.option('--debug',
              help='Enable debug output',
              type=bool,
              default=False,
              is_flag=True)
def test_alpha(
    width: int,
    height: int,
    display: str,
    font: str,
    debug: bool,
):
  if debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  logging.info('Running alpha test...')

  DeviceClass = DEVICES[display]
  device = DeviceClass(
      width=width,
      height=height,
      alpha=10,
  )

  font_object = ImageFont.truetype(font, 8)

  while True:
    for alpha in (1, 10, 20, 30, 40, 50, 100, 150, 200, 250):
      for hue in range(0, 360, 5):
        device.set_alpha(alpha)
        text = f'{alpha:3} {hue:3}°'

        with canvas(device.device) as draw:
          # Clear the canvas
          draw.rectangle(((0, 0), (device.device.width, device.device.height)),
                         fill='black')

          # Draw the text
          draw.text((0, 0),
                    text,
                    font=font_object,
                    fill=HSL_FORMAT.format(hue=hue))

        time.sleep(0.02)


@main.command()
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.option('--display',
              help='The device to use for output',
              type=click.Choice(DEVICES.keys()),
              default='terminal')
@click.option('--alpha',
              help='How bright to show the pixels (0-255)',
              type=int,
              default=40)
@click.option('--debug',
              help='Enable debug output',
              type=bool,
              default=False,
              is_flag=True)
def test_weather(
    width: int,
    height: int,
    display: str,
    alpha: int,
    debug: bool,
):
  if debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  logging.info('Running weather test...')

  DeviceClass = DEVICES[display]
  device = DeviceClass(
      width=width,
      height=height,
      alpha=alpha,
  )

  while True:
    for weather_filepath in WEATHER_IMAGES:
      image = Image.open(weather_filepath)
      device_image = Image.new('RGB', (width, height))
      device_image.paste(image)
      device.device.display(device_image)
      time.sleep(2)


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
