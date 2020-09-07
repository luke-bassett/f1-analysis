"""Pirelli data holder"""
import os
import re
import pandas as pd


class PirelliLoader:
    """Creates a data object to hold pirelli tyre data"""

    def __init__(self, path):
        """Loads pirelli data to dataframes.

        path (str):
            Location in which data is stored. Must be stored as csvs.

        """

        self.path = path
        self.data = {}
        self.load()

    def load(self):
        """Loads each csv listed in tables as a dataframe in the data dict"""
        pat = r"[\D]*(\d{4})[\D]*"
        for f in os.listdir(self.path):
            year = int(re.findall(pat, f)[0])
            self.data[year] = pd.read_csv(os.path.join(self.path, f))
