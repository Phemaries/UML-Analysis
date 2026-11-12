
import pandas as pd
import re


def standardize_data(dfs):

    column_map = {
        'vessel': 'vessel_name',
        'ship': 'vessel_name',
        'imo-no': 'imo',
        'date-loaded': 'load_date',
        'loading_date': 'load_date',
        'load-port': 'load_port',
        'loadport': 'load_port',
        'port': 'load_port',
        'cargo': 'product',
        'grade': 'product',
        'quantity_t': 'quantity_mt',
        'qty-(000-t)': 'quantity_mt'
    }

    cleaned_dfs = []

    for name, df in dfs.items():

        temp_df = df.copy()

        temp_df.rename(columns=column_map, inplace=True)

        # Convert quantities to metric tonnes
        if name == 'agent_reports' and 'quantity_mt' in temp_df.columns:
            temp_df['quantity_mt'] = (
                pd.to_numeric(temp_df['quantity_mt'], errors='coerce') * 1000
            )

        elif 'quantity_mt' in temp_df.columns:
            temp_df['quantity_mt'] = pd.to_numeric(
                temp_df['quantity_mt'], errors='coerce'
            )

        # Standardize dates
        if 'load_date' in temp_df.columns:
            temp_df['load_date'] = pd.to_datetime(
                temp_df['load_date'], errors='coerce'
            )

        # Remove MT prefix from vessel names
        if 'vessel_name' in temp_df.columns:
            temp_df['vessel_name'] = temp_df['vessel_name'].apply(
                lambda x: re.sub(
                    r"^MT\s+", "", str(x).strip(), flags=re.I
                )
            )

        # Standardize text fields
        for col in ['vessel_name', 'load_port', 'product']:
            if col in temp_df.columns:
                temp_df[col] = (
                    temp_df[col].astype(str).str.strip().str.capitalize()
                )

        temp_df['data_source'] = name

        cleaned_dfs.append(temp_df)

    # Combine datasets
    combined_df = pd.concat(cleaned_dfs, ignore_index=True)

    # Standardize port names
    port_name = {
        'Lagos (apapa)': 'Lagos',
        'Takoradi port': 'Takoradi',
        'Lomé': 'Lome',
        'Lome togo': 'Lome',
        'Tema port': 'Tema'
    }

    combined_df['load_port'] = combined_df['load_port'].replace(port_name)

    # Standardize products
    prod_cor = {
        'Jet a1': 'Jet A1',
        'Jet a-1': 'Jet A1'
    }

    combined_df['product'] = combined_df['product'].replace(prod_cor)

    # Standardize source names
    source = {
        'terminal_records': 'Terminal',
        'agent_reports': 'Agent',
        'broker_export': 'Broker'
    }

    combined_df['data_source'] = combined_df['data_source'].replace(source)

    # Remove unwanted columns
    combined_df.drop(
        columns=['voyage_ref', 'notes'],
        errors='ignore',
        inplace=True
    )

    # Assign source priority
    source_priority = {
        'Terminal': 1,
        'Agent': 2,
        'Broker': 3
    }

    combined_df['priority'] = combined_df['data_source'].map(
        source_priority
    )

    # Sort by IMO, loading date and priority
    combined_df.sort_values(
        by=['imo', 'load_date', 'priority'],
        inplace=True
    )

    return combined_df
