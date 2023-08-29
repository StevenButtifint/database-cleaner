import pandas as pd
import numpy as np
import datetime


def get_csv_data(directory):
    file_data = pd.read_csv(directory)
    return file_data


def get_csv_column_names(database):
    return list(database.columns)


def get_null_count_per_column(dataset):
    series = dataset.isnull().sum()
    ordered_series = series.sort_values(ascending=False)
    return ordered_series


def get_null_count_percentage(dataset):
    cell_count = np.product(dataset.shape)
    null_count = get_null_count_per_column(dataset).sum()
    return round((null_count / cell_count) * 100, 2)


def get_null_count_over_time(dataset):
    row_nulls_count = dataset.isnull().sum(axis=1).tolist()
    total_count = len(row_nulls_count)
    interval_size = total_count // 20
    tenth_sums = []
    current_position = 0
    for _ in range(20):
        end_position = current_position + interval_size
        tenth_sum = sum(row_nulls_count[current_position:end_position])
        tenth_sums.append(tenth_sum)
        current_position = end_position
    return tenth_sums


def count_numeric_outliers(database_column, minimum, maximum):
    outliers = 0
    try:
        float_min = float(minimum)
        float_max = float(maximum)
        for value in database_column:
            try:
                if (value > float_max) | (value < float_min):
                    outliers += 1
            except:
                pass
    except:
        pass
    return outliers


def count_date_outliers(database_column, minimum_date, maximum_date):
    outliers = 0
    try:
        date_min = datetime.strptime(minimum_date, "%d/%m/%Y")
        date_max = datetime.strptime(maximum_date, "%d/%m/%Y")
        for date in database_column:
            try:
                date = datetime.strptime(date, "%d/%m/%Y")
                if (date > date_max) | (date < date_min):
                    outliers += 1
            except:
                pass
    except:
        pass
    return outliers


def get_database_record_count(database):
    return database.shape[1]


def calculate_tenth_sums(data):
    total_count = len(data)
    interval_size = total_count // 10
    tenth_sums = []
    current_position = 0
    for _ in range(10):
        end_position = current_position + interval_size
        tenth_sum = sum(data[current_position:end_position])
        tenth_sums.append(tenth_sum)
        current_position = end_position
    return tenth_sums


def select_file():
    path = QFileDialog.getExistingDirectory(caption='Select a Folder')
    return path


def select_csv():
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFiles)
    file_dialog.setNameFilter("CSV files (*.csv)")
    if file_dialog.exec_():
        return file_dialog.selectedFiles()[0]

