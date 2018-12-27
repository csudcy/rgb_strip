#!/usr/bin/python
# -*- coding: utf8 -*-
import abc
import time


class BaseRenderer(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, loader, active=True):
        self.ACTIVE = active

    def render(self):
        if self.ACTIVE:
            self.do_render()

    @abc.abstractmethod
    def do_render(self):
        pass

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


class BaseSingleTimedRenderer(BaseSingleRenderer):

    def __init__(self, loader, interval_seconds=1, section=None, palette=None, active=True):
        super(BaseSingleTimedRenderer, self).__init__(
            loader, section=section, palette=palette, active=active)

        self.INTERVAL_SECONDS = interval_seconds
        self.NEXT_STEP = time.time() + interval_seconds

    def do_render(self):
        self.do_render_display()

        if time.time() > self.NEXT_STEP:
            self.NEXT_STEP = time.time() + self.INTERVAL_SECONDS
            self.do_render_step()

    @abc.abstractmethod
    def do_render_display(self):
        pass

    @abc.abstractmethod
    def do_render_step(self):
        pass


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
