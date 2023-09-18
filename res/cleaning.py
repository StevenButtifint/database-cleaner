import pandas as pd
import copy

from res.operations import *


class Cleaning:
    def __init__(self, database):
        self.database = database
        self.clean_database = None
