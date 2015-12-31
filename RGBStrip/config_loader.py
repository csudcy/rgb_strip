#!/usr/bin/python
# -*- coding: utf8 -*-
import yaml

from RGBStrip.constants import DISPLAYS, RENDERERS
from RGBStrip.controller import RGBStripController
from RGBStrip.section import SectionController
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
    return RGBStripController(**config)


def get_sections(controller, config):
    return {
        name: SectionController(
            controller,
            **params
        )
        for name, params in config.iteritems()
    }


def get_palettes(config):
    return {
        name: utils.make_palette(**params)
        for name, params in config.iteritems()
    }


def _resolve_sections(sections_dict, sections):
    # If sections is a list, lookup each one
    if hasattr(sections, '__iter__'):
        return [
            sections_dict[section]
            for section in sections
        ]

    # Otherwise, assume sections is just 1 to lookup
    return sections_dict[sections]


def get_renderers(sections_dict, palettes, config):
    renderers = []
    for renderer in config:
        if renderer['type'] not in RENDERERS:
            raise Exception(
                'Unknown renderer "{type}"; valid options are: {types}'.format(
                    type=renderer['type'],
                    types=RENDERERS.keys()
                )
            )
        renderer_class = RENDERERS[renderer.pop('type')]
        sections = _resolve_sections(sections_dict, renderer.pop('sections'))
        renderers.append(
            renderer_class(
                sections,
                palettes,
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
