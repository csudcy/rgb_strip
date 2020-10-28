#!/usr/bin/python
# -*- coding: utf8 -*-
import time

from RGBStrip.renderers.base import BaseMultiRenderer


class MultiTimedRenderer(BaseMultiRenderer):

    def __init__(
            self,
            loader,
            renderers=None,
            common_parameters=None,
            active=True,
            time_seconds=10):
        super().__init__(
            loader, renderers=renderers, common_parameters=common_parameters, active=active)

        self.TIME_SECONDS = time_seconds
        self.RENDERER_INDEX = 0
        self.NEXT_RENDERER_TIME = time.time() + time_seconds

    def do_render(self):
        if self.NEXT_RENDERER_TIME < time.time():
            self.RENDERER_INDEX = (self.RENDERER_INDEX + 1) % len(self.RENDERERS)
            self.NEXT_RENDERER_TIME = time.time() + self.TIME_SECONDS

        self.RENDERERS[self.RENDERER_INDEX].render()
