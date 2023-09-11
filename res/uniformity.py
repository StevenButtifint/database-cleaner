from res.operations import *


class Uniformity:
    def __init__(self, database_column):
        self.database_column = database_column
        self.column_length = len(database_column)
        self.unique_percentage = 0
        self.unique_count = 0

    def set_database_column(self, database_column):
        self.database_column = database_column

    def set_column_length(self, column_length):
        self.column_length = column_length

    def set_database(self, database_column):
        self.set_database_column(database_column)
        self.set_column_length(len(database_column))

    def set_unique_percentage(self, unique_percentage):
        self.unique_percentage = round(unique_percentage, 2)

    def set_unique_count(self, unique_count):
        self.unique_count = unique_count

    def get_column_length(self):
        return self.column_length

    def get_database_column(self):
        return self.database_column

    def get_unique_count(self):
        return self.unique_count

    def get_unique_percentage_string(self):
        return str(self.unique_percentage) + "%"

