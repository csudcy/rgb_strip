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

I use a Raspberry Pi to drive my lights. Specifically, a [Rasperry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/). Once you've got one & an SD card you'll need to choose an OS; I've tried with:
* [Raspberry Pi OS](https://www.raspberrypi.org/software/) - The defacto standard for running a Pi
* [DietPi](https://dietpi.com/) - In an attempt to get faster boots, I (unsuccessfully so far) tried to use this.

Some common notes:
* Each upddate/install below can take **very** long time on the Pi (**30+ minutes** long depending on your Pi model & SD card).
* It seems like SPI mode cannot be used if any of the pins have been used by GPIO (reboot to fix).

### 1a. Raspberry Pi OS

* Download [Raspberry Pi Image](https://www.raspberrypi.com/software/)
* Go through the imaging process
  * You can use the "Lite" version cause we don't need a desktop environment running
  * Set a host name e.g. `rpi-display`
  * Setup a user e.g. `pi`
  * Setup WiFi
  * Enable SSH
  * Flash it
* Boot the Pi
  * On first boot, the partition will be resized
* `ssh pi@rpi-display.local`, password is what you entered in the Imager
* To enable the SPI interface:
  * `sudo raspi-config`
    * `Interface Options`
    * `SPI`
    * `Enable`
* Update everything & install requirements:
```
# Update everything
sudo apt-get update
sudo apt-get full-upgrade

# Install things which don't come with defaut Raspberry Pi OS (lite at least)
sudo apt-get install --upgrade git cmake python3-pip

# For Pillow support
sudo apt-get install libopenjp2-7 libtiff5

# Now we have to update pip...
python3 -m pip install --upgrade pip

# Restart (just to be safe)
sudo shutdown -r now
```
* Now continue with the `Remaining Setup` instructions

### 1b. DietPi

I'm trying out [Diet Pi](https://dietpi.com) in an attempt to get faster boot times - maybe even a faster server!

**NOTE**: I ran into an issue where DietPi wouldn't properly drive the pixels (the first one would just flash green) so gave & moved back to Raspberry Pi OS. Good luck if you try DietPi!

* Get DietPi & flash it
* On the boot partition, edit:
  * `dietpi.txt`
    * `AUTO_SETUP_ACCEPT_LICENSE=1` So you don't have to manually accept the license
    * `AUTO_SETUP_NET_WIFI_ENABLED=1` So you don't have to manually start the wifi
    * `AUTO_SETUP_AUTOMATED=1` So it goes through the setup automatically
    * `CONFIG_BOOT_WAIT_FOR_NETWORK=2` Make the boot wait infinitely for network
    * `CONFIG_SERIAL_CONSOLE_ENABLE=0` We don't need the serial console so disable it
  * `dietpi-wifi.txt` - Setup your wifi details
    * **Note**: This is only used on first boot; if you forget to set it, the easiest thing to do it re-flash & start again.
    * `aWIFI_SSID`
    * `aWIFI_KEY`
  * `config.txt` (Note, when running, this is at `/boot/config.txt` and can be edited using `nano`)
    * `dtparam=spi=on`
* Boot the Pi
  * On first boot, the partition will be resized and everything will be updated (so it can take a while)
* `ssh root@<IP>`, password `dietpi`
* If you want to, you can change the boot wait for network setting in `/boot/dietpi.txt` by set `CONFIG_BOOT_WAIT_FOR_NETWORK=1`
  * You can set `CONFIG_BOOT_WAIT_FOR_NETWORK=0` (so boot doesn't wait for network). However, this made `timesyncd` take a long time (removing network saved ~5 seconds, `timesyncd` wait was ~60 seconds).
* Install some dependencies
```
# 17=Git, 130=Python3
dietpi-software install 17 130
# TODO: Is this needed?
# apt-get install cmake
apt-get install build-essential libffi-dev
```
* Now continue with the `Remaining Setup` instructions (though you don't need to `sudo` everything since you're logged in as root)

### 2. Using SPI for WS2812b Pixels

Because there's no clock signal for WS2812b pixles, the timing is very important. Therefore, you should really be using SPI (`Serial Peripheral Interface`) for WS2812b pixels. Unfortunately, it seems like having to do multiple SPI writes is too slow. Therefore, we have to make sure the data for all pixels can be sent in one go. But, that's limited by the buffer size.

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

### 3. Remaining Setup

```
# Clone the repo
cd ~
git clone https://github.com/csudcy/rgb_strip
cd rgb_strip

# TODO: Test the new-style pre-rendered images

# [Optional] Test clock using terminal emulator
# Note: Terminal didn't seem to work well over SSH
cd RGBImageDisplay
sudo apt-get install python3-sdl2
sudo python3 -m pip install -r requirements.txt
sudo python3 -m pip install pygame
sudo python3 main.py clock 64 8 --alpha=10

# [Optional] Test clock using ws2182 boards over SPI
cd RGBImageDisplay
sudo python3 -m pip install -r requirements.txt
sudo python3 -m pip install rpi-ws281x
sudo python3 main.py clock 64 8 --alpha=10 --device=ws2812_boards

# Test the old-style server
python3 -m pip install -r requirements.txt
python3 -m RGBStrip server ./configs/test.yaml

# Copy pre-renders to the pi
scp -r ./tree/renders/ pi@rpi-display.local:/home/pi/rgb_strip/tree/renders
```

### Running

* Create a config file: `cp ./configs/test.yaml ./configs/prod.yaml`
* Test the server: `python3 -m RGBStrip server ./configs/prod.yaml`
* Check the server is running on http://raspberrypi.local:8080
  * If the .local address doesn't work, you'll need to find the IP address of your Pi & use that.
  * DietPi defaults to the hostname dieti.local
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


## Image Display Notes

```
# Locally

rm -rf tree/image_renders && npm run image-renderer -- render ../tree/render_new.yaml ../tree/image_renders/ --filter scroll

npm run image-display -- run 12 120 ../tree/image_renders/ --delay=75 --alpha=255 --device=none

git commit --amend --no-edit --author="csudcy <csudcy@gmail.com>" && git rebase --continue

rsync -rvz ./RGBImageDisplay/ pi@192.168.0.67:/home/pi/rgb_strip/RGBImageDisplay/
rsync -rvz ./tree/image_renders/ pi@192.168.0.67:/home/pi/rgb_strip/tree/image_renders/

cd /home/pi/rgb_strip
mv RGBImageDisplay RGBImageDisplay_bak
mv RGBImageDisplay2 RGBImageDisplay
mv tree/image_renders tree/image_renders_bak
mv tree/image_renders2 tree/image_renders
sudo systemctl restart rgbid

scp ./init.d/* pi@192.168.0.67:/home/pi/rgb_strip/init.d/

cd RGBImageDisplay
sudo python3 -m pip install -r requirements.txt
sudo python3 -m pip install rpi-ws281x ws2812
sudo python3 main.py run 120 12 /home/pi/rgb_strip/tree/image_renders/ --delay=5 --alpha=40 --device=ws2812
```
Renderer
  Add rain effect
  Add game of life effect?

Improve display server
  Update config (unsaved?)
  Move specific
  Allow groups/images to be enabled/disabled

Update readme
