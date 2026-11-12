
import pandas as pd
from pathlib import Path


def generate_reports(cl_rd, excluded_loadings):

    output_folder = Path.cwd().parent / "data" / "output"

    output_folder.mkdir(parents=True, exist_ok=True)

    # Export cleaned dataset
    cl_rd.to_csv(
        output_folder / "clean_loadings.csv",
        index=False
    )

    # Export excluded dataset
    excluded_loadings.to_csv(
        output_folder / "excluding_loadings.csv",
        index=False
    )

    # Monthly reporting
    cl_rd['month'] = cl_rd['load_date'].dt.month
    cl_rd['month_name'] = cl_rd['load_date'].dt.month_name()

    # Monthly summary by port
    monthly_rep = cl_rd.groupby(
        ['load_port', 'month', 'month_name']
    )['quantity_mt'].sum().reset_index()

    monthly_rep = monthly_rep.sort_values(
        by=['load_port', 'month']
    )

    # Monthly summary by product
    monthly_prod = cl_rd.groupby(
        ['product', 'month', 'month_name']
    )['quantity_mt'].sum().reset_index()

    monthly_prod = monthly_prod.sort_values(
        by=['product', 'month']
    )

    # Monthly summary by port and product
    monthly_sum = cl_rd.groupby(
        ['load_port', 'product', 'month', 'month_name']
    )['quantity_mt'].sum().reset_index()

    monthly_sum = monthly_sum.sort_values(
        by=['load_port', 'product', 'month']
    )

    monthly_rep.to_csv(
        output_folder / "monthly_port_summary.csv",
        index=False
    )

    monthly_prod.to_csv(
        output_folder / "monthly_product_summary.csv",
        index=False
    )

    monthly_sum.to_csv(
        output_folder / "monthly_summary.csv",
        index=False
    )

    print("All reports generated successfully.")
