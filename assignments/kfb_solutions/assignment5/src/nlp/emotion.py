import pandas as pd
from transformers import pipeline

from src.data.loader import load_data
from src.nlp.common import nlp_script_args


def main(data_path: str, output_path: str) -> None:
    data = load_data(data_path)

    classifier = pipeline("text-classification",
                          model="j-hartmann/emotion-english-distilroberta-base",
                          return_all_scores=True)

    print("Processing data")
    emotion_predictions = classifier(data["text"].tolist())

    # Create one column per emotion and one for the actual prediction
    emotions = [
        {pred["label"]: pred["score"] for pred in pred_group} |
        {"emotion_prediction": max(pred_group, key=lambda x: x["score"])["label"]}
        for pred_group in emotion_predictions
    ]
    emotion_df = pd.DataFrame(emotions)

    emotion_df.to_csv(output_path + "/emotion-analysis.csv", index=False)


if __name__ == "__main__":
    args = nlp_script_args()
    main(*args)
