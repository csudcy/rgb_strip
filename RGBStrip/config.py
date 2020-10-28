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

        # Requires SECTIONS & PALETTES
        self.RENDERER = self.load_renderer(config['renderer'])

    def _load_controller(self, controller_config):
        return CONTROLLERS[controller_config.pop('type')](**controller_config)

    def _load_sections(self, section_configs):
        return {
            id: SECTIONS[params.pop('type')](
                self.CONTROLLER,
                **params
            )
            for id, params in (section_configs or {}).items()
        }

    def _load_palettes(self, palette_configs):
        return {
            id: utils.make_palette(**params)
            for id, params in (palette_configs or {}).items()
        }

    def load_renderer(self, renderer_config):
        return RENDERERS[renderer_config.pop('type')](
            self,
            **renderer_config
        )

    def _load_displays(self, display_configs):
        return [
            DISPLAYS[display.pop('type')](
                self.CONTROLLER,
                **display
            )
            for display in display_configs
        ]

    def resolve_section(self, section_id):
        return self.SECTIONS[section_id]

    def resolve_palette(self, palette):
        # This is either nothing
        if not palette:
            return None

        # Or a list of named colours
        if isinstance(palette, list):
            return [
                utils.resolve_colour(colour)
                for colour in palette
            ]

        # Or a named palette
        if palette in self.PALETTES:
            return self.PALETTES[palette]

        # Or a 'rainbow_{count}' palette
        if palette.startswith('rainbow_'):
            rainbow_steps = int(palette[8:])
            self.PALETTES[palette] = utils.make_palette(rainbow_steps=rainbow_steps)
            return self.PALETTES[palette]

        # Or is a single named colours
        return [utils.resolve_colour(palette)]
