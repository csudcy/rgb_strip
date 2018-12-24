#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseMultiRenderer


class MultiAllRenderer(BaseMultiRenderer):

    def do_render(self):
        for renderer in self.RENDERERS:
            renderer.render()
