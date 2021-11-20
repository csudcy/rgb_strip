from contextlib import contextmanager
import logging
import pathlib
import time

import click
import config as config_loader

LOGGER = logging.getLogger(__name__)


@contextmanager
def time_it(name: str) -> None:
  LOGGER.info(f'{name}...')
  start_time = time.time()
  yield
  diff_time = time.time() - start_time
  LOGGER.info(f'{name} done in {diff_time:.02f}s!')


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
  LOGGER.info('Filtering...')
  directory_path = directory.resolve()
  if filter:
    effects = [effect for effect in config_.effects if filter in effect.name]
    print(f'  Skipped {len(config_.effects) - len(effects)}...')
  else:
    effects = config_.effects

  # Ensure all directories are created
  LOGGER.info('Creating directories...')
  for effect in effects:
    filename = effect.get_filepath(directory)
    filename.parent.mkdir(parents=True, exist_ok=True)

  with time_it('Rendering effects'):
    for effect in effects:
      with time_it(f'Rendering {effect.name}'):
        effect.render(directory_path)


if __name__ == "__main__":
  main()
