# rgb_strip

A controller for addressable RGB LED strips with multiple outputs (mainly, Raspberry Pi).


## General Setup

* On the Pi, make sure everything is up-to-date:
  * `sudo apt-get update`
  * `sudo apt-get upgrade`
* You might need to:
  * `sudo apt-get install python-pip`
  * `sudo apt-get install python-tk`
* To use SPI (`Serial Peripheral Interface`) on the Pi:
  * `sudo raspi-config`
    * `Interfacing Options`
    * `SPI`
    * `Enable`
  * `sudo pip install spidev`
* Install all the required libraries:
  * Install [Poetry](https://python-poetry.org/docs/#installation):
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
  * Install requirements:
```
# To install command line & web
npm run poetry:install

# To install with SPI (only on Raspberry Pi)
npm run poetry:install:spi
```
  * **NOTE:** This can take **very** long time on the Pi (like **30 minutes** long!)

*Note:* It seems like SPI mode cannot be used if any of the pins have been used by GPIO (reboot to fix).


## Run For Development

* Run:
```
npm run serve:test

# To use a different YAML file
npm run serve configs/cone.yaml
```
* Go to http://localhost:8080/


## Run On Startup

* Create a `prod.yaml` config.
* Setup the service:
```bash
sudo ln -s /home/pi/rgb_strip/init.d/rgbs.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rgbs
```
* Control the service:
```
sudo systemctl start rgbs
sudo systemctl stop rgbs
sudo systemctl restart rgbs
```


## Connecting LEDs to Raspberry Pi

There are 2 main types of LEDs which can be used:
* [NeoPixel](https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels):
  * E.g. `WS2801`, `WS2812`, `WS2812B`, `WS2812`
  * Controlled by a single pin
* [DotStar](https://learn.adafruit.com/adafruit-dotstar-leds/overview)
  * E.g. `APA102`
  * Controlled by 2 pins

### Connecting NeoPixel's

TODO: Add this once I have some NeoPixels!

### Connecting DotStar's

My DotStar (specifically, `APA102`) has these 4 connections:
* Red - 5v
* Blue - Clock (connect to `SPI0 SCLK`)
* Green - Data (connect to `SPI0 MOSI`)
* Yellow - Ground

[Pinout.xyz](https://pinout.xyz/) is an excellent resource for working out how to plug your LEDs in (it will even [highlight the SPI pins](https://pinout.xyz/pinout/spi))!


## TODO

  * Everything!
  * Make RainbowTrain loop instead of jumping back to x=0 every line
  * Timed sections
  * Rotating sections?
  * Gravity trails
  * Knightrider
  * Cylons
  * Allow web server to choose between multiple configs?
  * Better web UI
  * Config builder web UI
  * Restart websocket on error
  * More config validation?
  * Don't let crashes stop the server
