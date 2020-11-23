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
      render['render_directory'] = render_directory
      renders.append(render)

      print(f'   Loaded {render["name"]}!')
    print(f'Loaded {len(renders)} renders!')

    next_frame_time = 0
    frame_indices = iter([])
    while (self.IS_ALIVE):
      # Check if it's time to display the next frame
      if time.time() > next_frame_time:
        try:
          frame_index = next(frame_indices)
        except StopIteration:
          # Move to another render
          current_render = random.choice(renders)
          print(f'New render: {current_render["name"]}')
          if 'interval_seconds' in current_render:
            frame_interval = current_render['interval_seconds'] / speed
          else:
            frame_interval = 0

          # Get the range of indices to use
          # TODO: Add random start/end points?
          # TODO: Add speed multiplier
          frame_count = current_render['frame_count']
          if random.randint(0, 1):
            # Reverse
            frame_indices = iter(range(frame_count - 1, 0, -1))
          else:
            frame_indices = iter(range(frame_count))
          frame_index = next(frame_indices)

        # Set the next frame time
        next_frame_time = time.time() + frame_interval

        # Load the frame
        framepath = os.path.join(current_render['render_directory'],
                                 f'{frame_index:04}.pickle')
        with open(framepath, 'rb') as f:
          frame = pickle.load(f)

        # Send it to controller
        if frame_index % 100 == 0:
          print(f'Frame {frame_index} / {frame_count}')
        self.CONFIG.CONTROLLER.set_frame(frame)

        # Update the displays
        for display in self.CONFIG.DISPLAYS:
          display.display()

      time.sleep(self.CONFIG.SLEEP_TIME)

  def run(self):
    self.output_forever()

  def stop(self):
    self.IS_ALIVE = False
