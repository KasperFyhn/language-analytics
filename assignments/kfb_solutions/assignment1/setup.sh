#!/usr/bin/bash

set -e

# create virtual env
python3 -m venv env

# activate env
source ./env/bin/activate

# install requirements
pip install --upgrade pip
pip install -r requirements.txt

# install SpaCy model
python -m spacy download en_core_web_md

# close the environment
deactivate