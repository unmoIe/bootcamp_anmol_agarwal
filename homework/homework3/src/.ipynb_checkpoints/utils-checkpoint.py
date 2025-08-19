def get_summary_stats( df, pivot, agg_col ):
    return( df.groupby(pivot)[agg_col].mean() )