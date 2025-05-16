import os

import joblib
from sklearn.metrics import classification_report


def train_test_and_dump(vectors, classifier, name):
    print("Training:", name)
    classifier.fit(vectors.x_train_feats, vectors.y_train)

    print("Running prediction and creating output ...")
    y_pred = classifier.predict(vectors.x_test_feats)

    report = classification_report(vectors.y_test, y_pred)
    with open(os.path.join("output", f"{name}_report.txt"), "w") as file:
        file.write(report)

    joblib.dump(classifier, os.path.join("output", f"{name}_model.joblib"))