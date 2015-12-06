#!/usr/bin/python
# -*- coding: utf8 -*-
from collections import namedtuple
from datetime import datetime
import math
import random
import time

import RPi.GPIO as GPIO

from gpio_22 import GPIO22
from lcd import LCD


def test_many(rgb_strip):
    r = PatchRenderer(5, 2)
    r.add_output('Patch-Red', rgb_strip, 5, 0)

    r = PatchRenderer(5, 2, RGBStrip.get_rgb_rainbow(250, max_rgb=32))
    r.add_output('Patch-Rainbow', rgb_strip, 15, 0)

    r = RainbowTrainRenderer(30, 1)
    r.add_output('RT-30x10', rgb_strip,  0, 0)

    r = RainbowTrainRenderer(30, 1, train_length=30)
    r.add_output('RT-30x30', rgb_strip,  30, 0)

    r = RainbowTrainRenderer(60, 1)
    r.add_output('RT-60x10', rgb_strip,  0, 1)

    r = ClockRenderer()
    r.add_output('Clock', rgb_strip, 0, 1)

    rgb_strip.output_forever()


def main():
    print 'Hello!'
    rgb_strip = None
    try:
        print 'Initialising...'
        GPIO.setmode(GPIO.BCM)
        rgb_strip = RGBStrip(
            #led_count=120,
            width=60,
            height=2,
            #pin_data=GPIO22.MOSI,
            #pin_clock=GPIO22.SCLK,
        )

        print 'Testing rgb_strip...'
        #test_brightness(rgb_strip)
        #test_rainbow_train(rgb_strip)
        #test_rainbow(rgb_strip)
        #test_clock(rgb_strip)
        #test_patch(rgb_strip)
        test_gravity(rgb_strip)
        test_many(rgb_strip)

    except KeyboardInterrupt:
        pass
    finally:
        print 'Cleaning up...'
        if rgb_strip and rgb_strip.SPI:
            rgb_strip.SPI.close()
        else:
            GPIO.cleanup()
    print 'Bye!'


if __name__ == '__main__':
    main()
