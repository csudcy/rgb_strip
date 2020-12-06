#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import pickle
import yaml

from RGBStrip import utils
from RGBStrip.constants import CONTROLLERS, DISPLAYS, RENDERERS, SECTIONS


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
    self.RENDERS = self._load_renders(general.get('render_files'))

    # Requires CONTROLLER
    self.SECTIONS = self._load_sections(config.get('sections', []))
    self.DISPLAYS = self._load_displays(config.get('displays', []))

    # Requires SECTIONS & PALETTES
    self.RENDERER = self.load_renderer(config.get('renderer'))

    if not (self.RENDERS or self.RENDERER):
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

  def _load_renders(self, render_files_config):
    if not render_files_config:
      return []

    # Get the config
    directory = render_files_config['directory']
    speed = render_files_config.get('speed', 1)
    names = render_files_config.get('names')

    # Load pre-renders into memory
    print(f'Loading renders from {directory} ...')
    renders = []
    for path in os.listdir(directory):
      # Check if we want to use this renderer
      print(f'  Loading {path} ...')
      if names and path not in names:
        print('  Not in names; skipped')
        continue

      # Check this really is a render
      render_directory = os.path.join(directory, path)
      init_filepath = os.path.join(render_directory, 'init.pickle')
      if not os.path.exists(init_filepath):
        print('  No init.pickle; skipped')
        continue

      # Load the renderer
      with open(init_filepath, 'rb') as f:
        render = pickle.load(f)

      # Add some extra config stuff
      if 'interval_seconds' in render:
        frame_interval = render['interval_seconds'] / speed
      else:
        frame_interval = 0
      render.update({
          'frame_count': len(render['frame_lengths']),
          'frame_interval': frame_interval,
          'framedata_path': os.path.join(render_directory, 'data.pickle'),
      })

      renders.append(render)

      print(f'   Loaded {render["name"]}!')
    print(f'Loaded {len(renders)} renders!')

    return renders

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
