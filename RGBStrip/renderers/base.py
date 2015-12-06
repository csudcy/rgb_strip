#!/usr/bin/python
# -*- coding: utf8 -*-

class BaseRenderer(object):
    def __init__(self, controllers):
        # Allow single controllers to be passed in
        if not hasattr(controllers, '__iter__'):
            controllers = [controllers]

        # Check we have some controllers
        if not controllers:
            raise Exception('To initialise a renderer, you must pass in at least 1 controller!')

        # Check all controllers have the same dimensions
        self.WIDTH = controllers[0].WIDTH
        self.HEIGHT = controllers[0].HEIGHT
        for controller in controllers[1:]:
            if self.WIDTH != controller.WIDTH or self.HEIGHT != controller.HEIGHT:
                raise Exception('All controllers assigned to a single renderer must have the same dimensions!')

        self.CONTROLLERS = controllers

    def render(self):
        raise Exception('render must be overridden by inheriting classes!')
