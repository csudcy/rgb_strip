#!/bin/bash
#
# Update poetry dependencies

# Change to the parent directory
cd "${BASH_SOURCE%/*}"
cd ..

echo "Updating dependencies..."
poetry add $@

echo "Generating requirements.txt file..."
poetry export --format=requirements.txt --without-hashes > requirements.txt
