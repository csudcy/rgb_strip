from RGBStrip.displays.cursesd import CursesDisplay
from RGBStrip.displays.rpi_spi import RPiSPIDisplay
from RGBStrip.displays.tk import TkDisplay
from RGBStrip.displays.websocket import WebSocketDisplay

from RGBStrip.renderers.clock import ClockRenderer
from RGBStrip.renderers.gravity_drip import GravityDripRenderer
from RGBStrip.renderers.gravity_shot import GravityShotRenderer
from RGBStrip.renderers.patch import PatchRenderer
from RGBStrip.renderers.rainbow import RainbowRenderer


DISPLAYS = {
    'curses': CursesDisplay,
    'rpi_spi': RPiSPIDisplay,
    'tk': TkDisplay,
    'websocket': WebSocketDisplay,
}

RENDERERS = {
    'clock': ClockRenderer,
    'gravity_drip': GravityDripRenderer,
    'gravity_shot': GravityShotRenderer,
    'patch': PatchRenderer,
    'rainbow': RainbowRenderer,
}

COLOURS = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'cyan': (0, 255, 255),
    'blue': (0, 0, 255),
    'pink': (255, 0, 255),
    'white': (255, 255, 255),
}
