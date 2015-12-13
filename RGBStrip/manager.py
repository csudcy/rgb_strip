#!/usr/bin/python
# -*- coding: utf8 -*-
import time


class RGBStripManager(object):
    def __init__(self, controller):
        self.CONTROLLER = controller

        # Setup a list of renderers & displays
        self.RENDERERS = []
        self.DISPLAYS = []

    def add_renderer(self, renderer):
        if renderer not in self.RENDERERS:
            self.RENDERERS.append(renderer)

    def add_display(self, display):
        if display not in self.DISPLAYS:
            self.DISPLAYS.append(display)

    def render(self):
        """
        Render all registered renderers
        """
        for renderer in self.RENDERERS:
            renderer.render()

    def display(self):
        """
        Display all registered displays
        """
        for display in self. DISPLAYS:
            display.display()

    def output(self):
        """
        Clear all LEDs, render and then display the results
        """
        self.CONTROLLER.set_leds()
        self.render()
        self.display()

    def output_forever(self, sleep_time=0.01):
        try:
            for display in self.DISPLAYS:
                display.setup()
            while (True):
                self.output()
                time.sleep(sleep_time)
        finally:
            for display in self.DISPLAYS:
                try:
                    display.safe_teardown()
                except Exception, ex:
                    print 'Exception '
