#!/usr/bin/python
# -*- coding: utf8 -*-
from threading import Thread
import time

from RGBStrip import config_loader


class RGBStripManager(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.CONTROLLER = None
        self.SLEEP_TIME = 0.01
        self.CONFIG_PATH = None

        # Setup a list of renderers & displays
        self.RENDERERS = []
        self.DISPLAYS = []

    def load_config(self, path=None, yaml_config=None):
        # Load the config & check it's valid
        if yaml_config:
            config = config_loader.load_config(yaml_config)
        else:
            self.CONFIG_PATH = path
            config = config_loader.load_config_path(path)

        # Clear existing config
        for renderer in self.RENDERERS:
            renderer.stop()
        for display in self.DISPLAYS:
            display.teardown()

        # Save evrything
        self.set_controller(config['controller'])
        self.RENDERERS = config['renderers']
        self.DISPLAYS = config['displays']
        self.SLEEP_TIME = config['general'].get('sleep_time', 0.01)
        self.YAML_CONFIG = config['yaml_config']

    def apply_config(self, yaml_config):
        """
        Load the given config & (if successful) overwrite the config on disk
        """
        if self.CONFIG_PATH is None:
            raise Exception('To apply_config, you must first load_config using a path!')

        # Validate & apply the new config
        self.load_config(yaml_config=yaml_config)

        # Save the new config
        with open(self.CONFIG_PATH, 'w') as f:
            f.write(yaml_config)

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

    def output_forever(self):
        try:
            for display in self.DISPLAYS:
                display.setup()
            self.IS_ALIVE = True
            while (self.IS_ALIVE):
                self.output()
                time.sleep(self.SLEEP_TIME)
        except KeyboardInterrupt:
            print 'Bye!'
        finally:
            for display in self.DISPLAYS:
                display.safe_teardown()

    def run(self):
        self.output_forever()

    def stop(self):
        self.IS_ALIVE = False