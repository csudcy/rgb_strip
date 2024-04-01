# rgb_strip

A controller for addressable RGB LED strips with multiple outputs (mainly, Raspberry Pi).

## Development

### Setup

* Install [Poetry](https://python-poetry.org/docs/#installation):
```
curl -sSL https://install.python-poetry.org | python3 -
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

### Connecting NeoPixel's (WS2812)

NeoPixels's (WS2812) are controlled by a single data pin.

- For old style server, connect to [pin 19 - SPI MOSI](https://pinout.xyz/pinout/pin19_gpio10/)
- For new style image display, connect to [pin 12 - PCM Clock](https://pinout.xyz/pinout/pin12_gpio18/)

### Setup

* Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
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
sudo apt-get install --upgrade git cmake python3-pip libopenjp2-7 libtiff5

# Now we have to update pip...
python3 -m pip install --upgrade pip

# Clone the repo
cd ~
git clone https://github.com/csudcy/rgb_strip

# Install requirements
cd rgb_strip/RGBImageDisplay
sudo python3 -m pip install -r requirements.txt
sudo python3 -m pip install rpi-ws281x

```

### Setup for Image Display

With this, you pre-render images from another computer, upload them to the Pi & the server cycles through displaying those in random order.

```
# Copy pre-renders to the pi from your computer
scp -r ./tree/renders/ pi@rpi-display.local:/home/pi/rgb_strip/tree/renders

sudo python3 main.py run 120 12 /home/pi/rgb_strip/tree/image_renders/ --delay=5 --alpha=40 --device=ws2812
```

### Setup for Clock

This renders a lovely clock!

```
sudo python3 main.py clock 64 8 --alpha=10 --device=ws2812_boards
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
sudo systemctl status rgbs
sudo systemctl stop rgbs
sudo systemctl restart rgbs
```

## Image Display Notes

```
# Locally

rm -rf tree/image_renders && npm run image-renderer -- render ../tree/render_new.yaml ../tree/image_renders/ --filter scroll

npm run image-display -- run 12 120 ../tree/image_renders/ --delay=75 --alpha=255 --device=none
```

Renderer
  Add rain effect
  Add game of life effect?

Improve display server
  Allow groups/images to be enabled/disabled
