#!/bin/bash

# Get to the rgb_strip directory
cd "$(dirname "$0")"
cd ..

# Start the process
nohup python -m RGBStrip --server ./configs/prod.yaml &
