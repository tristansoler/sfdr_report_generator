import json
import logging
import os
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import plot_builder
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/report_builder.log"), logging.StreamHandler()],
)

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


# define a ticker function
def ticker(input_array: list) -> str:
    return "X" if np.any(np.nan_to_num(input_array) > 0) else ""


def ticker_opposite(input_array: list) -> str:
    return "X" if np.all(np.nan_to_num(input_array) == 0) else ""


# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Load translations
with open(os.path.join(script_dir, "translations.json"), "r", encoding="utf-8") as f:
    translations = json.load(f)

# Check if languge code is provided as a command-line argument
if len(sys.argv) > 1:
    input_language = sys.argv[1]

# ask input for language (es, en, pt, or  pl) assign to constant
else:
    try:
        input_language = input("Enter the language code (es, en, pt, or pl): ")
    except ValueError as e:
        print(e)
        logging.error(e)

# Validate the input langugage
if not isinstance(input_language, str) or input_language not in [
    "es",
    "en",
    "pt",
    "pl",
]:
    raise ValueError("Invalid language code. Please enter 'es', 'en', 'pt', or 'pl'.")

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# define date as yyyymmdd
date = datetime.now().strftime("%Y%m%d")

# Set up paths
excel_path = os.path.join(
    script_dir,
    "..",
    "final_processed_data",
    f"{date}_final_processed_data.xlsx",
)

template_dir = os.path.join(script_dir, "..", "narrative_templates")
output_dir = os.path.join(script_dir, "..", "final_reports")
plots_dir = os.path.join(output_dir, "plots")

# Create output directories
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# Read the Excel file
df = pd.read_excel(excel_path)
# Remove unwanted spaces from column names
df.columns = df.columns.str.strip()

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(template_dir))

# Generate a report for each row
for index, row in df.iterrows():
    # Determine the template file based on the 'narrative' column
    template_file = f"{row['narrative']}_narrative_template_{input_language}.html"

    # Check if the template file exists
    if not os.path.exists(os.path.join(template_dir, template_file)):
        print(f"Warning: Template file {template_file} not found. Skipping this row.")
        continue

    # Get the template
    template = env.get_template(template_file)

    # Generate the plot
    plot_filename = plot_builder.build_plot(
        row, plots_dir, index, translations, input_language
    )

    # Replace NaN in specific columns with an empty string for rendering
    row = row.replace({np.nan: ""})

    # Prepare data for the template
    data = {
        "product_name": row["{{product_name}}"],
        "lei_code": row["{{lei_code}}"],
        "sust_invest": row["{{sust_invest}}"],
        "esg_score_2022": row["{{esg_score_2022}}"],
        "esg_score_2023": row["{{esg_score_2023}}"],
        "esg_score_2024": row["{{esg_score_2024}}"],
        "es_aligned": row["{{es_aligned}}"],
        "sust_invest_env": row["{{sust_invest_env}}"],
        "sust_invest_soc": row["{{sust_invest_soc}}"],
        "other_nones": row["{{other_nones}}"],
        "ref_period": row["{{ref_period}}"],
        "other_non_sust": row["{{other_non_sust}}"],
        "taxonomy_2022": row["{{taxonomy_2022}}"],
        "taxonomy_2023": row["{{taxonomy_2023}}"],
        "total_turnover_enabling": row["total_turnover_enabling"],
        "total_turnover_transition": row["total_turnover_transition"],
        "total_turnover_aligned": row["total_turnover_aligned"],
        "total_capex_enabling": row["total_capex_enabling"],
        "total_capex_transition": row["total_capex_transition"],
        "total_opex_enabling": row["total_opex_enabling"],
        "total_opex_transition": row["total_opex_transition"],
    }

    # Render the template with the data
    html_content = template.render(data)

    # Use BeautifulSoup to modify the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Prep variables to tick the checkboxes of the report using the ticker function
    # in the future we will change this to a more complex function
    article_8 = ticker([1])
    article_9 = ticker([0])  # so it would be 0 or 1 depending on the narrative.

    total_turnover_nuclear = row["total_turnover_nuclear"]
    total_capex_nuclear = row["total_capex_nuclear"]
    total_opex_nuclear = row["total_opex_nuclear"]
    total_turnover_gas = row["total_turnover_gas"]
    total_capex_gas = row["total_capex_gas"]
    total_opex_gas = row["total_opex_gas"]

    sust_invest = row["{{sust_invest}}"]
    sust_invest_env = row["{{sust_invest_env}}"]
    sust_invest_soc = row["{{sust_invest_soc}}"]

    # Update the checkboxes in the report
    # Let's update article 9 Check boxes
    checkbox_art9_00 = soup.find(id="cb_art9_00")
    if checkbox_art9_00:
        checkbox_art9_00.string = article_9

    checkbox_art9_01 = soup.find(id="cb_art9_01")
    if checkbox_art9_01:
        checkbox_art9_01.string = ticker([0])
    checkbox_art9_02 = soup.find(id="cb_art9_02")
    if checkbox_art9_02:
        checkbox_art9_02.string = ticker([0])

    checkbox_art9_03 = soup.find(id="cb_art9_03")
    if checkbox_art9_03:
        checkbox_art9_03.string = ticker([0])

    checkbox_art9_04 = soup.find(id="cb_art9_04")
    if checkbox_art9_04:
        checkbox_art9_04.string = ticker([0])

    # Let's update article 8 Check boxes
    checkbox_art8_00 = soup.find(id="cb_art8_00")
    if checkbox_art8_00:
        checkbox_art8_00.string = article_8

    #   did promote environmental or social characteristics
    checkbox_art8_01 = soup.find(id="cb_art8_01")
    if checkbox_art8_01:
        checkbox_art8_01.string = ticker([sust_invest])

    #   did promote environmental characteristics
    checkbox_art8_02 = soup.find(id="cb_art8_02")
    if checkbox_art8_02:
        checkbox_art8_02.string = ticker([sust_invest_env])

    #   did promote social characteristics
    checkbox_art8_03 = soup.find(id="cb_art8_03")
    if checkbox_art8_03:
        checkbox_art8_03.string = ticker([sust_invest_soc])

    #   did promote environmental or social characteristics but made no sustainable investments
    checkbox_art8_04 = soup.find(id="cb_art8_04")
    if checkbox_art8_04:
        checkbox_art8_04.string = ticker_opposite([sust_invest])

    # Let's update checkboxes of the suquestion 1 of question 5 id q05sq01
    #   did invest in activities related to nuclear energy or fossil gas
    checkbox_q5_001 = soup.find(id="cb_q5_001")
    if checkbox_q5_001:
        checkbox_q5_001.string = ticker(
            [
                total_turnover_nuclear,
                total_capex_nuclear,
                total_opex_nuclear,
                total_turnover_gas,
                total_capex_gas,
                total_opex_gas,
            ]
        )

    #  did not invest in activities related to nuclear energy or fosil gas
    checkbox_q5_002 = soup.find(id="cb_q5_002")
    if checkbox_q5_002:
        checkbox_q5_002.string = ticker_opposite(
            [
                total_turnover_nuclear,
                total_capex_nuclear,
                total_opex_nuclear,
                total_turnover_gas,
                total_capex_gas,
                total_opex_gas,
            ]
        )

    #  yes, in fossil gas
    checkbox_q5_003 = soup.find(id="cb_q5_003")
    if checkbox_q5_003:
        checkbox_q5_003.string = ticker(
            [total_turnover_gas, total_capex_gas, total_opex_gas]
        )

    #  yes, in nuclear energy
    checkbox_q5_004 = soup.find(id="cb_q5_004")
    if checkbox_q5_004:
        checkbox_q5_004.string = ticker(
            [total_turnover_nuclear, total_capex_nuclear, total_opex_nuclear]
        )

    # Update top investments table: div with id "q03_t1"
    q03_t1_div = soup.find("div", id="q03_t1")
    if q03_t1_div and "q03_t1" in row:
        q03_t1_div.clear()
        q03_t1_div.append(BeautifulSoup(row["q03_t1"], "html.parser"))

    # Update sectorial distribution table: div with id "q04_t"
    q04_t_div = soup.find("div", id="q04_t")
    if q04_t_div and "q04_t" in row:
        q04_t_div.clear()
        q04_t_div.append(BeautifulSoup(row["q04_t"], "html.parser"))

    # Find the div with class "chart"
    chart_div = soup.find("div", class_="chart")
    if chart_div:
        # Find the img tag within the chart div
        img_tag = chart_div.find("img")

        if img_tag:
            # Update the src attribute with the new filename
            img_tag["src"] = f"plots/{plot_filename}"
        else:
            print("Image tag not found within the chart div")
    else:
        print("Chart div not found")

    # Get the modified HTML content
    modified_html_content = str(soup)

    # Generate filename
    filename = f"{datetime.now().strftime('%Y%m%d')}_{row['{{product_name}}'].replace(' ', '_').replace(',','')}_{input_language}.html"

    # Write the HTML file
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(modified_html_content)

print(f"Generated {len(df)} reports in the '{output_dir}' directory.")
