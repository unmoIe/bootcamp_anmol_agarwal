import os
import pandas as pd
import datetime as dt
import pathlib
import sys
from src.config import *

load_env()

def getDataPath(isProcessed):
    return( pathlib.Path("../"+os.getenv('DATA_DIR_PROCESSED')) if isProcessed else pathlib.Path("../"+os.getenv('DATA_DIR_RAW')))

def validate_df( df, required_cols, dtypes_map, ticker, expected_shape ):
    msgs = {}
    missing = [ c for c in required_cols if c not in df.columns ]
    if missing:
        msgs['missing_cols'] = f"Missing columns: {missing}"
    if df.shape != expected_shape:
        msgs['shape'] = f"Shape is {df.shape}, but expected {expected_shape}"
    for col, dtype in dtypes_map.items():
        if (col,ticker) in df.columns:
            try:
                if dtype == 'datetime64[ns]':
                    df[(col,ticker)] = pd.to_datetime(df[(col,ticker)])
                elif dtype == 'float64':
                    df[(col,ticker)] = pd.to_numeric(df[(col,ticker)])
                elif dtype == 'int64':
                    df[(col,ticker)] = pd.to_numeric(df[(col,ticker)])
            except Exception as e:
                msgs[f'dtype{col}'] = f"Failed to coerce {col} to {dtype}: {e}"
    na_counts = df.isna().sum().sum()
    msgs['na_total'] = f"Total NA values: {na_counts}"
    return msgs

def get_summary_stats( df, pivot, agg_col ):
    return( df.groupby(pivot)[agg_col].mean() )
    
def write_df( df, isProcessed, suffix, file_name ):
    fdir = getDataPath(isProcessed)
    try:    
        if( suffix.lower()=="csv" ):
            df.to_csv(fdir/file_name, index=False)
        elif( suffix.lower()=="parquet" ):
            df.to_parquet(fdir/file_name,index=False)
        print("Successfully saved file to: ", fdir)
    except OSError:
        print(f"Directory {fdir} doesnt exist, creating it now and trying to save again.")
        fdir.mkdir(parents=True, exist_ok=True)
        if( suffix.lower()=="csv" ):
            df.to_csv(fdir/file_name, index=False)
        elif( suffix.lower()=="parquet" ):
            df.to_parquet(fdir/file_name,index=False)
        print("Successfully saved file to: ", fdir)
    except ImportError:
        print('Parquet engine not available. Install pyarrow or fastparquet to complete this step.')
    except Exception as e:
        print(f"Some error occured - {e}")

def read_df( isProcessed, suffix, file_name ):
    fdir = getDataPath(isProcessed)
    try:
        if( suffix.lower()=="csv" ):
            df = pd.read_csv(fdir/file_name)
        elif( suffix.lower()=="parquet" ):
            df = pd.read_parquet(fdir/file_name)
    except Exception as e:
        print(f"Some exception caught - {e}")
        df=pd.DataFrame()
    finally:
        return(df)

def save_stamp():
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")

def get_filename(prefix, meta, suffix):
    mid = "_".join([f"{k}-{str(v).replace(' ', '-').replace('/','|')[:100]}" for k, v in meta.items()])
    return f"{prefix}_{mid}_{save_stamp()}.{suffix}"        
                    
                