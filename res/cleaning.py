import pandas as pd
import copy

from res.operations import *


class Cleaning:
    def __init__(self, database):
        self.database = database
        self.clean_database = None
        self.remove_empty_attributes = False
        self.remove_empty_records = False
        self.remove_duplicate_records = False
        self.remove_numerical_outliers = False
        self.remove_date_outliers = False
        self.remove_invalid_syntax = False
        self.empty_attribute_threshold = 0
        self.numerical_outliers_attribute = None
        self.numerical_range = None
        self.date_outliers_attribute = None
        self.date_range = None
        self.syntax_attribute = None
        self.syntax_format = None

    def set_database(self, database):
        self.database = database

    def set_clean_database(self, database):
        self.clean_database = copy.deepcopy(database)

    def set_output_location(self, output_location):
        self.database.set_output_directory(output_location)

    def set_remove_empty_attributes(self, state):
        self.remove_empty_attributes = state

    def set_remove_empty_records(self, state):
        self.remove_empty_records = state

    def set_empty_attribute_threshold(self, value):
        self.empty_attribute_threshold = value

    def set_remove_duplicate_records(self, state):
        self.remove_duplicate_records = state

    def set_remove_numerical_outliers(self, state):
        self.remove_numerical_outliers = state

    def set_numerical_outliers_attribute(self, attribute):
        self.numerical_outliers_attribute = attribute

    def set_numerical_range(self, minimum, maximum):
        self.numerical_range = [minimum, maximum]

    def set_remove_date_outliers(self, state):
        self.remove_date_outliers = state

    def set_date_outliers_attribute(self, attribute):
        self.date_outliers_attribute = attribute

    def set_date_range(self, minimum, maximum):
        self.date_range = [minimum, maximum]

    def set_remove_invalid_syntax(self, state):
        self.remove_invalid_syntax = state

    def set_syntax_attribute(self, attribute):
        self.syntax_attribute = attribute

    def set_syntax_format(self, syntax):
        self.syntax_format = syntax

    def get_database(self):
        return self.database

    def get_output_location(self):
        return self.database.get_output_directory()

    def get_remove_empty_attributes(self):
        return self.remove_empty_attributes

    def get_remove_empty_records(self):
        return self.remove_empty_records

    def get_empty_attribute_threshold(self):
        return self.empty_attribute_threshold

    def get_remove_duplicate_records(self):
        return self.remove_duplicate_records

    def get_remove_numerical_outliers(self):
        return self.remove_numerical_outliers

    def get_numerical_outliers_attribute(self):
        return self.numerical_outliers_attribute

    def get_numerical_range(self):
        return self.numerical_range

    def get_remove_date_outliers(self):
        return self.remove_date_outliers

    def get_date_outliers_attribute(self):
        return self.date_outliers_attribute

    def get_date_range(self):
        return self.date_range

    def get_remove_invalid_syntax(self):
        return self.remove_invalid_syntax

    def get_syntax_attribute(self):
        return self.syntax_attribute

    def get_syntax_format(self):
        return self.syntax_format

    def get_clean_database(self):
        return self.clean_database

