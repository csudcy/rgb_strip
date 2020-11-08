#!/usr/bin/python
# -*- coding: utf8 -*-
import abc
import time


class BaseRenderer(abc.ABC):

  def __init__(self, loader, active=True):
    self.ACTIVE = active

  def render(self):
    if self.ACTIVE:
      self.do_render()

  @abc.abstractmethod
  def do_render(self):
    pass

  def stop(self):
    """Do any necessary cleanup.
    """
    pass


class BaseSingleRenderer(BaseRenderer):

  DEFAULT_PALETTE = None

  def __init__(self, loader, section=None, palette=None, active=True):
    super().__init__(loader, active=active)

    self.SECTION = loader.resolve_section(section)

    palette = loader.resolve_palette(palette or self.DEFAULT_PALETTE)
    if not palette:
      raise Exception(
          f'You must provide a palette for {self.__class__.__name__}!')
    self.PALETTE = palette


class BaseSingleTimedRenderer(BaseSingleRenderer):

  def __init__(self,
               loader,
               interval_seconds=1,
               section=None,
               palette=None,
               active=True):
    super().__init__(loader, section=section, palette=palette, active=active)

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

  def __init__(self,
               loader,
               renderers=None,
               common_parameters=None,
               active=True):
    super().__init__(loader, active=active)

    self.RENDERERS = []
    for renderers_config in renderers:
      if common_parameters:
        renderers_config.update(common_parameters)
      self.RENDERERS.append(loader.load_renderer(renderers_config))

  def stop(self):
    for renderer in self.RENDERERS:
      renderer.stop()
