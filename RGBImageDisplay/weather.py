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
  sunrise: datetime.datetime
  sunset: datetime.datetime
  weather_code: int
  weather_icon: Optional[str]


class WeatherService(threading.Thread):

  def __init__(
      self,
      *,
      latitude: float,
      longitude: float,
      timezone: str = 'Europe/London',
      pull_interval_minutes: int = 5,
  ):
    super().__init__(daemon=True, name='Weather Forecast')

    # Make a session for getting open-meteo data
    self.session = retry_requests.retry(Session(),
                                        retries=5,
                                        backoff_factor=0.2)
    self.params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': ['weather_code'],
        'daily': ['sunrise', 'sunset'],
        'timezone': timezone,
        'forecast_days': 1
    }

    # Load weather icons
    self.weather_image_by_icon = {
        weather_filepath.stem: Image.open(weather_filepath)
        for weather_filepath in WEATHER_DIRECTORY.glob('*.png')
    }

    # Pole for forecast updates
    self.pull_interval_seconds = pull_interval_minutes * 60
    self.current_forecast = None
    self.start()

  def run(self):
    while True:
      # Fetch new forecast
      self.current_forecast = self._fetch_current_forecast()

      # Wait...
      time.sleep(self.pull_interval_seconds)

  def _fetch_current_forecast(self) -> Optional[ForecastData]:
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
      "current_units":{
        "time":"iso8601",
        "interval":"seconds",
        "weather_code":"wmo code"
      },
      "current":{
        "time":"2024-04-30T21:30",
        "interval":900,
        "weather_code":2
      },
      "daily_units":{
        "time":"iso8601",
        "sunrise":"iso8601",
        "sunset":"iso8601"
      },
      "daily":{
        "time":["2024-04-30"],
        "sunrise":["2024-04-30T05:34"],
        "sunset":["2024-04-30T20:24"]
      }
    }
    """
    weather_code = response_json['current']['weather_code']
    sunrise = datetime.datetime.fromisoformat(response_json['daily']['sunrise'][0])
    sunset = datetime.datetime.fromisoformat(response_json['daily']['sunset'][0])
    return ForecastData(
        sunrise=sunrise,
        sunset=sunset,
        weather_code=weather_code,
        weather_icon=WEATHER_ICON_BY_CODE.get(weather_code),
    )

  def get_current_icon(self) -> Optional[Image.Image]:
    if self.current_forecast:
      now = datetime.datetime.now()
      if now < self.current_forecast.sunrise or self.current_forecast.sunset < now:
        return self.weather_image_by_icon.get('moon')
      else:
        return self.weather_image_by_icon.get(self.current_forecast.weather_icon)
    else:
      return None


if __name__ == '__main__':
  weather = WeatherService(latitude=52.52, longitude=13.41)
  while True:
    print(weather.current_forecast)
    time.sleep(5)
