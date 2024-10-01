import pandas as pd
from bs4 import BeautifulSoup
import os

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

# Load the Excel file
df = pd.read_excel(excel_file)

# Load the HTML template
with open(template_file, "r", encoding="utf-8") as file:
    template_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(template_content, 'html.parser')

# List of the column names (after the first two columns)
column_names = ['main_heading_text','product_name','lei_code','legal_text','sfdr_last_rep_inv_sust_inv','q01_a','q01sq01_a','q01sq02_a','q01sq03_a','q01sq04_a','q01sq04sq01_a',
                'q01sq04sq02_a','q02_a','q03_a1','q03_a2','q04_a','q04sq01_a','q04sq02_a','q05_a','q05sq02_a','q05sq03_a','q06_a','q07_a','q08_a','q09_a','q10_a','q10sq01_a','q10sq02_a','q10sq03_a','q10sq04_a']

# Process the first row of the Excel sheet (modify this for all rows if needed)
first_row = df.iloc[0]

# Loop through the column names and replace the content of the elements in the HTML
for col in column_names:
    # Find the element by its id (which matches the column name)
    element = soup.find(id=col)
    
    if element:
        # Get the value from the DataFrame (handle NaN and non-string types)
        value = first_row[col]
        
        if pd.isna(value):
            value = ""  # Handle NaN values by inserting an empty string
        else:
            value = str(value)  # Ensure the value is converted to a string
        
        # Clear the existing content and insert the new content
        element.clear()  # Remove any existing content
        element.append(BeautifulSoup(value, 'html.parser'))  # Insert the new content safely

# Save the result to a new HTML file in the specified directory
output_filename = f"{first_row['narrative']}_{first_row['narrative']}.html"
output_path = os.path.join(output_dir, output_filename)

with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write(str(soup))

print(f"Generated HTML file: {output_path}")