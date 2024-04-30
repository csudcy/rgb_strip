#!/usr/bin/python
# -*- coding: utf8 -*-
from dataclasses import dataclass
import datetime
import pathlib
import threading
import time
from typing import Optional

from PIL import Image
from requests import Session
import retry_requests

CURRENT_DIRECTORY = pathlib.Path(__file__).parent
WEATHER_DIRECTORY = CURRENT_DIRECTORY / 'weather'

FORECAST_API = 'https://api.open-meteo.com/v1/forecast'

# Weather codes from: https://open-meteo.com/en/docs
WEATHER_ICON_BY_CODE = {
    # 0 - Clear sky
    0: 'sun',
    # 1, 2, 3 - Mainly clear, partly cloudy, and overcast
    1: 'sun',
    2: 'sun_cloud',
    3: 'cloud',
    # 45, 48 - Fog and depositing rime fog
    45: 'sun_cloud',
    48: 'sun_cloud',
    # 51, 53, 55 - Drizzle: Light, moderate, and dense intensity
    51: 'sun_rain',
    53: 'sun_rain',
    55: 'sun_rain',
    # 56, 57 - Freezing Drizzle: Light and dense intensity
    56: 'freeze',
    57: 'freeze',
    # 61, 63, 65 - Rain: Slight, moderate and heavy intensity
    61: 'rain',
    63: 'rain',
    65: 'rain',
    # 66, 67 - Freezing Rain: Light and heavy intensity
    66: 'freeze',
    67: 'freeze',
    # 71, 73, 75 - Snow fall: Slight, moderate, and heavy intensity
    71: 'snow',
    73: 'snow',
    75: 'snow',
    # 77 - Snow grains
    77: 'snow',
    # 80, 81, 82 - Rain showers: Slight, moderate, and violent
    80: 'rain',
    81: 'rain',
    82: 'storm',
    # 85, 86 - Snow showers slight and heavy
    85: 'snow',
    86: 'snow',
    # 95 - Thunderstorm: Slight or moderate
    95: 'storm',
    # 96, 99 - Thunderstorm with slight and heavy hail
    96: 'storm',
    99: 'storm',
}


@dataclass
class ForecastData:
  start_time: datetime.datetime
  end_time: datetime.datetime
  temperature: float
  weather_code: int
  weather_icon: Optional[str]


class WeatherService(threading.Thread):

  def __init__(
      self,
      *,
      latitude: float,
      longitude: float,
      pull_interval_minutes: int = 30,
  ):
    super().__init__(daemon=True, name='Weather Forecast')

    # Make a session for getting open-meteo data
    self.session = retry_requests.retry(Session(),
                                        retries=5,
                                        backoff_factor=0.2)
    self.params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': ['temperature_2m', 'weather_code'],
        'forecast_days': 1
    }

    # Load weather icons
    self.weather_image_by_icon = {
        weather_filepath.stem: Image.open(weather_filepath)
        for weather_filepath in WEATHER_DIRECTORY.glob('*.png')
    }

    # Pole for forecast updates
    self.pull_interval_seconds = pull_interval_minutes * 60
    self.forecast_data = []
    self.start()

  def run(self):
    while True:
      # Fetch new forecast
      self.forecast_data = self._fetch_forecast()

      # Wait...
      time.sleep(self.pull_interval_seconds)

  # TODO: Cache this!
  def _fetch_forecast(self) -> list[ForecastData]:
    response = self.session.get(FORECAST_API, params=self.params)
    response.raise_for_status()
    response_json = response.json()
    """
    {
      "latitude": 52.52,
      "longitude": 13.419998,
      "generationtime_ms": 0.02002716064453125,
      "utc_offset_seconds": 0,
      "timezone": "GMT",
      "timezone_abbreviation": "GMT",
      "elevation": 38,
      "hourly_units": {
        "time": "iso8601",
        "temperature_2m": "°C",
        "weather_code": "wmo code"
      },
      "hourly": {
        "time": [
          "2024-04-07T00:00",
          ...,
          "2024-04-07T23:00"
        ],
        "temperature_2m": [
          15.5,
          ...,
          16.7
        ],
        "weather_code": [
          1,
          ...,
          3
        ]
      }
    }
    """

    hourly = response_json['hourly']
    start_times = [
        datetime.datetime.fromisoformat(iso_time) for iso_time in hourly['time']
    ]
    temperatures = hourly['temperature_2m']
    weather_codes = hourly['weather_code']
    combined = zip(start_times, temperatures, weather_codes)

    one_hour = datetime.timedelta(hours=1)

    return [
        ForecastData(
            start_time=start_time,
            end_time=start_time + one_hour,
            temperature=temperature,
            weather_code=weather_code,
            weather_icon=WEATHER_ICON_BY_CODE.get(weather_code),
        ) for start_time, temperature, weather_code in combined
    ]

  def get_current_forecast(self) -> Optional[ForecastData]:
    now = datetime.datetime.now()
    for forecast_data in self.forecast_data:
      if forecast_data.start_time <= now <= forecast_data.end_time:
        return forecast_data

    return None

  def get_current_icon(self) -> Optional[Image.Image]:
    current_forecast = self.get_current_forecast()
    if current_forecast:
      return self.weather_image_by_icon.get(current_forecast.weather_icon)


if __name__ == '__main__':
  weather = WeatherService(latitude=52.52, longitude=13.41)
  while True:
    print(weather.get_current_forecast())
    time.sleep(5)
