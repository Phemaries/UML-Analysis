
import streamlit as st
import pandas as pd
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Shipping & Loading Analytics",
    layout="wide"
)


# Define output directory
output_folder = Path(__file__).resolve().parent.parent / "data" / "output"


# Load datasets
@st.cache_data
def load_reports():

    clean_df = pd.read_csv(
        output_folder / "clean_loadings.csv",
        parse_dates=['load_date']
    )

    excluded_df = pd.read_csv(
        output_folder / "excluding_loadings.csv"
    )

    return clean_df, excluded_df


# Check whether reports exist
if not (output_folder / "clean_loadings.csv").exists():

    st.error("Clean loading records not found. Run main.py first.")
    st.stop()


# Load data
cl_rd, excluded_loadings = load_reports()


# Dashboard title
st.title("🚢 Shipping & Loading Analytics")

st.caption(
    "Analysis of vessel loading activities, cargo quantities "
    "and port performance."
)


# Sidebar filters
st.sidebar.header("Dashboard Filters")

ports = sorted(cl_rd['load_port'].dropna().unique())

products = sorted(cl_rd['product'].dropna().unique())

selected_ports = st.sidebar.multiselect(
    "Select Loading Port",
    ports,
    default=ports
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    products,
    default=products
)


# Apply filters
filtered_df = cl_rd[
    cl_rd['load_port'].isin(selected_ports) &
    cl_rd['product'].isin(selected_products)
].copy()


if filtered_df.empty:

    st.warning("No records found for the selected filters.")
    st.stop()


# KPI calculations
total_loadings = len(filtered_df)

total_quantity = filtered_df['quantity_mt'].sum()

total_vessels = filtered_df['vessel_name'].nunique()

total_ports = filtered_df['load_port'].nunique()


# Display KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Loadings",
    f"{total_loadings:,}"
)

col2.metric(
    "Total Quantity (MT)",
    f"{total_quantity:,.0f}"
)

col3.metric(
    "Unique Vessels",
    f"{total_vessels:,}"
)

col4.metric(
    "Loading Ports",
    f"{total_ports:,}"
)


st.divider()


# Monthly loading analysis
st.subheader("Monthly Loading Performance")

filtered_df['month'] = filtered_df['load_date'].dt.month

filtered_df['month_name'] = (
    filtered_df['load_date'].dt.month_name()
)

monthly_data = filtered_df.groupby(
    ['month', 'month_name']
)['quantity_mt'].sum().reset_index()

monthly_data = monthly_data.sort_values('month')

st.bar_chart(
    monthly_data.set_index('month_name')['quantity_mt'],
    y_label="Quantity (MT)",
    x_label="Month",
    color=["#25C900"]
)


# Port and product analysis
col1, col2 = st.columns(2)

with col1:

    st.subheader("Loading Quantity by Port")

    port_data = filtered_df.groupby(
        'load_port'
    )['quantity_mt'].sum().sort_values(ascending=False)

    st.bar_chart(port_data, color=["#C90079"])


with col2:

    st.subheader("Loading Quantity by Product")

    product_data = filtered_df.groupby(
        'product'
    )['quantity_mt'].sum().sort_values(ascending=False)

    st.bar_chart(product_data)


st.divider()


# Detailed loading records
st.subheader("Loading Records")

st.metric(
    "Total Loading Records",
    f"{len(cl_rd):,}"
)

st.dataframe(
    filtered_df.sort_values(
        by='load_date',
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# Excluded records
st.subheader("Excluded Loading Records")

st.metric(
    "Total Excluded Records",
    f"{len(excluded_loadings):,}"
)

st.dataframe(
    excluded_loadings,
    use_container_width=True,
    hide_index=True
)


# Download cleaned records
st.download_button(
    label="Download Filtered Loading Records",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_loadings.csv",
    mime="text/csv"
)
