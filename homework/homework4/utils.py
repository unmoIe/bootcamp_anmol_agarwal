from dotenv import load_dotenv
import os
import pandas as pd
import datetime as dt

load_dotenv()

def getApiKey():
    return( os.getenv("API_KEY") )

def validate_df( df, required_cols, dtypes_map ):
    msgs = {}
    missing = [ c for c in required_cols if c not in df.columns ]
    if missing:
        msgs['missing_cols'] = f"Missing columns: {missing}"
    for col, dtype in dtypes_map.items():
        if col in df.columns:
            try:
                if dtype == 'datetime64[ns]':
                    df[col] = pd.to_datetime(df[col])
                elif dtype == 'float64':
                    df[col] = pd.to_numeric(df[col])
                elif dtype == 'int64':
                    df[col] = pd.to_numeric(df[col])
            except Exception as e:
                msgs[f'dtype{col}'] = f"Failed to coerce {col} to {dtype}: {e}"
    na_counts = df.isna().sum().sum()
    msgs['na_total'] = f"Total NA values: {na_counts}"
    return msgs
                    
def save_stamp():
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")

def save_filename(prefix, meta):
    mid = "_".join([f"{k}-{str(v).replace(' ', '-').replace('/','|')[:100]}" for k, v in meta.items()])
    return f"{prefix}_{mid}_{save_stamp()}.csv"               
                    
                