"""Pirelli data holder"""
import os
import pandas as pd


def load_pirelli_tyre_data(path='data/pirelli'):
    """Return df containing all data in data/pirelli"""
    dfs = []
    for f in os.listdir(path):
        dfs.append(pd.read_csv(os.path.join(path, f)))
    return pd.concat(dfs)