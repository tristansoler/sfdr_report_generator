# %%
import warnings

import pandas as pd
from html_table_generator import generate_html_table

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def read_excel_table(file_path, sheet_name="Sheet1", skiprows=3):
    # First, read the entire Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)

    # Find the last valid row by looking for the first row where all values are NaN
    # or where the first column contains specific footer text indicators
    footer_indicators = ["Confidential", "Powered by"]

    last_valid_idx = None
    for idx, row in df.iterrows():
        # Check if all values in the row are NaN
        if row.isna().all():
            last_valid_idx = idx
            break

        # Check if the first column contains any footer indicators
        first_col_value = str(row.iloc[0])
        if any(indicator in first_col_value for indicator in footer_indicators):
            last_valid_idx = idx
            break

    # If we found a cutoff point, slice the dataframe
    if last_valid_idx is not None:
        df = df.iloc[:last_valid_idx]

    # Clean up any remaining NaN values
    df = df.dropna(how="all")

    return df


def process_excel_file(file_path):
    # Read the main dataframe and the two tables
    df = read_excel_table(
        file_path, sheet_name="Post-Contractual Info Data", skiprows=3
    )
    sector = read_excel_table(
        file_path, sheet_name="Sectorial Distribution", skiprows=3
    )
    investment = read_excel_table(file_path, sheet_name="Top Investments", skiprows=3)

    # Keep only the first 16 rows of investment table
    investment = investment.head(16)

    # Generate HTML tables without wrapper divs
    investment_html = generate_html_table(investment, "investment")
    sector_html = generate_html_table(sector, "sector")

    # Add the HTML strings as new columns to the main dataframe
    df["q03_t1"] = investment_html
    df["q04_t"] = sector_html

    return df


file_path = r"C:\Users\n740789\Documents\sfdr_report_generator\excel_books\aladdin_data\FIG05240 04-11-2024 Post-contractual Info.xlsx"
result_df = process_excel_file(file_path)
