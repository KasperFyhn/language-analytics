import jsonlines
import pandas as pd

with jsonlines.open("News_Category_Dataset_v3.json") as reader:
    df = pd.DataFrame(reader)

categories = {"TRAVEL", "SPORTS", "COMEDY", "BUSINESS", "FOOD & DRINK", "HOME & LIVING", "CRIME"}

select_categories = df[df["category"].isin(categories)]

subset = select_categories.groupby("category").sample(2000)

with jsonlines.open("News_Category_Dataset_v3_subset.jsonl", mode="w") as writer:
    writer.write_all(subset.to_dict(orient="records"))

