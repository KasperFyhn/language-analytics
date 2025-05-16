from glob import glob

import pandas as pd

def load_data(data_dir: str = "data/") -> pd.DataFrame:
    """Loads all scraped JSON files in the data directory and returns them as one dataframe."""
    files = glob(data_dir + '/*.json')
    zone_dfs = [pd.read_json(file) for file in files]
    return pd.concat(zone_dfs).reset_index(drop=True)
