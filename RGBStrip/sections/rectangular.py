#!/usr/bin/python
# -*- coding: utf8 -*-

class RectangularSection(object):
    """
    Allow a section of and RGBStrip to be controlled
    """
    def __init__(
            self,
            controller,
            x,
            y,
            width,
            height,
            active=True,
            reverse_x=False,
            reverse_y=False
        ):
        self.CONTROLLER = controller
        self.X = x
        self.Y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.ACTIVE = active
        self.REVERSE_X = reverse_x
        self.REVERSE_Y = reverse_y

    def add_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        if self.ACTIVE:
            ax, ay = self._get_absolute_xy(x, y)
            self.CONTROLLER.add_led_xy(ax, ay, r=r, g=g, b=b, a=a)

    def set_led_xy(self, x, y, r=0, g=0, b=0, a=0):
        if self.ACTIVE:
            ax, ay = self._get_absolute_xy(x, y)
            self.CONTROLLER.set_led_xy(ax, ay, r=r, g=g, b=b, a=a)

    def increment_xy(self, x, y):
        # Move to the next column
        x += 1
        if x >= self.WIDTH:
            # Move to the next row
            x = 0
            y += 1
            if y >= self.HEIGHT:
                y = 0
        return x, y

    def _get_absolute_xy(self, x, y):
        x = x % self.WIDTH
        y = y % self.HEIGHT
        if self.REVERSE_X:
            x = self.WIDTH - x - 1
        if self.REVERSE_Y:
            y = self.HEIGHT - y - 1
        return self.X + x, self.Y + y
