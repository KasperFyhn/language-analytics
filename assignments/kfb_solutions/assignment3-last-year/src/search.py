import re

import pandas as pd
import nltk


nltk.download('punkt_tab')


def _preprocess(text: str):
    tokens = nltk.word_tokenize(text.lower())
    return ' '.join(tokens)


class SearchIndex:

    def __init__(self, csv_file_path: str):
        df = pd.read_csv(csv_file_path)
        df['preproc_text'] = df['text'].apply(_preprocess)
        self.df = df

    def search(self, query: str | list[str], artist: str = None) -> pd.DataFrame:
        if isinstance(query, str):
            query = [query]
        pattern = re.compile(f'{"|".join(query)}')

        if artist is None:
            df = self.df
        else:
            df = self.df[self.df['artist'] == artist]

        matches = df[df["preproc_text"].str.contains(pattern, regex=True)]

        return matches