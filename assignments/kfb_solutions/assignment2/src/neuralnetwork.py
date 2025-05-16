from sklearn.neural_network import MLPClassifier

from classifierutils import train_test_and_dump
from vectorizer import load_vectors

vectors = load_vectors()

classifier = MLPClassifier(
    activation="logistic",
    hidden_layer_sizes=(20,),
    max_iter=1000,
    random_state=42
)

train_test_and_dump(
    vectors,
    classifier,
    "neural_network"
)