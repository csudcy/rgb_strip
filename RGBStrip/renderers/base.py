#!/usr/bin/python
# -*- coding: utf8 -*-

class BaseRenderer(object):

    def __init__(self, loader, active=True):
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


class BaseSingleRenderer(BaseRenderer):

    DEFAULT_PALETTE = None

    def __init__(self, loader, section=None, palette=None, active=True):
        super(BaseSingleRenderer, self).__init__(loader, active=active)

        self.SECTION = loader.resolve_section(section)

        palette = loader.resolve_palette(palette or self.DEFAULT_PALETTE)
        if not palette:
            raise Exception('You must provide a palette for %s!' % self.__class__.__name__)
        self.PALETTE = palette


class BaseMultiRenderer(BaseRenderer):

    def __init__(self, loader, renderers=None, active=True):
        super(BaseMultiRenderer, self).__init__(loader, active=active)

        self.RENDERERS = [
            loader.load_renderer(renderer)
            for renderer in renderers
        ]

    def stop(self):
        for renderer in self.RENDERERS:
            renderer.stop()
