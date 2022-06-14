import glob
import pandas as pd
import os
import pathlib


class DatasetRepository:
    def read_dataset(self, to_split_input_dir_path):
        path_to_files = self.read_path = glob.glob(
            '{}/*.csv'.format(to_split_input_dir_path))
        for path in path_to_files:
            return pd.read_csv(path)

    def read_splitted_dataset(self, input_dir_path, file_name):
        path_to_files = self.read_path = glob.glob(
            '{}/{}.csv'.format(input_dir_path, file_name))
        for path in path_to_files:
            return pd.read_csv(path)

    def save_dataset(self, output_dir_path, dataset, name):
        pathlib.Path(output_dir_path).mkdir(parents=True, exist_ok=True)
        path = os.path.join(output_dir_path, name + '.csv')
        dataset.to_csv(path, index=False)
