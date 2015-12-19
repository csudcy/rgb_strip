#!/usr/bin/python
# -*- coding: utf8 -*-
import sys

from RGBStrip import config_loader


if len(sys.argv) != 2:
    print 'Usage: python -m RGBStrip config_file.yaml'
    sys.exit(1)
config_loader.load_config(sys.argv[1])
