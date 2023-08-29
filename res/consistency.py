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

