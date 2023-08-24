from res.operations import select_csv, get_csv_data, get_csv_column_names


class Database:
    def __init__(self):
        self.name = None
        self.table = None
        self.attributes = None
        self.current_directory = None
        self.output_directory = None

