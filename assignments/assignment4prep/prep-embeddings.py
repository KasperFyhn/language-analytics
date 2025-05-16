from sentence_transformers import SentenceTransformer
import jsonlines
import numpy as np

sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_save(identifier: str, docs: list[str]):
    print(f"Creating {identifier} embeddings")
    embeddings = sentence_transformer.encode(docs, show_progress_bar=True)
    np.save(identifier, embeddings)
    print(f"Saved {identifier} embeddings")


with jsonlines.open("News_Category_Dataset_v3_subset.jsonl") as reader:
    data = list(reader)

headlines = [entry["headline"] for entry in data]
embed_and_save("embeddings_headlines", headlines)

headlines_and_descriptions = [entry["headline"] + "\n" + entry["short_description"]
                              for entry in data]
embed_and_save("embeddings_headlines+descriptions", headlines_and_descriptions)

