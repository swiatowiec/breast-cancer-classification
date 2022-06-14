from abc import ABC, abstractmethod
from domain.dataset import FulfillmentMode


class AbstractValueFiller(ABC):
    def __init__(self, metadata=None):
        self._metadata = {} if metadata is None else metadata

    @abstractmethod
    def calculate(self, df):
        raise Exception("Method not implemented!")

    def fill(self, df):
        if not self._metadata:
            self.calculate(df)
        for column_name, column_data in df.iteritems():
            df[column_name].fillna(
                value=self._metadata['filler_value'][column_name], inplace=True)
        return df

    def metadata(self):
        return self._metadata


class MeanValueFiller(AbstractValueFiller):
    def calculate(self, df):
        self._metadata['filler_type'] = FulfillmentMode.MEAN
        self._metadata['filler_value'] = {}
        for column_name, column_data in df.iteritems():
            self._metadata['filler_value'][column_name] = column_data.mean()


class MedianValueFiller(AbstractValueFiller):
    def calculate(self, df):
        self._metadata['filler_type'] = FulfillmentMode.MEDIAN
        self._metadata['filler_value'] = {}
        for column_name, column_data in df.iteritems():
            self._metadata['filler_value'][column_name] = column_data.median()
