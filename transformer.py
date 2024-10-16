from sklearn.base import BaseEstimator, TransformerMixin
import ipaddress
import pandas as pd

class IpToNumericTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.columns:
            X[col] = X[col].apply(lambda x: int(ipaddress.IPv4Address(x)))
        return X

class DurationTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, start_col, end_col, new_col):
        self.start_col = start_col
        self.end_col = end_col
        self.new_col = new_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X[self.start_col] = pd.to_datetime(X[self.start_col], errors='coerce')
        X[self.end_col] = pd.to_datetime(X[self.end_col], errors='coerce')
        X[self.new_col] = (X[self.end_col] - X[self.start_col]).dt.total_seconds()
        X = X.drop(columns=[self.start_col, self.end_col], errors='ignore')
        return X
