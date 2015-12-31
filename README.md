# rgb_strip
A controller for addressable RGB LED strips with multiple outputs (mainly, Raspberry Pi)


To use SPI mode:
  * sudo apt-get update
  * sudo apt-get upgrade
  * sudo raspi-config
    * Advanced options
    * SPI
    * Enable
  * sudo pip install spidev
*Note:* It seems like SPI mode cannot be used if any of the pins have been used by GPIO (reboot to fix).


To run on startup:
  * `sudo ln -s /home/pi/rgb_strip/init.d/rgbs /etc/init.d`
  * `sudo update-rc.d rgbs defaults`


TODO:
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
