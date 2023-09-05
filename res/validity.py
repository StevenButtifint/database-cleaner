from res.operations import *


class Validity:
    def __init__(self, database_column):
        self.database_column = database_column
        self.column_length = len(database_column)
        self.invalid_count = 0
        self.invalid_percentage = 0

    def set_database_column(self, database_column):
        self.database_column = database_column

    def set_invalid_count(self, invalid_count):
        self.invalid_count = invalid_count

    def set_invalid_percentage(self, invalid_percentage):
        self.invalid_percentage = round(invalid_percentage, 2)

    def get_invalid_count(self):
        return self.invalid_count

    def get_invalid_percentage(self):
        return self.invalid_percentage

    def get_invalid_percentage_string(self):
        return str(self.get_invalid_percentage())+'%'

