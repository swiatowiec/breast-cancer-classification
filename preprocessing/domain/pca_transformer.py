from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
from abc import ABC, abstractmethod


class AbstractPCA(ABC):
    def __init__(self, metadata=None):
        self._metadata = {} if metadata is None else metadata

    @abstractmethod
    def calculate(self, df):
        raise Exception("Method not implemented!")

    def metadata(self):
        return self._metadata

    def transform(self, df, target_column, n_components):
        if not self._metadata:
            self.calculate(df, target_column, n_components)
        X_fitted = self._metadata['scaler']
        target_pca = pd.DataFrame(df[target_column])
        X = X_fitted.transform(df)
        pca = PCA(n_components=n_components)
        pca_std = pca.fit(X, target_pca).transform(X)
        pca_std = pd.DataFrame(pca_std, columns=['COMP1', 'COMP2', 'COMP3'])
        pca_std = pca_std.merge(
            target_pca, left_index=True, right_index=True, how='left')


class PCATransformer(AbstractPCA):
    def calculate(self, df, target_column, n_components):
        data_pca = df.drop(target_column, axis=1)
        X_pca = data_pca.values
        X_fitted = StandardScaler().fit(X_pca)
        self._metadata['scaler'] = X_fitted
        self._metadata['n_components'] = n_components
