import colorsys
from typing import List, Tuple

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


def resolve_palette(palette: str) -> List[ColourType]:
  # A 'rainbow_{count}' palette
  if palette.startswith('rainbow_'):
    rainbow_steps = int(palette[8:])
    return make_rainbow(rainbow_steps)
  else:
    # A single named colour
    return [COLOURS[palette]]


def make_rainbow(steps: int):
  # Thanks to http://stackoverflow.com/questions/876853/generating-color-ranges-in-python
  hsv_values = [
      colorsys.hsv_to_rgb(degrees / steps, 1, 1) for degrees in range(steps)
  ]
  return [(int(h * 255), int(s * 255), int(v * 255)) for h, s, v in hsv_values]


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
