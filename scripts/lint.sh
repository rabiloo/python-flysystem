#!/bin/bash

set -eux

# exit-zero treats all errors as warnings.
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics --ignore W503

black . --check --target-version=py310 --line-length=120

isort . --check-only --profile=black --lbt=1 -l=120
