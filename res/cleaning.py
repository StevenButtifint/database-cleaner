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

