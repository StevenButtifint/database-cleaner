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

    def clean_empty_attributes(self):
        for column_name in self.clean_database.columns:
            column_data = self.clean_database[column_name]
            column_null_percentage = get_column_null_percentage(column_data)
            if column_null_percentage > self.empty_attribute_threshold:
                self.clean_database = self.clean_database.drop(columns=[column_name])

    def clean_empty_records(self):
        self.clean_database = self.clean_database.dropna()

    def clean_duplicate_records(self):
        self.clean_database = self.clean_database.drop_duplicates()

    def clean_numeric_outliers(self):
        attribute_name = self.get_numerical_outliers_attribute()
        minimum, maximum = self.get_numerical_range()
        cleaned = (self.clean_database[attribute_name] >= minimum) & (self.clean_database[attribute_name] <= maximum)
        self.clean_database = self.clean_database[cleaned]

    def clean_date_outliers(self):
        minimum, maximum = self.get_date_range()
        minimum_date = pd.to_datetime(minimum, format='%Y/%m/%d')
        maximum_date = pd.to_datetime(maximum, format='%Y/%m/%d')
        attribute = self.get_date_outliers_attribute()
        cleaned = (self.clean_database[attribute] >= minimum_date) & (self.clean_database[attribute] <= maximum_date)
        self.clean_database = self.clean_database[cleaned]

    def clean_invalid_syntax(self):
        regex_format = convert_format_to_regex(self.get_syntax_format())
        attribute = self.get_syntax_attribute()
        for index, row in self.clean_database.iterrows():
            if not re.match(regex_format, row[attribute]):
                self.clean_database.drop(index, inplace=True)

    def save_cleaned_database(self):
        dataframe_to_csv(self.get_clean_database(), self.database.get_name()[:-4]+"_cleaned")

    def create_cleaned_copy(self):
        self.set_clean_database(self.database.get_table())
        if self.remove_empty_attributes:
            self.clean_empty_attributes()
        if self.remove_empty_records:
            self.clean_empty_records()
        if self.remove_duplicate_records:
            self.clean_duplicate_records()
        if self.remove_numerical_outliers:
            self.clean_numeric_outliers()
        if self.remove_date_outliers:
            self.clean_date_outliers()
        if self.remove_invalid_syntax:
            self.clean_invalid_syntax()
        self.save_cleaned_database()
