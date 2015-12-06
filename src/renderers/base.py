#!/usr/bin/python
# -*- coding: utf8 -*-

class BaseRenderer(object):
    def __init__(self, width, height=1):
        self.WIDTH = width
        self.HEIGHT = height

        self.OUTPUTS = []

    def add_output(self, id, rgb_strip, x, y=0):
        # Save this in my list of outputs
        self.OUTPUTS.append(StripSection(
            id,
            rgb_strip,
            x,
            y
        ))

        # Register myself with the rgb_strip so I will get rendered & output
        rgb_strip.add_renderer(self)

    def render(self):
        raise Exception('render must be overridden by inheriting classes!')
