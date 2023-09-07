from res.operations import *


class Uniformity:
    def __init__(self, database_column):
        self.database_column = database_column
        self.column_length = len(database_column)
        self.unique_percentage = 0
        self.unique_count = 0

