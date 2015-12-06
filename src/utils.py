#!/usr/bin/python
# -*- coding: utf8 -*-
import colorsys


def get_rgb_rainbow(steps, max_rgb=127):
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
