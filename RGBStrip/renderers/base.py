#!/usr/bin/python
# -*- coding: utf8 -*-

class BaseRenderer(object):
    def __init__(self, controllers, active=True):
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
        self.ACTIVE = active

    def render(self):
        if self.ACTIVE:
            self.do_render()

    def do_render(self):
        raise Exception('do_render must be overridden by inheriting classes!')

    def stop(self):
        """
        Do any necessary cleanup
        """
        pass
