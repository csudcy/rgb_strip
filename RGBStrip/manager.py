#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import pickle
import random
import time
from threading import Thread

from RGBStrip import config


class RGBStripManager(Thread):

  def __init__(self, config_path):
    Thread.__init__(self)
    self.IS_ALIVE = True

    # Load the config
    self.CONFIG = None
    self.CONFIG_PATH = config_path
    with open(config_path) as f:
      return self.load_config(f.read())

  def load_config(self, yaml_config):
    # Load the config & check it's valid
    print('Loading config from yaml...')
    new_config = config.Config(yaml_config)

    if self.CONFIG:
      # Clear existing config
      if self.CONFIG.RENDERER:
        self.CONFIG.RENDERER.stop()
      for display in self.CONFIG.DISPLAYS:
        display.teardown()

    # Save the new config
    self.CONFIG = new_config

  def get_yaml_config(self):
    return self.CONFIG.YAML_CONFIG

  def apply_config(self, yaml_config):
    """Load the given config & (if successful) overwrite the config on disk.
    """
    # Validate & apply the new config
    self.load_config(yaml_config)

    # Save the new config
    with open(self.CONFIG_PATH, 'wb') as f:
      f.write(yaml_config)

  def output_forever(self):
    try:
      for display in self.CONFIG.DISPLAYS:
        display.setup()
      if self.CONFIG.RENDER_FILES:
        self._render_from_directory()
      else:
        self._render_live()
    except KeyboardInterrupt:
      print('Bye!')
    finally:
      for display in self.CONFIG.DISPLAYS:
        display.safe_teardown()

  def _render_live(self):
    while (self.IS_ALIVE):
      self.CONFIG.CONTROLLER.set_leds((0, 0, 0))
      self.CONFIG.RENDERER.render()
      for display in self.CONFIG.DISPLAYS:
        display.display()
      time.sleep(self.CONFIG.SLEEP_TIME)

  def _render_from_directory(self):
    # Get the config
    directory = self.CONFIG.RENDER_FILES['directory']
    speed = self.CONFIG.RENDER_FILES.get('speed', 1)
    names = self.CONFIG.RENDER_FILES.get('names')

    # Load pre-renders into memory
    renders = []
    print(f'Loading renders from {directory} ...')
    for path in os.listdir(directory):
      print(f'  Loading {path} ...')
      if names and path not in names:
        print('  Not in names; skipped')
        continue

      render_directory = os.path.join(directory, path)
      init_filepath = os.path.join(render_directory, 'init.pickle')
      if not os.path.exists(init_filepath):
        print('  No init.pickle; skipped')
        continue

      with open(init_filepath, 'rb') as f:
        render = pickle.load(f)
      render['framedata_path'] = os.path.join(render_directory, 'data.pickle')
      renders.append(render)

      print(f'   Loaded {render["name"]}!')
    print(f'Loaded {len(renders)} renders!')

    # TODO: Add random start/end points?
    # TODO: Add speed multiplier
    # TODO: Add reverse to render
    next_frame_time = 0
    while (self.IS_ALIVE):
      # Choose a new render
      render = random.choice(renders)
      print(f'New render: {render["name"]}')
      if 'interval_seconds' in render:
        frame_interval = render['interval_seconds'] / speed
      else:
        frame_interval = 0
      frame_count = len(render['frame_lengths'])

      # Open the data file & iterate over the frames
      with open(render['framedata_path'], 'rb') as framedata_file:
        for frame_index, frame_length in enumerate(render['frame_lengths']):
          if frame_index % 100 == 0:
            print(f'Frame {frame_index} / {frame_count}')

          # Load the next frame & send it to controller
          framedata = framedata_file.read(frame_length)
          frame = pickle.loads(framedata)
          self.CONFIG.CONTROLLER.set_frame(frame)

          # Update the displays
          for display in self.CONFIG.DISPLAYS:
            display.display()

          # Wait until it's time to display the next frame
          while time.time() <= next_frame_time:
            time.sleep(self.CONFIG.SLEEP_TIME)
          next_frame_time = time.time() + frame_interval

  def run(self):
    self.output_forever()

  def stop(self):
    self.IS_ALIVE = False
