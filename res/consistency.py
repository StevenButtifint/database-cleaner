from res.operations import *


class Consistency:
    def __init__(self, database):
        self.database = database
        self.invalid_record_count = 0
        self.invalid_record_percentage = 0

