#!/usr/bin/python
# -*- coding: utf8 -*-
import abc
import time


class BaseRenderer(abc.ABC):

  # Does this display have a "finished" point
  IS_FINISHABLE = False

  def __init__(self, loader, name=None, active=True):
    self.NAME = name
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

  def is_finished(self):
    """Check if this display is in a "finished" state.
    """
    raise Exception('Finishable displays must implement is_finished!')

  def render_to_memory(self, controller):
    """Render myself to memory.
    """
    frames = self._render_frames_to_memory(controller)
    return {
        'name': self.NAME,
        'frames': frames,
    }

  def _render_frames_to_memory(self,
                               controller,
                               frames_unfinishable=1000,
                               frames_max=2000):
    """Render all my frames to memory.
    """
    for frame_count in range(frames_max):
      # Check if finished
      if self.IS_FINISHABLE:
        if self.is_finished():
          break
      else:
        if frame_count >= frames_unfinishable:
          break

      controller.set_leds((0, 0, 0))
      self._render_frame()
      yield controller.PIXELS[:]

  def _render_frame(self):
    self.render()


class BaseSingleRenderer(BaseRenderer):

  DEFAULT_PALETTE = None

  def __init__(self,
               loader,
               name=None,
               section=None,
               palette=None,
               active=True):
    super().__init__(loader, name=name, active=active)

    self.SECTION = loader.resolve_section(section)

    palette = loader.resolve_palette(palette or self.DEFAULT_PALETTE)
    if not palette:
      raise Exception(
          f'You must provide a palette for {self.__class__.__name__}!')
    self.PALETTE = palette


class BaseSingleTimedRenderer(BaseSingleRenderer):

  def __init__(self,
               loader,
               name=None,
               interval_seconds=1,
               section=None,
               palette=None,
               active=True):
    super().__init__(loader,
                     name=name,
                     section=section,
                     palette=palette,
                     active=active)

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

  def render_to_memory(self, controller):
    """Render myself to memory.
    """
    rendered = super().render_to_memory(controller)
    rendered['interval_seconds'] = self.INTERVAL_SECONDS
    return rendered

  def _render_frame(self):
    self.do_render_display()
    self.do_render_step()


class BaseMultiRenderer(BaseRenderer):

  def __init__(self,
               loader,
               name=None,
               renderers=None,
               common_parameters=None,
               active=True):
    super().__init__(loader, name=name, active=active)

    self.RENDERERS = []
    for renderers_config in renderers:
      if common_parameters:
        renderers_config.update(common_parameters)
      self.RENDERERS.append(loader.load_renderer(renderers_config))

  def stop(self):
    for renderer in self.RENDERERS:
      renderer.stop()
