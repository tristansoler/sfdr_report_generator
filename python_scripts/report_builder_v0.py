import os
from datetime import datetime

import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set up paths
excel_path = os.path.join(script_dir, "..", "excel_books", "art8_spashares10_data.xlsx")
template_dir = os.path.join(script_dir, "..", "narrative_templates")
template_file = "art8_spshares_10_narrative_template.html"
output_dir = os.path.join(script_dir, "..", "art8_final_reports")

# Read the Excel file
df = pd.read_excel(excel_path)

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(template_file)

# Generate a report for each row
for index, row in df.iterrows():
    # Prepare data for the template
    data = {
        "PRODUCT_NAME": row["{{PRODUCT_NAME}}"],
        "LEI_CODE": row["{{LEI_CODE}}"],
        "SFDR_LAST_REP_INV_SUST_INV": row["{{SFDR_LAST_REP_INV_SUST_INV}}"],
        "ESG_RATING_23": row["{{ESG_RATING_23}}"],
        "ESG_RATING_24": row["{{ESG_RATING_24}}"],
        "SFDR_LAST_REP_INV_WITH_ENV_SOC": row["{{SFDR_LAST_REP_INV_WITH_ENV_SOC}}"],
        "SFDR_LAST_REP_INV_SUST_ENV": row["{{SFDR_LAST_REP_INV_SUST_ENV}}"],
        "SFDR_LAST_REP_SUST_INV_SOC": row["{{SFDR_LAST_REP_SUST_INV_SOC}}"],
        "SHR_TRANS_ACTIVIT_TO": row["{{SHR_TRANS_ACTIVIT_TO}}"],
        "SHR_ENABL_ACTIVIT_TO": row[
            " {{SHR_ENABL_ACTIVIT_TO}}"
        ],  # Note the leading space
        "OTHERS": row[" {{OTHERS}}"],  # Note the leading space
        "YEAR": datetime.now().year,
        "YEAR_PREV": datetime.now().year - 1,
    }

    # Render the template with the data
    html_content = template.render(data)

    # Generate filename
    filename = f"{row['{{PRODUCT_NAME}}'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html"

    # Write the HTML file
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(html_content)

print(f"Generated {len(df)} reports in the '{output_dir}' directory.")
