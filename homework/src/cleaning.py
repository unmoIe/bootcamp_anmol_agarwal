import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def fill_missing_median(df, cols):
    """
    Fill missing data in the given columns(cols) with the median
    Parameters:
        df : dataframe
        cols : target columns
    Returns :
        df: dataframe with missing data in target columns replace with median
    """
    df_copy = df.copy()
    if cols is None:
        cols = df.select_dtypes(include=np.number).columns
    for col in cols:
        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy

def drop_missing(df, cols=None, threshold=None):
    """
    Drop missing data in the given rows where less than threshold % of target columns are non null
    Parameters:
        df : dataframe
        cols : target columns
        threshold : threshold %
    Returns :
        df: dataframe with rows dropped where missing data(Nulls) in target columns was more than threshold%
    """
    df_copy = df.copy()
    if cols is not None:
        return df_copy.dropna(subset=cols)
    if threshold is not None:
        return df_copy.dropna(thresh=int(threshold*df_copy.shape[1]))
    return df_copy.dropna()

def normalize_data(df, cols=None, method='minmax'):
    """
    Fill missing data using normalization. Either min-max(linear) strategy or Standard(normal) strategy
    Parameters:
        df : dataframe
        cols : target columns
        method : minmax/standard
    Returns :
        df: dataframe with missing data filled using normalzation strategy
    """
    df_copy = df.copy()
    if cols is None:
        cols = df_copy.select_dtypes(include=np.number).columns
    if method=='minmax':
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()
    df_copy[cols] = scaler.fit_transform(df_copy[cols])
    return df_copy