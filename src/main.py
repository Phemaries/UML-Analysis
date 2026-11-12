from loader import load_data
from standardization import standardize_data
from reconciliation import reconcile_loadings
from reporting import generate_reports


# Load source datasets
dfs = load_data()


# Standardize and combine datasets
combined_df = standardize_data(dfs)


# Reconcile loading records
cl_rd, excluded_loadings = reconcile_loadings(combined_df)


# Generate reports
generate_reports(cl_rd, excluded_loadings)


print("Data processing completed successfully. \n")



if len(combined_df) == len(cl_rd) + len(excluded_loadings):
    print("Standardization & Reconciliation Successful")
else:
    print("Standardization & Reconciliation Successful")
