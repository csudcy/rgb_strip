#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import utils
from RGBStrip.controller import RGBStripController
from RGBStrip.displays.cursesd import CursesDisplay
from RGBStrip.displays.rpi_spi import RPiSPIDisplay
from RGBStrip.displays.tk import TkDisplay
from RGBStrip.manager import RGBStripManager
from RGBStrip.section import SectionController
from RGBStrip.renderers.clock import ClockRenderer
from RGBStrip.renderers.patch import PatchRenderer
from RGBStrip.renderers.rainbow import RainbowRenderer


def main():
    print 'Hello!'
    rgb_strip = None
    try:
        print 'Initialising strip...'
        rsc = RGBStripController(60, 2, reverse_x=True)
        rsm = RGBStripManager(rsc)

        print 'Initialising sections...'
        rss_tl = SectionController(rsc, 0, 0, 30, 1)
        rss_tr = SectionController(rsc, 30, 0, 30, 1)
        rss_b = SectionController(rsc, 0, 1, 60, 1)
        rss_p1 = SectionController(rsc, 5, 0, 5, 2)
        rss_p2 = SectionController(rsc, 15, 0, 5, 2)

        print 'Initialising renderers...'
        # Rainbows
        rsm.add_renderer(
            RainbowRenderer(rss_tl)
        )
        rsm.add_renderer(
            RainbowRenderer(rss_tr, train_length=30)
        )
        rsm.add_renderer(
            RainbowRenderer(rss_b)
        )

        # Patches
        rsm.add_renderer(
            PatchRenderer(rss_p1)
        )
        rsm.add_renderer(
            PatchRenderer(rss_p2, utils.get_rgb_rainbow(250), a=1)
        )

        # Clock
        rsm.add_renderer(
            ClockRenderer(rss_b)
        )

        # Gravity shots

        # Gravity Drips

        print 'Testing rgb_strip...'
        #with CursesDisplay(rsc) as rsd_curses:
        #    rsm.add_display(rsd_curses)
        with TkDisplay(rsc) as rsd_tk:
            rsm.add_display(rsd_tk)
        # with RPiSPIDisplay(rsc) as rsd_spi:
        #     rsm.add_display(rsd_spi)
            rsm.output_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print 'Cleaning up...'
        print 'TODO!'
    print 'Bye!'


if __name__ == '__main__':
    main()
