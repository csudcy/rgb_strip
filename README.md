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


TODO:
    Everything!
    Make RainbowTrain loop instead of jumping back to x=0 every line
    Add_led is buggy - if value is > 255, it should be 255 (not value & 255)
