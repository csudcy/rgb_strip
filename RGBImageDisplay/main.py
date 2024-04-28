#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
import pathlib
import time
import traceback
from typing import Optional

import click
from luma.core.render import canvas
from PIL import Image
from PIL import ImageFont

import devices
import rgb_clock
import rgb_image_display
import server
import weather

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
@click.option('--lat',
              help='Latitude to use for weather forecasting',
              type=float)
@click.option('--lng',
              help='Longitude to use for weather forecasting',
              type=float)
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
    lat: Optional[float],
    lng: Optional[float],
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

  if lat and lng:
    _weather = weather.WeatherService(latitude=lat, longitude=lng)
  else:
    _weather = None

  clock = rgb_clock.Clock(
      device=device,
      alpha_min=alpha_min,
      alpha_max=alpha_max,
      rainbow_seconds=rainbow_seconds,
      font=font,
      format=format,
      weather=_weather,
  )
  clock.run()


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
                    fill=f'hsl({hue}, 100%, 50%)')

        time.sleep(0.02)


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
    font: str,
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
  font_object = ImageFont.truetype(font, 8)

  while True:
    for weather_filepath in weather.WEATHER_DIRECTORY.glob('*.png'):
      image = Image.open(weather_filepath)

      _canvas = canvas(device.device)
      with _canvas as draw:
        # Clear the canvas
        draw.rectangle(
            ((0, 0), (device.device.width, device.device.height)),
            fill='black')

        # Draw the text
        draw.text((10, 0),
                  weather_filepath.stem,
                  font=font_object,
                  fill='hsl(1, 100%, 100%)')

        # Show the image
        _canvas.image.paste(image)

      time.sleep(2)


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
