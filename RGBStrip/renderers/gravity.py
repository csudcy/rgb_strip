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


def test_gravity(rgb_strip):
    """
    Shoot colours from one end and watch gravity pull them back down
    """
    COLOURS = RGBStrip.get_rgb_rainbow(10)
    SHOTS = []
    MIN_SPEED = 0.5
    MAX_SPEED = 1.0
    G_SPEED = MAX_SPEED / (rgb_strip.WIDTH * 2)
    print 'MAX_SPEED = {}'.format(MAX_SPEED)
    print 'WIDTH     = {}'.format(rgb_strip.WIDTH)
    print 'G_SPEED   = {}'.format(G_SPEED)

    while True:
        # Simulate existing shots
        for shot in SHOTS:
            # Update position
            shot['position'] += shot['speed']
            # Update speed
            shot['speed'] -= G_SPEED

        # Remove old shots
        SHOTS = [
            shot
            for shot in SHOTS
            if shot['position'] > 0
        ]

        # Add a new shot?
        if random.random() < 0.2 / (len(SHOTS) + 1):
            print 'Adding a shot! {count} existing'.format(count=len(SHOTS))
            SHOTS.append({
                'colour': random.choice(COLOURS),
                'speed': random.uniform(MIN_SPEED, MAX_SPEED),
                'position': 0.0
            })

        # Clear all the LEDs
        rgb_strip.set_leds(a=1)

        # Show all the shots
        for shot in SHOTS:
            for y in xrange(rgb_strip.HEIGHT):
                rgb_strip.add_led_xy(
                    int(shot['position']),
                    y,
                    *shot['colour']
                )

        # Update the output
        rgb_strip.output()

        time.sleep(0.02)

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
