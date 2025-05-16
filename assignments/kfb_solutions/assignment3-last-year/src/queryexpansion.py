import gensim.downloader as api

class QueryExpander:

    def __init__(self, model_name: str = "glove-wiki-gigaword-50"):
        self.model = api.load(model_name)

    def expand(self, query, n: int = 10) -> list[str]:
        most_similar = self.model.most_similar(query, topn=n)
        closest_words = [t[0] for t in most_similar]
        return [query] + closest_words