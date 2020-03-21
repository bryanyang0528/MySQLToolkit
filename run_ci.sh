#!/bin/bash

set -ex

nosetests \
    --logging-level=INFO \
    --detailed-errors \
    --verbosity=2 \
    --with-coverage \
    --cover-package .

python -m coverage xml