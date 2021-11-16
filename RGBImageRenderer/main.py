import logging
import os
import pathlib

import click
import config as config_loader

LOGGER = logging.getLogger(__name__)


@click.group()
def main() -> None:
  """Render moving images based on configurable effects!"""


@main.command()
@click.argument('config', type=pathlib.Path)
@click.argument('directory', type=pathlib.Path)
@click.option('--filter', help='Filter images rendered by name', type=str)
@click.option('--debug',
              help='Enable debug output',
              type=bool,
              default=False,
              is_flag=True)
def render(
    config: pathlib.Path,
    directory: pathlib.Path,
    filter: str,
    debug: bool,
):
  if debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  LOGGER.info('Loading config...')
  config_ = config_loader.Config.from_file(config)
  LOGGER.info('Rendering effects...')
  directory_path = directory.resolve()
  directory_path.mkdir(parents=True, exist_ok=True)
  for index, effect in enumerate(config_.effects):
    LOGGER.info(
        f'({index} / {len(config_.effects)}) Rendering {effect.name}...')
    effect.render(directory_path)


if __name__ == "__main__":
  main()
