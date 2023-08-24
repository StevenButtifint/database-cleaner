from res.operations import select_csv, get_csv_data, get_csv_column_names


class Database:
    def __init__(self):
        self.name = None
        self.table = None
        self.attributes = None
        self.current_directory = None
        self.output_directory = None

    def select_database(self):
        database_directory = select_csv()
        if len(database_directory) > 0:
            self.set_current_directory(database_directory)
            self.set_name(database_directory)
            self.set_table(database_directory)
            self.set_attributes()

    def set_current_directory(self, directory):
        self.current_directory = directory

    def set_table(self, directory):
        self.table = get_csv_data(directory)

    def set_name(self, directory):
        self.name = directory.split("/")[-1]

    def set_attributes(self):
        self.attributes = get_csv_column_names(self.table)

    def set_output_directory(self):
        self.output_directory = select_file()

    def get_table(self):
        return self.table

    def get_attributes(self):
        return self.attributes

    def get_current_directory(self):
        return self.current_directory

    def get_output_directory(self):
        return self.output_directory

    def total_record_count(self):
        return get_database_record_count(self.table)
