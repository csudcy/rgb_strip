# rgb_strip

A controller for addressable RGB LED strips with multiple outputs (mainly, Raspberry Pi).


## Development

### Setup

* Install [Poetry](https://python-poetry.org/docs/#installation):
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python2 -
```
* Install requirements:
```
# To install command line & web
npm run poetry:install
```


### Running

* Run:
```
npm run serve:test

# To use a different YAML file
npm run serve configs/cone.yaml
```
* Go to http://localhost:8080/


## Raspberry Pi

### Setup

* To use SPI (`Serial Peripheral Interface`) on the Pi:
  * `sudo raspi-config`
    * `Interfacing Options`
    * `SPI`
    * `Enable`
* Update everything & install requirements:
```
# Update everything
sudo apt-get update
sudo apt-get upgrade

# Install things which don't come with defaut Raspberry Pi OS (lite at least)
sudo apt-get install --upgrade git cmake python3-pip

# Now we have to update pip...
python3 -m pip install --upgrade pip

# Restart (just to be safe)
sudo shutdown -r now

# Install requirements
python3 -m pip install -r requirements.txt
```

**Note:** Each upddate/install can take **very** long time on the Pi (**30+ minutes** long depending on your Pi model & SD card).

**Note:** It seems like SPI mode cannot be used if any of the pins have been used by GPIO (reboot to fix).

### Using SPI for WS2812b Poxles

Because there's no clock signal for WS2812b pixles, the timing is very important. Therefore, you should really be using SPI for WS2812b pixels. Unfortunately, it seems like having to do multiple SPI writes is too slow. Therefore, we have to make sure the data for all pixels can be sent in one go. But, that's limited by the buffer size.

WS2812b pixels use 9 bytes per pixel (3 channels and 3 bytes per channel). Therefore, the maximum number of pixels which can be sent in one go are:
```
Buffer   Pixels
 4,096      455
 8,192      910
16,384    1,820
32,768    3,640
65,536    7,281
```
Note: Buffer size is limited to 65,536 bytes by the hardware DMA buffer.

Therefore, if you need 455 pixels or less, you can take the easy route:
```
python3 -m pip install spidev
```

If you need more pixels, we need to increase the SPIdev buffer (see [this issue](https://github.com/doceme/py-spidev/issues/62) for more info):
```
# Get the latest spidev source
cd ~
curl https://codeload.github.com/doceme/py-spidev/zip/master --output spidev.zip
unzip spidev.zip

# Change the system buffer size
sudo nano /boot/cmdline.txt
# Add " spidev.bufsiz=65536" at the end of the line
# Write - ctrl+o then enter
# Quit - ctrl+x

# Change the spidev buffer size & install
cd py-spidev-master
sed spidev_module.c -e "s/4096/65536/g" -i
make PYTHON=python3
sudo python3 setup.py install

# Reboot to apply changes
sudo shutdown -r now
```

### Running

* Create a config file: `cp ./configs/test.yaml ./configs/prod.yaml`
* Test the server: `python3 -m RGBStrip server ./configs/prod.yaml`
* Check the server is running on http://raspberrypi.local:8080
  * If the .local address doesn't work, you'll need to find the IP address of your Pi & use that.
* Once that's working, you can stop it & set it to run at startup:
```bash
# Setup the service
sudo ln -s /home/pi/rgb_strip/init.d/rgbs.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rgbs

# Control the service
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
