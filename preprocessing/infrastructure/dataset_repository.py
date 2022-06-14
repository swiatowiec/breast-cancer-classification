import os
from typing import Dict
import pandas as pd
import glob
from domain.dataset import Dataset


class DatasetRepository: 
    def read_dataset(self,
                     input_dir_path: str) -> Dataset:
        usecols = ['diagnosis', 'radius_mean', 'texture_mean',
                   'perimeter_mean', 'area_mean', 'smoothness_mean',
                   'compactness_mean', 'concavity_mean', 'concave points_mean',
                   'symmetry_mean', 'fractal_dimension_mean', 'radius_se',
                   'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
                   'compactness_se', 'concavity_se', 'concave points_se',
                   'symmetry_se', 'fractal_dimension_se', 'radius_worst',
                   'texture_worst', 'perimeter_worst', 'area_worst',
                   'smoothness_worst', 'compactness_worst', 'concavity_worst',
                   'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst']
        path_to_files = self.read_path = glob.glob(
            '{}/*.csv'.format(input_dir_path))
        for path in path_to_files:
            df = pd.read_csv(path, usecols=usecols)
            return Dataset(df)

    def read_measurements(measurements) -> Dataset:
        df = pd.DataFrame(measurements)
        return Dataset(df)

    def save_dataset(self,
                     dataset: Dataset,
                     output_dir_path: str,
                     output_file_name: str):
        df = dataset.get_data()
        os.mkdir(output_dir_path)
        df.to_csv(os.path.join(output_dir_path,
                               output_file_name,
                               ), index=False)
