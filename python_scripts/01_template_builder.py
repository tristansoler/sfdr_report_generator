import logging
import os
import warnings

import pandas as pd
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("template_builder.log"), logging.StreamHandler()],
)

# add feature ask user for input excel sheet, i.e. language
# ask input for language (es, en, pt, or  pl) assign to constant
try:
    input_language = input("Enter the language code (es, en, pt, or pl): ")
    # validete input language is a string and is one of the four languages
    if not isinstance(input_language, str) or input_language not in [
        "es",
        "en",
        "pt",
        "pl",
    ]:
        raise ValueError(
            "Invalid language code. Please enter 'es', 'en', 'pt', or 'pl'."
        )
except ValueError as e:
    print(e)
    logging.error(e)

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Set the base directory
base_dir = r"C:\Users\n740789\Documents\sfdr_report_generator"

# Set the output directory
output_dir = os.path.join(base_dir, "narrative_templates")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Set the path for the Excel file
excel_file = os.path.join(base_dir, "excel_books", "narratives_tables.xlsx")

# Set the path for the HTML template
template_file = os.path.join(base_dir, "template.html")

# Load the Excel file and choose the sheet = input_languge
df = pd.read_excel(excel_file, sheet_name=input_language)

# Load the HTML template
with open(template_file, "r", encoding="utf-8") as file:
    template_content = file.read()

# List of the column names (after the first two columns)
column_names = [
    "main_heading_text",
    "product_name",
    "lei_code",
    "legal_text",
    "sfdr_last_rep_inv_sust_inv",
    "q01_a",
    "q01sq01_a",
    "q01sq02_a",
    "q01sq03_a",
    "q01sq04_a",
    "q01sq04sq01_a",
    "q01sq04sq02_a",
    "q02_a",
    "q03_a1",
    "q03_a2",
    "q04_a",
    "q04sq01_a",
    "q04sq02_a",
    "q05_a",
    "q05sq02_a",
    "q05sq03_a",
    "q06_a",
    "q07_a",
    "q08_a",
    "q09_a",
    "q10_a",
    "q10sq01_a",
    "q10sq02_a",
    "q10sq03_a",
    "q10sq04_a",
]

# Filter the df and select the rows with the narrative == sostenible_fi_eq & narrative == sostenible_fi
df = df.loc[
    (df["narrative"] == "sostenible_fi_eq") | (df["narrative"] == "sostenible_fi")
]

# Process each row of the filtered DataFrame
for index, row in df.iterrows():
    # Parse the HTML using BeautifulSoup (create a new soup for each iteration)
    soup = BeautifulSoup(template_content, "html.parser")

    # Loop through the column names and replace the content of the elements in the HTML
    for col in column_names:
        # Find the element by its id (which matches the column name)
        element = soup.find(id=col)

        if element:
            # Get the value from the DataFrame (handle NaN and non-string types)
            value = row[col]

            if pd.isna(value):
                value = ""  # Handle NaN values by inserting an empty string
            else:
                value = str(value)  # Ensure the value is converted to a string

            # Clear the existing content and insert the new content
            element.clear()  # Remove any existing content
            element.append(
                BeautifulSoup(value, "html.parser")
            )  # Insert the new content safely

    # Generate a unique filename for each row
    output_filename = f"{row['narrative']}_narrative_template.html"
    output_path = os.path.join(output_dir, output_filename)

    # Save the result to a new HTML file in the specified directory
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(str(soup))

    print(f"Generated HTML file: {output_path}")

print("All files have been generated.")