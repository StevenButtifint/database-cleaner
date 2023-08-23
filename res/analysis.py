from res.operations import *
from res.completeness import Completeness


class Analysis:
    def __init__(self):
        self.database = None
        self.attributes = None
        self.completeness_stats = Completeness(self.database)

    def set_database(self, database):
        self.database = database

    def set_attributes(self, database):
        self.attributes = get_csv_column_names(database)

    def get_attributes(self):
        return self.attributes

    def calculate_completeness_stats(self):
        self.completeness_stats.set_database(self.database)
        self.completeness_stats.calculate_stats()
