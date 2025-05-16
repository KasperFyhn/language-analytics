import os
from collections import Counter, defaultdict
from glob import glob
import random

import joblib
from nltk import download, word_tokenize, ngrams  # function for generating n-grams
from tqdm import tqdm

download('punkt')  # tokenizer model


class NgramModel:

    def __init__(self, name: str, ngram_size: int = 2):
        self.name = name
        self.n_gram_size = ngram_size

        self._ngram_model = None


    def train(self, glob_pattern: str):
        # a master counter for all n-grams from the data
        ngram_counter = Counter()
        tokens_total = 0

        # iterate over the books and collect n-grams for the counter object
        files = glob(glob_pattern)
        for filename in tqdm(files, desc='Collecting n-grams'):
            with open(filename) as f:
                text = f.read()

            # create tokens and n-grams and count them
            tokens = word_tokenize(text)
            tokens_total += len(tokens)
            book_ngrams = ngrams(tokens, self.n_gram_size)

            # add all ngram counts to the master counter by using the update() method
            ngram_counter.update(book_ngrams)

        # this will be a dict of Counters, i.e. with the structure: {("a", "nice"): Counter({"bee": 731})}
        ngram_model_raw = defaultdict(Counter)

        for ngram, count in ngram_counter.items():
            history, continuation = ngram[:-1], ngram[-1]
            ngram_model_raw[history][continuation] += count

        ngram_model = dict()
        for ngram, counter in ngram_model_raw.items():
            # normalize counts by dividing it with the total counts for that "history" n-gram
            summed_count = sum(counter.values())
            ngram_model[ngram] = {word: count / summed_count
                                  for word, count in counter.items()}

        self._ngram_model = ngram_model

    def conditional_probability_distribution(self, history: tuple[str]):
        """Return p(w|history)"""
        return self._ngram_model.get(history, {})



    def generate(self, seed: tuple[str] = None, tokens: int = 25, top_k: int = None):
        """Generate a number of tokens given a seed.
        top_k is an optional argument to do top-k sampling."""
        if seed is None:
            seed = random.choice(list(self._ngram_model.keys()))
        # p rint the beginning of the  text: the seed
        for word in seed:
            print(word, end=' ')

        previous = seed
        for i in range(tokens):
            # conditional probability distribution given the previous n-1 tokens
            next_word_dist = self.conditional_probability_distribution(previous)

            if next_word_dist == {}:
                print("## Unknown history. Cannot predict more! ##")
                break

            if top_k is not None:
                top_k_words_and_probs = sorted(next_word_dist.items(), key=lambda x: x[1], reverse=True)[:top_k]
                next_word_dist = {key: value for key, value in top_k_words_and_probs}

            # create a list of words and their corresponding probabilities (as "weights")
            words = []
            weights = []
            for word, count in next_word_dist.items():
                words.append(word)
                weights.append(count)

            # make a random choice from the word list using the weights
            next_word = random.choices(words, weights=weights)[0]

            print(next_word, end=' ')

            # the new history that we should look up is the tail of the previous history and the new token
            previous = previous[1:] + (next_word,)

    def save(self, models_path: str = "models/"):
        """Save the model."""
        os.makedirs(models_path, exist_ok=True)
        joblib.dump(self, f'{models_path}/{self.name}.ngram')

    @classmethod
    def load(cls, model_name: str, models_path: str = "models/") -> "NgramModel":
        """Load and return an existing model"""
        return joblib.load(f'{models_path}/{model_name}.ngram')
