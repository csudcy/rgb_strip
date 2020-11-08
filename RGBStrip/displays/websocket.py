#!/usr/bin/python
# -*- coding: utf8 -*-
import json

from .base import BaseDisplay

WEBSOCKETS = set()


class WebSocketDisplay(BaseDisplay):
  """A display module for sending data over websockets.
  """

  # TODO: Error if multiple WebSocketDisplay's are instantiated?
  def display(self):
    data = json.dumps({
        'config': self.CONTROLLER.CONFIG,
        'alpha': self.CONTROLLER.ALPHA,
        'pixels': self.CONTROLLER.PIXELS,
    })
    for ws in WEBSOCKETS:
      ws.send(data)


def add_websocket(ws):
  # Add ws to the global list
  WEBSOCKETS.add(ws)


def remove_websocket(ws):
  # Remove ws from the global list
  WEBSOCKETS.remove(ws)
