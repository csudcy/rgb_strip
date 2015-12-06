#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime

from .base import BaseRenderer


class ClockRenderer(BaseRenderer):
    def __init__(self):
        super(ClockRenderer, self).__init__(60, 1)

    def render(self):
        now = datetime.now()
        for output in self.OUTPUTS:
            output.RGB_STRIP.add_led_xy(output.X + now.hour, output.Y, r=255, a=1)
            output.RGB_STRIP.add_led_xy(output.X + now.minute, output.Y, g=255, a=1)
            output.RGB_STRIP.add_led_xy(output.X + now.second, output.Y, b=255, a=1)


def test_clock(rgb_strip):
    """
    A clock! Hours=Red, Minutes=Green, Seconds=Blue
    """
    clock = ClockRenderer()
    for y in xrange(rgb_strip.HEIGHT):
        clock.add_output('RT', rgb_strip, 0, y)
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
