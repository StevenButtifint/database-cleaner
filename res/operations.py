import pandas as pd


def get_csv_data(directory):
    file_data = pd.read_csv(directory)
    return file_data


def get_null_count_per_column(dataset):
    return dataset.isnull().sum()


def get_null_count_percentage(dataset):
    cell_count = np.product(dataset.shape)
    null_count = get_null_count_per_column(dataset).sum()
    return round((null_count / cell_count) * 100, 2)


