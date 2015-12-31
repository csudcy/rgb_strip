#!/usr/bin/python
# -*- coding: utf8 -*-

class BaseRenderer(object):
    def __init__(self, sections, active=True):
        # Allow single sections to be passed in
        if not hasattr(sections, '__iter__'):
            sections = [sections]

        # Check we have some sections
        if not sections:
            raise Exception('To initialise a renderer, you must pass in at least 1 section!')

        # Check all sections have the same dimensions
        self.WIDTH = sections[0].WIDTH
        self.HEIGHT = sections[0].HEIGHT
        for section in sections[1:]:
            if self.WIDTH != section.WIDTH or self.HEIGHT != section.HEIGHT:
                raise Exception('All sections assigned to a single renderer must have the same dimensions!')

        self.SECTIONS = sections
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
