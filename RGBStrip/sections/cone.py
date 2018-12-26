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
        ):
        self.CONTROLLER = controller
        self.ACTIVE = active

        # Copy here for easy access
        self.LEVELS = controller.LEVELS

    def add_led(self, angle, level, colour):
        if self.ACTIVE:
            level_index = self._get_index_by_angle(angle, level)
            self.CONTROLLER.add_led(level_index, level, colour)

    def set_led(self, angle, level, colour):
        if self.ACTIVE:
            level_index = self._get_index_by_angle(angle, level)
            self.CONTROLLER.set_led(level_index, level, colour)

    def set_led_by_level_index(self, level_index, level, colour):
        if self.ACTIVE:
            self.CONTROLLER.set_led(level_index, level, colour)

    def _get_index_by_angle(self, angle, level):
        return int(angle/360.0 * self.CONTROLLER.LEVELS[level])
