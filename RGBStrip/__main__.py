#!/usr/bin/python
# -*- coding: utf8 -*-
import argparse

from RGBStrip import manager

# Parse our args
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--server', help='If the web server should be run', action='store_true')
parser.add_argument('--host', help='The host for the web server to bind to')
parser.add_argument('--port', help='The port for the web server to bind to', type=int)
parser.add_argument('config', help='The config file to load')
args = parser.parse_args()

# Start manager & load the config
manager = manager.RGBStripManager()
manager.load_config(args.config)

# If we need a server, start it now
if args.server:
    # Import this here so we don't require gevent when not using the server
    from RGBStrip import server

    # Start the server (non-blocking)
    kwargs = {}
    if args.host:
        kwargs['host'] = args.host
    if args.port:
        kwargs['port'] = args.port
    server.start_server(manager, **kwargs)

# Block on the manager thread
manager.output_forever()
