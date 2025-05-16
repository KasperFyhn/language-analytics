import argparse
import math
from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.data.loader import load_data


EMOTION_COLUMNS = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'neutral']


def create_grouped_piecharts_avg_prob_by_zone(df: pd.DataFrame, output_path: str = "output/"):
    zones = df['zone'].unique()
    num_zones = len(zones)

    # Determine the layout of subplots
    cols = int(math.sqrt(num_zones))  # You can change the number of columns
    rows = num_zones // cols # Calculate the number of rows needed
    if num_zones % cols != 0:
        rows += 1

    fig, axes = plt.subplots(rows, cols, figsize=(7 * cols, 5 * rows))  # Adjust figure size
    axes = axes.reshape(-1)

    for i, zone in enumerate(zones):
        zone_df = df[df['zone'] == zone][EMOTION_COLUMNS].sum()
        ax = axes[i]
        ax.pie(zone_df, labels=zone_df.index, autopct='%1.1f%%', startangle=140)
        ax.set_title(f'Zone: {zone}')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()
    plt.savefig(Path(output_path) / "emotions_by_zone_piecharts.png")
    plt.close()


def create_topics_by_zone(df: pd.DataFrame, output_path: str = "output/"):
    cross_tabulation = pd.crosstab(df["topic_name"], df["zone"], normalize="index")
    sns.heatmap(cross_tabulation, cmap="Blues")
    plt.title("Topics by zone")
    plt.yticks([i + .5 for i in range(len(cross_tabulation))], cross_tabulation.index, rotation=0)  # Explicitly set y-ticks

    plt.savefig(
        Path(output_path) /  "topics_by_zone.png",
        bbox_inches="tight"  # do not crop labels
    )
    plt.close()


def create_emotion_by_topics(df: pd.DataFrame, output_path: str = "output/"):
    cross_tabulation = pd.crosstab(df["topic_name"], df["emotion_prediction"], normalize="index")
    sns.heatmap(cross_tabulation, cmap="Blues")
    plt.title("Emotions by topics")
    plt.yticks([i + .5 for i in range(len(cross_tabulation))], cross_tabulation.index, rotation=0)  # Explicitly set y-ticks

    plt.savefig(
        Path(output_path) /  "emotion_by_topic.png",
        bbox_inches="tight"  # do not crop labels
    )
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', '-o', type=str, default='output/',
                        help='Directory in which to find NLP analysis output and output figures.')
    args = parser.parse_args()

    df_data = load_data()
    df_emotion = pd.read_csv(args.output_path + "emotion-analysis.csv")
    df_topics = pd.read_csv(args.output_path + "topic-analysis.csv")

    df = pd.concat([df_data, df_emotion, df_topics],axis=1)
    print(df.head())  # Sanity check

    create_topics_by_zone(df, args.output_path)
    create_emotion_by_topics(df, args.output_path)
    create_grouped_piecharts_avg_prob_by_zone(df, args.output_path)
