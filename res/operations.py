from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import numpy as np
import datetime
import re


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
    return database.shape[0]


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


def count_invalid_entry_format(values, expected_format):
    invalid_count = 0
    regex_format = convert_format_to_regex(expected_format)
    for value in values:
        try:
            if not re.match(regex_format, value):
                invalid_count += 1
        except:
            invalid_count += 1
    return invalid_count


def convert_format_to_regex(entered_format):
    regex_pattern = ""
    for char in entered_format:
        if char == 'L':
            regex_pattern += r'[A-Za-z]'
        elif char == 'N':
            regex_pattern += r'\d'
        elif char == ' ':
            regex_pattern += r'\s'
        elif char == '?':
            regex_pattern += r'\?'
        elif char == '*':
            regex_pattern += r'.*'
        else:
            pass
    return regex_pattern


def count_unique_items(data_series):
    return len(data_series.unique())


def create_boxplot_graph(canvas, axis, data):
    boxprops = dict(facecolor='grey', edgecolor='white')
    whiskerprops = dict(color='white')
    flierprops = dict(color='white')
    medianprops = dict(color='white')
    capprops = dict(color='white')
    axis.boxplot(data, vert=False, patch_artist=True, boxprops=boxprops, whiskerprops=whiskerprops, flierprops=flierprops, medianprops=medianprops, capprops=capprops)
    axis.set_xlabel('Values', color='white')
    axis.spines['bottom'].set_color('white')
    axis.spines['left'].set_color('white')
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.tick_params(axis='x', colors='white')
    axis.tick_params(axis='y', colors='white')
    canvas.draw()


def create_null_over_time_graph(canvas, axis, data):
    x = np.arange(len(data))
    axis.bar(x, data, color='white')
    axis.set_xticks(x)
    axis.set_xticklabels([str(i+1) for i in range(len(data))])
    axis.set_xlabel("Time Frames")
    axis.set_ylabel("Null Total Per Time Frame")
    axis.set_title("Nulls Over 20 Time Frames")
    axis.spines['bottom'].set_color('white')
    axis.spines['left'].set_color('white')
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.xaxis.label.set_color('white')
    axis.yaxis.label.set_color('white')
    axis.title.set_color('white')
    axis.tick_params(axis='both', colors='white')
    canvas.draw()
