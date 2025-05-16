from sklearn.linear_model import LogisticRegression

from classifierutils import train_test_and_dump
from vectorizer import load_vectors

vectors = load_vectors()

classifier = LogisticRegression(random_state=42)

train_test_and_dump(
    vectors,
    classifier,
    "logistic_regression"
)