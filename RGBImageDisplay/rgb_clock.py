#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime
import time
from typing import Optional

from luma.core.render import canvas
from PIL import Image
from PIL import ImageFont

import devices
import weather as _weather


class Clock:

  def __init__(
      self,
      *,
      device: devices.ImageDevice,
      alpha_min: int,
      alpha_max: int,
      rainbow_seconds: int,
      font: str,
      format: str,
      weather: Optional[_weather.WeatherService],
  ):
    # Save basic things
    self.device = device
    self.rainbow_seconds = rainbow_seconds
    self.seconds_multiplier = 360 / rainbow_seconds
    self.font_object = ImageFont.truetype(font, 8)
    self.format = format
    self.weather = weather

    # Work out alpha values to use per-minute
    alpha_ranges = (
        # (hour from, hour to, alpha from, alpha to)
        (0, 6, alpha_min, alpha_min),
        (6, 8, alpha_min, alpha_max),
        (8, 20, alpha_max, alpha_max),
        (20, 22, alpha_max, alpha_min),
        (22, 24, alpha_min, alpha_min),
    )
    self.alpha_lookup = []
    for hour_from, hour_to, alpha_from, alpha_to in alpha_ranges:
      length_minutes = (hour_to - hour_from) * 60
      alpha_diff = (alpha_to - alpha_from)
      for minute in range(length_minutes):
        self.alpha_lookup.append(alpha_from +
                                 int(alpha_diff * minute / length_minutes))
    assert len(self.alpha_lookup) == 24 * 60, 'Alpha lookup length incorrect!'

  def run(self):
    while True:
      now = datetime.now()
      text = now.strftime(self.format)
      seconds = now.timestamp() % self.rainbow_seconds
      hue = int(seconds * self.seconds_multiplier)

      alpha = self.alpha_lookup[now.hour * 60 + now.minute]
      self.device.set_alpha(alpha)

      if self.weather:
        weather_icon = self.weather.get_current_icon()
      else:
        weather_icon = None

      _canvas = canvas(self.device.device)
      with _canvas as draw:
        # Clear the canvas
        draw.rectangle(
            ((0, 0), (self.device.device.width, self.device.device.height)),
            fill='black')

        # Work out where to draw the text
        text_width = draw.textlength(text, font=self.font_object)
        offset = int(float(self.device.device.width - text_width) / 2.0)

        # Draw the text
        draw.text((offset, 0),
                  text,
                  font=self.font_object,
                  fill=f'hsl({hue}, 100%, 50%)')

        if weather_icon:
          _canvas.image.paste(weather_icon)

      time.sleep(0.01)
