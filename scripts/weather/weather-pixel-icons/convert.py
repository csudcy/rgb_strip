# Icons from https://github.com/Dhole/weather-pixel-icons
# Unfortunately, they don't really work at 8x8

import pathlib
import shutil

from PIL import Image

CURRENT_DIRECTORY = pathlib.Path(__file__).parent
SOURCE_DIRECTORY = CURRENT_DIRECTORY / '16'
DEST_DIRECTORY = CURRENT_DIRECTORY / '8'

# Clear the destination directory
if DEST_DIRECTORY.exists():
  print('Removing dest directory...')
  shutil.rmtree(DEST_DIRECTORY)
print('Creating dest directory...')
DEST_DIRECTORY.mkdir()

for index, filepath in enumerate(SOURCE_DIRECTORY.glob('*.xbm')):
  print(f'{index}. {filepath.name}:')
  print('  Loading...')
  try:
    image = Image.open(filepath)
  except Exception as ex:
    print(f'    Error: {ex}')
    continue

  print('  Resizing...')
  image = image.resize((8, 8))
  print('  Converting...')
  image = image.convert('RGB')

  print('  Saving...')
  output_path = DEST_DIRECTORY / f'{filepath.stem}.png'
  image.save(output_path, 'PNG')
  print('  Done!')

print('Done!')
