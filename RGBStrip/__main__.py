#!/usr/bin/python
# -*- coding: utf8 -*-
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


if __name__ == "__main__":
  main()
