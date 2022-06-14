from enum import Enum
from typing import List
import pandas as pd
from domain.filler import MedianValueFiller, MeanValueFiller
from domain.pca_transformer import PCATransformer


class FulfillmentMode(Enum):
    MEAN = 'mean'
    MEDIAN = 'median'


class Dataset:
    def __init__(self, df: pd.DataFrame):
        self._data = df

    def fulfill_missing_values(self,
                               filler: MeanValueFiller or MedianValueFiller,
                               columns_to_fulfill: List[str]):
        self._data[columns_to_fulfill] = filler.fill(
            self._data[columns_to_fulfill])

    def change_target_to_numeric(self,
                                 columns_to_change: List[str]):
        self._data[columns_to_change].replace(dict(M=1, B=0), inplace=True)

    def transform_with_PCA(self,
                           transformer: PCATransformer,
                           target_column: List,
                           n_components: int,
                           ):
        self._data = transformer.transform(
            self._data, target_column, n_components)

    def get_data(self):
        return self._data
