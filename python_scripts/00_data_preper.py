import datetime
import logging
import warnings
import sys
from pathlib import Path

import pandas as pd
from html_table_generator import generate_html_table, main as get_language

# Get language from command line or user input
input_language = get_language()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("data_preper.log"), logging.StreamHandler()],
)
# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Get the current date in yyyymmdd format
DATE = datetime.datetime.now().strftime("%Y%m%d")

# Define paths
base_path = Path.home() / "Documents" / "sfdr_report_generator"
input_path = base_path / "excel_books"
output_path = base_path / "final_processed_data"
aladdin_data_path = input_path / "aladdin_data"
bbdd_file = input_path / "bbdd_sfdr_wip.xlsx"

# Create output directory if it doesn't exist
output_path.mkdir(parents=True, exist_ok=True)

# Read Auxiliary data to all the funds, the BBDD file
bbdd = pd.read_excel(bbdd_file)
bbdd.rename(
    columns={"aladdin_code": "security_description"}, inplace=True
)  # Rename column to match the other dataframes


# Read the Fund data from the Aladdin Data folder
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


# Process the Excel file  and generate HTML tables
def process_excel_file(file_path, language):
    logging.info(f"Processing excel fund file from {file_path}")
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
    # Delete any column with name == ISIN
    investment = investment.loc[:, investment.columns != "ISIN"]

    # Generate HTML tables without wrapper divs
    investment_html = generate_html_table(investment, "investment", language)
    sector_html = generate_html_table(sector, "sector", language)

    # Add the HTML strings as new columns to the main dataframe
    df["q03_t1"] = investment_html
    df["q04_t"] = sector_html

    logging.info("Single fund data file processed")
    return df


# Process all the excel files in the input folder
def process_all_excel_files(folder_path, language):
    logging.info(f"Processing all Excel files in {folder_path}")
    # Get all Excel files in the specified folder
    excel_files = list(folder_path.glob("*.xlsx"))

    # List to store DataFrames for each file
    dfs = []

    for file_path in excel_files:
        print(f"Processing file: {file_path}")
        df = process_excel_file(file_path, language)
        dfs.append(df)

    # Concatenate all DataFrames vertically
    final_df = pd.concat(dfs, ignore_index=True)

    # Merge with the BBDD file
    final_df = pd.merge(final_df, bbdd, on="security_description", how="left")

    logging.info("All funds files processed and merged.")
    return final_df


def round_numeric_columns(df):
    # Get all numeric columns
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns

    # Round all numeric columns to 2 decimal places
    for col in numeric_columns:
        df[col] = df[col].round(2)

    return df


# Process all Excel files and get the final DataFrame
result_df = process_all_excel_files(aladdin_data_path, input_language)

# Round all numeric values
result_df = round_numeric_columns(result_df)

logging.info(f"Updating value of certain columns and generating new columns")
# Multiply es_aligned, sust_invest, sust_invest_env,and sust_invest_soc columns by 100
columns_to_multiply = [
    "{{es_aligned}}",
    "{{sust_invest}}",
    "{{sust_invest_env}}",
    "{{sust_invest_soc}}",
]
result_df[columns_to_multiply] *= 100

# Calculate new columns
result_df["{{other_nones}}"] = 100 - result_df["{{es_aligned}}"]
result_df["{{other_non_sust}}"] = 100 - result_df["{{sust_invest}}"]

# Calculate 'rest_' columns
aligned_columns = ["capex", "opex", "turnover"]
for col in aligned_columns:
    result_df[f"rest_{col}_aligned"] = 100 - result_df[f"total_{col}_aligned"]
    result_df[f"rest_{col}_aligned_exsovereign"] = (
        100 - result_df[f"total_{col}_aligned_exsovereign"]
    )


def sort_columns(df):
    logging.info("Sorting columns in the final DataFrame.")
    # Define the first columns in the desired order
    first_columns = [
        "security_description",
        "narrative",
        "language",
        "{{product_name}}",
    ]

    # Get all column names
    all_columns = df.columns.tolist()

    # Separate columns with '{{' and without
    columns_with_braces = [
        col for col in all_columns if "{{" in col and col not in first_columns
    ]
    columns_without_braces = [
        col
        for col in all_columns
        if "{{" not in col
        and col not in first_columns
        and col not in ["q03_t1", "q04_t"]
    ]

    # Sort the separated columns
    columns_with_braces.sort()
    columns_without_braces.sort()

    # Combine all columns in the desired order
    final_column_order = (
        first_columns
        + columns_with_braces
        + columns_without_braces
        + ["q03_t1", "q04_t"]
    )

    # Reorder the dataframe
    df_sorted = df[final_column_order]

    return df_sorted


result_df = sort_columns(result_df)

# Save the final DataFrame to a new Excel file with the date in the filename
logging.info("Saving final processed data to Excel file.")
output_file = output_path / f"{DATE}_final_processed_data.xlsx"
result_df.to_excel(output_file, index=False)

# log results of script contains the processed data from all Excel files
logging.info("Processed data from all Excel files.")
logging.info(f"Final dataframe shape: {result_df.shape}")
logging.info(f"Final processed data saved to: {output_file}")
