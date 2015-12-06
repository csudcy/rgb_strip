#!/usr/bin/python
# -*- coding: utf8 -*-
from .base import BaseRenderer


class PatchRenderer(BaseRenderer):
    def __init__(self, width, height=1, rgb_colours=((255, 0, 0), ), a=1):
        super(PatchRenderer, self).__init__(width, height)

        self.RGB_COLOURS = rgb_colours
        self.A = a
        self.INDEX = 0

    def render(self):
        rgb_colour = self.RGB_COLOURS[self.INDEX]
        for output in self.OUTPUTS:
            for x in xrange(self.WIDTH):
                for y in xrange(self.HEIGHT):
                    output.RGB_STRIP.add_led_xy(output.X + x, output.Y + y, *rgb_colour, a=self.A)
        self.INDEX = (self.INDEX + 1) % len(self.RGB_COLOURS)


def test_patch(rgb_strip):
    """
    Cycle the whole strip through a rainobw of colours
    """
    r = PatchRenderer(rgb_strip.WIDTH, rgb_strip.HEIGHT, RGBStrip.get_rgb_rainbow(250, max_rgb=32))
    r.add_output('Patch', rgb_strip, 0, 0)
    rgb_strip.output_forever()

def main():
    print 'Hello!'
    rgb_strip = None
    try:
        print 'Initialising...'
        GPIO.setmode(GPIO.BCM)
        rgb_strip = RGBStrip(
            width=60,
            height=2
        )

        print 'Testing rgb_strip...'
        test_patch(rgb_strip)

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
