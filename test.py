#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip.controller import RGBStripController
from RGBStrip.displays.cursesd import CursesDisplay
from RGBStrip.manager import RGBStripManager
from RGBStrip.section import SectionController
from RGBStrip.renderers.rainbow import RainbowRenderer


def main():
    print 'Hello!'
    rgb_strip = None
    try:
        print 'Initialising strip...'
        rsc = RGBStripController(60, 2)
        rsm = RGBStripManager(rsc)

        print 'Initialising sections...'
        rss1 = SectionController(rsc, 0, 0, 30, 1)

        print 'Initialising renderers...'
        # r = PatchRenderer(5, 2)
        # r.add_output('Patch-Red', rgb_strip, 5, 0)

        # r = PatchRenderer(5, 2, RGBStrip.get_rgb_rainbow(250, max_rgb=32))
        # r.add_output('Patch-Rainbow', rgb_strip, 15, 0)

        rsm.add_renderer(
            RainbowRenderer(rss1)
        )

        # r = RainbowRenderer(30, 1, train_length=30)
        # r.add_output('RT-30x30', rgb_strip,  30, 0)

        # r = RainbowRenderer(60, 1)
        # r.add_output('RT-60x10', rgb_strip,  0, 1)

        # r = ClockRenderer()
        # r.add_output('Clock', rgb_strip, 0, 1)

        print 'Testing rgb_strip...'
        with CursesDisplay(rsc) as rsd:
        #with RPiSPIDisplay(rsc) as rsd:
            rsm.add_display(rsd)
            rsm.output_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print 'Cleaning up...'
        print 'TODO!'
    print 'Bye!'


if __name__ == '__main__':
    main()
