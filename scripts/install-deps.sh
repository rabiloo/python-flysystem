#!/bin/bash

set -eux

pip install typing_extensions isort black flake8 pytest

if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
