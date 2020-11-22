#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.renderers.base import BaseMultiRenderer


class MultiSequential(BaseMultiRenderer):

  FINISHABLE = True

  def __init__(self,
               loader,
               renderers=None,
               common_parameters=None,
               active=True):
    super().__init__(loader,
                     renderers=renderers,
                     common_parameters=common_parameters,
                     active=active,
                     # How many frames to render for "unfinishable" renderers.
                     frames_unfinishable=1000)
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
