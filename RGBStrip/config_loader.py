#!/usr/bin/python
# -*- coding: utf8 -*-
import yaml

from RGBStrip.controller import RGBStripController
from RGBStrip.displays.cursesd import CursesDisplay
from RGBStrip.displays.rpi_spi import RPiSPIDisplay
from RGBStrip.displays.tk import TkDisplay
from RGBStrip.manager import RGBStripManager
from RGBStrip.renderers.clock import ClockRenderer
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
    'gravity_shot': GravityShotRenderer,
    'patch': PatchRenderer,
    'rainbow': RainbowRenderer,
}


def load_config(path):
    with open(path) as f:
        config = yaml.load(f.read())

    # Make Everything
    controller = get_controller(config['controller'])
    manager = get_manager(controller)
    sections = get_sections(controller, config['sections'])
    add_renderers(manager, sections, config['renderers'])
    add_displays(controller, manager, config['displays'])

    manager.output_forever()


def get_controller(config):
    return RGBStripController(**config)


def get_manager(controller):
    return RGBStripManager(controller)


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


def add_renderers(manager, sections, config):
    for renderer in config:
        renderer_class = RENDERERS[renderer['type']]
        manager.add_renderer(
            renderer_class(
                sections[renderer['section']],
                **renderer.get('params', {})
            )
        )


def add_displays(controller, manager, config):
    for display in config:
        display_class = DISPLAYS[display['type']]
        manager.add_display(
            display_class(
                controller,
                **display.get('params', {})
            )
        )
