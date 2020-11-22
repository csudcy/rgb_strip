#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import pickle
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
  if not isinstance(rendered, list):
    rendered = [rendered]
  for render in rendered:
    # Check this renderer has a name
    name = render["name"]
    if not name:
      print('  Cannot save renders without a name!')
      continue

    # Save the render
    print(f'  {name}...')
    with open(os.path.join(directory, f'{name}.pickle'), 'wb') as f:
      pickle.dump(render, f)

  print('Done!')


if __name__ == "__main__":
  main()
