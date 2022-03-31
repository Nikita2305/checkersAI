#!/bin/bash
ROOT="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; cd .. ; pwd -P )"
python3 -m pip install -r $ROOT/requirements.txt
