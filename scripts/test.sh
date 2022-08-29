#!/bin/bash

set -eux

pip install -e .

pytest
