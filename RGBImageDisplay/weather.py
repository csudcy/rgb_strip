#!/usr/bin/python
# -*- coding: utf8 -*-
from dataclasses import dataclass
from datetime import timedelta
import pathlib
import threading
from typing import Optional

import requests_cache
import retry_requests



CURRENT_DIRECTORY = pathlib.Path(__file__).parent
WEATHER_DIRECTORY = CURRENT_DIRECTORY / 'weather'
"""
See https://open-meteo.com/en/docs
0 - Clear sky
1, 2, 3 - Mainly clear, partly cloudy, and overcast
45, 48 - Fog and depositing rime fog
51, 53, 55 - Drizzle: Light, moderate, and dense intensity
56, 57 - Freezing Drizzle: Light and dense intensity
61, 63, 65 - Rain: Slight, moderate and heavy intensity
66, 67 - Freezing Rain: Light and heavy intensity
71, 73, 75 - Snow fall: Slight, moderate, and heavy intensity
77 - Snow grains
80, 81, 82 - Rain showers: Slight, moderate, and violent
85, 86 - Snow showers slight and heavy
95 - Thunderstorm: Slight or moderate
96, 99 - Thunderstorm with slight and heavy hail
"""
WEATHER_CODE_MAP = {}



@dataclass
class ImageInfo:
  parent: str


class WeatherService(threading.Thread):

  def __init__(self):
    # Make an open-meteo session
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    self.session = retry_requests.retry(cache_session,
                                        retries=5,
                                        backoff_factor=0.2)

  # TODO: Cache this!
  def _fetch_weather(self) -> Optional[str]:
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        # TODO: Get lat/lng from CLI args
        'latitude': 52.52,
        'longitude': 13.41,
        'hourly': ['temperature_2m', 'weather_code'],
        'forecast_days': 1
    }
    response = self.session.get(url, params=params)
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
    start_times = hourly['time']
    temperatures = hourly['temperature_2m']
    weather_codes = hourly['weather_code']
    combined = zip(start_times, temperatures, weather_codes)

    one_hour = timedelta(hours=1)

    for start_time, temperature, weather_code in combined:
      print((start_time, temperature, weather_code))

    import pdb
    pdb.set_trace()

    return None

  def _get_current_weather_icon(self) -> Optional[str]:
    pass
