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
  if filter:
    effects = [effect for effect in config_.effects if filter in effect.name]
    print(f'  Skipped {len(config_.effects) - len(effects)}...')
  else:
    effects = config_.effects

  for index, effect in enumerate(effects):
    LOGGER.info(f'({index} / {len(effects)}) Rendering {effect.name}...')
    effect.render(directory_path)


if __name__ == "__main__":
  main()
