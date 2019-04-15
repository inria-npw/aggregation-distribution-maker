#!/usr/bin/env bash

if [[ ! -d ./venv ]]; then
    echo "Cannot dump requirements: You do not have any virtualenv (./venv directory) associated with this project."
else
    source ./venv/bin/activate
    pip freeze > ./requirements.txt
    deactivate
fi