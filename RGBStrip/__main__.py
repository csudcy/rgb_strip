#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import pickle
import shutil
import traceback
from typing import Optional

import click

from RGBStrip.manager import RGBStripManager


@click.group()
def main() -> None:
  """Validate, diff, and convert Kintaro schemas!"""


@main.command()
@click.argument('config')
def run(config: str):
  # Create the manager from config
  manager = RGBStripManager(config)

  # Block on the manager thread
  manager.output_forever()


@main.command()
@click.argument('config')
@click.option('--host', help='The host for the web server to bind to')
@click.option('--port', help='The port for the web server to bind to', type=int)
def server(
    config: str,
    host: Optional[str],
    port: Optional[int],
):
  # Import this here so we don't require gevent when not using the server
  from RGBStrip import server

  # Create the manager from config
  manager = RGBStripManager(config)

  # Start the server (non-blocking)
  kwargs = {}
  if host:
    kwargs['host'] = host
  if port:
    kwargs['port'] = port
  server.start_server(manager, **kwargs)

  # Block on the manager thread
  manager.output_forever()


@main.command()
@click.argument('config')
@click.argument('directory')
def render(
    config: str,
    directory: Optional[str],
):
  # Create the manager from config
  manager = RGBStripManager(config)

  print('Rendering...')
  rendered = manager.CONFIG.RENDERER.render_to_memory(manager.CONFIG.CONTROLLER)

  print('Saving...')
  if isinstance(rendered, dict):
    rendered = [rendered]
  for render in rendered:
    # Check this renderer has a name
    name = render["name"]
    if not name:
      print('Cannot save renders without a name!')
      continue
    print(f'{name}: Rendering...')

    # Make sure the output directory exists & is clear
    render_directory = os.path.join(directory, name)
    if os.path.exists(render_directory):
      print(f'{name}: Removing directory...')
      shutil.rmtree(render_directory)
    print(f'{name}: Adding directory...')
    os.makedirs(render_directory)

    # Save the frames
    frames = render.pop('frames')
    frame_lengths = []
    framedata_path = os.path.join(render_directory, f'data.pickle')
    with open(framedata_path, 'wb') as f:
      for frame_count, frame in enumerate(frames):
        if frame_count % 100 == 0:
          print(f'{name}: Saved {frame_count} frames...')
        frame_dumped = pickle.dumps(frame)
        frame_lengths.append(len(frame_dumped))
        f.write(frame_dumped)
    print(f'{name}: Saved {frame_count} frames')

    # Save the init.pickle file
    render['frame_lengths'] = frame_lengths
    print(f'{name}: Writing init.pickle...')
    with open(os.path.join(render_directory, f'init.pickle'), 'wb') as f:
      pickle.dump(render, f)
    print(f'{name}: Done!')

  print('Done!')


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
