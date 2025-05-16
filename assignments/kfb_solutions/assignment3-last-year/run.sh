#!/usr/bin/bash

set -e

# activate the environment
source ./env/bin/activate

# run the code
python src/logisticregression.py

# close the environment
deactivate