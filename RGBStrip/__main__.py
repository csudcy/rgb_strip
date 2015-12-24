#!/usr/bin/python
# -*- coding: utf8 -*-
import argparse

from RGBStrip import manager
from RGBStrip import server

# Parse our args
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--server', help='If the web server should be run', action='store_true')
parser.add_argument('config', help='The config file to load')
args = parser.parse_args()

# Start
if args.server:
    server.start_server(args.config)
else:
    manager = manager.RGBStripManager()
    manager.load_config(args.config)
    manager.output_forever()
