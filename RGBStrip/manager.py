#!/usr/bin/python
# -*- coding: utf8 -*-
from threading import Thread
import time

from RGBStrip import config_loader

class RGBStripManager(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.CONTROLLER = None

        # Setup a list of renderers & displays
        self.RENDERERS = []
        self.DISPLAYS = []

    def load_config(self, path):
        # Clear existing config
        for renderer in self.RENDERERS:
            renderer.stop()
        for display in self.DISPLAYS:
            display.stop()

        # Make everything new
        config = config_loader.load_config(path)

        # Save evrything
        self.set_controller(config['controller'])
        self.RENDERERS = config['renderers']
        self.DISPLAYS = config['displays']

    def set_controller(self, controller):
        self.CONTROLLER = controller

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
            self.IS_ALIVE = True
            while (self.IS_ALIVE):
                self.output()
                time.sleep(sleep_time)
        finally:
            print 'Executing my finally!'
            for display in self.DISPLAYS:
                display.safe_teardown()

    def run(self):
        self.output_forever()

    def stop(self):
        self.IS_ALIVE = False