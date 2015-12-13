#!/usr/bin/python
# -*- coding: utf8 -*-
from RGBStrip import config_loader

def main():
    config_loader.load_config('./test_big.yaml')

if __name__ == '__main__':
    main()
