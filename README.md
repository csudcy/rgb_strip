# rgb_strip

A controller for addressable RGB LED strips with multiple outputs (mainly, Raspberry Pi).


## Run For Development

* Make a config
* Run `python -m RGBStrip --server ./configs/test.yaml`
* Go to http://localhost:8080/


## Run On Startup

  * Create a `prod.yaml` config.
  * `sudo ln -s /home/pi/rgb_strip/init.d/rgbs /etc/init.d`
  * `sudo update-rc.d rgbs defaults`
  * `service rgbs start`


## Connecting LEDs to Raspberry Pi

There are 2 main types of LEDs which can be used:
* [NeoPixel](https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels):
  * E.g. `WS2801`, `WS2812`, `WS2812B`, `WS2812`
  * Controlled by a single pin
* [DotStar](https://learn.adafruit.com/adafruit-dotstar-leds/overview)
  * E.g. `APA102`
  * Controlled by 2 pins

### Setup SPI

The best way to control your LEDs is via SPI (`Serial Peripheral Interface`); to set it up:

  * `sudo apt-get update`
  * `sudo apt-get upgrade`
  * `sudo raspi-config`
    * Advanced options
    * SPI
    * Enable
  * `sudo pip install spidev`

*Note:* It seems like SPI mode cannot be used if any of the pins have been used by GPIO (reboot to fix).

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
