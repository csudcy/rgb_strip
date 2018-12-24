#!/usr/bin/python
# -*- coding: utf8 -*-
import yaml

from RGBStrip.constants import CONTROLLERS, DISPLAYS, RENDERERS, SECTIONS
from RGBStrip import utils


class Config(object):

    def __init__(self, yaml_config):
        self.YAML_CONFIG = yaml_config

        # Make Everything
        config = yaml.load(yaml_config)

        # Requires nothing
        self.CONTROLLER = self._load_controller(config['controller'])
        self.PALETTES = self._load_palettes(config.get('palettes', {}))
        self.SLEEP_TIME = config.get('general', {}).get('sleep_time', 0.01)

        # Requires CONTROLLER
        self.SECTIONS = self._load_sections(config['sections'])
        self.DISPLAYS = self._load_displays(config['displays'])

        # Requires SECTIONS & PALETTERS
        self.RENDERERS = self._load_renderers(config['renderers'])

    def _load_controller(self, config):
        return CONTROLLERS[config.pop('type')](**config)

    def _load_sections(self, config):
        return {
            id: SECTIONS[params.pop('type')](
                self.CONTROLLER,
                **params
            )
            for id, params in (config or {}).iteritems()
        }

    def _load_palettes(self, config):
        return {
            id: utils.make_palette(**params)
            for id, params in (config or {}).iteritems()
        }

    def _load_renderers(self, config):
        return [
            RENDERERS[renderer.pop('type')](
                self.SECTIONS[renderer.pop('section')],
                self._resolve_palette(renderer.pop('palette', None)),
                **renderer
            )
            for renderer in config or []
        ]

    def _resolve_palette(self, palette):
        # This is either nothing
        if not palette:
            return None

        # Or a named palette
        if palette in self.PALETTES:
            return self.PALETTES[palette]

        # Or is a (list of) named colours
        if not hasattr(palette, '__iter__'):
            palette = [palette]
        return [
            utils.resolve_colour(colour)
            for colour in palette
        ]

    def _load_displays(self, config):
        return [
            DISPLAYS[display.pop('type')](
                self.CONTROLLER,
                **display
            )
            for display in config
        ]
