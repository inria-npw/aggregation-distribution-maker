#!/usr/bin/env bash

source ./venv/bin/activate

export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/src"

python3 ./src/fr/inria/npw/make_aggregation_dist.py "$@"

deactivate