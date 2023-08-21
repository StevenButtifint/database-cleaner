from res.operations import *
from res.completeness import Completeness


class Analysis:
    def __init__(self, database):
        self.database = database
        self.completeness_stats = Completeness(self.database)

    def calculate_completeness_stats(self):
        self.completeness_stats.set_database(self.database)
        self.completeness_stats.calculate_stats()
