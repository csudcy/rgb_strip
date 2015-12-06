#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.renderers.base import BaseRenderer


class RainbowRenderer(BaseRenderer):
    def __init__(self, width, height=1, train_length=10, max_rgb=127):
        super(RainbowRenderer, self).__init__(width, height)

        self.COLOURS = utils.get_rgb_rainbow(train_length, max_rgb=max_rgb)
        self.X = 0
        self.Y = 0

    def render(self):
        for output in self.OUTPUTS:
            # Output the colours
            x, y = self.X, self.Y
            for i, colour in enumerate(self.COLOURS):
                x, y = RGBStrip.xy_inc(x, y, self.WIDTH, self.HEIGHT)
                #print 'Out', output.ID, x, y, output.X + x, output.Y + y, self.WIDTH, self.HEIGHT
                output.RGB_STRIP.add_led_xy(output.X + x, output.Y + y, *colour, a=1)

        # Move the train along
        self.X, self.Y = RGBStrip.xy_inc(self.X, self.Y, self.WIDTH, self.HEIGHT)


def test_rainbow_train(rgb_strip):
    """
    Make a small rainbow move along the strip & cycle round
    """
    rt = RainbowRenderer(rgb_strip.WIDTH, rgb_strip.HEIGHT, 10)
    rt.add_output('RT', rgb_strip, 0, 0)
    rgb_strip.output_forever()


def test_rainbow(rgb_strip):
    """
    Make the whole strip into a cycling rainbow
    """
    rt = RainbowRenderer(rgb_strip.WIDTH, rgb_strip.HEIGHT, rgb_strip.WIDTH * rgb_strip.HEIGHT)
    rt.add_output('RT', rgb_strip, 0, 0)
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
        #test_rainbow_train(rgb_strip)
        #test_rainbow(rgb_strip)

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
