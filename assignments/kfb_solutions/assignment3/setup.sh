#!/usr/bin/bash

set -e

# create virtual env
python3 -m venv env

# activate env
source ./env/bin/activate

# install requirements
pip install --upgrade pip
pip install -r requirements.txt

# close the environment
deactivate