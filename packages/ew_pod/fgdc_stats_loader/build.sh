#!/bin/bash

set -e

virtualenv --without-pip virtualenv --python=python3.11
python3.11 -m pip install -r requirements.txt --target virtualenv/lib/python3.11/site-packages