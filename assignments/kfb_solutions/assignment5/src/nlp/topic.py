import argparse
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

import pandas as pd
from bertopic import BERTopic

from src.data.loader import load_data
from src.nlp.common import nlp_script_args


def main(data_path: str, output_path: str) -> None:
    data = load_data(data_path)

    vectorizer = TfidfVectorizer(
        stop_words='english',
        lowercase=True,
        ngram_range=(1, 3),
    )

    title_and_text = data["title"] + "\n" + data["text"]

    topic_model = BERTopic(language="english",
                           vectorizer_model=vectorizer,
                           verbose=True,
                           min_topic_size=5)
    topics, probs = topic_model.fit_transform(title_and_text)

    df = pd.DataFrame({"topic_id": topics})
    topic_names = {t["Topic"]: t["Name"]
                   for t in topic_model.get_topic_info().to_dict(orient="records")}
    df["topic_name"] = df["topic_id"].map(topic_names)

    df.to_csv(output_path + "topic-analysis.csv", index=False)


if __name__ == "__main__":
    args = nlp_script_args()

    main(*args)
