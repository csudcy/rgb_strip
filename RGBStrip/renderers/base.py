#!/usr/bin/python
# -*- coding: utf8 -*-

class BaseRenderer(object):

    DEFAULT_PALETTE = None

    def __init__(self, section, palette, active=True):
        self.SECTION = section

        palette = palette or self.DEFAULT_PALETTE
        if not palette:
            raise Exception('You must provide a palette for %s!' % self.__class__.__name__)
        self.PALETTE = palette

        self.ACTIVE = active

    def render(self):
        if self.ACTIVE:
            self.do_render()

    def do_render(self):
        raise Exception('do_render must be overridden by inheriting classes!')

    def stop(self):
        """
        Do any necessary cleanup
        """
        pass
