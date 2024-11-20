import logging
import os
import warnings
from datetime import datetime

import pandas as pd
import plot_builder
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("report_builder.log"), logging.StreamHandler()],
)

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


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
    template_file = f"{row['narrative']}_narrative_template.html"

    # Check if the template file exists
    if not os.path.exists(os.path.join(template_dir, template_file)):
        print(f"Warning: Template file {template_file} not found. Skipping this row.")
        continue

    # Get the template
    template = env.get_template(template_file)

    # Generate the plot
    plot_filename = plot_builder.build_plot(row, plots_dir, index)

    # Prepare data for the template
    data = {
        "product_name": row["{{product_name}}"],
        "lei_code": row["{{lei_code}}"],
        "sust_invest": row["{{sust_invest}}"],
        "esg_score_2023": row["{{esg_score_2023}}"],
        "esg_score_2024": row["{{esg_score_2024}}"],
        "es_aligned": row["{{es_aligned}}"],
        "sust_invest_env": row["{{sust_invest_env}}"],
        "sust_invest_soc": row["{{sust_invest_soc}}"],
        "other_nones": row["{{other_nones}}"],
        "ref_period": row["{{ref_period}}"],
        "other_non_sust": row["{{other_non_sust}}"],
        "plot_path": os.path.join("plots", plot_filename),  # Relative path to the plot
    }

    # Render the template with the data
    html_content = template.render(data)

    # Use BeautifulSoup to modify the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Update div with id "q03_t1"
    q03_t1_div = soup.find("div", id="q03_t1")
    if q03_t1_div and "q03_t1" in row:
        q03_t1_div.clear()
        q03_t1_div.append(BeautifulSoup(row["q03_t1"], "html.parser"))

    # Update div with id "q04_t"
    q04_t_div = soup.find("div", id="q04_t")
    if q04_t_div and "q04_t" in row:
        q04_t_div.clear()
        q04_t_div.append(BeautifulSoup(row["q04_t"], "html.parser"))

    # Get the modified HTML content
    modified_html_content = str(soup)

    # Generate filename
    filename = f"{row['{{product_name}}'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html"

    # Write the HTML file
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(modified_html_content)

print(f"Generated {len(df)} reports in the '{output_dir}' directory.")
