# Vector image by VectorStock / Heorhii
# https://www.vectorstock.com/royalty-free-vector/cartoon-icons-of-different-weather-conditions-vector-46552095

# Manually change background to black; seem reasonable on a laptop screen...

import pathlib
import shutil

from PIL import Image
from PIL import ImageDraw

CURRENT_DIRECTORY = pathlib.Path(__file__).parent
SOURCE_IMAGE = CURRENT_DIRECTORY / 'vectorstock_46552095_black.png'
DEST_DIRECTORY = CURRENT_DIRECTORY / '8'

R1 = 450
R2 = 1180
R3 = 1950

C1 = 425
C2 = 1220
C3 = 1945

SIZE = 630

IMAGE_PIXELS_PER_PIXEL = 63

IMAGES = {
    # Row 1
    'sun_cloud': (C1, R1),
    'sun': (C2, R1),
    'cloud': (C3, R1),
    # # Row 2
    'storm': (C1, R2),
    'wind': (C2, R2),
    'sun_rain': (C3, R2),
    # # Row 3
    'rain': (C1, R3),
    'snow': (C2, R3),
    'freeze': (C3, R3),
}

DEBUG_BOXES = False

print('Loading source image...')
source_image = Image.open(SOURCE_IMAGE)
print('Converting...')
source_image = source_image.convert('RGB')

if DEBUG_BOXES:
  # For working out where the bounding boxes are:
  print('Drawing boxes...')
  draw = ImageDraw.Draw(source_image)
  for filename, (x, y) in IMAGES.items():
    draw.rectangle((x, y, x + SIZE, y + SIZE), outline='white', width=20)

  # print('Resizing boxes...')
  # source_image = source_image.resize((
  #     int(source_image.size[0] / IMAGE_PIXELS_PER_PIXEL),
  #     int(source_image.size[1] / IMAGE_PIXELS_PER_PIXEL),
  # ))

  print('Saving...')
  output_path = DEST_DIRECTORY / f'boxes.png'
  source_image.save(output_path, 'PNG')
else:
  # Clear the destination directory
  if DEST_DIRECTORY.exists():
    print('Removing dest directory...')
    shutil.rmtree(DEST_DIRECTORY)
  print('Creating dest directory...')
  DEST_DIRECTORY.mkdir()

  # For extracting the images:
  for filename, (x, y) in IMAGES.items():
    print(f'{filename}:')

    print('  Extracting...')
    image = source_image.copy()
    image = image.crop((x, y, x + SIZE, y + SIZE))

    print('  Resizing...')
    image = image.resize((8, 8))

    print('  Saving...')
    output_path = DEST_DIRECTORY / f'{filename}.png'
    image.save(output_path, 'PNG')
    print('  Done!')

  print('Done!')
