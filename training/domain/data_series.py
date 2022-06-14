from enum import Enum
import pandas as pd


class DataSeries:
    def __init__(self, data):
        self.data = data

    def get_featues_and_target(self):
        X = self.data.loc[:, self.data.columns != 'diagnosis']
        y = self.data['diagnosis']
        return X, y

    def test(self, model, X):
        prediction = model.predict(X)
        return prediction

    def predict(self, model):
        prediction = model.predict(self.data)
        df = pd.DataFrame()
        df['id_number'] = self.data['id_number']
        df['diagnosis'] = prediction
        return df


class TrainingMode(Enum):
    LOG_REG_GRID_SEARCH = 'log_reg_grid_search'
    LOG_REG_RFE = 'log_reg_rfe'
    BAGGING = 'bagging'
    BOOSTING = 'boosting'
