#!/usr/bin/python
# -*- coding: utf8 -*-
from threading import Thread
import time

from RGBStrip import config


class RGBStripManager(Thread):
    def __init__(self, config_path):
        Thread.__init__(self)

        # Load the config
        self.CONFIG = None
        self.CONFIG_PATH = config_path
        with open(config_path) as f:
            return self.load_config(f.read())

    def load_config(self, yaml_config):
        # Load the config & check it's valid
        print 'Loading config from yaml...'
        new_config = config.Config(yaml_config)

        if self.CONFIG:
            # Clear existing config
            self.CONFIG.RENDERER.stop()
            for display in self.CONFIG.DISPLAYS:
                display.teardown()

        # Save the new config
        self.CONFIG = new_config

    def get_yaml_config(self):
        return self.CONFIG.YAML_CONFIG

    def apply_config(self, yaml_config):
        """
        Load the given config & (if successful) overwrite the config on disk
        """
        # Validate & apply the new config
        self.load_config(yaml_config)

        # Save the new config
        with open(self.CONFIG_PATH, 'w') as f:
            f.write(yaml_config)

    def output_forever(self):
        try:
            for display in self.CONFIG.DISPLAYS:
                display.setup()
            self.IS_ALIVE = True
            while (self.IS_ALIVE):
                self.CONFIG.CONTROLLER.set_leds((0, 0, 0))
                self.CONFIG.RENDERER.render()
                for display in self.CONFIG.DISPLAYS:
                    display.display()
                time.sleep(self.CONFIG.SLEEP_TIME)
        except KeyboardInterrupt:
            print 'Bye!'
        finally:
            for display in self.CONFIG.DISPLAYS:
                display.safe_teardown()

    def run(self):
        self.output_forever()

    def stop(self):
        self.IS_ALIVE = False
