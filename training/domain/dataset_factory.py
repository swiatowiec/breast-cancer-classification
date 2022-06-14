from domain.data_series import DataSeries
import pandas as pd
from typing import List, Dict
from sklearn.model_selection import train_test_split
from domain.dataset_repository import DatasetRepository


class DatasetFactory:
    def __init__(self,
                 dataset_repository: DatasetRepository,
                 test_size: int,
                 random_state: int):
        self._dataset_repository = dataset_repository
        self.test_size = test_size
        self.random_state = random_state

    def create_from_files(self, input_dir_path, file_name):
        data = self._dataset_repository.read_splitted_dataset(
            input_dir_path=input_dir_path, file_name=file_name)
        return DataSeries(data)

    def create_from_dict_list(records: List[Dict]):
        data = pd.DataFrame.from_records(records)
        return DataSeries(data)

    def split_data(self, to_split_input_dir_path, splitted_output_dir_path):
        data = self._dataset_repository.read_dataset(
            to_split_input_dir_path=to_split_input_dir_path)
        train, test = train_test_split(data,
                                       test_size=self.test_size,
                                       random_state=self.random_state)
        self._dataset_repository.save_dataset(
            splitted_output_dir_path, train, 'train')
        self._dataset_repository.save_dataset(
            splitted_output_dir_path, test, 'test')
