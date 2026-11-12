
import pandas as pd


def reconcile_loadings(combined_df):

    id_cols = ['imo', 'load_date', 'load_port']

    sorted_df = combined_df.sort_values(
        by=id_cols + ['priority'],
        ascending=True
    )

    # Identify duplicates
    removed_duplicates = sorted_df[
        sorted_df.duplicated(subset=id_cols, keep='first')
    ].copy()

    removed_duplicates['reason'] = 'Duplicated Loading Records'

    clean_df = combined_df.drop(
        removed_duplicates.index
    ).copy()

    # Invalid dates
    date_rd = clean_df[clean_df['load_date'].isna()].copy()

    date_rd['reason'] = 'Invalid Date or Empty Load Date'

    clean_df = clean_df.drop(date_rd.index)

    # Missing quantities
    qt_rd = clean_df[clean_df['quantity_mt'].isna()].copy()

    qt_rd['reason'] = 'Invalid Quantity or Quantity not reported'

    clean_df = clean_df.drop(qt_rd.index)

    # Missing IMO numbers
    im_rd = clean_df[clean_df['imo'].isna()].copy()

    im_rd['reason'] = 'IMO Numbers not reported'

    clean_df = clean_df.drop(im_rd.index)

    # Combine excluded records
    excluded_loadings = pd.concat(
        [removed_duplicates, date_rd, qt_rd, im_rd],
        ignore_index=True
    )

    # Standardize IMO data type
    excluded_loadings['imo'] = (
        excluded_loadings['imo'].astype('Int64').astype('string')
    )

    clean_df['imo'] = (
        clean_df['imo'].astype('Int64').astype('string')
    )

    clean_df.drop(columns=['priority'], inplace=True)

    return clean_df, excluded_loadings
