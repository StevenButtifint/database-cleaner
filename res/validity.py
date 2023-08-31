from res.operations import *


class Validity:
    def __init__(self, database_column):
        self.database_column = database_column
        self.column_length = len(database_column)
        self.invalid_count = 0
        self.invalid_percentage = 0

