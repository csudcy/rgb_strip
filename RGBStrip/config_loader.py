#!/usr/bin/python
# -*- coding: utf8 -*-
import yaml

from RGBStrip.controller import RGBStripController
from RGBStrip.displays.cursesd import CursesDisplay
from RGBStrip.displays.rpi_spi import RPiSPIDisplay
from RGBStrip.displays.tk import TkDisplay
from RGBStrip.renderers.clock import ClockRenderer
from RGBStrip.renderers.gravity_drip import GravityDripRenderer
from RGBStrip.renderers.gravity_shot import GravityShotRenderer
from RGBStrip.renderers.patch import PatchRenderer
from RGBStrip.renderers.rainbow import RainbowRenderer
from RGBStrip.section import SectionController

DISPLAYS = {
    'curses': CursesDisplay,
    'rpi_spi': RPiSPIDisplay,
    'tk': TkDisplay,
}

RENDERERS = {
    'clock': ClockRenderer,
    'gravity_drip': GravityDripRenderer,
    'gravity_shot': GravityShotRenderer,
    'patch': PatchRenderer,
    'rainbow': RainbowRenderer,
}


def load_config(path):
    with open(path) as f:
        config = yaml.load(f.read())

    # Make Everything
    controller = get_controller(config['controller'])
    sections = get_sections(controller, config['sections'])
    renderers = get_renderers(sections, config['renderers'])
    displays = get_displays(controller, config['displays'])

    return {
        'controller': controller,
        'sections': sections,
        'renderers': renderers,
        'displays': displays,
    }


def get_controller(config):
    return RGBStripController(**config)


def get_sections(controller, config):
    return dict(
        (
            section.pop('id'),
            SectionController(
                controller,
                **section
            )
        )
        for section in config
    )


def get_renderers(sections, config):
    renderers = []
    for renderer in config:
        if renderer['type'] not in RENDERERS:
            raise Exception(
                'Unknown renderer "{type}"; valid options are: {types}'.format(
                    type=renderer['type'],
                    types=RENDERERS.keys()
                )
            )
        renderer_class = RENDERERS[renderer['type']]
        renderers.append(
            renderer_class(
                sections[renderer['section']],
                **renderer.get('params', {})
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
