import datetime
import warnings
from pathlib import Path

import pandas as pd
from html_table_generator import generate_html_table

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

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


# Define the function to read the Fund Excel file and extract the tables
def read_excel_table(file_path, sheet_name="Sheet1", skiprows=3):
    # Read the entire Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)

    # Find the last valid row
    footer_indicators = ["Confidential", "Powered by"]
    last_valid_idx = None
    for idx, row in df.iterrows():
        if row.isna().all():
            last_valid_idx = idx
            break
        first_col_value = str(row.iloc[0])
        if any(indicator in first_col_value for indicator in footer_indicators):
            last_valid_idx = idx
            break

    # Slice the dataframe if we found a cutoff point
    if last_valid_idx is not None:
        df = df.iloc[:last_valid_idx]

    # Clean up any remaining NaN values
    df = df.dropna(how="all")

    return df


# Define the function to process the Excel file and Convert Sector and Investment tables to HTML
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
    # Delete any column with name == ISIN
    investment = investment.loc[:, investment.columns != "ISIN"]

    # Generate HTML tables without wrapper divs
    investment_html = generate_html_table(investment, "investment")
    sector_html = generate_html_table(sector, "sector")

    # Add the HTML strings as new columns to the main dataframe
    df["q03_t1"] = investment_html
    df["q04_t"] = sector_html

    return df


def process_all_excel_files(folder_path):
    # Get all Excel files in the specified folder
    excel_files = list(folder_path.glob("*.xlsx"))

    # List to store DataFrames for each file
    dfs = []

    for file_path in excel_files:
        print(f"Processing file: {file_path}")
        df = process_excel_file(file_path)
        dfs.append(df)

    # Concatenate all DataFrames vertically
    final_df = pd.concat(dfs, ignore_index=True)

    # Merge with the BBDD file
    final_df = pd.merge(final_df, bbdd, on="security_description", how="left")

    return final_df


# Process all Excel files and get the final DataFrame
result_df = process_all_excel_files(aladdin_data_path)

# Now result_df contains the processed data from all Excel files
print(result_df.shape)
print(result_df.columns)

# Get the current date in yyyymmdd format
current_date = datetime.datetime.now().strftime("%Y%m%d")

# Save the final DataFrame to a new Excel file with the date in the filename
output_file = output_path / f"{current_date}_final_processed_data.xlsx"
result_df.to_excel(output_file, index=False)

print(f"Final processed data saved to: {output_file}")
