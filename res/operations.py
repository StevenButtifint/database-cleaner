import pandas as pd


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


