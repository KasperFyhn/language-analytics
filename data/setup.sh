#!/bin/bash

curl -L -o gutenberg-nltk.zip https://www.kaggle.com/api/v1/datasets/download/nltkdata/gutenberg
unzip gutenberg-nltk.zip -d temp_gutenberg
mkdir -p gutenberg-nltk
mv temp_gutenberg/gutenberg/* gutenberg-nltk/
rm -rf temp_gutenberg gutenberg-nltk.zip

curl -L -o news-category-dataset.zip https://www.kaggle.com/api/v1/datasets/download/rmisra/news-category-dataset
unzip news-category-dataset.zip -d News_Category_Dataset_v3
rm -rf news-category-dataset.zip

curl -L -o imdb-dataset-of-50k-movie-reviews.zip https://www.kaggle.com/api/v1/datasets/download/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews
unzip imdb-dataset-of-50k-movie-reviews.zip -d imdb
rm -rf imdb-dataset-of-50k-movie-reviews.zip

# TODO: the USE corpus, fake news
