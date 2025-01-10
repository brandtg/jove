#!/bin/bash
ENVDIR=env
rm -rf $ENVDIR
python3.11 -m venv $ENVDIR
source $ENVDIR/bin/activate
pip install -e .[dev]
