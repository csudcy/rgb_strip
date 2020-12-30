import itertools
import logging
from typing import Any, Dict, Generator, Iterable, List

import yaml

import colours
from effects import base
from effects import fireworks
from effects import lines
from effects import sparkles
from effects import spiral
from effects import wandering_lines

LOGGER = logging.getLogger(__name__)

EffectType = Dict[str, Any]

EFFECTS = {
    'fireworks': fireworks.FireworksEffect,
    'lines': lines.LinesEffect,
    'sparkles': sparkles.SparklesEffect,
    'spiral': spiral.SpiralEffect,
    'wandering_lines': wandering_lines.WanderingLinesEffect,
}


class Config():

  def __init__(self, width: int, height: int, effects: List[EffectType]):
    self.width = width
    self.height = height
    LOGGER.info(f'Processing {len(effects)} effects...')
    processed_effects = list(self._process_effects(effects))
    LOGGER.info(f'Loading {len(processed_effects)} effects...')
    self.effects = [
        self._load_effect(processed_effect)
        for processed_effect in processed_effects
    ]
    LOGGER.info(f'Loading done!')

  def _process_effects(
      self, effects: Iterable[EffectType]) -> Generator[EffectType, None, None]:
    LOGGER.debug('Processing effects...')
    for count, effect in enumerate(effects):
      LOGGER.debug(f'Processing effect {count}...')
      for processed_effect in self._process_multi_effect(effect):
        yield from self._process_render_count_effect(processed_effect)
    LOGGER.debug(f'Processed effects.')

  def _process_multi_effect(
      self, effect: EffectType) -> Generator[EffectType, None, None]:
    if 'multis' in effect:
      LOGGER.debug(f'Processing multi effect...')
      multis = effect.pop('multis')
      multi_keys = multis.keys()
      multi_values = [multis[key] for key in multi_keys]
      for count, values in enumerate(itertools.product(*multi_values)):
        LOGGER.debug(f'Processing multi effect {count}...')
        permutation = dict(zip(multi_keys, values))
        permutation.update(effect)
        permutation['name'] = permutation['name'].format(**permutation)
        yield permutation
      LOGGER.debug(f'Processed multi effect.')
    else:
      LOGGER.debug(f'Processing single effect.')
      yield effect
      LOGGER.debug(f'Processed single effect.')

  def _process_render_count_effect(
      self, effect: EffectType) -> Generator[EffectType, None, None]:
    if 'render_count' in effect:
      LOGGER.debug(f'Processing render_count effect...')
      render_count = effect.pop('render_count', 1)
      effect_name = effect.pop('name')
      for count in range(render_count):
        LOGGER.debug(f'Processing render_count effect {count}...')
        processed_effect = {'name': f'{effect_name}_{count}'}
        processed_effect.update(effect)
        yield processed_effect
      LOGGER.debug(f'Processed render_count effect.')
    else:
      LOGGER.debug(f'Processing single effect.')
      yield effect
      LOGGER.debug(f'Processed single effect.')

  def _load_effect(self, effect: EffectType) -> base.BaseEffect:
    effect_name = effect.pop('name')
    effect_type = effect.pop('type')
    effect_palette = effect.pop('palette')
    if effect_type not in EFFECTS:
      raise Exception(f'Unknown effect type in {effect_name}: {effect_type}')
    return EFFECTS[effect_type](
        width=self.width,
        height=self.height,
        name=effect_name,
        palette=colours.resolve_palette(effect_palette),
        **effect,
    )

  @classmethod
  def from_file(cls, config_file: str) -> 'Config':
    with open(config_file, 'r') as f:
      config_yaml = yaml.load(f)
    return cls(config_yaml['width'], config_yaml['height'],
               config_yaml['effects'])
