
import pandas as pd
from pathlib import Path


def load_data():

    data_folder = Path.cwd().parent / "data" / "input"

    expected_sources = {
        "terminal_records",
        "agent_reports",
        "broker_export"
    }

    if not data_folder.is_dir():
        raise FileNotFoundError(
            f"Input directory not found: {data_folder}"
        )

    dfs = {
        file.stem: pd.read_csv(file)
        for file in data_folder.glob("*.csv")
    }

    missing_files = expected_sources - set(dfs.keys())

    if missing_files:
        raise FileNotFoundError(
            f"Missing required input files: {missing_files}"
        )

    unexpected_files = set(dfs.keys()) - expected_sources

    if unexpected_files:
        raise ValueError(
            f"Unexpected input files: {unexpected_files}"
        )

    for df in dfs.values():
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "-")
        )

    print("All three source files loaded successfully.")

    return dfs
