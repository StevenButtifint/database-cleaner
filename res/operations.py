import pandas as pd


def get_csv_data(directory):
    file_data = pd.read_csv(directory)
    return file_data

