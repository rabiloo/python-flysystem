#!/bin/bash

python -m pip install --upgrade pip
pip install black build flake8 pytest
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
