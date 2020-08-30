"""Ergast data holder"""
import os
import pandas as pd


class ErgastLoader:
    """Creates a data object to hold ergast data"""

    def __init__(self, path, tables=None):
        """Loads ergast data to dataframes.

        path (str):
            Location in which data is stored. Must be stoered as csvs.

        tables (list):
            Subset of tables to load. If None all tables are loaded.

        """
        self.path = path
        if not tables:
            self.tables = [
                x.replace(".csv", "") for x in os.listdir(self.path) if ".csv" in x
            ]
        else:
            self.tables = tables
        self.data = {}
        self.load_tables()

    def load_tables(self):
        """Loads each csv listed in tables as a dataframe in the data dict"""
        for table in self.tables:
            self.data[table] = pd.read_csv(os.path.join(self.path, table + ".csv"))
