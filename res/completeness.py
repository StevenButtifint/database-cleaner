from res.operations import *


class Completeness:
    def __init__(self, database):
        self.database = database
        self.overall_null_percentage = None
        self.null_count_per_column = None
        self.null_over_time = None

    def get_overall_null_percentage(self):
        return self.overall_null_percentage

    def get_null_count_per_column(self):
        return self.null_count_per_column

    def set_database(self, database):
        self.database = database

    def set_overall_null_percentage(self):
        self.overall_null_percentage = get_null_count_percentage(self.database.get_table())

    def set_null_count_per_column(self):
        self.null_count_per_column = get_null_count_per_column(self.database.get_table())

    def set_null_over_time(self):
        self.null_over_time = get_null_count_over_time(self.database.get_table())

    def calculate_stats(self):
        self.set_overall_null_percentage()
        self.set_null_count_per_column()
        self.set_null_over_time()

    def clear_stats(self):
        self.overall_null_percentage = None
        self.null_count_per_column = None
        self.null_over_time = None
