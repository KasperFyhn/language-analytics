#!/usr/bin/bash

set -e

# activate the environment
source ./env/bin/activate

# run the code
# first, I train a model on my Gutenberg data with 3-grams
python src/train.py gutenberg-model "data/gutenberg/*.txt" --ngram-size 3
# then, I generate a 100 word text with the model using top-k sampling of 5
python src/generate.py gutenberg-model --tokens 100 --top-k 5

# close the environment
deactivate