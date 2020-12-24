#!/usr/bin/python
# -*- coding: utf8 -*-
import traceback
from typing import Optional

import click

from RGBStrip.manager import RGBStripManager


@click.group()
def main() -> None:
  """Configurable interface for driving addressable RGB LEDs."""


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
  renders = manager.CONFIG.RENDERER.render_all_to_memory(
      manager.CONFIG.CONTROLLER)

  print('Saving...')
  for render in renders:
    render.write(directory)

  print('Done!')


if __name__ == "__main__":
  try:
    main()
  except Exception:
    # Make sure the traceback is printed
    traceback.print_exc()
    raise
