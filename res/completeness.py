from res.operations import *


class Completeness:
    def __init__(self, database):
        self.database = database
        self.overall_null_percentage = None
        self.null_count_per_column = None
        self.null_over_time = None

