#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from typing import List

import yaml

from RGBStrip import render_file
from RGBStrip import utils
from RGBStrip.constants import CONTROLLERS
from RGBStrip.constants import DISPLAYS
from RGBStrip.constants import RENDERERS
from RGBStrip.constants import SECTIONS


class Config(object):

  def __init__(self, yaml_config):
    self.YAML_CONFIG = yaml_config

    # Make Everything
    config = yaml.load(yaml_config)

    # Requires nothing
    self.CONTROLLER = self._load_controller(config['controller'])
    self.PALETTES = self._load_palettes(config.get('palettes', {}))
    general = config.get('general', {})
    self.SLEEP_TIME = general.get('sleep_time', 0.01)
    self.RENDER_GROUPS = self._load_render_groups(general.get('render_files'))

    # Requires CONTROLLER
    self.SECTIONS = self._load_sections(config.get('sections', []))
    self.DISPLAYS = self._load_displays(config.get('displays', []))

    # Requires SECTIONS & PALETTES
    self.RENDERER = self.load_renderer(config.get('renderer'))

    if not (self.RENDER_GROUPS or self.RENDERER):
      raise Exception('You must define either renderers or render_files')

  def _load_controller(self, controller_config):
    return CONTROLLERS[controller_config.pop('type')](**controller_config)

  def _load_sections(self, section_configs):
    return {
        id: SECTIONS[params.pop('type')](self.CONTROLLER, **params)
        for id, params in (section_configs or {}).items()
    }

  def _load_palettes(self, palette_configs):
    return {
        id: utils.make_palette(**params)
        for id, params in (palette_configs or {}).items()
    }

  def _load_render_groups(
      self, render_files_config) -> List[List[render_file.RenderReader]]:
    if not render_files_config:
      return []

    # Get the config
    directory = render_files_config['directory']
    speed = render_files_config.get('speed', 1)
    name_groups = render_files_config.get('name_groups')

    # Load pre-renders into memory
    print(f'Loading renders from {directory} ...')
    render_groups = []
    for name_group in name_groups:
      render_group = []
      for name in name_group:
        # Check if we want to use this renderer
        print(f'  Loading {name} ...')
        render = render_file.RenderReader.load(directory, name)
        if render:
          # Apply the speed modifier
          render.frame_interval /= speed
          render_group.append(render)
          print(f'    Loaded.')
        else:
          print(f'    Not found!')
      render_groups.append(render_group)
    print(f'Loaded {len(render_groups)} render groups!')

    return render_groups

  def load_renderer(self, renderer_config):
    if renderer_config is None:
      return None
    return RENDERERS[renderer_config.pop('type')](self, **renderer_config)

  def _load_displays(self, display_configs):
    return [
        DISPLAYS[display.pop('type')](self.CONTROLLER, **display)
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
      return [utils.resolve_colour(colour) for colour in palette]

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
