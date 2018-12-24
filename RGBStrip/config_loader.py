#!/usr/bin/python
# -*- coding: utf8 -*-
import yaml

from RGBStrip.constants import CONTROLLERS, DISPLAYS, RENDERERS, SECTIONS
from RGBStrip import utils


def load_config_path(path):
    with open(path) as f:
        return load_config(f.read())


def load_config(yaml_config):
    config = yaml.load(yaml_config)

    # Make Everything
    controller = get_controller(config['controller'])
    sections = get_sections(controller, config['sections'])
    palettes = get_palettes(config.get('palettes', {}))
    renderers = get_renderers(sections, palettes, config['renderers'])
    displays = get_displays(controller, config['displays'])

    return {
        'yaml_config': yaml_config,
        'general': config.get('general', {}),
        'controller': controller,
        'sections': sections,
        'palettes': palettes,
        'renderers': renderers,
        'displays': displays,
    }


def get_controller(config):
    type = config.pop('type')
    return CONTROLLERS[type](**config)


def get_sections(controller, config):
    sections = {}
    for id, params in (config or []).iteritems():
        type = params.pop('type')
        sections[id] = SECTIONS[type](
            controller,
            **params
        )
    return sections


def get_palettes(config):
    palettes = {}
    for id, params in (config or []).iteritems():
        palettes[id] = utils.make_palette(**params)
    return palettes


def get_renderers(sections_dict, palettes, config):
    renderers = []
    for renderer in config or []:
        if renderer['type'] not in RENDERERS:
            raise Exception(
                'Unknown renderer "{type}"; valid options are: {types}'.format(
                    type=renderer['type'],
                    types=RENDERERS.keys()
                )
            )
        renderer_class = RENDERERS[renderer.pop('type')]
        sections = sections_dict[renderer.pop('section')]
        palette = renderer.pop('palette', None)
        if palette:
            palette = utils.resolve_palette(palettes, palette)
        renderers.append(
            renderer_class(
                sections,
                palette,
                **renderer
            )
        )
    return renderers


def get_displays(controller, config):
    displays = []
    for display in config:
        if display['type'] not in DISPLAYS:
            raise Exception(
                'Unknown display "{type}"; valid options are: {types}'.format(
                    type=display['type'],
                    types=DISPLAYS.keys()
                )
            )
        display_class = DISPLAYS[display['type']]
        displays.append(
            display_class(
                controller,
                **display.get('params', {})
            )
        )
    return displays
