from res.operations import *


class Uniformity:
    def __init__(self, database_column):
        self.database_column = database_column
        self.column_length = len(database_column)
        self.unique_percentage = 0
        self.unique_count = 0

    def get_column_length(self):
        return self.column_length

    def get_database_column(self):
        return self.database_column

    def get_unique_count(self):
        return self.unique_count

    def get_unique_percentage_string(self):
        return str(self.unique_percentage) + "%"

