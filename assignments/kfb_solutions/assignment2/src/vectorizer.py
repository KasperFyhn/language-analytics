import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


class Vectors:
    def __init__(self, x_train, x_test, y_train, y_test, vectorizer):
        self.x_train = x_train
        self.x_train_feats = vectorizer.fit_transform(self.x_train)
        self.x_test = x_test
        self.x_test_feats = vectorizer.transform(self.x_test)
        self.y_train = y_train
        self.y_test = y_test
        self.vectorizer = vectorizer


def load_vectors():
    vectors_path = os.path.join("output", "vectors.joblib")
    if os.path.exists(vectors_path):
        print("Reusing vectors!")
        return joblib.load(vectors_path)
    else:
        print("Vectors not found, creating new vectors ...")
        filename = os.path.join("data", "fake_or_real_news.csv")
        data = pd.read_csv(filename, index_col=0)

        x = data["text"]
        y = data["label"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True,
            max_df=0.95,
            min_df=0.05,
            max_features=100
        )

        vectors = Vectors(x_train, x_test, y_train, y_test, vectorizer)

        if not os.path.exists(os.path.dirname(vectors_path)):
            os.makedirs(os.path.dirname(vectors_path))
        joblib.dump(vectors, vectors_path)

        return vectors
