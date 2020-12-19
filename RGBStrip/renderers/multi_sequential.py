#!/usr/bin/python
# -*- coding: utf8 -*-
from typing import Iterator

from RGBStrip import render_file
from RGBStrip.renderers.base import BaseMultiRenderer


class MultiSequential(BaseMultiRenderer):

  FINISHABLE = True

  def __init__(
      self,
      loader,
      name=None,
      renderers=None,
      common_parameters=None,
      active=True,
      # How many frames to render for "unfinishable" renderers.
      frames_unfinishable=1000,
      # Ignore any further arguments (in case common parameters was used)
      **kwargs,
  ):
    super().__init__(loader,
                     name=name,
                     renderers=renderers,
                     common_parameters=common_parameters,
                     active=active)
    self.FRAMES_UNFINISHABLE = frames_unfinishable
    self.FINISHED = False
    self._init_for_renderer(0)

  def is_finished(self):
    """Check if this display is in a "finished" state.
    """
    return self.FINISHED

  def _init_for_renderer(self, index):
    # Check if we've been through all our renderers at least once
    if index >= len(self.RENDERERS):
      self.FINISHED = True

    self.RENDERER_INDEX = index % len(self.RENDERERS)
    self.CURRENT_RENDERER = self.RENDERERS[self.RENDERER_INDEX]
    if self.CURRENT_RENDERER.IS_FINISHABLE:
      self.FRAMES_REMAINING = None
    else:
      self.FRAMES_REMAINING = self.FRAMES_UNFINISHABLE

  def do_render(self):
    # Is the current renderer finished?
    if self.CURRENT_RENDERER.IS_FINISHABLE:
      finished = self.CURRENT_RENDERER.is_finished()
    else:
      if self.FRAMES_REMAINING:
        self.FRAMES_REMAINING -= 1
        finished = False
      else:
        finished = True

    # If so, move to next renderer
    if finished:
      # TODO: Consider adding a renderer reset?
      self._init_for_renderer(self.RENDERER_INDEX + 1)

    self.CURRENT_RENDERER.render()

  def render_all_to_memory(self, controller) -> Iterator[render_file.RenderWriter]:
    for renderer in self.RENDERERS:
      yield renderer.render_to_memory(controller)

  def render_to_memory(self, controller, **data) -> render_file.RenderWriter:
    raise Exception('Cannot render_to_memory a multi renderer!')
