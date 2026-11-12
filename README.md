# Shipping & Loading Data Reconciliation and Analytics

## Project Overview

This project consolidates and reconciles vessel loading records from three independent sources: Terminal Records, Shipping Agent Reports, and Broker Export.

Using Python and Pandas, the solution standardizes the datasets, converts quantities into Metric Tonnes (MT), identifies duplicate loading records, and separates records with missing or invalid information.

It also generates monthly loading reports and provides an interactive Streamlit dashboard for exploring loading activities and cargo volumes across different ports and products.

## Key Features

- **Data Integration:** Consolidates records from three independent CSV sources.
- **Data Standardization:** Normalizes column names, vessel information, loading dates, ports, and product descriptions.
- **Unit Conversion:** Standardizes reported quantities into Metric Tonnes.
- **Data Reconciliation:** Removes duplicates using IMO Number, Loading Date, and Loading Port, retaining records according to source reliability.
- **Data Quality Checks:** Identifies and separates invalid or incomplete records.
- **Reporting:** Generates monthly loading summaries by port and product.
- **Visualization:** Interactive Streamlit dashboard for exploring processed records and reports.
- **Testing:** pytest scripts for validating key data-processing functions.

## Technologies

Python | Pandas | NumPy | Streamlit | pytest | Matplotlib | Seaborn

## Project Structure

```text
uml_test/
├── data/
│   ├── input/
│   └── output/
├── src/
│   ├── loader.py
│   ├── standardization.py
│   ├── reconciliation.py
│   ├── reporting.py
│   ├── main.py
│   └── streamlit_app.py
└── requirements.txt
```

## Installation & Execution

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Add the three source CSV files to `data/input/`.**

**3. Run the data processing pipeline**

```bash
python -m src.main
```

**5. Launch the Streamlit dashboard**

```bash
streamlit run src/app.py
```

Open `http://localhost:8501` in your browser.

## Output

The pipeline generates:

- `clean_loadings.csv` – Reconciled loading records.
- `excluding_loadings.csv` – Duplicate and invalid records with exclusion reasons.
- `monthly_port_summary.csv` – Monthly loading quantities by port.
- `monthly_product_summary.csv` – Monthly loading quantities by product.
- `monthly_summary.csv` – Monthly loading quantities by port and product.

## Objective

To transform multiple shipping data sources into a consolidated, standardized, and reliable dataset for operational reporting and business analysis.