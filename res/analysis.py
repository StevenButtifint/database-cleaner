from res.operations import *
from res.completeness import Completeness


class Analysis:
    def __init__(self):
        self.database = None
        self.completeness_stats = Completeness(self.database)

    def set_database(self, database):
        self.database = database

    def calculate_completeness_stats(self):
        self.completeness_stats.set_database(self.database)
        self.completeness_stats.calculate_stats()
