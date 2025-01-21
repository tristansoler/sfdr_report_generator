import datetime
import logging
import warnings
import sys
from pathlib import Path

import pandas as pd
from html_table_generator import generate_html_table, main as get_language
from aladdin_average_generator import main as process_aladdin_data

# Get language from command line or user input
input_language = get_language()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/data_preper.log"), logging.StreamHandler()],
)
# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Get the current date in yyyymmdd format
DATE = datetime.datetime.now().strftime("%Y%m%d")

# Define paths
base_path = Path.home() / "Documents" / "sfdr_report_generator"
input_path = base_path / "excel_books"
output_path = base_path / "final_processed_data"
aladdin_processed_path = input_path / "aladdin_data" / "aladdin_data_processed"
bbdd_file = input_path / "bbdd_sfdr_wip.xlsx"

# Create output directory if it doesn't exist
output_path.mkdir(parents=True, exist_ok=True)

# Read Auxiliary data to all the funds, the BBDD file
bbdd = pd.read_excel(bbdd_file)
bbdd.rename(
    columns={"aladdin_code": "security_description"}, inplace=True
)  # Rename column to match the other dataframes


# Define function to process the Aladdin data averaged and generate HTML tables
def read_processed_aladdin_files():
    """Read all processed Aladdin files from the processed directory"""
    logging.info(f"Reading processed Aladdin files from {aladdin_processed_path}")

    all_data = []
    processed_files = list(aladdin_processed_path.glob("average_output_*.xlsx"))

    if not processed_files:
        logging.error(f"No processed files found in {aladdin_processed_path}")
        return None

    for file_path in processed_files:
        try:
            logging.info(f"Processing file: {file_path}")
            # Read the Post-Contractual Info Data sheet
            df = pd.read_excel(
                file_path, sheet_name="Post-Contractual Info Data", header=None
            )
            # Check if the DataFrame has at least 5 rows
            if df.shape[0] < 2:
                logging.error(f"File {file_path} has fewer than 2 rows. Skipping.")
                continue

            # Get the header row (row 4, index 3)
            headers = df.iloc[0]

            # Get the data row (row 2, index 4)
            data = df.iloc[1]

            # Create a new DataFrame with proper headers
            processed_df = pd.DataFrame([data.values], columns=headers)

            # Debug log
            logging.info(f"Processing {file_path.name}")

            # Convert numeric columns
            numeric_columns = [
                "{{es_aligned}}",
                "{{sust_invest}}",
                "{{sust_invest_env}}",
                "{{sust_invest_soc}}",
            ]

            for col in numeric_columns:
                if col in processed_df.columns:
                    processed_df[col] = pd.to_numeric(
                        processed_df[col], errors="coerce"
                    )

            # Generate HTML tables
            sector_df = pd.read_excel(file_path, sheet_name="Sectorial Distribution")
            investment_df = pd.read_excel(file_path, sheet_name="Top Investments")

            # Convert float columns to string with one decimal place before passing to generate_html_table
            for df in [sector_df, investment_df]:
                numeric_cols = df.select_dtypes(include=["float64"]).columns
                for col in numeric_cols:
                    df[col] = df[col].apply(
                        lambda x: f"{float(x):.1f}" if pd.notnull(x) else ""
                    )

            processed_df["q03_t1"] = generate_html_table(
                investment_df, "investment", input_language
            )
            processed_df["q04_t"] = generate_html_table(
                sector_df, "sector", input_language
            )

            all_data.append(processed_df)

        except Exception as e:
            logging.error(f"Error processing file {file_path}: {str(e)}")
            logging.error("Full traceback:", exc_info=True)
            continue

    if not all_data:
        return None

    # Combine all processed data
    final_df = pd.concat(all_data, ignore_index=True)
    logging.info(f"Combined {len(all_data)} processed files")

    return final_df


def round_numeric_columns(df):
    # Get all numeric columns
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns

    # Round all numeric columns to 2 decimal places
    for col in numeric_columns:
        df[col] = df[col].round(2)

    return df


def transform_esg_score(average_score: float) -> str:
    """Transform the average ESG score based on defined conditions."""
    logging.debug(f"Transforming score: {average_score}")
    average_score = float(average_score)
    try:
        if average_score > 80:
            return "A+"
        elif 65 < average_score <= 80:
            return "A"
        elif 55 < average_score <= 65:
            return "A-"
        else:
            return "B"  # Assign a default grade for scores <= 55
    except Exception as e:
        logging.error(f"Error transforming ESG score: {str(e)}")
        return "B"  # Assign a default grade for any errors


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


if __name__ == "__main__":
    # First, run the aladdin_average_generator script
    logging.info("Running aladdin_average_generator...")
    try:
        aladdin_results = process_aladdin_data()
        if aladdin_results is None:
            logging.error("Failed to process Aladdin data. Exiting.")
            sys.exit(1)
        logging.info("Aladdin average generation completed successfully.")
    except Exception as e:
        logging.error(f"Error running aladdin_average_generator: {str(e)}")
        logging.error("Full traceback:", exc_info=True)
        sys.exit(1)

    # Read the processed Aladdin files
    result_df = read_processed_aladdin_files()

    if result_df is not None:
        # Read and merge BBDD file
        bbdd = pd.read_excel(bbdd_file)
        bbdd.rename(columns={"aladdin_code": "security_description"}, inplace=True)
        result_df = pd.merge(result_df, bbdd, on="security_description", how="left")

        # Multiply percentage columns by 100
        columns_to_multiply = [
            "{{es_aligned}}",
            "{{sust_invest}}",
            "{{sust_invest_env}}",
            "{{sust_invest_soc}}",
        ]
        result_df[columns_to_multiply] *= 100

        # Calculate new columns
        result_df["{{other_nones}}"] = 100 - result_df["{{es_aligned}}"]
        result_df["{{other_non_sust}}"] = (
            result_df["{{es_aligned}}"] - result_df["{{sust_invest}}"]
        )

        # Calculate 'rest_' columns
        aligned_columns = ["capex", "opex", "turnover"]
        for col in aligned_columns:
            result_df[f"rest_{col}_aligned"] = 100 - result_df[f"total_{col}_aligned"]
            result_df[f"rest_{col}_aligned_exsovereign"] = (
                100 - result_df[f"total_{col}_aligned_exsovereign"]
            )

        # transform esg_score_2024 using transform_esg_score()
        result_df["{{esg_score_2024}}"] = result_df["{{esg_score_2024}}"].apply(
            transform_esg_score
        )

        # Round numeric values
        result_df = round_numeric_columns(result_df)

        # Sort columns
        result_df = sort_columns(result_df)

        # Save the final DataFrame
        output_file = output_path / f"{DATE}_final_processed_data.xlsx"
        result_df.to_excel(output_file, index=False)

        logging.info(f"Final processed data saved to: {output_file}")
    else:
        logging.error("Failed to process Excel files")
