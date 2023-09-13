from res.operations import *


class Consistency:
    def __init__(self, database):
        self.database = database
        self.invalid_record_count = 0
        self.invalid_record_percentage = 0

    def get_invalid_record_count(self):
        return self.invalid_record_count

    def get_invalid_record_percentage(self):
        return self.invalid_record_percentage

    def get_invalid_record_percentage_string(self):
        return str(self.get_invalid_record_percentage())+'%'

    def set_database(self, database):
        self.database = database

    def set_numeric_invalid_record_count(self, column_name, minimum, maximum):
        self.invalid_record_count = count_numeric_outliers(self.database.table[column_name], minimum, maximum)

    def set_invalid_record_percentage(self):
        database_record_count = self.database.total_record_count()
        self.invalid_record_percentage = round((self.invalid_record_count / database_record_count)*100, 2)

    def set_date_invalid_record_count(self, column_name, minimum, maximum):
        self.invalid_record_count = count_date_outliers(self.database.table[column_name], minimum, maximum)

    def calculate_numeric_invalid_records(self, column_name, minimum, maximum):
        self.set_numeric_invalid_record_count(column_name, minimum, maximum)
        self.set_invalid_record_percentage()

    def calculate_date_invalid_records(self, column_name, minimum, maximum):
        self.set_date_invalid_record_count(column_name, minimum, maximum)
        self.set_invalid_record_percentage()
