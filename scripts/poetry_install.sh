#!/bin/bash
#
# Install poetry dependencies

# Set some failure conditions
set -o errexit   # Fail on any error
set -o pipefail  # Trace ERR through pipes
set -o errtrace  # Trace ERR through sub-shell commands

# Change to the parent directory
cd "${BASH_SOURCE%/*}"
cd ..

if [ ! -z "$(poetry env list)" ]; then
  echo "Removing old env..."
  poetry env remove python3
fi

echo "Upgrading pip..."
poetry run pip install --upgrade pip

echo "Installing dependencies..."
poetry install $@ $@
