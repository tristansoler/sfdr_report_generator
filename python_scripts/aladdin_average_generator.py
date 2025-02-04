import pandas as pd
import numpy as np
import os
import logging
from typing import List, Dict, Tuple
import warnings
from openpyxl import load_workbook

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def set_up_dir(output_folder: str, input_folder: str) -> None:
    """Create the output folder if it doesn't exist.
    and Check if the input folder exists.
    """
    os.makedirs(output_folder, exist_ok=True)
    logging.info(f"Output folder created or already exists: {output_folder}")

    if not os.path.exists(input_folder):
        logging.error(f"The input folder '{input_folder}' does not exist.")
        raise FileNotFoundError(f"The input folder '{input_folder}' does not exist.")
    logging.info(f"Input folder exists: {input_folder}")


def group_files(input_folder: str) -> Dict[str, List[str]]:
    """Group files by the first 9 characters in their names."""
    all_files = [file for file in os.listdir(input_folder) if file.endswith(".xlsx")]
    file_groups = {}  # created dictionary to store the grouped files
    for file in all_files:
        prefix = file[:9]  # Extract the first 9 characters
        if prefix not in file_groups:
            file_groups[prefix] = []  # keys are first 9-char & vals are list of files
        file_groups[prefix].append(os.path.join(input_folder, file))
    logging.info(f"Grouped {len(all_files)} files into {len(file_groups)} groups")
    return file_groups


def process_post_contractual(files: List[str]) -> pd.DataFrame:
    """Process 'Post-Contractual Info Data' sheet efficiently."""
    if not files:
        raise ValueError("No files provided to process_post_contractual")

    values_list = []
    security_description = None
    for file in files:
        try:
            # Read data row
            df = pd.read_excel(
                file,
                sheet_name="Post-Contractual Info Data",
                header=None,
                skiprows=4,  # Skip header rows
                nrows=1,  # Read only the data row
            )

            # Store security description from the first file if not already stored
            if security_description is None:
                security_description = df.iloc[0, 0]

            # Convert percentage values and handle empty cells
            for col in df.columns:
                if df[col].dtype == object:  # If column contains strings/objects
                    df[col] = df[col].astype(str).str.rstrip("%").str.replace(",", "")
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            # Fill NaN values with 0
            df = df.fillna(0)

            # Store first column separately and convert rest to numeric
            first_col = df[0].values[0]  # Store security description
            numeric_values = df.iloc[:, 1:].values[0]  # Get only numeric columns

            values_list.append(numeric_values)

        except Exception as e:
            logging.error(f"Error processing file {file}: {str(e)}")

    if not values_list:
        raise ValueError("No valid data found in any of the files")

    # Calculate average values for numeric columns
    average_values = np.mean(values_list, axis=0)

    # Read the header from the first file
    header_df = pd.read_excel(
        files[0], sheet_name="Post-Contractual Info Data", header=None, nrows=4
    )

    # Create result DataFrame
    result_df = pd.DataFrame(columns=header_df.columns)
    result_df.loc[3] = header_df.loc[3]  # Add headers

    # Add the averaged values, keeping first column empty for security description
    result_df.loc[4, 0] = security_description  # add security description
    result_df.loc[4, 1:] = average_values  # Add averaged values for numeric columns

    logging.info(f"Processed 'Post-Contractual Info Data' for {len(files)} files")
    return result_df


def process_sectorial_distribution(files: List[str]) -> pd.DataFrame:
    """Process 'Sectorial Distribution' sheet more efficiently."""
    df_list = []
    for file in files:
        try:
            # Read only columns B and C (indices 1 and 2), starting from row 6
            df = pd.read_excel(
                file,
                sheet_name="Sectorial Distribution",
                header=None,
                usecols=[1, 2],  # Read only columns B and C
                skiprows=5,  # Skip the first 5 rows (start from row 6)
            )

            if df.empty:
                logging.warning(f"Empty 'Sectorial Distribution' sheet in file: {file}")
                continue

            # Rename columns for clarity
            df.columns = ["Sector", "Market Value %"]

            # Convert percentage strings to numeric values
            df["Market Value %"] = (
                pd.to_numeric(
                    df["Market Value %"].astype(str).str.rstrip("%"), errors="coerce"
                )
                / 100.0
            )

            # Remove any rows where sector is missing
            df = df.dropna(subset=["Sector"])

            # Sum percentages for each sector within the file
            df = df.groupby("Sector")["Market Value %"].sum().reset_index()

            df_list.append(df)

        except Exception as e:
            logging.error(f"Error processing file {file}: {str(e)}")

    if not df_list:
        return pd.DataFrame()

    # Combine all dataframes
    combined_df = pd.concat(df_list, ignore_index=True)

    # Calculate weighted average of percentages across files
    result_df = combined_df.groupby("Sector")["Market Value %"].mean().reset_index()

    # Normalize percentages to ensure they sum to 100%
    total = result_df["Market Value %"].sum()
    result_df["Market Value %"] = result_df["Market Value %"] / total

    # Rename columns and set index
    result_df.columns = ["Sectors", "% Assets"]
    result_df.set_index("Sectors", inplace=True)

    # Sort by percentage in descending order
    result_df = result_df.sort_values("% Assets", ascending=False)

    # Format percentages with high precision
    result_df["% Assets"] = result_df["% Assets"].map("{:.1%}".format)

    return result_df


def process_top_investments(files: List[str]) -> pd.DataFrame:
    """Process 'Top Investments' sheet with normalized averages."""
    df_list = []
    for file in files:
        try:
            # Read the Top Investments sheet, skipping the header rows
            df = pd.read_excel(
                file,
                sheet_name="Top Investments",
                header=None,
                skiprows=4,  # Skip the first 4 rows to get to the data
            )

            if df.empty:
                logging.warning(f"Empty 'Top Investments' sheet in file: {file}")
                continue

            # Rename columns based on the structure
            df.columns = [
                "ISIN",
                "Largest Investments",
                "Sector",
                "% Assets",
                "Country Name",
            ]

            # Convert percentage strings to numeric values with high precision
            df["% Assets"] = (
                pd.to_numeric(
                    df["% Assets"].astype(str).str.rstrip("%"), errors="coerce"
                )
                / 100.0
            )

            # swap nan for "cash" in column ISIN and "others" in column Sector
            df["ISIN"] = df["ISIN"].fillna("Cash")
            df["Sector"] = df["Sector"].fillna("Others")

            # Remove any rows where essential data is missing
            df = df.dropna(subset=["Largest Investments"])

            df_list.append(df)

        except Exception as e:
            logging.error(f"Error processing file {file}: {str(e)}")

    if not df_list:
        return pd.DataFrame()

    # Combine all dataframes
    combined_df = pd.concat(df_list, ignore_index=True)

    # Group by ISIN and calculate mean percentage while keeping other information
    result_df = (
        combined_df.groupby("ISIN")
        .agg(
            {
                "Largest Investments": "first",
                "Sector": "first",
                "% Assets": "mean",
                "Country Name": "first",
            }
        )
        .reset_index()
    )

    # Normalize percentages to ensure they sum to 100%
    # total = result_df["% Assets"].sum()
    # result_df["% Assets"] = result_df["% Assets"] / total

    # Sort by percentage in descending order
    result_df = result_df.sort_values("% Assets", ascending=False)

    # Format percentages with high precision
    result_df["% Assets"] = result_df["% Assets"].map("{:.9%}".format)

    # return only first 15 rows
    # result_df = result_df.head(15)

    return result_df


def save_results(
    output_file: str,
    post_contractual: pd.DataFrame,
    sectorial: pd.DataFrame,
    top_investments: pd.DataFrame,
    template_file: str,
) -> None:
    """Save results to a new Excel file."""
    try:
        with pd.ExcelWriter(output_file) as writer:
            post_contractual.to_excel(
                writer,
                sheet_name="Post-Contractual Info Data",
                index=False,
                header=False,
            )
            sectorial.to_excel(writer, sheet_name="Sectorial Distribution", index=True)
            top_investments.to_excel(writer, sheet_name="Top Investments", index=False)

            # Copy other sheets from the template file
            template_sheets = pd.ExcelFile(template_file).sheet_names
            for sheet_name in template_sheets:
                if sheet_name not in [
                    "Post-Contractual Info Data",
                    "Sectorial Distribution",
                    "Top Investments",
                ]:
                    df_other_sheet = pd.read_excel(template_file, sheet_name=sheet_name)
                    df_other_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

        logging.info(f"Results saved to: {output_file}")
    except Exception as e:
        logging.error(f"Error saving results to {output_file}: {e}")


def process_group(files: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Process a group of files and return the resulting DataFrames."""
    logging.info(f"Processing group of files")

    post_contractual = process_post_contractual(files)
    sectorial = process_sectorial_distribution(files)
    top_investments = process_top_investments(files)

    return post_contractual, sectorial, top_investments


def main():
    # Define input and output folders
    input_folder = "excel_books/aladdin_data/aladdin_input"
    output_folder = "excel_books/aladdin_data/aladdin_data_processed"

    try:
        # Create output folder and check input folder
        set_up_dir(output_folder, input_folder)

        # Group files by prefix
        file_groups = group_files(input_folder)

        results = {}  # Store results for each group
        # Process each group of files
        for prefix, files in file_groups.items():
            logging.info(f"Processing group with prefix: {prefix}")

            prefix = prefix.strip()  # Remove any leading/trailing spaces
            # Process each sheet type
            post_contractual, sectorial, top_investments = process_group(files)

            # Save results to a new Excel file
            output_file = os.path.join(output_folder, f"average_output_{prefix}.xlsx")
            save_results(
                output_file, post_contractual, sectorial, top_investments, files[0]
            )

            # Store results in a dictionary
            results[prefix] = (post_contractual, sectorial, top_investments)

        logging.info("Processing complete.")
        return results

    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        # add more detailed error information
        import traceback

        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()

# Example usage:
main()
