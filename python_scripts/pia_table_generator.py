import json
import logging
import os
import sys
from pathlib import Path
import re
from datetime import datetime

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# set logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# get DATE in format YYYYMMDD
DATE = datetime.now().strftime("%Y%m%d")


# define function to create dict that maps report names to report codes
def get_mapping():
    logging.info("Getting mapping dict...")
    try:
        mapping_df = pd.read_excel(
            r"C:\Users\n740789\Documents\sfdr_report_generator\excel_books\bbdd_sfdr_wip.xlsx",
            usecols=["aladdin_code", "{{product_name}}"],
            engine="openpyxl",
        )

        mapping_df.aladdin_code = mapping_df.aladdin_code.str.strip().str.upper()
        mapping_df["{{product_name}}"] = (
            mapping_df["{{product_name}}"].str.strip().str.replace(" ", "_")
        )

        # Convert the DataFrame to a reversed dictionary
        mapping_dict = mapping_df.set_index("{{product_name}}").to_dict()[
            "aladdin_code"
        ]
        return mapping_dict
    except Exception as e:
        logging.error(f"Failed to get mapping dict: {e}")
        exit(1)


# Format percentage values
def process_percentage(value):
    if pd.isna(value):  # Handle NaN or None
        return np.nan
    try:
        # Ensure the value is treated as a string
        value_str = str(value).strip("%")
        numeric_value = float(value_str)

        # Return as integer if the value is exactly zero
        if numeric_value == 0.0:
            return int(numeric_value)
        else:
            return numeric_value

    except ValueError:  # Catch conversion errors (e.g., invalid strings)
        return value


# define function to generate html table from excel file
def generate_html_table(excel_path: str):

    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
        # replace "-" with "" in df["Unidades de medida"]
        df["Unidades de medida"] = (
            df["Unidades de medida"].str.strip().str.replace("-", "")
        )
        # drop rows with NaN in 'Métrica' column
        df = df.dropna(subset=["Métrica"])
        # value
        # format column "Métrica" to have only two decimal places using f-string
        df["Métrica"] = df["Métrica"].apply(lambda x: f"{x:.1f}")
        # format column "% Cobertura" with process_percentage function
        df["% Cobertura"] = (
            df["% Cobertura"]
            .apply(process_percentage)
            .apply(lambda x: "0%" if float(x) == 0 else f"{x*100:.2f}%")
        )
        # create new column "Métrica" with the values of the column "Métrica" and "Unidades de medida"
        df["Métrica"] = df["Métrica"] + " " + df["Unidades de medida"]
        df["Métrica"] = df["Métrica"].str.replace(" %", "%")

        df_filtered = df[["Indicadores", "Métrica", "% Cobertura"]].copy()
        # rename "% Cobertura" column to "Cobertura"
        df_filtered.rename(columns={"% Cobertura": "Cobertura"}, inplace=True)

        if df.empty:
            logging.warning(f"Excel file is empty: {excel_path}")
            return ""

        # Generate the initial HTML table
        html_str = df_filtered.to_html(classes="dataframe", index=False, escape=False)

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_str, "html.parser")

        # Define column structure based on table type
        colgroup = """
                    <colgroup>
                      <col class="col1" />
                      <col class="col2" /> 
                      <col class="col3" /> 
                    </colgroup>
            """
        # Create the table structure without the wrapper div
        new_table = f"""
            <table>
                {colgroup}
                <thead>
                    <tr>
                        {"".join(f"<th>{col}</th>" for col in df_filtered.columns)}
                    </tr>
                </thead>
                {str(soup.find("tbody"))}
            </table>
        """

        return new_table
    except Exception as e:
        logging.error(f"Error generating HTML table: {e}")
        return ""


# define funciton to insert html table into
def insert_html_table(html_path: str, html_table: str):
    """
    Inserts an HTML table inside the <div> with id="q02_t1" or creates it if missing.
    """
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Locate the target div by id
        target_div = soup.find("div", id="q02_t1")
        if not target_div:
            # Create the div if it does not exist
            logging.warning(
                f"Target div 'q02_t1' not found in {html_path}. Creating it."
            )
            target_div = soup.new_tag("div", id="q02_t1", class_="table-body")
            marker = soup.find(string="<!--Question 3-->")
            if marker:
                marker.insert_before(target_div)
            else:
                logging.error(f"Marker '<!--Question 3-->' not found in {html_path}.")
                return

        # Insert the HTML table inside the target div
        table_soup = BeautifulSoup(html_table, "html.parser")
        target_div.clear()  # Clear any existing content in the div
        target_div.append(table_soup)

        # Save the updated HTML file
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        logging.info(f"Successfully inserted table into {html_path}")
    except Exception as e:
        logging.error(f"Failed to insert table into {html_path}: {e}")


# define function to get file name
def extract_report_name(file_path):
    """Extracts the report name from a given file path using regex."""
    file_name = file_path.name  # Get the file name
    match = re.match(rf"{DATE}_(.+?)_pt\.html", file_name)
    if match:
        report_name = match.group(1)  # Extract the content inside the parentheses
        logging.debug(f"Extracted report name: {report_name}")
        return report_name
    logging.warning(f"Invalid file name format: {file_name}")
    return None


def main():
    logging.info("Starting report generation...")
    mapping_dict = get_mapping()

    for file in Path(
        r"C:\Users\n740789\Documents\sfdr_report_generator\final_reports"
    ).rglob("*.html"):
        # get report name
        report_name = extract_report_name(file)
        if not report_name:
            logging.warning(f"Skipping file with invalid name: {file}")
            continue

        # get product code
        product_code = mapping_dict.get(report_name)
        if not product_code:
            logging.warning(f"Product code not found for report: {report_name}")
            continue

        # get target excel file
        target_excel = Path(
            rf"C:\Users\n740789\Documents\sfdr_report_generator\excel_books\pt_tables_input\{product_code}_PIAS_311224.xlsx"
        )
        if not target_excel.exists():
            logging.error(f"Excel file not found: {target_excel}")
            continue
        # try generate table
        try:
            html_table = generate_html_table(target_excel)
            if not html_table:
                logging.warning(f"Failed to generate HTML table for: {target_excel}")
                continue
            insert_html_table(file, html_table)
            logging.info(f"Successfully updated: {file}")
        except Exception as e:
            logging.error(f"Failed to update {file}: {e}")

    logging.info("Report generation completed.")


if __name__ == "__main__":
    main()
