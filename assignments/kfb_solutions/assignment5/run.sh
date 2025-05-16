#!/usr/bin/bash

# activate the environment
source ./env/bin/activate

# run the code
python -m src.data.scraper data eastern-kingdoms/elwynn-forest eastern-kingdoms/westfall \
  eastern-kingdoms/redridge-mountains eastern-kingdoms/duskwood -x "duskwood mission"
python -m src.nlp.topic data/ -o output/
python -m src.nlp.emotion data/ -o output/
python -m src.visualization

# close the environment
deactivate