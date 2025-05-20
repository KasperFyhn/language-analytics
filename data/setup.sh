#!/bin/bash

download_and_unpack() {
  echo "$1"
  curl -s -L -o temp.zip "$2" && unzip -q -o temp.zip -d "$1" && rm temp.zip
}

download_and_unpack gutenberg-nltk "https://www.kaggle.com/api/v1/datasets/download/nltkdata/gutenberg"
echo "  Converting to UTF-8"

mkdir -p gutenberg-nltk
for file in gutenberg-nltk/gutenberg/*.txt; do
  iconv -f LATIN1 -t UTF-8 "$file" > "gutenberg-nltk/$(basename "$file")"
done
rm -rf gutenberg-nltk/gutenberg

download_and_unpack News_Category_Dataset_v3 "https://www.kaggle.com/api/v1/datasets/download/rmisra/news-category-dataset"

download_and_unpack imdb "https://www.kaggle.com/api/v1/datasets/download/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"

download_and_unpack fake-news "https://www.kaggle.com/api/v1/datasets/download/hassanamin/textdb3"

download_and_unpack USE_corpus "https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2457/allzip"
(
  echo "  Converting to UTF-8"
  cd USE_corpus || exit
  unzip -o -q USEcorpus.zip && rm USEcorpus.zip
  mv USEcorpus temp
  mkdir -p USEcorpus
  for file in temp/**/*.txt; do
    # Create target subdir if needed, then convert
    mkdir -p "USEcorpus/$(dirname "${file#temp/}")" && \
    iconv -f LATIN1 -t UTF-8 "$file" > "USEcorpus/${file#temp/}"
  done
  rm -rf temp
)