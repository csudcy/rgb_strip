import colorsys
from typing import Dict, List, Tuple, Union

ColourType = Tuple[int, int, int]

COLOURS = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'cyan': (0, 255, 255),
    'blue': (0, 0, 255),
    'pink': (255, 0, 255),
    'white': (255, 255, 255),
}

class Palette(List[ColourType]):
  name: str

  def __init__(self, name: str, *colours: ColourType):
    super().__init__(colours)
    self.name = name


def resolve_palette(palette_input: Union[str, List[str], Dict[str, List[str]]]) -> Palette:
  # A single dict of name -> palettes
  if isinstance(palette_input, dict):
    if len(palette_input) != 1:
      raise Exception('Named palettes must have exactly 1 key & value!')
    
    name, colours = list(palette_input.items())[0]
    palette = resolve_palette(colours)
    palette.name = name
    return palette

  # A list of sub-palettes
  if isinstance(palette_input, list):
    palette = Palette('_'.join(palette_input))
    for sub_palette in map(resolve_palette, palette_input):
      palette += sub_palette
    return palette

  # A 'rainbow_{count}' palette
  if palette_input.startswith('rainbow_'):
    steps = int(palette_input[8:])
    # Thanks to http://stackoverflow.com/questions/876853/generating-color-ranges-in-python
    rgb_values = [
        colorsys.hsv_to_rgb(degrees / steps, 1, 1) for degrees in range(steps)
    ]
    return Palette(palette_input,
        *((int(r * 255), int(g * 255), int(b * 255)) for r, g, b in rgb_values)
    )

  # A single named colour
  return Palette(palette_input, COLOURS[palette_input])


def fade_in_out(
    colour: ColourType,
    fade_steps_in: int,
    fade_steps_out: int,
    fade_hold_on: int,
    fade_hold_off: int,
) -> List[ColourType]:

  def get_colour(frac: float) -> ColourType:
    return (
        int(colour[0] * frac),
        int(colour[1] * frac),
        int(colour[2] * frac),
    )

  faded_colours = []

  # Fade in
  faded_colours += [get_colour(i / fade_steps_in) for i in range(fade_steps_in)]

  # Fully on
  faded_colours += [colour] * fade_hold_on

  # Fade out
  faded_colours += [
      get_colour(i / fade_steps_out) for i in range(fade_steps_out, 0, -1)
  ]

  # Fully off
  faded_colours += [(0, 0, 0)] * fade_hold_off

  return faded_colours
