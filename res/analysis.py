from res.operations import *
from res.completeness import Completeness
from res.consistency import Consistency


class Analysis:
    def __init__(self, database):
        self.database = database
        self.completeness_stats = Completeness(self.database)
        self.consistency = Consistency(self.database)

    def set_database(self, database):
        self.database = database

    def get_database(self):
        return self.database

    def calculate_completeness_stats(self):
        self.completeness_stats.calculate_stats()
