#!/usr/bin/python
# -*- coding: utf8 -*-

class ConeSection(object):
    """
    Allow a cone of an RGBStrip to be controlled.
    """
    def __init__(
            self,
            controller,
            active=True,
            reverse_angle=False
        ):
        self.CONTROLLER = controller
        self.ACTIVE = active
        self.REVERSE_ANGLE = reverse_angle

        # Copy here for easy access
        self.LEVELS = controller.LEVELS

    def add_led(self, angle, level, colour):
        if self.ACTIVE:
            aa, al = self._get_absolute_al(angle, level)
            self.CONTROLLER.add_led(aa, al, colour)

    def set_led(self, angle, level, colour):
        if self.ACTIVE:
            aa, al = self._get_absolute_al(angle, level)
            self.CONTROLLER.set_led(aa, al, colour)

    def _get_absolute_al(self, angle, level):
        if self.REVERSE_ANGLE:
            angle = 360.0 - angle
        return angle, level
