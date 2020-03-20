#!/bin/bash

set -ex

nosetests \
    --logging-level=INFO \
    --detailed-errors \
    --verbosity=2

python -m coverage xml