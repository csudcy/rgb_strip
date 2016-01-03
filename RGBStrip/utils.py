#!/usr/bin/python
# -*- coding: utf8 -*-
import colorsys
import math


def get_rgb_rainbow(steps, max_rgb=127):
    if max_rgb < 0 or max_rgb > 255:
        raise Exception('max_rgb must be in the range 0-255!')
    # Thanks to http://stackoverflow.com/questions/876853/generating-color-ranges-in-python
    HSV_tuples = [
        (x*1.0/steps, 1, 1)
        for x in range(steps)
    ]
    RGB_tuples = [
        [
            hsv * max_rgb
            for hsv in colorsys.hsv_to_rgb(*hsv)
        ]
        for hsv in HSV_tuples
    ]

    return RGB_tuples


def xy_inc(x, y, w, h):
    # Move to the next column
    x += 1
    if x >= w:
        # Move to the next row
        x = 0
        y += 1
        if y >= h:
            y = 0
    return x, y


def generate_binary_array_lookup(bit_count):
    # Generate a lookup for 0-2**bit_count in bit_count bit binary arrays
    return [
        [
            bit=='1'
            for bit in (bin(num)[2:]).zfill(bit_count)
        ]
        for num in xrange(2**bit_count)
    ]


COLOURS = {
    # 0
    (0, 0, 0): ' ',
    # 1
    (1, 0, 0): 'R',
    (0, 1, 0): 'G',
    (0, 0, 1): 'B',
    # 2
    (1, 1, 0): 'Y',
    (0, 1, 1): 'C',
    (1, 0, 1): 'M',
    # 3
    (1, 1, 1): 'W',
}
def classify_colour(r, g, b, a):
    if (a & 31) == 0:
        # Alpha is off; nothing will be displayed regardless of RGB values
        return ' '
    col = (
        1 if r > 64 else 0,
        1 if g > 64 else 0,
        1 if b > 64 else 0,
    )
    return COLOURS[col]


def fade_in_out(rgb_colours, fade_steps_in, fade_steps_out, fade_hold_on, fade_hold_off):
    faded_colours = []
    for colour in rgb_colours:
        # Fade in
        for i in xrange(fade_steps_in):
            frac = i / float(fade_steps_in)
            faded_colours.append(
                (
                    colour[0] * frac,
                    colour[1] * frac,
                    colour[2] * frac,
                )
            )

        # Fully on
        for i in xrange(fade_hold_on):
            faded_colours.append(colour)

        # Fade out
        for i in xrange(fade_steps_out, 0, -1):
            frac = i / float(fade_steps_out)
            faded_colours.append(
                (
                    colour[0] * frac,
                    colour[1] * frac,
                    colour[2] * frac,
                )
            )

        # Fully off
        for i in xrange(fade_hold_off):
            faded_colours.append([0, 0, 0])

    return faded_colours


def make_palette(
        # Choose a colour
        colour=None,
        colours=None,
        rainbow_steps=None,

        fade_steps_in=None,
        fade_steps_out=None,

        fade_hold_on=None,
        fade_hold_off=None
    ):
    """
    Construct a palette from the given parameters
    """
    # Work out the base colour(s)
    if colour is not None:
        palette = [resolve_colour(colour)]
    elif colours is not None:
        palette = resolve_colours(colours)
    elif rainbow_steps is not None:
        palette = get_rgb_rainbow(rainbow_steps)
    else:
        raise Exception('You must provide at least one of colour, colours or rainbow_steps!')

    # Apply fade if required
    if fade_steps_in:
        palette = fade_in_out(palette, fade_steps_in, fade_steps_out, fade_hold_on, fade_hold_off)

    return palette


def resolve_colour(colour):
    # Avoid circular imports
    from RGBStrip import constants

    # If this is a COLOUR constant, return that
    if isinstance(colour, basestring):
        return constants.COLOURS[colour]

    # Otherwise, assume this is an RGB tuple
    return colour


def resolve_colours(palette):
    return [
        resolve_colour(colour)
        for colour in palette
    ]


def resolve_palette(palettes, palette):
    # This might be a named palette
    if palette in palettes:
        return palettes[palette]

    # Or it might be a list of named colours
    if hasattr(palette, '__iter__'):
        return resolve_colours(palette)

    # Or it might be a single named colour
    return [resolve_colour(palette)]
