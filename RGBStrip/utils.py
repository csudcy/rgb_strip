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
